"""
Test OCR (Optical Character Recognition) on game timer.
"""

import subprocess
import time
from pathlib import Path
import pyautogui

try:
    import pytesseract
    from PIL import Image
    PYTESSERACT_AVAILABLE = True
except ImportError:
    PYTESSERACT_AVAILABLE = False


def parse_game_time(text):
    """Extract game time from OCR text like '3:37 / 9:28'."""
    # Clean up text
    text = text.strip().replace(' ', '')
    
    # Look for pattern: MM:SS/MM:SS
    if '/' in text:
        parts = text.split('/')
        if len(parts) == 2:
            current = parts[0].strip()
            total = parts[1].strip()
            return current, total
    
    return None, None


def capture_and_read_timer():
    """Capture timer region and read with OCR."""
    # Capture timer
    screenshot = pyautogui.screenshot(region=(1572, 590, 200, 25))
    
    if not PYTESSERACT_AVAILABLE:
        return None, screenshot
    
    # Convert to grayscale for better OCR
    screenshot = screenshot.convert('L')
    
    # Try OCR
    text = pytesseract.image_to_string(screenshot, config='--psm 7 digits')
    
    return text, screenshot


def main():
    """Test OCR timer reading during live replay."""
    if not PYTESSERACT_AVAILABLE:
        print("❌ pytesseract not installed!")
        print("   Install: poetry add pytesseract")
        print("   Also need Tesseract-OCR: https://github.com/UB-Mannheim/tesseract/wiki")
        return
    
    replay_path = Path("replays/4323200_changeling_Mike_MagannathaAIE_v2.SC2Replay")
    
    print("🔍 OCR TIMER READING TEST")
    print("=" * 80)
    print()
    print("🚀 Launching replay...")
    
    # Launch replay
    subprocess.Popen([str(replay_path.absolute())], shell=True)
    
    print("⏳ Waiting 35 seconds for gameplay to start...")
    time.sleep(35)
    
    # Test OCR multiple times
    print()
    for i in range(5):
        print(f"📊 SAMPLE {i+1}")
        print("-" * 80)
        
        text, screenshot = capture_and_read_timer()
        
        # Save screenshot
        img_path = Path(f"output/ocr_test_{i+1}.png")
        screenshot.save(img_path)
        
        if text:
            print(f"   Raw OCR: '{text}'")
            current, total = parse_game_time(text)
            if current and total:
                print(f"   ✅ Parsed: {current} / {total}")
            else:
                print(f"   ⚠️  Could not parse time")
        else:
            print(f"   ⚠️  OCR failed")
        
        print(f"   Saved: {img_path}")
        
        if i < 4:
            print(f"   ⏳ Waiting 5 seconds...\n")
            time.sleep(5)
    
    print()
    print("=" * 80)
    print("📋 RESULTS:")
    print("   Check accuracy of OCR readings above")
    print("   Compare with actual timer in screenshots")
    print()


if __name__ == "__main__":
    main()
