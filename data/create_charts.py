#!/usr/bin/env python3
"""Create 8 charts + sparklines on the All Time Financial Overview Google Sheet."""

import requests
import json
import sys

# === AUTH ===
r = requests.post('https://oauth2.googleapis.com/token', data={
    'client_id': '838433184423-1sd6hs0m7m7mrvm63f1sct2ovjhs88ut.apps.googleusercontent.com',
    'client_secret': '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',
    'refresh_token': '1//05PmAu-vBTVrWCgYIARAAGAUSNwF-L9Irl-dM7iPoS4XocG_eO32bhNSfNYM0rfwGMKBi-KwJYCpzpAlXYINO04lXIWVAAHmh0qw',
    'grant_type': 'refresh_token'
})
TOKEN = r.json()['access_token']
print(f"✅ Got token: {TOKEN[:20]}...")

SHEET_ID = '1v1di5lJT-84iMD7FfnKGFfWanFV-5gyWXWR5mGJuJZQ'
BASE_URL = f'https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}'
HEADERS = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}

# === CONSTANTS ===
DASHBOARD_SID = 0
CHARTS_SID = 100

# Colors (RGB 0-1 floats)
INDIGO  = {"red": 0.388, "green": 0.400, "blue": 0.945}
GREEN   = {"red": 0.133, "green": 0.773, "blue": 0.369}
RED     = {"red": 0.937, "green": 0.267, "blue": 0.267}
CYAN    = {"red": 0.024, "green": 0.714, "blue": 0.831}
AMBER   = {"red": 0.961, "green": 0.620, "blue": 0.043}
PURPLE  = {"red": 0.545, "green": 0.361, "blue": 0.965}
WHITE   = {"red": 1.0, "green": 1.0, "blue": 1.0}
NAVY    = {"red": 0.106, "green": 0.165, "blue": 0.290}
DARK_BG = {"red": 0.110, "green": 0.110, "blue": 0.122}
LIGHT_GRAY = {"red": 0.95, "green": 0.95, "blue": 0.95}

# === HELPERS ===
def grid_range(sheet_id, start_row, end_row, start_col, end_col):
    """0-indexed grid range."""
    return {
        "sheetId": sheet_id,
        "startRowIndex": start_row,
        "endRowIndex": end_row,
        "startColumnIndex": start_col,
        "endColumnIndex": end_col
    }

def chart_position(sheet_id, row, col, width=600, height=400):
    return {
        "overlayPosition": {
            "anchorCell": {
                "sheetId": sheet_id,
                "rowIndex": row,
                "columnIndex": col
            },
            "offsetXPixels": 0,
            "offsetYPixels": 0,
            "widthPixels": width,
            "heightPixels": height
        }
    }

def api_call(method, url, json_data=None):
    """Make API call with error handling."""
    if method == 'POST':
        resp = requests.post(url, headers=HEADERS, json=json_data)
    elif method == 'PUT':
        resp = requests.put(url, headers=HEADERS, json=json_data)
    elif method == 'GET':
        resp = requests.get(url, headers=HEADERS)
    else:
        raise ValueError(f"Unknown method: {method}")
    
    if resp.status_code not in (200, 201):
        print(f"❌ API Error {resp.status_code}: {resp.text[:500]}")
        return None
    return resp.json()

# ============================================================
# STEP 1: Create 📈 Charts tab
# ============================================================
print("\n📊 Step 1: Creating Charts tab...")

result = api_call('POST', f'{BASE_URL}:batchUpdate', {
    "requests": [{
        "addSheet": {
            "properties": {
                "sheetId": CHARTS_SID,
                "title": "📈 Charts",
                "index": 1,
                "tabColor": {
                    "red": 0.984,
                    "green": 0.737,
                    "blue": 0.016
                }
            }
        }
    }]
})

if result:
    print("✅ Charts tab created")
else:
    print("⚠️ Charts tab may already exist, continuing...")

# ============================================================
# STEP 2: Write helper data
# ============================================================
print("\n📝 Step 2: Writing helper data...")

