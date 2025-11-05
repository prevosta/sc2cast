"""Extract game events from SC2 replay files."""

import json
from pathlib import Path

# Import our patched loader
try:
    from .replay_loader import load_replay_safe
except ImportError:
    from replay_loader import load_replay_safe


class EventExtractor:
    """Extract and categorize events from SC2 replays."""
    
    def __init__(self, replay_path):
        """Initialize with replay path."""
        self.replay_path = str(replay_path)
        self.replay = None
        self.events = []
    
    def load_replay(self):
        """Load replay file with sc2reader."""
        print(f"📂 Loading replay: {self.replay_path}")
        
        # Try load level 3 (has events but avoids unknown event types in level 4)
        try:
            self.replay = load_replay_safe(self.replay_path, load_level=3)
            return
        except Exception as e:
            print(f"   ⚠️  Load level 3 failed: {e}")
        
        # Fall back to load level 2
        try:
            print(f"  Trying load_level=2...")
            self.replay = load_replay_safe(self.replay_path, load_level=2)
            return
        except Exception as e:
            print(f"   ⚠️  Load level 2 failed: {e}")
        
        # Last resort: minimal load
        print(f"  ⚠️  Using minimal load (0)...")
        self.replay = load_replay_safe(self.replay_path, load_level=0)
        print(f"✅ Replay loaded (minimal): {self.replay.game_length}")
    
    def extract_events(self):
        """Extract all game events from replay."""
        if not self.replay:
            raise ValueError("Replay not loaded. Call load_replay() first.")
        
        # Build unit registry from UnitBornEvents
        unit_registry = {}  # Maps unit_id -> unit_type_name
        
        # First pass: register all units
        for event in self.replay.events:
            if type(event).__name__ == "UnitBornEvent":
                unit_id = getattr(event, 'unit_id', None)
                unit_type = getattr(event, 'unit_type_name', None)
                if unit_id and unit_type:
                    unit_registry[unit_id] = unit_type
        
        print(f"🔍 Built unit registry with {len(unit_registry)} units")
        print(f"🔍 Processing {len(self.replay.events)} events...")
        
        # Second pass: extract events with unit type names
        for event in self.replay.events:
            event_data = self._process_event(event, unit_registry)
            if event_data:
                self.events.append(event_data)
        
        print(f"✅ Extracted {len(self.events)} relevant events")
    
    def _process_event(self, event, unit_registry):
        """Process individual event and extract relevant data."""
        event_type = type(event).__name__
        
        # Extract location if available
        location = None
        if hasattr(event, 'location') and event.location:
            location = {"x": event.location[0], "y": event.location[1]}
        elif hasattr(event, 'x') and hasattr(event, 'y'):
            location = {"x": event.x, "y": event.y}
        
        # Track unit births (buildings, units trained)
        if event_type == "UnitBornEvent":
            unit_name = getattr(event, 'unit_type_name', 'Unknown')
            return {
                "timestamp": event.second,
                "type": "unit_born",
                "unit_name": unit_name,
                "player": getattr(event, 'control_pid', 0),
                "priority": self._calculate_priority("unit_born", event, unit_name),
                "location": location
            }
        
        # Track unit deaths (battles, losses) - use unit registry for names
        elif event_type == "UnitDiedEvent":
            unit_id = getattr(event, 'unit_id', None)
            unit_name = unit_registry.get(unit_id, 'Unknown')
            
            return {
                "timestamp": event.second,
                "type": "unit_died",
                "unit_name": unit_name,
                "player": getattr(event, 'killer_pid', 0),
                "priority": self._calculate_priority("unit_died", event, unit_name),
                "location": location
            }
        
        # Track upgrades (no location data typically)
        elif event_type == "UpgradeCompleteEvent":
            upgrade_name = getattr(event, 'upgrade_type_name', 'Unknown')
            return {
                "timestamp": event.second,
                "type": "upgrade_complete",
                "upgrade_name": upgrade_name,
                "player": getattr(event, 'pid', 0),
                "priority": self._calculate_priority("upgrade_complete", event, upgrade_name),
                "location": None  # Upgrades don't have location
            }
        
        return None
    
    def _calculate_priority(self, event_type, event, unit_or_upgrade_name):
        """Calculate event priority for camera direction."""
        name = unit_or_upgrade_name.lower()
        
        if event_type == "unit_born":
            # High priority for expansions and tech buildings
            if 'hatchery' in name or 'nexus' in name or 'command' in name or 'orbital' in name or 'lair' in name or 'hive' in name:
                return "high"
            if 'spire' in name or 'fleet' in name or 'stargate' in name or 'robo' in name:
                return "high"
            # Medium for production buildings
            if 'gateway' in name or 'barracks' in name or 'factory' in name or 'starport' in name:
                return "medium"
            # Low for everything else (workers, minerals, etc.)
            return "low"
        
        elif event_type == "unit_died":
            # High priority for building/expensive unit deaths
            if 'hatchery' in name or 'nexus' in name or 'command' in name or 'orbital' in name:
                return "high"
            if 'carrier' in name or 'battlecruiser' in name or 'mothership' in name:
                return "high"
            if 'colossus' in name or 'thor' in name or 'ultralisk' in name or 'broodlord' in name:
                return "high"
            # Medium for army units
            if any(x in name for x in ['stalker', 'marine', 'zergling', 'roach', 'hydralisk', 'baneling']):
                return "medium"
            # Low for workers, minerals, etc.
            return "low"
        
        elif event_type == "upgrade_complete":
            # Filter out spray decals
            if 'spray' in name:
                return "low"
            # High for critical upgrades
            if any(x in name for x in ['speed', 'attack', 'armor', 'range']):
                return "medium"
            return "low"
        
        return "low"
    
    def categorize_events(self):
        """Categorize events by priority."""
        high_priority = [e for e in self.events if e["priority"] == "high"]
        medium_priority = [e for e in self.events if e["priority"] == "medium"]
        low_priority = [e for e in self.events if e["priority"] == "low"]
        
        print(f"\n📊 Event Categories:")
        print(f"  High priority: {len(high_priority)}")
        print(f"  Medium priority: {len(medium_priority)}")
        print(f"  Low priority: {len(low_priority)}")
        
        return {
            "high": high_priority,
            "medium": medium_priority,
            "low": low_priority
        }
    
    def save_to_json(self, output_path):
        """Save events to JSON file."""
        output_data = {
            "replay_file": self.replay_path,
            "game_length": str(self.replay.game_length) if self.replay.game_length else "Unknown",
            "total_events": len(self.events),
            "events": self.events
        }
        
        output_path = Path(output_path)
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2)
        
        print(f"✅ Events saved to: {output_path}")


def main():
    """Extract events from demo replay."""
    # Test with the new replay
    replay_path = Path("replays/4323395_Mike_SpeedlingBot_UltraloveAIE_v2.SC2Replay")
    
    if not replay_path.exists():
        print(f"❌ Replay file not found: {replay_path}")
        # Fall back to old replay
        replay_path = Path("replays/4323200_changeling_Mike_MagannathaAIE_v2.SC2Replay")
        if not replay_path.exists():
            print(f"❌ No replays found!")
            return
    
    # Extract events
    extractor = EventExtractor(replay_path)
    extractor.load_replay()
    extractor.extract_events()
    
    # Categorize by priority
    categories = extractor.categorize_events()
    
    # Show sample high-priority events
    print(f"\n🎯 Sample High-Priority Events:")
    for event in categories["high"][:5]:
        print(f"  {event['timestamp']:>4}s - {event['type']:15} - {event['unit_name']}")
    
    # Save to JSON
    output_path = Path("output/replay_events.json")
    extractor.save_to_json(output_path)
    
    print(f"\n✅ Event extraction complete!")


if __name__ == "__main__":
    main()
