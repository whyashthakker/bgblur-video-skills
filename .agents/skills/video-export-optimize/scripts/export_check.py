#!/usr/bin/env python3
"""
Validate video export against platform specs.
Usage: python3 scripts/export_check.py "output.mp4" --platform youtube
Requires: ffprobe (ffmpeg)
"""
import argparse
import json
import shutil
import subprocess
import sys

PLATFORMS = {
    "youtube": {"ratio": 16 / 9, "max_w": 3840, "max_h": 2160, "max_duration": 43200},
    "shorts": {"ratio": 9 / 16, "w": 1080, "h": 1920, "max_duration": 60},
    "tiktok": {"ratio": 9 / 16, "w": 1080, "h": 1920, "max_duration": 600},
    "reels": {"ratio": 9 / 16, "w": 1080, "h": 1920, "max_duration": 90},
    "instagram": {"ratio": 1.0, "w": 1080, "h": 1080, "max_duration": 60},
    "linkedin": {"ratio": 16 / 9, "max_w": 1920, "max_h": 1080, "max_duration": 600},
    "web": {"ratio": 16 / 9, "max_w": 1280, "max_h": 720, "max_duration": None},
}


def probe(path: str) -> dict | None:
    if not shutil.which("ffprobe"):
        print("error: ffprobe not found")
        sys.exit(1)
    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", path]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(r.stdout)
    except Exception as e:
        print(f"error: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Check export against platform specs")
    parser.add_argument("path")
    parser.add_argument("--platform", choices=list(PLATFORMS.keys()), default="youtube")
    args = parser.parse_args()

    spec = PLATFORMS[args.platform]
    data = probe(args.path)
    if not data:
        sys.exit(1)

    fmt = data["format"]
    video = next(s for s in data["streams"] if s["codec_type"] == "video")
    duration = float(fmt["duration"])
    size_mb = int(fmt["size"]) / (1024 * 1024)
    w, h = int(video["width"]), int(video["height"])
    ratio = w / h if h else 0
    codec = video["codec_name"]

    print(f"=== Export Check: {args.path} → {args.platform} ===")
    print()
    print(f"resolution: {w}x{h} (ratio {ratio:.3f})")
    print(f"duration: {duration:.1f}s")
    print(f"size: {size_mb:.1f} MB")
    print(f"codec: {codec}")
    print()

    issues = []
    target_ratio = spec.get("ratio")
    if target_ratio and abs(ratio - target_ratio) > 0.05:
        issues.append(f"aspect ratio {ratio:.2f} ≠ target {target_ratio:.2f}")

    max_dur = spec.get("max_duration")
    if max_dur and duration > max_dur:
        issues.append(f"duration {duration:.0f}s exceeds {max_dur}s limit")

    if codec not in ("h264", "hevc"):
        issues.append(f"codec {codec} — most platforms prefer H.264")

    if "w" in spec and (w != spec["w"] or h != spec["h"]):
        issues.append(f"resolution {w}x{h} ≠ recommended {spec['w']}x{spec['h']}")

    print("## Result")
    if issues:
        for i in issues:
            print(f"  ❌ {i}")
    else:
        print("  ✅ Passes platform checks")
    print()
    print("=== Check Complete ===")


if __name__ == "__main__":
    main()
