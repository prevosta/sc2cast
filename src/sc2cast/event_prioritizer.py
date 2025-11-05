"""
Event Prioritizer - Cluster and score game events for camera decisions.

Takes raw events from event_extractor and:
1. Clusters nearby deaths into battle events
2. Scores events by importance (army value, timing)
3. Filters noise (larvae, mineral fields, etc.)
4. Produces timeline of camera-worthy moments
"""

import json
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from collections import defaultdict


@dataclass
class BattleEvent:
    """A clustered battle event."""
    start_time: int           # When battle started (seconds)
    end_time: int             # When battle ended (seconds)
    location: Dict[str, int]  # Center location {"x": 100, "y": 120}
    deaths: List[Dict]        # List of death events in this battle
    army_value_lost: int      # Total army value lost
    priority: str             # "high", "medium", "low"
    
    @property
    def duration(self):
        """Battle duration in seconds."""
        return self.end_time - self.start_time
    
    @property
    def peak_time(self):
        """Time of peak activity (most deaths)."""
        # Use middle of battle as peak
        return (self.start_time + self.end_time) // 2
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration': self.duration,
            'peak_time': self.peak_time,
            'location': self.location,
            'death_count': len(self.deaths),
            'army_value_lost': self.army_value_lost,
            'priority': self.priority,
            'deaths': self.deaths
        }


@dataclass
class PrioritizedEvent:
    """A prioritized game event ready for camera script."""
    time_seconds: int
    event_type: str      # "battle", "expansion", "tech"
    description: str
    location: Dict[str, int] | None
    priority: str        # "high", "medium", "low"
    score: int          # Numeric score for sorting
    duration: int = 5   # How long to show this (seconds)
    
    def to_dict(self):
        """Convert to dictionary."""
        return asdict(self)


