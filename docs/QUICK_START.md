# SC2Cast - Quick Start Guide

## Executive Summary

**SC2Cast** is an automated system that transforms StarCraft II replays into professionally-commented video content using AI, then publishes to YouTube.

## 💰 **ZERO-BUDGET APPROACH**
**$0/month operational costs** using 100% open-source, locally-runnable AI:
- **LLM**: Llama 3.1 8B (via Ollama) - FREE
- **TTS**: Coqui TTS - FREE
- **All other components**: Open-source (sc2reader, FFmpeg, python-sc2) - FREE
- **Hardware**: Already available (RTX 3060+ 12GB VRAM, 32GB RAM)

### Pipeline
```
Replay → Analysis → Camera Direction → AI Commentary (Local Llama) → Audio Synthesis (Coqui) → Video Recording → YouTube Upload
```

### Time to Process (Zero-Budget)
- **Analysis**: 30 seconds
- **Commentary Generation**: 4 minutes (Local Llama 3.1)
- **Audio Synthesis**: 2 minutes (Coqui TTS)
- **Video Recording**: ~1x replay length (20 min game = 20 min)
- **Total**: ~34 minutes per replay (only 10% slower than APIs!)

### Resource Requirements
- 32GB RAM (16GB system + 16GB for models)
- NVIDIA GPU (RTX 3060+ 12GB VRAM minimum)
- Docker with GPU support
- Python 3.11+
- **Cost: $0 (already available)**

---

## Key Technical Decisions

### 1. Replay Analysis: **sc2reader**
- Pure Python, no SC2 client needed
- Fast parsing (30 sec for 20 min replay)
- Extracts: events, units, buildings, statistics
- **Cost: FREE** ✅

### 2. Video Recording: **python-sc2**
- Controls SC2 client via API
- Camera positioning and movement
- Frame capture and overlay rendering
- **Cost: FREE** ✅

### 3. Commentary: **Llama 3.1 8B (Local via Ollama)**
- Open-source, runs locally on GPU
- Good quality for factual game commentary
- No API costs, no external dependencies
- **Cost: $0/month** ✅

### 4. Audio: **Coqui TTS (Local)**
- Free, open-source neural TTS
- Acceptable quality for game casting
- Runs locally (GPU accelerated)
- **Cost: $0/month** ✅

### 5. Video Encoding: **FFmpeg**
- Industry standard
- 1080p60 target
- H.264 codec for YouTube
- **Cost: FREE** ✅

### 6. Container: **Docker + VS Code Dev Container**
- Reproducible environment
- GPU passthrough for acceleration (NVIDIA CUDA)
- Easy development workflow
- **Cost: FREE** ✅

---

## Project Structure

```
sc2cast/
├── src/
│   ├── acquisition/          # AI Arena replay downloading
│   │   ├── ai_arena_client.py
│   │   └── replay_queue.py
│   │
│   ├── analysis/             # Replay parsing and event detection
│   │   ├── replay_analyzer.py
│   │   ├── event_detector.py
│   │   └── statistics.py
│   │
│   ├── camera/               # Camera director system
│   │   ├── director.py
│   │   ├── priority_system.py
│   │   └── camera_script.py
│   │
│   ├── commentary/           # AI commentary generation
│   │   ├── generator.py
│   │   ├── llm_client.py
│   │   ├── prompt_builder.py
│   │   └── rag_database.py
│   │
│   ├── audio/                # Text-to-speech and mixing
│   │   ├── tts_engine.py
│   │   ├── audio_mixer.py
│   │   └── music_selector.py
│   │
│   ├── recording/            # Video capture and encoding
│   │   ├── sc2_controller.py
│   │   ├── frame_capture.py
│   │   ├── overlay_renderer.py
│   │   └── video_encoder.py
│   │
│   ├── upload/               # YouTube publishing
│   │   ├── youtube_client.py
│   │   ├── metadata_generator.py
│   │   └── thumbnail_generator.py
│   │
│   ├── models/               # Data models
│   │   ├── replay_data.py
│   │   ├── game_events.py
│   │   └── camera_script.py
│   │
│   ├── orchestrator.py       # Main pipeline coordination
│   ├── config.py             # Configuration management
│   └── cli.py                # Command-line interface
│
├── config/
│   ├── default_config.yaml
│   └── config_schema.json
│
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .devcontainer.json
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│
├── models/                   # Trained models (LLM adapters, etc.)
├── transcripts/              # Training corpus for commentary
├── replays/                  # Input replay files
├── output/                   # Generated videos
│
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## Critical Implementation Details

### Camera Director Algorithm

**Priority Scoring**:
```python
PRIORITY_WEIGHTS = {
    'major_engagement': 10,
    'base_destruction': 9,
    'tech_completion': 8,
    'drop_harassment': 7,
    'expansion': 6,
    'scout': 4,
}

