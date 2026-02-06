#!/usr/bin/env python3
"""Fix formatting for personal finance tabs (re-run after data is written)."""

import requests, json

def get_token():
    r = requests.post('https://oauth2.googleapis.com/token', data={
        'client_id': '838433184423-1sd6hs0m7m7mrvm63f1sct2ovjhs88ut.apps.googleusercontent.com',
        'client_secret': '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',
        'refresh_token': '1//05PmAu-vBTVrWCgYIARAAGAUSNwF-L9Irl-dM7iPoS4XocG_eO32bhNSfNYM0rfwGMKBi-KwJYCpzpAlXYINO04lXIWVAAHmh0qw',
        'grant_type': 'refresh_token'
    })
    return r.json()['access_token']

SHEET_ID = '1v1di5lJT-84iMD7FfnKGFfWanFV-5gyWXWR5mGJuJZQ'
TOKEN = get_token()

# Colors
NAVY = {"red": 0.106, "green": 0.165, "blue": 0.290}
WHITE = {"red": 1, "green": 1, "blue": 1}
LIGHT_GRAY = {"red": 0.953, "green": 0.953, "blue": 0.953}
PERSONAL_BLUE = {"red": 0.259, "green": 0.522, "blue": 0.957}
TOTALS_BG = {"red": 0.910, "green": 0.929, "blue": 0.949}
LIGHT_BLUE_BG = {"red": 0.886, "green": 0.937, "blue": 0.992}

def batch_update(reqs):
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}:batchUpdate'
    resp = requests.post(url, headers={
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }, json={'requests': reqs})
    if resp.status_code != 200:
        print(f"ERROR: {resp.status_code}")
        print(resp.text[:500])
        return False
    return True

def read_tab(tab_name):
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{requests.utils.quote(tab_name)}!A1:Z2000'
    resp = requests.get(url, headers={'Authorization': f'Bearer {TOKEN}'})
    return resp.json().get('values', [])

# Get sheet metadata for IDs
meta_url = f'https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}?fields=sheets(properties(sheetId,title))'
meta = requests.get(meta_url, headers={'Authorization': f'Bearer {TOKEN}'}).json()
sheet_ids = {s['properties']['title']: s['properties']['sheetId'] for s in meta['sheets']}
print("Sheets:", json.dumps(sheet_ids, indent=2))

# ============================================================
# Format 👤 Personal Overview
# ============================================================
print("\n🎨 Formatting Personal Overview...")
sid = sheet_ids['👤 Personal Overview']
rows = read_tab('👤 Personal Overview')
print(f"  Read {len(rows)} rows")

fmt_reqs = []

# Column widths
col_widths = [200, 130, 130, 130, 130, 100, 130, 130, 130, 130, 130, 130, 130, 130, 130]
for i, w in enumerate(col_widths):
    fmt_reqs.append({
        'updateDimensionProperties': {
            'range': {'sheetId': sid, 'dimension': 'COLUMNS', 'startIndex': i, 'endIndex': i+1},
            'properties': {'pixelSize': w},
            'fields': 'pixelSize'
        }
    })

# Default font for entire sheet
fmt_reqs.append({
    'repeatCell': {
        'range': {'sheetId': sid, 'startRowIndex': 0, 'endRowIndex': len(rows), 'startColumnIndex': 0, 'endColumnIndex': 15},
        'cell': {
            'userEnteredFormat': {
                'textFormat': {'fontFamily': 'Arial', 'fontSize': 10}
            }
        },
        'fields': 'userEnteredFormat(textFormat)'
    }
})

# Currency format for numeric columns
fmt_reqs.append({
    'repeatCell': {
        'range': {'sheetId': sid, 'startRowIndex': 0, 'endRowIndex': len(rows), 'startColumnIndex': 1, 'endColumnIndex': 15},
        'cell': {
            'userEnteredFormat': {
                'numberFormat': {'type': 'CURRENCY', 'pattern': '$#,##0.00;[Red]($#,##0.00)'},
                'textFormat': {'fontFamily': 'Arial', 'fontSize': 10}
            }
        },
        'fields': 'userEnteredFormat(numberFormat,textFormat)'
    }
})

