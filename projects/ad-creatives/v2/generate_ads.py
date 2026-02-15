#!/usr/bin/env python3
"""Generate all Meta ad images using Nano Banana Pro (Gemini 3 Pro Image)"""

import os
import base64
import requests
import json
import time

API_KEY = "AIzaSyCqkgVGAm6Ki8jN4y42JXxe7Cy5EChGyHk"
OUTPUT_DIR = "/home/ec2-user/clawd/projects/ad-creatives/v2"
MODEL = "gemini-3-pro-image-preview"  # Nano Banana Pro

MASTER_STYLE = """Square 1:1 format, 1024x1024 pixels. Near-black (#1A1A1A) background with subtle tech grid/data visualization texture. Bold white sans-serif headline at TOP. Digital counter displays for any numbers (LCD calculator style). Red color (#FF3333) for bad/problem elements with crossed-out or stamp effects. Blue (#3399FF) glow for good/solution elements. Silhouette illustration style, NOT realistic photos. Clear white tagline at BOTTOM. Sharp corners, tech/fintech aesthetic. DO NOT include: rounded corners, warm colors, realistic photos, emojis, soft gradients, human faces."""

ADS = [
    {
        "filename": "ad02-intake-defense.png",
        "prompt": f"""Generate a Meta advertisement image. {MASTER_STYLE}

Headline at top in bold white text: "YOUR INTAKE ISN'T THE PROBLEM"

Visual: Split screen composition. LEFT side shows a silhouette of an office worker overwhelmed, buried under an avalanche of papers falling on them, each paper labeled "JUNK LEADS" in red text. Papers are chaotic and messy. RIGHT side shows the same worker silhouette but with a clean, organized desk with just one single document glowing blue, labeled "SIGNED CASE" with a blue checkmark. 

The contrast should be stark - chaos vs clarity, red vs blue.

Tagline at bottom in white text: "Stop blaming downstream for upstream problems."
"""
    },
    {
        "filename": "ad03-speed-myth.png",
        "prompt": f"""Generate a Meta advertisement image. {MASTER_STYLE}

Headline at top in bold white text: "SPEED WON'T FIX BAD LEADS"

Visual: Center shows a large speedometer icon with a big red X crossing through it. Below it, a funnel shape filled with debris, trash, and unqualified text labels. Around the crossed-out speedometer, three red X callout boxes with text: "Faster dialer", "Better scripts", "More follow-ups" - all marked as ineffective.

At the bottom, a clean blue arrow flowing smoothly from left to right, representing the solution - bypassing the broken funnel entirely.

Tagline at bottom in white text: "Stop fixing the funnel. Remove it entirely."
"""
    },
    {
        "filename": "ad04-vendor-secret.png",
        "prompt": f"""Generate a Meta advertisement image. {MASTER_STYLE}

Headline at top in bold white text: "THE VENDOR DIRTY SECRET"

Visual: Split comparison diagram. LEFT side (red tinted): Shows one lead icon at top splitting into 4 arrows pointing to 4 different law firm building icons. A red stamp overlay reads "SHARED 4X". This side looks chaotic and bad.

RIGHT side (blue glow): Shows one lead icon connecting with a single arrow to one law firm icon. Blue checkmark beside it. Text label "EXCLUSIVE". This side is clean and highlighted as the solution.

A vertical dividing line separates the two sides.

Tagline at bottom in white text: "1 Campaign = 1 Firm"
"""
    },
    {
        "filename": "ad05-roi-simple.png",
        "prompt": f"""Generate a Meta advertisement image. {MASTER_STYLE}

Headline at top in bold white text: "$3,000 PER SIGNED MVA CASE"

Visual: Three-step horizontal process flow with LCD digital display style numbers. 
Step 1 box: "We Fund Ads" with dollar icon
Step 2 box: "We Qualify & Close" with filter icon  
Step 3 box: "You Receive Signed Cases" - this one glows blue and is highlighted

Below the steps, a large LCD calculator-style display showing "$3,000/case" with a blue checkmark next to it.

Arrows connect each step, flowing left to right.

Tagline at bottom in white text: "Predictable cost. Predictable cases."
"""
    },
    {
        "filename": "ad06-top-firms.png",
        "prompt": f"""Generate a Meta advertisement image. {MASTER_STYLE}

Headline at top in bold white text: "WHY TOP FIRMS NEVER SHARE THEIR SOURCES"

Visual: Top portion shows a mockup of a social media post/forum thread with text "Best PI Lead Vendors?" and faded, blurry reply comments below it. A gray/faded stamp overlay reads "DECOY" diagonally across it.

Below this, a blue-bordered box with solid styling contains text: "What top firms use: Private systems." This box has a subtle blue glow and looks premium/exclusive.

The contrast is between the public crowdsourced advice (bad) vs private exclusive systems (good).

Tagline at bottom in white text: "The best systems aren't crowdsourced."
"""
    },
    {
        "filename": "ad07-rage-bait.png",
        "prompt": f"""Generate a Meta advertisement image. {MASTER_STYLE}

Headline at top in bold white text: "YOUR VENDOR HOPES YOU NEVER READ THIS"

Visual: Large calculator/LCD display showing the math breakdown:
"100 leads × $200 = $20,000" 
Arrow pointing down to:
"5 cases signed"
Arrow pointing down to:
"$4,000/case" - displayed in RED as the bad outcome

Below this calculation, another line: "Their take: $80,000 from 4 firms" 
A large red stamp diagonally across reads "YOU'RE THE PRODUCT"

The whole visual exposes the vendor business model critically.

Tagline at bottom in white text: "Stop being the product."
"""
    },
    {
        "filename": "ad08-fomo.png",
        "prompt": f"""Generate a Meta advertisement image. {MASTER_STYLE}

Headline at top in bold white text: "YOUR COMPETITORS ALREADY KNOW"

Visual: Simplified US map silhouette in the center. Various states/markets are colored: some in GREEN with "TAKEN" labels, others in BLUE with "AVAILABLE" labels. Shows territorial exclusivity concept.

A digital clock/timer icon in the corner suggests urgency - time running out.

The map should show roughly half markets as taken (green) and half as still available (blue).

Tagline at bottom in white text: "One firm per market. When it's taken, it's taken."
"""
    },
    {
        "filename": "ad09-time-angle.png",
        "prompt": f"""Generate a Meta advertisement image. {MASTER_STYLE}

Headline at top in bold white text: "YOUR TIME IS WORTH MORE THAN SORTING LEADS"

Visual: Two parallel paths/timelines. LEFT path (red, negative): Shows a clock with fading/draining time, with stacked boxes labeled "Sort leads" → "Chase duds" → "Bad consultations" - representing wasted time. Clock is partially empty.

RIGHT path (blue, positive): Shows a full, glowing clock with a clean direct arrow to a single box labeled "Signed cases delivered" - efficient, no wasted steps.

The left path is cluttered and time-consuming, the right path is streamlined and valuable.

Tagline at bottom in white text: "Buy back your time."
"""
    },
    {
        "filename": "ad10-comparison.png",
        "prompt": f"""Generate a Meta advertisement image. {MASTER_STYLE}

Headline at top in bold white text: "THE REAL COST COMPARISON"

Visual: Horizontal bar chart with 4 bars stacked vertically:
1. "TV ADS: $50K/mo" - longest bar, RED color
2. "BILLBOARDS: $30K/mo" - medium-long bar, RED color  
3. "LEAD VENDORS: $4K+/case" - shorter bar, RED color
4. "KURIOS: $3K/case" - shortest bar, BLUE glow, with a checkmark

Each bar clearly labeled with the channel and cost. The comparison shows KURIOS as the clear winner with lowest cost and best value (blue glow and checkmark).

Tagline at bottom in white text: "The math is simple."
"""
    },
    {
        "filename": "ad12-nothing-a.png",
        "prompt": f"""Generate a Meta advertisement image. {MASTER_STYLE}

MINIMAL DESIGN - mostly dark background with subtle tech grid texture.

Centered large bold white text: "Stop Buying Leads. Start Receiving Cases."

A thin blue (#3399FF) underline beneath the text, about 60% of the text width.

No other visual elements. Clean, stark, impactful. The text is the entire message.

Very minimal, text-focused design with high contrast.
"""
    },
    {
        "filename": "ad13-nothing-b.png",
        "prompt": f"""Generate a Meta advertisement image. {MASTER_STYLE}

MINIMAL DESIGN - mostly dark background with subtle tech grid texture.

Centered large bold white text: "PI Attorneys: Signed MVA Cases — $3k Avg"

A thin blue (#3399FF) underline beneath the text, about 60% of the text width.

No other visual elements. Clean, stark, impactful. The text is the entire message.

Very minimal, text-focused design with high contrast.
"""
    },
    {
        "filename": "ad14-nothing-c.png",
        "prompt": f"""Generate a Meta advertisement image. {MASTER_STYLE}

MINIMAL DESIGN - mostly dark background with subtle tech grid texture.

Centered large bold white text: "Signed MVA Cases Delivered"

A thin blue (#3399FF) underline beneath the text, about 60% of the text width.

No other visual elements. Clean, stark, impactful. The text is the entire message.

Very minimal, text-focused design with high contrast.
"""
    }
]

