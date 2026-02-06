#!/usr/bin/env python3
"""Test the new granular scoring system"""
import requests
import re
import time

WEBSITES = [
    "trialtribe.com", "dgfirm.law", "munizkimlaw.com", "jalallaw.com",
    "theinjurypartners.com", "barneyinjurylaw.com", "bsinjurylaw.com",
    "eisenberglawgrouppc.com", "dkashlaw.com", "cosselawfirm.com"
]

def analyze(url):
    if not url.startswith('http'):
        url = 'https://' + url
    
    ai_checks = []
    local_checks = []
    
    try:
        # Robots
        robots_score = 10
        try:
            resp = requests.get(url + '/robots.txt', timeout=5)
            text = resp.text.lower()
            if 'user-agent: *' in text and 'disallow: /' in text:
                robots_score = 0
            elif 'gptbot' in text and 'disallow' in text:
                robots_score = 5
            else:
                robots_score = 15
        except:
            robots_score = 10
        ai_checks.append(('Robots', robots_score, 15))
        
        # Fetch page
        resp = requests.get(url, timeout=10)
        html = resp.text
        html_lower = html.lower()
        
        # Schema (0-20)
        schema_score = 0
        if 'application/ld+json' in html_lower:
            schema_score += 5
            if 'faqpage' in html_lower or '"@type":"question"' in html_lower:
                schema_score += 8
            if 'localbusiness' in html_lower or 'legalservice' in html_lower:
                schema_score += 4
            if '"@type":"organization"' in html_lower:
                schema_score += 3
        ai_checks.append(('Schema', min(schema_score, 20), 20))
        
        # Structure (0-15)
        h1 = len(re.findall(r'<h1', html_lower))
        h2 = len(re.findall(r'<h2', html_lower))
        h3 = len(re.findall(r'<h3', html_lower))
        struct_score = 0
        if h1 == 1: struct_score += 5
        elif h1 > 1: struct_score += 2
        if h2 >= 5: struct_score += 6
        elif h2 >= 3: struct_score += 4
        elif h2 >= 1: struct_score += 2
        if h3 >= 3: struct_score += 4
        elif h3 >= 1: struct_score += 2
        ai_checks.append(('Structure', struct_score, 15))
        
        # Meta (0-10)
        meta_score = 0
        title = re.search(r'<title[^>]*>([^<]+)</title>', html, re.I)
        desc = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)', html, re.I)
        if title and 20 < len(title.group(1)) < 70: meta_score += 5
        elif title: meta_score += 2
        if desc and 50 < len(desc.group(1)) < 160: meta_score += 5
        elif desc: meta_score += 2
        ai_checks.append(('Meta', meta_score, 10))
        
        # Content (0-10)
        words = len(re.sub(r'<[^>]+>', ' ', html).split())
        content_score = 0
        if words > 1500: content_score += 5
        elif words > 800: content_score += 3
        elif words > 400: content_score += 1
        if re.search(r'\d+%|\$\d+|million|billion', html): content_score += 3
        if len(re.findall(r'<li', html_lower)) >= 3: content_score += 2
        ai_checks.append(('Content', min(content_score, 10), 10))
        
        # HTTPS (0-10)
        https_score = 10 if url.startswith('https') else 0
        local_checks.append(('HTTPS', https_score, 10))
        
        # NAP (0-20)
        nap_score = 0
        if re.search(r'\(\d{3}\)\s*\d{3}[-.\s]?\d{4}|\d{3}[-.\s]\d{3}[-.\s]\d{4}', html): nap_score += 6
        if re.search(r'\d+\s+[\w\s]+(?:street|st|avenue|ave|road|rd)', html_lower): nap_score += 5
        if re.search(r'\b\d{5}(?:-\d{4})?\b', html): nap_score += 3
        if 'google.com/maps' in html_lower or 'maps.google' in html_lower: nap_score += 6
        local_checks.append(('NAP', nap_score, 20))
        
        # Local KW (0-15)
        kw_score = 0
        legal = sum(1 for t in ['attorney', 'lawyer', 'law firm', 'legal', 'counsel'] if t in html_lower)
        practice = sum(1 for t in ['injury', 'accident', 'personal injury', 'truck accident'] if t in html_lower)
        if legal >= 3: kw_score += 5
        elif legal >= 1: kw_score += 3
        if practice >= 3: kw_score += 6
        elif practice >= 1: kw_score += 3
        if re.search(r'houston|dallas|austin|texas|los angeles|new york', html_lower): kw_score += 4
        local_checks.append(('LocalKW', kw_score, 15))
        
        # Contact (0-10)
        contact_score = 0
        if 'tel:' in html_lower: contact_score += 4
        if 'mailto:' in html_lower or re.search(r'@[\w.-]+\.\w+', html): contact_score += 3
        if 'contact' in html_lower and '<form' in html_lower: contact_score += 3
        local_checks.append(('Contact', contact_score, 10))
        
        # Mobile (0-15)
        mobile_score = 0
        if 'viewport' in html_lower: mobile_score += 5
        if '@media' in html_lower or 'responsive' in html_lower: mobile_score += 5
        if len(html) < 500000: mobile_score += 5
        elif len(html) < 1000000: mobile_score += 3
        local_checks.append(('Mobile', mobile_score, 15))
        
        ai_total = sum(c[1] for c in ai_checks)
        ai_max = sum(c[2] for c in ai_checks)
        ai_score = round(ai_total / ai_max * 100)
        
        local_total = sum(c[1] for c in local_checks)
        local_max = sum(c[2] for c in local_checks)
        local_score = round(local_total / local_max * 100)
        
        total = round((ai_score + local_score) / 2)
        
        return {'url': url, 'ai': ai_score, 'local': local_score, 'total': total, 'ai_checks': ai_checks, 'local_checks': local_checks}
    except Exception as e:
        return {'url': url, 'error': str(e)[:40]}

print("Testing granular scoring (10 checks)...")
print("-" * 80)
results = []
for url in WEBSITES:
    r = analyze(url)
    results.append(r)
    if 'error' in r:
        print(f"{url}: ERROR - {r['error']}")
    else:
        print(f"{url}: AI={r['ai']} Local={r['local']} Total={r['total']}")
    time.sleep(0.5)

print("\n" + "=" * 80)
print("Score distribution:")
ai_scores = [r['ai'] for r in results if 'ai' in r]
local_scores = [r['local'] for r in results if 'local' in r]
total_scores = [r['total'] for r in results if 'total' in r]

print(f"AI scores:    {sorted(ai_scores)}")
print(f"Local scores: {sorted(local_scores)}")
print(f"Total scores: {sorted(total_scores)}")
print(f"\nUnique AI scores: {len(set(ai_scores))}/{len(ai_scores)}")
print(f"Unique Local scores: {len(set(local_scores))}/{len(local_scores)}")
print(f"Unique Total scores: {len(set(total_scores))}/{len(total_scores)}")