# 2a: Annual comparison data on Charts tab (M1:P4)
annual_data = [
    ["Year", "Revenue", "Expenses", "Net Profit"],
    ["2024", 25634.14, 44000.72, -18366.58],
    ["2025", 80201.66, 41120.87, 39080.79],
    ["2026 YTD", 10468.89, 11312.42, -843.53]
]

result = api_call('PUT', 
    f'{BASE_URL}/values/%F0%9F%93%88%20Charts!M1:P4?valueInputOption=RAW',
    {"values": annual_data}
)
if result:
    print("✅ Annual comparison data written to Charts!M1:P4")

# 2b: 50% target line on Dashboard G20:G45 (for profit margin chart)
target_data = [["50% Target"]] + [[0.5]] * 25  # header + 25 data rows
result = api_call('PUT',
    f'{BASE_URL}/values/%F0%9F%8C%90%20All%20Time%20Dashboard!G20:G45?valueInputOption=RAW',
    {"values": target_data}
)
if result:
    print("✅ 50% target line written to Dashboard!G20:G45")

# ============================================================
# STEP 3: Build all 8 charts
# ============================================================
print("\n📈 Step 3: Creating all 8 charts...")

chart_requests = []

# --- CHART 1: Monthly Revenue & Expenses (Line Chart) ---
# Dashboard data: Row 20 header, Rows 21-45 data (0-indexed: 19-44)
# Col A=Month(0), B=Revenue(1), C=Expenses(2)
chart_requests.append({
    "addChart": {
        "chart": {
            "spec": {
                "title": "Monthly Revenue & Expenses",
                "titleTextFormat": {"fontFamily": "Arial", "fontSize": 14, "bold": True},
                "basicChart": {
                    "chartType": "LINE",
                    "legendPosition": "BOTTOM_LEGEND",
                    "axis": [
                        {
                            "position": "BOTTOM_AXIS",
                            "title": "Month",
                            "format": {"fontFamily": "Arial", "fontSize": 10}
                        },
                        {
                            "position": "LEFT_AXIS",
                            "title": "Amount ($)",
                            "format": {"fontFamily": "Arial", "fontSize": 10}
                        }
                    ],
                    "domains": [{
                        "domain": {
                            "sourceRange": {
                                "sources": [grid_range(DASHBOARD_SID, 19, 45, 0, 1)]
                            }
                        }
                    }],
                    "series": [
                        {
                            "series": {
                                "sourceRange": {
                                    "sources": [grid_range(DASHBOARD_SID, 19, 45, 1, 2)]
                                }
                            },
                            "targetAxis": "LEFT_AXIS",
                            "color": INDIGO,
                            "lineStyle": {"width": 3}
                        },
                        {
                            "series": {
                                "sourceRange": {
                                    "sources": [grid_range(DASHBOARD_SID, 19, 45, 2, 3)]
                                }
                            },
                            "targetAxis": "LEFT_AXIS",
                            "color": RED,
                            "lineStyle": {"width": 3}
                        }
                    ],
                    "headerCount": 1
                }
            },
            "position": chart_position(CHARTS_SID, 2, 0)
        }
    }
})
print("  📊 Chart 1: Monthly Revenue & Expenses")

# --- CHART 2: Monthly Net Profit (Column Chart) ---
# Col D=Profit(3)
chart_requests.append({
    "addChart": {
        "chart": {
            "spec": {
                "title": "Monthly Net Profit",
                "titleTextFormat": {"fontFamily": "Arial", "fontSize": 14, "bold": True},
                "basicChart": {
                    "chartType": "COLUMN",
                    "legendPosition": "BOTTOM_LEGEND",
                    "axis": [
                        {
                            "position": "BOTTOM_AXIS",
                            "title": "Month",
                            "format": {"fontFamily": "Arial", "fontSize": 10}
                        },
                        {
                            "position": "LEFT_AXIS",
                            "title": "Profit ($)",
                            "format": {"fontFamily": "Arial", "fontSize": 10}
                        }
                    ],
                    "domains": [{
                        "domain": {
                            "sourceRange": {
                                "sources": [grid_range(DASHBOARD_SID, 19, 45, 0, 1)]
                            }
                        }
                    }],
                    "series": [{
                        "series": {
                            "sourceRange": {
                                "sources": [grid_range(DASHBOARD_SID, 19, 45, 3, 4)]
                            }
                        },
                        "targetAxis": "LEFT_AXIS",
                        "color": GREEN
                    }],
                    "headerCount": 1
                }
            },
            "position": chart_position(CHARTS_SID, 2, 7)
        }
    }
})
print("  📊 Chart 2: Monthly Net Profit")

