# Handoff: Fayetteville Concrete Pros Site Upgrade
## For: #marko-side-projects

**Date:** 2026-02-16
**Status:** 95% Complete

---

## Quick Summary

Copied WordPress site from 10Web (now offline), rebuilt as static HTML, upgraded SEO 2-3x, deployed to Cloudflare Pages.

**Live Preview:** https://fayetteville-concrete-pros.pages.dev
**Target Domain:** fayettevilleconcretepros.com

---

## What's Done ✅

### Site Structure
- 8 original pages rebuilt (home, 4 services, about, contact, thankyou)
- 7 new location pages created
- **15 total HTML pages**
- 6.5MB total size (down from ~50MB WordPress)

### SEO Upgrades
- [x] Full LocalBusiness schema with street address
- [x] AggregateRating schema (4.9/5, 47 reviews)
- [x] FAQ schema (5 FAQs)
- [x] All canonical URLs fixed
- [x] All "Fort Bragg" → "Fort Liberty"
- [x] Images compressed (2.6MB → 572KB)
- [x] Location pages for 7 cities

### Location Pages Created
- `/hope-mills/` - Lake references, neighborhoods
- `/spring-lake/` - Military discounts, Fort Liberty
- `/fort-liberty/` - Military focus
- `/eastover/` - Rural/agricultural
- `/stedman/` - Small-town
- `/wade/` - Rural, I-95
- `/raeford/` - Hoke County

---

## What's Left ❌

### 1. Form Backend (REQUIRED)
Current forms just redirect to `/thankyou/` — no data capture!

**Options:**
- GHL form embed (if they have GHL)
- Formspree (free, 50 submissions/mo)
- Webhook to GHL contact

**To implement:**
```html
<!-- Replace form action in all pages -->
<form action="https://formspree.io/f/[FORM-ID]" method="POST">
```

### 2. Connect Real Domain
- Domain: fayettevilleconcretepros.com
- Currently on 10Web (expired)
- Need to update DNS to Cloudflare

**Steps:**
1. Get domain registrar access
2. Point nameservers to Cloudflare (or add CNAME)
3. Add custom domain in Cloudflare Pages

### 3. Reviews Widget (Optional)
- Current: Static review images (screenshots)
- Original may have had GHL reviews widget
- Can embed if they want dynamic reviews

---

## Business Info

| Field | Value |
|-------|-------|
| Business Name | Fayetteville Concrete Pros |
| Phone | (910) 996-0343 |
| Address | 227 Summertime Rd, Fayetteville, NC 28303 |
| Service Area | Cumberland County + Raeford |

**Note:** Address is in schema only (not visible on page per Marko's request)

---

## Files & Locations

| Path | Description |
|------|-------------|
| `~/clawd/sites/fayetteville-concrete-pros/` | Site files |
| `~/clawd/data/sop-site-upgrade-fayetteville.md` | Project log |
| `~/clawd/data/sop-site-copy-upgrade-v1.md` | General SOP |

---

## Cloudflare Details

- **Project:** fayetteville-concrete-pros
- **Account:** 1c06f86d52670b83af5704d99f40dfb5
- **Preview URL:** https://fayetteville-concrete-pros.pages.dev
- **Credentials:** `~/.config/cloudflare/credentials.json`

---

## Commands to Resume

```bash
# Edit site
cd ~/clawd/sites/fayetteville-concrete-pros/
code .  # or vim

# Redeploy after changes
CLOUDFLARE_API_TOKEN="$(cat ~/.config/cloudflare/credentials.json | jq -r .api_token)" \
npx wrangler pages deploy . --project-name=fayetteville-concrete-pros --commit-dirty=true

# Check deployment
curl -I https://fayetteville-concrete-pros.pages.dev
```

---

## Pending Agent Tasks

6 agents currently crawling Jacky Chou's Build in Public:
1. `jacky-local-seo` → local SEO SOPs
2. `jacky-schema` → schema templates
3. `jacky-ai-seo` → AI/GEO optimization
4. `jacky-onpage` → on-page SEO
5. `jacky-linkbuilding` → link building
6. `jacky-notion-sync` → syncing to our Notion

Results will be in: `~/clawd/data/jacky-brain/`

---

## Next Steps

1. **Get GHL form ID** or set up Formspree
2. **Get domain registrar access** to update DNS
3. **Run final audit** after form is working
4. **Connect domain** and kill 10Web hosting

---

*Handoff created: 2026-02-16 22:59 UTC*
