# BGBlur Skills

> Canonical product: [bgblur.com](https://www.bgblur.com/en)  
> Publisher: BGBlur

First-party agent skills for the BGBlur ecosystem. For visual design tokens see [DESIGN.md](DESIGN.md).

## Purpose

This repository (`video-skills`) hosts **BGBlur-specific agent skills** — modular `SKILL.md` packages that teach AI agents how to work with AI video privacy: background blur, face anonymization, license plate redaction, export optimization, and API integration.

Skills here cover the full video blur pipeline — from FFmpeg prep and privacy compliance through QA and platform export — all aligned with [BGBlur](https://www.bgblur.com/en)'s browser-based, motion-tracked blur product.

## What BGBlur Is

BGBlur is a browser-based AI video privacy editor. No downloads, no manual masking — upload, blur, export in HD.

| Surface | URL | What it provides |
|---------|-----|------------------|
| Home | [/en](https://www.bgblur.com/en) | Product overview, feature cards, social proof |
| Upload / Editor | [/en/upload](https://www.bgblur.com/en/upload) | Browser video blur editor — upload, preview, export |
| Demo | [/demo](https://www.bgblur.com/demo) | Interactive product demo |
| Pricing | [/en/pricing](https://www.bgblur.com/en/pricing) | Credit tiers (Starter, Creator, Pro, Custom) |
| Enterprise | [/en/pricing#enterprise](https://www.bgblur.com/en/pricing#enterprise) | CCTV, high-volume pipelines, dedicated support |
| API & SDK | [/en/api-services](https://www.bgblur.com/en/api-services) | Face blur, plate blur, NSFW detection APIs |
| Background blur | [/en/features/blur-bg](https://www.bgblur.com/en/features/blur-bg) | AI background blur with subject isolation |
| Face blur | [/en/features/face-blur](https://www.bgblur.com/en/features/face-blur) | Motion-tracked face masking |
| Face anonymization | [/en/features/face-anonymization](https://www.bgblur.com/en/features/face-anonymization) | Compliance-grade identity removal |
| License plate blur | [/en/features/license-blur](https://www.bgblur.com/en/features/license-blur) | Dashcam and street footage plate redaction |
| Blur anything | [/en/features/blur-anything](https://www.bgblur.com/en/features/blur-anything) | Prompt-based object blur |
| How-to guide | [/en/how-to-blur-background-without-green-screen](https://www.bgblur.com/en/how-to-blur-background-without-green-screen) | Background blur without green screen |

**Quick start:** Upload at [bgblur.com/en/upload](https://www.bgblur.com/en/upload) → pick blur mode → export MP4/MOV/WebM.

**Free tier:** Videos under 200MB and 10 minutes. Zero data retention after export.

## Repository Layout

```
video-skills/
├── README.md                          # Overview, catalog, conventions
├── DESIGN.md                          # Visual design system (DESIGN.md spec — YAML + rationale)
└── .agents/skills/
    ├── video-privacy-blur/            # Privacy workflows — faces, plates, GDPR/CCPA/FERPA
    ├── ffmpeg-video-prep/             # Pre-process footage before upload (trim, convert, metadata)
    ├── video-export-optimize/         # Platform exports — YouTube, TikTok, Reels, LinkedIn
    ├── video-blur-qa/                 # QA blurred output — flicker, missed detections, halos
    └── bgblur-api-sdk/                # REST API integration — face/plate blur, batch pipelines
```

Each skill directory follows the standard layout:

```
skill-name/
├── SKILL.md              # Required — frontmatter + instructions
├── reference.md          # Optional — deep reference (progressive disclosure)
└── scripts/              # Optional — utility scripts
```

## Skill Catalog

### 1. `video-privacy-blur`

**Triggers:** User mentions face blur, face anonymization, license plate blur, privacy redaction, GDPR video compliance, PII removal, dashcam privacy, or anonymizing footage before publishing.

**Responsibilities:**
- Classify privacy risk (faces, plates, screens, audio PII)
- Choose BGBlur mode: Face Blur vs Anonymization vs Plate Blur vs Blur Anything
- Apply compliance rules (GDPR, CCPA, FERPA, journalism)
- Run `scripts/video_probe.py` for tier limit checks (200MB / 10 min free)
- Link to [Face Anonymization](https://www.bgblur.com/en/features/face-anonymization) and [License Plate Blur](https://www.bgblur.com/en/features/license-blur)

### 2. `ffmpeg-video-prep`

**Triggers:** User mentions ffmpeg, video conversion, trim video, normalize format, strip metadata, prepare video for upload, or MP4/MOV/MKV conversion.

**Responsibilities:**
- Inspect source with `scripts/video_probe.py`
- Trim, convert to H.264 MP4, normalize fps (24/30), strip EXIF/GPS
- Fix phone rotation, VFR, and oversize files for free tier
- One-shot prep command before [BGBlur Upload](https://www.bgblur.com/en/upload)

### 3. `video-export-optimize`

**Triggers:** User mentions export settings, social media video, platform upload, bitrate, vertical video, Reels, Shorts, or publishing blurred videos.

**Responsibilities:**
- Transcode BGBlur exports for YouTube, TikTok, Instagram, LinkedIn, web
- Preserve blur quality (CRF 18–20, single re-encode pass)
- Normalize audio loudness or strip audio for spoken PII
- Validate with `scripts/export_check.py --platform [youtube|tiktok|reels|...]`

### 4. `video-blur-qa`

**Triggers:** User mentions blur quality, QA review, mask artifacts, flickering blur, missed faces, plate tracking failure, or validating BGBlur output before delivery.

**Responsibilities:**
- Sample critical frames with `scripts/sample_frames.py`
- Review by blur type (face, plate, background, object)
- Classify defects P0–P3 (blocker → cosmetic)
- Run structural checks with `scripts/blur_qa_report.py`
- Route re-process failures to [BGBlur Upload](https://www.bgblur.com/en/upload) or [Enterprise](https://www.bgblur.com/en/pricing#enterprise)

### 5. `bgblur-api-sdk`

**Triggers:** User mentions BGBlur API, blur API integration, face blur API, license plate API, video blur SDK, or programmatic blur processing.

**Responsibilities:**
- Map use case to API endpoint (Face/Plate blur image/video, NSFW detection)
- Guide sync (image) vs async (video) integration patterns
- Document auth, webhooks, batch pipelines, error handling
- Run `scripts/api_health_check.py` for connectivity
- Link to [API Services](https://www.bgblur.com/en/api-services) and enterprise sales

## Project Docs

| File | Format | Who reads it |
|------|--------|--------------|
| [README.md](README.md) | Overview | Humans |
| [DESIGN.md](DESIGN.md) | DESIGN.md spec (YAML tokens + rationale) | Design agents |

## Conventions

### Skill authoring

1. **Concise SKILL.md** — Under 500 lines; agent is already capable; add only BGBlur-specific context.
2. **Third-person descriptions** — Descriptions drive auto-discovery; include WHAT + WHEN + trigger terms.
3. **Progressive disclosure** — Deep content in `reference.md`; one level of indirection max.
4. **Privacy-first** — Always mention zero data retention and browser-based processing where relevant.
5. **Canonical URLs** — Link to bgblur.com surfaces, not third-party mirrors.

### Naming conventions

- Prefix pipeline skills with `video-` (processing stages)
- Prefix integration skills with product name (e.g., `bgblur-api-sdk`)
- Lowercase, hyphens, max 64 chars

### Trigger coverage map

```
User intent                              → Skill
─────────────────────────────────────────────────────────────
"Blur faces for GDPR compliance"         → video-privacy-blur
"Anonymize dashcam footage"              → video-privacy-blur
"Convert MOV to MP4 before upload"       → ffmpeg-video-prep
"Strip GPS metadata from video"            → ffmpeg-video-prep
"Export for TikTok / Reels"              → video-export-optimize
"Blur looks flickery / missed a face"    → video-blur-qa
"Integrate blur API in our app"          → bgblur-api-sdk
"Batch process fleet camera footage"     → bgblur-api-sdk + video-privacy-blur
"Match BGBlur brand colors / UI"         → DESIGN.md
```

## BGBlur Product Summary

| Feature | Mode | Best for |
|---------|------|----------|
| Background blur | Subject isolation + bokeh | Vlogs, interviews, social clips |
| Face blur | Gaussian/pixel mask | Casual sharing, bystanders |
| Face anonymization | Strong identity removal | Public release, compliance, education |
| License plate blur | Motion-tracked redaction | Dashcam, street, fleet video |
| Blur anything | Prompt-based object blur | Screens, badges, custom PII |

**Processing model:** Browser-native AI with motion tracking. No frame-by-frame manual roto. Files deleted after export.

**Supported formats:** MP4, MOV, M4V, AVI, MKV (video); JPG, PNG, WebP, GIF (photo).

**Pricing tiers:**

| Plan | Price | Credits | Approx. video |
|------|-------|---------|---------------|
| Starter | $4.99/mo | 50 | < 1 min |
| Creator | $24.99/mo | 250 | ~4 min |
| Pro | $89.99/mo | 1,000 | ~16 min |
| Custom | $10 / 100 credits | 100 | ~1 min |

## Web Editor vs API

| Dimension | BGBlur Web Editor | BGBlur API & SDK |
|-----------|-------------------|------------------|
| Format | Browser upload UI | REST API + webhooks |
| Audience | Creators, editors, one-off edits | Developers, UGC platforms, fleet systems |
| Volume | Credit-based per clip | Tiered request plans + enterprise |
| Integration | None required | Embed in app pipeline |
| Entry | [bgblur.com/en/upload](https://www.bgblur.com/en/upload) | [bgblur.com/en/api-services](https://www.bgblur.com/en/api-services) |

## Video Pipeline (Skills Flow)

```
Source footage
    │
    ▼
ffmpeg-video-prep          Trim, convert, strip metadata
    │
    ▼
BGBlur editor / API        Blur faces, plates, backgrounds, objects
    │
    ▼
video-blur-qa              Sample frames, classify defects
    │
    ▼
video-export-optimize      Platform-specific transcode + publish
```

## Integration with Agent Runtimes

| Agent | Install path |
|-------|-------------|
| Cursor | `.cursor/skills/` or `.agents/skills/` |
| Claude Code | `.claude/skills/` |
| Cline | `.cline/` |
| Global | `~/.cursor/skills/`, `~/.claude/skills/` |

Manifest tracking: `skills-lock.json` (version + hash lock for installed packages).

## Install

Copy skills into your agent skills directory:

```bash
cp -r .agents/skills/* .cursor/skills/
```

Or symlink for local development:

```bash
ln -s "$(pwd)/.agents/skills" .cursor/skills/bgblur
```

When published to a skills registry:

```bash
npx skills init
npx skills add <source>/video-skills@video-privacy-blur -y
```

## Roadmap

| Skill | Priority | Notes |
|-------|----------|-------|
| `video-bulk-processing` | P1 | Enterprise/CCTV batch pipelines |
| `bgblur-photo-blur` | P1 | Photo background blur workflows |
| `video-motion-tracking` | P2 | Edge cases — fast motion, occlusions, scene cuts |
| `seo-geo` | P2 | Marketing SEO/GEO for bgblur.com pages |
| `architecture.md` | P2 | Engineering design doc for blur pipeline internals |

## References

- Product: https://www.bgblur.com/en
- Upload: https://www.bgblur.com/en/upload
- Pricing: https://www.bgblur.com/en/pricing
- API services: https://www.bgblur.com/en/api-services
- Demo: https://www.bgblur.com/demo
- Enterprise: https://www.bgblur.com/en/pricing#enterprise
