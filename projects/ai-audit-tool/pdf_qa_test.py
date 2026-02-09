#!/usr/bin/env python3
"""
Comprehensive PDF QA Testing for Directory Audit Tool
Tests PDF generation across many different scenarios
"""

import os
import sys
import json
import time
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any
from PyPDF2 import PdfReader
from io import BytesIO

# Import our modules
from directory_analyzer import DirectorySEOAnalyzer, DirectoryAuditResult, CategoryScore
from directory_pdf_generator import generate_directory_pdf

# Test output directory
OUTPUT_DIR = "/home/ec2-user/clawd/projects/ai-audit-tool/qa_pdfs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@dataclass
class PDFTestResult:
    """Results from testing a single PDF"""
    name: str
    url: str
    success: bool = True
    page_count: int = 0
    file_size: int = 0
    total_score: int = 0
    grade: str = "?"
    issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    pdf_path: str = ""
    text_extracted: bool = True
    extraction_error: str = ""


def create_synthetic_audit(
    url: str,
    name: str,
    total_score: int,
    structure_score: int = None,
    onpage_score: int = None,
    content_score: int = None,
    technical_score: int = None,
    authority_score: int = None,
    ai_score: int = None,
    num_findings: int = 5,
    num_recommendations: int = 3,
    long_findings: bool = False,
    empty_sections: bool = False,
    special_chars: bool = False
) -> DirectoryAuditResult:
    """Create synthetic audit data for testing edge cases"""
    
    # Default score distribution
    if structure_score is None:
        structure_score = min(50, max(0, int(total_score * 0.17)))
    if onpage_score is None:
        onpage_score = min(50, max(0, int(total_score * 0.17)))
    if content_score is None:
        content_score = min(40, max(0, int(total_score * 0.13)))
    if technical_score is None:
        technical_score = min(30, max(0, int(total_score * 0.10)))
    if authority_score is None:
        authority_score = min(30, max(0, int(total_score * 0.10)))
    if ai_score is None:
        ai_score = min(100, max(0, total_score - (structure_score + onpage_score + content_score + technical_score + authority_score)))
    
    # Calculate grade
    pct = total_score / 300 * 100
    if pct >= 90: grade = "A+"
    elif pct >= 80: grade = "A"
    elif pct >= 70: grade = "B"
    elif pct >= 60: grade = "C"
    elif pct >= 50: grade = "D"
    else: grade = "F"
    
    # Generate findings based on score level
    def make_finding(i, section, is_long=False):
        base = f"Finding #{i} for {section}: "
        if is_long:
            return base + "This is an extremely long finding that spans multiple lines and contains detailed technical information about the issue discovered during the audit process. It may include specific metrics, URLs, and recommendations that should wrap properly within the PDF column constraints. " * 3
        if special_chars:
            return base + "Testing special chars: <tag> & 'quotes' \"double\" ®™© £€¥ — émojis: ✅❌⚠️"
        return base + f"Standard finding with some details about the issue detected."
    
    def make_recommendation(i, is_long=False):
        base = f"Recommendation #{i}: "
        if is_long:
            return base + "Implement comprehensive schema markup across all listing pages including LocalBusiness, AggregateRating, ItemList, and FAQPage schema types to maximize rich snippet eligibility and improve click-through rates from search results. This should be prioritized as a high-impact technical SEO improvement. " * 2
        return base + "Standard recommendation text here."
    
    # Create category scores
    def make_categories(section_name: str, count: int, max_per_cat: int, total: int) -> List[CategoryScore]:
        if empty_sections:
            return []
        cats = []
        for i in range(count):
            score = min(max_per_cat, max(0, total // count))
            cats.append(CategoryScore(
                name=f"{section_name} Category {i+1}",
                score=score,
                max_score=max_per_cat,
                findings=[make_finding(j, section_name, long_findings) for j in range(num_findings)],
                recommendations=[make_recommendation(j, long_findings) for j in range(num_recommendations)]
            ))
        return cats
    
    result = DirectoryAuditResult(
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
    
    return result


def inspect_pdf(pdf_bytes: bytes, name: str) -> Dict[str, Any]:
    """Inspect PDF programmatically for issues"""
    issues = []
    warnings = []
    
    try:
        reader = PdfReader(BytesIO(pdf_bytes))
        page_count = len(reader.pages)
        
        # Check page count is reasonable
        if page_count < 3:
            warnings.append(f"Low page count ({page_count}) - may be missing sections")
        elif page_count > 20:
            warnings.append(f"High page count ({page_count}) - consider condensing")
        
        # Try to extract text from each page
        total_text = ""
        for i, page in enumerate(reader.pages):
            try:
                text = page.extract_text()
                total_text += text + "\n"
                
                # Check for obvious issues
                if len(text) < 50 and i > 0:  # Skip cover page
                    warnings.append(f"Page {i+1} has very little text ({len(text)} chars)")
                    
            except Exception as e:
                issues.append(f"Failed to extract text from page {i+1}: {e}")
        
        # Check for common text issues
        if "None" in total_text and total_text.count("None") > 5:
            warnings.append(f"Found multiple 'None' values in text - possible missing data")
        
        if "☐" in total_text or "✓" in total_text or "✅" in total_text:
            warnings.append("Found unsanitized emoji/special chars - may render incorrectly")
        
        # Check PDF metadata
        metadata = reader.metadata
        
        return {
            "page_count": page_count,
            "issues": issues,
            "warnings": warnings,
            "text_length": len(total_text),
            "has_metadata": metadata is not None,
            "extraction_success": True
        }
        
    except Exception as e:
        return {
            "page_count": 0,
            "issues": [f"Failed to read PDF: {e}"],
            "warnings": [],
            "text_length": 0,
            "extraction_success": False,
            "extraction_error": str(e)
        }


def run_live_audit(url: str, name: str) -> tuple:
    """Run actual audit on a live site"""
    print(f"  Auditing {url}...")
    try:
        analyzer = DirectorySEOAnalyzer(url)
        result = analyzer.run_full_audit()
        return result, None
    except Exception as e:
        return None, str(e)


def test_pdf_generation(result: DirectoryAuditResult, test_name: str) -> PDFTestResult:
    """Generate PDF and test it"""
    test_result = PDFTestResult(
        name=test_name,
        url=result.url,
        total_score=result.total_score,
        grade=result.grade
    )
    
    try:
        # Generate PDF
        pdf_path = os.path.join(OUTPUT_DIR, f"{test_name.replace(' ', '_')}.pdf")
        pdf_bytes = generate_directory_pdf(result, pdf_path)
        
        test_result.pdf_path = pdf_path
        test_result.file_size = len(pdf_bytes)
        
        # Inspect PDF
        inspection = inspect_pdf(pdf_bytes, test_name)
        test_result.page_count = inspection["page_count"]
        test_result.issues.extend(inspection["issues"])
        test_result.warnings.extend(inspection["warnings"])
        test_result.text_extracted = inspection["extraction_success"]
        
        if inspection["issues"]:
            test_result.success = False
            
    except Exception as e:
        test_result.success = False
        test_result.issues.append(f"PDF generation failed: {e}")
    
    return test_result


def main():
    print("=" * 70)
    print("PDF QA Testing for Directory Audit Tool")
    print("=" * 70)
    print()
    
    all_results: List[PDFTestResult] = []
    
    # ===== SYNTHETIC TESTS =====
    print("PHASE 1: Synthetic Tests (Edge Cases)")
    print("-" * 50)
    
    synthetic_tests = [
        # Score ranges
        ("high_score_250", "High Score Test Directory", 250, {}),
        ("medium_score_150", "Medium Score Test", 150, {}),
        ("low_score_50", "Low Score Test", 50, {}),
        ("very_low_score_20", "Very Low Score", 20, {}),
        ("perfect_score_300", "Perfect Score Directory", 300, {}),
        
        # Edge cases
        ("long_name", "This Is A Very Long Directory Name That Should Test Text Wrapping In The PDF Title And Headers Properly", 120, {}),
        ("special_chars_name", "Test & Company™ - Best 'Directory' <2024>", 100, {"special_chars": True}),
        ("many_findings", "Many Findings Test", 80, {"num_findings": 15, "num_recommendations": 10}),
        ("long_findings", "Long Text Test", 90, {"long_findings": True}),
        ("empty_sections", "Empty Sections Test", 70, {"empty_sections": True}),
        ("minimal_data", "Minimal Data", 30, {"num_findings": 1, "num_recommendations": 1}),
    ]
    
    for test_id, name, score, kwargs in synthetic_tests:
        print(f"  Testing: {test_id}...")
        result = create_synthetic_audit(f"https://{test_id.replace('_', '-')}.example.com", name, score, **kwargs)
        test_result = test_pdf_generation(result, test_id)
        all_results.append(test_result)
        
        status = "✓" if test_result.success else "✗"
        print(f"    {status} Pages: {test_result.page_count}, Size: {test_result.file_size/1024:.1f}KB")
        if test_result.issues:
            for issue in test_result.issues:
                print(f"      ISSUE: {issue}")
        if test_result.warnings:
            for warn in test_result.warnings[:3]:
                print(f"      WARN: {warn}")
    
    print()
    
    # ===== LIVE SITE TESTS =====
    print("PHASE 2: Live Site Tests")
    print("-" * 50)
    
    live_sites = [
        ("yelp.com", "Yelp"),
        ("yellowpages.com", "Yellow Pages"),
        ("bbb.org", "BBB"),
        ("manta.com", "Manta"),
        ("thumbtack.com", "Thumbtack"),
        ("houzz.com", "Houzz"),
        ("trustpilot.com", "Trustpilot"),
        ("g2.com", "G2"),
    ]
    
    for url, name in live_sites:
        result, error = run_live_audit(url, name)
        if error:
            print(f"  ✗ {name}: Audit failed - {error[:50]}...")
            all_results.append(PDFTestResult(
                name=f"live_{url.replace('.', '_')}",
                url=url,
                success=False,
                issues=[f"Audit failed: {error}"]
            ))
            continue
        
        test_result = test_pdf_generation(result, f"live_{url.replace('.', '_')}")
        all_results.append(test_result)
        
        status = "✓" if test_result.success else "✗"
        print(f"  {status} {name}: Score {result.total_score}/300 ({result.grade}), Pages: {test_result.page_count}, Size: {test_result.file_size/1024:.1f}KB")
        if test_result.issues:
            for issue in test_result.issues:
                print(f"      ISSUE: {issue}")
    
    print()
    
    # ===== SUMMARY =====
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for r in all_results if r.success)
    failed = len(all_results) - passed
    
    print(f"Total Tests: {len(all_results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print()
    
    if failed > 0:
        print("FAILED TESTS:")
        for r in all_results:
            if not r.success:
                print(f"  - {r.name}: {'; '.join(r.issues[:2])}")
    
    print()
    print("ALL WARNINGS:")
    all_warnings = []
    for r in all_results:
        for w in r.warnings:
            all_warnings.append(f"{r.name}: {w}")
    
    if all_warnings:
        for w in sorted(set(all_warnings))[:20]:
            print(f"  - {w}")
    else:
        print("  None!")
    
    print()
    print(f"PDFs saved to: {OUTPUT_DIR}")
    print("Review PDFs visually for layout issues not caught programmatically.")
    
    # Save results JSON
    results_path = os.path.join(OUTPUT_DIR, "qa_results.json")
    results_data = []
    for r in all_results:
        results_data.append({
            "name": r.name,
            "url": r.url,
            "success": r.success,
            "page_count": r.page_count,
            "file_size": r.file_size,
            "total_score": r.total_score,
            "grade": r.grade,
            "issues": r.issues,
            "warnings": r.warnings,
            "pdf_path": r.pdf_path
        })
    
    with open(results_path, 'w') as f:
        json.dump(results_data, f, indent=2)
    print(f"Results saved to: {results_path}")
    
    return all_results


if __name__ == "__main__":
    main()
