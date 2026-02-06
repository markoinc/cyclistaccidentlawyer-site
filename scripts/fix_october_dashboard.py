#!/usr/bin/env python3
"""
FIX 1: October 2025 Dashboard — Add missing sections F-I
Sheet ID: 1g403GZFVxpF2Siys_1Kpk_sTnOZZEb0-Xibfmiz16dA
Tab: 📊 Dashboard (sheetId: 538068003)

Dashboard currently ends at row 199 (Section E: Money Flow).
Need to add: F (Debt Tracking), G (Account Balances), H (Assets & Net Worth), I (Action Items)
"""
import requests
import json

# === OAuth ===
r = requests.post('https://oauth2.googleapis.com/token', data={
    'client_id': '838433184423-1sd6hs0m7m7mrvm63f1sct2ovjhs88ut.apps.googleusercontent.com',
    'client_secret': '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',
    'refresh_token': '1//05PmAu-vBTVrWCgYIARAAGAUSNwF-L9Irl-dM7iPoS4XocG_eO32bhNSfNYM0rfwGMKBi-KwJYCpzpAlXYINO04lXIWVAAHmh0qw',
    'grant_type': 'refresh_token'
})
TOKEN = r.json()['access_token']
HEADERS = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}

SHEET_ID = '1g403GZFVxpF2Siys_1Kpk_sTnOZZEb0-Xibfmiz16dA'
TAB_ID = 538068003  # 📊 Dashboard sheetId
API_BASE = f'https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}'

# === Color constants ===
NAVY = {"red": 0.106, "green": 0.165, "blue": 0.290}        # #1B2A4A
WHITE = {"red": 1, "green": 1, "blue": 1}
BLACK = {"red": 0, "green": 0, "blue": 0}
LIGHT_GRAY = {"red": 0.953, "green": 0.953, "blue": 0.953}   # #F3F3F3
LIGHT_NAVY = {"red": 0.910, "green": 0.929, "blue": 0.961}   # #E8EDF5
DARK_GREEN = {"red": 0, "green": 0.38, "blue": 0}             # #006100
DARK_RED = {"red": 0.8, "green": 0, "blue": 0}                # #CC0000

# === Data from transaction tabs ===
# Business 4991: Opening (Oct 1) = $1,365.33, Closing (Oct 31) = $1,473.58
# Personal 0068: Opening (Oct 1) = $302.23, Closing (Oct 31) = $1,036.46
# Sapphire 4252: Interest $165.48, Payment $262.00
# Ink CC 0678: Payment $91 + $102 = $193
# Student Loan payment: $106.34
# Discover payment: $122.00

# Debt estimates (from July 2025 data + October payments/interest):
# Student Loans: July was $9,213.98, ~3 months of $106.34 payments = ~$8,894
# Discover 6820: July was $5,967, payments ~$122/mo x3 + interest ≈ ~$5,800
# Sapphire 4252: July was $7,538.46, payment $262/mo x3, interest ~$165/mo x3 ≈ ~$7,250
# Ink 0678: July was $2,665.99, charges minus payments ≈ ~$3,100

def make_cell(value, bg=None, fg=None, bold=False, font_size=10, h_align=None, number_format=None):
    """Create a cell data object."""
    cell = {
        "userEnteredValue": {},
        "userEnteredFormat": {
            "textFormat": {
                "bold": bold,
                "fontSize": font_size
            }
        }
    }
    # Set value
    if isinstance(value, (int, float)):
        cell["userEnteredValue"]["numberValue"] = value
    elif value == "":
        cell["userEnteredValue"]["stringValue"] = ""
    else:
        cell["userEnteredValue"]["stringValue"] = str(value)
    
    # Colors
    if bg:
        cell["userEnteredFormat"]["backgroundColor"] = bg
    if fg:
        cell["userEnteredFormat"]["textFormat"]["foregroundColor"] = fg
    
    # Alignment
    if h_align:
        cell["userEnteredFormat"]["horizontalAlignment"] = h_align
    
    # Number format
    if number_format:
        cell["userEnteredFormat"]["numberFormat"] = number_format
    
    return cell

CURRENCY_FMT = {"type": "NUMBER", "pattern": "$#,##0.00"}
PERCENT_FMT = {"type": "PERCENT", "pattern": "0%"}

def section_header_row(text):
    """Create a section header row (navy bg, white text, 14pt bold)."""
    cells = [make_cell(text, bg=NAVY, fg=WHITE, bold=True, font_size=14)]
    # Fill remaining columns with navy background
    for _ in range(5):
        cells.append(make_cell("", bg=NAVY))
    return {"values": cells}

