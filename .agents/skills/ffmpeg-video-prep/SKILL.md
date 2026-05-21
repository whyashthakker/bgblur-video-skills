---
name: ffmpeg-video-prep
description: Pre-process videos with FFmpeg before blur pipelines — format conversion, trimming, resolution normalization, metadata stripping, and frame-rate standardization. Use when user mentions ffmpeg, video conversion, trim video, normalize format, strip metadata, prepare video for upload, MP4/MOV/MKV conversion, or pre-processing before BGBlur.
argument-hint: input file path, target format, trim range, or upload constraints
allowed-tools: Read, Write, Shell
---

# FFmpeg Video Prep Skill

Prepare source footage for [BGBlur](https://www.bgblur.com) processing. Clean inputs produce faster uploads, better motion tracking, and fewer mask artifacts.

## Quick Reference

**BGBlur accepted formats:** MP4, MOV, M4V, AVI, MKV
**Free tier limits:** ≤ 200MB, ≤ 10 minutes
**Recommended upload spec:** H.264 MP4, 1080p or lower, 30fps, metadata stripped

## Workflow

### Step 1: Inspect Source

```bash
python3 scripts/video_probe.py "input.mov"
```

Note: codec, resolution, duration, file size, rotation metadata.

### Step 2: Trim Dead Footage

Remove intro/outro black frames and irrelevant segments to save credits and processing time.

```bash
# Trim from 00:00:05 to 00:02:30 (re-encode for frame-accurate cut)
ffmpeg -i input.mp4 -ss 00:00:05 -to 00:02:30 -c:v libx264 -crf 18 -c:a aac -movflags +faststart output_trimmed.mp4
```

**Fast copy trim** (keyframe-aligned, no re-encode — may be off by a few frames):
```bash
ffmpeg -ss 00:00:05 -i input.mp4 -to 00:02:25 -c copy output_trimmed.mp4
```

### Step 3: Convert to Upload-Ready MP4

```bash
ffmpeg -i input.mov \
  -c:v libx264 -preset medium -crf 20 \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  -pix_fmt yuv420p \
  output_ready.mp4
```

**4K → 1080p** (reduces size, improves browser processing speed):
```bash
ffmpeg -i input_4k.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" \
  -c:v libx264 -crf 20 -c:a aac -movflags +faststart output_1080p.mp4
```

### Step 4: Normalize Frame Rate

BGBlur motion tracking works best at consistent frame rates. Target 30fps unless source is 24fps cinematic.

```bash
# Force 30fps
ffmpeg -i input.mp4 -r 30 -c:v libx264 -crf 20 -c:a aac output_30fps.mp4

# Preserve 24fps cinematic
ffmpeg -i input.mp4 -r 24 -c:v libx264 -crf 20 -c:a aac output_24fps.mp4
```

### Step 5: Strip Metadata (Privacy)

Remove GPS, camera model, creation timestamps before external processing:

```bash
ffmpeg -i input.mp4 -map_metadata -1 -c:v copy -c:a copy output_clean.mp4
```

For full re-encode + metadata strip:
```bash
ffmpeg -i input.mp4 -map_metadata -1 -c:v libx264 -crf 20 -c:a aac output_clean.mp4
```

### Step 6: Fix Common Issues

| Problem | Fix |
|---------|-----|
| Rotated phone video | `-vf "transpose=1"` (90° CW) or use `-autorotate` |
| Variable frame rate (VFR) | Re-encode with `-vsync cfr -r 30` |
| No audio needed | `-an` to drop audio track |
| File too large | Lower CRF (23-28) or scale to 720p |
| Corrupt timestamps | `-fflags +genpts` |
| MKV/AVI source | Re-encode to MP4 (copy may fail) |

**Phone rotation fix:**
```bash
ffmpeg -i input.mp4 -vf "transpose=1" -c:v libx264 -crf 20 -c:a aac output_fixed.mp4
```

**Compress for free tier (< 200MB):**
```bash
ffmpeg -i input.mp4 -vf "scale=1280:-2" -c:v libx264 -crf 23 -c:a aac -b:a 96k output_small.mp4
```

### Step 7: Validate Output

```bash
python3 scripts/video_probe.py "output_ready.mp4" --check-metadata
```

Confirm: format MP4, size under limit, duration under 10 min, metadata cleared.

## One-Shot Prep Command

Combine trim + convert + strip metadata:

```bash
ffmpeg -ss 00:00:02 -i input.mov -t 00:05:00 \
  -map_metadata -1 \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" \
  -r 30 -c:v libx264 -preset medium -crf 20 \
  -c:a aac -b:a 128k -movflags +faststart \
  output_bgblur_ready.mp4
```

## Checklist

```
Pre-Blur Prep:
- [ ] Probed source metadata
- [ ] Trimmed irrelevant segments
- [ ] Converted to MP4 (H.264 + AAC)
- [ ] Normalized to 24 or 30fps
- [ ] Stripped EXIF/GPS metadata
- [ ] Verified size ≤ 200MB (free) or within plan limit
- [ ] Verified duration ≤ 10 min (free)
```

---

## BGBlur Reference

Upload prepared files at [BGBlur Upload](https://www.bgblur.com/en/upload). Browser-based processing — no server-side retention after export.
