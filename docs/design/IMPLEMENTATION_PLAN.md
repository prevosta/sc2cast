# Implementation Plan - SC2Cast (Zero-Budget Edition)

## 💰 Budget Constraint
**ZERO external API costs** - All AI/ML runs locally using open-source models:
- **LLM**: Llama 3.1 8B (via Ollama)
- **TTS**: Coqui TTS
- **Hardware**: Already available (RTX 3060+ 12GB VRAM, 32GB RAM)

---

## Phase 1: Proof of Concept - Docker + Video Generation (Weeks 1-2)

**GOAL**: Prove we can generate a basic video from a replay file using Docker

### Sprint 1.1: Docker Environment Setup
- [ ] Initialize Git repository
- [ ] Create Dockerfile with:
  - [ ] NVIDIA CUDA base image
  - [ ] Python 3.11+ installation
  - [ ] StarCraft II client installation
  - [ ] Xvfb for headless rendering
  - [ ] FFmpeg for video encoding
- [ ] Set up docker-compose.yml with GPU support
- [ ] Configure VS Code dev container (.devcontainer.json)
- [ ] Test SC2 launches inside container
- [ ] Verify GPU is accessible (nvidia-smi)

**Deliverable**: SC2 runs in Docker container with GPU access ✅

### Sprint 1.2: Basic Replay Playback & Recording
- [ ] Install python-sc2 library
- [ ] Create minimal script to:
  - [ ] Load replay file (use provided demo replay)
  - [ ] Start SC2 observer mode
  - [ ] Play replay from start to finish
  - [ ] Capture frames using OpenCV
  - [ ] Save frames as video using FFmpeg
- [ ] Test with demo replay: `4323200_changeling_Mike_MagannathaAIE_v2.SC2Replay`
- [ ] Verify output video plays correctly
- [ ] Measure recording time vs replay length

**Deliverable**: First generated video (no commentary, no overlays, just raw replay recording) 🎥

**SUCCESS CRITERIA**: Can run `docker-compose up` and get a video file from the demo replay!

**Key Files to Create**:
```
src/
├── __init__.py
├── analysis/
│   ├── __init__.py
│   ├── replay_analyzer.py
│   ├── event_detector.py
│   └── statistics.py
├── models/
│   ├── __init__.py
│   ├── replay_data.py
│   └── game_events.py
└── utils/
    ├── __init__.py
    └── logger.py
```

## Phase 2: Replay Analysis & Overlays (Weeks 3-4)

### Sprint 2.1: Replay Analysis with sc2reader
- [ ] Install and test sc2reader library
- [ ] Create ReplayAnalyzer class
- [ ] Parse demo replay and extract:
  - [ ] Player names, races, result
  - [ ] Game length and map name
  - [ ] Timeline of events (deaths, buildings)
  - [ ] Supply/worker counts over time
- [ ] Implement basic event filtering
- [ ] Export analysis to JSON
- [ ] Unit tests for replay parsing

**Deliverable**: Complete replay analysis of demo replay with JSON output

### Sprint 2.2: Basic Overlays
- [ ] Create OverlayRenderer class
- [ ] Add to video recording:
  - [ ] Player names at top (with races)
  - [ ] Supply counters (e.g., "150/200")
  - [ ] Game timer
  - [ ] Simple graphics (rectangles, text with OpenCV)
- [ ] Integrate overlays into frame capture pipeline
- [ ] Test overlay rendering performance
- [ ] Generate second video with overlays

**Deliverable**: Video with basic HUD overlays 🎮

**Key Files**:
```
src/camera/
├── __init__.py
├── director.py
├── priority_system.py
├── transition_generator.py
└── camera_script.py
```

## Phase 3: Local AI Setup (Weeks 5-6)

### Sprint 3.1: Local LLM Setup (Llama 3.1)
- [ ] Install Ollama in Docker container
- [ ] Pull Llama 3.1 8B quantized model (Q4_K_M)
- [ ] Create LocalLLMClient class
- [ ] Test generation with SC2 prompts:
  - [ ] "Describe a marine push"
  - [ ] "What is a Zergling rush?"
- [ ] Benchmark inference speed (tokens/sec)
- [ ] Measure VRAM usage
- [ ] Implement prompt caching for common phrases
- [ ] Test batch generation

**Deliverable**: Working local LLM generating SC2 commentary text ✅

