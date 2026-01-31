"""
Review site scraper - Trustpilot, G2, Capterra, BBB
"""
import asyncio
import json
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from playwright.async_api import async_playwright, Page, Browser

import sys
sys.path.append(str(Path(__file__).parent.parent))
from base_scraper import BaseScraper

# Load config
CONFIG_PATH = Path(__file__).parent.parent.parent / "config" / "sources.json"
with open(CONFIG_PATH) as f:
    CONFIG = json.load(f)


class ReviewScraper(BaseScraper):
    """Scrapes review sites for vendor reviews"""
    
    def __init__(self):
        super().__init__("reviews")
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        
        # Known vendors to search for
        self.vendors = [
            "Alert Communications", "Smith.ai", "Ruby Receptionist", 
            "Legal Conversion Center", "LegalMatch", "Avvo", "FindLaw",
            "Martindale-Hubbell", "Rankings.io", "Scorpion", "Postali",
            "Consultwebs", "Market My Market", "4LegalLeads"
        ]
    
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
        if self.browser:
            await self.browser.close()

    # ─────────────────────────────────────────
    # TRUSTPILOT
    # ─────────────────────────────────────────
    async def scrape_trustpilot(self, company_name: str) -> Optional[Dict]:
        """Scrape Trustpilot for a company"""
        try:
            # Search for company
            search_url = f"https://www.trustpilot.com/search?query={company_name.replace(' ', '+')}"
            await self.page.goto(search_url, timeout=30000)
            await asyncio.sleep(2)
            
            # Find first result
            result = await self.page.query_selector("a[name='business-unit-card']")
            if not result:
                self.logger.debug(f"Trustpilot: No results for {company_name}")
                return None
            
            href = await result.get_attribute("href")
            company_url = f"https://www.trustpilot.com{href}"
            
            # Go to company page
            await self.page.goto(company_url, timeout=30000)
            await asyncio.sleep(2)
            
            data = {
                "source": "trustpilot",
                "company_name": company_name,
                "url": company_url,
                "scraped_at": datetime.now().isoformat()
            }
            
            # Get rating
            rating_elem = await self.page.query_selector("span[data-rating-typography]")
            if rating_elem:
                data["rating"] = await rating_elem.inner_text()
            
            # Get review count
            count_elem = await self.page.query_selector("span[data-reviews-count-typography]")
            if count_elem:
                count_text = await count_elem.inner_text()
                data["review_count"] = count_text
            
            # Get reviews
            reviews = []
            review_cards = await self.page.query_selector_all("article[data-service-review-card-paper]")
            
            for card in review_cards[:20]:
                try:
                    review = {}
                    
                    # Rating
                    stars = await card.query_selector("div[data-service-review-rating]")
                    if stars:
                        img = await stars.query_selector("img")
                        if img:
                            alt = await img.get_attribute("alt")
                            if alt:
                                review["rating"] = alt
                    
                    # Title
                    title = await card.query_selector("h2")
                    if title:
                        review["title"] = await title.inner_text()
                    
                    # Body
                    body = await card.query_selector("p[data-service-review-text-typography]")
                    if body:
                        review["body"] = await body.inner_text()
                    
                    # Date
                    date = await card.query_selector("time")
                    if date:
                        review["date"] = await date.get_attribute("datetime")
                    
                    if review.get("body"):
                        reviews.append(review)
                        
                except Exception as e:
                    continue
            
            data["reviews"] = reviews
            self.stats["items_scraped"] += 1
            
            return data
            
        except Exception as e:
            self.logger.error(f"Trustpilot error for {company_name}: {e}")
            self.stats["errors"] += 1
            return None

    # ─────────────────────────────────────────
    # G2
    # ─────────────────────────────────────────
    async def scrape_g2(self, company_name: str) -> Optional[Dict]:
        """Scrape G2 for a company"""
        try:
            search_url = f"https://www.g2.com/search?query={company_name.replace(' ', '%20')}"
            await self.page.goto(search_url, timeout=30000)
            await asyncio.sleep(2)
            
            # Find first product result
            result = await self.page.query_selector("a.product-listing__product-name")
            if not result:
                self.logger.debug(f"G2: No results for {company_name}")
                return None
            
            href = await result.get_attribute("href")
            product_url = f"https://www.g2.com{href}"
            
            await self.page.goto(product_url + "/reviews", timeout=30000)
            await asyncio.sleep(2)
            
            data = {
                "source": "g2",
                "company_name": company_name,
                "url": product_url,
                "scraped_at": datetime.now().isoformat()
            }
            
            # Get rating
            rating_elem = await self.page.query_selector("span.fw-semibold")
            if rating_elem:
                data["rating"] = await rating_elem.inner_text()
            
            # Get reviews
            reviews = []
            review_divs = await self.page.query_selector_all("div[itemprop='review']")
            
            for div in review_divs[:15]:
                try:
                    review = {}
                    
                    # Title
                    title = await div.query_selector("h3")
                    if title:
                        review["title"] = await title.inner_text()
                    
                    # Pros/Cons
                    sections = await div.query_selector_all("div.review-content")
                    for section in sections:
                        text = await section.inner_text()
                        if "What do you like best" in text:
                            review["pros"] = text
                        elif "What do you dislike" in text:
                            review["cons"] = text
                    
                    if review:
                        reviews.append(review)
                        
                except:
                    continue
            
            data["reviews"] = reviews
            self.stats["items_scraped"] += 1
            
            return data
            
        except Exception as e:
            self.logger.error(f"G2 error for {company_name}: {e}")
            self.stats["errors"] += 1
            return None

    # ─────────────────────────────────────────
    # GOOGLE REVIEWS (via Maps)
    # ─────────────────────────────────────────
    async def scrape_google_reviews(self, company_name: str) -> Optional[Dict]:
        """Scrape Google Maps reviews for a company"""
        try:
            search_url = f"https://www.google.com/maps/search/{company_name.replace(' ', '+')}"
            await self.page.goto(search_url, timeout=30000)
            await asyncio.sleep(3)
            
            data = {
                "source": "google_reviews",
                "company_name": company_name,
                "scraped_at": datetime.now().isoformat()
            }
            
            # Try to get rating from first result
            rating_elem = await self.page.query_selector("span.fontDisplayLarge")
            if rating_elem:
                data["rating"] = await rating_elem.inner_text()
            
            # Review count
            count_elem = await self.page.query_selector("span[aria-label*='reviews']")
            if count_elem:
                data["review_count"] = await count_elem.get_attribute("aria-label")
            
            self.stats["items_scraped"] += 1
            return data
            
        except Exception as e:
            self.logger.error(f"Google Reviews error for {company_name}: {e}")
            self.stats["errors"] += 1
            return None

    # ─────────────────────────────────────────
    # BBB
    # ─────────────────────────────────────────
    async def scrape_bbb(self, company_name: str) -> Optional[Dict]:
        """Scrape BBB for a company"""
        try:
            search_url = f"https://www.bbb.org/search?find_country=USA&find_text={company_name.replace(' ', '%20')}"
            await self.page.goto(search_url, timeout=30000)
            await asyncio.sleep(2)
            
            # Find first result
            result = await self.page.query_selector("a.text-blue-medium")
            if not result:
                return None
            
            href = await result.get_attribute("href")
            
            await self.page.goto(href, timeout=30000)
            await asyncio.sleep(2)
            
            data = {
                "source": "bbb",
                "company_name": company_name,
                "url": href,
                "scraped_at": datetime.now().isoformat()
            }
            
            # Get BBB rating
            rating_elem = await self.page.query_selector("span.bds-h2")
            if rating_elem:
                data["bbb_rating"] = await rating_elem.inner_text()
            
            # Accreditation status
            accredited = await self.page.query_selector("span:has-text('BBB Accredited')")
            data["accredited"] = accredited is not None
            
            # Complaint count
            complaint_elem = await self.page.query_selector("a:has-text('Complaints')")
            if complaint_elem:
                text = await complaint_elem.inner_text()
                data["complaints"] = text
            
            self.stats["items_scraped"] += 1
            return data
            
        except Exception as e:
            self.logger.error(f"BBB error for {company_name}: {e}")
            self.stats["errors"] += 1
            return None

    # ─────────────────────────────────────────
    # MAIN SCRAPE
    # ─────────────────────────────────────────
    async def scrape(self) -> List[Dict]:
        """Main scrape routine - all review sites for all vendors"""
        self.start()
        all_data = []
        
        await self.init_browser()
        
        try:
            for vendor in self.vendors:
                self.logger.info(f"Scraping reviews for: {vendor}")
                vendor_data = {"vendor": vendor, "reviews": {}}
                
                # Trustpilot
                tp = await self.scrape_trustpilot(vendor)
                if tp:
                    vendor_data["reviews"]["trustpilot"] = tp
                    self.save_raw(json.dumps(tp), tp.get("url"), {"vendor": vendor, "source": "trustpilot"})
                await asyncio.sleep(2)
                
                # G2
                g2 = await self.scrape_g2(vendor)
                if g2:
                    vendor_data["reviews"]["g2"] = g2
                    self.save_raw(json.dumps(g2), g2.get("url"), {"vendor": vendor, "source": "g2"})
                await asyncio.sleep(2)
                
                # BBB
                bbb = await self.scrape_bbb(vendor)
                if bbb:
                    vendor_data["reviews"]["bbb"] = bbb
                    self.save_raw(json.dumps(bbb), bbb.get("url"), {"vendor": vendor, "source": "bbb"})
                await asyncio.sleep(2)
                
                # Google (rate limit more carefully)
                google = await self.scrape_google_reviews(vendor)
                if google:
                    vendor_data["reviews"]["google"] = google
                await asyncio.sleep(3)
                
                all_data.append(vendor_data)
                
        finally:
            await self.close_browser()
        
        # Save full batch
        if all_data:
            self.save_raw_json({"vendors": all_data, "count": len(all_data)})
        
        self.finish(f"Scraped {len(self.vendors)} vendors across review sites")
        return all_data
    
    def get_status(self) -> Dict:
        return {
            "source": "reviews",
            "vendors": len(self.vendors),
            "sites": ["trustpilot", "g2", "bbb", "google"],
            "stats": self.stats
        }


async def main():
    scraper = ReviewScraper()
    data = await scraper.scrape()
    print(f"Scraped {len(data)} vendors")


if __name__ == "__main__":
    asyncio.run(main())
