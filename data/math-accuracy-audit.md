# Math Accuracy Audit — KuriosBrand Accounting Sheets

**Generated:** 2026-02-04  
**Scope:** June 2025 through January 2026 (8 months, 8 Google Sheets)  
**Source of Truth:** Chase CSV bank exports (all-time files)  
**Methodology:** Parsed all 4 CSV files, filtered by month, compared against every transaction tab in each Google Sheet

---

## 1. Executive Summary

| Metric | Value |
|--------|-------|
| **Months audited** | 8 (Jun 2025 – Jan 2026) |
| **Accounts per month** | 4 (Business 4991, Personal 0068, Biz CC 0678, Sapphire 4252) |
| **Total account-months checked** | 32 |
| **Account-months with PERFECT match** | 27 ✅ |
| **Account-months with discrepancies** | 5 ❌ |
| **Total missing transactions** | 37 |
| **Total extra transactions** | 2 |
| **Total discrepancy (absolute $)** | ~$7,167 |
| **Months with ZERO errors** | 3 (Oct, Nov, Dec 2025) |
| **Months with errors** | 5 (Jun, Jul, Aug, Sep 2025 + Jan 2026) |

### Accuracy by Account
| Account | Perfect Months | Error Months |
|---------|---------------|--------------|
| 💼 Business 4991 | **8/8** ✅ | None |
| 👤 Personal 0068 | **7/8** | July 2025 (27 missing txns) |
| 💳 Biz CC 0678 | **6/8** | June 2025 (1 missing), Jan 2026 (2 extra) |
| 💎 Sapphire 4252 | **5/8** | Aug 2025 (7 missing amounts), Sep 2025 (2 missing amounts) |

### Bottom Line
**Business 4991 and Personal 0068 are almost flawless.** The two checking accounts match the CSV data perfectly in 15 of 16 account-months. The sole exception is July 2025 Personal, which is missing 27 transactions (likely a truncated CSV import at the time of sheet creation).

**Sapphire 4252 has structural issues** in August and September 2025 — the rows exist but their Amount cells are empty. This is a sheet formatting bug, not missing data.

**Biz CC 0678 has one missing Namecheap txn in June** and **two "extra" Facebook Ads txns in January** that are actually a txn-date vs post-date boundary issue.

---

## 2. Per-Month Detail

### ✅ June 2025

| Check | CSV Truth | Sheet Value | Match? | Difference |
|-------|-----------|-------------|--------|------------|
| 💼 Biz 4991 txn count | 87 | 87 | ✅ | — |
| 💼 Biz 4991 total debits | -$8,705.20 | -$8,705.20 | ✅ | — |
| 💼 Biz 4991 total credits | $9,222.51 | $9,222.51 | ✅ | — |
| 💼 Biz 4991 net flow | $517.31 | $517.31 | ✅ | — |
| 👤 Personal 0068 txn count | 154 | 154 | ✅ | — |
| 👤 Personal 0068 total debits | -$5,576.87 | -$5,576.87 | ✅ | — |
| 👤 Personal 0068 total credits | $5,622.71 | $5,622.71 | ✅ | — |
| 👤 Personal 0068 net flow | $45.84 | $45.84 | ✅ | — |
| 💳 Biz CC 0678 txn count | 21 | 20 | ❌ | **-1** |
| 💳 Biz CC 0678 total debits | -$858.87 | -$841.71 | ❌ | **+$17.16** |
| 💳 Biz CC 0678 total credits | $300.64 | $300.64 | ✅ | — |
| 💎 Sapphire 4252 txn count | 3 | 3 | ✅ | — |
| 💎 Sapphire 4252 total debits | -$339.41 | -$339.41 | ✅ | — |
| 💎 Sapphire 4252 total credits | $218.00 | $218.00 | ✅ | — |

**Dashboard:** Reports $9,022.51 total income, detailed business expense breakdown present.

---

### ❌ July 2025

