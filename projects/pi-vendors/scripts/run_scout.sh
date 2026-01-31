#!/bin/bash
# Start SCOUT Telegram bot

cd /home/ec2-user/clawd/projects/pi-vendors

# Load env
if [ -f /home/ec2-user/clawd/.env.local ]; then
    export $(cat /home/ec2-user/clawd/.env.local | grep -v '^#' | xargs)
fi

# Run bot
python3 agents/scout_bot.py
