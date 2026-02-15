# SOP: Nano Banana Image Generation

## Overview
Use Nano Banana (AI image generation API) to create ad creatives, social media images, and marketing visuals. Nano Banana produces high-quality, photorealistic images ideal for Meta ads and landing pages.

**Who this is for:** Anyone creating marketing visuals who has basic command line familiarity.

**Time to first image:** ~5 minutes once set up.

---

## ⚡ Prerequisites Check (DO THIS FIRST)

Before you can generate images, verify you have:

### 1. API Access
```bash
# Check if credentials file exists
cat ~/.config/nanobanana/credentials.json
```
**Expected output:** JSON with `api_key` field  
**If missing:** Contact Mark to get API access provisioned

### 2. Required Tools
```bash
# Check curl is installed
curl --version
```
**Expected:** Version info (e.g., `curl 7.68.0`)  
**If missing:** `sudo apt install curl` (Linux) or `brew install curl` (Mac)

```bash
# Check jq for JSON parsing (optional but helpful)
jq --version
```
**If missing:** `sudo apt install jq` or `brew install jq`

### 3. Environment Setup (One-Time)
```bash
# Load API key into environment variable
export NANO_API_KEY=$(cat ~/.config/nanobanana/credentials.json | jq -r '.api_key')

# Verify it worked
echo $NANO_API_KEY
```
**Expected:** Your API key string (starts with `nb_`)

### 4. Test Connection
```bash
curl -s -X GET "https://api.nanobanana.com/v1/models" \
  -H "Authorization: Bearer $NANO_API_KEY" | jq .
```
**Expected:** List of available models  
**If error:** Check API key is correct, check internet connection

### 5. Output Directory
```bash
# Create folder for generated images
mkdir -p ~/generated-images
cd ~/generated-images
```

✅ **All checks passed? You're ready to generate!**

---

## 1. Your First Image (Quick Start)

### Step-by-Step for Complete Beginners

**Step 1: Open your terminal**
- Mac: Press `Cmd + Space`, type "Terminal", press Enter
- Linux: Press `Ctrl + Alt + T`
- Windows: Use WSL or Git Bash

**Step 2: Set up environment** (do this each new terminal session)
```bash
export NANO_API_KEY=$(cat ~/.config/nanobanana/credentials.json | jq -r '.api_key')
cd ~/generated-images
```

**Step 3: Run your first generation**
```bash
curl -X POST "https://api.nanobanana.com/v1/generate" \
  -H "Authorization: Bearer $NANO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Professional headshot of confident business woman in her 30s, modern office background, warm natural lighting, wearing navy blazer, friendly smile, sharp focus, high quality commercial photography",
    "width": 1080,
    "height": 1080,
    "num_images": 1
  }' | jq .
```

**Step 4: Understand the response**
```json
{
  "id": "gen_abc123",
  "status": "completed",
  "images": [
    {
      "url": "https://cdn.nanobanana.com/images/abc123.png",
      "seed": 42
    }
  ],
  "credits_used": 1,
  "credits_remaining": 99
}
```

**Step 5: Download your image**
```bash
# Copy the URL from the response, then:
curl -o my-first-image.png "https://cdn.nanobanana.com/images/abc123.png"

# Open it (Mac)
open my-first-image.png

# Open it (Linux)
xdg-open my-first-image.png
```

🎉 **Congratulations! You generated your first AI image!**

---

## 2. Understanding Prompts (The Foundation)

### What is a Prompt?
A prompt is a text description that tells the AI what image to create. Think of it like giving detailed instructions to a photographer.

**Bad prompt (vague):**
> "A person in an office"

**Good prompt (specific):**
> "Professional photography, confident male lawyer in his 40s, modern law office with bookshelves, warm natural lighting from large window, wearing charcoal gray suit with burgundy tie, approachable smile, looking directly at camera, sharp focus, shallow depth of field, high quality commercial photography"

### The Prompt Formula
```
[Style] + [Subject] + [Setting] + [Lighting] + [Mood/Expression] + [Technical Details]
```

Every good prompt has these 6 components. Let's break them down:

---

## 3. Visual Style Guide (Detailed Descriptions)

### Photography Styles Explained

