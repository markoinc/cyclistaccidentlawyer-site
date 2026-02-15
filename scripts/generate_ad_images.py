#!/usr/bin/env python3
"""
Generate MVA Ad Creative Images using Google Gemini API
Uses Gemini 2.0 Flash for image generation (Nano Banana equivalent)
"""

import os
import sys
import time
from pathlib import Path

# Install required packages if not present
try:
    from google import genai
    from google.genai import types
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-genai", "-q"])
    from google import genai
    from google.genai import types

from PIL import Image
from io import BytesIO

# Get API key from environment
API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("NANOBANANA_API_KEY")
if not API_KEY:
    # Try loading from .env.local
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

# Ad prompts from cases-campaign-v2-ads.md (excluding nothing ads)
ADS = [
    {
        "name": "ad1-guarantee-hook",
        "prompt": """Near-black (#1A1A1A) background. TOP: Large "7 CASES IN 30 DAYS" in white with #3399FF glow effect. Below: "OR WE WORK FREE" in smaller white text. CENTER: Calendar/timeline graphic showing 30-day window with case icons filling in. Checkmark at day 30. BOTTOM: "That's not marketing. That's the deal." in white. Guarantee-focused aesthetic. Sharp corners. DO NOT INCLUDE: rounded corners, warm colors, photos, soft gradients, emojis."""
    },
    {
        "name": "ad2-price-breakdown",
        "prompt": """Near-black (#1A1A1A) background. TOP: "THE REAL MATH" in white header. CENTER: Two-column comparison. LEFT COLUMN "DIY LEADS": Calculator showing $20k spend, 15 cases, "$1,333" crossed out, "+intake salary +your time" added, final "REAL COST: $2,000+" in amber. RIGHT COLUMN "WE DELIVER": Clean "$3,000/case" in #3399FF with glow, checkmarks for "We fund ads" "We qualify" "We sign". BOTTOM: "For $1k more, never touch intake again." Sharp corners. DO NOT INCLUDE: rounded corners, warm colors, photos, soft gradients, emojis."""
    },
    {
        "name": "ad3-expose-style",
        "prompt": """Near-black (#1A1A1A) background. TOP: "YOUR VENDOR IS PLAYING YOU" in aggressive white font with red alert icon. CENTER: Flow diagram showing: "Aggregator $50" → "Vendor $300" → splits to "YOU + 3 OTHER FIRMS". Red "4X MARKUP" stamp. CONTRAST: Blue box below "OUR MODEL: One campaign = One firm = Your cases". BOTTOM: "Stop being the product." in white. Sharp corners. DO NOT INCLUDE: rounded corners, warm colors, photos, soft gradients."""
    },
    {
        "name": "ad4-model-problem",
        "prompt": """Near-black (#1A1A1A) background. TOP: "IT'S NOT A LEAD PROBLEM. IT'S A MODEL PROBLEM." in bold white. CENTER: Two models compared. LEFT (faded/gray): "2015 MODEL" — "Buy leads → Hope → Chase → Maybe sign". RIGHT (highlighted #3399FF): "2026 MODEL" — "Buy outcomes → Receive signed cases → Litigate". Arrow pointing to 2026 model. BOTTOM: "Upgrade your model." in white. Sharp corners. DO NOT INCLUDE: rounded corners, warm colors, photos, soft gradients, emojis."""
    },
    {
        "name": "ad5-guarantee-hook-2",
        "prompt": """Near-black (#1A1A1A) background. TOP: "WHAT WOULD 7 SIGNED CASES DO FOR YOU?" in white with question mark icon. CENTER: Stack of 7 case file icons with checkmarks, arranged in grid. Label: "DELIVERED IN 30 DAYS". Blue glow effect. Below: "Or we work free." BOTTOM: Stats row "8 FIGURES GENERATED | 87% RETENTION | $3K AVG/CASE" in #3399FF. Sharp corners. DO NOT INCLUDE: rounded corners, warm colors, photos, soft gradients, emojis."""
    },
    {
        "name": "ad6-time-angle",
        "prompt": """Near-black (#1A1A1A) background. TOP: "YOUR TIME ISN'T FREE" with clock icon draining. CENTER: Two paths. LEFT (red tint): Tasks stacking — "Chase leads" "Bad consultations" "Dead follow-ups" — clock running out. RIGHT (blue): Clean path — "Signed cases delivered" — clock full. BOTTOM: "Get your time back." with "$3K/case" in #3399FF. Sharp corners. DO NOT INCLUDE: rounded corners, warm colors, photos, soft gradients, emojis."""
    },
    {
        "name": "ad7-emoji-attention",
        "prompt": """Near-black (#1A1A1A) background. TOP: "STILL BUYING LEADS IN 2026?" in bold white with scales of justice icons. CENTER: Two columns with emoji-style icons. LEFT (red Xs): List of failures — "100 leads" "85 don't qualify" etc. RIGHT (blue checkmarks): List of wins — "We fund" "We qualify" "We sign". Large contrast. BOTTOM: "87% renew" with "$3K/case" in #3399FF. Sharp corners. This one can have emoji icons in the image. DO NOT INCLUDE: rounded corners, warm colors, photos, soft gradients."""
    },
    {
        "name": "ad8-intake-defense",
        "prompt": """Near-black (#1A1A1A) background. TOP: "YOUR INTAKE TEAM ISN'T THE PROBLEM" in bold white. CENTER: Intake worker icon buried under papers labeled "JUNK LEADS" — then arrow to same worker with clean desk and single "SIGNED CASE" document. Before/after style. BOTTOM: "Stop handing them garbage." Blue checkmarks for qualification criteria. Sharp corners. DO NOT INCLUDE: rounded corners, warm colors, photos of real people, soft gradients, emojis."""
    },
    {
        "name": "ad9-comparison-angle",
        "prompt": """Near-black (#1A1A1A) background. TOP: "THE REAL COST COMPARISON" in white header. CENTER: Horizontal bar chart. TV ADS: $50K/mo (very tall red bar). BILLBOARDS: $30K/mo (tall red bar). LEAD VENDORS: $4K+/case (medium red bar). KURIOS: $3K/case (short #3399FF bar with glow, checkmark). Clear winner visual. BOTTOM: "The math is simple." Sharp corners. DO NOT INCLUDE: rounded corners, warm colors, photos, soft gradients, emojis."""
    }
]

