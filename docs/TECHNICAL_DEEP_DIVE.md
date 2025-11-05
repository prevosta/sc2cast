# Technical Deep Dive - SC2Cast

## 1. SC2 Replay Analysis with Python

### Available Libraries

#### python-sc2 (BurnySc2)
- **Purpose**: Bot development and game interaction
- **Pros**: Active development, good API, unit control
- **Cons**: Primarily for bots, not replay analysis
- **Use Case**: Video recording and game state observation

#### sc2reader
- **Purpose**: Replay file parsing and analysis
- **Pros**: Pure Python, no SC2 client needed, fast parsing
- **Cons**: Limited to replay data, no visual access
- **Use Case**: Initial analysis, metadata extraction, event timeline

```python
import sc2reader
replay = sc2reader.load_replay('replay.SC2Replay')
# Access: replay.players, replay.events, replay.game_length
```

#### pysc2 (DeepMind)
- **Purpose**: RL environment for SC2
- **Pros**: Official Blizzard support, feature layers
- **Cons**: Complex setup, primarily for AI training
- **Use Case**: Alternative for game observation

### Recommended Approach
**Hybrid System**: Use sc2reader for initial analysis and python-sc2 for playback/recording

```python
# Phase 1: Fast Analysis (sc2reader)
replay_data = analyze_replay_events(replay_file)
important_timestamps = identify_key_moments(replay_data)

# Phase 2: Recording (python-sc2)
record_replay_with_camera(replay_file, important_timestamps)
```

## 2. Camera Director Algorithm

### Priority System

```python
class CameraEvent:
    def __init__(self, timestamp, location, priority, duration, event_type):
        self.timestamp = timestamp
        self.location = location
        self.priority = priority  # 1-10 scale
        self.duration = duration
        self.event_type = event_type

PRIORITY_WEIGHTS = {
    'major_engagement': 10,      # Army vs army, >20 supply
    'base_destruction': 9,        # Nexus/CC/Hatchery destroyed
    'tech_completion': 8,         # Key tech finished (fleet beacon, ghost academy)
    'drop_harassment': 7,         # Units in opponent's base
    'expansion': 6,               # New base taken
    'scout': 4,                   # Scouting actions
    'production': 3,              # Building production
}
```

### Camera Smoothing
```python
def smooth_camera_transition(current_pos, target_pos, duration=1.5):
    """
    Ease-in-out camera movement to avoid jarring jumps
    Uses cubic Bezier curves for natural feel
    """
    pass
```

### Concurrent Event Handling
When multiple events happen simultaneously:
1. Prioritize by importance
2. Use picture-in-picture for secondary action
3. Quick cuts for rapid succession events
4. Return to overview for context

### Context Awareness
```python
def should_stay_on_scene(current_event, elapsed_time):
    """
    Decide if camera should remain on current scene
    Factors:
    - Event importance
    - Time already spent
    - Completion status (battle still ongoing?)
    - New event priority comparison
    """
    pass
```

## 3. Commentary Generation System (Zero-Budget: Local LLM)

### Local LLM Solution: Llama 3.1 8B

**Why Local Instead of APIs?**
- **Zero cost**: No API fees ($0 vs $100-300/month)
- **Privacy**: All data stays local
- **No rate limits**: Unlimited generation
- **Offline capable**: Works without internet

### Setup with Ollama

Ollama is the easiest way to run local LLMs:

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull Llama 3.1 8B (quantized for efficiency)
ollama pull llama3.1:8b-q4_K_M

# Test it
ollama run llama3.1:8b-q4_K_M "Describe a marine push in StarCraft II"
```

### Integration Code

```python
# src/commentary/llm_client.py
import requests
import json

class LocalLLMClient:
    """Client for local Llama via Ollama API."""
    
    def __init__(self, model="llama3.1:8b-q4_K_M", 
                 base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url
    
    def generate(self, prompt: str, temperature: float = 0.7, 
                max_tokens: int = 500) -> str:
        """Generate commentary using local Llama."""
        
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "temperature": temperature,
                "options": {
                    "num_predict": max_tokens,
                    "top_p": 0.9,
                },
                "stream": False
            }
        )
        
        return response.json()["response"]
