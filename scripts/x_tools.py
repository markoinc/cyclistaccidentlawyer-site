#!/usr/bin/env python3
"""
X/Twitter Tools for Sierra
- Scrape for reading (free)
- API for posting (paid)
"""

import json
import subprocess
from requests_oauthlib import OAuth1Session

CREDS_PATH = '/home/ec2-user/.config/x-api/credentials.json'

def load_creds():
    with open(CREDS_PATH) as f:
        return json.load(f)

def get_oauth_session():
    """Get authenticated OAuth1 session for posting"""
    creds = load_creds()
    return OAuth1Session(
        creds['oauth1']['consumer_key'],
        client_secret=creds['oauth1']['consumer_secret'],
        resource_owner_key=creds['oauth1']['access_token'],
        resource_owner_secret=creds['oauth1']['access_token_secret']
    )

def post_tweet(text, reply_to=None):
    """Post a tweet using API"""
    oauth = get_oauth_session()
    payload = {"text": text}
    if reply_to:
        payload["reply"] = {"in_reply_to_tweet_id": reply_to}
    
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload
    )
    return response.json()

def get_me():
    """Get authenticated user info"""
    oauth = get_oauth_session()
    response = oauth.get("https://api.twitter.com/2/users/me")
    return response.json()

def scrape_search(query, count=20):
    """Scrape X search results (no API credits needed)"""
    # Use nitter or similar for scraping
    import urllib.parse
    encoded = urllib.parse.quote(query)
    # This would need a proper scraper setup
    return {"note": "Scraping setup needed - use browser tool or external scraper"}

def scrape_user_tweets(username, count=20):
    """Scrape a user's tweets"""
    return {"note": f"Would scrape @{username} - use browser tool"}

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: x_tools.py [me|tweet|search] [args]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "me":
        print(json.dumps(get_me(), indent=2))
    
    elif cmd == "tweet" and len(sys.argv) > 2:
        text = " ".join(sys.argv[2:])
        result = post_tweet(text)
        print(json.dumps(result, indent=2))
    
    elif cmd == "search" and len(sys.argv) > 2:
        query = " ".join(sys.argv[2:])
        print(scrape_search(query))
    
    else:
        print("Unknown command")
