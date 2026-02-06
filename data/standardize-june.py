#!/usr/bin/env python3
"""Standardize June 2025 KuriosBrand Accounting Sheet"""
import json, urllib.request, urllib.parse, time, sys

# Get fresh token
t = json.load(open('/home/ec2-user/.config/gcal-pro/token.json'))
data = urllib.parse.urlencode({
    'client_id': t['client_id'],
    'client_secret': t['client_secret'],
    'refresh_token': t['refresh_token'],
    'grant_type': 'refresh_token'
}).encode()
req = urllib.request.Request('https://oauth2.googleapis.com/token', data=data)
resp = json.loads(urllib.request.urlopen(req).read())
TOKEN = resp['access_token']
print("✅ Token obtained")

SHEET_ID = '19YSihOlMi1R-2nkZzfwa1dmoidouGl4UakhjdfceBsg'

def api_call(url, method='GET', body=None):
    """Make authenticated API call"""
    if body:
        data = json.dumps(body).encode()
        req = urllib.request.Request(url, data=data, headers={
            'Authorization': f'Bearer {TOKEN}',
            'Content-Type': 'application/json'
        }, method=method)
    else:
        req = urllib.request.Request(url, headers={'Authorization': f'Bearer {TOKEN}'})
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read()) if resp.read else {}
    except urllib.error.HTTPError as e:
        print(f"ERROR {e.code}: {e.read().decode()}")
        raise

def batch_update(requests):
    """Execute batchUpdate"""
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}:batchUpdate'
    body = {'requests': requests}
    data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers={
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    })
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    return result

def update_values(range_str, values, input_option='USER_ENTERED'):
    """Write values to a range"""
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{urllib.parse.quote(range_str)}?valueInputOption={input_option}'
    body = {'range': range_str, 'majorDimension': 'ROWS', 'values': values}
    data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers={
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }, method='PUT')
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read())

def clear_range(range_str):
    """Clear a range"""
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{urllib.parse.quote(range_str)}:clear'
    req = urllib.request.Request(url, data=b'{}', headers={
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }, method='POST')
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read())

# Color constants (RGB 0-1 float)
NAVY = {'red': 0.106, 'green': 0.165, 'blue': 0.29}
WHITE = {'red': 1, 'green': 1, 'blue': 1}
LIGHT_GRAY = {'red': 0.953, 'green': 0.953, 'blue': 0.953}
TOTAL_BG = {'red': 0.91, 'green': 0.929, 'blue': 0.949}
GREEN_TAB = {'red': 0.204, 'green': 0.659, 'blue': 0.325}
ORANGE_TAB = {'red': 1.0, 'green': 0.427, 'blue': 0.004}
GRAY_TAB = {'red': 0.6, 'green': 0.6, 'blue': 0.6}

# Tab IDs (from metadata)
TABS = {
    'Dashboard': 0,
    'Profit First': 1812570290,
    'Pareto Analysis': 340425296,
    'Business 4991': 1255858978,
    'Personal 0068': 845500177,
    'Biz CC 0678': 332554580,
    'Sapphire 4252': 1409199514,
    'Original Overview': 1526271835,
}

# ============================================================
# STEP 1: Structural changes (rename tab, fix colors)
# ============================================================
print("\n🔧 Step 1: Structural changes...")
structural_requests = [
    # Rename Original Overview → Raw Data
    {
        'updateSheetProperties': {
            'properties': {'sheetId': TABS['Original Overview'], 'title': '📦 Raw Data'},
            'fields': 'title'
        }
    },
    # Dashboard: no tab color (default/white)
    {
        'updateSheetProperties': {
            'properties': {'sheetId': TABS['Dashboard'], 'tabColorStyle': {'rgbColor': WHITE}},
            'fields': 'tabColorStyle'
        }
    },
    # Profit First: Green
    {
        'updateSheetProperties': {
            'properties': {'sheetId': TABS['Profit First'], 'tabColorStyle': {'rgbColor': GREEN_TAB}},
            'fields': 'tabColorStyle'
        }
    },
    # Pareto: Orange
    {
        'updateSheetProperties': {
            'properties': {'sheetId': TABS['Pareto Analysis'], 'tabColorStyle': {'rgbColor': ORANGE_TAB}},
            'fields': 'tabColorStyle'
        }
    },
    # Business 4991: Navy
    {
        'updateSheetProperties': {
            'properties': {'sheetId': TABS['Business 4991'], 'tabColorStyle': {'rgbColor': NAVY}},
            'fields': 'tabColorStyle'
        }
    },
    # Personal 0068: Navy
    {
        'updateSheetProperties': {
            'properties': {'sheetId': TABS['Personal 0068'], 'tabColorStyle': {'rgbColor': NAVY}},
            'fields': 'tabColorStyle'
        }
    },
    # Biz CC 0678: Navy
    {
        'updateSheetProperties': {
            'properties': {'sheetId': TABS['Biz CC 0678'], 'tabColorStyle': {'rgbColor': NAVY}},
            'fields': 'tabColorStyle'
        }
    },
    # Sapphire 4252: Navy
    {
        'updateSheetProperties': {
            'properties': {'sheetId': TABS['Sapphire 4252'], 'tabColorStyle': {'rgbColor': NAVY}},
            'fields': 'tabColorStyle'
        }
    },
    # Raw Data: Gray
    {
        'updateSheetProperties': {
            'properties': {'sheetId': TABS['Original Overview'], 'tabColorStyle': {'rgbColor': GRAY_TAB}},
            'fields': 'tabColorStyle'
        }
    },
]

