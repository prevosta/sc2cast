# System Architecture - SC2Cast

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        SC2Cast System                            │
└─────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┴───────────────┐
                │                               │
        ┌───────▼────────┐              ┌──────▼──────┐
        │  Acquisition   │              │   Manual    │
        │    Module      │              │   Upload    │
        │  (AI Arena)    │              │             │
        └───────┬────────┘              └──────┬──────┘
                │                              │
                └──────────────┬───────────────┘
                               │
                      ┌────────▼─────────┐
                      │  Replay Storage  │
                      │   & Queue Mgmt   │
                      └────────┬─────────┘
                               │
                      ┌────────▼─────────┐
                      │ Analysis Engine  │
                      │   (sc2reader)    │
                      │                  │
                      │ - Parse events   │
                      │ - Extract stats  │
                      │ - Key moments    │
                      └────────┬─────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
        ┌───────▼────────┐          ┌────────▼─────────┐
        │     Camera     │          │   Commentary     │
        │    Director    │          │    Generator     │
        │                │          │                  │
        │ - Scene select │          │ - LLM prompts    │
        │ - Transitions  │          │ - Script timing  │
        │ - Priorities   │          │ - Emotion tags   │
        └───────┬────────┘          └────────┬─────────┘
                │                             │
                │                    ┌────────▼─────────┐
                │                    │ Audio Synthesis  │
                │                    │   (Coqui TTS)    │
                │                    │                  │
                │                    │ - Voice gen      │
                │                    │ - Music mix      │
                │                    └────────┬─────────┘
                │                             │
                └──────────────┬──────────────┘
                               │
                      ┌────────▼─────────┐
                      │ Video Recorder   │
                      │  (python-sc2 +   │
                      │     FFmpeg)      │
                      │                  │
                      │ - Replay control │
                      │ - Frame capture  │
                      │ - Overlays       │
                      │ - Encoding       │
                      └────────┬─────────┘
                               │
                      ┌────────▼─────────┐
                      │  Post-Process    │
                      │                  │
                      │ - Quality check  │
                      │ - Thumbnail gen  │
                      │ - Metadata       │
                      └────────┬─────────┘
                               │
                      ┌────────▼─────────┐
                      │ YouTube Uploader │
                      │   (YT API v3)    │
                      │                  │
                      │ - Authentication │
                      │ - Upload         │
                      │ - Playlist mgmt  │
                      └──────────────────┘
```

## Module Breakdown

### 1. Acquisition Module

**Responsibilities:**
- Poll AI Arena API for new replays
- Download replay files
- Validate replay integrity
- Queue management

**Input:** AI Arena API endpoint, filters (ELO, date)
**Output:** Valid .SC2Replay files in queue

**Key Classes:**
```python
class AIArenaClient:
    def fetch_replays(self, filters) -> List[ReplayMetadata]
    def download_replay(self, replay_id) -> Path
    
class ReplayQueue:
    def add(self, replay_path)
    def get_next(self) -> Path
    def mark_complete(self, replay_id)
    def mark_failed(self, replay_id, reason)
```

### 2. Analysis Engine

**Responsibilities:**
- Parse replay files completely
- Extract timeline of events
- Calculate statistics (APM, army value, economy)
- Identify key moments
- Generate analysis metadata

**Input:** .SC2Replay file
**Output:** AnalysisResult object

**Key Classes:**
```python
class ReplayAnalyzer:
    def parse_replay(self, replay_path) -> ReplayData
    def extract_events(self, replay) -> List[GameEvent]
    def identify_key_moments(self, events) -> List[KeyMoment]
    def calculate_statistics(self, replay) -> GameStatistics

class GameEvent:
    timestamp: float
    event_type: str
    location: Tuple[int, int]
    units_involved: List[str]
    players_involved: List[int]
    importance_score: float

class KeyMoment:
    timestamp: float
    duration: float
    event_type: str
    description: str
    priority: int
```

### 3. Camera Director

**Responsibilities:**
- Convert KeyMoments to camera instructions
- Resolve conflicts when multiple events overlap
- Generate smooth camera paths
- Handle transitions and context shots

**Input:** List[KeyMoment], ReplayData
**Output:** CameraScript

**Key Classes:**
```python
class CameraDirector:
    def create_camera_script(self, key_moments) -> CameraScript
    def resolve_conflicts(self, overlapping_events) -> CameraEvent
    def generate_transition(self, from_pos, to_pos) -> CameraPath
    
class CameraScript:
    events: List[CameraEvent]
    
    def get_camera_at_time(self, timestamp) -> CameraPosition
    def export_to_json(self) -> str

class CameraEvent:
    start_time: float
    end_time: float
    target_location: Tuple[float, float]
    zoom_level: float
    transition_type: str  # "cut", "pan", "zoom"
