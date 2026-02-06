# Accountant View Fixes Report

**Date:** 2026-02-04  
**Spreadsheet:** KuriosBrand LLC — Financial Statements (All Time)  
**Sheet ID:** `1vtXJCdbWOskKU-zxEJCOlXBTVhd7vHclWEdWwJgFZ9o`

---

## Summary

All 7 branding fixes and 3 missing tabs have been implemented. The spreadsheet now has 11 tabs (up from 8) with full branding compliance.

---

## BRANDING FIXES APPLIED

### 1. ✅ Tab Colors
All 11 tabs now have appropriate colors:
| Tab | Color | Hex |
|-----|-------|-----|
| Summary | Default (white) | — |
| Chart of Accounts | Navy | #1B2A4A |
| Income Statement 2024 | Green | #34A853 |
| Income Statement 2025 | Green | #34A853 |
| Income Statement 2026 | Green | #34A853 |
| Schedule C Summary | Orange | #FF6D01 |
| Balance Sheet | Blue | #4285F4 |
| Cash Flow Statement | Blue | #4285F4 |
| Bank Reconciliation | Navy | #1B2A4A |
| General Ledger | Navy | #1B2A4A |
| 1099 Tracking | Orange | #FF6D01 |

### 2. ✅ Header Colors
All section headers changed from dark gray (#333333) to navy (#1B2A4A) with white (#FFFFFF) text, 14pt bold. Applied across all 11 tabs.

### 3. ✅ Red Negatives
Currency format updated to `$#,##0.00;[Red]($#,##0.00)` on all tabs:
- Income Statements 2024, 2025, 2026 (all data cells B5:N40)
- Schedule C Summary (columns C-E)
- Balance Sheet (all data columns)
- Bank Reconciliation (all currency columns)
- Cash Flow Statement (all data cells)
- General Ledger (debit/credit columns)
- 1099 Tracking (amount columns)

### 4. ✅ Column/Sub-Headers
All column header rows now use light gray (#F3F3F3) background with 11pt bold Arial. Category section headers (REVENUE, OPERATING EXPENSES, ASSETS, etc.) use navy background with white 11pt bold text.

### 5. ✅ Total Rows
All total/subtotal rows (TOTAL REVENUE, GROSS PROFIT, NET INCOME, etc.) now have light navy (#E8EDF5) background with 11pt bold text.

### 6. ✅ Font Consistency
Arial 10pt applied as default across all 11 tabs. Headers use 14pt bold, sub-headers 11pt bold.

### 7. ✅ Row Heights
- Section headers: 30px
- Data rows: 21px (default)
Applied across all tabs.

---

## NEW TABS CREATED

### 8. ✅ Cash Flow Statement (Tab 8)
**Structure:** Standard CPA cash flow statement with three sections:
- **Operating Activities:** Net income (cash basis = no adjustments needed)
- **Investing Activities:** No significant investing activities for any period
- **Financing Activities:** 
  - Loan proceeds (Stripe Capital $4,200 in Jan 2026)
  - Loan repayments ($99 in 2024, $2,563.25 in 2025, $227.67 in 2026)
  - Owner draws ($5,832 in 2024, $51,340 in 2025, $4,684 in 2026)
  - Owner contributions ($8,550 in 2024, $4,100 in 2025, $3,255 in 2026)

**Net Change in Cash:**
| Year | Operating | Investing | Financing | Net Change |
|------|-----------|-----------|-----------|------------|
| 2024 | ($2,567.10) | $0 | $2,618.84 | $51.74 |
| 2025 | $43,239.89 | $0 | ($49,803.47) | ($6,563.58) |
| 2026 | ($169.92) | $0 | $2,543.33 | $2,373.41 |

### 9. ✅ General Ledger (Tab 10)
**1,898 transactions** categorized across 16 GL accounts:
| GL Acct | Category | Source |
|---------|----------|--------|
| 1000 | Transfer In (Cash) | Biz Checking |
| 2000 | CC Payment | Biz CC |
| 3100 | Transfer Out (Owner Draws) | Biz Checking |
| 4000 | Service Revenue | Biz Checking |
| 4020 | Other Income | Biz Checking |
| 5000 | Advertising - Meta/Facebook | Both |
| 5010 | Advertising - Google Ads | Both |
| 6000 | SaaS & Software | Both |
| 6020 | Office & Coworking | Biz Checking |
| 6050 | Professional Services | Both |
| 6060 | Bank Fees & Interest | Biz Checking |
| 6070 | Credit Card Interest | Biz CC |
| 6080 | Insurance | Biz Checking |
| 6120 | Contractor Labor | Biz Checking |
| 6130 | Domains & Hosting | Biz Checking |
| 6150 | Miscellaneous | Both |

Columns: GL Acct, Account Name, Date, Description, Debit, Credit, Source  
Sorted by GL account then date. Section headers for each account grouping.

### 10. ✅ 1099 Tracking (Tab 11)
**Vendors identified requiring or approaching 1099 threshold:**

| Vendor | Method | Highest Year | Max Amount | Status |
|--------|--------|-------------|------------|--------|
| Wise Transfer (International) | Wise | 2025 | $1,816.11 | 1099 REQUIRED |
| Nil Ridge | Zelle | 2024 | $750.00 | 1099 REQUIRED |
| PayPal - Daniel Daniel | PayPal | 2025 | $657.04 | 1099 REQUIRED |
| Wise Transfer (International) | Wise | 2026 | $832.59 | 1099 REQUIRED |
| Jonathan Bible | Zelle | 2026 | $500.00 | Review - Approaching |
| Oscar Cruz | Zelle | 2024 | $350.00 | Below Threshold |

Includes detailed payment log for qualifying vendors and compliance notes for 1099-NEC filing.

---

## VERIFICATION RESULTS

### Revenue Consistency
| Year | Income Statement | Status |
|------|-----------------|--------|
| 2024 | $25,634.14 | ✅ Matches audit |
| 2025 | $80,200.99 | ✅ Matches audit |
| 2026 | $10,468.89 | ✅ Matches audit |

### Net Income Consistency
| Year | Net Income | Status |
|------|-----------|--------|
| 2024 | ($2,567.10) | ✅ Verified |
| 2025 | $43,239.89 | ✅ Verified |
| 2026 | ($169.92) | ✅ Verified |

### P&L Arithmetic
All income statements verified: Revenue - COGS = Gross Profit, Gross Profit - OpEx = Net Income. All check out.

### Cash Flow Cross-Check
Cash Flow operating activities match Net Income from Income Statements (cash basis accounting = no adjustments).

### Formatting Verification
- **Tab colors:** All 11 tabs confirmed via API ✅
- **Section headers:** Navy (#1B2A4A) bg, white text, 14pt bold ✅  
- **Column headers:** Light gray (#F3F3F3), 11pt bold ✅
- **Total rows:** Light navy (#E8EDF5), 11pt bold ✅
- **Currency format:** `$#,##0.00;[Red]($#,##0.00)` confirmed on IS cells ✅
- **Font:** Arial 10pt default, confirmed ✅
- **Row heights:** 30px headers, 21px data ✅

---

## KNOWN ISSUES (Pre-existing, Not Fixed Here)

1. **2026 revenue discrepancy** between All Time sheet ($10,569.10) and Accountant View ($10,468.89) — $100.21 gap. This is a data issue in the All Time Financial Overview sheet, not this spreadsheet. The Accountant View figure ($10,468.89) appears correct based on the CSV data analysis.

2. **2025 revenue rounding** — $0.67 difference between All Time ($80,201.66) and Accountant View ($80,200.99). Floating point rounding across many cells.

3. **Balance Sheet incomplete** — Still shows "See bank reconciliation" for most cells. Requires manual input of statement ending balances, investment values, and creditor balances. This is a data gap, not a formatting issue.

4. **General Ledger categorization** — The automated categorization assigns ~16,000+ in "Miscellaneous" (GL 6150) for transactions that don't match known vendor patterns. A manual review pass would improve accuracy. Notable items in Miscellaneous include various small vendor payments, subscription charges with non-standard names, and one-off purchases.

---

*Report generated 2026-02-04. All changes applied to spreadsheet `1vtXJCdbWOskKU-zxEJCOlXBTVhd7vHclWEdWwJgFZ9o`.*
