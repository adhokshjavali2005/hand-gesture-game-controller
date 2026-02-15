"""
build_exe.py

Script to build standalone executable using PyInstaller.
Run this script to create the .exe file.
"""

import subprocess
import sys
import os

def build():
    """Build the executable using PyInstaller."""
    
    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=HandGestureController",
        "--onefile",  # Single executable
        "--windowed",  # No console window (use --console for debugging)
        "--icon=NONE",  # Add icon later if needed
        "--add-data=hand_landmarker.task;.",  # Include the MediaPipe model
        "--hidden-import=mediapipe",
        "--hidden-import=mediapipe.tasks",
        "--hidden-import=mediapipe.tasks.python",
        "--hidden-import=mediapipe.tasks.python.vision",
        "--hidden-import=cv2",
        "--hidden-import=numpy",
        "--hidden-import=pyautogui",
        "--hidden-import=sklearn",
        "--hidden-import=joblib",
        "--collect-all=mediapipe",
        "--collect-all=cv2",
        "main.py"
    ]
    
    print("Building executable...")
    print(f"Command: {' '.join(cmd)}")
    print()
    
    # Run PyInstaller
    result = subprocess.run(cmd, cwd=os.path.dirname(os.path.abspath(__file__)))
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("BUILD SUCCESSFUL!")
        print("=" * 60)
        print()
        print("Executable location:")
        print("  dist/HandGestureController.exe")
        print()
        print("To distribute:")
        print("  1. Copy 'dist/HandGestureController.exe' to target machine")
        print("  2. The .exe includes all dependencies")
        print("  3. No Python installation needed on target machine")
        print()
    else:
        print()
        print("BUILD FAILED! Check errors above.")
        
    return result.returncode

if __name__ == "__main__":
    sys.exit(build())
