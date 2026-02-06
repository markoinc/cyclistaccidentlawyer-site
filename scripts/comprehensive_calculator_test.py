#!/usr/bin/env python3
"""
Comprehensive Calculator Validation Test
Tests scoring accuracy across multiple dimensions
"""

import requests
import re
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Extended list of law firm websites to test
TEST_WEBSITES = [
    # From Kurios MVA Appointments
    "trialtribe.com", "dgfirm.law", "munizkimlaw.com", "jalallaw.com",
    "theinjurypartners.com", "barneyinjurylaw.com", "shanesmithlaw.com",
    "bsinjurylaw.com", "eisenberglawgrouppc.com", "dkashlaw.com",
    "cosselawfirm.com", "reydelaley.com", "rmdlaw.com", "jslawgroup.net",
    "highstakesinjurylaw.com",
    # Additional PI law firms for broader testing
    "morrisbart.com", "tlf.legal", "forthepeople.com", "rosenfeldinjurylawyers.com",
    "atticuslaw.com", "1800thelaw2.com", "800goldlaw.com", "joyelawfirm.com",
    "cellinolaw.com", "gersterlawfirm.com", "herrmanandherrman.com",
    "ketterman-law.com", "injurylawyer.com", "sullivanandgalleshaw.com",
    "dallascarwreck.com", "joyelawfirm.com", "texastriallaw.com",
    # Known good SEO sites (control group)
    "nolo.com", "findlaw.com", "avvo.com",
]

def check_robots_txt(url):
    """Check robots.txt for AI crawler access"""
    try:
        robots_url = url.rstrip('/') + '/robots.txt'
        resp = requests.get(robots_url, timeout=8, headers={'User-Agent': 'Mozilla/5.0'})
        if resp.status_code != 200:
            return {'status': 'warning', 'score': 5, 'detail': 'No robots.txt found'}
        
        text = resp.text.lower()
        
        # Check for specific AI bot blocks
        gptbot_blocked = 'user-agent: gptbot' in text and 'disallow' in text.split('user-agent: gptbot')[1][:100] if 'user-agent: gptbot' in text else False
        claude_blocked = 'user-agent: claudebot' in text or 'user-agent: claude-web' in text
        
        # Check for blanket block
        blanket_block = False
        if 'user-agent: *' in text:
            after_star = text.split('user-agent: *')[1][:200] if 'user-agent: *' in text else ''
            if 'disallow: /' in after_star and 'disallow: /.' not in after_star:
                blanket_block = True
        
        if blanket_block:
            return {'status': 'fail', 'score': 0, 'detail': 'Blocks all bots'}
        elif gptbot_blocked:
            return {'status': 'fail', 'score': 2, 'detail': 'GPTBot specifically blocked'}
        elif claude_blocked:
            return {'status': 'warning', 'score': 5, 'detail': 'Some AI bots blocked'}
        else:
            return {'status': 'pass', 'score': 10, 'detail': 'AI crawlers allowed'}
    except Exception as e:
        return {'status': 'warning', 'score': 5, 'detail': f'Check failed: {str(e)[:30]}'}

def check_schema(html):
    """Check for schema markup"""
    html_lower = html.lower()
    
    has_jsonld = 'application/ld+json' in html_lower
    has_faq = 'faqpage' in html_lower or '"@type":"question"' in html_lower or '"@type": "question"' in html_lower
    has_local = any(term in html_lower for term in ['localbusiness', 'legalservice', 'attorneysandlawfirms', '"attorney"'])
    has_org = '"@type":"organization"' in html_lower or '"@type": "organization"' in html_lower
    has_article = '"@type":"article"' in html_lower or '"@type": "article"' in html_lower
    
    score = 0
    found = []
    
    if has_jsonld:
        score += 2
        found.append('JSON-LD')
    if has_faq:
        score += 4
        found.append('FAQ')
    if has_local:
        score += 2
        found.append('LocalBusiness')
    if has_org:
        score += 1
        found.append('Organization')
    if has_article:
        score += 1
        found.append('Article')
    
    status = 'pass' if score >= 7 else 'warning' if score >= 3 else 'fail'
    return {'status': status, 'score': min(score, 10), 'detail': ', '.join(found) or 'None', 'found': found}

