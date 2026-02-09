# SOP: Autonomous Cloudflare Pages Deployment

## Overview
Sierra can deploy new MVA sites to Cloudflare Pages without human intervention.

## Prerequisites
- Cloudflare API token: `~/.config/cloudflare/credentials.json`
- Account ID: `1c06f86d52670b83af5704d99f40dfb5`
- Domain already in Cloudflare (check zones list)

## Full Workflow

### 1. Build the Site
```bash
cd /path/to/site
npm run build
# Output usually in: out/, dist/, or .next/
```

### 2. Create Pages Project (if new)
```bash
curl -X POST "https://api.cloudflare.com/client/v4/accounts/1c06f86d52670b83af5704d99f40dfb5/pages/projects" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "site-name",
    "production_branch": "main"
  }'
```

### 3. Deploy to Pages
```bash
# Install wrangler if needed
npm install -g wrangler

# Deploy (uses CLOUDFLARE_API_TOKEN env var)
CLOUDFLARE_API_TOKEN=$CF_TOKEN npx wrangler pages deploy ./out --project-name=site-name
```

### 4. Add Custom Domain
```bash
curl -X POST "https://api.cloudflare.com/client/v4/accounts/1c06f86d52670b83af5704d99f40dfb5/pages/projects/site-name/domains" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "example.com"}'
```

### 5. Configure DNS
Get zone ID first:
```bash
curl -X GET "https://api.cloudflare.com/client/v4/zones?name=example.com" \
  -H "Authorization: Bearer $CF_TOKEN"
```

Add CNAME record:
```bash
curl -X POST "https://api.cloudflare.com/client/v4/zones/ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "CNAME",
    "name": "@",
    "content": "site-name.pages.dev",
    "proxied": true
  }'
```

For www:
```bash
curl -X POST "https://api.cloudflare.com/client/v4/zones/ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "CNAME",
    "name": "www",
    "content": "site-name.pages.dev",
    "proxied": true
  }'
```

## Available Domains (Already in Cloudflare)
- commercialtrucklaw.com
- cyclistaccidentlawyer.com
- deliverytruckaccident.com
- drunkdriveraccident.com
- hitandrunlawyer.net
- lyftcrashlaw.com
- motorcyclewrecklaw.com
- pedestrianaccidentlawyer.net
- ridesharelawyersnearme.com
- texastruckaccidents.net
- uberlawyersnearme.com

## Token Permissions
Current token has:
- ✅ Pages: Create/deploy projects
- ✅ Zones: List and manage DNS
- ✅ DNS: Create/update records

## Automation Script
See: `/home/ec2-user/clawd/scripts/deploy-to-cloudflare.sh`
