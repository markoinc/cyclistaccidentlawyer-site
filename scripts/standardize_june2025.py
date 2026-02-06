#!/usr/bin/env python3
"""Standardize June 2025 KuriosBrand Accounting Sheet"""

import json
import urllib.request
import urllib.parse
import sys

SHEET_ID = "19YSihOlMi1R-2nkZzfwa1dmoidouGl4UakhjdfceBsg"

def get_token():
    t = json.load(open('/home/ec2-user/.config/gcal-pro/token.json'))
    data = urllib.parse.urlencode({
        'client_id': t['client_id'],
        'client_secret': t['client_secret'],
        'refresh_token': t['refresh_token'],
        'grant_type': 'refresh_token'
    }).encode()
    req = urllib.request.Request('https://oauth2.googleapis.com/token', data=data)
    resp = json.loads(urllib.request.urlopen(req).read())
    return resp['access_token']

def api_call(url, data=None, method='GET', token=None):
    if data is not None:
        payload = json.dumps(data).encode()
        req = urllib.request.Request(url, data=payload, method=method or 'POST')
        req.add_header('Content-Type', 'application/json')
    else:
        req = urllib.request.Request(url, method=method)
    req.add_header('Authorization', f'Bearer {token}')
    try:
        resp = urllib.request.urlopen(req)
        body = resp.read()
        return json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"API Error {e.code}: {error_body[:1000]}")
        raise

def batch_update(spreadsheet_id, requests, token):
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}:batchUpdate"
    return api_call(url, {"requests": requests}, token=token)

def values_update(spreadsheet_id, range_name, values, token):
    encoded = urllib.parse.quote(range_name)
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{encoded}?valueInputOption=USER_ENTERED"
    return api_call(url, {"range": range_name, "majorDimension": "ROWS", "values": values}, method='PUT', token=token)

def values_batch_update(spreadsheet_id, data, token):
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values:batchUpdate"
    return api_call(url, {"valueInputOption": "USER_ENTERED", "data": data}, token=token)

# Colors
NAVY = {"red": 0.106, "green": 0.165, "blue": 0.290}
WHITE = {"red": 1, "green": 1, "blue": 1}
LIGHT_GRAY = {"red": 0.953, "green": 0.953, "blue": 0.953}
LIGHT_NAVY = {"red": 0.910, "green": 0.929, "blue": 0.961}
GREEN_TAB = {"red": 0.204, "green": 0.659, "blue": 0.325}
ORANGE_TAB = {"red": 1.0, "green": 0.427, "blue": 0.004}
GRAY_TAB = {"red": 0.6, "green": 0.6, "blue": 0.6}
NAVY_TAB = {"red": 0.106, "green": 0.165, "blue": 0.290}

def make_cell_format(bg=None, bold=False, fg=None, size=None, halign=None):
    fmt = {"userEnteredFormat": {}}
    if bg:
        fmt["userEnteredFormat"]["backgroundColor"] = bg
    if bold or fg or size:
        tf = {}
        if bold: tf["bold"] = True
        if fg: tf["foregroundColor"] = fg
        if size: tf["fontSize"] = size
        fmt["userEnteredFormat"]["textFormat"] = tf
    if halign:
        fmt["userEnteredFormat"]["horizontalAlignment"] = halign
    return fmt

def repeat_cell_req(sheet_id, start_row, end_row, start_col, end_col, bg=None, bold=False, fg=None, size=None, halign=None):
    cell = make_cell_format(bg, bold, fg, size, halign)
    fields = []
    if bg: fields.append("userEnteredFormat.backgroundColor")
    if bold or fg or size: fields.append("userEnteredFormat.textFormat")
    if halign: fields.append("userEnteredFormat.horizontalAlignment")
    return {
        "repeatCell": {
            "range": {"sheetId": sheet_id, "startRowIndex": start_row, "endRowIndex": end_row, "startColumnIndex": start_col, "endColumnIndex": end_col},
            "cell": cell,
            "fields": ",".join(fields)
        }
    }

def col_width_req(sheet_id, col, width):
    return {
        "updateDimensionProperties": {
            "range": {"sheetId": sheet_id, "dimension": "COLUMNS", "startIndex": col, "endIndex": col + 1},
            "properties": {"pixelSize": width},
            "fields": "pixelSize"
        }
    }

def freeze_req(sheet_id, rows=0, cols=0):
    props = {}
    fields = []
    if rows:
        props["frozenRowCount"] = rows
        fields.append("gridProperties.frozenRowCount")
    if cols:
        props["frozenColumnCount"] = cols
        fields.append("gridProperties.frozenColumnCount")
    return {
        "updateSheetProperties": {
            "properties": {"sheetId": sheet_id, "gridProperties": props},
            "fields": ",".join(fields)
        }
    }

TOKEN = get_token()
print("✅ Got OAuth token")

