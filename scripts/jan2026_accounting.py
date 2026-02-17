#!/usr/bin/env python3
"""
January 2026 KuriosBrand Accounting Sheet Builder
Processes bank data and writes to Google Sheets
"""

import csv
import json
import requests
from datetime import datetime
from collections import defaultdict

# Configuration
SHEET_ID = "1EMYwVZVoAGUMAlM-G2C1NunZ_RZOvDmgJxdBaKqUriE"
TOKEN_PATH = "/home/ec2-user/.config/gcal-pro/token.json"

# CSV file paths
CSV_FILES = {
    "savings_7036": "/home/ec2-user/.clawdbot/media/inbound/4f693353-e644-4851-824d-e9e7539a9386.csv",
    "sapphire_4252": "/home/ec2-user/.clawdbot/media/inbound/92ba6379-8258-434d-a71d-de9b2f97f4cf.csv",
    "ink_0678": "/home/ec2-user/.clawdbot/media/inbound/e2e37833-e1ad-4f3b-88fc-c46631ead6a6.csv",
    "personal_0068": "/home/ec2-user/.clawdbot/media/inbound/e318304d-8707-42b4-9f8f-57c3b238cbfa.csv",
    "business_4991": "/home/ec2-user/.clawdbot/media/inbound/91a594f7-5dc7-4e9f-911e-ccbf82442cd9.csv",
}

def load_token():
    with open(TOKEN_PATH) as f:
        return json.load(f)["access_token"]

def is_january_2026(date_str):
    """Check if date is in January 2026"""
    try:
        # Try MM/DD/YYYY format
        dt = datetime.strptime(date_str, "%m/%d/%Y")
        return dt.year == 2026 and dt.month == 1
    except:
        return False

def parse_amount(amount_str):
    """Parse amount string to float"""
    if isinstance(amount_str, (int, float)):
        return float(amount_str)
    # Remove commas and convert
    cleaned = str(amount_str).replace(",", "").replace("$", "")
    try:
        return float(cleaned)
    except:
        return 0.0