```

### 4. Commentary Generator

**Responsibilities:**
- Generate contextual commentary script
- Sync commentary with game events
- Apply appropriate tone and emotion
- Ensure factual accuracy

**Input:** ReplayData, List[KeyMoment], CameraScript
**Output:** CommentaryScript

**Key Classes:**
```python
class CommentaryGenerator:
    def __init__(self, llm_client, training_corpus):
        self.llm = llm_client
        self.corpus = training_corpus
        self.rag_db = VectorDatabase(training_corpus)
    
    def generate_script(self, replay_data, key_moments) -> CommentaryScript
    def generate_segment(self, game_state, context) -> CommentarySegment
    def validate_facts(self, commentary, game_state) -> bool
    
class CommentaryScript:
    segments: List[CommentarySegment]
    
    def export_to_srt(self) -> str
    def get_segment_at_time(self, timestamp) -> CommentarySegment

class CommentarySegment:
    start_time: float
    end_time: float
    text: str
    emotion: str  # "neutral", "excited", "tense", "analytical"
    speed: float  # Speaking rate multiplier
```

### 5. Audio Synthesizer

**Responsibilities:**
- Convert text to speech
- Apply prosody and emotion
- Mix commentary with music/effects
- Sync audio with video timeline

**Input:** CommentaryScript
**Output:** Audio file (.wav)

**Key Classes:**
```python
class AudioSynthesizer:
    def __init__(self, tts_engine, voice_model):
        self.tts = tts_engine
        self.voice = voice_model
    
    def synthesize_script(self, script) -> AudioFile
    def apply_emotion(self, text, emotion) -> SSML
    def mix_with_background(self, commentary, music) -> AudioFile
    
class AudioMixer:
    def add_background_music(self, commentary, intensity_curve)
    def normalize_volume(self, audio)
    def add_pauses(self, audio, pause_points)
```

### 6. Video Recorder

**Responsibilities:**
- Launch SC2 client with replay
- Control replay playback
- Follow camera script
- Capture frames
- Render overlays
- Encode video with audio

**Input:** Replay file, CameraScript, Audio file
**Output:** Video file (.mp4)

**Key Classes:**
```python
class VideoRecorder:
    def __init__(self, sc2_controller, overlay_renderer):
        self.sc2 = sc2_controller
        self.overlay = overlay_renderer
        self.encoder = FFmpegEncoder()
    
    def record_replay(self, replay_path, camera_script, audio) -> Path
    def capture_frame(self) -> np.ndarray
    def render_overlays(self, frame, game_state) -> np.ndarray
    
class SC2Controller:
    def load_replay(self, replay_path)
    def set_camera_position(self, x, y, zoom)
    def set_playback_speed(self, speed)
    def get_game_state(self) -> GameState
    def capture_screen(self) -> np.ndarray
    
class OverlayRenderer:
    def render_player_info(self, frame, players)
    def render_supply(self, frame, supply)
    def render_resources(self, frame, minerals, gas)
    def render_army_value(self, frame, army_values)
    def render_production(self, frame, production_tab)
```

### 7. YouTube Uploader

**Responsibilities:**
- Authenticate with YouTube API
- Generate video metadata
- Upload video file
- Organize into playlists
- Handle rate limits and retries

**Input:** Video file, ReplayData
**Output:** YouTube video URL

**Key Classes:**
```python
class YouTubeUploader:
    def __init__(self, credentials):
        self.youtube = build('youtube', 'v3', credentials=credentials)
    
    def upload_video(self, video_path, metadata) -> str
    def generate_metadata(self, replay_data) -> VideoMetadata
    def generate_thumbnail(self, replay_data) -> Image
    def add_to_playlist(self, video_id, playlist_id)
    
class VideoMetadata:
    title: str
    description: str
    tags: List[str]
    category_id: str
    privacy_status: str
    thumbnail: Optional[Path]
```

## Data Models

### ReplayData
```python
@dataclass
class ReplayData:
    replay_id: str
    file_path: Path
    game_length: float  # seconds
    map_name: str
    game_date: datetime
    players: List[PlayerInfo]
    winner: int
    matchup: str  # "TvZ", "PvP", etc.
    game_version: str
    average_mmr: Optional[int]
    
@dataclass
class PlayerInfo:
    name: str
    race: str  # "Terran", "Protoss", "Zerg"
    result: str  # "Win", "Loss"
    apm: float
    mmr: Optional[int]
```

### GameStatistics
```python
@dataclass
class GameStatistics:
    supply_by_time: List[Tuple[float, int, int]]
    worker_count: List[Tuple[float, int, int]]
    resource_collection_rate: List[Tuple[float, float, float]]
    army_value: List[Tuple[float, int, int]]
    bases_by_time: List[Tuple[float, int, int]]
    tech_timings: Dict[str, float]
    battles: List[BattleInfo]
    
@dataclass
class BattleInfo:
    start_time: float
    end_time: float
    location: Tuple[int, int]
    units_lost: Dict[int, List[str]]
    supply_lost: Dict[int, int]
    winner: Optional[int]
