# SOP: Google Drive Integration

## Overview
Access Google Drive via API using OAuth tokens from gcal-pro. Used for managing shared folders, downloading files, and organizing business documents.

**Authenticated Account:** sierra@kuriosbrand.com

---

## 🔍 Prerequisites Check (DO THIS FIRST)

Before starting, verify you have everything needed.

### 1. Required Software
```bash
# Check if curl is installed
curl --version
# Expected: curl 7.x.x or 8.x.x

# Check if jq is installed (for JSON parsing)
jq --version
# Expected: jq-1.6 or higher

# If jq is missing, install it:
# Amazon Linux/RHEL: sudo yum install jq
# Ubuntu/Debian: sudo apt install jq
# macOS: brew install jq

# Check if Python3 is installed (for Python examples)
python3 --version
# Expected: Python 3.8+

# Check if requests library is installed
python3 -c "import requests; print('requests installed')"
# If missing: pip3 install requests
```

### 2. Verify Token File Exists
```bash
# Check token file exists
ls -la ~/.config/gcal-pro/token.json

# Expected output (something like):
# -rw------- 1 ec2-user ec2-user 1234 Feb 12 10:00 /home/ec2-user/.config/gcal-pro/token.json

# If file doesn't exist, you need to set up gcal-pro first
# See: /home/ec2-user/clawd/sops/google-calendar-setup.md
```

### 3. Verify Token Has Drive Scope
```bash
# Read and display your token scopes
cat ~/.config/gcal-pro/token.json | jq -r '.scope'

# You MUST see these scopes (among others):
# https://www.googleapis.com/auth/drive
# OR
# https://www.googleapis.com/auth/drive.file

# If you don't see drive scope, the token won't work for Drive API!
```

### 4. Test Your Access (Quick Validation)
```bash
# Set the token variable
TOKEN=$(cat ~/.config/gcal-pro/token.json | jq -r '.access_token')

# Test API access
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/about?fields=user" | jq

# ✅ EXPECTED SUCCESS RESPONSE:
# {
#   "user": {
#     "kind": "drive#user",
#     "displayName": "Sierra",
#     "emailAddress": "sierra@kuriosbrand.com",
#     "me": true
#   }
# }

# ❌ IF YOU SEE THIS - TOKEN IS EXPIRED:
# {
#   "error": {
#     "code": 401,
#     "message": "Request had invalid authentication credentials.",
#     "status": "UNAUTHENTICATED"
#   }
# }
# --> Go to Section 1.3 to refresh your token
```

---

## 1. Authentication

### 1.1 Token Location
```
~/.config/gcal-pro/token.json
```

The gcal-pro OAuth token has Google Drive scope, so we reuse it for Drive API calls.

### 1.2 Setting Up Your Token Variable
```bash
# ALWAYS run this at the start of your session:
export TOKEN=$(cat ~/.config/gcal-pro/token.json | jq -r '.access_token')

# Verify it's set:
echo $TOKEN
# Should output a long string starting with "ya29." (access tokens always start with ya29)
```

### 1.3 How to Know If Token Is Expired

Tokens expire after **1 hour**. Check expiry time:
```bash
# Check when token expires
cat ~/.config/gcal-pro/token.json | jq -r '.expiry'
# Example output: 2026-02-12T15:30:00Z

# Compare to current time
date -u +"%Y-%m-%dT%H:%M:%SZ"
# If current time > expiry time, you need to refresh
```

### 1.4 Refresh Token Flow

**⚠️ IMPORTANT:** Client ID and Client Secret are stored in the gcal-pro config:
```bash
# Find your client credentials
cat ~/.config/gcal-pro/credentials.json | jq
# This contains client_id and client_secret
```

**Refresh the token:**
```bash
# Load credentials
CLIENT_ID=$(cat ~/.config/gcal-pro/credentials.json | jq -r '.installed.client_id // .web.client_id')
CLIENT_SECRET=$(cat ~/.config/gcal-pro/credentials.json | jq -r '.installed.client_secret // .web.client_secret')
REFRESH_TOKEN=$(cat ~/.config/gcal-pro/token.json | jq -r '.refresh_token')

# Request new access token
RESPONSE=$(curl -s -X POST "https://oauth2.googleapis.com/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=$CLIENT_ID" \
  -d "client_secret=$CLIENT_SECRET" \
  -d "refresh_token=$REFRESH_TOKEN" \
  -d "grant_type=refresh_token")

# View response
echo "$RESPONSE" | jq

# ✅ SUCCESS RESPONSE:
# {
#   "access_token": "ya29.a0AfH6SMBx...",
#   "expires_in": 3599,
#   "scope": "https://www.googleapis.com/auth/drive ...",
#   "token_type": "Bearer"
# }

# ❌ ERROR RESPONSE (invalid refresh token):
# {
#   "error": "invalid_grant",
#   "error_description": "Token has been expired or revoked."
# }
# --> You need to re-authenticate via gcal-pro setup
```

