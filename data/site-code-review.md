# Kurios Sites Deep Code Review

**Date:** 2025-02-01  
**Reviewed By:** Sierra (AI Assistant)  
**Sites Reviewed:** kuriosbrand.com (original) & kuriosnew (remix)

---

## Executive Summary

You have **two similar but distinct Kurios landing sites**:

| Aspect | kuriosbrand (Site 1) | kuriosnew (Site 2) |
|--------|---------------------|-------------------|
| **Purpose** | Full lead qualification funnel with quiz | Simplified, conversion-focused LP |
| **Positioning** | "Click to Closed Case" - end-to-end | "Exclusive Leads & Live Transfers" |
| **Qualify Flow** | 3-step qualification quiz with disqualification logic | Simple checkbox + calendar |
| **Key Difference** | Has Login page, more sections | Geolocation-based personalization, dual offers |
| **Supabase Project** | vjqifdugfuskjakykbjx | zmjnqdaskwumskiycvjn |

**Recommendation:** kuriosnew is cleaner and more conversion-optimized. kuriosbrand has more legacy code and a broken Login page. Consider consolidating to one.

---

## Site 1: kuriosbrand.com (Original)

### Overview
- **Stack:** React 18 + Vite + TypeScript + Tailwind CSS + ShadCN UI
- **Supabase Project ID:** `vjqifdugfuskjakykbjx`
- **Build Status:** ✅ Successful (6.4s)
- **Design:** Dark/charcoal theme with blue accents, monospace fonts, tech/terminal aesthetic

### Pages & Routes

| Route | Page | Description |
|-------|------|-------------|
| `/` | Index | Main landing page with 13 sections |
| `/qualify` | Qualify | 3-step qualification quiz with email capture |
| `/onboarding` | Onboarding | 10-step client intake form |
| `/test-batch-calendar` | TestBatchCalendar | HighLevel calendar embed (booking widget) |
| `/login` | Login | ⚠️ **BROKEN** - No actual auth logic |
| `/privacy` | PrivacyPolicy | Privacy policy page |
| `/terms` | TermsOfService | Terms of service page |
| `/tcpa` | TCPACompliance | TCPA compliance info |
| `/aba-disclaimer` | ABADisclaimer | Attorney advertising disclaimer |

### Homepage Sections (Index)
1. Header (sticky, navigation)
2. HeroSection (animated terminal, "Click to Closed Case")
3. TrustBar (trust badges)
4. PartnershipModel
5. LiveTransfersSection
6. ServiceTiers
7. TrustStats
8. ComparisonTable
9. ValueProposition
10. HowItWorks
11. ComplianceSection
12. FounderSection (Mark Gundrum)
13. InHouseIntakeSection
14. FAQSection
15. TestBatchProtocol
16. Footer

### Key Features

#### Qualification Quiz (/qualify)
- **Stage 1:** Hero with email, position, firm URL capture + certification checkbox
- **Stage 2:** 3-question survey:
  1. Monthly MVA case volume (5 options)
  2. Intake team setup (6 options with disqualification logic)
  3. Cost per signed case (5 options)
- **Disqualification Triggers:**
  - Intake: "Attorneys handle intake" or "Building team" → Disqualified
  - Budget: "Under $1,500" per case → Disqualified
- **Webhook Integration:** Sends to Supabase edge function (`webhook-proxy`) → LeadConnector/HighLevel
- **UTM Tracking:** Captures utm_source, utm_medium, utm_campaign, utm_term, utm_content

#### Onboarding Form (/onboarding)
- 10-step comprehensive intake form
- Collects: Firm info, contacts, case types, geography, timing rules, quality filters, lead delivery preferences, intake availability, reporting preferences
- **Direct Webhook:** `https://services.leadconnectorhq.com/hooks/OsNgWuy8oZzLbp5BXbnD/webhook-trigger/caf6afbb-04d1-4dda-9b12-8ef27b95f6d8`
- Final step embeds HighLevel booking calendar