# ============================================================
# PHASE 1: Structural Changes
# ============================================================
print("\n📋 Phase 1: Structural changes...")

# Get current sheet metadata
url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}?fields=properties.title,sheets.properties"
meta = api_call(url, token=TOKEN)
print(f"  Current title: {meta['properties']['title']}")
for s in meta['sheets']:
    p = s['properties']
    print(f"  Tab {p['index']}: '{p['title']}' (id={p['sheetId']})")

existing_tabs = {s['properties']['title']: s['properties']['sheetId'] for s in meta['sheets']}

struct_requests = []

# 1. Rename spreadsheet
struct_requests.append({
    "updateSpreadsheetProperties": {
        "properties": {"title": "June 2025 — KuriosBrand Financial Overview"},
        "fields": "title"
    }
})

# 2. Add missing tabs (Profit First, Pareto)
PROFIT_FIRST_ID = 1111111
PARETO_ID = 2222222

if "💰 Profit First" not in existing_tabs:
    struct_requests.append({
        "addSheet": {
            "properties": {
                "sheetId": PROFIT_FIRST_ID,
                "title": "💰 Profit First",
                "index": 1,
                "tabColor": GREEN_TAB
            }
        }
    })
    print("  ➕ Adding 💰 Profit First tab")

if "🎯 Pareto Analysis" not in existing_tabs:
    struct_requests.append({
        "addSheet": {
            "properties": {
                "sheetId": PARETO_ID,
                "title": "🎯 Pareto Analysis",
                "index": 2,
                "tabColor": ORANGE_TAB
            }
        }
    })
    print("  ➕ Adding 🎯 Pareto Analysis tab")

# 3. Rename Original Overview to Raw Data
if "📦 Original Overview" in existing_tabs and "📦 Raw Data" not in existing_tabs:
    struct_requests.append({
        "updateSheetProperties": {
            "properties": {
                "sheetId": existing_tabs["📦 Original Overview"],
                "title": "📦 Raw Data"
            },
            "fields": "title"
        }
    })
    print("  ✏️ Renaming 📦 Original Overview → 📦 Raw Data")

# Execute structural changes
if struct_requests:
    batch_update(SHEET_ID, struct_requests, TOKEN)
    print("  ✅ Structural changes applied")

# Now reorder tabs and set colors
# Refresh metadata
meta = api_call(f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}?fields=sheets.properties", token=TOKEN)
existing_tabs = {s['properties']['title']: s['properties']['sheetId'] for s in meta['sheets']}
print(f"  Current tabs: {list(existing_tabs.keys())}")

target_order = [
    ("📊 Dashboard", None),
    ("💰 Profit First", GREEN_TAB),
    ("🎯 Pareto Analysis", ORANGE_TAB),
    ("💼 Business 4991", NAVY_TAB),
    ("👤 Personal 0068", NAVY_TAB),
    ("💳 Biz CC 0678", NAVY_TAB),
    ("💎 Sapphire 4252", NAVY_TAB),
    ("📦 Raw Data", GRAY_TAB),
]

reorder_requests = []
for idx, (name, color) in enumerate(target_order):
    if name in existing_tabs:
        props = {"sheetId": existing_tabs[name], "index": idx}
        fields = ["index"]
        if color:
            props["tabColor"] = color
            fields.append("tabColor")
        reorder_requests.append({
            "updateSheetProperties": {
                "properties": props,
                "fields": ",".join(fields)
            }
        })

if reorder_requests:
    batch_update(SHEET_ID, reorder_requests, TOKEN)
    print("  ✅ Tabs reordered and colored")

# ============================================================
# PHASE 2: Write Dashboard Data
# ============================================================
print("\n📊 Phase 2: Writing Dashboard data...")

# First clear the dashboard
values_update(SHEET_ID, "'📊 Dashboard'!A1:AB200", 
    [[""] * 28 for _ in range(200)], TOKEN)
print("  🧹 Cleared old dashboard data")

# Build dashboard rows
rows = []

# Row 0: Title
rows.append(["June 2025 — KuriosBrand Financial Overview"])
rows.append([])  # blank

