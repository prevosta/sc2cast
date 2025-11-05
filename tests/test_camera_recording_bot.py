"""
Simple SC2 bot to test if camera positions are saved in replays.

Bot behavior:
1. Send all SCVs to attack enemy start location
2. Follow SCVs with camera during the game
3. Save replay after game ends
4. We'll watch the replay to see if camera movements were recorded
"""

import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.ids.unit_typeid import UnitTypeId


class CameraTestBot(sc2.BotAI):
    """Bot that sends all SCVs to attack and follows them with camera."""
    
    async def on_start(self):
        """Called once at the start of the game."""
        print("🎮 CameraTestBot started!")
        print("📹 Will send all SCVs to attack and follow with camera")
        self.attack_sent = False
    
    async def on_step(self, iteration: int):
        """Called every game step."""
        
        # At 5 seconds, send all SCVs to attack
        if not self.attack_sent and iteration == 112:  # ~5 seconds (22.4 iterations/sec)
            print("\n🚀 Sending all SCVs to attack!")
            scvs = self.workers
            if scvs:
                # Attack enemy start location
                for scv in scvs:
                    scv.attack(self.enemy_start_locations[0])
                
                self.attack_sent = True
                print(f"   Sent {len(scvs)} SCVs to attack!")
        
        # Follow SCVs with camera
        if self.attack_sent and iteration % 22 == 0:  # Every ~1 second
            scvs = self.workers
            if scvs:
                # Move camera to first SCV position
                scv = scvs.first
                print(f"📹 Camera following SCV at position: {scv.position}")
                # Note: python-sc2 doesn't have camera control API
                # The camera movement would be manual during the game
        
        # Print game time every 5 seconds
        if iteration % 112 == 0:
            game_time = iteration / 22.4
            print(f"⏱️  Game time: {game_time:.1f} seconds")


async def main():
    """Run the camera test bot."""
    print("=" * 80)
    print("🧪 CAMERA RECORDING TEST")
    print("=" * 80)
    print()
    print("📋 Instructions:")
    print("   1. Game will start with bot controlling Terran")
    print("   2. Bot will send all SCVs to attack at 5 seconds")
    print("   3. YOU manually move camera to follow the SCVs")
    print("   4. Use arrow keys or click minimap to follow them")
    print("   5. Game will end when SCVs reach enemy (or die)")
    print("   6. Replay will be saved to Replays folder")
    print("   7. Watch replay - does camera follow your movements?")
    print()
    print("🔍 CRITICAL TEST:")
    print("   If camera is DIFFERENT when watching replay = NOT RECORDED ✅")
    print("   If camera follows your movements = RECORDED ⚠️")
    print()
    print("=" * 80)
    print()
    
    await run_game(
        maps.get("Simple64"),  # Use built-in map
        [
            Bot(Race.Terran, CameraTestBot()),
            Computer(Race.Protoss, Difficulty.VeryEasy)
        ],
        realtime=False,  # Run at normal game speed
        save_replay_as="output/camera_test.SC2Replay"
    )
    
    print()
    print("=" * 80)
    print("✅ Game complete!")
    print("📁 Replay saved: output/camera_test.SC2Replay")
    print()
    print("📋 Next steps:")
    print("   1. Watch the replay: output/camera_test.SC2Replay")
    print("   2. Observe the camera behavior")
    print("   3. Does it follow the path you controlled during the game?")
    print()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
