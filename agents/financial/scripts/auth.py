#!/usr/bin/env python3
"""
Google OAuth handler for Ledger financial agent.
Uses the existing gcal-pro token which has spreadsheets scope.
"""

import json
import os
from pathlib import Path
from datetime import datetime
import requests

TOKEN_PATH = Path.home() / ".config" / "gcal-pro" / "token.json"


def load_token() -> dict:
    """Load the OAuth token from disk."""
    if not TOKEN_PATH.exists():
        raise FileNotFoundError(f"Token not found at {TOKEN_PATH}")
    
    with open(TOKEN_PATH) as f:
        return json.load(f)


def refresh_token_if_needed(token_data: dict) -> dict:
    """Refresh the token if it's expired."""
    expiry = token_data.get("expiry")
    if expiry:
        expiry_dt = datetime.fromisoformat(expiry.replace("Z", "+00:00"))
        if datetime.now(expiry_dt.tzinfo) >= expiry_dt:
            return refresh_token(token_data)
    return token_data


def refresh_token(token_data: dict) -> dict:
    """Refresh the OAuth token."""
    response = requests.post(
        token_data["token_uri"],
        data={
            "client_id": token_data["client_id"],
            "client_secret": token_data["client_secret"],
            "refresh_token": token_data["refresh_token"],
            "grant_type": "refresh_token",
        }
    )
    response.raise_for_status()
    
    new_token = response.json()
    token_data["token"] = new_token["access_token"]
    
    if "expires_in" in new_token:
        from datetime import timedelta
        expiry = datetime.utcnow() + timedelta(seconds=new_token["expires_in"])
        token_data["expiry"] = expiry.isoformat() + "Z"
    
    # Save updated token
    with open(TOKEN_PATH, "w") as f:
        json.dump(token_data, f, indent=2)
    
    return token_data


def get_access_token() -> str:
    """Get a valid access token, refreshing if necessary."""
    token_data = load_token()
    token_data = refresh_token_if_needed(token_data)
    return token_data["token"]


def get_headers() -> dict:
    """Get headers for Google API requests."""
    return {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json"
    }


if __name__ == "__main__":
    # Test token loading
    try:
        token = get_access_token()
        print(f"✓ Token loaded successfully")
        print(f"  Token preview: {token[:20]}...")
    except Exception as e:
        print(f"✗ Error: {e}")