def check_content_structure(html):
    """Check heading structure"""
    h1_count = len(re.findall(r'<h1[^>]*>', html, re.IGNORECASE))
    h2_count = len(re.findall(r'<h2[^>]*>', html, re.IGNORECASE))
    h3_count = len(re.findall(r'<h3[^>]*>', html, re.IGNORECASE))
    
    # Ideal: 1 H1, 3+ H2s
    if h1_count == 1 and h2_count >= 3:
        score = 10
        status = 'pass'
    elif h1_count == 1 and h2_count >= 1:
        score = 7
        status = 'pass'
    elif h2_count >= 2:
        score = 5
        status = 'warning'
    else:
        score = 2
        status = 'fail'
    
    return {'status': status, 'score': score, 'detail': f'{h1_count} H1, {h2_count} H2, {h3_count} H3'}

def check_nap(html):
    """Check for NAP (Name, Address, Phone)"""
    # Phone patterns
    phone_patterns = [
        r'\(\d{3}\)\s*\d{3}[-.\s]?\d{4}',
        r'\d{3}[-.\s]\d{3}[-.\s]\d{4}',
        r'1[-.\s]?\d{3}[-.\s]\d{3}[-.\s]\d{4}',
        r'tel:\+?1?\d{10,11}',
    ]
    has_phone = any(re.search(p, html) for p in phone_patterns)
    
    # Address patterns
    address_patterns = [
        r'\d+\s+[\w\s]+(?:street|st|avenue|ave|road|rd|boulevard|blvd|drive|dr|lane|ln|way|court|ct|suite|ste)',
        r'\b\d{5}(?:-\d{4})?\b',  # ZIP code
    ]
    has_address = any(re.search(p, html, re.IGNORECASE) for p in address_patterns)
    
    # Map embed
    html_lower = html.lower()
    has_map = 'google.com/maps' in html_lower or 'maps.google' in html_lower or ('iframe' in html_lower and 'map' in html_lower)
    
    score = (4 if has_phone else 0) + (3 if has_address else 0) + (3 if has_map else 0)
    found = [x for x in ['Phone' if has_phone else None, 'Address' if has_address else None, 'Map' if has_map else None] if x]
    
    status = 'pass' if score >= 7 else 'warning' if score >= 4 else 'fail'
    return {'status': status, 'score': score, 'detail': ', '.join(found) or 'None found'}

def analyze_site(url):
    """Full analysis of a single site"""
    if not url.startswith('http'):
        url = 'https://' + url
    
    result = {
        'url': url,
        'checks': {},
        'ai_score': 0,
        'local_score': 0,
        'total_score': 0,
        'error': None
    }
    
    try:
        # Robots.txt check
        robots = check_robots_txt(url)
        result['checks']['robots'] = robots
        
        # Fetch main page
        resp = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
        html = resp.text
        
        # Schema check
        schema = check_schema(html)
        result['checks']['schema'] = schema
        
        # Content structure
        structure = check_content_structure(html)
        result['checks']['structure'] = structure
        
        # HTTPS
        is_https = url.startswith('https')
        result['checks']['https'] = {'status': 'pass' if is_https else 'fail', 'score': 10 if is_https else 0, 'detail': 'Secure' if is_https else 'Not secure'}
        
        # NAP
        nap = check_nap(html)
        result['checks']['nap'] = nap
        
        # Local keywords
        local_terms = ['attorney', 'lawyer', 'law firm', 'legal', 'injury', 'accident', 'personal injury']
        has_local = sum(1 for term in local_terms if term in html.lower()) >= 2
        result['checks']['local_kw'] = {'status': 'pass' if has_local else 'warning', 'score': 8 if has_local else 3, 'detail': 'Found' if has_local else 'Limited'}
        
        # Calculate scores
        ai_checks = ['robots', 'schema', 'structure']
        local_checks = ['https', 'nap', 'local_kw']
        
        ai_total = sum(result['checks'][c]['score'] for c in ai_checks)
        ai_max = 30
        result['ai_score'] = round(ai_total / ai_max * 100)
        
        local_total = sum(result['checks'][c]['score'] for c in local_checks)
        local_max = 28
        result['local_score'] = round(local_total / local_max * 100)
        
        result['total_score'] = round((result['ai_score'] + result['local_score']) / 2)
        
    except Exception as e:
        result['error'] = str(e)[:50]
    
    return result

def run_consistency_test(url, runs=5):
    """Run multiple times to check consistency"""
    scores = []
    for i in range(runs):
        result = analyze_site(url)
        scores.append((result['ai_score'], result['local_score'], result['total_score']))
        time.sleep(0.5)
    
    # Check if all runs are identical
    all_same = len(set(scores)) == 1
    return {'url': url, 'scores': scores, 'consistent': all_same}

