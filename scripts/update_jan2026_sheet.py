#!/usr/bin/env python3
"""
Update January 2026 Financial Sheet:
1. Fix Dashboard with verified audit numbers
2. Add Pareto Analysis tab
"""

import json
import requests
import sys

# ── Auth ──────────────────────────────────────────────────────────────────────
with open("/home/ec2-user/.config/gcal-pro/token.json") as f:
    token_data = json.load(f)

# Refresh token
resp = requests.post("https://oauth2.googleapis.com/token", data={
    "client_id": token_data["client_id"],
    "client_secret": token_data["client_secret"],
    "refresh_token": token_data["refresh_token"],
    "grant_type": "refresh_token"
})
access_token = resp.json()["access_token"]
HEADERS = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

with open("/home/ec2-user/clawd/data/jan-2026-sheet-id.txt") as f:
    SHEET_ID = f.read().strip()

BASE = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}"

def sheets_get(range_str):
    r = requests.get(f"{BASE}/values/{requests.utils.quote(range_str)}", headers=HEADERS)
    return r.json()

def sheets_update(range_str, values, input_option="USER_ENTERED"):
    r = requests.put(
        f"{BASE}/values/{requests.utils.quote(range_str)}?valueInputOption={input_option}",
        headers=HEADERS,
        json={"range": range_str, "majorDimension": "ROWS", "values": values}
    )
    return r.json()

def sheets_batch_update(requests_list):
    r = requests.post(
        f"{BASE}:batchUpdate",
        headers=HEADERS,
        json={"requests": requests_list}
    )
    return r.json()

def sheets_clear(range_str):
    r = requests.post(
        f"{BASE}/values/{requests.utils.quote(range_str)}:clear",
        headers=HEADERS,
        json={}
    )
    return r.json()

# ── Color helpers ─────────────────────────────────────────────────────────────
def rgb(r, g, b):
    return {"red": r/255, "green": g/255, "blue": b/255}

NAVY = rgb(26, 35, 66)        # Dark navy headers
DARK_BG = rgb(35, 45, 80)     # Slightly lighter for sub-headers
LIGHT_BG = rgb(240, 245, 255) # Light blue for alternating
WHITE = rgb(255, 255, 255)
GOLD = rgb(255, 193, 7)       # Gold for highlights
GREEN = rgb(46, 204, 113)     # Green for positive
RED = rgb(231, 76, 60)        # Red for negative
ORANGE = rgb(255, 152, 0)     # Orange for warnings
YELLOW_BG = rgb(255, 243, 224)# Light yellow for recommendations
LIGHT_GREEN = rgb(232, 245, 233)
LIGHT_RED = rgb(255, 235, 238)
GRAY = rgb(189, 189, 189)
DARK_TEXT = rgb(33, 33, 33)
TEAL = rgb(0, 150, 136)
PURPLE = rgb(103, 58, 183)

# ── Part 1: Update Dashboard ─────────────────────────────────────────────────
print("=== Part 1: Updating Dashboard ===")

# Clear existing Dashboard content
sheets_clear("'📊 Dashboard'!A1:H200")

