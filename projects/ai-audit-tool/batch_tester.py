#!/usr/bin/env python3
"""
Batch tester for AI & Local Visibility Audit Tool
Tests against many law firm websites to validate accuracy and performance
"""

import csv
import json
import time
import random
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
import os
import sys

from enhanced_analyzer import EnhancedWebsiteAnalyzer, AuditResult

# Sample law firm domains to test (will expand)
SAMPLE_LAW_FIRMS = [
    # National firms
    "forthepeople.com",
    "johnfoy.com", 
    "1800lawfirm.com",
    "weitzlux.com",
    "bfrlaw.com",
    "cellino.com",
    "herrmanandherrman.com",
    "joyelawfirm.com",
    "tlsslaw.com",
    "legalfinders.com",
    
    # Regional/local firms
    "injurytriallawyers.com",
    "rosenfeldinjurylawyers.com",
    "freeadvice.com",
    "nolo.com",
    "justia.com",
    "findlaw.com",
    "avvo.com",
    "lawinfo.com",
    "lawyers.com",
    "martindale.com",
    
    # More PI firms
    "millerandzois.com",
    "edgarlitigation.com", 
    "injuryclaimcoach.com",
    "accidentclaimlawyers.com",
    "personalinjurylawyers.com",
    "caraccidentlawyer.com",
    "autoaccidentlawyerhelp.com",
    "injurylawyernetwork.com",
    "accidentattorneys.org",
    "injuryattorneyflorida.com",
]


def get_law_firm_urls_from_serp() -> list:
    """
    Would use DataForSEO or SerpAPI to get real law firm URLs
    For now, returns expanded sample list
    """
    # Expand sample list by variations
    expanded = []
    
    # Base domains
    expanded.extend(SAMPLE_LAW_FIRMS)
    
    # Add more from common patterns (mock data for testing)
    cities = ['houston', 'dallas', 'austin', 'phoenix', 'atlanta', 'miami', 'tampa', 
              'orlando', 'chicago', 'detroit', 'cleveland', 'denver', 'seattle',
              'portland', 'losangeles', 'sandiego', 'sacramento', 'lasvegas']
    
    patterns = [
        '{city}caraccidentlawyer.com',
        '{city}injurylawyer.com', 
        '{city}personalinjury.com',
        '{city}accidentattorney.com',
    ]
    
    for city in cities[:25]:
        for pattern in patterns[:2]:
            expanded.append(pattern.format(city=city))
            
    return expanded


def run_single_audit(url: str, timeout: int = 60) -> dict:
    """Run audit on a single URL with timeout"""
    start_time = time.time()
    
    try:
        if not url.startswith('http'):
            url = f'https://{url}'
            
        analyzer = EnhancedWebsiteAnalyzer(url)
        result = analyzer.run_full_audit()
        
        elapsed = time.time() - start_time
        
        return {
            'url': url,
            'success': True,
            'business_name': result.business_name,
            'grade': result.grade,
            'ai_score': result.ai_visibility_score,
            'local_score': result.local_seo_score,
            'total_score': result.total_score,
            'elapsed_seconds': round(elapsed, 2),
            'error': None,
            'ai_breakdown': {cat.name: cat.score for cat in result.ai_categories},
            'local_breakdown': {cat.name: cat.score for cat in result.local_categories},
            'quick_wins': result.quick_wins[:3],
            'priority_fixes': result.priority_fixes[:3],
        }
        
    except Exception as e:
        elapsed = time.time() - start_time
        return {
            'url': url,
            'success': False,
            'business_name': None,
            'grade': None,
            'ai_score': None,
            'local_score': None,
            'total_score': None,
            'elapsed_seconds': round(elapsed, 2),
            'error': str(e),
            'ai_breakdown': {},
            'local_breakdown': {},
            'quick_wins': [],
            'priority_fixes': [],
        }