# SECTION A: INCOME SUMMARY
rows.append(["💰 SECTION A: INCOME SUMMARY", "", "", "", "", ""])
rows.append(["Business Line", "Source", "Method", "Amount", "% of Total", "Notes"])
# R&R items
rows.append(["🏗️ Rank & Rent", "Stripe (client subs)", "Stripe", 3017.51, "", "Client subscriptions"])
rows.append(["🏗️ Rank & Rent", "Zelle (client subs)", "Zelle", 2000, "", "Client subscriptions"])
rows.append(["🏗️ Rank & Rent", "Commissions (Hooked)", "Zelle", 1530, "", "Commissions"])
rows.append(["", "SUBTOTAL: 🏗️ Rank & Rent", "", 6547.51, "72.6%", ""])
# SEO items
rows.append(["🔧 SEO / One-Time", "Joshua Raymond SEO", "Stripe", 1125, "", "Monthly SEO"])
rows.append(["🔧 SEO / One-Time", "Willard Construction SEO", "Zelle", 1350, "", "Monthly SEO"])
rows.append(["", "SUBTOTAL: 🔧 SEO / One-Time", "", 2475, "27.4%", ""])
# MVA
rows.append(["🚗 MVA Lead Gen", "—", "—", 0, "0%", "Not yet active"])
rows.append(["", "SUBTOTAL: 🚗 MVA Lead Gen", "", 0, "0%", ""])
# Total
rows.append(["", "TOTAL INCOME", "", 9022.51, "100%", ""])
sec_a_start = 2  # row index of section header
sec_a_header_row = 3  # column headers
sec_a_subtotal_rows = [7, 10, 12]  # 0-indexed
sec_a_total_row = 13
rows.append([])
rows.append([])

# SECTION B: BUSINESS EXPENSES
sec_b_start = len(rows)
rows.append(["📊 SECTION B: BUSINESS EXPENSES", "", "", "", "", ""])
rows.append(["Category", "Vendor", "Status", "Amount", "Recurring?", "Notes"])

# SaaS & Tools
rows.append(["📱 SaaS & Tools", "", "", "", "", ""])
saas_items = [
    ["", "HighLevel", "recurring", -597, "Monthly", "CRM"],
    ["", "10web Hosting", "recurring", -136, "Monthly", "Website hosting"],
    ["", "PhotoAI.com", "", -99, "", "AI photos"],
    ["", "Aaron Abke", "cancelled", -99, "Monthly", "Education"],
    ["", "Namecheap Domains", "", -68.70, "", "Domain registrations"],
    ["", "Flowith", "recurring", -39.90, "Monthly", "AI subscription"],
    ["", "Google Software", "recurring", -28.16, "Monthly", "Workspace"],
    ["", "ChatGPT", "recurring", -20, "Monthly", "AI subscription"],
    ["", "Ideogram AI", "recurring", -20, "Monthly", "AI image gen"],
    ["", "Apple", "recurring", -15.23, "Monthly", ""],
    ["", "Canva", "recurring", -15, "Monthly", "Design"],
    ["", "Spotify", "recurring", -12.59, "Monthly", "Music/education"],
    ["", "Midjourney", "cancelled", -10.79, "Monthly", "AI image gen"],
]
saas_total = sum(item[3] for item in saas_items)
rows.extend(saas_items)
rows.append(["", "SUBTOTAL: 📱 SaaS & Tools", "", round(saas_total, 2), "", ""])
saas_subtotal_row = len(rows) - 1

# Marketing / Ads
rows.append(["📣 Marketing / Ads", "", "", "", "", ""])
marketing_items = [
    ["", "LocalRank Citations (Checking)", "", -1050, "", "SEO citations"],
    ["", "Reviews — Vendor", "", -358.40, "", "SEO reviews"],
    ["", "Indexsy — Guest Posts", "", -243, "", "SEO backlinks"],
    ["", "LocalRank.so (CC)", "recurring", -174.30, "Monthly", "SEO software"],
    ["", "Facebook Ads (CC)", "cancelled", -125.48, "", "Ad spend"],
    ["", "Reviews — CashApp", "", -116, "", "SEO reviews"],
    ["", "CTR Manipulation", "cancelled", -79, "", "SEO CTR"],
    ["", "Kevin's PBN", "cancelled", -67.40, "", "SEO backlinks"],
]
marketing_total = sum(item[3] for item in marketing_items)
rows.extend(marketing_items)
rows.append(["", "SUBTOTAL: 📣 Marketing / Ads", "", round(marketing_total, 2), "", ""])
marketing_subtotal_row = len(rows) - 1

# Operations
rows.append(["🏢 Operations", "", "", "", "", ""])
ops_items = [
    ["", "VA Outsource", "", -99, "", "Virtual assistant"],
    ["", "Regus (CC)", "recurring", -99, "Monthly", "Virtual address"],
    ["", "Boost Mobile", "recurring", -66.62, "Monthly", "Phone"],
    ["", "Spectrum WiFi (CC)", "recurring", -60, "Monthly", "Internet"],
    ["", "T-Mobile", "recurring", -55.36, "Monthly", "Phone"],
    ["", "Netipaulyu?", "", -33, "", "Unknown"],
    ["", "Zelle to Ross (logo)", "", -12.50, "", "Design commission"],
]
ops_total = sum(item[3] for item in ops_items)
rows.extend(ops_items)
rows.append(["", "SUBTOTAL: 🏢 Operations", "", round(ops_total, 2), "", ""])
ops_subtotal_row = len(rows) - 1

