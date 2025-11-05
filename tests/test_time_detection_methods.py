"""
Comprehensive test of all replay time detection methods.
"""

import subprocess
import time
from pathlib import Path
import win32gui
import pyautogui
from PIL import Image
import io


def get_all_sc2_info():
    """Get all possible SC2 window information."""
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if "StarCraft" in title or "SC2" in title or "Blizzard" in title:
                windows.append({
                    'hwnd': hwnd,
                    'title': title,
                    'class': win32gui.GetClassName(hwnd),
                    'rect': win32gui.GetWindowRect(hwnd)
                })
    
    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows


def capture_timer_region():
    """Capture the game timer region."""
    # Timer position: x=1572, y=590, width=200, height=25
    # (User-confirmed coordinates from fullscreen test)
    screenshot = pyautogui.screenshot(region=(1572, 590, 200, 25))
    return screenshot


def main():
    """Test all replay time detection methods comprehensively."""
    replay_path = Path("replays/4323200_changeling_Mike_MagannathaAIE_v2.SC2Replay")
    
    if not replay_path.exists():
        print(f"❌ Replay not found: {replay_path}")
        return
    
    print("⏱️  COMPREHENSIVE REPLAY TIME DETECTION")
    print("=" * 80)
    print()
    print("🚀 Launching replay...")
    
    # Launch replay
    process = subprocess.Popen([str(replay_path.absolute())], shell=True)
    
    print("⏳ Waiting 35 seconds for SC2 to fully load (loading screen ~30s)...")
    time.sleep(35)
    
    # Check window info multiple times
    for i in range(3):
        print()
        print(f"📊 SAMPLE {i+1} - Time: {i*5} seconds into monitoring")
        print("-" * 80)
        
        sc2_windows = get_all_sc2_info()
        if sc2_windows:
            for win in sc2_windows:
                print(f"   Title: {win['title']}")
                print(f"   Class: {win['class']}")
                print(f"   Rect:  {win['rect']}")
                print()
        else:
            print("   ❌ No SC2 windows found")
        
        # Capture timer region
        print("   📸 Capturing timer region...")
        try:
            timer_img = capture_timer_region()
            img_path = Path(f"output/timer_sample_{i+1}.png")
            timer_img.save(img_path)
            print(f"   ✅ Saved: {img_path}")
        except Exception as e:
            print(f"   ⚠️  Capture failed: {e}")
        
        if i < 2:
            print(f"   ⏳ Waiting 5 seconds...")
            time.sleep(5)
    
    print()
    print("=" * 80)
    print("📋 ANALYSIS:")
    print()
    print("1️⃣  Window Title Method:")
    print("    - Check if title contains time information")
    print("    - Look in output above for patterns like '5:30' or 'min:sec'")
    print()
    print("2️⃣  OCR Timer Method:")
    print("    - Check timer_sample_*.png images in output/")
    print("    - See if game timer is visible and readable")
    print("    - Need pytesseract for OCR (pip install pytesseract)")
    print()
    print("3️⃣  Timestamp Correlation:")
    print("    - Start time: Record when replay starts")
    print("    - Elapsed time: time.time() - start_time")
    print("    - Game time: elapsed_time * playback_speed")
    print("    - Pros: Simple, reliable")
    print("    - Cons: Can't detect pause/speed changes")
    print()
    print("💡 RECOMMENDATION:")
    print("   Use timestamp correlation as PRIMARY method")
    print("   + OCR as VALIDATION (every 10 seconds)")
    print("   = Accurate, self-correcting time tracking!")
    print()


if __name__ == "__main__":
    main()
