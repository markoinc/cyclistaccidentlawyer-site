# Marko's Financial Analysis — Comprehensive Deep Dive

*Generated from 3 Google Sheets accounting files: September, November, December 2025*

---

## 1. Account Mapping

| Account | Last 4 | Type | Owner | Purpose |
|---------|--------|------|-------|---------|
| Chase Checking | 4991 | Business Checking | KuriosBrand LLC | Primary business operating account |
| Chase Checking | 0068 | Personal Checking | Mark Gundrum | Personal expenses, living costs |
| Chase Savings | 7036 | Savings | Mark Gundrum | Linked savings (auto-transfers, OD protection) |
| Chase Ink CC | 0678 | Business Credit Card | KuriosBrand LLC | SaaS/tool subscriptions |
| Chase Sapphire CC | 4252 (Sept) / no last4 (Nov/Dec) | Personal Credit Card | Mark Gundrum | Personal purchases, travel |
| Discover CC | 6820 | Personal Credit Card | Mark Gundrum | Personal (being paid down) |
| Wise | — | International Transfer | KuriosBrand LLC | Converting USD for living expenses abroad |
| Robinhood | 912028016 | Brokerage | Mark Gundrum | Daily recurring stock purchases ($20-25/day) |
| Acorns | 9000142693 | Investment | Mark Gundrum | $5/day recurring + round-ups |
| Wells Fargo | — | Tax Account | Mark Gundrum | Separate tax savings (transfers to biz) |
| Stripe | — | Payment Processor | KuriosBrand LLC | Client billing |

### Account Flow Pattern
```
[Clients] → Stripe/Zelle → Chase Biz 4991
                                    ↓
                            Chase Personal 0068 (frequent small transfers)
                                    ↓
                            Wise (international ATM/spending)
                            Robinhood ($20/day recurring)
                            Acorns ($5/day recurring)
                            Savings 7036 (auto-saves $25-80 various days)
                            CC Payments (Sapphire, Discover, Ink)
                            Rent (Zelle to landlord)
```

---

## 2. Marko's Accounting Style & Conventions

### Sheet Structure
- **One Google Sheet per month** (separate spreadsheets, not tabs of one file)
- **Raw bank data imported as-is** in dedicated tabs per account
- **Chase CSV format**: `Details | Posting Date | Description | Amount | Type | Balance`
- **Credit Card CSV format**: `Card | Transaction Date | Post Date | Description | Category | Type | Amount`
- **Overview tab** = manual categorization & summary (only September had a completed overview)

### Categorization Method
- Marko **manually categorizes** transactions in the Overview tab by:
  1. Copying vendor names from raw bank data
  2. Grouping by expense category
  3. Summing totals manually (some formulas, mostly hardcoded)
  4. Adding **margin notes** in column A for action items

### Margin Note System (Column A)
These are Marko's personal annotations next to expenses:
| Note | Meaning | Examples |
|------|---------|---------|
| `cancelled` / `Cancelled` / `Cancelled!` / `cancelled :)` | Service has been cancelled | Cobrand, Flowith, Spectrum, Tradingview, Unbounce |
| `cancel!!` / `Cancel!` / `cancel` | Needs to be cancelled ASAP | Ideogram.ai, Dental Insurance, Exa, Revid |
| `look into` | Investigate this charge | Apple Bills, Affirm, Paypal |
| `Reduce...` / `reduce` | Need to reduce this cost | High Level, Foreign Exchange Fees, ATM Fees, Robinhood |
| `biz exp - switch` / `biz exp, switch` | Personal expense that should be on business | Airalo, Donations |
| `biz exp?` | Uncertain if business expense | Slate Digital, Dental Insurance |
| `won't be here next month` / `Wont be here next month` | One-time or ending expense | Anytime Mailbox, Elective, Affirm, Discover, various |
| `Find ways to reduce` | Actively look for cheaper alternatives | Go High Level |
| `reduced` / `reduced by 1/2` | Already reduced | Google One, Google Workspace |
| `Personal Expense ***` | Flagged as personal on business account | Markets purchase |

### Formula Usage (September Overview)
- `=S4/T4` — Credit card utilization percentage
- `=C22+J15-C16` — Total Business Expenses (4991 total + CC total - CC payment)
- `=K31+K32` — Pre-tax profit
- `=K34/K31` — Profit margin percentage
- `=W17+W18` — Net Worth (Total Assets + Total Liabilities)