# Debt Payments
rows.append(["💳 Debt Payments (Business)", "", "", "", "", ""])
debt_items = [
    ["", "Biz CC Payment (4991 → 0678)", "", -300, "", "CC payoff"],
    ["", "Credit Strong", "recurring", -90, "Monthly", "Credit building"],
    ["", "Self Lender", "recurring", -48, "Monthly", "Credit building"],
]
debt_total = sum(item[3] for item in debt_items)
rows.extend(debt_items)
rows.append(["", "SUBTOTAL: 💳 Debt Payments", "", round(debt_total, 2), "", ""])
debt_subtotal_row = len(rows) - 1

# Fees & Interest
rows.append(["💰 Business Fees & Interest", "", "", "", "", ""])
fees_items = [
    ["", "Chase Monthly Service Fee", "recurring", -15, "Monthly", ""],
]
fees_total = sum(item[3] for item in fees_items)
rows.extend(fees_items)
rows.append(["", "SUBTOTAL: 💰 Fees & Interest", "", round(fees_total, 2), "", ""])
fees_subtotal_row = len(rows) - 1

# Total Business Expenses
total_biz_exp = round(saas_total + marketing_total + ops_total + debt_total + fees_total, 2)
rows.append(["", "TOTAL BUSINESS EXPENSES", "", total_biz_exp, "", ""])
biz_exp_total_row = len(rows) - 1

sec_b_col_header = sec_b_start + 1
sec_b_category_rows = []  # Track category header rows
sec_b_subtotal_rows = [saas_subtotal_row, marketing_subtotal_row, ops_subtotal_row, debt_subtotal_row, fees_subtotal_row]

rows.append([])
rows.append([])

# SECTION C: PERSONAL EXPENSES
sec_c_start = len(rows)
rows.append(["👤 SECTION C: PERSONAL EXPENSES", "", "", "", "", ""])
rows.append(["Category", "Detail", "Count", "Amount", "", "Notes"])

# Investments
rows.append(["📈 Investments (Net Flows)", "", "", "", "", ""])
rows.append(["", "Robinhood / Crypto DCA", "", -496, "", "Daily crypto buys"])
rows.append(["", "Acorns Investing", "", -91.40, "", "Round-ups + investing"])
rows.append(["", "SUBTOTAL: 📈 Investments", "", -587.40, "", ""])

# Living / Local
rows.append(["🏠 Living / Local", "", "", "", "", ""])
rows.append(["", "Rent", "", -1100, "", "Monthly rent"])
rows.append(["", "Elite North Shore (Gym)", "", -191.36, "", "Gym membership"])
rows.append(["", "We Energies (Electric)", "", -112.85, "", "Utility"])
rows.append(["", "Lime Scooter", "", -64.81, "", "Transportation"])
rows.append(["", "Dental Insurance", "", -16.26, "", "Health"])
rows.append(["", "Tolls", "", -14.10, "", "Transportation"])
rows.append(["", "Downer Hardware", "", -13.39, "", "Home"])
rows.append(["", "Gasoline (net)", "", 196.93, "", "Gas refund/cashback?"])
rows.append(["", "SUBTOTAL: 🏠 Living / Local", "", round(-1100-191.36-112.85-64.81-16.26-14.10-13.39+196.93, 2), "", ""])

# Food & Dining
rows.append(["🍔 Food & Dining", "", "", "", "", ""])
rows.append(["", "Groceries", "", -715.82, "", ""])
rows.append(["", "Bars & Eating Out", "", -240.79, "", ""])
rows.append(["", "Magen Bday Dinner", "", -190, "", "Birthday"])
rows.append(["", "Coffee Shops", "", -82.12, "", ""])
rows.append(["", "CVS (chocolates)", "", -18.79, "", ""])
rows.append(["", "SUBTOTAL: 🍔 Food & Dining", "", round(-715.82-240.79-190-82.12-18.79, 2), "", ""])

# Subscriptions
rows.append(["📺 Subscriptions", "", "", "", "", ""])
rows.append(["", "Hulu", "", -32.36, "", "Streaming"])
rows.append(["", "Minecraft", "", -31.49, "", "Gaming"])
rows.append(["", "SUBTOTAL: 📺 Subscriptions", "", round(-32.36-31.49, 2), "", ""])

# Shopping & Misc
rows.append(["🛍️ Shopping & Misc", "", "", "", "", ""])
rows.append(["", "Ascended Gifs (Card Reading + Reiki)", "", -216.56, "", "Spiritual"])
rows.append(["", "Apple Cash (Magen)", "", -200, "", "To Magen"])
rows.append(["", "Target", "", -163.08, "", "Shopping"])
rows.append(["", "Amazon", "", -138.07, "", "Shopping"])
rows.append(["", "Weed", "", -77.93, "", ""])
rows.append(["", "Old Navy", "", -46.57, "", "Clothing"])
rows.append(["", "Bowling", "", -45, "", "Entertainment"])
rows.append(["", "Salon", "", -36.80, "", ""])
rows.append(["", "Vape", "", -21.57, "", ""])
shopping_sub = round(-216.56-200-163.08-138.07-77.93-46.57-45-36.80-21.57, 2)
rows.append(["", "SUBTOTAL: 🛍️ Shopping & Misc", "", shopping_sub, "", ""])

