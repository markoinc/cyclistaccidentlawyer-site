# MVA Lead Gen - Site Build Plan

## Site Architecture

```
Homepage
│
├── Lead Vendors (CATEGORY 1)
│   ├── All Lead Vendors List
│   ├── Individual Vendor Pages
│   ├── Lead Vendor Comparisons
│   └── "Best MVA Lead Gen" Guide
│
├── Intake Services (CATEGORY 2)
│   ├── All Intake Companies List
│   ├── Individual Company Pages
│   ├── Intake Service Comparisons
│   └── "Best Outsourced Intake" Guide
│
├── Exclusive Partners (PREMIUM TIER) ⭐
│   ├── Why Exclusive Partners?
│   ├── Cases on Demand (Lead Vendor)
│   ├── Inquire2Esquire (Intake Services)
│   └── Book a Call CTA
│
├── Resources/Blog
│   ├── Guides (leads + intake topics)
│   ├── Case Studies
│   └── Industry Analysis
│
├── About/Trust
│   ├── Our Methodology
│   ├── How We Vet Partners
│   └── Contact
│
└── Tools
    ├── ROI Calculator
    ├── Vendor Comparison Tool
    └── Intake Cost Calculator
```

**Cross-Category Opportunities:**
- "Complete Your Pipeline" CTAs (leads → intake)
- Bundle comparisons (lead + intake combos)
- "If you use X for leads, consider Y for intake"

---

## Page Types & Templates

### 1. Homepage
- Hero: "Find the Right MVA Lead Gen Partner"
- Quick stats: "50+ vendors reviewed | 3 exclusive partners"
- Exclusive Partners spotlight (above fold)
- Directory search/filter
- Trust signals (methodology, no pay-to-play claims)

### 2. Directory Listing Page
- Filterable grid of all 50+ vendors
- Sort by: Rating, Price, Case Type, Location
- Quick-view cards with key metrics
- "Exclusive Partner" badges on premium vendors
- Pagination or infinite scroll

### 3. Individual Vendor Page (Directory)
```
[Vendor Name]
├── Overall Rating (1-5 stars)
├── Quick Stats Box
│   ├── Avg Cost Per Lead
│   ├── Reported Conversion Rate
│   ├── Case Types
│   └── Service Areas
├── Our Analysis (editorial)
├── Pros & Cons
├── User Reviews (community)
├── Comparison: "vs Directory Average"
└── CTA: "Compare with Exclusive Partners"
```

### 4. Exclusive Partner Page (Premium)
```
[Partner Name] ⭐ EXCLUSIVE PARTNER
├── Why We Chose Them (trust)
├── Performance Stats vs Directory Avg
│   ├── 2.3x higher conversion
│   ├── 40% lower cost per case
│   └── 98% case acceptance rate
├── Detailed Case Studies
├── Pricing Transparency
├── Video Testimonials
└── CTA: "Book a Discovery Call" → OUR BOOKING SYSTEM
```

### 5. Comparison Page
- Side-by-side: Exclusive Partner vs Directory Average
- Interactive calculator: "What would your ROI be?"
- Testimonials from attorneys who switched

### 6. Blog/Resource Pages
- Standard content template
- Related vendors sidebar
- CTA to exclusive partners

---

## Key UI Components

### Exclusive Partner Callout Box
Appears on:
- Homepage (prominent)
- Directory pages (sidebar)
- Individual vendor pages (bottom)
- Blog posts (inline)

```
┌─────────────────────────────────────┐
│ ⭐ EXCLUSIVE PARTNERS               │
│ Vetted vendors with proven stats    │
│ 2.3x better conversion than average │
│                                     │
│ [See Exclusive Partners →]          │
└─────────────────────────────────────┘
```

### Stat Comparison Widget
```
┌─────────────────────────────────────┐
│         Directory Avg │ Exclusive   │
│ Conversion    12%     │    28%      │
│ Cost/Case    $3,200   │   $1,900    │
│ Accept Rate   71%     │    98%      │
└─────────────────────────────────────┘
```

### Booking Flow (Exclusive Partners)
1. User clicks "Book a Call"
2. Calendly/Cal.com embed (OUR calendar, not partner's)
3. User selects time slot
4. We capture lead info
5. We intro to partner
6. We track conversion → earn referral fee

---

## Tech Stack (Recommended)

- **Framework:** Next.js or Astro (SEO-optimized)
- **CMS:** Notion API or Sanity (easy content updates)
- **Reviews:** Custom or integrate with Trustpilot
- **Booking:** Cal.com (open source, trackable)
- **Analytics:** Plausible + custom conversion tracking
- **Hosting:** Vercel or Cloudflare Pages

---

## Build Phases

### Phase 1: MVP (Week 1-2)
- [ ] Homepage with value prop
- [ ] 10 vendor directory pages
- [ ] 2 exclusive partner pages
- [ ] Basic comparison widget
- [ ] Booking flow for exclusive partners

### Phase 2: Scale Content (Week 3-4)
- [ ] Expand to 30+ vendors
- [ ] Add user review system
- [ ] Build comparison tool
- [ ] Launch 5 blog posts

### Phase 3: Full Directory (Week 5-6)
- [ ] 50+ vendors complete
- [ ] ROI calculator
- [ ] Case studies
- [ ] Email capture + nurture sequence

---

## SEO Strategy Alignment

Every page serves dual purpose:
1. **Rank for keywords** (traffic)
2. **Funnel to exclusive partners** (revenue)

Homepage → "mva lead generation"
Directory → "mva lead gen companies" / "best mva leads"
Vendor Pages → "[Vendor] reviews" / "[Vendor] vs [Competitor]"
Exclusive Pages → "[Partner] review" + conversion-focused
Blog → Long-tail keywords + internal linking
