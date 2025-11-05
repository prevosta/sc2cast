import json

data = json.load(open('output/prioritized_events.json'))

print("=" * 80)
print("BATTLE DETAILS")
print("=" * 80)

for battle in data['battles']:
    mins = battle['start_time'] // 60
    secs = battle['start_time'] % 60
    end_mins = battle['end_time'] // 60
    end_secs = battle['end_time'] % 60
    
    print(f"\n⚔️  Battle #{data['battles'].index(battle) + 1}")
    print(f"   Time: {mins:02d}:{secs:02d} - {end_mins:02d}:{end_secs:02d} ({battle['duration']}s)")
    print(f"   Location: ({battle['location']['x']}, {battle['location']['y']})")
    print(f"   Deaths: {battle['death_count']}")
    print(f"   Army Value Lost: {battle['army_value_lost']}")
    print(f"   Priority: {battle['priority']}")
    print(f"   Peak Time: {battle['peak_time']//60:02d}:{battle['peak_time']%60:02d}")

print("\n" + "=" * 80)
print("CAMERA-READY EVENTS")
print("=" * 80)

for event in data['events']:
    mins = event['time_seconds'] // 60
    secs = event['time_seconds'] % 60
    loc = event.get('location')
    loc_str = f"@ ({loc['x']:>3}, {loc['y']:>3})" if loc else ""
    print(f"  {mins:02d}:{secs:02d} ({event['duration']:>2}s) - {event['priority']:6} - {event['description']:50} {loc_str}")
