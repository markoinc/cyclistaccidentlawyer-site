# UGC-Style Creatives for Ads: Fast Iterations With Consistent Models Using Nano Banana

**Source:** https://skywork.ai/blog/how-to-create-ugc-style-ad-creatives-nano-banana-guide/
**Type:** Comprehensive Workflow Guide
**Focus:** Creating authentic UGC-style ad creatives for Meta/TikTok

## Overview

If you need to crank out UGC-style ad creatives that look authentic and keep the same person consistent across dozens of shots, this guide walks you through a fast, repeatable workflow using Nano Banana.

- **Difficulty:** Intermediate (you can be a marketer, not a designer)
- **Time:** 60–90 minutes for your first 12–24 variants; 20–30 minutes per new batch once dialed
- **Requirements:** 1–3 clear reference photos, access to Nano Banana, a basic graphics tool for overlays, and ad accounts for Meta/TikTok

## Why this works

Nano Banana's underlying model focuses on identity consistency and scene preservation, enabling local edits (pose, outfit, prop) while keeping facial features and backgrounds intact.

---

## Step 1 — Define Your Creative Hypotheses and Constraints

Start with a tight mini-brief so your batches have purpose.

### Angles to try (pick 3–5):
- Problem/relief
- Quick demo
- Testimonial
- Before/after
- Objection-busting
- Social proof

### Define:
- **Target persona:** who they are, what hurts, what outcome they want
- **Brand cues:** colors, tone, must-have props, logo usage rules
- **Platform specs:** vertical 9:16 first; add 1:1 for feeds

### Checkpoint (pass/fail):
- Each angle has one clear promise (headline) and one visual idea (pose/prop/background)
- You listed exactly 2–3 variables you'll test first (e.g., hook line, background color, pose)

**Tip:** Start with two hooks and one pose per angle so you can attribute wins quickly.

---

## Step 2 — Prepare Reference Assets for Consistency

Your reference photo set determines how well the identity locks.

### Do this:
- Capture 1–3 high-resolution, watermark-free images of the person, front or 3/4 view, neutral lighting, uncluttered background
- Include at least one shot where the subject holds or is near your product
- Gather brand props (bottle, box), color swatches, and logo files

### Avoid:
- Extreme angles, heavy makeup or filters, sunglasses, or busy lighting
- Low-res or compressed images that smear facial features

### Folder structure:
`/01_References, /02_Batches, /03_Selects, /04_Finals`

---

## Step 3 — Nano Banana Setup and Identity Lock

Load your best reference and generate a first batch that prioritizes identity fidelity and a natural UGC look.

### Prompt Template:

```
Same person as reference, [pose], [expression], wearing [outfit], in [setting]; preserve background style; natural lighting; smartphone camera look; photorealistic. Minimal retouching. High detail face.

Negative: no extra fingers, no warped text, no watermark, no double face.
```

### Steps:
1. Import the top reference into Nano Banana. Choose identity/consistency or one-shot edit mode
2. Generate 6–12 variants with modest diversity. Keep background and styling similar to reference
3. Star or bucket by likeness and scene fidelity

### Checkpoint (be strict):
- **Likeness:** ≥90% by human judgment. Eyes, nose, mouth alignment, face shape, skin tone, and hairstyle match
- **Scene:** Background composition feels the same; only intended variable changed

**If likeness drifts:** Re-upload your best result as new reference, tighten prompt: "identical facial features as reference; maintain background unchanged."

---

## Step 4 — Scene-Preserving Edits and Prop/Pose Swaps

Iterate on hooks and visuals while holding identity constant.

### Variation ideas:
- **Hooks:** pointing at overlay text; holding product near face; "react" face; before/after split
- **Variables to change one at a time:** outfit color, backdrop color, hand pose, camera distance, prop orientation

### Prompt additions:

```
Same identity as reference, identical facial features; change only [outfit color to pastel blue] and [pose: pointing at text overlay], keep background unchanged; smartphone camera slight grain.
```

### Artifact prevention:
- **Hands:** Avoid intricate finger interlocks; prefer simple gestures
- **Over-polish:** Add "smartphone camera, slight grain, natural lighting" and remove "studio lighting" cues

**Tip:** Batch small—6 to 12 images—and promote only the top 2–3 per angle to composition.

