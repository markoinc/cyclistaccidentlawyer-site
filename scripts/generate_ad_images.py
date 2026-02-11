#!/usr/bin/env python3
"""Generate ad images using Gemini's Nano Banana image generation."""

import os
import base64
import json
import requests
from datetime import datetime

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyCqkgVGAm6Ki8jN4y42JXxe7Cy5EChGyHk')
OUTPUT_DIR = '/home/ec2-user/clawd/data/ad-images'

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Ad prompts - dark, professional, no warm colors, sharp corners
PROMPTS = {
    "ad1_quality_volume": """Near-black (#1A1A1A) background with subtle data visualization texture. TOP: "THE MATH YOUR VENDOR WON'T SHOW YOU" in white header. CENTER: Side-by-side calculator/breakdown displays. LEFT DISPLAY (labeled "LEAD MODEL"): "100 leads" in white, arrow down, "15 qualified" in amber, arrow down, "5 signed" in muted gray, "CPA: $4,000" stamped. RIGHT DISPLAY (labeled "OUR MODEL"): "100 prospects" in white, arrow down, "65 qualified" in #3399FF, arrow down, "25 signed" in #3399FF with glow, "CPA: $2,000" stamped. BOTTOM: "Same budget × We close = 5X signed cases" in white. Financial calculator aesthetic. Sharp angular design. DO NOT INCLUDE: rounded corners, warm colors, photos, soft gradients, emojis, human faces.""",
    
    "ad2_speed_wont_fix": """Near-black (#1A1A1A) background. TOP: "SPEED WON'T FIX THIS" in white header. CENTER: Stopwatch showing "30 SEC" with large red X overlaid. Arrow pointing to "STILL BAD LEAD" in muted red. BELOW: Flow diagram showing "Fast Call" → "Follow Up" → "Still No Case" — all crossed out in gray. ALTERNATIVE: Arrow bypassing to "QUALIFIED PROSPECT" → "SIGNED CASE" in #3399FF with glow. BOTTOM: "The problem isn't speed. It's source." in white. Technical diagnostic aesthetic. Sharp corners. DO NOT INCLUDE: rounded corners, warm colors, photos, soft gradients, emojis, human faces.""",
    
    "ad3_intake_problem": """Near-black (#1A1A1A) background. TOP: "DIAGNOSTIC: WHERE'S THE REAL PROBLEM?" in white technical header. CENTER: System flowchart. NODE 1: "LEAD SOURCE" with warning triangle, status "UNQUALIFIED INPUTS" in amber — highlighted as problem. Arrow to NODE 2: "WE QUALIFY" with checkmark in #3399FF. Arrow to NODE 3: "YOU CLOSE" with checkmark in #3399FF. DIAGNOSIS box pointing to Node 1: "PROBLEM IDENTIFIED" in amber. BOTTOM: "Before: Your team sorts garbage. After: Your team signs cases." in white. Sharp angular nodes. DO NOT INCLUDE: rounded corners, warm colors, photos, soft gradients, emojis, human faces.""",
    
    "ad4_burned_lawyer": """Near-black (#1A1A1A) background. TOP: "STOP GETTING BURNED" in white header with subtle flame icon crossed out. CENTER: Stack of crumpled receipts/invoices labeled "LEAD VENDOR" in grayscale, faded and worn. CONTRAST: Single clean document labeled "SIGNED CASE" in #3399FF with checkmark glow. Arrow from old stack pointing to new document. BOTTOM: "Different model. Different results." in white. Document comparison aesthetic. Sharp corners. DO NOT INCLUDE: rounded corners, warm colors, actual fire, soft gradients, emojis, human faces.""",
    
    "ad5_hidden_cost": """Near-black (#1A1A1A) background. TOP: "THE REAL COST OF CHEAP LEADS" in white header with calculator icon. CENTER: Two-column comparison. LEFT column: "$50 LEAD" with breakdown stacking up — "$50 lead + $100 intake + $200 attorney time + hidden costs = $800+ REAL COST" in escalating red-gray tones. RIGHT column: "$2,000 SIGNED CASE" in #3399FF — clean and simple, "TOTAL: $2,000" with checkmark. BOTTOM: "Which math works for you?" in white. Financial breakdown aesthetic. Sharp corners. DO NOT INCLUDE: rounded corners, warm colors, photos, soft gradients, emojis, human faces.""",
    
    "ad6_vendor_question": """Near-black (#1A1A1A) background. TOP: "ASK YOUR VENDOR THIS" in white header. CENTER: Large question mark in #3399FF. BELOW: Two contrasting boxes. LEFT BOX (gray outline): "THEIR MODEL" — "Paid per lead → No accountability → Volume over quality". RIGHT BOX (#3399FF outline): "OUR MODEL" — "Paid per case → We eat bad leads → Quality guaranteed". BOTTOM: "Aligned incentives. Aligned results." in white. Comparison contrast aesthetic. Sharp corners. DO NOT INCLUDE: rounded corners, warm colors, photos, soft gradients, emojis, human faces.""",
    
    "ad7_top_firms_quiet": """Deep charcoal (#1A1A1A) background. TOP: "THE SILENCE IS STRATEGIC" in bold white header with lock icon. CENTER: Dark-themed social media mockup showing "PI Marketing Discussion" group. Inside: Post previews like "Best lead vendors? 47 comments" with generic replies. OVERLAY: Large "DECOY" stamp in muted blue at angle. ANNOTATION: Arrow pointing with "Where average firms shop" in gray. BELOW: Dark box with #3399FF border showing "What top firms actually use: Signed cases from intake specialists" with lock icon, "LIMITED PER MARKET" badge. BOTTOM: "The best systems aren't crowdsourced." in white. Sharp corners. DO NOT INCLUDE: rounded corners, warm colors, real logos, photos, emojis, human faces."""
}