### Evolution Over Months
- **September**: Full overview with business/personal split, debt tracking, asset tracking, net worth
- **November**: No overview completed (Sheet1 empty); categorization done inline next to raw data in each tab
- **December**: No overview completed; inline categorization in business account tab with "won't be here next month" annotations

---

## 3. Monthly Financial Summaries

### September 2025

#### Business Income
| Source | Amount |
|--------|--------|
| Stripe (10 deposits) | $4,134.64 |
| Zelle (ACI Enterprise ×2 + David Monter Tolentino) | $2,375.00 |
| **Total Business Income** | **$6,509.64** |

#### Business Expenses (Account 4991)
| Category | Amount |
|----------|--------|
| Apple Bills | -$139.10 |
| Cashapp (reviews) | -$10.00 |
| Cobrand | -$85.00 |
| Flowith | -$19.90 |
| High Level (Agency Sub + Inc) | -$507.00 |
| Monthly service fee | -$15.00 |
| Affirm | -$179.65 |
| Chase CC Payment | -$76.00 |
| Credit Builder (Credit Strong + Self Lender) | -$138.00 |
| Safetywing (health insurance) | -$66.28 |
| T-Mobile Bill | -$55.36 |
| Tradingview | -$16.95 |
| Ross Zelle payment | -$12.50 |
| Wise (personal spending transfer) | -$300.51 |
| **Total 4991 Expenses** | **-$1,320.74** |

#### Business CC 0678 Expenses
| Category | Amount |
|----------|--------|
| 10web.io | -$136.00 |
| Canva | -$15.00 |
| Google (One + Workspace) | -$53.59 |
| Ideogram.ai | -$8.00 |
| localrank.so | -$174.30 |
| ChatGPT | -$20.00 |
| Interest | -$53.25 |
| Regus (coworking) | -$99.00 |
| Spectrum | -$70.00 |
| Spotify | -$12.59 |
| **Total CC Expenses** | **-$641.73** |
| Payment to Card | +$76.00 |

#### Business Summary (September)
| Metric | Amount |
|--------|--------|
| Total Business Income | $6,509.64 |
| Total Business Expenses (excl. debt payoff) | -$1,886.47 |
| Total Debt Payoff | -$76.00 |
| **Pre-tax Profit** | **$4,623.17** |
| **Profit Margin** | **71%** |

#### Personal Expenses (Account 0068)
| Category | Amount |
|----------|--------|
| Acorns Invest | -$214.02 |
| Airalo (eSIM) | -$34.30 |
| Apple Cash | -$110.00 |
| Restaurants | -$77.76 |
| Chase CC payment (Sapphire) | -$250.00 |
| Colombia Rent (coliving.com) | -$747.90 |
| Student Loan Payment | -$106.34 |
| Discover Card Payment | -$122.00 |
| Exchange Fees | -$1.93 |
| Donations (GoFundMe) | -$345.50 |
| Shopping (Target, iStore) | -$146.04 |
| Hostels (Hostelworld) | -$94.40 |
| ATM Fees | -$13.00 |
| ATM Withdrawals | -$627.01 |
| Robinhood Investing | -$1,128.00 |
| Onward Ticket | -$16.00 |
| Slate Digital | -$160.77 |
| Dental Insurance (Solstice) | -$8.13 |
| Southwest (flight) | -$504.18 |
| Travel Guard | -$28.25 |
| United (flight) | -$370.75 |
| Wise transfer | -$334.75 |
| PayPal | -$28.35 |
| Wisconsin Rent (Zelle to Patrick) | -$550.00 |
| **Total Personal Expenses** | **-$6,019.38** |

#### Personal CC 4252 (Sapphire)
- Interest: -$172.42
- Payment: +$250.00

#### Personal Discover CC
- Interest: -$101.80
- Payment: +$122.00

#### September Transfers
| From → To | Amount |
|-----------|--------|
| Biz 4991 → Personal 0068 | $5,887.00 |
| Biz 4991 → Wise | $300.51 |
| Personal 0068 → Biz 4991 | $300.00 |
| Savings 7036 → Biz 4991 | $400.00 |
| Tax Acct (Wells Fargo) → Biz 4991 | $950.00 |
| Biz 4991 → Personal 0068 | $5,887 (in 14 transfers of $100-$800) |
| Personal 0068 → Savings | $1,035.00 |
| Savings → Personal 0068 | $566.07 |