#### Supabase Edge Functions
1. **webhook-proxy:** Forwards payloads to LeadConnector (requires `LEADCONNECTOR_WEBHOOK_URL` env var)
2. **verify-website:** Verifies if a URL is reachable (HEAD request with 5s timeout)

### Issues Found (Site 1)

#### 🔴 CRITICAL
1. **Login Page is Non-Functional** (`/login`)
   - Form has no actual authentication logic
   - `handleSubmit` does nothing (`// Login functionality would be implemented here`)
   - Links to `/#sample-feed` which doesn't exist
   - **Recommendation:** Remove or implement properly

2. **Supabase Edge Function Requires Secret**
   - `webhook-proxy` requires `LEADCONNECTOR_WEBHOOK_URL` env var
   - If not set in Supabase, qualification submissions will fail silently
   - **Action:** Verify env var is set in Supabase dashboard

#### 🟡 MEDIUM
3. **No Database Tables**
   - Supabase types show `Tables: { [_ in never]: never }` - no tables defined
   - All data goes to webhooks, nothing persisted locally
   - Consider adding leads table for backup/analytics

4. **Dead Code / Unused Component**
   - `NavLink.tsx` exists but isn't used in Header

5. **Large Mark Gundrum Image**
   - `mark-gundrum.png` is 1.7MB - huge for web
   - Should be optimized (WebP, compressed, ~200KB target)

6. **TestBatchCalendar Uses Different Booking Link**
   - Uses `x2ycChO5k7nMsFBd8ngj` booking ID
   - Onboarding uses `7O0pR7pTszdSEmQVBWMK`
   - Verify both calendars are correct

#### 🟢 LOW
7. **Duplicate Toast Implementations**
   - Both `@/hooks/use-toast.ts` and `@/components/ui/use-toast.ts` exist
   - Standard ShadCN duplication, but could consolidate

8. **CSS @import Order Warnings** (build)
   - Font imports could be moved to top of CSS file

---

## Site 2: kuriosnew (Remix - Lead Platform)

### Overview
- **Stack:** React 18 + Vite + TypeScript + Tailwind CSS + ShadCN UI
- **Supabase Project ID:** `zmjnqdaskwumskiycvjn`
- **Build Status:** ✅ Successful (5.5s)
- **Design:** Lighter theme, rounded corners, cleaner modern SaaS aesthetic

### Pages & Routes

| Route | Page | Description |
|-------|------|-------------|
| `/` | Index | Main landing page with 8 sections |
| `/qualify` | Qualify | Simple certification checkbox → calendar |
| `/onboarding` | Onboarding | Same 10-step form as Site 1 |
| `/test-batch-calendar` | TestBatchCalendar | Different HighLevel booking ID |
| `/privacy` | PrivacyPolicy | Privacy policy |
| `/terms` | TermsOfService | Terms of service |
| `/tcpa` | TCPACompliance | TCPA compliance |
| `/aba-disclaimer` | ABADisclaimer | Attorney disclaimer |

**Notable:** No `/login` route (removed)

### Homepage Sections (Index)
1. Header (with phone number, state-based scarcity badge)
2. HeroSection (geolocation-based pricing)
3. TrustBar
4. TwoOfferCards (Leads vs Live Transfers split)
5. DualHowItWorks (side-by-side process comparison)
6. TrustCredibility
7. TestimonialsSlider (client results carousel)
8. FAQSection
9. FinalCTA
10. Footer
11. MobileStickyApply (sticky CTA on mobile)

### Key Features

#### Geolocation-Based Personalization
- **Hook:** `useGeoLocation.ts` - uses ipapi.co free API
- **Header:** Shows "2 spots left in [State]" scarcity badge
- **HeroSection:** Shows state-specific cost per case pricing
- **TestimonialsSlider:** Prioritizes user's state in carousel

