# SC2Cast - Implementation Plan

**All planning, timeline, and status in one place.**

---

## 🎯 Current Status

**Phase:** Phase 1 - Proof of Concept  
**Sprint:** 1.4 Starting (Video Recording PoC) **CRITICAL MILESTONE**  
**Started:** November 5, 2025  
**Progress:** 3/4 Phase 1 sprints complete (75%)

### Completed
- ✅ Sprint 1.1: Windows environment setup (Python 3.12.7, Poetry 1.8.5, SC2 verified)
- ✅ Sprint 1.2: Basic replay parsing (sc2reader working, JSON output created)
- ✅ Sprint 1.3: Event extraction framework (ready for SC2 client integration)

### Architecture Decision
- ❌ **REMOVED:** Docker + Linux containers (replay playback blocked by headless client)
- ✅ **NEW:** Native Windows execution (Windows SC2 client supports replays!)

### Why Windows Native?
1. **Replay Support:** Windows SC2 client can play replays (Linux headless cannot)
2. **Simplicity:** No Docker complexity, direct Python scripts
3. **GPU Access:** Direct NVIDIA driver access
4. **Development Speed:** Faster iteration, easier debugging

### Next
- Sprint 1.4: Video Recording PoC **CRITICAL** - Test if Windows SC2 can play and record replays

---

## 📅 Implementation Timeline (20 Weeks)

### Phase 1: Proof of Concept (Weeks 1-2)
**Goal:** Prove Windows + SC2 + video generation works

**Sprint 1.1:** Windows Environment Setup (Week 1)
- Install Python 3.11+ on Windows
- Install Poetry: `pip install poetry`
- Install dependencies: `poetry install`
- Install FFmpeg for Windows
- Verify SC2 installation path
- Deliverable: Can run Python scripts, SC2 detected

**Sprint 1.2:** Basic Replay Processing (Week 1)
- Parse demo replay file with sc2reader
- Extract metadata (players, duration, map)
- Test with AIArena replay format
- Deliverable: JSON output of replay data

**Sprint 1.3:** Event Extraction (Week 1-2)
- Extract game events (builds, battles, expansions)
- Categorize by priority (high/medium/low)
- Identify key moments for camera
- Deliverable: Events timeline with filtering

**Sprint 1.4:** Video Recording PoC (Week 2) **CRITICAL**
- Load replay with python-sc2 + Windows SC2 client
- Control replay playback programmatically
- Capture screen with FFmpeg or screen recording
- Deliverable: 10-second MP4 file from replay
- **Risk:** HIGH - If replays still don't work, need alternative approach

### Phase 2: Video Foundation (Weeks 3-4)
**Goal:** Record full-length videos from replays

**Sprint 2.1:** SC2 Replay Control
- python-sc2 observer mode
- Camera positioning and movement
- Replay speed control
- Deliverable: Can navigate replay programmatically

**Sprint 2.2:** Screen Recording
- FFmpeg screen capture setup
- Audio capture (game sounds)
- 1080p60 encoding settings
- Deliverable: Full-length replay video (no commentary)

### Phase 3: Local AI Setup (Weeks 5-6)
**Goal:** Get Llama + Coqui working on Windows

**Sprint 3.1:** Ollama on Windows
- Install Ollama for Windows
- Pull Llama 3.1 8B model
- Test basic text generation
- Deliverable: Can generate commentary text locally

**Sprint 3.2:** Coqui TTS on Windows
- Install Coqui TTS
- Configure NVIDIA GPU acceleration
- Test speech synthesis
- Deliverable: Can generate speech from text

### Phase 4: Event Detection (Weeks 7-8)
**Goal:** Identify key moments in replays

**Sprint 4.1:** Event Parser
- Parse replay events with sc2reader
- Classify event types and importance
- Build event timeline
- Deliverable: Structured event data

**Sprint 4.2:** Camera Director AI
- Priority scoring algorithm
- Camera path generation
- Conflict resolution (multiple events)
- Deliverable: Automated camera script

### Phase 5: AI Commentary (Weeks 9-11)
**Goal:** Generate commentary using local LLM

**Sprint 5.1:** Commentary Generator
- Prompt engineering for Llama
- Game state integration
- Fact validation system
- Deliverable: Text commentary for key moments

**Sprint 5.2:** Audio Synthesis
- Convert text to speech with Coqui
- Sync with video timeline
- Audio mixing and normalization
- Deliverable: Commentary audio track

**Sprint 5.3:** Quality Validation
- Automated fact-checking
- Hallucination detection
- Manual review workflow
- Deliverable: Quality control system