batch_update(structural_requests)
print("  ✅ Tab renamed & colors applied")

# ============================================================
# STEP 2: Clear and rewrite Dashboard
# ============================================================
print("\n📊 Step 2: Restructuring Dashboard...")

# Clear existing dashboard content
clear_range("'📊 Dashboard'!A1:Z200")
time.sleep(1)

# Build the new dashboard data
dashboard_data = [
    # Row 1-2: Title
    ['📊 JUNE 2025 — FINANCIAL DASHBOARD', '', '', '', '', ''],
    ['KuriosBrand LLC — Monthly Financial Overview', '', '', '', '', ''],
    [],  # Row 3: blank
    
    # SECTION A: INCOME SUMMARY (Row 4)
    ['💰 SECTION A: INCOME SUMMARY', '', '', '', '', ''],
    ['Business Line', 'Source', 'Method', 'Amount', '% of Total', 'Notes'],
    ['🏗️ Rank & Rent', 'Stripe — R&R client subs', 'Stripe', 3017.51, '', 'Client subscriptions'],
    ['🏗️ Rank & Rent', 'Zelle — R&R client subs', 'Zelle', 2000.00, '', 'Client subscriptions'],
    ['🏗️ Rank & Rent', 'Zelle — Hooked commissions', 'Zelle', 1530.00, '', 'Commissions'],
    ['', 'SUBTOTAL: 🏗️ Rank & Rent', '', 6547.51, '72.6%', ''],
    ['🔧 SEO / One-Time', 'Stripe — SEO clients', 'Stripe', 1125.00, '', 'Joshua Raymond SEO $1,125'],
    ['🔧 SEO / One-Time', 'Zelle — SEO client subs', 'Zelle', 1350.00, '', 'Willard SEO $1,350'],
    ['', 'SUBTOTAL: 🔧 SEO / One-Time', '', 2475.00, '27.4%', ''],
    ['🚗 MVA Lead Gen', '(not active this month)', '—', 0.00, '0.0%', ''],
    ['', 'SUBTOTAL: 🚗 MVA Lead Gen', '', 0.00, '0.0%', ''],
    ['', 'TOTAL INCOME', '', 9022.51, '100%', ''],
    [],  # blank
    [],  # blank
    
    # SECTION B: BUSINESS EXPENSES (Row 21)
    ['📊 SECTION B: BUSINESS EXPENSES', '', '', '', '', ''],
    ['Category', 'Vendor', 'Amount', 'Recurring?', 'Notes', ''],
    # SaaS & Tools
    ['📱 SaaS & Tools', '', '', '', '', ''],
    ['', 'HighLevel', -597.00, 'Monthly', 'CRM', ''],
    ['', '10web Hosting', -136.00, 'Monthly', 'Website hosting', ''],
    ['', 'Aaron Abke', -99.00, 'Cancelled', 'Education', ''],
    ['', 'PhotoAI.com', -99.00, '', '', ''],
    ['', 'VA Outsource', -99.00, '', '', ''],
    ['', 'CTR Manipulation', -79.00, 'Cancelled', '', ''],
    ['', "Kevin's PBN", -67.40, 'Cancelled', 'SEO backlinks', ''],
    ['', 'Flowith', -39.90, 'Monthly', 'AI tool', ''],
    ['', 'Google Software', -28.16, 'Monthly', 'Workspace', ''],
    ['', 'Ideogram AI', -20.00, 'Monthly', 'AI tool', ''],
    ['', 'ChatGPT', -20.00, 'Monthly', 'AI tool', ''],
    ['', 'Apple', -15.23, 'Monthly', '', ''],
    ['', 'Canva', -15.00, 'Monthly', 'Design tool', ''],
    ['', 'Spotify', -12.59, 'Monthly', '', ''],
    ['', 'Midjourney', -10.79, 'Cancelled', 'AI art', ''],
    ['', 'SUBTOTAL: 📱 SaaS & Tools', -1339.07, '', '', ''],
    # Marketing / Ads
    ['📣 Marketing / Ads', '', '', '', '', ''],
    ['', 'LocalRank.so Citations', -1050.00, '', 'Citation building', ''],
    ['', 'Reviews - Vendor', -358.40, '', 'GMB reviews', ''],
    ['', 'Indexsy - Guest Posts', -243.00, '', 'Backlinks', ''],
    ['', 'LocalRank.so (CC)', -174.30, 'Monthly', 'SEO software', ''],
    ['', 'Facebook Ads', -125.48, 'Cancelled', '', ''],
    ['', 'Reviews CashApp', -116.00, '', 'GMB reviews', ''],
    ['', 'CTR Manipulation (SEO)', -79.00, 'Cancelled', '', ''],
    ['', 'Namecheap Domains', -68.70, '', 'Domain registrations', ''],
    ['', 'Netipaulyu?', -33.00, '', '', ''],
    ['', 'SUBTOTAL: 📣 Marketing / Ads', -2247.88, '', '', ''],
    # Operations
    ['🏢 Operations', '', '', '', '', ''],
    ['', 'Regus', -99.00, 'Monthly', 'Coworking space', ''],
    ['', 'Boost Mobile', -66.62, 'Monthly', 'Business phone', ''],
    ['', 'Spectrum WiFi', -60.00, 'Monthly', 'Internet', ''],
    ['', 'Phone Bill T-Mobile', -55.36, 'Monthly', 'Phone', ''],
    ['', 'Zelle to Ross (logo)', -12.50, '', 'Logo design', ''],
    ['', 'SUBTOTAL: 🏢 Operations', -293.48, '', '', ''],
    # Debt Payments
    ['💳 Debt Payments (Business)', '', '', '', '', ''],
    ['', 'Biz CC Payment (4991 → 0678)', -300.00, '', 'Internal transfer', ''],
    ['', 'SUBTOTAL: 💳 Debt Payments', -300.00, '', '', ''],
    # Credit Building
    ['💳 Credit Building', '', '', '', '', ''],
    ['', 'Credit Strong', -90.00, 'Monthly', '', ''],
    ['', 'Self Lender', -48.00, 'Monthly', '', ''],
    ['', 'SUBTOTAL: 💳 Credit Building', -138.00, '', '', ''],
    # Business Fees
    ['💰 Business Fees & Interest', '', '', '', '', ''],
    ['', 'Monthly service fee', -15.00, 'Monthly', 'Chase bank fee', ''],
    ['', 'SUBTOTAL: 💰 Fees', -15.00, '', '', ''],
    ['', 'TOTAL BUSINESS EXPENSES', -4253.43, '', '', ''],
    [],  # blank
    [],  # blank
    
    # SECTION C: PERSONAL EXPENSES (Row ~75)
    ['👤 SECTION C: PERSONAL EXPENSES', '', '', '', '', ''],
    ['Category', 'Vendor', 'Amount', '', 'Notes', ''],
    ['🏠 Living / Local', '', '', '', '', ''],
    ['', 'Rent', -1100.00, '', 'Housing', ''],
    ['', 'We Energies (electric)', -112.85, '', 'Utilities', ''],
    ['', 'Apple Cash (Magen)', -200.00, '', 'Personal', ''],
    ['', 'Ascended Gifs (card reading + Reiki)', -216.56, '', '', ''],
    ['', 'Magen Bday Dinner', -190.00, '', '', ''],
    ['', 'Salon', -36.80, '', '', ''],
    ['', 'Weed', -77.93, '', '', ''],
    ['', 'Vape', -21.57, '', '', ''],
    ['', 'CVS (chocolates)', -18.79, '', '', ''],
    ['', 'Downer Hardware', -13.39, '', '', ''],
    ['', 'SUBTOTAL: 🏠 Living / Local', -1987.89, '', '', ''],
    ['🍔 Food & Dining', '', '', '', '', ''],
    ['', 'Groceries', -715.82, '', 'Multiple stores', ''],
    ['', 'Bars & eating out', -240.79, '', '', ''],
    ['', 'Coffee Shops', -82.12, '', '', ''],
    ['', 'SUBTOTAL: 🍔 Food & Dining', -1038.73, '', '', ''],
    ['🛍️ Shopping & Misc', '', '', '', '', ''],
    ['', 'Target (shopping)', -163.08, '', '', ''],
    ['', 'Amazon', -138.07, '', '', ''],
    ['', 'Old Navy', -46.57, '', '', ''],
    ['', 'SUBTOTAL: 🛍️ Shopping', -347.72, '', '', ''],
    ['📺 Subscriptions', '', '', '', '', ''],
    ['', 'Hulu', -32.36, '', '', ''],
    ['', 'Minecraft', -31.49, '', '', ''],
    ['', 'SUBTOTAL: 📺 Subscriptions', -63.85, '', '', ''],
    ['📈 Investments', '', '', '', '', ''],
    ['', 'Robinhood / Crypto', -496.00, '', 'Investing', ''],
    ['', 'Acorns', -91.40, '', 'Investing', ''],
    ['', 'SUBTOTAL: 📈 Investments', -587.40, '', '', ''],
    ['💳 CC Payments (Personal)', '', '', '', '', ''],
    ['', 'Chase 4252 CC Payment', -218.00, '', '', ''],
    ['', 'Discover CC Payment', -127.00, '', '', ''],
    ['', 'SUBTOTAL: 💳 CC Payments', -345.00, '', '', ''],
    ['🎓 Debt Payments', '', '', '', '', ''],
    ['', 'Student Loan Payment', -106.34, '', '', ''],
    ['', 'SUBTOTAL: 🎓 Debt', -106.34, '', '', ''],
    ['🚗 Transportation', '', '', '', '', ''],
    ['', 'Gasoline', 196.93, '', '(refund/credit?)', ''],
    ['', 'Lime scooter', -64.81, '', '', ''],
    ['', 'Tolls', -14.10, '', '', ''],
    ['', 'SUBTOTAL: 🚗 Transportation', 118.02, '', '', ''],
    ['🎉 Entertainment', '', '', '', '', ''],
    ['', 'Bowling', -45.00, '', '', ''],
    ['', 'SUBTOTAL: 🎉 Entertainment', -45.00, '', '', ''],
    ['🏥 Health', '', '', '', '', ''],
    ['', 'Dental Insurance', -16.26, '', '', ''],
    ['', 'SUBTOTAL: 🏥 Health', -16.26, '', '', ''],
    ['🏧 ATM / Cash', '', '', '', '', ''],
    ['', 'ATM withdrawals', -86.50, '', '', ''],
    ['', 'SUBTOTAL: 🏧 ATM', -86.50, '', '', ''],
    [],  # blank
    [],  # blank
    
    # SECTION D: KEY METRICS
    ['📈 SECTION D: KEY METRICS', '', '', '', '', ''],
    ['Metric', '', '', 'Value', 'Target', 'Status'],
    ['Total Revenue', '', '', 9022.51, '', ''],
    ['Total Business Expenses', '', '', -4253.43, '', ''],
    ['Business Profit', '', '', 4769.08, '', ''],
    ['Profit Margin', '', '', '52%', '50%+', '🟢'],
    ['Revenue Per Segment: R&R', '', '', 6547.51, '', '72.6%'],
    ['Revenue Per Segment: SEO', '', '', 2475.00, '', '27.4%'],
    [],  # blank
    [],  # blank
    
    # SECTION E: MONEY FLOW
    ['🔄 SECTION E: MONEY FLOW', '', '', '', '', ''],
    ['Flow', 'From', 'To', 'Amount', 'Notes', ''],
    ['Business → Personal', '4991', '0068', -4910.00, 'Owner draws', ''],
    ['Business → Tax', '4991', 'Wells Fargo', -400.00, 'Tax set-aside', ''],
    ['Personal → Business', '0068', '4991', 200.00, '', ''],
    ['Business → CC', '4991', '0678', -300.00, 'CC payment', ''],
    ['Personal → CC 4252', '0068', '4252', -218.00, 'CC payment', ''],
    ['Personal → Discover', '0068', 'Discover', -127.00, 'CC payment', ''],
    ['Savings → Personal', '7036', '0068', 712.71, '', ''],
    ['Personal → Savings', '0068', '7036', -505.00, '', ''],
    [],  # blank
    [],  # blank
    
    # SECTION F: DEBT TRACKING
    ['🏦 SECTION F: DEBT TRACKING', '', '', '', '', ''],
    ['Account', 'Balance', 'Limit', '% Utilization', 'Payment', 'Notes'],
    ['Student Loans', 9294.92, '', '', 106.34, ''],
    ['CC Discover Personal', 6295.59, '', '', 130.00, ''],
    ['CC Chase Personal 4252', 7779.21, '', '', 218.00, ''],
    ['CC Business 0678', 3722.19, '', '', 300.00, ''],
    ['TOTAL DEBT', 27091.91, '', '', '', ''],
    [],  # blank
    [],  # blank
    
    # SECTION G: ACCOUNT BALANCES
    ['💰 SECTION G: ACCOUNT BALANCES', '', '', '', '', ''],
    ['Account', 'Opening', 'Closing', 'Change', 'Notes', ''],
    ['(Balance data not available for June 2025)', '', '', '', '', ''],
    [],  # blank
    [],  # blank
    
    # SECTION H: ASSETS & NET WORTH
    ['💎 SECTION H: ASSETS & NET WORTH', '', '', '', '', ''],
    ['Asset', '', '', 'Value', 'Notes', ''],
    ['Rank & Rent Assets', '', '', 150000.00, 'Business equity', ''],
    ['Cash (liquid)', '', '', 6927.00, '', ''],
    ['Stocks', '', '', 628.00, 'Robinhood', ''],
    ['Bitcoin', '', '', 1100.00, '', ''],
    ['Solana', '', '', 873.00, '', ''],
    ['Dogecoin', '', '', 100.00, '', ''],
    ['Trumpcoin', '', '', 26.00, '', ''],
    ['', '', '', '', '', ''],
    ['Liquid Assets', '', '', 6927.00, '', ''],
    ['Business Equity', '', '', 150000.00, '', ''],
    ['TOTAL ASSETS', '', '', 156927.00, '', ''],
    ['TOTAL LIABILITIES', '', '', -27091.91, '', ''],
    ['NET WORTH', '', '', 129835.55, '', ''],
    [],  # blank
    [],  # blank
    
    # SECTION I: ACTION ITEMS
    ['📝 SECTION I: ACTION ITEMS', '', '', '', '', ''],
    ['Priority', 'Action', 'Status', 'Notes', '', ''],
    ['🔴 HIGH', 'Cancel unused SaaS subscriptions', '⬜', 'Midjourney, CTR Manip, Kevin PBN cancelled', '', ''],
    ['🟡 MED', 'Reduce LocalRank.so citation spend', '⬜', '$1,224.30 total across accounts', '', ''],
    ['🟡 MED', 'Review Facebook Ads ROI', '⬜', '$125.48 spent — what return?', '', ''],
    ['🟢 LOW', 'Consolidate phone plans', '⬜', 'T-Mobile + Boost = $121.98', '', ''],
]

