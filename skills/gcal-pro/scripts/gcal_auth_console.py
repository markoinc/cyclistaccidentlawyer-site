#!/usr/bin/env python3
"""Console-based OAuth for headless servers - Full scopes."""

import os
import json
from pathlib import Path
from google_auth_oauthlib.flow import Flow

CONFIG_DIR = Path.home() / ".config" / "gcal-pro"
CLIENT_SECRET_FILE = CONFIG_DIR / "client_secret.json"
TOKEN_FILE = CONFIG_DIR / "token.json"

# Full scopes: Calendar + Tasks + Drive + Docs
SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/tasks",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
]

def main():
    if not CLIENT_SECRET_FILE.exists():
        print(f"ERROR: {CLIENT_SECRET_FILE} not found")
        return
    
    # Create flow with localhost redirect (we'll extract code manually)
    flow = Flow.from_client_secrets_file(
        str(CLIENT_SECRET_FILE),
        scopes=SCOPES,
        redirect_uri='http://localhost:8080/'
    )
    
    # Get authorization URL
    auth_url, _ = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    
    print("\n" + "="*60)
    print("STEP 1: Open this URL in your browser:")
    print("="*60)
    print(f"\n{auth_url}\n")
    print("="*60)
    print("STEP 2: Sign in and authorize access")
    print("STEP 3: You'll be redirected to localhost (which won't load)")
    print("        Look at the URL bar - it will look like:")
    print("        http://localhost:8080/?code=XXXXX&scope=...")
    print("STEP 4: Copy JUST the code part (after code= and before &)")
    print("="*60)
    
    code = input("\nPaste the code here: ").strip()
    
    # Exchange code for credentials
    flow.fetch_token(code=code)
    creds = flow.credentials
    
    # Save token
    with open(TOKEN_FILE, "w") as f:
        f.write(creds.to_json())
    os.chmod(TOKEN_FILE, 0o600)
    
    print(f"\n[OK] Authentication successful!")
    print(f"Token saved to: {TOKEN_FILE}")
    print(f"Scopes: {', '.join(SCOPES)}")

if __name__ == "__main__":
    main()
