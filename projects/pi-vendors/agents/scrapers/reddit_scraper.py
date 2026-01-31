"""
Reddit scraper using Playwright (browser-based to avoid API limits)
"""
import asyncio
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from playwright.async_api import async_playwright, Page, Browser

import sys
sys.path.append(str(Path(__file__).parent.parent))
from base_scraper import BaseScraper

# Load config
CONFIG_PATH = Path(__file__).parent.parent.parent / "config" / "sources.json"
with open(CONFIG_PATH) as f:
    CONFIG = json.load(f)["reddit"]


class RedditScraper(BaseScraper):
    """Scrapes Reddit for legal marketing discussions"""
    
    def __init__(self):
        super().__init__("reddit")
        self.subreddits = CONFIG["subreddits"]
        self.keywords = CONFIG["keywords"]
        self.vendor_names = CONFIG["vendor_names"]
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
    
    async def init_browser(self):
        """Initialize Playwright browser"""
        pw = await async_playwright().start()
        self.browser = await pw.chromium.launch(headless=True)
        context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        self.page = await context.new_page()
        self.logger.info("Browser initialized")
    
    async def close_browser(self):
        """Close browser"""
        if self.browser:
            await self.browser.close()
    
    async def scrape_subreddit(self, subreddit: str, time_filter: str = "month") -> List[Dict]:
        """Scrape a subreddit for relevant posts"""
        posts = []
        url = f"https://old.reddit.com/r/{subreddit}/search?q={'+OR+'.join(self.keywords[:5])}&restrict_sr=on&sort=new&t={time_filter}"
        
        try:
            await self.page.goto(url, timeout=30000)
            await asyncio.sleep(2)  # Let page load
            
            # Get all post links
            post_elements = await self.page.query_selector_all("a.search-title")
            
            for elem in post_elements[:20]:  # Limit per subreddit
                try:
                    title = await elem.inner_text()
                    href = await elem.get_attribute("href")
                    
                    # Check if relevant
                    title_lower = title.lower()
                    if any(kw.lower() in title_lower for kw in self.keywords + self.vendor_names):
                        posts.append({
                            "subreddit": subreddit,
                            "title": title,
                            "url": f"https://reddit.com{href}" if href.startswith("/") else href,
                            "found_via": "search"
                        })
                        self.stats["items_scraped"] += 1
                except Exception as e:
                    self.logger.debug(f"Error parsing post: {e}")
                    continue
            
            self.logger.info(f"r/{subreddit}: found {len(posts)} relevant posts")
            
        except Exception as e:
            self.logger.error(f"Error scraping r/{subreddit}: {e}")
            self.stats["errors"] += 1
        
        return posts
    
    async def scrape_post(self, url: str) -> Optional[Dict]:
        """Scrape full post content and comments"""
        try:
            # Use old.reddit for easier scraping
            if "old.reddit" not in url:
                url = url.replace("www.reddit.com", "old.reddit.com").replace("reddit.com", "old.reddit.com")
            
            await self.page.goto(url, timeout=30000)
            await asyncio.sleep(1)
            
            # Get post content
            post_data = {
                "url": url,
                "scraped_at": datetime.now().isoformat()
            }
            
            # Title
            title_elem = await self.page.query_selector("a.title")
            if title_elem:
                post_data["title"] = await title_elem.inner_text()
            
            # Post body
            body_elem = await self.page.query_selector("div.usertext-body")
            if body_elem:
                post_data["body"] = await body_elem.inner_text()
            
            # Comments
            comments = []
            comment_elems = await self.page.query_selector_all("div.comment div.usertext-body")
            for i, elem in enumerate(comment_elems[:50]):  # Limit comments
                try:
                    text = await elem.inner_text()
                    if len(text) > 20:  # Skip short comments
                        comments.append(text)
                except:
                    continue
            
            post_data["comments"] = comments
            post_data["comment_count"] = len(comments)
            
            # Check for vendor mentions
            full_text = (post_data.get("body", "") + " " + " ".join(comments)).lower()
            mentioned_vendors = [v for v in self.vendor_names if v.lower() in full_text]
            post_data["mentioned_vendors"] = mentioned_vendors
            
            return post_data
            
        except Exception as e:
            self.logger.error(f"Error scraping post {url}: {e}")
            self.stats["errors"] += 1
            return None
    
    async def scrape(self) -> List[Dict]:
        """Main scrape routine"""
        self.start()
        all_posts = []
        
        await self.init_browser()
        
        try:
            # Scrape each subreddit
            for subreddit in self.subreddits:
                posts = await self.scrape_subreddit(subreddit)
                
                # Get full content for each post
                for post in posts:
                    full_post = await self.scrape_post(post["url"])
                    if full_post:
                        full_post["subreddit"] = post["subreddit"]
                        all_posts.append(full_post)
                        
                        # Save to database
                        self.save_raw(
                            content=json.dumps(full_post),
                            source_url=post["url"],
                            metadata={
                                "subreddit": post["subreddit"],
                                "title": full_post.get("title"),
                                "vendors_mentioned": full_post.get("mentioned_vendors", [])
                            }
                        )
                    
                    await asyncio.sleep(1)  # Rate limit
                
                await asyncio.sleep(2)  # Between subreddits
            
        finally:
            await self.close_browser()
        
        # Save batch to JSON
        if all_posts:
            self.save_raw_json({"posts": all_posts, "count": len(all_posts)})
        
        self.finish(f"Scraped {len(self.subreddits)} subreddits")
        return all_posts
    
    def get_status(self) -> Dict:
        return {
            "source": "reddit",
            "subreddits": len(self.subreddits),
            "keywords": len(self.keywords),
            "vendor_names": len(self.vendor_names),
            "stats": self.stats
        }


async def main():
    """Test run"""
    scraper = RedditScraper()
    posts = await scraper.scrape()
    print(f"Scraped {len(posts)} posts")


if __name__ == "__main__":
    asyncio.run(main())