| Style | What It Looks Like | When to Use | Example Words |
|-------|-------------------|-------------|---------------|
| **Professional/Commercial** | Clean, polished, like you'd see in corporate materials | Business headshots, company websites | "professional photography", "commercial quality", "corporate" |
| **Editorial** | Magazine-quality, tells a story, artistic | Feature articles, brand storytelling | "editorial style", "magazine photography", "fashion editorial" |
| **Lifestyle** | Candid, natural, like real life moments | Social media, relatable ads | "lifestyle photography", "candid moment", "authentic" |
| **Documentary** | Raw, unposed, journalistic feel | Trust-building, testimonials | "documentary style", "journalistic", "unposed" |
| **Cinematic** | Movie-like, dramatic, high production | Brand videos, hero images | "cinematic", "film still", "movie scene" |
| **Studio** | Controlled lighting, clean backgrounds | Product shots, formal portraits | "studio photography", "controlled lighting", "seamless background" |
| **Minimalist** | Simple, lots of white space, clean | Modern tech brands, luxury | "minimalist", "clean", "simple composition" |

### Lighting Types Explained

| Lighting | Visual Effect | Mood Created | Example Words |
|----------|--------------|--------------|---------------|
| **Natural/Window** | Soft, realistic shadows, warm tones | Authentic, trustworthy | "natural lighting", "window light", "available light" |
| **Golden Hour** | Warm orange/yellow glow, long shadows | Aspirational, beautiful | "golden hour", "sunset lighting", "magic hour" |
| **Soft/Diffused** | Even, no harsh shadows | Friendly, professional | "soft lighting", "diffused light", "even illumination" |
| **Dramatic** | High contrast, deep shadows | Powerful, serious | "dramatic lighting", "chiaroscuro", "high contrast" |
| **Rim/Backlight** | Glowing edges around subject | Heroic, inspirational | "rim lighting", "backlit", "edge light" |
| **Studio** | Controlled, professional | Corporate, polished | "studio lighting", "three-point lighting" |

### Camera Angles Explained

| Angle | Visual Effect | Psychological Impact | When to Use |
|-------|--------------|---------------------|-------------|
| **Eye Level** | Neutral, natural | Relatable, equal | Default for most uses |
| **Slightly Below** | Subject looks powerful | Authority, confidence | Executive portraits |
| **Slightly Above** | Subject looks approachable | Friendly, open | Lifestyle, casual |
| **Wide Angle** | See more of scene | Context, environment | Establishing shots |
| **Close-Up** | Intimate, detailed | Connection, emotion | Testimonials, empathy |

### Technical Terms Decoded

| Term | What It Means | Visual Effect |
|------|--------------|---------------|
| **Shallow depth of field** | Background is blurry, subject is sharp | Focus on person, professional look |
| **Bokeh** | Pretty blurry circles from lights in background | Aesthetic, cinematic |
| **Sharp focus** | Everything crisp and clear | Professional, high quality |
| **4K/High resolution** | Very detailed image | Zooms well, print-ready |
| **Aspect ratio** | Shape of image (1:1 = square, 4:5 = portrait) | Fits platform requirements |
| **Composition** | How elements are arranged | Balance, visual flow |

---

## 4. Prompt Templates (25 Ready-to-Use)

### Category A: Legal / MVA (5 Templates)

#### A1. Lawyer Authority Portrait
```
Professional commercial photography, authoritative lawyer in their 50s with gray temples, standing in prestigious law library, floor-to-ceiling bookshelves with leather-bound legal volumes, wearing navy pinstripe suit and red power tie, arms confidently crossed, serious yet approachable expression, warm tungsten lighting mixed with natural window light, shallow depth of field, shot from slightly below eye level for authority, high resolution 4K quality, editorial magazine style
```

#### A2. Compassionate Client Meeting
```
Documentary style photography, empathetic female attorney listening intently to client, modern conference room with glass walls, soft diffused lighting, attorney wearing professional gray blazer, leaning forward showing engagement, genuine concern in expression, client partially visible from behind, candid unposed moment, authentic interaction, shallow depth of field focused on attorney's face, high quality commercial photography
```

#### A3. Legal Team Collaboration
```
Editorial lifestyle photography, diverse legal team of 4 attorneys reviewing documents around mahogany conference table, modern law firm setting, natural lighting from large windows, mix of ages and ethnicities, professional attire, engaged discussion, some standing some sitting, paperwork and laptops visible, authentic teamwork moment, wide angle composition, 4K resolution, commercial quality
```