def column_header_row(headers):
    """Create a column header row (light gray bg, bold)."""
    cells = []
    for h in headers:
        cells.append(make_cell(h, bg=LIGHT_GRAY, fg=BLACK, bold=True))
    # Pad to 6 columns
    while len(cells) < 6:
        cells.append(make_cell("", bg=LIGHT_GRAY))
    return {"values": cells}

def data_row(values, number_cols=None, currency_cols=None, percent_cols=None):
    """Create a data row with optional number formatting."""
    if number_cols is None: number_cols = set()
    if currency_cols is None: currency_cols = set()
    if percent_cols is None: percent_cols = set()
    cells = []
    for i, v in enumerate(values):
        if i in currency_cols and isinstance(v, (int, float)):
            fg = DARK_RED if v < 0 else (DARK_GREEN if v > 0 else BLACK)
            cells.append(make_cell(v, fg=fg, number_format=CURRENCY_FMT))
        elif i in percent_cols and isinstance(v, (int, float)):
            cells.append(make_cell(v, number_format=PERCENT_FMT))
        else:
            cells.append(make_cell(v))
    # Pad to 6 columns
    while len(cells) < 6:
        cells.append(make_cell(""))
    return {"values": cells}

def total_row(values, currency_cols=None):
    """Create a total row (light navy bg, bold)."""
    if currency_cols is None: currency_cols = set()
    cells = []
    for i, v in enumerate(values):
        if i in currency_cols and isinstance(v, (int, float)):
            fg = DARK_RED if v < 0 else (DARK_GREEN if v > 0 else BLACK)
            cells.append(make_cell(v, bg=LIGHT_NAVY, fg=fg, bold=True, number_format=CURRENCY_FMT))
        else:
            cells.append(make_cell(v, bg=LIGHT_NAVY, fg=BLACK, bold=True))
    while len(cells) < 6:
        cells.append(make_cell("", bg=LIGHT_NAVY))
    return {"values": cells}

def blank_row():
    """Create a blank row."""
    return {"values": [make_cell("") for _ in range(6)]}

# === Build all rows for Sections F-I ===
all_rows = []

# 2 blank rows before Section F
all_rows.append(blank_row())
all_rows.append(blank_row())

# ===== SECTION F: DEBT TRACKING =====
all_rows.append(section_header_row("🏦 SECTION F: DEBT TRACKING"))
all_rows.append(column_header_row(["Account", "Balance", "Limit", "Utilization", "Min Payment", "Actual Payment"]))

# Student Loans
all_rows.append(data_row(["Student Loans", -8894, "", "", "", -106.34], currency_cols={1, 4, 5}))
# Discover 6820
all_rows.append(data_row(["Discover 6820", -5800, 6300, 0.92, "", -122], currency_cols={1, 2, 4, 5}, percent_cols={3}))
# Sapphire 4252
all_rows.append(data_row(["Sapphire 4252", -7250, 9300, 0.78, "", -262], currency_cols={1, 2, 4, 5}, percent_cols={3}))
# Ink CC 0678
all_rows.append(data_row(["Ink CC 0678", -3100, 5500, 0.56, "", -193], currency_cols={1, 2, 4, 5}, percent_cols={3}))
# Total row
all_rows.append(total_row(["TOTAL DEBT", -25044, "", "", "", -683.34], currency_cols={1, 5}))

# 2 blank rows
all_rows.append(blank_row())
all_rows.append(blank_row())

# ===== SECTION G: ACCOUNT BALANCES =====
all_rows.append(section_header_row("💰 SECTION G: ACCOUNT BALANCES"))
all_rows.append(column_header_row(["Account", "Opening", "Closing", "Change", "Notes", ""]))

# Business 4991
change_biz = 1473.58 - 1365.33
all_rows.append(data_row(["Chase Biz 4991", 1365.33, 1473.58, change_biz, ""], currency_cols={1, 2, 3}))
# Personal 0068
change_per = 1036.46 - 302.23
all_rows.append(data_row(["Chase Personal 0068", 302.23, 1036.46, change_per, ""], currency_cols={1, 2, 3}))
# Savings (estimated from money flow: $305 transferred to savings)
all_rows.append(data_row(["Chase Savings 7036", 1500, 1805, 305, "Estimated"], currency_cols={1, 2, 3}))
# Total
all_rows.append(total_row(["TOTAL CASH", 3167.56, 4315.04, change_biz + change_per + 305, ""], currency_cols={1, 2, 3}))