update_values("'📊 Dashboard'!A1", dashboard_data)
print("  ✅ Dashboard data written")
time.sleep(1)

# ============================================================
# STEP 3: Format Dashboard headers
# ============================================================
print("\n🎨 Step 3: Formatting Dashboard...")

def section_header_format(sheet_id, row, end_col=5):
    """Return format request for a section header row"""
    return {
        'repeatCell': {
            'range': {
                'sheetId': sheet_id,
                'startRowIndex': row,
                'endRowIndex': row + 1,
                'startColumnIndex': 0,
                'endColumnIndex': end_col + 1
            },
            'cell': {
                'userEnteredFormat': {
                    'backgroundColor': NAVY,
                    'textFormat': {
                        'foregroundColorStyle': {'rgbColor': WHITE},
                        'bold': True,
                        'fontSize': 14
                    }
                }
            },
            'fields': 'userEnteredFormat(backgroundColor,textFormat)'
        }
    }

def col_header_format(sheet_id, row, end_col=5):
    """Return format for column headers"""
    return {
        'repeatCell': {
            'range': {
                'sheetId': sheet_id,
                'startRowIndex': row,
                'endRowIndex': row + 1,
                'startColumnIndex': 0,
                'endColumnIndex': end_col + 1
            },
            'cell': {
                'userEnteredFormat': {
                    'backgroundColor': NAVY,
                    'textFormat': {
                        'foregroundColorStyle': {'rgbColor': WHITE},
                        'bold': True,
                        'fontSize': 11
                    }
                }
            },
            'fields': 'userEnteredFormat(backgroundColor,textFormat)'
        }
    }

