"""
Camera Director - Automated camera control during replay recording.

Executes camera scripts synchronized with game time.
"""

import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import sys

# Add parent directory to path for imports
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

from sc2cast.observer_hotkeys import ObserverHotkeys, StatPanel, UIPanel
from sc2cast.minimap_camera import MinimapCameraController


class ShotType(Enum):
    """Types of camera shots."""
    PLAYER_VIEW = "player_view"          # Switch to player perspective (F1-F8 or 1-2)
    MINIMAP_JUMP = "minimap_jump"        # Jump to minimap position
    STAT_PANEL = "stat_panel"            # Show stat comparison panel
    UI_PANEL = "ui_panel"                # Toggle UI panel
    FOLLOW_UNIT = "follow_unit"          # Follow selected unit


@dataclass
class CameraShot:
    """A single camera shot in the script."""
    time_seconds: int              # When to execute (game time)
    shot_type: ShotType           # Type of shot
    params: Dict[str, Any]        # Parameters for the shot
    executed: bool = False        # Whether shot has been executed
    
    def __repr__(self):
        return f"Shot({self.time_seconds}s, {self.shot_type.value}, {self.params})"


class CameraDirector:
    """
    Directs camera during replay recording.
    
    Executes camera scripts synchronized with game clock.
    """
    
    def __init__(self):
        """Initialize camera director."""
        self.hotkeys = ObserverHotkeys()
        self.minimap = MinimapCameraController()
        self.script: List[CameraShot] = []
        self.current_shot_index = 0
    
    def load_script(self, script: List[Dict[str, Any]]):
        """
        Load camera script.
        
        Args:
            script: List of shot dictionaries with format:
                {
                    "time": "MM:SS" or seconds (int),
                    "type": "player_view|minimap_jump|stat_panel|ui_panel",
                    "params": {...}
                }
        
        Example:
            [
                {"time": "0:30", "type": "player_view", "params": {"player": 1}},
                {"time": "1:00", "type": "player_view", "params": {"player": 2}},
                {"time": 90, "type": "stat_panel", "params": {"panel": "resources"}},
            ]
        """
        self.script = []
        
        for shot_dict in script:
            # Parse time
            time_val = shot_dict["time"]
            if isinstance(time_val, str):
                # Parse MM:SS format
                parts = time_val.split(":")
                time_seconds = int(parts[0]) * 60 + int(parts[1])
            else:
                time_seconds = int(time_val)
            
            # Parse type
            shot_type = ShotType(shot_dict["type"])
            
            # Get params
            params = shot_dict.get("params", {})
            
            shot = CameraShot(
                time_seconds=time_seconds,
                shot_type=shot_type,
                params=params
            )
            self.script.append(shot)
        
        # Sort by time
        self.script.sort(key=lambda s: s.time_seconds)
        self.current_shot_index = 0
        
        print(f"📋 Loaded camera script with {len(self.script)} shots")
        for shot in self.script:
            print(f"   {shot}")
    
    def execute_shot(self, shot: CameraShot):
        """
        Execute a single camera shot.
        
        Args:
            shot: CameraShot to execute
        """
        print(f"🎬 Executing: {shot}")
        
        # Small delay to ensure commands are processed
        time.sleep(0.1)
        
        if shot.shot_type == ShotType.PLAYER_VIEW:
            player = shot.params.get("player", 1)
            self.hotkeys.switch_to_player(player)
        
        elif shot.shot_type == ShotType.MINIMAP_JUMP:
            # Check if we have game coordinates (need conversion)
            game_x = shot.params.get("game_x")
            game_y = shot.params.get("game_y")
            x = shot.params.get("x")
            y = shot.params.get("y")
            
            if game_x and game_y:
                # Game coordinates - convert to minimap pixels
                self.minimap.move_to_game_position(game_x, game_y)
            elif x and y:
                # Assume these are game coordinates too (0-200 range)
                # Convert to minimap pixels
                self.minimap.move_to_game_position(x, y)
        
        elif shot.shot_type == ShotType.STAT_PANEL:
            panel_name = shot.params.get("panel", "resources")
            panel_map = {
                "army_value": StatPanel.ARMY_VALUE,
                "production": StatPanel.PRODUCTION,
                "income": StatPanel.INCOME,
                "units_lost": StatPanel.UNITS_LOST,
                "apm": StatPanel.APM,
                "resources": StatPanel.RESOURCES,
                "spending": StatPanel.SPENDING,
                "units": StatPanel.UNITS,
                "buildings": StatPanel.BUILDINGS,
                "upgrades": StatPanel.UPGRADES,
                "close": StatPanel.CLOSE_PANEL,
            }
            panel = panel_map.get(panel_name, StatPanel.RESOURCES)
            self.hotkeys.show_stat_panel(panel)
        
        elif shot.shot_type == ShotType.UI_PANEL:
            panel_name = shot.params.get("panel", "resources_panel")
            panel_map = {
                "name_panel": UIPanel.NAME_PANEL,
                "resources_panel": UIPanel.RESOURCES_PANEL,
                "army_supply_panel": UIPanel.ARMY_SUPPLY_PANEL,
                "units_killed_panel": UIPanel.UNITS_KILLED_PANEL,
                "apm_panel": UIPanel.APM_PANEL,
                "hide_all_ui": UIPanel.HIDE_ALL_UI,
            }
            panel = panel_map.get(panel_name, UIPanel.RESOURCES_PANEL)
            self.hotkeys.toggle_ui_panel(panel)
        
        elif shot.shot_type == ShotType.FOLLOW_UNIT:
            hold = shot.params.get("hold", False)
            self.hotkeys.follow_unit(hold=hold)
        
        shot.executed = True
    
    def update(self, current_game_time: int):
        """
        Update director - execute shots that are due.
        
        Args:
            current_game_time: Current game time in seconds
        """
        # Check if any shots need to be executed
        while self.current_shot_index < len(self.script):
            shot = self.script[self.current_shot_index]
            
            # If shot time has passed and not executed yet
            if current_game_time >= shot.time_seconds and not shot.executed:
                self.execute_shot(shot)
                self.current_shot_index += 1
            else:
                # No more shots ready yet
                break
    
    def get_progress(self) -> str:
        """Get progress string for logging."""
        total = len(self.script)
        executed = sum(1 for shot in self.script if shot.executed)
        return f"{executed}/{total} shots executed"


