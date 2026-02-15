#!/usr/bin/env python3
"""
Fix all ads: Create new creatives with clean URLs, update ads with clean creatives + ad-level URL params
"""

import json
import requests
import os

# Config
ACCESS_TOKEN = json.load(open(os.path.expanduser('~/.config/meta-ads/credentials.json')))['access_token']
AD_ACCOUNT_ID = "act_1940929156491998"
PAGE_ID = "114085101675828"
BASE_URL = "https://graph.facebook.com/v21.0"
LANDING_URL = "https://cases.kuriosbrand.com"

# Load ad config
with open('/home/ec2-user/clawd/data/mva-ads-config-final.json') as f:
    config = json.load(f)

# Load created ads
with open('/home/ec2-user/clawd/data/mva-ads-created.json') as f:
    created_ads = json.load(f)

# Map ad names to IDs
ad_name_to_id = {ad['name']: ad['ad_id'] for ad in created_ads}

# Image hashes from previous uploads
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

def create_clean_creative(ad_config):
    """Create creative with clean URL (no UTM params)"""
    url = f"{BASE_URL}/{AD_ACCOUNT_ID}/adcreatives"
    
    image_hash = IMAGE_HASHES.get(ad_config['name'])
    
    # Build link_data with CLEAN URL
    link_data = {
        "link": LANDING_URL,  # Clean URL - no UTMs!
        "name": ad_config['headline'],
        "description": ad_config.get('description', ''),
        "call_to_action": {
            "type": "LEARN_MORE",
            "value": {"link": LANDING_URL}
        }
    }
    
    # Add image if exists
    if image_hash:
        link_data["image_hash"] = image_hash
    
    # Add primary text if exists
    if ad_config.get('primary_text'):
        link_data["message"] = ad_config['primary_text']
    
    object_story_spec = {
        "page_id": PAGE_ID,
        "link_data": link_data
    }
    
    response = requests.post(url, data={
        "access_token": ACCESS_TOKEN,
        "name": f"Creative - {ad_config['name']} - Clean URL",
        "object_story_spec": json.dumps(object_story_spec)
    })
    
    result = response.json()
    if 'error' in result:
        print(f"  ❌ Creative error: {result['error'].get('error_user_msg', result['error'].get('message'))}")
        return None
    return result.get('id')

def update_ad_with_clean_creative_and_params(ad_id, creative_id, ad_name):
    """Update ad with new creative and ad-level URL params"""
    url = f"{BASE_URL}/{ad_id}"
    
    # Clean ad name for UTM
    utm_content = ad_name.replace(' ', '_').replace('-', '_')
    utm_params = f"utm_source=facebook&utm_medium=paid&utm_campaign=MVA_Lead_Gen_Feb_2026&utm_content={utm_content}"
    
    response = requests.post(url, data={
        "access_token": ACCESS_TOKEN,
        "creative": json.dumps({"creative_id": creative_id}),
        "url_tags": utm_params
    })
    
    result = response.json()
    if 'error' in result:
        print(f"  ❌ Ad update error: {result['error'].get('error_user_msg', result['error'].get('message'))}")
        return False
    return result.get('success', False)

def main():
    print("=" * 60)
    print("FIXING ALL ADS: Clean URLs + Ad-Level UTM Params")
    print("=" * 60)
    
    success_count = 0
    
    for ad_config in config['ads']:
        ad_name = ad_config['name']
        ad_id = ad_name_to_id.get(ad_name)
        
        if not ad_id:
            print(f"\n⚠️ {ad_name}: No ad ID found, skipping")
            continue
        
        print(f"\n{ad_name}:")
        
        # Create new creative with clean URL
        print("  Creating clean creative...")
        creative_id = create_clean_creative(ad_config)
        
        if not creative_id:
            continue
        
        print(f"  ✅ Creative: {creative_id}")
        
        # Update ad with new creative and URL params
        print("  Updating ad...")
        if update_ad_with_clean_creative_and_params(ad_id, creative_id, ad_name):
            print("  ✅ Ad updated with clean URL + UTM params")
            success_count += 1
        else:
            print("  ❌ Failed to update ad")
    
    print("\n" + "=" * 60)
    print(f"COMPLETE: {success_count}/{len(config['ads'])} ads fixed")
    print("=" * 60)

if __name__ == '__main__':
    main()