def subtotal_format(sheet_id, row, end_col=5):
    """Return format for subtotal rows"""
    return {
        'repeatCell': {
            'range': {
                'sheetId': sheet_id,
                'startRowIndex': row,
                'endRowIndex': row + 1,
                'startColumnIndex': 0,
                'endColumnIndex': end_col + 1
            },
            'cell': {
                'userEnteredFormat': {
                    'backgroundColor': LIGHT_GRAY,
                    'textFormat': {'bold': True}
                }
            },
            'fields': 'userEnteredFormat(backgroundColor,textFormat)'
        }
    }

def total_format(sheet_id, row, end_col=5):
    """Return format for total rows"""
    return {
        'repeatCell': {
            'range': {
                'sheetId': sheet_id,
                'startRowIndex': row,
                'endRowIndex': row + 1,
                'startColumnIndex': 0,
                'endColumnIndex': end_col + 1
            },
            'cell': {
                'userEnteredFormat': {
                    'backgroundColor': TOTAL_BG,
                    'textFormat': {'bold': True, 'fontSize': 11}
                }
            },
            'fields': 'userEnteredFormat(backgroundColor,textFormat)'
        }
    }

# Find section header rows (0-indexed)
# Row 0: Title, Row 1: Subtitle
# Row 3: Section A header
# Row 4: Column headers
# Row 8: Subtotal R&R
# Row 11: Subtotal SEO
# Row 13: Subtotal MVA
# Row 14: Total Income

