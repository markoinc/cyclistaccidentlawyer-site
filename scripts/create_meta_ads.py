#!/usr/bin/env python3
"""
Create Meta Ads with images and UTM tracking
"""

import json
import requests
import sys
import os
import base64

# Config
ACCESS_TOKEN = "EAAUqZBPDvaVsBQukQGfd0fM1lbY31dkNE3RvM14QDLGzS0SorhNi2FFIybhs6tj23GEpuVcChhyqGmZBF5R4OnLzXXXbhZCMM0gYkJHbAxK2bcIqZBe1Dc4ZAwk2FyiJHnPOdikn1ZBF3x1LxTmpDeGuTOOo0u83SywIQrRRODfxcgJrBo8yZCbXveMfSVkkABeFStKZAtcIgibIlhZBfYjm4FYFXe0f0a6zAVYyl2ppP"
API_VERSION = "v21.0"
AD_ACCOUNT_ID = "act_1940929156491998"
AD_SET_ID = "120242085816600594"
PAGE_ID = "114085101675828"  # Kurios page
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

LANDING_URL = "https://cases.kuriosbrand.com"
UTM_TEMPLATE = "utm_source=facebook&utm_medium=paid&utm_campaign=MVA_Lead_Gen_Feb_2026&utm_content={ad_name}"

def upload_image(image_path):
    """Upload image to Meta Ad Account using multipart form, return image hash"""
    url = f"{BASE_URL}/{AD_ACCOUNT_ID}/adimages"
    
    filename = os.path.basename(image_path)
    
    # Use multipart form-data with file upload
    with open(image_path, 'rb') as f:
        files = {
            'filename': (None, filename),
        }
        data = {
            'access_token': ACCESS_TOKEN,
        }
        # Send the actual file
        response = requests.post(
            url,
            data=data,
            files={filename: (filename, f, 'image/png')}
        )
    
    result = response.json()
    
    if 'error' in result:
        print(f"Error uploading {filename}: {result['error']}")
        return None
    
    # Extract hash from response
    images = result.get('images', {})
    for key, val in images.items():
        return val.get('hash')
    
    print(f"Unexpected response for {filename}: {result}")
    return None

def create_ad_creative(ad_config, image_hash=None):
    """Create ad creative with image or link-only"""
    url = f"{BASE_URL}/{AD_ACCOUNT_ID}/adcreatives"
    
    # Build URL with UTM
    ad_name_clean = ad_config['name'].replace(' ', '_').replace('-', '_')
    full_url = f"{LANDING_URL}?{UTM_TEMPLATE.format(ad_name=ad_name_clean)}"
    
    # Build object_story_spec
    if image_hash and ad_config.get('primary_text'):
        # Image ad with copy
        link_data = {
            "image_hash": image_hash,
            "link": full_url,
            "message": ad_config['primary_text'],
            "name": ad_config['headline'],
            "description": ad_config.get('description', ''),
            "call_to_action": {
                "type": ad_config.get('cta', 'LEARN_MORE'),
                "value": {"link": full_url}
            }
        }
    else:
        # Link-only ad (nothing style)
        link_data = {
            "link": full_url,
            "name": ad_config['headline'],
            "description": ad_config.get('description', ''),
            "call_to_action": {
                "type": ad_config.get('cta', 'LEARN_MORE'),
                "value": {"link": full_url}
            }
        }
    
    creative_data = {
        "name": f"Creative - {ad_config['name']}",
        "object_story_spec": json.dumps({
            "page_id": PAGE_ID,
            "link_data": link_data
        }),
        "access_token": ACCESS_TOKEN
    }
    
    response = requests.post(url, data=creative_data)
    result = response.json()
    
    if 'error' in result:
        print(f"Error creating creative for {ad_config['name']}: {result['error']}")
        return None
    
    return result.get('id')

def create_ad(ad_config, creative_id):
    """Create the actual ad"""
    url = f"{BASE_URL}/{AD_ACCOUNT_ID}/ads"
    
    ad_data = {
        "name": ad_config['name'],
        "adset_id": AD_SET_ID,
        "creative": json.dumps({"creative_id": creative_id}),
        "status": "PAUSED",
        "access_token": ACCESS_TOKEN
    }
    
    response = requests.post(url, data=ad_data)
    result = response.json()
    
    if 'error' in result:
        print(f"Error creating ad {ad_config['name']}: {result['error']}")
        return None
    
    return result.get('id')

def main():
    # Load config
    with open('/home/ec2-user/clawd/data/mva-ads-config-final.json', 'r') as f:
        config = json.load(f)
    
    ads_created = []
    
    for ad in config['ads']:
        print(f"\n{'='*50}")
        print(f"Processing: {ad['name']}")
        
        image_hash = None
        
        # Upload image if present
        if ad.get('image_path') and os.path.exists(ad['image_path']):
            print(f"  Uploading image: {os.path.basename(ad['image_path'])}")
            image_hash = upload_image(ad['image_path'])
            if image_hash:
                print(f"  ✅ Image uploaded: {image_hash}")
            else:
                print(f"  ❌ Image upload failed")
                continue
        elif ad.get('link_only'):
            print(f"  📎 Link-only ad (no image)")
        
        # Create creative
        print(f"  Creating creative...")
        creative_id = create_ad_creative(ad, image_hash)
        if creative_id:
            print(f"  ✅ Creative created: {creative_id}")
        else:
            print(f"  ❌ Creative creation failed")
            continue
        
        # Create ad
        print(f"  Creating ad...")
        ad_id = create_ad(ad, creative_id)
        if ad_id:
            print(f"  ✅ Ad created: {ad_id}")
            ads_created.append({
                'name': ad['name'],
                'ad_id': ad_id,
                'creative_id': creative_id,
                'image_hash': image_hash
            })
        else:
            print(f"  ❌ Ad creation failed")
    
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