# Build the corrected Dashboard data
dashboard_data = [
    # Row 1: Title
    ["January 2026 — KuriosBrand Financial Overview", "", "", "", "", "", "", "✅ Audit Verified"],
    # Row 2: empty
    [],
    # ── SECTION A: INCOME ──
    ["💰 SECTION A: INCOME SUMMARY"],
    ["Source", "Vendor / Client", "Date", "Amount"],
    # Stripe (7 transactions verified)
    ["Stripe", "Stripe", "01/02/2026", "$79.20"],
    ["Stripe", "Stripe", "01/05/2026", "$488.77"],
    ["Stripe", "Stripe", "01/20/2026", "$472.12"],
    ["Stripe", "Stripe", "01/23/2026", "$4,200.00"],
    ["Stripe", "Stripe", "01/27/2026", "$481.70"],
    ["Stripe", "Stripe", "02/02/2026", "$785.80"],
    ["Stripe", "Stripe", "02/03/2026", "$384.50"],
    ["", "", "Stripe Subtotal", "$6,892.09"],
    # Zelle (10 transactions verified)
    ["Zelle", "Anthony Reddin", "01/02/2026", "$250.00"],
    ["Zelle", "Anthony Reddin", "01/08/2026", "$250.00"],
    ["Zelle", "Alexander Shtabsky", "01/09/2026", "$500.00"],
    ["Zelle", "ACI Enterprise, LLC", "01/14/2026", "$1,000.00"],
    ["Zelle", "Anthony Reddin", "01/16/2026", "$250.00"],
    ["Zelle", "A-Z Mobile Apps, Inc.", "01/22/2026", "$3,000.00"],
    ["Zelle", "Anthony Reddin", "01/26/2026", "$250.00"],
    ["Zelle", "Jonathan Bible", "01/26/2026", "$500.00"],
    ["Zelle", "Christian Willard", "01/26/2026", "$700.00"],
    ["Zelle", "ACI Enterprise, LLC", "01/27/2026", "$1,000.00"],
    ["", "", "Zelle Subtotal", "$7,700.00"],
    # Other
    ["Other", "Credit Strong", "01/23/2026", "$100.00"],
    ["", "", "Other Subtotal", "$100.00"],
    ["", "", "TOTAL BUSINESS INCOME", "$14,692.09"],
    [],
    # ── SECTION B: BUSINESS EXPENSES ──
    ["📊 SECTION B: BUSINESS EXPENSES"],
    ["Category", "Vendor", "Count", "Total"],
    # SaaS & Tools
    ["📱 SaaS & Tools"],
    ["", "GoHighLevel", "4", "($507.00)"],
    ["", "Instantly", "4", "($283.06)"],
    ["", "10Web", "2", "($272.00)"],
    ["", "Claude AI (Anthropic)", "3", "($247.85)"],
    ["", "Google Ads", "3", "($234.80)"],
    ["", "Lemlist", "6", "($189.70)"],
    ["", "InVideo", "3", "($169.91)"],
    ["", "Google Workspace", "4", "($100.57)"],
    ["", "Exa.AI", "1", "($79.00)"],
    ["", "DataForSEO", "1", "($59.00)"],
    ["", "Higgsfield", "1", "($52.02)"],
    ["", "Lovable", "3", "($50.00)"],
    ["", "Apple (iCloud/services)", "2", "($46.73)"],
    ["", "Cloudflare", "2", "($36.86)"],
    ["", "HostMyApple", "1", "($35.79)"],
    ["", "MyFICO", "1", "($29.95)"],
    ["", "Spotify", "2", "($25.18)"],
    ["", "RapidURL Indexer", "1", "($25.00)"],
    ["", "Descript", "1", "($24.00)"],
    ["", "WI DFI (State Filing)", "2", "($20.00)"],
    ["", "Cursor IDE", "1", "($20.00)"],
    ["", "OpenAI/ChatGPT", "1", "($20.00)"],
    ["", "Traveling Mailbox", "1", "($19.95)"],
    ["", "Supermemory", "1", "($19.00)"],
    ["", "Namecheap", "1", "($11.48)"],
    ["", "Webshare Proxy", "1", "($10.68)"],
    ["", "NordVPN", "1", "($8.99)"],
    ["", "Google One", "1", "($1.99)"],
    ["", "Brave", "1", "($1.31)"],
    ["", "Google Cloud", "1", "($1.11)"],
    ["", "", "SaaS/Tools Subtotal", "($2,661.88)"],
    # Marketing / Ads
    ["📣 Marketing / Ads"],
    ["", "Meta Ads — Business 4991", "47", "($3,102.50)"],
    ["", "Meta Ads — Biz CC 0678", "8", "($3,101.81)"],
    ["", "Meta Ads — Sapphire 4252 ⚠️", "3", "($811.87)"],
    ["", "Google Ads", "3", "($243.75)"],
    ["", "", "Marketing Subtotal", "($7,259.93)"],
    # Operations
    ["🏢 Operations"],
    ["", "Wise Transfer", "2", "($832.59)"],
    ["", "T-Mobile", "1", "($55.66)"],
    ["", "SafetyWing (Insurance)", "1", "($66.28)"],
    ["", "Travel Auth (ETA-IL)", "2", "($8.21)"],
    ["", "", "Operations Subtotal", "($962.74)"],
    # Debt Payments
    ["💳 Debt Payments"],
    ["", "Affirm", "1", "($179.67)"],
    ["", "Self Lender (Credit Builder)", "1", "($48.00)"],
    ["", "", "Debt Subtotal", "($227.67)"],
    # Business Fees
    ["💰 Business Fees & Interest"],
    ["", "Biz CC 0678 Interest", "1", "($71.37)"],
    ["", "Monthly Service Fee (4991)", "1", "($15.00)"],
    ["", "Stop Payment Fee (4991)", "1", "($30.00)"],
    ["", "ATM Fee (4991)", "1", "($5.00)"],
    ["", "FX Fee (4991)", "2", "($11.07)"],
    ["", "", "Fees/Interest Subtotal", "($132.44)"],
    # ATM from business
    ["🏧 Business ATM"],
    ["", "ATM Withdrawal (4991)", "1", "($361.45)"],
    ["", "", "Business ATM Subtotal", "($361.45)"],
    ["", "", "TOTAL BUSINESS EXPENSES", "($11,606.11)"],
    [],
    # ── SECTION C: PERSONAL EXPENSES ──
    ["👤 SECTION C: PERSONAL EXPENSES"],
    ["Category", "Detail", "Count", "Total"],
    # ATM / Cash / FX
    ["🏧 ATM / Cash / FX Fees"],
    ["", "ATM Withdrawals (Peru)", "9", "($2,128.49)"],
    ["", "ATM Fees", "9", "($45.00)"],
    ["", "FX Fees", "10", "($64.29)"],
    ["", "", "ATM/Cash Subtotal", "($2,237.78)"],
    # Investments
    ["📈 Investments (Net Flows)"],
    ["", "Robinhood — Outflows", "34", "($459.00)"],
    ["", "Robinhood — Inflows", "5", "$2,725.37"],
    ["", "Robinhood Net", "", "+$2,266.37"],
    ["", "Acorns — Outflows", "34", "($214.36)"],
    ["", "Acorns — Inflows", "2", "$448.10"],
    ["", "Acorns Net", "", "+$233.74"],
    ["", "", "Investment Net", "+$2,500.11"],
    # Travel
    ["✈️ Travel"],
    ["", "Iberia (Lima flight)", "1", "($928.04)"],
    ["", "LATAM Airlines", "2", "($87.51)"],
    ["", "Airalo eSIM", "2", "($33.64)"],
    ["", "", "Travel Subtotal", "($1,049.19)"],
    # Subscriptions
    ["📺 Subscriptions"],
    ["", "Hulu", "2", "($71.20)"],
    ["", "Solstice", "1", "($8.99)"],
    ["", "Patreon", "1", "($5.28)"],
    ["", "Solstice Refund", "1", "$8.99"],
    ["", "", "Subscriptions Subtotal", "($76.48)"],
    # Student Loan
    ["🎓 Student Loan"],
    ["", "Dept of Education", "1", "($106.34)"],
    ["", "", "Student Loan Subtotal", "($106.34)"],
    # CC Payments
    ["💳 CC Payments (Personal → Sapphire)"],
    ["", "Chase Sapphire Autopay", "01/21", "($247.00)"],
    ["", "", "CC Payment Subtotal", "($247.00)"],
    # Personal CC Interest
    ["💰 CC Interest & Fees (Personal)"],
    ["", "Sapphire 4252 Interest", "1", "($165.86)"],
    ["", "Sapphire Annual Fee", "1", "($95.00)"],
    ["", "Sapphire Statement Credit", "1", "$108.86"],
    ["", "", "Personal CC Subtotal", "($152.00)"],
    # Living
    ["🏠 Living / Local"],
    ["", "Kula Community (Pisac)", "1", "($14.58)"],
    ["", "FX Fee on Kula", "1", "($0.43)"],
    ["", "", "Living Subtotal", "($15.01)"],
    [],
    # ── SECTION D: KEY METRICS ──
    ["📈 SECTION D: KEY METRICS"],
    ["Metric", "", "", "Value"],
    ["Business Income", "", "", "$14,692.09"],
    ["Business Expenses", "", "", "($11,606.11)"],
    ["Business Profit (before personal)", "", "", "$3,085.98"],
    ["Profit Margin", "", "", "21.0%"],
    [],
    ["⭐ Total Meta Ads Spend (ALL CARDS)", "", "", "($7,016.18)"],
    ["  → Business 4991 (46 FACEBK + 1 META WAVE)", "", "", "($3,102.50)"],
    ["  → Biz CC 0678 (8 charges)", "", "", "($3,101.81)"],
    ["  → Sapphire 4252 ⚠️ (3 charges)", "", "", "($811.87)"],
    [],
    ["Total Ad Spend (Meta + Google)", "", "", "($7,259.93)"],
    ["Total SaaS/Tools", "", "", "($2,661.88)"],
    ["CC Interest Total (All Cards)", "", "", "($237.23)"],
    ["Total Fees (ATM + FX + Bank)", "", "", "($502.59)"],
    ["Investment Net Flow (Robinhood + Acorns)", "", "", "+$2,500.11"],
    ["ATM Withdrawals (Peru)", "", "", "($2,128.49)"],
    ["Travel", "", "", "($1,049.19)"],
    ["Student Loan", "", "", "($106.34)"],
    ["Subscriptions", "", "", "($85.47)"],
    [],
    # ── SECTION E: MONEY FLOW ──
    ["🔄 SECTION E: MONEY FLOW"],
    ["Flow", "", "Count", "Total"],
    ["Biz 4991 → Personal 0068", "", "14", "$4,634.00"],
    ["Personal 0068 → Biz 4991", "", "6", "$3,255.00"],
    ["Net Flow (4991 → 0068)", "", "", "$1,379.00"],
    [],
    ["Personal → Savings 7036", "", "8", "$330.00"],
    ["Savings 7036 → Personal", "", "2", "$200.00"],
    ["Savings ODP → Personal", "", "1", "$2.37"],
    ["Savings → Business 4991", "", "1", "$200.00"],
    [],
    ["Biz 4991 → CC 0678", "", "3", "$5,261.00"],
    ["Biz 4991 → CC 4252", "", "1", "$261.00"],
    ["Personal 0068 → CC 4252 (autopay)", "", "1", "$247.00"],
    ["Zelle Outbound (Jonathan Bible)", "", "1", "$500.00"],
    [],
    # ── SECTION F: ACCOUNT BALANCES ──
    ["🏦 SECTION F: ACCOUNT BALANCES"],
    ["Account", "", "Start of Month", "End of Month"],
    ["Personal Checking 0068", "", "$155.64", "$269.21"],
    ["Business Checking 4991", "", "$1,443.77", "$1,357.74"],
    [],
    # ── SECTION G: ACTION ITEMS ──
    ["📝 SECTION G: ACTION ITEMS"],
    ["#", "Item", "Status", "Notes"],
    ["1", "Meta Ads on Sapphire 4252 — move to business card", "⚠️", "$811.87 on personal card"],
    ["2", "Reduce ATM fees — get Wise/Schwab debit card", "⚠️", "$50 ATM + $75 FX = $125 wasted"],
    ["3", "SaaS audit — $2,662/mo in tools, many underutilized", "🔍", "See 🎯 Pareto Analysis tab"],
    ["4", "Track Meta Ads → revenue attribution", "🔍", "2.1x ROAS but which campaigns?"],
    ["5", "Pay down CC debt ($237/mo interest)", "⚠️", "Investing while carrying CC debt"],
    ["6", "Review 10Web, InVideo, Higgsfield necessity", "", "Are these generating revenue?"],
]

