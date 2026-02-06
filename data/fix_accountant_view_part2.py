#!/usr/bin/env python3
"""
Part 2: Update Cash Flow with accurate data, update 1099 Tracking with detailed vendor data,
and do final formatting/verification.
"""

import requests
import json
import csv
import re
from datetime import datetime
from collections import defaultdict

# Auth
def get_token():
    r = requests.post('https://oauth2.googleapis.com/token', data={
        'client_id': '838433184423-1sd6hs0m7m7mrvm63f1sct2ovjhs88ut.apps.googleusercontent.com',
        'client_secret': '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',
        'refresh_token': '1//05PmAu-vBTVrWCgYIARAAGAUSNwF-L9Irl-dM7iPoS4XocG_eO32bhNSfNYM0rfwGMKBi-KwJYCpzpAlXYINO04lXIWVAAHmh0qw',
        'grant_type': 'refresh_token'
    })
    return r.json()['access_token']

TOKEN = get_token()
SHEET_ID = '1vtXJCdbWOskKU-zxEJCOlXBTVhd7vHclWEdWwJgFZ9o'
HEADERS = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}
API_BASE = f'https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}'

# Colors
NAVY = {"red": 0.106, "green": 0.165, "blue": 0.290}
WHITE = {"red": 1.0, "green": 1.0, "blue": 1.0}
LIGHT_GRAY = {"red": 0.953, "green": 0.953, "blue": 0.953}
LIGHT_NAVY = {"red": 0.910, "green": 0.929, "blue": 0.949}

def color_obj(c):
    return {"red": c["red"], "green": c["green"], "blue": c["blue"]}

def batch_update(requests_list):
    body = {"requests": requests_list}
    r = requests.post(f'{API_BASE}:batchUpdate', headers=HEADERS, json=body)
    if r.status_code != 200:
        print(f"ERROR: {r.status_code} - {r.text[:500]}")
        return None
    return r.json()

def update_values(range_str, values, value_input_option='USER_ENTERED'):
    import urllib.parse
    encoded = urllib.parse.quote(range_str)
    body = {"values": values, "majorDimension": "ROWS"}
    r = requests.put(f'{API_BASE}/values/{encoded}?valueInputOption={value_input_option}',
                     headers=HEADERS, json=body)
    if r.status_code != 200:
        print(f"ERROR: {r.status_code} - {r.text[:500]}")
    return r.json() if r.status_code == 200 else None

def get_values(range_str):
    import urllib.parse
    encoded = urllib.parse.quote(range_str)
    r = requests.get(f'{API_BASE}/values/{encoded}', headers=HEADERS)
    return r.json().get('values', []) if r.status_code == 200 else []

def format_section_header_row(sid, row_idx, end_col=8):
    return [
        {"repeatCell": {
            "range": {"sheetId": sid, "startRowIndex": row_idx, "endRowIndex": row_idx + 1,
                      "startColumnIndex": 0, "endColumnIndex": end_col},
            "cell": {"userEnteredFormat": {
                "backgroundColor": color_obj(NAVY),
                "textFormat": {"foregroundColor": color_obj(WHITE), "fontFamily": "Arial", "fontSize": 14, "bold": True}
            }},
            "fields": "userEnteredFormat.backgroundColor,userEnteredFormat.textFormat"
        }},
        {"updateDimensionProperties": {
            "range": {"sheetId": sid, "dimension": "ROWS", "startIndex": row_idx, "endIndex": row_idx + 1},
            "properties": {"pixelSize": 30}, "fields": "pixelSize"
        }}
    ]

def format_column_header_row(sid, row_idx, end_col=8):
    return [
        {"repeatCell": {
            "range": {"sheetId": sid, "startRowIndex": row_idx, "endRowIndex": row_idx + 1,
                      "startColumnIndex": 0, "endColumnIndex": end_col},
            "cell": {"userEnteredFormat": {
                "backgroundColor": color_obj(LIGHT_GRAY),
                "textFormat": {"fontFamily": "Arial", "fontSize": 11, "bold": True}
            }},
            "fields": "userEnteredFormat.backgroundColor,userEnteredFormat.textFormat"
        }},
        {"updateDimensionProperties": {
            "range": {"sheetId": sid, "dimension": "ROWS", "startIndex": row_idx, "endIndex": row_idx + 1},
            "properties": {"pixelSize": 30}, "fields": "pixelSize"
        }}
    ]