# --- CHART 3: Revenue by Business Line (Pie Chart) ---
# Dashboard rows 13-15 (0-indexed: 12-14), Col A=Label(0), Col E=All Time(4)
chart_requests.append({
    "addChart": {
        "chart": {
            "spec": {
                "title": "Revenue by Business Line",
                "titleTextFormat": {"fontFamily": "Arial", "fontSize": 14, "bold": True},
                "pieChart": {
                    "legendPosition": "RIGHT_LEGEND",
                    "domain": {
                        "sourceRange": {
                            "sources": [grid_range(DASHBOARD_SID, 12, 15, 0, 1)]
                        }
                    },
                    "series": {
                        "sourceRange": {
                            "sources": [grid_range(DASHBOARD_SID, 12, 15, 4, 5)]
                        }
                    },
                    "threeDimensional": False
                }
            },
            "position": chart_position(CHARTS_SID, 24, 0)
        }
    }
})
print("  📊 Chart 3: Revenue by Business Line")

# --- CHART 4: Expense Breakdown (Donut Chart) ---
# Dashboard rows 51-56 (0-indexed: 50-55), Col A=Category(0), Col E=All Time(4)
chart_requests.append({
    "addChart": {
        "chart": {
            "spec": {
                "title": "Expense Breakdown (All Time)",
                "titleTextFormat": {"fontFamily": "Arial", "fontSize": 14, "bold": True},
                "pieChart": {
                    "legendPosition": "RIGHT_LEGEND",
                    "domain": {
                        "sourceRange": {
                            "sources": [grid_range(DASHBOARD_SID, 50, 56, 0, 1)]
                        }
                    },
                    "series": {
                        "sourceRange": {
                            "sources": [grid_range(DASHBOARD_SID, 50, 56, 4, 5)]
                        }
                    },
                    "threeDimensional": False,
                    "pieHole": 0.4
                }
            },
            "position": chart_position(CHARTS_SID, 24, 7)
        }
    }
})
print("  📊 Chart 4: Expense Breakdown")

# --- CHART 5: Profit Margin Trend (Line Chart with 50% target) ---
# Dashboard rows 20-45, Col E=Margin(4), Col G=50% Target(6)
chart_requests.append({
    "addChart": {
        "chart": {
            "spec": {
                "title": "Profit Margin Trend",
                "titleTextFormat": {"fontFamily": "Arial", "fontSize": 14, "bold": True},
                "basicChart": {
                    "chartType": "LINE",
                    "legendPosition": "BOTTOM_LEGEND",
                    "axis": [
                        {
                            "position": "BOTTOM_AXIS",
                            "title": "Month",
                            "format": {"fontFamily": "Arial", "fontSize": 10}
                        },
                        {
                            "position": "LEFT_AXIS",
                            "title": "Margin",
                            "format": {"fontFamily": "Arial", "fontSize": 10}
                        }
                    ],
                    "domains": [{
                        "domain": {
                            "sourceRange": {
                                "sources": [grid_range(DASHBOARD_SID, 19, 45, 0, 1)]
                            }
                        }
                    }],
                    "series": [
                        {
                            "series": {
                                "sourceRange": {
                                    "sources": [grid_range(DASHBOARD_SID, 19, 45, 4, 5)]
                                }
                            },
                            "targetAxis": "LEFT_AXIS",
                            "color": CYAN,
                            "lineStyle": {"width": 3}
                        },
                        {
                            "series": {
                                "sourceRange": {
                                    "sources": [grid_range(DASHBOARD_SID, 19, 45, 6, 7)]
                                }
                            },
                            "targetAxis": "LEFT_AXIS",
                            "color": AMBER,
                            "lineStyle": {"width": 2, "type": "MEDIUM_DASHED"}
                        }
                    ],
                    "headerCount": 1
                }
            },
            "position": chart_position(CHARTS_SID, 46, 0)
        }
    }
})
print("  📊 Chart 5: Profit Margin Trend + 50% Target")