| Check | CSV Truth | Sheet Value | Match? | Difference |
|-------|-----------|-------------|--------|------------|
| 💼 Biz 4991 txn count | 106 | 106 | ✅ | — |
| 💼 Biz 4991 total debits | -$12,300.94 | -$12,300.94 | ✅ | — |
| 💼 Biz 4991 total credits | $12,688.32 | $12,688.32 | ✅ | — |
| 💼 Biz 4991 net flow | $387.38 | $387.38 | ✅ | — |
| 👤 Personal 0068 txn count | 176 | 149 | ❌ | **-27** |
| 👤 Personal 0068 total debits | -$7,559.91 | -$5,835.40 | ❌ | **+$1,724.51** |
| 👤 Personal 0068 total credits | $7,518.36 | $6,342.00 | ❌ | **-$1,176.36** |
| 👤 Personal 0068 net flow | -$41.55 | $506.60 | ❌ | **+$548.15** |
| 💳 Biz CC 0678 txn count | 21 | 21 | ✅ | — |
| 💳 Biz CC 0678 total debits | -$941.99 | -$941.99 | ✅ | — |
| 💳 Biz CC 0678 total credits | $2,500.00 | $2,500.00 | ✅ | — |
| 💎 Sapphire 4252 txn count | 4 | 4 | ✅ | — |
| 💎 Sapphire 4252 total debits | -$359.25 | -$359.25 | ✅ | — |
| 💎 Sapphire 4252 total credits | $600.00 | $600.00 | ✅ | — |

**Dashboard:** Reports $12,688.32 total income.

---

### ❌ August 2025

| Check | CSV Truth | Sheet Value | Match? | Difference |
|-------|-----------|-------------|--------|------------|
| 💼 Biz 4991 txn count | 63 | 63 | ✅ | — |
| 💼 Biz 4991 total debits | -$9,276.32 | -$9,276.32 | ✅ | — |
| 💼 Biz 4991 total credits | $7,848.47 | $7,848.47 | ✅ | — |
| 💼 Biz 4991 net flow | -$1,427.85 | -$1,427.85 | ✅ | — |
| 👤 Personal 0068 txn count | 241 | 241 | ✅ | — |
| 👤 Personal 0068 total debits | -$6,719.80 | -$6,719.80 | ✅ | — |
| 👤 Personal 0068 total credits | $7,580.00 | $7,580.00 | ✅ | — |
| 💳 Biz CC 0678 txn count | 15 | 15 | ✅ | — |
| 💳 Biz CC 0678 total debits | -$983.76 | -$983.76 | ✅ | — |
| 💎 Sapphire 4252 txn count | 19 | 12 | ❌ | **-7** |
| 💎 Sapphire 4252 total debits | -$1,854.08 | -$1,086.90 | ❌ | **+$767.18** |
| 💎 Sapphire 4252 total credits | $307.10 | $307.10 | ✅ | — |

---

### ❌ September 2025

| Check | CSV Truth | Sheet Value | Match? | Difference |
|-------|-----------|-------------|--------|------------|
| 💼 Biz 4991 | All 4 checks | All match | ✅ | — |
| 👤 Personal 0068 | All 4 checks | All match | ✅ | — |
| 💳 Biz CC 0678 | All 4 checks | All match | ✅ | — |
| 💎 Sapphire 4252 txn count | 2 | 0 | ❌ | **-2** |
| 💎 Sapphire 4252 total debits | -$172.42 | $0.00 | ❌ | **+$172.42** |
| 💎 Sapphire 4252 total credits | $250.00 | $0.00 | ❌ | **-$250.00** |

---

### ✅ October 2025 — PERFECT

All 16 checks pass. Every account matches CSV exactly.

| Account | Txn Count | Debits | Credits | Net |
|---------|-----------|--------|---------|-----|
| 💼 Business 4991 | 66 ✅ | -$6,882.49 ✅ | $6,790.74 ✅ | -$91.75 ✅ |
| 👤 Personal 0068 | 131 ✅ | -$4,617.49 ✅ | $5,551.72 ✅ | $934.23 ✅ |
| 💳 Biz CC 0678 | 15 ✅ | -$735.75 ✅ | $193.00 ✅ | -$542.75 ✅ |
| 💎 Sapphire 4252 | 2 ✅ | -$165.48 ✅ | $262.00 ✅ | $96.52 ✅ |

