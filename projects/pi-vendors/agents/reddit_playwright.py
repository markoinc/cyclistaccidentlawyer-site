#!/usr/bin/env python3
"""
Reddit Scraper using Playwright - Personal Injury Vendors Project
Scrapes Reddit like a human, no API needed
"""

import json
import time
import random
import asyncio
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

PROJECT_DIR = Path("/home/ec2-user/clawd/projects/pi-vendors")
DATA_DIR = PROJECT_DIR / "data" / "raw" / "reddit"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Subreddits to monitor
SUBREDDITS = [
    "LawFirm",
    "lawyers",
    "Lawyertalk", 
    "personalinjury",
    "legal",
    "Insurance",
    "marketing",
    "PPC",
    "digitalmarketing",
    "Entrepreneur",
    "smallbusiness"
]

# Expanded keywords for all PI
KEYWORDS = [
    # General lead gen
    "lead generation",
    "buying leads",
    "legal leads",
    "lawyer leads",
    "attorney leads",
    
    # PI specific
    "personal injury leads",
    "PI leads",
    "injury leads",
    "accident leads",
    
    # Case types
    "MVA leads",
    "car accident leads",
    "slip and fall leads",
    "medical malpractice leads",
    "workers comp leads",
    "mass tort leads",
    
    # Services
    "legal intake",
    "answering service",
    "legal marketing",
    "lawyer marketing",
    "law firm marketing",
    "PI marketing",
    
    # Vendors by name
    "Martindale",
    "Avvo",
    "FindLaw",
    "Scorpion",
    "Justia",
    "Super Lawyers",
    
    # Pain points
    "lead quality",
    "junk leads",
    "bad leads",
    "lead vendor",
    "marketing agency",
    "wasted money marketing"
]

async def random_delay(min_sec=2, max_sec=5):
    """Human-like random delay"""
    await asyncio.sleep(random.uniform(min_sec, max_sec))

async def scrape_search_results(page, subreddit, keyword):
    """Scrape Reddit search results for a keyword"""
    posts = []
    
    try:
        url = f"https://www.reddit.com/r/{subreddit}/search/?q={keyword}&restrict_sr=1&sort=relevance&t=all"
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await random_delay(2, 4)
        
        # Scroll to load more results
        for _ in range(3):
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await random_delay(1, 2)
        
        # Extract post data
        post_elements = await page.query_selector_all('div[data-testid="post-container"]')
        
        for post_el in post_elements[:20]:  # Limit per search
            try:
                title_el = await post_el.query_selector('h3')
                title = await title_el.inner_text() if title_el else ""
                
                link_el = await post_el.query_selector('a[data-click-id="body"]')
                link = await link_el.get_attribute('href') if link_el else ""
                
                # Get vote count
                vote_el = await post_el.query_selector('div[id^="vote-arrows"] span')
                votes = await vote_el.inner_text() if vote_el else "0"
                
                # Get comment count
                comment_el = await post_el.query_selector('span:has-text("comment")')
                comments = await comment_el.inner_text() if comment_el else "0 comments"
                
                if title:
                    posts.append({
                        "title": title,
                        "url": f"https://reddit.com{link}" if link and not link.startswith('http') else link,
                        "subreddit": subreddit,
                        "keyword": keyword,
                        "votes": votes,
                        "comments": comments,
                        "scraped_at": datetime.utcnow().isoformat()
                    })
            except Exception as e:
                continue
                
    except Exception as e:
        print(f"Error scraping r/{subreddit} for '{keyword}': {e}")
    
    return posts

async def scrape_post_comments(page, post_url):
    """Scrape comments from a specific post"""
    comments = []
    
    try:
        await page.goto(post_url, wait_until="networkidle", timeout=30000)
        await random_delay(2, 3)
        
        # Expand comments
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await random_delay(1, 2)
        
        # Get post body
        post_body_el = await page.query_selector('div[data-test-id="post-content"]')
        post_body = await post_body_el.inner_text() if post_body_el else ""
        
        # Get comments
        comment_elements = await page.query_selector_all('div[id^="t1_"]')
        
        for comment_el in comment_elements[:30]:  # Limit comments per post
            try:
                text_el = await comment_el.query_selector('div[data-testid="comment"]')
                text = await text_el.inner_text() if text_el else ""
                
                if text and len(text) > 20:
                    comments.append({
                        "text": text[:2000],  # Limit length
                        "post_url": post_url,
                        "scraped_at": datetime.utcnow().isoformat()
                    })
            except:
                continue
                
    except Exception as e:
        print(f"Error scraping comments from {post_url}: {e}")
    
    return post_body, comments

async def run_scrape(max_posts=500):
    """Main scraping function"""
    all_posts = []
    all_comments = []
    seen_urls = set()
    
    print(f"Starting Playwright Reddit scrape at {datetime.utcnow().isoformat()}")
    print(f"Subreddits: {len(SUBREDDITS)}, Keywords: {len(KEYWORDS)}")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        for subreddit in SUBREDDITS:
            for keyword in KEYWORDS:
                if len(all_posts) >= max_posts:
                    break
                    
                print(f"[{len(all_posts)}/{max_posts}] Searching r/{subreddit} for '{keyword}'...")
                
                posts = await scrape_search_results(page, subreddit, keyword)
                
                for post in posts:
                    if post["url"] not in seen_urls:
                        seen_urls.add(post["url"])
                        all_posts.append(post)
                        
                        # Get comments for high-engagement posts
                        if "comment" in post.get("comments", ""):
                            try:
                                num_comments = int(post["comments"].split()[0])
                                if num_comments > 5 and len(all_comments) < 2000:
                                    await random_delay(3, 6)
                                    body, comments = await scrape_post_comments(page, post["url"])
                                    post["body"] = body
                                    all_comments.extend(comments)
                            except:
                                pass
                
                await random_delay(5, 10)  # Longer delay between searches
            
            if len(all_posts) >= max_posts:
                break
        
        await browser.close()
    
    # Save results
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    
    posts_file = DATA_DIR / f"posts_{timestamp}.json"
    with open(posts_file, "w") as f:
        json.dump(all_posts, f, indent=2)
    
    comments_file = DATA_DIR / f"comments_{timestamp}.json"
    with open(comments_file, "w") as f:
        json.dump(all_comments, f, indent=2)
    
    print(f"\n{'='*50}")
    print(f"Scrape complete!")
    print(f"Posts collected: {len(all_posts)}")
    print(f"Comments collected: {len(all_comments)}")
    print(f"Saved to: {DATA_DIR}")
    print(f"{'='*50}")
    
    return {
        "posts": len(all_posts),
        "comments": len(all_comments),
        "files": [str(posts_file), str(comments_file)]
    }

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--max", type=int, default=500, help="Max posts to collect")
    args = parser.parse_args()
    
    asyncio.run(run_scrape(max_posts=args.max))
