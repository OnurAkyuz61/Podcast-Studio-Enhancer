import os
import sys
import subprocess

def build_macos_app():
    """Build macOS application using PyInstaller"""
    print("Building macOS application...")
    
    # Install PyInstaller if not already installed
    subprocess.call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Build the application
    subprocess.call([
        "pyinstaller",
        "--name=PodcastStudioEnhancer",
        "--windowed",
        "--onefile",
        "--icon=assets/logo/podcast-studio-enhencer-logo.icns",
        "--add-data=assets/logo/podcast-studio-enhencer-logo.png:assets/logo",
        "--hidden-import=scipy.signal",
        "--hidden-import=librosa",
        "--hidden-import=noisereduce",
        "--hidden-import=soundfile",
        "--hidden-import=PIL",
        "main.py"
    ])
    
    print("macOS build complete!")
    print("Application can be found in the 'dist' folder")

if __name__ == "__main__":
    build_macos_app()
