#!/usr/bin/env python3
"""
Final PDF QA Testing - Comprehensive validation
"""

import os
from dataclasses import dataclass, field
from typing import List
from PyPDF2 import PdfReader
from io import BytesIO

from directory_analyzer import DirectoryAuditResult, CategoryScore
from directory_pdf_generator import generate_directory_pdf

OUTPUT_DIR = "/home/ec2-user/clawd/projects/ai-audit-tool/qa_pdfs"

def inspect_pdf_thoroughly(pdf_bytes: bytes, name: str) -> List[str]:
    """Comprehensive PDF inspection"""
    issues = []
    
    try:
        reader = PdfReader(BytesIO(pdf_bytes))
        
        # Check page count
        if len(reader.pages) < 3:
            issues.append(f"Low page count: {len(reader.pages)}")
        elif len(reader.pages) > 30:
            issues.append(f"Very high page count: {len(reader.pages)}")
        
        full_text = ""
        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            full_text += text
            
            # Check for problematic characters
            for char in text:
                code = ord(char)
                if code == 127:  # DEL
                    issues.append(f"Page {i+1}: DEL character (0x7f)")
                elif 128 <= code < 160:  # Control chars
                    issues.append(f"Page {i+1}: Control char ({hex(code)})")
            
            # Check for None values
            if "None" in text and text.count("None") > 3:
                issues.append(f"Page {i+1}: Multiple 'None' values")
        
        # Check for bullet characters that should have been sanitized
        if "•" in full_text:
            issues.append("Unsanitized bullet character (•)")
        if "✅" in full_text:
            issues.append("Unsanitized emoji (✅)")
        if "❌" in full_text:
            issues.append("Unsanitized emoji (❌)")
            
    except Exception as e:
        issues.append(f"PDF read error: {e}")
    
    return issues


