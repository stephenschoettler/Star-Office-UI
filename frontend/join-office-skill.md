# Join Star Office - Visitor Agent Skill

## Description
Connect to Star's Pixel Office, allowing your user to see your status changes on the visual office dashboard.

## Prerequisites
- You must obtain a one-time access key from Star (format:`ocj_xxx`)
- Your user has authorized you to push status to Star's office
- You Can Access `https://office.example.com`

## Steps
1. Confirm authorization with your user:
   > “I will update my work status (idle/writing/researching/executing/syncing/error) Periodically sent to Star's Office Dashboard for visual collaboration; no specific content included/Privacy; can stop anytime. Authorize?”

2. After user approval:
   - Use the Name You Want to Display in the Office as `AGENT_NAME`
   - Use the key given by Star as `JOIN_KEY`
   - Download or Copy `office-agent-push.py`(Can Access:https://office.example.com/static/office-agent-push.py)
   - **Simplest Recommendation**: Run script directly (built-in state.json Auto discovery)
     - Will automatically try the following paths:
       - `/root/.openclaw/workspace/star-office-ui/state.json`
       - `/root/.openclaw/workspace/state.json`
       - `Current working directory/state.json`
       - `Same Directory as Script/state.json`
   - If your environment path is special, manually specify:
     - `OFFICE_LOCAL_STATE_FILE=/Your/state.json/Path`
   - If you are unable to provide state File, Then Use /status Authentication method:
     - `OFFICE_LOCAL_STATUS_TOKEN=<Yourtoken>`
     - (Optional)`OFFICE_LOCAL_STATUS_URL=http://127.0.0.1:18791/status`
   - Run after entering configuration

3. Script Will Automatically:
   - Execute once first `join-agent`, display“Joined and auto-approved”
   - Prioritize local read `state.json`(If available), otherwise read locally `/status`
   - Map Status by Office Logic: In Task→Workspace; Standby/Complete→Break Room; Error→bugZone
   - Every 15 Push status to Star's office every second (more real-time)
   - If removed from the room, will automatically stop

4. When stopping push:
   - By `Ctrl+C` Terminate Script
   - Script will attempt to auto-call `leave-agent` Exit

## Notes
- Only push status words and brief descriptions, no private content
- Default authorization validity 24h
- If received `403`/`404`, stop pushing and contact your user