def generate_image(prompt, filename):
    """Generate image using Nano Banana Pro (Gemini 3 Pro Image)"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
    
    # Use responseModalities without responseMimeType for image generation
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["IMAGE", "TEXT"]
        }
    }
    
    headers = {"Content-Type": "application/json"}
    
    print(f"Generating {filename}...")
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=180)
        
        if response.status_code == 200:
            result = response.json()
            # Extract image from response
            if "candidates" in result:
                for candidate in result["candidates"]:
                    if "content" in candidate and "parts" in candidate["content"]:
                        for part in candidate["content"]["parts"]:
                            if "inlineData" in part:
                                img_data = part["inlineData"].get("data")
                                mime_type = part["inlineData"].get("mimeType", "image/png")
                                if img_data:
                                    img_bytes = base64.b64decode(img_data)
                                    filepath = os.path.join(OUTPUT_DIR, filename)
                                    with open(filepath, "wb") as f:
                                        f.write(img_bytes)
                                    size_kb = len(img_bytes) / 1024
                                    print(f"  ✓ Saved: {filename} ({size_kb:.1f} KB)")
                                    return True, size_kb
        
        print(f"  ✗ Failed: {filename} - {response.status_code}: {response.text[:300]}")
        return False, 0
    except Exception as e:
        print(f"  ✗ Error: {filename} - {str(e)}")
        return False, 0

def main():
    print(f"Generating {len(ADS)} ads with Nano Banana Pro (Gemini 3 Pro Image)...\n")
    
    results = []
    for ad in ADS:
        success, size = generate_image(ad["prompt"], ad["filename"])
        results.append({"file": ad["filename"], "success": success, "size_kb": size})
        time.sleep(3)  # Rate limit between requests
    
    print("\n" + "="*50)
    print("GENERATION COMPLETE")
    print("="*50)
    
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    
    print(f"\n✓ Successful: {len(successful)}/{len(results)}")
    for r in successful:
        print(f"  - {r['file']}: {r['size_kb']:.1f} KB")
    
    if failed:
        print(f"\n✗ Failed: {len(failed)}")
        for r in failed:
            print(f"  - {r['file']}")
    
    total_size = sum(r["size_kb"] for r in successful)
    print(f"\nTotal size: {total_size:.1f} KB ({total_size/1024:.2f} MB)")

if __name__ == "__main__":
    main()