# Write all dashboard data
result = sheets_update("'📊 Dashboard'!A1", dashboard_data)
print(f"Dashboard data written: {result.get('updatedCells', 'unknown')} cells")

# ── Dashboard Formatting ──────────────────────────────────────────────────────
print("Applying Dashboard formatting...")

DASHBOARD_ID = 0
fmt_requests = []

def fmt_range(sheet_id, r1, r2, c1, c2):
    return {
        "sheetId": sheet_id,
        "startRowIndex": r1,
        "endRowIndex": r2,
        "startColumnIndex": c1,
        "endColumnIndex": c2,
    }

def cell_fmt(rng, bg=None, fg=None, bold=False, fontSize=None, halign=None, numfmt=None):
    cell = {"userEnteredFormat": {}}
    fields = []
    if bg:
        cell["userEnteredFormat"]["backgroundColor"] = bg
        fields.append("userEnteredFormat.backgroundColor")
    if fg:
        cell["userEnteredFormat"]["textFormat"] = cell["userEnteredFormat"].get("textFormat", {})
        cell["userEnteredFormat"]["textFormat"]["foregroundColor"] = fg
        fields.append("userEnteredFormat.textFormat.foregroundColor")
    if bold:
        cell["userEnteredFormat"]["textFormat"] = cell["userEnteredFormat"].get("textFormat", {})
        cell["userEnteredFormat"]["textFormat"]["bold"] = True
        fields.append("userEnteredFormat.textFormat.bold")
    if fontSize:
        cell["userEnteredFormat"]["textFormat"] = cell["userEnteredFormat"].get("textFormat", {})
        cell["userEnteredFormat"]["textFormat"]["fontSize"] = fontSize
        fields.append("userEnteredFormat.textFormat.fontSize")
    if halign:
        cell["userEnteredFormat"]["horizontalAlignment"] = halign
        fields.append("userEnteredFormat.horizontalAlignment")
    if numfmt:
        cell["userEnteredFormat"]["numberFormat"] = numfmt
        fields.append("userEnteredFormat.numberFormat")
    return {
        "repeatCell": {
            "range": rng,
            "cell": cell,
            "fields": ",".join(fields)
        }
    }