#### A4. Courthouse Exterior (Context Shot)
```
Architectural photography, impressive stone courthouse building with classical columns, American flag waving, blue sky with dramatic clouds, golden hour warm lighting, wide angle establishing shot, people walking up steps in business attire, sense of justice and authority, high resolution, clean sharp focus throughout, editorial quality
```

#### A5. Recovery Success Story
```
Lifestyle photography, happy middle-aged man walking confidently in sunny park, recovered from injury, slight smile showing relief and gratitude, casual comfortable clothing, natural golden hour sunlight, green trees and path in soft focus background, authentic candid moment, warm color grading, sense of new beginning, high quality 4K resolution
```

### Category B: Business / B2B (5 Templates)

#### B1. Executive Leadership Portrait
```
Corporate photography, confident female CEO in her 40s, standing at floor-to-ceiling window overlooking city skyline, power pose with hands on hips, wearing tailored black suit, determined focused expression, dramatic natural lighting creating silhouette edge, modern minimalist office interior, shot from slightly below eye level, shallow depth of field, commercial quality, high resolution
```

#### B2. Sales Discovery Call
```
Lifestyle business photography, engaged sales professional on video call at modern desk setup, smiling warmly at laptop screen, professional casual attire, ring light reflection visible in eyes, organized workspace with plant and coffee cup, natural window light supplementing, authentic working moment, shallow depth of field on subject, 4K commercial quality
```

#### B3. Startup Team Energy
```
Editorial photography, enthusiastic startup team of 5 celebrating around standing desk, modern open office with exposed brick, casual tech attire (hoodies, jeans), genuine excited expressions, high-fiving and laughing, bright natural lighting, colorful but professional environment, candid authentic moment, wide angle to capture full scene, lifestyle brand photography
```

#### B4. Keynote Presentation
```
Event photography, confident speaker presenting on stage to audience, large screen with presentation visible behind, dramatic stage lighting with spotlight, professional conference setting, speaker gesturing expressively, audience silhouettes in foreground, cinematic wide angle shot, high contrast dramatic lighting, editorial documentary style, 4K resolution
```

#### B5. Strategic Planning Session
```
Corporate lifestyle photography, two executives reviewing strategy on whiteboard, modern glass-walled office, professional business attire, engaged collaborative discussion, one pointing at whiteboard content, natural window lighting, clean minimalist decor, authentic working moment, shot through glass for depth, shallow focus on subjects, commercial quality
```

### Category C: Healthcare / Medical (4 Templates)

#### C1. Compassionate Doctor Portrait
```
Professional medical photography, caring female doctor in white coat with stethoscope, modern medical office setting, warm approachable smile, hands clasped professionally, soft even lighting, clean organized background with subtle medical equipment, looking directly at camera, trustworthy and competent expression, shallow depth of field, commercial healthcare photography, high resolution
```

#### C2. Patient Consultation
```
Documentary healthcare photography, attentive physician explaining results to patient on tablet, modern examination room, soft diffused lighting, doctor making eye contact with patient, genuine empathetic expression, patient partially visible, clean medical environment, authentic caring moment, lifestyle medical photography, high quality 4K
```

#### C3. Medical Team
```
Corporate healthcare photography, diverse team of 4 medical professionals, doctors and nurses, modern hospital corridor, professional scrubs and white coats, confident smiles, standing together in V formation, clean bright lighting, teamwork and competence feeling, shallow depth of field, commercial medical photography, high resolution
```

#### C4. Wellness/Recovery
```
Lifestyle wellness photography, healthy senior woman doing gentle yoga in bright studio, natural sunlight streaming through windows, peaceful content expression, comfortable workout attire, clean minimal environment, sense of health and vitality, soft warm color tones, shallow depth of field, authentic wellness moment, 4K quality
```

### Category D: Real Estate / Property (3 Templates)

#### D1. Confident Realtor Portrait
```
Professional real estate photography, confident male realtor in his 40s, standing in front of beautiful home entrance, wearing smart casual blazer and open collar, welcoming smile with crossed arms, property visible behind, golden hour warm lighting, shallow depth of field, approachable yet professional, commercial real estate marketing, high resolution 4K
```