### Sprint 3.2: Local TTS Setup (Coqui)
- [ ] Install Coqui TTS in Docker
- [ ] Download VCTK multi-speaker model
- [ ] Create LocalTTSEngine class
- [ ] Test synthesis with sample text
- [ ] Try different speakers (male voices for casting)
- [ ] Benchmark synthesis speed (real-time factor)
- [ ] Test emotion modifications (excited vs calm)
- [ ] Generate test audio files

**Deliverable**: Working local TTS generating natural speech 🎙️

**Deliverable**: Complete overlay system with all HUD elements

## Phase 4: Camera Director & Key Moments (Weeks 7-8)

### Sprint 4.1: Key Moment Detection
- [ ] Implement battle detection (spatiotemporal clustering)
- [ ] Detect base expansions/destructions
- [ ] Identify harassment events
- [ ] Calculate priority scores (1-10 scale)
- [ ] Test on demo replay
- [ ] Tune detection parameters
- [ ] Export key moments to JSON

**Deliverable**: List of key moments from demo replay with timestamps

### Sprint 4.2: Camera Director
- [ ] Create CameraDirector class
- [ ] Implement priority-based scene selection
- [ ] Add smooth transitions (Bezier curves)
- [ ] Handle conflict resolution (overlapping events)
- [ ] Generate camera script (JSON with timestamps & positions)
- [ ] Visualize camera path
- [ ] Integrate with video recording (camera follows script)

**Deliverable**: Video with intelligent camera movement 📹

**Key Files**:
```
src/recording/
├── __init__.py
├── sc2_controller.py
├── frame_capture.py
├── overlay_renderer.py
└── video_encoder.py
```

## Phase 4: AI Commentary (Weeks 8-10)

### Sprint 4.1: Training Data Collection
- [ ] YouTube transcript scraper
- [ ] Parse and structure transcripts
- [ ] Align transcripts with game states
- [ ] Build training dataset
- [ ] Categorize commentary types
- [ ] Create embeddings database (RAG)
- [ ] Quality filtering

**Deliverable**: Structured training corpus of 100+ hours

### Sprint 4.2: LLM Integration
- [ ] Set up OpenAI/Anthropic API
- [ ] Design prompt templates
- [ ] Implement context building
- [ ] Few-shot prompting system
- [ ] Fallback strategies
- [ ] Response validation
- [ ] Cost tracking and optimization

**Deliverable**: Working LLM-based commentary generator

### Sprint 4.3: Commentary Script Generation
- [ ] Integrate analysis + LLM
- [ ] Generate time-synced scripts
- [ ] Emotion and tone tagging
- [ ] Fact-checking against game state
- [ ] Natural flow and transitions
- [ ] A/B testing framework
- [ ] Human evaluation setup

**Deliverable**: Complete commentary generation pipeline

**Key Files**:
```
src/commentary/
├── __init__.py
├── generator.py
├── llm_client.py
├── prompt_builder.py
├── training_corpus.py
├── rag_database.py
└── validators.py
```

## Phase 5: Audio Synthesis (Weeks 11-12)

### Sprint 5.1: TTS Implementation
- [ ] Evaluate TTS options (Coqui, ElevenLabs)
- [ ] Set up chosen TTS engine
- [ ] Voice selection and customization
- [ ] SSML/prosody implementation
- [ ] Batch processing optimization
- [ ] Quality assessment
- [ ] Fallback TTS option

**Deliverable**: Working TTS system with quality voice

### Sprint 5.2: Audio Post-Processing
- [ ] Audio normalization
- [ ] Background music integration
- [ ] Volume mixing and ducking
- [ ] Pause insertion
- [ ] Final audio export
- [ ] Sync validation with video

**Deliverable**: Complete audio pipeline with music

**Key Files**:
```
src/audio/
├── __init__.py
├── tts_engine.py
├── audio_mixer.py
├── music_selector.py
└── audio_processor.py
```

## Phase 6: YouTube Automation (Weeks 12-13)

### Sprint 6.1: YouTube Upload Integration
- [ ] Set up YouTube Data API v3
- [ ] Implement OAuth 2.0 authentication
- [ ] Create YouTubeUploader class
- [ ] Test manual video upload
- [ ] Generate metadata (title, description, tags)
- [ ] Create thumbnail from key frame
- [ ] Handle rate limits and errors
- [ ] Verify upload success

**Deliverable**: Manual YouTube upload working ✅

