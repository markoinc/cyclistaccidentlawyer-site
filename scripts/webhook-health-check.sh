#!/bin/bash

WEBHOOK_URL="https://webhook.kuriosbrand.com/health"
SLACK_WEBHOOK_URL="https://hooks.slack.com/services/placeholder" # We'll use the bot instead
SLACK_CHANNEL="C0ACS689MT4"  # #mark-sierra

# Check health
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$WEBHOOK_URL")

if [ "$RESPONSE" != "200" ]; then
    echo "[$(date)] ❌ Webhook DOWN! Response: $RESPONSE"
    
    # Try to restart
    pm2 restart lead-webhook 2>/dev/null
    sleep 5
    
    # Check again
    RETRY=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$WEBHOOK_URL")
    
    if [ "$RETRY" != "200" ]; then
        echo "[$(date)] ❌ Still DOWN after restart!"
        # Would send Slack alert here
    else
        echo "[$(date)] ✅ Recovered after restart"
    fi
else
    echo "[$(date)] ✅ Webhook healthy"
fi