# Count rows for formatting
total_rows = len(dashboard_data)

# Title row (row 0)
fmt_requests.append(cell_fmt(fmt_range(DASHBOARD_ID, 0, 1, 0, 8), bg=NAVY, fg=WHITE, bold=True, fontSize=14))

# Find section header rows and format them
section_headers = []
subtotal_rows = []
total_rows_list = []
column_header_rows = []

for i, row in enumerate(dashboard_data):
    if not row:
        continue
    first_cell = str(row[0]) if row else ""
    # Section headers (emoji headers)
    if first_cell.startswith(("💰 SECTION", "📊 SECTION", "👤 SECTION", "📈 SECTION", "🔄 SECTION", "🏦 SECTION", "📝 SECTION", "⭐")):
        section_headers.append(i)
    # Category sub-headers
    elif first_cell.startswith(("📱", "📣", "🏢", "💳", "💰", "🏧", "📈", "✈️", "📺", "🎓", "🏠", "🛡️")):
        section_headers.append(i)
    # Column header rows
    elif first_cell in ("Source", "Category", "Metric", "Flow", "Account", "#") and len(row) > 1:
        column_header_rows.append(i)
    
    # Subtotal and total rows
    if len(row) >= 3:
        cell2 = str(row[2]) if len(row) > 2 else ""
        if "Subtotal" in cell2 or "Subtotal" in str(row[1] if len(row) > 1 else ""):
            subtotal_rows.append(i)
        if "TOTAL" in cell2.upper():
            total_rows_list.append(i)

# Format section headers - navy background
for r in section_headers:
    fmt_requests.append(cell_fmt(fmt_range(DASHBOARD_ID, r, r+1, 0, 8), bg=NAVY, fg=WHITE, bold=True, fontSize=11))

# Format column headers - dark background  
for r in column_header_rows:
    fmt_requests.append(cell_fmt(fmt_range(DASHBOARD_ID, r, r+1, 0, 8), bg=DARK_BG, fg=WHITE, bold=True))

# Format subtotal rows - light background, bold
for r in subtotal_rows:
    fmt_requests.append(cell_fmt(fmt_range(DASHBOARD_ID, r, r+1, 0, 8), bg=LIGHT_BG, bold=True))

# Format TOTAL rows - green/bold
for r in total_rows_list:
    fmt_requests.append(cell_fmt(fmt_range(DASHBOARD_ID, r, r+1, 0, 8), bg=rgb(200, 230, 201), bold=True, fontSize=12))

# Column D (amounts) right-aligned
fmt_requests.append(cell_fmt(fmt_range(DASHBOARD_ID, 0, len(dashboard_data), 3, 4), halign="RIGHT"))

# Bold the audit verified text
fmt_requests.append(cell_fmt(fmt_range(DASHBOARD_ID, 0, 1, 7, 8), fg=GREEN, bold=True))

# Set column widths
for col_idx, width in [(0, 220), (1, 250), (2, 180), (3, 140), (4, 40), (5, 40), (6, 40), (7, 140)]:
    fmt_requests.append({
        "updateDimensionProperties": {
            "range": {
                "sheetId": DASHBOARD_ID,
                "dimension": "COLUMNS",
                "startIndex": col_idx,
                "endIndex": col_idx + 1,
            },
            "properties": {"pixelSize": width},
            "fields": "pixelSize"
        }
    })

# Apply formatting
if fmt_requests:
    result = sheets_batch_update(fmt_requests)
    print(f"Dashboard formatting applied: {len(fmt_requests)} requests")

# ══════════════════════════════════════════════════════════════════════════════
# Part 2: Create Pareto Analysis Tab
# ══════════════════════════════════════════════════════════════════════════════
print("\n=== Part 2: Creating Pareto Analysis Tab ===")

# Check if tab already exists, delete if so, then create
resp = requests.get(f"{BASE}?fields=sheets(properties)", headers=HEADERS)
existing_sheets = resp.json().get("sheets", [])
pareto_exists = None
for s in existing_sheets:
    if "Pareto" in s["properties"]["title"]:
        pareto_exists = s["properties"]["sheetId"]

create_requests = []
if pareto_exists is not None:
    create_requests.append({"deleteSheet": {"sheetId": pareto_exists}})

PARETO_ID = 999  # Arbitrary ID for new sheet
create_requests.append({
    "addSheet": {
        "properties": {
            "sheetId": PARETO_ID,
            "title": "🎯 Pareto Analysis",
            "index": 1,  # Right after Dashboard
            "gridProperties": {
                "rowCount": 200,
                "columnCount": 8,
                "frozenRowCount": 1,
            }
        }
    }
})

result = sheets_batch_update(create_requests)
print(f"Pareto tab created: {result.get('replies', [])}")

# ── Build Pareto Data ─────────────────────────────────────────────────────────
# Revenue total
TOTAL_REV = 14692.09

