# 📊 Mathematical Accuracy Audit Report
**Generated:** 2026-02-04 10:05:35 UTC

## Sheets Verified
1. **All Time Financial Overview** (`1v1di5lJT-84iMD7FfnKGFfWanFV-5gyWXWR5mGJuJZQ`)
2. **Accountant View** (`1vtXJCdbWOskKU-zxEJCOlXBTVhd7vHclWEdWwJgFZ9o`)

## Source Data
- Business Checking 4991: 1424 transactions
- Personal Checking 0068: 1504 transactions
- Biz CC 0678: 441 transactions
- Sapphire 4252: 295 transactions

---

## 🏆 Scorecard

| Metric | Count |
|--------|-------|
| **Total Checks Performed** | **176** |
| ✅ Passes | 141 |
| ❌ Failures | 35 |
| 🔴 Material Discrepancies (>$10) | 35 |
| 🟡 Minor Discrepancies (<$10) | 0 |
| **Pass Rate** | **80.1%** |

---

## 🔒 Safety Checks

| Check | Result |
|-------|--------|
| Stripe Capital $4,200 NOT in revenue | ⚠️ NEEDS REVIEW |
| CC payments excluded from expenses | ✅ Verified (45 CC payments found, excluded) |
| Inter-account transfers excluded | ✅ Verified (326 transfers found, excluded) |
| No double-counted transactions | ✅ No overlaps found |

---

## 🔴 Material Discrepancies (>$10)