# CC Payments
rows.append(["💳 CC Payments (Personal)", "", "", "", "", ""])
rows.append(["", "Chase Sapphire 4252 Payment", "", -218, "", ""])
rows.append(["", "Discover CC Payment", "", -127, "", ""])
rows.append(["", "Student Loan Payment", "", -106.34, "", ""])
rows.append(["", "SUBTOTAL: 💳 CC Payments", "", round(-218-127-106.34, 2), "", ""])

# CC Interest
rows.append(["💰 CC Interest & Fees (Personal)", "", "", "", "", ""])
rows.append(["", "Interest Charge (Sapphire 4252)", "", -148.05, "", ""])
rows.append(["", "SUBTOTAL: 💰 CC Interest", "", -148.05, "", ""])

# ATM
rows.append(["🏧 ATM / Cash / FX", "", "", "", "", ""])
rows.append(["", "ATM Withdrawals", "", -86.50, "", ""])
rows.append(["", "SUBTOTAL: 🏧 ATM / Cash", "", -86.50, "", ""])

rows.append([])
rows.append([])

# SECTION D: KEY METRICS
sec_d_start = len(rows)
rows.append(["📈 SECTION D: KEY METRICS", "", "", "", "", ""])
rows.append(["Metric", "", "", "Value", "Target", "Status"])
rows.append(["Total Revenue", "", "", 9022.51, "", ""])
rows.append(["Total Business Expenses", "", "", total_biz_exp, "", ""])
rows.append(["Business Profit", "", "", 4769.08, "", ""])
rows.append(["Profit Margin", "", "", "52.9%", "50%+", "🟢"])
rows.append(["MoM Revenue Change", "", "", "—", "", "First tracked month"])
rows.append(["Burn Rate", "", "", f"${abs(total_biz_exp):,.2f}/mo", "", ""])

rows.append([])
rows.append([])

# SECTION E: MONEY FLOW
sec_e_start = len(rows)
rows.append(["🔄 SECTION E: MONEY FLOW", "", "", "", "", ""])
rows.append(["Flow", "From", "To", "Amount", "", "Notes"])
rows.append(["Business → Personal", "4991", "0068", -4910, "", "Owner draws"])
rows.append(["Business → Tax", "4991", "Wells Fargo", -400, "", "Tax set-aside"])
rows.append(["Business → CC", "4991", "0678", -300, "", "CC payment"])
rows.append(["Personal → CC", "0068", "4252", -218, "", "CC payment"])
rows.append(["Personal → CC", "0068", "Discover", -127, "", "CC payment"])
rows.append(["Personal → Biz", "0068", "4991", 200, "", "Transfer"])
rows.append(["Savings → Personal", "7036", "0068", 712.71, "", ""])
rows.append(["Personal → Savings", "0068", "7036", -505, "", "Auto-saves"])

rows.append([])
rows.append([])

# SECTION F: DEBT TRACKING
sec_f_start = len(rows)
rows.append(["🏦 SECTION F: DEBT TRACKING", "", "", "", "", ""])
rows.append(["Account", "Balance", "Limit", "Utilization", "Min Payment", "Actual Payment"])
rows.append(["Student Loans", 9294.92, "—", "—", "", 106.34])
rows.append(["CC Discover Personal", 6295.59, 6300, "99.9%", "", 130])
rows.append(["CC Chase Sapphire 4252", 7779.21, 9300, "83.6%", "", 218])
rows.append(["CC Business Ink 0678", 3722.19, 5500, "67.7%", "", 300])
rows.append(["TOTAL DEBT", 27091.91, "", "", "", ""])

rows.append([])
rows.append([])

# SECTION G: ACCOUNT BALANCES (limited data for June)
sec_g_start = len(rows)
rows.append(["💰 SECTION G: ACCOUNT BALANCES", "", "", "", "", ""])
rows.append(["Account", "Opening", "Closing", "Change", "", "Notes"])
rows.append(["Chase Biz 4991", "—", "—", "—", "", "Statement not available"])
rows.append(["Chase Personal 0068", "—", "—", "—", "", "Statement not available"])
rows.append(["Chase Savings 7036", "—", "—", "—", "", "Statement not available"])

rows.append([])
rows.append([])

