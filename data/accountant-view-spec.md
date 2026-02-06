# 📊 KuriosBrand — Accountant View (All Time) Specification

**Purpose:** CPA-ready financial statements. No emojis, standard accounting terminology.
**Audience:** Any accountant or CPA reviewing KuriosBrand LLC financials.

---

## SPREADSHEET NAME
`KuriosBrand LLC — Financial Statements (All Time)`

---

## TAB STRUCTURE

| # | Tab Name | Purpose |
|---|----------|---------|
| 1 | Summary | Business overview, entity info, accounting methods |
| 2 | Chart of Accounts | GL account numbering |
| 3 | Income Statement 2025 | P&L by month (Jun–Dec 2025) |
| 4 | Income Statement 2026 | P&L by month (Jan–Dec 2026) |
| 5 | Balance Sheet | Assets, liabilities, equity snapshots |
| 6 | Cash Flow | Operating, investing, financing activities |
| 7 | General Ledger | Every transaction with GL account codes |
| 8 | Schedule C Summary | IRS Schedule C expense categories |
| 9 | Bank Reconciliation | Statement vs. books comparison |
| 10 | 1099 Tracking | Contractor payments >$600 |

---

## TAB 1: SUMMARY

```
Entity: KuriosBrand LLC
EIN: [TBD]
Entity Type: Single-Member LLC (Schedule C)
Owner: Mark Gundrum
Fiscal Year: Calendar (Jan–Dec)
Accounting Method: Cash Basis
Industry: Digital Marketing / Lead Generation
Address: 361 Falls Rd, Grafton, WI

Bank Accounts:
- Chase Business Checking (...4991) — Primary operating
- Chase Ink Business CC (...0678) — Business expenses
- Chase Personal Checking (...0068) — Owner personal
- Chase Sapphire CC (...4252) — Owner personal CC
- Stripe — Payment processor
- Wells Fargo — Tax savings

Accounting Period Covered: February 2024 — Present
Data Source: Chase bank exports (CSV), Stripe API
```

---

## TAB 2: CHART OF ACCOUNTS

```
Acct# | Name | Type | Normal Balance

ASSETS (1000s)
1000 | Cash — Business Checking (4991) | Asset | Debit
1010 | Cash — Personal Checking (0068) | Asset | Debit
1020 | Cash — Savings (7036) | Asset | Debit
1030 | Cash — Tax Account (Wells Fargo) | Asset | Debit
1100 | Accounts Receivable | Asset | Debit
1200 | Stripe Pending | Asset | Debit
1300 | Investments — Robinhood | Asset | Debit
1310 | Investments — Acorns | Asset | Debit
1320 | Investments — Crypto | Asset | Debit
1400 | Business Equity (R&R Assets) | Asset | Debit

LIABILITIES (2000s)
2000 | Credit Card — Ink Business (0678) | Liability | Credit
2010 | Credit Card — Sapphire (4252) | Liability | Credit
2020 | Credit Card — Discover (6820) | Liability | Credit
2100 | Student Loans | Liability | Credit
2200 | Stripe Capital Loan | Liability | Credit

EQUITY (3000s)
3000 | Owner's Equity | Equity | Credit
3100 | Owner's Draws | Equity | Debit
3200 | Retained Earnings | Equity | Credit

REVENUE (4000s)
4000 | Service Revenue — MVA Lead Gen | Revenue | Credit
4010 | Service Revenue — Rank & Rent | Revenue | Credit
4020 | Service Revenue — SEO / Projects | Revenue | Credit
4100 | Stripe Processing (contra) | Revenue | Debit

COST OF GOODS SOLD (5000s)
5000 | Advertising — Meta/Facebook | COGS | Debit
5010 | Advertising — Google Ads | COGS | Debit
5020 | Lead Generation Tools | COGS | Debit

OPERATING EXPENSES (6000s)
6000 | SaaS & Software | Expense | Debit
6010 | SEO Services & Tools | Expense | Debit
6020 | Office & Coworking | Expense | Debit
6030 | Telecommunications | Expense | Debit
6040 | Internet Service | Expense | Debit
6050 | Professional Services | Expense | Debit
6060 | Bank Fees & Interest | Expense | Debit
6070 | Credit Card Interest (Business) | Expense | Debit
6080 | Insurance | Expense | Debit
6090 | Travel (Business) | Expense | Debit
6100 | Meals (Business, 50%) | Expense | Debit
6110 | Loan Repayment — Stripe Capital | Expense | Debit
6120 | Contractor Labor | Expense | Debit
6130 | Domains & Hosting | Expense | Debit
6140 | Education & Training | Expense | Debit
6150 | Miscellaneous | Expense | Debit

PERSONAL (7000s — not on Schedule C)
7000 | Owner's Draws / Transfers | N/A | Debit
7100 | Personal Living Expenses | N/A | Debit
7200 | Personal Investments | N/A | Debit
7300 | Personal Debt Payments | N/A | Debit
```

---

## TAB 3-4: INCOME STATEMENTS (By Year)