#### D2. Home Tour Moment
```
Lifestyle real estate photography, excited couple walking through spacious modern living room, natural light flooding through large windows, realtor visible in background, genuine happy expressions, contemporary home interior with neutral tones, candid house-hunting moment, wide angle to show space, bright airy feeling, commercial property photography
```

#### D3. Luxury Property Exterior
```
Architectural photography, stunning modern luxury home exterior at twilight, dramatic blue hour lighting, warm interior lights glowing through windows, manicured landscaping, contemporary design with clean lines, wide angle establishing shot, professional real estate photography, HDR quality, high resolution, aspirational lifestyle imagery
```

### Category E: E-commerce / Products (3 Templates)

#### E1. Lifestyle Product in Use
```
Lifestyle product photography, person using premium wireless headphones while working at cafe, natural window lighting, subject in casual stylish attire, product clearly visible but not posed, authentic usage moment, shallow depth of field focused on product, warm cozy cafe atmosphere in background, commercial product photography, high quality 4K
```

#### E2. Clean Product Hero Shot
```
Studio product photography, premium skincare bottle on clean white marble surface, soft diffused lighting from above, subtle shadows for depth, minimalist composition with small plant accent, product label clearly visible, professional cosmetics photography, high resolution macro detail, commercial advertising quality
```

#### E3. Unboxing Experience
```
Lifestyle e-commerce photography, hands opening premium subscription box, beautiful packaging visible, product contents partially revealed, clean desk surface, soft natural lighting from side, excitement and discovery feeling, shallow depth of field, Instagram-worthy aesthetic, commercial product photography, 4K quality
```

### Category F: Food & Restaurant (2 Templates)

#### F1. Hero Food Shot
```
Professional food photography, gourmet burger with melted cheese and fresh toppings on rustic wooden board, dark moody background, dramatic side lighting highlighting textures, steam rising subtly, shallow depth of field, rich saturated colors, appetizing composition, commercial restaurant photography, high resolution, magazine quality
```

#### F2. Restaurant Atmosphere
```
Lifestyle restaurant photography, happy couple enjoying dinner at upscale restaurant, warm ambient candlelight, engaged conversation, wine glasses on table, blurred bokeh background with other diners, intimate romantic atmosphere, genuine smiles, editorial dining photography, shallow depth of field, high quality commercial photography
```

### Category G: Fitness & Wellness (2 Templates)

#### G1. Training in Action
```
Dynamic fitness photography, athletic woman mid-workout doing kettlebell swing, modern gym environment, dramatic lighting highlighting muscle definition, determined focused expression, motion blur on weight suggesting power, sweat visible, authentic workout intensity, shallow depth of field, commercial sports photography, high resolution 4K
```

#### G2. Wellness Lifestyle
```
Lifestyle wellness photography, relaxed woman meditating in bright minimalist room, natural morning sunlight streaming in, peaceful serene expression, comfortable athleisure wear, plants and calm decor, sense of tranquility and self-care, soft warm color tones, commercial wellness brand photography, high quality 4K resolution
```

### Category H: Technology / SaaS (1 Template)

#### H1. Tech Product Demo
```
Commercial technology photography, person using sleek laptop showing SaaS dashboard, modern minimalist workspace, clean desk with single plant, soft even lighting, focused engaged expression, screen clearly visible with colorful interface, professional tech company aesthetic, shallow depth of field, commercial quality, high resolution 4K
```

---

## 5. Negative Prompts (What to Avoid)

Nano Banana doesn't use a separate negative prompt field, but you should avoid these in your prompts AND know what causes problems:

### ❌ Words/Concepts That Create Problems

| Avoid This | Why | What Happens |
|------------|-----|--------------|
| "text", "words", "lettering", "sign with text" | AI generates garbled, unreadable text | Gibberish letters, embarrassing results |
| "hands in focus", "showing hands clearly" | AI struggles with finger anatomy | Wrong number of fingers, weird positioning |
| "celebrity name", "famous person" | Legal issues + poor results | Generic face or copyright problems |
| "logo", "brand name", "Nike/Apple/etc" | Can't render trademarks accurately | Garbled logos, legal issues |
| "teeth" (in close-up) | Often renders dental issues | Crooked, too many, or weird teeth |
| "group of 10+ people" | Too many faces to render well | Face distortion, merged bodies |
| "complex patterns" (plaid, stripes close-up) | Moiré effects, pattern breaking | Glitchy, unrealistic patterns |

