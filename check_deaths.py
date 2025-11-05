import json

data = json.load(open('output/replay_events.json'))
deaths = [e for e in data['events'] if e['type'] == 'unit_died']

print(f"Unit deaths: {len(deaths)}")
print("\nFirst 30 unit deaths:")
for e in deaths[:30]:
    name = e.get('unit_name', 'Unknown')
    print(f"  {e['timestamp']:>4}s - P{e['player']} - {name}")

# Group by minute
print("\nDeaths by minute:")
for minute in range(7):
    min_deaths = [e for e in deaths if minute * 60 <= e['timestamp'] < (minute + 1) * 60]
    if min_deaths:
        print(f"  {minute}:00-{minute}:59 → {len(min_deaths)} deaths")