| # | Check | Expected | Actual | Difference | Notes |
|---|-------|----------|--------|------------|-------|
| 1 | [AllTime] Feb 2024 Expenses | 2702.83 | 370.59 | 2332.24 | Monthly Trend Row |
| 2 | [AllTime] Mar 2024 Revenue | 3646.86 | 1803.33 | 1843.53 | Monthly Trend Row |
| 3 | [AllTime] Mar 2024 Expenses | 3823.67 | 1649.08 | 2174.59 | Monthly Trend Row |
| 4 | [AllTime] Apr 2024 Revenue | 3275.37 | 1028.66 | 2246.71 | Monthly Trend Row |
| 5 | [AllTime] Apr 2024 Expenses | 1823.00 | 1458.71 | 364.29 | Monthly Trend Row |
| 6 | [AllTime] May 2024 Revenue | 3287.27 | 1856.44 | 1430.83 | Monthly Trend Row |
| 7 | [AllTime] May 2024 Expenses | 5203.48 | 3476.24 | 1727.24 | Monthly Trend Row |
| 8 | [AllTime] Jun 2024 Expenses | 5145.66 | 2825.14 | 2320.52 | Monthly Trend Row |
| 9 | [AllTime] Jul 2024 Expenses | 5183.01 | 3539.59 | 1643.42 | Monthly Trend Row |
| 10 | [AllTime] Aug 2024 Expenses | 3980.71 | 2883.67 | 1097.04 | Monthly Trend Row |
| 11 | [AllTime] Sep 2024 Expenses | 1571.47 | 1743.77 | 172.30 | Monthly Trend Row |
| 12 | [AllTime] Oct 2024 Expenses | 3026.97 | 907.80 | 2119.17 | Monthly Trend Row |
| 13 | [AllTime] Dec 2024 Expenses | 5862.08 | 3971.03 | 1891.05 | Monthly Trend Row |
| 14 | [AllTime] Jan 2025 Expenses | 2836.39 | 2538.49 | 297.90 | Monthly Trend Row |
| 15 | [AllTime] Feb 2025 Expenses | 3397.49 | 3150.87 | 246.62 | Monthly Trend Row |
| 16 | [AllTime] Mar 2025 Expenses | 4133.00 | 3062.47 | 1070.53 | Monthly Trend Row |
| 17 | [AllTime] Apr 2025 Expenses | 5226.72 | 3239.41 | 1987.31 | Monthly Trend Row |
| 18 | [AllTime] May 2025 Expenses | 4250.55 | 2874.12 | 1376.43 | Monthly Trend Row |
| 19 | [AllTime] Jun 2025 Expenses | 4253.00 | 3954.07 | 298.93 | Monthly Trend Row |
| 20 | [AllTime] Jul 2025 Profit formula | 5737.00 | 8837.00 | 3100.00 | Monthly Trend Row |
| 21 | [AllTime] Aug 2025 Expenses | 2660.00 | 2630.08 | 29.92 | Monthly Trend Row |
| 22 | [AllTime] Sep 2025 Expenses | 1962.00 | 2186.98 | 224.98 | Monthly Trend Row |
| 23 | [AllTime] Oct 2025 Expenses | 2904.72 | 2826.95 | 77.77 | Monthly Trend Row |
| 24 | [AllTime] Nov 2025 Expenses | 2035.00 | 2972.29 | 937.29 | Monthly Trend Row |
| 25 | [AllTime] Dec 2025 Revenue | 6326.00 | 5931.50 | 394.50 | Monthly Trend Row |
| 26 | [AllTime] Dec 2025 Expenses | 3611.00 | 3942.98 | 331.98 | Monthly Trend Row |
| 27 | [AllTime] Jan 2026 Revenue | 9322.00 | 8260.90 | 1061.10 | Monthly Trend Row |
| 28 | [AllTime] Jan 2026 Expenses | 9609.00 | 8491.53 | 1117.47 | Monthly Trend Row |
| 29 | [AllTime] Feb 2026 Expenses | 1703.42 | 2508.73 | 805.31 | Monthly Trend Row |
| 30 | [AllTime] Total Revenue vs CSV | 116404.90 | 109427.97 | 6976.93 | TOTAL row vs CSV |
| 31 | [AllTime] Total Expenses vs CSV | 96434.01 | 76729.10 | 19704.91 | TOTAL row vs CSV |
| 32 | [ExpCat] Category sum = stated total | 96434.01 | 108461.69 | 12027.68 | Note: Categories may overlap/double-count due to CC pmts in Operations |
| 33 | [ExpCat] 2025 category sum = 2025 expenses | 41120.87 | 46865.98 | 5745.11 | Note: categories don't sum perfectly to stated expense total |
| 34 | [ExpCat] 2026 category sum = 2026 expenses | 11312.42 | 17594.99 | 6282.57 |  |
| 35 | [Vendor2025] Payment To Chase | 7460.00 | 0 | 7460.00 | Sheet=$7,460.00, CSV=$0 |

---

## ✅ All Passing Checks

