#!/bin/bash
# Stop PI Vendors Coordinator

echo "Stopping PI Vendors Coordinator..."
pkill -f "coordinator.py" && echo "✅ Stopped" || echo "⚠️ Not running"
rm -f /home/ec2-user/clawd/projects/pi-vendors/coordinator.pid