# Expense categories for Pareto
expenses = [
    ("Meta Ads", 7016.18),
    ("SaaS/Tools", 2661.88),
    ("ATM/Living (Peru)", 2128.49),
    ("Travel", 1049.19),
    ("Wise Transfers", 832.59),
    ("CC Interest (all cards)", 237.23),
    ("Affirm", 179.67),
    ("Student Loan", 106.34),
    ("Annual CC Fee", 95.00),
    ("Subscriptions", 85.47),
    ("FX Fees", 75.36),
    ("SafetyWing Insurance", 66.28),
    ("T-Mobile", 55.66),
    ("ATM Fees", 50.00),
    ("Credit Builder", 48.00),
    ("Bank Fees", 45.00),
]
total_expenses = sum(e[1] for e in expenses)

# SaaS tools for deep dive
saas_tools = [
    ("GoHighLevel", 507.00, "ESSENTIAL"),
    ("Instantly", 283.06, "USEFUL"),
    ("10Web", 272.00, "NICE-TO-HAVE"),
    ("Claude AI", 247.85, "USEFUL"),
    ("Google Ads", 234.80, "ESSENTIAL"),
    ("Lemlist", 189.70, "USEFUL"),
    ("InVideo", 169.91, "NICE-TO-HAVE"),
    ("Google Workspace", 100.57, "ESSENTIAL"),
    ("Exa.AI", 79.00, "NICE-TO-HAVE"),
    ("DataForSEO", 59.00, "USEFUL"),
    ("Higgsfield", 52.02, "NICE-TO-HAVE"),
    ("Lovable", 50.00, "NICE-TO-HAVE"),
    ("Apple (iCloud)", 46.73, "USEFUL"),
    ("Cloudflare", 36.86, "USEFUL"),
    ("HostMyApple", 35.79, "USEFUL"),
    ("MyFICO", 29.95, "NICE-TO-HAVE"),
    ("Spotify", 25.18, "NICE-TO-HAVE"),
    ("RapidURLIndexer", 25.00, "NICE-TO-HAVE"),
    ("Descript", 24.00, "NICE-TO-HAVE"),
    ("WI DFI (State)", 20.00, "ESSENTIAL"),
    ("Cursor IDE", 20.00, "USEFUL"),
    ("OpenAI", 20.00, "USEFUL"),
    ("Traveling Mailbox", 19.95, "USEFUL"),
    ("Supermemory", 19.00, "USEFUL"),
    ("Namecheap", 11.48, "ESSENTIAL"),
    ("Webshare Proxy", 10.68, "USEFUL"),
    ("NordVPN", 8.99, "USEFUL"),
    ("Google One", 1.99, "NICE-TO-HAVE"),
    ("Brave", 1.31, "NICE-TO-HAVE"),
    ("Google Cloud", 1.11, "USEFUL"),
]

saas_total = sum(s[1] for s in saas_tools)

# Revenue sources
revenue_sources = [
    ("Stripe (multiple clients)", 6892.09, 46.9),
    ("A-Z Mobile Apps (Zelle)", 3000.00, 20.4),
    ("ACI Enterprise (Zelle)", 2000.00, 13.6),
    ("Anthony Reddin (Zelle)", 1000.00, 6.8),
    ("Christian Willard (Zelle)", 700.00, 4.8),
    ("Alexander Shtabsky (Zelle)", 500.00, 3.4),
    ("Jonathan Bible (Zelle)", 500.00, 3.4),
    ("Credit Strong", 100.00, 0.7),
]

# Build visual bars
def bar(pct, max_chars=20):
    filled = int(pct / 100 * max_chars)
    return "█" * filled + "░" * (max_chars - filled)

# ── Assemble Pareto tab data ─────────────────────────────────────────────────
pareto_data = []

# Row 0: Title
pareto_data.append(["🎯 PARETO ANALYSIS — January 2026", "", "", "", "", "", "", ""])
pareto_data.append(["Which 20% of spend produces 80% of results?", "", "", "", "", "", "", ""])
pareto_data.append([])

# ── Section A: Revenue Sources ──
pareto_data.append(["SECTION A: REVENUE SOURCES", "", "", "", "", "", "", ""])
pareto_data.append(["Rank", "Source", "Amount", "% of Total", "Cumul. %", "Bar", "", ""])

cum_pct = 0
for i, (name, amt, pct) in enumerate(revenue_sources, 1):
    cum_pct += pct
    pareto_data.append([
        str(i), name, f"${amt:,.2f}", f"{pct:.1f}%", f"{cum_pct:.1f}%", bar(pct, 25), "", ""
    ])

pareto_data.append(["", "TOTAL", f"${TOTAL_REV:,.2f}", "100%", "", "", "", ""])
pareto_data.append([])
pareto_data.append(["💡 KEY INSIGHT: Top 3 sources (Stripe + A-Z + ACI) = 80.9% of revenue", "", "", "", "", "", "", ""])
pareto_data.append(["⚠️ ROAS: $7,016 Meta Ads → $14,692 revenue = 2.1x ROAS (if all ad-attributed)", "", "", "", "", "", "", ""])
pareto_data.append(["❓ Unknown: How much Stripe revenue came from Meta Ads leads vs organic/referral?", "", "", "", "", "", "", ""])
pareto_data.append([])

# ── Section B: Expense Rankings (Pareto) ──
pareto_data.append(["SECTION B: EXPENSE RANKINGS (PARETO)", "", "", "", "", "", "", ""])
pareto_data.append(["Rank", "Category", "Amount", "% of Total", "Cumul. %", "Bar", "80% Line", ""])

