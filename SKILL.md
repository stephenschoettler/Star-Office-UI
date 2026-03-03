---
name: star-office-ui
description: Star Office UI one-click Skill — quickly deploy the pixel office dashboard with multi-agent support, status visualization, mobile viewing, and public access.
---

# Star Office UI Skill

This Skill is for OpenClaw agents who want to set up the **pixel office dashboard** for their user.

**Goal:** Get the user to "see it working" with minimal friction — run the steps below in order.

---

## 0. Tell Your User What This Is

You can open with:
> "This is a multi-agent pixel office dashboard — your AI assistants automatically move to different zones based on their status, and you can see yesterday's activity summary!"

---

## 1. One-Click Launch (Do This First)

Run these commands on the user's machine in order:

```bash
# 1) Clone the repo
git clone https://github.com/ringhyacinth/Star-Office-UI.git
cd Star-Office-UI

# 2) Install dependencies
pip install -r backend/requirements.txt

# 3) Initialize state file (first time)
cp state.sample.json state.json

# 4) Start the backend
python3 backend/app.py
```

Then tell the user:
> "Done! Open http://127.0.0.1:18791 to see the pixel office!"

---

## 2. Demo the State Switching

Run from the project root:

```bash
# Working → goes to desk
python3 set_state.py writing "Organizing your docs"

# Syncing
python3 set_state.py syncing "Syncing progress"

# Error → goes to bug zone
python3 set_state.py error "Bug found, investigating"

# Standby → back to break room
python3 set_state.py idle "On standby, ready for you"
```

---

## 3. Public Access (Optional)

### Recommended: Cloudflare Tunnel (fastest)

If `cloudflared` is available on the machine:

```bash
cloudflared tunnel --url http://127.0.0.1:18791
```

You'll get an `https://xxx.trycloudflare.com` link to share with the user.

If `cloudflared` isn't available, use your preferred public access method (Nginx/Caddy reverse proxy, custom domain, other tunnels).

---

## 4. Invite Other Agents to Join (Optional)

If other OpenClaw agents want to join the office:

### Step A: Use `office-agent-push.py`
Have the other agent:
1. Download `office-agent-push.py` from this repo
2. Call `join-agent` + periodic `agent-push`
3. They'll appear on the office dashboard

### Step B: Join Key Info
- Default keys: `ocj_starteam01` through `ocj_starteam08` (in `join-keys.json`)
- Max 3 concurrent agents per key
- You can generate custom keys for the user

---

## 5. Yesterday's Notes (Optional)

If the user wants to see the "Yesterday's Notes" panel:
- Place a `memory/YYYY-MM-DD.md` file in the directory above the repo
- The backend will auto-read yesterday's (or most recent available) entry and display a sanitized summary

---

## 6. Common Questions

### Q1: "Why is the main character Staryu?"
> Staryu is a Nintendo Pokémon IP, not an original creation. The original author chose it as a fun name pun — this is a non-commercial fan project for learning/demo only.

### Q2: "Can I use this commercially?"
> The code (MIT) is fine for commercial use, but **the art assets (characters, backgrounds) are non-commercial only**. Replace with your own original art if you're going commercial.

### Q3: "How do other agents join?"
> They use a join key and push their status periodically. `office-agent-push.py` is the ready-to-use script for other agents.

---

## 7. Tips for You (the Agent)

- Complete the launch steps for the user — let them just watch and experience it
- For public access, lead with Cloudflare Tunnel (fastest)
- You can call `set_state.py` on behalf of the user — don't make them type commands
- Never expose the user's internal network addresses or private info in the dashboard
