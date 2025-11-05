"""
Take fullscreen screenshot after 1 minute to identify timer position.
"""

import subprocess
import time
from pathlib import Path
import pyautogui


def main():
    """Launch replay and take fullscreen screenshot after 1 minute."""
    replay_path = Path("replays/4323200_changeling_Mike_MagannathaAIE_v2.SC2Replay")
    
    if not replay_path.exists():
        print(f"❌ Replay not found: {replay_path}")
        return
    
    print("📸 FULLSCREEN TIMER POSITION TEST")
    print("=" * 80)
    print()
    print("🚀 Launching replay...")
    
    # Launch replay
    process = subprocess.Popen([str(replay_path.absolute())], shell=True)
    
    print("⏳ Waiting 1 minute for gameplay...")
    print("   (30s loading + 30s gameplay)")
    
    # Wait 60 seconds total
    for i in range(60, 0, -10):
        print(f"   {i} seconds remaining...")
        time.sleep(10)
    
    print()
    print("📸 Taking fullscreen screenshot NOW!")
    screenshot = pyautogui.screenshot()
    
    output_path = Path("output/fullscreen_timer_1min.png")
    screenshot.save(output_path)
    
    print(f"✅ Saved: {output_path}")
    print()
    print("📋 Next steps:")
    print("   1. Open the screenshot")
    print("   2. Find the game timer position")
    print("   3. Report coordinates (x, y, width, height)")
    print()


if __name__ == "__main__":
    main()
