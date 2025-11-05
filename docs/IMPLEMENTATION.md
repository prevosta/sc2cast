# SC2Cast - Implementation Plan

**All planning, timeline, and status in one place.**

---

## 🎯 Current Status

**Phase:** Phase 1 - Proof of Concept  
**Sprint:** 1.4 In Progress ⏳ (Video Recording PoC)  
**Started:** November 5, 2025  
**Progress:** 3/4 Phase 1 sprints complete (75%)

### Completed
- ✅ Sprint 1.1: Docker Environment Setup (GPU + SC2 working)
- ✅ Sprint 1.2: Replay Parser (metadata extraction)
- ✅ Sprint 1.3: Event Extraction (key moments identified)

### In Progress
- ⏳ Sprint 1.4: Video Recording PoC - **HIGHEST TECHNICAL RISK**
  - Goal: Prove SC2 + Docker + FFmpeg → MP4 video file
  - If this fails, entire project needs pivot

### Next
- Phase 2: Video Foundation (if PoC succeeds)

---

## 📅 Implementation Timeline (20 Weeks)

### Phase 1: Proof of Concept (Weeks 1-2) ⏳ 75% Complete
**Goal:** Prove Docker + SC2 + video generation works

**Sprint 1.1:** Docker Environment ✅ COMPLETE
- Docker + SC2 + GPU support
- Deliverable: Container runs, GPU accessible
- **Completed:** Nov 5, 2025

**Sprint 1.2:** Basic Replay Processing ✅ COMPLETE
- Parse demo replay file
- Extract basic info (players, duration, map)
- Deliverable: JSON output of replay data
- **Completed:** Nov 5, 2025

**Sprint 1.3:** Event Extraction ✅ COMPLETE
- Extract game events (builds, battles, expansions)
- Categorize by priority (high/medium/low)
- Identify key moments for camera
- Deliverable: Events timeline with filtering
- **Completed:** Nov 5, 2025

**Sprint 1.4:** Video Recording PoC ⏳ IN PROGRESS
- Install video dependencies (Xvfb, FFmpeg, python-sc2)
- Launch SC2 headless, open replay programmatically
- Record 10-second video clip with FFmpeg
- Deliverable: MP4 file in output/ directory
- **Risk Level:** 🔴 HIGHEST - This is make-or-break for the project
- **Started:** Nov 5, 2025

**Sprint 1.4:** Video PoC (Week 2) ⏳ NEXT
- Record short video clip from replay
- Basic FFmpeg encoding
- Deliverable: First video file (no commentary)

### Phase 2: Video Foundation (Weeks 3-4)
**Goal:** Record and encode video from replay

**Sprint 2.1:** SC2 Control
- Control SC2 client via python-sc2
- Basic camera movement
- Deliverable: Can watch replay programmatically

**Sprint 2.2:** Video Recording
- Capture frames
- Encode with FFmpeg
- Deliverable: First video file (no commentary, no overlays)

### Phase 3: Local AI Setup (Weeks 5-6)
**Goal:** Get Llama + Coqui working

**Sprint 3.1:** Ollama Integration
- Install Ollama
- Pull Llama 3.1 8B
- Test basic generation
- Deliverable: Can generate text locally

**Sprint 3.2:** Coqui TTS Integration
- Install Coqui TTS
- Configure GPU acceleration
- Test speech synthesis
- Deliverable: Can generate speech locally

### Phase 4: Event Detection (Weeks 7-8)
**Goal:** Identify key moments in replays

**Sprint 4.1:** Event Parser
- Parse replay events (battles, expansions, tech)
- Classify event types
- Deliverable: Timeline of key events

**Sprint 4.2:** Camera Director
- Priority scoring algorithm
- Camera path generation
- Deliverable: Automated camera script

### Phase 5: AI Commentary (Weeks 9-11)
**Goal:** Generate commentary using local LLM

**Sprint 5.1:** Commentary Generator
- Prompt engineering for Llama
- Game state integration
- Deliverable: Text commentary for key moments

**Sprint 5.2:** Validation System
- Fact-checking against game state
- Hallucination detection
- Deliverable: Validated commentary

**Sprint 5.3:** Audio Synthesis
- Convert text to speech (Coqui)
- Sync with video timeline
- Deliverable: Audio track

### Phase 6: Video Production (Weeks 12-14)
**Goal:** Complete video with commentary

**Sprint 6.1:** Overlay System
- HUD elements (supply, resources)
- Player info bars
- Deliverable: Overlays rendered

**Sprint 6.2:** Integration
- Combine video + audio + overlays
- Final encoding
- Deliverable: Complete cast video

**Sprint 6.3:** Quality Control
- Automated checks
- Manual review process
- Deliverable: QA system

### Phase 7: YouTube Integration (Weeks 15-16)
**Goal:** Automated upload

**Sprint 7.1:** API Integration
- OAuth authentication
- Upload functionality
- Deliverable: Can upload videos

**Sprint 7.2:** Metadata Generation
- Titles, descriptions, tags
- Thumbnails
- Deliverable: Fully automated pipeline

### Phase 8: Testing (Weeks 17-18)
**Goal:** Process 50+ diverse replays

**Sprint 8.1:** Testing Suite
- Unit tests
- Integration tests
- Deliverable: Test coverage >80%

**Sprint 8.2:** Replay Processing
- Test with various matchups
- Different game lengths
- Deliverable: Success rate >95%

### Phase 9: Optimization (Weeks 19-20)
**Goal:** Improve speed and quality

**Sprint 9.1:** Performance
- Parallel processing
- Caching strategies
- Deliverable: <25 min processing time

**Sprint 9.2:** Quality Tuning
- Commentary improvements
- Camera refinements
- Deliverable: User feedback >4/5

### Phase 10: Production Launch (Week 21)
**Goal:** Go live

- Final testing
- Documentation
- First batch of videos published
- **Deliverable: Live YouTube channel**

---

## 📊 Resource Requirements

### Hardware (Already Available)
- GPU: RTX 3060+ 12GB VRAM ✅
- RAM: 32GB ✅
- Storage: 1TB SSD ✅
- CPU: 8+ cores ✅

### Software (All Free)
- Docker Desktop ✅
- Ollama (Llama 3.1) 
- Coqui TTS
- Python 3.11+
- FFmpeg

### Costs
- **Operational**: $0/month
- **Electricity**: ~$20-30/month
- **Total**: **$0/month** ✅

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
| Llama quality too low | High | Test early (Sprint 3.1), can fine-tune |
| Coqui voice quality poor | Medium | Multiple voice options, can adjust |
| SC2 crashes | Medium | Checkpoint system, auto-restart |
| Processing too slow | Low | Optimization in Phase 9 |

---

## 📝 Milestones

- ✅ **Week 0**: Planning complete
- ⏳ **Week 2**: PoC video generated
- **Week 6**: Local AI working
- **Week 11**: First AI-commented video
- **Week 14**: Full pipeline working
- **Week 18**: Testing complete
- **Week 21**: Production launch

---

**See `TECHNICAL.md` for technical details**  
**See `docs/dev/CURRENT_SPRINT.md` for active work**  
**See `docs/dev/DEVLOG.md` for history**
