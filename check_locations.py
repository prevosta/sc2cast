import json

data = json.load(open('output/replay_events.json'))

# Check high-priority events with locations
high = [e for e in data['events'] if e['priority'] == 'high' and e.get('location')]

print("=" * 80)
print("HIGH-PRIORITY EVENTS WITH LOCATIONS")
print("=" * 80)
for e in high:
    name = e.get('unit_name', e.get('upgrade_name', 'Unknown'))
    loc = e.get('location')
    mins = e['timestamp'] // 60
    secs = e['timestamp'] % 60
    print(f"  {mins:02d}:{secs:02d} - {e['type']:15} - P{e['player']} - {name:20} @ ({loc['x']:>3}, {loc['y']:>3})")

# Check battle locations (medium priority deaths)
print("\n" + "=" * 80)
print("BATTLE LOCATIONS (Sample from minutes 4-6)")
print("=" * 80)
battles = [e for e in data['events'] 
           if e['type'] == 'unit_died' 
           and e['priority'] == 'medium' 
           and 240 <= e['timestamp'] < 378
           and e.get('location')]

print(f"Found {len(battles)} army deaths with locations")
print("\nFirst 15 battle events:")
for e in battles[:15]:
    name = e.get('unit_name', 'Unknown')
    loc = e.get('location')
    mins = e['timestamp'] // 60
    secs = e['timestamp'] % 60
    print(f"  {mins:02d}:{secs:02d} - P{e['player']} - {name:15} @ ({loc['x']:>3}, {loc['y']:>3})")

# Find battle clusters
print("\n" + "=" * 80)
print("BATTLE HOTSPOTS (clustered by location)")
print("=" * 80)

# Simple clustering by rounding to nearest 10
clusters = {}
for e in battles:
    if e.get('location'):
        loc = e['location']
        cluster_key = (round(loc['x'] / 10) * 10, round(loc['y'] / 10) * 10)
        if cluster_key not in clusters:
            clusters[cluster_key] = []
        clusters[cluster_key].append(e)

# Show top battle locations
top_clusters = sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True)[:5]
for (x, y), events in top_clusters:
    time_range = f"{min(e['timestamp'] for e in events)}s - {max(e['timestamp'] for e in events)}s"
    print(f"  Location ({x:>3}, {y:>3}): {len(events):>2} deaths, {time_range}")
