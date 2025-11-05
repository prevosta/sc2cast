import json

data = json.load(open('output/replay_events.json'))

# Get high-priority events (battles, expansions)
high = [e for e in data['events'] if e['priority'] == 'high']
medium = [e for e in data['events'] if e['priority'] == 'medium']

print("=" * 80)
print("HIGH-PRIORITY EVENTS (Expansions, Major Units)")
print("=" * 80)
for e in high:
    name = e.get('unit_name', e.get('upgrade_name', 'Unknown'))
    mins = e['timestamp'] // 60
    secs = e['timestamp'] % 60
    print(f"  {mins:02d}:{secs:02d} - {e['type']:15} - P{e['player']} - {name}")

print("\n" + "=" * 80)
print("MEDIUM-PRIORITY EVENTS (Army Units, Production)")
print("=" * 80)
print(f"Total: {len(medium)}")

# Group by minute for battles
print("\nArmy deaths by minute:")
for minute in range(7):
    min_events = [e for e in medium if minute * 60 <= e['timestamp'] < (minute + 1) * 60 and e['type'] == 'unit_died']
    if min_events:
        # Show unit types
        units = {}
        for e in min_events:
            unit = e.get('unit_name', 'Unknown')
            units[unit] = units.get(unit, 0) + 1
        unit_str = ", ".join([f"{count} {unit}" for unit, count in sorted(units.items(), key=lambda x: -x[1])[:3]])
        print(f"  {minute}:00-{minute}:59 → {len(min_events)} army deaths ({unit_str})")

# Show some key battles
print("\nSample battle events (minutes 4-6):")
battle_events = [e for e in medium if 240 <= e['timestamp'] < 378 and e['type'] == 'unit_died']
for e in battle_events[:15]:
    name = e.get('unit_name', 'Unknown')
    mins = e['timestamp'] // 60
    secs = e['timestamp'] % 60
    print(f"  {mins:02d}:{secs:02d} - P{e['player']} - {name}")
