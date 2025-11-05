"""
Robust game timer reader using EasyOCR with cleanup logic.
"""

import re
import pyautogui
from pathlib import Path
import easyocr
import numpy as np


class GameTimerReader:
    """Read game timer from screen with OCR and cleanup."""
    
    def __init__(self):
        """Initialize EasyOCR reader."""
        print("🔧 Initializing OCR reader...")
        self.reader = easyocr.Reader(['en'], gpu=False)
        print("✅ OCR ready!")
    
    def capture_timer(self):
        """Capture timer region (1572, 590, 200x25)."""
        screenshot = pyautogui.screenshot(region=(1572, 590, 200, 25))
        # Convert to numpy array for EasyOCR
        return np.array(screenshot)
    
    def clean_time_string(self, text):
        """Clean OCR output to get valid MM:SS format."""
        # Remove spaces
        text = text.replace(' ', '')
        
        # Fix common OCR errors
        text = text.replace('.', ':')  # . confused with :
        text = text.replace(',', ':')  # , confused with :
        text = text.replace('|', ':')  # | confused with :
        text = text.replace('I', '1')  # I confused with 1
        text = text.replace('O', '0')  # O confused with 0
        text = text.replace('o', '0')  # o confused with 0
        
        # Extract just the current time (before /)
        if '/' in text:
            text = text.split('/')[0]
        
        # Look for MM:SS pattern
        match = re.search(r'(\d{1,2}):(\d{2})', text)
        if match:
            minutes = match.group(1)
            seconds = match.group(2)
            return f"{minutes}:{seconds}"
        
        return None
    
    def read_timer(self):
        """
        Capture and read game timer.
        
        Returns:
            str: Time in "MM:SS" format, or None if read failed
        """
        # Capture screen
        img = self.capture_timer()
        
        # OCR
        results = self.reader.readtext(img, detail=0)
        
        if not results:
            return None
        
        # Combine all text
        raw_text = ' '.join(results)
        
        # Clean and parse
        clean_time = self.clean_time_string(raw_text)
        
        return clean_time, raw_text
    
    def time_to_seconds(self, time_str):
        """Convert MM:SS to total seconds."""
        if not time_str or ':' not in time_str:
            return None
        
        try:
            parts = time_str.split(':')
            minutes = int(parts[0])
            seconds = int(parts[1])
            return minutes * 60 + seconds
        except (ValueError, IndexError):
            return None


def main():
    """Test the timer reader."""
    import time
    import subprocess
    
    replay_path = Path("replays/4323200_changeling_Mike_MagannathaAIE_v2.SC2Replay")
    
    print("⏱️  ROBUST TIMER READING TEST")
    print("=" * 80)
    print()
    
    # Initialize reader
    timer_reader = GameTimerReader()
    
    print()
    print("🚀 Launching replay...")
    subprocess.Popen([str(replay_path.absolute())], shell=True)
    
    print("⏳ Waiting 35 seconds for gameplay...")
    time.sleep(35)
    
    print()
    print("📊 Reading timer every 3 seconds (10 samples):")
    print("-" * 80)
    
    for i in range(10):
        result = timer_reader.read_timer()
        
        if result:
            clean_time, raw_text = result
            if clean_time:
                seconds = timer_reader.time_to_seconds(clean_time)
                print(f"Sample {i+1:2d} | Clean: {clean_time:>5s} | Seconds: {seconds:>3d} | Raw: {raw_text}")
            else:
                print(f"Sample {i+1:2d} | ⚠️  Parse failed | Raw: {raw_text}")
        else:
            print(f"Sample {i+1:2d} | ❌ Failed to read timer")
        
        if i < 9:
            time.sleep(3)
    
    print()
    print("=" * 80)
    print("✅ Test complete!")
    print()
    print("📋 Analysis:")
    print("   - Check if times increment correctly")
    print("   - Should increase by ~3 seconds each sample")
    print("   - Clean time should be consistent MM:SS format")
    print()


if __name__ == "__main__":
    main()
