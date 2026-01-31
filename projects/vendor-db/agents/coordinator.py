#!/usr/bin/env python3
"""
Coordinator Agent - Manages scraping swarm 24/7
"""

import json
import time
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_DIR = Path("/home/ec2-user/clawd/projects/vendor-db")
DATA_DIR = PROJECT_DIR / "data"
LOGS_DIR = PROJECT_DIR / "logs"
AGENTS_DIR = PROJECT_DIR / "agents"

DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Scrape schedule (hours between runs)
SCHEDULE = {
    "reddit_scraper": 4,     # Every 4 hours
    "vendor_scraper": 12,    # Every 12 hours
}

# Track last run times
state_file = PROJECT_DIR / "coordinator_state.json"

def load_state():
    if state_file.exists():
        with open(state_file) as f:
            return json.load(f)
    return {"last_runs": {}, "stats": {"total_runs": 0, "errors": 0}}

def save_state(state):
    with open(state_file, "w") as f:
        json.dump(state, f, indent=2)

def should_run(agent_name, state):
    """Check if agent should run based on schedule"""
    last_run = state["last_runs"].get(agent_name)
    if not last_run:
        return True
    
    hours_since = (datetime.utcnow() - datetime.fromisoformat(last_run)).total_seconds() / 3600
    return hours_since >= SCHEDULE.get(agent_name, 24)

def run_agent(agent_name):
    """Run a scraper agent"""
    script = AGENTS_DIR / f"{agent_name}.py"
    log_file = LOGS_DIR / f"{agent_name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.log"
    
    print(f"[{datetime.utcnow().isoformat()}] Running {agent_name}...")
    
    try:
        result = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True,
            text=True,
            timeout=3600  # 1 hour timeout
        )
        
        with open(log_file, "w") as f:
            f.write(f"=== {agent_name} run at {datetime.utcnow().isoformat()} ===\n\n")
            f.write("STDOUT:\n")
            f.write(result.stdout)
            f.write("\n\nSTDERR:\n")
            f.write(result.stderr)
            f.write(f"\n\nReturn code: {result.returncode}")
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print(f"  ERROR: {agent_name} timed out")
        return False
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def get_data_stats():
    """Get statistics on collected data"""
    stats = {
        "total_files": 0,
        "total_size_mb": 0,
        "reddit_posts": 0,
        "reddit_comments": 0,
        "vendors": 0
    }
    
    for f in DATA_DIR.glob("*.json"):
        stats["total_files"] += 1
        stats["total_size_mb"] += f.stat().st_size / (1024 * 1024)
        
        try:
            with open(f) as file:
                data = json.load(file)
                if "reddit_posts" in f.name:
                    stats["reddit_posts"] += len(data)
                elif "reddit_comments" in f.name:
                    stats["reddit_comments"] += len(data)
                elif "vendors" in f.name:
                    stats["vendors"] += len(data)
        except:
            pass
    
    return stats

def run_forever():
    """Main coordinator loop"""
    print("=" * 60)
    print("VENDOR DATABASE COORDINATOR - STARTING")
    print("=" * 60)
    print(f"Start time: {datetime.utcnow().isoformat()}")
    print(f"Data directory: {DATA_DIR}")
    print(f"Log directory: {LOGS_DIR}")
    print("")
    
    state = load_state()
    
    while True:
        try:
            for agent_name in SCHEDULE.keys():
                if should_run(agent_name, state):
                    success = run_agent(agent_name)
                    
                    state["last_runs"][agent_name] = datetime.utcnow().isoformat()
                    state["stats"]["total_runs"] += 1
                    if not success:
                        state["stats"]["errors"] += 1
                    
                    save_state(state)
            
            # Print stats every loop
            stats = get_data_stats()
            print(f"\n[{datetime.utcnow().isoformat()}] Data collected:")
            print(f"  Reddit posts: {stats['reddit_posts']}")
            print(f"  Reddit comments: {stats['reddit_comments']}")
            print(f"  Vendor profiles: {stats['vendors']}")
            print(f"  Total files: {stats['total_files']}")
            print(f"  Total size: {stats['total_size_mb']:.2f} MB")
            print(f"  Total runs: {state['stats']['total_runs']}")
            print(f"  Errors: {state['stats']['errors']}")
            
            # Sleep for 15 minutes before checking again
            print(f"\nSleeping for 15 minutes...")
            time.sleep(900)
            
        except KeyboardInterrupt:
            print("\nShutting down coordinator...")
            save_state(state)
            break
        except Exception as e:
            print(f"Coordinator error: {e}")
            time.sleep(60)

def run_once():
    """Run all agents once (for testing)"""
    print("Running all agents once...")
    
    for agent_name in SCHEDULE.keys():
        run_agent(agent_name)
    
    stats = get_data_stats()
    print(f"\nData collected:")
    print(f"  Reddit posts: {stats['reddit_posts']}")
    print(f"  Reddit comments: {stats['reddit_comments']}")
    print(f"  Vendor profiles: {stats['vendors']}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="Run once instead of forever")
    args = parser.parse_args()
    
    if args.once:
        run_once()
    else:
        run_forever()
