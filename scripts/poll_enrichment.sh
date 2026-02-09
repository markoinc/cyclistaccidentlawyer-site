#!/bin/bash
# Poll BetterContact enrichment and save results

BATCH_ID="4e880444f4b7238ae64e"
API_KEY="15fbeb3e1bd54b77520d"
MAX_ATTEMPTS=30

echo "🔄 Polling enrichment batch: $BATCH_ID"

for i in $(seq 1 $MAX_ATTEMPTS); do
  RESULT=$(curl -s "https://app.bettercontact.rocks/api/v2/async/$BATCH_ID" \
    -H "X-API-Key: $API_KEY")
  
  STATUS=$(echo "$RESULT" | jq -r '.status // "unknown"')
  
  echo "[$i/$MAX_ATTEMPTS] Status: $STATUS"
  
  if [[ "$STATUS" == "completed" ]]; then
    echo "✅ ENRICHMENT COMPLETE!"
    echo "$RESULT" | jq . > /home/ec2-user/clawd/data/enrichment-4leads-result.json
    echo "Results saved to /home/ec2-user/clawd/data/enrichment-4leads-result.json"
    
    # Print summary
    echo ""
    echo "📊 ENRICHMENT RESULTS:"
    echo "$RESULT" | jq -r '.data[] | "• \(.first_name) \(.last_name): \(.email // "no email") | \(.phone // "no phone")"'
    exit 0
  fi
  
  if [[ "$STATUS" == "failed" ]]; then
    echo "❌ ENRICHMENT FAILED"
    echo "$RESULT" | jq .
    exit 1
  fi
  
  sleep 10
done

echo "⏰ Timeout after $MAX_ATTEMPTS attempts"
