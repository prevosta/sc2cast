"""Extract game events from SC2 replay files."""

import json
from pathlib import Path
import sc2reader


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
        try:
            # Load with full event tracking
            self.replay = sc2reader.load_replay(
                self.replay_path,
                load_level=4,
                load_map=False
            )
            print(f"✅ Replay loaded: {self.replay.game_length}")
        except (IndexError, AttributeError, KeyError) as e:
            print(f"⚠️  Full load failed ({e}), trying minimal load...")
            self.replay = sc2reader.load_replay(
                self.replay_path,
                load_level=0,
                load_map=False
            )
            print(f"✅ Replay loaded (minimal): {self.replay.game_length}")
    
    def extract_events(self):
        """Extract all game events from replay."""
        if not self.replay:
            raise ValueError("Replay not loaded. Call load_replay() first.")
        
        print(f"🔍 Extracting events from {len(self.replay.events)} replay events...")
        
        for event in self.replay.events:
            event_data = self._process_event(event)
            if event_data:
                self.events.append(event_data)
        
        print(f"✅ Extracted {len(self.events)} relevant events")
    
    def _process_event(self, event):
        """Process individual event and extract relevant data."""
        event_type = type(event).__name__
        
        # Track unit births (buildings, units trained)
        if event_type == "UnitBornEvent":
            return {
                "timestamp": event.second,
                "type": "unit_born",
                "unit_name": getattr(event, 'unit_type_name', 'Unknown'),
                "player": getattr(event, 'control_pid', 0),
                "priority": self._calculate_priority("unit_born", event)
            }
        
        # Track unit deaths (battles, losses)
        elif event_type == "UnitDiedEvent":
            return {
                "timestamp": event.second,
                "type": "unit_died",
                "unit_name": getattr(event, 'unit_type_name', 'Unknown'),
                "player": getattr(event, 'killer_pid', 0),
                "priority": self._calculate_priority("unit_died", event)
            }
        
        # Track upgrades
        elif event_type == "UpgradeCompleteEvent":
            return {
                "timestamp": event.second,
                "type": "upgrade_complete",
                "upgrade_name": getattr(event, 'upgrade_type_name', 'Unknown'),
                "player": getattr(event, 'pid', 0),
                "priority": "medium"
            }
        
        return None
    
    def _calculate_priority(self, event_type, event):
        """Calculate event priority for camera direction."""
        if event_type == "unit_born":
            unit = getattr(event, 'unit_type_name', '').lower()
            # High priority for expansions and tech buildings
            if 'hatchery' in unit or 'nexus' in unit or 'command' in unit:
                return "high"
            if 'spire' in unit or 'fleet' in unit or 'stargate' in unit:
                return "high"
            # Medium for production buildings
            if 'gateway' in unit or 'barracks' in unit or 'factory' in unit:
                return "medium"
            return "low"
        
        elif event_type == "unit_died":
            unit = getattr(event, 'unit_type_name', '').lower()
            # High priority for building/expensive unit deaths
            if 'hatchery' in unit or 'nexus' in unit or 'command' in unit:
                return "high"
            if 'carrier' in unit or 'battlecruiser' in unit or 'mothership' in unit:
                return "high"
            # Medium for army units
            if any(x in unit for x in ['stalker', 'marine', 'zergling', 'roach']):
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
    replay_path = Path("replays/4323200_changeling_Mike_MagannathaAIE_v2.SC2Replay")
    
    if not replay_path.exists():
        print(f"❌ Replay file not found: {replay_path}")
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
