#!/usr/bin/env python3
"""
Scrape Jacky Chou's Build in Public Notion pages for link building content.
"""

import requests
import time
import json
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Key episodes related to link building (extracted from main page)
LINK_BUILDING_EPISODES = {
    # Reddit Marketing
    "reddit_course": "https://indexsy.notion.site/Sept-27-EP-650-The-Complete-Reddit-Marketing-Course-2000-VALUE-27be1e50bed28070a788e6e647ddd69f",
    "reddit_agency": "https://indexsy.notion.site/Sept-26-EP-649-The-10k-mo-Reddit-Agency-OFFER-You-Can-Sell-TODAY-27ae1e50bed2803dadd5c675adee24e0",
    "reddit_local": "https://indexsy.notion.site/Sept-13-EP-637-Reddit-Marketing-for-Local-Businesses-FULL-SOP-26de1e50bed280268c6af8648e56df42",
    "reddit_10k": "https://indexsy.notion.site/Sept-11-EP-635-I-made-over-10k-spamming-Reddit-here-s-my-SOP-26be1e50bed280bfb90ade15bb895a89",
    "reddit_spam_10k": "https://indexsy.notion.site/Jan-19-EP-742-We-spammed-Reddit-with-10k-comments-here-s-what-I-learned-2ede1e50bed280be9e05d1af30eb4219",
    
    # Parasite SEO
    "parasite_24h": "https://indexsy.notion.site/Jan-17-EP-740-I-ranked-in-24-hours-with-this-parasite-2ebe1e50bed2800c9c33fb0c20dec760",
    "parasite_dr92": "https://indexsy.notion.site/Jan-16-EP-739-This-DR92-Site-is-the-PERFECT-Parasite-DO-THIS-NOW-2eae1e50bed2806fa731f8924c384b35",
    "parasite_google": "https://indexsy.notion.site/Nov-14-EP-687-Google-is-formally-targeting-Parasite-SEO-again-2abe1e50bed280d6a303fc5ea9f9b607",
    "parasite_fly": "https://indexsy.notion.site/Sept-18-EP-642-This-Parasite-SEO-is-about-to-FLY-273e1e50bed280809b5dec40b3c265262",
    "parasite_dr100": "https://indexsy.notion.site/Sept-17-EP-641-The-DR100-FREE-PARASITE-SEO-SITE-272e1e50bed280029337e018dc34a50c",
    "parasite_ranked": "https://indexsy.notion.site/Sept-9-EP-633-I-ranked-in-24-hours-with-parasite-SEO-269e1e50bed2805197dddd9c37152e25",
    "parasite_dr93": "https://indexsy.notion.site/Sept-8-EP-632-The-free-DR93-Parasite-SEO-you-re-welcome-268e1e50bed280bd8b84e485c314e62b",
    "browserblast_parasite": "https://indexsy.notion.site/Sept-12-EP-636-I-BrowserBlasted-a-Parasite-and-it-hit-1-in-24-hours-26ce1e50bed280e8a5d9e6034a9b4f98",
    
    # Subdomain Abuse
    "subdomain_working": "https://indexsy.notion.site/Jan-8-EP-731-Subdomain-Abuse-is-STILL-Working-2e2e1e50bed28078ac86c9a4e52b6c40",
    "subdomain_expired": "https://indexsy.notion.site/Dec-23-EP-720-The-expired-subdomain-trick-WTF-2d2e1e50bed2802bb936e3ad4c71ae0f",
    "subdomain_hreflang": "https://indexsy.notion.site/Dec-14-EP-713-rel-Hreflang-spam-subdomains-2c9e1e50bed2808ca1c8f8482adcf600",
    "subdomain_explained": "https://indexsy.notion.site/Dec-13-EP-712-Subdomain-Abuse-EXPLAINED-Next-GOLD-RUSH-2c8e1e50bed28035aa58f19defaf430b",
    
    # Link Building / Backlinks
    "wikipedia_links": "https://indexsy.notion.site/Oct-30-EP-680-I-Built-Do-Follow-Wikipedia-Links-For-Free-29ce1e50bed2800e9702cde8d14a28aa",
    "10k_backlinks_local": "https://indexsy.notion.site/August-25-EP-621-I-Built-10k-Backlinks-for-Local-SEO-NO-RISK-25ae1e50bed280e2be69dcb3251d8d39",
    "spammy_backlinks": "https://indexsy.notion.site/August-12-EP-611-The-Spammy-Backlinks-Case-Study-24de1e50bed2807392d2ec076ce110ca",
    "free_backlinks": "https://indexsy.notion.site/August-11-EP-610-Free-Automated-Backlinks-in-2025-Yes-please-CASE-STUDY-24ce1e50bed2806e8f54dc152e255edd",
    "fiverr_backlinks": "https://indexsy.notion.site/August-10-EP-609-I-bought-a-million-backlinks-from-Fiverr-and-it-worked-24be1e50bed28056b576f4336852941c",
    "spammed_backlinks_update": "https://indexsy.notion.site/August-28-EP-624-I-spammed-backlinks-in-the-middle-of-a-Google-Spam-Update-25de1e50bed280558e6bf443f1a12c14",
    "fiverr_bulk": "https://indexsy.notion.site/August-6-EP-605-I-bought-1-155-000-backlinks-for-35-from-Fiverr-248e1e50bed280ca995ce31db02f0fd5",
    
    # Authority / Topical
    "topical_authority": "https://indexsy.notion.site/Jan-5-EP-728-Topical-Authority-IS-BACK-SEO-in-2026-2dfe1e50bed28023b63ac0793e1af1ba",
    
    # Guest Posts / Digital PR
    "hijack_reddit": "https://indexsy.notion.site/Oct-2-EP-655-I-Hijacked-a-Reddit-Post-Outranked-It-on-Google-in-24-Hours-280e1e50bed280a6bd16fe0b1c0404df",
    
    # LLM Citations / GEO
    "llm_citations": "https://indexsy.notion.site/Dec-11-EP-710-LLM-Citations-will-be-the-NEW-Local-SEO-2c6e1e50bed280ddb163c82655047662",
    "llm_listicle": "https://indexsy.notion.site/Dec-29-EP-722-The-Free-LLM-Listicle-SOP-DO-THIS-NOW-2d8e1e50bed28001a1b8eacb4a55f482",
    "chatgpt_rank": "https://indexsy.notion.site/Dec-4-EP-704-How-to-Rank-on-ChatGPT-A-26-283-URL-Study-2bfe1e50bed2801e9fdcd587e32ecae6",
    "research_company": "https://indexsy.notion.site/Dec-18-EP-716-I-Built-a-Research-Company-to-Control-ChatGPT-Rankings-2cde1e50bed280ca8ba0ef251f94413e",
    "chatgpt_10_days": "https://indexsy.notion.site/Dec-17-EP-715-1-on-ChatGPT-in-10-days-FULL-REVEAL-2cce1e50bed2801ead19edda591f5ea6",
    
    # Cold Email / Outreach
    "cold_email_machine": "https://indexsy.notion.site/Sept-28-EP-651-I-Built-a-Cold-Email-Machine-That-Prints-Money-Step-by-Step-Setup-27ce1e50bed2805b81c8f27dce224bfa",
    "7_day_sequence": "https://indexsy.notion.site/Sept-30-EP-653-Steal-My-7-Day-Sequence-That-Prints-Appointments-From-Leads-27ee1e50bed2805ea03cd4106874f033",
    
    # Forums / Web 2.0
    "forums_ranking": "https://indexsy.notion.site/Jan-2-EP-726-Google-Is-Secretly-Ranking-Forums-Again-This-One-Makes-Millions-2dce1e50bed2809e8a60fe669308e71e",
    "facebook_groups": "https://indexsy.notion.site/Dec-27-EP-721-Facebook-Groups-are-SO-EASY-Right-Now-DO-THIS-NOW-2d6e1e50bed2805491cdecc43d36101f",
    
    # Ranking Hacks
    "rank_any_website": "https://indexsy.notion.site/Sept-15-EP-639-How-to-rank-ANY-Website-1-in-2025-HACKS-INSIDE-270e1e50bed2809a89c9ce321fa19469",
    "browserblast": "https://indexsy.notion.site/August-9-EP-608-I-can-finally-GUARANTEE-rankings-WITH-BROWSERBLAST-24ae1e50bed280fc9155e5cf650b7f17",
    
    # PBN
    "casino_clapped": "https://indexsy.notion.site/Jan-7-EP-730-Casino-Affiliates-CLAPPED-this-DR89-Site-2e1e1e50bed28030b362f17c3bb246f8",
    
    # Local SEO Citations
    "citation_services": "https://indexsy.notion.site/August-17-EP-616-The-truth-about-local-citation-services-252e1e50bed2806db6d0f96142ef55a6",
    "direction_boost": "https://indexsy.notion.site/Oct-27-EP-677-We-can-finally-GUARANTEE-Google-Maps-rankings-Direction-Boost-299e1e50bed28011b721f2480fc302b1",
}

def scrape_notion_page_via_api(page_id):
    """Try to scrape Notion page using unofficial content endpoints."""
    # Notion's public content API
    url = f"https://indexsy.notion.site/api/v3/loadPageChunk"
    payload = {
        "page": {"id": page_id},
        "limit": 50,
        "cursor": {"stack": []},
        "chunkNumber": 0,
        "verticalColumns": False
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print(f"API error: {e}")
    return None

def extract_page_id(url):
    """Extract page ID from Notion URL."""
    # Format: https://indexsy.notion.site/Title-PageID
    # PageID is the last 32 hex chars after the last dash
    match = re.search(r'-([a-f0-9]{32})(?:\?|$)', url)
    if match:
        page_id = match.group(1)
        # Format as UUID
        return f"{page_id[:8]}-{page_id[8:12]}-{page_id[12:16]}-{page_id[16:20]}-{page_id[20:]}"
    return None

if __name__ == "__main__":
    # Print all URLs for manual scraping reference
    print("Link Building Related Episodes:")
    print("=" * 80)
    for name, url in LINK_BUILDING_EPISODES.items():
        print(f"\n{name}:")
        print(f"  {url}")
        page_id = extract_page_id(url)
        print(f"  Page ID: {page_id}")