def main():
    """Test camera director with sample script."""
    import subprocess
    from sc2cast.game_clock import GameClock
    
    print("🎬 CAMERA DIRECTOR TEST")
    print("=" * 80)
    print()
    
    # Sample camera script
    script = [
        {"time": "0:05", "type": "player_view", "params": {"player": 1}},
        {"time": "0:15", "type": "player_view", "params": {"player": 2}},
        {"time": "0:25", "type": "stat_panel", "params": {"panel": "resources"}},
        {"time": "0:35", "type": "stat_panel", "params": {"panel": "close"}},
        {"time": "0:45", "type": "player_view", "params": {"player": 1}},
        {"time": "1:00", "type": "minimap_jump", "params": {"game_x": 100, "game_y": 100}},
        {"time": "1:10", "type": "player_view", "params": {"player": 2}},
    ]
    
    # Initialize director
    director = CameraDirector()
    director.load_script(script)
    
    print()
    
    # Launch replay
    replay_path = Path("replays/4323200_changeling_Mike_MagannathaAIE_v2.SC2Replay")
    print("🚀 Launching replay...")
    subprocess.Popen([str(replay_path.absolute())], shell=True)
    
    # Create clock
    clock = GameClock(replay_duration_seconds=568)
    
    # Wait for start
    if not clock.wait_for_replay_start(timeout=60.0):
        print("❌ Failed to detect replay start")
        return
    
    print()
    print("🎬 Running camera director...")
    print("-" * 80)
    
    # Run for 90 seconds to see the script execute
    test_duration = 90
    start_test = time.time()
    last_print = time.time()
    
    while time.time() - start_test < test_duration:
        current_time = clock.get_current_game_time()
        
        # Update director
        director.update(current_time)
        
        # Print progress every 5 seconds
        if time.time() - last_print >= 5.0:
            print(f"⏱️  {clock.get_current_game_time_formatted()} | {director.get_progress()}")
            last_print = time.time()
        
        time.sleep(0.2)
    
    print()
    print("-" * 80)
    print("✅ Director test complete!")
    print(f"   {director.get_progress()}")
    print()


if __name__ == "__main__":
    main()
