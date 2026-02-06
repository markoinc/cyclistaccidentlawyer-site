#!/usr/bin/env python3
"""
Run 1000-site stress test across multiple keywords
"""

import json
import time
import os
import sys
import base64
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# Add parent to path
sys.path.insert(0, os.path.dirname(__file__))

from enhanced_analyzer import EnhancedWebsiteAnalyzer


def get_urls_from_dataforseo(keyword: str, location: str = "United States", limit: int = 100) -> list:
    """Get real URLs from DataForSEO SERP API"""
    login = 'mark@kuriosbrand.com'
    password = 'b292b4a5e686bc75'
    auth = base64.b64encode(f"{login}:{password}".encode()).decode()
    
    headers = {
        'Authorization': f'Basic {auth}',
        'Content-Type': 'application/json'
    }
    
    endpoint = "https://api.dataforseo.com/v3/serp/google/organic/live/advanced"
    
    payload = [{
        "keyword": keyword,
        "location_name": location,
        "language_name": "English",
        "depth": min(limit, 100),
        "se_domain": "google.com"
    }]
    
    try:
        resp = requests.post(endpoint, json=payload, headers=headers, timeout=60)
        data = resp.json()
        
        if data.get('status_code') == 20000:
            urls = []
            for task in data.get('tasks', []):
                for result in task.get('result', []):
                    for item in result.get('items', []):
                        if item.get('type') == 'organic':
                            url = item.get('url')
                            if url and 'youtube.com' not in url and 'facebook.com' not in url:
                                urls.append(url)
            return urls[:limit]
    except Exception as e:
        print(f"DataForSEO error for '{keyword}': {e}")
    return []


def run_audit(url: str) -> dict:
    """Run single audit"""
    start = time.time()
    try:
        analyzer = EnhancedWebsiteAnalyzer(url)
        result = analyzer.run_full_audit()
        elapsed = time.time() - start
        
        return {
            'url': url,
            'success': True,
            'grade': result.grade,
            'ai_score': result.ai_visibility_score,
            'local_score': result.local_seo_score,
            'total_score': result.total_score,
            'elapsed': round(elapsed, 2),
            'error': None
        }
    except Exception as e:
        return {
            'url': url,
            'success': False,
            'grade': None,
            'ai_score': None,
            'local_score': None,
            'total_score': None,
            'elapsed': round(time.time() - start, 2),
            'error': str(e)
        }


def main():
    # Keywords to search (will get ~100 URLs each)
    keywords = [
        # PI variations
        "personal injury lawyer",
        "car accident lawyer",
        "truck accident attorney",
        "motorcycle accident lawyer",
        "slip and fall lawyer",
        "medical malpractice attorney",
        "wrongful death lawyer",
        
        # City-specific
        "houston personal injury lawyer",
        "los angeles car accident attorney",
        "miami personal injury lawyer",
        "chicago injury attorney",
        "dallas accident lawyer",
        "phoenix car accident lawyer",
        "atlanta personal injury attorney",
        "denver injury lawyer",
        "seattle car accident attorney",
        "boston injury lawyer",
    ]
    
    print("=" * 70)
    print("🚀 1000-SITE STRESS TEST")
    print("=" * 70)
    
    # Collect URLs from multiple keywords
    all_urls = set()
    
    for kw in keywords:
        print(f"Fetching: '{kw}'...", end=" ")
        urls = get_urls_from_dataforseo(kw, limit=100)
        new_urls = len(urls) - len(all_urls.intersection(urls))
        all_urls.update(urls)
        print(f"+{new_urls} new ({len(all_urls)} total)")
        time.sleep(0.5)  # Rate limit
        
        if len(all_urls) >= 1000:
            break
    
    urls = list(all_urls)[:1000]
    
    print(f"\n📊 Testing {len(urls)} unique URLs")
    print("-" * 70)
    
    results = []
    start_time = time.time()
    
    # Run with 10 workers
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(run_audit, url): url for url in urls}
        
        completed = 0
        for future in as_completed(futures):
            completed += 1
            result = future.result()
            results.append(result)
            
            if completed % 50 == 0 or completed == len(urls):
                success = sum(1 for r in results if r['success'] and r['total_score'] and r['total_score'] > 0)
                avg_score = sum(r['total_score'] for r in results if r['total_score']) / max(1, success)
                elapsed = time.time() - start_time
                rate = completed / elapsed
                print(f"[{completed}/{len(urls)}] Success: {success} | Avg: {avg_score:.0f}/200 | Rate: {rate:.1f}/s")
    
    total_time = time.time() - start_time
    
    # Calculate stats
    valid_results = [r for r in results if r['success'] and r['total_score'] and r['total_score'] > 0]
    
    scores = [r['total_score'] for r in valid_results]
    ai_scores = [r['ai_score'] for r in valid_results]
    local_scores = [r['local_score'] for r in valid_results]
    grades = [r['grade'] for r in valid_results]
    
    grade_dist = {}
    for g in ['A', 'B+', 'B', 'C+', 'C', 'D', 'F']:
        grade_dist[g] = grades.count(g)
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output = {
        'timestamp': timestamp,
        'total_urls': len(urls),
        'valid_results': len(valid_results),
        'failed': len(urls) - len(valid_results),
        'total_time_seconds': round(total_time, 1),
        'urls_per_second': round(len(urls) / total_time, 2),
        'score_average': round(sum(scores) / len(scores), 1) if scores else 0,
        'score_min': min(scores) if scores else 0,
        'score_max': max(scores) if scores else 0,
        'ai_average': round(sum(ai_scores) / len(ai_scores), 1) if ai_scores else 0,
        'local_average': round(sum(local_scores) / len(local_scores), 1) if local_scores else 0,
        'grade_distribution': grade_dist,
        'results': results
    }
    
    os.makedirs('./results', exist_ok=True)
    with open(f'./results/stress_test_1000_{timestamp}.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    # Print summary
    print("\n" + "=" * 70)
    print("📊 1000-SITE STRESS TEST RESULTS")
    print("=" * 70)
    print(f"   Total URLs: {len(urls)}")
    print(f"   Valid Results: {len(valid_results)}")
    print(f"   Failed/Blocked: {len(urls) - len(valid_results)}")
    print(f"   Total Time: {total_time:.1f}s")
    print(f"   Rate: {len(urls) / total_time:.1f} sites/second")
    print()
    print(f"   Score Average: {output['score_average']}/200")
    print(f"   Score Range: {output['score_min']} - {output['score_max']}")
    print(f"   AI Average: {output['ai_average']}/100")
    print(f"   Local Average: {output['local_average']}/100")
    print()
    print("   Grade Distribution:")
    for grade in ['A', 'B+', 'B', 'C+', 'C', 'D', 'F']:
        count = grade_dist.get(grade, 0)
        pct = count / len(valid_results) * 100 if valid_results else 0
        bar = '█' * int(pct / 2)
        print(f"      {grade}: {bar} {count} ({pct:.1f}%)")
    
    print(f"\n   Results saved to: ./results/stress_test_1000_{timestamp}.json")


if __name__ == "__main__":
    main()