class EventPrioritizer:
    """Prioritize and cluster game events for intelligent camera control."""
    
    # Army unit values (rough supply/importance)
    UNIT_VALUES = {
        # Terran
        'marine': 1, 'marauder': 2, 'reaper': 1, 'hellion': 2, 'hellbat': 2,
        'siegetank': 3, 'thor': 6, 'viking': 2, 'medivac': 2, 'liberator': 3,
        'banshee': 3, 'raven': 2, 'battlecruiser': 6, 'ghost': 2,
        
        # Protoss
        'zealot': 2, 'stalker': 2, 'sentry': 2, 'adept': 2, 'hightemplar': 2,
        'darktemplar': 2, 'archon': 4, 'immortal': 4, 'colossus': 6, 'disruptor': 3,
        'phoenix': 2, 'voidray': 4, 'oracle': 3, 'tempest': 5, 'carrier': 6,
        'mothership': 8, 'observer': 1, 'warpprism': 2,
        
        # Zerg
        'zergling': 0.5, 'baneling': 0.5, 'roach': 2, 'ravager': 3, 'hydralisk': 2,
        'lurker': 3, 'infestor': 2, 'swarmhost': 3, 'ultralisk': 6, 'mutalisk': 2,
        'corruptor': 2, 'viper': 3, 'broodlord': 4, 'queen': 2, 'overlord': 0,
        
        # Workers
        'scv': 0, 'probe': 0, 'drone': 0,
        
        # Noise
        'larva': 0, 'egg': 0, 'mineralfield': 0, 'mineralfield750': 0,
        'labmineralfield': 0, 'labmineralfield750': 0,
    }
    
    # Building values for expansion/tech tracking
    BUILDING_VALUES = {
        'commandcenter': 100, 'orbitalcommand': 100, 'planetaryfortress': 100,
        'nexus': 100, 'hatchery': 100, 'lair': 100, 'hive': 100,
        'barracks': 50, 'factory': 50, 'starport': 50,
        'gateway': 50, 'roboticsfacility': 50, 'stargate': 50,
        'spawningpool': 50, 'roachwarren': 50, 'hydraliskden': 50,
        'spire': 75, 'greaterspire': 75, 'fleetbeacon': 75, 'templararchive': 75,
    }
    
    def __init__(self):
        """Initialize prioritizer."""
        self.battles: List[BattleEvent] = []
        self.expansions: List[PrioritizedEvent] = []
        self.tech_events: List[PrioritizedEvent] = []
        self.all_priority_events: List[PrioritizedEvent] = []
    
    def process_events(self, events: List[Dict]) -> List[PrioritizedEvent]:
        """
        Process raw events and return prioritized timeline.
        
        Args:
            events: List of raw events from event_extractor
            
        Returns:
            List of prioritized events sorted by time
        """
        print(f"📊 Processing {len(events)} raw events...")
        
        # Separate events by type
        deaths = [e for e in events if e['type'] == 'unit_died']
        births = [e for e in events if e['type'] == 'unit_born']
        upgrades = [e for e in events if e['type'] == 'upgrade_complete']
        
        print(f"   Deaths: {len(deaths)}, Births: {len(births)}, Upgrades: {len(upgrades)}")
        
        # Cluster deaths into battles
        self._cluster_battles(deaths)
        print(f"   Found {len(self.battles)} battle clusters")
        
        # Process expansions
        self._process_expansions(births)
        print(f"   Found {len(self.expansions)} expansion events")
        
        # Process tech buildings
        self._process_tech(births)
        print(f"   Found {len(self.tech_events)} tech events")
        
        # Combine and prioritize all events
        self._combine_events()
        
        print(f"✅ Generated {len(self.all_priority_events)} prioritized events")
        return self.all_priority_events
    
    def _cluster_battles(self, deaths: List[Dict]):
        """Cluster death events into battles by time and location."""
        # Filter out noise (workers, larvae, minerals)
        army_deaths = []
        for death in deaths:
            unit_name = death.get('unit_name', '').lower()
            if unit_name in self.UNIT_VALUES and self.UNIT_VALUES[unit_name] > 0:
                if death.get('location'):  # Must have location
                    army_deaths.append(death)
        
        print(f"   Army deaths (with locations): {len(army_deaths)}")
        
        if not army_deaths:
            return
        
        # Sort by time
        army_deaths.sort(key=lambda e: e['timestamp'])
        
        # Cluster using time and space windows
        TIME_WINDOW = 30  # Deaths within 30 seconds
        SPACE_WINDOW = 20  # Deaths within 20 map units
        
        current_cluster = []
        
        for death in army_deaths:
            if not current_cluster:
                current_cluster.append(death)
                continue
            
            # Check if death belongs to current cluster
            last_death = current_cluster[-1]
            time_diff = death['timestamp'] - last_death['timestamp']
            
            if time_diff <= TIME_WINDOW:
                # Check spatial proximity
                loc1 = death['location']
                loc2 = last_death['location']
                distance = ((loc1['x'] - loc2['x'])**2 + (loc1['y'] - loc2['y'])**2)**0.5
                
                if distance <= SPACE_WINDOW:
                    # Add to current cluster
                    current_cluster.append(death)
                else:
                    # Too far away, save current cluster and start new one
                    self._save_battle_cluster(current_cluster)
                    current_cluster = [death]
            else:
                # Too much time passed, save cluster and start new one
                self._save_battle_cluster(current_cluster)
                current_cluster = [death]
        
        # Save last cluster
        if current_cluster:
            self._save_battle_cluster(current_cluster)
    
    def _save_battle_cluster(self, cluster: List[Dict]):
        """Save a battle cluster if it's significant enough."""
        MIN_DEATHS = 3  # Need at least 3 deaths to be a battle
        
        if len(cluster) < MIN_DEATHS:
            return
        
        # Calculate center location
        avg_x = sum(d['location']['x'] for d in cluster) / len(cluster)
        avg_y = sum(d['location']['y'] for d in cluster) / len(cluster)
        
        # Calculate army value lost
        total_value = 0
        for death in cluster:
            unit_name = death.get('unit_name', '').lower()
            value = self.UNIT_VALUES.get(unit_name, 1)
            total_value += value
        
        # Determine priority based on value and death count
        if total_value >= 20 or len(cluster) >= 15:
            priority = "high"
        elif total_value >= 10 or len(cluster) >= 8:
            priority = "medium"
        else:
            priority = "low"
        
        battle = BattleEvent(
            start_time=cluster[0]['timestamp'],
            end_time=cluster[-1]['timestamp'],
            location={'x': int(avg_x), 'y': int(avg_y)},
            deaths=cluster,
            army_value_lost=int(total_value),
            priority=priority
        )
        
        self.battles.append(battle)
    
    def _process_expansions(self, births: List[Dict]):
        """Extract expansion events."""
        expansion_buildings = ['commandcenter', 'orbitalcommand', 'nexus', 'hatchery', 'lair', 'hive']
        
        for birth in births:
            unit_name = birth.get('unit_name', '').lower()
            if any(exp in unit_name for exp in expansion_buildings):
                # Skip starting bases (time 0)
                if birth['timestamp'] < 10:
                    continue
                
                score = 100  # Expansions are always important
                
                self.expansions.append(PrioritizedEvent(
                    time_seconds=birth['timestamp'],
                    event_type='expansion',
                    description=f"P{birth['player']} expands - {birth['unit_name']}",
                    location=birth.get('location'),
                    priority='high',
                    score=score,
                    duration=8  # Show expansions longer
                ))
    
    def _process_tech(self, births: List[Dict]):
        """Extract tech building events."""
        tech_buildings = ['spire', 'greaterspire', 'fleetbeacon', 'templararchive', 
                         'stargate', 'roboticsfacility', 'factory', 'starport', 'fusioncore']
        
        for birth in births:
            unit_name = birth.get('unit_name', '').lower()
            if any(tech in unit_name for tech in tech_buildings):
                score = 60  # Tech is moderately important
                
                self.tech_events.append(PrioritizedEvent(
                    time_seconds=birth['timestamp'],
                    event_type='tech',
                    description=f"P{birth['player']} builds {birth['unit_name']}",
                    location=birth.get('location'),
                    priority='medium',
                    score=score,
                    duration=5
                ))
    
    def _combine_events(self):
        """Combine all event types into single prioritized timeline."""
        # Add battles
        for battle in self.battles:
            score = battle.army_value_lost * 2  # Weight by value lost
            if battle.priority == 'high':
                score += 50
            elif battle.priority == 'medium':
                score += 25
            
            self.all_priority_events.append(PrioritizedEvent(
                time_seconds=battle.peak_time,
                event_type='battle',
                description=f"Battle: {len(battle.deaths)} deaths, {battle.army_value_lost} value lost",
                location=battle.location,
                priority=battle.priority,
                score=score,
                duration=min(10, battle.duration + 3)  # Show battle duration + buffer
            ))
        
        # Add expansions
        self.all_priority_events.extend(self.expansions)
        
        # Add tech (only medium/high priority)
        self.all_priority_events.extend([t for t in self.tech_events if t.priority in ['high', 'medium']])
        
        # Sort by time
        self.all_priority_events.sort(key=lambda e: e.time_seconds)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of prioritized events."""
        return {
            'total_events': len(self.all_priority_events),
            'battles': len(self.battles),
            'expansions': len(self.expansions),
            'tech': len(self.tech_events),
            'by_priority': {
                'high': len([e for e in self.all_priority_events if e.priority == 'high']),
                'medium': len([e for e in self.all_priority_events if e.priority == 'medium']),
                'low': len([e for e in self.all_priority_events if e.priority == 'low']),
            },
            'timeline': self._get_timeline()
        }
    
    def _get_timeline(self) -> List[Dict]:
        """Get timeline breakdown by minute."""
        timeline = []
        max_time = max(e.time_seconds for e in self.all_priority_events) if self.all_priority_events else 0
        
        for minute in range((max_time // 60) + 1):
            time_range = (minute * 60, (minute + 1) * 60)
            events_in_range = [e for e in self.all_priority_events 
                             if time_range[0] <= e.time_seconds < time_range[1]]
            if events_in_range:
                timeline.append({
                    'time': f"{minute}:00-{minute}:59",
                    'count': len(events_in_range),
                    'high_priority': len([e for e in events_in_range if e.priority == 'high']),
                    'battles': len([e for e in events_in_range if e.event_type == 'battle']),
                })
        
        return timeline
    
    def save_to_json(self, output_path: Path):
        """Save prioritized events to JSON."""
        output_data = {
            'summary': self.get_summary(),
            'events': [e.to_dict() for e in self.all_priority_events],
            'battles': [b.to_dict() for b in self.battles]
        }
        
        output_path.parent.mkdir(exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"💾 Saved prioritized events to: {output_path}")


def main():
    """Test event prioritization."""
    print("=" * 80)
    print("EVENT PRIORITIZER")
    print("=" * 80)
    
    # Load raw events
    events_path = Path("output/replay_events.json")
    if not events_path.exists():
        print(f"❌ No events file found: {events_path}")
        print("   Run event_extractor.py first!")
        return
    
    with open(events_path, 'r') as f:
        data = json.load(f)
        raw_events = data['events']
    
    print(f"\n📂 Loaded {len(raw_events)} raw events")
    
    # Prioritize events
    prioritizer = EventPrioritizer()
    priority_events = prioritizer.process_events(raw_events)
    
    # Show summary
    print("\n" + "=" * 80)
    print("PRIORITIZATION SUMMARY")
    print("=" * 80)
    
    summary = prioritizer.get_summary()
    print(f"\nTotal Priority Events: {summary['total_events']}")
    print(f"  Battles: {summary['battles']}")
    print(f"  Expansions: {summary['expansions']}")
    print(f"  Tech: {summary['tech']}")
    
    print("\nBy Priority:")
    for priority, count in summary['by_priority'].items():
        print(f"  {priority}: {count}")
    
    print("\nTimeline:")
    for time_slot in summary['timeline']:
        print(f"  {time_slot['time']}: {time_slot['count']} events ({time_slot['high_priority']} high, {time_slot['battles']} battles)")
    
    # Show high-priority events
    print("\n" + "=" * 80)
    print("HIGH-PRIORITY EVENTS")
    print("=" * 80)
    high_priority = [e for e in priority_events if e.priority == 'high']
    for event in high_priority:
        mins = event.time_seconds // 60
        secs = event.time_seconds % 60
        loc_str = f"@ ({event.location['x']}, {event.location['y']})" if event.location else ""
        print(f"  {mins:02d}:{secs:02d} - {event.event_type:10} - {event.description:40} {loc_str}")
    
    # Save to JSON
    output_path = Path("output/prioritized_events.json")
    prioritizer.save_to_json(output_path)
    
    print("\n✅ Event prioritization complete!")


if __name__ == "__main__":
    main()