# SECTION H: ASSETS & NET WORTH
sec_h_start = len(rows)
rows.append(["💎 SECTION H: ASSETS & NET WORTH", "", "", "", "", ""])
rows.append(["Asset", "", "", "Value", "Change", "Notes"])
rows.append(["Business Equity", "", "", 150000, "—", "Rank & rent portfolio"])
rows.append(["Cash (all accounts)", "", "", 4200, "", ""])
rows.append(["Robinhood / Stocks", "", "", 628, "", ""])
rows.append(["Bitcoin", "", "", 1100, "", ""])
rows.append(["Solana", "", "", 873, "", ""])
rows.append(["Dogecoin", "", "", 100, "", ""])
rows.append(["Trumpcoin", "", "", 26, "", ""])
rows.append([])
rows.append(["Liquid Assets", "", "", 6927, "", ""])
rows.append(["Business Equity", "", "", 150000, "", ""])
rows.append(["TOTAL ASSETS", "", "", 156927.46, "", ""])
rows.append(["TOTAL LIABILITIES", "", "", -27091.91, "", "From Section F"])
rows.append(["NET WORTH", "", "", 129835.55, "", ""])

rows.append([])
rows.append([])

# SECTION I: ACTION ITEMS
sec_i_start = len(rows)
rows.append(["📝 SECTION I: ACTION ITEMS", "", "", "", "", ""])
rows.append(["Priority", "Action", "Status", "Due", "", "Notes"])
rows.append(["🔴 HIGH", "Cancel unused subscriptions (Midjourney, CTR, Kevin's PBN)", "✅ Done", "", "", "Cancelled in June"])
rows.append(["🟡 MED", "Reduce HighLevel plan ($597/mo)", "⬜", "", "", "Consider downgrade"])
rows.append(["🟡 MED", "Start paying $2k/mo toward CC debt", "⬜", "", "", "Per original strategy note"])
rows.append(["🟢 LOW", "Keep $2k in Chase Biz to eliminate service fee", "⬜", "", "", "Currently paying $15/mo"])

# Write dashboard data
print(f"  Writing {len(rows)} rows to Dashboard...")
values_update(SHEET_ID, "'📊 Dashboard'!A1:F" + str(len(rows)), rows, TOKEN)
print("  ✅ Dashboard data written")

# ============================================================
# PHASE 3: Write Profit First Tab
# ============================================================
print("\n💰 Phase 3: Writing Profit First tab...")

revenue = 9022.51
pf_rows = [
    ["💰 PROFIT FIRST ANALYSIS — June 2025"],
    [],
    ["Bucket", "Target %", "Current %", "Target Amount", "Actual Amount", "Gap"],
    ["Revenue (TAPs)", "100%", "100%", revenue, revenue, "—"],
    ["Profit", "5%", f"{round(4769.08/revenue*100,1)}%", round(revenue * 0.05, 2), 4769.08, round(4769.08 - revenue * 0.05, 2)],
    ["Owner's Comp", "50%", "54.4%", round(revenue * 0.50, 2), 4910, round(4910 - revenue * 0.50, 2)],
    ["Tax", "15%", f"{round(400/revenue*100,1)}%", round(revenue * 0.15, 2), 400, round(400 - revenue * 0.15, 2)],
    ["OpEx", "30%", f"{round(abs(total_biz_exp)/revenue*100,1)}%", round(revenue * 0.30, 2), round(abs(total_biz_exp), 2), round(abs(total_biz_exp) - revenue * 0.30, 2)],
    [],
    ["Notes:"],
    ["• Owner's Comp ($4,910) = transfers to personal checking"],
    ["• Tax ($400) = transfer to tax account"],
    [f"• OpEx (${abs(total_biz_exp):,.2f}) = total business expenses"],
    [f"• Profit is the residual after all allocations"],
]

values_update(SHEET_ID, "'💰 Profit First'!A1:F" + str(len(pf_rows)), pf_rows, TOKEN)
print("  ✅ Profit First data written")

# ============================================================
# PHASE 4: Write Pareto Analysis Tab
# ============================================================
print("\n🎯 Phase 4: Writing Pareto Analysis tab...")

