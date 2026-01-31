#!/usr/bin/env python3
"""
Sierra Dashboard API
Generates real-time dashboard data from Clawdbot state
"""

import json
import subprocess
import os
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

CANVAS_DIR = Path("/home/ec2-user/clawd/canvas")
MEMORY_FILE = Path("/home/ec2-user/clawd/MEMORY.md")

def get_sessions():
    """Get active sessions from clawdbot"""
    try:
        result = subprocess.run(
            ["clawdbot", "sessions", "list", "--json"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception as e:
        print(f"Error getting sessions: {e}")
    return {"sessions": []}

def get_cron_jobs():
    """Get cron jobs from clawdbot"""
    try:
        result = subprocess.run(
            ["clawdbot", "cron", "list", "--json"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception as e:
        print(f"Error getting cron: {e}")
    return {"jobs": []}

def generate_dashboard_json():
    """Generate dashboard data as JSON"""
    sessions = get_sessions()
    cron = get_cron_jobs()
    
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "sessions": sessions.get("sessions", []),
        "cronJobs": cron.get("jobs", []),
        "stats": {
            "activeSessions": len(sessions.get("sessions", [])),
            "cronJobs": len([j for j in cron.get("jobs", []) if j.get("enabled")]),
            "projects": 3,
            "pipelineLeads": 13
        }
    }

def update_dashboard_html():
    """Update the dashboard HTML with fresh data"""
    data = generate_dashboard_json()
    
    # Read current HTML
    html_path = CANVAS_DIR / "dashboard.html"
    if not html_path.exists():
        return
    
    html = html_path.read_text()
    
    # Update the embedded data
    sessions_json = json.dumps(data["sessions"], indent=8)
    cron_json = json.dumps(data["cronJobs"], indent=8)
    
    # Save data file for dynamic loading
    data_path = CANVAS_DIR / "dashboard-data.json"
    data_path.write_text(json.dumps(data, indent=2))
    
    print(f"Dashboard data updated at {data['timestamp']}")
    return data

class DashboardHandler(SimpleHTTPRequestHandler):
    """Custom handler for dashboard with CORS and API endpoints"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(CANVAS_DIR), **kwargs)
    
    def do_GET(self):
        if self.path == "/api/dashboard":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            data = generate_dashboard_json()
            self.wfile.write(json.dumps(data).encode())
        elif self.path == "/api/refresh":
            data = update_dashboard_html()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "data": data}).encode())
        else:
            super().do_GET()

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--serve", action="store_true", help="Start HTTP server")
    parser.add_argument("--port", type=int, default=8765, help="Server port")
    parser.add_argument("--update", action="store_true", help="Update dashboard data")
    args = parser.parse_args()
    
    if args.update:
        update_dashboard_html()
    elif args.serve:
        print(f"Starting dashboard server on port {args.port}...")
        server = HTTPServer(("0.0.0.0", args.port), DashboardHandler)
        server.serve_forever()
    else:
        # Just print data
        print(json.dumps(generate_dashboard_json(), indent=2))

if __name__ == "__main__":
    main()
