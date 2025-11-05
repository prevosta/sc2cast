"""
Test methods for getting current replay time during playback.

We need to know "we're at 5:30 game time" to sync:
- Commentary with game events
- Stats panels with timeline
- Camera decisions with action
"""

import subprocess
import time
from pathlib import Path
import win32gui
import win32con


def get_sc2_window_title():
    """Get StarCraft II window title (might contain time info)."""
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if "StarCraft II" in title or "SC2" in title:
                windows.append((hwnd, title))
    
    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows


def main():
    """Test replay time detection methods."""
    replay_path = Path("replays/4323200_changeling_Mike_MagannathaAIE_v2.SC2Replay")
    
    if not replay_path.exists():
        print(f"❌ Replay not found: {replay_path}")
        return
    
    print("⏱️  REPLAY TIME DETECTION TEST")
    print("=" * 60)
    print()
    print("🚀 Launching replay...")
    print()
    
    # Launch replay
    process = subprocess.Popen([str(replay_path.absolute())], shell=True)
    
    print("⏳ Waiting 5 seconds for SC2 to start...")
    time.sleep(5)
    
    print()
    print("🔍 METHOD 1: Window Title Detection")
    print("-" * 60)
    
    try:
        sc2_windows = get_sc2_window_title()
        if sc2_windows:
            for hwnd, title in sc2_windows:
                print(f"   Window: {title}")
                print(f"   Handle: {hwnd}")
        else:
            print("   ❌ No SC2 window found")
    except Exception as e:
        print(f"   ⚠️  Error: {e}")
    
    print()
    print("🔍 METHOD 2: OCR on Game Timer")
    print("-" * 60)
    print("   📝 Would need to:")
    print("   1. Capture game timer region (top-center of screen)")
    print("   2. Use OCR (pytesseract) to read MM:SS")
    print("   3. Convert to game time")
    print("   ⚠️  Depends on: screen resolution, UI scaling, OCR accuracy")
    
    print()
    print("🔍 METHOD 3: sc2reader Timeline")
    print("-" * 60)
    print("   📝 sc2reader can parse replay timeline")
    print("   ⚠️  But only for FINISHED replays, not DURING playback")
    print("   ⚠️  Can't use for live camera control")
    
    print()
    print("🔍 METHOD 4: Timestamp Correlation")
    print("-" * 60)
    print("   📝 Track when replay started + elapsed time")
    print("   ⚠️  Assumes constant playback speed (no pause/fast-forward)")
    print("   ⚠️  Can drift over long replays")
    
    print()
    print("=" * 60)
    print("💡 RECOMMENDATION:")
    print("   Best approach likely: Window title + timestamp correlation")
    print("   with periodic OCR validation for accuracy")
    print()
    print("🧪 Let SC2 run for 10 seconds, then check window title again...")
    time.sleep(10)
    
    print()
    print("🔍 Window Title After 10 Seconds:")
    print("-" * 60)
    try:
        sc2_windows = get_sc2_window_title()
        if sc2_windows:
            for hwnd, title in sc2_windows:
                print(f"   Window: {title}")
        else:
            print("   ❌ No SC2 window found")
    except Exception as e:
        print(f"   ⚠️  Error: {e}")
    
    print()
    print("✅ Test complete!")
    print("📋 Manually observe: Does window title show game time?")


if __name__ == "__main__":
    main()