# 2 blank rows
all_rows.append(blank_row())
all_rows.append(blank_row())

# ===== SECTION H: ASSETS & NET WORTH =====
all_rows.append(section_header_row("💎 SECTION H: ASSETS & NET WORTH"))
all_rows.append(column_header_row(["Asset", "Value", "Change", "Notes", "", ""]))

all_rows.append(data_row(["Business Equity", 150000, "", "Rank & rent portfolio"], currency_cols={1}))
all_rows.append(data_row(["Robinhood", 2500, "", "Stocks"], currency_cols={1}))
all_rows.append(data_row(["Acorns", 400, "", "Index funds"], currency_cols={1}))
all_rows.append(data_row(["Bitcoin", 1500, "", ""], currency_cols={1}))
all_rows.append(data_row(["Solana", 2200, "", ""], currency_cols={1}))
all_rows.append(data_row(["Cash (all accounts)", 4315.04, "", "Sum of Section G"], currency_cols={1}))

# Totals
all_rows.append(total_row(["TOTAL ASSETS", 160915.04, "", ""], currency_cols={1}))
all_rows.append(total_row(["TOTAL LIABILITIES", -25044, "", "From Section F"], currency_cols={1}))
all_rows.append(total_row(["NET WORTH", 135871.04, "", ""], currency_cols={1}))

# 2 blank rows
all_rows.append(blank_row())
all_rows.append(blank_row())

# ===== SECTION I: ACTION ITEMS =====
all_rows.append(section_header_row("📝 SECTION I: ACTION ITEMS"))
all_rows.append(column_header_row(["Priority", "Action", "Status", "Due", "Notes", ""]))

all_rows.append(data_row(["🔴 HIGH", "Pay down Discover CC (92% utilization)", "⬜", "", "Highest utilization — reduce to <50%"]))
all_rows.append(data_row(["🔴 HIGH", "Cancel unused SaaS subscriptions", "⬜", "", "Review $1,275 SaaS spend"]))
all_rows.append(data_row(["🟡 MED", "Reduce ATM withdrawal fees ($30 in fees)", "⬜", "", "Use local bank or get fee-free card"]))
all_rows.append(data_row(["🟡 MED", "Track Stripe deposits vs CC processing fees", "⬜", "", "Ensure net positive per client"]))
all_rows.append(data_row(["🟢 LOW", "Set up auto-pay for Discover CC", "⬜", "", "Avoid late payment risk"]))

print(f"Total rows to append: {len(all_rows)}")

# === Step 1: Write values using spreadsheets.values.append ===
# First, let's use updateCells via batchUpdate for full formatting control

# Build the batchUpdate request
requests_list = []

# We start writing at row 200 (0-indexed: 199)
START_ROW = 199  # 0-indexed

# updateCells request to write all rows with formatting
requests_list.append({
    "updateCells": {
        "rows": all_rows,
        "fields": "userEnteredValue,userEnteredFormat",
        "start": {
            "sheetId": TAB_ID,
            "rowIndex": START_ROW,
            "columnIndex": 0
        }
    }
})

# === Merge cells for section headers ===
# Section headers need to be merged across all 6 columns
# Calculate which rows are section headers (relative to START_ROW)
section_header_offsets = []
for i, row in enumerate(all_rows):
    if row["values"] and len(row["values"]) > 0:
        val = row["values"][0].get("userEnteredValue", {}).get("stringValue", "")
        if "SECTION" in val:
            section_header_offsets.append(i)

print(f"Section header offsets: {section_header_offsets}")

for offset in section_header_offsets:
    row_idx = START_ROW + offset
    requests_list.append({
        "mergeCells": {
            "range": {
                "sheetId": TAB_ID,
                "startRowIndex": row_idx,
                "endRowIndex": row_idx + 1,
                "startColumnIndex": 0,
                "endColumnIndex": 6
            },
            "mergeType": "MERGE_ALL"
        }
    })

# === Execute batchUpdate ===
body = {"requests": requests_list}
url = f'{API_BASE}:batchUpdate'
resp = requests.post(url, headers=HEADERS, json=body)

if resp.status_code == 200:
    print("✅ October 2025 dashboard updated successfully!")
    print(f"   Added {len(all_rows)} rows starting at row {START_ROW + 1}")
    print(f"   Sections added: F (Debt Tracking), G (Account Balances), H (Assets & Net Worth), I (Action Items)")
else:
    print(f"❌ Error: {resp.status_code}")
    print(resp.text[:1000])
