# SC2Cast - Technical Documentation

**All technical information in one place.**

---

## 💰 Zero-Budget Approach

**$0/month operational costs** using 100% local, open-source AI:

| Component | Technology | Cost |
|-----------|-----------|------|
| LLM | Llama 3.1 8B (via Ollama) | FREE |
| TTS | Coqui TTS | FREE |
| Video | FFmpeg + python-sc2 | FREE |
| Platform | Native Windows (no Docker) | FREE |
| Hardware | RTX 3060+ 12GB VRAM (already owned) | $0 |
| **Total** | | **$0/month** ✅ |

### Hardware Requirements
- **GPU:** RTX 3060+ (12GB VRAM minimum)
- **RAM:** 32GB (16GB system + 16GB for models)
- **Storage:** 1TB SSD
- **CPU:** 8+ cores recommended
- **OS:** Windows 10/11 (SC2 must be installed)

### Performance
- Processing time: ~34 min for 20-min replay
- Quality: 77% of paid APIs (7.5/10 commentary, 7/10 voice)
- Trade-off: Acceptable quality at zero cost

---

## 🏗️ Architecture (Windows Native)

### Why Windows Native?
1. **Replay Support:** Windows SC2 client supports replay playback (Linux headless does not)
2. **Simplicity:** No Docker overhead, direct Python execution
3. **GPU Access:** Direct NVIDIA driver access, no virtualization
4. **Development:** Faster iteration, easier debugging

### Pipeline (7 Stages)
```
1. Replay Analysis (sc2reader)
   ↓
2. Event Detection & Prioritization
   ↓
3. Camera Director (AI-driven)
   ↓
4. Commentary Generation (Llama 3.1)
   ↓
5. Audio Synthesis (Coqui TTS)
   ↓
6. Video Recording (SC2 + FFmpeg/OBS)
   ↓
7. YouTube Upload
```

### Tech Stack
- **Language:** Python 3.11+
- **Replay Parsing:** sc2reader
- **SC2 Control:** python-sc2 (burnysc2 fork)
- **LLM:** Llama 3.1 8B via Ollama (local)
- **TTS:** Coqui TTS (local, GPU-accelerated)
- **Screen Capture:** FFmpeg or OBS Studio
- **Video Encoding:** FFmpeg (H.264, 1080p60)
- **Upload:** YouTube Data API v3

---

## 🚀 Setup (Zero-Budget)

### 1. Prerequisites
```powershell
# Verify SC2 is installed
Test-Path "C:\Program Files (x86)\StarCraft II\SC2_x64.exe"

# Verify Python 3.11+
python --version

# Verify NVIDIA GPU
nvidia-smi
```

### 2. Install Python Dependencies
```powershell
# Install Poetry (if not already installed)
pip install poetry

# Install project dependencies (creates virtual environment automatically)
poetry install

# Activate Poetry shell (optional)
poetry shell
```

### 3. Install Ollama (Local LLM)
```powershell
# Download from: https://ollama.com
winget install Ollama.Ollama

# Pull Llama 3.1 8B quantized
ollama pull llama3.1:8b-q4_K_M

# Test
ollama run llama3.1:8b-q4_K_M "Hello"
```

### 4. Install FFmpeg
```powershell
# Download from: https://ffmpeg.org/download.html
# Or use winget
winget install Gyan.FFmpeg

# Add to PATH, then test
ffmpeg -version
```

### 5. Install Coqui TTS (Sprint 3.2)
```powershell
poetry add TTS

# Test GPU acceleration
poetry run python -c "import torch; print(torch.cuda.is_available())"
```

### 6. Test Setup
```powershell
# Parse demo replay (Sprint 1.2)
poetry run python src/parse_replay.py

# Test SC2 connection (Sprint 1.4)
poetry run python tests/test_sc2.py
```

---

## 💻 Code Examples

### Replay Parser (Sprint 1.2)

**Extract basic metadata from SC2 replay files:**

```powershell
poetry run python src/parse_replay.py
```

