#!/usr/bin/env python3
"""
PDF Report Generator for Directory SEO Audit

Generates professional PDF reports for directory website audits.
Based on the existing pdf_generator.py but customized for directory-specific metrics.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, ListFlowable, ListItem
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect, String
from io import BytesIO
from datetime import datetime
from directory_analyzer import DirectoryAuditResult, CategoryScore
import os
import re


def sanitize_for_pdf(text: str) -> str:
    """Replace emojis and special chars with ASCII-safe alternatives"""
    if not text:
        return ""
    
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
        '🚨': '[!]',
        '📋': '',
        '📞': '',
        '📧': '',
        '📈': '',
        '📄': '',
        # Additional bullet/special chars
        '•': '-',
        '●': '-',
        '○': '-',
        '◆': '-',
        '◇': '-',
        '▪': '-',
        '▫': '-',
        '►': '>',
        '→': '->',
        '←': '<-',
        '↑': '^',
        '↓': 'v',
        '★': '*',
        '☆': '*',
        '✔': '[OK]',
        '✗': '[X]',
        '✘': '[X]',
        '⚙': '',
        '🔗': '',
        '🌐': '',
        '📱': '',
        '💻': '',
        '🏠': '',
        '📝': '',
        '🎯': '',
        '🚀': '',
        '⭐': '*',
        '❗': '!',
        '❓': '?',
        '❕': '!',
        '❔': '?',
        '✨': '',
        '🔒': '',
        '🔓': '',
        # Typographic quotes and dashes
        '"': '"',
        '"': '"',
        ''': "'",
        ''': "'",
        '–': '-',
        '—': '-',
        '…': '...',
    }
    for emoji, replacement in replacements.items():
        text = text.replace(emoji, replacement)
    
    # Remove any remaining non-ASCII characters that could cause issues
    # But keep safe extended ASCII like accented letters
    result = []
    for char in text:
        code = ord(char)
        if code < 128:  # Basic ASCII
            result.append(char)
        elif 160 <= code <= 255:  # Extended ASCII (accented chars, etc.)
            result.append(char)
        elif code in [8211, 8212]:  # En-dash, em-dash already handled
            result.append('-')
        elif code == 8226:  # Bullet point
            result.append('-')
        else:
            # Skip other Unicode characters that might cause font issues
            pass
    
    return ''.join(result)


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
    pct = score / max_score if max_score > 0 else 0
    if pct >= 0.7:
        return SUCCESS
    elif pct >= 0.4:
        return WARNING
    else:
        return DANGER


def get_grade_color(grade: str) -> HexColor:
    """Return color based on letter grade"""
    if grade in ['A+', 'A']:
        return SUCCESS
    elif grade in ['B']:
        return HexColor('#90EE90')  # Light green
    elif grade in ['C']:
        return WARNING
    elif grade in ['D']:
        return HexColor('#FFA500')  # Orange
    else:
        return DANGER


def generate_directory_pdf(result: DirectoryAuditResult, output_path: str = None) -> bytes:
    """Generate PDF report from directory audit result
    
    Args:
        result: DirectoryAuditResult from the analyzer
        output_path: Optional file path to save PDF
        
    Returns:
        PDF as bytes
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
        name='SubsectionHeader',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=SECONDARY,
        spaceBefore=15,
        spaceAfter=8,
    ))
    
    styles.add(ParagraphStyle(
        name='CategoryHeader',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=ACCENT,
        spaceBefore=12,
        spaceAfter=5,
    ))
    
    styles.add(ParagraphStyle(
        name='Finding',
        parent=styles['Normal'],
        fontSize=10,
        leftIndent=20,
        rightIndent=10,
        spaceBefore=2,
        spaceAfter=2,
        wordWrap='CJK',  # Better word wrapping
    ))
    
    styles.add(ParagraphStyle(
        name='Recommendation',
        parent=styles['Normal'],
        fontSize=10,
        leftIndent=20,
        rightIndent=10,
        textColor=ACCENT,
        spaceBefore=2,
        spaceAfter=2,
        wordWrap='CJK',  # Better word wrapping
    ))
    
    styles.add(ParagraphStyle(
        name='QuickWin',
        parent=styles['Normal'],
        fontSize=11,
        leftIndent=15,
        rightIndent=10,
        textColor=HexColor('#155724'),
        backColor=HexColor('#d4edda'),
        borderPadding=5,
        spaceBefore=5,
        spaceAfter=5,
        wordWrap='CJK',
    ))
    
    styles.add(ParagraphStyle(
        name='PriorityFix',
        parent=styles['Normal'],
        fontSize=11,
        leftIndent=15,
        rightIndent=10,
        textColor=HexColor('#721c24'),
        backColor=HexColor('#f8d7da'),
        borderPadding=5,
        spaceBefore=5,
        spaceAfter=5,
        wordWrap='CJK',
    ))
    
    # Build content
    story = []
    
    # === COVER PAGE ===
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph("Directory SEO", styles['CustomTitle']))
    story.append(Paragraph("COMPREHENSIVE AUDIT REPORT", styles['CustomSubtitle']))
    story.append(Spacer(1, 0.5*inch))
    
    # Directory info - truncate very long URLs/names
    url_display = result.url if len(result.url) <= 60 else result.url[:57] + "..."
    story.append(Paragraph(f"<b>Website:</b> {sanitize_for_pdf(url_display)}", styles['Normal']))
    if result.directory_name:
        dir_name = sanitize_for_pdf(result.directory_name)
        # Truncate very long names
        if len(dir_name) > 80:
            dir_name = dir_name[:77] + "..."
        story.append(Paragraph(f"<b>Directory:</b> {dir_name}", styles['Normal']))
    story.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%B %d, %Y at %H:%M')}", styles['Normal']))
    story.append(Spacer(1, 0.5*inch))
    
    # Main health score box
    grade_color = get_grade_color(result.grade)
    
    story.append(Paragraph(
        f"<font size='36' color='#{grade_color.hexval()[2:]}'><b>TOTAL SCORE</b></font>",
        ParagraphStyle('ScoreTitle', parent=styles['Normal'], alignment=TA_CENTER)
    ))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        f"<font size='48' color='#{grade_color.hexval()[2:]}'><b>{result.total_score}/300</b></font>",
        ParagraphStyle('Score', parent=styles['Normal'], alignment=TA_CENTER, leading=55)
    ))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        f"<font size='12' color='#{DARK.hexval()[2:]}'>Directory SEO: {result.directory_health_score}/200  |  AI Visibility: {result.ai_visibility_score}/100</font>",
        ParagraphStyle('SubScore', parent=styles['Normal'], alignment=TA_CENTER, leading=18)
    ))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        f"<font size='24' color='#{grade_color.hexval()[2:]}'><b>Grade: {result.grade}</b></font>",
        ParagraphStyle('Grade', parent=styles['Normal'], alignment=TA_CENTER, leading=30)
    ))
    story.append(Spacer(1, 0.5*inch))
    
    # Section scores table
    score_data = [
        ['Section', 'Score', 'Max', 'Status'],
        ['Structure & Architecture', str(result.structure_score), '50', get_status(result.structure_score, 50)],
        ['On-Page SEO', str(result.onpage_score), '50', get_status(result.onpage_score, 50)],
        ['Content Quality', str(result.content_score), '40', get_status(result.content_score, 40)],
        ['Technical SEO', str(result.technical_score), '30', get_status(result.technical_score, 30)],
        ['Authority & Trust', str(result.authority_score), '30', get_status(result.authority_score, 30)],
        ['AI Visibility', str(result.ai_visibility_score), '100', get_status(result.ai_visibility_score, 100)],
        ['TOTAL', str(result.total_score), '300', result.grade],
    ]
    
    score_table = Table(score_data, colWidths=[2.5*inch, 1*inch, 1*inch, 1.5*inch])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, -1), (-1, -1), LIGHT),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, ACCENT),
        ('ROWHEIGHTS', (0, 0), (-1, -1), 30),
    ]))
    story.append(score_table)
    
    story.append(Spacer(1, 0.5*inch))
    
    # Quick interpretation
    interpretation = get_interpretation(result.directory_health_score)
    story.append(Paragraph(f"<i>{interpretation}</i>", styles['Normal']))
    story.append(PageBreak())
    
    # === EXECUTIVE SUMMARY ===
    story.append(Paragraph("EXECUTIVE SUMMARY", styles['SectionHeader']))
    story.append(Spacer(1, 10))
    
    # Pages analyzed stats
    tech_data = result.technical_data
    stats_data = [
        ['Metric', 'Value'],
        ['Listing Pages Analyzed', str(tech_data.get('listing_pages', 0))],
        ['Category Pages Analyzed', str(tech_data.get('category_pages', 0))],
        ['Location Pages Found', str(tech_data.get('location_pages', 0))],
        ['Sitemap URLs', str(tech_data.get('sitemap_urls', 0))],
        ['Schema Objects Found', str(tech_data.get('schemas_found', 0))],
    ]
    
    stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SECONDARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, LIGHT),
        ('ROWHEIGHTS', (0, 0), (-1, -1), 25),
    ]))
    story.append(stats_table)
    story.append(Spacer(1, 20))
    
    # === PRIORITY FIXES ===
    if result.priority_fixes:
        story.append(Paragraph("PRIORITY FIXES", styles['SectionHeader']))
        story.append(Paragraph("Categories scoring below 50% that need immediate attention:", styles['Normal']))
        story.append(Spacer(1, 10))
        
        for pf in result.priority_fixes[:8]:
            story.append(Paragraph(sanitize_for_pdf(pf), styles['PriorityFix']))
            
        story.append(Spacer(1, 20))
    
    # === QUICK WINS ===
    if result.quick_wins:
        story.append(Paragraph("QUICK WINS", styles['SectionHeader']))
        story.append(Paragraph("High-impact improvements you can make quickly:", styles['Normal']))
        story.append(Spacer(1, 10))
        
        for qw in result.quick_wins[:8]:
            story.append(Paragraph(f"* {sanitize_for_pdf(qw)}", styles['QuickWin']))
    
    story.append(PageBreak())
    
    # === STRUCTURE & ARCHITECTURE SECTION ===
    story.append(Paragraph(f"STRUCTURE & ARCHITECTURE ({result.structure_score}/50)", styles['SectionHeader']))
    story.append(Paragraph(
        "How well your directory is organized - listings, categories, locations, and internal linking.",
        styles['Normal']
    ))
    story.append(Spacer(1, 10))
    
    for cat in result.structure_categories:
        add_category_section(story, cat, styles)
    
    story.append(PageBreak())
    
    # === ON-PAGE SEO SECTION ===
    story.append(Paragraph(f"ON-PAGE SEO ({result.onpage_score}/50)", styles['SectionHeader']))
    story.append(Paragraph(
        "Title tags, meta descriptions, headings, schema markup, and canonicals.",
        styles['Normal']
    ))
    story.append(Spacer(1, 10))
    
    for cat in result.onpage_categories:
        add_category_section(story, cat, styles)
    
    story.append(PageBreak())
    
    # === CONTENT QUALITY SECTION ===
    story.append(Paragraph(f"CONTENT QUALITY ({result.content_score}/40)", styles['SectionHeader']))
    story.append(Paragraph(
        "Listing descriptions, user-generated content, editorial content, and freshness.",
        styles['Normal']
    ))
    story.append(Spacer(1, 10))
    
    for cat in result.content_categories:
        add_category_section(story, cat, styles)
    
    story.append(PageBreak())
    
    # === TECHNICAL SEO SECTION ===
    story.append(Paragraph(f"TECHNICAL SEO ({result.technical_score}/30)", styles['SectionHeader']))
    story.append(Paragraph(
        "Page speed, mobile usability, and crawlability.",
        styles['Normal']
    ))
    story.append(Spacer(1, 10))
    
    for cat in result.technical_categories:
        add_category_section(story, cat, styles)
    
    story.append(Spacer(1, 20))
    
    # === AUTHORITY & TRUST SECTION ===
    story.append(Paragraph(f"AUTHORITY & TRUST ({result.authority_score}/30)", styles['SectionHeader']))
    story.append(Paragraph(
        "Backlink profile, social proof, and E-E-A-T signals.",
        styles['Normal']
    ))
    story.append(Spacer(1, 10))
    
    for cat in result.authority_categories:
        add_category_section(story, cat, styles)
    
    story.append(Spacer(1, 20))
    
    # === AI VISIBILITY SECTION ===
    if result.ai_categories:
        story.append(Paragraph(f"AI VISIBILITY ({result.ai_visibility_score}/100)", styles['SectionHeader']))
        story.append(Paragraph(
            "How well the site is optimized for AI crawlers, LLMs, and AI-powered search engines.",
            styles['Normal']
        ))
        story.append(Spacer(1, 10))
        
        for cat in result.ai_categories:
            add_category_section(story, cat, styles)
    
    story.append(PageBreak())
    
    # === 30-DAY ACTION PLAN ===
    story.append(Paragraph("30-DAY DIRECTORY IMPROVEMENT PLAN", styles['SectionHeader']))
    
    # Week 1
    story.append(Paragraph("<b>Week 1: Foundation & Structure</b>", styles['SubsectionHeader']))
    week1_actions = [
        "Audit and fix URL structure for consistency",
        "Implement or fix BreadcrumbList schema",
        "Ensure all listings have canonical tags",
        "Block filter/sort URLs in robots.txt",
        "Submit updated sitemap with all listing pages",
    ]
    for action in week1_actions:
        story.append(Paragraph(f"[ ] {action}", styles['Finding']))
    
    story.append(Spacer(1, 10))
    
    # Week 2
    story.append(Paragraph("<b>Week 2: Schema & On-Page</b>", styles['SubsectionHeader']))
    week2_actions = [
        "Implement LocalBusiness schema on all listing pages",
        "Add ItemList schema to category pages",
        "Ensure unique title tags (50-60 chars) per page",
        "Write unique meta descriptions (150-160 chars)",
        "Fix heading hierarchy (single H1, structured H2/H3)",
    ]
    for action in week2_actions:
        story.append(Paragraph(f"[ ] {action}", styles['Finding']))
    
    story.append(Spacer(1, 10))
    
    # Week 3
    story.append(Paragraph("<b>Week 3: Content Quality</b>", styles['SubsectionHeader']))
    week3_actions = [
        "Expand thin listing descriptions to 300+ words",
        "Add/improve review and rating system",
        "Create 'Related Listings' sections",
        "Start blog with 'Best [Category] in [Location]' posts",
        "Add visible dates (last updated) to listings",
    ]
    for action in week3_actions:
        story.append(Paragraph(f"[ ] {action}", styles['Finding']))
    
    story.append(Spacer(1, 10))
    
    # Week 4
    story.append(Paragraph("<b>Week 4: Authority & Growth</b>", styles['SubsectionHeader']))
    week4_actions = [
        "Add About, Contact, Privacy, and Terms pages",
        "Implement social sharing and links",
        "Create 'How We Rate' methodology page",
        "Begin outreach for backlinks and partnerships",
        "Set up Google Search Console monitoring",
    ]
    for action in week4_actions:
        story.append(Paragraph(f"[ ] {action}", styles['Finding']))
    
    story.append(Spacer(1, 0.5*inch))
    
    # === DIRECTORY-SPECIFIC RECOMMENDATIONS ===
    story.append(Paragraph("DIRECTORY-SPECIFIC RECOMMENDATIONS", styles['SectionHeader']))
    
    directory_tips = [
        "<b>Listing Page Template:</b> Ensure every listing has: name, description (300+ words), address, phone, hours, images, categories, reviews, and external website link.",
        "<b>Category Hub Strategy:</b> Create pillar category pages with unique intro content, filtering options, and internal links to subcategories and top listings.",
        "<b>Location Pages:</b> If geo-relevant, create city/state landing pages targeting '[category] in [city]' searches.",
        "<b>User-Generated Content:</b> Encourage and display reviews - this creates unique content and builds trust with users and search engines.",
        "<b>Schema for Rich Results:</b> LocalBusiness, AggregateRating, ItemList, and FAQPage schemas can earn rich snippets in search results.",
        "<b>Programmatic SEO:</b> Use templates + unique data points to generate valuable pages at scale without thin content issues.",
    ]
    
    for tip in directory_tips:
        story.append(Paragraph(f"- {tip}", styles['Finding']))
        story.append(Spacer(1, 5))
    
    story.append(PageBreak())
    
    # === CATEGORY SCORE SUMMARY TABLE ===
    story.append(Paragraph("COMPLETE CATEGORY BREAKDOWN", styles['SectionHeader']))
    
    all_categories = (
        result.structure_categories + 
        result.onpage_categories + 
        result.content_categories + 
        result.technical_categories + 
        result.authority_categories
    )
    
    cat_data = [['#', 'Category', 'Score', 'Max', '%']]
    for i, cat in enumerate(all_categories, 1):
        score = cat.score if cat.score is not None else 0
        max_score = cat.max_score if cat.max_score is not None else 10
        name = sanitize_for_pdf(cat.name if cat.name else "Unknown")
        pct = score / max_score * 100 if max_score > 0 else 0
        cat_data.append([
            str(i),
            name[:35],
            str(score),
            str(max_score),
            f"{pct:.0f}%"
        ])
    
    cat_table = Table(cat_data, colWidths=[0.4*inch, 3.2*inch, 0.7*inch, 0.6*inch, 0.7*inch])
    cat_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, LIGHT),
        ('ROWHEIGHTS', (0, 0), (-1, -1), 22),
    ]))
    
    # Color-code rows by score
    for i, cat in enumerate(all_categories, 1):
        pct = cat.score / cat.max_score if cat.max_score > 0 else 0
        if pct < 0.4:
            cat_table.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), HexColor('#ffe6e6'))]))
        elif pct < 0.7:
            cat_table.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), HexColor('#fff3e6'))]))
            
    story.append(cat_table)
    
    story.append(Spacer(1, 0.5*inch))
    
    # === FOOTER / CTA ===
    story.append(Paragraph("-" * 70, styles['Normal']))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "<b>Need help implementing these recommendations?</b>",
        ParagraphStyle('CTA', parent=styles['Normal'], fontSize=14, alignment=TA_CENTER)
    ))
    story.append(Paragraph(
        "Schedule a free strategy call to discuss your directory SEO roadmap.",
        ParagraphStyle('CTAText', parent=styles['Normal'], fontSize=12, alignment=TA_CENTER)
    ))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "<b>Book a Call: kuriosbrand.com/call</b>",
        ParagraphStyle('CTALink', parent=styles['Normal'], fontSize=14, alignment=TA_CENTER, textColor=HIGHLIGHT)
    ))
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        f"<i>Report generated by Kurios Directory SEO Audit Tool - {datetime.now().strftime('%Y')}</i>",
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


