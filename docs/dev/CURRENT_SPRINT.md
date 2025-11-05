# Sprint 1.2: Basic Replay Processing

**Goal:** Parse demo replay file and extract metadata  
**Started:** November 5, 2025  
**Status:** In Progress

---

## 🎯 Tasks

- [ ] **Task 1:** Load demo replay with sc2reader
  - Use existing replay: `replays/4323200_changeling_Mike_MagannathaAIE_v2.SC2Replay`
  - Parse replay file
  - Verify it loads without errors

- [ ] **Task 2:** Extract basic metadata
  - Players (names, races)
  - Map name
  - Game duration
  - Match date/time

- [ ] **Task 3:** Extract game information
  - Matchup (e.g., "TvZ")
  - Winner
  - Game speed
  - Replay version

- [ ] **Task 4:** Output to JSON
  - Create structured JSON output
  - Save to `output/replay_metadata.json`
  - Human-readable formatting

- [ ] **Task 5:** Test with demo replay
  - Run parser on AIArena replay
  - Verify all fields populated
  - Check output is valid JSON

---

## 📦 Deliverables

- `src/sc2cast/replay_parser.py` - Replay parsing module
- `output/replay_metadata.json` - Parsed replay data
- Working replay parsing pipeline

---

## 🎯 Success Criteria

- ✅ Can load SC2 replay files
- ✅ Extract player and match information
- ✅ Output valid JSON
- ✅ Handles AIArena replay format
- ✅ No crashes or errors

---

**Next Sprint:** 1.3 - Event Extraction
