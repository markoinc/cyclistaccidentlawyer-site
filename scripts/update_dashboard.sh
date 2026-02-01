#!/bin/bash
# Update dashboard data from business registry + calendar

CANVAS_DIR="/home/ec2-user/clawd/canvas"
REGISTRY="/home/ec2-user/clawd/data/business-registry.json"
DATA_FILE="$CANVAS_DIR/dashboard-data.json"
CAL_FILE="$CANVAS_DIR/calendar-data.json"

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Fetch calendar
python3 /home/ec2-user/clawd/scripts/fetch_calendar.py 2>/dev/null > "$CAL_FILE"

# Copy registry to dashboard data with timestamp
if [ -f "$REGISTRY" ]; then
    jq --arg ts "$TIMESTAMP" '. + {timestamp: $ts}' "$REGISTRY" > "$DATA_FILE"
else
    echo '{"error": "Registry not found"}' > "$DATA_FILE"
fi

echo "Dashboard data updated at $TIMESTAMP"
