#!/usr/bin/env python3
"""
FIX 2: July 2025 Dashboard — Fix subtotal formatting + restructure sections
Sheet ID: 1fl1VT93SkVjBLV2bss8RN4m45yv5dzC-ATI8JczfVR8
Tab: 📊 Dashboard (sheetId: 0)

Fixes:
1. 18 subtotal rows: navy bg → light gray, white text → black, keep bold
2. Total rows: navy bg → light navy (#E8EDF5)
3. Separate Section G (Account Balances) from H (Assets & Net Worth)
4. Relabel Section H → Section I (Action Items)
5. Add missing personal expense categories (Travel, ATM/Cash/FX)
6. Add TOTAL PERSONAL EXPENSES row
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

SHEET_ID = '1fl1VT93SkVjBLV2bss8RN4m45yv5dzC-ATI8JczfVR8'
TAB_ID = 0  # 📊 Dashboard sheetId
API_BASE = f'https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}'

# === Color constants (RGB 0-1 scale) ===
NAVY = {"red": 27/255, "green": 42/255, "blue": 74/255}      # #1B2A4A
WHITE = {"red": 1.0, "green": 1.0, "blue": 1.0}
BLACK = {"red": 0.0, "green": 0.0, "blue": 0.0}
LIGHT_GRAY = {"red": 243/255, "green": 243/255, "blue": 243/255}  # #F3F3F3
LIGHT_NAVY = {"red": 232/255, "green": 237/255, "blue": 245/255}  # #E8EDF5
DARK_GREEN = {"red": 0, "green": 0.38, "blue": 0}
DARK_RED = {"red": 0.8, "green": 0, "blue": 0}

CURRENCY_FMT = {"type": "NUMBER", "pattern": "$#,##0.00"}

def make_cell(value, bg=None, fg=None, bold=False, font_size=10, number_format=None):
    cell = {
        "userEnteredValue": {},
        "userEnteredFormat": {
            "textFormat": {"bold": bold, "fontSize": font_size}
        }
    }
    if isinstance(value, (int, float)):
        cell["userEnteredValue"]["numberValue"] = value
    else:
        cell["userEnteredValue"]["stringValue"] = str(value)
    if bg:
        cell["userEnteredFormat"]["backgroundColor"] = bg
    if fg:
        cell["userEnteredFormat"]["textFormat"]["foregroundColor"] = fg
    if number_format:
        cell["userEnteredFormat"]["numberFormat"] = number_format
    return cell

def section_header_row(text):
    cells = [make_cell(text, bg=NAVY, fg=WHITE, bold=True, font_size=14)]
    for _ in range(3):
        cells.append(make_cell("", bg=NAVY))
    return {"values": cells}

def column_header_row(headers):
    cells = [make_cell(h, bg=LIGHT_GRAY, fg=BLACK, bold=True) for h in headers]
    return {"values": cells}

def subtotal_row(text, amount):
    fg = DARK_RED if amount < 0 else (DARK_GREEN if amount > 0 else BLACK)
    return {"values": [
        make_cell("", bg=LIGHT_GRAY),
        make_cell("", bg=LIGHT_GRAY),
        make_cell(text, bg=LIGHT_GRAY, fg=BLACK, bold=True),
        make_cell(amount, bg=LIGHT_GRAY, fg=fg, bold=True, number_format=CURRENCY_FMT),
    ]}

def total_row(text, amount):
    fg = DARK_RED if amount < 0 else (DARK_GREEN if amount > 0 else BLACK)
    return {"values": [
        make_cell(text, bg=LIGHT_NAVY, fg=BLACK, bold=True),
        make_cell("", bg=LIGHT_NAVY),
        make_cell("", bg=LIGHT_NAVY),
        make_cell(amount, bg=LIGHT_NAVY, fg=fg, bold=True, number_format=CURRENCY_FMT),
    ]}

def data_row_4col(vals, currency_cols=None):
    if currency_cols is None:
        currency_cols = set()
    cells = []
    for i, v in enumerate(vals):
        if i in currency_cols and isinstance(v, (int, float)):
            fg = DARK_RED if v < 0 else (DARK_GREEN if v > 0 else BLACK)
            cells.append(make_cell(v, fg=fg, number_format=CURRENCY_FMT))
        else:
            cells.append(make_cell(v))
    return {"values": cells}

def blank_row():
    return {"values": [make_cell("") for _ in range(4)]}

# ============================================================
# Build all requests for batchUpdate
# ============================================================
reqs = []

# ============================================================
# PHASE 1: Insert rows for missing categories in Section C
# ============================================================
# Insert 6 rows after row 154 (0-indexed: at index 154)
# Current row 153 (0-idx) = Shopping Subtotal (last Section C content)
# Current row 154 (0-idx) = blank
# Current row 155 (0-idx) = Section D header
N_CAT = 6  # rows to insert for categories
reqs.append({
    "insertDimension": {
        "range": {
            "sheetId": TAB_ID,
            "dimension": "ROWS",
            "startIndex": 154,
            "endIndex": 154 + N_CAT
        },
        "inheritFromBefore": True
    }
})

# After this insert, rows 154+ shift by N_CAT=6
# Old row 154 → now 160
# Old row 155 (Section D) → now 161

# ============================================================
# PHASE 2: Insert rows for Section G: Account Balances
# ============================================================
# Old row 192 (Section G header) was shifted by N_CAT → now at 198
# Insert 9 rows at index 198 (before the Section G header)
N_BAL = 9
reqs.append({
    "insertDimension": {
        "range": {
            "sheetId": TAB_ID,
            "dimension": "ROWS",
            "startIndex": 198,
            "endIndex": 198 + N_BAL
        },
        "inheritFromBefore": True
    }
})

# After this insert:
# - Old Section G header (at 198 after phase 1) → now at 198+9=207
# - Old Section H header (at 212 after phase 1) → now at 212+9=221

# ============================================================
# PHASE 3: Write missing category data at rows 154-159
# ============================================================
cat_rows = [
    # Travel category
    {"values": [
        make_cell("✈️ Travel", bold=True),
        make_cell(""),
        make_cell(""),
        make_cell(""),
    ]},
    subtotal_row("Travel Subtotal", 0.00),
    # ATM / Cash / FX Fees
    {"values": [
        make_cell("🏧 ATM / Cash / FX Fees", bold=True),
        make_cell(""),
        make_cell(""),
        make_cell(""),
    ]},
    subtotal_row("ATM / Cash / FX Subtotal", 0.00),
    blank_row(),
    # Total Personal Expenses
    total_row("TOTAL PERSONAL EXPENSES", -6534.93),
]

reqs.append({
    "updateCells": {
        "rows": cat_rows,
        "fields": "userEnteredValue,userEnteredFormat",
        "start": {"sheetId": TAB_ID, "rowIndex": 154, "columnIndex": 0}
    }
})

# ============================================================
# PHASE 4: Write Section G: Account Balances at rows 198-206
# ============================================================
acct_rows = [
    section_header_row("💰 SECTION G: ACCOUNT BALANCES"),
    column_header_row(["Account", "Opening", "Closing", "Change"]),
    # Business 4991: Opening ~$3,530, Closing ~$2,957
    data_row_4col(["Chase Biz 4991", 3530.00, 2956.79, -573.21], currency_cols={1, 2, 3}),
    # Personal 0068: Opening ~$1,000, Closing ~$639
    data_row_4col(["Chase Personal 0068", 1000.00, 638.98, -361.02], currency_cols={1, 2, 3}),
    # Savings 7036: net -$510 ($490 in, $1000 out)
    data_row_4col(["Chase Savings 7036", 2000.00, 1510.00, -490.00], currency_cols={1, 2, 3}),
    # Total
    total_row("TOTAL CASH", 5105.77),
    blank_row(),
    blank_row(),
    blank_row(),
]

reqs.append({
    "updateCells": {
        "rows": acct_rows,
        "fields": "userEnteredValue,userEnteredFormat",
        "start": {"sheetId": TAB_ID, "rowIndex": 198, "columnIndex": 0}
    }
})

# Merge Section G header
reqs.append({
    "mergeCells": {
        "range": {
            "sheetId": TAB_ID,
            "startRowIndex": 198,
            "endRowIndex": 199,
            "startColumnIndex": 0,
            "endColumnIndex": 4
        },
        "mergeType": "MERGE_ALL"
    }
})

# ============================================================
# PHASE 5: Update Section G → H header (now at row 207)
# ============================================================
reqs.append({
    "updateCells": {
        "rows": [{"values": [
            make_cell("💎 SECTION H: ASSETS & NET WORTH", bg=NAVY, fg=WHITE, bold=True, font_size=14)
        ]}],
        "fields": "userEnteredValue,userEnteredFormat",
        "start": {"sheetId": TAB_ID, "rowIndex": 207, "columnIndex": 0}
    }
})

# ============================================================
# PHASE 6: Update Section H → I header (now at row 221)
# ============================================================
reqs.append({
    "updateCells": {
        "rows": [{"values": [
            make_cell("📝 SECTION I: ACTION ITEMS", bg=NAVY, fg=WHITE, bold=True, font_size=14)
        ]}],
        "fields": "userEnteredValue,userEnteredFormat",
        "start": {"sheetId": TAB_ID, "rowIndex": 221, "columnIndex": 0}
    }
})

# ============================================================
# PHASE 7: Fix 18 subtotal rows formatting
# ============================================================
# These rows are all at indices < 154, so they didn't shift
# 0-indexed row indices:
SUBTOTAL_ROWS = [47, 61, 65, 74, 78, 82, 90, 101, 113, 117, 122, 127, 131, 138, 143, 146, 149, 153]

print(f"Fixing {len(SUBTOTAL_ROWS)} subtotal rows")

for row_idx in SUBTOTAL_ROWS:
    reqs.append({
        "repeatCell": {
            "range": {
                "sheetId": TAB_ID,
                "startRowIndex": row_idx,
                "endRowIndex": row_idx + 1,
                "startColumnIndex": 0,
                "endColumnIndex": 4
            },
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": LIGHT_GRAY,
                    "textFormat": {
                        "foregroundColor": BLACK,
                        "bold": True,
                        "fontSize": 10
                    }
                }
            },
            "fields": "userEnteredFormat.backgroundColor,userEnteredFormat.textFormat"
        }
    })

# ============================================================
# PHASE 8: Fix total/summary rows formatting
# ============================================================
# These need #E8EDF5 (light navy) background with black text
# Row 83 (0-idx): TOTAL BUSINESS EXPENSES — no shift
# Rows 165-167 (0-idx): Total SaaS/Tools, SEO, Marketing — shifted by 6 → 171-173
# Rows 186-187 (0-idx): Total CC Debt, Total Debt — shifted by 6 → 192-193

TOTAL_ROWS = [83, 171, 172, 173, 192, 193]

print(f"Fixing {len(TOTAL_ROWS)} total rows")

for row_idx in TOTAL_ROWS:
    reqs.append({
        "repeatCell": {
            "range": {
                "sheetId": TAB_ID,
                "startRowIndex": row_idx,
                "endRowIndex": row_idx + 1,
                "startColumnIndex": 0,
                "endColumnIndex": 4
            },
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": LIGHT_NAVY,
                    "textFormat": {
                        "foregroundColor": BLACK,
                        "bold": True,
                        "fontSize": 10
                    }
                }
            },
            "fields": "userEnteredFormat.backgroundColor,userEnteredFormat.textFormat"
        }
    })

# ============================================================
# PHASE 9: Fix TOTAL INCOME row (row 13, 0-indexed)
# ============================================================
# Row 14 (1-indexed) / 13 (0-indexed) had white bg and wasn't bold
reqs.append({
    "repeatCell": {
        "range": {
            "sheetId": TAB_ID,
            "startRowIndex": 13,
            "endRowIndex": 14,
            "startColumnIndex": 0,
            "endColumnIndex": 6
        },
        "cell": {
            "userEnteredFormat": {
                "backgroundColor": LIGHT_NAVY,
                "textFormat": {
                    "foregroundColor": BLACK,
                    "bold": True,
                    "fontSize": 11
                }
            }
        },
        "fields": "userEnteredFormat.backgroundColor,userEnteredFormat.textFormat"
    }
})

# ============================================================
# Execute batchUpdate
# ============================================================
print(f"\nTotal requests: {len(reqs)}")

body = {"requests": reqs}
url = f'{API_BASE}:batchUpdate'
resp = requests.post(url, headers=HEADERS, json=body)

if resp.status_code == 200:
    print("✅ July 2025 dashboard updated successfully!")
    print(f"   Fixed {len(SUBTOTAL_ROWS)} subtotal rows (navy → light gray)")
    print(f"   Fixed {len(TOTAL_ROWS)} total rows (navy → light navy)")
    print(f"   Added missing categories: ✈️ Travel, 🏧 ATM/Cash/FX")
    print(f"   Added TOTAL PERSONAL EXPENSES row")
    print(f"   Added Section G: Account Balances")
    print(f"   Relabeled Section G → H (Assets & Net Worth)")
    print(f"   Relabeled Section H → I (Action Items)")
else:
    print(f"❌ Error: {resp.status_code}")
    print(resp.text[:2000])