# --- CHART 6: Debt Payoff Progress (Line Chart) ---
# Dashboard: Row 99 headers, Rows 100-108 data (0-indexed: 98-107)
# Col A=Date(0), B=Student Loans(1), C=Discover(2), D=Sapphire(3), E=Ink(4), F=Stripe(5), G=Total(6)
chart_requests.append({
    "addChart": {
        "chart": {
            "spec": {
                "title": "Debt Payoff Progress",
                "titleTextFormat": {"fontFamily": "Arial", "fontSize": 14, "bold": True},
                "basicChart": {
                    "chartType": "LINE",
                    "legendPosition": "BOTTOM_LEGEND",
                    "axis": [
                        {
                            "position": "BOTTOM_AXIS",
                            "title": "Month",
                            "format": {"fontFamily": "Arial", "fontSize": 10}
                        },
                        {
                            "position": "LEFT_AXIS",
                            "title": "Debt ($)",
                            "format": {"fontFamily": "Arial", "fontSize": 10}
                        }
                    ],
                    "domains": [{
                        "domain": {
                            "sourceRange": {
                                "sources": [grid_range(DASHBOARD_SID, 98, 108, 0, 1)]
                            }
                        }
                    }],
                    "series": [
                        {
                            "series": {
                                "sourceRange": {
                                    "sources": [grid_range(DASHBOARD_SID, 98, 108, 1, 2)]
                                }
                            },
                            "targetAxis": "LEFT_AXIS",
                            "color": PURPLE,
                            "lineStyle": {"width": 2}
                        },
                        {
                            "series": {
                                "sourceRange": {
                                    "sources": [grid_range(DASHBOARD_SID, 98, 108, 2, 3)]
                                }
                            },
                            "targetAxis": "LEFT_AXIS",
                            "color": CYAN,
                            "lineStyle": {"width": 2}
                        },
                        {
                            "series": {
                                "sourceRange": {
                                    "sources": [grid_range(DASHBOARD_SID, 98, 108, 3, 4)]
                                }
                            },
                            "targetAxis": "LEFT_AXIS",
                            "color": AMBER,
                            "lineStyle": {"width": 2}
                        },
                        {
                            "series": {
                                "sourceRange": {
                                    "sources": [grid_range(DASHBOARD_SID, 98, 108, 4, 5)]
                                }
                            },
                            "targetAxis": "LEFT_AXIS",
                            "color": RED,
                            "lineStyle": {"width": 2}
                        },
                        {
                            "series": {
                                "sourceRange": {
                                    "sources": [grid_range(DASHBOARD_SID, 98, 108, 6, 7)]
                                }
                            },
                            "targetAxis": "LEFT_AXIS",
                            "color": INDIGO,
                            "lineStyle": {"width": 4}
                        }
                    ],
                    "headerCount": 1
                }
            },
            "position": chart_position(CHARTS_SID, 46, 7)
        }
    }
})
print("  📊 Chart 6: Debt Payoff Progress")