def generate_image(client, prompt: str, name: str) -> Path:
    """Generate a single image using Gemini"""
    print(f"\n🎨 Generating: {name}")
    print(f"   Prompt: {prompt[:100]}...")
    
    try:
        # Use gemini-2.0-flash-exp for image generation
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp-image-generation",
            contents=[f"Generate a professional advertising image for a law firm lead generation service. Square format (1:1 aspect ratio). {prompt}"],
            config=types.GenerateContentConfig(
                response_modalities=['Image'],
            )
        )
        
        # Extract image from response
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image = Image.open(BytesIO(part.inline_data.data))
                output_path = OUTPUT_DIR / f"{name}.png"
                image.save(output_path)
                print(f"   ✅ Saved: {output_path}")
                return output_path
        
        print(f"   ❌ No image in response")
        return None
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        
        # Try fallback to Imagen model
        try:
            print(f"   🔄 Trying Imagen fallback...")
            result = client.models.generate_image(
                model="imagen-3.0-generate-002",
                prompt=f"Professional advertising image for law firm lead generation. {prompt}",
                config=types.GenerateImageConfig(
                    number_of_images=1,
                    output_mime_type="image/png",
                    aspect_ratio="1:1"
                )
            )
            
            if result.generated_images:
                image = Image.open(BytesIO(result.generated_images[0].image.image_bytes))
                output_path = OUTPUT_DIR / f"{name}.png"
                image.save(output_path)
                print(f"   ✅ Saved (Imagen): {output_path}")
                return output_path
                
        except Exception as e2:
            print(f"   ❌ Imagen fallback also failed: {e2}")
        
        return None

def main():
    print("=" * 60)
    print("MVA Ad Creative Generator")
    print(f"Output directory: {OUTPUT_DIR}")
    print("=" * 60)
    
    # Initialize client
    client = genai.Client(api_key=API_KEY)
    
    generated = []
    failed = []
    
    for ad in ADS:
        result = generate_image(client, ad["prompt"], ad["name"])
        if result:
            generated.append(ad["name"])
        else:
            failed.append(ad["name"])
        
        # Rate limiting
        time.sleep(2)
    
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