---

## Step 5 — Composition and Export

Compose quickly and stay native to the platform vibe.

### For images:
- Add headline-style overlays that read like subtitles; use 1–2 emojis sparingly
- Keep text within safe zones
- Use brand colors for borders or callouts, but keep the UGC feel

### For video slideshows:
- Assemble 3–5 frames with snappy cuts
- Add VO or trend-aligned audio natively in TikTok or Reels

### Export specs:
- **Aspect ratios:** 9:16 first (1080×1920); also 1:1 (1080×1080). Keep sRGB
- **Formats:** JPG/PNG for images; MP4 (H.264 + AAC) for video

### Device preview checkpoint:
Test on iOS and Android phones. Make sure overlays don't collide with platform UI.

---

## Step 6 — Launch and Test

Keep tests clean so you can trust the read.

### Design:
- Change one variable per batch (e.g., hook line, background color, pose)
- Hold identity, composition, and copy constant
- 3–6 creatives per ad set/ad group
- Run long enough to gather 1,000–2,000 impressions per creative, or 3–5 days for an early directional read

### Platform setups:
- **Meta:** Start with broad targeting, Advantage+ placements, and CBO for faster learning
- **TikTok:** Vertical assets, trend-aligned audio, and automatic reach expansion

### Metrics to watch:
- **Early indicators:** thumb-stop rate and first 3-second view rate (video), CTR, CPC
- Use your account medians as the real bar

### Decision gates:
- Pause creatives materially below your account's median CTR after sufficient impressions
- Promote winners that beat median CTR by ≥20% or reduce CPC materially

---

## Step 7 — Iterate and Scale

Scale what works; re-mix one variable at a time to extend winners.

- **Budget scaling:** Increase by 20–30% every 24–48 hours on winners; avoid drastic jumps
- **Fatigue watch:** Retire assets when CTR drops ~20% week-over-week or frequency exceeds ~3–4 without improved ROAS
- **Naming/versioning:** Use a schema you can scan quickly

### Example naming:
`Brand_Angle_V1-HookA-Pose2_BGblue_2025-09-14`

**Learning log:** Keep a simple doc with "What changed, What happened, What we'll try next."

---

## Troubleshooting: Fast Fixes

### Character drift across variants
Re-upload the best likeness as the new reference; tighten prompt with "identical facial features; preserve background; same skin tone and hair details."

### Hands or prop artifacts
Simplify the gesture; crop tighter; or generate a separate product close-up and composite.

### Overly polished (not UGC)
Add "smartphone camera, slight grain, natural lighting; mild motion blur; no studio lighting." Use everyday backgrounds.

### Scene changes unexpectedly
Add "preserve background style" or edit from the best frame in one-shot mode.

### Watermarks or platform rejections
Ensure references and outputs are watermark-free and that overlays avoid unrealistic claims.

---

## Verification Checklists

### Pre-export (image/video):
- Identity likeness: Eyes, nose, mouth alignment match best reference
- Artifact scan: 100–200% zoom on hands, jewelry, edges, and text
- Composition: Overlay text inside safe zones; legible on 6.1-inch phone

### Export settings:
- 9:16 at 1080×1920; 1:1 at 1080×1080; sRGB
- JPG/PNG for images, MP4 H.264 + AAC for video

### Pre-launch QA:
- Device previews on iOS and Android; check UI collisions
- Policy: No watermarks; no exaggerated claims; branding appropriate
- UTM or naming conventions applied

### Early read (after 1,000–2,000 impressions per creative):
- Video: thumb-stop rate, first 3-second view rate
- All: CTR, CPC vs. account medians

### Scale/kill rules:
- Scale winners +20–30% budget every 24–48h if CTR ≥ +20% vs. median
- Kill underperformers; document "change → outcome → next move"

---

## FAQ

**Do I need multiple references?** One strong reference can work, but 2–3 from similar lighting helps stabilize features.

**Can I swap backgrounds?** Yes, but if identity starts drifting, revert to scene-preserving edits.

**How many variants per batch?** Start with 6–12. Promote only the top 2–3; then remix a single variable.

**What file type gets better reach?** Platforms don't favor a type blindly; they favor engagement. Keep specs compliant and test.
