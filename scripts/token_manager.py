#!/usr/bin/env python3
"""
Token Manager - Monitors and auto-refreshes API tokens/keys
Runs as cron job or daemon to prevent expiration issues
"""

import os
import json
import time
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import requests

CONFIG_DIR = Path.home() / ".config"
CLAWD_DIR = Path("/home/ec2-user/clawd")
LOG_FILE = CLAWD_DIR / "data" / "token-refresh.log"

# Token configurations
TOKENS = {
    "gcal": {
        "path": CONFIG_DIR / "gcal-pro" / "token.json",
        "type": "oauth2",
        "refresh_url": "https://oauth2.googleapis.com/token",
        "client_id_path": CONFIG_DIR / "gcal-pro" / "credentials.json",
        "check_interval_hours": 12,
    },
    "cloudflare": {
        "path": CONFIG_DIR / "cloudflare" / "credentials.json",
        "type": "api_key",
        "test_url": "https://api.cloudflare.com/client/v4/user/tokens/verify",
        "check_interval_hours": 24,
    },
    "notion": {
        "path": CONFIG_DIR / "notion" / "api_key",
        "type": "api_key",
        "test_url": "https://api.notion.com/v1/users/me",
        "check_interval_hours": 24,
    },
    "x_twitter": {
        "path": CONFIG_DIR / "x-api" / "credentials.json",
        "type": "oauth1",
        "check_interval_hours": 168,  # Weekly
    },
    "ghl": {
        "path": CONFIG_DIR / "ghl" / "credentials.json",
        "type": "api_key",
        "test_url": "https://services.leadconnectorhq.com/locations/",
        "check_interval_hours": 24,
    },
}

def log(msg):
    """Log to file and stdout"""
    timestamp = datetime.utcnow().isoformat()
    line = f"[{timestamp}] {msg}"
    print(line)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def check_token_exists(token_name, config):
    """Check if token file exists"""
    return config["path"].exists()

def check_oauth2_token(token_name, config):
    """Check and refresh OAuth2 token if needed"""
    if not config["path"].exists():
        log(f"⚠️ {token_name}: Token file missing!")
        return False, "missing"
    
    try:
        token_data = json.loads(config["path"].read_text())
        
        # Check if expired
        if "expiry" in token_data:
            expiry = datetime.fromisoformat(token_data["expiry"].replace("Z", "+00:00"))
            now = datetime.now(expiry.tzinfo)
            
            if expiry < now:
                log(f"⚠️ {token_name}: Token EXPIRED at {expiry}")
                return refresh_oauth2_token(token_name, config, token_data)
            elif expiry < now + timedelta(hours=1):
                log(f"🔄 {token_name}: Token expiring soon, refreshing...")
                return refresh_oauth2_token(token_name, config, token_data)
            else:
                log(f"✅ {token_name}: Valid until {expiry}")
                return True, "valid"
        
        return True, "no_expiry"
        
    except Exception as e:
        log(f"❌ {token_name}: Error checking token - {e}")
        return False, str(e)

def refresh_oauth2_token(token_name, config, token_data):
    """Refresh OAuth2 token using refresh_token"""
    try:
        if "refresh_token" not in token_data:
            log(f"❌ {token_name}: No refresh_token available!")
            return False, "no_refresh_token"
        
        # Load client credentials
        creds_path = config.get("client_id_path")
        if creds_path and creds_path.exists():
            creds = json.loads(creds_path.read_text())
            if "installed" in creds:
                creds = creds["installed"]
            elif "web" in creds:
                creds = creds["web"]
        else:
            log(f"❌ {token_name}: Client credentials not found!")
            return False, "no_client_creds"
        
        # Refresh the token
        response = requests.post(config["refresh_url"], data={
            "client_id": creds["client_id"],
            "client_secret": creds["client_secret"],
            "refresh_token": token_data["refresh_token"],
            "grant_type": "refresh_token",
        })
        
        if response.status_code == 200:
            new_token = response.json()
            
            # Update token data
            token_data["access_token"] = new_token["access_token"]
            if "expires_in" in new_token:
                expiry = datetime.utcnow() + timedelta(seconds=new_token["expires_in"])
                token_data["expiry"] = expiry.isoformat() + "Z"
            if "refresh_token" in new_token:
                token_data["refresh_token"] = new_token["refresh_token"]
            
            # Save updated token
            config["path"].write_text(json.dumps(token_data, indent=2))
            log(f"✅ {token_name}: Token refreshed successfully!")
            return True, "refreshed"
        else:
            log(f"❌ {token_name}: Refresh failed - {response.status_code} {response.text}")
            return False, f"refresh_failed_{response.status_code}"
            
    except Exception as e:
        log(f"❌ {token_name}: Refresh error - {e}")
        return False, str(e)

def check_api_key(token_name, config):
    """Test API key validity"""
    if not config["path"].exists():
        log(f"⚠️ {token_name}: Credentials file missing!")
        return False, "missing"
    
    try:
        # Read credentials
        content = config["path"].read_text().strip()
        if config["path"].suffix == ".json":
            creds = json.loads(content)
            api_key = creds.get("api_token") or creds.get("api_key") or creds.get("token")
        else:
            api_key = content
        
        if not api_key:
            log(f"⚠️ {token_name}: No API key found in file!")
            return False, "no_key"
        
        # Test the API
        if "test_url" in config:
            headers = {"Authorization": f"Bearer {api_key}"}
            if "notion" in token_name:
                headers["Notion-Version"] = "2022-06-28"
            
            response = requests.get(config["test_url"], headers=headers, timeout=10)
            
            if response.status_code == 200:
                log(f"✅ {token_name}: API key valid")
                return True, "valid"
            elif response.status_code == 401:
                log(f"❌ {token_name}: API key INVALID/EXPIRED!")
                return False, "invalid"
            else:
                log(f"⚠️ {token_name}: API returned {response.status_code}")
                return True, f"status_{response.status_code}"
        
        return True, "unchecked"
        
    except Exception as e:
        log(f"❌ {token_name}: Check error - {e}")
        return False, str(e)

def send_alert(token_name, status):
    """Send alert about token issue (via Telegram/Discord)"""
    # Could integrate with clawdbot messaging here
    log(f"🚨 ALERT: {token_name} needs attention - {status}")

def check_all_tokens():
    """Check all configured tokens"""
    log("=" * 50)
    log("Token Manager - Starting check")
    log("=" * 50)
    
    results = {}
    
    for token_name, config in TOKENS.items():
        if config["type"] == "oauth2":
            success, status = check_oauth2_token(token_name, config)
        else:
            success, status = check_api_key(token_name, config)
        
        results[token_name] = {"success": success, "status": status}
        
        if not success and status not in ["missing"]:
            send_alert(token_name, status)
    
    # Save results
    results_file = CLAWD_DIR / "data" / "token-status.json"
    results_file.write_text(json.dumps({
        "checked_at": datetime.utcnow().isoformat(),
        "results": results
    }, indent=2))
    
    log("=" * 50)
    log("Token Manager - Check complete")
    log("=" * 50)
    
    return results

if __name__ == "__main__":
    check_all_tokens()
