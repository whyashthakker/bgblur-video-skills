---
version: alpha
name: BGBlur
description: Visual identity for BGBlur — AI-powered browser video privacy tool for background blur, face anonymization, and license plate redaction.
colors:
  primary: "#264E57"
  primary-dark: "#1F3A40"
  primary-darker: "#1D3A42"
  primary-light: "#2B5863"
  primary-muted: "#5D8D98"
  accent: "#58A6B5"
  accent-soft: "#9DC2CC"
  surface: "#FFFFF7"
  surface-alt: "#F4F7F9"
  surface-muted: "#EEF3F7"
  surface-tint: "#E9F7FA"
  on-surface: "#1F3A40"
  on-surface-muted: "#6B7280"
  border: "#CFD3DB"
  border-light: "#E5EBF1"
  border-subtle: "#D7DDE3"
  white: "#FFFFFF"
  dark: "#0A0A0A"
  star: "#F4C518"
  success: "#1F6F7A"
  error: "#DC2626"
typography:
  headline-display:
    fontFamily: swissNow
    fontSize: 56px
    fontWeight: 600
    lineHeight: 1.05
    letterSpacing: -0.03em
  headline-lg:
    fontFamily: swissNow
    fontSize: 40px
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: -0.02em
  headline-md:
    fontFamily: swissNow
    fontSize: 28px
    fontWeight: 600
    lineHeight: 1.15
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: swissNow
    fontSize: 20px
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: -0.01em
  body-lg:
    fontFamily: baseNeue
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.6
  body-md:
    fontFamily: baseNeue
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  body-sm:
    fontFamily: swissNowRegular
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
  label-md:
    fontFamily: swissNowRegular
    fontSize: 13px
    fontWeight: 600
    lineHeight: 1.3
  label-sm:
    fontFamily: swissNowRegular
    fontSize: 11px
    fontWeight: 500
    lineHeight: 1.2
  caption:
    fontFamily: swissNowRegular
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.4
  stat:
    fontFamily: calFont
    fontSize: 48px
    fontWeight: 600
    lineHeight: 1
    letterSpacing: -0.02em
rounded:
  sm: 4px
  md: 8px
  lg: 12px
  xl: 16px
  2xl: 20px
  3xl: 24px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  3xl: 64px
  section-y: 48px
  container-max: 1280px
  gutter: 24px
  card-padding: 16px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.white}"
    typography: "{typography.label-md}"
    rounded: "{rounded.lg}"
    padding: 12px 24px
  button-primary-hover:
    backgroundColor: "{colors.primary-light}"
  button-secondary:
    backgroundColor: "{colors.white}"
    textColor: "{colors.primary}"
    typography: "{typography.label-md}"
    rounded: "{rounded.lg}"
    padding: 12px 24px
  button-secondary-border:
    borderColor: "{colors.border-subtle}"
  card:
    backgroundColor: "{colors.white}"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.xl}"
    padding: "{spacing.card-padding}"
    borderColor: "{colors.border-light}"
  card-feature:
    backgroundColor: "{colors.white}"
    rounded: "{rounded.xl}"
    padding: 16px
    borderColor: "{colors.border}"
  badge-popular:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.white}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.full}"
  input-field:
    backgroundColor: "{colors.white}"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.lg}"
    padding: 12px 16px
    borderColor: "{colors.border-subtle}"
  upload-zone:
    backgroundColor: "{colors.surface-alt}"
    borderColor: "{colors.primary-light}"
    rounded: "{rounded.2xl}"
  avatar:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.white}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.full}"
    size: 32px
  step-number:
    backgroundColor: "{colors.primary}1A"
    textColor: "{colors.primary}"
    typography: "{typography.label-md}"
    rounded: "{rounded.lg}"
---

# BGBlur Design System

## Overview

BGBlur is a **privacy-first, browser-based AI video editor**. The visual identity balances **institutional trust** (compliance, enterprise, journalism) with **creator accessibility** (no downloads, one-click blur, social-ready exports).

**Brand personality:** Calm, precise, secure. Not flashy or playful — think *professional privacy tool*, not consumer filter app.

**Target audience:** Content creators, video editors, educators, journalists, fleet/security teams, and developers integrating blur APIs.

**Emotional tone:** The UI should feel like a clean editorial workspace — spacious, warm neutrals, deep teal accents. Users should feel their data is safe (privacy-first) and the tool is competent (motion-tracked AI, HD exports).

**Core product metaphors:**
- **Depth of field** — sharp subject, soft background (bokeh, cinematic blur)
- **Masking/redaction** — protective shield over sensitive regions
- **Browser-native** — no install friction; instant preview

**Voice & copy:**
- Lead with outcomes: "Protect privacy", "Export instantly", "No manual masking"
- Use concrete feature names: Face Blur, License Plate Blur, Face Anonymization, Blur Anything
- Stats build trust: "120K+ Blurred Clips", "500K+ License Plates Hidden", "Zero data retention"

