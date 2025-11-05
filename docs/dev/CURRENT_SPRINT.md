# Sprint 2.1: Live Camera Director System

**Goal:** Build automated camera director that controls replay playback in real-time  
**Started:** November 6, 2025  
**Status:** ✅ COMPLETE

---

## 🎉 SPRINT 2.1 COMPLETE!

All tasks finished successfully! The complete automated recording pipeline is now working:
- ✅ Launches replay and waits 30s for loading
- ✅ Detects replay start via OCR (3-frame validation)
- ✅ Sets playback speed (Fast x4 = 8x speed)
- ✅ Records with FFmpeg while executing camera script
- ✅ 15 camera shots execute perfectly (camera switching + stat panels)
- ✅ Detects replay end and stops recording
- ✅ Automatically closes SC2_x64.exe
- ✅ Produces complete, working video files!

**Key Achievement:** Full end-to-end automation from replay file to finished video! 🎬

---

## 🎯 Objective

Create a camera director system that:
1. Launches replay and waits for loading
2. **Detects replay start via OCR** (when timer appears, e.g. "0:00")
3. Uses timestamp correlation (real time = game time at normal speed)
4. Validates sync periodically (every 10-15 seconds) via OCR
5. **Detects replay end via OCR** (when timer stops or reaches end time)
6. Makes intelligent camera decisions
7. Controls camera via hotkeys and minimap
8. Records full-length video with FFmpeg

**Success = Full automated replay video with dynamic camera control!**

---

## 📋 Tasks

- [x] **Task 1:** Camera Director Architecture ✅
  - Design camera decision algorithm
  - Define camera shot types (player view, minimap jump, follow unit)
  - Create timeline/script format for camera cues
  - Deliverable: `src/sc2cast/camera_director.py` skeleton
  - **STATUS:** Complete - full implementation with shot types and script execution

- [x] **Task 2:** Timer Synchronization & Game Clock ✅
  - **Start Detection:** Poll OCR until timer appears (not "0:00" yet = loading)
  - **Start Time:** When OCR reads "0:00" or first valid time → recording starts
  - **Primary Sync:** Timestamp correlation (start_time + elapsed = game_time)
  - **Periodic Validation:** OCR every 10-15 seconds to detect drift/pause
  - **End Detection:** OCR detects timer stopped or reached final time (9:28)
  - At normal speed ("Faster"): 1:1 real time = game time
  - Deliverable: Game clock with OCR-based start/end detection
  - **STATUS:** Complete - full implementation with auto-recalibration

- [x] **Task 3:** Basic Camera Script ✅
  - Create simple camera script for demo replay
  - Example: "0:30 - Player 1, 1:00 - Player 2, 1:30 - Center"
  - Execute script synchronized with game time
  - Deliverable: Working scripted camera control
  - **STATUS:** Complete - 15 camera shots execute perfectly! Camera switching (1, 2 keys) and stat panels (A, D, I) all working!

- [x] **Task 4:** Integrated Recording Pipeline ✅
  - Launch replay → Wait for loading → Start FFmpeg
  - Run camera director during recording
  - Monitor game timer throughout
  - Stop recording at replay end
  - Deliverable: End-to-end automated recording
  - **STATUS:** Complete - full pipeline implemented with multiple speed support

- [x] **Task 5:** Full Replay Recording Test ✅
  - Record entire 5:10 demo replay
  - Execute full camera script
  - Verify video quality and synchronization
  - Deliverable: Complete automated replay video!
  - **STATUS:** Complete - Full end-to-end automation working!

---

## 📦 Deliverables

- `src/sc2cast/camera_director.py` - Main camera director system
- `src/sc2cast/game_clock.py` - Game time synchronization with OCR validation
- `src/sc2cast/recording_pipeline.py` - End-to-end recording automation
- `output/automated_replay_full.mp4` - Complete automated video
- Camera script format/examples

---

## 🎯 Success Criteria

- ✅ Camera director runs autonomously during replay
- ✅ Game timer synchronization accurate within ±2 seconds
- ✅ Camera changes execute at correct times (number keys 1, 2 for camera switching)
- ✅ Full 5:10 replay recorded to MP4 at 8x speed
- ✅ Video plays smoothly with proper camera work and stat overlays
- ✅ **Can generate automated videos without manual intervention!**

---

## 🔧 Technical Solutions Implemented

**Key Fixes:**
1. **Duration**: Corrected to 5:10 (310s) for demo replay
2. **Loading Wait**: 30-second delay before OCR starts
3. **OCR Validation**: 3-frame median filtering for reliable timing
4. **Speed Control**: Set AFTER replay starts (3x + presses for Fast x4)
5. **SC2 Process**: Correctly targets SC2_x64.exe (not SC2.exe)
6. **Camera Hotkeys**: Uses number keys (1, 2) instead of F-keys for observer mode
7. **FFmpeg Cleanup**: Proper shutdown with communicate() for valid videos
8. **Camera Script**: All events within replay duration (no events past 5:10)

---

## 📝 Notes

**Key Technical Challenges:**
- SC2 loading time (~30s) must be handled
- OCR errors need validation/filtering
- Camera commands must execute reliably
- FFmpeg must start/stop at right times