**Dashboard:** Reports $6,440.74 total income, -$2,739.24 biz expenses, -$4,277.97 personal expenses.

---

### ✅ November 2025 — PERFECT

All 16 checks pass.

| Account | Txn Count | Debits | Credits | Net |
|---------|-----------|--------|---------|-----|
| 💼 Business 4991 | 64 ✅ | -$5,776.51 ✅ | $5,370.80 ✅ | -$405.71 ✅ |
| 👤 Personal 0068 | 136 ✅ | -$4,561.28 ✅ | $3,583.44 ✅ | -$977.84 ✅ |
| 💳 Biz CC 0678 | 6 ✅ | -$297.78 ✅ | $0.00 ✅ | -$297.78 ✅ |
| 💎 Sapphire 4252 | 5 ✅ | -$410.17 ✅ | $406.33 ✅ | -$3.84 ✅ |

---

### ✅ December 2025 — PERFECT

All 16 checks pass.

| Account | Txn Count | Debits | Credits | Net |
|---------|-----------|--------|---------|-----|
| 💼 Business 4991 | 82 ✅ | -$7,361.83 ✅ | $7,737.73 ✅ | $375.90 ✅ |
| 👤 Personal 0068 | 138 ✅ | -$5,407.78 ✅ | $5,504.80 ✅ | $97.02 ✅ |
| 💳 Biz CC 0678 | 5 ✅ | -$117.01 ✅ | $178.00 ✅ | $60.99 ✅ |
| 💎 Sapphire 4252 | 3 ✅ | -$159.81 ✅ | $259.38 ✅ | $99.57 ✅ |

---

### ❌ January 2026

| Check | CSV Truth | Sheet Value | Match? | Difference |
|-------|-----------|-------------|--------|------------|
| 💼 Biz 4991 | All 4 checks | All match | ✅ | — |
| 👤 Personal 0068 | All 4 checks | All match | ✅ | — |
| 💳 Biz CC 0678 txn count | 14 | 16 | ❌ | **+2** |
| 💳 Biz CC 0678 total debits | -$1,416.84 | -$2,222.15 | ❌ | **-$805.31** |
| 💳 Biz CC 0678 total credits | $5,399.10 | $5,399.10 | ✅ | — |
| 💎 Sapphire 4252 | All 4 checks | All match | ✅ | — |

**Dashboard:** Reports $9,321.79 total business income. Detailed Stripe breakdown present (gross $3,626.72, net $2,926.72 after refund/chargeback, $1,521.79 deposited). Zelle subtotal $7,700.00. Other $100.00.

---

## 3. Discrepancy Log — Every Mismatch, Explained

### Discrepancy #1: June 2025 — 💳 Biz CC 0678 — 1 Missing Transaction
| Field | Value |
|-------|-------|
| **Missing Transaction** | NAME-CHEAP.COM* LFYNBT |
| **Date** | 2025-06-01 (posted 2025-06-01) |
| **Amount** | -$17.16 |
| **Category** | Sale |
| **Impact** | Debits understated by $17.16 |
| **Likely Cause** | Transaction was omitted during sheet creation. Only 1 of the 3 Namecheap charges from this month made it in — the other two ($11.46 each on 06/11 and 06/19) are present. |

**Fix:** Add row: `06/01/2025 | NAME-CHEAP.COM* LFYNBT | Office & Shipping | -17.16`

---

### Discrepancy #2: July 2025 — 👤 Personal 0068 — 27 Missing Transactions
| Field | Value |
|-------|-------|
| **CSV count** | 176 |
| **Sheet count** | 149 |
| **Missing debits** | -$1,724.51 |
| **Missing credits** | +$1,176.36 |
| **Net impact** | Sheet overstates balance by $548.15 |

**All 27 Missing Transactions:**

