# SC2Cast - Automated StarCraft II Replay Recording System

> **Intelligent camera system** that automatically records SC2 replays with dynamic camera work following the action

## 🎯 What is SC2Cast?

SC2Cast is an automated StarCraft II replay recording system with intelligent camera control:

**Currently Working:**
1. ✅ Analyzes replays to extract all game events (battles, expansions, tech)
2. ✅ Prioritizes important moments using intelligent clustering
3. ✅ Generates camera scripts automatically from event analysis
4. ✅ Directs an intelligent camera to follow the action
5. ✅ Records high-quality video (1080p60) with FFmpeg
6. ✅ Full automation: replay file → video output

**In Development:**
- 🔜 AI commentary generation (Llama 3.1 8B local)
- 🔜 Text-to-speech narration (Coqui TTS local)
- 🔜 YouTube upload automation

**Stack**: 100% open-source | Windows native | Python + FFmpeg  
**Cost**: $0/month operational | No external APIs

---

## 🚀 Quick Start

### Prerequisites

**Required Software:**
1. **Python 3.11+** - [Download from python.org](https://www.python.org/downloads/)
2. **Poetry** - Python dependency management
3. **FFmpeg** - Video encoding and screen capture
4. **StarCraft II** - Must be installed on Windows

### Installation

```powershell
# 1. Clone repository
git clone https://github.com/prevosta/sc2cast.git
cd sc2cast

# 2. Install Poetry (if not already installed)
pip install poetry

# 3. Install FFmpeg (REQUIRED for video recording)
winget install Gyan.FFmpeg
# Alternative: choco install ffmpeg (if using Chocolatey)
# After installation, restart your terminal/VS Code to refresh PATH

# 4. Install project dependencies
poetry install

# 5. Run tests
poetry run python tests/test_keyboard_automation.py  # Test camera control
poetry run python tests/test_screen_capture.py       # Test video capture (after FFmpeg PATH refresh)
```

**Note:** After installing FFmpeg, you may need to restart your terminal or VS Code for the PATH to update.

### Verify Installation

```powershell
# Check Python version
python --version  # Should be 3.11+

# Check Poetry
poetry --version

# Check FFmpeg (restart terminal if just installed)
ffmpeg -version

# Check SC2 installation
poetry run python src/sc2cast/verify_sc2.py
```

**Output**: All checks should pass ✅

---

## 📂 Project Structure

```
sc2cast/
├── docs/
│   ├── TECHNICAL.md       # Architecture, setup, code examples
│   ├── IMPLEMENTATION.md  # Timeline, status, milestones
│   ├── FAQ.md             # Common questions & troubleshooting
│   └── dev/               # Sprint workflow & devlog
├── src/                   # Source code (Sprint 1.2+)
├── tests/                 # Test files (Sprint 2.x+)  
├── config/                # Configuration files (Sprint 3.x+)
├── replays/               # Demo replay files
├── output/                # Generated videos (gitignored)
└── README.md              # This file
```

## 📚 Documentation

**Three consolidated documents cover everything:**

1. **[docs/TECHNICAL.md](docs/TECHNICAL.md)** 🔧 **TECHNICAL DEEP DIVE**
   - Architecture & data flow
   - Event extraction and prioritization
   - Camera script generation
   - Code examples (replay parsing, event processing)
   - Troubleshooting

2. **[docs/IMPLEMENTATION.md](docs/IMPLEMENTATION.md)** 📋 **PLANNING & STATUS**
   - Project roadmap and timeline
   - Resource requirements (hardware, storage)
   - Success metrics & milestones
   - Risk management

3. **[docs/FAQ.md](docs/FAQ.md)** ❓ **FAQ & TROUBLESHOOTING**
   - Zero-budget strategy explained
   - Technical Q&A (GPU, Docker, SC2)
   - Project planning & timeline
   - Quality comparisons vs paid APIs
   - YouTube automation
   - Common issues & fixes

### Development Workflow (`docs/dev/`)
- **[docs/dev/WORKFLOW.md](docs/dev/WORKFLOW.md)** - Sprint process, file discipline, quality rules
- **[docs/dev/CURRENT_SPRINT.md](docs/dev/CURRENT_SPRINT.md)** - Current sprint tasks & status
- **[docs/dev/DEVLOG.md](docs/dev/DEVLOG.md)** - Concise development history

---

## 🏗️ Technology Stack

| Component | Technology | Status |
|-----------|-----------|--------|
| Language | Python 3.11+ | ✅ Working |
| Replay Parsing | sc2reader | ✅ Working |
| Event Extraction | sc2reader events API | ✅ Working |
| Game Control | pyautogui (keyboard automation) | ✅ Working |
| Timer Sync | EasyOCR | ✅ Working |
| Screen Capture | FFmpeg | ✅ Working |
| Video Encoding | FFmpeg (H.264, 1080p60) | ✅ Working |
| Platform | **Windows Native** | ✅ Required (SC2 support) |
| Commentary | Llama 3.1 8B (Ollama) | 🔜 Planned |
| TTS | Coqui TTS | 🔜 Planned |
| Upload | YouTube API v3 | 🔜 Planned |

**💰 Total API Costs: $0/month** - Everything runs locally on Windows

---

## 📊 Current Status

**Sprint 2.2: Event-Based Camera Intelligence** ✅ **COMPLETE**

**Working Features:**
- ✅ **Replay Event Extraction** - Extracts 700+ events per replay (battles, deaths, buildings, upgrades)
- ✅ **Event Prioritization** - Clusters events into battles with importance scoring
- ✅ **Camera Script Generation** - Automatically generates 18+ camera shots from events
- ✅ **Automated Recording** - Full pipeline from replay file to video output
- ✅ **Intelligent Camera** - Camera follows battles, expansions, and key moments automatically
- ✅ **OCR Timer Sync** - Game time synchronization for perfect timing
- ✅ **Multi-Replay Support** - Works with any SC2 replay file

**Quick Test:**
```powershell
# Run the complete event-based pipeline
poetry run python src/sc2cast/event_based_pipeline.py

# Or test individual components
poetry run python src/sc2cast/event_extractor.py      # Extract events
poetry run python src/sc2cast/event_prioritizer.py    # Prioritize events
poetry run python src/sc2cast/script_generator.py     # Generate camera script
```

**Latest Achievement:** Complete automation - load any replay, get intelligent video output!

**Next Sprint**: TBD (Polish features, add commentary, or production-ready CLI)

See [docs/dev/DEVLOG.md](docs/dev/DEVLOG.md) for complete development history.

---

## 🎯 Current Capabilities

### What Works Now
- ✅ **Event Detection** - Identifies 700+ game events automatically
- ✅ **Battle Clustering** - Groups events into 9+ major battles per game
- ✅ **Camera Intelligence** - Moves to action 3 seconds before it peaks
- ✅ **Recording Quality** - 1080p60 H.264 video output
- ✅ **Automation** - Zero manual intervention required

### Metrics (Current Sprint)
- ✅ 100% replay processing success (tested on multiple replays)
- ✅ 9 major battles detected and tracked per game
- ✅ 18 intelligent camera shots generated automatically
- ✅ ~6-10 minutes processing time per replay
- ✅ 1080p60 video output with FFmpeg

---

## 🏛️ Hardware Requirements

### Current (Video Recording Only)
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 100GB for replays and videos
- **CPU**: 4+ cores (for FFmpeg encoding)
- **OS**: Windows 10/11 (SC2 must be installed)
- **GPU**: Not required yet

### Future (When AI Commentary Added)
- **GPU**: NVIDIA RTX 3060+ (12GB VRAM) for local LLM
- **RAM**: 32GB (16GB system + 16GB for models)
- **Storage**: 1TB SSD (models + replays + output)

---

## 🤝 Contributing

Project is in active development (Sprint 2.2 complete - intelligent camera working!). 

See [docs/dev/WORKFLOW.md](docs/dev/WORKFLOW.md) for development process.

---

## 📄 License

TBD - Likely MIT or GPL depending on dependencies

---

## 🙏 Acknowledgments

- **StarCraft II Community**: For the amazing game and esports scene
- **SC2 Casters**: Lowko, PiG, Harstem, Winter - inspiration for commentary styles
- **AI Arena**: For providing high-quality bot replays
- **Open Source Projects**: sc2reader, python-sc2, Ollama, Coqui TTS, FFmpeg

---

**Built with ❤️ for the StarCraft II community | Zero-cost, open-source, GPU-powered**

🎮 May your replays be epic and your commentary legendary! 🎮