**Update the token file:**
```bash
# Merge new access token with existing file (keeps refresh_token)
NEW_ACCESS_TOKEN=$(echo "$RESPONSE" | jq -r '.access_token')
NEW_EXPIRY=$(date -u -d "+1 hour" +"%Y-%m-%dT%H:%M:%SZ")  # Linux
# For macOS: NEW_EXPIRY=$(date -u -v+1H +"%Y-%m-%dT%H:%M:%SZ")

# Update token file
jq --arg at "$NEW_ACCESS_TOKEN" --arg exp "$NEW_EXPIRY" \
  '.access_token = $at | .expiry = $exp' \
  ~/.config/gcal-pro/token.json > /tmp/token.tmp && \
  mv /tmp/token.tmp ~/.config/gcal-pro/token.json

# Update your session variable
export TOKEN=$(cat ~/.config/gcal-pro/token.json | jq -r '.access_token')
echo "Token refreshed successfully!"
```

---

## 2. Key Folders

### Kurios Business Folders
| Folder | ID | Purpose |
|--------|-----|---------|
| Kurios Automated Business | `1igaRyFYqMF0rAKR3rVcRWa747j9hroUQ` | Main business folder |
| MVA Carlos & Mark Partnership | `1qshu4wTkayK-3C_h8nPEy_YWtWoaPAUX` | Partnership docs |

### Quick Access Variables
```bash
# Set these for easy access:
export KURIOS_FOLDER="1igaRyFYqMF0rAKR3rVcRWa747j9hroUQ"
export MVA_FOLDER="1qshu4wTkayK-3C_h8nPEy_YWtWoaPAUX"
```

---

## 3. Common Operations

### 3.1 List Files in Folder

**Basic command:**
```bash
# Replace FOLDER_ID with actual ID (e.g., $KURIOS_FOLDER)
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files?q='$KURIOS_FOLDER'+in+parents&fields=files(id,name,mimeType,modifiedTime)" | jq
```

**✅ SUCCESS RESPONSE:**
```json
{
  "files": [
    {
      "id": "1abc123def456...",
      "name": "Q1 2026 Report.pdf",
      "mimeType": "application/pdf",
      "modifiedTime": "2026-02-10T14:30:00.000Z"
    },
    {
      "id": "1xyz789ghi012...",
      "name": "Client Contracts",
      "mimeType": "application/vnd.google-apps.folder",
      "modifiedTime": "2026-02-08T09:15:00.000Z"
    }
  ]
}
```

**❌ COMMON ERRORS:**
```json
// Empty folder or wrong ID:
{ "files": [] }

// Invalid folder ID:
{
  "error": {
    "code": 404,
    "message": "File not found: invalid_id"
  }
}
```

**Pagination (for folders with >100 files):**
```bash
# First request
RESPONSE=$(curl -s -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files?q='$KURIOS_FOLDER'+in+parents&pageSize=100&fields=nextPageToken,files(id,name)")

# Get next page token
NEXT_PAGE=$(echo "$RESPONSE" | jq -r '.nextPageToken')

# If nextPageToken exists, fetch next page:
if [ "$NEXT_PAGE" != "null" ]; then
  curl -s -H "Authorization: Bearer $TOKEN" \
    "https://www.googleapis.com/drive/v3/files?q='$KURIOS_FOLDER'+in+parents&pageSize=100&pageToken=$NEXT_PAGE&fields=nextPageToken,files(id,name)" | jq
fi
```

### 3.2 Search for Files

**Search by name (anywhere):**
```bash
SEARCH_TERM="contract"
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files?q=name+contains+'$SEARCH_TERM'&fields=files(id,name,mimeType,parents)" | jq
```

**Search in specific folder:**
```bash
SEARCH_TERM="invoice"
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files?q='$KURIOS_FOLDER'+in+parents+and+name+contains+'$SEARCH_TERM'&fields=files(id,name,mimeType)" | jq
```

**Search by file type:**
```bash
# Find all Google Docs
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files?q=mimeType='application/vnd.google-apps.document'&fields=files(id,name)" | jq

# Find all PDFs
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files?q=mimeType='application/pdf'&fields=files(id,name)" | jq
```

**Search modified recently:**
```bash
# Files modified in last 7 days
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files?q=modifiedTime>'$(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%S)'&fields=files(id,name,modifiedTime)" | jq
```

### 3.3 Download File

**Step 1: Get the file ID** (from listing or searching)
```bash
# Example file ID from a search result
FILE_ID="1abc123def456ghi789"
```

**Step 2a: Download regular file (PDF, image, etc.):**
```bash
# Download to current directory
curl -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files/$FILE_ID?alt=media" \
  -o "downloaded_file.pdf"

# Verify download
ls -la downloaded_file.pdf
# Should show file size > 0

# Check file type
file downloaded_file.pdf
# Expected: "downloaded_file.pdf: PDF document, version 1.4"
```