def generate_image(prompt: str, filename: str):
    """Generate image using Gemini's image generation."""
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={GEMINI_API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    
    data = {
        "contents": [{
            "parts": [{
                "text": f"Generate a 1080x1080 social media ad image. Style: Dark, professional, high contrast. {prompt}"
            }]
        }],
        "generationConfig": {
            "responseModalities": ["image", "text"],
            "imagePrecision": "high"
        }
    }
    
    print(f"Generating: {filename}...")
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        
        # Extract image from response
        if 'candidates' in result and len(result['candidates']) > 0:
            parts = result['candidates'][0].get('content', {}).get('parts', [])
            for part in parts:
                if 'inlineData' in part:
                    image_data = part['inlineData']['data']
                    mime_type = part['inlineData'].get('mimeType', 'image/png')
                    ext = 'png' if 'png' in mime_type else 'jpg'
                    
                    filepath = os.path.join(OUTPUT_DIR, f"{filename}.{ext}")
                    with open(filepath, 'wb') as f:
                        f.write(base64.b64decode(image_data))
                    
                    print(f"  ✓ Saved: {filepath}")
                    return filepath
        
        print(f"  ✗ No image in response for {filename}")
        print(f"  Response: {json.dumps(result, indent=2)[:500]}")
        return None
        
    except Exception as e:
        print(f"  ✗ Error generating {filename}: {e}")
        return None

def main():
    print(f"\n{'='*50}")
    print("NANO BANANA IMAGE GENERATION")
    print(f"{'='*50}\n")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Generating {len(PROMPTS)} images...\n")
    
    results = {}
    for name, prompt in PROMPTS.items():
        filepath = generate_image(prompt, name)
        results[name] = filepath
    
    print(f"\n{'='*50}")
    print("SUMMARY")
    print(f"{'='*50}")
    
    success = sum(1 for v in results.values() if v)
    print(f"Generated: {success}/{len(PROMPTS)}")
    
    for name, path in results.items():
        status = "✓" if path else "✗"
        print(f"  {status} {name}")
    
    return results

if __name__ == "__main__":
    main()
