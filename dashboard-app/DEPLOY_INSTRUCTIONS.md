# 🚀 Deploy Sierra Dashboard to Cloudflare

## Quick Deploy (5 minutes)

### Step 1: Get Cloudflare API Token

1. Go to: https://dash.cloudflare.com/profile/api-tokens
2. Click "Create Token"
3. Use template: **"Edit Cloudflare Workers"**
4. Or custom permissions: `Account.Cloudflare Pages (Edit)`
5. Copy the token

### Step 2: Get Account ID

1. Go to: https://dash.cloudflare.com/
2. Look at the URL: `https://dash.cloudflare.com/[YOUR_ACCOUNT_ID]/...`
3. Copy the Account ID (long string of characters)

### Step 3: Deploy

```bash
# Set credentials
export CLOUDFLARE_API_TOKEN='your-token-here'
export CLOUDFLARE_ACCOUNT_ID='your-account-id'

# Deploy
cd /home/ec2-user/clawd/dashboard-app
./deploy.sh
```

Your dashboard will be live at: **https://sierra-dashboard.pages.dev**

---

## Alternative: Direct Upload

If you prefer not to use the CLI:

1. Go to: https://dash.cloudflare.com/?to=/:account/pages
2. Click "Create a project" → "Direct Upload"
3. Name it: `sierra-dashboard`
4. Upload the `/home/ec2-user/clawd/dashboard-app` folder contents
5. Click Deploy

---

## Access Codes

The dashboard uses simple password auth:
- **Primary:** `sierra2026`
- **Alternate:** `kurios`

---

## 🔒 Recommended: Add Cloudflare Access

For production security, add Cloudflare Access (Zero Trust):

1. Go to: https://one.dash.cloudflare.com/
2. Access → Applications → Add application
3. Choose "Self-hosted"
4. Application URL: `sierra-dashboard.pages.dev`
5. Add policy (email, Google SSO, etc.)

This gives you:
- Email OTP login
- Google/GitHub/Okta SSO
- Audit logging
- No password in code

---

## Updating the Dashboard

To update data, edit `data.json` and redeploy:

```bash
# Edit the data
nano data.json

# Redeploy
./deploy.sh
```

Or use the Cloudflare dashboard to upload updated files.

---

## Files in this Package

```
dashboard-app/
├── index.html          # Main dashboard
├── app.js              # Dashboard logic
├── data.json           # Business data (edit this!)
├── calendar.json       # Calendar events
├── _headers            # Security headers
├── _redirects          # SPA routing
├── deploy.sh           # Deployment script
├── README.md           # Full documentation
└── DEPLOY_INSTRUCTIONS.md  # This file
```

---

## Custom Domain (Optional)

To use a custom domain like `dashboard.kuriosbrand.com`:

1. In Cloudflare Pages → Your project → Custom domains
2. Add domain: `dashboard.kuriosbrand.com`
3. Add DNS record in Cloudflare DNS (auto-prompted)

---

Built for Marko 🏔️
