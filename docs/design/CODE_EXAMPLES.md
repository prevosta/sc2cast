# SC2Cast - Example Code Snippets

## 1. Replay Analysis

### Basic Replay Parsing
```python
# src/analysis/replay_analyzer.py

import sc2reader
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ReplayData:
    replay_id: str
    game_length: float
    map_name: str
    players: List['PlayerInfo']
    winner_id: int
    matchup: str

@dataclass
class PlayerInfo:
    name: str
    race: str
    result: str
    apm: float

class ReplayAnalyzer:
    def __init__(self):
        self.sc2reader = sc2reader
    
    def parse_replay(self, replay_path: str) -> ReplayData:
        """Parse SC2 replay file and extract basic information."""
        replay = sc2reader.load_replay(replay_path)
        
        # Extract player information
        players = []
        for player in replay.players:
            players.append(PlayerInfo(
                name=player.name,
                race=player.play_race,
                result=player.result,
                apm=player.avg_apm
            ))
        
        # Determine matchup (e.g., "TvZ", "PvP")
        matchup = ''.join([p.race[0] for p in players])
        
        # Find winner
        winner_id = next(
            (i for i, p in enumerate(replay.players) if p.result == 'Win'),
            None
        )
        
        return ReplayData(
            replay_id=replay.filehash,
            game_length=replay.game_length.total_seconds(),
            map_name=replay.map_name,
            players=players,
            winner_id=winner_id,
            matchup=matchup
        )
```

### Key Moment Detection
```python
# src/analysis/event_detector.py

from typing import List, Tuple
from collections import defaultdict
import numpy as np

@dataclass
class KeyMoment:
    timestamp: float
    duration: float
    event_type: str
    location: Tuple[float, float]
    priority: int
    description: str

class KeyMomentDetector:
    def detect_battles(self, death_events: List['GameEvent']) -> List[KeyMoment]:
        """Detect battles using spatiotemporal clustering."""
        clusters = self._cluster_events(death_events)
        
        battles = []
        for cluster in clusters:
            supply_lost = self._calculate_supply_lost(cluster)
            
            if supply_lost >= 20:  # Significant battle
                battles.append(KeyMoment(
                    timestamp=min(e.timestamp for e in cluster),
                    duration=max(e.timestamp for e in cluster) - min(e.timestamp for e in cluster),
                    event_type='major_engagement',
                    location=self._average_location(cluster),
                    priority=self._calculate_priority(supply_lost),
                    description=f"Major engagement - {supply_lost} supply lost"
                ))
        
        return battles
```

## 2. Camera Director

```python
# src/camera/director.py

from typing import List
from dataclasses import dataclass

@dataclass
class CameraEvent:
    start_time: float
    end_time: float
    target_location: Tuple[float, float]
    zoom_level: float
    transition_type: str

class CameraDirector:
    def create_camera_script(self, key_moments: List[KeyMoment]) -> 'CameraScript':
        """Convert key moments into smooth camera movements."""
        camera_events = []
        
        for moment in sorted(key_moments, key=lambda m: m.timestamp):
            # Handle conflicts
            if camera_events and moment.timestamp < camera_events[-1].end_time:
                camera_events[-1] = self._resolve_conflict(camera_events[-1], moment)
            else:
                # Add transition
                if camera_events:
                    transition = self._create_transition(
                        camera_events[-1].target_location,
                        moment.location,
                        camera_events[-1].end_time,
                        moment.timestamp
                    )
                    if transition:
                        camera_events.append(transition)
                
                # Add main event
                camera_events.append(CameraEvent(
                    start_time=moment.timestamp,
                    end_time=moment.timestamp + max(moment.duration, 3.0),
                    target_location=moment.location,
                    zoom_level=self._calculate_zoom(moment),
                    transition_type="smooth"
                ))
        
        return CameraScript(camera_events)
```

## 3. Commentary Generation (Local Llama 3.1)

