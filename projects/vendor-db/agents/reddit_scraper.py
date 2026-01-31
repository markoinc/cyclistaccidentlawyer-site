#!/usr/bin/env python3
"""
Reddit Scraper Agent - Gathers PI attorney discussions about lead vendors
"""

import json
import time
import requests
from datetime import datetime
from pathlib import Path

DATA_DIR = Path("/home/ec2-user/clawd/projects/vendor-db/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Subreddits to monitor
SUBREDDITS = [
    "LawFirm",
    "lawyers", 
    "Lawyertalk",
    "legal",
    "personalinjury",
    "Insurance",
    "marketing",
    "PPC",
    "digitalmarketing"
]

# Keywords to search
KEYWORDS = [
    "lead generation",
    "PI leads",
    "personal injury leads",
    "MVA leads",
    "legal leads",
    "lawyer marketing",
    "law firm marketing",
    "intake service",
    "lead vendor",
    "buying leads",
    "case leads",
    "Martindale",
    "Avvo",
    "FindLaw",
    "Scorpion",
    "mass tort leads"
]

def get_reddit_posts(subreddit, keyword, limit=100):
    """Search Reddit for posts matching keyword"""
    url = f"https://www.reddit.com/r/{subreddit}/search.json"
    params = {
        "q": keyword,
        "restrict_sr": "on",
        "sort": "relevance",
        "limit": limit,
        "t": "all"
    }
    headers = {"User-Agent": "VendorResearchBot/1.0"}
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json().get("data", {}).get("children", [])
        elif response.status_code == 429:
            print(f"Rate limited on r/{subreddit}, waiting...")
            time.sleep(60)
            return []
    except Exception as e:
        print(f"Error fetching r/{subreddit}: {e}")
    return []

def get_post_comments(permalink, limit=500):
    """Get comments from a specific post"""
    url = f"https://www.reddit.com{permalink}.json"
    params = {"limit": limit}
    headers = {"User-Agent": "VendorResearchBot/1.0"}
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if len(data) > 1:
                return data[1].get("data", {}).get("children", [])
    except Exception as e:
        print(f"Error fetching comments: {e}")
    return []

def extract_post_data(post):
    """Extract relevant data from a post"""
    data = post.get("data", {})
    return {
        "id": data.get("id"),
        "title": data.get("title"),
        "selftext": data.get("selftext"),
        "subreddit": data.get("subreddit"),
        "author": data.get("author"),
        "score": data.get("score"),
        "num_comments": data.get("num_comments"),
        "created_utc": data.get("created_utc"),
        "permalink": data.get("permalink"),
        "url": data.get("url"),
        "scraped_at": datetime.utcnow().isoformat()
    }

def extract_comment_data(comment):
    """Extract relevant data from a comment"""
    data = comment.get("data", {})
    if data.get("body") and data.get("body") != "[deleted]":
        return {
            "id": data.get("id"),
            "body": data.get("body"),
            "author": data.get("author"),
            "score": data.get("score"),
            "created_utc": data.get("created_utc"),
            "permalink": data.get("permalink"),
            "scraped_at": datetime.utcnow().isoformat()
        }
    return None

def run_scrape():
    """Main scraping function"""
    all_posts = []
    all_comments = []
    seen_ids = set()
    
    print(f"Starting Reddit scrape at {datetime.utcnow().isoformat()}")
    
    for subreddit in SUBREDDITS:
        for keyword in KEYWORDS:
            print(f"Searching r/{subreddit} for '{keyword}'...")
            posts = get_reddit_posts(subreddit, keyword)
            
            for post in posts:
                post_data = extract_post_data(post)
                if post_data["id"] not in seen_ids:
                    seen_ids.add(post_data["id"])
                    all_posts.append(post_data)
                    
                    # Get comments for high-engagement posts
                    if post_data["num_comments"] > 5:
                        time.sleep(1)  # Rate limit
                        comments = get_post_comments(post_data["permalink"])
                        for comment in comments:
                            comment_data = extract_comment_data(comment)
                            if comment_data:
                                all_comments.append(comment_data)
            
            time.sleep(2)  # Rate limit between searches
    
    # Save results
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    
    posts_file = DATA_DIR / f"reddit_posts_{timestamp}.json"
    with open(posts_file, "w") as f:
        json.dump(all_posts, f, indent=2)
    
    comments_file = DATA_DIR / f"reddit_comments_{timestamp}.json"
    with open(comments_file, "w") as f:
        json.dump(all_comments, f, indent=2)
    
    print(f"\nScrape complete!")
    print(f"Posts collected: {len(all_posts)}")
    print(f"Comments collected: {len(all_comments)}")
    print(f"Saved to: {DATA_DIR}")
    
    return {
        "posts": len(all_posts),
        "comments": len(all_comments),
        "files": [str(posts_file), str(comments_file)]
    }

if __name__ == "__main__":
    run_scrape()
