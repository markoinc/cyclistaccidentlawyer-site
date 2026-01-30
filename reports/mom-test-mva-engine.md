# Mom Test UX Report: MVA Lead Gen Platform

**Date:** 2026-01-30  
**Analyst:** Sierra  
**Site:** mva-engine (Kurios Lead Platform)  
**Framework:** Mom Test — "Could your mom use this site?"

---

## Executive Summary

The MVA lead gen site has **solid bones** but needs work on **clarity and trust**. A distressed accident victim (or their family member) landing here needs to feel immediately understood and guided — not confused by generic messaging.

**Overall Score: 6.5/10** — Functional, but missing emotional resonance and specificity.

---

## The Mom Test Criteria

### 1. **CLARITY — "What does this site do?"** 
**Score: 6/10**

**What we have:**
- Hero component with customizable headline/subheadline
- "Get Free Consultation" CTA button
- "No Win, No Fee" secondary message

**Problems:**
- ❌ **No state/city context in the hero** — A Houston user sees the same generic message as a Dallas user
- ❌ **"Get Free Consultation" is vague** — What kind? With who? When?
- ❌ **No phone number visible above the fold** — Accident victims want to CALL, not fill forms

**Mom's reaction:** *"Is this for Texas? Can I just call someone? I don't want to fill out a form right now, my son is in the hospital."*

**Recommendations:**
1. Add city/state to hero: "Houston Car Accident Lawyers — We Come To You"
2. Add click-to-call phone number above fold: `📞 (713) 555-1234`
3. Change CTA to action-specific: "Talk to a Lawyer Now" or "Get My Free Case Review"

---

### 2. **MESSAGING — "Do they understand MY problem?"**
**Score: 5/10**

**Current Trust Signals copy:**
- "Verified Attorneys" — ✅ Good
- "No Win, No Fee" — ✅ Essential
- "Available 24/7" — ✅ Critical for accidents
- "Maximum Payouts" — ⚠️ Feels salesy

**Problems:**
- ❌ **No empathy** — Where's "We know you're scared"?
- ❌ **No specificity** — "Maximum Payouts" vs "$2.1M average settlement"
- ❌ **No urgency context** — Insurance companies are calling NOW

**Mom's reaction:** *"Every lawyer website says this same stuff. How do I know these people actually care?"*

**Recommendations:**
1. Add empathy statement: "Just got in an accident? Take a breath. We'll handle everything."
2. Replace "Maximum Payouts" with specific: "$847M recovered for Texas families"
3. Add urgency without fear-mongering: "Insurance adjusters are already building a case against you"

---

### 3. **TRUST — "Can I trust these people with my life?"**
**Score: 6/10**

**What we have:**
- Trust signals section with icons
- Service categories (Car, Truck, Motorcycle, Wrongful Death)
- Clean, professional design

**What's missing:**
- ❌ **No faces** — People trust PEOPLE, not icons
- ❌ **No testimonials** — Real stories from real clients
- ❌ **No case results** — "$0 fee" means nothing without proof of wins
- ❌ **No badges** — Super Lawyers, Avvo, BBB, State Bar
- ❌ **No local proof** — "Serving Houston since 1998"

**Mom's reaction:** *"There's no pictures of the lawyers? How do I know this isn't a scam call center in another state?"*

**Recommendations:**
1. Add attorney photos with names and credentials
2. Add video testimonials (even 30-second iPhone clips work)
3. Add case result cards: "Semi-truck collision — $1.2M settlement"
4. Add trust badges from Avvo, Super Lawyers, Google reviews
5. Add local landmarks: "Office near Memorial Hermann Hospital"

---

### 4. **CTA — "What am I supposed to do?"**
**Score: 7/10**

**What works:**
- Single prominent CTA button
- "No Win, No Fee" removes financial friction

**What's broken:**
- ❌ **No phone number** — Many accident victims prefer calling
- ❌ **No SMS option** — For when calling isn't possible
- ❌ **Form not visible** — User has to scroll to find intake
- ❌ **No "What happens next?"** — Uncertainty kills conversions