def format_total_row(sid, row_idx, end_col=8):
    return [{"repeatCell": {
        "range": {"sheetId": sid, "startRowIndex": row_idx, "endRowIndex": row_idx + 1,
                  "startColumnIndex": 0, "endColumnIndex": end_col},
        "cell": {"userEnteredFormat": {
            "backgroundColor": color_obj(LIGHT_NAVY),
            "textFormat": {"fontFamily": "Arial", "fontSize": 11, "bold": True}
        }},
        "fields": "userEnteredFormat.backgroundColor,userEnteredFormat.textFormat"
    }}]

def format_category_header_row(sid, row_idx, end_col=8):
    return [{"repeatCell": {
        "range": {"sheetId": sid, "startRowIndex": row_idx, "endRowIndex": row_idx + 1,
                  "startColumnIndex": 0, "endColumnIndex": end_col},
        "cell": {"userEnteredFormat": {
            "backgroundColor": color_obj(NAVY),
            "textFormat": {"foregroundColor": color_obj(WHITE), "fontFamily": "Arial", "fontSize": 11, "bold": True}
        }},
        "fields": "userEnteredFormat.backgroundColor,userEnteredFormat.textFormat"
    }}]


# ============================================================
# UPDATED CASH FLOW with accurate owner draw/contribution data
# ============================================================
def update_cash_flow():
    """Rewrite Cash Flow with accurate data."""
    
    # Net income from verified income statements
    net_income = {2024: -2567.10, 2025: 43239.89, 2026: -169.92}
    
    # Owner draws from CSV analysis
    owner_draws = {2024: -5832.22, 2025: -51340.22, 2026: -4684.00}
    owner_contribs = {2024: 8550.06, 2025: 4100.00, 2026: 3255.00}
    
    # Stripe Capital: $4,200 loan in Jan 2026
    # Repayment is 20% of Stripe deposits - automatically deducted before transfer
    # So repayments don't show as a separate transaction in checking
    loan_proceeds = {2024: 0, 2025: 0, 2026: 4200.00}
    
    # Loan repayments from the Income Statements (Loan Repayment line)
    loan_repayments = {2024: -99.00, 2025: -2563.25, 2026: -227.67}
    
    rows = [
        ["KuriosBrand LLC — Statement of Cash Flows"],
        ["For the Years Ended December 31, 2024, 2025, and 2026 YTD"],
        [""],
        ["", "2024", "2025", "2026 YTD"],
    ]
    
    for year in [2024, 2025, 2026]:
        ni = net_income[year]
        op_total = ni  # Cash basis = net income IS operating cash
        
        inv_total = 0  # No significant investing activities
        
        draws = owner_draws[year]
        contribs = owner_contribs[year]
        proceeds = loan_proceeds[year]
        repay = loan_repayments[year]
        fin_total = draws + contribs + proceeds + repay
        
        net_change = op_total + inv_total + fin_total
        
        if year == 2024:
            rows.extend([
                ["OPERATING ACTIVITIES"],
                ["  Net Income", ni, net_income[2025], net_income[2026]],
                ["  Adjustments to reconcile net income to net cash:"],
                ["    (Cash basis accounting - no non-cash adjustments)", "", "", ""],
                ["NET CASH FROM OPERATING ACTIVITIES", net_income[2024], net_income[2025], net_income[2026]],
                [""],
                ["INVESTING ACTIVITIES"],
                ["  Capital Expenditures / Equipment", 0, 0, 0],
                ["NET CASH FROM INVESTING ACTIVITIES", 0, 0, 0],
                [""],
                ["FINANCING ACTIVITIES"],
                ["  Loan Proceeds (Stripe Capital)", loan_proceeds[2024], loan_proceeds[2025], loan_proceeds[2026]],
                ["  Loan Repayments", loan_repayments[2024], loan_repayments[2025], loan_repayments[2026]],
                ["  Owner Draws (Transfers to Personal)", owner_draws[2024], owner_draws[2025], owner_draws[2026]],
                ["  Owner Contributions (Transfers from Personal)", owner_contribs[2024], owner_contribs[2025], owner_contribs[2026]],
                ["NET CASH FROM FINANCING ACTIVITIES", 
                    owner_draws[2024] + owner_contribs[2024] + loan_proceeds[2024] + loan_repayments[2024],
                    owner_draws[2025] + owner_contribs[2025] + loan_proceeds[2025] + loan_repayments[2025],
                    owner_draws[2026] + owner_contribs[2026] + loan_proceeds[2026] + loan_repayments[2026]],
                [""],
                ["NET CHANGE IN CASH",
                    net_income[2024] + owner_draws[2024] + owner_contribs[2024] + loan_proceeds[2024] + loan_repayments[2024],
                    net_income[2025] + owner_draws[2025] + owner_contribs[2025] + loan_proceeds[2025] + loan_repayments[2025],
                    net_income[2026] + owner_draws[2026] + owner_contribs[2026] + loan_proceeds[2026] + loan_repayments[2026]],
                [""],
                ["Notes:"],
                ["1. Cash basis accounting: operating cash flow equals net income (no accrual adjustments)."],
                ["2. Stripe Capital loan of $4,200 disbursed January 23, 2026 (total repayment: $5,035 at 19.9%)."],
                ["3. Loan repayments include a previous loan fully repaid in 2024 and early 2025, then current Stripe Capital."],
                ["4. Owner draws represent net transfers from business checking (4991) to personal checking (0068)."],
                ["5. Owner contributions represent transfers from personal to business during cash-tight periods."],
            ])
            break  # We only need to write once (data for all 3 years in the same rows)
    
    return rows

