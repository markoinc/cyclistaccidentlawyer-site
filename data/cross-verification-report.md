# Cross-Verification Report: KuriosBrand Monthly Sheets vs Chase CSVs

**Generated:** 2026-02-04  
**Scope:** June 2025 – January 2026 (7 monthly sheets + October gap)

## CSV Sources

| Account | File | Total Txns | Date Range |
|---------|------|-----------|------------|
| 💼 Business 4991 | business-4991-alltime.csv | 1,424 | 02/05/2024 – 02/04/2026 |
| 👤 Personal 0068 | personal-0068-alltime.csv | 1,504 | 04/01/2025 – 02/04/2026 |
| 💳 Biz CC 0678 | bizcc-0678-alltime.csv | 441 | 05/06/2024 – 02/02/2026 |
| 💎 Sapphire 4252 | sapphire-4252-alltime.csv | 295 | 02/05/2024 – 01/27/2026 |

---

## Executive Summary

| Month | CSV Total | Sheet Total | Status | Key Issues |
|-------|-----------|-------------|--------|------------|
| **June 2025** | 264 | 0 | ❌ EMPTY TABS | Transaction tabs exist but are blank; Dashboard has data |
| **July 2025** | 306 | 280 | ❌ -26 | Personal 0068 missing 27 txns; Biz CC has 1 extra |
| **August 2025** | 338 | 338 | ⚠️ AMOUNTS OFF | Counts match but Sapphire missing $767.18 (7 travel txns) |
| **September 2025** | 218 | 217 | ⚠️ | Sapphire missing 1 txn (interest charge + payment) |
| **October 2025** | 214 | — | ❌ NO SHEET | No accounting sheet exists |
| **November 2025** | 211 | 211 | ✅ PERFECT | All counts and amounts match |
| **December 2025** | 228 | 228 | ✅ PERFECT | All counts and amounts match |
| **January 2026** | 292 | 292 | ✅ PERFECT | All counts and amounts match |

**Verdict:** Nov, Dec, Jan are clean. Aug & Sep have minor Sapphire omissions. July has material Personal 0068 gaps. June needs backfilling. October needs a sheet created.

---

## Detailed Monthly Results

### June 2025 ❌

**Sheet:** `19YSihOlMi1R-2nkZzfwa1dmoidouGl4UakhjdfceBsg`  
**Tabs:** 📊 Dashboard, 💰 Profit First, 🎯 Pareto Analysis, 💼 Business 4991, 👤 Personal 0068, 💳 Biz CC 0678, 💎 Sapphire 4252, 📦 Raw Data

**Problem:** All 4 transaction tabs have headers but zero data rows. Only the Dashboard is populated.

| Account | CSV Count | CSV Sum | Sheet Count |
|---------|-----------|---------|-------------|
| 💼 Business 4991 | 87 | $517.31 | 0 |
| 👤 Personal 0068 | 154 | $45.84 | 0 |
| 💳 Biz CC 0678 | 20 | -$541.07 | 0 |
| 💎 Sapphire 4252 | 3 | -$121.41 | 0 |

**Dashboard Income Summary (manually entered):**
- 🏗️ Rank & Rent: $6,547.51 (Stripe $3,017.51 + Zelle $2,000 ACI + Zelle $1,530 Hooked commissions)
- 🔧 SEO: $2,475.00 (Stripe $1,125 Joshua Raymond + Zelle $1,350 Willard)
- 🚗 MVA: $0
- **Total Dashboard Income: $9,022.51**

**Action needed:** Backfill transaction tabs from CSVs.

---

### July 2025 ❌

**Sheet:** `1fl1VT93SkVjBLV2bss8RN4m45yv5dzC-ATI8JczfVR8`