def add_category_section(story, cat: CategoryScore, styles):
    """Add a category section to the report"""
    if cat is None:
        return
    
    # Safely get score values
    score = cat.score if cat.score is not None else 0
    max_score = cat.max_score if cat.max_score is not None else 10
    name = cat.name if cat.name else "Unnamed Category"
    
    color = get_score_color(score, max_score)
    color_hex = f"#{color.hexval()[2:]}"
    
    story.append(Paragraph(
        f"<font color='{color_hex}'><b>[{score}/{max_score}]</b></font> <b>{sanitize_for_pdf(name)}</b>",
        styles['CategoryHeader']
    ))
    
    # Findings (handle None and empty)
    findings = cat.findings if cat.findings else []
    for finding in findings[:5]:
        if finding:  # Skip None or empty findings
            story.append(Paragraph(sanitize_for_pdf(str(finding)), styles['Finding']))
        
    # Recommendations (handle None and empty)
    recommendations = cat.recommendations if cat.recommendations else []
    if recommendations:
        story.append(Paragraph("<b>Recommendations:</b>", styles['Finding']))
        for rec in recommendations[:3]:
            if rec:  # Skip None or empty recommendations
                story.append(Paragraph(f"  > {sanitize_for_pdf(str(rec))}", styles['Recommendation']))
    
    story.append(Spacer(1, 10))


