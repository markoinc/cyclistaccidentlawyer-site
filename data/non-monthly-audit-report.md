# 📊 Non-Monthly Sheets — Branding & Visual Audit Report

**Date:** 2026-02-04  
**Auditor:** Sierra (Automated)  
**Status:** READ-ONLY (findings only, no changes made)

---

## 📋 Sheet 1: All Time Financial Overview

**Spreadsheet:** `📊 KuriosBrand — All Time Financial Overview`  
**ID:** `1v1di5lJT-84iMD7FfnKGFfWanFV-5gyWXWR5mGJuJZQ`  
**Tabs:** 4 (🌐 All Time Dashboard, 📅 2025, 📅 2026, 📅 2024)

### Branding Compliance Score: **62/100**

---

### ✅ What's Correct

| Element | Status | Notes |
|---------|--------|-------|
| Tab colors | ✅ Pass | All Time = Gold/Amber (#FABB04 ≈ #FBBC04), Year tabs = Navy (#1B2A49 ≈ #1B2A4A) |
| Font family | ✅ Pass | Arial throughout, all tabs |
| Section header bg color | ✅ Pass | Navy (#1B2A49) with white text — correct |
| Section header font | ✅ Pass | 14pt bold Arial — correct |
| Column header bg | ✅ Pass | Light gray (#F3F3F3) — correct |
| Column header row font | ✅ Pass | 11pt bold on actual header rows (Row 2, 12, 20, etc.) |
| Default data font | ✅ Pass | 10pt Arial — correct |
| Default row height | ✅ Pass | 21px for data rows — correct |

### ❌ Deviations Found

#### 1. Section Header Row Heights (HIGH — All Tabs)
**Spec:** 30px | **Actual:** 21px  
**Affected:** Every section header across all 4 tabs (24 total)
- 🌐 All Time: Rows 1, 11, 19, 49, 60, 71
- 📅 2025: Rows 1, 12, 29, 39, 58, 77
- 📅 2026: Rows 1, 12, 19, 29, 48, 60
- 📅 2024: Rows 1, 12, 28, 38, 57, 64

#### 2. Data Rows Have Gray Background Instead of White (MEDIUM — All Tabs)
**Spec:** Data rows should be white (#FFFFFF); gray (#F3F3F3) only for column headers and subtotals  
**Actual:** The entire table body (all data rows) has #F3F3F3 background  
**Impact:** Makes it impossible to visually distinguish column headers from data rows. The visual hierarchy is flattened.

#### 3. Total Row Background Color Mismatch (LOW — All Tabs)
**Spec:** Light navy #E8EDF5 | **Actual:** #E7ECF1  
**Difference:** Close but not exact — off by ~3-4 values in each RGB channel  
**Affected:** TOTAL rows in all tabs (e.g., All Time Rows 16, 46, 57; 2025 Rows 26, 74; etc.)

#### 4. Total Row Font Size (MEDIUM — All Tabs)
**Spec:** 11pt bold | **Actual:** 10pt bold  
**Affected:** All TOTAL rows across all tabs

#### 5. Currency Number Format (HIGH — All Tabs)
**Spec:** `$#,##0.00;[Red]($#,##0.00)` (red negative parenthetical)  
**Actual:** `"$"#,##0.00` (plain, no red negatives, no parentheses)  
**Affected:** ~348 cells with currency values across all tabs  
**Impact:** Negative amounts display as `-$X,XXX.XX` in black text instead of `($X,XXX.XX)` in red

#### 6. Negative Amount Text Color (HIGH — All Tabs)
**Spec:** Dark red (#CC0000) for negative amounts  
**Actual:** Black (#000000) for ALL negative amounts  
**Affected:** All negative dollar amounts (12+ in Dashboard alone, 30+ across all tabs)  
**Examples:**
- 🌐 Dashboard Row 21 Col D: `-$849.01` — black
- 🌐 Dashboard Row 44 Col D: `-$287.00` — black
- 📅 2024 Row 5 Col B: `-$18,366.58` — black
- 📅 2026 Row 5 Col B: `-$743.32` — black

#### 7. Positive Amount Text Color (LOW — All Tabs)
**Spec:** Dark green (#006100) for positive amounts  
**Actual:** Black (#000000)  
**Note:** The spec calls for green on positive amounts, but this is less critical than the red-on-negative convention

#### 8. Percentage Format (MEDIUM — All Tabs)
**Spec:** `0.0%` (one decimal) | **Actual:** `0%` (no decimal)  
**Affected:** All percentage cells (margin %, category %, etc.)  
**Examples:** "45%" instead of "45.0%", "-72%" instead of "-72.0%"

#### 9. Missing Light Navy Background on Alternating or Key Rows
**Spec:** Alternating rows use #F0F4FF if used  
**Actual:** Not implemented (all data rows use #F3F3F3)

---

### 📐 Spec Compliance Check (vs all-time-template-spec.md)

#### All Time Dashboard Sections
| Section | Present | Notes |
|---------|---------|-------|
| Executive Summary | ✅ | Correct structure |
| Revenue by Business Line | ✅ | Correct |
| Monthly Revenue Trend | ✅ | Correct |
| Expense Categories | ✅ | Correct |
| Key Ratios & Health Metrics | ✅ | Correct |
| Business Pivot Timeline | ✅ | Correct |
| **Net Worth Progression** | ❌ MISSING | Spec Section 5 |
| **Debt Payoff Tracker** | ❌ MISSING | Spec Section 6 |

#### Year Tab Sections
| Section | Present | Notes |
|---------|---------|-------|
| Annual Summary | ✅ | All 3 year tabs |
| Monthly Breakdown | ✅ | All 3 year tabs |
| Expense Categories | ✅ | All 3 year tabs |
| Top Vendors | ✅ | All 3 year tabs |
| Income by Client | ✅ | All 3 year tabs |
| Tax Summary | ✅ | All 3 year tabs |
| **Account Balances (Monthly)** | ❌ MISSING | Spec Section 6 |
| **Debt Progression** | ❌ MISSING | Spec Section 7 |

---

### 🔢 Math Accuracy Check

#### Revenue Cross-Check (All Time vs Accountant View)
| Year | All Time Dashboard | Accountant IS | Difference | Status |
|------|-------------------|---------------|------------|--------|
| 2024 | $25,634.14 | $25,634.14 | $0.00 | ✅ Match |
| 2025 | $80,201.66 | $80,200.99 | **$0.67** | ⚠️ Minor |
| 2026 | $10,569.10 | $10,468.89 | **$100.21** | ❌ Mismatch |

#### 2026 Expense Category Percentages — MATH ERROR
The expense category percentages in 2026 tab (Rows 21-26) add up to **155%**, not 100%:
- 🏢 Operations: 67%
- 📣 Marketing / Ads: **64%**
- 📱 SaaS & Tools: 17%
- 🏧 ATM / Cash: 3%
- 💰 Fees & Interest: 3%
- 💳 Debt Payment: 1%
- **Total: 155%** ❌

This appears to be because the percentages are calculated as `category / total_expenses` but some transactions are being double-counted across categories, or the total denominator is wrong.

#### 2026 Jan Internal Inconsistency
- Revenue column: **$9,322.00**
- 🚗 MVA column: **$13,421.79**
- The MVA business line amount ($13,421.79) is **greater than** the total revenue ($9,322.00) for the same month — this is impossible and indicates a categorization or data error

#### All Time Total Cross-Check
- All Time sum: $25,634.14 + $80,201.66 + $10,569.10 = $116,404.90 ✅ (matches)

#### CSV Transaction Count Verification
Raw CSV records vs sheet coverage:
| Account | CSV Records | Date Range |
|---------|-------------|------------|
| Business 4991 | 1,424 | Feb 2024 – Feb 2026 |
| Personal 0068 | 1,504 | Jan 2025 – Feb 2026 |
| Biz CC 0678 | 441 | Feb 2024 – Feb 2026 |
| Sapphire 4252 | 295 | Feb 2024 – Jan 2026 |

Revenue from CSV (Business 4991 credits) vs Sheet:
| Year | CSV Total Credits | Sheet Revenue | Note |
|------|------------------|---------------|------|
| 2024 | $40,806.64 | $25,634.14 | Difference is transfers, non-revenue credits |
| 2025 | $89,019.24 | $80,201.66 | Difference is transfers, non-revenue credits |
| 2026 | $18,223.89 | $10,569.10 | Difference is transfers, non-revenue credits |

The revenue figures are correctly filtered from raw credits (excluding transfers, CC payments, etc.)

---

## 📋 Sheet 2: Accountant View (CPA-Ready)

**Spreadsheet:** `KuriosBrand LLC — Financial Statements (All Time)`  
**ID:** `1vtXJCdbWOskKU-zxEJCOlXBTVhd7vHclWEdWwJgFZ9o`  
**Tabs:** 8 (Summary, Chart of Accounts, Income Statement 2024/2025/2026, Schedule C Summary, Balance Sheet, Bank Reconciliation)

### Branding Compliance Score: **55/100**

**Important Note:** The Accountant View spec intentionally differs from the master template in some ways (no emojis, professional accounting format, "dark gray" headers). However, the task requires checking against the **master branding guidelines**, so deviations from the branding standard are flagged even if they match the accountant spec.

---

### ✅ What's Correct

| Element | Status | Notes |
|---------|--------|-------|
| Font family | ✅ Pass | Arial throughout, all 8 tabs |
| Default font size | ✅ Pass | 10pt default |
| Title font size | ✅ Pass | 14pt used for sheet titles |
| Sub-header bg | ✅ Pass | #F3F3F3 light gray for column headers |
| Currency format (partial) | ✅ Pass | `$#,##0.00;($#,##0.00)` — parenthetical negatives ✓ |
| Percentage format | ✅ Pass | `0.0%` — correct with decimal |
| Total row bg | ✅ Pass | #E7EDF4 (≈ #E8EDF5) for GROSS PROFIT / NET INCOME rows |
| Date format | ✅ Pass | `mmm yyyy` used in Bank Reconciliation |

### ❌ Deviations Found

#### 1. NO Tab Colors Set (HIGH — All 8 Tabs)
**Spec:** Navy for data tabs, relevant colors for analysis tabs  
**Actual:** ALL 8 tabs have NO tab color  
**Affected:** Summary, Chart of Accounts, Income Statement 2024, Income Statement 2025, Income Statement 2026, Schedule C Summary, Balance Sheet, Bank Reconciliation

#### 2. Section Headers Use Dark Gray Instead of Navy (MEDIUM — 4 Tabs)
**Spec:** Navy #1B2A4A background with white #FFFFFF text  
**Actual:** Dark gray #333333 background with white text  
**Affected:** Summary (Rows 3, 17, 26), Chart of Accounts (Row 3), Schedule C (Row 4), Bank Reconciliation (Row 4)  
**Note:** The accountant-view-spec.md says "Headers: Bold, dark gray background" — so this matches its OWN spec but deviates from master branding

#### 3. Income Statements Have NO Section Headers (MEDIUM — 3 Tabs)
**Actual:** Income Statements use plain text labels (REVENUE, COST OF REVENUE, etc.) with no background color on section label rows  
**Expected per branding:** Navy or dark gray header bars for each section  
**Note:** Standard P&L formatting uses indentation and underlines rather than colored header bars — this is a deliberate accounting convention

#### 4. Section Header Row Heights (LOW — All Tabs)
**Spec:** 30px for headers | **Actual:** 21px for all rows  
**Impact:** All row heights are uniform at 21px

#### 5. Negative Amount Text Color (HIGH — All Tabs)
**Spec:** Dark red (#CC0000)  
**Actual:** Black (#000000) for ALL negative amounts  
**Affected:** 315+ negative dollar cells across Income Statements  
**Note:** The currency format does use parentheses for negatives `($X,XXX.XX)` which is correct accounting convention, but the `[Red]` color modifier is missing

#### 6. Currency Format Missing Red Color (MEDIUM — All IS Tabs)
**Spec:** `$#,##0.00;[Red]($#,##0.00)`  
**Actual:** `$#,##0.00;($#,##0.00)` — parentheses ✓ but no red color  
**Close but not complete**

#### 7. No Positive Amount Green Color (LOW)
**Spec:** Dark green (#006100) for positive amounts  
**Actual:** Black throughout

#### 8. Total Row Font Size (LOW)
**Spec:** 11pt bold for totals  
**Actual:** 10pt bold — confirmed on GROSS PROFIT and NET INCOME rows

---

### 📐 Spec Compliance Check (vs accountant-view-spec.md)

| Tab | Present | Notes |
|-----|---------|-------|
| Summary | ✅ | Entity info, bank accounts, notes |
| Chart of Accounts | ✅ | GL account numbering |
| Income Statement 2024 | ✅ | Not in original spec but correctly added |
| Income Statement 2025 | ✅ | Per spec |
| Income Statement 2026 | ✅ | Per spec |
| Schedule C Summary | ✅ | IRS line mappings |
| Balance Sheet | ✅ | Monthly snapshots |
| Bank Reconciliation | ✅ | Statement vs books |
| **Cash Flow** | ❌ MISSING | Spec Tab 6 |
| **General Ledger** | ❌ MISSING | Spec Tab 7 |
| **1099 Tracking** | ❌ MISSING | Spec Tab 10 |

---

### 🔢 Math Accuracy Check

#### Income Statement 2024 Internal Math
| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Revenue Total | Sum of months | $25,634.14 | ✅ Verified |
| Cost of Revenue Total | Sum of months | ($5,486.84) | ✅ Verified |
| Gross Profit | Revenue - COGS | $20,147.30 | ✅ ($25,634.14 - $5,486.84 = $20,147.30) |
| OpEx Total | Sum of categories | ($22,714.40) | ✅ Verified |
| Net Income | Gross Profit - OpEx | ($2,567.10) | ✅ ($20,147.30 - $22,714.40 = -$2,567.10) |

#### Income Statement 2025 Internal Math
| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Revenue Total | Sum of months | $80,200.99 | ✅ Verified |
| Cost of Revenue Total | Sum of months | ($2,642.31) | ✅ Verified |
| Gross Profit | Revenue - COGS | $77,558.68 | ✅ ($80,200.99 - $2,642.31 = $77,558.68) |
| OpEx Total | Sum of categories | ($34,318.79) | ✅ Verified |
| Net Income | Gross Profit - OpEx | $43,239.89 | ✅ ($77,558.68 - $34,318.79 = $43,239.89) |

#### Income Statement 2026 Internal Math
| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Revenue Total | Sum of months | $10,468.89 | ✅ Verified |
| Cost of Revenue Total | Sum of months | ($6,437.56) | ✅ Verified |
| Gross Profit | Revenue - COGS | $4,031.33 | ✅ ($10,468.89 - $6,437.56 = $4,031.33) |
| OpEx Total | Sum of categories | ($4,201.25) | ✅ Verified |
| Net Income | Gross Profit - OpEx | ($169.92) | ✅ ($4,031.33 - $4,201.25 = -$169.92) |

#### Cross-Sheet Revenue Discrepancy
| Year | Accountant IS | All Time Dashboard | Difference |
|------|--------------|-------------------|------------|
| 2024 | $25,634.14 | $25,634.14 | ✅ Match |
| 2025 | **$80,200.99** | **$80,201.66** | ⚠️ $0.67 off |
| 2026 | **$10,468.89** | **$10,569.10** | ❌ $100.21 off |

The 2026 discrepancy ($100.21) between the two sheets needs investigation. One possible explanation: a transaction categorized differently, or one sheet includes a Jan-26 deposit the other doesn't.

For 2025, the $0.67 difference could be floating point rounding across many cells.

---

## 🏆 Overall Assessment

### Summary Table

| Sheet | Branding Score | Math Score | Missing Sections | Critical Issues |
|-------|---------------|------------|------------------|-----------------|
| All Time Financial Overview | 62/100 | 85/100 | 2 dashboard + 2 per year tab | 3 |
| Accountant View (CPA-ready) | 55/100 | 95/100 | 3 tabs (Cash Flow, GL, 1099) | 2 |

### Top Critical Issues (Fix Priority)

1. **🔴 Currency format missing red negatives** — Both sheets lack `[Red]` in currency format. All negative amounts display in black text. This is the single biggest branding deviation, affecting 400+ cells total.

2. **🔴 2026 expense percentages add to 155%** — Math error in All Time → 2026 tab expense categories. Categories are likely using wrong denominators or double-counting transactions.

3. **🔴 2026 Jan MVA > Revenue inconsistency** — In the All Time 2026 tab, the MVA column shows $13,421.79 but total revenue for Jan is only $9,322.00. A business line can't exceed the total.

4. **🔴 2026 revenue discrepancy between sheets** — All Time shows $10,569.10 but Accountant View shows $10,468.89 for 2026. $100.21 gap needs reconciliation.

5. **🟡 No tab colors on Accountant View** — All 8 tabs have no color, making it visually inconsistent with the branded look.

6. **🟡 Section header heights at 21px everywhere** — Both sheets use 21px for all rows including section headers (should be 30px per spec).

7. **🟡 Data rows use gray background** — All Time sheet applies #F3F3F3 to all rows (data + headers), eliminating visual hierarchy. Data rows should be white.

8. **🟡 Total row font size** — 10pt instead of 11pt on total/subtotal rows (both sheets).

9. **🟢 Percentage format on All Time** — Uses `0%` instead of `0.0%` (Accountant View correctly uses `0.0%`).

10. **🟢 Accountant View uses dark gray (#333333) headers instead of navy (#1B2A4A)** — This matches the accountant spec but not the master branding. Deliberate design choice for CPA audience.

### Sections Missing per Own Specs

**All Time Financial Overview:**
- Net Worth Progression (All Time Dashboard)
- Debt Payoff Tracker (All Time Dashboard)
- Account Balances monthly snapshots (Year tabs)
- Debt Progression (Year tabs)

**Accountant View:**
- Cash Flow tab (Operating, Investing, Financing activities)
- General Ledger tab (Every transaction with GL codes)
- 1099 Tracking tab (Contractor payments >$600)

---

*Report generated 2026-02-04. Read-only audit — no changes were made to either spreadsheet.*