**Step 2b: Export Google Doc/Sheet (can't download directly):**
```bash
# Export Google Doc as PDF
DOC_ID="1googleDocId..."
curl -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files/$DOC_ID/export?mimeType=application/pdf" \
  -o "document.pdf"

# Export Google Doc as Word
curl -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files/$DOC_ID/export?mimeType=application/vnd.openxmlformats-officedocument.wordprocessingml.document" \
  -o "document.docx"

# Export Google Sheet as CSV
SHEET_ID="1googleSheetId..."
curl -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files/$SHEET_ID/export?mimeType=text/csv" \
  -o "spreadsheet.csv"

# Export Google Sheet as Excel
curl -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files/$SHEET_ID/export?mimeType=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" \
  -o "spreadsheet.xlsx"
```

**⚠️ GOTCHA:** If you try to download a Google Doc with `?alt=media`, you'll get an error:
```json
{
  "error": {
    "code": 403,
    "message": "Export only supported for Google Docs Editors files.",
    "errors": [{"reason": "fileNotDownloadable"}]
  }
}
```
**Solution:** Use `/export` endpoint instead of `?alt=media` for Google Workspace files.

### 3.4 Upload File

**Simple upload (no metadata):**
```bash
# Upload a file - it goes to root of "My Drive"
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/pdf" \
  --data-binary @"/path/to/local/file.pdf" \
  "https://www.googleapis.com/upload/drive/v3/files?uploadType=media"

# ✅ SUCCESS RESPONSE:
# {
#   "kind": "drive#file",
#   "id": "1newFileId...",
#   "name": "file.pdf",
#   "mimeType": "application/pdf"
# }
```

**Upload to specific folder with name:**
```bash
# Create metadata JSON
METADATA='{"name": "My Report.pdf", "parents": ["'$KURIOS_FOLDER'"]}'

# Upload with multipart
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -F "metadata=$METADATA;type=application/json;charset=UTF-8" \
  -F "file=@/path/to/local/report.pdf;type=application/pdf" \
  "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart"

# ✅ SUCCESS RESPONSE:
# {
#   "kind": "drive#file",
#   "id": "1newFileId...",
#   "name": "My Report.pdf",
#   "mimeType": "application/pdf"
# }
```

**Verification - confirm file was uploaded:**
```bash
# Get the new file ID from the response
NEW_FILE_ID="1newFileId..."

# Verify it exists
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files/$NEW_FILE_ID?fields=id,name,parents,size,createdTime" | jq

# Should show:
# {
#   "id": "1newFileId...",
#   "name": "My Report.pdf",
#   "parents": ["1igaRyFYqMF0rAKR3rVcRWa747j9hroUQ"],
#   "size": "102400",
#   "createdTime": "2026-02-12T10:30:00.000Z"
# }
```

### 3.5 Create Folder

```bash
# Create folder in Kurios folder
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "February 2026 Reports",
    "mimeType": "application/vnd.google-apps.folder",
    "parents": ["'$KURIOS_FOLDER'"]
  }' \
  "https://www.googleapis.com/drive/v3/files"

# ✅ SUCCESS RESPONSE:
# {
#   "kind": "drive#file",
#   "id": "1newFolderId...",
#   "name": "February 2026 Reports",
#   "mimeType": "application/vnd.google-apps.folder"
# }

# Save the new folder ID for later use:
NEW_FOLDER_ID="1newFolderId..."
```

### 3.6 Move File

```bash
FILE_ID="1fileToMove..."
OLD_FOLDER_ID="1originalFolder..."
NEW_FOLDER_ID="1destinationFolder..."

curl -X PATCH \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}' \
  "https://www.googleapis.com/drive/v3/files/$FILE_ID?addParents=$NEW_FOLDER_ID&removeParents=$OLD_FOLDER_ID"

# ✅ SUCCESS RESPONSE shows file with new parent:
# {
#   "kind": "drive#file",
#   "id": "1fileToMove...",
#   "name": "somefile.pdf",
#   "mimeType": "application/pdf"
# }

# Verify move worked
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files/$FILE_ID?fields=id,name,parents" | jq
# Should show new parent ID
```

### 3.7 Rename File

```bash
FILE_ID="1fileToRename..."

curl -X PATCH \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "New Filename.pdf"}' \
  "https://www.googleapis.com/drive/v3/files/$FILE_ID"

# ✅ SUCCESS RESPONSE:
# {
#   "kind": "drive#file",
#   "id": "1fileToRename...",
#   "name": "New Filename.pdf"
# }
```

### 3.8 Delete File (Move to Trash)

```bash
FILE_ID="1fileToDelete..."

# Move to trash (recoverable for 30 days)
curl -X PATCH \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"trashed": true}' \
  "https://www.googleapis.com/drive/v3/files/$FILE_ID"

# ✅ SUCCESS RESPONSE shows trashed: true
# {
#   "kind": "drive#file",
#   "id": "1fileToDelete...",
#   "trashed": true
# }

# Permanently delete (IRREVERSIBLE!):
curl -X DELETE \
  -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files/$FILE_ID"

# Success returns empty response with HTTP 204
```

### 3.9 Get File Metadata

```bash
FILE_ID="1someFile..."

# Get detailed metadata
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files/$FILE_ID?fields=id,name,mimeType,size,createdTime,modifiedTime,parents,webViewLink,owners,permissions" | jq

# ✅ RESPONSE:
# {
#   "id": "1someFile...",
#   "name": "Document.pdf",
#   "mimeType": "application/pdf",
#   "size": "1048576",
#   "createdTime": "2026-01-15T10:00:00.000Z",
#   "modifiedTime": "2026-02-10T14:30:00.000Z",
#   "parents": ["1igaRyFYqMF0rAKR3rVcRWa747j9hroUQ"],
#   "webViewLink": "https://drive.google.com/file/d/1someFile.../view?usp=drivesdk",
#   "owners": [{"emailAddress": "sierra@kuriosbrand.com"}]
# }
```

---

## 4. Batch Operations

### 4.1 Batch API Overview

Google Drive supports batch requests to combine multiple API calls into one HTTP request. This is crucial for:
- Staying under rate limits
- Improving performance (fewer round trips)
- Operations on multiple files

### 4.2 Batch Request Example

```bash
# Create a batch request to get metadata for 3 files
BATCH_BOUNDARY="batch_boundary_string"

curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: multipart/mixed; boundary=$BATCH_BOUNDARY" \
  --data-binary @- \
  "https://www.googleapis.com/batch/drive/v3" << EOF
--$BATCH_BOUNDARY
Content-Type: application/http
Content-ID: <item1>

GET /drive/v3/files/FILE_ID_1?fields=id,name

--$BATCH_BOUNDARY
Content-Type: application/http
Content-ID: <item2>

GET /drive/v3/files/FILE_ID_2?fields=id,name

--$BATCH_BOUNDARY
Content-Type: application/http
Content-ID: <item3>

GET /drive/v3/files/FILE_ID_3?fields=id,name

--$BATCH_BOUNDARY--
EOF
```

### 4.3 Batch Update Multiple Files

```bash
# Move multiple files to trash in one request
BATCH_BOUNDARY="batch_trash_files"

curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: multipart/mixed; boundary=$BATCH_BOUNDARY" \
  --data-binary @- \
  "https://www.googleapis.com/batch/drive/v3" << EOF
--$BATCH_BOUNDARY
Content-Type: application/http
Content-ID: <trash1>

PATCH /drive/v3/files/FILE_ID_1
Content-Type: application/json

{"trashed": true}

--$BATCH_BOUNDARY
Content-Type: application/http
Content-ID: <trash2>

PATCH /drive/v3/files/FILE_ID_2
Content-Type: application/json

{"trashed": true}

--$BATCH_BOUNDARY--
EOF
```

### 4.4 Python Batch Helper

```python
#!/usr/bin/env python3
"""Batch operations helper for Google Drive"""

import json
import requests

def get_token():
    with open('/home/ec2-user/.config/gcal-pro/token.json') as f:
        return json.load(f)['access_token']

def batch_get_files(file_ids):
    """Get metadata for multiple files in one request."""
    token = get_token()
    boundary = "batch_get_files"
    
    body_parts = []
    for i, file_id in enumerate(file_ids):
        body_parts.append(f"""--{boundary}
Content-Type: application/http
Content-ID: <item{i}>

GET /drive/v3/files/{file_id}?fields=id,name,mimeType,size
""")
    
    body = "\n".join(body_parts) + f"\n--{boundary}--"
    
    response = requests.post(
        "https://www.googleapis.com/batch/drive/v3",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/mixed; boundary={boundary}"
        },
        data=body
    )
    return response.text

def batch_move_files(file_ids, target_folder_id, source_folder_id=None):
    """Move multiple files to a folder in one request."""
    token = get_token()
    boundary = "batch_move"
    
    body_parts = []
    for i, file_id in enumerate(file_ids):
        params = f"addParents={target_folder_id}"
        if source_folder_id:
            params += f"&removeParents={source_folder_id}"
        
        body_parts.append(f"""--{boundary}
Content-Type: application/http
Content-ID: <move{i}>

PATCH /drive/v3/files/{file_id}?{params}
Content-Type: application/json

{{}}
""")
    
    body = "\n".join(body_parts) + f"\n--{boundary}--"
    
    response = requests.post(
        "https://www.googleapis.com/batch/drive/v3",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/mixed; boundary={boundary}"
        },
        data=body
    )
    return response.text

# Example usage:
if __name__ == "__main__":
    # Get metadata for multiple files
    file_ids = ["1abc...", "1def...", "1ghi..."]
    result = batch_get_files(file_ids)
    print(result)
```

---

## 5. Rate Limiting & Best Practices

### 5.1 Google Drive API Quotas

| Quota Type | Limit | Reset |
|------------|-------|-------|
| Queries per day | 1,000,000,000 | Daily at midnight PT |
| Queries per 100 seconds per user | 1,000 | Rolling window |
| Queries per 100 seconds | 10,000 | Rolling window |

**⚠️ Per-user limit (1,000/100s = 10/second) is what you'll hit most often.**

### 5.2 Rate Limit Error

When you hit rate limits, you'll see:
```json
{
  "error": {
    "code": 429,
    "message": "Rate Limit Exceeded",
    "errors": [{
      "domain": "usageLimits",
      "reason": "rateLimitExceeded"
    }]
  }
}
```

### 5.3 Exponential Backoff Implementation

```bash
#!/bin/bash
# Retry with exponential backoff

make_request() {
    local url="$1"
    local max_retries=5
    local retry=0
    local wait_time=1
    
    while [ $retry -lt $max_retries ]; do
        response=$(curl -s -w "\n%{http_code}" -H "Authorization: Bearer $TOKEN" "$url")
        http_code=$(echo "$response" | tail -n1)
        body=$(echo "$response" | sed '$d')
        
        if [ "$http_code" = "200" ]; then
            echo "$body"
            return 0
        elif [ "$http_code" = "429" ]; then
            echo "Rate limited. Waiting ${wait_time}s..." >&2
            sleep $wait_time
            wait_time=$((wait_time * 2))  # Exponential backoff
            retry=$((retry + 1))
        else
            echo "Error: HTTP $http_code" >&2
            echo "$body" >&2
            return 1
        fi
    done
    
    echo "Max retries exceeded" >&2
    return 1
}

# Usage:
make_request "https://www.googleapis.com/drive/v3/files?q='$KURIOS_FOLDER'+in+parents"
```

### 5.4 Python Rate Limit Handler

```python
import time
import requests

def make_request_with_retry(url, headers, max_retries=5):
    """Make API request with exponential backoff on rate limits."""
    wait_time = 1
    
    for attempt in range(max_retries):
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print(f"Rate limited. Waiting {wait_time}s...")
            time.sleep(wait_time)
            wait_time *= 2  # Exponential backoff
        elif response.status_code == 401:
            raise Exception("Token expired - refresh required")
        else:
            raise Exception(f"API error: {response.status_code} - {response.text}")
    
    raise Exception("Max retries exceeded")
```

### 5.5 Best Practices

1. **Use batch requests** - Combine multiple operations (see Section 4)
2. **Use fields parameter** - Only request data you need
   ```bash
   # Bad: returns all fields
   ?q='folder'+in+parents
   
   # Good: returns only what you need
   ?q='folder'+in+parents&fields=files(id,name)
   ```
3. **Cache responses** - Don't re-fetch unchanged data
4. **Use pageSize wisely** - Default is 100, max is 1000
5. **Implement backoff** - Always handle 429 errors gracefully

---

## 6. MIME Types Reference

### Google Workspace Types
| Type | MIME Type |
|------|-----------|
| Google Doc | `application/vnd.google-apps.document` |
| Google Sheet | `application/vnd.google-apps.spreadsheet` |
| Google Slide | `application/vnd.google-apps.presentation` |
| Google Form | `application/vnd.google-apps.form` |
| Google Drawing | `application/vnd.google-apps.drawing` |
| Folder | `application/vnd.google-apps.folder` |

### Export Formats
| From | To | MIME Type |
|------|-----|-----------|
| Doc | PDF | `application/pdf` |
| Doc | DOCX | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` |
| Doc | Plain Text | `text/plain` |
| Doc | HTML | `text/html` |
| Sheet | CSV | `text/csv` |
| Sheet | XLSX | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` |
| Sheet | PDF | `application/pdf` |
| Slide | PDF | `application/pdf` |
| Slide | PPTX | `application/vnd.openxmlformats-officedocument.presentationml.presentation` |
| Drawing | PNG | `image/png` |
| Drawing | SVG | `image/svg+xml` |

---

## 7. Python Helper Script (Full Version)

Save this to `/home/ec2-user/clawd/scripts/gdrive_helper.py`:

```python
#!/usr/bin/env python3
"""
Google Drive helper functions with error handling and token refresh.
Location: /home/ec2-user/clawd/scripts/gdrive_helper.py

Usage:
    python3 gdrive_helper.py list FOLDER_ID
    python3 gdrive_helper.py search "keyword"
    python3 gdrive_helper.py download FILE_ID output.pdf
    python3 gdrive_helper.py upload /path/to/file.pdf FOLDER_ID
"""

import json
import os
import sys
import time
import requests
from datetime import datetime, timezone

# Configuration
TOKEN_PATH = os.path.expanduser('~/.config/gcal-pro/token.json')
CREDS_PATH = os.path.expanduser('~/.config/gcal-pro/credentials.json')
API_BASE = 'https://www.googleapis.com/drive/v3'

# Known folders
KURIOS_FOLDER = '1igaRyFYqMF0rAKR3rVcRWa747j9hroUQ'
MVA_FOLDER = '1qshu4wTkayK-3C_h8nPEy_YWtWoaPAUX'


class DriveClient:
    def __init__(self):
        self.token = None
        self.load_token()
    
    def load_token(self):
        """Load access token from config file."""
        with open(TOKEN_PATH) as f:
            data = json.load(f)
            self.token = data['access_token']
            self.refresh_token = data.get('refresh_token')
            self.expiry = data.get('expiry')
    
    def is_token_expired(self):
        """Check if access token is expired."""
        if not self.expiry:
            return False
        expiry_time = datetime.fromisoformat(self.expiry.replace('Z', '+00:00'))
        return datetime.now(timezone.utc) >= expiry_time
    
    def refresh_access_token(self):
        """Refresh the access token using refresh token."""
        print("Refreshing access token...")
        
        with open(CREDS_PATH) as f:
            creds = json.load(f)
        
        # Handle both installed and web app credentials
        if 'installed' in creds:
            client_id = creds['installed']['client_id']
            client_secret = creds['installed']['client_secret']
        else:
            client_id = creds['web']['client_id']
            client_secret = creds['web']['client_secret']
        
        response = requests.post(
            'https://oauth2.googleapis.com/token',
            data={
                'client_id': client_id,
                'client_secret': client_secret,
                'refresh_token': self.refresh_token,
                'grant_type': 'refresh_token'
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Token refresh failed: {response.text}")
        
        new_token_data = response.json()
        self.token = new_token_data['access_token']
        
        # Update token file
        with open(TOKEN_PATH) as f:
            token_data = json.load(f)
        
        token_data['access_token'] = self.token
        token_data['expiry'] = (
            datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        )
        
        with open(TOKEN_PATH, 'w') as f:
            json.dump(token_data, f, indent=2)
        
        print("Token refreshed successfully!")
    
    def _headers(self):
        """Get authorization headers."""
        return {'Authorization': f'Bearer {self.token}'}
    
    def _request(self, method, url, **kwargs):
        """Make API request with automatic retry and token refresh."""
        max_retries = 5
        wait_time = 1
        
        for attempt in range(max_retries):
            # Check token expiry before request
            if self.is_token_expired():
                self.refresh_access_token()
            
            response = requests.request(
                method, url, 
                headers=self._headers(),
                **kwargs
            )
            
            if response.status_code == 200:
                return response
            elif response.status_code == 401:
                print("Token expired, refreshing...")
                self.refresh_access_token()
            elif response.status_code == 429:
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
                wait_time *= 2
            elif response.status_code == 204:
                return response  # No content (e.g., delete)
            else:
                error_msg = f"API Error {response.status_code}: {response.text}"
                raise Exception(error_msg)
        
        raise Exception("Max retries exceeded")
    
    def list_folder(self, folder_id, page_size=100):
        """List all files in a folder (handles pagination)."""
        all_files = []
        page_token = None
        
        while True:
            params = {
                'q': f"'{folder_id}' in parents and trashed=false",
                'fields': 'nextPageToken,files(id,name,mimeType,size,modifiedTime)',
                'pageSize': page_size
            }
            if page_token:
                params['pageToken'] = page_token
            
            response = self._request('GET', f'{API_BASE}/files', params=params)
            data = response.json()
            
            all_files.extend(data.get('files', []))
            page_token = data.get('nextPageToken')
            
            if not page_token:
                break
        
        return all_files
    
    def search(self, query, folder_id=None):
        """Search for files by name."""
        q = f"name contains '{query}' and trashed=false"
        if folder_id:
            q = f"'{folder_id}' in parents and " + q
        
        params = {
            'q': q,
            'fields': 'files(id,name,mimeType,size,modifiedTime,parents)'
        }
        
        response = self._request('GET', f'{API_BASE}/files', params=params)
        return response.json().get('files', [])
    
    def download(self, file_id, output_path):
        """Download a file."""
        # First get file metadata to check type
        meta_response = self._request(
            'GET', 
            f'{API_BASE}/files/{file_id}',
            params={'fields': 'mimeType,name'}
        )
        metadata = meta_response.json()
        mime_type = metadata.get('mimeType', '')
        
        # Google Workspace files need export
        if mime_type.startswith('application/vnd.google-apps'):
            export_map = {
                'application/vnd.google-apps.document': 'application/pdf',
                'application/vnd.google-apps.spreadsheet': 'text/csv',
                'application/vnd.google-apps.presentation': 'application/pdf',
            }
            export_mime = export_map.get(mime_type, 'application/pdf')
            url = f'{API_BASE}/files/{file_id}/export'
            params = {'mimeType': export_mime}
        else:
            url = f'{API_BASE}/files/{file_id}'
            params = {'alt': 'media'}
        
        response = self._request('GET', url, params=params)
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"Downloaded: {output_path} ({len(response.content)} bytes)")
        return output_path
    
    def upload(self, local_path, folder_id, name=None):
        """Upload a file to a folder."""
        if name is None:
            name = os.path.basename(local_path)
        
        # Determine MIME type
        import mimetypes
        mime_type, _ = mimetypes.guess_type(local_path)
        if mime_type is None:
            mime_type = 'application/octet-stream'
        
        # Create metadata
        metadata = {
            'name': name,
            'parents': [folder_id]
        }
        
        with open(local_path, 'rb') as f:
            files = {
                'metadata': ('metadata', json.dumps(metadata), 'application/json'),
                'file': (name, f, mime_type)
            }
            
            # Manual multipart for better control
            response = requests.post(
                'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart',
                headers=self._headers(),
                files=files
            )
        
        if response.status_code != 200:
            raise Exception(f"Upload failed: {response.text}")
        
        result = response.json()
        print(f"Uploaded: {name} (ID: {result['id']})")
        return result
    
    def create_folder(self, name, parent_id):
        """Create a new folder."""
        metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }
        
        response = self._request(
            'POST',
            f'{API_BASE}/files',
            json=metadata
        )
        
        result = response.json()
        print(f"Created folder: {name} (ID: {result['id']})")
        return result
    
    def move(self, file_id, new_folder_id, old_folder_id=None):
        """Move a file to a different folder."""
        params = {'addParents': new_folder_id}
        if old_folder_id:
            params['removeParents'] = old_folder_id
        
        response = self._request(
            'PATCH',
            f'{API_BASE}/files/{file_id}',
            params=params,
            json={}
        )
        
        return response.json()
    
    def trash(self, file_id):
        """Move a file to trash."""
        response = self._request(
            'PATCH',
            f'{API_BASE}/files/{file_id}',
            json={'trashed': True}
        )
        print(f"Trashed file: {file_id}")
        return response.json()
    
    def get_metadata(self, file_id):
        """Get file metadata."""
        response = self._request(
            'GET',
            f'{API_BASE}/files/{file_id}',
            params={'fields': 'id,name,mimeType,size,createdTime,modifiedTime,parents,webViewLink'}
        )
        return response.json()


def main():
    """CLI interface."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    client = DriveClient()
    command = sys.argv[1]
    
    if command == 'list':
        folder_id = sys.argv[2] if len(sys.argv) > 2 else KURIOS_FOLDER
        files = client.list_folder(folder_id)
        for f in files:
            size = f.get('size', 'N/A')
            print(f"{f['name']:<50} {f['mimeType']:<40} {size:>10}")
    
    elif command == 'search':
        query = sys.argv[2]
        folder_id = sys.argv[3] if len(sys.argv) > 3 else None
        files = client.search(query, folder_id)
        for f in files:
            print(f"{f['id']}: {f['name']} ({f['mimeType']})")
    
    elif command == 'download':
        file_id = sys.argv[2]
        output = sys.argv[3] if len(sys.argv) > 3 else 'download'
        client.download(file_id, output)
    
    elif command == 'upload':
        local_path = sys.argv[2]
        folder_id = sys.argv[3] if len(sys.argv) > 3 else KURIOS_FOLDER
        client.upload(local_path, folder_id)
    
    elif command == 'mkdir':
        name = sys.argv[2]
        parent_id = sys.argv[3] if len(sys.argv) > 3 else KURIOS_FOLDER
        client.create_folder(name, parent_id)
    
    elif command == 'trash':
        file_id = sys.argv[2]
        client.trash(file_id)
    
    elif command == 'info':
        file_id = sys.argv[2]
        meta = client.get_metadata(file_id)
        print(json.dumps(meta, indent=2))
    
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()
```

---

## 8. Common Mistakes & Troubleshooting

### 8.1 Mistake: Using Wrong URL for Google Workspace Files

**❌ WRONG:**
```bash
# Trying to download a Google Doc directly
curl -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files/GOOGLE_DOC_ID?alt=media"
```
**Error:** `403 - Export only supported for Google Docs Editors files`

**✅ CORRECT:**
```bash
# Export Google Doc to PDF
curl -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files/GOOGLE_DOC_ID/export?mimeType=application/pdf"
```

### 8.2 Mistake: Forgetting URL Encoding in Queries

**❌ WRONG:**
```bash
# Spaces break the query
curl "https://www.googleapis.com/drive/v3/files?q=name contains 'my file'"
```

**✅ CORRECT:**
```bash
# Use + for spaces in query parameter
curl "https://www.googleapis.com/drive/v3/files?q=name+contains+'my+file'"

# Or use --data-urlencode
curl -G --data-urlencode "q=name contains 'my file'" \
  -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files"
```

### 8.3 Mistake: Not Handling Pagination

**❌ WRONG:**
```bash
# Only gets first 100 files
curl "https://www.googleapis.com/drive/v3/files?q='FOLDER'+in+parents"
```

**✅ CORRECT:**
```bash
# Check for nextPageToken and iterate (see Section 3.1)
```

### 8.4 Mistake: Expired Token

**Symptom:**
```json
{
  "error": {
    "code": 401,
    "message": "Request had invalid authentication credentials."
  }
}
```

**Fix:** Run token refresh (Section 1.4)

### 8.5 Mistake: Wrong Folder ID Format

**❌ WRONG:**
```bash
# Using URL instead of ID
FOLDER="https://drive.google.com/drive/folders/1abc123..."
```

**✅ CORRECT:**
```bash
# Just the ID portion
FOLDER="1abc123..."
```

**How to find folder ID:**
1. Open folder in Google Drive web
2. Look at URL: `https://drive.google.com/drive/folders/1abc123xyz...`
3. Copy just the ID part: `1abc123xyz...`

### 8.6 Mistake: Upload Without Specifying Folder

**❌ Result:** File goes to root of "My Drive" (hard to find)

**✅ Better:** Always specify `parents` in upload metadata

---

## 9. Debugging API Errors

### 9.1 Enable Verbose Output

```bash
# See full request/response
curl -v -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files"
```

### 9.2 Common Error Codes

| Code | Meaning | Debug Steps |
|------|---------|-------------|
| 400 | Bad Request | Check JSON syntax, query format |
| 401 | Unauthorized | Token expired/invalid - refresh it |
| 403 | Forbidden | No permission to access file/folder |
| 404 | Not Found | File deleted or wrong ID |
| 429 | Rate Limited | Wait and retry with backoff |
| 500 | Server Error | Google issue - retry later |

### 9.3 Debug 403 Forbidden

```bash
# Check what permissions you have
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files/FILE_ID?fields=permissions" | jq

# Check your authenticated user
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/about?fields=user" | jq

# Is file trashed?
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files/FILE_ID?fields=trashed" | jq
```

### 9.4 Debug Token Issues

```bash
# Check token validity
curl -s "https://oauth2.googleapis.com/tokeninfo?access_token=$TOKEN" | jq

# Expected valid response:
# {
#   "azp": "client-id...",
#   "aud": "client-id...",
#   "scope": "https://www.googleapis.com/auth/drive ...",
#   "exp": "1707750000",
#   "access_type": "offline"
# }

# Invalid token response:
# {
#   "error": "invalid_token",
#   "error_description": "Invalid Value"
# }
```

---

## 10. Verification Steps

### After Uploading a File
```bash
# 1. Check file exists
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files/$NEW_FILE_ID?fields=id,name,size,parents" | jq

# 2. Verify it's in the right folder
# parents should contain your target folder ID

# 3. Check file size matches local
ls -la /path/to/uploaded/file
# Compare with "size" in API response
```

### After Moving a File
```bash
# Verify new location
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files/$FILE_ID?fields=id,name,parents" | jq

# parents array should show new folder, not old
```

### After Deleting (Trashing)
```bash
# Verify in trash
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files/$FILE_ID?fields=id,name,trashed" | jq

# Should show: "trashed": true
```

### After Token Refresh
```bash
# Test with a simple API call
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/about?fields=user" | jq

# Should return user info, not error
```

---

## 11. Quick Reference Card

```bash
# === SETUP ===
export TOKEN=$(cat ~/.config/gcal-pro/token.json | jq -r '.access_token')
export KURIOS_FOLDER="1igaRyFYqMF0rAKR3rVcRWa747j9hroUQ"

# === TEST ACCESS ===
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/about?fields=user" | jq

# === LIST FOLDER ===
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files?q='$KURIOS_FOLDER'+in+parents&fields=files(id,name,mimeType)" | jq

# === SEARCH ===
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files?q=name+contains+'keyword'&fields=files(id,name)" | jq

# === DOWNLOAD FILE ===
curl -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files/FILE_ID?alt=media" -o output.pdf

# === EXPORT GOOGLE DOC ===
curl -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files/DOC_ID/export?mimeType=application/pdf" -o doc.pdf

# === UPLOAD FILE ===
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -F 'metadata={"name":"file.pdf","parents":["FOLDER_ID"]};type=application/json' \
  -F "file=@/path/to/file.pdf" \
  "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart"

# === CREATE FOLDER ===
curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"name":"New Folder","mimeType":"application/vnd.google-apps.folder","parents":["PARENT_ID"]}' \
  "https://www.googleapis.com/drive/v3/files"

# === TRASH FILE ===
curl -X PATCH -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"trashed":true}' "https://www.googleapis.com/drive/v3/files/FILE_ID"
```

---

## 12. Security Notes

- **Never commit tokens** to git (add to .gitignore)
- Token files should be `chmod 600`
- Use service accounts for production automations
- Rotate tokens periodically
- Audit file access via Drive audit logs (Admin console)

---

*Version 2.0 | Updated: 2026-02-12*
*For: Kurios Brand*
*Auth: Uses gcal-pro OAuth token with Drive scope*
*Account: sierra@kuriosbrand.com*
