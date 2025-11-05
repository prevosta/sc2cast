# SC2Cast - AI-Powered StarCraft II Replay Casting System

> **Zero-cost automated pipeline** that generates professionally-commented videos from SC2 replays and publishes to YouTube

## 🎯 What is SC2Cast?

SC2Cast transforms StarCraft II replays into professional cast videos with **zero operational costs**:
1. Analyzes gameplay to identify key moments
2. Directs an intelligent camera to capture the action  
3. Generates contextual AI commentary (Llama 3.1 8B local)
4. Synthesizes professional audio narration (Coqui TTS local)
5. Records and encodes high-quality video (1080p60)
6. Automatically uploads to YouTube with optimized metadata

**Stack**: 100% open-source | Runs in Docker | Uses local GPU (RTX 3060+ 12GB VRAM)  
**Cost**: $0/month operational | No external APIs | Self-hosted LLM + TTS

---

## 🚀 Quick Start

```powershell
# 1. Clone repository
git clone https://github.com/prevosta/sc2cast.git
cd sc2cast

# 2. Build Docker container (includes SC2 + CUDA + Python)
docker compose build

# 3. Run demo (processes replay in replays/demo/)
docker compose run sc2cast python src/process_replay.py
```

**Output**: Generated video in `output/` folder (1080p60 MP4)

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
├── replays/demo/          # Demo replay files
├── output/                # Generated videos (gitignored)
├── Dockerfile             # SC2 + CUDA + Python environment
├── docker-compose.yml     # GPU-enabled container config
└── README.md              # This file
```

## 📚 Documentation

**Three consolidated documents cover everything:**

1. **[docs/TECHNICAL.md](docs/TECHNICAL.md)** 🔧 **TECHNICAL DEEP DIVE**
   - Zero-budget approach (Llama 3.1 + Coqui TTS)
   - Architecture & data flow
   - Docker setup & GPU configuration
   - Code examples (LLM, TTS, replay parsing)
   - Camera director & commentary generation
   - Troubleshooting

2. **[docs/IMPLEMENTATION.md](docs/IMPLEMENTATION.md)** � **PLANNING & STATUS**
   - Current status (Sprint 1.1: Docker Environment Setup)
   - 20-week timeline (10 phases)
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

## 🏗️ Technology Stack (Zero-Budget Edition)

| Component | Technology | Why |
|-----------|-----------|-----|
| Language | Python 3.11+ | Rich ecosystem, rapid development |
| Replay Parsing | sc2reader | Fast, pure Python, FREE |
| Game Control | python-sc2 | Official API, FREE |
| Commentary | **Llama 3.1 8B (Ollama)** | Open-source, local GPU inference, FREE |
| TTS | **Coqui TTS** | Open-source, local synthesis, FREE |
| Video | FFmpeg | Industry standard, FREE |
| Container | Docker + CUDA | Reproducibility, GPU support, FREE |
| Upload | YouTube API v3 | Official integration, FREE |

**💰 Total API Costs: $0/month** - Everything runs locally on RTX 3060+ GPU!

---

## 📊 Current Status

**Sprint 1.1**: Docker Environment Setup (In Progress)
- ✅ Dockerfile created (SC2 + CUDA + Python)
- ✅ docker-compose.yml created (GPU support)
- ✅ Project structure organized
- ⏳ Docker build (troubleshooting SC2 download)
- ⏳ Test GPU access
- ⏳ Test Python environment

**Next Sprint**: Replay parser implementation

See [docs/IMPLEMENTATION.md](docs/IMPLEMENTATION.md) for full 20-week timeline.

---

## 🎯 Success Criteria

### Technical
- 95%+ replay processing success rate
- 90%+ factual commentary accuracy
- 85%+ key moment capture rate
- <34 min processing time per 20-min replay (local inference)

### Quality vs Paid APIs
- **Commentary**: 7.5/10 vs 9/10 (OpenAI GPT-4)
- **Voice**: 7/10 vs 9/10 (ElevenLabs)
- **Trade-off**: Acceptable quality at zero cost

---

## �️ Hardware Requirements

- **GPU**: NVIDIA RTX 3060+ (12GB VRAM minimum)
- **RAM**: 32GB (16GB system + 16GB models)
- **Storage**: 1TB SSD (models + replays + output)
- **CPU**: 8+ cores recommended
- **OS**: Windows/Linux with Docker + NVIDIA Container Toolkit

---

## 🤝 Contributing

Project is in early development (Sprint 1.1). See [docs/dev/WORKFLOW.md](docs/dev/WORKFLOW.md) for development process.

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
