# Current Sprint: 1.2 - Replay Parser Implementation

## 🎯 Sprint Goal
**Parse the demo replay file and extract basic game information. No video, no AI - just prove we can read replays.**

## ✅ Success Criteria
- [ ] `sc2reader` library installed in container
- [ ] Can parse demo replay without errors
- [ ] Extract: players, races, map, duration, winner
- [ ] Output clean JSON to stdout

## 📋 Tasks (In Order)

### Task 1: Install sc2reader
Update `Dockerfile` to install `sc2reader`:
```dockerfile
RUN pip install --no-cache-dir sc2reader
```
Rebuild container.

### Task 2: Create Basic Parser Script
Create `src/parse_replay.py`:
- Load replay from `/replays/demo/` folder
- Extract basic metadata (players, races, map, duration)
- Print JSON to stdout
- Keep it simple (~50 lines max)

### Task 3: Test Parser
```powershell
docker compose run --rm sc2cast python3 src/parse_replay.py
```
Verify: Outputs valid JSON with replay info

### Task 4: Add Error Handling
Update `src/parse_replay.py`:
- Handle missing replay file
- Handle corrupted replay
- Clear error messages
- Exit codes (0=success, 1=error)

### Task 5: Document Output Format
Update `docs/TECHNICAL.md`:
- Add "Replay Parser Output" section
- Document JSON schema
- Keep it concise (10-15 lines)

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
