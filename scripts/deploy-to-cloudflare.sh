#!/bin/bash
# deploy-to-cloudflare.sh - Autonomous Cloudflare Pages deployment
# Usage: ./deploy-to-cloudflare.sh <site-dir> <project-name> <domain>

set -e

SITE_DIR=$1
PROJECT_NAME=$2
DOMAIN=$3

if [ -z "$SITE_DIR" ] || [ -z "$PROJECT_NAME" ] || [ -z "$DOMAIN" ]; then
    echo "Usage: $0 <site-dir> <project-name> <domain>"
    echo "Example: $0 ./mva-sites/commercialtrucklaw commercialtrucklaw commercialtrucklaw.com"
    exit 1
fi

# Load credentials
CF_TOKEN=$(cat ~/.config/cloudflare/credentials.json | jq -r '.api_token')
CF_ACCOUNT="1c06f86d52670b83af5704d99f40dfb5"

echo "🚀 Deploying $PROJECT_NAME to Cloudflare Pages..."

# Step 1: Build the site
echo "📦 Building site..."
cd "$SITE_DIR"
npm install --silent
npm run build

# Detect output directory
if [ -d "out" ]; then
    OUTPUT_DIR="out"
elif [ -d "dist" ]; then
    OUTPUT_DIR="dist"
elif [ -d ".next" ]; then
    OUTPUT_DIR=".next"
else
    echo "❌ Could not find build output directory"
    exit 1
fi

echo "✅ Build complete. Output: $OUTPUT_DIR"

# Step 2: Check if project exists, create if not
echo "🔍 Checking if Pages project exists..."
PROJECT_EXISTS=$(curl -s "https://api.cloudflare.com/client/v4/accounts/$CF_ACCOUNT/pages/projects/$PROJECT_NAME" \
    -H "Authorization: Bearer $CF_TOKEN" | jq -r '.success')

if [ "$PROJECT_EXISTS" != "true" ]; then
    echo "📝 Creating new Pages project: $PROJECT_NAME"
    curl -s -X POST "https://api.cloudflare.com/client/v4/accounts/$CF_ACCOUNT/pages/projects" \
        -H "Authorization: Bearer $CF_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"name\": \"$PROJECT_NAME\", \"production_branch\": \"main\"}" | jq '.success'
fi

# Step 3: Deploy
echo "🚀 Deploying to Pages..."
CLOUDFLARE_API_TOKEN=$CF_TOKEN npx wrangler pages deploy "./$OUTPUT_DIR" --project-name="$PROJECT_NAME" --commit-dirty=true

# Step 4: Add custom domain
echo "🌐 Adding custom domain: $DOMAIN"
curl -s -X POST "https://api.cloudflare.com/client/v4/accounts/$CF_ACCOUNT/pages/projects/$PROJECT_NAME/domains" \
    -H "Authorization: Bearer $CF_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"$DOMAIN\"}" | jq '.success'

# Also add www
curl -s -X POST "https://api.cloudflare.com/client/v4/accounts/$CF_ACCOUNT/pages/projects/$PROJECT_NAME/domains" \
    -H "Authorization: Bearer $CF_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"www.$DOMAIN\"}" | jq '.success'

# Step 5: Get zone ID for DNS
echo "🔧 Configuring DNS..."
ZONE_ID=$(curl -s "https://api.cloudflare.com/client/v4/zones?name=$DOMAIN" \
    -H "Authorization: Bearer $CF_TOKEN" | jq -r '.result[0].id')

if [ "$ZONE_ID" != "null" ] && [ -n "$ZONE_ID" ]; then
    # Delete existing A/CNAME records for @ and www
    for record_name in "$DOMAIN" "www.$DOMAIN"; do
        EXISTING=$(curl -s "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records?name=$record_name&type=A,CNAME" \
            -H "Authorization: Bearer $CF_TOKEN" | jq -r '.result[].id')
        for rid in $EXISTING; do
            curl -s -X DELETE "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records/$rid" \
                -H "Authorization: Bearer $CF_TOKEN" > /dev/null
        done
    done

    # Add CNAME for root
    curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
        -H "Authorization: Bearer $CF_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"type\": \"CNAME\", \"name\": \"@\", \"content\": \"$PROJECT_NAME.pages.dev\", \"proxied\": true}" | jq '.success'

    # Add CNAME for www
    curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
        -H "Authorization: Bearer $CF_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"type\": \"CNAME\", \"name\": \"www\", \"content\": \"$PROJECT_NAME.pages.dev\", \"proxied\": true}" | jq '.success'

    echo "✅ DNS configured!"
else
    echo "⚠️ Zone not found for $DOMAIN - DNS not configured"
fi

echo ""
echo "🎉 Deployment complete!"
echo "   Pages URL: https://$PROJECT_NAME.pages.dev"
echo "   Custom URL: https://$DOMAIN"