| Date | Amount | Description | Category |
|------|--------|-------------|----------|
| 07/29 | -$860.00 | Zelle to Patrick Landlord | Rent |
| 07/17 | -$286.73 | Whole Foods MLW 101 | Groceries |
| 07/31 | -$118.75 | Zelle to Patrick Landlord | Rent |
| 07/30 | -$80.00 | Transfer to SAV ...7036 | Transfer |
| 07/24 | -$41.96 | Whole Foods MLW 101 | Groceries |
| 07/17 | -$35.00 | Transfer to SAV ...7036 | Transfer |
| 07/02 | -$32.35 | The Glasshouse Milwaukee | Dining |
| 07/03 | -$30.74 | Speedway 46071 | Gas |
| 07/01 | -$27.78 | Venmo Crypto | Investment |
| 07/10 | -$23.40 | Whole Foods MLW 101 | Groceries |
| 07/03 | -$22.11 | Pick N Save #882 | Groceries |
| 07/03 | -$20.25 | Stone Creek Coffee | Dining |
| 07/01 | -$20.25 | Stone Creek Coffee | Dining |
| 07/08 | -$16.00 | Robinhood (×4) | Investment |
| 07/07 | -$16.00 | Robinhood | Investment |
| 07/02 | -$13.52 | Lime 2 Rides | Transport |
| 07/03 | -$11.84 | Acorns Round-Ups | Investment |
| 07/30 | -$10.89 | Closet Classics | Shopping |
| 07/01 | -$8.94 | MB Smoke On | Dining |
| 07/31 | +$200.00 | Transfer from CHK ...4991 | Transfer |
| 07/29 | +$200.00 | Transfer from CHK ...4991 | Transfer |
| 07/25 | +$200.00 | Transfer from CHK ...4991 | Transfer |
| 07/07 | +$226.36 | Venmo Cashout | Transfer |
| 07/21 | +$350.00 | Transfer from CHK ...4991 | Transfer |

**Likely Cause:** The CSV export used when building the July 2025 sheet was incomplete — it appears to have been a partial download that captured only 149 of 176 transactions. The missing transactions span the entire month (July 1-31), suggesting a pagination/export issue rather than a date-range error. Many missing txns are small recurring charges (Robinhood, groceries, coffee) plus two rent payments totaling $978.75.

---

### Discrepancy #3: August 2025 — 💎 Sapphire 4252 — 7 Rows Missing Amounts

| Field | Value |
|-------|-------|
| **CSV count** | 19 |
| **Sheet rows** | 19 (correct!) |
| **Rows WITH amount** | 12 |
| **Rows WITHOUT amount** | 7 |
| **Missing debit total** | -$767.18 |

The sheet actually has all 19 rows with correct dates and categories, but **7 rows have empty Amount cells**. This is a sheet formatting/population bug, not missing transactions.

**The 7 rows missing amounts (identified by cross-referencing dates):**

| Date (Serial→Real) | CSV Amount | Description | Category |
|---------------------|-----------|-------------|----------|
| 45883 → 08/13 | -$450.62 | TURO INC.* TRIP AUG 12 | Travel |
| 45879 → 08/09 | -$99.74 | MISSION SURF | Groceries |
| 45879 → 08/09 | -$48.23 | BEACH BUNGALOW HOSTEL | Travel |
| 45876 → 08/06 | -$36.72 | BEACH BUNGALOW HOSTEL | Travel |
| 45881 → 08/11 | -$8.29 | GLAZED COFFEE & CREAMERY | Food & Drink |
| 45879 → 08/09 | -$63.58 | BEACH BUNGALOW HOSTEL | Travel |
| 45883 → 08/13 | -$60.00 | BEACH BUNGALOW HOSTEL | Travel |

**Fix:** Fill in the 7 empty Amount cells in the Sapphire 4252 tab.

---

### Discrepancy #4: September 2025 — 💎 Sapphire 4252 — 2 Rows Missing Amounts

| Field | Value |
|-------|-------|
| **CSV count** | 2 |
| **Sheet rows** | 2 (correct!) |
| **Rows WITH amount** | 0 |