# All expenses sorted by absolute amount
all_expenses = [
    ("LocalRank Citations", 1050, "📣 Marketing / Ads"),
    ("HighLevel", 597, "📱 SaaS & Tools"),
    ("Reviews — Vendor", 358.40, "📣 Marketing / Ads"),
    ("Biz CC Payment (0678)", 300, "💳 Debt Payments"),
    ("Indexsy — Guest Posts", 243, "📣 Marketing / Ads"),
    ("LocalRank.so (CC)", 174.30, "📣 Marketing / Ads"),
    ("10web Hosting", 136, "📱 SaaS & Tools"),
    ("Facebook Ads (CC)", 125.48, "📣 Marketing / Ads"),
    ("Reviews CashApp", 116, "📣 Marketing / Ads"),
    ("VA Outsource", 99, "🏢 Operations"),
    ("Regus (CC)", 99, "🏢 Operations"),
    ("Aaron Abke (CC)", 99, "📱 SaaS & Tools"),
    ("PhotoAI", 99, "📱 SaaS & Tools"),
    ("Credit Strong", 90, "💳 Debt Payments"),
    ("CTR Manipulation", 79, "📣 Marketing / Ads"),
    ("Namecheap (CC)", 68.70, "📱 SaaS & Tools"),
    ("Kevin's PBN", 67.40, "📣 Marketing / Ads"),
    ("Boost Mobile", 66.62, "🏢 Operations"),
    ("Spectrum WiFi (CC)", 60, "🏢 Operations"),
    ("T-Mobile", 55.36, "🏢 Operations"),
    ("Self Lender", 48, "💳 Debt Payments"),
    ("Flowith", 39.90, "📱 SaaS & Tools"),
    ("Netipaulyu?", 33, "🏢 Operations"),
    ("Google Software (CC)", 28.16, "📱 SaaS & Tools"),
    ("ChatGPT (CC)", 20, "📱 SaaS & Tools"),
    ("Ideogram AI (CC)", 20, "📱 SaaS & Tools"),
    ("Apple", 15.23, "📱 SaaS & Tools"),
    ("Chase Service Fee", 15, "💰 Fees & Interest"),
    ("Canva (CC)", 15, "📱 SaaS & Tools"),
    ("Zelle to Ross", 12.50, "🏢 Operations"),
    ("Spotify (CC)", 12.59, "📱 SaaS & Tools"),
    ("Midjourney", 10.79, "📱 SaaS & Tools"),
]

# Sort by amount descending
all_expenses.sort(key=lambda x: x[1], reverse=True)
grand_total = sum(e[1] for e in all_expenses)

pareto_rows = [
    ["🎯 PARETO ANALYSIS — June 2025 Business Expenses"],
    [],
    ["Rank", "Expense", "Amount", "Cumulative", "Cum %", "Category"],
]

cumulative = 0
for i, (name, amount, category) in enumerate(all_expenses):
    cumulative += amount
    cum_pct = cumulative / grand_total * 100
    marker = " ← 80% line" if i > 0 and (cumulative - amount) / grand_total * 100 < 80 <= cum_pct else ""
    pareto_rows.append([
        i + 1, name, f"-${amount:,.2f}", f"-${cumulative:,.2f}", f"{cum_pct:.1f}%{marker}", category
    ])

pareto_rows.append([])
pareto_rows.append(["", "TOTAL", f"-${grand_total:,.2f}", "", "100%", ""])
pareto_rows.append([])
pareto_rows.append(["Key Insight: Top 5 expenses account for " + 
    f"{sum(e[1] for e in all_expenses[:5])/grand_total*100:.0f}% of total business spending"])

values_update(SHEET_ID, "'🎯 Pareto Analysis'!A1:F" + str(len(pareto_rows)), pareto_rows, TOKEN)
print("  ✅ Pareto Analysis data written")

# ============================================================
# PHASE 5: Format Transaction Tabs
# ============================================================
print("\n📋 Phase 5: Formatting transaction tabs...")

txn_tabs = [
    ("💼 Business 4991", existing_tabs.get("💼 Business 4991")),
    ("👤 Personal 0068", existing_tabs.get("👤 Personal 0068")),
    ("💳 Biz CC 0678", existing_tabs.get("💳 Biz CC 0678")),
    ("💎 Sapphire 4252", existing_tabs.get("💎 Sapphire 4252")),
]

for tab_name, tab_id in txn_tabs:
    if tab_id is None:
        continue
    # Clear and write headers + data lost message
    header = ["Date", "Vendor", "Category", "Amount", "Balance", "Notes"]
    data_lost = [
        [],
        ["⚠️ DATA LOST — Transaction data was lost during a previous redesign (Feb 2026 audit)."],
        ["The 📦 Raw Data tab preserves the original Dashboard summary."],
        ["To restore: Re-download June 2025 statement from Chase.com"],
    ]
    values_update(SHEET_ID, f"'{tab_name}'!A1:F10", 
        [[""] * 6 for _ in range(10)], TOKEN)
    values_update(SHEET_ID, f"'{tab_name}'!A1:F5",
        [header] + data_lost, TOKEN)

print("  ✅ Transaction tab headers written")

# ============================================================
# PHASE 6: Apply Formatting
# ============================================================
print("\n🎨 Phase 6: Applying formatting...")

fmt_requests = []
dashboard_id = 0

# Title formatting (row 0)
fmt_requests.append(repeat_cell_req(dashboard_id, 0, 1, 0, 6, bold=True, size=14))

