# SC2Cast - FAQ

**Common questions and answers.**

---

## Zero-Budget Approach

### Q: Why not use GPT-4?
**A:** Budget constraint: $0/month. Llama 3.1 8B is free and good enough (7.5/10 vs 9/10 quality).

### Q: Is local AI really free?
**A:** Yes. Only costs: electricity (~$20-30/mo) and one-time hardware (already owned).

### Q: What if Llama quality isn't good enough?
**A:** 
1. Fine-tune on SC2 transcripts (Sprint 5.2)
2. Use larger model (70B) for important videos
3. Worst case: Allocate small API budget for highlights

### Q: Why Coqui TTS vs ElevenLabs?
**A:** ElevenLabs costs $150/mo. Coqui is free and 7/10 quality (vs 10/10). Acceptable trade-off.

---

## Technical

### Q: Can this run on CPU only?
**A:** No. GPU required for:
- Coqui TTS (can run on CPU but 10x slower)
- Llama 3.1 (needs GPU for reasonable speed)
- Video encoding (can use CPU but much slower)

### Q: What if I don't have RTX 3060+?
**A:** 
- Minimum: RTX 2060 6GB (will be slower)
- Recommended: RTX 3060+ 12GB
- Optimal: RTX 4090 24GB

### Q: How long does it take to process one replay?
**A:** ~34 minutes for a 20-minute replay:
- Analysis: 30s
- Commentary: 4min
- Audio: 2min
- Recording: 20min (1x speed)
- Encoding: 3min
- Upload: 5min

### Q: Can I speed it up?
**A:** Yes (Phase 9 - Optimization):
- Parallel commentary generation: -30%
- GPU encoding (NVENC): -60% encode time
- Target: <25 minutes total

### Q: Does this work on Windows/Mac/Linux?
**A:** 
- **Windows**: Yes (WSL 2 + Docker Desktop)
- **Linux**: Yes (native Docker)
- **Mac**: Limited (no NVIDIA GPU support)

---

## Project

### Q: How long to build?
**A:** 20 weeks (5 months) for full production system.
- Week 2: PoC (basic video)
- Week 6: Local AI working
- Week 11: First AI commentary
- Week 21: Production launch

### Q: Can I help / contribute?
**A:** Project is currently in solo development (learning phase). Open to collaboration after MVP.

### Q: Will you open-source it?
**A:** Considering it. Deciding after Sprint 5 (when AI commentary works).

---

## Replays

### Q: Where do replays come from?
**A:** 
- AI Arena (automated download)
- Manual upload
- Community submissions (future)

### Q: What replay versions are supported?
**A:** All SC2 versions via sc2reader library (kept up to date).

### Q: Can I request my game be casted?
**A:** Not yet. Phase 7 (weeks 15-16) adds submission system.

---

## Quality

### Q: How good is the commentary?
**A:** Target: 7.5/10
- Factually accurate
- Somewhat robotic
- Good for learning, not entertainment

### Q: How does it compare to human casters?
**A:** 
- **Better than**: No commentary at all
- **Comparable to**: Amateur casters
- **Worse than**: Professional casters (Tastosis, Lowko)

### Q: Will it improve over time?
**A:** Yes:
- Fine-tuning on more data
- Better prompts
- Larger models for special content

---

## YouTube

### Q: Will YouTube allow AI-generated content?
**A:** Yes, with proper disclosure. We clearly label videos as AI-generated.

### Q: Can this be monetized?
**A:** Yes, once channel meets YouTube requirements (1k subs, 4k watch hours).

### Q: What's the content strategy?
**A:** 
- High volume (10+ videos/day)
- Niche focus (SC2 community)
- Consistent quality
- Educational value

---

## Costs

### Q: Truly $0/month?
**A:** Operational costs: $0/month
- No API fees
- No cloud hosting
- No paid services

Only costs: Electricity (~$20-30/mo)

### Q: What if I want better quality?
**A:** Options:
- Use GPT-4 ($150/mo) for commentary
- Use ElevenLabs ($150/mo) for voice
- Total: ~$300/mo for 9/10 quality

Trade-off: 2x quality, infinite cost increase.

---

## Troubleshooting

### Q: Docker build fails?
**A:** 
- Ensure Docker Desktop is running
- Check: `docker --version`
- Retry: `docker compose build --no-cache`

### Q: GPU not detected?
**A:**
- Check: `nvidia-smi`
- Install NVIDIA drivers
- Enable GPU in Docker settings

### Q: Ollama not responding?
**A:**
- Check: `ollama list`
- Restart: `ollama serve`
- Re-pull: `ollama pull llama3.1:8b-q4_K_M`

### Q: Out of memory errors?
**A:**
- Close other GPU applications
- Use quantized models (q4_K_M)
- Reduce batch sizes

---

**For technical details, see `TECHNICAL.md`**  
**For timeline, see `IMPLEMENTATION.md`**