def calculate_priority(event):
    base_priority = PRIORITY_WEIGHTS[event.type]
    
    # Modifiers
    if event.supply_engaged > 100:
        base_priority += 2
    
    if event.game_time > 1200:  # Late game
        base_priority += 1
    
    return min(base_priority, 10)
```

**Conflict Resolution**:
- If multiple high-priority events overlap, use split-screen or rapid cuts
- Always prioritize army engagements over single-unit harassment
- Use "picture-in-picture" for secondary simultaneous action

---

### Commentary Generation

**Prompt Structure**:
```python
prompt = f"""
You are a StarCraft II commentator with {caster_style} style.

GAME CONTEXT (verified facts only):
- Time: {format_time(game_time)}
- Players: {player1.name} ({player1.race}) vs {player2.name} ({player2.race})
- Supply: {player1.supply} vs {player2.supply}
- Economy: {player1.workers} workers vs {player2.workers} workers
- Current Event: {event.description}

RECENT HISTORY:
{format_recent_events(last_3_events)}

Generate 2-3 sentences of engaging commentary for this moment.
Focus on: {focus_areas}

Output JSON:
{{
  "text": "commentary here",
  "emotion": "excited|neutral|tense|analytical",
  "speed": 1.0-1.5
}}
"""
```

**Validation**:
```python
def validate_commentary(commentary, game_state):
    # Check for factual errors
    if mentions_units_not_in_game(commentary, game_state):
        return False
    
    # Check for repetition
    if too_similar_to_recent_commentary(commentary):
        return False
    
    # Check length
    if len(commentary.split()) > 100:
        return False
    
    return True
```

---

### Video Recording

**Overlay Rendering**:
```python
class OverlayRenderer:
    def render_frame(self, game_frame, game_state):
        # Start with base SC2 frame
        img = game_frame.copy()
        
        # Top bar: Player info
        self.draw_player_info(img, game_state.players)
        
        # Top-right: Supply
        self.draw_supply(img, game_state.supply, position=(1700, 50))
        
        # Resources
        self.draw_resources(img, game_state.minerals, game_state.gas)
        
        # Army value comparison
        self.draw_army_value(img, game_state.army_values)
        
        # Production tab (if active)
        if game_state.show_production:
            self.draw_production(img, game_state.production_tab)
        
        return img
```

---

### YouTube Upload

**Metadata Generation**:
```python
def generate_metadata(replay_data):
    # Title with SEO
    title = f"{replay_data.player1} ({replay_data.race1}) vs "
            f"{replay_data.player2} ({replay_data.race2}) - "
            f"{replay_data.map_name} | SC2 AI Cast"
    
    # Description with timestamps
    description = f"""
AI-Generated StarCraft II Commentary

🎮 Players:
  • {replay_data.player1} playing {replay_data.race1}
  • {replay_data.player2} playing {replay_data.race2}

🗺️ Map: {replay_data.map_name}
⏱️ Game Length: {format_duration(replay_data.game_length)}

⚔️ Key Moments:
{generate_timestamp_list(replay_data.key_moments)}

📊 Final Stats:
  • APM: {replay_data.player1.apm} vs {replay_data.player2.apm}
  • Army Value: {replay_data.max_army_value[0]} vs {replay_data.max_army_value[1]}

This video was automatically generated using AI analysis and commentary.

#StarCraft2 #SC2 #AIGenerated #{replay_data.matchup} #{replay_data.race1} #{replay_data.race2}
"""
    
    tags = [
        "StarCraft 2", "SC2", "StarCraft II",
        replay_data.race1, replay_data.race2, replay_data.matchup,
        replay_data.map_name, "AI Commentary", "Gaming",
        "Esports", "RTS", "Strategy"
    ]
    
    return {
        'title': title[:100],  # YouTube limit
        'description': description[:5000],
        'tags': tags[:30],
        'categoryId': '20',
        'privacyStatus': 'public'
    }