# --- CHART 7: Annual Revenue Comparison (Column Chart) ---
# Helper data on Charts tab: M1:P4 (0-indexed: sheetId=100, rows 0-3, cols 12-15)
chart_requests.append({
    "addChart": {
        "chart": {
            "spec": {
                "title": "Annual Revenue Comparison",
                "titleTextFormat": {"fontFamily": "Arial", "fontSize": 14, "bold": True},
                "basicChart": {
                    "chartType": "COLUMN",
                    "legendPosition": "BOTTOM_LEGEND",
                    "axis": [
                        {
                            "position": "BOTTOM_AXIS",
                            "title": "Year",
                            "format": {"fontFamily": "Arial", "fontSize": 10}
                        },
                        {
                            "position": "LEFT_AXIS",
                            "title": "Amount ($)",
                            "format": {"fontFamily": "Arial", "fontSize": 10}
                        }
                    ],
                    "domains": [{
                        "domain": {
                            "sourceRange": {
                                "sources": [grid_range(CHARTS_SID, 0, 4, 12, 13)]
                            }
                        }
                    }],
                    "series": [
                        {
                            "series": {
                                "sourceRange": {
                                    "sources": [grid_range(CHARTS_SID, 0, 4, 13, 14)]
                                }
                            },
                            "targetAxis": "LEFT_AXIS",
                            "color": INDIGO
                        },
                        {
                            "series": {
                                "sourceRange": {
                                    "sources": [grid_range(CHARTS_SID, 0, 4, 14, 15)]
                                }
                            },
                            "targetAxis": "LEFT_AXIS",
                            "color": RED
                        },
                        {
                            "series": {
                                "sourceRange": {
                                    "sources": [grid_range(CHARTS_SID, 0, 4, 15, 16)]
                                }
                            },
                            "targetAxis": "LEFT_AXIS",
                            "color": GREEN
                        }
                    ],
                    "headerCount": 1
                }
            },
            "position": chart_position(CHARTS_SID, 68, 0)
        }
    }
})
print("  📊 Chart 7: Annual Revenue Comparison")

# --- CHART 8: Net Worth Over Time (Area Chart) ---
# Dashboard: Row 86 headers, Rows 87-95 data (0-indexed: 85-94)
# Col A=Date(0), D=Net Worth(3)
chart_requests.append({
    "addChart": {
        "chart": {
            "spec": {
                "title": "Net Worth Over Time",
                "titleTextFormat": {"fontFamily": "Arial", "fontSize": 14, "bold": True},
                "basicChart": {
                    "chartType": "AREA",
                    "legendPosition": "BOTTOM_LEGEND",
                    "axis": [
                        {
                            "position": "BOTTOM_AXIS",
                            "title": "Month",
                            "format": {"fontFamily": "Arial", "fontSize": 10}
                        },
                        {
                            "position": "LEFT_AXIS",
                            "title": "Net Worth ($)",
                            "format": {"fontFamily": "Arial", "fontSize": 10}
                        }
                    ],
                    "domains": [{
                        "domain": {
                            "sourceRange": {
                                "sources": [grid_range(DASHBOARD_SID, 85, 95, 0, 1)]
                            }
                        }
                    }],
                    "series": [{
                        "series": {
                            "sourceRange": {
                                "sources": [grid_range(DASHBOARD_SID, 85, 95, 3, 4)]
                            }
                        },
                        "targetAxis": "LEFT_AXIS",
                        "color": GREEN,
                        "lineStyle": {"width": 3}
                    }],
                    "headerCount": 1
                }
            },
            "position": chart_position(CHARTS_SID, 68, 7)
        }
    }
})
print("  📊 Chart 8: Net Worth Over Time")

# Execute all chart creation in one batch
result = api_call('POST', f'{BASE_URL}:batchUpdate', {"requests": chart_requests})
if result:
    chart_ids = []
    for reply in result.get('replies', []):
        if 'addChart' in reply:
            chart_ids.append(reply['addChart']['chart']['chartId'])
    print(f"✅ All 8 charts created! Chart IDs: {chart_ids}")
else:
    print("❌ Failed to create charts")
    sys.exit(1)

# ============================================================
# STEP 4: Format the Charts tab
# ============================================================
print("\n🎨 Step 4: Formatting Charts tab...")