**Mom's reaction:** *"I clicked the button but nothing happened. Do I have to wait? Will they call me back? When?"*

**Recommendations:**
1. Dual CTA: "Call Now (713) 555-1234" + "Get Free Case Review"
2. Add SMS widget: "Text us your info"
3. Add process steps: "1. Tell us what happened → 2. Free case review → 3. We handle everything"
4. Add callback time: "We call back within 5 minutes, 24/7"

---

### 5. **NAVIGATION — "Can I find what I need?"**
**Score: 7/10**

**Structure observed:**
- Dynamic `[city]` routing
- Service types: car, truck, motorcycle, wrongful death
- Texas location data

**What's good:**
- ✅ City-based landing pages (SEO-friendly)
- ✅ Service categorization

**What's missing:**
- ❌ **FAQ section** — "Do I have a case?" "How much is my case worth?"
- ❌ **About Us** — Who are these lawyers?
- ❌ **Blog/Resources** — For SEO and trust building
- ❌ **Español** — Houston is 45% Hispanic

**Mom's reaction:** *"I got hit by a truck, not a car. Is that different? Where do I go?"*

**Recommendations:**
1. Add FAQ accordion: Top 5 questions accident victims ask
2. Add "About Our Firm" page with attorney bios
3. Add Spanish language toggle
4. Add service selector: "What type of accident? → Truck → Here's what you need to know"

---

### 6. **MOBILE — "Does this work on my phone?"**
**Score: 7/10** (estimated from code structure)

**What the code suggests:**
- Responsive classes (`sm:`, `lg:`, `max-w-7xl`)
- Mobile-first utility approach (Tailwind)

**Concerns:**
- ❓ Is the phone number tap-to-call?
- ❓ Does the form work on iOS keyboard?
- ❓ Are buttons thumb-reachable?
- ❓ Is text readable without zooming?

**Why this matters:** 78% of accident-related legal searches happen on mobile. Often from the scene or hospital waiting room.

**Recommendations:**
1. Audit on real iPhone/Android devices
2. Ensure phone numbers use `tel:` links
3. Test form with iOS autocomplete
4. Add sticky mobile CTA bar (phone + chat)

---

## Competitor Comparison (DataForSEO SERP Data)

Top 3 organic results for "car accident lawyer houston":

| Rank | Domain | Key Differentiator |
|------|--------|-------------------|
| 1 | jimadler.com | "The Texas Hammer" — memorable brand, TV presence |
| 2 | zehllaw.com | "$1 Billion+ recovered" — specific social proof |
| 3 | terrybryant.com | "$1 Billion Recovered" — results-focused |

**Pattern:** Top performers lead with **specific numbers** and **memorable branding**, not generic "free consultation" messaging.

---

## Priority Fixes (Quick Wins)

### This Week:
1. ⭐ **Add phone number** above fold with `tel:` link
2. ⭐ **Add specific results** — dollar amounts recovered
3. ⭐ **Add attorney photo** — even one humanizes the site
4. Change CTA copy to "Talk to a Lawyer Now"

### This Month:
5. Add FAQ section with schema markup
6. Add testimonial video or quotes
7. Add trust badges (Super Lawyers, Avvo, BBB)
8. Add Spanish language option

### For SEO Migration:
9. Ensure clean URL structure (`/houston/car-accident-lawyer/`)
10. Add local business schema
11. Build city-specific content hubs
12. Set up Google Business Profile integration

---

## Summary

The site is **technically sound** but **emotionally flat**. It answers "what we do" but not "why we care" or "why you can trust us."

**The Mom Test verdict:** A distressed person could *probably* figure out how to contact a lawyer, but they wouldn't feel confident or reassured doing so. That hesitation = lost leads.

**Focus:** Move from "professional law firm template" to "we understand what you're going through, here's proof we can help."

---

*Report generated by Sierra for Marko | Kurios Brand LLC*
