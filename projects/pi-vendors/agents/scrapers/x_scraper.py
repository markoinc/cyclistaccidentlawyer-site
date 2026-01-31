"""
X/Twitter scraper for AI agent use cases
Monitors keywords and finds high-value content for Clawdbot/Moltbot
"""
import asyncio
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from playwright.async_api import async_playwright, Page, Browser
import logging

import sys
sys.path.append(str(Path(__file__).parent.parent))
from base_scraper import BaseScraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("x_scraper")


class XScraper(BaseScraper):
    """Scrapes X/Twitter for AI agent use cases"""
    
    def __init__(self):
        super().__init__("x_twitter")
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        
        # Keywords to monitor for PI industry intelligence
        self.keywords = [
            # Core PI industry terms
            "#personalinjury", "#legaltech", "#lawsuit", "#attorney",
            "personal injury", "PI attorney", "law firm technology",
            "legal software", "case management", "legal automation",
            
            # Vendor/buyer discussions
            "CaseMap", "LexisNexis", "Westlaw", "MyCase", "Clio",
            "law firm CRM", "legal billing", "case tracking",
            "discovery software", "document review", "litigation support",
            
            # AI in legal
            "AI lawyer", "legal AI", "AI paralegal", "legal automation",
            "contract review AI", "legal research AI", "AI discovery",
            "law firm AI", "legal chatbot", "AI document review",
            
            # Industry trends
            "legal innovation", "lawtech", "legal startup",
            "law firm efficiency", "legal practice management",
            "attorney productivity", "legal workflow"
        ]
        
        # Accounts to monitor (PI law, legal tech)
        self.accounts = [
            "AmericanBar", "LegalTech", "LawSites", "Above_the_Law",
            "LawyerMagazine", "LegalInnovate", "LawTechTalk",
            "PILawyerMag", "ATLA_org", "TrialLawyers"
        ]
        
        # Quality filters - must have engagement OR be from key accounts
        self.min_likes = 10
        self.min_retweets = 3
    
    async def init_browser(self):
        pw = await async_playwright().start()
        self.browser = await pw.chromium.launch(headless=True)
        context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        self.page = await context.new_page()
        logger.info("Browser initialized")
    
    async def close_browser(self):
        if self.browser:
            await self.browser.close()

    async def search_x_via_google(self, query: str, hours_ago: int = 24) -> List[Dict]:
        """Search X via Google (avoids login requirement)"""
        results = []
        try:
            # Use Google to search recent X posts
            search_url = f"https://www.google.com/search?q=site:x.com+{query.replace(' ', '+')}&tbs=qdr:d"
            await self.page.goto(search_url, timeout=30000)
            await asyncio.sleep(2)
            
            # Get search results
            result_divs = await self.page.query_selector_all("div.g")
            
            for div in result_divs[:10]:
                try:
                    link = await div.query_selector("a")
                    title_elem = await div.query_selector("h3")
                    snippet_elem = await div.query_selector("div.VwiC3b")
                    
                    if link and title_elem:
                        href = await link.get_attribute("href")
                        title = await title_elem.inner_text()
                        snippet = ""
                        if snippet_elem:
                            snippet = await snippet_elem.inner_text()
                        
                        if "x.com" in href and "/status/" in href:
                            results.append({
                                "url": href,
                                "title": title,
                                "snippet": snippet,
                                "query": query,
                                "source": "x_via_google",
                                "found_at": datetime.now().isoformat()
                            })
                            self.stats["items_scraped"] += 1
                except:
                    continue
            
            logger.info(f"Found {len(results)} X posts for '{query}'")
            
        except Exception as e:
            logger.error(f"Google X search error: {e}")
            self.stats["errors"] += 1
        
        return results

    async def search_nitter(self, query: str) -> List[Dict]:
        """Search via Nitter (Twitter frontend, no login needed)"""
        results = []
        nitter_instances = [
            "nitter.net",
            "nitter.privacydev.net",
            "nitter.poast.org"
        ]
        
        for instance in nitter_instances:
            try:
                search_url = f"https://{instance}/search?f=tweets&q={query.replace(' ', '+')}"
                await self.page.goto(search_url, timeout=15000)
                await asyncio.sleep(2)
                
                # Check if instance is working
                if "error" in (await self.page.content()).lower():
                    continue
                
                # Get tweets
                tweet_items = await self.page.query_selector_all("div.timeline-item")
                
                for item in tweet_items[:15]:
                    try:
                        tweet = {}
                        
                        # Username
                        username = await item.query_selector("a.username")
                        if username:
                            tweet["username"] = await username.inner_text()
                        
                        # Content
                        content = await item.query_selector("div.tweet-content")
                        if content:
                            tweet["content"] = await content.inner_text()
                        
                        # Link
                        link = await item.query_selector("a.tweet-link")
                        if link:
                            href = await link.get_attribute("href")
                            # Convert nitter link to x.com
                            tweet["url"] = f"https://x.com{href}"
                        
                        # Stats
                        stats = await item.query_selector("div.tweet-stats")
                        if stats:
                            tweet["stats"] = await stats.inner_text()
                        
                        if tweet.get("content") and tweet.get("url"):
                            tweet["query"] = query
                            tweet["source"] = "nitter"
                            tweet["found_at"] = datetime.now().isoformat()
                            results.append(tweet)
                            self.stats["items_scraped"] += 1
                            
                    except:
                        continue
                
                if results:
                    logger.info(f"Nitter ({instance}): found {len(results)} tweets for '{query}'")
                    break  # Got results, stop trying instances
                    
            except Exception as e:
                logger.debug(f"Nitter {instance} failed: {e}")
                continue
        
        return results

    def is_high_value(self, tweet: Dict) -> bool:
        """Filter for high-value PI industry content"""
        content = tweet.get("content", "").lower()
        
        # High-value indicators for PI industry
        high_value_indicators = [
            # Technology adoption/discussion
            "switched to", "started using", "implemented", "rolled out",
            "software review", "platform review", "tool review",
            "workflow", "efficiency", "automation", "streamlined",
            
            # Buyer sentiment
            "love this", "hate this", "recommend", "avoid",
            "best tool", "worst experience", "game changer",
            "waste of money", "worth it", "overpriced",
            
            # Market intelligence
            "new feature", "just launched", "beta access",
            "pricing change", "integration", "partnership",
            "acquisition", "funding", "investment",
            
            # Legal industry insights
            "case won", "settlement", "verdict", "trial outcome",
            "legal trend", "court ruling", "regulation",
            "compliance", "ethics", "bar association"
        ]
        
        has_value = any(indicator in content for indicator in high_value_indicators)
        
        # Exclude low-value patterns
        low_value_patterns = [
            "hiring", "job opening", "looking for",
            "subscribe", "follow me", "check out my",
            "dm me", "link in bio", "buy my course",
            "giveaway", "win a", "contest", "webinar"
        ]
        
        is_spam = any(pat in content for pat in low_value_patterns)
        
        return has_value and not is_spam

    def format_for_telegram(self, tweet: Dict) -> str:
        """Format tweet for Telegram group post"""
        content = tweet.get("content", "")[:500]
        url = tweet.get("url", "")
        username = tweet.get("username", "Unknown")
        query = tweet.get("query", "")
        
        msg = f"🔍 **Found via:** {query}\n"
        msg += f"👤 **@{username}**\n\n"
        msg += f"{content}\n\n"
        msg += f"🔗 {url}"
        
        return msg

    async def scrape(self) -> List[Dict]:
        """Main scrape routine"""
        self.start()
        all_results = []
        high_value = []
        
        await self.init_browser()
        
        try:
            # Search for each keyword
            for keyword in self.keywords[:10]:  # Limit to avoid rate limits
                logger.info(f"Searching X for: {keyword}")
                
                # Try Google first
                results = await self.search_x_via_google(keyword)
                
                # Try Nitter as backup
                if len(results) < 3:
                    nitter_results = await self.search_nitter(keyword)
                    results.extend(nitter_results)
                
                for result in results:
                    # Save raw
                    self.save_raw(
                        json.dumps(result),
                        result.get("url"),
                        {"query": keyword, "source": result.get("source")}
                    )
                    all_results.append(result)
                    
                    # Check if high value
                    if self.is_high_value(result):
                        high_value.append(result)
                
                await asyncio.sleep(3)  # Rate limit
            
        finally:
            await self.close_browser()
        
        # Save high-value results separately
        if high_value:
            hv_path = self.save_raw_json({
                "high_value_tweets": high_value,
                "count": len(high_value),
                "scraped_at": datetime.now().isoformat()
            }, f"high_value_{datetime.now().strftime('%Y%m%d_%H%M')}.json")
            logger.info(f"Saved {len(high_value)} high-value tweets to {hv_path}")
        
        self.finish(f"Found {len(all_results)} total, {len(high_value)} high-value")
        
        return high_value  # Return only high-value for notifications
    
    def get_status(self) -> Dict:
        return {
            "source": "x_twitter",
            "keywords": len(self.keywords),
            "accounts": len(self.accounts),
            "stats": self.stats
        }


async def main():
    scraper = XScraper()
    results = await scraper.scrape()
    print(f"Found {len(results)} high-value tweets")
    for r in results[:5]:
        print(f"\n---\n{r.get('content', '')[:200]}")


if __name__ == "__main__":
    asyncio.run(main())
