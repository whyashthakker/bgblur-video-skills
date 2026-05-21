#!/usr/bin/env python3
"""
Video metadata probe for FFmpeg prep workflows.
Usage: python3 scripts/video_probe.py "input.mp4" [--check-metadata]
Requires: ffprobe (ffmpeg)
"""
import argparse
import json
import shutil
import subprocess
import sys


def run_ffprobe(path: str) -> dict | None:
    if not shutil.which("ffprobe"):
        print("error: ffprobe not found. Install ffmpeg.")
        sys.exit(1)
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", "-show_streams", path,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"error: ffprobe failed — {e}")
        return None


def format_size(size_bytes: str | int | float) -> str:
    size = float(size_bytes)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def parse_fps(rate: str) -> float | None:
    if not rate or rate == "0/0":
        return None
    if "/" in rate:
        num, den = rate.split("/")
        return float(num) / float(den) if float(den) else None
    return float(rate)


def main():
    parser = argparse.ArgumentParser(description="Probe video before FFmpeg prep")
    parser.add_argument("path", help="Path to video file")
    parser.add_argument("--check-metadata", action="store_true")
    args = parser.parse_args()

    data = run_ffprobe(args.path)
    if not data:
        sys.exit(1)

    fmt = data.get("format", {})
    streams = data.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio = next((s for s in streams if s.get("codec_type") == "audio"), {})

    duration = float(fmt.get("duration", 0))
    size = int(fmt.get("size", 0))
    width = video.get("width", 0)
    height = video.get("height", 0)
    fps = parse_fps(video.get("r_frame_rate", ""))
    codec = video.get("codec_name", "unknown")
    fmt_name = fmt.get("format_name", "unknown")

    print(f"=== Video Probe: {args.path} ===")
    print()
    print(f"container: {fmt_name}")
    print(f"duration: {duration:.1f}s ({duration / 60:.1f} min)")
    print(f"size: {format_size(size)}")
    print(f"resolution: {width}x{height}")
    print(f"video_codec: {codec}")
    print(f"fps: {fps:.2f}" if fps else "fps: unknown")
    print(f"audio: {'yes (' + audio.get('codec_name', '?') + ')' if audio else 'no'}")
    print()

    print("## Prep Recommendations")
    if codec not in ("h264", "hevc"):
        print(f"- re-encode: {codec} → h264 for best BGBlur compatibility")
    if fmt_name and "mp4" not in fmt_name and "mov" not in fmt_name:
        print("- convert container to MP4")
    if size > 200 * 1024 * 1024:
        print("- compress: file exceeds 200MB free tier limit")
    if duration > 600:
        print("- trim: duration exceeds 10 min free tier limit")
    if fps and fps > 60:
        print(f"- normalize fps: {fps:.0f}fps is high; target 30fps")
    if video.get("side_data_list"):
        print("- check rotation: side_data present — may need transpose filter")
    print()

    if args.check_metadata:
        tags = fmt.get("tags", {})
        stream_tags = video.get("tags", {})
        all_tags = {**tags, **stream_tags}
        print("## Metadata")
        if all_tags:
            for k, v in all_tags.items():
                print(f"  {k}: {v}")
            print("action: strip with -map_metadata -1")
        else:
            print("  clean — no embedded tags")
        print()

    print("=== Probe Complete ===")


if __name__ == "__main__":
    main()