### ❌ Concepts That Trigger Poor Quality

| Avoid | Better Alternative |
|-------|-------------------|
| "nice photo" | "professional photography, commercial quality" |
| "good lighting" | "soft natural window lighting" (be specific) |
| "in an office" | "modern glass-walled office with city view" |
| "looking professional" | "confident expression, wearing tailored navy suit" |
| "high quality" alone | "high quality 4K resolution, sharp focus, commercial photography" |

### ❌ Structural Mistakes

| Mistake | Example | Why It's Bad |
|---------|---------|--------------|
| Too vague | "business person" | Could be anything |
| Too long (100+ words) | [wall of text] | AI loses focus, ignores parts |
| Contradictory | "dark moody bright cheerful" | Confusing, unpredictable results |
| Too many subjects | "lawyer, dog, car, building, crowd" | Nothing rendered well |
| Negative phrasing | "not ugly, not blurry, no bad lighting" | AI may include what you negate |

### ✅ Instead, Always Use Positive Phrasing

| ❌ Don't Say | ✅ Do Say |
|-------------|----------|
| "not blurry" | "sharp focus" |
| "no bad lighting" | "soft even lighting" |
| "avoid looking awkward" | "natural relaxed pose" |
| "not generic" | "unique authentic moment" |
| "don't make it dark" | "bright well-lit" |

---

## 6. Common Mistakes & How to Fix Them

### Mistake 1: Vague Subject Description
**Bad:**
> "A lawyer in an office"

**Why it fails:** No age, gender, expression, clothing, or specifics

**Good:**
> "Confident female lawyer in her 40s, silver streaked black hair, wearing tailored charcoal blazer, warm approachable smile"

---

### Mistake 2: Missing Lighting Instructions
**Bad:**
> "CEO portrait in office, professional look"

**Why it fails:** AI picks random lighting, often unflattering

**Good:**
> "CEO portrait in corner office, natural window light from left side creating soft shadows, warm golden hour tones, rim light separating from background"

---

### Mistake 3: No Style Reference
**Bad:**
> "Team meeting photo, people talking"

**Why it fails:** Could be stock photo style, candid, editorial, anything

**Good:**
> "Editorial lifestyle photography style, authentic candid team meeting, documentary feel, magazine quality"

---

### Mistake 4: Requesting Text
**Bad:**
> "Billboard showing 'Call Now 555-1234' text"

**Why it fails:** AI cannot render readable text reliably

**Good:**
> "Billboard in urban setting with blurred placeholder content" + add real text in Canva/Figma after

---

### Mistake 5: Overloading the Prompt
**Bad:**
> "Professional lawyer standing in prestigious law office with mahogany desk and leather chair and bookshelves full of legal books and diplomas on wall and city view through window and partner working at other desk and assistant bringing coffee and plant in corner and American flag and scales of justice statue and family photo on desk..."

**Why it fails:** Too many elements, AI can't prioritize, some get ignored or distorted

**Good:**
> "Professional lawyer standing in prestigious law office, mahogany desk and leather chair visible, bookshelves with legal books in background, warm lighting from window with city view, shallow depth of field focusing on subject"

---

### Mistake 6: Inconsistent Style Words
**Bad:**
> "Cinematic dramatic dark moody bright cheerful professional casual photo"

**Why it fails:** Contradictory instructions confuse the AI

**Good:**
> "Cinematic dramatic photography, high contrast lighting, confident powerful mood" (pick ONE direction)

---

## 7. Debugging Bad Outputs (Systematic Troubleshooting)

### Problem → Diagnosis → Fix

#### Problem: Faces Look Weird/Distorted
**Possible causes:**
1. Too many people in scene
2. Face too small in frame
3. Unusual angle requested

**Fixes to try:**
- Reduce number of people (max 4-5 for reliable faces)
- Add "portrait shot" or "close-up" for larger faces
- Use "eye level camera angle" for natural faces
- Add "realistic face, natural features" to prompt

---

#### Problem: Wrong Ethnicity/Age/Gender
**Cause:** Not specified or buried in prompt

**Fix:** Put demographic info EARLY in prompt
```
✅ "Professional photography, African American male executive in his 50s..."
❌ "Professional photography, executive in office... African American male in his 50s"
```

---

#### Problem: Looks Too "Stock Photo" / Generic
**Cause:** Missing authenticity keywords