```

## Configuration Management

### config.yaml
```yaml
# SC2 Installation
sc2:
  path: /opt/StarCraftII
  display_mode: headless
  resolution: [1920, 1080]
  graphics_quality: medium
  fps: 60

# AI Arena
ai_arena:
  api_url: https://aiarena.net/api
  polling_interval: 3600  # seconds
  min_elo: 2000
  replay_limit: 100

# LLM Configuration (Zero-Budget: Local Llama 3.1)
llm:
  provider: ollama  # Local LLM via Ollama
  model: llama3.1:8b-q4_K_M  # Quantized for efficiency
  base_url: http://localhost:11434
  # api_key: NOT NEEDED! ✅
  temperature: 0.7
  max_tokens: 500

# TTS Configuration (Zero-Budget: Local Coqui)
tts:
  provider: coqui  # Local TTS (FREE)
  model: tts_models/en/vctk/vits
  speaker: p326  # British male voice
  sample_rate: 22050
  use_gpu: true

# Video Encoding
video:
  resolution: [1920, 1080]
  fps: 60
  codec: libx264
  preset: medium
  crf: 23
  audio_bitrate: 192k

# YouTube
youtube:
  credentials_path: ./credentials/youtube_token.json
  default_privacy: public
  default_category: 20  # Gaming
  playlist_id: ${YOUTUBE_PLAYLIST_ID}

# Processing
processing:
  max_parallel_jobs: 2
  temp_directory: ./temp
  output_directory: ./output
  keep_temp_files: false
```

## Database Schema (SQLite)

```sql
CREATE TABLE replays (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    replay_id TEXT UNIQUE NOT NULL,
    file_path TEXT NOT NULL,
    source TEXT NOT NULL,  -- 'ai_arena' or 'manual'
    status TEXT NOT NULL,  -- 'queued', 'processing', 'complete', 'failed'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,
    
    -- Game metadata
    game_length REAL,
    map_name TEXT,
    matchup TEXT,
    
    -- Processing results
    video_path TEXT,
    youtube_url TEXT,
    youtube_video_id TEXT,
    
    error_message TEXT
);

CREATE TABLE players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    replay_id TEXT NOT NULL,
    player_name TEXT NOT NULL,
    race TEXT NOT NULL,
    result TEXT NOT NULL,
    apm REAL,
    mmr INTEGER,
    
    FOREIGN KEY (replay_id) REFERENCES replays(replay_id)
);

CREATE TABLE key_moments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    replay_id TEXT NOT NULL,
    timestamp REAL NOT NULL,
    event_type TEXT NOT NULL,
    description TEXT,
    priority INTEGER,
    
    FOREIGN KEY (replay_id) REFERENCES replays(replay_id)
);

CREATE TABLE processing_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    replay_id TEXT NOT NULL,
    stage TEXT NOT NULL,  -- 'analysis', 'commentary', 'audio', 'video', 'upload'
    duration REAL NOT NULL,
    success BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (replay_id) REFERENCES replays(replay_id)
);
```

## Error Handling Strategy

### Retry Logic
```python
class RetryableOperation:
    def __init__(self, max_retries=3, backoff_factor=2):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
    
    def execute(self, operation, *args, **kwargs):
        for attempt in range(self.max_retries):
            try:
                return operation(*args, **kwargs)
            except RetryableError as e:
                if attempt == self.max_retries - 1:
                    raise
                wait_time = self.backoff_factor ** attempt
                logger.warning(f"Retry {attempt + 1}/{self.max_retries} after {wait_time}s")
                time.sleep(wait_time)
```

### Error Categories
1. **Retryable**: Network errors, API rate limits, temporary SC2 crashes
2. **Fatal**: Corrupt replays, invalid formats, missing dependencies
3. **Degraded**: LLM timeouts (fallback to simpler commentary), TTS failures (fallback to different voice)

## Logging Strategy

```python
import logging
from logging.handlers import RotatingFileHandler

# Structured logging
logger = logging.getLogger('sc2cast')
logger.setLevel(logging.INFO)

# File handler with rotation
file_handler = RotatingFileHandler(
    'logs/sc2cast.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))

logger.addHandler(file_handler)
```

### Log Levels
- **DEBUG**: Internal state, variable values
- **INFO**: Stage completions, progress updates
- **WARNING**: Retryable errors, degraded mode
- **ERROR**: Fatal errors, processing failures
- **CRITICAL**: System-wide failures

## Monitoring & Metrics

### Key Metrics to Track
1. **Processing Pipeline**:
   - Average processing time per replay
   - Success/failure rate by stage
   - Queue depth

2. **Quality Metrics**:
   - Commentary coherence score
   - Camera coverage (% of key moments captured)
   - Audio-video sync accuracy

3. **YouTube Performance**:
   - Upload success rate
   - Average views per video
   - Engagement metrics (likes, comments)

4. **Resource Usage**:
   - CPU/GPU utilization
   - Memory consumption
   - Disk space usage