format_requests = [
    # Add title row
    {
        "updateCells": {
            "range": grid_range(CHARTS_SID, 0, 1, 0, 7),
            "rows": [{
                "values": [{
                    "userEnteredValue": {"stringValue": "📈 FINANCIAL CHARTS DASHBOARD"},
                    "userEnteredFormat": {
                        "backgroundColor": NAVY,
                        "textFormat": {
                            "foregroundColor": WHITE,
                            "fontFamily": "Arial",
                            "fontSize": 16,
                            "bold": True
                        },
                        "horizontalAlignment": "CENTER",
                        "verticalAlignment": "MIDDLE"
                    }
                }] + [{"userEnteredFormat": {"backgroundColor": NAVY}}] * 6
            }],
            "fields": "userEnteredValue,userEnteredFormat"
        }
    },
    # Merge title cells
    {
        "mergeCells": {
            "range": grid_range(CHARTS_SID, 0, 1, 0, 14),
            "mergeType": "MERGE_ALL"
        }
    },
    # Set row height for title
    {
        "updateDimensionProperties": {
            "range": {
                "sheetId": CHARTS_SID,
                "dimension": "ROWS",
                "startIndex": 0,
                "endIndex": 1
            },
            "properties": {"pixelSize": 50},
            "fields": "pixelSize"
        }
    },
    # Section labels
    {
        "updateCells": {
            "range": grid_range(CHARTS_SID, 1, 2, 0, 7),
            "rows": [{
                "values": [{
                    "userEnteredValue": {"stringValue": "Revenue & Profit Trends"},
                    "userEnteredFormat": {
                        "textFormat": {
                            "fontFamily": "Arial",
                            "fontSize": 11,
                            "bold": True,
                            "foregroundColor": NAVY
                        }
                    }
                }] + [{}] * 6
            }],
            "fields": "userEnteredValue,userEnteredFormat"
        }
    },
    {
        "updateCells": {
            "range": grid_range(CHARTS_SID, 23, 24, 0, 7),
            "rows": [{
                "values": [{
                    "userEnteredValue": {"stringValue": "Revenue & Expense Breakdown"},
                    "userEnteredFormat": {
                        "textFormat": {
                            "fontFamily": "Arial",
                            "fontSize": 11,
                            "bold": True,
                            "foregroundColor": NAVY
                        }
                    }
                }] + [{}] * 6
            }],
            "fields": "userEnteredValue,userEnteredFormat"
        }
    },
    {
        "updateCells": {
            "range": grid_range(CHARTS_SID, 45, 46, 0, 7),
            "rows": [{
                "values": [{
                    "userEnteredValue": {"stringValue": "Margins & Debt Tracking"},
                    "userEnteredFormat": {
                        "textFormat": {
                            "fontFamily": "Arial",
                            "fontSize": 11,
                            "bold": True,
                            "foregroundColor": NAVY
                        }
                    }
                }] + [{}] * 6
            }],
            "fields": "userEnteredValue,userEnteredFormat"
        }
    },
    {
        "updateCells": {
            "range": grid_range(CHARTS_SID, 67, 68, 0, 7),
            "rows": [{
                "values": [{
                    "userEnteredValue": {"stringValue": "Annual Comparison & Net Worth"},
                    "userEnteredFormat": {
                        "textFormat": {
                            "fontFamily": "Arial",
                            "fontSize": 11,
                            "bold": True,
                            "foregroundColor": NAVY
                        }
                    }
                }] + [{}] * 6
            }],
            "fields": "userEnteredValue,userEnteredFormat"
        }
    },
    # Set background color for the whole sheet
    {
        "updateCells": {
            "range": grid_range(CHARTS_SID, 0, 90, 0, 14),
            "rows": [{"values": [{"userEnteredFormat": {"backgroundColor": {"red": 0.98, "green": 0.98, "blue": 0.98}}}] * 14}] * 90,
            "fields": "userEnteredFormat.backgroundColor"
        }
    }
]

result = api_call('POST', f'{BASE_URL}:batchUpdate', {"requests": format_requests})
if result:
    print("✅ Charts tab formatted")
