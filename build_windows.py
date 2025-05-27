import os
import sys
import subprocess

def build_windows_exe():
    """Build Windows executable using PyInstaller"""
    print("Building Windows executable...")
    
    # Install PyInstaller if not already installed
    subprocess.call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Build the executable
    subprocess.call([
        "pyinstaller",
        "--name=PodcastStudioEnhancer",
        "--windowed",
        "--onefile",
        "--icon=assets/logo/podcast-studio-enhencer-logo.ico",
        "--add-data=assets/logo/podcast-studio-enhencer-logo.png:assets/logo",
        "--hidden-import=scipy.signal",
        "--hidden-import=librosa",
        "--hidden-import=noisereduce",
        "--hidden-import=soundfile",
        "--hidden-import=PIL",
        "main.py"
    ])
    
    print("Windows build complete!")
    print("Executable can be found in the 'dist' folder")

if __name__ == "__main__":
    build_windows_exe()
