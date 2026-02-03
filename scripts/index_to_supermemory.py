#!/usr/bin/env python3
"""
Memory Indexer - Scans all files and adds to Supermemory
Run periodically to keep memory up to date
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

CLAWD_DIR = Path("/home/ec2-user/clawd")
INDEXED_LOG = CLAWD_DIR / "data" / "indexed_files.json"

# File patterns to index
PATTERNS = {
    "data": ["*.json", "*.md"],
    "memory": ["*.md"],
    "scripts": ["*.py", "*.sh"],
}

# Load already indexed files
def load_indexed():
    if INDEXED_LOG.exists():
        return json.loads(INDEXED_LOG.read_text())
    return {"files": {}, "last_run": None}

def save_indexed(data):
    INDEXED_LOG.parent.mkdir(parents=True, exist_ok=True)
    INDEXED_LOG.write_text(json.dumps(data, indent=2))

def get_file_hash(path):
    """Get mtime as simple hash"""
    return str(os.path.getmtime(path))

def should_index(path, indexed):
    """Check if file needs indexing"""
    path_str = str(path)
    current_hash = get_file_hash(path)
    if path_str not in indexed["files"]:
        return True
    return indexed["files"][path_str] != current_hash

def categorize_file(path):
    """Determine file category and metadata"""
    path_str = str(path)
    
    if "/data/books/" in path_str:
        return {"type": "book", "topic": "learning"}
    elif "/data/videos/" in path_str:
        return {"type": "video", "topic": "learning"}
    elif "/data/meta-ads/" in path_str:
        return {"type": "playbook", "topic": "meta-ads"}
    elif "/memory/projects/mva" in path_str:
        return {"type": "project", "topic": "mva-lead-gen"}
    elif "/scripts/" in path_str:
        return {"type": "script", "topic": "automation"}
    elif "/data/discovery/" in path_str:
        return {"type": "research", "topic": "business-intel"}
    elif "registry" in path_str or "pipeline" in path_str:
        return {"type": "crm", "topic": "sales"}
    else:
        return {"type": "document", "topic": "general"}

def add_to_supermemory(content, metadata, custom_id):
    """Add content to Supermemory via clawdbot"""
    # This would use the supermemory API
    # For now, print what would be added
    print(f"Would index: {custom_id}")
    print(f"  Metadata: {metadata}")
    print(f"  Content length: {len(content)} chars")
    return True

def main():
    print(f"Memory Indexer starting at {datetime.utcnow().isoformat()}")
    
    indexed = load_indexed()
    new_indexed = 0
    
    # Scan directories
    for subdir, patterns in PATTERNS.items():
        dir_path = CLAWD_DIR / subdir
        if not dir_path.exists():
            continue
            
        for pattern in patterns:
            for file_path in dir_path.rglob(pattern):
                if not file_path.is_file():
                    continue
                if file_path.stat().st_size > 100000:  # Skip files > 100KB
                    continue
                    
                if should_index(file_path, indexed):
                    try:
                        content = file_path.read_text(errors='ignore')
                        metadata = categorize_file(file_path)
                        custom_id = f"file-{file_path.stem}-{hash(str(file_path)) % 10000}"
                        
                        # Add to supermemory
                        add_to_supermemory(content, metadata, custom_id)
                        
                        # Mark as indexed
                        indexed["files"][str(file_path)] = get_file_hash(file_path)
                        new_indexed += 1
                        
                    except Exception as e:
                        print(f"Error indexing {file_path}: {e}")
    
    indexed["last_run"] = datetime.utcnow().isoformat()
    save_indexed(indexed)
    
    print(f"Indexed {new_indexed} new/updated files")
    print(f"Total tracked files: {len(indexed['files'])}")

if __name__ == "__main__":
    main()