## Colors

The palette is rooted in **deep ocean teal** on **warm limestone** surfaces — evoking clarity, depth, and the visual language of lens blur itself.

- **Primary (#264E57):** Deep teal for headlines, CTAs, avatars, and brand anchors. The signature BGBlur color — used on buttons, icons, and active states.
- **Primary Dark (#1F3A40):** Headline text on light surfaces. Slightly warmer than pure black for editorial softness.
- **Accent (#58A6B5):** Lighter teal for hover states, links, and secondary highlights. Suggests the "glow" of a well-blurred background.
- **Surface (#FFFFF7):** Warm off-white page background. Softer and more premium than `#FFFFFF` — the dominant section background on marketing pages.
- **Surface Alt (#F4F7F9):** Cool gray-teal tint for icon containers, upload zones, and nested panels.
- **Border (#CFD3DB):** Structural grid lines and section dividers. Used in the editorial grid layout with corner crosshair decorations.
- **White (#FFFFFF):** Cards, modals, and elevated content panels.
- **Star (#F4C518):** Review/rating stars only — do not use as a general accent.
- **Dark (#0A0A0A):** Reserved for dark-mode UI shells and editor chrome, not marketing hero backgrounds.

**Semantic usage:**
| Role | Token | Usage |
|------|-------|-------|
| Primary action | `primary` | Upload, Export, Sign In, Try Free |
| Body text | `on-surface` | Headings, card titles |
| Secondary text | `on-surface-muted` | Descriptions, metadata, captions |
| Page background | `surface` | Marketing sections, FAQ |
| Card background | `white` | Feature cards, testimonials, pricing |
| Icon container | `surface-alt` + `primary` at 10% opacity | Feature icons, step numbers |

## Typography

BGBlur uses a **dual-font system**: geometric display type for headlines, humanist sans for body.

- **Headlines (swissNow):** Tight tracking (`-0.02em` to `-0.03em`), semibold. Establishes technical precision and editorial authority. Used for H1–H3 and section titles.
- **Body (baseNeue):** Regular weight at 16–18px for long-form readability. Used for paragraphs, FAQ answers, and feature descriptions.
- **Labels (swissNowRegular):** 11–13px for metadata, step labels, testimonial roles, and UI chrome.
- **Stats (calFont / Cal Sans):** Large numerals for social proof counters ("120K+", "500K+"). Distinct from headlines — use only for metrics.

**Type scale:**

| Level | Font | Size | Weight | Use |
|-------|------|------|--------|-----|
| Display | swissNow | 48–56px | 600 | Hero H1 |
| H2 | swissNow | 28–40px | 600 | Section headings |
| H3 | swissNow | 15–20px | 600 | Card titles, steps |
| Body | baseNeue | 16–18px | 400 | Paragraphs |
| Small | swissNowRegular | 13–14px | 400 | Card descriptions |
| Caption | swissNowRegular | 11–12px | 400–500 | Metadata, roles |

**Fallback stack:** `system-ui, sans-serif` when custom fonts unavailable.

## Layout

BGBlur marketing pages use an **editorial grid layout** — full-bleed sections with contained max-width content and visible structural borders.

- **Container:** `max-width: 1280px` (`max-w-7xl`), centered, horizontal padding 16–24px
- **Section rhythm:** 48px vertical padding (`py-12`); alternate `surface` (#FFFFF7) and `white` backgrounds
- **Grid borders:** Sections use `border-x border-[#cfd3db]/80` on the container, creating a visible column frame. Corner **crosshair markers** (small `+` decorations) sit at grid intersections — a signature layout detail
- **Spacing scale:** 4px base unit; common steps: 8, 16, 24, 32, 48, 64px
- **Card grids:** 1-col mobile → 2-col tablet → 3–5 col desktop for feature cards
- **Full-bleed sections:** `w-screen` with `left-1/2 -translate-x-1/2` breakout pattern for alternating background bands

**Content density:** Generous whitespace. Marketing pages are spacious, not dense. The editor/upload UI can be denser but should retain the same color tokens.

## Elevation & Depth

Depth is achieved through **tonal layers and soft shadows**, not heavy drop shadows — mirroring the product's own blur aesthetic.

- **Level 0 — Page:** `surface` (#FFFFF7) or `white`
- **Level 1 — Cards:** White background, `1px border` in `border-light`, `shadow-sm` (`0 2px 12px rgba(0,0,0,0.06)`)
- **Level 2 — Active/Featured:** Stronger shadow with teal tint: `0 12px 40px rgba(43,88,99,0.18)` on selected feature cards
- **Level 3 — Modals/Overlays:** White panel on semi-transparent backdrop; `backdrop-blur: 24px` for glass effect in editor UI

**Hover states:** Cards lift subtly (`-translate-y-0.5`, `scale-[1.01]`) with shadow increase — never dramatic bounces.

**Blur as UI metaphor:** Use `backdrop-blur` sparingly in editor chrome and preview overlays. Marketing pages stay flat and editorial.

## Shapes

The shape language is **soft-modern**: rounded but not pill-shaped everywhere.

- **Cards & panels:** `12px` (`rounded-xl`) — primary container radius
- **Buttons:** `8–12px` (`rounded-lg` to `rounded-xl`)
- **Icon containers:** `rounded-lg` (8px) for square icons; `rounded-full` for circular avatars and feature orbit buttons
- **Upload zones:** `20–24px` (`rounded-2xl`) — larger radius signals drop-target affordance
- **Badges:** `rounded-full` for "Most Popular", step pills, and status tags
- **Step numbers:** Small rounded squares with `primary/10` background tint

Avoid mixing sharp (`0px`) and very round (`full`) corners on the same component group.

## Components

### Buttons

**Primary:** Teal background (`primary`), white text, semibold 13–14px, `rounded-lg`, padding 12×24px. Used for: "Try Background Blur for Free", "Upload", "Export", "Sign In".

**Secondary:** White background, teal text, `border-subtle` border. Used for: "Explore", secondary navigation.

**Ghost/Text:** Teal or muted text, no background. Used for: footer links, "Create account".

**Google OAuth:** White button with border, Google logo left-aligned. Standard third-party auth pattern.

### Feature Cards

White card, `rounded-xl`, `border-light`, `p-4`. Contains:
- Icon in `surface-alt` container with teal icon color
- Title in `headline-sm` (15–16px semibold, `on-surface`)
- Description in 13px muted text
- Optional "Explore →" link

**Product cards** (BGBlur Video, Photo, Enterprise, API): Larger cards with hover lift. "Most popular" badge on featured card.

### Step Cards (How It Works)

Numbered steps (`01`, `02`, `03`) in teal-tinted badge. Card with embedded **mini UI preview** at bottom — a cropped mock of the upload/editor interface in `surface-muted` background with border.

### Testimonial Cards

White card, `rounded-xl`, star row in gold (`star`), blockquote text, divider, circular avatar (teal bg + white initials), name + role caption.

### Pricing Cards

Tier name, strikethrough original price, bold sale price, credit count, CTA button. "MOST POPULAR" badge on Creator tier. Trust stats row below tiers.

### Upload / Editor UI

- **Upload zone:** Dashed or solid border in `primary-light`, `surface-alt` background, large `rounded-2xl`, progress bar in teal
- **Blur mode selector:** Horizontal pill tabs or stacked orbit buttons (Background Blur, Face Blur, License Plate, etc.)
- **Preview panel:** Video player with blur overlay preview; controls below
- **Export bar:** Progress indicator, format selector (MP4/MOV/WebM), download CTA

### Form Inputs

White background, `border-subtle`, `rounded-lg`, 12px vertical padding. Labels in `label-md`. Error states use `error` red with helper text below.

### Navigation

Clean top nav: logo left, feature links center/right, "Upload" + "Sign In" CTAs. Minimal — no mega menus on marketing pages.

### Icons

**Lucide** icon set (stroke, 2px weight). Common icons: `image`, `car`, `user-round`, `shield`, `sparkles`, `star`, `upload`. Icon size 16px in feature cards, 24px in larger contexts.

## Do's and Don'ts

**Do:**
- Use warm `surface` (#FFFFF7) as the default page background on marketing pages
- Keep teal (`primary`) for the single primary CTA per viewport section
- Use tight negative letter-spacing on headlines (`-0.01em` to `-0.03em`)
- Show product UI mockups/previews inside step and feature cards
- Lead copy with privacy outcomes: "privacy-safe", "GDPR", "anonymize", "no manual masking"
- Maintain WCAG AA contrast: `primary` on `white` passes; `on-surface-muted` on `white` for secondary text only
- Use the editorial grid borders and crosshair markers on full-width sections
- Apply subtle hover lifts on interactive cards (`translate-y`, `shadow-sm` → `shadow-md`)

**Don't:**
- Use pure `#FFFFFF` as page background — prefer warm `surface`
- Use star gold (`#F4C518`) outside of review ratings
- Mix more than two font families on a single screen (swissNow + baseNeue is the pair)
- Use heavy drop shadows or neon gradients — the aesthetic is calm and editorial
- Use red/error colors for non-error states
- Show stock "AI brain" imagery — prefer actual blur before/after comparisons and UI screenshots
- Promise server-side processing in copy — BGBlur runs in the browser with zero data retention
- Use pill-shaped buttons for primary CTAs — prefer `rounded-lg` to `rounded-xl`

---

*Extracted from [bgblur.com](https://www.bgblur.com) production styles. Tokens reflect the marketing site and editor UI as of 2026. Confirm font licensing (baseNeue, swissNow, Cal Sans) before use outside the BGBlur product.*