for i, row in enumerate(rows):
    if not row or not row[0]:
        continue
    label = str(row[0])
    
    # Section headers (emoji + uppercase titles)
    if any(label.startswith(prefix) for prefix in ['💰 PERSONAL', '💸 PERSONAL', '📈 PERSONAL', '💎 SAPPHIRE', '📊 MONTHLY']):
        fmt_reqs.append({
            'repeatCell': {
                'range': {'sheetId': sid, 'startRowIndex': i, 'endRowIndex': i+1, 'startColumnIndex': 0, 'endColumnIndex': 15},
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': NAVY,
                        'textFormat': {'foregroundColorStyle': {'rgbColor': WHITE}, 'bold': True, 'fontSize': 14, 'fontFamily': 'Arial'},
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat)'
            }
        })
        fmt_reqs.append({
            'mergeCells': {
                'range': {'sheetId': sid, 'startRowIndex': i, 'endRowIndex': i+1, 'startColumnIndex': 0, 'endColumnIndex': 5},
                'mergeType': 'MERGE_ALL'
            }
        })
        fmt_reqs.append({
            'updateDimensionProperties': {
                'range': {'sheetId': sid, 'dimension': 'ROWS', 'startIndex': i, 'endIndex': i+1},
                'properties': {'pixelSize': 30},
                'fields': 'pixelSize'
            }
        })
    
    # Column headers
    if label in ['Source', 'Category', 'Month']:
        fmt_reqs.append({
            'repeatCell': {
                'range': {'sheetId': sid, 'startRowIndex': i, 'endRowIndex': i+1, 'startColumnIndex': 0, 'endColumnIndex': 15},
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': LIGHT_GRAY,
                        'textFormat': {'bold': True, 'fontSize': 11, 'fontFamily': 'Arial'},
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat)'
            }
        })
    
    # TOTAL rows
    if label.startswith('TOTAL'):
        fmt_reqs.append({
            'repeatCell': {
                'range': {'sheetId': sid, 'startRowIndex': i, 'endRowIndex': i+1, 'startColumnIndex': 0, 'endColumnIndex': 15},
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': TOTALS_BG,
                        'textFormat': {'bold': True, 'fontSize': 11, 'fontFamily': 'Arial'},
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat)'
            }
        })

# Apply in batches
batch_size = 60
for i in range(0, len(fmt_reqs), batch_size):
    batch = fmt_reqs[i:i+batch_size]
    print(f"  Batch {i//batch_size + 1}: {len(batch)} requests...")
    if not batch_update(batch):
        print("  ⚠️ Batch failed")
print("  ✅ Personal Overview formatted")

# ============================================================
# Format 👤 Personal 0068
# ============================================================
print("\n🎨 Formatting Personal 0068...")
sid_0068 = sheet_ids['👤 Personal 0068']
rows_0068 = read_tab('👤 Personal 0068')
print(f"  Read {len(rows_0068)} rows")

fmt_0068 = []

# Column widths
widths = [110, 250, 200, 130, 130, 200]
for i, w in enumerate(widths):
    fmt_0068.append({
        'updateDimensionProperties': {
            'range': {'sheetId': sid_0068, 'dimension': 'COLUMNS', 'startIndex': i, 'endIndex': i+1},
            'properties': {'pixelSize': w},
            'fields': 'pixelSize'
        }
    })

# Header row
fmt_0068.append({
    'repeatCell': {
        'range': {'sheetId': sid_0068, 'startRowIndex': 0, 'endRowIndex': 1, 'startColumnIndex': 0, 'endColumnIndex': 6},
        'cell': {
            'userEnteredFormat': {
                'backgroundColor': NAVY,
                'textFormat': {'foregroundColorStyle': {'rgbColor': WHITE}, 'bold': True, 'fontSize': 11, 'fontFamily': 'Arial'},
                'horizontalAlignment': 'CENTER'
            }
        },
        'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)'
    }
})
fmt_0068.append({
    'updateDimensionProperties': {
        'range': {'sheetId': sid_0068, 'dimension': 'ROWS', 'startIndex': 0, 'endIndex': 1},
        'properties': {'pixelSize': 30},
        'fields': 'pixelSize'
    }
})

# Default font
fmt_0068.append({
    'repeatCell': {
        'range': {'sheetId': sid_0068, 'startRowIndex': 1, 'endRowIndex': len(rows_0068), 'startColumnIndex': 0, 'endColumnIndex': 6},
        'cell': {
            'userEnteredFormat': {
                'textFormat': {'fontFamily': 'Arial', 'fontSize': 10}
            }
        },
        'fields': 'userEnteredFormat(textFormat)'
    }
})

# Currency format for Amount (D) and Balance (E) columns
fmt_0068.append({
    'repeatCell': {
        'range': {'sheetId': sid_0068, 'startRowIndex': 1, 'endRowIndex': len(rows_0068), 'startColumnIndex': 3, 'endColumnIndex': 5},
        'cell': {
            'userEnteredFormat': {
                'numberFormat': {'type': 'CURRENCY', 'pattern': '$#,##0.00;[Red]($#,##0.00)'},
                'textFormat': {'fontFamily': 'Arial', 'fontSize': 10}
            }
        },
        'fields': 'userEnteredFormat(numberFormat,textFormat)'
    }
})

