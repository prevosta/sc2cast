"""
Custom SC2 Replay Loader - Workaround for cache_handles bug.

The replays we have are from AI matches and lack cache_handles data,
which causes sc2reader to crash. This module provides a workaround.
"""

import sc2reader
from sc2reader.resources import Replay
import types


def create_patched_load_details(original_method):
    """Create a patched version of load_details."""
    def patched_load_details(self):
        """Call original but handle cache_handles error."""
        try:
            return original_method(self)
        except IndexError as e:
            if "cache_handles" in str(e) or "list index out of range" in str(e):
                # Manually set default region for AI games
                self.region = "unknown"
                print("   ℹ️  Patched: Set region='unknown' (AI game)")
            else:
                raise
    return patched_load_details


# Apply the patch
if hasattr(Replay, 'load_details'):
    original_load_details = Replay.load_details
    Replay.load_details = create_patched_load_details(original_load_details)
    print("🔧 Applied sc2reader patch for cache_handles bug")


def load_replay_safe(replay_path: str, load_level: int = 4):
    """
    Load replay with our patched version.
    
    Args:
        replay_path: Path to .SC2Replay file
        load_level: How much data to load (0-4)
        
    Returns:
        Replay object with events
    """
    print(f"📂 Loading replay: {replay_path}")
    print(f"   Load level: {load_level}")
    
    try:
        replay = sc2reader.load_replay(
            replay_path,
            load_level=load_level,
            load_map=False
        )
        print(f"✅ Replay loaded successfully!")
        print(f"   Duration: {replay.game_length}")
        print(f"   Region: {getattr(replay, 'region', 'N/A')}")
        
        # Check for events
        if hasattr(replay, 'events'):
            print(f"   Total events: {len(replay.events)}")
        if hasattr(replay, 'tracker_events'):
            print(f"   Tracker events: {len(replay.tracker_events)}")
        
        return replay
        
    except Exception as e:
        print(f"❌ Failed to load replay: {e}")
        import traceback
        traceback.print_exc()
        raise


def main():
    """Test the patched loader."""
    import sys
    
    replay_path = sys.argv[1] if len(sys.argv) > 1 else "replays/4323395_Mike_SpeedlingBot_UltraloveAIE_v2.SC2Replay"
    
    print("=" * 80)
    print("TESTING PATCHED SC2READER")
    print("=" * 80)
    print()
    
    # Try different load levels
    for level in [4, 3, 2]:
        print(f"\n{'='*60}")
        print(f"LOAD LEVEL {level}")
        print(f"{'='*60}")
        try:
            replay = load_replay_safe(replay_path, load_level=level)
            
            # Show sample events if available
            if hasattr(replay, 'events') and len(replay.events) > 0:
                print(f"\n✅ SUCCESS! Found {len(replay.events)} events")
                print("\nFirst 10 events:")
                for i, event in enumerate(replay.events[:10]):
                    print(f"  {i+1}. {event.second:>3}s - {type(event).__name__}")
                break
            else:
                print(f"\n⚠️  Loaded but no events found")
        except Exception as e:
            print(f"\n❌ Failed: {e}")
            continue
    
    print("\n" + "=" * 80)
    print("✅ Test complete!")


if __name__ == "__main__":
    main()
