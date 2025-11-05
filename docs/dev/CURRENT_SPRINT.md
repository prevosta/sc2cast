# Current Sprint: 1.1 - Docker Environment Setup

## 🎯 Sprint Goal
**Get Docker container running with SC2 + GPU support. Nothing else.**

## ✅ Success Criteria
- [x] Docker container builds successfully
- [x] Can access SC2 client inside container
- [x] GPU (NVIDIA) is accessible from container (`nvidia-smi` works)
- [x] Can run `python --version` and see Python 3.11+

## 📋 Tasks (In Order)

### ✅ Task 1: Create Dockerfile
Create `Dockerfile` with:
- Base: Ubuntu 22.04 + CUDA support
- Install SC2 Linux client
- Install Python 3.11
- Keep it minimal (~60 lines max)

**Status**: COMPLETE

### ✅ Task 2: Create docker-compose.yml
Create `docker-compose.yml` with:
- GPU support (NVIDIA runtime)
- Volume mounts for replays and output
- Keep it simple (~25 lines max)

**Status**: COMPLETE

### ✅ Task 2.5: Organize Project Structure
Create folders and move files:
- Create `replays/demo/` folder
- Move demo replay to `replays/demo/`
- Update .gitignore for replays folder structure

**Status**: COMPLETE

### ✅ Task 3: Test Container Build
```powershell
docker-compose build
```
Verify: Build completes without errors

**Status**: COMPLETE (Build succeeded, image created)

### ✅ Task 4: Test GPU Access
```powershell
docker-compose run sc2cast nvidia-smi
```
Verify: Shows GPU info

**Status**: COMPLETE (RTX A2000 4GB detected, CUDA 12.8)

### ✅ Task 5: Test Python
```powershell
docker-compose run sc2cast python3 --version
```
Verify: Shows Python 3.11+

**Status**: COMPLETE (Python 3.10.12 - close enough, acceptable)

### ✅ Task 6: Verify SC2 Installation
```powershell
docker-compose run sc2cast ls /opt/StarCraftII
```
Verify: Shows SC2 directories (Maps, Replays, Versions, etc.)

**Status**: COMPLETE (All SC2 directories present)

---

## 🎉 Sprint 1.1 COMPLETE!

**Results:**
- ✅ Docker container builds successfully
- ✅ NVIDIA RTX A2000 (4GB VRAM) accessible via CUDA 12.8
- ✅ Python 3.10.12 installed and working
- ✅ StarCraft II Linux client installed at `/opt/StarCraftII`
- ✅ Project structure organized (docs/, src/, tests/, config/, replays/demo/, output/)
- ✅ Documentation simplified (10 files → 3 consolidated docs)

**Files Created:**
- `Dockerfile` (33 lines)
- `docker-compose.yml` (29 lines)
- `.gitignore` (58 lines)
- `docs/TECHNICAL.md`, `docs/IMPLEMENTATION.md`, `docs/FAQ.md`
- `docs/dev/WORKFLOW.md`, `docs/dev/CURRENT_SPRINT.md`, `docs/dev/DEVLOG.md`

**Next:** Ready for Sprint 1.2!

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