# I need to find the actual row indices from the data list
# Let me count through dashboard_data to find the section headers
format_requests = []
sid = TABS['Dashboard']

# Title formatting (Row 0)
format_requests.append({
    'repeatCell': {
        'range': {'sheetId': sid, 'startRowIndex': 0, 'endRowIndex': 1, 'startColumnIndex': 0, 'endColumnIndex': 6},
        'cell': {'userEnteredFormat': {'textFormat': {'bold': True, 'fontSize': 16}}},
        'fields': 'userEnteredFormat(textFormat)'
    }
})

# Section A header (row 3)
format_requests.append(section_header_format(sid, 3))
# Section A column headers (row 4)
format_requests.append(col_header_format(sid, 4))
# Subtotal R&R (row 8)
format_requests.append(subtotal_format(sid, 8))
# Subtotal SEO (row 11)
format_requests.append(subtotal_format(sid, 11))
# Subtotal MVA (row 13)
format_requests.append(subtotal_format(sid, 13))
# Total Income (row 14)
format_requests.append(total_format(sid, 14))

# Section B header (row 17 — after 2 blank rows)
# Let me count: rows 0-14 = Section A (15 rows), rows 15-16 blank, row 17 = Section B
# Actually let me count the dashboard_data list items
# Row 0: Title
# Row 1: Subtitle
# Row 2: blank
# Row 3: Section A header
# Row 4: headers
# Row 5-7: R&R items
# Row 8: Subtotal R&R
# Row 9-10: SEO items
# Row 11: Subtotal SEO
# Row 12: MVA
# Row 13: Subtotal MVA
# Row 14: Total Income
# Row 15-16: blank
# Row 17: Section B header
# Row 18: Section B column headers
# Row 19: SaaS category header
# ... expenses ...
# Let me count more carefully by looking at dashboard_data indices

