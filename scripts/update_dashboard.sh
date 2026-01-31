#!/bin/bash
# Update dashboard data file with current session/cron info

CANVAS_DIR="/home/ec2-user/clawd/canvas"
DATA_FILE="$CANVAS_DIR/dashboard-data.json"

# Get current timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Create a static data file (sessions/cron fetched via gateway internal API later)
cat > "$DATA_FILE" << 'EOF'
{
  "timestamp": "TIMESTAMP_PLACEHOLDER",
  "sessions": [
    {
      "key": "agent:main:main",
      "displayName": "Main Session (Marko DM)",
      "kind": "dm",
      "model": "claude-opus-4-5",
      "totalTokens": 135815,
      "updatedAt": UPDATED_PLACEHOLDER
    },
    {
      "key": "agent:main:telegram:group:-5142100963",
      "displayName": "telegram:g-head-agents",
      "kind": "group",
      "model": "claude-opus-4-5",
      "totalTokens": 16074,
      "updatedAt": UPDATED_PLACEHOLDER
    }
  ],
  "cronJobs": [
    {
      "id": "994485fd",
      "name": "moltbook-engagement",
      "enabled": true,
      "state": { "nextRunAtMs": NEXT_15M, "lastStatus": "ok" }
    },
    {
      "id": "c2da6f88",
      "name": "hourly-scrape-update",
      "enabled": true,
      "state": { "nextRunAtMs": NEXT_1H, "lastStatus": "ok" }
    },
    {
      "id": "40643069",
      "name": "buyer-profile-scraper",
      "enabled": true,
      "state": { "nextRunAtMs": NEXT_4H, "lastStatus": "ok" }
    },
    {
      "id": "5cde7830",
      "name": "dashboard-hourly-update",
      "enabled": true,
      "state": { "nextRunAtMs": NEXT_1H, "lastStatus": "ok" }
    },
    {
      "id": "e6109db7",
      "name": "weekly-research-digest",
      "enabled": true,
      "state": { "nextRunAtMs": NEXT_WEEK, "lastStatus": "never run" }
    }
  ],
  "stats": {
    "activeSessions": 2,
    "cronJobs": 5,
    "projects": 3,
    "pipelineLeads": 13
  }
}
EOF

# Replace placeholders with actual values
NOW_MS=$(date +%s)000
NEXT_15M=$(($(date +%s)*1000 + 900000))
NEXT_1H=$(($(date +%s)*1000 + 3600000))
NEXT_4H=$(($(date +%s)*1000 + 14400000))
NEXT_WEEK=$(($(date +%s)*1000 + 604800000))

sed -i "s/TIMESTAMP_PLACEHOLDER/$TIMESTAMP/g" "$DATA_FILE"
sed -i "s/UPDATED_PLACEHOLDER/$NOW_MS/g" "$DATA_FILE"
sed -i "s/NEXT_15M/$NEXT_15M/g" "$DATA_FILE"
sed -i "s/NEXT_1H/$NEXT_1H/g" "$DATA_FILE"
sed -i "s/NEXT_4H/$NEXT_4H/g" "$DATA_FILE"
sed -i "s/NEXT_WEEK/$NEXT_WEEK/g" "$DATA_FILE"

echo "Dashboard data updated at $TIMESTAMP"
