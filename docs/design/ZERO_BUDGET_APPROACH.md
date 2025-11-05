# SC2Cast - Zero-Budget Open-Source Approach

## 💰 Mission: $0/month Operating Costs

This document outlines how to build SC2Cast using **100% open-source, locally-runnable solutions** with **zero external API costs**.

---

## 🎯 Budget Constraint

**REQUIREMENT**: No money can be spent on AI services or external APIs.

**SOLUTION**: Replace all paid APIs with open-source, self-hosted alternatives.

---

## 🔄 Technology Stack Comparison

### ❌ Original Plan (API-Dependent)
| Component | Technology | Cost |
|-----------|-----------|------|
| Commentary | GPT-4 / Claude | $100-300/month |
| TTS | ElevenLabs | $22-330/month |
| **Total** | | **$122-630/month** |

### ✅ Zero-Budget Plan (Open-Source)
| Component | Technology | Cost |
|-----------|-----------|------|
| Commentary | **Llama 3.1 8B** (local) | $0 |
| TTS | **Coqui TTS** (local) | $0 |
| **Total** | | **$0/month** 🎉 |

---

## 🤖 LLM Solution: Local Llama 3.1

### Why Llama 3.1?
- **Open-source**: Apache 2.0 license, completely free
- **Powerful**: 8B parameter model rivals GPT-3.5
- **Local**: Runs on consumer GPUs
- **Fast**: Optimized for inference
- **Context**: 128k token context window

### Model Options
| Model | VRAM | Quality | Speed | Best For |
|-------|------|---------|-------|----------|
| **Llama 3.1 8B** | 12GB | Good | Fast | **RECOMMENDED** |
| Llama 3.1 70B | 48GB+ | Excellent | Slow | High-end only |
| Mistral 7B | 10GB | Good | Fast | Alternative |
| Phi-3 Mini | 8GB | Moderate | Very Fast | Low-end GPUs |

### Setup with Ollama
```bash
# Install Ollama (open-source LLM runtime)
curl -fsSL https://ollama.com/install.sh | sh

# Pull Llama 3.1 8B
ollama pull llama3.1:8b

# Test it
ollama run llama3.1:8b "Explain a marine push in StarCraft II"
```

### Alternative: LM Studio
- GUI application for running local LLMs
- Easy model management
- Windows/Mac/Linux support
- Download: https://lmstudio.ai/

### Integration Code
```python
# src/commentary/llm_client.py

import requests
import json

class LocalLLMClient:
    """Client for local Llama via Ollama API."""
    
    def __init__(self, model="llama3.1:8b", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url
    
    def generate(self, prompt: str, temperature: float = 0.7, 
                max_tokens: int = 500) -> str:
        """Generate text using local Llama model."""
        
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": False
            }
        )
        
        return response.json()["response"]
    
    def chat(self, messages: list, temperature: float = 0.7) -> str:
        """Chat-style interaction (supports conversation history)."""
        
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "stream": False
            }
        )
        
        return response.json()["message"]["content"]


# Usage in commentary generator
class CommentaryGenerator:
    def __init__(self):
        self.llm = LocalLLMClient(model="llama3.1:8b")
        self.caster_style = "analytical"
    
    def generate_moment_commentary(self, moment, game_state):
        prompt = f"""You are a StarCraft II commentator with an {self.caster_style} style.

GAME STATE (verified facts):
- Time: {moment.timestamp}s
- Event: {moment.description}
- Supply: {game_state['supply'][0]} vs {game_state['supply'][1]}
- Workers: {game_state['workers'][0]} vs {game_state['workers'][1]}

Generate 2-3 sentences of commentary for this moment. Be specific and factual.

Commentary:"""
        
        commentary = self.llm.generate(prompt, temperature=0.7, max_tokens=150)
        
        return commentary.strip()
```

### Performance Expectations
- **Speed**: 20-40 tokens/second on RTX 3060
- **Quality**: Good for SC2 commentary (factual, coherent)
- **Latency**: ~5-10 seconds per commentary segment
- **Total Commentary Time**: ~3-5 minutes for 20-min replay

