# Current Sprint: 1.4 - Video Recording Proof of Concept

## 🎯 Sprint Goal
**Prove we can run a SC2 replay in Docker and capture video. This is the BIGGEST technical risk - if this doesn't work, the whole project is blocked.**

## ✅ Success Criteria
- [ ] python-sc2 library installed and working
- [ ] Can launch SC2 client in headless mode (Xvfb)
- [ ] Can control replay playback programmatically
- [ ] Can capture frames with FFmpeg
- [ ] Generate 10-second MP4 video file

## 📋 Tasks (In Order)

### Task 1: Install Video Dependencies
Update `Dockerfile`:
- Install Xvfb (virtual framebuffer for headless)
- Install FFmpeg
- Install python-sc2 library
- Set up display environment

### Task 2: Test SC2 Launches
Create `src/test_sc2.py`:
- Launch SC2 client
- Verify it starts without crashing
- Exit cleanly
- Keep it simple (~30 lines)

### Task 3: Open Replay Programmatically
Extend `src/test_sc2.py`:
- Load demo replay file
- Start replay playback
- Confirm it's actually playing
- No recording yet - just prove control works

### Task 4: Capture Video
Create `src/record_replay.py`:
- Start SC2 with replay
- Use FFmpeg to capture screen
- Record 10 seconds
- Output MP4 file to `/workspace/output/`

### Task 5: Test Full Pipeline
```powershell
docker compose run --rm sc2cast python3 src/record_replay.py
```
Verify: 10-second MP4 file exists in `output/` folder

## 🚫 Out of Scope for This Sprint
- ❌ NO smart camera movement yet (fixed camera is fine)
- ❌ NO overlays or HUD
- ❌ NO audio/commentary
- ❌ NO event-based recording
- ❌ Just prove: SC2 → Video works!

## 📝 Expected Output

```
output/
└── test_replay.mp4  # 10 seconds, 1080p, showing replay
```

## ⚠️ Technical Risks

**HIGH RISK: This might not work because:**
- SC2 might not run headless in Docker
- Xvfb display issues
- python-sc2 might not work with our replay format
- FFmpeg screen capture might be slow/broken

**If it fails:** We may need to:
- Use wine + Windows SC2 version
- Different capture method (obs-studio?)
- Run SC2 outside Docker (not ideal)

## 🎯 Why This Sprint Matters

**This is the make-or-break moment.** If we can't record video from replays, the entire project needs to pivot. We're testing this NOW (Week 1) instead of discovering it in Week 7.

**If successful:** We have proof the core pipeline works, everything else is "just" features.

---

## 💬 Example Commands

```powershell
# Build with new dependencies
docker compose build

# Test SC2 launches
docker compose run --rm sc2cast python3 src/test_sc2.py

# Record 10-second video
docker compose run --rm sc2cast python3 src/record_replay.py

# Check output
ls output/test_replay.mp4
```

## 🚫 Out of Scope for This Sprint
- ❌ NO camera control yet
- ❌ NO video recording yet
- ❌ NO commentary generation yet
- ❌ Just extract and categorize events!

## 📝 Files to Modify
```
sc2cast/
└── src/
    └── parse_replay.py     # ← Extend this (~250 lines)
```

## 🎯 Next Sprint Preview
**Sprint 2.1**: Camera director - determine what to show and when

---

## 💬 Example Output (Target)

```json
{
  "filename": "...",
  "map": "Magannatha AIE",
  "duration_seconds": 568,
  "players": [...],
  "events": [
    {
      "time": 12,
      "type": "expansion",
      "player": "Mike",
      "priority": "high",
      "details": "Natural expansion"
    },
    {
      "time": 145,
      "type": "battle",
      "priority": "high",
      "details": "15 units lost, player1: 8, player2: 7"
    }
  ],
  "key_moments": [12, 145, 234, 389, 512]
}
```

## 🚫 Out of Scope for This Sprint
- ❌ NO video recording yet
- ❌ NO camera control yet
- ❌ NO AI/LLM yet
- ❌ NO detailed event analysis yet
- ❌ Just basic metadata extraction!

## 📝 Files to Create/Modify
```
sc2cast/
├── Dockerfile              # ← Modify (add sc2reader)
└── src/
    └── parse_replay.py     # ← Create this (~50 lines)
```

## � Next Sprint Preview
**Sprint 1.3**: Extract game events (builds, attacks, expansions) from replay

---

## 💬 Example Output (Target)

```json
{
  "filename": "4323200_changeling_Mike_MagannathaAIE_v2.SC2Replay",
  "map": "Equilibrium LE",
  "duration_seconds": 1247,
  "duration_human": "20:47",
  "players": [
    {
      "name": "Mike",
      "race": "Zerg",
      "result": "Win"
    },
    {
      "name": "MagannathaAIE",
      "race": "Protoss", 
      "result": "Loss"
    }
  ]
}
```

### Task 4: Test GPU Access
```powershell
docker-compose run sc2cast nvidia-smi
```
Verify: Shows GPU info

### Task 5: Test Python
```powershell
docker-compose run sc2cast python3 --version
```
Verify: Shows Python 3.11+

## 🚫 Out of Scope for This Sprint
- ❌ NO replay parsing yet
- ❌ NO Python libraries (sc2reader, etc.) yet
- ❌ NO AI models (Ollama, Coqui) yet
- ❌ NO video recording yet
- ❌ Just get the environment working!

## 📝 Files to Create (This Sprint Only)
```
sc2cast/
├── Dockerfile           # ← Create this
├── docker-compose.yml   # ← Create this
└── .devcontainer/
    └── devcontainer.json  # ← Create this (optional, for VS Code)
```

## 🎯 Next Sprint Preview
**Sprint 1.2**: Parse the demo replay file and extract basic info (no video yet)

---

## 💬 How to Prompt Me

**Good prompts for this sprint:**
- "Create the Dockerfile"
- "Add GPU support to docker-compose"
- "Test if SC2 is accessible"
- "Fix the Docker build error"

**Bad prompts (too broad):**
- "Start implementing the project" ❌
- "Set up everything" ❌
- "Create all the code" ❌

**Perfect prompt:**
- "Complete Sprint 1.1 task 1" ✅
- "Create the Dockerfile for SC2 + CUDA" ✅
- "What's the next task in CURRENT_SPRINT.md?" ✅