```python
# src/commentary/generator.py

import requests
import json
from typing import Dict

class LocalLLMClient:
    """Client for Ollama/Llama 3.1 running locally."""
    
    def __init__(self, model: str = "llama3.1:8b-q4_K_M", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
    
    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 500) -> str:
        """Generate text using local Llama model."""
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "temperature": temperature,
                "num_predict": max_tokens,
                "stream": False
            }
        )
        return response.json()["response"]

class CommentaryGenerator:
    def __init__(self):
        self.llm = LocalLLMClient()  # No API key needed! ✅
    
    def generate_moment_commentary(self, moment: KeyMoment, 
                                   game_state: Dict) -> 'CommentarySegment':
        """Generate commentary for a specific moment."""
        
        prompt = f"""You are a StarCraft II commentator. Generate commentary for this moment.

VERIFIED FACTS:
- Game Time: {self._format_time(moment.timestamp)}
- Event: {moment.description}
- Supply: {game_state['supply'][0]} vs {game_state['supply'][1]}
- Workers: {game_state['workers'][0]} vs {game_state['workers'][1]}

Generate 2-3 sentences. Be specific and accurate.

Output JSON:
{{
  "text": "commentary here",
  "emotion": "excited|neutral|tense",
  "duration": 8.0
}}
"""
        
        # Local Llama generation (no API costs!)
        response_text = self.llm.generate(prompt, temperature=0.7, max_tokens=200)
        
        # Parse JSON from response
        try:
            result = json.loads(response_text)
        except json.JSONDecodeError:
            # Fallback if model doesn't output perfect JSON
            result = {
                "text": response_text,
                "emotion": "neutral",
                "duration": 8.0
            }
        
        return CommentarySegment(
            start_time=moment.timestamp,
            end_time=moment.timestamp + result['duration'],
            text=result['text'],
            emotion=result['emotion']
        )
```

## 4. Audio Synthesis (Coqui TTS - Local, Free)

```python
# src/audio/tts_engine.py

from TTS.api import TTS
from pydub import AudioSegment
import torch

class LocalTTSEngine:
    """Local text-to-speech using Coqui TTS (FREE!)"""
    
    def __init__(self, use_gpu: bool = True):
        # Use multi-speaker VITS model with good quality
        self.tts = TTS("tts_models/en/vctk/vits")
        
        if use_gpu and torch.cuda.is_available():
            self.tts.to("cuda")  # GPU acceleration
    
    def synthesize(self, text: str, speaker: str = "p326") -> np.ndarray:
        """
        Synthesize speech from text.
        
        Args:
            text: Text to synthesize
            speaker: VCTK speaker ID (p225-p376)
                    p326 = British male (good for casting)
                    p236 = British female
        
        Returns:
            Audio waveform as numpy array
        """
        wav = self.tts.tts(text=text, speaker=speaker)
        return wav

class AudioSynthesizer:
    def __init__(self):
        self.tts = LocalTTSEngine()  # No API costs! ✅
    
    def synthesize_script(self, segments: List['CommentarySegment'], 
                         output_path: str) -> str:
        """Synthesize audio for entire script."""
        audio_segments = []
        
        for segment in segments:
            # Local TTS generation
            wav = self.tts.synthesize(
                text=segment.text,
                speaker="p326"  # British male voice
            )
            
            # Convert to AudioSegment
            audio = AudioSegment(
                wav.tobytes(),
                frame_rate=22050,
                sample_width=2,
                channels=1
            )
            
            audio_segments.append({
                'audio': audio,
                'start_time': segment.start_time
            })
        
        # Merge with timing
        final_audio = self._merge_segments(audio_segments)
        final_audio.export(output_path, format="wav")
        return output_path
    
    def _merge_segments(self, segments):
        """Merge segments at correct timestamps."""
        max_time = max(seg['start_time'] for seg in segments) + 30
        silence = AudioSegment.silent(duration=int(max_time * 1000))
        
        for seg in segments:
            position_ms = int(seg['start_time'] * 1000)
            silence = silence.overlay(seg['audio'], position=position_ms)
        
        return silence
```

## 5. Video Recording

```python
# src/recording/video_encoder.py

import subprocess
import cv2
import numpy as np

class VideoEncoder:
    def __init__(self, output_path: str, fps: int = 60):
        self.output_path = output_path
        self.fps = fps
        self.resolution = (1920, 1080)
    
    def start(self, audio_path: str):
        """Start FFmpeg process."""
        command = [
            'ffmpeg', '-y',
            '-f', 'rawvideo',
            '-vcodec', 'rawvideo',
            '-s', f'{self.resolution[0]}x{self.resolution[1]}',
            '-pix_fmt', 'bgr24',
            '-r', str(self.fps),
            '-i', '-',  # stdin
            '-i', audio_path,
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '192k',
            self.output_path
        ]
        
        self.process = subprocess.Popen(command, stdin=subprocess.PIPE)
    
    def write_frame(self, frame: np.ndarray):
        """Write frame to video."""
        if frame.shape[:2] != (self.resolution[1], self.resolution[0]):
            frame = cv2.resize(frame, self.resolution)
        self.process.stdin.write(frame.tobytes())
    
    def finish(self):
        """Finalize video."""
        self.process.stdin.close()
        self.process.wait()

class OverlayRenderer:
    """Render HUD overlays."""
    
    def render(self, frame: np.ndarray, game_state: Dict) -> np.ndarray:
        """Add overlays to frame."""
        frame = frame.copy()
        
        self._draw_player_bar(frame, game_state)
        self._draw_supply(frame, game_state['supply'])
        self._draw_resources(frame, game_state['minerals'], game_state['gas'])
        self._draw_army_value(frame, game_state['army_value'])
        
        return frame
    
    def _draw_player_bar(self, frame, game_state):
        """Draw player names at top."""
        cv2.rectangle(frame, (0, 0), (1920, 60), (0, 0, 0), -1)
        
        player1 = f"{game_state['players'][0]['name']} ({game_state['players'][0]['race']})"
        cv2.putText(frame, player1, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.7, (255, 255, 255), 2)
        
        cv2.putText(frame, "VS", (920, 40), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.7, (255, 255, 255), 2)
        
        player2 = f"{game_state['players'][1]['name']} ({game_state['players'][1]['race']})"
        cv2.putText(frame, player2, (1400, 40), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.7, (255, 255, 255), 2)
```