Standard P&L format:
```
                                    Jan    Feb    Mar    ...    Dec    TOTAL
REVENUE
  Service Revenue — MVA             $X     $X                          $X
  Service Revenue — R&R             $X     $X                          $X
  Service Revenue — SEO             $X     $X                          $X
  Less: Stripe Fees                ($X)   ($X)                        ($X)
  ─────────────────────────────────────────────────────────────────────────
  TOTAL NET REVENUE                 $X     $X                          $X

COST OF REVENUE
  Advertising — Meta/Facebook      ($X)   ($X)                        ($X)
  Advertising — Google Ads         ($X)   ($X)                        ($X)
  ─────────────────────────────────────────────────────────────────────────
  TOTAL COST OF REVENUE            ($X)   ($X)                        ($X)

GROSS PROFIT                        $X     $X                          $X
  Gross Margin %                    X%     X%                          X%

OPERATING EXPENSES
  SaaS & Software                  ($X)   ($X)                        ($X)
  SEO Services & Tools             ($X)   ($X)                        ($X)
  Office & Coworking               ($X)   ($X)                        ($X)
  Telecommunications               ($X)   ($X)                        ($X)
  Bank Fees & Interest             ($X)   ($X)                        ($X)
  Insurance                        ($X)   ($X)                        ($X)
  Contractor Labor                 ($X)   ($X)                        ($X)
  Other                            ($X)   ($X)                        ($X)
  ─────────────────────────────────────────────────────────────────────────
  TOTAL OPERATING EXPENSES         ($X)   ($X)                        ($X)

NET OPERATING INCOME                $X     $X                          $X
  Operating Margin %                X%     X%                          X%

OTHER INCOME/EXPENSE
  Interest Income                   $X     $X                          $X
  Interest Expense (CC)            ($X)   ($X)                        ($X)
  Loan Interest (Stripe Capital)   ($X)   ($X)                        ($X)
  ─────────────────────────────────────────────────────────────────────────
  NET OTHER                        ($X)   ($X)                        ($X)

NET INCOME                          $X     $X                          $X
  Net Margin %                      X%     X%                          X%
```

---

## TAB 5: BALANCE SHEET

Monthly snapshots:
```
                                    Jun 25  Jul 25  ...  Jan 26  Current
ASSETS
  Current Assets
    Cash — Business Checking        $X      $X             $X      $X
    Cash — Personal Checking        $X      $X             $X      $X
    Cash — Savings                  $X      $X             $X      $X
    Stripe Pending                  $X      $X             $X      $X
  Total Current Assets              $X      $X             $X      $X

  Investments
    Robinhood                       $X      $X             $X      $X
    Acorns                          $X      $X             $X      $X
    Crypto                          $X      $X             $X      $X
  Total Investments                 $X      $X             $X      $X

  Other Assets
    Business Equity (R&R)           $X      $X             $X      $X
  Total Other Assets                $X      $X             $X      $X

TOTAL ASSETS                        $X      $X             $X      $X

LIABILITIES
  Current Liabilities
    CC — Ink Business (0678)        $X      $X             $X      $X
    CC — Sapphire (4252)            $X      $X             $X      $X
    CC — Discover (6820)            $X      $X             $X      $X
    Stripe Capital Loan             $0      $0             $X      $X
  Total Current Liabilities         $X      $X             $X      $X

  Long-Term Liabilities
    Student Loans                   $X      $X             $X      $X
  Total Long-Term Liabilities       $X      $X             $X      $X

TOTAL LIABILITIES                   $X      $X             $X      $X

EQUITY
  Owner's Equity                    $X      $X             $X      $X
  Retained Earnings                 $X      $X             $X      $X
  Owner's Draws (YTD)             ($X)    ($X)           ($X)    ($X)
TOTAL EQUITY                        $X      $X             $X      $X

TOTAL LIAB + EQUITY                 $X      $X             $X      $X
```

---

## TAB 8: SCHEDULE C SUMMARY

Map all business expenses to IRS Schedule C lines:
```
Line | Category | 2025 Total | 2026 YTD | Notes
8    | Advertising | $X | $X | Meta Ads, Google Ads
11   | Contract labor | $X | $X | Freelancers, VAs
15   | Insurance | $X | $X | Triwest health
17   | Legal & professional | $X | $X |
18   | Office expense | $X | $X | Coworking, supplies
25   | Utilities | $X | $X | Internet, phone
27a  | Other expenses | $X | $X | SaaS, domains, etc.
     |   SaaS & Software | $X | $X |
     |   Domains & Hosting | $X | $X |
     |   SEO Tools & Services | $X | $X |
     |   Bank & Processing Fees | $X | $X |
     |   Education | $X | $X |
     TOTAL EXPENSES | $X | $X |
```

---

## FORMATTING

- **No emojis** — professional accounting format
- Font: Arial, 10pt
- Headers: Bold, dark gray background
- Currency: Standard accounting ($X,XXX.XX) with negatives in parentheses
- Subtotals: Single underline
- Totals: Double underline
- Clean grid lines, alternating row shading optional
