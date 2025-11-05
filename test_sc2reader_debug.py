"""Debug sc2reader loading."""

import sc2reader
import traceback
import sys

replay_path = sys.argv[1] if len(sys.argv) > 1 else "replays/4323200_changeling_Mike_MagannathaAIE_v2.SC2Replay"

print("Testing sc2reader with full traceback...\n")

for level in [4, 3, 2, 1, 0]:
    print(f"\n{'='*60}")
    print(f"LOAD LEVEL {level}")
    print(f"{'='*60}")
    try:
        replay = sc2reader.load_replay(replay_path, load_level=level, load_map=False)
        print(f"✅ SUCCESS!")
        print(f"   Game length: {replay.game_length}")
        print(f"   Players: {len(replay.players)}")
        print(f"   Has events: {hasattr(replay, 'events')}")
        if hasattr(replay, 'events'):
            print(f"   Event count: {len(replay.events)}")
            if len(replay.events) > 0:
                print(f"   First event: {type(replay.events[0]).__name__}")
        print(f"   Has tracker_events: {hasattr(replay, 'tracker_events')}")
        if hasattr(replay, 'tracker_events'):
            print(f"   Tracker event count: {len(replay.tracker_events)}")
        break
    except Exception as e:
        print(f"❌ FAILED: {e}")
        print("\nFull traceback:")
        traceback.print_exc()
