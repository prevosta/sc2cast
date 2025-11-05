"""Debug event attributes."""
import sys
sys.path.insert(0, 'src/sc2cast')

from replay_loader import load_replay_safe

replay = load_replay_safe("replays/4323395_Mike_SpeedlingBot_UltraloveAIE_v2.SC2Replay", load_level=3)

print(f"\nTotal events: {len(replay.events)}")
print("\nSample event types:")
event_types = {}
for event in replay.events[:200]:
    event_type = type(event).__name__
    if event_type not in event_types:
        event_types[event_type] = event
        print(f"\n{event_type}:")
        print(f"  Attributes: {[attr for attr in dir(event) if not attr.startswith('_')][:15]}")

# Check unit died events specifically
print("\n" + "=" * 60)
print("UNIT DIED EVENTS:")
died_events = [e for e in replay.events if type(e).__name__ == 'UnitDiedEvent']
print(f"Found {len(died_events)} unit died events")

if died_events:
    sample = died_events[100]  # Get one from mid-game
    print(f"\nSample (timestamp {sample.second}s):")
    attrs = [attr for attr in dir(sample) if not attr.startswith('_')]
    for attr in attrs[:20]:
        try:
            value = getattr(sample, attr)
            if not callable(value):
                print(f"  {attr}: {value}")
        except:
            pass
