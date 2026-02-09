# SOP: MVA Site Build & Deployment

**Last Updated:** 2026-02-09
**Author:** Sierra
**Version:** 1.0

---

## Overview

This SOP covers the complete workflow for building, auditing, and deploying MVA (Motor Vehicle Accident) lead generation sites to Cloudflare Pages with custom domains.

---

## Phase 1: Site Build

### 1.1 Project Setup
```bash
# Create project directory
mkdir -p ~/clawd/sites/[domain-name]
cd ~/clawd/sites/[domain-name]

# Initialize Astro project
npm create astro@latest . -- --template minimal --typescript --git
npm install tailwindcss @tailwindcss/typography
npm install @astrojs/sitemap
```

### 1.2 Required Configuration

**astro.config.mjs:**
```javascript
export default defineConfig({
  site: 'https://[domain-name]',  // ⚠️ MUST be production URL, NOT localhost
  integrations: [sitemap()],
});
```

### 1.3 Required Files Checklist
- [ ] `public/robots.txt` with sitemap reference
- [ ] `src/pages/404.astro` custom error page
- [ ] `src/pages/privacy-policy.astro`
- [ ] `src/pages/terms-of-service.astro`
- [ ] `src/pages/disclaimer.astro`
- [ ] Lead capture forms on ALL pages

### 1.4 Content Requirements

**NO PHONE NUMBERS OR CALL BUTTONS** on any site except `texastruckaccidents.net`

❌ WRONG:
```html
<a href="tel:1-800-555-0123">Call Now</a>
```

✅ CORRECT:
```html
<a href="/free-consultation">Free Consultation</a>
<a href="#contact-form">Chat With Us 24/7</a>
```

### 1.5 Form Configuration

All forms MUST have:
```html
<form 
  action="https://services.leadconnectorhq.com/hooks/ASHRZ5ZFolSHXM3RyPvk/webhook-trigger/[WEBHOOK-ID]"
  method="POST"
>
```

**Webhook IDs by site type:**
- `ctlaw-home` - Homepage forms
- `ctlaw-state` - State page forms
- `ctlaw-city` - City page forms
- `ctlaw-blog` - Blog sidebar forms
- `ctlaw-contact` - Contact page forms
- `ctlaw-consultation` - Free consultation forms

---

## Phase 2: Audit Process

### 2.1 Audit Requirements
- **Minimum 3 audits per site**
- **Passing score: 950+/1000**
- Must pass ALL 3 audits before deployment

### 2.2 Audit Categories
| Category | Weight | Key Checks |
|----------|--------|------------|
| Technical SEO | 250 | robots.txt, sitemap, 404, canonical tags |
| On-Page SEO | 250 | Title <60 chars, meta <160 chars, single H1 |
| Content Quality | 250 | Legal pages, E-E-A-T signals, unique content |
| Conversion | 250 | All forms work, GHL webhooks, no broken links |

### 2.3 Common Audit Failures
1. **Forms missing action/method** → -25 points per page type
2. **Title tags >60 chars** → -5 points per 10 pages
3. **Missing robots.txt** → -20 points
4. **Missing 404 page** → -15 points
5. **Phone numbers present** → -50 points (except texastruckaccidents.net)

---

## Phase 3: Cloudflare Pages Deployment

### 3.1 Pre-Deployment Checklist
- [ ] `npm run build` succeeds locally
- [ ] All 3 audits passed (950+ each)
- [ ] No phone numbers in code (grep -r "tel:" src/)
- [ ] No localhost references (grep -r "localhost" src/)
- [ ] Site URL correct in astro.config.mjs

### 3.2 Read Credentials First

⚠️ **CRITICAL: ALWAYS read credentials from file before ANY API call**

```bash
# ALWAYS do this FIRST
cat ~/.config/cloudflare/credentials.json
```

Then use the token from the file. **NEVER use tokens from memory.**

### 3.3 Deploy to Cloudflare Pages

**Step 1: Build the site**
```bash
cd ~/clawd/sites/[domain-name]
npm run build
```

**Step 2: Deploy via Wrangler**
```bash
# Read token first
export CLOUDFLARE_API_TOKEN=$(cat ~/.config/cloudflare/credentials.json | jq -r '.api_token')
export CLOUDFLARE_ACCOUNT_ID="1c06f86d52670b83af5704d99f40dfb5"

# Deploy
npx wrangler pages deploy dist --project-name=[project-name]-site
```

**Step 3: Verify deployment**
```bash
curl -I https://[project-name]-site.pages.dev
# Should return 200 OK
```

---

## Phase 4: Custom Domain Configuration

### 4.1 Domain Attachment Flow

This is where failures often occur. Follow EXACTLY:

**Step 1: Check if domain is already attached to another project**
```bash
# List all Pages projects
curl -X GET "https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/pages/projects" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" | jq '.result[] | {name, domains}'
```

**Step 2: If domain attached to OLD project, remove it first**
```bash
# Remove from old project
curl -X DELETE "https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/pages/projects/[OLD-PROJECT]/domains/[domain.com]" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN"
```

**Step 3: Add domain to NEW project**
```bash
# Add root domain
curl -X POST "https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/pages/projects/[NEW-PROJECT]/domains" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "[domain.com]"}'

# Add www subdomain
curl -X POST "https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/pages/projects/[NEW-PROJECT]/domains" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "www.[domain.com]"}'
```