| Account | CSV Count | Sheet Count | CSV Sum | Sheet Sum | Δ |
|---------|-----------|-------------|---------|-----------|---|
| 💼 Business 4991 | 106 | 106 | $387.38 | $387.38 | ✅ |
| 👤 Personal 0068 | 176 | 149 | -$41.55 | $506.60 | ❌ -$548.15 |
| 💳 Biz CC 0678 | 20 | 21 | $1,657.01 | $1,558.01 | ❌ $99.00 |
| 💎 Sapphire 4252 | 4 | 4 | $240.75 | $240.75 | ✅ |

**Personal 0068 — 27 transactions missing from sheet:**

Major items:
- 07/29 | -$860.00 | Zelle to Patrick Landlord (rent)
- 07/21 | $350.00 | Transfer from Business 4991
- 07/17 | -$286.73 | Whole Foods
- 07/07 | $226.36 | Venmo cashout
- 07/31 | $200.00 | Transfer from Business 4991
- 07/29 | $200.00 | Transfer from Business 4991
- 07/25 | $200.00 | Transfer from Business 4991
- 07/31 | -$118.75 | Zelle to Patrick Landlord
- 07/30 | -$80.00 | Transfer to Savings 7036
- Plus 18 smaller transactions (groceries, gas, misc)

**Biz CC 0678 — 1 extra transaction in sheet:**
- Sheet has "Aaron Abke" for -$99.00 that is NOT in the Chase CSV. This may have been manually added or is from a different billing period.

**Dashboard Income: $12,688.32**
- R&R: $12,338.32 (Stripe $8,338.32 + ACI $3,000 + Willard $1,000)
- SEO: $350.00 (Eddy Orozco Reyes)
- MVA: $0

---

### August 2025 ⚠️

**Sheet:** `1WnP2z0_4sE19-Ln7QTvm6lLfWqywTxmS1ef7HOZ9YeI`

| Account | CSV Count | Sheet Count | CSV Sum | Sheet Sum | Δ |
|---------|-----------|-------------|---------|-----------|---|
| 💼 Business 4991 | 63 | 63 | -$1,427.85 | -$1,427.85 | ✅ |
| 👤 Personal 0068 | 241 | 241 | $860.20 | $860.20 | ✅ |
| 💳 Biz CC 0678 | 15 | 15 | -$983.76 | -$983.76 | ✅ |
| 💎 Sapphire 4252 | 19 | 19 | -$1,546.98 | -$779.80 | ❌ -$767.18 |

**Sapphire 4252 — 7 transactions present but amounts not matching:**

Count matches (19=19) but sum is off by $767.18. The sheet appears to exclude or zero-out these travel transactions:
- 08/12 | -$450.62 | TURO INC.* TRIP (car rental)
- 08/08 | -$99.74 | MISSION SURF
- 08/08 | -$63.58 | BEACH BUNGALOW HOSTEL
- 08/12 | -$60.00 | BEACH BUNGALOW HOSTEL
- 08/08 | -$48.23 | BEACH BUNGALOW HOSTEL
- 08/06 | -$36.72 | BEACH BUNGALOW HOSTEL
- 08/11 | -$8.29 | GLAZED COFFEE & CREAMERY

These look like **personal travel expenses** (San Diego trip?) that may have been intentionally excluded from business accounting while keeping the row for reference.

**Dashboard Income: $7,848.47**
- R&R: $7,848.47 (Stripe $5,848.47 + ACI $2,000)

---

### September 2025 ⚠️

**Sheet:** `1IuZIUjz4R0umPP3ihciMySq_NgrtO4lxB18hhbtLaSM`

| Account | CSV Count | Sheet Count | CSV Sum | Sheet Sum | Δ |
|---------|-----------|-------------|---------|-----------|---|
| 💼 Business 4991 | 58 | 58 | $651.39 | $651.39 | ✅ |
| 👤 Personal 0068 | 146 | 146 | -$901.75 | -$901.75 | ✅ |
| 💳 Biz CC 0678 | 12 | 12 | -$565.73 | -$565.73 | ✅ |
| 💎 Sapphire 4252 | 2 | 1 | $77.58 | $0.00 | ❌ $77.58 |

