#!/usr/bin/env python3
"""Upload files to Google Drive using OAuth token from gcal-pro"""
import json
import os
import sys
import requests

TOKEN_PATH = os.path.expanduser("~/.config/gcal-pro/token.json")
KURIOS_FOLDER_ID = "1igaRyFYqMF0rAKR3rVcRWa747j9hroUQ"

def get_access_token():
    """Get or refresh access token"""
    with open(TOKEN_PATH) as f:
        token_data = json.load(f)
    
    # Try to refresh token
    refresh_resp = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": token_data["client_id"],
        "client_secret": token_data["client_secret"],
        "refresh_token": token_data["refresh_token"],
        "grant_type": "refresh_token"
    })
    
    if refresh_resp.status_code == 200:
        new_token = refresh_resp.json()["access_token"]
        token_data["token"] = new_token
        with open(TOKEN_PATH, "w") as f:
            json.dump(token_data, f, indent=2)
        return new_token
    
    return token_data["token"]

def upload_file(file_path, folder_id=KURIOS_FOLDER_ID, mime_type=None):
    """Upload a file to Google Drive"""
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    filename = os.path.basename(file_path)
    
    # Auto-detect mime type
    if mime_type is None:
        if file_path.endswith(".csv"):
            mime_type = "text/csv"
        elif file_path.endswith(".md"):
            mime_type = "text/markdown"
        else:
            mime_type = "application/octet-stream"
    
    # Create file metadata
    metadata = {
        "name": filename,
        "parents": [folder_id]
    }
    
    # Multipart upload
    with open(file_path, "rb") as f:
        files = {
            "metadata": ("metadata", json.dumps(metadata), "application/json"),
            "file": (filename, f, mime_type)
        }
        
        resp = requests.post(
            "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
            headers=headers,
            files=files
        )
    
    if resp.status_code == 200:
        file_data = resp.json()
        print(f"✅ Uploaded: {filename}")
        print(f"   File ID: {file_data['id']}")
        print(f"   Link: https://drive.google.com/file/d/{file_data['id']}/view")
        return file_data
    else:
        print(f"❌ Failed to upload: {resp.status_code}")
        print(resp.text)
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: gdrive_upload.py <file_path> [folder_id]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    folder_id = sys.argv[2] if len(sys.argv) > 2 else KURIOS_FOLDER_ID
    
    upload_file(file_path, folder_id)