**Fixes to add:**
- "candid moment"
- "authentic"
- "documentary style"
- "natural unposed"
- "lifestyle photography"
- "genuine expression"

---

#### Problem: Wrong Aspect Ratio / Composition
**Cause:** Didn't specify dimensions or framing

**Fix:** Always include:
1. Correct width/height in API call
2. Composition guidance: "portrait orientation", "centered subject", "rule of thirds"

---

#### Problem: Lighting Is Flat/Boring
**Cause:** No lighting direction specified

**Fixes to add:**
- Specify light SOURCE: "natural window light from left"
- Specify light QUALITY: "soft diffused" vs "dramatic harsh"
- Specify light MOOD: "warm golden" vs "cool blue"

---

#### Problem: Hands Look Wrong
**Cause:** AI hand anatomy is unreliable

**Fixes:**
1. Avoid hands in focus entirely
2. Use "arms crossed" (hides hands)
3. Use "hands in pockets"
4. Use "holding object" (less finger detail needed)
5. Crop hands out in post-processing

---

#### Problem: Image Looks Over-Processed/Fake
**Cause:** Too many enhancement keywords

**Fix:** Balance quality keywords with natural ones:
```
✅ "professional photography, natural skin texture, realistic lighting, authentic"
❌ "ultra HD 8K hyper-realistic perfect flawless airbrushed enhanced maximized"
```

---

## 8. Before/After Prompt Refinement Examples

### Example 1: Lawyer Portrait

**Version 1 (Weak) →**
> "Lawyer in office"

**Problems:** No style, no subject details, no lighting, no mood, no technical specs

**Version 2 (Better) →**
> "Professional lawyer, male, in modern office, looking confident"

**Problems:** Still vague on age, clothing, lighting, style, quality

**Version 3 (Good) →**
> "Professional photography, confident male lawyer in his 40s, modern law office with bookshelves, warm lighting, wearing navy suit, looking at camera, high quality"

**Problems:** Could be sharper on lighting direction, missing depth/background treatment

**Version 4 (Excellent) ✅ →**
> "Professional commercial photography, confident male lawyer in his mid-40s with distinguished salt-and-pepper hair, standing in modern law office, floor-to-ceiling bookshelves with legal volumes behind, warm natural lighting from large window on left side, wearing tailored navy suit with subtle pinstripe and burgundy tie, approachable yet authoritative smile, direct eye contact with camera, shallow depth of field with bokeh background, shot from slightly below eye level, high resolution 4K quality, editorial magazine style"

---

### Example 2: Team Photo

**Version 1 (Weak) →**
> "Business team photo"

**Version 2 (Better) →**
> "Group of business people in meeting room, professional"

**Version 3 (Good) →**
> "Professional photography, diverse business team of 4 people in modern conference room, engaged discussion, natural lighting, commercial quality"

**Version 4 (Excellent) ✅ →**
> "Editorial lifestyle photography, diverse business team of 4 professionals collaborating around modern white conference table, glass-walled meeting room with city view, mix of sitting and standing, engaged animated discussion with genuine expressions, natural window lighting creating soft shadows, professional smart-casual attire, candid authentic moment not posed, shallow depth of field, 4K commercial quality, magazine editorial style"

---

### Example 3: Product Lifestyle Shot

**Version 1 (Weak) →**
> "Coffee cup on desk"

**Version 2 (Better) →**
> "Premium coffee cup on nice desk, aesthetic photo"

**Version 3 (Good) →**
> "Lifestyle product photography, premium coffee cup on clean minimalist desk, morning light, shallow depth of field, Instagram aesthetic"

**Version 4 (Excellent) ✅ →**
> "Lifestyle product photography, premium ceramic coffee cup with latte art on clean Scandinavian minimalist desk, soft natural morning light streaming from left, subtle steam rising from cup, MacBook and small succulent plant in soft focus background, warm cozy work-from-home atmosphere, shallow depth of field focused on coffee cup, neutral warm color tones, Instagram-worthy aesthetic, commercial product photography, high resolution 4K"

---

## 9. Iteration Workflow (Step-by-Step)

### Phase 1: First Generation (Exploration)
```bash
# Generate 4 variations to see range
curl -X POST "https://api.nanobanana.com/v1/generate" \
  -H "Authorization: Bearer $NANO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "YOUR_PROMPT_HERE",
    "width": 1080,
    "height": 1080,
    "num_images": 4
  }' | jq .
```