**Building Blocks Available:**
- ✅ `timer_reader.py` - OCR timer reading
- ✅ `observer_hotkeys.py` - All SC2 controls
- ✅ `minimap_camera.py` - Minimap navigation
- ✅ `replay_controller.py` - Replay launching
- ✅ FFmpeg screen capture tested

**Camera Shot Types:**
1. Player perspective (F1-F8 or 1-2 hotkeys)
2. Minimap location jump (strategic positions)
3. Follow unit (Ctrl+Shift+F after selection)
4. Stats panel overlay (A, D, I, L, R, etc.)

---

**This sprint turns all Phase 1 components into a working automated system!** 🎥

**Goal:** Load replay with SC2 client and generate 10-second video  
**Started:** November 5, 2025  
**Status:** In Progress

---

## 🚨 CRITICAL RISK

**This sprint tests if the entire project is viable!**

If Windows SC2 client can't play replays programmatically → Need alternative approach

---

## 🎯 Tasks

- [x] **Task 1:** Research python-sc2 library ✅
  - Check if python-sc2 supports replay playback
  - **FINDING:** python-sc2 is for creating AI bots, NOT replay playback
  - **ALTERNATIVE:** Use SC2 client directly + screen capture (FFmpeg/OBS)
  - Created test script to verify replay playback manually

- [x] **Task 2:** Load replay with SC2 client ✅
  - Use python-sc2 or SC2 API
  - Launch SC2 and load the demo replay
  - **SUCCESS:** Replay plays when double-clicked!
  - **CRITICAL MILESTONE ACHIEVED:** Windows SC2 + AIArena replays = WORKS! 🎉

- [x] **Task 3:** Test keyboard automation **NEW CRITICAL TASK** ✅
  - Install pyautogui or pynput library
  - Test sending keyboard inputs to SC2 window
  - Try camera hotkeys (1, 2) during replay
  - **RESULT:** Camera switching works perfectly! (1, 2 keys)
  - **SUCCESS:** Can control camera during replay playback!
  - Tab (stats toggle) may need refinement but not critical
  - 🎉 **CAMERA DIRECTOR IS VIABLE!**

- [x] **Task 4:** Capture screen/video ✅
  - Test FFmpeg screen capture
  - **SOLUTION:** Found FFmpeg in WinGet packages directory
  - Updated test script to auto-detect FFmpeg location
  - Captured 10 seconds successfully (12 MB MP4)
  - **SUCCESS:** Screen capture working perfectly!

- [x] **Task 5:** Generate first video file ✅
  - Record 10-second clip from replay
  - **RESULT:** Test video created and verified
  - Video captures screen correctly
  - Ready to combine with camera automation
  - **SUCCESS CRITERIA MET:** Working video from replay! 🎉

- [x] **Task 6:** Validate camera & hotkey controls ✅
  - **FINDING:** Multiple camera control methods work! ✅
    - Keyboard hotkeys (F1-F8 for players, 1-2 shortcuts)
    - Minimap clicks (x=25, y=810, 267x256)
    - All observer hotkeys documented and tested
  - **RESULT:** Complete control system in:
    - `src/sc2cast/observer_hotkeys.py` - All SC2 observer hotkeys
    - `src/sc2cast/minimap_camera.py` - Minimap-based camera control
  - **BONUS:** Stats panels (A, D, I, L, M, R, S, U, T, G)
  - **BONUS:** UI panels (Ctrl+N, I, A, R, V, W)
  - **NOTE:** Camera recording test deferred (not critical - we control live)

- [x] **Task 7:** Get replay time for synchronization ✅
  - Find way to read current replay time during playback
  - Need for syncing: commentary, stats panels, camera decisions
  - Options tested:
    - ~~SC2 window title/UI detection~~ ❌ Just shows "StarCraft II"
    - **OCR with EasyOCR** ✅ WORKING! ~90% accuracy
  - **SOLUTION:** EasyOCR reading game timer at (1572, 590, 200x25)
  - Cleanup logic handles `:` vs `.` confusion
  - Can filter outliers (e.g. "29:28" instead of "2:42")
  - **RESULT:** Working timer reader in `src/sc2cast/timer_reader.py`
  - **CRITICAL:** SC2 loading takes ~30 seconds before replay starts
  - **SUCCESS:** Can read "3:04" game time reliably! 🎉

---

## 📦 Deliverables

- `src/sc2cast/replay_controller.py` - SC2 replay control module
- `output/test_video.mp4` - 10-second test video
- Proof that Windows SC2 + replay playback + recording works!

---

## 🎯 Success Criteria

- ✅ SC2 client launches and loads replay
- ✅ Can control replay playback programmatically
- ✅ Can capture video footage
- ✅ Generated MP4 file plays correctly
- ✅ **PROJECT IS VIABLE** 🎉

---

## ⚠️ Failure Scenarios

If replay playback doesn't work:
1. Try alternative SC2 API approaches
2. Try replay → game state conversion
3. Consider pre-recorded footage + AI overlay approach
4. **Worst case:** Pivot entire project strategy

---

**This is THE critical test. Let's find out if this works!** 🚀