---

### November 2025

#### Business Income
| Source | Amount |
|--------|--------|
| Stripe (9 deposits) | $3,070.80 |
| Zelle (ACI Enterprise ×2) | $2,000.00 |
| **Total Business Income** | **$5,070.80** |

#### Business Expenses (Account 4991)
| Category | Amount |
|----------|--------|
| Apple | -$46.73 |
| Flowith | -$19.90 |
| Foreign exchange fees | -$1.02 |
| Google Ads | -$399.72 |
| Go High Level | -$507.00 |
| Markets (personal!) | -$34.33 |
| Monthly Service Fee | -$15.00 |
| Namecheap (domains) | -$37.36 |
| Affirm | -$179.65 |
| Biz CC Payment | -$102.00 |
| Credit Builder Products | -$138.00 |
| Safetywing | -$66.28 |
| T-Mobile | -$73.79 |
| Tradingview | -$16.95 |
| Unbounce | -$99.00 |
| Wise transfers (14 transfers) | -$1,039.78 |
| **Total 4991 Expenses** | **~-$2,776.51** |

#### Business CC 0678 (November)
| Category | Amount |
|----------|--------|
| Google One | -$19.99 |
| Interest | -$68.19 |
| ChatGPT | -$20.00 |
| Ideogram AI | -$20.00 |
| 10web.io | -$136.00 |
| Google Workspace | -$33.60 |
| **Total CC** | **-$297.78** |

#### Personal Expenses (Account 0068 — November)
| Category | Amount |
|----------|--------|
| Acorns Invest | -$168.18 |
| Airlines/tickets (Satena, Aerovias) | -$155.48 |
| Airbnb's | -$51.03 |
| Buses (Redbus) | -$11.97 |
| Casa Kayam (hostel & music — Quibdó) | -$683.90 |
| Sapphire CC Payment | -$254.00 |
| Student Loan | -$106.34 |
| Discover Card Payments | -$121.00 |
| Markets (Exito) | -$27.36 |
| Foreign Exchange Fees | -$59.30 |
| Hulu | -$35.60 |
| Restaurant | -$12.13 |
| Robinhood Invest | -$540.00 |
| Dental Insurance | -$8.13 |
| Random Zelles (Duvan Valdes, Vane) | -$69.02 |
| Rent (Zelle to Patrick) | -$550.00 |
| Onward Ticket | -$16.00 |
| ATM Withdrawals (8 withdrawals, Colombia & Peru) | -$1,142.84 |
| ATM Fees | -$40.00 |
| Savings transfers out | -$365.00 |
| To Biz Account | -$200.00 |
| **Total Personal Expenses** | **~-$4,666.28** |

#### Personal Sapphire CC (November)
- Airalo: -$33.00 (note: switch to biz debit)
- Interest: -$168.56
- Airbnb: -$208.61 (note: "don't do again")
- Airbnb return: +$152.33
- Payment: +$254.00

#### November CC Debt Status (noted in sheet)
| Card | APR | Balance |
|------|-----|---------|
| Discover Personal | 19.99% | $6,000 |
| Chase Sapphire | 21.99% | $9,000 |
| Chase Ink (Biz) | 16.99% | $5,000 |

---

### December 2025

#### Business Income
| Source | Amount |
|--------|--------|
| Stripe (6 deposits) | $2,181.50 |
| Zelle (ACI Enterprise ×3 + Alexander Shtabsky + Anthony Reddin) | $3,750.00 |
| From tax acct (real-time payment via Stripe/Robinhood route) | $394.09 |
| **Total Business Income** | **$6,325.59** |

