# Star Office UI — Open-source release preparation checklist (prepare only, do not upload)

## 0. Current Objective
- This document is for“Pre-release preparation”, Do Not Perform Actual Upload.
- All push Actions require final approval from Star.

## 1. Privacy and Security Review Results (current repository)

### High-risk file detected (must be excluded)
- Run log:
  - `cloudflared.out`
  - `cloudflared-named.out`
  - `cloudflared-quick.out`
  - `healthcheck.log`
  - `backend.log`
  - `backend/backend.out`
- Running Status:
  - `state.json`
  - `agents-state.json`
  - `backend/backend.pid`
- Backup/Historical Files:
  - `index.html.backup.*`
  - `index.html.original`
  - `*.backup*` Directory and files
- Local Virtual Environment and Cache:
  - `.venv/`
  - `__pycache__/`

### Potential sensitive content detected
- Code contains absolute path `/root/...`(Suggest changing to relative path or environment variable)
- Documents and scripts contain private domain names `office.example.com`(Can be retained as an example, but suggested to change to a placeholder domain)

## 2. Mandatory changes (before submission)

### A. .gitignore(Needs completion)
Suggested Additions:
```
*.log
*.out
*.pid
state.json
agents-state.json
join-keys.json
*.backup*
*.original
__pycache__/
.venv/
venv/
```

### B. README Copyright statement (must be added)
Add“Art asset copyright and usage restrictions”Chapter:
- Code under open-source license (e.g. MIT)
- Art Assets Return to Original Author/Studio all
- Materials for learning only/Demo,**Commercial use prohibited**

### C. Slim down release directory
- Clean Run Logs, Runtime Files, Backup Files
- Keep Only“Minimum Runnable Set + Necessary materials + Document”

## 3. Suggested Structure for Upcoming Release Package
```
star-office-ui/
  backend/
    app.py
    requirements.txt
    run.sh
  frontend/
    index.html
    game.js (If still needed)
    layout.js
    assets/* (Public materials only)
  office-agent-push.py
  set_state.py
  state.sample.json
  README.md
  LICENSE
  SKILL.md
  docs/
```

## 4. Final check before release (confirm with Star)
- [ ] Whether to retain private domain name example (`office.example.com`)
- [ ] Which art resources are allowed to be public (confirm individually)
- [ ] README Does the non-commercial statement meet your expected wording
- [ ] Do you need to“Awen Lobster Joint Debugging Script”Place Separately examples Directory

## 5. Current status
- ✅ Document preparation complete (summary, feature description,Skill v2Publish checklist)
- ⏳ Waiting for Star's Confirmation“Public Asset Scope + Statement Copy + Start executing cleanup script?”
- ⛔ Not yet executed GitHub Upload
