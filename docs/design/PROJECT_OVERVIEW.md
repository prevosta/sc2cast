# SC2Cast - Automated StarCraft II Replay Casting System

## Project Overview
An end-to-end automated system that generates AI-commented video casts of StarCraft II replays and publishes them to YouTube.

## 💰 Zero-Budget Approach
**Operational Cost: $0/month**

All AI/ML processing uses open-source, locally-runnable models:
- **LLM**: Llama 3.1 8B (via Ollama) - FREE
- **TTS**: Coqui TTS - FREE
- **Hardware**: Already available (RTX 3060+ 12GB VRAM, 32GB RAM)

No external API costs. Everything runs on your local GPU.

## Core Pipeline
```
Replay Acquisition → Replay Analysis → Camera Director → Script Generation → 
Audio Synthesis → Video Recording → Post-Processing → YouTube Upload
```

## Technology Stack

### Language & Environment
- **Python 3.11+** - Primary language
- **Docker** - Containerized development and deployment
- **VS Code** - Development environment with remote container support

### Key Components

#### 1. Replay Acquisition & Parsing
- **python-sc2** - SC2 API interaction library
- **sc2reader** - Replay file parsing
- **aiarena-client** - AI Arena replay downloading
- Manual replay upload support

#### 2. Replay Analysis Engine
- Real-time game state analysis
- Build order detection
- Army composition tracking
- Economic analysis (workers, bases, resources)
- Combat engagement detection
- Key event identification (drops, harassment, tech switches)

#### 3. Camera Director System
- Dynamic viewport control
- Priority-based scene selection:
  - Main army engagements (highest priority)
  - Multi-pronged attacks
  - Economic harassment (drops, run-bys)
  - Tech progression moments
  - Scout/reconnaissance actions
  - Base expansions
- Smooth camera transitions
- Minimap awareness overlay

#### 4. Commentary Script Generation
- **LLM Integration**: Llama 3.1 8B (local, via Ollama) - **ZERO COST**
- Training corpus: YouTube SC2 cast transcripts (optional enhancement)
- Prompt-based generation with game context
- Context-aware commentary:
  - Opening analysis
  - Mid-game strategy discussion
  - Engagement-by-engagement breakdown
  - Player decision analysis

#### 5. Audio Synthesis
- **Coqui TTS (local)** - **ZERO COST**
- Multi-speaker VCTK model
- Voice customization for caster personality
- Prosody control for excitement/tension
- Background music mixing (optional)

#### 6. Video Recording & Processing
- **pysc2** - SC2 game environment control
- **OpenCV** or **FFmpeg** - Video capture and encoding
- Overlay graphics:
  - Player names and races
  - Supply counts
  - Resource counters
  - Army values
  - Production tab
- 1080p/60fps output target

#### 7. YouTube Upload Automation
- **google-api-python-client** - YouTube Data API v3
- Automated metadata generation:
  - Title generation based on players/matchup
  - Description with timestamps
  - Tags and category assignment
  - Thumbnail generation
- Playlist organization
- Upload scheduling

## Development Environment

### Docker Setup
```dockerfile
FROM python:3.11-slim

# SC2 client installation
# Required libraries and dependencies
# Development tools
```

### VS Code Integration
- Dev Container configuration
- Python extensions
- Debugger setup for containerized environment
- Volume mounting for replay files

## Project Structure
```
sc2cast/
├── src/
│   ├── acquisition/      # Replay downloading
│   ├── analysis/         # Game state analysis
│   ├── camera/           # Camera director
│   ├── commentary/       # Script generation
│   ├── synthesis/        # Audio generation
│   ├── recording/        # Video capture
│   └── upload/           # YouTube publishing
├── models/               # Trained models and weights
├── config/               # Configuration files
├── replays/             # Input replay files
├── output/              # Generated videos
├── transcripts/         # Training data for commentary
├── tests/               # Unit and integration tests
├── docker/              # Dockerfile and compose
└── docs/                # Documentation
```

## Key Technical Challenges

1. **SC2 Client Headless Operation** - Running SC2 without GUI in container
2. **Replay Playback Control** - Precise speed control and frame-perfect recording
3. **Camera AI** - Intelligent scene selection without missing action
4. **Commentary Quality** - Natural, engaging, and contextually accurate
5. **Processing Time** - Optimization for reasonable generation time
6. **Resource Requirements** - GPU for video encoding and LLM inference

## Success Metrics
- Commentary coherence and relevance
- Camera director effectiveness (% of key moments captured)
- Processing time per replay minute
- Video quality (resolution, frame rate, smoothness)
- Upload success rate
- Community reception (views, likes, comments)

## Future Enhancements
- Multi-language support
- Live casting mode
- Interactive viewer choices
- Tournament bracket support
- Player statistics integration
