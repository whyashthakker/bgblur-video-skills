---
name: video-blur-qa
description: Quality assurance for AI-blurred videos — detect mask bleeding, temporal flicker, missed detections, edge halos, and motion-tracking failures. Use when user mentions blur quality, QA review, mask artifacts, flickering blur, missed faces, plate tracking failure, blur edge halo, or validating BGBlur output before delivery.
argument-hint: blurred video path, blur type (face/background/plate), or QA severity level
allowed-tools: Read, Write, Shell
---

# Video Blur QA Skill

Systematic quality assurance for videos processed with [BGBlur](https://www.bgblur.com) AI blur. Catch the failures users notice: flickering masks, missed faces, plate slips, and background bleed into subjects.

## Quick Reference

**Top 5 blur defects:**
1. **Temporal flicker** — mask toggles on/off between frames
2. **Edge halo** — sharp ring around blur boundary (subject hair, shoulders)
3. **Missed detection** — face/plate visible for 1+ frames after scene change
4. **Tracking slip** — mask drifts off target during fast motion
5. **Background bleed** — blur eats into subject (common with strong background blur)

## Workflow

### Step 1: Sample Critical Frames

Extract frames at high-risk timestamps:

```bash
python3 scripts/sample_frames.py "blurred_output.mp4" --output ./qa_frames/
```

Auto-samples: start, end, every 5s, and scene-change intervals.

**Manual extraction at suspect timestamps:**
```bash
ffmpeg -i blurred_output.mp4 -ss 00:01:23 -vframes 1 qa_frame_0123.jpg
```

### Step 2: Review by Blur Type

**Face Blur / Anonymization:**
- [ ] All visible faces masked (including partial/profile views)
- [ ] Reflections in mirrors/windows also blurred
- [ ] Minors and background bystanders covered
- [ ] Mask strength sufficient (can't reconstruct identity)
- [ ] No unblurred frames at scene cuts (check ±3 frames)

**License Plate Blur:**
- [ ] Plates readable nowhere in clip (scrub at 2x speed)
- [ ] Tracking holds during acceleration/braking
- [ ] Partial plates at frame edges caught
- [ ] Multiple vehicles each tracked independently
- [ ] Night/low-light plates still detected

**Background Blur:**
- [ ] Subject edges clean (hair, hands, moving limbs)
- [ ] No foreground object accidentally blurred
- [ ] Blur strength consistent across clip
- [ ] No pulsing blur intensity (temporal instability)
- [ ] Subject separation stable during movement

**Blur Anything (prompt-based):**
- [ ] All named objects blurred throughout
- [ ] Similar objects not missed (e.g., "laptop screen" → all screens)
- [ ] Object blur persists through occlusion/reappearance

### Step 3: Motion Stress Test

Review these high-risk segments at **2x playback**:

| Segment Type | What to Check |
|-------------|---------------|
| Fast pan | Background blur edge stability |
| Subject turns head | Face mask follows rotation |
| Vehicle passes | Plate tracked through motion blur |
| Scene cut | New detections within 2 frames |
| Zoom in/out | Mask scale matches subject |
| Low light / noise | Detection doesn't drop out |

### Step 4: Side-by-Side Comparison

Compare original vs blurred for delivery QA:

```bash
ffmpeg -i original.mp4 -i blurred_output.mp4 \
  -filter_complex "[0:v][1:v]hstack=inputs=2" \
  -c:v libx264 -crf 18 comparison.mp4
```

### Step 5: Automated Checks

```bash
python3 scripts/blur_qa_report.py "blurred_output.mp4"
```

Reports: resolution consistency, frame count, duration match, black frames, frozen segments.

### Step 6: Severity Classification

| Severity | Definition | Action |
|----------|-----------|--------|
| **P0 — Blocker** | Unblurred PII visible (face, plate, screen) | Re-process; do not ship |
| **P1 — Major** | Tracking slip > 5 frames or identity reconstructable | Re-process affected segment |
| **P2 — Minor** | Edge halo, 1-2 frame flicker | Accept or touch up if client-facing |
| **P3 — Cosmetic** | Slight blur intensity inconsistency | Accept |

## Common Fixes

| Defect | Likely Cause | Fix |
|--------|-------------|-----|
| Face missed at cut | Scene change | Re-upload; trim at cut point and process separately |
| Plate slip | Fast motion / low res | Upscale source or trim to slower segment |
| Background eats hair | Similar color to bg | Reduce blur strength; improve subject/background contrast in source |
| Flickering mask | VFR source footage | Re-prep with `ffmpeg-video-prep` (force 30fps CFR) |
| Object not found | Vague prompt | Use specific prompt: "white Tesla license plate" not "plate" |

## Report Template

```markdown
## Blur QA Report

### Asset
- File: [blurred_output.mp4]
- Blur type: [face / plate / background / object]
- Duration reviewed: [full / segments]

### Findings
| Timestamp | Severity | Issue | Notes |
|-----------|----------|-------|-------|
| 00:01:23 | P0 | Unblurred face | Bystander at frame edge |
| 00:02:45 | P2 | Edge halo | Subject hair, 3 frames |

### Verdict
- [ ] PASS — ready for delivery
- [ ] FAIL — re-process required

### Re-process Notes
[Specific segments, BGBlur mode changes, or prep fixes needed]
```

---

## BGBlur Reference

Re-process failed segments at [BGBlur Upload](https://www.bgblur.com/en/upload). For systematic failures on long footage, consider [Enterprise](https://www.bgblur.com/en/pricing#enterprise) batch pipelines.
