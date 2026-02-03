#!/bin/bash
# Push updated dashboard data to GitHub

# Update the data first
/home/ec2-user/clawd/scripts/update_dashboard.sh

# Copy latest data to repo
cp /home/ec2-user/clawd/dashboard-app/data.json /tmp/goals-dashboard/data.json 2>/dev/null

# If repo doesn't exist, clone it
if [ ! -d "/tmp/goals-dashboard/.git" ]; then
    cd /tmp && rm -rf goals-dashboard
    git clone https://github.com/markoinc/goals-dashboard.git
fi

cd /tmp/goals-dashboard

# Copy fresh data
cp /home/ec2-user/clawd/dashboard-app/data.json ./data.json
cp /home/ec2-user/clawd/dashboard-app/calendar.json ./calendar.json 2>/dev/null

# Check if there are changes
if git diff --quiet; then
    echo "No changes to push"
    exit 0
fi

# Commit and push
git config user.name "Sierra Bot"
git config user.email "sierra@kuriosbrand.com"
git add data.json calendar.json
git commit -m "📊 Data update $(date -u +%Y-%m-%dT%H:%M:%SZ)"
git push origin main

echo "Dashboard data pushed at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
