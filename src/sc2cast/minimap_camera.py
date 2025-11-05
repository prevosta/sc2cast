"""
Minimap camera controller for SC2 replays.

Controls camera by clicking on minimap to jump to different map locations.
"""

import pyautogui
import time
from typing import Tuple, List


class MinimapCameraController:
    """Control SC2 camera by clicking on minimap."""
    
    # Minimap coordinates (1920x1080 resolution)
    MINIMAP_X = 25
    MINIMAP_Y = 810
    MINIMAP_WIDTH = 267
    MINIMAP_HEIGHT = 256
    
    def __init__(self):
        """Initialize minimap camera controller."""
        self.center_x = self.MINIMAP_X + self.MINIMAP_WIDTH // 2
        self.center_y = self.MINIMAP_Y + self.MINIMAP_HEIGHT // 2
    
    def map_to_minimap(self, game_x: float, game_y: float, map_size: int = 200) -> Tuple[int, int]:
        """
        Convert game coordinates to minimap pixel coordinates.
        
        Args:
            game_x: X coordinate in game (0-map_size)
            game_y: Y coordinate in game (0-map_size)
            map_size: Size of the map (default 200 for most maps)
        
        Returns:
            (pixel_x, pixel_y) for minimap click
        """
        # Normalize to 0-1 range
        norm_x = game_x / map_size
        norm_y = game_y / map_size
        
        # Map to minimap pixels
        pixel_x = self.MINIMAP_X + int(norm_x * self.MINIMAP_WIDTH)
        pixel_y = self.MINIMAP_Y + int(norm_y * self.MINIMAP_HEIGHT)
        
        return pixel_x, pixel_y
    
    def click_minimap_position(self, x: int, y: int, duration: float = 0.1):
        """
        Click a specific position on the minimap.
        
        Args:
            x: Pixel X coordinate on screen
            y: Pixel Y coordinate on screen
            duration: Click duration in seconds
        """
        pyautogui.click(x, y, duration=duration)
    
    def move_to_game_position(self, game_x: float, game_y: float, map_size: int = 200):
        """
        Move camera to specific game coordinates.
        
        Args:
            game_x: X coordinate in game
            game_y: Y coordinate in game
            map_size: Size of the map
        """
        pixel_x, pixel_y = self.map_to_minimap(game_x, game_y, map_size)
        self.click_minimap_position(pixel_x, pixel_y)
    
    def get_strategic_positions(self) -> List[Tuple[int, int, str]]:
        """
        Get strategic minimap positions for common camera views.
        
        Returns:
            List of (pixel_x, pixel_y, description) tuples
        """
        return [
            (self.center_x, self.center_y, "Map Center"),
            (self.MINIMAP_X + 30, self.MINIMAP_Y + 30, "Top-Left (Player 1 Start)"),
            (self.MINIMAP_X + self.MINIMAP_WIDTH - 30, 
             self.MINIMAP_Y + self.MINIMAP_HEIGHT - 30, "Bottom-Right (Player 2 Start)"),
            (self.MINIMAP_X + 30, 
             self.MINIMAP_Y + self.MINIMAP_HEIGHT - 30, "Bottom-Left Expansion"),
            (self.MINIMAP_X + self.MINIMAP_WIDTH - 30, 
             self.MINIMAP_Y + 30, "Top-Right Expansion"),
            (self.center_x, self.MINIMAP_Y + 30, "Top-Center Watch Tower"),
            (self.center_x, 
             self.MINIMAP_Y + self.MINIMAP_HEIGHT - 30, "Bottom-Center Watch Tower"),
        ]
    
    def tour_map(self, pause_seconds: float = 2.0):
        """
        Tour strategic map positions for overview.
        
        Args:
            pause_seconds: Seconds to pause at each position
        """
        positions = self.get_strategic_positions()
        
        for x, y, description in positions:
            print(f"📹 Moving to: {description}")
            self.click_minimap_position(x, y)
            time.sleep(pause_seconds)


def main():
    """Test minimap camera controller."""
    import subprocess
    from pathlib import Path
    
    print("🗺️  MINIMAP CAMERA CONTROLLER TEST")
    print("=" * 80)
    print()
    
    # Initialize controller
    controller = MinimapCameraController()
    
    print("📋 Minimap Configuration:")
    print(f"   Position: ({controller.MINIMAP_X}, {controller.MINIMAP_Y})")
    print(f"   Size: {controller.MINIMAP_WIDTH}x{controller.MINIMAP_HEIGHT}")
    print(f"   Center: ({controller.center_x}, {controller.center_y})")
    print()
    
    # Launch replay
    replay_path = Path("replays/4323200_changeling_Mike_MagannathaAIE_v2.SC2Replay")
    print("🚀 Launching replay...")
    subprocess.Popen([str(replay_path.absolute())], shell=True)
    
    print("⏳ Waiting 35 seconds for replay to start...")
    time.sleep(35)
    
    print()
    print("🎥 Starting map tour...")
    print("-" * 80)
    
    controller.tour_map(pause_seconds=2.5)
    
    print()
    print("-" * 80)
    print("✅ Map tour complete!")
    print()


if __name__ == "__main__":
    main()
