---
name: bgblur-api-sdk
description: Integrate BGBlur blur APIs into apps and pipelines — face blur, license plate blur, NSFW detection for images and video. Covers REST API patterns, batch processing, webhook delivery, and SDK usage. Use when user mentions BGBlur API, blur API integration, face blur API, license plate API, video blur SDK, embed blur in app, or programmatic blur processing.
argument-hint: API endpoint, integration language, batch vs realtime, or use case
allowed-tools: Read, Write, WebSearch, Shell
---

# BGBlur API & SDK Skill

Integrate [BGBlur API services](https://www.bgblur.com/en/api-services) into applications, CI pipelines, and batch processing workflows.

## Quick Reference

**Available APIs:**

| API | Type | Use Case |
|-----|------|----------|
| Face Blur (Image) | Image | Profile photos, thumbnails, uploads |
| Face Blur (Video) | Video | Frame-aware face tracking + blur |
| License Plate Blur (Image) | Image | Parking, fleet photo redaction |
| License Plate Blur (Video) | Video | Dashcam, CCTV, street footage |
| NSFW Image Detector | Image | Content moderation gate |
| NSFW Video Detector | Video | Timestamped moderation scores |

**Integration patterns:**
- **Sync** — upload → process → download (short clips, images)
- **Async + webhook** — submit job → poll/webhook → fetch result (long video)
- **Batch** — queue multiple files → bulk download (enterprise)

## Workflow

### Step 1: Choose API Endpoint

```
Input is image?
├── Need face redaction? → Face Blur (Image)
├── Need plate redaction? → License Plate Blur (Image)
└── Need moderation? → NSFW Image Detector

Input is video?
├── Need face redaction? → Face Blur (Video)
├── Need plate redaction? → License Plate Blur (Video)
└── Need moderation? → NSFW Video Detector
```

### Step 2: Authentication

Store API key in environment variable — never hardcode:

```bash
export BGBLUR_API_KEY="your_api_key_here"
```

Verify connectivity:
```bash
python3 scripts/api_health_check.py
```

### Step 3: Image Processing (Sync)

**Face blur — single image:**
```python
import os
import requests

API_KEY = os.environ["BGBLUR_API_KEY"]
BASE = "https://api.bgblur.com/v1"  # confirm current base URL in docs

with open("photo.jpg", "rb") as f:
    resp = requests.post(
        f"{BASE}/face-blur/image",
        headers={"Authorization": f"Bearer {API_KEY}"},
        files={"file": f},
        data={"blur_strength": "medium"},
    )
    resp.raise_for_status()
    with open("photo_blurred.jpg", "wb") as out:
        out.write(resp.content)
```

**License plate blur — image:**
```python
resp = requests.post(
    f"{BASE}/license-plate-blur/image",
    headers={"Authorization": f"Bearer {API_KEY}"},
    files={"file": open("dashcam_frame.jpg", "rb")},
)
```

### Step 4: Video Processing (Async)

Video APIs are async — submit, poll, download:

```python
import time
import requests

# 1. Submit job
with open("clip.mp4", "rb") as f:
    job = requests.post(
        f"{BASE}/face-blur/video",
        headers={"Authorization": f"Bearer {API_KEY}"},
        files={"file": f},
        data={"webhook_url": "https://yourapp.com/hooks/bgblur"},
    ).json()

job_id = job["id"]

# 2. Poll until complete
while True:
    status = requests.get(
        f"{BASE}/jobs/{job_id}",
        headers={"Authorization": f"Bearer {API_KEY}"},
    ).json()
    if status["state"] == "completed":
        break
    if status["state"] == "failed":
        raise RuntimeError(status.get("error", "Job failed"))
    time.sleep(5)

# 3. Download result
result = requests.get(
    status["output_url"],
    headers={"Authorization": f"Bearer {API_KEY}"},
)
with open("clip_blurred.mp4", "wb") as f:
    f.write(result.content)
```

### Step 5: NSFW Moderation

**Image — accept/reject gate before publishing:**
```python
resp = requests.post(
    f"{BASE}/nsfw/image",
    headers={"Authorization": f"Bearer {API_KEY}"},
    files={"file": open("upload.jpg", "rb")},
).json()

if resp["score"] > 0.85:
    reject_upload(resp["categories"])
```

**Video — timestamped flags for review queue:**
```python
resp = requests.post(
    f"{BASE}/nsfw/video",
    headers={"Authorization": f"Bearer {API_KEY}"},
    files={"file": open("clip.mp4", "rb")},
).json()

for flag in resp["timestamps"]:
    print(f"NSFW at {flag['start']}s–{flag['end']}s: {flag['score']:.2f}")
```

### Step 6: Batch Pipeline

For high-volume (CCTV, fleet, UGC platforms):

```
Upload batch → Queue → Process parallel → Webhook per job → Aggregate results
```

**Batch pattern:**
```python
import concurrent.futures

def process_file(path: str) -> str:
    # submit + poll each file
    return output_path

files = ["cam1.mp4", "cam2.mp4", "cam3.mp4"]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    results = list(pool.map(process_file, files))
```

Enterprise tier: [BGBlur Enterprise](https://www.bgblur.com/en/pricing#enterprise) for dedicated throughput and SLA.

### Step 7: Error Handling

| HTTP Code | Meaning | Action |
|-----------|---------|--------|
| 400 | Invalid file/format | Validate with `ffmpeg-video-prep` first |
| 401 | Bad API key | Check `BGBLUR_API_KEY` |
| 413 | File too large | Compress or split video |
| 429 | Rate limited | Exponential backoff |
| 500 | Server error | Retry with idempotency key |

**Retry wrapper:**
```python
import time

def with_retry(fn, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            return fn()
        except requests.HTTPError as e:
            if e.response.status_code in (429, 500) and attempt < max_attempts - 1:
                time.sleep(2 ** attempt)
            else:
                raise
```

## Integration Checklist

```
API Integration:
- [ ] API key in env var (not source code)
- [ ] Input validation (format, size, duration)
- [ ] Async polling or webhook handler implemented
- [ ] Error handling with retry for 429/500
- [ ] Output stored securely; temp files cleaned up
- [ ] Rate limits respected for batch jobs
- [ ] QA step on sample outputs (see video-blur-qa skill)
```

## Architecture Patterns

**UGC upload gate:**
```
User upload → NSFW detect → (pass) → Face blur → Store → Publish
                           → (fail) → Reject
```

**Fleet dashcam pipeline:**
```
Camera upload → Plate blur (video) → QA sample → Archive
```

**CMS thumbnail safety:**
```
Featured image → Face blur (image) → CDN → Frontend
```

## Report Template

```markdown
## BGBlur API Integration Plan

### Use Case
[UGC moderation / fleet redaction / CMS thumbnails / etc.]

### APIs Selected
- [Endpoint] — [why]

### Flow
[Sync / Async / Batch]

### Volume Estimate
- [X videos/day] | avg [Y min] | [Z MB]

### Open Questions
- [Webhook endpoint ready?]
- [Enterprise tier needed?]
```

---

## BGBlur Reference

- [API Services](https://www.bgblur.com/en/api-services) — full endpoint catalog
- [Pricing](https://www.bgblur.com/en/pricing) — credit tiers and enterprise
- [Upload (manual fallback)](https://www.bgblur.com/en/upload) — for testing API output quality

**Note:** Confirm current API base URL, request schemas, and auth headers against official BGBlur API documentation before production deployment.