### Phase 6: Video Production (Weeks 12-14)
**Goal:** Complete video with commentary and overlays

**Sprint 6.1:** Overlay System
- HUD elements (supply, resources, upgrades)
- Player info bars
- Minimap overlay
- Deliverable: Rendered overlays

**Sprint 6.2:** Video Assembly
- Combine video + audio + overlays
- Final encoding (H.264, 1080p60)
- Thumbnail generation
- Deliverable: Complete cast video

**Sprint 6.3:** Quality Control
- Automated validation checks
- Manual review process
- Error reporting
- Deliverable: QA pipeline

### Phase 7: YouTube Integration (Weeks 15-16)
**Goal:** Automated upload pipeline

**Sprint 7.1:** YouTube API
- OAuth authentication setup
- Upload functionality
- Playlist management
- Deliverable: Can upload videos programmatically

**Sprint 7.2:** Metadata Generation
- Title generation (AI-assisted)
- Description and tags
- Thumbnail creation
- Deliverable: Fully automated publishing

### Phase 8: Testing (Weeks 17-18)
**Goal:** Process 50+ diverse replays

**Sprint 8.1:** Test Suite
- Unit tests for all components
- Integration tests
- Replay diversity testing
- Deliverable: >80% test coverage

**Sprint 8.2:** Batch Processing
- Test various matchups (TvZ, PvP, etc.)
- Different game lengths (5min - 60min)
- Edge cases (early GG, disconnects)
- Deliverable: >95% success rate

### Phase 9: Optimization (Weeks 19-20)
**Goal:** Improve speed and quality

**Sprint 9.1:** Performance Optimization
- Parallel processing where possible
- Caching strategies
- GPU optimization
- Deliverable: <25 min processing time for 20-min replay

**Sprint 9.2:** Quality Tuning
- Commentary improvements
- Camera work refinement
- Audio quality enhancement
- Deliverable: User feedback >4/5 stars

### Phase 10: Production Launch (Week 21)
**Goal:** Go live with automated system

- Final end-to-end testing
- Documentation completion
- First batch upload (10 videos)
- Channel announcement
- **Deliverable: Live YouTube channel with automated uploads**

---

## 📊 Resource Requirements

### Hardware (Already Available)
- **GPU:** RTX 3060+ 12GB VRAM ✅
- **RAM:** 32GB ✅
- **Storage:** 1TB SSD ✅
- **CPU:** 8+ cores ✅
- **OS:** Windows 10/11 ✅

### Software (All Free)
- Python 3.11+
- Poetry (dependency management)
- StarCraft II (installed)
- Ollama (Llama 3.1)
- Coqui TTS
- FFmpeg
- OBS Studio (optional for capture)

### Costs
- **Operational:** $0/month
- **Electricity:** ~$20-30/month
- **Total:** **$0/month** ✅

---

## 🎯 Success Metrics

### Technical
- ✅ 95%+ replay processing success rate
- ✅ 90%+ factual accuracy in commentary
- ✅ <35 min processing time per 20-min replay
- ✅ 1080p60 video output

### Quality
- ✅ Commentary: 7+/10 rating
- ✅ Voice: 7+/10 rating
- ✅ Camera work: 8+/10 rating
- ✅ Overall: "Good enough for automated content"

### Business (Future)
- 1k subscribers by month 3
- 10k subscribers by month 6
- 50% avg watch time
- YouTube monetization enabled

---

## ⚠️ Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Windows SC2 replay fails | **CRITICAL** | Test Sprint 1.4 immediately, pivot if needed |
| Llama quality too low | High | Test early (Sprint 3.1), can fine-tune or use larger model |
| Coqui voice quality poor | Medium | Multiple voice options, can adjust settings |
| SC2 crashes | Medium | Checkpoint system, auto-restart |
| Processing too slow | Low | Optimization in Phase 9 |
| Screen capture performance | Medium | Test multiple methods (FFmpeg, OBS, Windows Game Bar) |

---

## 📝 Milestones

- ✅ **Week 0**: Planning complete, architecture decided (Windows native)
- **Week 2**: PoC video generated from replay ← **CRITICAL MILESTONE**
- **Week 6**: Local AI working (Llama + Coqui)
- **Week 11**: First AI-commented video
- **Week 14**: Full pipeline working end-to-end
- **Week 18**: Testing complete, 95%+ success rate
- **Week 21**: Production launch, channel goes live

---

**See `TECHNICAL.md` for technical details**  
**See `docs/dev/CURRENT_SPRINT.md` for active work**  
**See `docs/dev/DEVLOG.md` for history**
