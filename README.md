# SC2Cast - AI-Powered StarCraft II Replay Casting System

> Automated system that generates professionally-commented videos from SC2 replays and publishes to YouTube

## 🎯 What is SC2Cast?

SC2Cast is an end-to-end automated pipeline that:
1. Acquires StarCraft II replays (from AI Arena or manual upload)
2. Analyzes gameplay to identify key moments
3. Directs an intelligent camera to capture the action
4. Generates contextual AI commentary
5. Synthesizes professional audio narration
6. Records and encodes high-quality video (1080p60)
7. Automatically uploads to YouTube with optimized metadata

**Result**: Professional-quality cast videos without human intervention

---

## 📂 Project Structure

```
sc2cast/
├── docs/
│   ├── design/           # Technical design documentation  
│   └── dev/              # Development workflow & logs
├── src/                  # Source code (Sprint 1.2+)
├── tests/                # Test files (Sprint 2.x+)
├── config/               # Configuration files (Sprint 3.x+)
├── replays/
│   └── demo/             # Demo replay files
├── output/               # Generated videos (gitignored)
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 📚 Documentation

### Design Documentation (`docs/design/`)

1. **[docs/design/PANEL_PRESENTATION.md](docs/design/PANEL_PRESENTATION.md)** ⭐ START HERE
   - Executive summary and project overview
   - Quick facts and key innovations
   - Perfect for understanding the project at a glance

2. **[docs/design/ZERO_BUDGET_APPROACH.md](docs/design/ZERO_BUDGET_APPROACH.md)** 💰 **ZERO-COST STRATEGY**
   - 100% open-source, locally-runnable solutions
   - No external API costs
   - Self-hosted LLM and TTS options
   - Budget-conscious architecture

3. **[docs/design/PROJECT_OVERVIEW.md](docs/design/PROJECT_OVERVIEW.md)**
   - High-level system design
   - Technology stack decisions
   - Project structure and success metrics

4. **[docs/design/TECHNICAL_DEEP_DIVE.md](docs/design/TECHNICAL_DEEP_DIVE.md)**
   - Detailed technical analysis of each component
   - Algorithm explanations
   - Library comparisons and justifications

5. **[docs/design/ARCHITECTURE.md](docs/design/ARCHITECTURE.md)**
   - System architecture diagrams
   - Module breakdown and responsibilities
   - Data models and database schema
   - Configuration management

6. **[docs/IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md)**
   - 20-week development roadmap
   - Sprint-by-sprint breakdown
   - Milestones and deliverables
   - Resource requirements

7. **[docs/FAQ_TECHNICAL_PANEL.md](docs/FAQ_TECHNICAL_PANEL.md)**
   - 60+ anticipated technical questions with detailed answers
   - Covers all aspects from SC2 integration to YouTube policies

8. **[docs/QUICK_START.md](docs/QUICK_START.md)**
   - Getting started guide
   - Key technical decisions summary
   - Development workflow

9. **[docs/CODE_EXAMPLES.md](docs/CODE_EXAMPLES.md)**
   - Concrete Python implementations
   - Example code for all major components

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker with GPU support
- NVIDIA GPU (RTX 3060+)
- 16GB RAM minimum

### Setup (Planned)
```bash
# Clone repository
git clone <repo-url>
cd sc2cast

# Open in VS Code (will use dev container)
code .

# Process a replay
python -m src.cli process --replay ./replays/sample.SC2Replay
```

---

## 🏗️ Technology Stack (Zero-Budget Edition)

| Component | Technology | Why |
|-----------|-----------|-----|
| Language | Python 3.11+ | Rich ecosystem, rapid development |
| Replay Parsing | sc2reader | Fast, pure Python, FREE |
| Game Control | python-sc2 | Official API, FREE |
| Commentary | **Llama 3.1 (local)** | Open-source, runs locally, FREE |
| TTS | **Coqui TTS (local)** | Open-source, runs locally, FREE |
| Video | FFmpeg | Industry standard, FREE |
| Container | Docker | Reproducibility, FREE |
| Upload | YouTube API v3 | Official integration, FREE |

**💰 Total API Costs: $0/month** - Everything runs locally!

---

## 📊 Pipeline Overview

```
┌─────────────┐
│   Replay    │
│  Acquisition│
└──────┬──────┘
       │
┌──────▼──────┐
│  Analysis   │ (sc2reader - 30 seconds)
│   Engine    │
└──────┬──────┘
       │
┌──────▼──────┐
│   Camera    │ (Priority-based - 10 seconds)
│  Director   │
└──────┬──────┘
       │
┌──────▼──────┐
│ Commentary  │ (LLM - 2 minutes)
│  Generator  │
└──────┬──────┘
       │
┌──────▼──────┐
│   Audio     │ (TTS - 1 minute)
│  Synthesis  │
└──────┬──────┘
       │
┌──────▼──────┐
│   Video     │ (Recording - 1x replay time)
│  Recording  │
└──────┬──────┘
       │
┌──────▼──────┐
│  YouTube    │ (Upload - 5 minutes)
│   Upload    │
└─────────────┘

