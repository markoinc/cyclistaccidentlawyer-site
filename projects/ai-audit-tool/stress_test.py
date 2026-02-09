#!/usr/bin/env python3
"""
Comprehensive stress test for the Directory Analyzer
Tests against diverse directory sites to find bugs and edge cases
"""

import sys
import time
import traceback
from datetime import datetime

# Test URLs organized by category
TEST_DIRECTORIES = {
    # Business Directories
    "business": [
        "https://www.yelp.com",
        "https://www.yellowpages.com",
        "https://clutch.co",
        "https://www.g2.com",
        "https://www.bbb.org",
        "https://www.manta.com",
    ],
    # Product/Software Directories
    "product": [
        "https://www.producthunt.com",
        "https://www.capterra.com",
        "https://alternativeto.net",
        "https://www.getapp.com",
        "https://sourceforge.net",
    ],
    # Local/Review Directories
    "local": [
        "https://www.tripadvisor.com",
        "https://www.healthgrades.com",
        "https://www.lawyers.com",
        "https://www.zocdoc.com",
        "https://www.homeadvisor.com",
    ],
    # Niche Directories
    "niche": [
        "https://www.goodfirms.co",
        "https://www.crunchbase.com",
        "https://www.glassdoor.com",
        "https://angel.co",
        "https://www.thomasnet.com",
    ],
    # Small/Indie Directories
    "indie": [
        "https://www.designrush.com",
        "https://topdesignfirms.com",
        "https://www.sortlist.com",
        "https://www.agencyspotter.com",
    ],
    # Edge cases - potentially broken/unusual
    "edge": [
        "https://example.com",  # Not a real directory
        "https://httpstat.us/404",  # 404 page
        "https://httpstat.us/500",  # 500 error
        "https://httpstat.us/timeout/5000",  # Slow response
    ],
}

def test_single_url(url: str, timeout: int = 120) -> dict:
    """Test a single URL and return results"""
    result = {
        "url": url,
        "status": "unknown",
        "error": None,
        "error_type": None,
        "traceback": None,
        "duration_seconds": 0,
        "score": None,
        "grade": None,
        "warnings": [],
    }
    
    start_time = time.time()
    
    try:
        from directory_analyzer import DirectorySEOAnalyzer
        
        analyzer = DirectorySEOAnalyzer(url)
        audit_result = analyzer.run_full_audit()
        
        result["status"] = "success"
        result["score"] = audit_result.total_score
        result["grade"] = audit_result.grade
        result["directory_score"] = audit_result.directory_health_score
        result["ai_score"] = audit_result.ai_visibility_score
        result["pages_found"] = {
            "listings": len(analyzer.listing_pages),
            "categories": len(analyzer.category_pages),
            "locations": len(analyzer.location_pages),
        }
        
        # Capture any oddities
        if audit_result.total_score == 0:
            result["warnings"].append("Zero score - likely failed to analyze")
        if audit_result.total_score > 280:
            result["warnings"].append("Suspiciously high score - verify accuracy")
        if len(analyzer.listing_pages) == 0 and len(analyzer.category_pages) == 0:
            result["warnings"].append("No listing or category pages found")
            
    except KeyboardInterrupt:
        result["status"] = "interrupted"
        result["error"] = "User interrupt"
        
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        result["error_type"] = type(e).__name__
        result["traceback"] = traceback.format_exc()
        
    finally:
        result["duration_seconds"] = round(time.time() - start_time, 2)
        
    return result

def run_stress_test(categories=None, max_per_category=None):
    """Run stress test on all or selected categories"""
    all_results = []
    
    # Filter categories if specified
    test_urls = TEST_DIRECTORIES
    if categories:
        test_urls = {k: v for k, v in TEST_DIRECTORIES.items() if k in categories}
        
    total_urls = sum(len(urls) for urls in test_urls.values())
    current = 0
    
    print(f"\n{'='*60}")
    print(f"DIRECTORY ANALYZER STRESS TEST")
    print(f"Testing {total_urls} URLs across {len(test_urls)} categories")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    for category, urls in test_urls.items():
        print(f"\n📂 Category: {category.upper()}")
        print("-" * 40)
        
        urls_to_test = urls[:max_per_category] if max_per_category else urls
        
        for url in urls_to_test:
            current += 1
            print(f"\n[{current}/{total_urls}] Testing: {url}")
            
            result = test_single_url(url)
            result["category"] = category
            all_results.append(result)
            
            # Print immediate result
            if result["status"] == "success":
                print(f"  ✅ Score: {result['score']}/300 ({result['grade']})")
                print(f"  ⏱️  Duration: {result['duration_seconds']}s")
                if result["warnings"]:
                    for w in result["warnings"]:
                        print(f"  ⚠️  {w}")
            else:
                print(f"  ❌ {result['status'].upper()}: {result['error']}")
                print(f"  ⏱️  Duration: {result['duration_seconds']}s")
                if result.get("error_type"):
                    print(f"  📋 Error type: {result['error_type']}")
                    
            # Rate limiting
            time.sleep(1)
            
    return all_results

