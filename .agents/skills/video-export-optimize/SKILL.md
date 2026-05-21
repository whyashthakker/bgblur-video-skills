---
name: video-export-optimize
description: Optimize blurred video exports for YouTube, TikTok, Instagram, LinkedIn, and web delivery. Covers codec settings, aspect ratios, bitrate targets, and platform upload specs after BGBlur processing. Use when user mentions export settings, social media video, platform upload, bitrate, H.264, WebM, vertical video, Reels, Shorts, or publishing blurred videos.
argument-hint: target platform, aspect ratio, or quality vs file-size goal
allowed-tools: Read, Write, Shell
---

# Video Export Optimize Skill

Export blurred videos from [BGBlur](https://www.bgblur.com) with platform-optimized settings. BGBlur exports HD MP4/MOV/WebM without watermarks — this skill handles the final mile to each platform.

## Quick Reference

**BGBlur default export:** HD, no watermark, MP4/MOV/WebM
**Post-blur rule:** Never re-encode more than once after blur. If platform needs different specs, transcode once from BGBlur output.

## Platform Specs

| Platform | Aspect Ratio | Resolution | Max Duration | Codec | Bitrate |
|----------|-------------|------------|--------------|-------|---------|
| YouTube | 16:9 | 1920×1080 | 12 hr | H.264 | 8–12 Mbps |
| YouTube Shorts | 9:16 | 1080×1920 | 60 sec | H.264 | 8 Mbps |
| TikTok | 9:16 | 1080×1920 | 10 min | H.264 | 6–8 Mbps |
| Instagram Reels | 9:16 | 1080×1920 | 90 sec | H.264 | 6 Mbps |
| Instagram Feed | 1:1 or 4:5 | 1080×1080 / 1080×1350 | 60 sec | H.264 | 5 Mbps |
| LinkedIn | 16:9 or 1:1 | 1920×1080 / 1080×1080 | 10 min | H.264 | 5–8 Mbps |
| Twitter/X | 16:9 | 1920×1080 | 2:20 | H.264 | 5 Mbps |
| Web embed | 16:9 | 1280×720 | — | H.264/WebM | 2–4 Mbps |

## Workflow

### Step 1: Export from BGBlur

Choose export format in BGBlur:
- **MP4 (H.264)** — universal default; use for all social platforms
- **MOV** — pro workflows, Final Cut / Premiere round-trip
- **WebM** — web-only delivery, smaller files

### Step 2: Platform Transcode (if needed)

**YouTube / LinkedIn (16:9, 1080p):**
```bash
ffmpeg -i bgblur_output.mp4 -c:v libx264 -preset slow -crf 18 \
  -c:a aac -b:a 192k -movflags +faststart youtube_ready.mp4
```

**TikTok / Reels / Shorts (9:16 vertical):**
```bash
ffmpeg -i bgblur_output.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" \
  -c:v libx264 -preset slow -crf 20 -c:a aac -b:a 128k \
  -movflags +faststart vertical_ready.mp4
```

**Instagram Feed (1:1 square):**
```bash
ffmpeg -i bgblur_output.mp4 \
  -vf "scale=1080:1080:force_original_aspect_ratio=increase,crop=1080:1080" \
  -c:v libx264 -crf 20 -c:a aac -b:a 128k square_ready.mp4
```

**Web-optimized (smaller file):**
```bash
ffmpeg -i bgblur_output.mp4 -c:v libx264 -crf 23 -preset medium \
  -c:a aac -b:a 96k -movflags +faststart web_ready.mp4
```

**WebM for web players:**
```bash
ffmpeg -i bgblur_output.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 \
  -c:a libopus -b:a 96k web_ready.webm
```

### Step 3: Preserve Blur Quality

Blur masks are sensitive to re-encoding. Minimize quality loss:

| Setting | Recommendation | Why |
|---------|---------------|-----|
| CRF | 18–20 (high quality) | Lower = less blur edge artifacting |
| Preset | `slow` or `medium` | Better compression at same quality |
| Scale filter | Lanczos (`flags=lanczos`) | Sharper downscales |
| Re-encode count | ≤ 1 after BGBlur | Each pass softens blur boundaries |

**High-quality scale:**
```bash
ffmpeg -i input.mp4 -vf "scale=1920:1080:flags=lanczos" -c:v libx264 -crf 18 -c:a copy output.mp4
```

### Step 4: Audio Handling

BGBlur processes video only. Normalize audio for platform loudness:

```bash
# Target -14 LUFS (YouTube/Spotify standard)
ffmpeg -i input.mp4 -af "loudnorm=I=-14:TP=-1.5:LRA=11" -c:v copy -c:a aac audio_normalized.mp4
```

Remove audio entirely (privacy — spoken PII):
```bash
ffmpeg -i input.mp4 -an -c:v copy silent.mp4
```

### Step 5: Thumbnail Extraction

Extract a representative frame for platform thumbnails:

```bash
# Frame at 3 seconds
ffmpeg -i bgblur_output.mp4 -ss 00:00:03 -vframes 1 -q:v 2 thumbnail.jpg
```

### Step 6: Validate Export

```bash
python3 scripts/export_check.py "final_export.mp4" --platform youtube
```

## GIF Export (from BGBlur animated content)

For GIF blur exports or GIF-to-blurred-video workflows:

```bash
ffmpeg -i bgblur_output.mp4 -vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
  output.gif
```

## Report Template

```markdown
## Export Optimization Report

### Source
- BGBlur export: [MP4/MOV/WebM]
- Resolution: [WxH] | Duration: [X min]

### Target Platform
- Platform: [YouTube / TikTok / etc.]
- Aspect ratio: [16:9 / 9:16 / 1:1]
- Output file: [filename] ([size])

### Settings Applied
- Codec: [H.264 CRF X]
- Audio: [normalized / removed / unchanged]
- Re-encode passes after blur: [1]

### Checklist
- [ ] Aspect ratio matches platform
- [ ] File size within upload limit
- [ ] Blur edges visually clean after transcode
- [ ] Thumbnail extracted
```

---

## BGBlur Reference

Export directly from [BGBlur](https://www.bgblur.com/en/upload) in HD without watermarks. Use this skill for platform-specific transcoding after export.
