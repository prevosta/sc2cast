"""
SC2 Replay Observer Hotkeys Controller.

All hotkeys for controlling stats panels, camera, and UI during replay observation.
Source: https://liquipedia.net/starcraft2/Hotkeys
"""

import pyautogui
import time
from enum import Enum
from typing import Optional


class StatPanel(Enum):
    """Available statistics comparison panels."""
    ARMY_VALUE = 'A'           # Compare total mineral, gas and population cost of fightable units
    PRODUCTION = 'D'           # Compare units being produced, buildings being built, tech being researched
    INCOME = 'I'              # Compare mineral/gas gathered per minute and worker count
    UNITS_LOST = 'L'          # Compare lost units and their costs
    APM = 'M'                 # Compare Actions Per Minute
    EPM = 'shift+C'           # Compare Effective actions Per Minute
    RESOURCES = 'R'           # Compare current mineral, gas and population
    SPENDING = 'S'            # Compare resources spent on tech and units
    UNITS = 'U'               # Compare all units
    BUILDINGS = 'T'           # Compare all structures
    UPGRADES = 'G'            # Compare upgrades
    CLOSE_PANEL = 'N'         # Close compare window


class UIPanel(Enum):
    """Toggle-able UI panels (Ctrl + key)."""
    NAME_PANEL = 'ctrl+n'              # Toggle 1v1 Name Panel
    RESOURCES_PANEL = 'ctrl+i'         # Toggle 1v1 Resource Compare Panel
    ARMY_SUPPLY_PANEL = 'ctrl+a'       # Toggle 1v1 Army/Worker Supply Compare Panel
    UNITS_KILLED_PANEL = 'ctrl+r'      # Toggle 1v1 Unit/Worker Killed Compare Panel
    APM_PANEL = 'ctrl+v'               # Toggle 1v1 APM Compare Panel
    HIDE_ALL_UI = 'ctrl+w'             # Toggle UI (Command Card/Minimap/etc.)


