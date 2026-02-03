#!/usr/bin/env python3
"""
De-Neuralyzer Session Analyzer
Analyzes session transcripts to extract and recover context after compaction.
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict
import argparse

SESSIONS_DIR = Path.home() / ".clawdbot/agents/main/sessions"
OUTPUT_DIR = Path(__file__).parent

class SessionAnalyzer:
    """Analyzes session transcripts for context recovery."""
    
    def __init__(self, session_path: Path = None):
        self.sessions_dir = SESSIONS_DIR
        self.session_path = session_path
        
    def find_main_session(self) -> Path:
        """Find the largest active (non-deleted) session file."""
        sessions = []
        for f in self.sessions_dir.glob("*.jsonl"):
            if ".deleted." in f.name or f.name.endswith(".lock"):
                continue
            sessions.append((f.stat().st_size, f.stat().st_mtime, f))
        
        if not sessions:
            raise FileNotFoundError("No active session files found")
        
        # Return the largest session (main session is usually biggest)
        sessions.sort(reverse=True)
        return sessions[0][2]
    
    def load_session(self, path: Path) -> List[Dict]:
        """Load all entries from a session file."""
        entries = []
        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    entries.append(json.loads(line))
        return entries
    
    def find_compaction_events(self, entries: List[Dict]) -> List[Dict]:
        """Find all compaction events in the session."""
        return [e for e in entries if e.get('type') == 'compaction']
    
    def get_recent_compaction(self, entries: List[Dict]) -> Optional[Dict]:
        """Get the most recent compaction event."""
        compactions = self.find_compaction_events(entries)
        if not compactions:
            return None
        return max(compactions, key=lambda x: x.get('timestamp', ''))
    
    def extract_messages(self, entries: List[Dict], since_entry_id: str = None) -> List[Dict]:
        """Extract user and assistant messages, optionally since a specific entry."""
        messages = []
        found_start = since_entry_id is None
        
        for entry in entries:
            if not found_start:
                if entry.get('id') == since_entry_id:
                    found_start = True
                continue
                
            if entry.get('type') == 'message':
                msg = entry.get('message', {})
                role = msg.get('role')
                if role in ('user', 'assistant'):
                    content = msg.get('content', [])
                    text_content = []
                    for item in content:
                        if isinstance(item, dict):
                            if item.get('type') == 'text':
                                text_content.append(item.get('text', ''))
                            elif item.get('type') == 'toolCall':
                                text_content.append(f"[Tool: {item.get('name')}]")
                    
                    if text_content:
                        messages.append({
                            'timestamp': entry.get('timestamp'),
                            'role': role,
                            'text': '\n'.join(text_content)[:2000],  # Truncate long messages
                            'id': entry.get('id')
                        })
        return messages
    
    def extract_decisions(self, messages: List[Dict]) -> List[str]:
        """Extract key decisions from assistant messages."""
        decision_keywords = [
            'decided', 'will do', 'going to', 'plan is', 'approach:',
            'strategy:', 'solution:', 'next step', 'action item',
            'created', 'updated', 'modified', 'deployed', 'fixed'
        ]
        
        decisions = []
        for msg in messages:
            if msg['role'] != 'assistant':
                continue
            text_lower = msg['text'].lower()
            for keyword in decision_keywords:
                if keyword in text_lower:
                    # Extract the sentence containing the keyword
                    lines = msg['text'].split('\n')
                    for line in lines:
                        if keyword in line.lower() and len(line) > 20:
                            decisions.append({
                                'timestamp': msg['timestamp'],
                                'decision': line.strip()[:500]
                            })
                            break
                    break
        return decisions[-20:]  # Return last 20 decisions
    
    def extract_active_tasks(self, messages: List[Dict]) -> List[Dict]:
        """Extract tasks that appear to be in-progress."""
        task_indicators = [
            'working on', 'in progress', 'currently', 'now doing',
            'let me', "i'll", 'spawning', 'checking', 'analyzing'
        ]
        
        tasks = []
        for msg in messages[-50:]:  # Check last 50 messages
            if msg['role'] != 'assistant':
                continue
            text_lower = msg['text'].lower()
            for indicator in task_indicators:
                if indicator in text_lower:
                    # Get first line or first 200 chars
                    summary = msg['text'].split('\n')[0][:200]
                    tasks.append({
                        'timestamp': msg['timestamp'],
                        'task': summary,
                        'indicator': indicator
                    })
                    break
        
        # De-duplicate and return most recent
        seen = set()
        unique_tasks = []
        for task in reversed(tasks):
            key = task['task'][:50]
            if key not in seen:
                seen.add(key)
                unique_tasks.append(task)
        
        return list(reversed(unique_tasks[-10:]))
    
    def extract_user_requests(self, messages: List[Dict], last_n: int = 10) -> List[Dict]:
        """Extract recent user requests."""
        user_msgs = [m for m in messages if m['role'] == 'user']
        return user_msgs[-last_n:]
    
    def extract_files_touched(self, entries: List[Dict]) -> Dict[str, List[str]]:
        """Extract files that were read or modified from compaction details."""
        files = {'read': set(), 'modified': set()}
        
        for entry in entries:
            if entry.get('type') == 'compaction':
                details = entry.get('details', {})
                files['read'].update(details.get('readFiles', []))
                files['modified'].update(details.get('modifiedFiles', []))
            
            # Also check tool results for file operations
            if entry.get('type') == 'message':
                msg = entry.get('message', {})
                if msg.get('role') == 'toolResult':
                    tool_name = msg.get('toolName', '')
                    if tool_name in ('Read', 'Edit', 'Write'):
                        # Could extract file paths from tool calls
                        pass
        
        return {k: list(v)[-30:] for k, v in files.items()}  # Limit to 30 each
    
    def get_conversation_summary(self, messages: List[Dict], last_n: int = 20) -> str:
        """Create a summary of recent conversation."""
        recent = messages[-last_n:]
        summary_lines = []
        
        for msg in recent:
            role = "👤 USER" if msg['role'] == 'user' else "🤖 ASSISTANT"
            text = msg['text'][:300]
            if len(msg['text']) > 300:
                text += "..."
            summary_lines.append(f"[{msg['timestamp'][:19]}] {role}:\n{text}\n")
        
        return '\n'.join(summary_lines)
    
    def generate_context_recovery(self, entries: List[Dict] = None) -> Dict:
        """Generate full context recovery data."""
        if entries is None:
            path = self.session_path or self.find_main_session()
            entries = self.load_session(path)
        
        # Find recent compaction
        recent_compaction = self.get_recent_compaction(entries)
        
        # Get messages since compaction (or all if no compaction)
        since_id = recent_compaction.get('firstKeptEntryId') if recent_compaction else None
        messages = self.extract_messages(entries, since_id)
        
        # Extract key context
        context = {
            'generated_at': datetime.utcnow().isoformat() + 'Z',
            'session_file': str(self.session_path or self.find_main_session()),
            'compaction': {
                'last_compaction': recent_compaction.get('timestamp') if recent_compaction else None,
                'tokens_before': recent_compaction.get('tokensBefore') if recent_compaction else None,
                'total_compactions': len(self.find_compaction_events(entries)),
            },
            'recent_user_requests': self.extract_user_requests(messages, 10),
            'active_tasks': self.extract_active_tasks(messages),
            'key_decisions': self.extract_decisions(messages),
            'files_touched': self.extract_files_touched(entries),
            'conversation_summary': self.get_conversation_summary(messages, 15),
            'message_count': len(messages),
            'messages_since_compaction': len(messages),
        }
        
        return context
    
    def detect_compaction_happened(self, entries: List[Dict]) -> bool:
        """Check if a compaction recently happened (last hour)."""
        compactions = self.find_compaction_events(entries)
        if not compactions:
            return False
        
        recent = max(compactions, key=lambda x: x.get('timestamp', ''))
        try:
            ts = datetime.fromisoformat(recent['timestamp'].rstrip('Z'))
            return (datetime.utcnow() - ts) < timedelta(hours=1)
        except:
            return False


def main():
    parser = argparse.ArgumentParser(description='De-Neuralyzer Session Analyzer')
    parser.add_argument('--session', type=str, help='Path to specific session file')
    parser.add_argument('--output', type=str, default=str(OUTPUT_DIR / 'current-context.json'),
                       help='Output path for context JSON')
    parser.add_argument('--detect', action='store_true', help='Just detect if compaction happened')
    parser.add_argument('--summary', action='store_true', help='Print conversation summary only')
    args = parser.parse_args()
    
    analyzer = SessionAnalyzer(Path(args.session) if args.session else None)
    
    try:
        path = Path(args.session) if args.session else analyzer.find_main_session()
        entries = analyzer.load_session(path)
        
        if args.detect:
            if analyzer.detect_compaction_happened(entries):
                print("COMPACTION_DETECTED")
                sys.exit(1)
            else:
                print("NO_RECENT_COMPACTION")
                sys.exit(0)
        
        context = analyzer.generate_context_recovery(entries)
        
        if args.summary:
            print(context['conversation_summary'])
            return
        
        # Write context to file
        with open(args.output, 'w') as f:
            json.dump(context, f, indent=2)
        
        print(f"✅ Context extracted to {args.output}")
        print(f"   Messages analyzed: {context['message_count']}")
        print(f"   Total compactions: {context['compaction']['total_compactions']}")
        print(f"   Active tasks: {len(context['active_tasks'])}")
        print(f"   Recent requests: {len(context['recent_user_requests'])}")
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
