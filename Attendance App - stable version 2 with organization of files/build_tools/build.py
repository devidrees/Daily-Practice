import os
import subprocess
from app_icon import create_icon

def build_executable():
    # First create the icon
    print("Generating application icon...")
    create_icon()
    
    # Build the executable using PyInstaller
    print("Building executable...")
    cmd = [
        'pyinstaller',
        '--noconfirm',
        '--onefile',
        '--windowed',
        '--icon=app_icon.ico',
        '--name=WorkTimer',
        '--add-data=settings.json;.',
        'work_timer.py'
    ]
    
    subprocess.run(cmd)
    
    print("\nBuild complete! The executable can be found in the 'dist' folder.")
    print("You can create a shortcut to WorkTimer.exe and place it anywhere on your system.")

if __name__ == '__main__':
    build_executable() 