# Helper for section headers
section_header_rows = [sec_a_start, sec_b_start, sec_c_start, sec_d_start, sec_e_start, sec_f_start, sec_g_start, sec_h_start, sec_i_start]
for r in section_header_rows:
    fmt_requests.append(repeat_cell_req(dashboard_id, r, r+1, 0, 6, bg=NAVY, bold=True, fg=WHITE, size=12))

# Column header rows (row after section header)
col_header_rows = [sec_a_start+1, sec_b_start+1, sec_c_start+1, sec_d_start+1, sec_e_start+1, sec_f_start+1, sec_g_start+1, sec_h_start+1, sec_i_start+1]
for r in col_header_rows:
    fmt_requests.append(repeat_cell_req(dashboard_id, r, r+1, 0, 6, bg=LIGHT_GRAY, bold=True, size=10))

# Section A subtotals and total
for r in sec_a_subtotal_rows:
    fmt_requests.append(repeat_cell_req(dashboard_id, r, r+1, 0, 6, bg=LIGHT_GRAY, bold=True))
fmt_requests.append(repeat_cell_req(dashboard_id, sec_a_total_row, sec_a_total_row+1, 0, 6, bg=LIGHT_NAVY, bold=True))

# Section B subtotals and total
for r in sec_b_subtotal_rows:
    fmt_requests.append(repeat_cell_req(dashboard_id, r, r+1, 0, 6, bg=LIGHT_GRAY, bold=True))
fmt_requests.append(repeat_cell_req(dashboard_id, biz_exp_total_row, biz_exp_total_row+1, 0, 6, bg=LIGHT_NAVY, bold=True))

# Column widths for Dashboard
widths = [200, 250, 100, 120, 100, 200]
for i, w in enumerate(widths):
    fmt_requests.append(col_width_req(dashboard_id, i, w))

# Freeze row 0 on Dashboard (no freeze needed since no header row to freeze)

# Transaction tab formatting
for tab_name, tab_id in txn_tabs:
    if tab_id is None:
        continue
    # Header row formatting
    fmt_requests.append(repeat_cell_req(tab_id, 0, 1, 0, 6, bg=NAVY, bold=True, fg=WHITE, size=11))
    # Freeze row 1
    fmt_requests.append(freeze_req(tab_id, rows=1))
    # Column widths
    txn_widths = [110, 250, 250, 130, 130, 250]
    for i, w in enumerate(txn_widths):
        fmt_requests.append(col_width_req(tab_id, i, w))

# Profit First formatting
pf_id = PROFIT_FIRST_ID
fmt_requests.append(repeat_cell_req(pf_id, 0, 1, 0, 6, bold=True, size=14))
fmt_requests.append(repeat_cell_req(pf_id, 2, 3, 0, 6, bg=NAVY, bold=True, fg=WHITE, size=11))
# Column widths for Profit First
for i, w in enumerate([180, 100, 100, 140, 140, 140]):
    fmt_requests.append(col_width_req(pf_id, i, w))

# Pareto formatting
pa_id = PARETO_ID
fmt_requests.append(repeat_cell_req(pa_id, 0, 1, 0, 6, bold=True, size=14))
fmt_requests.append(repeat_cell_req(pa_id, 2, 3, 0, 6, bg=NAVY, bold=True, fg=WHITE, size=11))
for i, w in enumerate([60, 250, 120, 120, 100, 180]):
    fmt_requests.append(col_width_req(pa_id, i, w))

# Raw Data tab formatting
raw_id = existing_tabs.get("📦 Raw Data") or existing_tabs.get("📦 Original Overview")
if raw_id:
    fmt_requests.append({
        "updateSheetProperties": {
            "properties": {"sheetId": raw_id, "tabColor": GRAY_TAB},
            "fields": "tabColor"
        }
    })

# Execute formatting
print(f"  Applying {len(fmt_requests)} formatting requests...")
# Split into batches of 50 to avoid size limits
for i in range(0, len(fmt_requests), 50):
    batch = fmt_requests[i:i+50]
    batch_update(SHEET_ID, batch, TOKEN)
print("  ✅ Formatting applied")

# ============================================================
# VERIFICATION
# ============================================================
print("\n✅ VERIFICATION")
print(f"  Total Income: $9,022.51 (R&R: $6,547.51 + SEO: $2,475.00)")
print(f"  Total Business Expenses: ${total_biz_exp:,.2f}")
print(f"  Expected: -$4,253.43")
print(f"  Match: {'✅ YES' if abs(total_biz_exp - (-4253.43)) < 0.01 else '❌ NO — diff: ' + str(round(total_biz_exp - (-4253.43), 2))}")
print(f"  Pre-tax Profit: $4,769.08")
print(f"  Profit check: {round(9022.51 + total_biz_exp, 2)} (should be ~4769.08)")
print(f"  Net Worth: $129,835.55")
print(f"  Total Debt: $27,091.91")

print("\n🎉 June 2025 standardization complete!")
