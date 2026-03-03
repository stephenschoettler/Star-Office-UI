# Star Office UI

A real-time pixel-art office dashboard for multi-agent AI teams. Your AI agents (OpenClaw / lobster bots) show up as animated characters on a shared office map — you can see who's working, who's on standby, and who's in the bug zone.

![Star Office UI Preview](docs/screenshots/office-preview-20260301.jpg)

---

## What is this?

Star Office UI is a **multi-agent status dashboard** — think of it as:
> A live-updating pixel office: your AI assistants automatically move to different zones (break room / work area / bug zone) based on their current state, and you can see their "Yesterday's Notes" summaries.

Built for [OpenClaw](https://openclaw.dev) and compatible agents.

---

## ✨ Quick Start (30 seconds)

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

Open: **http://127.0.0.1:18791**

Try switching states (run from project root):

```bash
python3 set_state.py writing "Drafting the docs"
python3 set_state.py syncing "Syncing progress"
python3 set_state.py error "Bug found, investigating"
python3 set_state.py idle "On standby"
```

---

## Features

### 1. Agent Status Visualization
- States: `idle` (break room), `writing` (desk), `researching` (desk), `executing` (desk), `syncing` (desk), `error` (bug zone)
- State maps to office zones with animations and speech bubbles

### 2. Yesterday's Notes
- Frontend displays a "Yesterday's Notes" card
- Backend reads `memory/*.md` files, sanitizes sensitive content, and renders a summary

### 3. Multi-Agent Guest System
- Other agents join via a join key (`POST /join-agent`)
- Guests push their status continuously (`POST /agent-push`)
- Up to 3 concurrent agents per key (configurable)

### 4. Mobile-Friendly
- Responsive layout — works on phone browsers
- Horizontal pan gesture for office navigation

### 5. Flexible Public Access
- Expose via Cloudflare Tunnel, Nginx, or any reverse proxy

---

## API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/status` | GET | Main agent status |
| `/set_state` | POST | Set main agent state |
| `/agents` | GET | List all guest agents |
| `/join-agent` | POST | Guest agent joins |
| `/agent-push` | POST | Guest pushes status update |
| `/leave-agent` | POST | Guest leaves |
| `/yesterday-memo` | GET | Yesterday's Notes content |

---

## Art Assets — Please Read

### Guest Character Assets
Guest character animations use free assets from **LimeZu** (itch.io).  
Please retain attribution when redistributing or demoing, and follow the original license terms.

### Main Character — Legal Notice
- The main character sprite is based on **Staryu** from Nintendo's Pokémon franchise — **this is not an original IP**.
- This project is **non-commercial fan creation only**: the character was chosen for a fun name pun by the original author.
- This project is for **learning, demo, and non-commercial use only**.
- Pokémon and Staryu are trademarks of Nintendo / The Pokémon Company.
- **If you plan to deploy this publicly, please replace with your own original character art.**

### Commercial Use Restriction ⚠️
- Code (logic/backend/frontend) is **MIT licensed** — use freely.
- **All art assets in this repo (characters, backgrounds, sprites) are non-commercial only.**
- For commercial use, you must replace all art assets with your own originals.

---

## License

- **Code / Logic: MIT** (see `LICENSE`)
- **Art Assets: Non-commercial, learning/demo use only**

Fork it, extend it, open PRs — but respect the asset boundaries.

---

## Extend It

Ideas for what to build on top of this:
- Richer state semantics and auto-orchestration
- Multi-room / multi-team office maps
- Task boards, timelines, auto-generated daily reports
- Full access control and permission systems

---

## Authors

- **Ring Hyacinth** — [@ring_hyacinth](https://x.com/ring_hyacinth) on X
- **Simon Lee** — [@simonxxoo](https://x.com/simonxxoo) on X

---

## Project Structure

```
Star-Office-UI/
├── frontend/
│   ├── index.html          # Main office page
│   ├── join.html           # Guest join page
│   ├── invite.html         # Invite instructions page
│   ├── game.js             # Phaser game logic
│   ├── layout.js           # Layout/coordinate config
│   └── fonts/              # Pixel font (ArkPixel)
├── backend/
│   ├── app.py              # Flask API server
│   └── requirements.txt
├── docs/                   # Documentation
├── state.json              # Main agent state (runtime)
├── agents-state.json       # Guest agents state (runtime)
├── join-keys.json          # Join key configuration
├── set_state.py            # CLI state switcher
├── office-agent-push.py    # Guest agent push script
└── state.sample.json       # State file template
```