**Review and rate each image:**
- ✅ Good composition, good face, good lighting
- ⚠️ Partial success (good parts to keep)
- ❌ Miss (identify what went wrong)

### Phase 2: Analyze What's Wrong

**Create a diagnosis checklist:**
- [ ] Face quality OK?
- [ ] Lighting matches intent?
- [ ] Background appropriate?
- [ ] Clothing/appearance correct?
- [ ] Mood/expression right?
- [ ] Technical quality (sharp, not grainy)?
- [ ] Composition works for ad placement?

### Phase 3: Refine Prompt

**Based on diagnosis, adjust ONE thing at a time:**

| Issue Found | Prompt Addition |
|-------------|-----------------|
| Face too harsh | Add "friendly approachable expression, soft features" |
| Lighting too flat | Add "dramatic side lighting, rim light" |
| Too stock-photo | Add "candid authentic moment, documentary style" |
| Wrong age | Move age description earlier, be more specific "mid-40s" |
| Background distracting | Add "shallow depth of field, blurred bokeh background" |

### Phase 4: Generate Refined Batch
```bash
# Generate 4 more with refined prompt
curl -X POST "https://api.nanobanana.com/v1/generate" \
  -H "Authorization: Bearer $NANO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "REFINED_PROMPT_HERE",
    "width": 1080,
    "height": 1080,
    "num_images": 4
  }' | jq .
```

### Phase 5: Select Winners
- Choose best 1-2 images
- Note the seed number for future variations
- Download at full resolution

### Phase 6: Create Variations (Optional)
Once you have a winner, create variations:
```bash
# Use same seed for consistency, tweak prompt slightly
curl -X POST "https://api.nanobanana.com/v1/generate" \
  -H "Authorization: Bearer $NANO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "SAME_PROMPT_WITH_MINOR_VARIATION",
    "width": 1080,
    "height": 1080,
    "num_images": 2,
    "seed": 42
  }' | jq .
```

**Variation ideas:**
- Same scene, different expression
- Same person, different outfit color
- Same concept, different demographic
- Same style, different time of day (lighting)

---

## 10. Image Specifications Reference

### Meta Ads Specs
| Placement | Dimensions | Aspect Ratio | Use Case |
|-----------|------------|--------------|----------|
| Feed (Square) | 1080 x 1080 | 1:1 | ✅ Primary - works everywhere |
| Feed (Portrait) | 1080 x 1350 | 4:5 | Takes more screen space |
| Stories/Reels | 1080 x 1920 | 9:16 | Full screen vertical |
| Carousel | 1080 x 1080 | 1:1 | Multi-image ads |
| Link Preview | 1200 x 628 | 1.91:1 | Click-through ads |

### Platform Quick Reference
| Platform | Recommended Size | Notes |
|----------|-----------------|-------|
| Meta Feed | 1080 x 1080 | Safe for all placements |
| Meta Stories | 1080 x 1920 | Full screen |
| LinkedIn | 1200 x 627 | Landscape preferred |
| Twitter/X | 1200 x 675 | 16:9 ratio |
| Email Header | 600 x 300 | Keep file small |
| Website Hero | 1920 x 1080 | 16:9 ratio |

### Recommended Workflow
1. **Generate at:** 1080 x 1080 (square) for most flexibility
2. **Crop to:** Other ratios as needed in post
3. **Export as:** PNG for quality, JPG for file size

---

## 11. Best Practices Summary

### ✅ DO:
- Be SPECIFIC about every element (lighting, expression, clothing, setting)
- Put most important descriptors FIRST (style, subject demographics)
- Include technical quality terms ("4K", "sharp focus", "commercial photography")
- Generate 4+ variations to choose from
- Save seed numbers of good generations
- Add style reference at start ("editorial photography", "lifestyle", etc.)
- Test prompts iteratively, changing ONE thing at a time

### ❌ DON'T:
- Request text/words in images (add in Canva later)
- Focus on hands (crop out or hide)
- Use celebrity names or brand logos
- Write prompts over 100 words (diminishing returns)
- Use negative phrasing ("not blurry" → "sharp focus")
- Mix contradictory styles ("dark moody bright cheerful")
- Generate just 1 image (always 2-4 minimum)