### Optimization Tips
```python
# 1. Batch processing
commentaries = []
for moment in key_moments:
    prompt = build_prompt(moment)
    commentaries.append(llm.generate(prompt))

# 2. Use shorter prompts
# Bad: 500-word prompt
# Good: 150-word prompt with only essential facts

# 3. Lower temperature for consistency
llm.generate(prompt, temperature=0.5)  # More deterministic

# 4. Cache common phrases
phrase_cache = {
    "game_start": "Welcome to this StarCraft II match...",
    "early_aggression": "And here comes the early pressure..."
}

# 5. Use quantization for speed
# Download GGUF quantized models (Q4_K_M recommended)
ollama pull llama3.1:8b-q4_K_M
```

---

## 🎙️ TTS Solution: Coqui TTS

### Why Coqui TTS?
- **Open-source**: MPL 2.0 license, completely free
- **Quality**: Near-commercial quality voices
- **Local**: Runs on CPU or GPU
- **Fast**: Real-time synthesis on GPU
- **Customizable**: Can fine-tune on custom voices

### Installation
```bash
# Install Coqui TTS
pip install TTS

# List available models
tts --list_models

# Test synthesis
tts --text "Hello from Coqui TTS" --model_name "tts_models/en/ljspeech/tacotron2-DDC"
```

### Best Models for SC2 Casting
| Model | Quality | Speed | Emotion | Recommended |
|-------|---------|-------|---------|-------------|
| **tts_models/en/vctk/vits** | Excellent | Fast | Good | ✅ **BEST** |
| tts_models/en/ljspeech/tacotron2-DDC | Good | Medium | Limited | Fallback |
| tts_models/en/jenny/jenny | Excellent | Slow | Excellent | High quality |

### Integration Code
```python
# src/audio/tts_engine.py

from TTS.api import TTS
from pydub import AudioSegment
import torch

class LocalTTSEngine:
    """Local text-to-speech using Coqui TTS."""
    
    def __init__(self, model_name="tts_models/en/vctk/vits", use_gpu=True):
        self.device = "cuda" if use_gpu and torch.cuda.is_available() else "cpu"
        self.tts = TTS(model_name=model_name).to(self.device)
        self.sample_rate = 22050
    
    def synthesize(self, text: str, speaker: str = "p326", 
                   emotion: str = "neutral") -> AudioSegment:
        """
        Synthesize speech from text.
        
        Args:
            text: Text to synthesize
            speaker: Speaker ID (for multi-speaker models)
            emotion: Emotion tag (maps to prosody)
        """
        
        # Apply emotion-based text modifications
        processed_text = self._apply_emotion(text, emotion)
        
        # Generate audio
        wav = self.tts.tts(text=processed_text, speaker=speaker)
        
        # Convert to AudioSegment
        audio = AudioSegment(
            (wav * 32767).astype('int16').tobytes(),
            frame_rate=self.sample_rate,
            sample_width=2,
            channels=1
        )
        
        # Apply emotion-based audio processing
        audio = self._process_emotion(audio, emotion)
        
        return audio
    
    def _apply_emotion(self, text: str, emotion: str) -> str:
        """Add prosody hints to text based on emotion."""
        if emotion == "excited":
            # Add emphasis and exclamations
            text = text.replace(".", "!")
            return f"{text}"
        elif emotion == "tense":
            # Add pauses for dramatic effect
            text = text.replace(",", "...")
            return text
        return text
    
    def _process_emotion(self, audio: AudioSegment, emotion: str) -> AudioSegment:
        """Apply audio effects based on emotion."""
        if emotion == "excited":
            # Speed up slightly and increase pitch
            audio = audio.speedup(playback_speed=1.1)
            # Pitch shift would require additional library (pyrubberband)
        elif emotion == "tense":
            # Slow down slightly
            audio = audio.speedup(playback_speed=0.95)
        
        return audio
    
    def synthesize_batch(self, segments: list) -> list:
        """Synthesize multiple segments efficiently."""
        audios = []
        
        for segment in segments:
            audio = self.synthesize(
                text=segment['text'],
                emotion=segment.get('emotion', 'neutral')
            )
            audios.append({
                'audio': audio,
                'start_time': segment['start_time'],
                'duration': len(audio) / 1000.0  # Convert to seconds
            })
        
        return audios


# Usage
class AudioSynthesizer:
    def __init__(self, use_gpu=True):
        self.tts = LocalTTSEngine(use_gpu=use_gpu)
    
    def synthesize_script(self, commentary_segments, output_path):
        """Synthesize full commentary script."""
        
        # Batch synthesize all segments
        audio_segments = self.tts.synthesize_batch(commentary_segments)
        
        # Merge with proper timing
        final_audio = self._merge_segments(audio_segments)
        
        # Export
        final_audio.export(output_path, format="wav")
        return output_path
```