```

---

## Development Workflow

### 0. Prerequisites Setup (Zero-Budget)
```powershell
# Install Ollama (for Llama 3.1)
# Download from: https://ollama.com/download/windows
# Or use: winget install Ollama.Ollama

# Pull Llama 3.1 8B quantized model
ollama pull llama3.1:8b-q4_K_M

# Install Coqui TTS (inside Docker container later)
# pip install TTS

# Verify GPU available
nvidia-smi
```

### 1. Initial Setup
```powershell
# Clone repository
git clone <repo-url>
cd sc2cast

# Open in VS Code
code .

# VS Code will prompt to reopen in container
# (dev container auto-installs dependencies + CUDA support)
```

### 2. Test Local AI First (Proof of Concept)
```bash
# Inside container
python -m src.cli test-llm

# Expected output:
# Testing Ollama connection...
# ✓ Connected to Llama 3.1 8B (quantized)
# ✓ Generated sample commentary (3.2s)
# Quality: Acceptable for game casting

python -m src.cli test-tts

# Expected output:
# Testing Coqui TTS...
# ✓ Loading model (10s)
# ✓ Generated sample audio (2.5s)
# ✓ Saved to ./output/test_tts.wav
```

### 3. Test with Sample Replay
```bash
# Inside container
python -m src.cli process --replay ./4323200_changeling_Mike_MagannathaAIE_v2.SC2Replay --output ./output/

# Expected output:
# [1/7] Analyzing replay... ✓ (0:28)
# [2/7] Generating camera script... ✓ (0:12)
# [3/7] Creating commentary (Local Llama)... ✓ (4:05)
# [4/7] Synthesizing audio (Coqui TTS)... ✓ (2:10)
# [5/7] Recording video... ✓ (20:15)
# [6/7] Encoding final video... ✓ (2:30)
# [7/7] Complete! Video saved to ./output/sample_cast.mp4
```

### 4. Review Output
```bash
# Play video (inside container with X forwarding)
vlc ./output/sample_cast.mp4

# Check logs
tail -f logs/sc2cast.log
```

### 5. Iterate
```bash
# Modify commentary prompts for Llama
nano src/commentary/prompt_builder.py

# Re-run with debug mode
python -m src.cli process --replay ./4323200_changeling_Mike_MagannathaAIE_v2.SC2Replay --debug
```

---

## Configuration

### config/default_config.yaml
```yaml
sc2:
  path: /opt/StarCraftII
  resolution: [1920, 1080]
  fps: 60

llm:
  provider: ollama  # Local Llama 3.1
  model: llama3.1:8b-q4_K_M
  base_url: http://localhost:11434
  # No API key needed! ✅

tts:
  provider: coqui  # Local TTS
  model: tts_models/en/vctk/vits
  speaker: p326  # British male voice
  use_gpu: true

video:
  codec: libx264
  preset: medium
  crf: 23

youtube:
  credentials_path: ./credentials/youtube_token.json
  auto_upload: false  # Set true for automation
```

### Environment Variables
```bash
# .env file (much simpler with zero-budget!)
# OPENAI_API_KEY - NOT NEEDED! ✅
# ELEVENLABS_API_KEY - NOT NEEDED! ✅
YOUTUBE_CLIENT_ID=...
YOUTUBE_CLIENT_SECRET=...
```

---

## Testing Strategy

### Unit Tests
```bash
pytest tests/unit/ -v