**Output Format (JSON):**
```json
{
  "filename": "4323200_changeling_Mike_MagannathaAIE_v2.SC2Replay",
  "map": "Magannatha AIE",
  "duration_seconds": 568,
  "duration_human": "9:28",
  "players": [
    {
      "name": "changeling",
      "race": "Zerg",
      "result": "Win"
    },
    {
      "name": "Mike",
      "race": "Terran",
      "result": "Loss"
    }
  ]
}
```

### Event Extraction (Sprint 1.3)

**Extract game events with priorities:**

```powershell
# All events
poetry run python src/parse_replay.py --events

# Key moments only (high priority)
poetry run python src/parse_replay.py --events --key-moments

# Filter by player
poetry run python src/parse_replay.py --events --player Mike
```

**Event Types:**
- `expansion` - New base started (high priority)
- `upgrade` - Tech upgrade completed (high priority)  
- `battle` - Combat engagement (high priority)
- `building` - Structure completed (medium priority)
- `unit_death` - Unit killed (medium priority)

**Priority Levels:**
- `high` - Key moments (expansions, upgrades, big battles)
- `medium` - Noteworthy events (buildings, combat)
- `low` - Minor events (workers, small engagements)

### SC2 Replay Control (Sprint 1.4 / 2.1)

**Open and control replay playback:**

```python
from sc2.main import run_replay
from sc2.observer_ai import ObserverAI

class ReplayObserver(ObserverAI):
    async def on_start(self):
        print(f"Replay started: {self.game_info.map_name}")
    
    async def on_step(self, iteration: int):
        # Control replay, move camera, etc.
        if iteration % 100 == 0:
            game_time = iteration / 22.4
            print(f"Game time: {game_time:.1f}s")

# Run replay
run_replay(
    ReplayObserver(),
    replay_path="replays/demo/game.SC2Replay",
    realtime=True
)
```

### Screen Capture with FFmpeg (Sprint 2.2)

**Capture SC2 window:**

```python
import subprocess
import time

def capture_screen(output_file, duration=10):
    """Capture SC2 window with FFmpeg"""
    
    # Start recording
    process = subprocess.Popen([
        'ffmpeg',
        '-f', 'gdigrab',  # Windows screen capture
        '-framerate', '60',
        '-i', 'title=StarCraft II',  # SC2 window title
        '-t', str(duration),  # Duration in seconds
        '-c:v', 'libx264',  # H.264 codec
        '-preset', 'fast',
        '-crf', '23',  # Quality (lower = better)
        output_file
    ])
    
    # Wait for completion
    process.wait()
    return output_file
```

---

## 🎥 LLM Integration (Sprint 3.x)

### Local LLM Client
```python
import requests

class LocalLLM:
    def __init__(self, model="llama3.1:8b-q4_K_M"):
        self.model = model
        self.url = "http://localhost:11434"
    
    def generate(self, prompt, max_tokens=500):
        response = requests.post(
            f"{self.url}/api/generate",
            json={
                "model": self.model, 
                "prompt": prompt, 
                "max_tokens": max_tokens
            }
        )
        return response.json()["response"]

# Usage
llm = LocalLLM()
commentary = llm.generate("Describe this battle: 20 marines vs 15 zerglings")
```

### Local TTS Engine
```python
from TTS.api import TTS

class LocalTTS:
    def __init__(self):
        # Load model to GPU
        self.tts = TTS("tts_models/en/vctk/vits").to("cuda")
    
    def synthesize(self, text, output_file, speaker="p326"):
        """Generate speech from text"""
        self.tts.tts_to_file(
            text=text,
            file_path=output_file,
            speaker=speaker
        )
        return output_file

# Usage
tts = LocalTTS()
tts.synthesize("The game begins!", "output/commentary.wav")
```

---

## 🎮 Camera Director Algorithm

### Priority Scoring (10-point scale)
```python
PRIORITIES = {
    'major_battle': 10,      # 100+ supply engaged
    'base_destroy': 9,       # Nexus/CC/Hatchery killed
    'tech_complete': 8,      # Major tech (Hive, Colossus, etc.)
    'harassment': 7,         # Drops, run-bys
    'expansion': 6,          # New base
    'scout': 4,              # Observer, Overlord
}

def calculate_priority(event):
    base = PRIORITIES[event.type]
    if event.supply_lost > 50:
        base += 2  # Bonus for large engagements
    return min(base, 10)
```

