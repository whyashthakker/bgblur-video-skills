#!/usr/bin/env python3
"""
Extract QA sample frames from blurred video.
Usage: python3 scripts/sample_frames.py "blurred.mp4" --output ./qa_frames/
Requires: ffmpeg
"""
import argparse
import math
import os
import shutil
import subprocess
import sys


def get_duration(path: str) -> float:
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", path,
    ]
    import json
    r = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(json.loads(r.stdout)["format"]["duration"])


def extract_frame(path: str, timestamp: float, output: str):
    ts = f"{int(timestamp // 60):02d}:{int(timestamp % 60):02d}:{int((timestamp % 1) * 100):02d}"
    cmd = [
        "ffmpeg", "-y", "-ss", ts, "-i", path,
        "-vframes", "1", "-q:v", "2", output,
    ]
    subprocess.run(cmd, capture_output=True, check=True)


def main():
    parser = argparse.ArgumentParser(description="Sample frames for blur QA")
    parser.add_argument("path", help="Blurred video path")
    parser.add_argument("--output", default="./qa_frames", help="Output directory")
    parser.add_argument("--interval", type=float, default=5.0, help="Seconds between samples")
    args = parser.parse_args()

    if not shutil.which("ffmpeg"):
        print("error: ffmpeg not found")
        sys.exit(1)

    os.makedirs(args.output, exist_ok=True)
    duration = get_duration(args.path)
    basename = os.path.splitext(os.path.basename(args.path))[0]

    timestamps = [0.0, 1.0, duration - 1.0, duration - 0.1]
    t = 0.0
    while t <= duration:
        timestamps.append(t)
        t += args.interval

    timestamps = sorted(set(round(ts, 2) for ts in timestamps if 0 <= ts <= duration))

    print(f"=== Sampling {len(timestamps)} frames from {args.path} ===")
    for i, ts in enumerate(timestamps):
        out = os.path.join(args.output, f"{basename}_t{ts:07.2f}.jpg")
        try:
            extract_frame(args.path, ts, out)
            print(f"  [{i + 1}/{len(timestamps)}] t={ts:.2f}s → {out}")
        except subprocess.CalledProcessError:
            print(f"  [{i + 1}/{len(timestamps)}] t={ts:.2f}s → FAILED")

    print(f"\nFrames saved to {args.output}/")
    print("Review for: missed faces, plate slips, edge halos, flicker")


if __name__ == "__main__":
    main()