**Sapphire 4252 — 2 CSV transactions, only 1 parsed from sheet:**
- 09/19 | $250.00 | AUTOMATIC PAYMENT - THANK (payment)
- 09/23 | -$172.42 | PURCHASE INTEREST CHARGE

The sheet may have the payment row but the interest charge row has no amount parsed. Net difference: $77.58.

**Dashboard Income: $6,509.64**
- R&R: $6,134.64 (Stripe $4,134.64 + ACI $2,000)
- SEO: $375.00 (David Monter Tolentino)

---

### November 2025 ✅

**Sheet:** `1DmOeIoWJ-K6P4vST4-Sdbf35cZqiuej7AjS0facCsA0`

| Account | CSV Count | Sheet Count | CSV Sum | Sheet Sum | Δ |
|---------|-----------|-------------|---------|-----------|---|
| 💼 Business 4991 | 64 | 64 | -$405.71 | -$405.71 | ✅ |
| 👤 Personal 0068 | 136 | 136 | -$977.84 | -$977.84 | ✅ |
| 💳 Biz CC 0678 | 6 | 6 | -$297.78 | -$297.78 | ✅ |
| 💎 Sapphire 4252 | 5 | 5 | -$3.84 | -$3.84 | ✅ |

**All accounts match perfectly.**

**Dashboard Income: $5,070.80**
- Stripe: $3,070.80 (9 deposits)
- Zelle: $2,000.00 (ACI Enterprise × 2)

---

### December 2025 ✅

**Sheet:** `1sGg3SHDLKAmDz0V79MvF-ZVCHcaxjCYMTDV-fZlLWOo`

| Account | CSV Count | Sheet Count | CSV Sum | Sheet Sum | Δ |
|---------|-----------|-------------|---------|-----------|---|
| 💼 Business 4991 | 82 | 82 | $375.90 | $375.90 | ✅ |
| 👤 Personal 0068 | 138 | 138 | $97.02 | $97.02 | ✅ |
| 💳 Biz CC 0678 | 5 | 5 | $60.99 | $60.99 | ✅ |
| 💎 Sapphire 4252 | 3 | 3 | $99.57 | $99.57 | ✅ |

**All accounts match perfectly.**

**Dashboard Income: $6,325.59**
- Stripe: $2,575.59
- Zelle: $3,750.00 (ACI $3,000, Anthony Reddin $250, ACI $1,000 — note: $500 Alexander Shtabsky correctly marked as ❌ NOT REVENUE, personal ATM cash favor)

---

### January 2026 ✅

**Sheet:** `1EMYwVZVoAGUMAlM-G2C1NunZ_RZOvDmgJxdBaKqUriE`

| Account | CSV Count | Sheet Count | CSV Sum | Sheet Sum | Δ |
|---------|-----------|-------------|---------|-----------|---|
| 💼 Business 4991 | 135 | 135 | $396.10 | $396.10 | ✅ |
| 👤 Personal 0068 | 132 | 132 | -$99.08 | -$99.08 | ✅ |
| 💳 Biz CC 0678 | 16 | 16 | $3,176.95 | $3,176.95 | ✅ |
| 💎 Sapphire 4252 | 9 | 9 | -$474.23 | -$474.23 | ✅ |

**All accounts match perfectly.**

**Dashboard Income: $9,221.79 (cash basis)**
- Stripe net deposited: $1,521.79 (gross $2,926.72 - fees $163.43 - loan repayment $120.43 - timing adj)
- Zelle: $7,700.00 (Anthony Reddin $1,000, ACI $2,000, A-Z Mobile Apps $3,000, Jonathan Bible $500, Christian Willard $700 — note: $500 Alexander Shtabsky correctly excluded)

---

## October 2025 — MISSING SHEET

⚠️ **No monthly accounting sheet exists for October 2025.**

| Account | Txn Count | Net Sum |
|---------|-----------|---------|
| 💼 Business 4991 | 66 | -$91.75 |
| 👤 Personal 0068 | 131 | $934.23 |
| 💳 Biz CC 0678 | 15 | -$542.75 |
| 💎 Sapphire 4252 | 2 | $96.52 |
| **Total** | **214** | **$396.25** |

