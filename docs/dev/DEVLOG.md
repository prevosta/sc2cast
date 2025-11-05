# SC2Cast Development Log

**Concise history of all development work across sprints**

---

## Sprint 1.1: Docker Environment Setup
**Goal:** Get Docker running with SC2 + GPU support  
**Dates:** Nov 5, 2025 - In Progress

### Actions Taken:
1. Created `.gitignore` for Python/Docker projects
2. Created `Dockerfile`:
   - Base: Ubuntu 22.04 + CUDA 12.2
   - Installed: wget, unzip, Python 3.11, pip
   - Downloaded SC2 Linux client (4GB)
   - Set `SC2PATH=/opt/StarCraftII`
3. Created `docker-compose.yml`:
   - Enabled NVIDIA GPU support
   - Mounted volumes: src/, output/, project root
   - Interactive mode (stdin/tty)
4. **Organized project structure**:
   - Created folders: `docs/design/`, `docs/dev/`, `src/`, `tests/`, `config/`, `output/`, `replays/demo/`
   - Moved design docs to `docs/design/`
   - Moved dev files to `docs/dev/` (WORKFLOW.md, CURRENT_SPRINT.md, DEVLOG.md)
   - Moved demo replay to `replays/demo/`
   - Updated .gitignore for new structure
5. Started Docker build (Task 3 in progress - downloading SC2)

### Files Created:
- `.gitignore` (58 lines)
- `Dockerfile` (33 lines)
- `docker-compose.yml` (29 lines)
- Folder structure (7 new directories)

### Files Moved:
- All design docs → `docs/design/`
- Dev workflow files → `docs/dev/`
- Demo replay → `replays/demo/`

### Files Deleted:
- `CLEANUP.md` (temporary file)

### Status: ⏳ Waiting for build to complete

### Recent Updates:
- Fixed PROJECT_STATUS.md: Updated cost analysis to reflect zero-budget approach
- Fixed PROJECT_STATUS.md: Changed technology decisions from "options" to final decisions
- Fixed QUICK_START.md: Replaced API references with local alternatives (Ollama, Coqui)
- Updated WORKFLOW.md: Added file creation discipline rules (minimize new files)
- Cleaned up: Removed docker-compose.yml version warning

### Next Steps:
- Complete build verification
- Test GPU access (`nvidia-smi`)
- Test Python (`python3 --version`)
- Mark sprint complete

---

## Sprint 1.2: TBD
*Not started yet*

---

## Project Setup (Pre-Sprint)
**Date:** Nov 5, 2025

### Documentation Created:
- `README.md` - Project overview with zero-budget approach
- `CURRENT_SPRINT.md` - Active sprint tracker
- `WORKFLOW.md` - Development workflow guide + history log
- `docs/PROJECT_OVERVIEW.md` - High-level design
- `docs/TECHNICAL_DEEP_DIVE.md` - Detailed technical decisions
- `docs/ARCHITECTURE.md` - System architecture & data models
- `docs/IMPLEMENTATION_PLAN.md` - 20-week roadmap (PoC-first)
- `docs/FAQ_TECHNICAL_PANEL.md` - Technical Q&A
- `docs/QUICK_START.md` - Getting started guide
- `docs/CODE_EXAMPLES.md` - Implementation examples
- `docs/PANEL_PRESENTATION.md` - Executive summary
- `docs/PROJECT_STATUS.md` - Current status
- `docs/ZERO_BUDGET_APPROACH.md` - Local AI setup guide

### Key Decisions:
- **Zero-budget constraint**: $0/month operational costs
- **Local AI**: Llama 3.1 8B + Coqui TTS (no APIs)
- **Hardware**: RTX 3060+ 12GB VRAM (already available)
- **PoC-first approach**: Weeks 1-2 = Docker + video generation proof

### Repository Setup:
- GitHub repo: https://github.com/prevosta/sc2cast.git
- Initial commit: All documentation
- Demo replay included: `4323200_changeling_Mike_MagannathaAIE_v2.SC2Replay`

---

*This log is updated after each significant milestone or sprint completion.*