#### Business Expenses (Account 4991 — December)
| Category | Amount | Notes |
|----------|--------|-------|
| 10web | -$136.00 | |
| Anytime Mailbox | -$19.99 | won't be here next month |
| Apify | -$39.00 | cancelled |
| Apple (Capcut, Canva, Expand) | -$71.91 | reduced to $10/mo, cancel Capcut/Canva/Expand |
| Elective | -$816.67 | won't be here next month |
| Exa.ai (3 charges) | -$491.90 | Cancel before EOM |
| Flowith | -$19.90 | |
| Google Ads (3 campaigns) | -$360.25 | won't be here next month |
| Google One | -$19.99 | |
| Google Workspace | -$23.76 | |
| n8n template | -$1.06 | won't be here next month |
| Harbor Compliance | -$159.00 | won't be here next month |
| High Level (Agency + Inc) | -$407.00 | |
| Instantly (5 charges) | -$139.00 | cancels EOM, renew if email working |
| Lemlist | -$50.00 | now $99/mo |
| Lovable (2 charges) | -$50.00 | downgrade to $5/mo |
| Monthly service fee | -$15.00 | |
| MyFICO (2 charges) | -$59.90 | won't be here next month |
| Namecheap (2 domains) | -$37.36 | |
| Affirm | -$179.65 | won't be here next month |
| OpenAI API credits | -$50.00 | |
| ChatGPT Subscription | -$20.00 | |
| Chase Ink CC Payment | -$178.00 | |
| Credit Strong (2 charges) | -$189.00 | |
| Self Lender | -$48.00 | |
| Wise (living expenses, 2 transfers) | -$100.18 | |
| Revid | -$39.00 | cancel |
| Safetywing (2 charges) | -$132.56 | will be half next month |
| T-Mobile phone bill | -$55.66 | |
| Traveling Mailbox | -$19.95 | |
| Change Biz Address With Gov | -$40.00 | won't be here next month |
| Perplexity AI | -$10.00 | won't be here next month |
| **Total 4991 Expenses** | **~-$3,778.69** |

#### Chase Biz Ink CC 0678 (December)
| Category | Amount |
|----------|--------|
| Interest | -$70.82 |
| Spotify | -$12.59 |
| Google Workspace | -$33.60 |
| Payments received | +$178.00 |

#### Personal Account 0068 (December)
| Category | Amount | Notes |
|----------|--------|-------|
| Acorns | -$164.82 | |
| Chase Sapphire CC Payment | -$257.00 | |
| Student Loan Payment | -$106.34 | |
| Discover CC Payment | -$122.00 | won't be here next month |
| Foreign Exchange Fees | -$64.85 | reduce |
| Hulu | -$35.60 | |
| Paypal - Iian Gabriel | -$52.50 | look into |
| ATM Fees | -$55.00 | reduce (less transactions) |
| ATM Withdrawals (Living) | -$1,861.54 | reduce (market food - could reduce by ~200) |
| Weed | -$300.00 | reduce (send money to savings) |
| Robinhood Investments | -$680.00 | reduce |
| Dental Insurance | -$8.13 | cancel |
| Savings transfers | -$400.00 | |
| Transfer to Business | -$1,300.00 | |
| **Total Personal Expenses** | **~-$5,407.78** |

**Personal Income/Transfers In:**
- Acorns liquidation: +$1,200.00
- OD from savings: +$80.00
- Kurios Income (from biz 4991): +$3,370.00
- From Savings: +$400.00
- From Robinhood: +$454.80

#### Chase Sapphire CC (December)
- Interest: -$159.81
- Payment: +$257.00
- Google Ads return: +$2.38

#### December Goal (noted)
> "Goal: save $500/mo to settle with the collectors"

---

## 4. Recurring Subscriptions & Services

### Business Subscriptions (via 4991 and 0678)