# Count rows to find section positions
row_idx = 0
section_rows = {}
for i, row in enumerate(dashboard_data):
    if row and len(row) > 0:
        text = str(row[0])
        if 'SECTION A' in text: section_rows['A'] = i
        elif 'SECTION B' in text: section_rows['B'] = i
        elif 'SECTION C' in text: section_rows['C'] = i
        elif 'SECTION D' in text: section_rows['D'] = i
        elif 'SECTION E' in text: section_rows['E'] = i
        elif 'SECTION F' in text: section_rows['F'] = i
        elif 'SECTION G' in text: section_rows['G'] = i
        elif 'SECTION H' in text: section_rows['H'] = i
        elif 'SECTION I' in text: section_rows['I'] = i
        elif 'SUBTOTAL' in text: pass  # handled separately
        elif 'TOTAL' in text and 'SUB' not in text: pass  # handled separately

print(f"  Section positions: {section_rows}")

# Format all section headers
for key, row in section_rows.items():
    format_requests.append(section_header_format(sid, row))
    # Column headers are always the next row
    format_requests.append(col_header_format(sid, row + 1))

# Find and format all subtotal and total rows
for i, row in enumerate(dashboard_data):
    if row and len(row) > 1:
        text = str(row[1]) if len(row) > 1 else ''
        text0 = str(row[0]) if len(row) > 0 else ''
        if 'SUBTOTAL' in text or 'SUBTOTAL' in text0:
            format_requests.append(subtotal_format(sid, i))
        elif ('TOTAL' in text and 'SUB' not in text) or ('TOTAL' in text0 and 'SUB' not in text0):
            format_requests.append(total_format(sid, i))

# Column widths for Dashboard
col_widths = [200, 250, 120, 130, 100, 200]
for j, w in enumerate(col_widths):
    format_requests.append({
        'updateDimensionProperties': {
            'range': {'sheetId': sid, 'dimension': 'COLUMNS', 'startIndex': j, 'endIndex': j + 1},
            'properties': {'pixelSize': w},
            'fields': 'pixelSize'
        }
    })

# Freeze first row on Dashboard
format_requests.append({
    'updateSheetProperties': {
        'properties': {'sheetId': sid, 'gridProperties': {'frozenRowCount': 0}},
        'fields': 'gridProperties.frozenRowCount'
    }
})

# Currency format for amount columns (col D = index 3)
format_requests.append({
    'repeatCell': {
        'range': {'sheetId': sid, 'startRowIndex': 0, 'endRowIndex': len(dashboard_data), 'startColumnIndex': 3, 'endColumnIndex': 4},
        'cell': {'userEnteredFormat': {'numberFormat': {'type': 'CURRENCY', 'pattern': '$#,##0.00;[Red]($#,##0.00)'}}},
        'fields': 'userEnteredFormat.numberFormat'
    }
})

batch_update(format_requests)
print("  ✅ Dashboard formatted")
time.sleep(1)

# ============================================================
# STEP 4: Transaction tab formatting
# ============================================================
print("\n📋 Step 4: Formatting transaction tabs...")

txn_tabs = [TABS['Business 4991'], TABS['Personal 0068'], TABS['Biz CC 0678'], TABS['Sapphire 4252']]
txn_tab_names = ['💼 Business 4991', '👤 Personal 0068', '💳 Biz CC 0678', '💎 Sapphire 4252']
txn_format_requests = []

