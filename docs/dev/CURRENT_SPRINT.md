# Current Sprint: 1.1 - Docker Environment Setup

## 🎯 Sprint Goal
**Get Docker container running with SC2 + GPU support. Nothing else.**

## ✅ Success Criteria
- [ ] Docker container builds successfully
- [ ] Can access SC2 client inside container
- [ ] GPU (NVIDIA) is accessible from container (`nvidia-smi` works)
- [ ] Can run `python --version` and see Python 3.11+

## 📋 Tasks (In Order)

### Task 1: Create Dockerfile
Create `Dockerfile` with:
- Base: Ubuntu 22.04 + CUDA support
- Install SC2 Linux client
- Install Python 3.11
- Keep it minimal (~60 lines max)

### Task 2: Create docker-compose.yml
Create `docker-compose.yml` with:
- GPU support (NVIDIA runtime)
- Volume mounts for replays and output
- Keep it simple (~25 lines max)

### Task 2.5: Organize Project Structure
Create folders and move files:
- Create `replays/demo/` folder
- Move demo replay to `replays/demo/`
- Update .gitignore for replays folder structure

### Task 3: Test Container Build
```powershell
docker-compose build
```
Verify: Build completes without errors

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