cum_pct_exp = 0
for i, (name, amt) in enumerate(expenses, 1):
    pct = amt / total_expenses * 100
    cum_pct_exp += pct
    in_80 = "← TOP 80%" if cum_pct_exp <= 82 else ""
    pareto_data.append([
        str(i), name, f"${amt:,.2f}", f"{pct:.1f}%", f"{cum_pct_exp:.1f}%", bar(pct, 25), in_80, ""
    ])

pareto_data.append(["", "TOTAL EXPENSES", f"${total_expenses:,.2f}", "100%", "", "", "", ""])
pareto_data.append([])

# Count items in top 80%
cum = 0
top_80_count = 0
for name, amt in expenses:
    cum += amt / total_expenses * 100
    top_80_count += 1
    if cum >= 80:
        break

pareto_data.append([f"🔑 TOP {top_80_count} of {len(expenses)} categories ({top_80_count}/{len(expenses)} = {top_80_count/len(expenses)*100:.0f}%) make up 80%+ of all expenses", "", "", "", "", "", "", ""])
pareto_data.append(["The remaining categories are relatively small — focus optimization on the top items", "", "", "", "", "", "", ""])
pareto_data.append([])

# ── Section C: SaaS Deep Dive ──
pareto_data.append(["SECTION C: SaaS DEEP DIVE ($2,661.88/mo)", "", "", "", "", "", "", ""])
pareto_data.append(["Rank", "Tool", "Cost/Mo", "% of SaaS", "Cumul. %", "Classification", "Bar", ""])

cum_saas = 0
essential_total = 0
useful_total = 0
nice_total = 0

for i, (name, amt, cls) in enumerate(saas_tools, 1):
    pct = amt / saas_total * 100
    cum_saas += pct
    if cls == "ESSENTIAL":
        essential_total += amt
    elif cls == "USEFUL":
        useful_total += amt
    else:
        nice_total += amt
    pareto_data.append([
        str(i), name, f"${amt:,.2f}", f"{pct:.1f}%", f"{cum_saas:.1f}%", cls, bar(pct, 20), ""
    ])

pareto_data.append(["", "TOTAL", f"${saas_total:,.2f}", "100%", "", "", "", ""])
pareto_data.append([])
pareto_data.append(["SaaS Classification Summary", "", "", "", "", "", "", ""])
pareto_data.append(["🟢 ESSENTIAL (drives revenue)", "", f"${essential_total:,.2f}", f"{essential_total/saas_total*100:.1f}%", "", f"{len([s for s in saas_tools if s[2]=='ESSENTIAL'])} tools", "", ""])
pareto_data.append(["🟡 USEFUL (saves time)", "", f"${useful_total:,.2f}", f"{useful_total/saas_total*100:.1f}%", "", f"{len([s for s in saas_tools if s[2]=='USEFUL'])} tools", "", ""])
pareto_data.append(["🔴 NICE-TO-HAVE (could cut)", "", f"${nice_total:,.2f}", f"{nice_total/saas_total*100:.1f}%", "", f"{len([s for s in saas_tools if s[2]=='NICE-TO-HAVE'])} tools", "", ""])
pareto_data.append([])
pareto_data.append([f"💡 Cutting all NICE-TO-HAVE saves ${nice_total:,.2f}/mo (${nice_total*12:,.2f}/yr)", "", "", "", "", "", "", ""])
pareto_data.append([f"💡 Top 5 SaaS (GHL, Instantly, 10Web, Claude, Google Ads) = ${507+283.06+272+247.85+234.80:,.2f} = {(507+283.06+272+247.85+234.80)/saas_total*100:.0f}% of SaaS spend", "", "", "", "", "", "", ""])
pareto_data.append([])

# ── Section D: First Principles Profit View ──
pareto_data.append(["SECTION D: FIRST PRINCIPLES PROFIT VIEW", "", "", "", "", "", "", ""])
pareto_data.append(["What does Marko ACTUALLY need to run the business?", "", "", "", "", "", "", ""])
pareto_data.append([])

pareto_data.append(["Tier", "Category", "Items", "Monthly Cost", "", "", "", ""])
pareto_data.append(["🟢 ESSENTIAL", "Revenue-generating", "Meta Ads + GHL + Google Workspace + Google Ads", f"${7016.18 + 507 + 100.57 + 234.80:,.2f}", "", "", "", ""])
pareto_data.append(["🟡 OPERATIONAL", "Business operations", "T-Mobile + SafetyWing + Namecheap + WI DFI", f"${55.66 + 66.28 + 11.48 + 20:,.2f}", "", "", "", ""])
pareto_data.append(["🟠 OUTREACH", "Cold outreach (ROI unclear)", "Lemlist + Instantly + DataForSEO", f"${189.70 + 283.06 + 59:,.2f}", "", "", "", ""])
pareto_data.append(["🔴 OPTIONAL", "Everything else", "All other SaaS + subscriptions", f"${saas_total - (507+100.57+234.80+55.66+66.28+11.48+20+189.70+283.06+59):,.2f}", "", "", "", ""])
pareto_data.append([])

essential_spend = 7016.18 + 507 + 100.57 + 234.80
operational_spend = 55.66 + 66.28 + 11.48 + 20
outreach_spend = 189.70 + 283.06 + 59
optional_spend = saas_total - (507+100.57+234.80+189.70+283.06+59+55.66+66.28+11.48+20)
# Also include non-SaaS expenses
all_biz_expenses = total_expenses  # all expense categories
actual_profit = TOTAL_REV - total_expenses