else:
    print("⚠️ Formatting partially failed")

# ============================================================
# STEP 5: Add sparklines to Dashboard
# ============================================================
print("\n✨ Step 5: Adding sparklines to Dashboard...")

# Add sparkline formulas in column F next to key metrics
# Using SPARKLINE function to show mini inline charts
# We'll place sparklines in cells that are currently empty

sparkline_data = [
    # Revenue trend sparkline next to "Total Revenue" row
    ['=SPARKLINE(B21:B45, {"charttype","line";"color","#6366F1";"linewidth",2})'],
    # Expenses trend sparkline next to "Total Expenses"
    ['=SPARKLINE(C21:C45, {"charttype","line";"color","#EF4444";"linewidth",2})'],
    # Profit trend sparkline next to "Net Profit"
    ['=SPARKLINE(D21:D45, {"charttype","line";"color","#22C55E";"linewidth",2})'],
    # Margin trend sparkline next to "Profit Margin"
    ['=SPARKLINE(E21:E45, {"charttype","line";"color","#06B6D4";"linewidth",2})'],
]

result = api_call('PUT',
    f'{BASE_URL}/values/%F0%9F%8C%90%20All%20Time%20Dashboard!F3:F6?valueInputOption=USER_ENTERED',
    {"values": sparkline_data}
)
if result:
    print("✅ Revenue/Expense/Profit/Margin sparklines added (F3:F6)")

# Add sparkline header
result = api_call('PUT',
    f'{BASE_URL}/values/%F0%9F%8C%90%20All%20Time%20Dashboard!F2:F2?valueInputOption=RAW',
    {"values": [["Trend"]]}
)
if result:
    print("✅ Trend header added (F2)")

# Debt trend sparkline near the debt section
debt_sparkline = [
    ['=SPARKLINE({27092,25385,24100,23200,22400,21600,20800,24745,24196}, {"charttype","line";"color","#8B5CF6";"linewidth",2})']
]
result = api_call('PUT',
    f'{BASE_URL}/values/%F0%9F%8C%90%20All%20Time%20Dashboard!H99:H99?valueInputOption=USER_ENTERED',
    {"values": debt_sparkline}
)
if result:
    print("✅ Debt trend sparkline added (H99)")

# Net worth sparkline
nw_sparkline = [
    ['=SPARKLINE({129836,131661,135700,137300,138800,138200,139300,133800,133700}, {"charttype","line";"color","#22C55E";"linewidth",2})']
]
result = api_call('PUT',
    f'{BASE_URL}/values/%F0%9F%8C%90%20All%20Time%20Dashboard!F86:F86?valueInputOption=USER_ENTERED',
    {"values": nw_sparkline}
)
if result:
    print("✅ Net worth sparkline added (F86)")

# Format the sparkline header cell
format_sparkline = [
    {
        "updateCells": {
            "range": grid_range(DASHBOARD_SID, 1, 2, 5, 6),
            "rows": [{
                "values": [{
                    "userEnteredFormat": {
                        "backgroundColor": LIGHT_GRAY,
                        "textFormat": {
                            "fontFamily": "Arial",
                            "fontSize": 11,
                            "bold": True
                        },
                        "horizontalAlignment": "CENTER"
                    }
                }]
            }],
            "fields": "userEnteredFormat"
        }
    },
    # Make sparkline column wider
    {
        "updateDimensionProperties": {
            "range": {
                "sheetId": DASHBOARD_SID,
                "dimension": "COLUMNS",
                "startIndex": 5,
                "endIndex": 6
            },
            "properties": {"pixelSize": 150},
            "fields": "pixelSize"
        }
    }
]

result = api_call('POST', f'{BASE_URL}:batchUpdate', {"requests": format_sparkline})
if result:
    print("✅ Sparkline formatting applied")

print("\n" + "="*50)
print("🎉 ALL DONE! 8 charts + sparklines created successfully!")
print(f"📊 View: https://docs.google.com/spreadsheets/d/{SHEET_ID}")
print("="*50)