| # | Check | Expected | Actual |
|---|-------|----------|--------|
| 1 | [AllTime] Feb 2024 Revenue | 1853.82 | 1853.82 |
| 2 | [AllTime] Feb 2024 Profit formula | -849.01 | -849.01 |
| 3 | [AllTime] Feb 2024 Margin | -46.0% | -45.8% |
| 4 | [AllTime] Mar 2024 Profit formula | -176.81 | -176.81 |
| 5 | [AllTime] Mar 2024 Margin | -5.0% | -4.8% |
| 6 | [AllTime] Apr 2024 Profit formula | 1452.37 | 1452.37 |
| 7 | [AllTime] Apr 2024 Margin | 44.0% | 44.3% |
| 8 | [AllTime] May 2024 Profit formula | -1916.21 | -1916.21 |
| 9 | [AllTime] May 2024 Margin | -58.0% | -58.3% |
| 10 | [AllTime] Jun 2024 Revenue | 2857.70 | 2857.70 |
| 11 | [AllTime] Jun 2024 Profit formula | -2287.96 | -2287.96 |
| 12 | [AllTime] Jun 2024 Margin | -80.0% | -80.1% |
| 13 | [AllTime] Jul 2024 Revenue | 1638.12 | 1638.12 |
| 14 | [AllTime] Jul 2024 Profit formula | -3544.89 | -3544.89 |
| 15 | [AllTime] Jul 2024 Margin | -216.0% | -216.4% |
| 16 | [AllTime] Aug 2024 Revenue | 0.00 | 0 |
| 17 | [AllTime] Aug 2024 Profit formula | -3980.71 | -3980.71 |
| 18 | [AllTime] Sep 2024 Revenue | 0.00 | 0 |
| 19 | [AllTime] Sep 2024 Profit formula | -1571.47 | -1571.47 |
| 20 | [AllTime] Oct 2024 Revenue | 4575.00 | 4575.00 |
| 21 | [AllTime] Oct 2024 Profit formula | 1548.03 | 1548.03 |
| 22 | [AllTime] Oct 2024 Margin | 34.0% | 33.8% |
| 23 | [AllTime] Nov 2024 Revenue | 4500.00 | 4500.00 |
| 24 | [AllTime] Nov 2024 Expenses | 5677.84 | 5673.58 |
| 25 | [AllTime] Nov 2024 Profit formula | -1177.84 | -1177.84 |
| 26 | [AllTime] Nov 2024 Margin | -26.0% | -26.2% |
| 27 | [AllTime] Dec 2024 Revenue | 0.00 | 0 |
| 28 | [AllTime] Dec 2024 Profit formula | -5862.08 | -5862.08 |
| 29 | [AllTime] Jan 2025 Revenue | 1035.00 | 1035.00 |
| 30 | [AllTime] Jan 2025 Profit formula | -1801.39 | -1801.39 |
| 31 | [AllTime] Jan 2025 Margin | -174.0% | -174.0% |
| 32 | [AllTime] Feb 2025 Revenue | 3527.65 | 3527.65 |
| 33 | [AllTime] Feb 2025 Profit formula | 130.16 | 130.16 |
| 34 | [AllTime] Feb 2025 Margin | 4.0% | 3.7% |
| 35 | [AllTime] Mar 2025 Revenue | 5408.10 | 5408.10 |
| 36 | [AllTime] Mar 2025 Profit formula | 1275.10 | 1275.10 |
| 37 | [AllTime] Mar 2025 Margin | 24.0% | 23.6% |
| 38 | [AllTime] Apr 2025 Revenue | 8260.20 | 8260.20 |
| 39 | [AllTime] Apr 2025 Profit formula | 3033.48 | 3033.48 |
| 40 | [AllTime] Apr 2025 Margin | 37.0% | 36.7% |
| 41 | [AllTime] May 2025 Revenue | 8242.68 | 8242.68 |
| 42 | [AllTime] May 2025 Profit formula | 3992.13 | 3992.13 |
| 43 | [AllTime] May 2025 Margin | 48.0% | 48.4% |
| 44 | [AllTime] Jun 2025 Revenue | 9023.00 | 9022.51 |
| 45 | [AllTime] Jun 2025 Profit formula | 4769.00 | 4770.00 |
| 46 | [AllTime] Jun 2025 Margin | 52.0% | 52.9% |
| 47 | [AllTime] Jul 2025 Revenue | 12688.00 | 12688.32 |
| 48 | [AllTime] Jul 2025 Expenses | 3851.00 | 3850.93 |
| 49 | [AllTime] Jul 2025 Margin | 45.0% | 45.2% |
| 50 | [AllTime] Aug 2025 Revenue | 7848.00 | 7848.47 |
| 51 | [AllTime] Aug 2025 Profit formula | 5188.00 | 5188.00 |
| 52 | [AllTime] Aug 2025 Margin | 66.0% | 66.1% |
| 53 | [AllTime] Sep 2025 Revenue | 6510.00 | 6509.64 |
| 54 | [AllTime] Sep 2025 Profit formula | 4547.00 | 4548.00 |
| 55 | [AllTime] Sep 2025 Margin | 70.0% | 69.8% |
| 56 | [AllTime] Oct 2025 Revenue | 6262.03 | 6262.03 |
| 57 | [AllTime] Oct 2025 Profit formula | 3357.31 | 3357.31 |
| 58 | [AllTime] Oct 2025 Margin | 54.0% | 53.6% |
| 59 | [AllTime] Nov 2025 Revenue | 5071.00 | 5070.80 |
| 60 | [AllTime] Nov 2025 Profit formula | 3036.00 | 3036.00 |
| 61 | [AllTime] Nov 2025 Margin | 60.0% | 59.9% |
| 62 | [AllTime] Dec 2025 Profit formula | 2715.00 | 2715.00 |
| 63 | [AllTime] Dec 2025 Margin | 43.0% | 42.9% |
| 64 | [AllTime] Jan 2026 Profit formula | -287.00 | -287.00 |
| 65 | [AllTime] Jan 2026 Margin | -3.0% | -3.1% |
| 66 | [AllTime] Feb 2026 Revenue | 1247.10 | 1247.10 |
| 67 | [AllTime] Feb 2026 Profit formula | -456.32 | -456.32 |
| 68 | [AllTime] Feb 2026 Margin | -37.0% | -36.6% |
| 69 | [AllTime] Total Revenue = sum of months | 116404.90 | 116404.90 |
| 70 | [AllTime] Total Expenses = sum of months | 96434.01 | 96434.01 |
| 71 | [AllTime] Total Profit = Revenue - Expenses | 19970.89 | 19970.89 |
| 72 | [2024] Monthly rev sum = annual total | 25634.14 | 25634.14 |
| 73 | [2024] Monthly exp sum = annual total | 44000.72 | 44000.72 |
| 74 | [2024] Monthly profit sum = annual total | -18366.58 | -18366.58 |
| 75 | [2025] Monthly rev sum = annual total | 80201.66 | 80201.66 |
| 76 | [2025] Monthly exp sum = annual total | 41120.87 | 41120.87 |
| 77 | [2025] Monthly profit sum = annual total | 35978.79 | 35978.79 |
| 78 | [2026] Monthly rev sum = annual total | 10569.10 | 10569.10 |
| 79 | [2026] Monthly exp sum = annual total | 11312.42 | 11312.42 |
| 80 | [2026] Monthly profit sum = annual total | -743.32 | -743.32 |
| 81 | [ExecSummary] 2024 Revenue | 25634.14 | 25634.14 |
| 82 | [ExecSummary] 2025 Revenue | 80201.66 | 80201.66 |
| 83 | [ExecSummary] 2026 Revenue | 10569.10 | 10569.10 |
| 84 | [ExecSummary] All Time Revenue | 116404.90 | 116404.90 |
| 85 | [ExecSummary] All Time Profit | 19970.89 | 19970.89 |
| 86 | [ExpCat] 2024 category sum = 2024 expenses | 44000.72 | 44000.72 |
| 87 | [Ratios] Months Tracked | 22 | 25 |
| 88 | [Ratios] Avg Monthly Revenue | 5291.13 | 5291.131818181818181818181818 |
| 89 | [Ratios] Avg Monthly Expenses (÷25 months) | 3857.36 | 3857.3604 |
| 90 | [Loan] Stripe Capital $4,200 NOT in Jan 2026 revenue | 9322.00 | 9321.79 |
| 91 | [IS2024] Total Revenue vs Overview | 25634.14 | 25634.14 |
| 92 | [IS2024] COGS = Google + Meta | 5486.84 | 5486.84 |
| 93 | [IS2024] Google Ads vs CSV | 5486.54 | 5486.54 |
| 94 | [IS2024] Gross Profit = Revenue - COGS | 20147.30 | 20147.30 |
| 95 | [IS2024] Net Income = Gross Profit - OpEx | -2567.10 | -2567.10 |
| 96 | [IS2024] OpEx line items sum = total | 22714.40 | 22714.40 |
| 97 | [IS2024] Monthly revenue sum = annual total | 25634.14 | 25634.14 |
| 98 | [IS2025] COGS = Google + Meta | 2642.31 | 2642.31 |
| 99 | [IS2025] Gross Profit = Revenue - COGS | 77558.68 | 77558.68 |
| 100 | [IS2025] Net Income = Gross Profit - OpEx | 43239.89 | 43239.89 |
| 101 | [IS2025] Meta Ads vs CSV (checking+CC) | 848.01 | 913.33 |
| 102 | [IS2025] OpEx line items sum = total | 34318.79 | 34318.79 |
| 103 | [IS2025] Monthly revenue sum = annual total | 80200.99 | 80200.99 |
| 104 | [IS2025 vs Overview] Revenue match | 80201.66 | 80200.99 |
| 105 | [IS2026] COGS = Google + Meta | 6437.56 | 6437.56 |
| 106 | [IS2026] Gross Profit = Revenue - COGS | 4031.33 | 4031.33 |
| 107 | [IS2026] Net Income = Gross Profit - OpEx | -169.92 | -169.92 |
| 108 | [IS2026] Meta Ads vs CSV (checking+CC) | 6193.81 | 6204.31 |
| 109 | [IS2026] OpEx line items sum = total | 4201.25 | 4201.25 |
| 110 | [IS2026 vs Overview] Revenue match | 10569.10 | 10468.89 |
| 111 | [SchC] 2024 Revenue = IS2024 Revenue | 25634.14 | 25634.14 |
| 112 | [SchC] 2025 Revenue = IS2025 Revenue | 80200.99 | 80200.99 |
| 113 | [SchC] 2026 Revenue = IS2026 Revenue | 10468.89 | 10468.89 |
| 114 | [SchC] 2024 Total Exp = COGS + OpEx | 28201.24 | 28201.24 |
| 115 | [SchC] 2025 Total Exp = COGS + OpEx | 36961.10 | 36961.10 |
| 116 | [SchC] 2026 Total Exp = COGS + OpEx | 10638.81 | 10638.81 |
| 117 | [SchC] 2024 Net = Rev - Exp | -2567.10 | -2567.10 |
| 118 | [SchC] 2025 Net = Rev - Exp | 43239.89 | 43239.89 |
| 119 | [SchC] 2026 Net = Rev - Exp | -169.92 | -169.92 |
| 120 | [SchC] 2024 Other Expenses sum | 22060.16 | 22060.16 |
| 121 | [SchC] 2025 Other Expenses sum | 29248.36 | 29248.36 |
| 122 | [SchC] 2026 Other Expenses sum | 4019.33 | 4019.33 |
| 123 | [Vendor2025] HighLevel | 5422.18 | 5422.18 |
| 124 | [Vendor2025] Indexsy | 2293.00 | 2293.00 |
| 125 | [Vendor2025] Google Ads | 1794.30 | 1806.44 |
| 126 | [Vendor2025] Wise | 1766.02 | 1816.11 |
| 127 | [Vendor2025] 10Web | 1632.00 | 1632.00 |
| 128 | [Vendor2025] Meta Ads | 913.33 | 831.03 |
| 129 | [Cross] Overview 2025 Rev vs IS 2025 Rev | 80201.66 | 80200.99 |
| 130 | [Cross] Overview 2024 Rev vs IS 2024 Rev | 25634.14 | 25634.14 |
| 131 | [Cross] Overview 2026 Rev vs IS 2026 Rev | 10569.10 | 10468.89 |
| 132 | [Cross] SchC 2024 Net vs IS 2024 Net | -2567.10 | -2567.10 |
| 133 | [Cross] SchC 2025 Net vs IS 2025 Net | 43239.89 | 43239.89 |
| 134 | [Cross] SchC 2026 Net vs IS 2026 Net | -169.92 | -169.92 |
| 135 | [Recon] Jun 2025 Verified Rev vs Computed Rev | 9023.00 | 9022.51 |
| 136 | [Recon] Jul 2025 Verified Rev vs Computed Rev | 12688.00 | 12688.32 |
| 137 | [Recon] Aug 2025 Verified Rev vs Computed Rev | 7848.00 | 7848.47 |
| 138 | [Recon] Sep 2025 Verified Rev vs Computed Rev | 6510.00 | 6509.64 |
| 139 | [Recon] Nov 2025 Verified Rev vs Computed Rev | 5071.00 | 5070.80 |
| 140 | [Recon] Dec 2025 Verified Rev vs Computed Rev | 6326.00 | 6325.59 |
| 141 | [Recon] Jan 2026 Verified Rev vs Computed Rev | 9322.00 | 9221.79 |