**State Pricing Map:**
```javascript
Arizona/Utah: $1,716
North Carolina: $2,145
Florida/Virginia/Ohio/South Carolina: $2,288
New York/Pennsylvania: $2,503
Oregon/Idaho: $2,574
Texas: $2,646
Georgia/Louisiana/New Mexico: $2,860
Washington: $3,575
California: $4,290
Default: $2,500
```

#### Simplified Qualify Flow (/qualify)
- Single certification checkbox
- No quiz, no disqualification
- Direct to booking calendar
- **Much faster conversion path**

#### Dual Offer Cards
- **Exclusive Leads:** "You call. You control." - 10-20% sign rate
- **Live Transfers:** "We call. You sign." - 40-60% sign rate, Premium badge
- Links to `/qualify?offer=leads` or `/qualify?offer=transfers`
- ⚠️ Query params NOT currently used in Qualify page

#### Client Results Slider
- 10 pre-defined state results with metrics
- Auto-rotates every 4-5 seconds
- User's state shown first (if detected)
- Shows cost per case, conversion rate, cases/month

### Issues Found (Site 2)

#### 🔴 CRITICAL
1. **Offer Query Params Ignored**
   - TwoOfferCards links to `/qualify?offer=leads` and `/qualify?offer=transfers`
   - Qualify page doesn't read these params
   - Lead/Transfer preference is lost
   - **Fix:** Read query param and pass to calendar or webhook

2. **Hard-Coded Scarcity Message**
   - "2 spots left in [State]" is always "2" regardless of actual availability
   - Could be seen as deceptive marketing
   - **Recommendation:** Make dynamic or remove

#### 🟡 MEDIUM
3. **Geolocation API Rate Limits**
   - Uses free ipapi.co API
   - Rate limited to 30k/month (about 1k/day)
   - No fallback if API fails (shows default pricing)
   - **Consider:** Caching, paid API, or server-side detection

4. **No Supabase Edge Functions**
   - Site 2 has supabase folder but no edge functions deployed
   - Onboarding still uses direct webhook (same as Site 1)
   - Less resilient than proxied approach

5. **Missing Components Not Used**
   - Several components exist but aren't imported in Index:
     - AIFirstSection.tsx
     - ExclusiveLeadsSection.tsx
     - GuaranteeSection.tsx
     - WeHandleDirtyWork.tsx
     - ComparisonTable.tsx
     - ComplianceSection.tsx
     - FounderSection.tsx
     - etc.
   - Dead code that should be cleaned up

6. **Different Booking Calendar ID**
   - TestBatchCalendar uses `qouvhbJbcESjMOoZePop`
   - Different from Site 1's `x2ycChO5k7nMsFBd8ngj`
   - **Verify:** Are these intentionally different calendars?

7. **Large Bundle Size**
   - index.js is 326KB (gzipped: 105KB)
   - Site 1's is 139KB (gzipped: 40KB)
   - Likely due to no code splitting on testimonials slider

#### 🟢 LOW
8. **Missing LazySection Component**
   - Site 1 uses LazySection for intersection-observer loading
   - Site 2 removed it - all sections load immediately
   - Minor performance impact

9. **Phone Number Hard-Coded**
   - `(806) 541-5366` in Header
   - Should probably be configurable

---

## Shared Issues (Both Sites)

### Environment Variables
Both sites use placeholder env values that must be configured:

| Var | Site 1 | Site 2 | Notes |
|-----|--------|--------|-------|
| `VITE_SUPABASE_URL` | ✅ Set | ✅ Set | Different projects |
| `VITE_SUPABASE_PUBLISHABLE_KEY` | ✅ Set | ✅ Set | Anon keys |
| `LEADCONNECTOR_WEBHOOK_URL` | ❓ Server | N/A | Supabase secret |

### Webhook URLs (Hardcoded)
- **Onboarding (both):** `https://services.leadconnectorhq.com/hooks/OsNgWuy8oZzLbp5BXbnD/webhook-trigger/caf6afbb-04d1-4dda-9b12-8ef27b95f6d8`
- **Site 1 Qualify:** Uses Supabase edge function proxy

