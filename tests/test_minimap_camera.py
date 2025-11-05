"""
Test camera control by clicking on minimap during replay playback.

The minimap allows us to jump camera to different locations.
We'll click various positions to move camera around the map.
"""

import subprocess
import time
from pathlib import Path
import pyautogui


def get_minimap_clicks():
    """
    Get minimap click positions for a 1920x1080 screen.
    
    Minimap position: x=25, y=810, width=267, height=256
    (User-confirmed coordinates)
    
    Returns list of (x, y) positions to click on minimap.
    """
    # Minimap bounds
    MINIMAP_X = 25
    MINIMAP_Y = 810
    MINIMAP_WIDTH = 267
    MINIMAP_HEIGHT = 256
    
    # Calculate center and corners
    center_x = MINIMAP_X + MINIMAP_WIDTH // 2
    center_y = MINIMAP_Y + MINIMAP_HEIGHT // 2
    
    # Strategic positions on minimap
    minimap_positions = [
        (center_x, center_y),                              # Center
        (MINIMAP_X + 20, MINIMAP_Y + 20),                 # Top-left (player 1 start)
        (MINIMAP_X + MINIMAP_WIDTH - 20, MINIMAP_Y + MINIMAP_HEIGHT - 20),  # Bottom-right (player 2 start)
        (MINIMAP_X + 20, MINIMAP_Y + MINIMAP_HEIGHT - 20), # Bottom-left
        (MINIMAP_X + MINIMAP_WIDTH - 20, MINIMAP_Y + 20),  # Top-right
        (center_x, MINIMAP_Y + 20),                        # Top-center
        (center_x, MINIMAP_Y + MINIMAP_HEIGHT - 20),       # Bottom-center
        (MINIMAP_X + 20, center_y),                        # Left-center
        (MINIMAP_X + MINIMAP_WIDTH - 20, center_y),        # Right-center
    ]
    
    return minimap_positions


def main():
    """Test camera control via minimap clicks."""
    replay_path = Path("replays/4323200_changeling_Mike_MagannathaAIE_v2.SC2Replay")
    
    if not replay_path.exists():
        print(f"❌ Replay not found: {replay_path}")
        return
    
    print("🗺️  MINIMAP CAMERA CONTROL TEST")
    print("=" * 80)
    print()
    print("📋 This test will:")
    print("   1. Launch replay")
    print("   2. Wait for loading (~30 seconds)")
    print("   3. Click different positions on minimap")
    print("   4. Camera should jump to those locations")
    print()
    print("🎯 Goal: Test if we can control camera via minimap clicks")
    print()
    print("=" * 80)
    print()
    print("🚀 Launching replay...")
    
    # Launch replay
    subprocess.Popen([str(replay_path.absolute())], shell=True)
    
    print("⏳ Waiting 35 seconds for replay to start...")
    time.sleep(35)
    
    print()
    print("🗺️  Starting minimap click sequence!")
    print("-" * 80)
    
    minimap_positions = get_minimap_clicks()
    
    for i, (x, y) in enumerate(minimap_positions, 1):
        print(f"Click {i}/9: Moving to position ({x}, {y})")
        
        # Click minimap position
        pyautogui.click(x, y)
        
        # Wait 2 seconds to observe camera movement
        time.sleep(2)
    
    print()
    print("-" * 80)
    print("✅ Minimap click test complete!")
    print()
    print("📋 Observations:")
    print("   - Did camera jump to different map locations?")
    print("   - Did minimap clicks work reliably?")
    print("   - This proves we can control camera during replay!")
    print()
    print("🎥 Next: Test if camera movements are SAVED in replay:")
    print("   1. Play a real game (not replay)")
    print("   2. Manually move camera via minimap during game")
    print("   3. Save game as replay")
    print("   4. Watch replay - does camera follow same path?")
    print()


if __name__ == "__main__":
    main()
