#!/bin/bash
# Deploy Sierra Dashboard to Cloudflare Pages

set -e

echo "🏔️ Sierra Dashboard Deployment"
echo "==============================="

# Check for API token
if [ -z "$CLOUDFLARE_API_TOKEN" ]; then
    echo ""
    echo "⚠️  CLOUDFLARE_API_TOKEN not set!"
    echo ""
    echo "To deploy, you need a Cloudflare API token:"
    echo "1. Go to: https://dash.cloudflare.com/profile/api-tokens"
    echo "2. Create token → Use 'Edit Cloudflare Workers' template"
    echo "3. Or create custom with: Account.Cloudflare Pages (Edit)"
    echo ""
    echo "Then run:"
    echo "  export CLOUDFLARE_API_TOKEN='your-token-here'"
    echo "  ./deploy.sh"
    echo ""
    exit 1
fi

# Check for account ID
if [ -z "$CLOUDFLARE_ACCOUNT_ID" ]; then
    echo ""
    echo "⚠️  CLOUDFLARE_ACCOUNT_ID not set!"
    echo ""
    echo "Find your Account ID in the Cloudflare dashboard URL:"
    echo "https://dash.cloudflare.com/[ACCOUNT_ID]/..."
    echo ""
    echo "Then run:"
    echo "  export CLOUDFLARE_ACCOUNT_ID='your-account-id'"
    echo "  ./deploy.sh"
    echo ""
    exit 1
fi

PROJECT_NAME="sierra-dashboard"

echo "📦 Deploying to Cloudflare Pages..."
echo "   Project: $PROJECT_NAME"
echo ""

# Deploy
wrangler pages deploy . --project-name "$PROJECT_NAME"

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Your dashboard should be live at:"
echo "   https://$PROJECT_NAME.pages.dev"
echo ""
echo "To set up Cloudflare Access (recommended):"
echo "1. Go to: https://one.dash.cloudflare.com/"
echo "2. Access → Applications → Add an application"
echo "3. Select 'Self-hosted' and use your Pages URL"
echo ""
