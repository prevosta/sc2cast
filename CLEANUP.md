# Pre-Development Cleanup Checklist

## Files to Keep (Essential)
- ✅ `README.md` - Project overview
- ✅ `CURRENT_SPRINT.md` - Active sprint (THE MOST IMPORTANT FILE)
- ✅ `WORKFLOW.md` - How to work with me
- ✅ `docs/` folder - All design documentation (reference only)
- ✅ `4323200_changeling_Mike_MagannathaAIE_v2.SC2Replay` - Demo file

## Files to Create (When Starting Sprint 1.1)
- `Dockerfile` - During sprint 1.1, task 1
- `docker-compose.yml` - During sprint 1.1, task 2
- `.devcontainer/devcontainer.json` - During sprint 1.1, task 4 (optional)

## Folders to Create (When Needed)
- `src/` - Start in Sprint 1.2 (replay parsing)
- `tests/` - Start in Sprint 2.x (when we have code to test)
- `config/` - Start in Sprint 3.x (when we need configuration)

## 📋 Cleanup Actions (Optional, Do Now)

### Option A: Minimal Cleanup (Recommended)
Just verify structure:
```powershell
# Current structure should be:
sc2cast/
├── README.md
├── CURRENT_SPRINT.md
├── WORKFLOW.md
├── 4323200_changeling_Mike_MagannathaAIE_v2.SC2Replay
└── docs/
    ├── PROJECT_OVERVIEW.md
    ├── TECHNICAL_DEEP_DIVE.md
    ├── ARCHITECTURE.md
    ├── IMPLEMENTATION_PLAN.md
    ├── FAQ_TECHNICAL_PANEL.md
    ├── QUICK_START.md
    ├── CODE_EXAMPLES.md
    ├── PROJECT_STATUS.md
    ├── PANEL_PRESENTATION.md
    └── ZERO_BUDGET_APPROACH.md
```

### Option B: Add .gitignore (Good Practice)
Create `.gitignore` for Python/Docker:
```
__pycache__/
*.py[cod]
.venv/
venv/
.env
*.log
output/
replays/*.SC2Replay  # Don't commit large replay files
!4323200_changeling_Mike_MagannathaAIE_v2.SC2Replay  # Except demo
.vscode/
.idea/
```

### Option C: Create Empty Folders (For Later)
```powershell
# Don't create these yet! 
# But you can if you want structure visible:
mkdir src
mkdir tests
mkdir config
mkdir output
```

## 🎯 My Recommendation

**Do Option A (verify structure) + Option B (add .gitignore)**

Then say:
- **"Start Sprint 1.1"** - I'll update CURRENT_SPRINT.md
- **"Do task 1"** - I'll create the Dockerfile

That's it. No more prep needed!

## ⚠️ What NOT to Do

- ❌ Don't create empty Python files (I'll do that per task)
- ❌ Don't create folder structure in advance (YAGNI)
- ❌ Don't create requirements.txt yet (Sprint 1.2+)
- ❌ Don't install anything locally (everything goes in Docker)

## ✅ When You're Ready

Just say one of:
1. "Let's do the cleanup" (I'll create .gitignore)
2. "Skip cleanup, start Sprint 1.1" (Jump right in)
3. "Just create .gitignore then start Sprint 1.1" (Recommended)

**Keep it simple. Start small. Build incrementally.** 🎯