# ============================================================
# UPDATED 1099 TRACKING with detailed vendor analysis
# ============================================================
def update_1099_tracking():
    """Build comprehensive 1099 tracking."""
    
    biz = []
    with open('chase-exports/business-4991-alltime.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            biz.append(row)
    
    # Identify contractor payments by vendor
    vendor_payments = defaultdict(lambda: {'2024': 0, '2025': 0, '2026': 0, 'details': []})
    
    for row in biz:
        desc = row.get('Description', '')
        amt = float(row.get('Amount', 0))
        dt_str = row.get('Posting Date', '')
        
        if amt >= 0:
            continue
        
        try:
            dt = datetime.strptime(dt_str.strip(), '%m/%d/%Y')
            year = str(dt.year)
        except:
            continue
        
        desc_upper = desc.upper()
        desc_clean = re.sub(r'\s+', ' ', desc.strip())
        vendor = None
        payment_method = ''
        
        # Zelle payments
        if 'ZELLE' in desc_upper:
            m = re.search(r'Zelle\s+payment\s+to\s+(.+?)\s+(?:JPM|25\d|24\d|26\d|\d{10})', desc_clean, re.IGNORECASE)
            if m:
                vendor = m.group(1).strip()
            payment_method = 'Zelle'
        
        # Wise transfers (contractor payments)
        elif 'WISE' in desc_upper:
            vendor = 'Wise Transfer (International Contractor)'
            payment_method = 'Wise'
        
        # PayPal with named recipients  
        elif 'PAYPAL' in desc_upper:
            # Extract specific payee names
            m = re.search(r'ORIG CO NAME:([A-Z ]+?)(?:\s+ORIG)', desc_clean)
            if m:
                name = m.group(1).strip()
                if name not in ('PAYPAL',):
                    vendor = f'PayPal - {name.title()}'
            else:
                # Generic PayPal
                if 'IOTSOLUTION' in desc_upper:
                    vendor = 'PayPal - IoT Solution'
                else:
                    vendor = 'PayPal (Various)'
            payment_method = 'PayPal'
        
        if vendor:
            # Skip self-transfers
            if any(skip in vendor.upper() for skip in ['MARK GUNDRUM', 'WELLS FARGO BIZ']):
                continue
            
            vendor_payments[vendor][year] += abs(amt)
            vendor_payments[vendor]['details'].append({
                'date': dt.strftime('%m/%d/%Y'),
                'amount': abs(amt),
                'method': payment_method,
                'desc': desc_clean[:80]
            })
    
    # Build the sheet
    rows = [
        ["KuriosBrand LLC — 1099-NEC Tracking"],
        ["Vendors/Contractors Paid >= $600 in Any Calendar Year"],
        [""],
        ["Vendor / Contractor", "Payment Method", "2024 Total", "2025 Total", "2026 YTD", "Max Year Total", "1099 Required?", "TIN on File?", "Status"],
    ]
    
    # Sort by total across all years
    sorted_vendors = sorted(vendor_payments.items(), 
                           key=lambda x: x[1]['2024'] + x[1]['2025'] + x[1]['2026'], 
                           reverse=True)
    
    qualifying_count = 0
    review_count = 0
    
    for vendor, data in sorted_vendors:
        y24 = data['2024']
        y25 = data['2025']
        y26 = data['2026']
        max_year = max(y24, y25, y26)
        
        if max_year >= 600:
            status = "1099 REQUIRED"
            qualifying_count += 1
        elif max_year >= 400:
            status = "REVIEW - Approaching Threshold"
            review_count += 1
        else:
            status = "Below Threshold"
        
        required = "Yes" if max_year >= 600 else "Review" if max_year >= 400 else "No"
        
        # Determine payment method from first detail
        method = data['details'][0]['method'] if data['details'] else ''
        
        rows.append([
            vendor,
            method,
            y24 if y24 > 0 else "",
            y25 if y25 > 0 else "",
            y26 if y26 > 0 else "",
            max_year,
            required,
            "No",
            status
        ])
    
    rows.append([""])
    rows.append([f"SUMMARY: {qualifying_count} vendors require 1099-NEC filing, {review_count} approaching threshold"])
    rows.append([""])
    rows.append([""])
    
    # Detailed payment log for qualifying vendors
    rows.append(["DETAILED PAYMENT LOG — Qualifying Vendors (>=$600 in any year)"])
    rows.append(["Vendor", "Date", "Amount", "Method", "Description"])
    
    for vendor, data in sorted_vendors:
        max_year = max(data['2024'], data['2025'], data['2026'])
        if max_year >= 600:
            for txn in sorted(data['details'], key=lambda x: x['date']):
                rows.append([
                    vendor,
                    txn['date'],
                    txn['amount'],
                    txn['method'],
                    txn['desc'][:70]
                ])
    
    rows.append([""])
    rows.append(["NOTES & COMPLIANCE REQUIREMENTS"])
    rows.append(["1. Form 1099-NEC is required for non-corporate contractors paid >= $600 in a calendar year."])
    rows.append(["2. Corporations (C-Corp, S-Corp) are generally EXEMPT from 1099 reporting."])
    rows.append(["3. Wise transfers are international contractor payments - verify recipient entity type."])
    rows.append(["4. PayPal payments >= $600 may be reported by PayPal via 1099-K (verify to avoid double reporting)."])
    rows.append(["5. Request W-9 from all domestic contractors BEFORE first payment."])
    rows.append(["6. International contractors: Request W-8BEN instead of W-9."])
    rows.append(["7. Filing deadline: January 31 of the following year (e.g., 2025 1099s due Jan 31, 2026)."])
    rows.append(["8. 'Nil Ridge' and 'Oscar Cruz' Zelle payments should be reviewed to determine if individual or business."])
    
    return rows

# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 60)
    print("PART 2: UPDATING CASH FLOW & 1099 TRACKING")
    print("=" * 60)
    
    # Step 1: Update Cash Flow
    print("\n--- Updating Cash Flow Statement ---")
    cf_rows = update_cash_flow()
    result = update_values("'Cash Flow Statement'!A1:D30", cf_rows)
    print(f"  Cash Flow data: {'OK' if result else 'FAILED'} ({len(cf_rows)} rows)")
    
    # Format Cash Flow (re-apply since we rewrote data)
    cf_reqs = []
    sid = 100
    
    # Title rows
    cf_reqs.extend(format_section_header_row(sid, 0, 5))
    cf_reqs.extend(format_section_header_row(sid, 1, 5))
    
    # Column header
    cf_reqs.extend(format_column_header_row(sid, 3, 5))
    
    # Section headers (OPERATING, INVESTING, FINANCING)
    cf_reqs.extend(format_category_header_row(sid, 4, 5))   # OPERATING ACTIVITIES
    cf_reqs.extend(format_category_header_row(sid, 10, 5))  # INVESTING ACTIVITIES
    cf_reqs.extend(format_category_header_row(sid, 14, 5))  # FINANCING ACTIVITIES
    
    # Total rows
    cf_reqs.extend(format_total_row(sid, 8, 5))   # NET CASH FROM OPERATING
    cf_reqs.extend(format_total_row(sid, 12, 5))   # NET CASH FROM INVESTING
    cf_reqs.extend(format_total_row(sid, 19, 5))  # NET CASH FROM FINANCING
    cf_reqs.extend(format_total_row(sid, 21, 5))  # NET CHANGE IN CASH
    
    # Currency format for data cells
    cf_reqs.append({
        "repeatCell": {
            "range": {"sheetId": sid, "startRowIndex": 4, "endRowIndex": 22,
                      "startColumnIndex": 1, "endColumnIndex": 4},
            "cell": {"userEnteredFormat": {
                "numberFormat": {"type": "NUMBER", "pattern": "$#,##0.00;[Red]($#,##0.00)"}
            }},
            "fields": "userEnteredFormat.numberFormat"
        }
    })
    
    # Global font
    cf_reqs.append({
        "repeatCell": {
            "range": {"sheetId": sid, "startRowIndex": 0, "endRowIndex": 30,
                      "startColumnIndex": 0, "endColumnIndex": 5},
            "cell": {"userEnteredFormat": {"textFormat": {"fontFamily": "Arial", "fontSize": 10}}},
            "fields": "userEnteredFormat.textFormat.fontFamily,userEnteredFormat.textFormat.fontSize"
        }
    })
    
    # Default row heights
    cf_reqs.append({
        "updateDimensionProperties": {
            "range": {"sheetId": sid, "dimension": "ROWS", "startIndex": 0, "endIndex": 30},
            "properties": {"pixelSize": 21}, "fields": "pixelSize"
        }
    })
    
    # Column widths
    cf_reqs.append({
        "updateDimensionProperties": {
            "range": {"sheetId": sid, "dimension": "COLUMNS", "startIndex": 0, "endIndex": 1},
            "properties": {"pixelSize": 380}, "fields": "pixelSize"
        }
    })
    for col_idx in range(1, 4):
        cf_reqs.append({
            "updateDimensionProperties": {
                "range": {"sheetId": sid, "dimension": "COLUMNS", "startIndex": col_idx, "endIndex": col_idx + 1},
                "properties": {"pixelSize": 150}, "fields": "pixelSize"
            }
        })
    
    result = batch_update(cf_reqs)
    print(f"  Cash Flow formatting: {'OK' if result else 'FAILED'}")
    
    # Step 2: Update 1099 Tracking
    print("\n--- Updating 1099 Tracking ---")
    
    # First clear existing data
    clear_body = {"ranges": ["'1099 Tracking'!A1:I200"]}
    r = requests.post(f'{API_BASE}/values:batchClear', headers=HEADERS, json=clear_body)
    print(f"  Cleared old data: {r.status_code}")
    
    t1099_rows = update_1099_tracking()
    result = update_values("'1099 Tracking'!A1", t1099_rows)
    print(f"  1099 data: {'OK' if result else 'FAILED'} ({len(t1099_rows)} rows)")
    
    # Format 1099
    t1099_reqs = []
    sid = 102
    
    # Title
    t1099_reqs.extend(format_section_header_row(sid, 0, 9))
    t1099_reqs.extend(format_section_header_row(sid, 1, 9))
    
    # Column header
    t1099_reqs.extend(format_column_header_row(sid, 3, 9))
    
    # Currency format
    t1099_reqs.append({
        "repeatCell": {
            "range": {"sheetId": sid, "startRowIndex": 4, "endRowIndex": 50,
                      "startColumnIndex": 2, "endColumnIndex": 6},
            "cell": {"userEnteredFormat": {
                "numberFormat": {"type": "NUMBER", "pattern": "$#,##0.00;[Red]($#,##0.00)"}
            }},
            "fields": "userEnteredFormat.numberFormat"
        }
    })
    
    # Global font
    t1099_reqs.append({
        "repeatCell": {
            "range": {"sheetId": sid, "startRowIndex": 0, "endRowIndex": len(t1099_rows) + 5,
                      "startColumnIndex": 0, "endColumnIndex": 9},
            "cell": {"userEnteredFormat": {"textFormat": {"fontFamily": "Arial", "fontSize": 10}}},
            "fields": "userEnteredFormat.textFormat.fontFamily,userEnteredFormat.textFormat.fontSize"
        }
    })
    
    # Row heights
    t1099_reqs.append({
        "updateDimensionProperties": {
            "range": {"sheetId": sid, "dimension": "ROWS", "startIndex": 0, "endIndex": len(t1099_rows) + 5},
            "properties": {"pixelSize": 21}, "fields": "pixelSize"
        }
    })
    
    # Column widths
    col_widths = [300, 120, 120, 120, 120, 130, 120, 100, 200]
    for i, w in enumerate(col_widths):
        t1099_reqs.append({
            "updateDimensionProperties": {
                "range": {"sheetId": sid, "dimension": "COLUMNS", "startIndex": i, "endIndex": i + 1},
                "properties": {"pixelSize": w}, "fields": "pixelSize"
            }
        })
    
    # Find and format the "DETAILED PAYMENT LOG" row
    for i, row in enumerate(t1099_rows):
        if row and str(row[0]).startswith('DETAILED PAYMENT LOG'):
            t1099_reqs.extend(format_category_header_row(sid, i, 9))
            if i + 1 < len(t1099_rows):
                t1099_reqs.extend(format_column_header_row(sid, i + 1, 9))
        if row and str(row[0]).startswith('NOTES'):
            t1099_reqs.extend(format_category_header_row(sid, i, 9))
        if row and str(row[0]).startswith('SUMMARY'):
            t1099_reqs.extend(format_total_row(sid, i, 9))
    
    result = batch_update(t1099_reqs)
    print(f"  1099 formatting: {'OK' if result else 'FAILED'}")
    
    # Step 3: Fix General Ledger column widths and formatting
    print("\n--- Fixing General Ledger formatting ---")
    gl_reqs = []
    sid = 101
    
    gl_col_widths = [80, 250, 100, 350, 120, 120, 150]
    for i, w in enumerate(gl_col_widths):
        gl_reqs.append({
            "updateDimensionProperties": {
                "range": {"sheetId": sid, "dimension": "COLUMNS", "startIndex": i, "endIndex": i + 1},
                "properties": {"pixelSize": w}, "fields": "pixelSize"
            }
        })
    
    result = batch_update(gl_reqs)
    print(f"  GL column widths: {'OK' if result else 'FAILED'}")
    
    # Step 4: Fix existing tab column widths where needed
    print("\n--- Fixing existing tab column widths ---")
    width_reqs = []
    
    # Income Statements: Column A should be wider (category names)
    for sid in [7, 2, 3]:  # IS 2024, 2025, 2026
        width_reqs.append({
            "updateDimensionProperties": {
                "range": {"sheetId": sid, "dimension": "COLUMNS", "startIndex": 0, "endIndex": 1},
                "properties": {"pixelSize": 280}, "fields": "pixelSize"
            }
        })
    
    # Summary: Column A wider
    width_reqs.append({
        "updateDimensionProperties": {
            "range": {"sheetId": 0, "dimension": "COLUMNS", "startIndex": 0, "endIndex": 1},
            "properties": {"pixelSize": 300}, "fields": "pixelSize"
        }
    })
    
    result = batch_update(width_reqs)
    print(f"  Column widths: {'OK' if result else 'FAILED'}")
    
    # Step 5: Verify
    print("\n--- VERIFICATION ---")
    
    # Check revenue figures
    for year in [2024, 2025, 2026]:
        data = get_values(f"'Income Statement {year}'!A1:N40")
        for row in data:
            if row and 'TOTAL REVENUE' in str(row[0]):
                total = row[-1] if len(row) > 1 else 'N/A'
                print(f"  IS {year} Total Revenue: {total}")
            if row and 'NET INCOME' in str(row[0]) and 'Margin' not in str(row[0]):
                total = row[-1] if len(row) > 1 else 'N/A'
                print(f"  IS {year} Net Income: {total}")
    
    # Check Cash Flow
    cf_data = get_values("'Cash Flow Statement'!A1:D25")
    for row in cf_data:
        if row and 'NET CHANGE' in str(row[0]).upper():
            print(f"  Cash Flow Net Change: 2024={row[1] if len(row)>1 else 'N/A'}, 2025={row[2] if len(row)>2 else 'N/A'}, 2026={row[3] if len(row)>3 else 'N/A'}")
    
    # Check tab count
    r = requests.get(f'{API_BASE}?fields=sheets.properties.title', headers=HEADERS)
    tabs = [s['properties']['title'] for s in r.json().get('sheets', [])]
    print(f"\n  Total tabs: {len(tabs)}")
    for t in tabs:
        print(f"    - {t}")
    
    print("\n" + "=" * 60)
    print("PART 2 COMPLETE!")
    print("=" * 60)

if __name__ == '__main__':
    main()