def main():
    print("=" * 100)
    print("COMPREHENSIVE VISIBILITY CALCULATOR VALIDATION")
    print("=" * 100)
    
    # Phase 1: Test all websites once
    print("\n[PHASE 1] Testing all websites...")
    print("-" * 100)
    
    results = []
    for i, url in enumerate(TEST_WEBSITES):
        print(f"  [{i+1}/{len(TEST_WEBSITES)}] Testing {url}...", end=" ", flush=True)
        result = analyze_site(url)
        results.append(result)
        if result['error']:
            print(f"ERROR: {result['error']}")
        else:
            print(f"AI:{result['ai_score']} Local:{result['local_score']} Total:{result['total_score']}")
        time.sleep(0.5)
    
    # Phase 2: Consistency test on sample
    print("\n[PHASE 2] Consistency testing (5 runs each on 10 random sites)...")
    print("-" * 100)
    
    sample_urls = TEST_WEBSITES[:10]
    consistency_results = []
    for url in sample_urls:
        print(f"  Testing {url} x5...", end=" ", flush=True)
        cons = run_consistency_test(url)
        consistency_results.append(cons)
        print("✓ CONSISTENT" if cons['consistent'] else f"✗ VARIED: {cons['scores']}")
    
    # Summary
    print("\n" + "=" * 100)
    print("SUMMARY")
    print("=" * 100)
    
    # Score distribution
    ai_scores = [r['ai_score'] for r in results if not r['error']]
    local_scores = [r['local_score'] for r in results if not r['error']]
    total_scores = [r['total_score'] for r in results if not r['error']]
    
    print(f"\nSites tested: {len(results)}")
    print(f"Successful: {len([r for r in results if not r['error']])}")
    print(f"Errors: {len([r for r in results if r['error']])}")
    
    print(f"\nAI Visibility Scores:")
    print(f"  Min: {min(ai_scores)}, Max: {max(ai_scores)}, Avg: {sum(ai_scores)/len(ai_scores):.1f}")
    print(f"  Distribution: 0-30: {len([s for s in ai_scores if s < 30])}, 30-60: {len([s for s in ai_scores if 30 <= s < 60])}, 60-80: {len([s for s in ai_scores if 60 <= s < 80])}, 80+: {len([s for s in ai_scores if s >= 80])}")
    
    print(f"\nLocal Visibility Scores:")
    print(f"  Min: {min(local_scores)}, Max: {max(local_scores)}, Avg: {sum(local_scores)/len(local_scores):.1f}")
    print(f"  Distribution: 0-30: {len([s for s in local_scores if s < 30])}, 30-60: {len([s for s in local_scores if 30 <= s < 60])}, 60-80: {len([s for s in local_scores if 60 <= s < 80])}, 80+: {len([s for s in local_scores if s >= 80])}")
    
    print(f"\nConsistency: {sum(1 for c in consistency_results if c['consistent'])}/{len(consistency_results)} sites returned identical scores across 5 runs")
    
    # Detailed results table
    print("\n" + "-" * 100)
    print(f"{'Website':<35} {'AI':>5} {'Local':>6} {'Total':>6} {'Robots':<12} {'Schema':<20} {'NAP':<15}")
    print("-" * 100)
    for r in sorted(results, key=lambda x: x['total_score'], reverse=True):
        if not r['error']:
            robots = r['checks'].get('robots', {}).get('status', '?')[:4]
            schema = r['checks'].get('schema', {}).get('detail', '?')[:18]
            nap = r['checks'].get('nap', {}).get('detail', '?')[:13]
            print(f"{r['url']:<35} {r['ai_score']:>5} {r['local_score']:>6} {r['total_score']:>6} {robots:<12} {schema:<20} {nap:<15}")
    
    # Check accuracy indicators
    print("\n" + "=" * 100)
    print("ACCURACY VALIDATION")
    print("=" * 100)
    
    # Known good sites should score higher
    known_good = ['nolo.com', 'findlaw.com', 'avvo.com']
    good_scores = [r['total_score'] for r in results if any(g in r['url'] for g in known_good) and not r['error']]
    other_scores = [r['total_score'] for r in results if not any(g in r['url'] for g in known_good) and not r['error']]
    
    if good_scores and other_scores:
        print(f"\nKnown good sites avg: {sum(good_scores)/len(good_scores):.1f}")
        print(f"Other sites avg: {sum(other_scores)/len(other_scores):.1f}")
        if sum(good_scores)/len(good_scores) > sum(other_scores)/len(other_scores):
            print("✓ Known good sites score higher on average (expected)")
        else:
            print("! Known good sites don't score higher - may need calibration")
    
    print("\n✓ Test complete")

if __name__ == '__main__':
    main()