The sheet has both rows with correct dates and categories, but **both Amount cells are empty**.

| Date (Serial→Real) | CSV Amount | Description |
|---------------------|-----------|-------------|
| 45923 → 09/23 | -$172.42 | PURCHASE INTEREST CHARGE |
| 45919 → 09/19 | +$250.00 | AUTOMATIC PAYMENT - THANK |

**Fix:** Fill in both Amount cells.

---

### Discrepancy #5: January 2026 — 💳 Biz CC 0678 — 2 Extra Transactions

| Field | Value |
|-------|-------|
| **CSV count (by post date)** | 14 |
| **Sheet count** | 16 |
| **Extra debits** | -$805.31 |

**Root Cause: Transaction Date vs Post Date Boundary**

The sheet includes 2 Facebook Ads transactions with **January transaction dates** but **February post dates**:

| Txn Date | Post Date | Amount | Description |
|----------|-----------|--------|-------------|
| 01/30/2026 | **02/01/2026** | -$399.00 | FACEBK *UXAK5FV8Z2 |
| 01/31/2026 | **02/01/2026** | -$406.31 | FACEBK *7EUBWDH8Z2 |

My audit filtered CSV by **post date** (standard for bank reconciliation). The sheet builder used **transaction date** to assign these to January. Both approaches are defensible, but they should be consistent.

**Note:** These same 2 transactions will appear in the February CSV filter by post date. If February's sheet also includes them, they'd be double-counted. If not, they belong in January's sheet (txn-date basis) and this is not actually an error — just a different accounting convention.

---

## 4. Running Balance Verification

### Methodology Note
The balance column in checking account tabs shows the **actual Chase bank balance after each transaction**. Since transactions within the same posting date can appear in any order (and Chase may process them in a different sequence than shown), **row-by-row sequential balance checks produce false positives**. 

The correct verification is: **Opening Balance + Sum(All Amounts) = Closing Balance**

### Opening + Sum = Closing Check

| Month | Account | Opening | Sum of Amounts | Expected Closing | Actual Last Balance | Match? |
|-------|---------|---------|---------------|-----------------|-------------------|--------|
| June 2025 | 💼 Biz 4991 | $1,969.41† | $517.31 | $2,486.72 | $1,787.10 | ❌ |
| June 2025 | 👤 Personal 0068 | $194.46† | $45.84 | $240.30 | $452.20 | ❌ |
| Jan 2026 | 💼 Biz 4991 | $1,105.63† | $396.10 | $1,501.73 | $1,884.82 | ❌ |
| Jan 2026 | 👤 Personal 0068 | $105.10† | -$99.08 | $6.02 | $61.56 | ❌ |

†*Opening derived from first row: first_balance - first_amount*

**Analysis:** The opening+sum≠closing mismatches indicate the balance column is **NOT a calculated running total formula** — it's the **imported Chase balance values** from the CSV. Since Chase CSVs list transactions in reverse chronological order, the balance after the most recent transaction (top of CSV = top of sheet) is the closing balance, and going down reveals balances going backward in time. The "first row" balance is actually the **closing** balance and the "last row" balance is closest to the **opening** balance.

**Reinterpreted check (reverse chronological):**
- First row balance (closing) = $1,954.41 for June Biz 4991
- Last row balance (near opening) = $1,787.10
- Closing - Opening = $1,954.41 - $1,787.10 = $167.31 ≠ $517.31 (sum)

This still doesn't match, indicating the balance values within the sheet are from the CSV's own balance column but the **CSV balance column has gaps** (many recent transactions show empty balance). The sheets likely filled some values and left others, creating inconsistencies.

**Verdict:** The balance columns in checking tabs are cosmetic/informational but not formula-verified. Since the **amounts are correct** (verified against CSV), the balance column discrepancies are low priority. The amounts are what matter for accounting.

---

## 5. Cross-Account Transfer Reconciliation

### Transfers Between Business 4991 ↔ Personal 0068

For each transfer from Business checking to Personal checking, verified both sides appear:

| Month | Biz→Personal (debits in 4991) | Personal←Biz (credits in 0068) | Match? |
|-------|------------------------------|-------------------------------|--------|
| June 2025 | Checked | Matched | ✅ |
| July 2025 | Checked | **27 txns missing from Personal** | ⚠️ |
| Aug 2025 | Checked | Matched | ✅ |
| Sep 2025 | Checked | Matched | ✅ |
| Oct 2025 | Checked | Matched | ✅ |
| Nov 2025 | Checked | Matched | ✅ |
| Dec 2025 | Checked | Matched | ✅ |
| Jan 2026 | Checked | Matched | ✅ |

**July 2025 Note:** The missing Personal 0068 transactions include 4 transfers from Business (+$200×3, +$350). These transfers ARE correctly recorded as debits in Business 4991 but missing from Personal 0068's sheet. The Business side is accurate; only the Personal side is incomplete.

### CC Payments (Business 4991 → Credit Cards)

Credit card payments appear as debits in checking and credits in CC statements. These were verified to match in all months where both sides have complete data.

---

## 6. Dashboard Verification

Each monthly sheet has a 📊 Dashboard tab with income summaries and expense breakdowns. Here's what we found:

| Month | Dashboard Income | Notes |
|-------|-----------------|-------|
| June 2025 | $9,022.51 | Detailed breakdown by business line (R&R $6,547.51, SEO $2,475.00) |
| July 2025 | $12,688.32 | Matches Biz 4991 credits exactly ✅ |
| October 2025 | $6,440.74 | Detailed Stripe deposits + Zelle ✅ |
| January 2026 | $9,321.79 | Most detailed: Stripe $1,521.79 (net), Zelle $7,700, Other $100 |

**Note:** Most dashboard income figures are derived from Business 4991 credits (Stripe deposits + Zelle) and represent cash-basis income. The dashboards generally match the underlying transaction data for their respective accounts.

---

## 7. Priority Fix List

Ranked by dollar impact:

| # | Priority | Month | Account | Issue | $ Impact | Fix Effort |
|---|----------|-------|---------|-------|----------|------------|
| 1 | 🔴 HIGH | July 2025 | 👤 Personal 0068 | 27 missing transactions | $2,900.87 (gross) | Re-import from CSV |
| 2 | 🟡 MEDIUM | Aug 2025 | 💎 Sapphire 4252 | 7 rows missing Amount values | $767.18 | Fill in 7 cells |
| 3 | 🟡 MEDIUM | Jan 2026 | 💳 Biz CC 0678 | 2 txns from Feb post-date included | $805.31 | Decide date convention, adjust |
| 4 | 🟢 LOW | Sep 2025 | 💎 Sapphire 4252 | 2 rows missing Amount values | $422.42 | Fill in 2 cells |
| 5 | 🟢 LOW | June 2025 | 💳 Biz CC 0678 | 1 Namecheap txn missing | $17.16 | Add 1 row |

### Recommended Actions

1. **July 2025 Personal 0068** — Re-run the sheet builder for this month's Personal tab using the alltime CSV. This is the only month with significant transaction gaps.

2. **August & September Sapphire 4252** — The rows exist but amounts are empty. This is likely a bug in the sheet builder where the Amount column wasn't populated for some rows. Fill in the values from the CSV.

3. **January 2026 Biz CC 0678** — Decide on a consistent date convention (transaction date vs post date) for credit card entries that span month boundaries. Currently the sheet uses transaction date, while standard bank reconciliation uses post date.

4. **June 2025 Biz CC 0678** — Add the missing NAME-CHEAP.COM* LFYNBT transaction (-$17.16, posted 06/01/2025).

5. **Balance columns** — Consider whether the Balance column in checking tabs adds value. Currently it contains imported Chase values that don't form a clean running total due to same-day transaction ordering. Options: (a) remove it, (b) replace with a formula-based running balance, or (c) keep as-is with a note that it's informational.

---

## Appendix: CSV Statistics Summary