pareto_data.append(["PROFIT SCENARIOS", "", "", "", "", "", "", ""])
pareto_data.append(["Scenario", "", "Spend", "Profit", "Margin", "", "", ""])
pareto_data.append(["Essential only (Ads + GHL + Workspace + Ads)", "", f"${essential_spend:,.2f}", f"${TOTAL_REV - essential_spend:,.2f}", f"{(TOTAL_REV - essential_spend)/TOTAL_REV*100:.1f}%", "", "", ""])
pareto_data.append(["+ Operational", "", f"${essential_spend + operational_spend:,.2f}", f"${TOTAL_REV - essential_spend - operational_spend:,.2f}", f"{(TOTAL_REV - essential_spend - operational_spend)/TOTAL_REV*100:.1f}%", "", "", ""])
pareto_data.append(["+ Outreach tools", "", f"${essential_spend + operational_spend + outreach_spend:,.2f}", f"${TOTAL_REV - essential_spend - operational_spend - outreach_spend:,.2f}", f"{(TOTAL_REV - essential_spend - operational_spend - outreach_spend)/TOTAL_REV*100:.1f}%", "", "", ""])
pareto_data.append(["Current reality (all expenses)", "", f"${total_expenses:,.2f}", f"${actual_profit:,.2f}", f"{actual_profit/TOTAL_REV*100:.1f}%", "", "", ""])
pareto_data.append([])

# ── Section E: Recommendations ──
pareto_data.append(["SECTION E: RECOMMENDATIONS", "", "", "", "", "", "", ""])
pareto_data.append([])
pareto_data.append(["#", "Recommendation", "Impact", "Priority", "Detail", "", "", ""])
pareto_data.append([
    "1",
    "Track Meta Ads → Revenue Attribution",
    "HIGH",
    "🔴 URGENT",
    "2.1x ROAS ($7k → $14.7k) but which campaigns drive booked calls? Kill underwater campaigns. Could save $1-3k/mo.",
    "", "", ""
])
pareto_data.append([
    "2",
    "SaaS Audit & Cuts",
    "MEDIUM",
    "🟡 THIS WEEK",
    f"${nice_total:,.2f}/mo in NICE-TO-HAVE tools. Is 10Web ($272) generating revenue? InVideo ($170)? Higgsfield ($52)?",
    "", "", ""
])
pareto_data.append([
    "3",
    "Eliminate ATM/FX Fee Waste",
    "LOW",
    "🟢 EASY WIN",
    "$50 ATM + $75 FX = $125/mo wasted. Get Wise or Schwab debit card (no foreign fees). Saves $1,500/yr.",
    "", "", ""
])
pareto_data.append([
    "4",
    "Pay Down CC Debt",
    "MEDIUM",
    "🟡 THIS MONTH",
    "$237/mo in CC interest across all cards. That's $2,844/yr in pure waste. Prioritize 4252 ($165.86 interest + $95 annual fee).",
    "", "", ""
])
pareto_data.append([
    "5",
    "Sapphire Card Review",
    "LOW",
    "🟢 REVIEW",
    "$95 annual fee + $165.86 interest = $260.86/mo cost. If not using travel rewards extensively, downgrade to no-fee card.",
    "", "", ""
])
pareto_data.append([
    "6",
    "Cold Outreach ROI Check",
    "MEDIUM",
    "🟡 THIS WEEK",
    f"Lemlist + Instantly + DataForSEO = ${outreach_spend:,.2f}/mo. How many deals closed from cold outreach vs Meta Ads?",
    "", "", ""
])
pareto_data.append([
    "7",
    "Consolidate Meta Ads to One Card",
    "LOW",
    "🟢 EASY WIN",
    "Ads split across 3 cards ($3,102 + $3,101 + $811). Consolidate to business card for cleaner accounting & rewards.",
    "", "", ""
])
pareto_data.append([])

# Final summary box
pareto_data.append(["═══ BOTTOM LINE ═══", "", "", "", "", "", "", ""])
pareto_data.append([f"Revenue: ${TOTAL_REV:,.2f}  |  Expenses: ${total_expenses:,.2f}  |  Profit: ${actual_profit:,.2f}  |  Margin: {actual_profit/TOTAL_REV*100:.1f}%", "", "", "", "", "", "", ""])
pareto_data.append([f"🎯 Meta Ads = {7016.18/total_expenses*100:.0f}% of spend. If you improve ROAS from 2.1x to 3x, profit doubles.", "", "", "", "", "", "", ""])
pareto_data.append([f"🎯 SaaS = {saas_total/total_expenses*100:.0f}% of spend. Cutting NICE-TO-HAVE saves ${nice_total:,.2f}/mo = ${nice_total*12:,.2f}/yr.", "", "", "", "", "", "", ""])
pareto_data.append([f"🎯 Biggest lever: Know which Meta campaigns produce revenue. Everything else is optimization.", "", "", "", "", "", "", ""])

# Write Pareto data
result = sheets_update("'🎯 Pareto Analysis'!A1", pareto_data)
print(f"Pareto data written: {result.get('updatedCells', 'unknown')} cells")

# ── Pareto Formatting ─────────────────────────────────────────────────────────
print("Applying Pareto formatting...")

pareto_fmt = []

# Title rows
pareto_fmt.append(cell_fmt(fmt_range(PARETO_ID, 0, 1, 0, 8), bg=NAVY, fg=WHITE, bold=True, fontSize=14))
pareto_fmt.append(cell_fmt(fmt_range(PARETO_ID, 1, 2, 0, 8), bg=NAVY, fg=GOLD, bold=True, fontSize=11))