class ObserverHotkeys:
    """Controller for SC2 replay observer mode hotkeys."""
    
    def __init__(self):
        """Initialize observer hotkey controller."""
        self.current_player = 1
    
    # Camera Controls
    
    def switch_to_player(self, player_num: int):
        """
        Switch camera to player perspective (F1-F8).
        
        Args:
            player_num: Player number (1-8)
        """
        if 1 <= player_num <= 8:
            pyautogui.press(f'f{player_num}')
            self.current_player = player_num
            print(f"📹 Switched to Player {player_num}")
    
    def show_pov(self):
        """Show POV (Point of View) of current player."""
        pyautogui.press('c')
        print(f"👁️ Showing POV of Player {self.current_player}")
    
    def show_all_vision(self):
        """Show vision of all players."""
        pyautogui.press('e')
        print("👁️ Showing vision of all players")
    
    def toggle_hp_bars(self):
        """Show/hide HP bars."""
        pyautogui.press('h')
        print("💚 Toggled HP bars")
    
    def follow_unit(self, hold: bool = False):
        """
        Follow selected unit with camera.
        
        Args:
            hold: If True, use Ctrl+F (hold to follow). If False, use Ctrl+Shift+F (continuous follow)
        """
        if hold:
            # Note: This requires holding the key, which is harder to automate
            pyautogui.hotkey('ctrl', 'f')
            print("📹 Hold Ctrl+F to follow selected unit")
        else:
            pyautogui.hotkey('ctrl', 'shift', 'f')
            print("📹 Continuous follow mode enabled")
    
    def rotate_camera(self, clockwise: bool = True):
        """
        Rotate camera.
        
        Args:
            clockwise: True for CW (Insert), False for CCW (Delete)
        """
        if clockwise:
            pyautogui.press('insert')
            print("🔄 Rotating camera clockwise")
        else:
            pyautogui.press('delete')
            print("🔄 Rotating camera counter-clockwise")
    
    def view_unit_vision(self):
        """Limit vision to selected unit's owner (hold V to view)."""
        pyautogui.press('v')
        print("👁️ Viewing selected unit's vision (hold V)")
    
    # Stats Panels
    
    def show_stat_panel(self, panel: StatPanel):
        """
        Show a statistics comparison panel.
        
        Args:
            panel: StatPanel enum value
        """
        if panel == StatPanel.EPM:
            pyautogui.hotkey('shift', 'c')
        else:
            pyautogui.press(panel.value.lower())
        
        panel_names = {
            StatPanel.ARMY_VALUE: "Army Value",
            StatPanel.PRODUCTION: "Production",
            StatPanel.INCOME: "Income",
            StatPanel.UNITS_LOST: "Units Lost",
            StatPanel.APM: "APM",
            StatPanel.EPM: "EPM",
            StatPanel.RESOURCES: "Resources",
            StatPanel.SPENDING: "Spending",
            StatPanel.UNITS: "Units",
            StatPanel.BUILDINGS: "Buildings",
            StatPanel.UPGRADES: "Upgrades",
            StatPanel.CLOSE_PANEL: "Close Panel",
        }
        print(f"📊 Showing: {panel_names[panel]}")
    
    def close_stat_panel(self):
        """Close the current stats panel."""
        self.show_stat_panel(StatPanel.CLOSE_PANEL)
    
    # UI Panels
    
    def toggle_ui_panel(self, panel: UIPanel):
        """
        Toggle a UI panel.
        
        Args:
            panel: UIPanel enum value
        """
        keys = panel.value.split('+')
        pyautogui.hotkey(*keys)
        
        panel_names = {
            UIPanel.NAME_PANEL: "Name Panel",
            UIPanel.RESOURCES_PANEL: "Resources Panel",
            UIPanel.ARMY_SUPPLY_PANEL: "Army/Supply Panel",
            UIPanel.UNITS_KILLED_PANEL: "Units Killed Panel",
            UIPanel.APM_PANEL: "APM Panel",
            UIPanel.HIDE_ALL_UI: "All UI",
        }
        print(f"🎛️ Toggled: {panel_names[panel]}")
    
    # Playback Controls
    
    def pause(self):
        """Pause/resume replay."""
        pyautogui.press('p')
        print("⏸️ Pause/Resume")
    
    def speed_up(self):
        """Increase playback speed."""
        pyautogui.press('+')
        print("⏩ Speed increased")
    
    def slow_down(self):
        """Decrease playback speed."""
        pyautogui.press('-')
        print("⏪ Speed decreased")


def main():
    """Test observer hotkeys."""
    import subprocess
    from pathlib import Path
    
    print("🎮 SC2 OBSERVER HOTKEYS TEST")
    print("=" * 80)
    print()
    
    # Initialize controller
    obs = ObserverHotkeys()
    
    # Launch replay
    replay_path = Path("replays/4323200_changeling_Mike_MagannathaAIE_v2.SC2Replay")
    print("🚀 Launching replay...")
    subprocess.Popen([str(replay_path.absolute())], shell=True)
    
    print("⏳ Waiting 35 seconds for replay to start...")
    time.sleep(35)
    
    print()
    print("🧪 Testing hotkeys...")
    print("-" * 80)
    
    # Test camera switches
    obs.switch_to_player(1)
    time.sleep(2)
    
    obs.switch_to_player(2)
    time.sleep(2)
    
    # Test stats panels
    obs.show_stat_panel(StatPanel.RESOURCES)
    time.sleep(2)
    
    obs.show_stat_panel(StatPanel.ARMY_VALUE)
    time.sleep(2)
    
    obs.show_stat_panel(StatPanel.INCOME)
    time.sleep(2)
    
    obs.close_stat_panel()
    time.sleep(1)
    
    # Test UI panels
    obs.toggle_ui_panel(UIPanel.RESOURCES_PANEL)
    time.sleep(2)
    
    obs.toggle_ui_panel(UIPanel.RESOURCES_PANEL)  # Toggle off
    time.sleep(1)
    
    obs.toggle_hp_bars()
    time.sleep(2)
    
    print()
    print("-" * 80)
    print("✅ Hotkey test complete!")
    print()
    print("📋 Available hotkeys documented in ObserverHotkeys class")
    print()


if __name__ == "__main__":
    main()
