"""
Test if camera positions are recorded in replays or viewer-controlled.

MANUAL TEST:
1. Launch a replay
2. Move camera around during playback (arrow keys, minimap clicks)
3. Let it play for ~1 minute
4. Exit and re-watch the same replay
5. Does camera follow your previous movements?

Expected Result:
- If camera is DIFFERENT each viewing -> NOT RECORDED (our approach works!)
- If camera follows previous movements -> RECORDED (need different approach)
"""

import subprocess
from pathlib import Path


def main():
    """Launch replay for manual camera recording test."""
    replay_path = Path("replays/4323200_changeling_Mike_MagannathaAIE_v2.SC2Replay")
    
    if not replay_path.exists():
        print(f"❌ Replay not found: {replay_path}")
        return
    
    print("🎮 CAMERA RECORDING TEST")
    print("=" * 60)
    print()
    print("📋 INSTRUCTIONS:")
    print("1. Watch replay for 30 seconds without touching anything")
    print("2. Exit SC2")
    print("3. Run this script again")
    print("4. This time, actively move camera around (arrow keys, minimap)")
    print("5. Exit SC2 after 30 seconds")
    print("6. Run script a THIRD time")
    print("7. Watch - does camera follow your movements from step 4?")
    print()
    print("🔍 CRITICAL QUESTION:")
    print("   Does the camera position change between viewings?")
    print()
    print("   ✅ Different each time = NOT RECORDED (our approach works!)")
    print("   ⚠️  Same as previous = RECORDED (need different strategy)")
    print()
    print("=" * 60)
    print(f"🚀 Launching replay: {replay_path.name}")
    print()
    
    # Launch replay
    subprocess.Popen([str(replay_path.absolute())], shell=True)
    
    print("⏳ Waiting for SC2 to start...")
    print("📹 Observe the camera behavior!")


if __name__ == "__main__":
    main()