# Format month headers and subtotals
for i, row in enumerate(rows_0068):
    if i == 0 or not row:
        continue
    label = str(row[0]) if row[0] else ''
    col2 = str(row[2]) if len(row) > 2 and row[2] else ''
    
    if label.startswith('📅'):
        fmt_0068.append({
            'repeatCell': {
                'range': {'sheetId': sid_0068, 'startRowIndex': i, 'endRowIndex': i+1, 'startColumnIndex': 0, 'endColumnIndex': 6},
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': LIGHT_BLUE_BG,
                        'textFormat': {'bold': True, 'fontSize': 11, 'fontFamily': 'Arial'},
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat)'
            }
        })
    
    if 'SUBTOTAL' in col2:
        fmt_0068.append({
            'repeatCell': {
                'range': {'sheetId': sid_0068, 'startRowIndex': i, 'endRowIndex': i+1, 'startColumnIndex': 0, 'endColumnIndex': 6},
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': TOTALS_BG,
                        'textFormat': {'bold': True, 'fontSize': 10, 'fontFamily': 'Arial'},
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat)'
            }
        })

# Apply
for i in range(0, len(fmt_0068), batch_size):
    batch = fmt_0068[i:i+batch_size]
    print(f"  Batch {i//batch_size + 1}: {len(batch)} requests...")
    if not batch_update(batch):
        print("  ⚠️ Batch failed")
print("  ✅ Personal 0068 formatted")

# ============================================================
# Format 💎 Personal 4252
# ============================================================
print("\n🎨 Formatting Personal 4252...")
sid_4252 = sheet_ids['💎 Personal 4252']
rows_4252 = read_tab('💎 Personal 4252')
print(f"  Read {len(rows_4252)} rows")

fmt_4252 = []

for i, w in enumerate(widths):
    fmt_4252.append({
        'updateDimensionProperties': {
            'range': {'sheetId': sid_4252, 'dimension': 'COLUMNS', 'startIndex': i, 'endIndex': i+1},
            'properties': {'pixelSize': w},
            'fields': 'pixelSize'
        }
    })

fmt_4252.append({
    'repeatCell': {
        'range': {'sheetId': sid_4252, 'startRowIndex': 0, 'endRowIndex': 1, 'startColumnIndex': 0, 'endColumnIndex': 6},
        'cell': {
            'userEnteredFormat': {
                'backgroundColor': NAVY,
                'textFormat': {'foregroundColorStyle': {'rgbColor': WHITE}, 'bold': True, 'fontSize': 11, 'fontFamily': 'Arial'},
                'horizontalAlignment': 'CENTER'
            }
        },
        'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)'
    }
})
fmt_4252.append({
    'updateDimensionProperties': {
        'range': {'sheetId': sid_4252, 'dimension': 'ROWS', 'startIndex': 0, 'endIndex': 1},
        'properties': {'pixelSize': 30},
        'fields': 'pixelSize'
    }
})

fmt_4252.append({
    'repeatCell': {
        'range': {'sheetId': sid_4252, 'startRowIndex': 1, 'endRowIndex': len(rows_4252), 'startColumnIndex': 0, 'endColumnIndex': 6},
        'cell': {
            'userEnteredFormat': {
                'textFormat': {'fontFamily': 'Arial', 'fontSize': 10}
            }
        },
        'fields': 'userEnteredFormat(textFormat)'
    }
})

fmt_4252.append({
    'repeatCell': {
        'range': {'sheetId': sid_4252, 'startRowIndex': 1, 'endRowIndex': len(rows_4252), 'startColumnIndex': 3, 'endColumnIndex': 5},
        'cell': {
            'userEnteredFormat': {
                'numberFormat': {'type': 'CURRENCY', 'pattern': '$#,##0.00;[Red]($#,##0.00)'},
                'textFormat': {'fontFamily': 'Arial', 'fontSize': 10}
            }
        },
        'fields': 'userEnteredFormat(numberFormat,textFormat)'
    }
})

for i, row in enumerate(rows_4252):
    if i == 0 or not row:
        continue
    label = str(row[0]) if row[0] else ''
    col2 = str(row[2]) if len(row) > 2 and row[2] else ''
    
    if label.startswith('📅'):
        fmt_4252.append({
            'repeatCell': {
                'range': {'sheetId': sid_4252, 'startRowIndex': i, 'endRowIndex': i+1, 'startColumnIndex': 0, 'endColumnIndex': 6},
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': LIGHT_BLUE_BG,
                        'textFormat': {'bold': True, 'fontSize': 11, 'fontFamily': 'Arial'},
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat)'
            }
        })
    
    if 'SUBTOTAL' in col2:
        fmt_4252.append({
            'repeatCell': {
                'range': {'sheetId': sid_4252, 'startRowIndex': i, 'endRowIndex': i+1, 'startColumnIndex': 0, 'endColumnIndex': 6},
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': TOTALS_BG,
                        'textFormat': {'bold': True, 'fontSize': 10, 'fontFamily': 'Arial'},
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat)'
            }
        })

