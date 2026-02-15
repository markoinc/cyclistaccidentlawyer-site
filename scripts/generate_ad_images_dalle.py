#!/usr/bin/env python3
"""
Generate MVA Ad Creative Images using OpenAI DALL-E 3
"""

import os
import sys
import time
import requests
from pathlib import Path

# Get API key
API_KEY = None
env_path = Path("/home/ec2-user/clawd/.env.local")
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if line.startswith("OPENAI_API_KEY="):
            API_KEY = line.split("=", 1)[1]
            break

if not API_KEY:
    print("Error: No OPENAI_API_KEY found")
    sys.exit(1)

# Output directory
OUTPUT_DIR = Path("/home/ec2-user/clawd/ads/mva-feb-2026-v4")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Ad prompts optimized for DALL-E 3
ADS = [
    {
        "name": "ad1-guarantee-hook",
        "prompt": "Professional B2B advertising graphic with dark charcoal (#1A1A1A) background. Bold typography at top reading '7 CASES IN 30 DAYS' in white with electric blue (#3399FF) glow effect. Below in smaller white text: 'OR WE WORK FREE'. Center shows a clean 30-day calendar/timeline graphic with document icons filling in progressively. Blue checkmark at day 30. Bottom text: 'That's not marketing. That's the deal.' Modern fintech/SaaS aesthetic with sharp corners, data visualization style. Square format, professional infographic design."
    },
    {
        "name": "ad2-price-breakdown", 
        "prompt": "Professional B2B cost comparison infographic on dark charcoal (#1A1A1A) background. Header 'THE REAL MATH' in bold white. Two columns side by side: LEFT column labeled 'DIY LEADS' shows calculator with red-amber numbers ($20,000 spend, struck-through '$1,333', 'REAL COST: $2,000+'). RIGHT column labeled 'WE DELIVER' shows clean '$3,000/case' in bright blue (#3399FF) with glow, checkmarks for 'We fund ads', 'We qualify', 'We sign'. Bottom: 'For $1k more, never touch intake again.' Sharp data visualization aesthetic, square format."
    },
    {
        "name": "ad3-expose-style",
        "prompt": "Bold B2B advertising graphic on dark charcoal (#1A1A1A) background. Red alert icon at top with bold white text 'YOUR VENDOR IS PLAYING YOU'. Center shows flow diagram: 'Aggregator $50' arrow to 'Vendor $300' which splits to multiple icons representing law firms. Large red 'X4 MARKUP' stamp overlay. Below in blue (#3399FF) box: 'OUR MODEL: One campaign = One firm = Your cases'. Bottom: 'Stop being the product.' Industrial tech aesthetic, sharp corners, square format."
    },
    {
        "name": "ad4-model-problem",
        "prompt": "Professional B2B comparison graphic on dark charcoal (#1A1A1A) background. Bold header 'IT'S NOT A LEAD PROBLEM. IT'S A MODEL PROBLEM.' Two columns: LEFT shows faded gray '2015 MODEL' with flowchart 'Buy leads → Hope → Chase → Maybe sign'. RIGHT shows highlighted blue (#3399FF) '2026 MODEL' with clean flowchart 'Buy outcomes → Receive signed cases → Litigate'. Arrow pointing to modern model. Bottom: 'Upgrade your model.' Clean tech aesthetic, square format."
    },
    {
        "name": "ad5-guarantee-hook-2",
        "prompt": "Professional B2B advertising graphic on dark charcoal (#1A1A1A) background. Header with question mark icon: 'WHAT WOULD 7 SIGNED CASES DO FOR YOU?' Center shows clean grid of 7 case file/folder icons with blue (#3399FF) checkmarks. Label: 'DELIVERED IN 30 DAYS' with blue glow. Below: 'Or we work free.' Stats bar at bottom: '8 FIGURES GENERATED | 87% RETENTION | $3K AVG/CASE' in blue. Modern dashboard aesthetic, square format."
    },
    {
        "name": "ad6-time-angle",
        "prompt": "Professional B2B advertising graphic on dark charcoal (#1A1A1A) background. Header 'YOUR TIME ISN'T FREE' with clock icon. Split comparison: LEFT (red/gray tint) shows clock draining with task icons stacking: 'Chase leads', 'Bad consultations', 'Dead follow-ups'. RIGHT (blue tint) shows full clock with clean path: 'Signed cases delivered'. Bottom: 'Get your time back. $3K/case' in blue (#3399FF). Time management infographic style, square format."
    },
    {
        "name": "ad7-emoji-attention",
        "prompt": "Bold B2B advertising graphic on dark charcoal (#1A1A1A) background. Header 'STILL BUYING LEADS IN 2026?' with scales of justice icons. Two columns with high contrast: LEFT shows red X marks with failure list '100 leads, 85 don't qualify, 10 already have lawyer'. RIGHT shows blue (#3399FF) checkmarks with success list 'We fund, We qualify, We sign, You receive cases'. Bottom: '87% renew | $3K/case'. Bold typography, comparison style, square format."
    },
    {
        "name": "ad8-intake-defense",
        "prompt": "Professional B2B advertising graphic on dark charcoal (#1A1A1A) background. Bold header 'YOUR INTAKE TEAM ISN'T THE PROBLEM'. Before/after visual: LEFT shows overwhelmed office worker icon buried under stack of papers labeled 'JUNK LEADS'. RIGHT shows same worker at clean desk with single document labeled 'SIGNED CASE' in blue (#3399FF) glow. Arrow between them. Bottom: 'Stop handing them garbage.' Blue qualification checklist. Corporate infographic style, square format."
    },
    {
        "name": "ad9-comparison-angle",
        "prompt": "Professional B2B cost comparison bar chart on dark charcoal (#1A1A1A) background. Header 'THE REAL COST COMPARISON' in white. Horizontal bar chart showing: TV ADS '$50K/mo' (tallest red bar), BILLBOARDS '$30K/mo' (medium red bar), LEAD VENDORS '$4K+/case' (shorter red bar), KURIOS '$3K/case' (shortest bar, blue #3399FF with glow and checkmark). Clear visual winner. Bottom: 'The math is simple.' Financial dashboard aesthetic, square format."
    }
]