```

### Training Data Collection (Optional Enhancement)

For better quality, collect SC2 caster transcripts:

#### YouTube Transcript Extraction
```python
from youtube_transcript_api import YouTubeTranscriptApi

def collect_caster_transcripts(channel_ids):
    """
    Scrape transcripts from popular SC2 casters:
    - Lowko
    - PiG
    - Harstem
    - WinterStarcraft
    - Artosis
    """
    pass
```

#### Data Structure
```json
{
  "timestamp": "00:03:45",
  "game_state": {
    "supply": [45, 38],
    "workers": [32, 28],
    "event_type": "early_aggression",
    "units_involved": ["marine", "marauder", "medivac"]
  },
  "commentary": "And here comes the two medivac timing! This is exactly what we expected from a Terran on this map...",
  "emotion": "excitement",
  "caster": "lowko"
}
```

### LLM Approach: Local Llama 3.1

**No API Costs** - Everything runs on your GPU:

#### Option 1: Ollama (Recommended for Development)
```python
# Simple prompt-based generation
commentary = llm.generate(f"""
You are a StarCraft II commentator.

Game State:
- Time: {game_time}
- Event: {event_description}
- Supply: {supply}

Generate 2-3 sentences of commentary:
""")
```

#### Option 2: Fine-tuning (Advanced, Optional)
- Collect 100+ hours of SC2 caster transcripts
- Fine-tune Llama 3.1 using LoRA
- Results in more natural, SC2-specific commentary
- Can be done later as enhancement

#### Option 3: RAG (Retrieval-Augmented Generation)
```python
def generate_commentary(game_state, event):
    # Find similar past situations
    similar_contexts = vector_db.search(game_state)
    
    # Use as examples for LLM
    prompt = build_prompt_with_examples(game_state, similar_contexts)
    
    return llm.generate(prompt)
```

### Commentary Types

1. **Opening Analysis** (0-5 minutes)
   - Build order identification
   - Strategic prediction
   - Map analysis

2. **Mid-game Development** (5-15 minutes)
   - Economy comparison
   - Tech path discussion
   - Positioning analysis

3. **Engagement Commentary** (battles)
   - Unit composition breakdown
   - Micro analysis
   - Engagement outcome prediction

4. **Strategic Analysis** (throughout)
   - Player decision making
   - Alternative strategies
   - Victory condition discussion

### Emotion and Pacing
```python
def calculate_excitement_level(game_state):
    """
    Modulate speech tempo and energy based on:
    - Battle intensity
    - Supply difference changes
    - Game time (late game = more intense)
    - Comeback potential
    """
    factors = {
        'battle_supply_engaged': 0.4,
        'supply_swing': 0.3,
        'game_stage': 0.2,
        'upset_potential': 0.1
    }
    return weighted_score(factors)
```

## 4. Video Recording System

### SC2 Client Control

#### Headless Operation
```python
# Run SC2 in offscreen rendering mode
SC2_PATH = "/opt/StarCraftII"
settings = {
    "display_mode": "headless",
    "resolution": "1920x1080",
    "graphics": "medium",  # Balance quality/performance
    "fps": 60
}
```

#### Replay Playback Control
```python
class ReplayController:
    def __init__(self, replay_path):
        self.replay = replay_path
        self.current_time = 0
        
    def jump_to_time(self, game_seconds):
        """Jump to specific game time"""
        pass
    
    def set_playback_speed(self, speed):
        """1.0 = normal, 2.0 = 2x speed, etc."""
        pass
    
    def set_camera_position(self, x, y):
        """Move camera to map coordinates"""
        pass
    
    def capture_frame(self):
        """Capture current game frame"""
        pass
```

### Overlay System

#### Real-time Graphics
```python
import cv2
import numpy as np

class OverlayRenderer:
    def add_player_info(self, frame, player_data):
        """Add player names, races, scores at top"""
        pass
    
    def add_supply_counter(self, frame, supply):
        """Display supply in corner"""
        pass
    
    def add_resource_count(self, frame, minerals, gas):
        """Show resource counts"""
        pass
    
    def add_army_value(self, frame, army_value):
        """Display army value comparison"""
        pass
    
    def add_production_tab(self, frame, production_data):
        """Show building production status"""
        pass
