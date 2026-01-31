#!/bin/bash
# Start PI Vendors Data Collection

PROJECT_DIR="/home/ec2-user/clawd/projects/pi-vendors"
LOG_FILE="$PROJECT_DIR/logs/coordinator_$(date +%Y%m%d).log"

echo "Starting PI Vendors Coordinator..."
echo "Logs: $LOG_FILE"

cd $PROJECT_DIR
nohup python3 agents/coordinator.py >> "$LOG_FILE" 2>&1 &

echo "Started with PID: $!"
echo $! > "$PROJECT_DIR/coordinator.pid"
echo "Done. Check status with: $PROJECT_DIR/scripts/status.sh"
