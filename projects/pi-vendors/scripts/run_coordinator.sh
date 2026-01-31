#!/bin/bash
# Start the main coordinator (24/7 scraper orchestrator)

cd /home/ec2-user/clawd/projects/pi-vendors

# Load env
if [ -f /home/ec2-user/clawd/.env.local ]; then
    export $(cat /home/ec2-user/clawd/.env.local | grep -v '^#' | xargs)
fi

# Run coordinator
python3 agents/coordinator.py