| Service | Monthly Cost | Category | Status (as of Dec) | Notes |
|---------|-------------|----------|---------------------|-------|
| GoHighLevel (Agency Sub) | $297.00 | CRM/Marketing | Active | "Find ways to reduce" |
| GoHighLevel (Inc - extra seats) | $100-110 | CRM/Marketing | Active | Usually $100 + $10 |
| 10web.io | $136.00 | Website hosting | Active | On CC 0678 |
| Affirm loan | $179.65 | Debt payment | Ending | "Only 1 more" (Nov), "won't be here" (Dec) |
| SafetyWing | $66.28 | Health insurance | Active | 2× in Dec ($132.56), "will be half next month" |
| T-Mobile | $55-74 | Phone | Active | Was $55.36 (Sept), $73.79 (Nov), $55.66 (Dec) |
| Credit Strong | $90.00 | Credit building | Active | Increased to $99 in Dec (additional charge) |
| Self Lender | $48.00 | Credit building | Active | |
| Google Workspace | $23.76 | Email/business | Active | Was $33.60 on CC, "reduced by 1/2" |
| Google One | $19.99 | Cloud storage | Active | "Reduced" |
| ChatGPT (OpenAI) | $20.00 | AI tools | Active | On CC 0678 |
| Namecheap (domains) | ~$37.36 | Domains | Active | ~2 domains at $18.68/ea |
| Spotify | $12.59 | Music | Active | On CC 0678 |
| TradingView | $16.95 | Trading | Cancelled | "Cancelled :)" (Nov) |
| Flowith.io | $19.90 | AI tool | Cancelled | |
| Cobrand | $85.00 | Marketing | Cancelled | (Sept only) |
| Canva | $15.00 | Design | Cancelled | (Sept only, on CC) |
| localrank.so | $174.30 | SEO tool | Cancelled | (Sept only) |
| Ideogram AI | $8-20 | AI image gen | Cancelled | $8 Sept, $20 Nov |
| Regus | $99.00 | Coworking | Cancelled | (Sept only) |
| Spectrum | $70.00 | Internet | Cancelled | (Sept only) |
| Unbounce | $99.00 | Landing pages | Cancelled | "Cancelled :)" (Nov) |
| MyFICO | $29.95 | Credit score | One-time | Dec only, "won't be here" |
| Instantly | ~$139.00 | Email outreach | Conditional | "Cancels EOM - renew if email working" |
| Lemlist | $50.00 | Email outreach | Active | "Now $99/mo" |
| Lovable | $50.00 | AI dev tool | Active | "Downgrade to $5/mo" |
| Exa.ai | ~$491.90 | AI search API | Ending | "Cancel before EOM" |
| Apify | $39.00 | Web scraping | Cancelled | |
| Harbor Compliance | $159.00 | Legal/compliance | One-time | |
| Elective | $816.67 | Unknown | One-time | "Won't be here next month" |
| Anytime Mailbox | $19.99 | Virtual mailbox | One-time | |
| Traveling Mailbox | $19.95 | Virtual mailbox | Active | |
| Revid | $39.00 | Video tool | Cancelled | |
| Perplexity AI | $10.00 | AI search | Ending | "Won't be here next month" |
| OpenAI API | $50.00 | AI API | Active | Dec only (separate from ChatGPT sub) |

### Personal Subscriptions

| Service | Monthly Cost | Category | Status |
|---------|-------------|----------|--------|
| Hulu | $35.60 | Entertainment | Active |
| Dental Insurance (Solstice) | $8.13 | Insurance | "Cancel" |
| Acorns subscription | $3.00 | Investment fee | Active |
| Robinhood recurring buys | ~$500-1,128/mo | Investment | Active, "reduce" |
| Acorns recurring deposits | ~$165-215/mo | Investment | Active |
| Student Loan (Dept Education) | $106.34 | Debt | Active |
| Rent (Zelle to Patrick) | $550.00 | Housing | Active (Wisconsin) |
| Discover CC payment | $121-122 | Debt | Active |
| Chase Sapphire CC payment | $250-257 | Debt | Active |

---

## 5. Business vs Personal Expense Breakdown

### Business Expense Categories

| Category | Sept | Nov | Dec | Trend |
|----------|------|-----|-----|-------|
| **SaaS/Tools** | | | | |
| GoHighLevel | $507 | $507 | $407 | ↓ Reducing |
| 10web.io | $136 | $136 | $136 | → Stable |
| Google (Workspace + One + Ads) | $54 | $454 | $404 | ↑ Ads added |
| ChatGPT/OpenAI | $20 | $20 | $70 | ↑ Added API |
| SEO tools (localrank, Instantly, etc.) | $174 | $0 | $139 | Variable |
| Various AI (Exa, Lovable, Perplexity) | $0 | $0 | $552 | ↑ AI spending spike |
| **Operations** | | | | |
| Apple subscriptions | $139 | $47 | $72 | ↓ Reducing |
| SafetyWing (health) | $66 | $66 | $133 | ↑ Double charge |
| T-Mobile | $55 | $74 | $56 | → Stable |
| Domains (Namecheap) | $0 | $37 | $37 | → Stable |
| Monthly service fee | $15 | $15 | $15 | → Stable |
| **Debt/Credit** | | | | |
| Affirm | $180 | $180 | $180 | → Ending soon |
| Credit builders | $138 | $138 | $237 | ↑ Extra payment |
| CC payments | $76 | $102 | $178 | ↑ Paying more |
| **CC Interest** | $53 | $68 | $71 | ↑ Growing |