### 4.2 DNS Configuration

**Step 1: Get Zone ID**
```bash
curl -X GET "https://api.cloudflare.com/client/v4/zones?name=[domain.com]" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" | jq '.result[0].id'
```

**Step 2: Delete old DNS records (if any)**
```bash
# List existing records
curl -X GET "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" | jq '.result[] | {id, type, name, content}'

# Delete conflicting A/CNAME records
curl -X DELETE "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records/[RECORD_ID]" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN"
```

**Step 3: Create correct CNAME records**
```bash
# Root domain (@) - CNAME flattening
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "CNAME",
    "name": "@",
    "content": "[project-name]-site.pages.dev",
    "proxied": true
  }'

# WWW subdomain
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "CNAME",
    "name": "www",
    "content": "[project-name]-site.pages.dev",
    "proxied": true
  }'
```

### 4.3 Verify Domain Connection

```bash
# Check Pages domain status
curl -X GET "https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/pages/projects/[PROJECT]/domains" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" | jq '.result[] | {name, status}'

# Should show "active" for both domains

# Test live site
curl -I https://[domain.com]
# Should return 200 OK
```

---

## Phase 5: Post-Deployment Verification

### 5.1 Full Verification Checklist
- [ ] `https://[domain.com]` returns 200 OK
- [ ] `https://www.[domain.com]` returns 200 OK
- [ ] SSL certificate active (padlock shows)
- [ ] All pages load (spot check 5-10 pages)
- [ ] Forms submit successfully (test submission)
- [ ] No phone numbers visible on site
- [ ] Footer shows "Built by Sierra, an autonomous AI agent"

### 5.2 DNS Propagation

If site returns 522 or ERR_NAME_NOT_RESOLVED:
1. **Wait 5-10 minutes** — DNS propagation takes time
2. **Check DNS resolution:**
   ```bash
   dig [domain.com] +short
   # Should return Cloudflare IPs (104.x.x.x or 172.x.x.x)
   ```
3. **Flush local DNS cache** (if testing locally)
4. **Test via pages.dev** to confirm deployment worked:
   ```bash
   curl -I https://[project-name]-site.pages.dev
   ```

---

## Common Failure Modes & Fixes

### Failure: "Site not deployed"
**Symptom:** Domain shows error, but pages.dev works
**Cause:** Domain not attached to Pages project
**Fix:** Run Phase 4.1 (Domain Attachment Flow)

### Failure: "DNS pointing to wrong project"
**Symptom:** Old/wrong site shows on domain
**Cause:** CNAME points to old project (e.g., `[project].pages.dev` instead of `[project]-site.pages.dev`)
**Fix:**
1. Delete old CNAME records
2. Create new CNAME pointing to `[project]-site.pages.dev`

### Failure: "Domain conflict"
**Symptom:** "Domain already in use" error
**Cause:** Domain attached to different Pages project
**Fix:**
1. Find which project has the domain (Phase 4.1 Step 1)
2. Remove domain from old project (Phase 4.1 Step 2)
3. Add to new project (Phase 4.1 Step 3)

### Failure: "Invalid token"
**Symptom:** 401 Unauthorized on API calls
**Cause:** Using old/wrong token from memory
**Fix:**
1. `cat ~/.config/cloudflare/credentials.json`
2. Use the token from the file, not memory
3. If still fails, ask Marko to roll token

### Failure: "Phone numbers on site"
**Symptom:** Marko finds call buttons
**Cause:** Template included phone links
**Fix:**
```bash
# Find all phone references
grep -r "tel:" src/
grep -r "1-800" src/
grep -r "Call Now" src/

# Replace with form CTAs
# "Call Now" → "Free Consultation"
# "tel:" links → "/free-consultation" links
```

---

## Quick Reference

### Project Naming Convention
- Domain: `commercialtrucklaw.com`
- Pages Project: `commercialtrucklaw-site`
- Pages URL: `commercialtrucklaw-site.pages.dev`

### Cloudflare Account
- Account ID: `1c06f86d52670b83af5704d99f40dfb5`
- Credentials: `~/.config/cloudflare/credentials.json`

### GHL Location
- Location ID: `OsNgWuy8oZzLbp5BXbnD`
- Webhook base: `https://services.leadconnectorhq.com/hooks/ASHRZ5ZFolSHXM3RyPvk/webhook-trigger/`

---

## Deployment Summary Checklist

```
□ 1. Build site locally (npm run build)
□ 2. Pass 3x audits (950+ each)
□ 3. READ Cloudflare credentials from file
□ 4. Deploy to Cloudflare Pages
□ 5. Verify pages.dev URL works
□ 6. Check if domain attached to old project → remove if yes
□ 7. Attach domain to new project (root + www)
□ 8. Delete old DNS CNAME records
□ 9. Create new DNS CNAME records → [project]-site.pages.dev
□ 10. Wait for DNS propagation (5-10 min)
□ 11. Verify https://[domain.com] returns 200
□ 12. Test form submission
□ 13. Confirm no phone numbers on site
□ 14. Update site-build-tracker.md
```

---

*This SOP was created after the 2026-02-09 commercialtrucklaw.com deployment where multiple issues occurred: domain not attached, DNS pointing to wrong project, phone numbers present. Following this SOP will prevent those failures.*
