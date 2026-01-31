#!/bin/bash
# Check PI Vendors status

PROJECT_DIR="/home/ec2-user/clawd/projects/pi-vendors"

echo "=== PI VENDORS STATUS ==="
echo ""

# Check if coordinator is running
if pgrep -f "coordinator.py" > /dev/null; then
    echo "✅ Coordinator: RUNNING"
    pgrep -f "coordinator.py" | xargs ps -o pid,etime,cmd -p 2>/dev/null | tail -1
else
    echo "❌ Coordinator: NOT RUNNING"
fi

echo ""
echo "=== DATA COLLECTED ==="
if [ -d "$PROJECT_DIR/data/raw/reddit" ]; then
    POSTS=$(cat $PROJECT_DIR/data/raw/reddit/posts_*.json 2>/dev/null | python3 -c "import sys,json; data=[]; [data.extend(json.load(open(f))) for f in sys.argv[1:] if f]; print(len(data))" $PROJECT_DIR/data/raw/reddit/posts_*.json 2>/dev/null || echo "0")
    COMMENTS=$(cat $PROJECT_DIR/data/raw/reddit/comments_*.json 2>/dev/null | python3 -c "import sys,json; data=[]; [data.extend(json.load(open(f))) for f in sys.argv[1:] if f]; print(len(data))" $PROJECT_DIR/data/raw/reddit/comments_*.json 2>/dev/null || echo "0")
    FILES=$(ls -1 $PROJECT_DIR/data/raw/reddit/*.json 2>/dev/null | wc -l)
    SIZE=$(du -sh $PROJECT_DIR/data/raw/reddit 2>/dev/null | cut -f1)
    
    echo "Posts: $POSTS"
    echo "Comments: $COMMENTS"
    echo "Files: $FILES"
    echo "Size: $SIZE"
else
    echo "No data yet"
fi

echo ""
echo "=== COORDINATOR STATE ==="
if [ -f "$PROJECT_DIR/coordinator_state.json" ]; then
    cat "$PROJECT_DIR/coordinator_state.json" | python3 -m json.tool 2>/dev/null || cat "$PROJECT_DIR/coordinator_state.json"
else
    echo "No state file yet"
fi

echo ""
echo "=== RECENT LOGS ==="
LATEST_LOG=$(ls -t $PROJECT_DIR/logs/*.log 2>/dev/null | head -1)
if [ -n "$LATEST_LOG" ]; then
    echo "From: $LATEST_LOG"
    tail -20 "$LATEST_LOG"
else
    echo "No logs yet"
fi
