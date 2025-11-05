"""
Game Clock - Synchronized time tracking for replay recording.

Uses OCR to detect replay start/end and timestamp correlation for accurate timing.
"""

import time
from typing import Optional, Tuple
from pathlib import Path
import sys

# Add parent directory to path for imports
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

from sc2cast.timer_reader import GameTimerReader


class GameClock:
    """
    Manages game time during replay recording.
    
    Strategy:
    1. Poll OCR until timer appears (replay started)
    2. Use timestamp correlation (real_time = game_time at normal speed)
    3. Validate periodically with OCR (every 10-15 seconds)
    4. Detect end when timer reaches final time
    """
    
    def __init__(self, replay_duration_seconds: int, speed_multiplier: float = 1.0):
        """
        Initialize game clock.
        
        Args:
            replay_duration_seconds: Total replay length (from replay metadata)
            speed_multiplier: Playback speed multiplier (1.0 = normal, 2.0 = 2x speed)
        """
        self.replay_duration = replay_duration_seconds
        self.speed_multiplier = speed_multiplier
        self.timer_reader = GameTimerReader()
        
        # State
        self.game_start_time: Optional[float] = None
        self.game_start_offset: int = 0  # If replay doesn't start at 0:00
        self.last_ocr_time: Optional[float] = None
        self.last_ocr_game_time: Optional[int] = None
        self.is_started = False
        self.is_ended = False
    
    def wait_for_replay_start(self, timeout: float = 60.0, poll_interval: float = 2.0) -> bool:
        """
        Poll OCR until timer appears (replay has started).
        
        Uses 3 consecutive readings to confirm start.
        
        Args:
            timeout: Max seconds to wait
            poll_interval: Seconds between OCR checks
            
        Returns:
            True if started, False if timeout
        """
        print("⏳ Waiting for replay to start...")
        start_wait = time.time()
        
        while time.time() - start_wait < timeout:
            # Try to read timer 3 times for validation
            readings = []
            for i in range(3):
                result = self.timer_reader.read_timer()
                if result:
                    clean_time, raw_text = result
                    if clean_time:
                        game_seconds = self.timer_reader.time_to_seconds(clean_time)
                        if game_seconds is not None:
                            readings.append((game_seconds, clean_time))
                if i < 2:
                    time.sleep(0.2)
            
            # If we got at least 2 consistent readings, replay might be starting
            if len(readings) >= 2:
                # Use median for robustness
                readings.sort(key=lambda x: x[0])
                median_idx = len(readings) // 2
                game_seconds, clean_time = readings[median_idx]
                
                # Wait for timer to advance past 0:00 to ensure game loaded
                # (loading screen can show 0:00 before game starts)
                if game_seconds < 3:
                    print(f"⏳ Timer detected at {clean_time}, waiting for game to fully load...")
                    time.sleep(3)  # Wait a bit more
                    continue
                
                self.game_start_time = time.time()
                self.game_start_offset = game_seconds
                self.is_started = True
                self.last_ocr_time = self.game_start_time
                self.last_ocr_game_time = game_seconds
                
                print(f"✅ Replay started! First timer reading: {clean_time}")
                print(f"   Validated with {len(readings)}/3 readings")
                print(f"   Start offset: {self.game_start_offset}s")
                return True
            
            # Not ready yet, wait and retry
            time.sleep(poll_interval)
        
        print(f"❌ Timeout waiting for replay start after {timeout}s")
        return False
    
    def get_current_game_time(self) -> int:
        """
        Get current game time in seconds.
        
        Uses timestamp correlation: game_time = start_offset + (now - start_time) * speed_multiplier
        
        Returns:
            Current game time in seconds
        """
        if not self.is_started or self.game_start_time is None:
            return 0
        
        elapsed = time.time() - self.game_start_time
        current_time = self.game_start_offset + int(elapsed * self.speed_multiplier)
        
        return current_time
    
    def get_current_game_time_formatted(self) -> str:
        """Get current game time as MM:SS string."""
        seconds = self.get_current_game_time()
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}:{secs:02d}"
    
    def validate_sync(self) -> Tuple[bool, Optional[int]]:
        """
        Validate clock sync with OCR.
        
        Reads timer via OCR 3 times and uses consensus for reliability.
        Auto-corrects if drift detected.
        
        Returns:
            (is_valid, drift_seconds) - drift is None if OCR failed
        """
        # Read timer 3 times over 0.6 seconds (3 frames at 30fps = 0.1s apart)
        readings = []
        for i in range(3):
            result = self.timer_reader.read_timer()
            if result:
                clean_time, raw_text = result
                if clean_time:
                    ocr_seconds = self.timer_reader.time_to_seconds(clean_time)
                    if ocr_seconds is not None:
                        readings.append((ocr_seconds, clean_time))
            if i < 2:  # Don't sleep after last reading
                time.sleep(0.2)
        
        if not readings:
            return True, None  # All OCR failed, assume OK
        
        # Use median value for robustness
        readings.sort(key=lambda x: x[0])
        median_idx = len(readings) // 2
        ocr_seconds, clean_time = readings[median_idx]
        
        # Compare with our timestamp-based time
        our_time = self.get_current_game_time()
        drift = abs(ocr_seconds - our_time)
        
        self.last_ocr_time = time.time()
        self.last_ocr_game_time = ocr_seconds
        
        # If drift > 3 seconds, auto-correct
        if drift > 3:
            print(f"⚠️  Clock drift detected: {drift}s (OCR: {clean_time}, Clock: {self.get_current_game_time_formatted()})")
            print(f"   Validated with {len(readings)}/3 readings")
            print(f"   Auto-correcting...")
            
            # Recalibrate: set new start time based on OCR reading
            self.game_start_time = time.time()
            self.game_start_offset = ocr_seconds
            
            print(f"   ✅ Recalibrated to: {clean_time}")
            return False, drift
        
        return True, drift
    
    def check_if_ended(self) -> bool:
        """
        Check if replay has ended.
        
        Uses OCR to detect when timer reaches end time.
        Validates with 3 consecutive readings for reliability.
        """
        if not self.is_started:
            return False
        
        current_time = self.get_current_game_time()
        
        # Check if we've reached expected duration
        if current_time >= self.replay_duration - 30:
            # Near the end - verify with 3 OCR readings
            readings = []
            for i in range(3):
                result = self.timer_reader.read_timer()
                if result:
                    clean_time, _ = result
                    if clean_time:
                        ocr_seconds = self.timer_reader.time_to_seconds(clean_time)
                        if ocr_seconds is not None:
                            readings.append((ocr_seconds, clean_time))
                if i < 2:
                    time.sleep(0.2)
            
            if len(readings) >= 2:
                # Use median
                readings.sort(key=lambda x: x[0])
                median_idx = len(readings) // 2
                ocr_seconds, clean_time = readings[median_idx]
                
                # Check if we're at or past the end
                if ocr_seconds >= self.replay_duration - 5:
                    if not self.is_ended:
                        print(f"🏁 Replay ended! Duration: {clean_time}")
                        print(f"   Validated with {len(readings)}/3 readings")
                        self.is_ended = True
                    return True
        
        # Fallback: if we're way past duration
        if current_time >= self.replay_duration + 30:
            if not self.is_ended:
                print(f"🏁 Replay ended! Duration: {self.get_current_game_time_formatted()} (timeout)")
                self.is_ended = True
            return True
        
        return False
    
    def should_validate_now(self, validation_interval: float = 15.0) -> bool:
        """
        Check if it's time for periodic OCR validation.
        
        Args:
            validation_interval: Seconds between validations
            
        Returns:
            True if validation is due
        """
        if not self.is_started or self.last_ocr_time is None:
            return False
        
        elapsed_since_last = time.time() - self.last_ocr_time
        return elapsed_since_last >= validation_interval