### Sprint 6.2: AI Arena Replay Acquisition (Optional)
- [ ] Create AIArenaClient class
- [ ] Implement replay downloading
- [ ] Filter by ELO/date
- [ ] Queue management (SQLite database)
- [ ] Status tracking
- [ ] Error handling and retries

**Deliverable**: Automated replay acquisition (if desired) 📥

## Phase 7: Pipeline Integration & CLI (Weeks 14-15)

### Sprint 7.1: Main Pipeline Orchestrator
- [ ] Create SC2CastOrchestrator class
- [ ] Implement stage-by-stage execution:
  1. Load replay
  2. Analyze events
  3. Generate camera script
  4. Generate commentary
  5. Synthesize audio
  6. Record video
  7. Upload to YouTube
- [ ] Add progress tracking and logging
- [ ] Implement error handling and recovery
- [ ] Add checkpoints (resume from failure)

**Deliverable**: End-to-end automation 🚀

### Sprint 7.2: CLI & Configuration
- [ ] Create CLI using Click/Typer
- [ ] Commands:
  - `sc2cast process <replay>` - Process single replay
  - `sc2cast batch <folder>` - Process multiple replays
  - `sc2cast status` - Check pipeline status
- [ ] YAML configuration system
- [ ] Environment variable support
- [ ] Logging configuration

**Deliverable**: User-friendly command-line interface 🖥️

## Phase 8: Testing & Optimization (Weeks 16-17)

### Sprint 8.1: Testing Suite
- [ ] Unit tests for all modules (pytest)
- [ ] Integration tests
- [ ] Test with multiple replay types:
  - [ ] Different matchups (TvZ, PvP, ZvZ, etc.)
  - [ ] Different game lengths (5min rush vs 30min macro)
  - [ ] Different maps
- [ ] Mock components for faster tests
- [ ] Coverage reporting (aim for 70%+)
- [ ] CI/CD setup (GitHub Actions)

**Deliverable**: Comprehensive test suite ✅

### Sprint 8.2: Performance Optimization
- [ ] Profile bottlenecks
- [ ] Optimize LLM inference (quantization, caching)
- [ ] Optimize TTS synthesis (batch processing)
- [ ] Optimize video encoding (GPU acceleration)
- [ ] Reduce memory usage
- [ ] Benchmark performance improvements
- [ ] Document optimization results

**Deliverable**: Faster, more efficient pipeline ⚡

## Phase 9: Quality & Documentation (Weeks 18-19)

### Sprint 9.1: Quality Improvements
- [ ] Manual review of 10+ generated videos
- [ ] Tune commentary prompts based on output
- [ ] Improve camera director logic
- [ ] Enhance overlay visuals
- [ ] Fine-tune TTS emotion mapping
- [ ] Add more comprehensive error messages
- [ ] Implement quality validation checks

**Deliverable**: High-quality, polished output 💎

### Sprint 9.2: Documentation
- [ ] User guide (how to use the system)
- [ ] Developer documentation (code structure)
- [ ] API documentation (module interfaces)
- [ ] Configuration guide
- [ ] Troubleshooting guide
- [ ] Contributing guidelines
- [ ] README with examples

**Deliverable**: Complete documentation 📚

## Phase 10: Production Preparation (Week 20)

### Sprint 10.1: Production Setup
- [ ] Process 20+ different replays end-to-end
- [ ] Collect quality metrics
- [ ] Fix remaining bugs
- [ ] Optimize Docker image size
- [ ] Set up monitoring/logging
- [ ] Create backup strategy
- [ ] Write deployment instructions

**Deliverable**: Production-ready system 🎉

### Sprint 10.2: Launch & Iteration
- [ ] Upload first batch of videos to YouTube
- [ ] Monitor performance and errors
- [ ] Collect community feedback
- [ ] Create issue tracker
- [ ] Plan v1.1 improvements
- [ ] Document lessons learned

**Deliverable**: Live system generating videos! 🚀

---

## Development Milestones (Updated for Zero-Budget)

### ✅ Milestone 1: Proof of Concept (Week 2)
- Docker environment working
- SC2 replay plays and records to video file
- **SUCCESS**: Can generate a basic video from demo replay

### ✅ Milestone 2: Basic Intelligence (Week 4)
- Replay analysis extracts key information
- Basic overlays render on video
- **SUCCESS**: Video has player info and supply counters

### ✅ Milestone 3: Local AI Working (Week 6)
- Llama 3.1 generates SC2 commentary text
- Coqui TTS synthesizes natural speech
- **SUCCESS**: Can generate commentary audio locally