```

### FFmpeg Integration
```python
ffmpeg_command = [
    'ffmpeg',
    '-f', 'rawvideo',
    '-pixel_format', 'bgr24',
    '-video_size', '1920x1080',
    '-framerate', '60',
    '-i', 'pipe:0',  # Input from stdin
    '-i', 'commentary_audio.wav',  # Audio track
    '-c:v', 'libx264',
    '-preset', 'medium',
    '-crf', '23',  # Quality factor
    '-c:a', 'aac',
    '-b:a', '192k',
    'output.mp4'
]
```

## 5. Audio Synthesis (Zero-Budget: Coqui TTS)

### TTS Solution: Coqui TTS (Local, Free)

**Why Coqui TTS?**
- **Zero cost**: Completely free and open-source
- **Good quality**: 7/10 voice quality (vs 10/10 for ElevenLabs)
- **Local**: Runs on GPU or CPU
- **Fast**: 2-5x real-time on GPU
- **Customizable**: Multiple voices and speakers

### Installation & Setup

```bash
# Install Coqui TTS
pip install TTS

# List available models
tts --list_models

# Recommended model for SC2 casting
model = "tts_models/en/vctk/vits"  # Multi-speaker, good quality
```

### Integration Code

```python
# src/audio/tts_engine.py
from TTS.api import TTS
import torch

class LocalTTSEngine:
    def __init__(self, use_gpu=True):
        self.device = "cuda" if use_gpu and torch.cuda.is_available() else "cpu"
        self.tts = TTS(
            model_name="tts_models/en/vctk/vits"
        ).to(self.device)
    
    def synthesize(self, text: str, speaker: str = "p326",
                   emotion: str = "neutral"):
        """
        Generate speech from text.
        speaker: "p326" = British male (good for casting)
        """
        wav = self.tts.tts(text=text, speaker=speaker)
        return wav
```

### Voice Selection

Best speakers for SC2 casting:
- **p326**: British male, clear, good for analytical casting
- **p330**: American male, energetic
- **p340**: American male, deeper voice

### TTS Options Comparison (Updated)

| Option | Quality | Speed | Cost | Decision |
|--------|---------|-------|------|----------|
| **Coqui TTS (local)** | 7/10 | Fast | **FREE** | ✅ **CHOSEN** |
| ElevenLabs | 10/10 | Fast | $22-330/mo | ❌ Too expensive |
| Google Cloud TTS | 8/10 | Fast | $$  | ❌ API costs |
| Azure TTS | 8/10 | Fast | $$ | ❌ API costs |

**Decision**: Use Coqui TTS - acceptable quality at zero cost!
```python
class AudioSynthesizer:
    def __init__(self, primary_tts="coqui", fallback_tts="gtts"):
        self.primary = load_tts(primary_tts)
        self.fallback = load_tts(fallback_tts)
    
    def generate_commentary_audio(self, script_segments):
        audio_files = []
        for segment in script_segments:
            # Add prosody markers
            ssml = self.add_prosody(segment.text, segment.emotion)
            audio = self.primary.synthesize(ssml)
            audio_files.append(audio)
        
        # Concatenate with timing
        return self.merge_audio_with_timing(audio_files, script_segments)
    
    def add_prosody(self, text, emotion):
        """Add SSML tags for emphasis, pauses, pitch"""
        if emotion == "excitement":
            return f'<prosody rate="fast" pitch="+10%">{text}</prosody>'
        elif emotion == "tension":
            return f'<prosody rate="slow" pitch="-5%">{text}</prosody>'
        return text
```

### Audio Mixing
```python
from pydub import AudioSegment

def mix_commentary_with_music(commentary, game_time):
    """
    Add background music and game sounds
    - Quiet background music during calm moments
    - No music during intense battles
    - Fade in/out for transitions
    """
    music = get_appropriate_music(game_time)
    music = music - 25  # Reduce volume by 25dB
    
    return commentary.overlay(music)
```

## 6. YouTube Upload System

### Authentication
```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_youtube_service():
    """
    OAuth 2.0 authentication
    Store credentials securely in environment
    """
    creds = Credentials.from_authorized_user_file('token.json')
    return build('youtube', 'v3', credentials=creds)