def main():
    """Test game clock with live replay."""
    import subprocess
    
    print("⏱️  GAME CLOCK TEST")
    print("=" * 80)
    print()
    
    # Launch replay
    replay_path = Path("replays/4323200_changeling_Mike_MagannathaAIE_v2.SC2Replay")
    print("🚀 Launching replay...")
    subprocess.Popen([str(replay_path.absolute())], shell=True)
    
    # Create clock (9:28 = 568 seconds)
    clock = GameClock(replay_duration_seconds=568)
    
    # Wait for start
    if not clock.wait_for_replay_start(timeout=60.0):
        print("❌ Failed to detect replay start")
        return
    
    print()
    print("🎬 Replay running - monitoring clock...")
    print("-" * 80)
    
    # Monitor clock until end
    last_print = time.time()
    validation_count = 0
    
    while not clock.check_if_ended():
        current_time = clock.get_current_game_time_formatted()
        
        # Print every 5 seconds
        if time.time() - last_print >= 5.0:
            print(f"⏱️  Game time: {current_time}")
            last_print = time.time()
        
        # Periodic validation
        if clock.should_validate_now(validation_interval=15.0):
            is_valid, drift = clock.validate_sync()
            validation_count += 1
            
            if drift is not None:
                if is_valid:
                    print(f"✅ Validation #{validation_count}: Sync OK (drift: {drift}s)")
                else:
                    print(f"⚠️  Validation #{validation_count}: Recalibrated (drift was: {drift}s)")
        
        time.sleep(0.5)
    
    print()
    print("-" * 80)
    print("✅ Clock test complete!")
    print(f"   Final time: {clock.get_current_game_time_formatted()}")
    print(f"   Validations performed: {validation_count}")
    print()


if __name__ == "__main__":
    main()