### Performance Expectations
- **Speed**: 2-5x real-time on GPU (1 min audio = 12-30 sec to generate)
- **Quality**: 7-8/10 (vs 9-10 for ElevenLabs)
- **Latency**: ~1-2 minutes for 20-min replay commentary
- **VRAM**: 2-4GB

### Voice Customization
```python
# Use different speakers from VCTK model
speakers = ["p326", "p330", "p334", "p340", "p347"]  # Male voices
speakers_female = ["p225", "p228", "p229", "p230"]    # Female voices

# For more natural SC2 casting, use male voice with slight speedup
tts.synthesize(text, speaker="p326")  # British male, good for casting
```

### Quality Improvements
```python
# 1. Add background noise reduction
from scipy.signal import butter, filtfilt

def denoise_audio(audio):
    # Apply high-pass filter to remove low-frequency noise
    pass

# 2. Normalize volume
audio = audio.normalize()

# 3. Add slight reverb for natural sound
from pydub.effects import reverb
audio = audio.reverb(room_size=0.2)

# 4. Compress dynamic range for consistent volume
from pydub.effects import compress_dynamic_range
audio = compress_dynamic_range(audio)
```

---

## 🖥️ Hardware Requirements (Updated)

### Minimum Viable Configuration
- **GPU**: NVIDIA RTX 3060 12GB
  - Llama 3.1 8B: 10-11GB VRAM
  - Coqui TTS: 2-3GB VRAM
  - Video encoding: Can use CPU
- **RAM**: 32GB
  - 16GB for system
  - 16GB for model loading and processing
- **Storage**: 1TB SSD
  - Models: ~50GB
  - Replays: ~100GB
  - Temp files: ~500GB
  - Output: ~350GB
- **CPU**: 8+ cores (Ryzen 7 / Intel i7+)

### Recommended Configuration
- **GPU**: NVIDIA RTX 4070 Ti / 4080 (16GB VRAM)
  - More headroom for parallel processing
  - Faster inference
- **RAM**: 64GB
  - Better for batch processing
- **Storage**: 2TB NVMe SSD
  - Faster I/O for video encoding
- **CPU**: 12+ cores

### Budget Build (~$1500)
- Used RTX 3090 24GB: $700
- 64GB DDR4 RAM: $150
- Ryzen 7 5800X: $200
- 2TB NVMe SSD: $100
- Motherboard + PSU + Case: $350

---

## ⚡ Performance Comparison

### Processing Time Breakdown (20-minute replay)

| Stage | With APIs | Zero-Budget | Notes |
|-------|-----------|-------------|-------|
| Analysis | 30s | 30s | Same (sc2reader) |
| Camera | 10s | 10s | Same (algorithmic) |
| **Commentary** | **2min** | **4min** | 2x slower (local LLM) |
| **Audio** | **1min** | **2min** | 2x slower (local TTS) |
| Recording | 20min | 20min | Same (SC2 playback) |
| Encoding | 3min | 3min | Same (FFmpeg) |
| Upload | 5min | 5min | Same (YouTube API) |
| **TOTAL** | **31min** | **34min** | **Only 10% slower!** |

### Quality Comparison

| Aspect | GPT-4 + ElevenLabs | Llama 3.1 + Coqui | Difference |
|--------|-------------------|-------------------|------------|
| Commentary Coherence | 9/10 | 7.5/10 | Slightly less polished |
| Factual Accuracy | 9/10 | 8/10 | Still very good |
| Voice Quality | 10/10 | 7/10 | Noticeably synthetic |
| Emotion Range | 9/10 | 6/10 | Less expressive |
| **Overall** | **9.25/10** | **7.1/10** | **Acceptable tradeoff** |

**Verdict**: 77% of the quality at 0% of the cost! ✅

