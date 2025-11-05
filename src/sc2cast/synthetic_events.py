"""
Synthetic Event Generator - Create realistic game events for testing.

Since the demo replay has sc2reader compatibility issues, this generates
synthetic events that simulate a real game for testing the camera system.
"""

import random
from pathlib import Path
from typing import List
from dataclasses import dataclass, asdict
from enum import Enum
import json


class EventType(Enum):
    """Types of game events."""
    EXPANSION = "expansion"
    TECH_BUILDING = "tech_building"
    ARMY_PRODUCTION = "army_production"
    BATTLE = "battle"
    UNIT_DEATH = "unit_death"
    UPGRADE = "upgrade"
    BASE_ATTACK = "base_attack"


@dataclass
class SyntheticEvent:
    """A synthetic game event for testing."""
    time_seconds: int
    event_type: str
    player_id: int
    description: str
    priority: str  # "high", "medium", "low"
    location: tuple = None
    value: int = 0
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'timestamp': self.time_seconds,
            'type': self.event_type,
            'player': self.player_id,
            'description': self.description,
            'priority': self.priority,
            'location': self.location,
            'value': self.value
        }


class SyntheticEventGenerator:
    """Generate realistic synthetic game events."""
    
    def __init__(self, game_duration_seconds: int = 310):
        """Initialize generator with game duration."""
        self.duration = game_duration_seconds
        self.events: List[SyntheticEvent] = []
    
    def generate_standard_game(self) -> List[SyntheticEvent]:
        """Generate events for a standard game progression."""
        print(f"🎮 Generating synthetic events for {self.duration}s game...")
        
        self.events = []
        
        # Early game (0-120s): Expansions, tech buildings
        self._generate_early_game()
        
        # Mid game (120-240s): Army production, small skirmishes
        self._generate_mid_game()
        
        # Late game (240+s): Major battles, base attacks
        self._generate_late_game()
        
        # Sort by time
        self.events.sort(key=lambda e: e.time_seconds)
        
        print(f"✅ Generated {len(self.events)} events")
        return self.events
    
    def _generate_early_game(self):
        """Generate early game events (0-120s)."""
        # Both players take natural expansion
        for player in [1, 2]:
            expand_time = random.randint(40, 60)
            self.events.append(SyntheticEvent(
                time_seconds=expand_time,
                event_type=EventType.EXPANSION.value,
                player_id=player,
                description=f"Player {player} expands to natural",
                priority="high",
                location=(random.randint(20, 80), random.randint(20, 80)),
                value=100
            ))
        
        # Tech buildings
        tech_buildings = [
            ("Gateway", 50, 75),
            ("Barracks", 45, 70),
            ("Spawning Pool", 40, 60),
        ]
        
        for player in [1, 2]:
            for building, min_time, max_time in tech_buildings[:2]:
                tech_time = random.randint(min_time, max_time)
                self.events.append(SyntheticEvent(
                    time_seconds=tech_time,
                    event_type=EventType.TECH_BUILDING.value,
                    player_id=player,
                    description=f"Player {player} builds {building}",
                    priority="medium",
                    location=(random.randint(20, 80), random.randint(20, 80)),
                    value=50
                ))
    
    def _generate_mid_game(self):
        """Generate mid game events (120-240s)."""
        # More expansions
        for player in [1, 2]:
            third_base_time = random.randint(140, 180)
            self.events.append(SyntheticEvent(
                time_seconds=third_base_time,
                event_type=EventType.EXPANSION.value,
                player_id=player,
                description=f"Player {player} takes third base",
                priority="high",
                location=(random.randint(20, 80), random.randint(20, 80)),
                value=100
            ))
        
        # Small skirmishes (3-5 during mid game)
        num_skirmishes = random.randint(3, 5)
        for i in range(num_skirmishes):
            battle_time = random.randint(130, 230)
            attacker = random.choice([1, 2])
            self.events.append(SyntheticEvent(
                time_seconds=battle_time,
                event_type=EventType.BATTLE.value,
                player_id=attacker,
                description=f"Small battle - Player {attacker} attacks",
                priority="medium",
                location=(random.randint(30, 70), random.randint(30, 70)),
                value=60
            ))
        
        # Army production
        for player in [1, 2]:
            for i in range(3):
                prod_time = random.randint(150, 220)
                self.events.append(SyntheticEvent(
                    time_seconds=prod_time,
                    event_type=EventType.ARMY_PRODUCTION.value,
                    player_id=player,
                    description=f"Player {player} mass production",
                    priority="low",
                    location=(random.randint(20, 80), random.randint(20, 80)),
                    value=20
                ))
    
    def _generate_late_game(self):
        """Generate late game events (240+s)."""
        if self.duration < 240:
            return
        
        # Major battles
        num_big_battles = random.randint(2, 4)
        for i in range(num_big_battles):
            battle_time = random.randint(240, min(self.duration - 20, 300))
            attacker = random.choice([1, 2])
            self.events.append(SyntheticEvent(
                time_seconds=battle_time,
                event_type=EventType.BATTLE.value,
                player_id=attacker,
                description=f"MAJOR BATTLE - Player {attacker} engages",
                priority="high",
                location=(random.randint(30, 70), random.randint(30, 70)),
                value=150
            ))
        
        # Base attacks
        num_base_attacks = random.randint(1, 2)
        for i in range(num_base_attacks):
            attack_time = random.randint(260, min(self.duration - 10, 300))
            attacker = random.choice([1, 2])
            defender = 2 if attacker == 1 else 1
            self.events.append(SyntheticEvent(
                time_seconds=attack_time,
                event_type=EventType.BASE_ATTACK.value,
                player_id=attacker,
                description=f"Player {attacker} attacks Player {defender}'s base!",
                priority="high",
                location=(random.randint(10, 90), random.randint(10, 90)),
                value=200
            ))
    
    def save_to_json(self, output_path: Path):
        """Save events to JSON file."""
        output_data = {
            'source': 'synthetic',
            'game_duration_seconds': self.duration,
            'total_events': len(self.events),
            'events': [e.to_dict() for e in self.events]
        }
        
        output_path.parent.mkdir(exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"💾 Saved events to: {output_path}")
    
    def get_summary(self):
        """Get event summary."""
        by_type = {}
        by_priority = {}
        
        for event in self.events:
            # Count by type
            by_type[event.event_type] = by_type.get(event.event_type, 0) + 1
            
            # Count by priority
            by_priority[event.priority] = by_priority.get(event.priority, 0) + 1
        
        return {
            'total': len(self.events),
            'by_type': by_type,
            'by_priority': by_priority
        }


