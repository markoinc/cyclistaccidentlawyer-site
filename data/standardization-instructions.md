# Standardization Instructions for Sub-Agents

## Your Mission
Apply the master template design to assigned monthly accounting sheets. Verify all data accuracy against the original data in the sheet.

## OAuth Token
Get a fresh access token:
```python
import json, urllib.request, urllib.parse
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
```

## Template Reference
- Template Sheet ID: `1iZcuMZL_HeuDCxk-wx5Sf4smNA4B9lvxCJO7CLkHrdk`
- Full spec: `/home/ec2-user/clawd/data/master-template-spec.md`
- Design audit: `/home/ec2-user/clawd/data/design-consistency-audit.md`
- Old sheets catalog: `/home/ec2-user/clawd/data/old-sheets-catalog.md`

## For Each Sheet, Do:

### 1. Read ALL existing data first
- Read every tab completely
- Store the original data in memory before making changes
- Note the 📦 Original Overview tab data (this is the truth source)

### 2. Rename the spreadsheet
- Format: `{Month} {Year} — KuriosBrand Financial Overview`

### 3. Standardize tab names
- Rename to match template exactly: 📊 Dashboard, 💰 Profit First, 🎯 Pareto Analysis, 💼 Business 4991, 👤 Personal 0068, 💳 Biz CC 0678, 💎 Sapphire 4252, 📦 Raw Data
- Create missing tabs (Profit First, Pareto if they don't exist)
- If "💎 Sapphire CC" → rename to "💎 Sapphire 4252"
- If "📦 Original Overview" → rename to "📦 Raw Data" (but keep original content!)
- Remove leftover raw import tabs (like "Biz 4991 Transactions" etc.) ONLY after ensuring their data is preserved in 📦 Raw Data

### 4. Reorder tabs
Match template order: Dashboard → Profit First → Pareto → Business 4991 → Personal 0068 → Biz CC 0678 → Sapphire 4252 → Raw Data

### 5. Format Dashboard
Apply the master template structure — Sections A through I:

**SECTION A: INCOME SUMMARY** — Group by business line:
- 🚗 MVA Lead Gen (clients who pay for MVA leads)
- 🏗️ Rank & Rent (concrete site lead rentals)
- 🔧 SEO / One-Time (SEO services, one-off projects)
Each gets a subtotal row with % of total. Classify each income source into the right business line.

Historical context for classification:
- Jun-Sep 2025: Income was primarily Stripe (client subscriptions) + Zelle. SEO clients (Indexsy work, guest posts) = 🔧 SEO. Concrete site leads = 🏗️ Rank & Rent. Everything else client-related = likely 🏗️ or 🔧.
- Nov-Dec 2025: Transition period, some MVA starting
- Jan 2026: Primarily 🚗 MVA Lead Gen (Meta ads for lawyers)

If you can't determine the business line from the data, use 🔧 SEO / One-Time as default.

**SECTIONS B through I** — Match template structure exactly. Use existing data from the current Dashboard.

### 6. Format Transaction Tabs
- Headers: Date | Vendor | Category | Amount | Balance | Notes
- Header row: #1B2A4A navy background, white bold 11pt text
- Freeze row 1
- Column widths: 110 / 250 / 250 / 130 / 130 / 250
- Currency format: $#,##0.00;[Red]($#,##0.00)
- Add data validation for Category column

### 7. Build Profit First Tab
Calculate from the month's actual data:
- Revenue = Total income from Section A
- Profit allocation targets: 5% profit, 50% owner comp, 15% tax, 30% OpEx
- Current allocation: calculate from actual spending

### 8. Build Pareto Analysis Tab
- List ALL expenses sorted by amount (largest first)
- Add cumulative sum and cumulative % columns
- Mark the 80% threshold line

### 9. Verify Data Accuracy
**CRITICAL:** After all changes, verify:
- Total income matches original sheet's income
- Total expenses match original sheet's expenses
- Individual transaction counts match (same number of rows in each tab)
- No data was lost or corrupted
- Profit calculation is correct

### 10. Report
Write results to `/home/ec2-user/clawd/data/standardization-report-{month}.md`:
- What was changed
- Data verification results (pass/fail for each check)
- Any discrepancies found
- Any data that couldn't be classified

## IMPORTANT RULES
1. **NEVER delete original data** — if uncertain, keep both old and new
2. **Raw Data tab is sacred** — preserve original bank CSV data exactly
3. **Original Overview content** — save to 📦 Raw Data if not already there
4. **When in doubt, preserve** — it's better to have extra data than lost data
5. **June is special** — transaction tabs are empty, only Dashboard has data. Do your best but note limitations.

## Formatting Colors Reference
- Section header BG: #1B2A4A (rgb 0.106, 0.165, 0.29)
- Section header text: white
- Subtotal row BG: #F3F3F3 (rgb 0.953, 0.953, 0.953)
- Total row BG: #E8EDF5 (rgb 0.91, 0.929, 0.949)
- Transaction header BG: #1B2A4A
- Tab colors: Green (#34A853) for Profit First, Orange (#FF6D01) for Pareto, Navy for transaction tabs, Gray for Raw Data
