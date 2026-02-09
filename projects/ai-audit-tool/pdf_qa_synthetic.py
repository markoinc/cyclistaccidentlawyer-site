#!/usr/bin/env python3
"""
PDF QA - Synthetic Tests Only (No network)
"""

import os
import sys
from dataclasses import dataclass, field
from typing import List
from PyPDF2 import PdfReader
from io import BytesIO

from directory_analyzer import DirectoryAuditResult, CategoryScore
from directory_pdf_generator import generate_directory_pdf

OUTPUT_DIR = "/home/ec2-user/clawd/projects/ai-audit-tool/qa_pdfs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_synthetic_audit(
    url: str,
    name: str,
    total_score: int,
    num_findings: int = 5,
    num_recommendations: int = 3,
    long_findings: bool = False,
    empty_sections: bool = False,
    special_chars: bool = False
) -> DirectoryAuditResult:
    """Create synthetic audit data for testing"""
    
    # Score distribution
    structure_score = min(50, max(0, int(total_score * 0.17)))
    onpage_score = min(50, max(0, int(total_score * 0.17)))
    content_score = min(40, max(0, int(total_score * 0.13)))
    technical_score = min(30, max(0, int(total_score * 0.10)))
    authority_score = min(30, max(0, int(total_score * 0.10)))
    ai_score = min(100, max(0, total_score - (structure_score + onpage_score + content_score + technical_score + authority_score)))
    
    # Grade
    pct = total_score / 300 * 100
    if pct >= 90: grade = "A+"
    elif pct >= 80: grade = "A"
    elif pct >= 70: grade = "B"
    elif pct >= 60: grade = "C"
    elif pct >= 50: grade = "D"
    else: grade = "F"
    
    def make_finding(i, section, is_long=False):
        base = f"Finding #{i} for {section}: "
        if is_long:
            return base + "This is an extremely long finding that spans multiple lines and contains detailed technical information about the issue discovered during the audit process. It may include specific metrics, URLs, and recommendations that should wrap properly within the PDF column constraints. This text is intentionally verbose to test text wrapping capabilities. " * 2
        if special_chars:
            return base + "Testing special chars: <tag> & 'quotes' \"double\" -- em-dash"
        return base + f"Standard finding with details about the detected issue."
    
    def make_recommendation(i, is_long=False):
        base = f"Recommendation #{i}: "
        if is_long:
            return base + "Implement comprehensive schema markup across all listing pages including LocalBusiness, AggregateRating, ItemList, and FAQPage schema types to maximize rich snippet eligibility. " * 2
        return base + "Standard recommendation text here."
    
    def make_categories(section_name: str, count: int, max_per_cat: int, total: int) -> List[CategoryScore]:
        if empty_sections:
            return []
        cats = []
        scores = [total // count] * count
        for i in range(count):
            cats.append(CategoryScore(
                name=f"{section_name} Category {i+1}",
                score=min(max_per_cat, scores[i]),
                max_score=max_per_cat,
                findings=[make_finding(j, section_name, is_long=long_findings) for j in range(1, num_findings+1)],
                recommendations=[make_recommendation(j, is_long=long_findings) for j in range(1, num_recommendations+1)]
            ))
        return cats
    
    return DirectoryAuditResult(
        url=url,
        directory_name=name,
        directory_type="business",
        structure_score=structure_score,
        onpage_score=onpage_score,
        content_score=content_score,
        technical_score=technical_score,
        authority_score=authority_score,
        ai_visibility_score=ai_score,
        directory_health_score=structure_score + onpage_score + content_score + technical_score + authority_score,
        total_score=total_score,
        grade=grade,
        structure_categories=make_categories("Structure", 5, 10, structure_score),
        onpage_categories=make_categories("On-Page", 5, 10, onpage_score),
        content_categories=make_categories("Content", 4, 10, content_score),
        technical_categories=make_categories("Technical", 3, 10, technical_score),
        authority_categories=make_categories("Authority", 3, 10, authority_score),
        ai_categories=make_categories("AI Visibility", 10, 10, ai_score) if not empty_sections else [],
        quick_wins=[f"Quick Win #{i}: Implement this quick improvement for immediate results." for i in range(1, 6)],
        priority_fixes=[f"Priority Fix #{i}: Critical issue requiring immediate attention." for i in range(1, 6)],
        technical_data={
            "listing_pages": 150,
            "category_pages": 25,
            "location_pages": 10,
            "sitemap_urls": 500,
            "schemas_found": 12
        }
    )

def inspect_pdf(pdf_bytes: bytes) -> dict:
    """Inspect PDF for issues"""
    issues = []
    warnings = []
    
    try:
        reader = PdfReader(BytesIO(pdf_bytes))
        page_count = len(reader.pages)
        
        if page_count < 3:
            warnings.append(f"Low page count ({page_count})")
        elif page_count > 20:
            warnings.append(f"High page count ({page_count})")
        
        total_text = ""
        for i, page in enumerate(reader.pages):
            try:
                text = page.extract_text() or ""
                total_text += text + "\n"
                if len(text) < 50 and i > 0:
                    warnings.append(f"Page {i+1} has little text")
            except Exception as e:
                issues.append(f"Text extraction failed page {i+1}: {e}")
        
        if total_text.count("None") > 5:
            warnings.append("Multiple 'None' values found")
        
        return {"page_count": page_count, "issues": issues, "warnings": warnings, "text_length": len(total_text)}
    except Exception as e:
        return {"page_count": 0, "issues": [f"PDF read failed: {e}"], "warnings": [], "text_length": 0}

def main():
    print("=" * 60)
    print("PDF QA - Synthetic Tests")
    print("=" * 60)
    
    tests = [
        ("high_score_250", "High Score Directory", 250, {}),
        ("medium_score_150", "Medium Score Test", 150, {}),
        ("low_score_50", "Low Score Test", 50, {}),
        ("very_low_20", "Very Low Score", 20, {}),
        ("perfect_300", "Perfect Score", 300, {}),
        ("long_name", "This Is A Very Long Directory Name That Should Test Text Wrapping In PDF Title And Headers Properly And See If It Breaks", 120, {}),
        ("special_chars", "Test & Company - Best 'Directory' (2024)", 100, {"special_chars": True}),
        ("many_findings", "Many Findings Test", 80, {"num_findings": 12, "num_recommendations": 8}),
        ("long_findings", "Long Text Test", 90, {"long_findings": True}),
        ("empty_sections", "Empty Sections", 70, {"empty_sections": True}),
        ("minimal_data", "Minimal", 30, {"num_findings": 1, "num_recommendations": 1}),
    ]
    
    all_issues = []
    all_warnings = []
    
    for test_id, name, score, kwargs in tests:
        print(f"\nTesting: {test_id}...")
        
        result = create_synthetic_audit(f"https://{test_id}.example.com", name, score, **kwargs)
        pdf_path = os.path.join(OUTPUT_DIR, f"{test_id}.pdf")
        
        try:
            pdf_bytes = generate_directory_pdf(result, pdf_path)
            inspection = inspect_pdf(pdf_bytes)
            
            status = "OK" if not inspection["issues"] else "FAIL"
            print(f"  {status} | Score: {score}/300 ({result.grade}) | Pages: {inspection['page_count']} | Size: {len(pdf_bytes)/1024:.1f}KB")
            
            if inspection["issues"]:
                for i in inspection["issues"]:
                    print(f"    ISSUE: {i}")
                    all_issues.append(f"{test_id}: {i}")
            if inspection["warnings"]:
                for w in inspection["warnings"]:
                    print(f"    WARN: {w}")
                    all_warnings.append(f"{test_id}: {w}")
                    
        except Exception as e:
            print(f"  FAIL | Error: {e}")
            all_issues.append(f"{test_id}: {e}")
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Tests: {len(tests)}")
    print(f"Issues: {len(all_issues)}")
    print(f"Warnings: {len(all_warnings)}")
    
    if all_issues:
        print("\nAll Issues:")
        for i in all_issues:
            print(f"  - {i}")
    
    if all_warnings:
        print("\nAll Warnings:")
        for w in all_warnings:
            print(f"  - {w}")
    
    print(f"\nPDFs saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
