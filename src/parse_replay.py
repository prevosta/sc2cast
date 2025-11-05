#!/usr/bin/env python3
"""
SC2Cast Replay Parser
Sprint 1.2: Basic metadata extraction from SC2 replay files
"""

import json
import sys
from pathlib import Path
import sc2reader


# Monkey-patch sc2reader to handle AI Arena replays with empty cache_handles
def patched_load_details(self):
    """Patched version that handles empty cache_handles."""
    if "replay.details" in self.raw_data:
        details = self.raw_data["replay.details"]
    elif "replay.details.backup" in self.raw_data:
        details = self.raw_data["replay.details.backup"]
    else:
        return

    self.map_name = details["map_name"]
    
    # Original crashes here with AI Arena replays: details["cache_handles"][0].server.lower()
    if details.get("cache_handles") and len(details["cache_handles"]) > 0:
        self.region = details["cache_handles"][0].server.lower()
        self.map_hash = details["cache_handles"][-1].hash
        self.map_file = details["cache_handles"][-1]
    else:
        # Fallback for AI Arena replays with empty cache_handles
        self.region = "unknown"
        self.map_hash = None
        self.map_file = None
    
    # Rest of the original logic (expansion detection, timestamps, etc.)
    # Skipping for now - we only need basic info


# Apply the patch
from sc2reader.resources import Replay
Replay.load_details = patched_load_details


def parse_replay(replay_path: Path) -> dict:
    """Parse SC2 replay and extract basic metadata."""
    
    # Load replay (with patched load_details to handle empty cache_handles)
    # Try load_level=4 (includes full game data), fallback to level 3 if events fail
    try:
        replay = sc2reader.load_replay(str(replay_path), load_level=4)
    except Exception:
        # Fallback: load_level=3 skips game events but has initData with player info
        replay = sc2reader.load_replay(str(replay_path), load_level=3)
    
    # Extract duration
    duration_seconds = int(replay.game_length.total_seconds())
    duration_minutes = duration_seconds // 60
    duration_secs_remainder = duration_seconds % 60
    
    # Extract player info
    players = []
    
    # At load_level=3, player data is in raw_data initData
    if 'replay.initData' in replay.raw_data:
        init_data = replay.raw_data['replay.initData']
        
        # Extract player info from user_initial_data
        if isinstance(init_data, dict) and 'user_initial_data' in init_data:
            for user_data in init_data['user_initial_data']:
                # Skip empty slots (lobby slots with no players)
                if not user_data or not user_data.get('name'):
                    continue
                
                # Get race (race_preference may be None for AI Arena bots)
                race_map = {0: "Random", 1: "Terran", 2: "Zerg", 3: "Protoss"}
                race_pref = user_data.get('race_preference')
                race = race_map.get(race_pref, "Unknown") if race_pref is not None else "Unknown"
                    
                players.append({
                    "name": user_data['name'],
                    "race": race,
                    "result": "Unknown"  # Result requires game events (load_level=4+)
                })
    
    # Build metadata dict
    metadata = {
        "filename": replay_path.name,
        "map": replay.map_name if hasattr(replay, 'map_name') and replay.map_name else "Unknown",
        "duration_seconds": duration_seconds,
        "duration_human": f"{duration_minutes}:{duration_secs_remainder:02d}",
        "players": players
    }
    
    return metadata


def main():
    """Main entry point."""
    
    # Find replay file in demo folder
    replay_dir = Path("/workspace/replays/demo")
    
    # Check if directory exists
    if not replay_dir.exists():
        print(f"ERROR: Replay directory not found: {replay_dir}", file=sys.stderr)
        print("Make sure /workspace/replays/demo is mounted in Docker", file=sys.stderr)
        sys.exit(1)
    
    # Find replay files
    replay_files = list(replay_dir.glob("*.SC2Replay"))
    
    if not replay_files:
        print(f"ERROR: No .SC2Replay files found in {replay_dir}", file=sys.stderr)
        print("Add replay files to the replays/demo/ folder", file=sys.stderr)
        sys.exit(1)
    
    # Use first replay found
    replay_path = replay_files[0]
    
    # Check file is readable
    if not replay_path.is_file():
        print(f"ERROR: Not a valid file: {replay_path}", file=sys.stderr)
        sys.exit(1)
    
    # Check file size (corrupted replays are usually very small)
    file_size = replay_path.stat().st_size
    if file_size < 1024:  # Less than 1KB is suspicious
        print(f"ERROR: Replay file too small ({file_size} bytes), possibly corrupted", file=sys.stderr)
        sys.exit(1)
    
    try:
        metadata = parse_replay(replay_path)
        
        # Validate we got some data
        if not metadata.get('players'):
            print("WARNING: No players found in replay", file=sys.stderr)
        
        print(json.dumps(metadata, indent=2))
        sys.exit(0)
        
    except FileNotFoundError as e:
        print(f"ERROR: Replay file not found: {e}", file=sys.stderr)
        sys.exit(1)
    except PermissionError as e:
        print(f"ERROR: Permission denied reading replay: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Failed to parse replay '{replay_path.name}': {e}", file=sys.stderr)
        print("This replay may be corrupted or from an unsupported SC2 version", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