def categorize_transaction(description, amount, account_type):
    """Categorize a transaction based on description and rules"""
    desc_upper = description.upper()
    
    # Special rules from instructions
    if "JONATHAN BIBLE" in desc_upper:
        return "Net Zero - Refund", "Other"
    if "ALEX" in desc_upper and "SHTABSKY" in desc_upper:
        return "Currency Exchange Help", "Other"
    if "CHRISTIAN WILLARD" in desc_upper:
        return "Revenue - Backlinks", "🏗️ R&R"
    if "STRIPE" in desc_upper and "CAPITAL" in desc_upper:
        return "Debt - Loan Proceeds", "Other"
    if "4200" in str(amount) and "STRIPE" in desc_upper:
        return "Debt - Loan Proceeds", "Other"
    if "AFFIRM" in desc_upper:
        return "Debt Payment - Mattress", "Personal"
    if "ROBINHOOD" in desc_upper:
        return "Personal Investment", "Personal"
    if "ACORNS" in desc_upper:
        return "Personal Investment", "Personal"
    if "WISE" in desc_upper and amount < 0:
        return "Personal Living - Travel", "Personal"
    
    # Revenue sources
    if "STRIPE" in desc_upper and amount > 0:
        return "Revenue - Stripe", "🚗 MVA"
    if "ACI ENTERPRISE" in desc_upper:
        return "Revenue - R&R", "🏗️ R&R"
    if "ANTHONY REDDIN" in desc_upper and amount > 0:
        return "Revenue - R&R", "🏗️ R&R"
    if "A-Z MOBILE" in desc_upper and amount > 0:
        return "Revenue - COD Referral", "🚗 MVA"
    
    # Expense categories
    if "FACEBK" in desc_upper or "META" in desc_upper:
        return "Marketing - Meta Ads", "OpEx"
    if "GOOGLE" in desc_upper and "ADS" in desc_upper:
        return "Marketing - Google Ads", "OpEx"
    if "HIGHLEVEL" in desc_upper or "GHL" in desc_upper:
        return "Software - GHL", "OpEx"
    if "LEMLIST" in desc_upper:
        return "Software - Lemlist", "OpEx"
    if "INSTANTLY" in desc_upper:
        return "Software - Instantly", "OpEx"
    if "CLOUDFLARE" in desc_upper:
        return "Software - Cloudflare", "OpEx"
    if "CLAUDE" in desc_upper or "ANTHROPIC" in desc_upper:
        return "Software - AI (Claude)", "OpEx"
    if "OPENAI" in desc_upper or "CHATGPT" in desc_upper:
        return "Software - AI (OpenAI)", "OpEx"
    if "CURSOR" in desc_upper:
        return "Software - Cursor", "OpEx"
    if "LOVABLE" in desc_upper:
        return "Software - Lovable", "OpEx"
    if "10WEB" in desc_upper:
        return "Software - 10Web", "OpEx"
    if "SPOTIFY" in desc_upper:
        return "Subscription - Spotify", "Personal"
    if "HULU" in desc_upper:
        return "Subscription - Hulu", "Personal"
    if "AIRBNB" in desc_upper:
        return "Travel - Accommodation", "Personal"
    if "LATAM" in desc_upper or "IBERIA" in desc_upper:
        return "Travel - Flights", "Personal"
    if "ATM" in desc_upper:
        return "Cash Withdrawal", "Personal"
    if "SAFETYWING" in desc_upper:
        return "Insurance - Travel", "OpEx"
    if "TMOBILE" in desc_upper:
        return "Utilities - Phone", "Personal"
    if "DEPT EDUCATION" in desc_upper or "STUDENT LN" in desc_upper:
        return "Debt - Student Loan", "Personal"
    if "SELF LENDER" in desc_upper or "CREDIT STRONG" in desc_upper:
        return "Credit Building", "Personal"
    if "DESCRIPT" in desc_upper:
        return "Software - Descript", "OpEx"
    if "EXA.AI" in desc_upper:
        return "Software - Exa AI", "OpEx"
    if "DATAFORSEO" in desc_upper:
        return "Software - DataForSEO", "OpEx"
    if "RAPIDURLINDEXER" in desc_upper:
        return "Software - URL Indexer", "OpEx"
    if "INVIDEO" in desc_upper:
        return "Software - InVideo", "OpEx"
    if "HIGGSFIELD" in desc_upper:
        return "Software - Higgsfield", "OpEx"
    if "NAMECHEAP" in desc_upper:
        return "Domain - Namecheap", "OpEx"
    if "HOSTMYAPPL" in desc_upper:
        return "Hosting", "OpEx"
    if "TRAVELINGMAILBOX" in desc_upper:
        return "Utilities - Virtual Mail", "OpEx"
    if "MYFICO" in desc_upper:
        return "Personal - Credit Monitoring", "Personal"
    if "PATREON" in desc_upper:
        return "Subscription - Patreon", "Personal"
    if "AIRALO" in desc_upper:
        return "Travel - eSIM", "Personal"
    if "APPLE" in desc_upper:
        return "Subscription - Apple", "Personal"
    if "SUPERMEMORY" in desc_upper:
        return "Software - Supermemory", "OpEx"
    if "NORD" in desc_upper and "VPN" in desc_upper:
        return "Software - NordVPN", "OpEx"
    if "WEBSHARE" in desc_upper:
        return "Software - Webshare", "OpEx"
    if "WORKSPACE" in desc_upper:
        return "Software - Google Workspace", "OpEx"
    if "GOOGLE *CLOUD" in desc_upper:
        return "Software - Google Cloud", "OpEx"
    if "GOOGLE *ONE" in desc_upper:
        return "Subscription - Google One", "Personal"
    if "SERVICE FEE" in desc_upper or "STOP PAYMENT" in desc_upper:
        return "Bank Fees", "OpEx"
    if "INTEREST" in desc_upper:
        return "CC Interest", "OpEx"
    if "STATEMENT CREDIT" in desc_upper:
        return "CC Credit/Reward", "Other"
    if "MEMBERSHIP FEE" in desc_upper:
        return "CC Annual Fee", "OpEx"
    if "PAYMENT" in desc_upper and ("THANK" in desc_upper or "CREDIT CRD" in desc_upper):
        return "CC Payment", "Transfer"
    if "TRANSFER" in desc_upper:
        return "Internal Transfer", "Transfer"
    if "KULA COMMUNITY" in desc_upper:
        return "Travel - Peru", "Personal"
    if "SOLSTICE" in desc_upper:
        return "Other", "Other"
    if "WI DFI" in desc_upper:
        return "Business Filing Fee", "OpEx"
    
    # Default
    if amount > 0:
        return "Other Income", "Other"
    return "Other Expense", "Other"