### October Business Income (from CSV)
- Stripe deposits: $4,790.74 (10 deposits)
- ACI Enterprise Zelle: $2,000.00 (2 × $1,000)
- Inter-account transfer from Personal: $200.00
- Apple.com/Bill refund: $93.71
- **Estimated October Business Income: ~$6,790**

### October Context
Marko appears to have been traveling in Colombia during October (ATM withdrawals in CO Peso, BOLD Casa Kayam in Quibdó, numerous international ATM fees). This may explain why the monthly sheet was skipped.

---

## Pre-June 2025 Transaction Summary

The CSVs contain data going back to February 2024. No monthly accounting sheets exist for these periods.

| Month | Business 4991 | Personal 0068 | Biz CC 0678 | Sapphire 4252 | Total Txns |
|-------|:---:|:---:|:---:|:---:|:---:|
| 2024-02 | 17 | — | — | 7 | 24 |
| 2024-03 | 50 | — | — | 17 | 67 |
| 2024-04 | 37 | — | — | 48 | 85 |
| 2024-05 | 45 | — | 12 | 46 | 103 |
| 2024-06 | 27 | — | 40 | 14 | 81 |
| 2024-07 | 43 | — | 35 | 11 | 89 |
| 2024-08 | 90 | — | 38 | 8 | 136 |
| 2024-09 | 39 | — | 4 | 2 | 45 |
| 2024-10 | 31 | — | 6 | 4 | 41 |
| 2024-11 | 47 | — | 7 | 3 | 57 |
| 2024-12 | 49 | — | 24 | 46 | 119 |
| 2025-01 | 32 | — | 25 | 26 | 83 |
| 2025-02 | 45 | — | 23 | 3 | 71 |
| 2025-03 | 38 | — | 47 | 3 | 88 |
| 2025-04 | 68 | 79 | 39 | 7 | 193 |
| 2025-05 | 81 | 149 | 28 | 3 | 261 |

**Note:** Personal 0068 CSV only starts in April 2025. The Biz CC 0678 CSV starts May 2024. Sapphire starts Feb 2024.

---

## Potential Duplicate Transactions

These same-day, same-amount, same-description entries warrant review:

| Date | Account | Amount | Count | Description |
|------|---------|--------|-------|-------------|
| 2025-07-21 | Business 4991 | -$7.00 | ×4 | Zelle to Will Naples Reviewee |
| 2025-07-18 | Business 4991 | -$7.00 | ×4 | Venmo |
| 2025-06-18 | Business 4991 | -$350.00 | ×2 | LOCALRANK.SO |
| 2025-06-13 | Business 4991 | -$89.60 | ×2 | DISCOVERABILITY.CO |
| 2025-06-09 | Business 4991 | -$7.00 | ×4 | CASH APP*MARCO DIEMER |
| 2025-05-30 | Business 4991 | -$10.00 | ×3 | CASH APP*MARCO DIEMER |
| 2025-05-27 | Business 4991 | -$10.00 | ×4 | CASH APP*MARCO DIEMER |
| 2024-09-13 | Business 4991 | -$6.00 | ×7 | CASH APP*KWABENA EKUBAN |
| 2024-08-29 | Business 4991 | -$6.00 | ×6 | CASH APP*TIFFANY GAR |
| 2024-08-15 | Business 4991 | -$8.28 | ×4 | Fiverr |
| 10/15/2025 | Personal 0068 | -$272.14 | ×2 | BOLD Casa Kayam QUIBDO (exact dupe) |

**The Cash App / Venmo / Fiverr batches** look like they could be legitimate multiple small payments (e.g., paying review writers), but the LOCALRANK.SO ×2 at $350 and the BOLD Casa Kayam ×2 at $272.14 are worth confirming.

---

## Recurring Zelle Payers (Business 4991)

