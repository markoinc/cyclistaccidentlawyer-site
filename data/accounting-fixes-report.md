# Accounting Fixes Report
**Date:** 2025-07-08
**Sheet:** All Time Financial Dashboard (`1v1di5lJT-84iMD7FfnKGFfWanFV-5gyWXWR5mGJuJZQ`)

---

## ✅ FIXED: July 2025 Profit Error ($3,100 correction)

**Root Cause:** July 2025 profit was hardcoded as $5,737 instead of the correct $8,837 ($12,688 revenue - $3,851 expenses). This was a $3,100 arithmetic error — likely a data entry mistake.

### Cells Updated

| Location | Cell(s) | Before | After |
|----------|---------|--------|-------|
| **📅 2025 tab** | D20 (Jul Profit) | $5,737.00 | **$8,837.00** |
| **📅 2025 tab** | E20 (Jul Margin) | 45% | **70%** |
| **📅 2025 tab** | B5 (Annual Net Profit) | $39,080.79 | **$42,180.79** |
| **📅 2025 tab** | B6 (Annual Margin) | 49% | **53%** |
| **📅 2025 tab** | B9 (Avg Monthly Profit) | $3,256.73 | **$3,515.07** |
| **📅 2025 tab** | D26:E26 (Total row) | $39,080.79 / 49% | **$42,180.79 / 53%** |
| **🌐 All Time Dashboard** | D38 (Jul 2025 Profit) | $5,737.00 | **$8,837.00** |
| **🌐 All Time Dashboard** | E38 (Jul 2025 Margin) | 45.0% | **70.0%** |
| **🌐 All Time Dashboard** | C5 (2025 Net Profit) | $39,080.79 | **$42,180.79** |
| **🌐 All Time Dashboard** | C6 (2025 Margin) | 49.0% | **53.0%** |
| **🌐 All Time Dashboard** | E5 (All Time Net Profit) | $19,870.68 | **$22,970.68** |
| **🌐 All Time Dashboard** | E6 (All Time Margin) | 17.0% | **20.0%** |
| **🌐 All Time Dashboard** | D46:E46 (Total row) | $19,870.68 / 17.0% | **$22,970.68 / 20.0%** |

**Total cells updated:** 15 (across 2 tabs)

### Impact Summary
- **2025 profit** increased from $39,081 → **$42,181** (+$3,100)
- **2025 margin** improved from 49% → **53%**
- **All-time profit** increased from $19,871 → **$22,971** (+$3,100)
- **All-time margin** improved from 17% → **20%**

---

## ℹ️ October 2025: No Discrepancy Found

The previous agent flagged "All Time shows $6,262 vs Dashboard $6,440 — $178 discrepancy."

**Current state (both tabs match):**
- Revenue: $6,262.03
- Expenses: $2,904.72
- Profit: $3,357.31
- Margin: 54%

Both the `📅 2025` tab and `🌐 All Time Dashboard` tab show identical October values. The $178 discrepancy was either already resolved by a prior fix, or referred to a comparison with an external source (e.g., Stripe or bank data). **No action taken.**

---

## ℹ️ December 2025: No Internal Discrepancy Found

The previous agent flagged "All Time $6,326 vs Dashboard $5,825 — $500 Shtabsky difference."

**Current state (both tabs match):**
- Revenue: $6,326.00
- Expenses: $3,611.00
- Profit: $2,715.00
- Margin: 43%

Both tabs are consistent at $6,326 revenue. The mention of "Shtabsky" and a $500 difference likely refers to whether a $500 Shtabsky payment should be included in December revenue. Since both sheets agree internally, and there's no external source data to adjudicate, this requires **human judgment** — specifically:

> **Question for Marko:** Should December 2025 revenue include the ~$500 Shtabsky payment ($6,326) or exclude it ($5,825)?

---

## ⚠️ Note: Hardcoded Values

All values in this spreadsheet appear to be hardcoded (no formulas). This means any future corrections to individual month rows will also require manual updates to:
1. The summary section at the top of each tab
2. The TOTAL row at the bottom of each monthly breakdown
3. The All Time Dashboard summary and totals

Consider adding SUM/AVERAGE formulas to the total rows to prevent future drift.