### HighLevel Calendar Embeds
| Location | Site 1 | Site 2 |
|----------|--------|--------|
| Qualify → Calendar | `x2ycChO5k7nMsFBd8ngj` | `qouvhbJbcESjMOoZePop` |
| Onboarding Step 10 | `7O0pR7pTszdSEmQVBWMK` | `7O0pR7pTszdSEmQVBWMK` |

---

## Component Comparison

### Only in Site 1 (kuriosbrand)
- `InHouseIntakeSection.tsx`
- `LazySection.tsx`
- `LiveTransfersSection.tsx`
- `Login.tsx` (broken)

### Only in Site 2 (kuriosnew)
- `AIFirstSection.tsx` (unused)
- `DualHowItWorks.tsx`
- `ExclusiveLeadsSection.tsx` (unused)
- `FinalCTA.tsx`
- `GuaranteeSection.tsx` (unused)
- `MobileStickyApply.tsx`
- `TestimonialsSlider.tsx`
- `TrustCredibility.tsx`
- `TwoOfferCards.tsx`
- `WeHandleDirtyWork.tsx` (unused)
- `useGeoLocation.ts` hook

### In Both (potentially different implementations)
- HeroSection (very different)
- Header (Site 2 has phone, geolocation)
- Qualify (Site 1 has quiz, Site 2 is simple)
- Footer (similar)
- Most legal pages

---

## Recommendations

### Immediate Actions (This Week)
1. **Remove or fix Login page** on Site 1
2. **Verify Supabase webhook-proxy env var** is set
3. **Implement offer query param handling** on Site 2
4. **Optimize mark-gundrum.png** (compress to <300KB)
5. **Verify all 3 HighLevel calendars** are correct

### Short-Term (This Month)
1. **Clean up unused components** in Site 2
2. **Add error tracking** (Sentry or similar)
3. **Add lead backup to Supabase** tables
4. **Consider consolidating** to one site
5. **Fix hard-coded scarcity** messaging

### Long-Term Considerations
1. **A/B test** Site 1 vs Site 2 to determine winner
2. **Implement proper authentication** if client portal needed
3. **Server-side geolocation** for reliability
4. **Analytics integration** (GA4, Mixpanel)

---

## Files Reference

### Site 1 Key Files
```
/tmp/kuriosbrand/
├── src/
│   ├── pages/
│   │   ├── Index.tsx (13 lazy-loaded sections)
│   │   ├── Qualify.tsx (3-step quiz + webhook)
│   │   ├── Onboarding.tsx (10-step form)
│   │   ├── Login.tsx (BROKEN)
│   │   └── TestBatchCalendar.tsx
│   ├── components/ (20 components)
│   └── integrations/supabase/
├── supabase/functions/
│   ├── webhook-proxy/
│   └── verify-website/
└── .env
```

### Site 2 Key Files
```
/tmp/kuriosnew/
├── src/
│   ├── pages/
│   │   ├── Index.tsx (8 sections + mobile sticky)
│   │   ├── Qualify.tsx (simple checkbox)
│   │   ├── Onboarding.tsx (same as Site 1)
│   │   └── TestBatchCalendar.tsx
│   ├── components/ (27 components, some unused)
│   ├── hooks/useGeoLocation.ts
│   └── integrations/supabase/
└── .env
```

---

## Conclusion

**kuriosnew (Site 2) is the more polished, conversion-optimized version** with:
- Cleaner design
- Geolocation personalization
- Dual offer structure
- Simpler qualification flow

**kuriosbrand (Site 1) has legacy features** including:
- Detailed qualification quiz (good for filtering)
- Broken login page
- More conservative conversion path

**My recommendation:** Use Site 2 for new traffic, but implement the offer query param handling first. Consider migrating the qualification quiz logic from Site 1 if you want to filter out low-quality leads before they book calls.