def main():
    """Generate synthetic events for testing."""
    print("=" * 80)
    print("SYNTHETIC EVENT GENERATOR")
    print("=" * 80)
    print("\n⚠️  Note: Using synthetic events because demo replay has sc2reader")
    print("   compatibility issues (empty cache_handles in replay details).\n")
    
    # Generate events matching our 5:10 demo replay
    generator = SyntheticEventGenerator(game_duration_seconds=310)
    events = generator.generate_standard_game()
    
    # Show summary
    print("\n" + "=" * 80)
    print("EVENT SUMMARY")
    print("=" * 80)
    
    summary = generator.get_summary()
    print(f"\nTotal Events: {summary['total']}")
    
    print("\nBy Type:")
    for event_type, count in summary['by_type'].items():
        print(f"  {event_type}: {count}")
    
    print("\nBy Priority:")
    for priority, count in summary['by_priority'].items():
        print(f"  {priority}: {count}")
    
    # Show timeline
    print("\nTimeline:")
    for minute in range(6):
        min_time = minute * 60
        max_time = (minute + 1) * 60
        minute_events = [e for e in events if min_time <= e.time_seconds < max_time]
        if minute_events:
            high_priority = sum(1 for e in minute_events if e.priority == "high")
            print(f"  {minute}:00-{minute}:59 → {len(minute_events)} events ({high_priority} high-priority)")
    
    # Show high-priority events
    print("\n" + "=" * 80)
    print("HIGH-PRIORITY EVENTS")
    print("=" * 80)
    high_priority = [e for e in events if e.priority == "high"]
    for event in high_priority:
        mins = event.time_seconds // 60
        secs = event.time_seconds % 60
        print(f"  {mins:02d}:{secs:02d} - {event.description}")
    
    # Save to JSON
    output_path = Path("output/synthetic_events.json")
    generator.save_to_json(output_path)
    
    print("\n✅ Synthetic event generation complete!")
    print("\n💡 Next step: Build event prioritizer and script generator")


if __name__ == "__main__":
    main()