def run_batch_test(urls: list, max_workers: int = 5, output_dir: str = './results') -> dict:
    """Run batch test across multiple URLs"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results = []
    
    total = len(urls)
    completed = 0
    success_count = 0
    fail_count = 0
    
    print(f"\n🚀 Starting batch test of {total} URLs")
    print(f"   Workers: {max_workers}")
    print(f"   Output: {output_dir}")
    print("=" * 60)
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(run_single_audit, url): url for url in urls}
        
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            completed += 1
            
            try:
                result = future.result()
                results.append(result)
                
                if result['success']:
                    success_count += 1
                    print(f"[{completed}/{total}] ✅ {result['url'][:40]}... Grade: {result['grade']} ({result['total_score']}/200) in {result['elapsed_seconds']}s")
                else:
                    fail_count += 1
                    print(f"[{completed}/{total}] ❌ {result['url'][:40]}... Error: {result['error'][:50]}")
                    
            except Exception as e:
                fail_count += 1
                print(f"[{completed}/{total}] ❌ {url[:40]}... Exception: {str(e)[:50]}")
                results.append({
                    'url': url,
                    'success': False,
                    'error': str(e),
                })
                
    elapsed_total = time.time() - start_time
    
    # Calculate statistics
    successful_results = [r for r in results if r['success']]
    
    stats = {
        'total_urls': total,
        'successful': success_count,
        'failed': fail_count,
        'success_rate': round(success_count / total * 100, 1) if total > 0 else 0,
        'total_time_seconds': round(elapsed_total, 1),
        'avg_time_per_site': round(elapsed_total / total, 2) if total > 0 else 0,
        'timestamp': timestamp,
    }
    
    if successful_results:
        scores = [r['total_score'] for r in successful_results if r['total_score'] is not None]
        ai_scores = [r['ai_score'] for r in successful_results if r['ai_score'] is not None]
        local_scores = [r['local_score'] for r in successful_results if r['local_score'] is not None]
        
        stats['score_avg'] = round(sum(scores) / len(scores), 1) if scores else 0
        stats['score_min'] = min(scores) if scores else 0
        stats['score_max'] = max(scores) if scores else 0
        stats['ai_avg'] = round(sum(ai_scores) / len(ai_scores), 1) if ai_scores else 0
        stats['local_avg'] = round(sum(local_scores) / len(local_scores), 1) if local_scores else 0
        
        # Grade distribution
        grades = [r['grade'] for r in successful_results if r['grade']]
        stats['grade_distribution'] = {g: grades.count(g) for g in set(grades)}
        
    # Save results
    results_file = os.path.join(output_dir, f'batch_results_{timestamp}.json')
    with open(results_file, 'w') as f:
        json.dump({
            'stats': stats,
            'results': results
        }, f, indent=2)
        
    # Save CSV for easy viewing
    csv_file = os.path.join(output_dir, f'batch_results_{timestamp}.csv')
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['URL', 'Success', 'Business', 'Grade', 'AI Score', 'Local Score', 'Total', 'Time(s)', 'Error'])
        for r in results:
            writer.writerow([
                r.get('url', ''),
                r.get('success', False),
                r.get('business_name', ''),
                r.get('grade', ''),
                r.get('ai_score', ''),
                r.get('local_score', ''),
                r.get('total_score', ''),
                r.get('elapsed_seconds', ''),
                r.get('error', '')[:100] if r.get('error') else ''
            ])
            
    # Print summary
    print("\n" + "=" * 60)
    print("📊 BATCH TEST SUMMARY")
    print("=" * 60)
    print(f"   Total URLs: {stats['total_urls']}")
    print(f"   Successful: {stats['successful']} ({stats['success_rate']}%)")
    print(f"   Failed: {stats['failed']}")
    print(f"   Total Time: {stats['total_time_seconds']}s")
    print(f"   Avg per Site: {stats['avg_time_per_site']}s")
    
    if 'score_avg' in stats:
        print(f"\n   Score Average: {stats['score_avg']}/200")
        print(f"   Score Range: {stats['score_min']} - {stats['score_max']}")
        print(f"   AI Avg: {stats['ai_avg']}/100")
        print(f"   Local Avg: {stats['local_avg']}/100")
        
    if 'grade_distribution' in stats:
        print(f"\n   Grade Distribution:")
        for grade in ['A', 'B+', 'B', 'C+', 'C', 'D', 'F']:
            count = stats['grade_distribution'].get(grade, 0)
            if count > 0:
                bar = '█' * min(count, 20)
                print(f"      {grade}: {bar} ({count})")
                
    print(f"\n   Results saved to:")
    print(f"      {results_file}")
    print(f"      {csv_file}")
    
    return {'stats': stats, 'results': results}


def get_urls_from_dataforseo(keyword: str = "car accident lawyer", location: str = "United States", limit: int = 100) -> list:
    """
    Get real law firm URLs from DataForSEO SERP API
    """
    import base64
    
    # DataForSEO credentials
    creds_path = os.path.expanduser("~/.config/dataforseo/credentials.json")
    if os.path.exists(creds_path):
        with open(creds_path) as f:
            creds = json.load(f)
            login = creds.get('login', 'mark@kuriosbrand.com')
            password = creds.get('password', 'b292b4a5e686bc75')
    else:
        login = 'mark@kuriosbrand.com'
        password = 'b292b4a5e686bc75'
        
    auth = base64.b64encode(f"{login}:{password}".encode()).decode()
    
    headers = {
        'Authorization': f'Basic {auth}',
        'Content-Type': 'application/json'
    }
    
    # SERP endpoint
    endpoint = "https://api.dataforseo.com/v3/serp/google/organic/live/advanced"
    
    payload = [{
        "keyword": keyword,
        "location_name": location,
        "language_name": "English",
        "depth": min(limit, 100),
        "se_domain": "google.com"
    }]
    
    try:
        import requests
        resp = requests.post(endpoint, json=payload, headers=headers, timeout=60)
        data = resp.json()
        
        if data.get('status_code') == 20000:
            urls = []
            for task in data.get('tasks', []):
                for result in task.get('result', []):
                    for item in result.get('items', []):
                        if item.get('type') == 'organic':
                            url = item.get('url')
                            if url:
                                urls.append(url)
                                
            return urls[:limit]
    except Exception as e:
        print(f"DataForSEO error: {e}")
        
    return []


def main():
    """Run batch test"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Batch test AI & Local Visibility Audit')
    parser.add_argument('--count', type=int, default=50, help='Number of sites to test')
    parser.add_argument('--workers', type=int, default=5, help='Concurrent workers')
    parser.add_argument('--output', type=str, default='./results', help='Output directory')
    parser.add_argument('--use-serp', action='store_true', help='Use DataForSEO for real URLs')
    parser.add_argument('--keyword', type=str, default='car accident lawyer', help='SERP keyword')
    
    args = parser.parse_args()
    
    # Get URLs
    if args.use_serp:
        print(f"🔍 Fetching URLs from DataForSEO for: '{args.keyword}'...")
        urls = get_urls_from_dataforseo(args.keyword, limit=args.count)
        print(f"   Found {len(urls)} URLs from SERP")
    else:
        # Use sample + generated URLs
        urls = get_law_firm_urls_from_serp()
        
    # Limit to requested count
    urls = urls[:args.count]
    
    if not urls:
        print("❌ No URLs to test!")
        return
        
    # Run batch test
    results = run_batch_test(
        urls=urls,
        max_workers=args.workers,
        output_dir=args.output
    )
    
    return results


if __name__ == "__main__":
    main()
