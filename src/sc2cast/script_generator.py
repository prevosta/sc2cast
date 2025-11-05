"""
Script Generator - Convert game events to camera scripts.

Takes prioritized events and generates CameraShot sequences for the director.
"""

import json
from pathlib import Path
from typing import List, Dict, Any
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sc2cast.camera_director import CameraShot, ShotType


class ScriptGenerator:
    """Generate camera scripts from prioritized game events."""
    
    def __init__(self):
        """Initialize script generator."""
        self.shots: List[CameraShot] = []
    
    def generate_from_events(self, prioritized_events: List[Dict], replay_duration: int) -> List[CameraShot]:
        """
        Generate camera script from prioritized events.
        
        Args:
            prioritized_events: List of events from event_prioritizer
            replay_duration: Total replay duration in seconds
            
        Returns:
            List of CameraShot objects ready for execution
        """
        print(f"🎬 Generating camera script from {len(prioritized_events)} events...")
        
        self.shots = []
        
        # Add opening shot
        self._add_opening_shots()
        
        # Convert events to camera shots
        for event in prioritized_events:
            self._process_event(event)
        
        # Add periodic overview shots between events
        self._add_overview_shots(prioritized_events, replay_duration)
        
        # Sort shots by time
        self.shots.sort(key=lambda s: s.time_seconds)
        
        print(f"✅ Generated {len(self.shots)} camera shots")
        return self.shots
    
    def _add_opening_shots(self):
        """Add opening shots at start of replay."""
        # Start with Player 1 view
        self.shots.append(CameraShot(
            time_seconds=5,
            shot_type=ShotType.PLAYER_VIEW,
            params={'player': 1}
        ))
        
        # Show income stats early
        self.shots.append(CameraShot(
            time_seconds=15,
            shot_type=ShotType.STAT_PANEL,
            params={'panel': 'income'}
        ))
        
        # Switch to Player 2
        self.shots.append(CameraShot(
            time_seconds=25,
            shot_type=ShotType.PLAYER_VIEW,
            params={'player': 2}
        ))
    
    def _process_event(self, event: Dict):
        """Convert a single event to camera shot(s)."""
        event_time = event['time_seconds']
        event_type = event['event_type']
        location = event.get('location')
        priority = event.get('priority', 'medium')
        
        # Add arrival buffer - move camera before event peaks
        ARRIVAL_BUFFER = 3  # seconds before event
        arrival_time = max(5, event_time - ARRIVAL_BUFFER)
        
        if event_type == 'battle' and location:
            # For battles, move camera to location
            self.shots.append(CameraShot(
                time_seconds=arrival_time,
                shot_type=ShotType.MINIMAP_JUMP,
                params={
                    'x': location['x'],
                    'y': location['y'],
                    'description': f"Move to battle @ ({location['x']}, {location['y']})"
                }
            ))
            
            # Show army stats during battle
            if priority in ['high', 'medium']:
                self.shots.append(CameraShot(
                    time_seconds=event_time,
                    shot_type=ShotType.STAT_PANEL,
                    params={'panel': 'army'}
                ))
        
        elif event_type == 'expansion' and location:
            # For expansions, move camera and show income
            self.shots.append(CameraShot(
                time_seconds=arrival_time,
                shot_type=ShotType.MINIMAP_JUMP,
                params={
                    'x': location['x'],
                    'y': location['y'],
                    'description': f"Expansion @ ({location['x']}, {location['y']})"
                }
            ))
            
            # Show income stats for expansion
            self.shots.append(CameraShot(
                time_seconds=event_time + 2,
                shot_type=ShotType.STAT_PANEL,
                params={'panel': 'income'}
            ))
        
        elif event_type == 'tech' and location:
            # For tech buildings, quick look
            self.shots.append(CameraShot(
                time_seconds=arrival_time,
                shot_type=ShotType.MINIMAP_JUMP,
                params={
                    'x': location['x'],
                    'y': location['y'],
                    'description': f"Tech building @ ({location['x']}, {location['y']})"
                }
            ))
    
    def _add_overview_shots(self, events: List[Dict], replay_duration: int):
        """Add periodic player overview shots between events."""
        MIN_GAP = 20  # Minimum gap between events to add overview
        
        # Get event times
        event_times = sorted([e['time_seconds'] for e in events])
        
        # Add player alternating shots in gaps
        current_player = 1
        last_event_time = 0
        
        for event_time in event_times:
            gap = event_time - last_event_time
            
            if gap >= MIN_GAP:
                # Add overview shot in the middle of gap
                overview_time = last_event_time + (gap // 2)
                
                self.shots.append(CameraShot(
                    time_seconds=overview_time,
                    shot_type=ShotType.PLAYER_VIEW,
                    params={'player': current_player}
                ))
                
                # Alternate players
                current_player = 2 if current_player == 1 else 1
            
            last_event_time = event_time
        
        # Add final overview if there's time
        if replay_duration - last_event_time >= MIN_GAP:
            overview_time = last_event_time + 10
            if overview_time < replay_duration - 5:
                self.shots.append(CameraShot(
                    time_seconds=overview_time,
                    shot_type=ShotType.PLAYER_VIEW,
                    params={'player': current_player}
                ))
    
    def save_script(self, shots: List[CameraShot], output_path: Path):
        """Save camera script to JSON for debugging."""
        shots_data = []
        for shot in shots:
            shots_data.append({
                'time_seconds': shot.time_seconds,
                'shot_type': shot.shot_type.value,
                'params': shot.params
            })
        
        output_data = {
            'total_shots': len(shots),
            'shots': shots_data
        }
        
        output_path.parent.mkdir(exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"💾 Saved camera script to: {output_path}")


def main():
    """Test script generation."""
    print("=" * 80)
    print("CAMERA SCRIPT GENERATOR")
    print("=" * 80)
    
    # Load prioritized events
    events_path = Path("output/prioritized_events.json")
    if not events_path.exists():
        print(f"❌ No prioritized events found: {events_path}")
        print("   Run event_prioritizer.py first!")
        return
    
    with open(events_path, 'r') as f:
        data = json.load(f)
        prioritized_events = data['events']
    
    print(f"\n📂 Loaded {len(prioritized_events)} prioritized events")
    
    # Generate script
    generator = ScriptGenerator()
    
    # Use new replay duration (6:18 = 378 seconds)
    replay_duration = 378
    shots = generator.generate_from_events(prioritized_events, replay_duration)
    
    # Show generated shots
    print("\n" + "=" * 80)
    print("GENERATED CAMERA SCRIPT")
    print("=" * 80)
    
    print(f"\nTotal Shots: {len(shots)}")
    print("\nShot Timeline:")
    for shot in shots:
        mins = shot.time_seconds // 60
        secs = shot.time_seconds % 60
        desc = shot.params.get('description', '')
        if not desc:
            if shot.shot_type == ShotType.PLAYER_VIEW:
                desc = f"Player {shot.params.get('player', '?')} view"
            elif shot.shot_type == ShotType.STAT_PANEL:
                desc = f"{shot.params.get('panel', '?')} stats"
            else:
                desc = str(shot.params)
        
        print(f"  {mins:02d}:{secs:02d} - {shot.shot_type.value:15} - {desc}")
    
    # Save script
    output_path = Path("output/generated_camera_script.json")
    generator.save_script(shots, output_path)
    
    print("\n✅ Camera script generation complete!")
    print("\n💡 Next: Update recording_pipeline.py to use this script!")


if __name__ == "__main__":
    main()
