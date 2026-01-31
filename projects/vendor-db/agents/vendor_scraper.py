#!/usr/bin/env python3
"""
Vendor Scraper Agent - Gathers data on PI lead generation vendors
"""

import json
import time
import requests
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup

DATA_DIR = Path("/home/ec2-user/clawd/projects/vendor-db/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Known vendors to research
KNOWN_VENDORS = [
    # Major Lead Gen Companies
    "Cases on Demand",
    "Inquired Esquire",
    "eGenerationMarketing", 
    "4LegalLeads",
    "Legal Brand Marketing",
    "LeadRival",
    "On Point Legal Leads",
    "Mass Tort Leads",
    "Tort Experts",
    "LeadingResponse",
    "Best Case Leads",
    
    # Directory Networks
    "Martindale-Avvo",
    "FindLaw",
    "Justia",
    "Lawyers.com",
    "Nolo",
    "Super Lawyers",
    
    # Marketing Agencies
    "Scorpion Legal",
    "Walker Advertising",
    "Quintessa Marketing",
    "Louder Media",
    "Law Pro Nation",
    "Foster Web Marketing",
    "PaperStreet",
    "Rankings.io",
    "Consultwebs",
    
    # Intake Services
    "Alert Communications",
    "Smith.ai",
    "Ruby Receptionists",
    "LEX Reception",
    "Answering Legal",
    "BackOffice Betties",
    "Intake Conversion Experts",
    "PATLive",
    "Nexa",
    "LawyerLine",
    
    # Mass Tort Specific
    "Sokolove Law",
    "Morgan & Morgan",
    "George Sink",
    "Rosen Injury Lawyers"
]

def search_vendor_reviews(vendor_name):
    """Search for vendor reviews across platforms"""
    results = {
        "vendor": vendor_name,
        "scraped_at": datetime.utcnow().isoformat(),
        "sources": []
    }
    
    # Search Google for reviews
    search_queries = [
        f"{vendor_name} reviews",
        f"{vendor_name} complaints",
        f"{vendor_name} legal leads",
        f'"{vendor_name}" site:reddit.com'
    ]
    
    return results

def scrape_trustpilot(vendor_name):
    """Scrape Trustpilot reviews for a vendor"""
    # Note: Would need proper implementation
    return {"source": "trustpilot", "status": "needs_implementation"}

def scrape_g2(vendor_name):
    """Scrape G2 reviews for a vendor"""
    return {"source": "g2", "status": "needs_implementation"}

def scrape_bbb(vendor_name):
    """Scrape BBB profile and complaints"""
    return {"source": "bbb", "status": "needs_implementation"}

def search_reddit_vendor(vendor_name):
    """Search Reddit for vendor mentions"""
    url = "https://www.reddit.com/search.json"
    params = {
        "q": f'"{vendor_name}"',
        "sort": "relevance",
        "limit": 100,
        "t": "all"
    }
    headers = {"User-Agent": "VendorResearchBot/1.0"}
    
    mentions = []
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            posts = response.json().get("data", {}).get("children", [])
            for post in posts:
                data = post.get("data", {})
                mentions.append({
                    "title": data.get("title"),
                    "subreddit": data.get("subreddit"),
                    "score": data.get("score"),
                    "num_comments": data.get("num_comments"),
                    "selftext": data.get("selftext", "")[:500],
                    "permalink": data.get("permalink"),
                    "created_utc": data.get("created_utc")
                })
    except Exception as e:
        print(f"Error searching for {vendor_name}: {e}")
    
    return mentions

def run_vendor_scrape():
    """Main vendor scraping function"""
    all_vendors = []
    
    print(f"Starting vendor scrape at {datetime.utcnow().isoformat()}")
    print(f"Researching {len(KNOWN_VENDORS)} vendors...")
    
    for i, vendor in enumerate(KNOWN_VENDORS):
        print(f"[{i+1}/{len(KNOWN_VENDORS)}] Researching: {vendor}")
        
        vendor_data = {
            "name": vendor,
            "scraped_at": datetime.utcnow().isoformat(),
            "reddit_mentions": search_reddit_vendor(vendor),
            "review_sources": []
        }
        
        all_vendors.append(vendor_data)
        time.sleep(2)  # Rate limit
    
    # Save results
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    output_file = DATA_DIR / f"vendors_{timestamp}.json"
    
    with open(output_file, "w") as f:
        json.dump(all_vendors, f, indent=2)
    
    # Calculate stats
    total_mentions = sum(len(v["reddit_mentions"]) for v in all_vendors)
    
    print(f"\nVendor scrape complete!")
    print(f"Vendors researched: {len(all_vendors)}")
    print(f"Total Reddit mentions: {total_mentions}")
    print(f"Saved to: {output_file}")
    
    return {
        "vendors": len(all_vendors),
        "reddit_mentions": total_mentions,
        "file": str(output_file)
    }

if __name__ == "__main__":
    run_vendor_scrape()