def get_status(score: int, max_score: int) -> str:
    """Get status text based on score percentage"""
    pct = score / max_score if max_score > 0 else 0
    if pct >= 0.8:
        return "Excellent"
    elif pct >= 0.6:
        return "Good"
    elif pct >= 0.4:
        return "Needs Work"
    else:
        return "Critical"


def get_interpretation(score: int) -> str:
    """Get interpretation text based on total score"""
    pct = score / 300 * 100
    
    if pct >= 80:
        return "Your directory is performing excellently. Focus on the specific recommendations to maintain and enhance your competitive advantage."
    elif pct >= 60:
        return "Your directory has a solid foundation with room for improvement. Prioritize the quick wins and work through the action plan to boost your rankings."
    elif pct >= 40:
        return "Your directory needs significant improvements across multiple areas. Start with the priority fixes and follow the 30-day action plan systematically."
    else:
        return "Your directory requires urgent attention. Implementing the recommendations in this report could dramatically improve your search visibility and user experience."


def main():
    """Test PDF generation"""
    from directory_analyzer import DirectorySEOAnalyzer
    import sys
    
    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    
    print(f"Analyzing {url}...")
    analyzer = DirectorySEOAnalyzer(url)
    result = analyzer.run_full_audit()
    
    output_path = f"directory_audit_{result.directory_name or 'website'}.pdf".replace(' ', '_')
    generate_directory_pdf(result, output_path)
    print(f"PDF saved to: {output_path}")


if __name__ == "__main__":
    main()
