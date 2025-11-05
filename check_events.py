import json

data = json.load(open('output/replay_events.json'))
high = [e for e in data['events'] if e['priority'] == 'high']
medium = [e for e in data['events'] if e['priority'] == 'medium']

print(f"High priority: {len(high)}")
for e in high[:20]:
    name = e.get('unit_name') or e.get('upgrade_name') or 'Unknown'
    print(f"  {e['timestamp']:>4}s - {e['type']:15} - {name}")

print(f"\nMedium priority: {len(medium)}")
for e in medium[:20]:
    name = e.get('unit_name') or e.get('upgrade_name') or 'Unknown'
    print(f"  {e['timestamp']:>4}s - {e['type']:15} - {name}")