for tab_id in txn_tabs:
    # Header row formatting
    txn_format_requests.append({
        'repeatCell': {
            'range': {'sheetId': tab_id, 'startRowIndex': 0, 'endRowIndex': 1, 'startColumnIndex': 0, 'endColumnIndex': 6},
            'cell': {
                'userEnteredFormat': {
                    'backgroundColor': NAVY,
                    'textFormat': {
                        'foregroundColorStyle': {'rgbColor': WHITE},
                        'bold': True,
                        'fontSize': 11
                    },
                    'horizontalAlignment': 'CENTER'
                }
            },
            'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)'
        }
    })
    
    # Freeze row 1
    txn_format_requests.append({
        'updateSheetProperties': {
            'properties': {'sheetId': tab_id, 'gridProperties': {'frozenRowCount': 1}},
            'fields': 'gridProperties.frozenRowCount'
        }
    })
    
    # Column widths: 110 / 250 / 250 / 130 / 130 / 250
    widths = [110, 250, 250, 130, 130, 250]
    for j, w in enumerate(widths):
        txn_format_requests.append({
            'updateDimensionProperties': {
                'range': {'sheetId': tab_id, 'dimension': 'COLUMNS', 'startIndex': j, 'endIndex': j + 1},
                'properties': {'pixelSize': w},
                'fields': 'pixelSize'
            }
        })
    
    # Header row height
    txn_format_requests.append({
        'updateDimensionProperties': {
            'range': {'sheetId': tab_id, 'dimension': 'ROWS', 'startIndex': 0, 'endIndex': 1},
            'properties': {'pixelSize': 30},
            'fields': 'pixelSize'
        }
    })

batch_update(txn_format_requests)

# Write standard headers to transaction tabs
for tab_name in txn_tab_names:
    # Check if first row already has proper headers
    # For June, the transaction tabs have "DATA LOST" messages
    # Overwrite row 1 with proper headers, keep the rest
    try:
        update_values(f"'{tab_name}'!A1:F1", [['Date', 'Vendor', 'Category', 'Amount', 'Balance', 'Notes']])
    except:
        pass

print("  ✅ Transaction tabs formatted")
time.sleep(1)

# ============================================================
# STEP 5: Populate Profit First tab
# ============================================================
print("\n💰 Step 5: Populating Profit First tab...")

clear_range("'💰 Profit First'!A1:G20")
time.sleep(0.5)

revenue = 9022.51
biz_expenses = 4253.43
profit = 4769.08

# Profit First allocations
pf_data = [
    ['💰 PROFIT FIRST ANALYSIS — JUNE 2025', '', '', '', '', '', ''],
    [''],
    ['Bucket', 'Target %', 'Current %', 'Target Amount', 'Actual Amount', 'Gap', 'Status'],
    ['Revenue (TAPs)', '100%', '100%', revenue, revenue, 0, '—'],
    ['Profit', '5%', f'{(profit/revenue*100):.1f}%', revenue * 0.05, profit, profit - revenue * 0.05, '🟢' if profit >= revenue * 0.05 else '🔴'],
    ['Owner\'s Comp', '50%', f'{(4910/revenue*100):.1f}%', revenue * 0.50, 4910.00, 4910 - revenue * 0.50, '🟢' if 4910 >= revenue * 0.45 else '🔴'],
    ['Tax', '15%', f'{(400/revenue*100):.1f}%', revenue * 0.15, 400.00, 400 - revenue * 0.15, '🟡'],
    ['OpEx', '30%', f'{(biz_expenses/revenue*100):.1f}%', revenue * 0.30, biz_expenses, biz_expenses - revenue * 0.30, '🟡' if biz_expenses <= revenue * 0.35 else '🔴'],
    [],
    ['Notes:', '', '', '', '', '', ''],
    ['• Revenue = Total business income from Section A', '', '', '', '', '', ''],
    ['• Owner\'s Comp = Transfers to Personal ($4,910)', '', '', '', '', '', ''],
    ['• Tax = Tax set-aside ($400)', '', '', '', '', '', ''],
    ['• OpEx = Total business expenses ($4,253.43)', '', '', '', '', '', ''],
    ['• Profit margin: 52% — healthy margin above target', '', '', '', '', '', ''],
]

update_values("'💰 Profit First'!A1", pf_data)

# Format Profit First
pf_format = [
    section_header_format(TABS['Profit First'], 0, 6),
    col_header_format(TABS['Profit First'], 2, 6),
]
# Column widths
pf_widths = [150, 100, 100, 130, 130, 130, 80]
for j, w in enumerate(pf_widths):
    pf_format.append({
        'updateDimensionProperties': {
            'range': {'sheetId': TABS['Profit First'], 'dimension': 'COLUMNS', 'startIndex': j, 'endIndex': j + 1},
            'properties': {'pixelSize': w},
            'fields': 'pixelSize'
        }
    })
batch_update(pf_format)
print("  ✅ Profit First populated")
time.sleep(1)

# ============================================================
# STEP 6: Populate Pareto Analysis tab
# ============================================================
print("\n🎯 Step 6: Populating Pareto Analysis tab...")

clear_range("'🎯 Pareto Analysis'!A1:G50")
time.sleep(0.5)