### ✅ Milestone 4: Smart Camera (Week 8)
- Camera director identifies key moments
- Video follows intelligent camera script
- **SUCCESS**: Camera shows battles and important events

### ✅ Milestone 5: Complete Pipeline (Week 11)
- Full video with AI commentary and smart camera
- **SUCCESS**: First professional-quality AI-casted video

### ✅ Milestone 6: Automation (Week 13)
- YouTube upload working
- **SUCCESS**: Can process replay and upload automatically

### ✅ Milestone 7: Production Ready (Week 20)
- All features complete, tested, and documented
- **SUCCESS**: System reliably generates quality videos

## Resource Requirements (Zero-Budget Edition)

### Development Team
- **Full-time Developer**: 1 person
- **Hardware**: Already available (no additional cost)
- **Budget**: $0/month operational costs

### Hardware Requirements (Available)
- **GPU**: NVIDIA RTX 3060+ (12GB+ VRAM)
  - Llama 3.1 8B: ~10GB VRAM
  - Coqui TTS: ~2GB VRAM
  - Video encoding: Can use CPU or GPU
- **RAM**: 32GB minimum (16GB system + 16GB for models)
- **Storage**: 1TB+ SSD
  - Models: ~50GB
  - Replays: ~100GB
  - Workspace/temp: ~500GB
  - Output videos: ~350GB
- **CPU**: 8+ cores recommended
- **Internet**: Stable connection for YouTube uploads

### Software Costs
- **LLM**: Llama 3.1 8B - **FREE** (open-source)
- **TTS**: Coqui TTS - **FREE** (open-source)
- **SC2 Client**: **FREE** (via Linux installer)
- **All Libraries**: **FREE** (open-source)
- **YouTube API**: **FREE** (within quotas: ~6 uploads/day)
- **TOTAL**: **$0/month** 🎉

### Electricity Cost (Estimated)
- GPU power: ~200W under load
- 8 hours/day processing: ~$15-30/month
- (This is unavoidable with any approach)

## Risk Mitigation (Zero-Budget Edition)

### Technical Risks
1. **SC2 Client Stability**: Crashes in headless mode
   - *Mitigation*: Checkpoint system, auto-restart, Xvfb configuration

2. **Local LLM Quality**: May not match GPT-4 quality
   - *Mitigation*: Prompt engineering, fine-tuning on SC2 content, accept slightly lower quality

3. **TTS Voice Quality**: More synthetic than ElevenLabs
   - *Mitigation*: Voice selection, post-processing, emotion tuning, acceptable tradeoff

4. **Processing Time**: Local inference slower than APIs
   - *Mitigation*: Model quantization, caching, parallel processing, still acceptable (~34 min for 20 min replay)

5. **VRAM Limitations**: Running out of GPU memory
   - *Mitigation*: Use quantized models (Q4), process stages sequentially, clear cache between stages

### Business Risks
1. **YouTube Policy Violations**: AI content restrictions
   - *Mitigation*: Follow YT guidelines, proper disclosure, quality control

2. **Copyright Issues**: Game content or music
   - *Mitigation*: Use royalty-free music, proper attribution

3. **Low Engagement**: Videos don't get views
   - *Mitigation*: Quality focus, SEO optimization, community engagement

## Success Criteria

### Phase 1-2 Success
- [ ] Can parse any SC2 replay
- [ ] Identifies 90%+ of major battles
- [ ] Camera script makes logical sense

### Phase 3 Success
- [ ] Records full game without crashes
- [ ] Overlays are readable and accurate
- [ ] Video quality is broadcast-worthy (1080p60)

### Phase 4-5 Success
- [ ] Commentary is contextually relevant
- [ ] No major factual errors
- [ ] Audio sounds natural and engaging

### Phase 6-7 Success
- [ ] Can process replays automatically
- [ ] Successfully uploads to YouTube
- [ ] Pipeline runs without manual intervention

### Phase 8-10 Success
- [ ] Processes 10+ replays/day reliably
- [ ] <5% failure rate
- [ ] Videos receive positive community feedback
- [ ] System is maintainable and documented

## Next Steps

1. **Immediate**: Set up Docker environment and project structure
2. **Week 1**: Get sc2reader working, parse first replay
3. **Week 2**: Implement key moment detection
4. **Week 3**: Begin SC2 controller integration
5. **Review**: Weekly progress review, adjust timeline as needed
