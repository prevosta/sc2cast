"""
Test EasyOCR for reading game timer (pure Python, no external dependencies).
"""

import subprocess
import time
from pathlib import Path
import pyautogui
import easyocr
import numpy as np


def parse_game_time(text):
    """Extract game time from text like '3:37 / 9:28' or '3:37/9:28'."""
    # Clean up text
    text = text.strip().replace(' ', '')
    
    # Look for pattern: MM:SS/MM:SS
    if '/' in text:
        parts = text.split('/')
        if len(parts) == 2:
            current = parts[0].strip()
            total = parts[1].strip()
            # Validate format (should be M:SS or MM:SS)
            if ':' in current and ':' in total:
                return current, total
    
    return None, None


def capture_and_read_timer(reader):
    """Capture timer region and read with EasyOCR."""
    # Capture timer (1572, 590, 200x25)
    screenshot = pyautogui.screenshot(region=(1572, 590, 200, 25))
    
    # Convert to numpy array for EasyOCR
    img_array = np.array(screenshot)
    
    # Run OCR
    results = reader.readtext(img_array, detail=0)
    
    # Combine all text
    text = ' '.join(results) if results else ''
    
    return text, screenshot


def main():
    """Test EasyOCR timer reading during live replay."""
    replay_path = Path("replays/4323200_changeling_Mike_MagannathaAIE_v2.SC2Replay")
    
    print("🔍 EASYOCR TIMER READING TEST")
    print("=" * 80)
    print()
    print("⏳ Initializing EasyOCR (first run downloads models ~100MB)...")
    
    # Initialize EasyOCR reader (English only, no GPU needed)
    reader = easyocr.Reader(['en'], gpu=False)
    
    print("✅ EasyOCR ready!")
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
        
        text, screenshot = capture_and_read_timer(reader)
        
        # Save screenshot
        img_path = Path(f"output/easyocr_test_{i+1}.png")
        screenshot.save(img_path)
        
        print(f"   Raw OCR: '{text}'")
        
        current, total = parse_game_time(text)
        if current and total:
            print(f"   ✅ Parsed: {current} / {total}")
        else:
            print(f"   ⚠️  Could not parse time from: '{text}'")
        
        print(f"   Saved: {img_path}")
        
        if i < 4:
            print(f"   ⏳ Waiting 5 seconds...\n")
            time.sleep(5)
    
    print()
    print("=" * 80)
    print("📋 RESULTS:")
    print("   ✅ If most samples parsed correctly -> OCR is viable!")
    print("   ⚠️  If parsing failed -> Use timestamp correlation instead")
    print()


if __name__ == "__main__":
    main()
