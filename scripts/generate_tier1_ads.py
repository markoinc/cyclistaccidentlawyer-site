#!/usr/bin/env python3
"""Generate Tier 1 ad images using Nano Banana Pro image generation."""

import os
import sys
import base64
import json
import requests
import time

# Force unbuffered output
sys.stdout = sys.__stdout__
os.environ['PYTHONUNBUFFERED'] = '1'

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyCqkgVGAm6Ki8jN4y42JXxe7Cy5EChGyHk')
OUTPUT_DIR = '/home/ec2-user/clawd/projects/ad-creatives'

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Tier 1 Ad Prompts - All SQUARE 1:1 format
ADS = [
    {
        "filename": "ad01-quality-volume.png",
        "prompt": "Square 1:1 format. Near-black (#1A1A1A) background with subtle data visualization texture. TOP: 'THE MATH YOUR VENDOR DOESN'T SHOW YOU' in white header. CENTER: Side-by-side calculator displays. LEFT (LEAD MODEL): 100 leads → 15 qualified → 5 signed → CPA $4,000, 'YOU DO THE WORK' stamp in red. RIGHT (CLOSED CASE MODEL): 100 prospects → 65 qualified → 25 signed → CPA ~$3,000 in #3399FF with glow, 'WE DO THE WORK' stamp in blue. BOTTOM: 'Same budget × We close = 5X signed cases'. Financial calculator aesthetic, data visualization style. Sharp corners. DO NOT INCLUDE: rounded corners, warm colors, photos, soft gradients, emojis."
    },
    {
        "filename": "ad04-vendor-secret.png",
        "prompt": "Square 1:1 format. Near-black (#1A1A1A) background. TOP: 'THE VENDOR DIRTY SECRET' in bold white. CENTER: Split comparison. LEFT (red tint, 'SHARED LEADS'): Single lead icon splitting to 4 firm icons, labeled 'Same lead sold 4X', red X marks. RIGHT (blue tint, 'EXCLUSIVE LEADS'): Single lead to single firm with checkmark, 'One firm = one lead'. BOTTOM: Blue glowing box '1 CAMPAIGN = 1 FIRM'. Sharp corners. DO NOT INCLUDE: rounded corners, warm colors, photos, emojis."
    },
    {
        "filename": "ad07-rage-bait.png",
        "prompt": "Square 1:1 format. Near-black (#1A1A1A) background. TOP: 'YOUR LEAD VENDOR HOPES YOU NEVER READ THIS' in aggressive white font. CENTER: Calculator showing vendor math: '100 leads x $200 = $20,000' → '5 cases signed' → '$4,000 per case' in red. Contrast box: 'THEIR TAKE: $80,000 from 4 firms'. Arrow pointing to 'YOU ARE THE PRODUCT' stamp in red. BOTTOM: 'Stop being the product.' with '~$3K per signed case' in #3399FF. Exposé aesthetic. Sharp corners. DO NOT INCLUDE: rounded corners, warm colors, photos, emojis."
    },
    {
        "filename": "ad12-nothing-a.png",
        "prompt": "Square 1:1 format. Near-black (#1A1A1A) background, extremely minimal. Single line of clean white sans-serif text perfectly centered reading 'Stop Buying Leads. Start Receiving Cases.' Thin #3399FF underline beneath text. Very subtle grid/data texture in background, barely visible. Nothing else. Extreme minimalism. DO NOT INCLUDE: logos, decorations, images, icons."
    },
    {
        "filename": "ad13-nothing-b.png",
        "prompt": "Square 1:1 format. Near-black (#1A1A1A) background, extremely minimal. Single line of clean white sans-serif text perfectly centered reading 'PI Attorneys: Signed MVA Cases — $3k Avg' Thin #3399FF underline beneath text. Very subtle grid/data texture in background, barely visible. Nothing else. Extreme minimalism. DO NOT INCLUDE: logos, decorations, images, icons."
    },
    {
        "filename": "ad14-nothing-c.png",
        "prompt": "Square 1:1 format. Near-black (#1A1A1A) background, extremely minimal. Single line of clean white sans-serif text perfectly centered reading 'Signed MVA Cases Delivered' Thin #3399FF underline beneath text. Very subtle grid/data texture in background, barely visible. Nothing else. Extreme minimalism. DO NOT INCLUDE: logos, decorations, images, icons."
    }
]

def log(msg):
    print(msg, flush=True)

def generate_image_nano_banana(prompt: str, filename: str):
    """Generate image using Nano Banana Pro Preview model."""
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/nano-banana-pro-preview:generateContent?key={GEMINI_API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    
    data = {
        "contents": [{
            "parts": [{
                "text": f"Generate a 1080x1080 professional social media advertisement image. Square format. High quality, crisp details. {prompt}"
            }]
        }],
        "generationConfig": {
            "responseModalities": ["image", "text"]
        }
    }
    
    log(f"\n🍌 Generating: {filename}")
    log(f"   Prompt: {prompt[:80]}...")
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=120)
        
        if response.status_code != 200:
            log(f"   ❌ HTTP {response.status_code}: {response.text[:400]}")
            return None
        
        result = response.json()
        
        if 'candidates' in result and len(result['candidates']) > 0:
            parts = result['candidates'][0].get('content', {}).get('parts', [])
            for part in parts:
                if 'inlineData' in part:
                    image_data = part['inlineData']['data']
                    mime_type = part['inlineData'].get('mimeType', 'image/png')
                    
                    filepath = os.path.join(OUTPUT_DIR, filename)
                    with open(filepath, 'wb') as f:
                        f.write(base64.b64decode(image_data))
                    
                    size_kb = os.path.getsize(filepath) / 1024
                    log(f"   ✅ Saved: {filepath} ({size_kb:.1f} KB)")
                    return filepath
        
        log(f"   ❌ No image in response")
        log(f"   Response keys: {list(result.keys())}")
        return None
        
    except requests.exceptions.Timeout:
        log(f"   ❌ Timeout after 120s")
        return None
    except Exception as e:
        log(f"   ❌ Error: {type(e).__name__}: {e}")
        return None

def main():
    log("="*60)
    log("🍌 NANO BANANA PRO - TIER 1 AD GENERATION")
    log("="*60)
    log(f"Model: nano-banana-pro-preview")
    log(f"Output: {OUTPUT_DIR}")
    log(f"Generating {len(ADS)} ads...")
    
    results = []
    for i, ad in enumerate(ADS):
        filepath = generate_image_nano_banana(ad['prompt'], ad['filename'])
        results.append((ad['filename'], filepath))
        
        # Rate limiting between requests
        if i < len(ADS) - 1:
            log("   ⏳ Waiting 3s...")
            time.sleep(3)
    
    log("\n" + "="*60)
    log("📊 GENERATION SUMMARY")
    log("="*60)
    
    success = sum(1 for _, path in results if path)
    log(f"Generated: {success}/{len(ADS)}\n")
    
    for filename, path in results:
        status = "✅" if path else "❌"
        log(f"  {status} {filename}")
    
    if success > 0:
        log(f"\n📁 Files saved to: {OUTPUT_DIR}")
    
    return results

if __name__ == "__main__":
    main()
