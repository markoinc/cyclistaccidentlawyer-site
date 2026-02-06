#!/usr/bin/env python3
"""
PDF Report Generator for AI & Local Visibility Audit

Note: ReportLab has limited Unicode/emoji support. 
We use ASCII-safe alternatives for reliability.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, ListFlowable, ListItem
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from io import BytesIO
from datetime import datetime
try:
    from enhanced_analyzer import AuditResult, CategoryScore
except ImportError:
    from analyzer import AuditResult, CategoryScore
import os
import re


def sanitize_for_pdf(text: str) -> str:
    """Replace emojis and special chars with ASCII-safe alternatives for PDF rendering"""
    replacements = {
        '✅': '[OK]',
        '❌': '[X]',
        '⚠️': '[!]',
        'ℹ️': '[i]',
        '💡': '[TIP]',
        '🏆': '[#1]',
        '📊': '',
        '🔍': '',
        '🔴': '',
        '🟡': '',
        '🟢': '',
        '💰': '',
        '✓': '[OK]',
        '☐': '[ ]',
        '🤖': '',
        '📍': '',
        '⚡': '',
        '🚨': '',
        '📋': '',
        '📞': '',
        '📧': '',
    }
    for emoji, replacement in replacements.items():
        text = text.replace(emoji, replacement)
    return text


# Brand colors
PRIMARY = HexColor('#1a1a2e')
SECONDARY = HexColor('#16213e')
ACCENT = HexColor('#0f3460')
HIGHLIGHT = HexColor('#e94560')
SUCCESS = HexColor('#00d26a')
WARNING = HexColor('#ffb100')
DANGER = HexColor('#ff4757')
LIGHT = HexColor('#f8f9fa')
DARK = HexColor('#212529')


def get_score_color(score: int, max_score: int = 10) -> HexColor:
    """Return color based on score percentage"""
    pct = score / max_score
    if pct >= 0.7:
        return SUCCESS
    elif pct >= 0.4:
        return WARNING
    else:
        return DANGER


def create_score_badge(score: int, max_score: int, label: str) -> Drawing:
    """Create a visual score badge"""
    d = Drawing(100, 80)
    
    # Background circle
    color = get_score_color(score, max_score)
    
    # Score text
    score_text = String(50, 45, f"{score}", textAnchor='middle')
    score_text.fontName = 'Helvetica-Bold'
    score_text.fontSize = 24
    score_text.fillColor = color
    d.add(score_text)
    
    # Max score
    max_text = String(50, 25, f"/ {max_score}", textAnchor='middle')
    max_text.fontName = 'Helvetica'
    max_text.fontSize = 12
    max_text.fillColor = DARK
    d.add(max_text)
    
    # Label
    label_text = String(50, 5, label, textAnchor='middle')
    label_text.fontName = 'Helvetica'
    label_text.fontSize = 10
    label_text.fillColor = DARK
    d.add(label_text)
    
    return d


def generate_pdf(result: AuditResult, enhanced_result = None, output_path: str = None) -> bytes:
    """Generate PDF report from audit result
    
    Args:
        result: Basic audit result
        enhanced_result: Optional EnhancedAuditResult with DataForSEO data
        output_path: Optional file path to save PDF
    """
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Title'],
        fontSize=28,
        textColor=PRIMARY,
        spaceAfter=20,
        alignment=TA_CENTER
    ))
    
    styles.add(ParagraphStyle(
        name='CustomSubtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=ACCENT,
        spaceAfter=30,
        alignment=TA_CENTER
    ))
    
    styles.add(ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=PRIMARY,
        spaceBefore=20,
        spaceAfter=10,
        borderPadding=(10, 10, 10, 10),
    ))
    
    styles.add(ParagraphStyle(
        name='CategoryHeader',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=ACCENT,
        spaceBefore=15,
        spaceAfter=5,
    ))
    
    styles.add(ParagraphStyle(
        name='Finding',
        parent=styles['Normal'],
        fontSize=10,
        leftIndent=20,
        spaceBefore=2,
        spaceAfter=2,
    ))
    
    styles.add(ParagraphStyle(
        name='Recommendation',
        parent=styles['Normal'],
        fontSize=10,
        leftIndent=20,
        textColor=ACCENT,
        spaceBefore=2,
        spaceAfter=2,
    ))
    
    styles.add(ParagraphStyle(
        name='QuickWin',
        parent=styles['Normal'],
        fontSize=11,
        leftIndent=15,
        textColor=HexColor('#155724'),
        backColor=HexColor('#d4edda'),
        borderPadding=5,
        spaceBefore=5,
        spaceAfter=5,
    ))
    
    # Build content
    story = []
    
    # === COVER PAGE ===
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph("AI & Local Visibility", styles['CustomTitle']))
    story.append(Paragraph("COMPREHENSIVE AUDIT REPORT", styles['CustomSubtitle']))
    story.append(Spacer(1, 0.5*inch))
    
    # Business info
    story.append(Paragraph(f"<b>Website:</b> {result.url}", styles['Normal']))
    if result.business_name:
        story.append(Paragraph(f"<b>Business:</b> {result.business_name}", styles['Normal']))
    story.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
    story.append(Spacer(1, 0.5*inch))
    
    # Overall scores - use text ratings instead of emojis
    def get_rating(score, max_score):
        pct = score / max_score
        if pct >= 0.7:
            return 'Good'
        elif pct >= 0.4:
            return 'Needs Work'
        else:
            return 'Critical'
    
    score_data = [
        ['Category', 'Score', 'Rating'],
        ['AI Visibility', f"{result.ai_visibility_score}/100", get_rating(result.ai_visibility_score, 100)],
        ['Local SEO', f"{result.local_seo_score}/100", get_rating(result.local_seo_score, 100)],
        ['TOTAL', f"{result.total_score}/200", get_rating(result.total_score, 200)],
    ]
    
    score_table = Table(score_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, -1), (-1, -1), LIGHT),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, ACCENT),
        ('ROWHEIGHTS', (0, 0), (-1, -1), 35),
    ]))
    story.append(score_table)
    
    story.append(Spacer(1, 0.5*inch))
    
    # Quick interpretation
    if result.total_score >= 140:
        interpretation = "Your website is performing well in both AI visibility and local SEO. Focus on the specific recommendations below to reach excellence."
    elif result.total_score >= 80:
        interpretation = "Your website has a solid foundation but significant improvements are needed. Prioritize the quick wins and critical fixes identified in this report."
    else:
        interpretation = "Your website needs urgent attention in both AI visibility and local SEO. Implementing the recommendations in this report could dramatically improve your visibility."
    
    story.append(Paragraph(f"<i>{interpretation}</i>", styles['Normal']))
    story.append(PageBreak())
    
    # === QUICK WINS ===
    story.append(Paragraph("QUICK WINS", styles['SectionHeader']))
    story.append(Paragraph("High-impact, low-effort improvements you can make today:", styles['Normal']))
    story.append(Spacer(1, 10))
    
    for qw in result.quick_wins[:7]:
        story.append(Paragraph(f"* {sanitize_for_pdf(qw)}", styles['QuickWin']))
    
    story.append(Spacer(1, 20))
    
    # === PRIORITY FIXES ===
    if result.priority_fixes:
        story.append(Paragraph("PRIORITY FIXES", styles['SectionHeader']))
        story.append(Paragraph("Categories scoring below 50% that need immediate attention:", styles['Normal']))
        story.append(Spacer(1, 10))
        
        for pf in result.priority_fixes:
            story.append(Paragraph(f"- {sanitize_for_pdf(pf)}", styles['Finding']))
    
    story.append(PageBreak())
    
    # === AI VISIBILITY DETAILED ===
    story.append(Paragraph("AI VISIBILITY AUDIT", styles['SectionHeader']))
    story.append(Paragraph(
        f"Score: <b>{result.ai_visibility_score}/100</b> - "
        "AI visibility determines how likely your business appears in ChatGPT, Claude, Perplexity, and AI-powered search.",
        styles['Normal']
    ))
    story.append(Spacer(1, 10))
    
    for cat in result.ai_categories:
        color = get_score_color(cat.score, cat.max_score if cat.max_score > 0 else 10)
        color_hex = f"#{color.hexval()[2:]}"
        max_display = cat.max_score if cat.max_score > 0 else 10
        story.append(Paragraph(
            f"<font color='{color_hex}'>[{cat.score}/{max_display}]</font> <b>{cat.name}</b>",
            styles['CategoryHeader']
        ))
        
        for finding in cat.findings[:4]:
            story.append(Paragraph(sanitize_for_pdf(finding), styles['Finding']))
            
        if cat.recommendations:
            story.append(Paragraph("<b>Recommendations:</b>", styles['Finding']))
            for rec in cat.recommendations[:3]:
                story.append(Paragraph(f"  > {sanitize_for_pdf(rec)}", styles['Recommendation']))
        
        story.append(Spacer(1, 10))
    
    story.append(PageBreak())
    
    # === LOCAL SEO DETAILED ===
    story.append(Paragraph("LOCAL SEO AUDIT", styles['SectionHeader']))
    story.append(Paragraph(
        f"Score: <b>{result.local_seo_score}/100</b> - "
        "Local SEO determines your visibility in Google Maps, local search, and 'near me' queries.",
        styles['Normal']
    ))
    story.append(Spacer(1, 10))
    
    for cat in result.local_categories:
        # Skip informational-only categories (max_score=0) in detailed breakdown if no findings
        if cat.max_score == 0 and not cat.findings:
            continue
            
        color = get_score_color(cat.score, cat.max_score if cat.max_score > 0 else 10)
        color_hex = f"#{color.hexval()[2:]}"
        
        # For informational categories, show differently
        if cat.max_score == 0:
            story.append(Paragraph(f"<b>{cat.name}</b> (Informational)", styles['CategoryHeader']))
        else:
            story.append(Paragraph(
                f"<font color='{color_hex}'>[{cat.score}/{cat.max_score}]</font> <b>{cat.name}</b>",
                styles['CategoryHeader']
            ))
        
        for finding in cat.findings[:4]:
            story.append(Paragraph(sanitize_for_pdf(finding), styles['Finding']))
            
        if cat.recommendations:
            story.append(Paragraph("<b>Recommendations:</b>", styles['Finding']))
            for rec in cat.recommendations[:3]:
                story.append(Paragraph(f"  > {sanitize_for_pdf(rec)}", styles['Recommendation']))
        
        story.append(Spacer(1, 10))
    
    story.append(PageBreak())
    
    # === ACTION PLAN ===
    story.append(Paragraph("30-DAY ACTION PLAN", styles['SectionHeader']))
    
    # Week 1
    story.append(Paragraph("<b>Week 1: Foundation</b>", styles['CategoryHeader']))
    week1_actions = [
        "Verify/claim Google Business Profile",
        "Fix any blocked AI crawlers in robots.txt",
        "Add LocalBusiness schema markup",
        "Ensure NAP consistency across site",
    ]
    for action in week1_actions:
        story.append(Paragraph(f"[ ] {action}", styles['Finding']))
    
    story.append(Spacer(1, 10))
    
    # Week 2
    story.append(Paragraph("<b>Week 2: Content and Structure</b>", styles['CategoryHeader']))
    week2_actions = [
        "Add FAQ section with schema markup",
        "Create/update city-specific landing pages",
        "Add datePublished/dateModified to content",
        "Optimize heading structure (H1, H2, H3)",
    ]
    for action in week2_actions:
        story.append(Paragraph(f"[ ] {action}", styles['Finding']))
    
    story.append(Spacer(1, 10))
    
    # Week 3
    story.append(Paragraph("<b>Week 3: Authority and Trust</b>", styles['CategoryHeader']))
    week3_actions = [
        "Add author bios with credentials",
        "Display case results and testimonials",
        "Link to authoritative sources",
        "Add trust badges (Avvo, BBB, etc.)",
    ]
    for action in week3_actions:
        story.append(Paragraph(f"[ ] {action}", styles['Finding']))
    
    story.append(Spacer(1, 10))
    
    # Week 4
    story.append(Paragraph("<b>Week 4: Engagement and Reviews</b>", styles['CategoryHeader']))
    week4_actions = [
        "Launch review generation campaign",
        "Post weekly to Google Business Profile",
        "Respond to all existing reviews",
        "Set up ongoing content calendar",
    ]
    for action in week4_actions:
        story.append(Paragraph(f"[ ] {action}", styles['Finding']))
    
    story.append(Spacer(1, 0.5*inch))
    
    # === ENHANCED DATA (DataForSEO) ===
    if enhanced_result:
        story.append(PageBreak())
        story.append(Paragraph("LIVE SEARCH DATA (via DataForSEO)", styles['SectionHeader']))
        story.append(Paragraph(
            f"Real-time Google ranking data - API cost: ${enhanced_result.api_cost:.4f}",
            styles['CustomSubtitle']
        ))
        story.append(Spacer(1, 10))
        
        # Ranked Keywords
        if enhanced_result.ranked_keywords:
            story.append(Paragraph("<b>Your Top Ranked Keywords</b>", styles['CategoryHeader']))
            for i, kw in enumerate(enhanced_result.ranked_keywords[:15], 1):
                vol = kw.get('volume')
                vol_str = f" ({vol:,} searches/mo)" if vol else ""
                pos = kw.get('position', '?')
                keyword = kw.get('keyword', 'Unknown')
                story.append(Paragraph(
                    f"#{pos}: {keyword}{vol_str}",
                    styles['Finding']
                ))
            story.append(Spacer(1, 15))
        
        # Competitors - only show if we have meaningful data
        competitors_with_data = [c for c in enhanced_result.competitors if c.get('keywords_count') and c.get('keywords_count') != 'None']
        if competitors_with_data:
            story.append(Paragraph("<b>Your Top Organic Competitors</b>", styles['CategoryHeader']))
            for comp in competitors_with_data[:10]:
                kw_count = comp.get('keywords_count', 0)
                domain = comp.get('domain', 'Unknown')
                if kw_count and int(kw_count) > 0:
                    story.append(Paragraph(
                        f"- {domain} ({kw_count} overlapping keywords)",
                        styles['Finding']
                    ))
            story.append(Spacer(1, 15))
        
        # SERP Rankings
        if enhanced_result.serp_rankings:
            story.append(Paragraph("<b>Your Google Rankings (Live Check)</b>", styles['CategoryHeader']))
            for r in enhanced_result.serp_rankings:
                pos = r.get('position', '?')
                kw = r.get('keyword', '')
                story.append(Paragraph(
                    f"Position #{pos} for \"{kw}\"",
                    styles['Finding']
                ))
            story.append(Spacer(1, 15))
        
        # On-Page Issues - translate to human-readable
        if enhanced_result.onpage_issues:
            story.append(Paragraph("<b>Technical SEO Issues Detected</b>", styles['CategoryHeader']))
            
            # Translate cryptic issue names to human-readable
            issue_translations = {
                'no content encoding': 'No compression enabled (gzip/brotli)',
                'high loading time': 'Slow page load time',
                'high waiting time': 'Slow server response time',
                'is redirect': 'Page has redirects',
                'is 4xx code': 'Page returns 4xx error',
                'is 5xx code': 'Page returns server error',
                'is broken': 'Page has broken elements',
                'is http': 'Page uses insecure HTTP',
                'from sitemap': 'Not in sitemap',
                'has micromarkup': 'Missing structured data',
                'no content encoding': 'No gzip/brotli compression',
            }
            
            for issue in enhanced_result.onpage_issues[:10]:
                issue_text = issue.get('issue', 'Unknown issue').lower()
                human_readable = issue_translations.get(issue_text, issue.get('issue', 'Unknown issue'))
                severity = issue.get('severity', 'warning')
                marker = '[!]' if severity == 'critical' else '[-]'
                story.append(Paragraph(
                    f"{marker} {human_readable}",
                    styles['Finding']
                ))
            story.append(Spacer(1, 15))
    
    # === FOOTER / CTA ===
    story.append(Paragraph("-" * 70, styles['Normal']))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "<b>Need help implementing these recommendations?</b>",
        ParagraphStyle('CTA', parent=styles['Normal'], fontSize=14, alignment=TA_CENTER)
    ))
    story.append(Paragraph(
        "Schedule a free strategy call to discuss your AI visibility and local SEO roadmap.",
        ParagraphStyle('CTAText', parent=styles['Normal'], fontSize=12, alignment=TA_CENTER)
    ))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "<b>Book a Call: kuriosbrand.com/call</b>",
        ParagraphStyle('CTALink', parent=styles['Normal'], fontSize=14, alignment=TA_CENTER, textColor=HIGHLIGHT)
    ))
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        f"<i>Report generated by Kurios AI Audit Tool - {datetime.now().strftime('%Y')}</i>",
        ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, alignment=TA_CENTER, textColor=ACCENT)
    ))
    
    # Build PDF
    doc.build(story)
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    if output_path:
        with open(output_path, 'wb') as f:
            f.write(pdf_bytes)
            
    return pdf_bytes


def main():
    """Test PDF generation"""
    from analyzer import WebsiteAnalyzer
    import sys
    
    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    
    print(f"Analyzing {url}...")
    analyzer = WebsiteAnalyzer(url)
    result = analyzer.run_full_audit()
    
    output_path = f"audit_report_{result.business_name or 'website'}.pdf".replace(' ', '_')
    generate_pdf(result, output_path)
    print(f"PDF saved to: {output_path}")


if __name__ == "__main__":
    main()