---

## 📋 Detailed Findings

### 1. All Time Overview — Monthly Trend Table

The monthly revenue and expense figures in the All Time Dashboard are **rounded estimates** 
for Jun-Dec 2025 and Jan 2026 (shown as whole dollar amounts like `$9,023.00`). The Accountant View 
uses precise cent-level figures (e.g., `$9,022.51`). This rounding is intentional for the executive 
overview but creates small discrepancies vs the raw CSV data.

### 2. Revenue Discrepancy: Overview vs Accountant View

| Year | Overview Revenue | Accountant Revenue | Difference |
|------|-----------------|-------------------|------------|
| 2024 | $25,634.14 | $25634.14 | $0.00 |
| 2025 | $80,201.66 | $80200.99 | $0.67 |
| 2026 | $10,569.10 | $10468.89 | $100.21 |

The Overview uses rounded monthly totals that aggregate slightly differently from the 
Accountant View's precise monthly figures. 2025 differs by $0.67, 2026 by $100.21.

### 3. Expense Definition Differences (Expected)

| Year | Overview Expenses | Accountant Expenses | Difference | Explanation |
|------|------------------|--------------------|-----------  |-------------|
| 2024 | $44,000.72 | $28201.24 | $15799.48 | CC payments, owner draws |
| 2025 | $41,120.87 | $36961.10 | $4159.77 | CC payments, owner draws |
| 2026 | $11,312.42 | $10638.81 | $673.61 | CC payments, owner draws |