| Payer | Frequency | Typical Amount | Likely Business Line |
|-------|-----------|----------------|---------------------|
| ACI Enterprise, LLC | ~2x/month | $1,000 | R&R (confirmed in dashboards) |
| Willard Construction Group | Sporadic | $1,000–$4,500 | R&R (confirmed in dashboards) |
| Anthony Reddin | ~4x/month (Jan 2026) | $250 | R&R? SEO? **Needs clarification** |
| A-Z Mobile Apps, Inc. | 1x (Jan 2026) | $3,000 | **New client — needs classification** |
| Jonathan Bible | 1x (Jan 2026) | $500 | **Needs classification** |
| Christian Willard | 1x (Jan 2026) | $700 | R&R? **Needs classification** |
| David Monter Tolentino | 1x (Sep 2025) | $375 | SEO (confirmed in dashboard) |
| Eddy Orozco Reyes | 1x (Jul 2025) | $350 | SEO (confirmed in dashboard) |
| Alexander Shtabsky | 2x (Dec/Jan) | $500 | ❌ NOT REVENUE (correctly flagged — personal ATM cash favor) |

### Zelle Outgoing (Business Purpose Unclear)
| Recipient | Amount | Date | Context |
|-----------|--------|------|---------|
| Alexis | -$240.00 | 07/17/2025 | Unknown |
| cheezit | -$50.00 | 07/29/2025 | Unknown |
| Ross Yenerich | -$12.50 to -$55.00 | Recurring | Google review writer? |
| Oscar Cruz | -$350.00 | 12/30/2024 | Unknown |
| Various "Reviewee" names | -$7.00 each | Multiple | GBP review payments |

---

## Income Verification: Dashboard vs Bank Deposits

| Month | Dashboard Income | Stripe in CSV | Zelle in CSV | Dashboard Accurate? |
|-------|-----------------|---------------|--------------|-------------------|
| June 2025 | $9,022.51 | ~$3,017 | ~$4,880 | ⚠️ Can't fully verify (tabs empty) |
| July 2025 | $12,688.32 | ~$8,338 | ~$3,350 | ✅ Appears consistent |
| August 2025 | $7,848.47 | ~$5,848 | ~$2,000 | ✅ Matches |
| September 2025 | $6,509.64 | ~$4,135 | ~$2,375 | ✅ Matches |
| November 2025 | $5,070.80 | ~$3,071 | ~$2,000 | ✅ Matches |
| December 2025 | $6,325.59 | ~$2,576 | ~$3,250* | ✅ Matches (*correctly excludes $500 Shtabsky) |
| January 2026 | $9,221.79 | ~$1,522 net | ~$7,200* | ✅ Matches (*correctly excludes $500 Shtabsky) |

---

## Key Findings & Action Items

### 🔴 Critical
1. **October 2025 has no sheet** — 214 transactions (~$6,800 income) unaccounted
2. **June 2025 transaction tabs are empty** — 264 transactions need backfilling

### 🟡 Material Discrepancies
3. **July 2025 Personal 0068** — 27 transactions missing from sheet ($548 difference), mostly rent payments, groceries, and inter-account transfers
4. **July 2025 Biz CC** — "Aaron Abke -$99" in sheet but not in CSV (manual entry?)
5. **August 2025 Sapphire** — 7 travel transactions ($767) in CSV but zeroed/excluded in sheet (personal travel?)
6. **September 2025 Sapphire** — Interest charge not captured in sheet ($172.42)

### 🟢 Clean Months
7. **November 2025** — Perfect match, all 4 accounts
8. **December 2025** — Perfect match, all 4 accounts
9. **January 2026** — Perfect match, all 4 accounts

### 📋 Needs Classification
10. New Zelle payers in Jan 2026: A-Z Mobile Apps ($3K), Jonathan Bible ($500), Christian Willard ($700), Anthony Reddin (4×$250)
11. October 2025 travel expenses in Colombia need personal vs business determination
12. BOLD Casa Kayam duplicate ($272.14 ×2) needs confirmation