def generate_report(results: list, output_path: str):
    """Generate markdown report from results"""
    
    # Categorize results
    successes = [r for r in results if r["status"] == "success"]
    errors = [r for r in results if r["status"] == "error"]
    warnings = [r for r in results if r.get("warnings")]
    
    report = f"""# Directory Analyzer Stress Test Results

**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Total Tests:** {len(results)}  
**Successes:** {len(successes)}  
**Errors:** {len(errors)}  

## Summary

| Metric | Value |
|--------|-------|
| Success Rate | {len(successes)/len(results)*100:.1f}% |
| Error Rate | {len(errors)/len(results)*100:.1f}% |
| Avg Duration | {sum(r['duration_seconds'] for r in results)/len(results):.1f}s |
| Tests with Warnings | {len(warnings)} |

## Errors Found

"""
    
    if errors:
        for e in errors:
            report += f"""### ❌ {e['url']}
- **Category:** {e.get('category', 'N/A')}
- **Error Type:** {e.get('error_type', 'Unknown')}
- **Error Message:** {e.get('error', 'No message')}
- **Duration:** {e['duration_seconds']}s

<details>
<summary>Full Traceback</summary>

```
{e.get('traceback', 'No traceback available')}
```
</details>

"""
    else:
        report += "No errors encountered! ✅\n\n"
        
    report += """## Warnings Found

"""
    
    if warnings:
        for w in warnings:
            if w.get("warnings"):
                report += f"""### ⚠️ {w['url']}
- **Score:** {w.get('score', 'N/A')}/300 ({w.get('grade', 'N/A')})
- **Warnings:**
"""
                for warning in w["warnings"]:
                    report += f"  - {warning}\n"
                report += "\n"
    else:
        report += "No warnings! ✅\n\n"
        
    report += """## Successful Tests

| URL | Category | Score | Grade | Duration |
|-----|----------|-------|-------|----------|
"""
    
    for s in successes:
        report += f"| {s['url'][:40]}... | {s.get('category', 'N/A')} | {s.get('score', 'N/A')}/300 | {s.get('grade', 'N/A')} | {s['duration_seconds']}s |\n"
        
    report += """

## Test Categories Tested

"""
    
    for category in TEST_DIRECTORIES.keys():
        cat_results = [r for r in results if r.get("category") == category]
        cat_successes = [r for r in cat_results if r["status"] == "success"]
        report += f"- **{category}:** {len(cat_successes)}/{len(cat_results)} passed\n"
        
    report += """

## Recommendations for Code Fixes

Based on the test results, here are the issues to address:

"""
    
    # Categorize unique errors
    error_types = {}
    for e in errors:
        etype = e.get("error_type", "Unknown")
        if etype not in error_types:
            error_types[etype] = []
        error_types[etype].append(e)
        
    for etype, errs in error_types.items():
        report += f"""### {etype}
- **Occurrences:** {len(errs)}
- **Affected URLs:** {', '.join(e['url'][:30] + '...' for e in errs[:3])}
- **Sample Error:** {errs[0].get('error', 'No message')[:200]}

"""
    
    # Write report
    with open(output_path, 'w') as f:
        f.write(report)
        
    print(f"\n📄 Report saved to: {output_path}")
    return report

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--categories", nargs="*", help="Specific categories to test")
    parser.add_argument("--max", type=int, help="Max URLs per category")
    parser.add_argument("--output", default="/home/ec2-user/clawd/data/directory-audit-test-results.md")
    args = parser.parse_args()
    
    results = run_stress_test(
        categories=args.categories,
        max_per_category=args.max
    )
    
    generate_report(results, args.output)