### Camera Positioning
```python
async def move_camera_to_event(bot, event):
    """Move camera to focus on game event"""
    
    # Get event location
    x, y = event.location
    
    # Center camera
    await bot.client.move_camera(x, y)
    
    # Adjust zoom based on event type
    if event.type == 'major_battle':
        await bot.client.move_camera(x, y, distance=15)
    elif event.type == 'expansion':
        await bot.client.move_camera(x, y, distance=20)
```

---

## 🎤 Commentary Generation

### Prompt Structure
```python
def build_prompt(event, game_state):
    return f"""You are a StarCraft II commentator.

GAME CONTEXT (verified facts only):
- Time: {format_time(event.timestamp)}
- Event: {event.description}
- Supply: {game_state.supply[0]} vs {game_state.supply[1]}
- Workers: {game_state.workers[0]} vs {game_state.workers[1]}
- Army: {game_state.army_value[0]} vs {game_state.army_value[1]}

Generate 2-3 sentences of engaging commentary.
Be factual, specific, and avoid speculation.

Output JSON: {{"text": "...", "emotion": "neutral|excited|tense"}}
"""
```

### Validation System
```python
def validate_commentary(commentary, game_state):
    """Check commentary against game state"""
    
    # Extract claims from commentary
    claims = extract_claims(commentary)
    
    # Verify each claim
    for claim in claims:
        if not verify_claim(claim, game_state):
            return False, f"Invalid claim: {claim}"
    
    return True, "Commentary validated"
```

---

## 🔧 Configuration

### config/config.yaml
```yaml
sc2:
  install_path: "C:/Program Files (x86)/StarCraft II"
  replay_folder: "./replays"

llm:
  provider: ollama
  model: llama3.1:8b-q4_K_M
  base_url: http://localhost:11434
  temperature: 0.7

tts:
  provider: coqui
  model: tts_models/en/vctk/vits
  speaker: p326  # British male
  use_gpu: true

video:
  resolution: [1920, 1080]
  fps: 60
  codec: libx264
  preset: fast
  crf: 23

capture:
  method: ffmpeg  # or 'obs'
  window_title: "StarCraft II"

youtube:
  credentials: ./credentials/youtube_token.json
  auto_upload: false
  channel_id: ""
```

---

## 🐛 Troubleshooting

### SC2 Not Detected
```powershell
# Check installation
Get-ChildItem "C:\Program Files (x86)\StarCraft II\SC2_x64.exe"

# Verify environment
python -c "from sc2.paths import Paths; print(Paths().BASE)"
```

### Ollama Not Working
```powershell
# Check service status
ollama list

# Restart service
Stop-Process -Name ollama -Force
ollama serve

# Re-pull model
ollama pull llama3.1:8b-q4_K_M
```

### GPU Not Detected
```powershell
# Check CUDA
nvidia-smi

# Check PyTorch
poetry run python -c "import torch; print(torch.cuda.is_available())"

# Reinstall PyTorch with CUDA
poetry add torch torchvision torchaudio --source https://download.pytorch.org/whl/cu118
```

### FFmpeg Capture Issues
```powershell
# Test capture
ffmpeg -f gdigrab -i desktop -t 5 test.mp4

# List capture devices
ffmpeg -list_devices true -f dshow -i dummy
```

---

## 📚 Resources

- **Ollama:** https://ollama.com
- **Coqui TTS:** https://github.com/coqui-ai/TTS
- **sc2reader:** https://sc2reader.readthedocs.io
- **python-sc2:** https://burnysc2.github.io/python-sc2
- **FFmpeg:** https://ffmpeg.org
- **OBS Studio:** https://obsproject.com
- **YouTube API:** https://developers.google.com/youtube/v3

---

**For implementation timeline, see `IMPLEMENTATION.md`**  
**For common questions, see `FAQ.md`**