### Personal Expense Categories

| Category | Sept | Nov | Dec | Trend |
|----------|------|-----|-----|-------|
| **Housing** | | | | |
| Rent (WI or abroad) | $1,298 | $1,234 | $0* | Traveling |
| ATM Withdrawals (living abroad) | $627 | $1,143 | $1,862 | ↑ Major increase |
| **Transportation** | | | | |
| Flights | $903 | $155 | $0 | Variable |
| Hostels/Airbnb | $94 | $735 | $0 | Variable |
| **Investments** | | | | |
| Robinhood | $1,128 | $540 | $680 | ↓ Reducing |
| Acorns | $214 | $168 | $165 | → Stable |
| **Debt** | | | | |
| Student Loan | $106 | $106 | $106 | → Fixed |
| Discover CC | $122 | $121 | $122 | → Fixed |
| Sapphire CC | $250 | $254 | $257 | → Slight increase |
| CC Interest (personal) | $274 | $169 | $160 | ↓ Improving |
| **Living** | | | | |
| Hulu | $0 | $36 | $36 | → Stable |
| Exchange fees | $2 | $59 | $65 | ↑ More intl ATM use |
| Dental | $8 | $8 | $8 | → Cancel pending |

*Dec rent: likely paid via ATM/Wise since he was in Peru

---

## 6. Income Analysis

### Client Income by Source

| Source | Sept | Nov | Dec |
|--------|------|-----|-----|
| **Stripe** | $4,134.64 | $3,070.80 | $2,181.50 |
| **Zelle (ACI Enterprise)** | $2,000.00 | $2,000.00 | $3,000.00 |
| **Zelle (Other clients)** | $375.00 | $0.00 | $750.00 |
| **Total** | **$6,509.64** | **$5,070.80** | **$5,931.50** |

### Stripe Deposit Pattern
- Deposits come 2-4 times per week
- Individual amounts range from $96-$662 per deposit
- Likely tied to client billing cycles (monthly retainers processed via Stripe)

### Known Clients (Zelle)
- **ACI Enterprise, LLC** — Regular $1,000 Zelle payments (2-3×/month), appears to be primary client
- **David Monter Tolentino** — $375 (Sept only)
- **Alexander Shtabsky** — $500 (Dec)
- **Anthony Reddin** — $250 (Dec)

---

## 7. Debt Situation

### September 2025 Snapshot
| Debt | Balance | Limit | Utilization | Goal |
|------|---------|-------|-------------|------|
| Discover Personal CC | $5,926.48 | $6,250 | 95% | $937.50 |
| Chase Sapphire CC | $9,007.86 | $9,300 | 97% | $1,395 |
| Chase Ink (Biz) CC | $4,400.93 | $5,500 | 80% | $825 |
| **Total CC Debt** | **$19,335.27** | | | |
| Student Loans | $8,978.06 | | | |
| **Total Debt** | **$28,313.33** | | | |

### November 2025 Update (from inline notes)
| Card | APR | Balance |
|------|-----|---------|
| Discover | 19.99% | $6,000 |
| Sapphire | 21.99% | $9,000 |
| Ink | 16.99% | $5,000 |

### Monthly Interest Cost (estimated from actual charges)
| Card | Sept Interest | Nov Interest | Dec Interest |
|------|--------------|--------------|--------------|
| Biz Ink 0678 | $53.25 | $68.19 | $70.82 |
| Sapphire 4252 | $172.42 | $168.56 | $159.81 |
| Discover | $101.80 | N/A | N/A |
| **Total Monthly Interest** | **~$327** | **~$237+** | **~$231+** |

### Debt Strategy Notes
- September: "Aggressively aim to pay $4k/mo toward CC debt"
- December: "Goal: save $500/mo to settle with the collectors"
- Strategy shifted from aggressive payoff to settlement approach

---

## 8. Asset & Net Worth Tracking

