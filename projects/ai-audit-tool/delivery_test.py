#!/usr/bin/env python3
"""
Test the full delivery pipeline:
1. Analyze website
2. Generate PDF
3. (Optional) Send email

Tests PDF generation at scale
"""

import os
import sys
import json
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(__file__))

from enhanced_analyzer import EnhancedWebsiteAnalyzer
from pdf_generator import generate_pdf


def test_single_delivery(url: str, output_dir: str = './test_pdfs') -> dict:
    """Test full delivery for a single URL"""
    start = time.time()
    result = {
        'url': url,
        'success': False,
        'analysis_time': 0,
        'pdf_time': 0,
        'total_time': 0,
        'pdf_size_kb': 0,
        'grade': None,
        'score': None,
        'error': None
    }
    
    try:
        # Step 1: Analyze
        analysis_start = time.time()
        analyzer = EnhancedWebsiteAnalyzer(url)
        audit_result = analyzer.run_full_audit()
        result['analysis_time'] = round(time.time() - analysis_start, 2)
        result['grade'] = audit_result.grade
        result['score'] = audit_result.total_score
        
        # Skip PDF if analysis failed (score = 0)
        if audit_result.total_score == 0:
            result['error'] = "Analysis returned score 0 (site blocked or error)"
            return result
        
        # Step 2: Generate PDF
        pdf_start = time.time()
        
        # Create filename
        safe_name = ''.join(c if c.isalnum() else '_' for c in (audit_result.business_name or url)[:30])
        pdf_path = os.path.join(output_dir, f"audit_{safe_name}_{int(time.time())}.pdf")
        
        pdf_bytes = generate_pdf(audit_result, pdf_path)
        result['pdf_time'] = round(time.time() - pdf_start, 2)
        result['pdf_size_kb'] = round(len(pdf_bytes) / 1024, 1)
        result['pdf_path'] = pdf_path
        
        result['success'] = True
        result['total_time'] = round(time.time() - start, 2)
        
    except Exception as e:
        result['error'] = str(e)
        result['total_time'] = round(time.time() - start, 2)
    
    return result


def run_delivery_test(urls: list, workers: int = 5, output_dir: str = './test_pdfs') -> dict:
    """Run delivery test on multiple URLs"""
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n🚀 DELIVERY PIPELINE TEST")
    print(f"=" * 60)
    print(f"   URLs: {len(urls)}")
    print(f"   Workers: {workers}")
    print(f"   Output: {output_dir}")
    print(f"=" * 60)
    
    results = []
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(test_single_delivery, url, output_dir): url for url in urls}
        
        completed = 0
        for future in as_completed(futures):
            completed += 1
            result = future.result()
            results.append(result)
            
            if result['success']:
                print(f"[{completed}/{len(urls)}] ✅ {result['url'][:40]}... {result['grade']} | Analysis: {result['analysis_time']}s | PDF: {result['pdf_time']}s ({result['pdf_size_kb']}KB)")
            else:
                print(f"[{completed}/{len(urls)}] ❌ {result['url'][:40]}... Error: {str(result['error'])[:40]}")
    
    total_time = time.time() - start_time
    
    # Stats
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    if successful:
        avg_analysis = sum(r['analysis_time'] for r in successful) / len(successful)
        avg_pdf = sum(r['pdf_time'] for r in successful) / len(successful)
        avg_total = sum(r['total_time'] for r in successful) / len(successful)
        avg_size = sum(r['pdf_size_kb'] for r in successful) / len(successful)
        total_pdfs_mb = sum(r['pdf_size_kb'] for r in successful) / 1024
    else:
        avg_analysis = avg_pdf = avg_total = avg_size = total_pdfs_mb = 0
    
    stats = {
        'total_urls': len(urls),
        'successful': len(successful),
        'failed': len(failed),
        'success_rate': round(len(successful) / len(urls) * 100, 1) if urls else 0,
        'total_time_seconds': round(total_time, 1),
        'throughput_per_minute': round(len(urls) / total_time * 60, 1) if total_time > 0 else 0,
        'avg_analysis_time': round(avg_analysis, 2),
        'avg_pdf_time': round(avg_pdf, 2),
        'avg_total_time': round(avg_total, 2),
        'avg_pdf_size_kb': round(avg_size, 1),
        'total_pdfs_mb': round(total_pdfs_mb, 2),
    }
    
    # Grade distribution
    grades = [r['grade'] for r in successful if r['grade']]
    stats['grade_distribution'] = {g: grades.count(g) for g in set(grades)}
    
    # Print summary
    print(f"\n" + "=" * 60)
    print(f"📊 DELIVERY PIPELINE TEST RESULTS")
    print(f"=" * 60)
    print(f"   Total URLs: {stats['total_urls']}")
    print(f"   Successful: {stats['successful']} ({stats['success_rate']}%)")
    print(f"   Failed: {stats['failed']}")
    print(f"\n   Total Time: {stats['total_time_seconds']}s")
    print(f"   Throughput: {stats['throughput_per_minute']} deliveries/minute")
    print(f"\n   Avg Analysis Time: {stats['avg_analysis_time']}s")
    print(f"   Avg PDF Generation: {stats['avg_pdf_time']}s")
    print(f"   Avg Total Time: {stats['avg_total_time']}s")
    print(f"\n   Avg PDF Size: {stats['avg_pdf_size_kb']} KB")
    print(f"   Total PDFs: {stats['total_pdfs_mb']} MB")
    
    if stats['grade_distribution']:
        print(f"\n   Grade Distribution:")
        for grade in ['A', 'B+', 'B', 'C+', 'C', 'D', 'F']:
            count = stats['grade_distribution'].get(grade, 0)
            if count > 0:
                print(f"      {grade}: {'█' * min(count, 20)} ({count})")
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = f'./results/delivery_test_{timestamp}.json'
    with open(results_file, 'w') as f:
        json.dump({'stats': stats, 'results': results}, f, indent=2)
    print(f"\n   Results saved to: {results_file}")
    
    return {'stats': stats, 'results': results}


def main():
    import argparse
    import base64
    import requests
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', type=int, default=50)
    parser.add_argument('--workers', type=int, default=5)
    parser.add_argument('--keyword', type=str, default='personal injury attorney')
    args = parser.parse_args()
    
    # Get URLs from DataForSEO
    print(f"🔍 Fetching URLs for: '{args.keyword}'...")
    
    login = 'mark@kuriosbrand.com'
    password = 'b292b4a5e686bc75'
    auth = base64.b64encode(f"{login}:{password}".encode()).decode()
    
    resp = requests.post(
        "https://api.dataforseo.com/v3/serp/google/organic/live/advanced",
        json=[{"keyword": args.keyword, "location_name": "United States", "depth": args.count}],
        headers={'Authorization': f'Basic {auth}', 'Content-Type': 'application/json'},
        timeout=60
    )
    
    urls = []
    data = resp.json()
    if data.get('status_code') == 20000:
        for task in data.get('tasks', []):
            for result in (task.get('result') or []):
                for item in (result.get('items') or []):
                    if item.get('type') == 'organic' and item.get('url'):
                        url = item['url']
                        if 'youtube.com' not in url:
                            urls.append(url)
    
    urls = urls[:args.count]
    print(f"   Found {len(urls)} URLs")
    
    if not urls:
        print("❌ No URLs found!")
        return
    
    # Run test
    run_delivery_test(urls, workers=args.workers)


if __name__ == "__main__":
    main()