# Test specific module
pytest tests/unit/test_camera_director.py -v
```

### Integration Tests
```bash
pytest tests/integration/ -v --slow
```

### End-to-End Test
```bash
# Process test replay through full pipeline
python -m src.cli process --replay ./tests/fixtures/test_replay.SC2Replay --test-mode
```

---

## Performance Benchmarks

### Target Performance (20-minute replay, Zero-Budget):
| Stage | Time | Notes |
|-------|------|-------|
| Analysis | 30s | sc2reader parsing |
| Camera Script | 10s | Event prioritization |
| Commentary | 4min | Local Llama 3.1 8B (quantized) |
| Audio Synthesis | 2min | Coqui TTS (GPU accelerated) |
| Video Recording | 20min | 1x playback speed |
| Encoding | 3min | FFmpeg H.264 |
| Upload | 5min | Network dependent |
| **Total** | **34min** | Only 10% slower than APIs! |

### Optimization Opportunities:
- **Parallel Commentary**: Generate segments concurrently (-30% LLM time → 2.8min)
- **Faster Playback**: Record at 2x during boring parts (-30% recording time → 14min)
- **GPU Encoding**: Use NVENC instead of libx264 (-60% encoding time → 1.2min)
- **Optimized**: **22-25 minutes total** for 20-minute replay

### Quality Comparison:
| Aspect | With APIs | Zero-Budget | Verdict |
|--------|-----------|-------------|---------|
| Commentary | 9/10 | 7.5/10 | Good enough ✅ |
| Voice Quality | 10/10 | 7/10 | Acceptable ✅ |
| Processing Time | 31min | 34min | Only +10% ✅ |
| **Cost** | **$300/mo** | **$0/mo** | **100% savings!** 🎉 |

---

## Deployment Options

### Option 1: Local Development Machine (RECOMMENDED - Zero Cost!)
- Run during off-hours on existing hardware
- Process 5-10 replays overnight
- RTX 3060+ 12GB VRAM + 32GB RAM (already available)
- **Cost: $0 upfront + $20-30/month electricity** ✅

### Option 2: Dedicated Server
- Build/buy workstation with RTX 4090 (if scaling beyond 10 videos/day)
- Run 24/7, process 50+ replays/day
- Cost: $3000 upfront + electricity

### Option 3: Cloud (AWS) - NOT RECOMMENDED (expensive!)
- g5.2xlarge instance ($1.21/hour)
- Spot instances for 60% savings
- Process on-demand
- Cost: $0.50-1.00 per replay

### Recommendation
- **Start**: Local development machine (already have hardware!) ✅
- **Scale**: Keep using local if <10 videos/day
- **Production**: Build dedicated server only if volume justifies (50+ videos/day)

---

## Risk Mitigation

### Technical Risks
1. **SC2 Crashes**: Checkpoint system, auto-restart
2. **Local LLM Quality**: Tune prompts, use larger model if needed (Llama 3.1 70B)
3. **Processing Bottleneck**: Queue system, parallel workers
4. **GPU Memory**: Use quantized models (Q4_K_M), monitor VRAM usage

### Business Risks
1. **YouTube Policy**: Clear AI disclosure, follow guidelines
2. **Low Engagement**: Focus on quality, community feedback
3. **Competition**: Differentiate with volume and zero-cost advantage

---

## Success Metrics

### Phase 1 (MVP):
- [ ] Process 1 replay end-to-end successfully
- [ ] Commentary is coherent and relevant
- [ ] Video quality is 1080p60
- [ ] Uploaded to YouTube

### Phase 2 (Alpha):
- [ ] Process 10 replays with <5% failure rate
- [ ] Average watch time >50% of video length
- [ ] Positive community feedback

### Phase 3 (Beta):
- [ ] Process 100 replays
- [ ] Automated pipeline (AI Arena → YouTube)
- [ ] 1000+ views on best videos

### Phase 4 (Production):
- [ ] Process 10+ replays/day reliably
- [ ] 10k+ channel subscribers
- [ ] Monetization enabled

---

## Next Actions

### Immediate (This Week):
1. Set up Docker environment
2. Install sc2reader, test parsing
3. Process first replay to extract events
4. Design camera director algorithm

### Short-term (This Month):
1. Implement full analysis pipeline
2. Create camera script generator
3. Integrate LLM for basic commentary
4. Record first test video

### Medium-term (Next 3 Months):
1. Complete all pipeline stages
2. Test on 50+ diverse replays
3. Tune quality and performance
4. Deploy automated system

---

## Resources & References

### Documentation
- [sc2reader docs](https://sc2reader.readthedocs.io/)
- [python-sc2 docs](https://burnysc2.github.io/python-sc2/)
- [FFmpeg guide](https://ffmpeg.org/documentation.html)
- [YouTube Data API](https://developers.google.com/youtube/v3)

### Community
- [r/starcraft](https://reddit.com/r/starcraft)
- [AI Arena Discord](https://discord.gg/aiarena)
- [SC2 API Discord](https://discord.gg/sc2api)

### Training Resources
- YouTube channels: Lowko, PiG, Harstem, Winter
- Transcript tool: youtube-transcript-api
- LLM APIs: OpenAI, Anthropic, Together.ai

---

## Questions & Support

For technical questions about this design:
- Review the detailed `TECHNICAL_DEEP_DIVE.md`
- Check `FAQ_TECHNICAL_PANEL.md` for specific scenarios
- See `ARCHITECTURE.md` for system design details

**Ready to implement!** 🚀