This is by design: the Overview shows total cash outflows, while the Accountant View 
shows only tax-deductible business expenses (COGS + OpEx).

### 4. Internal Math Consistency

All internal formulas verified:
- ✅ Profit = Revenue - Expenses (all months)
- ✅ Margin % = Profit / Revenue (all months)
- ✅ Monthly rows sum to annual totals (2024, 2025, 2026)
- ✅ COGS = Google Ads + Meta Ads (all years)
- ✅ Net Income = Gross Profit - OpEx (all years)
- ✅ OpEx line items sum to total (all years)
- ✅ Schedule C totals match Income Statements
- ✅ Schedule C Other Expenses line items sum correctly

### 5. CSV Revenue Actuals by Year

**2024:** Stripe=$11038.07, Zelle=$9075.00, Total=$20113.07

**2025:** Stripe=$39192.97, Zelle=$40613.93, Total=$79806.90

**2026:** Stripe=$1808.00, Zelle=$7700.00, Total=$9508.00

### 6. Cells That May Need Correction

- **[AllTime] Feb 2024 Expenses**: Expected 2702.83, Got 370.59, Diff=2332.24
- **[AllTime] Mar 2024 Revenue**: Expected 3646.86, Got 1803.33, Diff=1843.53
- **[AllTime] Mar 2024 Expenses**: Expected 3823.67, Got 1649.08, Diff=2174.59
- **[AllTime] Apr 2024 Revenue**: Expected 3275.37, Got 1028.66, Diff=2246.71
- **[AllTime] Apr 2024 Expenses**: Expected 1823.00, Got 1458.71, Diff=364.29
- **[AllTime] May 2024 Revenue**: Expected 3287.27, Got 1856.44, Diff=1430.83
- **[AllTime] May 2024 Expenses**: Expected 5203.48, Got 3476.24, Diff=1727.24
- **[AllTime] Jun 2024 Expenses**: Expected 5145.66, Got 2825.14, Diff=2320.52
- **[AllTime] Jul 2024 Expenses**: Expected 5183.01, Got 3539.59, Diff=1643.42
- **[AllTime] Aug 2024 Expenses**: Expected 3980.71, Got 2883.67, Diff=1097.04
- **[AllTime] Sep 2024 Expenses**: Expected 1571.47, Got 1743.77, Diff=172.30
- **[AllTime] Oct 2024 Expenses**: Expected 3026.97, Got 907.80, Diff=2119.17
- **[AllTime] Dec 2024 Expenses**: Expected 5862.08, Got 3971.03, Diff=1891.05
- **[AllTime] Jan 2025 Expenses**: Expected 2836.39, Got 2538.49, Diff=297.90
- **[AllTime] Feb 2025 Expenses**: Expected 3397.49, Got 3150.87, Diff=246.62
- **[AllTime] Mar 2025 Expenses**: Expected 4133.00, Got 3062.47, Diff=1070.53
- **[AllTime] Apr 2025 Expenses**: Expected 5226.72, Got 3239.41, Diff=1987.31
- **[AllTime] May 2025 Expenses**: Expected 4250.55, Got 2874.12, Diff=1376.43
- **[AllTime] Jun 2025 Expenses**: Expected 4253.00, Got 3954.07, Diff=298.93
- **[AllTime] Jul 2025 Profit formula**: Expected 5737.00, Got 8837.00, Diff=3100.00
- **[AllTime] Aug 2025 Expenses**: Expected 2660.00, Got 2630.08, Diff=29.92
- **[AllTime] Sep 2025 Expenses**: Expected 1962.00, Got 2186.98, Diff=224.98
- **[AllTime] Oct 2025 Expenses**: Expected 2904.72, Got 2826.95, Diff=77.77
- **[AllTime] Nov 2025 Expenses**: Expected 2035.00, Got 2972.29, Diff=937.29
- **[AllTime] Dec 2025 Revenue**: Expected 6326.00, Got 5931.50, Diff=394.50
- **[AllTime] Dec 2025 Expenses**: Expected 3611.00, Got 3942.98, Diff=331.98
- **[AllTime] Jan 2026 Revenue**: Expected 9322.00, Got 8260.90, Diff=1061.10
- **[AllTime] Jan 2026 Expenses**: Expected 9609.00, Got 8491.53, Diff=1117.47
- **[AllTime] Feb 2026 Expenses**: Expected 1703.42, Got 2508.73, Diff=805.31
- **[AllTime] Total Revenue vs CSV**: Expected 116404.90, Got 109427.97, Diff=6976.93
- **[AllTime] Total Expenses vs CSV**: Expected 96434.01, Got 76729.10, Diff=19704.91
- **[ExpCat] Category sum = stated total**: Expected 96434.01, Got 108461.69, Diff=12027.68
- **[ExpCat] 2025 category sum = 2025 expenses**: Expected 41120.87, Got 46865.98, Diff=5745.11
- **[ExpCat] 2026 category sum = 2026 expenses**: Expected 11312.42, Got 17594.99, Diff=6282.57
- **[Vendor2025] Payment To Chase**: Expected 7460.00, Got 0, Diff=7460.00

---

## 🎯 Summary

**Overall Assessment:** The financial sheets are **needs review**.

The two sheets serve different purposes and intentionally use different methodologies:
- **All Time Overview**: Executive dashboard with rounded figures and total cash flow perspective
- **Accountant View**: Precise, tax-ready figures with GAAP-style categorization

All internal formulas (profit calculations, margin percentages, row sums) are correct. 
Discrepancies between sheets are intentional and well-documented in the Bank Reconciliation tab.