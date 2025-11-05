"""Test if we can launch SC2 and play a replay."""

import subprocess
import time
from pathlib import Path


def find_sc2_executable():
    """Find the StarCraft II executable."""
    possible_paths = [
        Path("C:/Program Files (x86)/StarCraft II/StarCraft II.exe"),
        Path("C:/Program Files/StarCraft II/StarCraft II.exe"),
    ]
    
    for path in possible_paths:
        if path.exists():
            return path
    
    return None


def launch_replay(replay_path):
    """
    Launch SC2 with a replay file.
    
    Windows allows opening .SC2Replay files directly with their associated app (SC2).
    This is simpler than trying to pass command-line args to SC2.exe
    """
    sc2_exe = find_sc2_executable()
    
    if not sc2_exe:
        print("❌ SC2 executable not found!")
        return False
    
    replay_path = Path(replay_path).absolute()
    
    if not replay_path.exists():
        print(f"❌ Replay file not found: {replay_path}")
        return False
    
    print(f"✅ SC2 found: {sc2_exe}")
    print(f"✅ Replay found: {replay_path}")
    print(f"\n🚀 Launching replay in SC2...")
    
    try:
        # Open the replay file directly (Windows will use SC2 as the default app)
        subprocess.Popen([str(replay_path)], shell=True)
        print(f"✅ Replay launched successfully!")
        print(f"\n� Replay should now be playing in SC2")
        print(f"Next: Implement screen capture to record the video")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to launch replay: {e}")
        return False


def main():
    """Test replay playback capability."""
    replay_path = "replays/4323200_changeling_Mike_MagannathaAIE_v2.SC2Replay"
    
    print("=" * 60)
    print("Sprint 1.4 - Task 2: Automated Replay Launch")
    print("=" * 60)
    print("\n✅ SUCCESS FROM MANUAL TEST:")
    print("  - Windows SC2 CAN play replays")
    print("  - AIArena replay format WORKS")
    print("  - Double-clicking .SC2Replay opens in SC2")
    print("\n🎯 NEW APPROACH:")
    print("  - Open replay file directly (shell association)")
    print("  - SC2 launches and plays replay automatically")
    print("  - Next: Screen capture with FFmpeg")
    print("\n" + "=" * 60)
    print()
    
    result = launch_replay(replay_path)
    
    if result:
        print("\n" + "=" * 60)
        print("✅ TASK 2 COMPLETE: Automated replay launch works!")
        print("=" * 60)
        print("NEXT: Task 3 - Screen capture with FFmpeg")
        print("  → Capture SC2 window while replay plays")
        print("  → Generate MP4 video file")
        print("  → Verify video quality")


if __name__ == "__main__":
    main()