for i in range(0, len(fmt_4252), batch_size):
    batch = fmt_4252[i:i+batch_size]
    print(f"  Batch {i//batch_size + 1}: {len(batch)} requests...")
    if not batch_update(batch):
        print("  ⚠️ Batch failed")
print("  ✅ Personal 4252 formatted")

# ============================================================
# Format year tab personal sections
# ============================================================
print("\n🎨 Formatting year tab personal sections...")

for tab_name in ['📅 2024', '📅 2025', '📅 2026']:
    sid_yr = sheet_ids[tab_name]
    rows_yr = read_tab(tab_name)
    print(f"\n  {tab_name}: {len(rows_yr)} rows")
    
    fmt_yr = []
    
    for i, row in enumerate(rows_yr):
        if not row or not row[0]:
            continue
        label = str(row[0])
        
        # Personal section headers (👤, 💵 with PERSONAL/INCOME, 📅 with MONTHLY PERSONAL)
        if label.startswith('👤') or (label.startswith('💵') and 'PERSONAL' in label) or \
           (label.startswith('📅') and 'MONTHLY PERSONAL' in label):
            fmt_yr.append({
                'repeatCell': {
                    'range': {'sheetId': sid_yr, 'startRowIndex': i, 'endRowIndex': i+1, 'startColumnIndex': 0, 'endColumnIndex': 8},
                    'cell': {
                        'userEnteredFormat': {
                            'backgroundColor': PERSONAL_BLUE,
                            'textFormat': {'foregroundColorStyle': {'rgbColor': WHITE}, 'bold': True, 'fontSize': 14, 'fontFamily': 'Arial'},
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                }
            })
            fmt_yr.append({
                'mergeCells': {
                    'range': {'sheetId': sid_yr, 'startRowIndex': i, 'endRowIndex': i+1, 'startColumnIndex': 0, 'endColumnIndex': 5},
                    'mergeType': 'MERGE_ALL'
                }
            })
            fmt_yr.append({
                'updateDimensionProperties': {
                    'range': {'sheetId': sid_yr, 'dimension': 'ROWS', 'startIndex': i, 'endIndex': i+1},
                    'properties': {'pixelSize': 30},
                    'fields': 'pixelSize'
                }
            })
        
        # Column headers in personal section
        if label in ['Category', 'Source', 'Month'] and i > 50:  # Only in personal section (after main content)
            fmt_yr.append({
                'repeatCell': {
                    'range': {'sheetId': sid_yr, 'startRowIndex': i, 'endRowIndex': i+1, 'startColumnIndex': 0, 'endColumnIndex': 8},
                    'cell': {
                        'userEnteredFormat': {
                            'backgroundColor': LIGHT_GRAY,
                            'textFormat': {'bold': True, 'fontSize': 11, 'fontFamily': 'Arial'},
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                }
            })
        
        # TOTAL and NET rows in personal section
        if (label.startswith('TOTAL') or label.startswith('💰 NET')) and i > 50:
            fmt_yr.append({
                'repeatCell': {
                    'range': {'sheetId': sid_yr, 'startRowIndex': i, 'endRowIndex': i+1, 'startColumnIndex': 0, 'endColumnIndex': 8},
                    'cell': {
                        'userEnteredFormat': {
                            'backgroundColor': TOTALS_BG,
                            'textFormat': {'bold': True, 'fontSize': 11, 'fontFamily': 'Arial'},
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                }
            })
    
    # Currency format for personal section (find where personal data starts)
    personal_start = None
    for i, row in enumerate(rows_yr):
        if row and row[0] and str(row[0]).startswith('👤'):
            personal_start = i
            break
    
    if personal_start:
        fmt_yr.append({
            'repeatCell': {
                'range': {'sheetId': sid_yr, 'startRowIndex': personal_start, 'endRowIndex': len(rows_yr), 'startColumnIndex': 1, 'endColumnIndex': 6},
                'cell': {
                    'userEnteredFormat': {
                        'numberFormat': {'type': 'CURRENCY', 'pattern': '$#,##0.00;[Red]($#,##0.00)'},
                        'textFormat': {'fontFamily': 'Arial', 'fontSize': 10}
                    }
                },
                'fields': 'userEnteredFormat(numberFormat,textFormat)'
            }
        })
    
    if fmt_yr:
        for j in range(0, len(fmt_yr), batch_size):
            batch = fmt_yr[j:j+batch_size]
            print(f"    Batch {j//batch_size + 1}: {len(batch)} requests...")
            if not batch_update(batch):
                print("    ⚠️ Batch failed")
        print(f"  ✅ {tab_name} formatted")

print("\n🎉 All formatting complete!")
