import json

data = json.load(open('output/generated_camera_script.json'))

print("=" * 80)
print("EVENT-BASED CAMERA SCRIPT - COMPLETE TIMELINE")
print("=" * 80)
print(f"\nTotal Shots: {data['total_shots']}")
print("\nTimeline with descriptions:\n")

for shot in data['shots']:
    mins = shot['time_seconds'] // 60
    secs = shot['time_seconds'] % 60
    shot_type = shot['shot_type']
    params = shot['params']
    
    # Build description
    if shot_type == 'minimap_jump':
        desc = params.get('description', f"Jump to ({params.get('x')}, {params.get('y')})")
    elif shot_type == 'player_view':
        desc = f"Switch to Player {params.get('player')} perspective"
    elif shot_type == 'stat_panel':
        desc = f"Show {params.get('panel', '?').upper()} comparison panel"
    else:
        desc = str(params)
    
    print(f"  {mins:02d}:{secs:02d} │ {shot_type:15} │ {desc}")

print("\n" + "=" * 80)
print("CAMERA FLOW SUMMARY")
print("=" * 80)
print("""
0:00-0:30  : Opening - Introduce both players
2:00-4:00  : Player 1 overview
4:00-4:45  : Track small skirmishes (4 battles)
5:08       : Player 2 check-in
5:36-5:39  : ⚔️  MAJOR BATTLE (115, 123) + army stats
6:14-6:46  : Player 1 overview  
6:46-7:18  : Track late-game battles
7:35-7:50  : Player 2 overview
7:50+      : Final battle coverage
""")

print("✅ Camera will automatically follow all action!")
print("🎬 Ready for full recording pipeline integration!")
