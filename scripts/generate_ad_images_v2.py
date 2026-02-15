#!/usr/bin/env python3
"""
Generate MVA Ad Creative Images using Google Imagen API
Uses REST API directly for image generation
"""

import os
import sys
import time
import json
import base64
import requests
from pathlib import Path

# Get API key from environment
API_KEY = None
env_path = Path("/home/ec2-user/clawd/.env.local")
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if line.startswith("GEMINI_API_KEY="):
            API_KEY = line.split("=", 1)[1]
            break

if not API_KEY:
    print("Error: No GEMINI_API_KEY found")
    sys.exit(1)

# Output directory
OUTPUT_DIR = Path("/home/ec2-user/clawd/ads/mva-feb-2026-v4")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Ad prompts - simplified for Imagen
ADS = [
    {
        "name": "ad1-guarantee-hook",
        "prompt": "Professional B2B advertising image with dark charcoal background. Bold white text '7 CASES IN 30 DAYS' at top with blue glow. Below shows 'OR WE WORK FREE'. Calendar timeline graphic in center showing 30-day period with checkmarks. Bottom text 'That's not marketing. That's the deal.' Modern tech financial aesthetic, sharp corners, clean lines. Square format."
    },
    {
        "name": "ad2-price-breakdown",
        "prompt": "Professional B2B advertising infographic with dark charcoal background. Header 'THE REAL MATH' in white. Two column comparison: Left shows 'DIY LEADS' with costs adding up in red-amber ($20k, $4000+ crossed out). Right shows 'WE DELIVER' with '$3,000/case' highlighted in bright blue. Calculator visual aesthetic. Bottom text 'For $1k more, never touch intake again.' Square format."
    },
    {
        "name": "ad3-expose-style",
        "prompt": "Bold B2B advertising image with dark charcoal background. Red alert header 'YOUR VENDOR IS PLAYING YOU'. Flow diagram showing: Lead aggregator $50 to Vendor $300 splitting to multiple law firms. Large red '4X MARKUP' stamp. Blue contrast box 'OUR MODEL: One campaign = One firm'. Bottom: 'Stop being the product.' Sharp industrial aesthetic. Square format."
    },
    {
        "name": "ad4-model-problem",
        "prompt": "Professional B2B comparison graphic with dark charcoal background. Bold header 'IT'S NOT A LEAD PROBLEM. IT'S A MODEL PROBLEM.' Two columns: Left faded gray '2015 MODEL - Buy leads, Hope, Chase, Maybe sign'. Right highlighted blue '2026 MODEL - Buy outcomes, Receive signed cases, Litigate'. Arrow pointing to modern model. Bottom: 'Upgrade your model.' Square format."
    },
    {
        "name": "ad5-guarantee-hook-2",
        "prompt": "Professional B2B advertising image with dark charcoal background. Question header 'WHAT WOULD 7 SIGNED CASES DO FOR YOU?' Grid of 7 case file icons with blue checkmarks. Label 'DELIVERED IN 30 DAYS'. Below: 'Or we work free.' Stats bar at bottom: '8 FIGURES GENERATED | 87% RETENTION | $3K AVG/CASE' in blue. Square format."
    },
    {
        "name": "ad6-time-angle",
        "prompt": "Professional B2B advertising image with dark charcoal background. Header 'YOUR TIME ISN'T FREE' with draining clock icon. Two path comparison: Left in red shows tasks piling up 'Chase leads, Bad consultations, Dead follow-ups' with empty clock. Right in blue shows clean path 'Signed cases delivered' with full clock. Bottom: 'Get your time back. $3K/case'. Square format."
    },
    {
        "name": "ad7-emoji-attention",
        "prompt": "Bold B2B advertising image with dark charcoal background. Header 'STILL BUYING LEADS IN 2026?' with scales of justice icons. Two columns: Left with red X marks listing failures '100 leads, 85 dont qualify, etc'. Right with blue checkmarks listing wins 'We fund, We qualify, We sign'. High contrast. Bottom: '87% renew, $3K/case'. Square format."
    },
    {
        "name": "ad8-intake-defense",
        "prompt": "Professional B2B advertising image with dark charcoal background. Bold header 'YOUR INTAKE TEAM ISN'T THE PROBLEM'. Before/after visual: Left shows worker overwhelmed by 'JUNK LEADS' papers. Right shows same worker at clean desk with single 'SIGNED CASE' document in blue. Bottom: 'Stop handing them garbage.' Blue qualification checklist. Square format."
    },
    {
        "name": "ad9-comparison-angle",
        "prompt": "Professional B2B cost comparison chart with dark charcoal background. Header 'THE REAL COST COMPARISON'. Horizontal bar chart showing: TV ADS $50K/mo (tall red bar), BILLBOARDS $30K/mo (medium red bar), LEAD VENDORS $4K+/case (red bar), KURIOS $3K/case (short blue glowing bar with checkmark). Bottom: 'The math is simple.' Square format."
    }
]

def generate_with_imagen(prompt: str, name: str) -> Path:
    """Generate image using Imagen REST API"""
    print(f"\n🎨 Generating: {name}")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={API_KEY}"
    
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": "1:1",
            "safetyFilterLevel": "block_medium_and_above"
        }
    }
    
    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        
        if response.status_code != 200:
            print(f"   ❌ API Error: {response.status_code} - {response.text[:200]}")
            return None
            
        data = response.json()
        
        if "predictions" in data and len(data["predictions"]) > 0:
            image_data = data["predictions"][0].get("bytesBase64Encoded")
            if image_data:
                output_path = OUTPUT_DIR / f"{name}.png"
                with open(output_path, "wb") as f:
                    f.write(base64.b64decode(image_data))
                print(f"   ✅ Saved: {output_path}")
                return output_path
        
        print(f"   ❌ No image in response: {json.dumps(data)[:200]}")
        return None
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def generate_with_gemini_flash(prompt: str, name: str) -> Path:
    """Try Gemini 2.0 Flash with image output"""
    print(f"   🔄 Trying Gemini 2.0 Flash...")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": f"Generate a professional advertising image. {prompt}"
            }]
        }],
        "generationConfig": {
            "responseModalities": ["IMAGE", "TEXT"]
        }
    }
    
    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        
        if response.status_code != 200:
            print(f"   ❌ Gemini Error: {response.status_code}")
            return None
            
        data = response.json()
        
        # Extract image from response
        if "candidates" in data:
            for part in data["candidates"][0].get("content", {}).get("parts", []):
                if "inlineData" in part:
                    image_data = part["inlineData"].get("data")
                    if image_data:
                        output_path = OUTPUT_DIR / f"{name}.png"
                        with open(output_path, "wb") as f:
                            f.write(base64.b64decode(image_data))
                        print(f"   ✅ Saved (Gemini): {output_path}")
                        return output_path
        
        print(f"   ❌ No image from Gemini")
        return None
        
    except Exception as e:
        print(f"   ❌ Gemini Error: {e}")
        return None

def main():
    print("=" * 60)
    print("MVA Ad Creative Generator v2")
    print(f"Output directory: {OUTPUT_DIR}")
    print("=" * 60)
    
    generated = []
    failed = []
    
    for ad in ADS:
        result = generate_with_imagen(ad["prompt"], ad["name"])
        
        if not result:
            result = generate_with_gemini_flash(ad["prompt"], ad["name"])
        
        if result:
            generated.append(ad["name"])
        else:
            failed.append(ad["name"])
        
        # Rate limiting
        time.sleep(3)
    
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
