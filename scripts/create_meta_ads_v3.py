#!/usr/bin/env python3
"""
Create Meta Ads using asset_feed_spec (Advantage+ style)
This might bypass the page post restriction
"""

import json
import requests

# Config
ACCESS_TOKEN = "EAAUqZBPDvaVsBQukQGfd0fM1lbY31dkNE3RvM14QDLGzS0SorhNi2FFIybhs6tj23GEpuVcChhyqGmZBF5R4OnLzXXXbhZCMM0gYkJHbAxK2bcIqZBe1Dc4ZAwk2FyiJHnPOdikn1ZBF3x1LxTmpDeGuTOOo0u83SywIQrRRODfxcgJrBo8yZCbXveMfSVkkABeFStKZAtcIgibIlhZBfYjm4FYFXe0f0a6zAVYyl2ppP"
API_VERSION = "v21.0"
AD_ACCOUNT_ID = "act_1940929156491998"
AD_SET_ID = "120242085816600594"
PAGE_ID = "114085101675828"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

LANDING_URL = "https://cases.kuriosbrand.com"

# Test with just one ad first
AD_CONFIG = {
    "name": "AD01 - Quality Volume",
    "image_hash": "c10742c53b7cec624bfadca46eaf8ab5",
    "headline": "Quality Problems Hide as Volume",
    "primary_text": "You don't have a lead volume problem. You have a lead quality problem disguised as volume.\n\nYour vendor sends 100 MVA leads. Your intake qualifies 15. You sign 5.\n\n~$2,900 average cost per signed case.\n\nNo retainers. No setup fees. No ad spend required.",
}

def test_asset_feed():
    """Try using asset_feed_spec"""
    url = f"{BASE_URL}/{AD_ACCOUNT_ID}/adcreatives"
    
    full_url = f"{LANDING_URL}?utm_source=facebook&utm_medium=paid&utm_content=AD01"
    
    # Asset feed spec approach
    creative_data = {
        "name": "Test Asset Feed Creative",
        "asset_feed_spec": json.dumps({
            "images": [{
                "hash": AD_CONFIG["image_hash"]
            }],
            "bodies": [{
                "text": AD_CONFIG["primary_text"]
            }],
            "titles": [{
                "text": AD_CONFIG["headline"]
            }],
            "link_urls": [{
                "website_url": full_url
            }],
            "call_to_action_types": ["LEARN_MORE"],
            "ad_formats": ["SINGLE_IMAGE"]
        }),
        "degrees_of_freedom_spec": json.dumps({
            "creative_features_spec": {
                "standard_enhancements": {
                    "enroll_status": "OPT_OUT"
                }
            }
        }),
        "access_token": ACCESS_TOKEN
    }
    
    print("Testing asset_feed_spec approach...")
    response = requests.post(url, data=creative_data)
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    return result

def test_object_story_link():
    """Try using object_story_spec but with link object instead"""
    url = f"{BASE_URL}/{AD_ACCOUNT_ID}/adcreatives"
    
    full_url = f"{LANDING_URL}?utm_source=facebook&utm_medium=paid&utm_content=AD01"
    
    # Try with just the creative basics, no page post
    creative_data = {
        "name": "Test Link Creative",
        "title": AD_CONFIG["headline"],
        "body": AD_CONFIG["primary_text"][:250],
        "image_hash": AD_CONFIG["image_hash"],
        "link_url": full_url,
        "call_to_action_type": "LEARN_MORE",
        "access_token": ACCESS_TOKEN
    }
    
    print("\nTesting simple creative approach...")
    response = requests.post(url, data=creative_data)
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    return result

def test_ad_direct():
    """Try creating ad directly with inline creative"""
    url = f"{BASE_URL}/{AD_ACCOUNT_ID}/ads"
    
    full_url = f"{LANDING_URL}?utm_source=facebook&utm_medium=paid&utm_content=AD01"
    
    # Use page_id in creative without object_story_spec
    ad_data = {
        "name": "Test Ad Direct",
        "adset_id": AD_SET_ID,
        "creative": json.dumps({
            "title": AD_CONFIG["headline"],
            "body": AD_CONFIG["primary_text"][:250],
            "image_hash": AD_CONFIG["image_hash"],
            "link_url": full_url,
            "call_to_action_type": "LEARN_MORE"
        }),
        "status": "PAUSED",
        "access_token": ACCESS_TOKEN
    }
    
    print("\nTesting ad direct approach...")
    response = requests.post(url, data=ad_data)
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    return result

if __name__ == '__main__':
    test_asset_feed()
    test_object_story_link()
    test_ad_direct()