```

### Automated Metadata
```python
def generate_video_metadata(replay_data):
    title = f"{replay_data.player1} ({replay_data.race1}) vs " \
            f"{replay_data.player2} ({replay_data.race2}) - " \
            f"{replay_data.map_name}"
    
    description = f"""
    AI-Generated StarCraft II Cast
    
    Players:
    - {replay_data.player1} ({replay_data.race1})
    - {replay_data.player2} ({replay_data.race2})
    
    Map: {replay_data.map_name}
    Game Length: {format_time(replay_data.game_length)}
    
    Key Moments:
    {generate_timestamps(replay_data.key_events)}
    
    #StarCraftII #SC2 #AIGenerated
    """
    
    tags = [
        "StarCraft 2", "SC2", replay_data.race1, replay_data.race2,
        replay_data.map_name, "AI Commentary", "Gaming"
    ]
    
    return {
        'title': title,
        'description': description,
        'tags': tags,
        'categoryId': '20',  # Gaming category
        'privacyStatus': 'public'
    }
```

## 7. AI Arena Integration

### Replay Downloading
```python
import requests

class AIArenaClient:
    BASE_URL = "https://aiarena.net/api"
    
    def get_recent_replays(self, limit=100, min_elo=2000):
        """
        Fetch replays from AI Arena
        Filter by ELO for quality games
        """
        endpoint = f"{self.BASE_URL}/replays/"
        params = {
            'limit': limit,
            'ordering': '-created',
            'min_elo': min_elo
        }
        response = requests.get(endpoint, params=params)
        return response.json()
    
    def download_replay(self, replay_id, output_path):
        """Download specific replay file"""
        url = f"{self.BASE_URL}/replays/{replay_id}/download/"
        response = requests.get(url, stream=True)
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
```

## 8. Docker Environment

### Dockerfile
```dockerfile
FROM nvidia/cuda:12.2-runtime-ubuntu22.04

# Install Python
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    ffmpeg \
    xvfb \
    wget \
    unzip

# Install StarCraft II
RUN wget http://blzdistsc2-a.akamaihd.net/Linux/SC2.4.10.zip && \
    unzip -P iagreetotheeula SC2.4.10.zip -d /opt/ && \
    rm SC2.4.10.zip

# Python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Set up workspace
WORKDIR /workspace
COPY . .

# Environment variables
ENV SC2PATH=/opt/StarCraftII
ENV DISPLAY=:99

CMD ["/bin/bash"]
```

### VS Code Dev Container
```json
{
  "name": "SC2Cast Development",
  "dockerFile": "Dockerfile",
  "mounts": [
    "source=${localWorkspaceFolder}/replays,target=/workspace/replays,type=bind",
    "source=${localWorkspaceFolder}/output,target=/workspace/output,type=bind"
  ],
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.black-formatter"
      ]
    }
  },
  "runArgs": ["--gpus", "all"],
  "postCreateCommand": "pip install -e ."
}
```

## 9. Performance Optimization

### Processing Pipeline
```
Single 20-minute replay:
- Analysis: 30 seconds (sc2reader)
- Commentary Generation: 2 minutes (LLM)
- Audio Synthesis: 1 minute (TTS)
- Video Recording: 10 minutes (1x playback speed)
- Encoding: 3 minutes (FFmpeg)
- Upload: 5 minutes (network dependent)

Total: ~21 minutes per replay
```

### Optimization Strategies
1. **Parallel Processing**: Analyze multiple replays simultaneously
2. **GPU Acceleration**: Use CUDA for video encoding and LLM inference
3. **Caching**: Store analysis results, reuse commentary patterns
4. **Adaptive Quality**: Lower quality for testing, high for production
5. **Batch Processing**: Queue multiple replays, process overnight

## 10. Quality Control

### Automated Checks
```python
class QualityValidator:
    def validate_commentary(self, script):
        """
        Check:
        - No repetitive phrases
        - Factual accuracy (units mentioned exist in replay)
        - Appropriate length
        - Natural transitions
        """
        pass
    
    def validate_camera(self, camera_log, key_events):
        """
        Ensure:
        - All major events captured
        - No excessive jumping
        - Smooth transitions
        - Appropriate dwell time
        """
        pass
    
    def validate_video(self, video_path):
        """
        Verify:
        - Resolution and framerate
        - Audio sync
        - No corruption
        - Acceptable file size
        """
        pass
```

### Human Review Queue
- Flag unusual games for review
- Manual thumbnail selection
- Commentary spot-checks
- Viewer feedback integration
