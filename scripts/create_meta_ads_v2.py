#!/usr/bin/env python3
"""
Create Meta Ads without object_story_spec (using existing image hashes)
Uses adcreative without page post to bypass development mode restrictions
"""

import json
import requests
import sys
import os

# Config
ACCESS_TOKEN = "EAAUqZBPDvaVsBQukQGfd0fM1lbY31dkNE3RvM14QDLGzS0SorhNi2FFIybhs6tj23GEpuVcChhyqGmZBF5R4OnLzXXXbhZCMM0gYkJHbAxK2bcIqZBe1Dc4ZAwk2FyiJHnPOdikn1ZBF3x1LxTmpDeGuTOOo0u83SywIQrRRODfxcgJrBo8yZCbXveMfSVkkABeFStKZAtcIgibIlhZBfYjm4FYFXe0f0a6zAVYyl2ppP"
API_VERSION = "v21.0"
AD_ACCOUNT_ID = "act_1940929156491998"
AD_SET_ID = "120242085816600594"
PAGE_ID = "114085101675828"  # Kurios page
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

LANDING_URL = "https://cases.kuriosbrand.com"
UTM_TEMPLATE = "utm_source=facebook&utm_medium=paid&utm_campaign=MVA_Lead_Gen_Feb_2026&utm_content={ad_name}"

# Image hashes from previous upload
IMAGE_HASHES = {
    "AD01 - Quality Volume": "c10742c53b7cec624bfadca46eaf8ab5",
    "AD02 - Intake Defense": "9152f0cba9aa946d20ade7223205f4a8",
    "AD04 - Vendor Secret": "f1e13bf4f9770b8a6e893c33763aa954",
    "AD05 - ROI Simple": "7e3af445a03999dc8660057f3a2f78c1",
    "AD07 - Rage Bait": "17ebccec923c4117fd22c4a125b12a02",
    "AD10 - Comparison": "2c44047d60cf8717871ccd07a428198d",
    "AD11 - Burnout": "723b6b51a46282e6c3ffdcead72cae81",
    "V2-01 - Guarantee Hook": "846c0637a639386bea3b033528ac1391",
    "V2-03 - Expose Style": "8c3fcdb8a287410b799ca67435c4e8f0",
    "V2-05 - Guarantee Hook 2": "631530ddcf42622d8aa243206db1c3eb",
    "11A - Case Study Timeline": "d99d5dc8a805abc04077887776ced782",
    "11B - Case Study Math": "ad45e0513a509dbcdc2caf371a9c047e",
    "11C - Case Study FOMO": "c349397fd8bf11c86550433bc8d96913",
}

def create_ad_with_creative(ad_config, image_hash=None):
    """Create ad directly using ad creative spec"""
    url = f"{BASE_URL}/{AD_ACCOUNT_ID}/ads"
    
    # Build URL with UTM
    ad_name_clean = ad_config['name'].replace(' ', '_').replace('-', '_')
    full_url = f"{LANDING_URL}?{UTM_TEMPLATE.format(ad_name=ad_name_clean)}"
    
    # Build creative spec inline
    if image_hash:
        creative = {
            "object_story_spec": {
                "page_id": PAGE_ID,
                "link_data": {
                    "image_hash": image_hash,
                    "link": full_url,
                    "message": ad_config.get('primary_text', ''),
                    "name": ad_config['headline'],
                    "call_to_action": {
                        "type": "LEARN_MORE",
                        "value": {"link": full_url}
                    }
                }
            }
        }
    else:
        creative = {
            "object_story_spec": {
                "page_id": PAGE_ID,
                "link_data": {
                    "link": full_url,
                    "name": ad_config['headline'],
                    "call_to_action": {
                        "type": "LEARN_MORE",
                        "value": {"link": full_url}
                    }
                }
            }
        }
    
    ad_data = {
        "name": ad_config['name'],
        "adset_id": AD_SET_ID,
        "creative": json.dumps(creative),
        "status": "PAUSED",
        "access_token": ACCESS_TOKEN
    }
    
    response = requests.post(url, data=ad_data)
    result = response.json()
    
    if 'error' in result:
        return None, result['error']
    
    return result.get('id'), None

def main():
    # Load config
    with open('/home/ec2-user/clawd/data/mva-ads-config-final.json', 'r') as f:
        config = json.load(f)
    
    ads_created = []
    
    for ad in config['ads']:
        print(f"\n{'='*50}")
        print(f"Processing: {ad['name']}")
        
        # Get image hash
        image_hash = IMAGE_HASHES.get(ad['name'])
        if not image_hash and not ad.get('link_only'):
            print(f"  ⚠️ No image hash found, skipping")
            continue
        
        # Create ad
        print(f"  Creating ad...")
        ad_id, error = create_ad_with_creative(ad, image_hash)
        if ad_id:
            print(f"  ✅ Ad created: {ad_id}")
            ads_created.append({
                'name': ad['name'],
                'ad_id': ad_id,
                'image_hash': image_hash
            })
        else:
            print(f"  ❌ Failed: {error}")
    
    # Summary
    print(f"\n{'='*50}")
    print(f"SUMMARY: {len(ads_created)}/{len(config['ads'])} ads created")
    print(f"{'='*50}")
    
    for ad in ads_created:
        print(f"✅ {ad['name']}: {ad['ad_id']}")
    
    # Save results
    with open('/home/ec2-user/clawd/data/mva-ads-created.json', 'w') as f:
        json.dump(ads_created, f, indent=2)
    
    print(f"\nResults saved to /home/ec2-user/clawd/data/mva-ads-created.json")

if __name__ == '__main__':
    main()