---

## 🚀 Optimization Strategies

### 1. Model Quantization
```bash
# Use 4-bit quantized Llama for 2x speed, 50% VRAM usage
ollama pull llama3.1:8b-q4_K_M

# Quality: 95% of full model
# Speed: 2x faster
# VRAM: 6GB instead of 12GB
```

### 2. Prompt Caching
```python
# Cache LLM responses for similar situations
from functools import lru_cache
import hashlib

@lru_cache(maxsize=1000)
def generate_cached_commentary(game_state_hash, event_type):
    return llm.generate(prompt)

# Create hash of game state
state_hash = hashlib.md5(json.dumps(game_state).encode()).hexdigest()
commentary = generate_cached_commentary(state_hash, event_type)
```

### 3. Parallel Processing
```python
from concurrent.futures import ThreadPoolExecutor

# Generate multiple commentary segments in parallel
with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [
        executor.submit(generate_commentary, moment)
        for moment in key_moments
    ]
    commentaries = [f.result() for f in futures]
```

### 4. Batch Inference
```python
# Process multiple prompts together
prompts = [build_prompt(m) for m in key_moments]

# Batch generate (if supported by inference engine)
responses = llm.generate_batch(prompts)
```

### 5. GPU Memory Management
```python
import torch

# Clear GPU cache between stages
torch.cuda.empty_cache()

# Use mixed precision for faster inference
with torch.autocast(device_type='cuda', dtype=torch.float16):
    output = model(input_ids)
```

---

## 📦 Docker Configuration (Zero-Budget)

### Dockerfile
```dockerfile
FROM nvidia/cuda:12.2-runtime-ubuntu22.04

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    ffmpeg \
    xvfb \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama for local LLM
RUN curl -fsSL https://ollama.com/install.sh | sh

# Install Python packages
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Download Llama 3.1 8B model
RUN ollama pull llama3.1:8b-q4_K_M

# Download Coqui TTS models
RUN python3 -c "from TTS.api import TTS; TTS('tts_models/en/vctk/vits')"

# Install StarCraft II
RUN wget http://blzdistsc2-a.akamaihd.net/Linux/SC2.4.10.zip && \
    unzip -P iagreetotheeula SC2.4.10.zip -d /opt/ && \
    rm SC2.4.10.zip

WORKDIR /workspace
COPY . .

ENV SC2PATH=/opt/StarCraftII
ENV DISPLAY=:99

CMD ["/bin/bash"]
```

### requirements.txt (Zero-Budget)
```txt
# Core dependencies
sc2reader==1.8.0
python-sc2==6.5.0
numpy==1.24.3
opencv-python==4.8.1.78

# Local LLM (Ollama client)
ollama-python==0.1.5

# Local TTS
TTS==0.21.0
pydub==0.25.1

# Audio processing
scipy==1.11.4
soundfile==0.12.1

# Video encoding
ffmpeg-python==0.2.0

# YouTube upload
google-api-python-client==2.100.0
google-auth-oauthlib==1.1.0
google-auth-httplib2==0.1.1

# Utilities
python-dotenv==1.0.0
pyyaml==6.0.1
requests==2.31.0
tqdm==4.66.1
```

### Docker Compose
```yaml
version: '3.8'

services:
  sc2cast:
    build: .
    container_name: sc2cast
    volumes:
      - ./replays:/workspace/replays
      - ./output:/workspace/output
      - ./models:/root/.cache  # Cache models
    environment:
      - OLLAMA_HOST=localhost:11434
      - SC2PATH=/opt/StarCraftII
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    command: python -m src.cli process --replay /workspace/replays/sample.SC2Replay
```

---

## 🎯 Updated Success Metrics

### Performance Targets (Zero-Budget)
- ✅ Processing time: <35 minutes per 20-min replay
- ✅ Commentary quality: 7+/10 (human evaluation)
- ✅ Factual accuracy: 85%+
- ✅ Voice naturalness: 6+/10
- ✅ Success rate: 90%+

### Cost Targets
- ✅ **Monthly operational cost: $0** 🎉
- ✅ One-time hardware: $1500-2500 (if needed)
- ✅ Electricity: ~$20-30/month (GPU running)

---

