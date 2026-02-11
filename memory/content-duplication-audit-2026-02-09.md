# MVA Sites Content Duplication Audit
**Date:** 2026-02-09
**Sites Audited:** 9 MVA lead gen sites
**Status:** ✅ ALL FIXED (2026-02-10)

## 🎉 FIXED — All Issues Resolved

**All critical issues fixed and deployed.** Sites now have unique content and no broken find/replace errors.

---

## CRITICAL ISSUES (Fix Immediately)

### 1. BROKEN FIND/REPLACE - Lyft Site Has "Lyft and Lyft"
**Severity:** 🔴 CRITICAL
**Site:** lyftcrashlaw
**Problem:** Lazy find/replace of "Uber" → "Lyft" resulted in "Lyft and Lyft" instead of "Uber and Lyft"

**Files affected (100+ instances):**
- `/home/ec2-user/sites/lyftcrashlaw/src/pages/faq.astro` (Line ~82: "Lyft and Lyft accident claims")
- `/home/ec2-user/sites/lyftcrashlaw/src/pages/about.astro` ("Lyft and Lyft accident victims")
- `/home/ec2-user/sites/lyftcrashlaw/src/pages/disclaimer.astro` (2 occurrences)
- `/home/ec2-user/sites/lyftcrashlaw/src/pages/terms-of-service.astro`
- `/home/ec2-user/sites/lyftcrashlaw/src/pages/case-types/index.astro`
- `/home/ec2-user/sites/lyftcrashlaw/src/data/articles.ts` ("Lyft and Lyft")
- `/home/ec2-user/sites/lyftcrashlaw/src/data/resources.ts`
- `/home/ec2-user/sites/lyftcrashlaw/src/pages/blog/[slug].astro` - affects ALL 80+ blog posts

**Fix:** Global find/replace: `"Lyft and Lyft"` → `"Uber and Lyft"` OR `"Lyft"`

---

### 2. BROKEN FIND/REPLACE - Rideshare Site Has "Uber or Lyft or Lyft"
**Severity:** 🔴 CRITICAL
**Site:** ridesharelawyersnearme
**Problem:** Double "Lyft" in passenger description

**Files affected:**
- `/home/ec2-user/sites/ridesharelawyersnearme/src/pages/index.astro` (Line ~232)
  - Text: `"Injured while riding in an Uber or Lyft or Lyft vehicle"`
- `/home/ec2-user/sites/ridesharelawyersnearme/src/pages/about.astro`

**Fix:** Replace `"Uber or Lyft or Lyft"` → `"Uber or Lyft"`

---

### 3. FAQ Pages Are Near-Identical (SEO Risk)
**Severity:** 🟠 HIGH
**Sites:** uberlawyersnearme, ridesharelawyersnearme, lyftcrashlaw
**Problem:** All 3 sites share virtually the same 12 FAQs with only brand name substitutions

**Example - Same FAQ answer appearing on all 3:**
```
"Most Uber accident attorneys work on a contingency fee basis..."
```
This appears word-for-word on:
- `/home/ec2-user/sites/uberlawyersnearme/src/pages/faq.astro`
- `/home/ec2-user/sites/ridesharelawyersnearme/src/pages/faq.astro` (says "Uber" in answers)
- `/home/ec2-user/sites/lyftcrashlaw/src/pages/faq.astro` (says "Uber" in some answers!)

**Fix:** Rewrite FAQs to be unique per site:
- Uber site: Focus on Uber-specific questions (Uber One, UberX vs Uber Black, etc.)
- Lyft site: Focus on Lyft-specific (Lyft Pink, Lyft history, Lyft vs Uber differences)
- Rideshare site: Generic rideshare focus, compare both platforms

---

### 4. Lyft FAQ Still References "Uber" in Answers
**Severity:** 🟠 HIGH  
**Site:** lyftcrashlaw
**Problem:** FAQ questions say "Lyft" but answers still reference Uber

**File:** `/home/ec2-user/sites/lyftcrashlaw/src/pages/faq.astro`

**Examples:**
- Line ~28: `"Most Lyft accident attorneys work on a contingency fee basis..."` (should mention Lyft)
- Line ~69: `"...Uber's uninsured/underinsured motorist coverage..."` (should be Lyft)
- Line ~52: `"Yes, Lyft passengers typically have strong cases..."` but then says "Uber" 

**Fix:** Manually review and rewrite answers to reference Lyft specifically

---

## MODERATE ISSUES

### 5. State Page Templates Nearly Identical
**Severity:** 🟡 MODERATE
**Sites:** uberlawyersnearme, ridesharelawyersnearme, lyftcrashlaw

**Files:**
- `/home/ec2-user/sites/uberlawyersnearme/src/pages/states/[state].astro`
- `/home/ec2-user/sites/ridesharelawyersnearme/src/pages/states/[state].astro`
- `/home/ec2-user/sites/lyftcrashlaw/src/pages/states/[state].astro`

**Problem:** Same template structure, same sections, just different brand names. Google may see these as duplicate content since they serve the same intent.

