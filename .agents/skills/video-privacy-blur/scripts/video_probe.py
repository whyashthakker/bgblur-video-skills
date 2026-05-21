#!/usr/bin/env python3
"""
Video metadata probe for privacy blur workflows.
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


def main():
    parser = argparse.ArgumentParser(description="Probe video metadata for privacy workflows")
    parser.add_argument("path", help="Path to video file")
    parser.add_argument("--check-metadata", action="store_true", help="Flag embedded metadata/EXIF")
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
    width = video.get("width", "?")
    height = video.get("height", "?")
    fps = video.get("r_frame_rate", "?")

    print(f"=== Video Probe: {args.path} ===")
    print()
    print(f"duration: {duration:.1f}s ({duration / 60:.1f} min)")
    print(f"size: {format_size(size)}")
    print(f"resolution: {width}x{height}")
    print(f"codec: {video.get('codec_name', 'unknown')}")
    print(f"fps: {fps}")
    print(f"audio: {'yes' if audio else 'no'}")
    print()

    # BGBlur free tier limits
    print("## BGBlur Tier Check")
    size_ok = size <= 200 * 1024 * 1024
    duration_ok = duration <= 600
    print(f"size_under_200mb: {'yes' if size_ok else 'NO — exceeds free tier'}")
    print(f"duration_under_10min: {'yes' if duration_ok else 'NO — exceeds free tier'}")
    print()

    if args.check_metadata:
        tags = fmt.get("tags", {})
        print("## Embedded Metadata")
        if tags:
            for k, v in tags.items():
                print(f"  {k}: {v}")
            print("warning: strip metadata before external sharing")
        else:
            print("  none detected")
        print()

    print("=== Probe Complete ===")


if __name__ == "__main__":
    main()
