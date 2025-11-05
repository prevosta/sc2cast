"""Parse StarCraft II replay files and extract metadata."""

import json
from pathlib import Path
import sc2reader


def parse_replay(replay_path):
    """
    Parse a SC2 replay file and extract metadata.
    
    Args:
        replay_path: Path to the .SC2Replay file
        
    Returns:
        dict: Replay metadata including players, map, duration, etc.
    """
    # Load replay - try different load levels if first fails
    try:
        replay = sc2reader.load_replay(str(replay_path), load_level=2)
    except (IndexError, AttributeError, KeyError) as e:
        print(f"⚠️  Warning: Could not fully load replay ({e})")
        print(f"⚠️  Trying minimal load...")
        replay = sc2reader.load_replay(str(replay_path), load_level=0)
    
    # Extract player information
    players = []
    for player in replay.players:
        players.append({
            "name": player.name,
            "race": getattr(player, 'play_race', 'Unknown'),
            "result": getattr(player, 'result', 'Unknown'),
            "is_human": getattr(player, 'is_human', True),
        })
    
    # Build metadata dictionary
    metadata = {
        "file": str(replay_path),
        "map_name": getattr(replay, 'map_name', 'Unknown'),
        "game_length_seconds": replay.game_length.seconds if hasattr(replay, 'game_length') and replay.game_length else 0,
        "game_length_formatted": str(replay.game_length) if hasattr(replay, 'game_length') and replay.game_length else "Unknown",
        "date": replay.date.isoformat() if hasattr(replay, 'date') and replay.date else None,
        "game_version": getattr(replay, 'release_string', 'Unknown'),
        "game_speed": getattr(replay, 'speed', 'Unknown'),
        "players": players,
    }
    
    return metadata


def main():
    """Parse the demo replay and output metadata to JSON."""
    # Path to demo replay
    replay_path = Path("replays/4323200_changeling_Mike_MagannathaAIE_v2.SC2Replay")
    
    if not replay_path.exists():
        print(f"❌ Replay file not found: {replay_path}")
        return
    
    print(f"📂 Loading replay: {replay_path}")
    
    # Parse replay
    metadata = parse_replay(replay_path)
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Save to JSON
    output_path = output_dir / "replay_metadata.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✅ Metadata extracted successfully!")
    print(f"📄 Output saved to: {output_path}")
    print("\n📊 Summary:")
    print(f"  Map: {metadata['map_name']}")
    print(f"  Duration: {metadata['game_length_formatted']}")
    print(f"  Players: {len(metadata['players'])}")
    for player in metadata['players']:
        print(f"    - {player['name']} ({player['race']}) - {player['result']}")


if __name__ == "__main__":
    main()
