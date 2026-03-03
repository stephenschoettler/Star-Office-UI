#!/usr/bin/env python3
"""
Star's Office - Agent State Active Push Script

Usage:
1. Fill in below JOIN_KEY(One-time from Star join key)
2. Fill in AGENT_NAME(Name you want to display in the office)
3. Run:python office-agent-push.py
4. The script will automatically first join(First Run), then every 30s Push your current status to Star's office once
"""

import json
import os
import time
import sys
from datetime import datetime

# === Information you need to fill in ===
JOIN_KEY = ""   # Required: Your one-time join key
AGENT_NAME = "" # Required: Your name in the office
OFFICE_URL = "https://office.example.com"  # Star's office address (usually no need to change)

# === Push configuration ===
PUSH_INTERVAL_SECONDS = 15  # Push every few seconds (more real-time)
STATUS_ENDPOINT = "/status"
JOIN_ENDPOINT = "/join-agent"
PUSH_ENDPOINT = "/agent-push"

# Local State Storage (remember last join Obtained agentId)
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "office-agent-state.json")

# Prioritize local read OpenClaw Workspace status file (more fitting AGENTS.md Workflow)
# Support auto-discovery to reduce manual configuration cost for others.
DEFAULT_STATE_CANDIDATES = [
    "/root/.openclaw/workspace/star-office-ui/state.json",
    "/root/.openclaw/workspace/state.json",
    os.path.join(os.getcwd(), "state.json"),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json"),
]

# If local /status Authentication required, fill in here token(Or via environment variables OFFICE_LOCAL_STATUS_TOKEN)
LOCAL_STATUS_TOKEN = os.environ.get("OFFICE_LOCAL_STATUS_TOKEN", "")
LOCAL_STATUS_URL = os.environ.get("OFFICE_LOCAL_STATUS_URL", "http://127.0.0.1:18791/status")
# Optional: Directly specify local state file path (simplest solution: bypass /status Authentication)
LOCAL_STATE_FILE = os.environ.get("OFFICE_LOCAL_STATE_FILE", "")
VERBOSE = os.environ.get("OFFICE_VERBOSE", "0") in {"1", "true", "TRUE", "yes", "YES"}


def load_local_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "agentId": None,
        "joined": False,
        "joinKey": JOIN_KEY,
        "agentName": AGENT_NAME
    }


def save_local_state(data):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def normalize_state(s):
    """Compatible with different local state terms and map to office recognized states."""
    s = (s or "").strip().lower()
    if s in {"writing", "researching", "executing", "syncing", "error", "idle"}:
        return s
    if s in {"working", "busy", "write"}:
        return "writing"
    if s in {"run", "running", "execute", "exec"}:
        return "executing"
    if s in {"research", "search"}:
        return "researching"
    if s in {"sync"}:
        return "syncing"
    return "idle"


def map_detail_to_state(detail, fallback_state="idle"):
    """When only detail When using keywords to infer status (close to AGENTS.md Office area logic)."""
    d = (detail or "").lower()
    if any(k in d for k in ["Error", "error", "bug", "Exception", "Alert"]):
        return "error"
    if any(k in d for k in ["Sync", "sync", "Backup"]):
        return "syncing"
    if any(k in d for k in ["Research", "research", "Search", "Research"]):
        return "researching"
    if any(k in d for k in ["Execute", "run", "Advance", "Process task", "Working", "writing"]):
        return "writing"
    if any(k in d for k in ["Standby", "Break", "idle", "Complete", "done"]):
        return "idle"
    return fallback_state