# Find section headers in pareto data
for i, row in enumerate(pareto_data):
    if not row:
        continue
    first = str(row[0])
    
    # Main section headers
    if first.startswith("SECTION "):
        pareto_fmt.append(cell_fmt(fmt_range(PARETO_ID, i, i+1, 0, 8), bg=NAVY, fg=WHITE, bold=True, fontSize=12))
    
    # Column header rows (Rank, Tier, Scenario, #)
    elif first in ("Rank", "Tier", "Scenario", "#") and len(row) > 1 and row[1]:
        pareto_fmt.append(cell_fmt(fmt_range(PARETO_ID, i, i+1, 0, 8), bg=DARK_BG, fg=WHITE, bold=True))
    
    # Insight rows
    elif first.startswith(("💡", "⚠️", "❓", "🔑", "🎯")):
        pareto_fmt.append(cell_fmt(fmt_range(PARETO_ID, i, i+1, 0, 8), bg=YELLOW_BG, bold=True))
    
    # Classification summary
    elif first.startswith("🟢 ESSENTIAL"):
        pareto_fmt.append(cell_fmt(fmt_range(PARETO_ID, i, i+1, 0, 8), bg=LIGHT_GREEN, bold=True))
    elif first.startswith("🟡 USEFUL"):
        pareto_fmt.append(cell_fmt(fmt_range(PARETO_ID, i, i+1, 0, 8), bg=YELLOW_BG, bold=True))
    elif first.startswith("🔴 NICE"):
        pareto_fmt.append(cell_fmt(fmt_range(PARETO_ID, i, i+1, 0, 8), bg=LIGHT_RED, bold=True))
    
    # Total rows
    elif len(row) > 1 and row[1] in ("TOTAL", "TOTAL EXPENSES", "TOTAL SaaS"):
        pareto_fmt.append(cell_fmt(fmt_range(PARETO_ID, i, i+1, 0, 8), bg=LIGHT_BG, bold=True, fontSize=11))
    
    # SaaS Classification Summary header
    elif first == "SaaS Classification Summary":
        pareto_fmt.append(cell_fmt(fmt_range(PARETO_ID, i, i+1, 0, 8), bg=DARK_BG, fg=WHITE, bold=True))
    
    # PROFIT SCENARIOS header
    elif first == "PROFIT SCENARIOS":
        pareto_fmt.append(cell_fmt(fmt_range(PARETO_ID, i, i+1, 0, 8), bg=DARK_BG, fg=WHITE, bold=True, fontSize=11))
    
    # Bottom line
    elif first.startswith("═══"):
        pareto_fmt.append(cell_fmt(fmt_range(PARETO_ID, i, i+1, 0, 8), bg=NAVY, fg=GOLD, bold=True, fontSize=12))
    
    # Profit scenario — current reality row (highlight)
    elif first == "Current reality (all expenses)":
        pareto_fmt.append(cell_fmt(fmt_range(PARETO_ID, i, i+1, 0, 8), bg=LIGHT_RED, bold=True))
    
    # Essential only scenario (highlight green)
    elif "Essential only" in first:
        pareto_fmt.append(cell_fmt(fmt_range(PARETO_ID, i, i+1, 0, 8), bg=LIGHT_GREEN))

# Format recommendation priority cells
for i, row in enumerate(pareto_data):
    if len(row) >= 4 and str(row[3]).startswith("🔴"):
        pareto_fmt.append(cell_fmt(fmt_range(PARETO_ID, i, i+1, 3, 4), bg=LIGHT_RED, bold=True))
    elif len(row) >= 4 and str(row[3]).startswith("🟡"):
        pareto_fmt.append(cell_fmt(fmt_range(PARETO_ID, i, i+1, 3, 4), bg=YELLOW_BG, bold=True))
    elif len(row) >= 4 and str(row[3]).startswith("🟢"):
        pareto_fmt.append(cell_fmt(fmt_range(PARETO_ID, i, i+1, 3, 4), bg=LIGHT_GREEN, bold=True))

# Color-code SaaS classification column in Section C
in_saas_section = False
for i, row in enumerate(pareto_data):
    if not row:
        continue
    if str(row[0]).startswith("SECTION C"):
        in_saas_section = True
        continue
    if str(row[0]).startswith("SECTION D"):
        in_saas_section = False
        continue
    if in_saas_section and len(row) >= 6:
        cls = str(row[5])
        if cls == "ESSENTIAL":
            pareto_fmt.append(cell_fmt(fmt_range(PARETO_ID, i, i+1, 5, 6), bg=LIGHT_GREEN, bold=True))
        elif cls == "USEFUL":
            pareto_fmt.append(cell_fmt(fmt_range(PARETO_ID, i, i+1, 5, 6), bg=YELLOW_BG))
        elif cls == "NICE-TO-HAVE":
            pareto_fmt.append(cell_fmt(fmt_range(PARETO_ID, i, i+1, 5, 6), bg=LIGHT_RED))

# Mark "← TOP 80%" in expense section
for i, row in enumerate(pareto_data):
    if len(row) >= 7 and "TOP 80%" in str(row[6]):
        pareto_fmt.append(cell_fmt(fmt_range(PARETO_ID, i, i+1, 6, 7), fg=RED, bold=True))

# Column widths for Pareto
for col_idx, width in [(0, 120), (1, 320), (2, 120), (3, 100), (4, 100), (5, 200), (6, 120), (7, 80)]:
    pareto_fmt.append({
        "updateDimensionProperties": {
            "range": {
                "sheetId": PARETO_ID,
                "dimension": "COLUMNS",
                "startIndex": col_idx,
                "endIndex": col_idx + 1,
            },
            "properties": {"pixelSize": width},
            "fields": "pixelSize"
        }
    })

# Freeze first row
pareto_fmt.append({
    "updateSheetProperties": {
        "properties": {
            "sheetId": PARETO_ID,
            "gridProperties": {"frozenRowCount": 1}
        },
        "fields": "gridProperties.frozenRowCount"
    }
})

if pareto_fmt:
    result = sheets_batch_update(pareto_fmt)
    print(f"Pareto formatting applied: {len(pareto_fmt)} requests")

print("\n✅ All done! Dashboard updated + Pareto Analysis tab created.")
print(f"Sheet URL: https://docs.google.com/spreadsheets/d/{SHEET_ID}")