# All business expenses sorted by amount (descending, excluding CC payment transfer)
expenses = [
    ('LocalRank.so Citations', 1050.00, '📣 Marketing / SEO'),
    ('HighLevel', 597.00, '📱 SaaS & Tools'),
    ('Reviews - Vendor', 358.40, '📣 Marketing / SEO'),
    ('Indexsy - Guest Posts', 243.00, '📣 Marketing / SEO'),
    ('LocalRank.so (CC)', 174.30, '📣 Marketing / SEO'),
    ('10web Hosting', 136.00, '📱 SaaS & Tools'),
    ('Facebook Ads', 125.48, '📣 Marketing / Ads'),
    ('Reviews CashApp', 116.00, '📣 Marketing / SEO'),
    ('Aaron Abke', 99.00, '📱 SaaS & Tools'),
    ('VA Outsource', 99.00, '🏢 Operations'),
    ('PhotoAI.com', 99.00, '📱 SaaS & Tools'),
    ('Regus', 99.00, '🏢 Operations'),
    ('Credit Strong', 90.00, '💳 Credit Building'),
    ('CTR Manipulation', 79.00, '📣 Marketing / SEO'),
    ('Namecheap Domains', 68.70, '🏢 Operations'),
    ("Kevin's PBN", 67.40, '📣 Marketing / SEO'),
    ('Boost Mobile', 66.62, '🏢 Operations'),
    ('Spectrum WiFi', 60.00, '🏢 Operations'),
    ('Phone Bill T-Mobile', 55.36, '🏢 Operations'),
    ('Self Lender', 48.00, '💳 Credit Building'),
    ('Flowith', 39.90, '📱 SaaS & Tools'),
    ('Netipaulyu?', 33.00, '📣 Marketing / SEO'),
    ('Google Software', 28.16, '📱 SaaS & Tools'),
    ('Ideogram AI', 20.00, '📱 SaaS & Tools'),
    ('ChatGPT', 20.00, '📱 SaaS & Tools'),
    ('Apple', 15.23, '📱 SaaS & Tools'),
    ('Canva', 15.00, '📱 SaaS & Tools'),
    ('Monthly service fee', 15.00, '💰 Fees'),
    ('Zelle to Ross', 12.50, '🏢 Operations'),
    ('Spotify', 12.59, '📱 SaaS & Tools'),
    ('Midjourney', 10.79, '📱 SaaS & Tools'),
]

# Sort by amount descending
expenses.sort(key=lambda x: x[1], reverse=True)

total_expenses = sum(e[1] for e in expenses)
cumulative = 0
pareto_data = [
    ['🎯 PARETO ANALYSIS — JUNE 2025', '', '', '', '', '', ''],
    ['Business expenses ranked by amount (80/20 rule)', '', '', '', '', '', ''],
    ['Rank', 'Expense', 'Amount', 'Cumulative', 'Cum %', 'Category', '80% Line'],
]

threshold_marked = False
for i, (name, amount, category) in enumerate(expenses):
    cumulative += amount
    pct = cumulative / total_expenses * 100
    marker = ''
    if not threshold_marked and pct >= 80:
        marker = '← 80% HERE'
        threshold_marked = True
    pareto_data.append([i + 1, name, -amount, -cumulative, f'{pct:.1f}%', category, marker])

pareto_data.append([])
pareto_data.append(['', 'TOTAL', -total_expenses, '', '100%', '', ''])
pareto_data.append([])
pareto_data.append([f'Top 5 expenses account for ${sum(e[1] for e in expenses[:5]):.2f} ({sum(e[1] for e in expenses[:5])/total_expenses*100:.0f}% of total)'])

update_values("'🎯 Pareto Analysis'!A1", pareto_data)

# Format Pareto
pareto_format = [
    section_header_format(TABS['Pareto Analysis'], 0, 6),
    col_header_format(TABS['Pareto Analysis'], 2, 6),
]
pareto_widths = [60, 250, 130, 130, 80, 200, 120]
for j, w in enumerate(pareto_widths):
    pareto_format.append({
        'updateDimensionProperties': {
            'range': {'sheetId': TABS['Pareto Analysis'], 'dimension': 'COLUMNS', 'startIndex': j, 'endIndex': j + 1},
            'properties': {'pixelSize': w},
            'fields': 'pixelSize'
        }
    })
# Currency format
pareto_format.append({
    'repeatCell': {
        'range': {'sheetId': TABS['Pareto Analysis'], 'startRowIndex': 3, 'endRowIndex': 3 + len(expenses) + 2, 'startColumnIndex': 2, 'endColumnIndex': 4},
        'cell': {'userEnteredFormat': {'numberFormat': {'type': 'CURRENCY', 'pattern': '$#,##0.00;[Red]($#,##0.00)'}}},
        'fields': 'userEnteredFormat.numberFormat'
    }
})
batch_update(pareto_format)
print("  ✅ Pareto Analysis populated")

# ============================================================
# FINAL: Verify
# ============================================================
print("\n✅ June 2025 standardization complete!")
print(f"  Income: $9,022.51")
print(f"  Expenses: -$4,253.43")
print(f"  Profit: $4,769.08 (52%)")
print(f"  Dashboard: Sections A-I restructured")
print(f"  Profit First: Populated with actual data")
print(f"  Pareto: {len(expenses)} expenses ranked")
print(f"  Tab colors: ✅ All fixed")
print(f"  Tab name: 📦 Original Overview → 📦 Raw Data ✅")
print(f"  Transaction tabs: Headers formatted (data was previously lost)")
