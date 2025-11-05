"""Install FFmpeg and test screen capture for SC2 replays."""

import subprocess
import time
from pathlib import Path


def check_ffmpeg():
    """Check if FFmpeg is installed."""
    # First try system PATH
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return "ffmpeg"
    except FileNotFoundError:
        pass
    
    # Try WinGet installation location
    import os
    winget_path = os.path.expandvars(
        r"C:\Users\$USERNAME\AppData\Local\Microsoft\WinGet\Packages"
    )
    
    if os.path.exists(winget_path):
        for root, dirs, files in os.walk(winget_path):
            if "ffmpeg.exe" in files:
                ffmpeg_exe = os.path.join(root, "ffmpeg.exe")
                try:
                    result = subprocess.run(
                        [ffmpeg_exe, "-version"],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode == 0:
                        return ffmpeg_exe
                except:
                    pass
    
    return None


def install_ffmpeg_instructions():
    """Print instructions for installing FFmpeg on Windows."""
    print("\n" + "=" * 60)
    print("FFmpeg Installation Required")
    print("=" * 60)
    print("\n📦 FFmpeg is needed for screen recording")
    print("\n🔧 Installation options:")
    print("\n1. Using Chocolatey (recommended):")
    print("   → Open PowerShell as Administrator")
    print("   → Run: choco install ffmpeg")
    print("\n2. Using Scoop:")
    print("   → Run: scoop install ffmpeg")
    print("\n3. Manual download:")
    print("   → Download from: https://www.gyan.dev/ffmpeg/builds/")
    print("   → Extract and add to PATH")
    print("\n4. Using winget:")
    print("   → Run: winget install ffmpeg")
    print("\n" + "=" * 60)
    print("\n⏸️  Please install FFmpeg and run this script again")
    print("=" * 60)


def test_screen_capture():
    """
    Test FFmpeg screen capture.
    
    This will capture 10 seconds of screen recording as a test.
    """
    print("\n" + "=" * 60)
    print("Sprint 1.4 - Task 4: Screen Capture Test")
    print("=" * 60)
    
    # Check for ffmpeg
    ffmpeg_cmd = check_ffmpeg()
    if not ffmpeg_cmd:
        print("\n❌ FFmpeg not found!")
        install_ffmpeg_instructions()
        return False
    
    print(f"\n✅ FFmpeg found: {ffmpeg_cmd if isinstance(ffmpeg_cmd, str) and len(ffmpeg_cmd) > 20 else 'System PATH'}")
    
    print("\n🎥 Testing FFmpeg screen capture...")
    print("\n📝 SETUP:")
    print("  1. Launch SC2 replay manually")
    print("  2. Let it play for a few seconds")
    print("  3. Come back here and press Enter...")
    
    input()
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "test_capture_10s.mp4"
    
    print(f"\n🎬 Recording 10 seconds to: {output_file}")
    print("   Recording will start in 3 seconds...")
    print("   Make sure SC2 window is visible!")
    time.sleep(3)
    
    # FFmpeg command for Windows screen capture using gdigrab
    # Captures the entire screen at 1920x1080, 30fps, for 10 seconds
    cmd = [
        ffmpeg_cmd if isinstance(ffmpeg_cmd, str) and len(ffmpeg_cmd) > 20 else "ffmpeg",
        "-f", "gdigrab",              # Windows screen capture
        "-framerate", "30",            # 30 fps
        "-video_size", "1920x1080",    # Resolution
        "-i", "desktop",               # Capture entire desktop
        "-t", "10",                    # Duration: 10 seconds
        "-c:v", "libx264",             # H.264 codec
        "-preset", "ultrafast",        # Fast encoding
        "-pix_fmt", "yuv420p",         # Pixel format
        "-y",                          # Overwrite output
        str(output_file)
    ]
    
    try:
        print("\n🔴 RECORDING NOW (10 seconds)...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"\n✅ Recording complete!")
            print(f"📄 File saved: {output_file}")
            print(f"📊 File size: {output_file.stat().st_size / 1024 / 1024:.2f} MB")
            print("\n🎯 Next: Play the video to verify quality")
            print(f"   Run: {output_file}")
            return True
        else:
            print(f"\n❌ Recording failed!")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"\n❌ FFmpeg error: {e}")
        return False


def main():
    """Main test function."""
    print("=" * 60)
    print("Task 4: FFmpeg Screen Capture Setup")
    print("=" * 60)
    
    # Check if FFmpeg is installed
    if not check_ffmpeg():
        print("\n❌ FFmpeg not found!")
        install_ffmpeg_instructions()
        return
    
    print("\n✅ FFmpeg is installed!")
    
    # Run screen capture test
    success = test_screen_capture()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ TASK 4 COMPLETE!")
        print("=" * 60)
        print("\nNext steps:")
        print("  1. Review the test video")
        print("  2. Combine with keyboard automation (Task 3)")
        print("  3. Record full replay with camera control")
        print("  → Sprint 1.4 almost complete!")


if __name__ == "__main__":
    main()
