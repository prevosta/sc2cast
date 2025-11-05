"""Test keyboard automation for SC2 camera control during replay playback."""

import time
import pyautogui
from pathlib import Path
import subprocess


def launch_replay(replay_path):
    """Launch the replay in SC2."""
    replay_path = Path(replay_path).absolute()
    
    if not replay_path.exists():
        print(f"❌ Replay file not found: {replay_path}")
        return False
    
    print(f"✅ Replay found: {replay_path}")
    print(f"🚀 Launching replay in SC2...")
    
    try:
        subprocess.Popen([str(replay_path)], shell=True)
        print(f"✅ Replay launched!")
        return True
    except Exception as e:
        print(f"❌ Failed to launch replay: {e}")
        return False


def test_keyboard_automation():
    """
    Test sending keyboard inputs to SC2 during replay.
    
    Camera hotkeys in SC2 replays:
    - 1, 2: Switch to Player 1, Player 2 camera
    - F1-F12: Custom camera locations (if set)
    - Tab: Toggle stats/production panel
    - Space: Center on selection
    """
    print("\n" + "=" * 60)
    print("Sprint 1.4 - Task 3: Keyboard Automation Test")
    print("=" * 60)
    
    print("\n🎯 CRITICAL TEST:")
    print("  This determines if we can control camera during replay!")
    print("  If this works → Camera director is viable")
    print("  If this fails → Need alternative approach")
    
    print("\n📝 MANUAL TEST STEPS:")
    print("  1. Replay should be starting in SC2")
    print("  2. Once replay is playing, come back here")
    print("  3. Press Enter when replay is running...")
    
    input()
    
    print("\n⏳ Waiting 3 seconds for you to focus on SC2 window...")
    time.sleep(3)
    
    print("\n🎮 Sending keyboard inputs to SC2:")
    
    # Test 1: Switch to Player 1 camera
    print("  → Pressing '1' (Player 1 camera)...")
    pyautogui.press('1')
    time.sleep(2)
    
    # Test 2: Switch to Player 2 camera
    print("  → Pressing '2' (Player 2 camera)...")
    pyautogui.press('2')
    time.sleep(2)
    
    # Test 3: Toggle stats panel
    print("  → Pressing 'Tab' (Toggle stats)...")
    pyautogui.press('tab')
    time.sleep(2)
    
    # Test 4: Toggle stats again
    print("  → Pressing 'Tab' again (Toggle stats off)...")
    pyautogui.press('tab')
    time.sleep(2)
    
    # Test 5: Switch back to Player 1
    print("  → Pressing '1' again (Player 1 camera)...")
    pyautogui.press('1')
    time.sleep(1)
    
    print("\n✅ Keyboard inputs sent!")
    print("\n" + "=" * 60)
    print("VERIFICATION:")
    print("=" * 60)
    print("\n❓ Did the camera switch between players?")
    print("❓ Did the stats panel toggle on/off?")
    print("\nIf YES:")
    print("  ✅ CRITICAL SUCCESS - Camera control works!")
    print("  ✅ Camera director is viable!")
    print("  → Continue to Task 4 (screen capture)")
    print("\nIf NO:")
    print("  ❌ Keyboard automation failed")
    print("  → Try alternative input methods")
    print("  → May need to use SC2 API or different approach")


def main():
    """Run keyboard automation test."""
    replay_path = "replays/4323200_changeling_Mike_MagannathaAIE_v2.SC2Replay"
    
    # Launch replay
    if not launch_replay(replay_path):
        return
    
    # Give SC2 time to start
    print("\n⏳ Waiting 15 seconds for SC2 to load replay...")
    print("   (SC2 startup can be slow)")
    time.sleep(15)
    
    # Test keyboard automation
    test_keyboard_automation()


if __name__ == "__main__":
    main()
