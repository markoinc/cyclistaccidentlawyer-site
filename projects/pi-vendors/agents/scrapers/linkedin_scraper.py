"""
LinkedIn scraper - company pages and discussions
Note: LinkedIn is aggressive with anti-bot, so this uses search + public pages only
"""
import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from playwright.async_api import async_playwright, Page, Browser

import sys
sys.path.append(str(Path(__file__).parent.parent))
from base_scraper import BaseScraper


class LinkedInScraper(BaseScraper):
    """Scrapes LinkedIn for legal marketing company info and discussions"""
    
    def __init__(self):
        super().__init__("linkedin")
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        
        # Companies to track
        self.companies = [
            "scorpion", "findlaw", "martindale-avvo", "rankings-io",
            "consultwebs", "postali", "mockingbird-marketing", "foster-web-marketing"
        ]
        
        # Search queries
        self.search_queries = [
            "legal lead generation",
            "PI attorney marketing",
            "personal injury leads",
            "law firm marketing"
        ]
    
    async def init_browser(self):
        pw = await async_playwright().start()
        self.browser = await pw.chromium.launch(headless=True)
        context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        self.page = await context.new_page()
        self.logger.info("Browser initialized")
    
    async def close_browser(self):
        if self.browser:
            await self.browser.close()

    async def scrape_company_page(self, company_slug: str) -> Optional[Dict]:
        """Scrape a LinkedIn company page (public view)"""
        try:
            url = f"https://www.linkedin.com/company/{company_slug}"
            await self.page.goto(url, timeout=30000)
            await asyncio.sleep(3)
            
            # Check if we got blocked or redirected to login
            current_url = self.page.url
            if "login" in current_url or "authwall" in current_url:
                self.logger.warning(f"LinkedIn blocked access to {company_slug}")
                return None
            
            data = {
                "source": "linkedin",
                "company_slug": company_slug,
                "url": url,
                "scraped_at": datetime.now().isoformat()
            }
            
            # Company name
            name_elem = await self.page.query_selector("h1")
            if name_elem:
                data["name"] = await name_elem.inner_text()
            
            # Description
            desc_elem = await self.page.query_selector("p.break-words")
            if desc_elem:
                data["description"] = await desc_elem.inner_text()
            
            # Employee count
            emp_elem = await self.page.query_selector("a[href*='people']")
            if emp_elem:
                data["employees"] = await emp_elem.inner_text()
            
            # Industry
            industry_elem = await self.page.query_selector("div.org-top-card-summary-info-list__info-item")
            if industry_elem:
                data["industry"] = await industry_elem.inner_text()
            
            self.stats["items_scraped"] += 1
            return data
            
        except Exception as e:
            self.logger.error(f"LinkedIn company error for {company_slug}: {e}")
            self.stats["errors"] += 1
            return None

    async def scrape_google_linkedin_posts(self, query: str) -> List[Dict]:
        """Use Google to find LinkedIn posts (avoids LinkedIn's anti-bot)"""
        posts = []
        try:
            search_url = f"https://www.google.com/search?q=site:linkedin.com/posts+{query.replace(' ', '+')}"
            await self.page.goto(search_url, timeout=30000)
            await asyncio.sleep(2)
            
            # Get search results
            results = await self.page.query_selector_all("div.g")
            
            for result in results[:10]:
                try:
                    link = await result.query_selector("a")
                    title_elem = await result.query_selector("h3")
                    snippet_elem = await result.query_selector("div.VwiC3b")
                    
                    if link and title_elem:
                        href = await link.get_attribute("href")
                        title = await title_elem.inner_text()
                        snippet = ""
                        if snippet_elem:
                            snippet = await snippet_elem.inner_text()
                        
                        if "linkedin.com/posts" in href:
                            posts.append({
                                "url": href,
                                "title": title,
                                "snippet": snippet,
                                "query": query,
                                "source": "linkedin_via_google"
                            })
                            self.stats["items_scraped"] += 1
                except:
                    continue
            
            self.logger.info(f"Found {len(posts)} LinkedIn posts for '{query}'")
            
        except Exception as e:
            self.logger.error(f"Google LinkedIn search error: {e}")
            self.stats["errors"] += 1
        
        return posts

    async def scrape(self) -> List[Dict]:
        """Main scrape routine"""
        self.start()
        all_data = {"companies": [], "posts": []}
        
        await self.init_browser()
        
        try:
            # Scrape company pages
            for company in self.companies:
                self.logger.info(f"Scraping LinkedIn company: {company}")
                data = await self.scrape_company_page(company)
                if data:
                    all_data["companies"].append(data)
                    self.save_raw(
                        json.dumps(data), 
                        data.get("url"),
                        {"type": "company", "company": company}
                    )
                await asyncio.sleep(5)  # LinkedIn is aggressive
            
            # Search for posts via Google
            for query in self.search_queries:
                self.logger.info(f"Searching LinkedIn posts: {query}")
                posts = await self.scrape_google_linkedin_posts(query)
                all_data["posts"].extend(posts)
                
                for post in posts:
                    self.save_raw(
                        json.dumps(post),
                        post.get("url"),
                        {"type": "post", "query": query}
                    )
                
                await asyncio.sleep(3)
            
        finally:
            await self.close_browser()
        
        # Save batch
        self.save_raw_json(all_data)
        
        self.finish(f"Scraped {len(all_data['companies'])} companies, {len(all_data['posts'])} posts")
        return [all_data]
    
    def get_status(self) -> Dict:
        return {
            "source": "linkedin",
            "companies": len(self.companies),
            "queries": len(self.search_queries),
            "stats": self.stats
        }


async def main():
    scraper = LinkedInScraper()
    await scraper.scrape()


if __name__ == "__main__":
    asyncio.run(main())
