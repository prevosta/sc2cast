"""
Event-Based Recording Pipeline - Intelligent camera from game events.

Complete workflow:
1. Load replay → Extract events → Prioritize → Generate camera script
2. Launch replay and start recording with intelligent camera
"""

import json
from pathlib import Path
from typing import Optional
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sc2cast.event_extractor import EventExtractor
from sc2cast.event_prioritizer import EventPrioritizer
from sc2cast.script_generator import ScriptGenerator
from sc2cast.recording_pipeline import RecordingPipeline


class EventBasedPipeline:
    """
    Event-driven recording pipeline with intelligent camera.
    
    Automatically:
    - Extracts game events from replay
    - Prioritizes battles, expansions, tech
    - Generates camera script
    - Records with dynamic camera control
    """
    
    def __init__(self, replay_path: Path, output_path: Path):
        """
        Initialize event-based pipeline.
        
        Args:
            replay_path: Path to .SC2Replay file
            output_path: Output video file path
        """
        self.replay_path = replay_path
        self.output_path = output_path
    
    def run(self):
        """Execute complete event-based recording pipeline."""
        print("=" * 80)
        print("EVENT-BASED RECORDING PIPELINE")
        print("=" * 80)
        print(f"\n📂 Replay: {self.replay_path.name}")
        print(f"📹 Output: {self.output_path}")
        
        # Step 1: Extract events
        print("\n" + "=" * 80)
        print("STEP 1: EXTRACT EVENTS")
        print("=" * 80)
        
        extractor = EventExtractor(str(self.replay_path))
        extractor.load_replay()
        extractor.extract_events()
        
        raw_events = extractor.events
        replay_duration = extractor.replay.game_length.seconds if extractor.replay else 378
        
        print(f"✅ Extracted {len(raw_events)} events")
        print(f"✅ Replay duration: {replay_duration}s")
        
        # Step 2: Prioritize events
        print("\n" + "=" * 80)
        print("STEP 2: PRIORITIZE & CLUSTER EVENTS")
        print("=" * 80)
        
        prioritizer = EventPrioritizer()
        priority_events = prioritizer.process_events(raw_events)
        
        summary = prioritizer.get_summary()
        print(f"✅ {summary['total_events']} priority events")
        print(f"   Battles: {summary['battles']}")
        print(f"   High-priority: {summary['by_priority']['high']}")
        
        # Step 3: Generate camera script
        print("\n" + "=" * 80)
        print("STEP 3: GENERATE CAMERA SCRIPT")
        print("=" * 80)
        
        generator = ScriptGenerator()
        camera_shots = generator.generate_from_events(priority_events, replay_duration)
        
        print(f"✅ {len(camera_shots)} camera shots generated")
        
        # Show key shots
        print("\nKey camera movements:")
        battle_shots = [s for s in camera_shots if s.shot_type.value == 'minimap_jump'][:5]
        for shot in battle_shots:
            mins = shot.time_seconds // 60
            secs = shot.time_seconds % 60
            desc = shot.params.get('description', '')
            print(f"  {mins:02d}:{secs:02d} - {desc}")
        
        # Convert shots to dict format for RecordingPipeline
        camera_script = []
        for shot in camera_shots:
            camera_script.append({
                'time': shot.time_seconds,  # CameraDirector expects 'time' not 'time_seconds'
                'type': shot.shot_type.value,
                'params': shot.params
            })
        
        # Step 4: Execute recording
        print("\n" + "=" * 80)
        print("STEP 4: RECORD WITH EVENT-BASED CAMERA")
        print("=" * 80)
        print("\n🎬 Starting automated recording...")
        print("   (This will take several minutes)\n")
        
        pipeline = RecordingPipeline(
            replay_path=self.replay_path,
            camera_script=camera_script,
            output_path=self.output_path,
            replay_speed="fast_x4"  # 8x speed
        )
        
        success = pipeline.run()
        
        # Final summary
        print("\n" + "=" * 80)
        print("RECORDING COMPLETE")
        print("=" * 80)
        
        if success and self.output_path.exists():
            file_size_mb = self.output_path.stat().st_size / (1024 * 1024)
            print(f"\n✅ Video saved: {self.output_path}")
            print(f"   Size: {file_size_mb:.1f} MB")
            print(f"   Duration: {replay_duration}s gameplay")
            print(f"   Camera shots: {len(camera_shots)}")
            print(f"   Battles tracked: {summary['battles']}")
            print("\n🎉 EVENT-BASED RECORDING SUCCESS!")
        else:
            print("\n❌ Recording failed!")
        
        return success


def main():
    """Run event-based recording pipeline."""
    # Use the new replay
    replay_path = Path("replays/4323395_Mike_SpeedlingBot_UltraloveAIE_v2.SC2Replay")
    output_path = Path("output/event_based_recording.mp4")
    
    if not replay_path.exists():
        print(f"❌ Replay not found: {replay_path}")
        return
    
    # Run pipeline
    pipeline = EventBasedPipeline(replay_path, output_path)
    success = pipeline.run()
    
    if success:
        print("\n✅ Event-based recording pipeline complete!")
        print(f"📹 Watch your video: {output_path}")
    else:
        print("\n❌ Recording failed!")


if __name__ == "__main__":
    main()