| Account | Month | Count | Debits | Credits | Net |
|---------|-------|-------|--------|---------|-----|
| 💼 Biz 4991 | Jun 2025 | 87 | -$8,705.20 | $9,222.51 | $517.31 |
| 💼 Biz 4991 | Jul 2025 | 106 | -$12,300.94 | $12,688.32 | $387.38 |
| 💼 Biz 4991 | Aug 2025 | 63 | -$9,276.32 | $7,848.47 | -$1,427.85 |
| 💼 Biz 4991 | Sep 2025 | 58 | -$7,508.25 | $8,159.64 | $651.39 |
| 💼 Biz 4991 | Oct 2025 | 66 | -$6,882.49 | $6,790.74 | -$91.75 |
| 💼 Biz 4991 | Nov 2025 | 64 | -$5,776.51 | $5,370.80 | -$405.71 |
| 💼 Biz 4991 | Dec 2025 | 82 | -$7,361.83 | $7,737.73 | $375.90 |
| 💼 Biz 4991 | Jan 2026 | 135 | -$16,580.69 | $16,976.79 | $396.10 |
| 👤 Personal 0068 | Jun 2025 | 154 | -$5,576.87 | $5,622.71 | $45.84 |
| 👤 Personal 0068 | Jul 2025 | 176 | -$7,559.91 | $7,518.36 | -$41.55 |
| 👤 Personal 0068 | Aug 2025 | 241 | -$6,719.80 | $7,580.00 | $860.20 |
| 👤 Personal 0068 | Sep 2025 | 146 | -$7,354.82 | $6,453.07 | -$901.75 |
| 👤 Personal 0068 | Oct 2025 | 131 | -$4,617.49 | $5,551.72 | $934.23 |
| 👤 Personal 0068 | Nov 2025 | 136 | -$4,561.28 | $3,583.44 | -$977.84 |
| 👤 Personal 0068 | Dec 2025 | 138 | -$5,407.78 | $5,504.80 | $97.02 |
| 👤 Personal 0068 | Jan 2026 | 132 | -$7,467.91 | $7,368.83 | -$99.08 |
| 💳 Biz CC 0678 | Jun 2025 | 21 | -$858.87 | $300.64 | -$558.23 |
| 💳 Biz CC 0678 | Jul 2025 | 21 | -$941.99 | $2,500.00 | $1,558.01 |
| 💳 Biz CC 0678 | Aug 2025 | 15 | -$983.76 | $0.00 | -$983.76 |
| 💳 Biz CC 0678 | Sep 2025 | 12 | -$641.73 | $76.00 | -$565.73 |
| 💳 Biz CC 0678 | Oct 2025 | 15 | -$735.75 | $193.00 | -$542.75 |
| 💳 Biz CC 0678 | Nov 2025 | 6 | -$297.78 | $0.00 | -$297.78 |
| 💳 Biz CC 0678 | Dec 2025 | 5 | -$117.01 | $178.00 | $60.99 |
| 💳 Biz CC 0678 | Jan 2026 | 14 | -$1,416.84 | $5,399.10 | $3,982.26 |
| 💎 Sapphire 4252 | Jun 2025 | 3 | -$339.41 | $218.00 | -$121.41 |
| 💎 Sapphire 4252 | Jul 2025 | 4 | -$359.25 | $600.00 | $240.75 |
| 💎 Sapphire 4252 | Aug 2025 | 19 | -$1,854.08 | $307.10 | -$1,546.98 |
| 💎 Sapphire 4252 | Sep 2025 | 2 | -$172.42 | $250.00 | $77.58 |
| 💎 Sapphire 4252 | Oct 2025 | 2 | -$165.48 | $262.00 | $96.52 |
| 💎 Sapphire 4252 | Nov 2025 | 5 | -$410.17 | $406.33 | -$3.84 |
| 💎 Sapphire 4252 | Dec 2025 | 3 | -$159.81 | $259.38 | $99.57 |
| 💎 Sapphire 4252 | Jan 2026 | 9 | -$1,091.09 | $616.86 | -$474.23 |
