#!/usr/bin/env python3
"""
Email sender for audit reports
Uses Gmail SMTP with OAuth or app password
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
import json
from datetime import datetime


def load_credentials():
    """Load email credentials from config"""
    creds_path = os.path.expanduser("~/.config/gmail/credentials.json")
    if os.path.exists(creds_path):
        with open(creds_path) as f:
            return json.load(f)
    
    # Fallback to env vars
    return {
        "email": os.getenv("GMAIL_EMAIL", "sierra@kuriosbrand.com"),
        "app_password": os.getenv("GMAIL_APP_PASSWORD", ""),
    }


def send_audit_report(
    to_email: str,
    business_name: str,
    url: str,
    ai_score: int,
    local_score: int,
    total_score: int,
    pdf_bytes: bytes
) -> bool:
    """Send audit report email with PDF attachment"""
    
    creds = load_credentials()
    from_email = creds.get("email", "sierra@kuriosbrand.com")
    app_password = creds.get("app_password", "")
    
    if not app_password:
        print("Warning: No app password configured, email not sent")
        return False
    
    # Create message
    msg = MIMEMultipart('mixed')
    msg['From'] = f"Kurios AI Audit <{from_email}>"
    msg['To'] = to_email
    msg['Subject'] = f"Your AI & Local Visibility Audit Report - {business_name or url}"
    
    # Score interpretation
    if total_score >= 140:
        grade = "A"
        interpretation = "performing well"
        emoji = "🟢"
    elif total_score >= 100:
        grade = "B"
        interpretation = "on the right track"
        emoji = "🟡"
    elif total_score >= 60:
        grade = "C"
        interpretation = "needs improvement"
        emoji = "🟠"
    else:
        grade = "D"
        interpretation = "needs urgent attention"
        emoji = "🔴"
    
    # HTML body - minimal, clean for deliverability
    html_body = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">

<h2>Your AI & Local Visibility Audit</h2>
<p><strong>Website:</strong> {url}</p>

<p>Hi there,</p>

<p>Your audit is ready! We analyzed your website across 20 factors that determine visibility in AI search (ChatGPT, Claude, Perplexity) and local search (Google Maps).</p>

<h3>Your Scores</h3>
<ul>
<li><strong>AI Visibility:</strong> {ai_score}/100</li>
<li><strong>Local SEO:</strong> {local_score}/100</li>
<li><strong>Overall:</strong> {total_score}/200 (Grade: {grade}) - {interpretation}</li>
</ul>

<p>The attached PDF contains:</p>
<ul>
<li>Detailed breakdown of all 20 categories</li>
<li>Quick wins you can implement today</li>
<li>Priority fixes that need attention</li>
</ul>

<h3>What's next?</h3>
<p>Want help implementing these recommendations? Book a free strategy call:</p>
<p><a href="https://kuriosbrand.com/call">https://kuriosbrand.com/call</a></p>

<p>Questions? Just reply to this email.</p>

<p>Best,<br>
The Kurios Team</p>

<hr style="border: none; border-top: 1px solid #ccc; margin: 20px 0;">
<p style="font-size: 12px; color: #666;">You received this email because you requested an audit at kuriosbrand.com</p>

</body>
</html>"""
    
    # Plain text alternative
    text_body = f"""
    Your AI & Local Visibility Audit Results
    ==========================================
    
    Website: {url}
    
    SCORES:
    • AI Visibility: {ai_score}/100
    • Local SEO: {local_score}/100
    • Overall: {total_score}/200 (Grade: {grade})
    
    Your website is {interpretation}.
    
    The attached PDF contains:
    - Detailed breakdown of all 20 scoring categories
    - Quick wins you can implement today
    - Priority fixes that need immediate attention  
    - A 30-day action plan
    
    NEXT STEPS:
    Book a free strategy call: https://kuriosbrand.com/call
    
    Questions? Reply to this email.
    
    Best,
    The KuriosBrand Team
    """
    
    # Create alternatives
    msg_alternative = MIMEMultipart('alternative')
    msg_alternative.attach(MIMEText(text_body, 'plain'))
    msg_alternative.attach(MIMEText(html_body, 'html'))
    msg.attach(msg_alternative)
    
    # Attach PDF
    pdf_attachment = MIMEApplication(pdf_bytes, _subtype='pdf')
    filename = f"AI_Local_Visibility_Audit_{business_name or 'Report'}_{datetime.now().strftime('%Y%m%d')}.pdf"
    filename = filename.replace(' ', '_')
    pdf_attachment.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(pdf_attachment)
    
    # Send
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(from_email, app_password)
            server.send_message(msg)
        print(f"✅ Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False


def main():
    """Test email sending"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python email_sender.py <to_email>")
        return
        
    # Create a dummy PDF for testing
    from analyzer import WebsiteAnalyzer
    from pdf_generator import generate_pdf
    
    url = "https://example.com"
    analyzer = WebsiteAnalyzer(url)
    result = analyzer.run_full_audit()
    pdf_bytes = generate_pdf(result)
    
    send_audit_report(
        to_email=sys.argv[1],
        business_name=result.business_name,
        url=url,
        ai_score=result.ai_visibility_score,
        local_score=result.local_seo_score,
        total_score=result.total_score,
        pdf_bytes=pdf_bytes
    )


if __name__ == "__main__":
    main()
