#!/usr/bin/env python3
"""
Enhanced Audit with DataForSEO Integration

Two-tier approach:
1. FAST (< 10 sec): Basic audit + 1 SERP check for web display
2. FULL (email): All DataForSEO data for comprehensive PDF report
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import time

from analyzer import WebsiteAnalyzer, AuditResult, CategoryScore
from dataforseo_client import DataForSEOClient


@dataclass
class EnhancedAuditResult:
    """Extended audit result with DataForSEO data"""
    # Basic audit
    basic_result: AuditResult = None
    
    # DataForSEO enhanced data (for PDF)
    ranked_keywords: List[Dict] = field(default_factory=list)
    keyword_volumes: Dict[str, int] = field(default_factory=dict)
    competitors: List[Dict] = field(default_factory=list)
    serp_rankings: List[Dict] = field(default_factory=list)
    onpage_issues: List[Dict] = field(default_factory=list)
    
    # Meta
    api_cost: float = 0.0
    fast_mode_time: float = 0.0
    full_mode_time: float = 0.0


class EnhancedAuditor:
    """Two-tier audit system: fast for web, full for email"""
    
    def __init__(self, url: str):
        self.url = url
        self.analyzer = WebsiteAnalyzer(url)
        self.dataforseo = DataForSEOClient()
        self.domain = self.analyzer.domain
        
    def run_fast_audit(self) -> EnhancedAuditResult:
        """
        FAST MODE (< 10 seconds)
        - Basic HTML analysis (20 categories)
        - 1 quick SERP check (1 keyword only for speed!)
        
        For web display.
        """
        start = time.time()
        result = EnhancedAuditResult()
        
        # Run basic audit WITHOUT the slow SERP check
        result.basic_result = self.analyzer.run_full_audit(include_serp_check=False)
        
        # Quick SERP check - ONLY 1 KEYWORD for speed (<5 sec)
        try:
            keywords = self._generate_keywords()[:1]  # Just 1 keyword!
            serp = self.dataforseo.check_serp_rankings(self.domain, keywords)
            result.serp_rankings = serp.get('rankings', [])
            result.api_cost += serp.get('cost', 0)
            
            # Add SERP results to local categories (informational only, doesn't affect score)
            serp_score = self._serp_to_category(serp, keywords)
            result.basic_result.local_categories.append(serp_score)
            
            # DON'T recalculate total - SERP is bonus info with max_score=0
            # Score stays as sum of 10 AI + 10 Local categories = /200 max
            
        except Exception as e:
            print(f"SERP check failed: {e}")
            
        result.fast_mode_time = time.time() - start
        return result
    
    def run_full_audit(self) -> EnhancedAuditResult:
        """
        FULL MODE (30-60 seconds)
        - Everything from fast mode
        - All ranked keywords for domain
        - Search volumes
        - Competitor analysis
        - On-page technical issues
        
        For email PDF report.
        """
        start = time.time()
        
        # Start with fast audit
        result = self.run_fast_audit()
        
        # Add comprehensive DataForSEO data
        try:
            # 1. Get ALL ranked keywords for domain
            ranked = self._get_ranked_keywords()
            result.ranked_keywords = ranked.get('items', [])[:50]  # Top 50
            result.api_cost += ranked.get('cost', 0)
            
            # 2. Get search volumes for top keywords
            if result.ranked_keywords:
                top_kws = [k['keyword'] for k in result.ranked_keywords[:10]]
                volumes = self._get_search_volumes(top_kws)
                result.keyword_volumes = volumes.get('volumes', {})
                result.api_cost += volumes.get('cost', 0)
            
            # 3. Get competitors
            competitors = self._get_competitors()
            result.competitors = competitors.get('items', [])[:10]
            result.api_cost += competitors.get('cost', 0)
            
            # 4. Get on-page issues (if not blocked by Cloudflare)
            onpage = self._get_onpage_issues()
            result.onpage_issues = onpage.get('issues', [])
            result.api_cost += onpage.get('cost', 0)
            
        except Exception as e:
            print(f"Full audit DataForSEO error: {e}")
            
        result.full_mode_time = time.time() - start
        return result
    
    def _generate_keywords(self) -> List[str]:
        """Generate relevant keywords based on page content"""
        keywords = []
        
        # Detect business type from page
        business_type = "personal injury lawyer"
        city = None
        state = None
        
        if self.analyzer.soup:
            text = self.analyzer.soup.get_text().lower()
            html = str(self.analyzer.soup).lower()
            
            # Business type detection
            if "car accident" in text:
                business_type = "car accident lawyer"
            elif "truck accident" in text:
                business_type = "truck accident lawyer"
            elif "motorcycle" in text:
                business_type = "motorcycle accident lawyer"
            elif "medical malpractice" in text:
                business_type = "medical malpractice lawyer"
            elif "wrongful death" in text:
                business_type = "wrongful death lawyer"
            elif "criminal defense" in text:
                business_type = "criminal defense lawyer"
            elif "dui" in text or "dwi" in text:
                business_type = "dui lawyer"
                
            # IMPROVED CITY DETECTION - check multiple sources
            # Priority: schema address > meta tags > page content
            
            # Large list of US cities (top 200)
            cities = [
                # Top 50
                "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia",
                "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville",
                "Fort Worth", "Columbus", "Charlotte", "San Francisco", "Indianapolis",
                "Seattle", "Denver", "Washington", "Boston", "El Paso", "Nashville",
                "Detroit", "Oklahoma City", "Portland", "Las Vegas", "Memphis", "Louisville",
                "Baltimore", "Milwaukee", "Albuquerque", "Tucson", "Fresno", "Mesa",
                "Sacramento", "Atlanta", "Kansas City", "Colorado Springs", "Omaha", "Raleigh",
                "Miami", "Long Beach", "Virginia Beach", "Oakland", "Minneapolis", "Tulsa",
                "Tampa", "Arlington", "New Orleans",
                # More cities
                "Marietta", "Sandy Springs", "Roswell", "Alpharetta", "Savannah", "Augusta",
                "Macon", "Athens", "Lawrenceville", "Decatur",  # Georgia cities
                "Plano", "Irving", "Garland", "Frisco", "McKinney", "Grand Prairie",  # Texas
                "Scottsdale", "Gilbert", "Tempe", "Chandler", "Glendale",  # Arizona
                "Orlando", "St. Petersburg", "Hialeah", "Fort Lauderdale", "Tallahassee",  # Florida
                "Anaheim", "Santa Ana", "Riverside", "Stockton", "Irvine", "Chula Vista",  # California
            ]
            
            # 1. Check structured data/schema for address
            import json
            for script in self.analyzer.soup.find_all('script', type='application/ld+json'):
                try:
                    data = json.loads(script.string)
                    if isinstance(data, dict):
                        # Check for address in schema
                        addr = data.get('address', {})
                        if isinstance(addr, dict):
                            schema_city = addr.get('addressLocality', '')
                            if schema_city:
                                city = schema_city
                                break
                except:
                    pass
            
            # 2. Check meta tags and title for city names
            if not city:
                title = self.analyzer.soup.find('title')
                meta_desc = self.analyzer.soup.find('meta', {'name': 'description'})
                header_text = ""
                if title:
                    header_text += title.get_text().lower()
                if meta_desc:
                    header_text += " " + (meta_desc.get('content', '') or '').lower()
                    
                for c in cities:
                    if c.lower() in header_text:
                        city = c
                        break
            
            # 3. Check page content for city names
            if not city:
                for c in cities:
                    if c.lower() in text:
                        city = c
                        break
            
            # Detect state (for fallback)
            states = ["Georgia", "Texas", "California", "Florida", "Arizona", "New York",
                     "Illinois", "Pennsylvania", "Ohio", "Michigan", "North Carolina"]
            for s in states:
                if s.lower() in text:
                    state = s
                    break
        
        # Store detected location for display
        self.detected_city = city
        self.detected_state = state
        
        # Generate keyword variations - CITY FIRST for fast mode
        if city:
            # City-specific keywords first (more likely to rank)
            keywords.append(f"{business_type} {city}")
            keywords.append(f"{city} {business_type}")
            keywords.append(f"best {business_type} in {city}")
            keywords.append(f"best {business_type} {city}")
        elif state:
            # Fall back to state if no city found
            keywords.append(f"{business_type} {state}")
            keywords.append(f"{state} {business_type}")
        
        # Generic keywords after
        keywords.append(business_type)
        keywords.append(f"best {business_type}")
        keywords.append(f"{business_type} near me")
        
        return keywords[:10]
    
    def _serp_to_category(self, serp_data: Dict, keywords_checked: List[str] = None) -> CategoryScore:
        """Convert SERP results to CategoryScore - NOT counted toward /100 score"""
        score = CategoryScore(name="Google Rankings (Live)")
        score.max_score = 0  # Don't count toward total - this is bonus info
        findings = []
        
        # Show what keyword we checked
        if keywords_checked:
            findings.append(f"🔍 Searched for: \"{keywords_checked[0]}\"")
        
        rankings = serp_data.get('rankings_found', 0)
        top3 = serp_data.get('top_3_count', 0)
        top10 = serp_data.get('top_10_count', 0)
        top20 = serp_data.get('top_20_count', 0)
        
        if rankings > 0:
            if top3 > 0:
                findings.append(f"🏆 Ranking in top 3!")
            elif top10 > 0:
                findings.append(f"✅ Ranking in top 10")
            elif top20 > 0:
                findings.append(f"⚠️ Ranking in positions 11-20")
                
            for r in serp_data.get('rankings', [])[:3]:
                findings.append(f"  #{r['position']} for \"{r['keyword']}\"")
        else:
            # Show that we checked but didn't find rankings
            if keywords_checked:
                findings.append(f"❌ Not ranking for \"{keywords_checked[0]}\"")
            else:
                findings.append("❌ No rankings found for target keyword")
            
            # Helpful recommendations
            city_hint = getattr(self, 'detected_city', None) or getattr(self, 'detected_state', 'your area')
            score.recommendations = [
                f"Focus on ranking for your primary keywords in {city_hint}",
                "Build local backlinks and citations",
                "Create city-specific content pages"
            ]
            
        score.score = 0  # Always 0 - this is informational only
        score.findings = findings
        return score
    
    def _get_ranked_keywords(self) -> Dict[str, Any]:
        """Get all keywords domain ranks for"""
        result = {"items": [], "cost": 0}
        
        try:
            payload = [{
                "target": self.domain,
                "location_code": 2840,  # USA
                "language_code": "en",
                "limit": 100
            }]
            
            data = self.dataforseo._post("/dataforseo_labs/google/ranked_keywords/live", payload)
            if data and data.get("status_code") == 20000:
                result["cost"] = data.get("cost", 0)
                tasks = data.get("tasks", [])
                if tasks and tasks[0].get("result"):
                    for r in tasks[0]["result"]:
                        items = r.get("items", [])
                        result["items"] = [
                            {
                                "keyword": i.get("keyword_data", {}).get("keyword"),
                                "position": i.get("ranked_serp_element", {}).get("serp_item", {}).get("rank_group"),
                                "volume": i.get("keyword_data", {}).get("keyword_info", {}).get("search_volume"),
                                "url": i.get("ranked_serp_element", {}).get("serp_item", {}).get("url"),
                            }
                            for i in items if i.get("keyword_data")
                        ]
        except Exception as e:
            print(f"Ranked keywords error: {e}")
            
        return result
    
    def _get_search_volumes(self, keywords: List[str]) -> Dict[str, Any]:
        """Get search volumes for keywords"""
        result = {"volumes": {}, "cost": 0}
        
        try:
            payload = [{
                "keywords": keywords,
                "location_code": 2840,
                "language_code": "en"
            }]
            
            data = self.dataforseo._post("/keywords_data/google_ads/search_volume/live", payload)
            if data and data.get("status_code") == 20000:
                result["cost"] = data.get("cost", 0)
                tasks = data.get("tasks", [])
                if tasks and tasks[0].get("result"):
                    for item in tasks[0]["result"]:
                        kw = item.get("keyword")
                        vol = item.get("search_volume")
                        if kw and vol:
                            result["volumes"][kw] = vol
        except Exception as e:
            print(f"Search volume error: {e}")
            
        return result
    
    def _get_competitors(self) -> Dict[str, Any]:
        """Get organic competitors"""
        result = {"items": [], "cost": 0}
        
        try:
            payload = [{
                "target": self.domain,
                "location_code": 2840,
                "language_code": "en",
                "limit": 20
            }]
            
            data = self.dataforseo._post("/dataforseo_labs/google/competitors_domain/live", payload)
            if data and data.get("status_code") == 20000:
                result["cost"] = data.get("cost", 0)
                tasks = data.get("tasks", [])
                if tasks and tasks[0].get("result"):
                    for r in tasks[0]["result"]:
                        items = r.get("items", [])
                        result["items"] = [
                            {
                                "domain": i.get("domain"),
                                "avg_position": i.get("avg_position"),
                                "keywords_count": i.get("se_keywords"),
                                "visibility": i.get("intersections")
                            }
                            for i in items
                        ]
        except Exception as e:
            print(f"Competitors error: {e}")
            
        return result
    
    def _get_onpage_issues(self) -> Dict[str, Any]:
        """Get on-page SEO issues"""
        result = {"issues": [], "cost": 0}
        
        try:
            payload = [{
                "url": self.url,
                "enable_javascript": True
            }]
            
            data = self.dataforseo._post("/on_page/instant_pages", payload, timeout=15)
            if data and data.get("status_code") == 20000:
                result["cost"] = data.get("cost", 0)
                tasks = data.get("tasks", [])
                if tasks and tasks[0].get("result"):
                    for r in tasks[0]["result"]:
                        items = r.get("items", [])
                        if items:
                            page = items[0]
                            checks = page.get("checks", {})
                            # Find failed checks
                            for check, passed in checks.items():
                                if passed == False:
                                    result["issues"].append({
                                        "issue": check.replace("_", " ").title(),
                                        "severity": "warning"
                                    })
                            
                            # Add meta info
                            meta = page.get("meta", {})
                            if not meta.get("title"):
                                result["issues"].append({"issue": "Missing title tag", "severity": "critical"})
                            if not meta.get("description"):
                                result["issues"].append({"issue": "Missing meta description", "severity": "warning"})
                                
        except Exception as e:
            print(f"On-page error: {e}")
            
        return result


# Test
if __name__ == "__main__":
    url = "https://www.zehllaw.com"
    print(f"Testing enhanced audit for {url}")
    print("=" * 60)
    
    auditor = EnhancedAuditor(url)
    
    # Fast mode
    print("\n--- FAST MODE ---")
    fast = auditor.run_fast_audit()
    print(f"Time: {fast.fast_mode_time:.1f}s")
    print(f"Score: {fast.basic_result.total_score}/200")
    print(f"API cost: ${fast.api_cost:.4f}")
    print(f"Rankings: {len(fast.serp_rankings)}")
    
    # Full mode
    print("\n--- FULL MODE ---")
    full = auditor.run_full_audit()
    print(f"Time: {full.full_mode_time:.1f}s")
    print(f"API cost: ${full.api_cost:.4f}")
    print(f"Ranked keywords: {len(full.ranked_keywords)}")
    print(f"Competitors: {len(full.competitors)}")
    print(f"On-page issues: {len(full.onpage_issues)}")
    
    # Show some data
    if full.ranked_keywords:
        print("\nTop 5 ranked keywords:")
        for kw in full.ranked_keywords[:5]:
            print(f"  #{kw.get('position')} - {kw.get('keyword')} ({kw.get('volume')} vol)")
            
    if full.competitors:
        print("\nTop 3 competitors:")
        for c in full.competitors[:3]:
            print(f"  {c.get('domain')} - {c.get('keywords_count')} keywords")
