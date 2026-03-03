# Star Office UI — New feature description (this phase)

## 1. Multi-Agent Guest System
- Support multiple remotes OpenClaw Join the same office simultaneously.
- Guest supports independent avatar, name, status, area, bubble.
- Supports dynamic online/offline and real-time refresh.

## 2. Join Key Mechanism Upgrade
- From“One-time key”Upgrade to“Fixed Reusable key”.
- Default key:`ocj_starteam01` ~ `ocj_starteam08`.
- Retain security control: each key Concurrency Limit of `maxConcurrent`(Default 3).

## 3. Concurrency control (race condition fixed)
- Fix concurrency join Race condition (race condition).
- Same key No. 4 Concurrent join Will be correctly rejected (HTTP 429).

## 4. Guest status mapping and area rendering
- `idle -> breakroom`
- `writing/researching/executing/syncing -> writing`
- `error -> error`
- Guest bubble text syncs with status, no longer misaligned.

## 5. Guest animation and resource optimization
- Guest upgraded from static image to animated sprite (pixel style).
- `guest_anim_1~6` Provided webp Version, reduce load size.

## 6. Optimize name and bubble display
- Non demo Move guest name and bubble position up to avoid character overlap.
- Bubble anchor changed to name-based positioning, ensure“Bubble above name”.

## 7. Mobile display
- Page Can Be Accessed and Displayed on Mobile.
- Layout has basic mobile adaptation, suitable for demo scenarios.

## 8. Remote push script joint debugging improvement
- Support reading from status file and pushing status to office.
- Add status source diagnostic logs (for locating“Why always idle”).
- Fix AGENT_NAME Environment variable override timing issue.
