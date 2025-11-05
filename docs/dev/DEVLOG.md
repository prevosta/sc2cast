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

### Status: ✅ Sprint 1.1 COMPLETE!

**Final Results:**
- Docker container built successfully (sc2cast:latest)
- NVIDIA RTX A2000 (4GB VRAM) accessible via CUDA 12.8
- Python 3.10.12 installed and working
- StarCraft II Linux client verified at `/opt/StarCraftII`
- Documentation simplified: 10 files → 3 consolidated docs (60% reduction)
- Project structure organized and clean

**Duration:** ~2 hours (including documentation work)

### Recent Updates:
- Fixed PROJECT_STATUS.md: Updated cost analysis to reflect zero-budget approach
- Fixed PROJECT_STATUS.md: Changed technology decisions from "options" to final decisions
- Fixed QUICK_START.md: Replaced API references with local alternatives (Ollama, Coqui)
- Updated WORKFLOW.md: Added file creation discipline rules (minimize new files)
- Cleaned up: Removed docker-compose.yml version warning
- **Documentation simplification**: Consolidated 10 design docs → 3 essential docs
  - Created: `TECHNICAL.md` (replaces 5 docs: TECHNICAL_DEEP_DIVE, ARCHITECTURE, ZERO_BUDGET_APPROACH, CODE_EXAMPLES, PROJECT_OVERVIEW)
  - Created: `IMPLEMENTATION.md` (replaces 2 docs: IMPLEMENTATION_PLAN, PROJECT_STATUS)
  - Created: `FAQ.md` (simplified from FAQ_TECHNICAL_PANEL)
  - Deleted: `docs/design/` folder (10 redundant files removed)
  - Updated: `README.md` to reference new 3-doc structure
  - Updated: `WORKFLOW.md` with strict anti-bloat rules

### Next Steps:
- Complete build verification
- Test GPU access (`nvidia-smi`)
- Test Python (`python3 --version`)
- Mark sprint complete

---

## Sprint 1.2: Replay Parser Implementation
**Goal:** Parse demo replay and extract basic metadata  
**Dates:** Nov 5, 2025 - Complete

### Actions Taken:
1. Added `sc2reader` to Dockerfile
2. Created `src/parse_replay.py` (143 lines):
   - Parses SC2 replay files
   - Extracts players, map, duration
   - Outputs clean JSON
   - Robust error handling
3. **Critical fix**: Monkey-patched sc2reader to handle AI Arena replays
   - AI Arena replays have empty `cache_handles` array
   - Original sc2reader crashes on `details["cache_handles"][0]`
   - Patched to fallback to "unknown" region when empty
4. Added `/workspace/replays` volume mount to docker-compose
5. Moved map file to `replays/maps/`
6. Updated `docs/TECHNICAL.md` with parser documentation

### Files Created:
- `src/parse_replay.py` (143 lines)

### Files Modified:
- `Dockerfile` (added sc2reader)
- `docker-compose.yml` (added replays mount)
- `docs/TECHNICAL.md` (added parser docs)
- `replays/maps/MagannathaAIE_v2.SC2Map` (moved from root)

### Status: ✅ Sprint 1.2 COMPLETE!

**Results:**
- Successfully parses AI Arena replays
- Extracts: filename, map, duration, player names
- Clean JSON output with error handling
- Exit codes: 0=success, 1=error

**Limitations:**
- Race shows "Unknown" (requires game events parsing)
- Result shows "Unknown" (requires game events parsing)
- These will be addressed in Sprint 1.3+

**Duration:** ~3 hours (including sc2reader debugging)

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