Total: ~30 minutes for 20-minute replay
```

---

## 🎯 Key Features

### Intelligent Camera Director
- Priority-based scene selection (10-point scale)
- Smooth transitions with Bezier curves
- Conflict resolution for simultaneous events
- Context-aware dwell times

### AI Commentary
- LLM-powered contextual narration
- Trained on 100+ hours of real caster transcripts
- Factual accuracy validation
- Emotion-aware delivery (excited, tense, analytical)

### Production Quality
- 1080p 60fps video output
- Professional HUD overlays (supply, resources, army value)
- Background music mixing
- Optimized encoding for YouTube

### Full Automation
- AI Arena replay downloading
- Unattended batch processing
- Automatic YouTube upload with metadata
- Error handling and retry logic

---

## 📈 Development Status

**Current Phase**: Planning & Design Complete ✅

**Next Steps**:
1. Environment setup (Week 1)
2. Replay analysis implementation (Weeks 2-4)
3. Camera director (Weeks 3-4)
4. Video pipeline (Weeks 5-7)
5. Commentary & audio (Weeks 8-12)
6. Automation & integration (Weeks 13-16)
7. Testing & launch (Weeks 17-21)

**Target Launch**: ~5 months from start

---

## 💰 Cost Analysis (Zero-Budget Approach)

### Current Strategy: 100% Open-Source
- **Hardware**: Use existing gaming PC with GPU
- **LLM**: Llama 3.1 8B (local inference)
- **TTS**: Coqui TTS (local synthesis)
- **APIs**: None - everything runs locally
- **Cloud**: None - self-hosted only
- **Total**: **$0/month** 🎉

### Hardware Requirements
- **GPU**: NVIDIA RTX 3060+ (12GB VRAM minimum for Llama 3.1 8B)
- **RAM**: 32GB (16GB for system + 16GB for models)
- **Storage**: 1TB SSD (models + replays + output)
- **CPU**: 8+ cores recommended

---

## 🎯 Success Criteria

### Technical
- ✅ 95%+ replay processing success rate
- ✅ 90%+ factual commentary accuracy
- ✅ 85%+ key moment capture rate
- ✅ <30 min processing time per 20-min replay

### Business
- ✅ 1k YouTube subscribers (month 3)
- ✅ 10k subscribers (month 6)
- ✅ 50%+ average watch time
- ✅ Positive community feedback
- ✅ YouTube monetization enabled

---

## 🛡️ Risk Mitigation

### Technical
- **SC2 Stability**: Checkpoint system, auto-restart
- **API Costs**: Local model fallback, caching
- **Processing Time**: Parallel workers, GPU acceleration

### Business
- **YouTube Policies**: Clear AI disclosure, follow guidelines
- **Engagement**: Quality focus, community feedback
- **Copyright**: Royalty-free music, proper attribution

---

## 🔮 Future Roadmap

### v1.0 (Launch)
- Core pipeline working
- Automated processing
- YouTube integration

### v1.5 (Quality)
- Fine-tuned models
- Better camera AI
- Voice cloning
- Multi-language

### v2.0 (Interactive)
- Live casting
- Viewer polls
- Custom requests
- Player dashboards

### v3.0 (Platform)
- Web interface
- Mobile app
- Tournament support
- Creator API

---

## 📚 Learning Resources

### SC2 Development
- [sc2reader documentation](https://sc2reader.readthedocs.io/)
- [python-sc2 guide](https://burnysc2.github.io/python-sc2/)
- [SC2 API Discord](https://discord.gg/sc2api)

### AI/ML
- [OpenAI API docs](https://platform.openai.com/docs)
- [Coqui TTS](https://github.com/coqui-ai/TTS)
- [LangChain for RAG](https://python.langchain.com/)

### Video Production
- [FFmpeg guide](https://ffmpeg.org/documentation.html)
- [YouTube Data API](https://developers.google.com/youtube/v3)

---

## 🤝 Contributing

This project is currently in the design phase. Once implementation begins, contributions will be welcome in:
- Replay analysis algorithms
- Camera director improvements
- Commentary prompt engineering
- Video overlay designs
- Testing and bug reports

---

## 📄 License

TBD - Likely MIT or GPL depending on dependencies

---

## 🙏 Acknowledgments

- **StarCraft II Community**: For the amazing game and esports scene
- **SC2 Casters**: Lowko, PiG, Harstem, Winter, Artosis, Tasteless - inspiration for commentary styles
- **AI Arena**: For providing a source of high-quality bot replays
- **Open Source Projects**: sc2reader, python-sc2, Coqui TTS, FFmpeg, and countless others

---

## 📞 Contact & Support

For questions about this project design:
- Review the comprehensive documentation in this repository
- Check [FAQ_TECHNICAL_PANEL.md](FAQ_TECHNICAL_PANEL.md) for detailed technical Q&A

---

## 🎬 Project Status

**Status**: 📋 Design & Planning Complete  
**Phase**: Ready for technical panel review  
**Next**: Awaiting go-ahead to begin implementation

---

**Built with ❤️ for the StarCraft II community**

🎮 May your replays be epic and your commentary legendary! 🎮
