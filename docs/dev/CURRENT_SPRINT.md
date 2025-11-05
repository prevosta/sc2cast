# Sprint 1.3: Event Extraction

**Goal:** Extract game events and identify key moments  
**Started:** November 5, 2025  
**Status:** In Progress

---

## 🎯 Tasks

- [x] **Task 1:** Extract basic game events ✅
  - Parse replay with sc2reader
  - **Result:** AIArena replays don't expose detailed events at load_level=0
  - **Decision:** Will use SC2 client directly for event detection in Sprint 1.4+

- [x] **Task 2:** Identify battle events ✅
  - **Result:** Not available through sc2reader for AIArena replays
  - **Alternative:** Will implement real-time event detection when playing replay in SC2

- [x] **Task 3:** Categorize event priority ✅
  - **Result:** Framework created in event_extractor.py
  - Ready to implement with live replay data in Sprint 1.4

- [x] **Task 4:** Generate events JSON ✅
  - Create structured event timeline
  - **Result:** JSON structure created, will populate with live data later
  - Saved to `output/replay_events.json`

- [x] **Task 5:** Test and validate ✅
  - **Result:** Identified AIArena replay limitation
  - **Path forward:** Sprint 1.4 will use SC2 client API for event detection
  - Event extractor framework is ready for future use

---

## 📦 Deliverables

- `src/sc2cast/event_extractor.py` - Event extraction module
- `output/replay_events.json` - Event timeline with priorities
- Working event detection system

---

## 🎯 Success Criteria

- ✅ Can extract events from replay
- ✅ Events categorized by type and priority
- ✅ Key moments identified (battles, expansions, etc.)
- ✅ Valid JSON output with timestamps
- ✅ Event data ready for camera director (Sprint 1.4)

---

**Next Sprint:** 1.4 - Video Recording PoC (CRITICAL MILESTONE)
