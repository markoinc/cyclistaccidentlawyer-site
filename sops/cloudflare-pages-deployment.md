# SOP: Deploying Sites & Apps to Cloudflare Pages

**Created:** 2026-02-01  
**Last Updated:** 2026-02-01

---

## Overview

Deploy static sites and web apps (Next.js, Astro, React, etc.) to Cloudflare Pages via GitHub integration. Free tier includes unlimited sites, unlimited bandwidth, and automatic deployments.

---

## Prerequisites

- Cloudflare account (free)
- GitHub repo with your site code
- Domain in Cloudflare DNS (if using custom domain)

---

## Part 1: Connect GitHub Repo to Cloudflare Pages

### Step 1: Create Pages Project

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Select your account → **Workers & Pages** (left sidebar)
3. Click **Create** → **Pages** → **Connect to Git**
4. Authorize Cloudflare to access your GitHub (first time only)
5. Select the repository

### Step 2: Configure Build Settings

| Framework | Build Command | Output Directory |
|-----------|---------------|------------------|
| **Next.js** | `npm run build` | `.next` or `out` (static export) |
| **Astro** | `npm run build` | `dist` |
| **React (CRA)** | `npm run build` | `build` |
| **Vite** | `npm run build` | `dist` |
| **Static HTML** | (leave empty) | `/` or folder name |

**Environment Variables:**
- Add any needed env vars (API keys, etc.)
- For Next.js: set `NODE_VERSION=18` or higher if needed

### Step 3: Deploy

1. Click **Save and Deploy**
2. Wait for build to complete (~1-3 min)
3. Get your `*.pages.dev` URL

---

## Part 2: Connect Custom Domain

### Option A: Domain Already in Cloudflare

1. In your Pages project → **Custom domains** tab
2. Click **Set up a custom domain**
3. Enter your domain (e.g., `example.com` or `app.example.com`)
4. Cloudflare auto-adds the DNS record
5. Wait for SSL certificate (~minutes)

### Option B: Domain in Another Registrar (e.g., Namecheap)

**Step 1: Add domain to Cloudflare**
1. Cloudflare Dashboard → **Add a site**
2. Enter domain → Select **Free** plan
3. Cloudflare scans existing DNS records
4. Review/add records as needed

**Step 2: Update nameservers**
1. Cloudflare shows two nameservers (e.g., `ada.ns.cloudflare.com`)
2. Go to your registrar (Namecheap, etc.)
3. Change nameservers from default to Cloudflare's
4. Wait for propagation (minutes to 24h, usually fast)

**Step 3: Connect to Pages**
- Follow Option A above once domain is active in Cloudflare

### DNS Record Reference

| Type | Name | Target | Proxy |
|------|------|--------|-------|
| **CNAME** | `@` (root) | `your-project.pages.dev` | ✅ Proxied |
| **CNAME** | `www` | `your-project.pages.dev` | ✅ Proxied |
| **CNAME** | `app` (subdomain) | `your-project.pages.dev` | ✅ Proxied |

> Cloudflare uses "CNAME flattening" for root domains — just add CNAME with `@`.

---

## Part 3: Automatic Deployments

Once connected, every push to your default branch triggers a new deployment:

- **Production branch:** `main` or `master` → deploys to production URL
- **Preview branches:** Other branches → get unique preview URLs

### Branch Deploy Settings

1. Pages project → **Settings** → **Builds & deployments**
2. Configure which branches trigger builds
3. Set production branch

---

## Part 4: Migrating from Other Hosts

### From Lovable/Vercel/Netlify

1. Export code to GitHub (Lovable: connect repo in settings)
2. Create new Cloudflare Pages project
3. Point custom domain to Pages
4. Old host's DNS records become inactive once nameservers change

### From WordPress on Shared Hosting

1. Convert to static (optional) or keep as-is
2. For static: use a WordPress static generator
3. Push to GitHub → deploy to Pages
4. Cancel old hosting once confirmed working

---

## Part 5: Troubleshooting

### Site shows "Page not found" after deploy

- Check build output directory matches what Cloudflare expects
- Verify build command runs successfully in logs
- For Next.js static export: ensure `output: 'export'` in `next.config.js`

### Domain not working after nameserver change

- DNS propagation takes time — check with `dig yourdomain.com`
- Verify both nameservers are correctly set at registrar
- Check Cloudflare shows domain as "Active"

### Build fails

- Check build logs in Cloudflare Pages
- Verify `node_modules` isn't committed (Cloudflare installs dependencies)
- Set correct Node version in environment variables

### HTTPS not working

- Cloudflare handles SSL automatically
- Wait a few minutes for certificate provisioning
- Check SSL/TLS settings in Cloudflare (use "Full" or "Full (strict)")

---

## Quick Reference

```bash
# Typical workflow:
1. Push code to GitHub
2. Cloudflare auto-deploys
3. Check *.pages.dev URL
4. (Optional) Connect custom domain

# Manual redeploy:
Pages project → Deployments → Retry deployment
```

---

## Related

- [Cloudflare Pages Docs](https://developers.cloudflare.com/pages)
- [Cloudflare DNS Docs](https://developers.cloudflare.com/dns)
- [Framework Guides](https://developers.cloudflare.com/pages/framework-guides)