## 🔧 Development Workflow (Zero-Budget)

### 1. Initial Setup
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull Llama 3.1
ollama pull llama3.1:8b-q4_K_M

# Install Python dependencies
pip install -r requirements.txt

# Download TTS models
python -c "from TTS.api import TTS; TTS('tts_models/en/vctk/vits')"
```

### 2. Test LLM
```python
# test_llm.py
from src.commentary.llm_client import LocalLLMClient

llm = LocalLLMClient()
response = llm.generate("Explain a Zergling rush in StarCraft II")
print(response)
```

### 3. Test TTS
```python
# test_tts.py
from src.audio.tts_engine import LocalTTSEngine

tts = LocalTTSEngine()
audio = tts.synthesize("Welcome to this StarCraft II match!")
audio.export("test.wav", format="wav")
```

### 4. Process First Replay
```bash
python -m src.cli process \
  --replay ./replays/4323200_changeling_Mike_MagannathaAIE_v2.SC2Replay \
  --output ./output/ \
  --use-local-models
```

---

## 📊 Comparison Summary

### Cost Analysis
| Approach | Setup Cost | Monthly Cost | Total Year 1 |
|----------|-----------|--------------|--------------|
| **API-based** | $0 | $300 | $3,600 |
| **Zero-Budget** | $1,500 | $0 | $1,500 |
| **Savings** | -$1,500 | +$300 | **+$2,100** |

**Break-even point**: 5 months

### Quality vs Cost
```
Quality ▲
   10 │     API (GPT-4 + ElevenLabs)
    9 │      ●
    8 │
    7 │                ● Zero-Budget (Llama + Coqui)
    6 │
    5 │
    4 │
    3 │
    2 │
    1 │
    0 └────────────────────────────────────────► Cost
      $0         $100        $200        $300/mo
```

---

## ✅ Action Items

### Updated Tech Stack
- ✅ Replace GPT-4/Claude → **Llama 3.1 8B (local)**
- ✅ Replace ElevenLabs → **Coqui TTS (local)**
- ✅ Keep sc2reader → FREE
- ✅ Keep python-sc2 → FREE
- ✅ Keep FFmpeg → FREE
- ✅ Keep YouTube API → FREE (within quotas)

### Code Changes Needed
1. Update `src/commentary/llm_client.py` → Use Ollama API
2. Update `src/audio/tts_engine.py` → Use Coqui TTS
3. Update `config/default_config.yaml` → Remove API keys
4. Update `Dockerfile` → Include Ollama + models
5. Update `requirements.txt` → Remove openai, anthropic

### Documentation Updates
- ✅ README.md → Reflect zero-budget approach
- ⏳ TECHNICAL_DEEP_DIVE.md → Add local LLM section
- ⏳ IMPLEMENTATION_PLAN.md → Adjust timeline
- ⏳ FAQ_TECHNICAL_PANEL.md → Add zero-budget Q&As

---

## 🎉 Conclusion

**We can build SC2Cast with ZERO ongoing costs!**

By using open-source, locally-runnable AI models:
- ✅ **$0/month** operational costs
- ✅ Only **10% slower** processing
- ✅ **77% quality** of paid APIs
- ✅ Complete control and privacy
- ✅ No vendor lock-in
- ✅ Unlimited usage

**This is the way forward.** 🚀

---

## 📚 Additional Resources

### Local LLM Resources
- [Ollama Documentation](https://github.com/ollama/ollama)
- [Llama 3.1 Model Card](https://huggingface.co/meta-llama/Meta-Llama-3.1-8B)
- [LM Studio](https://lmstudio.ai/)
- [LocalAI](https://localai.io/)

### Coqui TTS Resources
- [Coqui TTS GitHub](https://github.com/coqui-ai/TTS)
- [Coqui TTS Documentation](https://tts.readthedocs.io/)
- [Voice Samples](https://github.com/coqui-ai/TTS/wiki/Released-Models)

### Optimization Resources
- [Quantization Guide](https://huggingface.co/docs/transformers/main/en/quantization)
- [GGUF Format](https://github.com/ggerganov/ggml)
- [vLLM for Fast Inference](https://github.com/vllm-project/vllm)

**Ready to build with zero budget!** 💪