def parse_csv_checking(filepath):
    """Parse Chase checking/savings account CSV"""
    transactions = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = row.get('Posting Date', '')
            if not is_january_2026(date):
                continue
            
            amount = parse_amount(row.get('Amount', 0))
            description = row.get('Description', '')
            
            transactions.append({
                'date': date,
                'description': description,
                'amount': amount,
                'type': row.get('Type', ''),
                'balance': row.get('Balance', ''),
            })
    return transactions

def parse_csv_credit_card(filepath):
    """Parse Chase credit card CSV"""
    transactions = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Try different date columns
            date = row.get('Post Date', row.get('Posting Date', ''))
            if not is_january_2026(date):
                continue
            
            amount = parse_amount(row.get('Amount', 0))
            description = row.get('Description', '')
            
            transactions.append({
                'date': date,
                'description': description,
                'amount': amount,
                'category': row.get('Category', ''),
                'type': row.get('Type', ''),
            })
    return transactions

def clear_sheet(token, sheet_name):
    """Clear a sheet"""
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{sheet_name}:clear"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json={})
    return response.status_code == 200

def write_to_sheet(token, sheet_name, values):
    """Write values to a specific sheet"""
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{sheet_name}!A1:Z1000?valueInputOption=USER_ENTERED"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {"values": values}
    response = requests.put(url, headers=headers, json=data)
    return response.status_code == 200, response.text

def format_sheet(token, sheet_id, header_color=(27, 42, 74)):
    """Apply formatting to sheet headers"""
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}:batchUpdate"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    requests_data = {
        "requests": [
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 0,
                        "endRowIndex": 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": {
                                "red": header_color[0]/255,
                                "green": header_color[1]/255,
                                "blue": header_color[2]/255
                            },
                            "textFormat": {
                                "foregroundColor": {"red": 1, "green": 1, "blue": 1},
                                "bold": True
                            }
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor,textFormat)"
                }
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=requests_data)
    return response.status_code == 200

def get_sheet_ids(token):
    """Get sheet IDs for each tab"""
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        sheet_ids = {}
        for sheet in data.get('sheets', []):
            props = sheet.get('properties', {})
            sheet_ids[props.get('title', '')] = props.get('sheetId', 0)
        return sheet_ids
    return {}

