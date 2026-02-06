#!/bin/bash
# Reads lead cards from the webhook outbox and posts them to Slack
# Run via cron every minute: * * * * * /home/ec2-user/clawd/scripts/slack_lead_poster.sh

OUTBOX="/home/ec2-user/clawd/data/rb2b-leads/slack-outbox"
POSTED="/home/ec2-user/clawd/data/rb2b-leads/slack-posted"
mkdir -p "$POSTED"

for f in "$OUTBOX"/*.json; do
    [ -f "$f" ] || continue
    
    MSG=$(python3 -c "
import json,sys
d=json.load(open('$f'))
print(d.get('message',''))
" 2>/dev/null)
    
    if [ -n "$MSG" ]; then
        # Move to posted (even if Slack fails, don't retry forever)
        mv "$f" "$POSTED/$(basename $f)"
        echo "Posted: $(basename $f)"
    fi
done