### September 2025 (only month with full tracking)
| Category | Amount |
|----------|--------|
| Rank and rent assets | $150,000 |
| Cash | $1,807.43 |
| Stocks & options | $1,852.00 |
| Bitcoin | $2,000.00 |
| Solana | $500.00 |
| Dogecoin | $260.00 |
| XRP | $95.00 |
| CreditBuilder Accounts | $700.00 |
| **Liquid Assets** | **$7,214.43** |
| **Business Equity** | **$150,000.00** |
| **Total Assets** | **$157,214.43** |
| **Total Liabilities** | **-$28,313.33** |
| **Net Worth** | **$128,901.10** |

---

## 9. Lifestyle & Location Context

Based on transaction data, Marko is a **digital nomad**:

| Month | Primary Location | Evidence |
|-------|-----------------|----------|
| Sept (early) | Milwaukee, WI | Auntie Anne's WI, MKE Pizzeria, Southwest flight out |
| Sept (mid) | San Francisco, CA | SFO iStore, Kitava SF, SQ Merchandising |
| Sept (late) | Medellín, Colombia | Coliving.com, Masaya Medellín, ATM withdrawals in CO Peso |
| November | Colombia → Peru | Quibdó (Casa Kayam), Bogotá, Medellín, then Lima (Nuevo Sol ATMs) |
| December | Peru (Lima/Cusco) | Pisac/Cusco ATMs, Calle Bolívar Lima ATMs, all Nuevo Sol |

### Living Cost Patterns Abroad
- **ATM withdrawals** are primary spending method (converts USD → local currency)
- September: $627 (Colombia)
- November: $1,143 (Colombia + Peru)
- December: $1,862 (Peru — larger withdrawals)
- **Each ATM hit has $5 fee** — Marko notes "reduce (less transactions)"
- Uses **Wise** for some international transfers from business account
- **Rent**: $550/mo Wisconsin (Zelle to Patrick Landlord) + $747.90 Colombia coliving (Sept)

---

## 10. Key Patterns & Insights

### Spending Trends
1. **SaaS Bloat → Active Pruning**: Marko is actively cancelling subscriptions each month. Sept had Cobrand, Flowith, Spectrum, localrank. Nov cancelled Unbounce, Tradingview. Dec marked many "won't be here next month"
2. **AI Tool Experimentation**: Cycling through AI tools — Ideogram, Flowith, Exa, Lovable, Perplexity, Revid. High December spend ($550+) on AI tools alone
3. **GoHighLevel is largest recurring biz expense**: $407-507/mo, noted "find ways to reduce"
4. **Robinhood daily purchases**: $20-25/day every single day — adds up to $500-1,100/mo. Very consistent, automated recurring buys
5. **Acorns similarly**: $5/day + round-ups = ~$165-215/mo
6. **Investment vs Debt**: Investing ~$700-1,300/mo while carrying ~$20k in high-interest CC debt (17-22% APR). The math doesn't work — CC interest (~$327/mo) far exceeds likely investment returns
7. **Business income declining slightly**: $6,510 → $5,071 → $5,932 (Stripe declining, Zelle increasing)
8. **Living costs rising abroad**: ATM withdrawals went from $627 → $1,143 → $1,862. December also has $300 "weed" expense noted
9. **Transfer complexity**: Money moves biz→personal→savings→biz in complex patterns. Dozens of small transfers ($100-350) rather than monthly lump sums
10. **CC debt barely moving**: Minimum payments + interest means balances stay roughly the same ($19k-20k range)

### Biggest Costs (All-In Monthly)
1. **GoHighLevel**: ~$507/mo
2. **ATM Living Expenses**: $627-1,862/mo (trending up)
3. **Robinhood Investing**: $540-1,128/mo
4. **Rent**: $550/mo (WI landlord)
5. **CC Interest**: ~$230-330/mo
6. **Student Loan**: $106/mo
7. **Affirm**: $180/mo (ending)
8. **Credit Builders**: $138-237/mo
9. **10web.io**: $136/mo
10. **Safetywing**: $66-133/mo

---

## 11. Recommendations for Financial Agent Architecture

### Core Functions Needed

#### 1. **Transaction Ingestion & Categorization**
- Auto-import from Chase CSV downloads (or ideally Plaid API)
- Pattern-match vendors to categories using the taxonomy Marko already uses
- Handle the 6 different account formats (checking vs CC have different columns)
- Separate transfers from real expenses automatically

