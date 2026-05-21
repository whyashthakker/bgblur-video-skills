#!/usr/bin/env python3
"""
Automated blur QA report — structural checks on blurred video.
Usage: python3 scripts/blur_qa_report.py "blurred_output.mp4"
Requires: ffprobe (ffmpeg)
"""
import argparse
import json
import shutil
import subprocess
import sys


def probe(path: str) -> dict:
    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", "-count_frames", path]
    r = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def main():
    parser = argparse.ArgumentParser(description="Automated blur QA structural report")
    parser.add_argument("path")
    args = parser.parse_args()

    if not shutil.which("ffprobe"):
        print("error: ffprobe not found")
        sys.exit(1)

    data = probe(args.path)
    fmt = data["format"]
    video = next(s for s in data["streams"] if s["codec_type"] == "video")
    duration = float(fmt["duration"])
    size_mb = int(fmt["size"]) / (1024 * 1024)
    nb_frames = video.get("nb_read_frames") or video.get("nb_frames", "?")
    fps_str = video.get("r_frame_rate", "0/0")
    num, den = fps_str.split("/") if "/" in fps_str else (fps_str, "1")
    fps = float(num) / float(den) if float(den) else 0

    print(f"=== Blur QA Report: {args.path} ===")
    print()
    print(f"duration: {duration:.2f}s")
    print(f"size: {size_mb:.1f} MB")
    print(f"resolution: {video['width']}x{video['height']}")
    print(f"codec: {video['codec_name']}")
    print(f"fps: {fps:.2f}")
    print(f"frames: {nb_frames}")
    print()

    warnings = []
    if duration < 1:
        warnings.append("Very short clip — verify this is the full export")
    if size_mb < 0.5 and duration > 10:
        warnings.append("Unusually small file for duration — check quality/bitrate")
    if video["codec_name"] not in ("h264", "hevc", "vp9", "av1"):
        warnings.append(f"Uncommon codec '{video['codec_name']}' — verify playback compatibility")
    if fps > 0 and abs(fps - round(fps)) > 0.01:
        warnings.append(f"Non-integer fps ({fps:.3f}) — may cause flicker in blur masks")

    expected_frames = int(duration * fps) if fps else 0
    if nb_frames != "?" and expected_frames and abs(int(nb_frames) - expected_frames) > expected_frames * 0.05:
        warnings.append(f"Frame count mismatch: {nb_frames} vs ~{expected_frames} expected")

    print("## Structural Checks")
    if warnings:
        for w in warnings:
            print(f"  ⚠️  {w}")
    else:
        print("  ✅ No structural issues detected")
    print()
    print("## Manual Review Required")
    print("  Run sample_frames.py and inspect for P0/P1 blur defects")
    print("  Scrub at 2x speed checking faces, plates, and mask edges")
    print()
    print("=== Report Complete ===")


if __name__ == "__main__":
    main()
