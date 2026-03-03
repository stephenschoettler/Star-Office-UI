# Star Office UI — Feature description (Overview)

Star Office UI Is a“Pixel Office”Visual interface, used to AI Assistant/Multiple OpenClaw Guest status, rendered into a small office scene viewable on the web (including mobile).

## What you can see
- Pixel Office Background (Top View)
- Role (Star + Guests Move to Different Areas Based on Status
- Name and Bubble (bubble) Display Current Status/Ideas (customizable mapping)
- Can be displayed when opened on mobile (suitable for showcasing)/Live Broadcast/External Demo)

## Core Abilities

### 1) Single Agent(Local Star) Status rendering
- Backend Read `state.json` Provide `GET /status`
- Frontend polling `/status`, according to `state` Render Star Current area
- Provide `set_state.py` Quickly Switch State

### 2) Multiple Guests (Multiple Agents) Joining Office
- Guest via `POST /join-agent` Join to gain `agentId`
- Guest via `POST /agent-push` Continuously push own status
- Frontend passed `GET /agents` Fetch and render guest list

### 3) Join Key(Access key) mechanism
- Supports Fixed Reusable join key(Such as `ocj_starteam01~08`)
- Support each key Concurrent online limit (default 3)
- Easy to control“Who can enter the office”and“Same key Number of Agents Allowed Simultaneously”

### 4) Status → Area mapping (unified logic)
- idle → breakroom(Break room)
- writing / researching / executing / syncing → writing(Workspace)
- error → error(Bug Zone)

### 5) Guest animation and performance optimization
- Guest character uses animated sprite
- Support WebP Resources (smaller size, faster loading)

### 6) Name/Layout where bubbles don't block
- Real Guest and demo Guest Separation Logic
- Non demo Move guest name and bubble upwards
- bubble Anchor above name to avoid covering it

### 7) Demo Mode (optional)
- `?demo=1` Only display demo Guest (default hidden)
- demo No impact on real guests

## Main Interface (Backend)
- `GET /`: Frontend Page
- `GET /status`: single agent Status (compatible with old version)
- `GET /agents`: Multiple agent List (for guest rendering)
- `POST /join-agent`: Guest joined
- `POST /agent-push`: Guest push status
- `POST /leave-agent`: Guest Departure
- `GET /health`: Health Check

## Security and Privacy Notice
- Do not write private information into `detail`(Because it will be rendered/Can be pulled)
- Must clean before open source: logs, runtime files,join keysTunnel output, etc.

## Art asset usage statement (mandatory)
- Code can be open-sourced, but art assets (backgrounds, characters, animations, etc.) are copyrighted by the original author/Studio Owned.
- Art Assets for Learning and Demonstration Only,**Commercial use prohibited**.