### 💡 PRO TIPS:
1. **Save your best prompts** in a template library
2. **Note seed numbers** of winners for consistent variations
3. **A/B test visual styles** across ad campaigns
4. **Check existing creative style** before generating new images for same brand
5. **Use reference images** to describe style (even though you can't upload them)

---

## 12. Complete API Reference

### Basic Generation
```bash
curl -X POST "https://api.nanobanana.com/v1/generate" \
  -H "Authorization: Bearer $NANO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Your detailed prompt here",
    "width": 1080,
    "height": 1080,
    "num_images": 4
  }'
```

### With Seed (Reproducible)
```bash
curl -X POST "https://api.nanobanana.com/v1/generate" \
  -H "Authorization: Bearer $NANO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Your prompt",
    "width": 1080,
    "height": 1080,
    "num_images": 1,
    "seed": 12345
  }'
```

### Response Format
```json
{
  "id": "gen_abc123xyz",
  "status": "completed",
  "created_at": "2026-02-12T10:30:00Z",
  "images": [
    {
      "url": "https://cdn.nanobanana.com/images/abc123.png",
      "seed": 12345
    }
  ],
  "credits_used": 4,
  "credits_remaining": 96,
  "prompt": "Your prompt here"
}
```

### Download Images Script
```bash
#!/bin/bash
# Save as download-images.sh

# Parse JSON response and download all images
response=$(curl -s -X POST "https://api.nanobanana.com/v1/generate" \
  -H "Authorization: Bearer $NANO_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"prompt\": \"$1\",
    \"width\": ${2:-1080},
    \"height\": ${3:-1080},
    \"num_images\": ${4:-4}
  }")

echo "$response" | jq -r '.images[].url' | while read url; do
  filename=$(basename "$url")
  echo "Downloading $filename..."
  curl -s -o "$filename" "$url"
done

echo "Done! Downloaded $(echo "$response" | jq '.images | length') images"
```

Usage:
```bash
chmod +x download-images.sh
./download-images.sh "Your prompt here" 1080 1080 4
```

---

## 13. Troubleshooting & FAQ

### "I get a 401 Unauthorized error"
```bash
# Check your API key is loaded
echo $NANO_API_KEY

# If empty, reload it
export NANO_API_KEY=$(cat ~/.config/nanobanana/credentials.json | jq -r '.api_key')
```

### "I get a 429 Too Many Requests error"
You've hit rate limits. Wait 60 seconds and try again. Consider:
- Batching requests (use num_images: 4)
- Spreading generations over time

### "Images are taking forever"
Normal generation takes 10-30 seconds. If longer:
- Check internet connection
- API may be under load, try again later

### "I can't find my downloaded images"
```bash
# Check current directory
pwd
ls -la *.png *.jpg

# Check downloads folder
ls ~/generated-images/
```

### "The image quality is low"
- Always generate at full resolution (1080+ px)
- Don't compress when downloading
- Check your prompt includes quality terms: "4K", "high resolution", "sharp focus"

### "Colors look different than expected"
Add color guidance to prompt:
- "warm color tones" / "cool blue tones"
- "high saturation vibrant colors" / "muted desaturated colors"
- "natural realistic colors"

---

## 14. Quick Reference Card (Print This)

### Prompt Formula
```
[Style] + [Subject] + [Setting] + [Lighting] + [Mood] + [Technical]
```

### Essential Quality Keywords
```
professional photography, commercial quality, 4K resolution, sharp focus, 
shallow depth of field, high resolution, editorial style
```

### Common Dimensions
```
Square: 1080 x 1080
Portrait: 1080 x 1350  
Story: 1080 x 1920
Landscape: 1200 x 628
```

### Quick Fixes
| Problem | Add to Prompt |
|---------|---------------|
| Too generic | "authentic candid moment, documentary style" |
| Bad lighting | "soft natural window light from left side" |
| Wrong expression | "warm genuine smile, approachable" |
| Background distracting | "shallow depth of field, bokeh background" |

### DON'T Include
❌ Text/words, hands in focus, celebrity names, logos, 100+ words

---

*Version 2.0 | Updated: 2026-02-12*
*Complete rewrite with prerequisites, templates, troubleshooting, and examples*
*For: Kurios Brand / MVA Lead Gen*
*Related: meta-campaign-full-workflow.md, meta-ads-creative-testing-playbook.md*