**Recommendation:** Add unique sections per site:
- Uber site: Add Uber-specific state regulations, Uber market size per state
- Lyft site: Add Lyft-specific data, Lyft driver requirements by state
- Rideshare: Compare both platforms in each state

---

### 6. City Templates Follow Same Pattern
**Severity:** 🟡 MODERATE  
**Same issue as state templates**

---

### 7. Privacy/Terms/Disclaimer Pages
**Severity:** 🟢 LOW (acceptable)
**Problem:** These are essentially the same with brand name substitutions
**Verdict:** This is FINE - legal boilerplate is expected to be similar

---

## GOOD NEWS ✅

### Unique Homepage Content
All 9 sites have properly differentiated homepage content:

| Site | Niche Focus | Verdict |
|------|-------------|---------|
| commercialtrucklaw | 18-wheelers, FMCSA regs, truck-specific | ✅ Unique |
| cyclistaccidentlawyer | Bicycle laws, dooring, bike lanes | ✅ Unique |
| motorcyclewrecklaw | Helmet laws, lane splitting, rider bias | ✅ Unique |
| pedestrianaccidentlawyer | Crosswalk laws, vulnerable road users | ✅ Unique |
| ridesharelawyersnearme | General rideshare, insurance tiers | ✅ Unique |
| lyftcrashlaw | Lyft-specific history, pink mustache era | ✅ Unique |
| uberlawyersnearme | Uber-specific focus | ✅ Unique |
| hitandrunlawyer | UM/UIM claims, finding drivers | ✅ Unique |
| deliverytruckaccident | Amazon, FedEx, UPS specific | ✅ Unique |

### Hit and Run Site Has Unique FAQs ✅
`/home/ec2-user/sites/hitandrunlawyer/src/pages/faq.astro` is properly unique with hit-and-run specific content (UM coverage, finding drivers, parking lot incidents, etc.)

### Delivery Truck Site Is Properly Unique ✅
Focus on Amazon DSP, FedEx Ground, UPS - not duplicated from other sites.

---

## RECOMMENDED FIXES (Priority Order)

### PRIORITY 1: Fix Broken Text (30 mins)
```bash
# Fix Lyft site "Lyft and Lyft" 
cd /home/ec2-user/sites/lyftcrashlaw
grep -rl "Lyft and Lyft" src/ | xargs sed -i 's/Lyft and Lyft/Uber and Lyft/g'

# Fix Rideshare site double Lyft
cd /home/ec2-user/sites/ridesharelawyersnearme
grep -rl "Uber or Lyft or Lyft" src/ | xargs sed -i 's/Uber or Lyft or Lyft/Uber or Lyft/g'
```

### PRIORITY 2: Fix Lyft FAQ References (1 hour)
Manually rewrite `/home/ec2-user/sites/lyftcrashlaw/src/pages/faq.astro` to:
- Change all "Uber" references to "Lyft" 
- Add Lyft-specific context

### PRIORITY 3: Differentiate FAQ Pages (2-3 hours)
Rewrite FAQs on each rideshare site to be unique:

**Uber site - Add unique questions like:**
- "What's the difference between UberX and Uber Black coverage?"
- "Does Uber's new safety features affect my claim?"

**Lyft site - Add unique questions like:**
- "How does Lyft's insurance differ from Uber's?"
- "What happened to Lyft's original pink mustache policy?"

**Rideshare site - Keep generic but add:**
- "Should I use Uber or Lyft after an accident?"
- "How do I check which app the driver was using?"

### PRIORITY 4: Add Unique Sections to State Pages (4-6 hours)
Each site's state template should have 1-2 unique sections that the others don't have.

---

## Files Summary

| Issue | File Path | Line/Location | Fix |
|-------|-----------|---------------|-----|
| "Lyft and Lyft" | lyftcrashlaw/src/pages/faq.astro | Multiple | Find/replace |
| "Lyft and Lyft" | lyftcrashlaw/src/pages/about.astro | Line 15 | Find/replace |
| "Lyft and Lyft" | lyftcrashlaw/src/pages/disclaimer.astro | Lines 8, 21 | Find/replace |
| "Lyft and Lyft" | lyftcrashlaw/src/data/articles.ts | Multiple | Find/replace |
| "Lyft and Lyft" | lyftcrashlaw/src/pages/blog/[slug].astro | Intro paragraph | Find/replace |
| "Uber or Lyft or Lyft" | ridesharelawyersnearme/src/pages/index.astro | Line 232 | Find/replace |
| "Uber or Lyft or Lyft" | ridesharelawyersnearme/src/pages/about.astro | Line 88-89 | Find/replace |
| Duplicate FAQ | uberlawyersnearme/src/pages/faq.astro | All | Rewrite |
| Duplicate FAQ | ridesharelawyersnearme/src/pages/faq.astro | All | Rewrite |
| Duplicate FAQ | lyftcrashlaw/src/pages/faq.astro | All | Rewrite |
| Uber refs in Lyft | lyftcrashlaw/src/pages/faq.astro | Lines 28, 52, 69 | Manual fix |

---

**Audit completed by Sierra | 2026-02-09**
