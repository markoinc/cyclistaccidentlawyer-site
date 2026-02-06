#!/usr/bin/env python3
"""Test the visibility calculator against real law firm websites"""

import requests
import re
import json
import time

WEBSITES = [
    ("Rich Hyde", "trialtribe.com"),
    ("Dagmawi Getachew", "dgfirm.law"),
    ("Lucas Naccarati", "munizkimlaw.com"),
    ("Jalal Abdallah", "jalallaw.com"),
    ("Omeed Hakimianpour", "theinjurypartners.com"),
    ("Scott Barney", "barneyinjurylaw.com"),
    ("Josh Sweeney", "shanesmithlaw.com"),
    ("Michael Shirts", "bsinjurylaw.com"),
    ("Jason E", "eisenberglawgrouppc.com"),
    ("David Kashani", "dkashlaw.com"),
]

def analyze_website(url):
    """Analyze a website for AI and Local SEO visibility"""
    if not url.startswith('http'):
        url = 'https://' + url
    
    results = {
        'url': url,
        'checks': [],
        'ai_score': 0,
        'local_score': 0,
    }
    
    # Check robots.txt
    try:
        robots_url = url.rstrip('/') + '/robots.txt'
        resp = requests.get(robots_url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        robots_text = resp.text.lower()
        
        # Check if AI bots are blocked
        blocks_all = 'user-agent: *' in robots_text and 'disallow: /' in robots_text
        blocks_gptbot = 'user-agent: gptbot' in robots_text and 'disallow' in robots_text
        
        if blocks_all:
            results['checks'].append(('AI Crawler Access', 'FAIL', 0, 10, 'Blocks all bots'))
        elif blocks_gptbot:
            results['checks'].append(('AI Crawler Access', 'WARN', 5, 10, 'Blocks GPTBot specifically'))
        else:
            results['checks'].append(('AI Crawler Access', 'PASS', 10, 10, 'AI crawlers allowed'))
    except Exception as e:
        results['checks'].append(('AI Crawler Access', 'WARN', 5, 10, f'Could not check: {str(e)[:30]}'))
    
    # Check main page content
    try:
        resp = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
        html = resp.text
        html_lower = html.lower()
        
        # Check for schema markup
        has_jsonld = 'application/ld+json' in html_lower
        has_faq = 'faqpage' in html_lower or '"@type":"question"' in html_lower
        has_local = 'localbusiness' in html_lower or 'legalservice' in html_lower or 'attorney' in html_lower
        has_org = '"@type":"organization"' in html_lower
        
        schema_score = 0
        schema_details = []
        if has_jsonld:
            schema_score += 3
            schema_details.append('JSON-LD')
        if has_faq:
            schema_score += 4
            schema_details.append('FAQ')
        if has_local:
            schema_score += 2
            schema_details.append('LocalBusiness')
        if has_org:
            schema_score += 1
            schema_details.append('Organization')
        
        status = 'PASS' if schema_score >= 7 else 'WARN' if schema_score >= 3 else 'FAIL'
        results['checks'].append(('Schema Markup', status, schema_score, 10, ', '.join(schema_details) or 'None found'))
        
        # Check content structure
        h1_count = len(re.findall(r'<h1', html_lower))
        h2_count = len(re.findall(r'<h2', html_lower))
        
        if h1_count == 1 and h2_count >= 3:
            results['checks'].append(('Content Structure', 'PASS', 8, 10, f'{h1_count} H1, {h2_count} H2s'))
        elif h2_count >= 2:
            results['checks'].append(('Content Structure', 'WARN', 5, 10, f'{h1_count} H1, {h2_count} H2s'))
        else:
            results['checks'].append(('Content Structure', 'FAIL', 2, 10, f'Poor: {h1_count} H1, {h2_count} H2s'))
        
        # Check HTTPS
        is_https = url.startswith('https')
        results['checks'].append(('HTTPS', 'PASS' if is_https else 'FAIL', 10 if is_https else 0, 10, 'Secure' if is_https else 'Not secure'))
        
        # Check NAP (Name, Address, Phone)
        has_phone = bool(re.search(r'\(\d{3}\)\s*\d{3}[-.\s]?\d{4}|\d{3}[-.\s]\d{3}[-.\s]\d{4}', html))
        has_address = bool(re.search(r'\d+\s+[\w\s]+(?:street|st|avenue|ave|road|rd|boulevard|blvd|drive|dr|lane|ln|way|court|ct)', html_lower))
        has_map = 'google.com/maps' in html_lower or 'maps.google' in html_lower
        
        nap_score = (3 if has_phone else 0) + (3 if has_address else 0) + (4 if has_map else 0)
        nap_details = ', '.join(filter(None, ['Phone' if has_phone else None, 'Address' if has_address else None, 'Map' if has_map else None])) or 'None found'
        status = 'PASS' if nap_score >= 7 else 'WARN' if nap_score >= 4 else 'FAIL'
        results['checks'].append(('NAP Info', status, nap_score, 10, nap_details))
        
        # Check for local keywords
        local_terms = ['attorney', 'lawyer', 'law firm', 'legal', 'injury', 'accident']
        has_local_keywords = any(term in html_lower for term in local_terms)
        results['checks'].append(('Local Keywords', 'PASS' if has_local_keywords else 'WARN', 8 if has_local_keywords else 3, 10, 'Found' if has_local_keywords else 'Limited'))
        
    except Exception as e:
        results['checks'].append(('Page Analysis', 'FAIL', 0, 10, f'Error: {str(e)[:40]}'))
    
    # Calculate scores
    ai_checks = [c for c in results['checks'] if c[0] in ['AI Crawler Access', 'Schema Markup', 'Content Structure']]
    local_checks = [c for c in results['checks'] if c[0] in ['HTTPS', 'NAP Info', 'Local Keywords']]
    
    if ai_checks:
        results['ai_score'] = round(sum(c[2] for c in ai_checks) / sum(c[3] for c in ai_checks) * 100)
    if local_checks:
        results['local_score'] = round(sum(c[2] for c in local_checks) / sum(c[3] for c in local_checks) * 100)
    
    results['total_score'] = round((results['ai_score'] + results['local_score']) / 2)
    
    return results

def main():
    print("=" * 80)
    print("VISIBILITY CALCULATOR TEST - 10 Law Firms from Kurios MVA Appointments")
    print("=" * 80)
    print()
    
    all_results = []
    
    for name, website in WEBSITES:
        print(f"Testing: {name} ({website})")
        print("-" * 60)
        
        result = analyze_website(website)
        all_results.append({'name': name, **result})
        
        print(f"  AI Score:    {result['ai_score']}/100")
        print(f"  Local Score: {result['local_score']}/100")
        print(f"  Total Score: {result['total_score']}/100")
        print()
        print("  Checks:")
        for check in result['checks']:
            status_icon = '✓' if check[1] == 'PASS' else '!' if check[1] == 'WARN' else '✗'
            print(f"    [{status_icon}] {check[0]}: {check[4]} ({check[2]}/{check[3]})")
        print()
        
        time.sleep(1)  # Be nice to servers
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"{'Name':<25} {'Website':<30} {'AI':>5} {'Local':>6} {'Total':>6}")
    print("-" * 80)
    for r in all_results:
        print(f"{r['name']:<25} {r['url']:<30} {r['ai_score']:>5} {r['local_score']:>6} {r['total_score']:>6}")
    
    avg_ai = sum(r['ai_score'] for r in all_results) / len(all_results)
    avg_local = sum(r['local_score'] for r in all_results) / len(all_results)
    avg_total = sum(r['total_score'] for r in all_results) / len(all_results)
    print("-" * 80)
    print(f"{'AVERAGE':<25} {'':<30} {avg_ai:>5.0f} {avg_local:>6.0f} {avg_total:>6.0f}")

if __name__ == '__main__':
    main()
