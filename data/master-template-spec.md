# 📋 Master Template Specification — KuriosBrand Monthly Accounting

**Version:** 1.0
**Date:** 2026-02-04
**Purpose:** Definitive standard for all monthly accounting sheets

---

## 1. SPREADSHEET NAMING

**Format:** `{Month} {Year} — KuriosBrand Financial Overview`
**Example:** `January 2026 — KuriosBrand Financial Overview`

---

## 2. TAB STRUCTURE (Exact Order)

| # | Tab Name | Emoji | Color | Purpose |
|---|----------|-------|-------|---------|
| 1 | 📊 Dashboard | — | Default (white) | Financial summary & analysis |
| 2 | 💰 Profit First | — | Green (#34A853) | Profit First allocation analysis |
| 3 | 🎯 Pareto Analysis | — | Orange (#FF6D01) | 80/20 expense analysis |
| 4 | 💼 Business 4991 | — | Navy (#1B2A4A) | Chase Business Checking transactions |
| 5 | 👤 Personal 0068 | — | Navy (#1B2A4A) | Chase Personal Checking transactions |
| 6 | 💳 Biz CC 0678 | — | Navy (#1B2A4A) | Chase Ink Business CC transactions |
| 7 | 💎 Sapphire 4252 | — | Navy (#1B2A4A) | Chase Sapphire Personal CC transactions |
| 8 | 📦 Raw Data | — | Gray (#999999) | Original imported CSVs, untouched |

**Notes:**
- Profit First and Pareto tabs are STANDARD (not "extra") — every month gets them
- Raw Data preserves the original bank exports exactly as imported
- Tab order is fixed — never reorder

---

## 3. DASHBOARD LAYOUT

### Color Scheme
| Element | Color | Hex |
|---------|-------|-----|
| Section headers (full-width bars) | Dark Navy | #1B2A4A |
| Section header text | White | #FFFFFF |
| Category headers (sub-sections) | Light Gray | #F3F3F3 |
| Positive amounts | Dark Green | #006100 |
| Negative amounts / losses | Dark Red | #CC0000 |
| Background | White | #FFFFFF |
| Alternating rows | Very light blue | #F0F4FF |
| Totals rows | Light navy | #E8EDF5 |

### Section Structure (Fixed — A through I)

#### 💰 SECTION A: INCOME SUMMARY
Row layout — **grouped by business line** with subtotals:
```
| Business Line | Source | Method | Amount | % of Total | Notes |
|---------------|--------|--------|--------|------------|-------|
| 🚗 MVA Lead Gen | Client A | Stripe | $X,XXX | | Retainer |
| 🚗 MVA Lead Gen | Client B | Zelle | $X,XXX | | Per-lead |
| | SUBTOTAL: 🚗 MVA Lead Gen | | $X,XXX | XX% | |
| 🏗️ Rank & Rent | Site A — Leads | Zelle | $X,XXX | | Lead rental |
| | SUBTOTAL: 🏗️ Rank & Rent | | $X,XXX | XX% | |
| 🔧 SEO / One-Time | Client C — SEO | Stripe | $X,XXX | | Monthly |
| | SUBTOTAL: 🔧 SEO / One-Time | | $X,XXX | XX% | |
| | TOTAL INCOME | | $XX,XXX | 100% | |
```

**Three business lines (always present, even if $0):**
1. 🚗 MVA Lead Gen — Motor vehicle accident lead generation
2. 🏗️ Rank & Rent — Local SEO sites rented to contractors
3. 🔧 SEO / One-Time — SEO services, website builds, one-off projects

- Each business line gets a subtotal with % of total income
- Method column: Stripe, Zelle, Wire, Check, Other
- Subtotal rows: light gray #F3F3F3, bold
- Total row: light navy #E8EDF5, bold 11pt

#### 📊 SECTION B: BUSINESS EXPENSES
Row layout:
```
| Category | Vendor | Amount | Recurring? | Notes |
|----------|--------|--------|------------|-------|
| 📱 SaaS & Tools | HighLevel | -$497.00 | Monthly | CRM |
| 📱 SaaS & Tools | ... | | | |
| SUBTOTAL: 📱 SaaS & Tools | | -$X,XXX | | |
| 📣 Marketing / Ads | Meta Ads | -$X,XXX | Variable | MVA campaigns |
| SUBTOTAL: 📣 Marketing / Ads | | -$X,XXX | | |
| ... | | | | |
| TOTAL BUSINESS EXPENSES | | -$XX,XXX | | |
```

**Standard Business Categories (in this order):**
1. 📱 SaaS & Tools
2. 📣 Marketing / Ads
3. 🏢 Operations
4. 💳 Debt Payments (Business)
5. 💰 Business Fees & Interest
6. 🏧 Business ATM / Cash

Each category gets a subtotal row. Grand total at bottom.

#### 👤 SECTION C: PERSONAL EXPENSES
Same layout as Section B but with personal categories.

**Standard Personal Categories (in this order):**
1. 📈 Investments (Net Flows)
2. 🏠 Living / Local (rent, utilities, groceries, local spending)
3. 🍔 Food & Dining
4. 📺 Subscriptions
5. ✈️ Travel
6. 🛍️ Shopping & Misc
7. 💳 CC Payments (Personal)
8. 💰 CC Interest & Fees (Personal)
9. 🏧 ATM / Cash / FX Fees

#### 📈 SECTION D: KEY METRICS
```
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Total Revenue | $XX,XXX | | |
| Total Business Expenses | -$XX,XXX | | |
| Business Profit | $X,XXX | | |
| Profit Margin | XX% | 50%+ | 🟢/🟡/🔴 |
| Meta Ad Spend | -$X,XXX | | |
| Cost Per Call | $XXX | <$150 | 🟢/🟡/🔴 |
| Revenue Per Client | $X,XXX | | |
| MoM Revenue Change | +XX% | | |
| Burn Rate | $X,XXX/mo | | |
```

#### 🔄 SECTION E: MONEY FLOW
```
| Flow | From | To | Amount | Notes |
|------|------|-----|--------|-------|
| Business → Personal | 4991 | 0068 | $X,XXX | Owner draws |
| Business → Tax | 4991 | Wells Fargo | $XXX | Tax set-aside |
| Personal → Investments | 0068 | Robinhood | $XXX | Daily buys |
| Personal → Investments | 0068 | Acorns | $XXX | Daily + roundups |
| Personal → Savings | 0068 | 7036 | $XXX | Auto-saves |
```

#### 🏦 SECTION F: DEBT TRACKING
```
| Account | Balance | Limit | Utilization | Min Payment | Actual Payment | Notes |
|---------|---------|-------|-------------|-------------|----------------|-------|
| Student Loans | $X,XXX | — | — | $XXX | $XXX | |
| Discover 6820 | $X,XXX | $6,300 | XX% | $XXX | $XXX | |
| Sapphire 4252 | $X,XXX | $9,300 | XX% | $XXX | $XXX | |
| Ink 0678 | $X,XXX | $5,500 | XX% | $XXX | $XXX | |
| Stripe Loan | $X,XXX | — | — | 20% of deposits | $XXX | |
| TOTAL DEBT | $XX,XXX | | | | | |
```

#### 💰 SECTION G: ACCOUNT BALANCES
```
| Account | Opening | Closing | Change | Notes |
|---------|---------|---------|--------|-------|
| Chase Biz 4991 | $X,XXX | $X,XXX | +/-$XXX | |
| Chase Personal 0068 | $X,XXX | $X,XXX | +/-$XXX | |
| Chase Savings 7036 | $X,XXX | $X,XXX | +/-$XXX | |
| Wells Fargo Tax | $X,XXX | $X,XXX | +/-$XXX | |
```

#### 💎 SECTION H: ASSETS & NET WORTH
```
| Asset | Value | Change | Notes |
|-------|-------|--------|-------|
| Business Equity | $150,000 | — | Rank & rent portfolio |
| Robinhood | $X,XXX | +$XXX | Stocks |
| Acorns | $X,XXX | +$XXX | Index funds |
| Bitcoin | $X,XXX | +/-$XXX | |
| Solana | $X,XXX | +/-$XXX | |
| Cash (all accounts) | $X,XXX | | Sum of Section G |
| TOTAL ASSETS | $XXX,XXX | | |
| TOTAL LIABILITIES | -$XX,XXX | | From Section F |
| NET WORTH | $XXX,XXX | +/-$X,XXX | |
```

#### 📝 SECTION I: ACTION ITEMS
```
| Priority | Action | Status | Due | Notes |
|----------|--------|--------|-----|-------|
| 🔴 HIGH | Cancel unused subscriptions | ⬜ | | Save $XXX/mo |
| 🟡 MED | Reduce Meta Ad spend or improve ROAS | ⬜ | | Currently 64% of revenue |
| 🟢 LOW | Set up Discover auto-pay | ⬜ | | |
```

---

## 4. TRANSACTION TAB FORMAT

### Column Structure (All 4 tabs identical)
| Column | Header | Width | Format |
|--------|--------|-------|--------|
| A | Date | 110px | MM/DD/YYYY |
| B | Vendor | 250px | Text |
| C | Category | 250px | Text (emoji-prefixed) |
| D | Amount | 130px | $#,##0.00;($#,##0.00) red negatives |
| E | Balance | 130px | $#,##0.00 |
| F | Notes | 250px | Text |

### Formatting Rules
| Element | Value |
|---------|-------|
| Header row background | #1B2A4A (dark navy) |
| Header row text | White, Bold, 11pt |
| Header row height | 30px |
| Data font | 10pt, default |
| Frozen rows | 1 |
| Frozen columns | 0 |
| Currency format | `$#,##0.00;[Red]($#,##0.00)` — red negatives in parens |
| Date format | `MM/DD/YYYY` |
| Alternating colors | Off (clean look) |
| Grid lines | Default visible |
| Sorting | Date descending (newest first) or ascending (oldest first) — pick one |

### Category Values (Standardized Dropdown)

**Business Categories (for 💼 4991 and 💳 0678):**
- 📱 SaaS & Tools
- 📣 Marketing / Ads
- 🏢 Operations
- 💳 Debt Payment
- 💰 Fees & Interest
- 🏧 ATM / Cash
- 💵 Revenue (for incoming)
- 🔄 Transfer

**Personal Categories (for 👤 0068 and 💎 4252):**
- 📈 Investment
- 🏠 Living / Local
- 🍔 Food & Dining
- 📺 Subscription
- ✈️ Travel
- 🛍️ Shopping & Misc
- 💳 CC Payment
- 💰 Interest & Fees
- 🏧 ATM / Cash / FX
- 🔄 Transfer
- 💵 Income (for incoming transfers)

---

## 5. PROFIT FIRST TAB

Based on Mike Michalowicz's framework.

### Layout
```
| Bucket | Target % | Current % | Target Amount | Actual Amount | Gap |
|--------|----------|-----------|---------------|---------------|-----|
| Revenue (TAPs) | 100% | 100% | $XX,XXX | $XX,XXX | — |
| Profit | 5% | X% | $XXX | $XXX | -$XXX |
| Owner's Comp | 50% | X% | $X,XXX | $X,XXX | -$X,XXX |
| Tax | 15% | X% | $X,XXX | $X,XXX | -$X,XXX |
| OpEx | 30% | X% | $X,XXX | $X,XXX | +/-$X,XXX |
```

### Color Coding
- On target or better: Green background
- Within 5%: Yellow background
- Off target by >5%: Red background

---

## 6. PARETO ANALYSIS TAB

### Layout
```
| Rank | Expense | Amount | Cumulative | Cum % | Category |
|------|---------|--------|------------|-------|----------|
| 1 | Meta Ads | $7,016 | $7,016 | 64% | 📣 Marketing |
| 2 | HighLevel | $497 | $7,513 | 68% | 📱 SaaS |
| ... | | | | | |
```
- Sorted by amount descending
- Cumulative percentage column
- Highlight the 80% line
- Color: items above 80% line = orange, below = gray

---

## 7. RAW DATA TAB

- Exact bank CSV data, pasted as-is
- No formatting changes
- Labeled sub-sections:
  ```
  === CHASE BUSINESS 4991 ===
  [raw CSV data]
  
  === CHASE PERSONAL 0068 ===
  [raw CSV data]
  
  === CHASE INK CC 0678 ===
  [raw CSV data]
  
  === CHASE SAPPHIRE 4252 ===
  [raw CSV data]
  ```

---

## 8. GLOBAL FORMATTING RULES

| Property | Value |
|----------|-------|
| Default font | Arial or Google Sans |
| Default font size | 10pt |
| Section header font size | 14pt bold |
| Sub-header font size | 11pt bold |
| Section header BG | #1B2A4A |
| Section header text | #FFFFFF |
| Totals row BG | #E8EDF5 |
| Totals row text | Bold |
| Subtotals row BG | #F3F3F3 |
| Subtotals row text | Bold |
| Currency format | $#,##0.00;[Red]($#,##0.00) |
| Percentage format | 0.0% |
| Column header alignment | Center |
| Data alignment | Left (text), Right (numbers) |
| Row height | 21px (default) |
| Section spacing | 2 blank rows between sections |

---

## IMPLEMENTATION CHECKLIST

- [ ] Create template Google Sheet in Accounting folder
- [ ] Build all 8 tabs with correct structure
- [ ] Apply all formatting (colors, fonts, widths, freezes)
- [ ] Add data validation dropdowns for Category columns
- [ ] Add example data showing proper format
- [ ] Add conditional formatting for currency (red negatives)
- [ ] Show to Marko for approval
- [ ] Then run standardization pass on all 7 existing sheets