def fetch_local_status():
    """Read local state:
    1) Priority state.json(Complies with AGENTS.md: Before task cut writing, switch after completion idle)
    2) Then try local HTTP /status
    3) Finally fallback idle
    """
    # 1) Read local state.json(Prioritize reading explicitly specified paths, then auto-discover)
    candidate_files = []
    if LOCAL_STATE_FILE:
        candidate_files.append(LOCAL_STATE_FILE)
    for fp in DEFAULT_STATE_CANDIDATES:
        if fp not in candidate_files:
            candidate_files.append(fp)

    for fp in candidate_files:
        try:
            if fp and os.path.exists(fp):
                with open(fp, "r", encoding="utf-8") as f:
                    data = json.load(f)

                    # Only Accept“Status File”Structure; avoid mistakenly office-agent-state.json(Cache only agentId) When Status Source
                    if not isinstance(data, dict):
                        continue
                    has_state = "state" in data
                    has_detail = "detail" in data
                    if (not has_state) and (not has_detail):
                        continue

                    state = normalize_state(data.get("state", "idle"))
                    detail = data.get("detail", "") or ""
                    # detail Fallback correction, ensure“Work/Break/Alert”Can correctly land in zone
                    state = map_detail_to_state(detail, fallback_state=state)
                    if VERBOSE:
                        print(f"[status-source:file] path={fp} state={state} detail={detail[:60]}")
                    return {"state": state, "detail": detail}
        except Exception:
            pass

    # 2) Try locally /status(May require authentication)
    try:
        import requests
        headers = {}
        if LOCAL_STATUS_TOKEN:
            headers["Authorization"] = f"Bearer {LOCAL_STATUS_TOKEN}"
        r = requests.get(LOCAL_STATUS_URL, headers=headers, timeout=5)
        if r.status_code == 200:
            data = r.json()
            state = normalize_state(data.get("state", "idle"))
            detail = data.get("detail", "") or ""
            state = map_detail_to_state(detail, fallback_state=state)
            if VERBOSE:
                print(f"[status-source:http] url={LOCAL_STATUS_URL} state={state} detail={detail[:60]}")
            return {"state": state, "detail": detail}
        # If 401, indicates need token
        if r.status_code == 401:
            return {"state": "idle", "detail": "Local/statusRequires authentication (401), please set OFFICE_LOCAL_STATUS_TOKEN"}
    except Exception:
        pass

    # 3) Default fallback
    if VERBOSE:
        print("[status-source:fallback] state=idle detail=On Standby")
    return {"state": "idle", "detail": "On Standby"}


def do_join(local):
    import requests
    payload = {
        "name": local.get("agentName", AGENT_NAME),
        "joinKey": local.get("joinKey", JOIN_KEY),
        "state": "idle",
        "detail": "Just Joined"
    }
    r = requests.post(f"{OFFICE_URL}{JOIN_ENDPOINT}", json=payload, timeout=10)
    if r.status_code in (200, 201):
        data = r.json()
        if data.get("ok"):
            local["joined"] = True
            local["agentId"] = data.get("agentId")
            save_local_state(local)
            print(f"✅ Joined Star's office,agentId={local['agentId']}")
            return True
    print(f"❌ Join failed:{r.text}")
    return False


def do_push(local, status_data):
    import requests
    payload = {
        "agentId": local.get("agentId"),
        "joinKey": local.get("joinKey", JOIN_KEY),
        "state": status_data.get("state", "idle"),
        "detail": status_data.get("detail", ""),
        "name": local.get("agentName", AGENT_NAME)
    }
    r = requests.post(f"{OFFICE_URL}{PUSH_ENDPOINT}", json=payload, timeout=10)
    if r.status_code in (200, 201):
        data = r.json()
        if data.get("ok"):
            area = data.get("area", "breakroom")
            print(f"✅ Status synced, current area={area}")
            return True

    # 403/404: Deny/Remove → Stop push
    if r.status_code in (403, 404):
        msg = ""
        try:
            msg = (r.json() or {}).get("msg", "")
        except Exception:
            msg = r.text
        print(f"⚠️  Access denied or removed from room ({r.status_code}), stop push:{msg}")
        local["joined"] = False
        local["agentId"] = None
        save_local_state(local)
        sys.exit(1)

    print(f"⚠️  Push failed:{r.text}")
    return False


def main():
    local = load_local_state()

    # First confirm if the configuration is complete
    if not JOIN_KEY or not AGENT_NAME:
        print("❌ Please fill in at the beginning of the script JOIN_KEY and AGENT_NAME")
        sys.exit(1)

    # If not before join, first join
    if not local.get("joined") or not local.get("agentId"):
        ok = do_join(local)
        if not ok:
            sys.exit(1)

    # Continuous Push
    print(f"🚀 Start continuous status push, interval={PUSH_INTERVAL_SECONDS}Seconds")
    print("🧭 Status logic: In task→Workspace; Standby/Complete→Break Room; Error→bugZone")
    print("🔐 If local /status Return Unauthorized(401), please set environment variable:OFFICE_LOCAL_STATUS_TOKEN Or OFFICE_LOCAL_STATUS_URL")
    try:
        while True:
            try:
                status_data = fetch_local_status()
                do_push(local, status_data)
            except Exception as e:
                print(f"⚠️  Push exception:{e}")
            time.sleep(PUSH_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\n👋 Stop push")
        sys.exit(0)


if __name__ == "__main__":
    main()