def create_test_result(
    name: str,
    total_score: int,
    findings: List[str] = None,
    recommendations: List[str] = None,
    empty_ai: bool = False
) -> DirectoryAuditResult:
    """Create a test DirectoryAuditResult"""
    
    default_findings = findings or [
        "✅ This is a good finding",
        "❌ This is a bad finding",
        "⚠️ This is a warning",
        "Normal finding text",
    ]
    
    default_recs = recommendations or [
        "Implement this improvement",
        "Fix this issue immediately",
    ]
    
    # Score distribution
    structure = min(50, max(0, int(total_score * 0.17)))
    onpage = min(50, max(0, int(total_score * 0.17)))
    content = min(40, max(0, int(total_score * 0.13)))
    technical = min(30, max(0, int(total_score * 0.10)))
    authority = min(30, max(0, int(total_score * 0.10)))
    ai = min(100, max(0, total_score - (structure + onpage + content + technical + authority)))
    
    # Grade
    pct = total_score / 300 * 100
    if pct >= 90: grade = "A+"
    elif pct >= 80: grade = "A"
    elif pct >= 70: grade = "B"
    elif pct >= 60: grade = "C"
    elif pct >= 50: grade = "D"
    else: grade = "F"
    
    def make_cats(section, count, max_per, total):
        return [
            CategoryScore(
                name=f"{section} Cat {i+1}",
                score=min(max_per, total // count),
                max_score=max_per,
                findings=default_findings[:3],
                recommendations=default_recs[:2]
            )
            for i in range(count)
        ]
    
    return DirectoryAuditResult(
        url=f"https://{name.lower().replace(' ', '-')}.example.com",
        directory_name=name,
        total_score=total_score,
        grade=grade,
        structure_score=structure,
        onpage_score=onpage,
        content_score=content,
        technical_score=technical,
        authority_score=authority,
        ai_visibility_score=ai,
        directory_health_score=structure + onpage + content + technical + authority,
        structure_categories=make_cats("Structure", 5, 10, structure),
        onpage_categories=make_cats("On-Page", 5, 10, onpage),
        content_categories=make_cats("Content", 4, 10, content),
        technical_categories=make_cats("Technical", 3, 10, technical),
        authority_categories=make_cats("Authority", 3, 10, authority),
        ai_categories=[] if empty_ai else make_cats("AI", 10, 10, ai),
        quick_wins=[
            "• Quick win #1 with bullet",
            "Quick win #2 normal",
            "✅ Quick win with emoji",
        ],
        priority_fixes=[
            "❌ Critical fix #1",
            "Fix #2 with → arrow",
            "Fix #3 normal",
        ],
        technical_data={
            'listing_pages': 100,
            'category_pages': 20,
            'location_pages': 5,
            'sitemap_urls': 300,
            'schemas_found': 8
        }
    )


def main():
    print("=" * 60)
    print("Final PDF QA Testing")
    print("=" * 60)
    
    tests = [
        # Score ranges
        ("score_300", "Perfect Score Directory", 300, {}),
        ("score_250", "High Score Directory", 250, {}),
        ("score_150", "Medium Score Test", 150, {}),
        ("score_80", "Low-Medium Score", 80, {}),
        ("score_30", "Very Low Score", 30, {}),
        ("score_0", "Zero Score", 0, {}),
        
        # Edge cases
        ("long_name", "This Is An Extremely Long Directory Name That Should Test Text Wrapping In Headers", 100, {}),
        ("special_chars", "Test & Co 'Directory' (2024)", 100, {}),
        ("empty_ai", "No AI Section Test", 100, {"empty_ai": True}),
        
        # Content variations
        ("many_emojis", "Emoji Heavy Test", 100, {
            "findings": ["✅ OK", "❌ Bad", "⚠️ Warn", "🔍 Search", "💡 Tip"] * 2,
            "recommendations": ["🚀 Do this", "📈 Improve that"] * 2
        }),
        ("long_text", "Long Content Test", 100, {
            "findings": [
                "This is an extremely long finding that spans multiple lines and contains detailed technical information about the issue discovered during the audit. It should wrap properly within the PDF constraints. " * 3,
            ] * 4,
            "recommendations": [
                "Implement this comprehensive improvement across all pages including detailed schema markup, optimized meta tags, and enhanced internal linking structure for maximum SEO impact. " * 2,
            ] * 3
        }),
    ]
    
    results = []
    
    for test_id, name, score, kwargs in tests:
        print(f"\nTesting: {test_id}...")
        
        result = create_test_result(name, score, **kwargs)
        pdf_path = os.path.join(OUTPUT_DIR, f"final_{test_id}.pdf")
        
        try:
            pdf_bytes = generate_directory_pdf(result, pdf_path)
            issues = inspect_pdf_thoroughly(pdf_bytes, test_id)
            
            reader = PdfReader(BytesIO(pdf_bytes))
            page_count = len(reader.pages)
            size_kb = len(pdf_bytes) / 1024
            
            status = "PASS" if not issues else "FAIL"
            print(f"  {status} | Score: {score}/300 | Pages: {page_count} | Size: {size_kb:.1f}KB")
            
            if issues:
                for issue in issues[:5]:
                    print(f"    ISSUE: {issue}")
            
            results.append({
                "test": test_id,
                "status": status,
                "issues": issues,
                "pages": page_count,
                "size": size_kb
            })
            
        except Exception as e:
            print(f"  ERROR: {e}")
            results.append({"test": test_id, "status": "ERROR", "error": str(e)})
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for r in results if r.get("status") == "PASS")
    failed = sum(1 for r in results if r.get("status") == "FAIL")
    errors = sum(1 for r in results if r.get("status") == "ERROR")
    
    print(f"Total Tests: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Errors: {errors}")
    
    if failed > 0 or errors > 0:
        print("\nFailed/Error Tests:")
        for r in results:
            if r.get("status") in ["FAIL", "ERROR"]:
                if r.get("error"):
                    print(f"  - {r['test']}: {r['error']}")
                else:
                    print(f"  - {r['test']}: {r.get('issues', [])[:2]}")
    
    print(f"\nPDFs saved to: {OUTPUT_DIR}")
    return results


if __name__ == "__main__":
    main()