## 6. YouTube Upload

```python
# src/upload/youtube_client.py

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

class YouTubeUploader:
    def __init__(self, credentials_path: str):
        creds = Credentials.from_authorized_user_file(credentials_path)
        self.youtube = build('youtube', 'v3', credentials=creds)
    
    def upload_video(self, video_path: str, replay_data: 'ReplayData') -> str:
        """Upload video to YouTube."""
        
        metadata = self.generate_metadata(replay_data)
        
        request = self.youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": metadata['title'],
                    "description": metadata['description'],
                    "tags": metadata['tags'],
                    "categoryId": metadata['categoryId']
                },
                "status": {
                    "privacyStatus": metadata['privacyStatus']
                }
            },
            media_body=MediaFileUpload(video_path, chunksize=-1, resumable=True)
        )
        
        response = request.execute()
        
        video_id = response['id']
        return f"https://youtube.com/watch?v={video_id}"
    
    def generate_metadata(self, replay_data: 'ReplayData') -> dict:
        """Generate video metadata."""
        title = (f"{replay_data.players[0].name} ({replay_data.players[0].race}) vs "
                f"{replay_data.players[1].name} ({replay_data.players[1].race}) - "
                f"{replay_data.map_name}")
        
        description = f"""
AI-Generated StarCraft II Cast

Players:
• {replay_data.players[0].name} ({replay_data.players[0].race})
• {replay_data.players[1].name} ({replay_data.players[1].race})

Map: {replay_data.map_name}
Game Length: {self._format_duration(replay_data.game_length)}

#StarCraft2 #SC2 #AIGenerated
"""
        
        return {
            'title': title[:100],
            'description': description,
            'tags': ["StarCraft 2", "SC2", replay_data.players[0].race, 
                    replay_data.players[1].race, "AI Commentary"],
            'categoryId': '20',
            'privacyStatus': 'public'
        }
```

## 7. Main Pipeline

```python
# src/orchestrator.py

from pathlib import Path
import logging

class SC2CastOrchestrator:
    def __init__(self, config: dict):
        self.config = config
        self.logger = logging.getLogger('sc2cast')
        
        # Initialize components
        self.analyzer = ReplayAnalyzer()
        self.detector = KeyMomentDetector()
        self.camera_director = CameraDirector()
        self.commentary_gen = CommentaryGenerator(config['llm']['api_key'])
        self.audio_synth = AudioSynthesizer()
        self.video_encoder = VideoEncoder()
        self.uploader = YouTubeUploader(config['youtube']['credentials_path'])
    
    def process_replay(self, replay_path: Path) -> str:
        """Process a replay end-to-end."""
        
        self.logger.info(f"[1/7] Analyzing replay: {replay_path.name}")
        replay_data = self.analyzer.parse_replay(str(replay_path))
        events = self.analyzer.extract_events(str(replay_path))
        
        self.logger.info("[2/7] Detecting key moments...")
        key_moments = self.detector.detect_battles(events)
        key_moments += self.detector.detect_expansions(events)
        
        self.logger.info("[3/7] Generating camera script...")
        camera_script = self.camera_director.create_camera_script(key_moments)
        
        self.logger.info("[4/7] Generating commentary...")
        commentary_script = self.commentary_gen.generate_script(replay_data, key_moments)
        
        self.logger.info("[5/7] Synthesizing audio...")
        audio_path = self.audio_synth.synthesize_script(
            commentary_script, 
            "temp/commentary.wav"
        )
        
        self.logger.info("[6/7] Recording video...")
        video_path = self._record_video(replay_path, camera_script, audio_path)
        
        if self.config['youtube']['auto_upload']:
            self.logger.info("[7/7] Uploading to YouTube...")
            youtube_url = self.uploader.upload_video(video_path, replay_data)
            self.logger.info(f"✓ Complete! Video: {youtube_url}")
            return youtube_url
        else:
            self.logger.info(f"✓ Complete! Video: {video_path}")
            return str(video_path)
```

---

These code examples provide concrete implementations of the key components. They can be used as starting points for the actual implementation.
