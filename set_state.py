#!/usr/bin/env python3
"""Simple status update tool for testing Star Office UI"""

import json
import os
import sys
from datetime import datetime

STATE_FILE = "/root/.openclaw/workspace/star-office-ui/state.json"

VALID_STATES = [
    "idle",
    "writing",
    "researching",
    "executing",
    "syncing",
    "error"
]

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "state": "idle",
        "detail": "On Standby...",
        "progress": 0,
        "updated_at": datetime.now().isoformat()
    }

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python set_state.py <state> [detail]")
        print(f"State Options: {', '.join(VALID_STATES)}")
        print("\nExample:")
        print("  python set_state.py idle")
        print("  python set_state.py researching \"Checking Godot MCP...\"")
        print("  python set_state.py writing \"Writing Hotspot Daily Template...\"")
        sys.exit(1)
    
    state_name = sys.argv[1]
    detail = sys.argv[2] if len(sys.argv) > 2 else ""
    
    if state_name not in VALID_STATES:
        print(f"Invalid status: {state_name}")
        print(f"Valid options: {', '.join(VALID_STATES)}")
        sys.exit(1)
    
    state = load_state()
    state["state"] = state_name
    state["detail"] = detail
    state["updated_at"] = datetime.now().isoformat()
    
    save_state(state)
    print(f"Status updated: {state_name} - {detail}")
