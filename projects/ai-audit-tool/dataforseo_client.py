#!/usr/bin/env python3
"""
DataForSEO API Client for real SEO data

Available APIs (on current plan):
- SERP API ✅ ($0.002/request)
- On-Page API ✅ ($0.00125/request)
- Backlinks API ❌ (needs subscription activation)
"""

import requests
from typing import Optional, Dict, Any, List
from urllib.parse import urlparse


class DataForSEOClient:
    """Client for DataForSEO API"""
    
    BASE_URL = "https://api.dataforseo.com/v3"
    
    def __init__(self):
        # Credentials from TOOLS.md
        self.auth = "bWFya0BrdXJpb3NicmFuZC5jb206YjI5MmI0YTVlNjg2YmM3NQ=="
        self.headers = {
            "Authorization": f"Basic {self.auth}",
            "Content-Type": "application/json"
        }
        
    def _post(self, endpoint: str, payload: list, timeout: int = 30) -> Optional[dict]:
        """Make POST request to DataForSEO"""
        try:
            resp = requests.post(
                f"{self.BASE_URL}{endpoint}",
                json=payload,
                headers=self.headers,
                timeout=timeout
            )
            if resp.status_code == 200:
                return resp.json()
            else:
                print(f"DataForSEO error: {resp.status_code}")
                return None
        except Exception as e:
            print(f"DataForSEO request failed: {e}")
            return None
    
    def check_serp_rankings(self, domain: str, keywords: List[str], location: str = "United States") -> Dict[str, Any]:
        """
        Check actual Google rankings for domain across multiple keywords.
        
        Cost: ~$0.002 per keyword
        """
        results = {
            "keywords_checked": 0,
            "rankings_found": 0,
            "top_3_count": 0,
            "top_10_count": 0,
            "top_20_count": 0,
            "rankings": [],
            "cost": 0
        }
        
        # Clean domain
        domain = domain.replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0]
        
        for keyword in keywords[:10]:  # Limit to 10 keywords to manage costs
            payload = [{
                "keyword": keyword,
                "location_name": location,
                "language_name": "English",
                "depth": 30,
                "se_domain": "google.com"
            }]
            
            data = self._post("/serp/google/organic/live/regular", payload)
            if data and data.get("status_code") == 20000:
                results["cost"] += data.get("cost", 0)
                results["keywords_checked"] += 1
                
                tasks = data.get("tasks", [])
                if tasks and tasks[0].get("result"):
                    for result in tasks[0]["result"]:
                        for item in result.get("items", []):
                            if item.get("type") == "organic":
                                url = item.get("url", "")
                                # Check if domain matches
                                item_domain = urlparse(url).netloc.replace("www.", "")
                                if domain in item_domain:
                                    position = item.get("rank_group", 999)
                                    results["rankings_found"] += 1
                                    if position <= 3:
                                        results["top_3_count"] += 1
                                    if position <= 10:
                                        results["top_10_count"] += 1
                                    if position <= 20:
                                        results["top_20_count"] += 1
                                    results["rankings"].append({
                                        "keyword": keyword,
                                        "position": position,
                                        "url": url,
                                        "title": item.get("title", "")
                                    })
                                    break  # Found for this keyword, move to next
        
        return results
    
    def get_serp_competitors(self, keyword: str, location: str = "United States") -> List[Dict[str, Any]]:
        """
        Get top 10 competitors for a keyword.
        
        Cost: ~$0.002
        """
        competitors = []
        
        payload = [{
            "keyword": keyword,
            "location_name": location,
            "language_name": "English",
            "depth": 10,
            "se_domain": "google.com"
        }]
        
        data = self._post("/serp/google/organic/live/regular", payload)
        if data and data.get("status_code") == 20000:
            tasks = data.get("tasks", [])
            if tasks and tasks[0].get("result"):
                for result in tasks[0]["result"]:
                    for item in result.get("items", []):
                        if item.get("type") == "organic":
                            competitors.append({
                                "position": item.get("rank_group"),
                                "url": item.get("url"),
                                "domain": urlparse(item.get("url", "")).netloc,
                                "title": item.get("title")
                            })
        
        return competitors[:10]
    
    def generate_local_keywords(self, business_type: str, city: str = None, state: str = None) -> List[str]:
        """Generate relevant local keywords for checking rankings"""
        keywords = []
        
        # Base keywords for PI lawyers
        base_keywords = [
            f"{business_type}",
            f"best {business_type}",
            f"{business_type} near me",
        ]
        
        if city:
            keywords.extend([
                f"{business_type} {city}",
                f"{city} {business_type}",
                f"best {business_type} in {city}",
            ])
            
        if state:
            keywords.extend([
                f"{business_type} {state}",
                f"{state} {business_type}",
            ])
            
        # Add variations
        if "lawyer" in business_type.lower():
            attorney_type = business_type.replace("lawyer", "attorney").replace("Lawyer", "Attorney")
            keywords.append(attorney_type)
            if city:
                keywords.append(f"{attorney_type} {city}")
                
        return keywords[:10]  # Cap at 10


# Test
if __name__ == "__main__":
    client = DataForSEOClient()
    
    print("Testing DataForSEO SERP API")
    print("=" * 50)
    
    # Test SERP rankings
    domain = "morgan-morgan.com"
    keywords = [
        "personal injury lawyer",
        "car accident lawyer",
        "personal injury attorney florida"
    ]
    
    print(f"\nChecking rankings for {domain}...")
    results = client.check_serp_rankings(domain, keywords)
    print(f"  Keywords checked: {results['keywords_checked']}")
    print(f"  Rankings found: {results['rankings_found']}")
    print(f"  Top 10: {results['top_10_count']}")
    print(f"  Cost: ${results['cost']:.4f}")
    for r in results['rankings']:
        print(f"    #{r['position']} for '{r['keyword']}'")
    
    # Test competitors
    print(f"\nTop competitors for 'personal injury lawyer':")
    competitors = client.get_serp_competitors("personal injury lawyer")
    for c in competitors[:5]:
        print(f"  #{c['position']}: {c['domain']}")