#### 2. **Category Taxonomy** (based on Marko's existing system)
```
Business Income:
  - stripe_income
  - zelle_income (client payments)
  - other_income

Business Expenses:
  - saas_tools (HighLevel, 10web, Google, OpenAI, etc.)
  - marketing (Google Ads, Instantly, Lemlist)
  - operations (T-Mobile, domains, mailbox, compliance)
  - insurance (SafetyWing)
  - debt_payments (Affirm, CC payments, credit builders)
  - cc_interest
  - bank_fees
  - wise_transfers (for personal spending abroad)

Personal Expenses:
  - housing (rent, coliving)
  - living_abroad (ATM withdrawals, exchange fees)
  - food (restaurants, markets)
  - transportation (flights, buses, hostels, Airbnb)
  - subscriptions (Hulu, Spotify, dental)
  - investments (Robinhood, Acorns)
  - debt_payments (student loan, CC payments)
  - cc_interest
  - misc (weed, donations, PayPal)

Transfers (not expenses):
  - biz_to_personal
  - personal_to_biz
  - to_savings
  - from_savings
  - to_wise
```

#### 3. **Subscription Tracker**
- Detect recurring charges automatically
- Flag new subscriptions
- Track cancelled subscriptions to verify they stopped
- Alert if a "cancelled" service still charges
- Show total monthly subscription burn

#### 4. **Overview Generator**
- Auto-generate the monthly overview Marko builds manually
- Business income/expense/profit summary
- Personal expense breakdown
- Transfer reconciliation (make sure transfers balance)
- CC interest tracking
- Net worth update

#### 5. **Budget Alerts**
- ATM spending thresholds (Marko wants to reduce)
- Investment spending caps (Robinhood/Acorns vs CC debt tradeoff)
- Subscription creep detection
- "Won't be here next month" verification

#### 6. **Debt Dashboard**
- Track all CC balances over time
- Calculate monthly interest cost
- Show payoff projections at current payment rates
- Compare investment deposits vs CC interest (highlight the gap)
- Settlement strategy tracking

### Data Model
```
accounts:
  - id, name, last4, type (checking/cc/savings/brokerage), owner (business/personal)

transactions:
  - id, account_id, date, description, amount, type, balance
  - category (auto or manual), is_transfer, transfer_pair_id
  - vendor (normalized), is_recurring, subscription_id
  - notes (Marko's annotations)

subscriptions:
  - id, vendor, amount, frequency, account_id, status (active/cancelled/pending)
  - first_seen, last_seen, cancel_date

monthly_summaries:
  - month, biz_income, biz_expenses, biz_profit, profit_margin
  - personal_income, personal_expenses
  - total_cc_interest, total_cc_balance
  - net_worth_snapshot
```

### Implementation Priority
1. **Transaction import + auto-categorization** (highest value — saves hours of manual work)
2. **Monthly overview generation** (replaces the manual overview tab)
3. **Subscription tracking + alerts** (catches leaks)
4. **Debt dashboard** (strategic value)
5. **Transfer reconciliation** (complex but important for accuracy)

### API Integration Options
- **Plaid** for automatic bank feeds (eliminates CSV downloads)
- **Stripe API** for income detail (already have access via Stripe account)
- **Google Sheets API** to read existing spreadsheets and write summaries
- **Google Calendar** integration for financial review reminders

---

## 12. Raw Transaction Counts

| Sheet | Tab | Rows |
|-------|-----|------|
| Sept | Overview | 88 rows |
| Sept | Chase4991 (biz checking) | 59 transactions |
| Sept | Chase0068 (personal checking) | 147 transactions |
| Sept | Chase0678 (biz CC) | 13 transactions |
| Sept | Chase4252 (personal CC) | 2 transactions |
| Nov | Sheet1 (overview) | Empty |
| Nov | Biz Acct 4991 | 65 transactions |
| Nov | Biz CC 0678 | 7 transactions |
| Nov | Personal 0068 | 137 transactions |
| Nov | Personal Sapphire CC | 5 transactions |
| Dec | Overview | Empty |
| Dec | Chase Personal 0068 | 139 transactions |
| Dec | Chase Business 4991 | 83 transactions |
| Dec | Chase Sapphire CC | 3 transactions |
| Dec | Chase Biz Ink CC | 5 transactions |
| Dec | Discover Personal Car | Empty |
| Dec | Sheet7 | Empty |

---

*Analysis complete. Every cell from all 3 spreadsheets has been read and categorized.*