def generate_image(prompt: str, name: str) -> Path:
    """Generate image using DALL-E 3"""
    print(f"\n🎨 Generating: {name}")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024",
        "quality": "standard",
        "response_format": "url"
    }
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers=headers,
            json=payload,
            timeout=120
        )
        
        if response.status_code != 200:
            print(f"   ❌ API Error: {response.status_code} - {response.text[:300]}")
            return None
            
        data = response.json()
        
        if "data" in data and len(data["data"]) > 0:
            image_url = data["data"][0].get("url")
            if image_url:
                # Download the image
                img_response = requests.get(image_url, timeout=60)
                if img_response.status_code == 200:
                    output_path = OUTPUT_DIR / f"{name}.png"
                    with open(output_path, "wb") as f:
                        f.write(img_response.content)
                    print(f"   ✅ Saved: {output_path}")
                    
                    # Also save the revised prompt
                    revised_prompt = data["data"][0].get("revised_prompt", "")
                    if revised_prompt:
                        prompt_path = OUTPUT_DIR / f"{name}_prompt.txt"
                        with open(prompt_path, "w") as f:
                            f.write(f"Original: {prompt}\n\nRevised: {revised_prompt}")
                    
                    return output_path
        
        print(f"   ❌ No image in response")
        return None
        
    except requests.exceptions.Timeout:
        print(f"   ❌ Request timed out")
        return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def main():
    print("=" * 60)
    print("MVA Ad Creative Generator - DALL-E 3")
    print(f"Output directory: {OUTPUT_DIR}")
    print("=" * 60)
    
    generated = []
    failed = []
    
    for ad in ADS:
        result = generate_image(ad["prompt"], ad["name"])
        
        if result:
            generated.append(ad["name"])
        else:
            failed.append(ad["name"])
        
        # Rate limiting - DALL-E has strict limits
        if result:
            print("   ⏳ Waiting 15s for rate limit...")
            time.sleep(15)
        else:
            time.sleep(5)
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"✅ Generated: {len(generated)}")
    for name in generated:
        print(f"   - {name}")
    
    if failed:
        print(f"\n❌ Failed: {len(failed)}")
        for name in failed:
            print(f"   - {name}")
    
    print(f"\n📁 Output: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