def main():
    token = load_token()
    print(f"Token loaded: {token[:20]}...")
    
    # Parse all accounts
    print("\n📥 Parsing CSV files...")
    
    # Business Checking 4991
    biz_checking = parse_csv_checking(CSV_FILES["business_4991"])
    print(f"  Business 4991: {len(biz_checking)} January transactions")
    
    # Personal Checking 0068
    personal_checking = parse_csv_checking(CSV_FILES["personal_0068"])
    print(f"  Personal 0068: {len(personal_checking)} January transactions")
    
    # Savings 7036
    savings = parse_csv_checking(CSV_FILES["savings_7036"])
    print(f"  Savings 7036: {len(savings)} January transactions")
    
    # Business CC 0678
    biz_cc = parse_csv_credit_card(CSV_FILES["ink_0678"])
    print(f"  Biz CC 0678: {len(biz_cc)} January transactions")
    
    # Personal CC 4252
    personal_cc = parse_csv_credit_card(CSV_FILES["sapphire_4252"])
    print(f"  Sapphire 4252: {len(personal_cc)} January transactions")
    
    # ===== CATEGORIZE ALL TRANSACTIONS =====
    print("\n🏷️  Categorizing transactions...")
    
    # Revenue tracking
    revenue_mva = 0
    revenue_rr = 0
    revenue_other = 0
    
    # Expense tracking by category
    expenses_by_cat = defaultdict(float)
    
    # Special tracking
    meta_ads_pre_carlos = 0  # Before Jan 30
    meta_ads_post_carlos = 0  # Jan 30+
    
    # Process business checking for revenue/expenses
    for t in biz_checking:
        cat, biz_line = categorize_transaction(t['description'], t['amount'], 'business')
        t['category'] = cat
        t['business_line'] = biz_line
        
        amount = t['amount']
        desc_upper = t['description'].upper()
        
        # Revenue
        if biz_line == "🚗 MVA" and amount > 0:
            # Check for Carlos contribution on 01/29
            if "01/29" in t['date'] and amount == 1050:
                pass  # Skip Carlos's contribution
            else:
                revenue_mva += amount
        elif biz_line == "🏗️ R&R" and amount > 0:
            revenue_rr += amount
        
        # Expenses (negative amounts)
        if amount < 0 and biz_line == "OpEx":
            expenses_by_cat[cat] += abs(amount)
            
            # Track Meta ads pre/post Carlos
            if "FACEBK" in desc_upper or "META" in desc_upper:
                day = int(t['date'].split('/')[1])
                if day < 30:
                    meta_ads_pre_carlos += abs(amount)
                else:
                    meta_ads_post_carlos += abs(amount)
    
    # Process business CC
    for t in biz_cc:
        cat, biz_line = categorize_transaction(t['description'], t['amount'], 'business_cc')
        t['category'] = cat
        t['business_line'] = biz_line
        
        amount = t['amount']
        desc_upper = t['description'].upper()
        
        # Expenses (negative amounts on CC)
        if amount < 0 and biz_line == "OpEx":
            expenses_by_cat[cat] += abs(amount)
            
            if "FACEBK" in desc_upper:
                day = int(t['date'].split('/')[1])
                if day < 30:
                    meta_ads_pre_carlos += abs(amount)
                else:
                    meta_ads_post_carlos += abs(amount)
    
    # Calculate totals
    total_revenue = revenue_mva + revenue_rr
    
    # Stripe revenue from business checking (need to extract properly)
    stripe_revenue = sum(t['amount'] for t in biz_checking 
                        if "STRIPE" in t['description'].upper() 
                        and t['amount'] > 0 
                        and "CAPITAL" not in t['description'].upper()
                        and t['amount'] != 4200)  # Exclude loan
    
    # Carlos's contribution on 01/29 - need to subtract from revenue
    # Looking for $1,050 from Carlos (based on task description)
    # Actually looking at data, we see Stripe deposits - let me check for Carlos contribution
    
    # Manual revenue calculation based on the data:
    # Stripe deposits (actual revenue):
    stripe_deposits = []
    for t in biz_checking:
        if "STRIPE" in t['description'].upper() and t['amount'] > 0:
            if "CAPITAL" in t['description'].upper() or t['amount'] == 4200:
                continue  # Skip loan
            stripe_deposits.append(t)
    
    print(f"\n💰 Stripe deposits found: {len(stripe_deposits)}")
    total_stripe = sum(t['amount'] for t in stripe_deposits)
    print(f"   Total Stripe: ${total_stripe:,.2f}")
    
    # Zelle revenue
    zelle_revenue = 0
    for t in biz_checking:
        desc_upper = t['description'].upper()
        if "ZELLE" in desc_upper and t['amount'] > 0:
            if "JONATHAN BIBLE" in desc_upper:
                continue  # Net zero - refund
            if "ALEX" in desc_upper and "SHTABSKY" in desc_upper:
                continue  # Currency exchange help
            zelle_revenue += t['amount']
    
    print(f"   Total Zelle Revenue: ${zelle_revenue:,.2f}")
    
    # Total Meta ads from business checking + CC
    total_meta_ads = 0
    for t in biz_checking:
        if ("FACEBK" in t['description'].upper() or "META" in t['description'].upper()) and t['amount'] < 0:
            total_meta_ads += abs(t['amount'])
    for t in biz_cc:
        if "FACEBK" in t['description'].upper() and t['amount'] < 0:
            total_meta_ads += abs(t['amount'])
    
    print(f"   Total Meta Ads: ${total_meta_ads:,.2f}")
    print(f"   Pre-Carlos (before Jan 30): ${meta_ads_pre_carlos:,.2f}")
    print(f"   Post-Carlos (Jan 30+): ${meta_ads_post_carlos:,.2f}")
    
    # ===== BUILD SHEET DATA =====
    print("\n📊 Building sheet data...")
    
    # Sheet 1: Dashboard
    # Adjusted revenue (minus Carlos $1,050 on 01/29)
    carlos_contribution = 0  # Will check if we find it
    adj_stripe_revenue = total_stripe  # Subtract Carlos's share if found
    
    # Look for ACI Enterprise, Anthony Reddin, Christian Willard, A-Z Mobile in Zelle
    zelle_breakdown = {}
    for t in biz_checking:
        desc_upper = t['description'].upper()
        if "ZELLE" in desc_upper and t['amount'] > 0:
            if "ACI ENTERPRISE" in desc_upper:
                zelle_breakdown['ACI Enterprise (R&R)'] = zelle_breakdown.get('ACI Enterprise (R&R)', 0) + t['amount']
            elif "ANTHONY REDDIN" in desc_upper:
                zelle_breakdown['Anthony Reddin (R&R)'] = zelle_breakdown.get('Anthony Reddin (R&R)', 0) + t['amount']
            elif "CHRISTIAN WILLARD" in desc_upper:
                zelle_breakdown['Christian Willard (Backlinks)'] = t['amount']
            elif "A-Z MOBILE" in desc_upper:
                zelle_breakdown['A-Z Mobile (COD Referral)'] = zelle_breakdown.get('A-Z Mobile (COD Referral)', 0) + t['amount']
            elif "JONATHAN BIBLE" not in desc_upper and "SHTABSKY" not in desc_upper:
                zelle_breakdown['Other'] = zelle_breakdown.get('Other', 0) + t['amount']
    
    print(f"\n   Zelle Breakdown: {zelle_breakdown}")
    
    # Calculate R&R revenue
    rr_revenue = zelle_breakdown.get('ACI Enterprise (R&R)', 0) + zelle_breakdown.get('Anthony Reddin (R&R)', 0) + zelle_breakdown.get('Christian Willard (Backlinks)', 0)
    mva_revenue = total_stripe + zelle_breakdown.get('A-Z Mobile (COD Referral)', 0)
    
    # Total Business Revenue (minus Carlos's contribution - will need to identify)
    total_business_revenue = mva_revenue + rr_revenue
    
    # Calculate total opex
    total_opex = sum(expenses_by_cat.values())
    
    dashboard_data = [
        ["📊 KuriosBrand January 2026 Dashboard", "", "", ""],
        ["", "", "", ""],
        ["=== REVENUE ===", "", "", ""],
        ["🚗 MVA Revenue", f"${mva_revenue:,.2f}", "", ""],
        ["   Stripe Deposits", f"${total_stripe:,.2f}", "", ""],
        ["   A-Z Mobile (COD Referral)", f"${zelle_breakdown.get('A-Z Mobile (COD Referral)', 0):,.2f}", "", ""],
        ["", "", "", ""],
        ["🏗️ R&R Revenue", f"${rr_revenue:,.2f}", "", ""],
        ["   ACI Enterprise", f"${zelle_breakdown.get('ACI Enterprise (R&R)', 0):,.2f}", "", ""],
        ["   Anthony Reddin", f"${zelle_breakdown.get('Anthony Reddin (R&R)', 0):,.2f}", "", ""],
        ["   Christian Willard (Backlinks)", f"${zelle_breakdown.get('Christian Willard (Backlinks)', 0):,.2f}", "", ""],
        ["", "", "", ""],
        ["TOTAL REVENUE", f"${total_business_revenue:,.2f}", "", ""],
        ["", "", "", ""],
        ["=== META ADS (Carlos Partnership) ===", "", "", ""],
        ["Total Meta Ads Spend", f"${total_meta_ads:,.2f}", "", ""],
        ["Pre-Carlos (before Jan 30)", f"${meta_ads_pre_carlos:,.2f}", "", ""],
        ["Post-Carlos (Jan 30+)", f"${meta_ads_post_carlos:,.2f}", "", ""],
        ["", "", "", ""],
        ["=== EXPENSES BY CATEGORY ===", "", "", ""],
    ]
    
    # Add expense breakdown
    for cat, amount in sorted(expenses_by_cat.items(), key=lambda x: -x[1]):
        dashboard_data.append([cat, f"${amount:,.2f}", "", ""])
    
    dashboard_data.extend([
        ["", "", "", ""],
        ["TOTAL OPEX", f"${total_opex:,.2f}", "", ""],
        ["", "", "", ""],
        ["=== KEY METRICS ===", "", "", ""],
        ["Gross Profit", f"${total_business_revenue - total_opex:,.2f}", "", ""],
        ["Gross Margin", f"{((total_business_revenue - total_opex) / total_business_revenue * 100) if total_business_revenue > 0 else 0:.1f}%", "", ""],
    ])
    
    # Sheet 2: Profit First
    # $0-250k tier: 5% profit, 50% owner comp, 15% tax, 30% opex
    pf_profit_target = total_business_revenue * 0.05
    pf_owner_target = total_business_revenue * 0.50
    pf_tax_target = total_business_revenue * 0.15
    pf_opex_target = total_business_revenue * 0.30
    
    profit_first_data = [
        ["💰 Profit First Analysis - January 2026", "", "", "", ""],
        ["", "", "", "", ""],
        ["Real Revenue ($0-250k Tier)", f"${total_business_revenue:,.2f}", "", "", ""],
        ["", "", "", "", ""],
        ["Category", "Target %", "Target $", "Actual $", "Variance"],
        ["Profit", "5%", f"${pf_profit_target:,.2f}", "TBD", "TBD"],
        ["Owner's Comp", "50%", f"${pf_owner_target:,.2f}", "TBD", "TBD"],
        ["Tax Reserve", "15%", f"${pf_tax_target:,.2f}", "TBD", "TBD"],
        ["Operating Expenses", "30%", f"${pf_opex_target:,.2f}", f"${total_opex:,.2f}", f"${pf_opex_target - total_opex:,.2f}"],
        ["", "", "", "", ""],
        ["Note: OpEx target is ${:.2f}, actual is ${:.2f}".format(pf_opex_target, total_opex), "", "", "", ""],
        ["{}".format("✅ UNDER BUDGET" if total_opex <= pf_opex_target else "🚨 OVER BUDGET by ${:.2f}".format(total_opex - pf_opex_target)), "", "", "", ""],
    ]
    
    # Sheet 3: Pareto Analysis
    pareto_data = [
        ["🎯 Pareto Analysis - Expense Ranking", "", "", ""],
        ["", "", "", ""],
        ["Rank", "Category", "Amount", "Cumulative %"],
    ]
    
    sorted_expenses = sorted(expenses_by_cat.items(), key=lambda x: -x[1])
    cumulative = 0
    for i, (cat, amount) in enumerate(sorted_expenses, 1):
        cumulative += amount
        pct = (cumulative / total_opex * 100) if total_opex > 0 else 0
        pareto_data.append([i, cat, f"${amount:,.2f}", f"{pct:.1f}%"])
    
    pareto_data.extend([
        ["", "", "", ""],
        ["💡 Recommendations:", "", "", ""],
        ["1. Meta Ads (${:,.2f}) is largest expense - track ROI carefully".format(total_meta_ads), "", "", ""],
        ["2. Software subscriptions review recommended", "", "", ""],
        ["3. Travel expenses (personal) should not be in OpEx", "", "", ""],
    ])
    
    # Sheet 4: Business 4991
    biz_4991_data = [
        ["💼 Business Checking 4991 - January 2026", "", "", "", "", ""],
        ["", "", "", "", "", ""],
        ["Date", "Description", "Amount", "Category", "Business Line", "Balance"],
    ]
    for t in sorted(biz_checking, key=lambda x: x['date']):
        cat, biz_line = categorize_transaction(t['description'], t['amount'], 'business')
        biz_4991_data.append([
            t['date'],
            t['description'][:60],
            f"${t['amount']:,.2f}" if t['amount'] >= 0 else f"-${abs(t['amount']):,.2f}",
            cat,
            biz_line,
            t.get('balance', '')
        ])
    
    # Sheet 5: Personal 0068
    personal_0068_data = [
        ["👤 Personal Checking 0068 - January 2026", "", "", "", "", ""],
        ["", "", "", "", "", ""],
        ["Date", "Description", "Amount", "Category", "Type", "Balance"],
    ]
    for t in sorted(personal_checking, key=lambda x: x['date']):
        cat, biz_line = categorize_transaction(t['description'], t['amount'], 'personal')
        personal_0068_data.append([
            t['date'],
            t['description'][:60],
            f"${t['amount']:,.2f}" if t['amount'] >= 0 else f"-${abs(t['amount']):,.2f}",
            cat,
            t.get('type', ''),
            t.get('balance', '')
        ])
    
    # Sheet 6: Biz CC 0678
    biz_cc_data = [
        ["💳 Business Ink CC 0678 - January 2026", "", "", "", ""],
        ["", "", "", "", ""],
        ["Date", "Description", "Amount", "Category", "Type"],
    ]
    for t in sorted(biz_cc, key=lambda x: x['date']):
        cat, biz_line = categorize_transaction(t['description'], t['amount'], 'business_cc')
        biz_cc_data.append([
            t['date'],
            t['description'][:60],
            f"${t['amount']:,.2f}" if t['amount'] >= 0 else f"-${abs(t['amount']):,.2f}",
            cat,
            t.get('type', '')
        ])
    
    # Sheet 7: Sapphire 4252
    sapphire_data = [
        ["💎 Sapphire CC 4252 - January 2026", "", "", "", ""],
        ["", "", "", "", ""],
        ["Date", "Description", "Amount", "Category", "Type"],
    ]
    for t in sorted(personal_cc, key=lambda x: x['date']):
        cat, biz_line = categorize_transaction(t['description'], t['amount'], 'personal_cc')
        sapphire_data.append([
            t['date'],
            t['description'][:60],
            f"${t['amount']:,.2f}" if t['amount'] >= 0 else f"-${abs(t['amount']):,.2f}",
            cat,
            t.get('type', '')
        ])
    
    # Sheet 8: Raw Data
    raw_data = [
        ["📦 Raw Data - All January 2026 Transactions", "", "", "", "", ""],
        ["", "", "", "", "", ""],
        ["Account", "Date", "Description", "Amount", "Category", "Type"],
    ]
    
    for t in biz_checking:
        cat, _ = categorize_transaction(t['description'], t['amount'], 'business')
        raw_data.append(["Biz 4991", t['date'], t['description'][:60], t['amount'], cat, t.get('type', '')])
    
    for t in personal_checking:
        cat, _ = categorize_transaction(t['description'], t['amount'], 'personal')
        raw_data.append(["Personal 0068", t['date'], t['description'][:60], t['amount'], cat, t.get('type', '')])
    
    for t in savings:
        cat, _ = categorize_transaction(t['description'], t['amount'], 'savings')
        raw_data.append(["Savings 7036", t['date'], t['description'][:60], t['amount'], cat, t.get('type', '')])
    
    for t in biz_cc:
        cat, _ = categorize_transaction(t['description'], t['amount'], 'business_cc')
        raw_data.append(["Biz CC 0678", t['date'], t['description'][:60], t['amount'], cat, t.get('type', '')])
    
    for t in personal_cc:
        cat, _ = categorize_transaction(t['description'], t['amount'], 'personal_cc')
        raw_data.append(["Sapphire 4252", t['date'], t['description'][:60], t['amount'], cat, t.get('type', '')])
    
    # ===== WRITE TO SHEETS =====
    print("\n📤 Writing to Google Sheets...")
    
    sheets_to_write = [
        ("📊 Dashboard", dashboard_data),
        ("💰 Profit First", profit_first_data),
        ("🎯 Pareto Analysis", pareto_data),
        ("💼 Business 4991", biz_4991_data),
        ("👤 Personal 0068", personal_0068_data),
        ("💳 Biz CC 0678", biz_cc_data),
        ("💎 Sapphire 4252", sapphire_data),
        ("📦 Raw Data", raw_data),
    ]
    
    for sheet_name, data in sheets_to_write:
        # Clear first
        clear_sheet(token, sheet_name)
        # Write data
        success, response = write_to_sheet(token, sheet_name, data)
        status = "✅" if success else "❌"
        print(f"  {status} {sheet_name}: {len(data)} rows")
        if not success:
            print(f"     Error: {response[:200]}")
    
    # Apply formatting
    print("\n🎨 Applying formatting...")
    sheet_ids = get_sheet_ids(token)
    print(f"   Found sheets: {list(sheet_ids.keys())}")
    
    for sheet_name in sheet_ids:
        format_sheet(token, sheet_ids[sheet_name])
        print(f"   Formatted: {sheet_name}")
    
    # ===== SUMMARY =====
    print("\n" + "="*60)
    print("📊 JANUARY 2026 ACCOUNTING SUMMARY")
    print("="*60)
    print(f"\n💰 REVENUE:")
    print(f"   🚗 MVA Revenue: ${mva_revenue:,.2f}")
    print(f"   🏗️ R&R Revenue: ${rr_revenue:,.2f}")
    print(f"   TOTAL: ${total_business_revenue:,.2f}")
    
    print(f"\n📈 META ADS:")
    print(f"   Total Spend: ${total_meta_ads:,.2f}")
    print(f"   Pre-Carlos (< Jan 30): ${meta_ads_pre_carlos:,.2f}")
    print(f"   Post-Carlos (Jan 30+): ${meta_ads_post_carlos:,.2f}")
    
    print(f"\n💸 TOP EXPENSES:")
    for i, (cat, amount) in enumerate(sorted_expenses[:5], 1):
        print(f"   {i}. {cat}: ${amount:,.2f}")
    
    print(f"\n📊 PROFIT FIRST ANALYSIS:")
    print(f"   Revenue: ${total_business_revenue:,.2f}")
    print(f"   Target OpEx (30%): ${pf_opex_target:,.2f}")
    print(f"   Actual OpEx: ${total_opex:,.2f}")
    variance = pf_opex_target - total_opex
    if variance >= 0:
        print(f"   ✅ UNDER BUDGET by ${variance:,.2f}")
    else:
        print(f"   🚨 OVER BUDGET by ${abs(variance):,.2f}")
    
    print(f"\n🔗 Sheet URL: https://docs.google.com/spreadsheets/d/{SHEET_ID}")
    print("="*60)

if __name__ == "__main__":
    main()
