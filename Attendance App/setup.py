import sys
import os
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": [
        "tkinter", 
        "ttkthemes",
        "pandas",
        "PIL",
        "openpyxl",
        "json",
        "datetime",
        "numpy",
        "pytz",
        "six",
        "idna",
        "numbers",
        "pkg_resources",
        "logging",
        "threading",
        "queue"
    ],
    "includes": [
        "tkinter.ttk",
        "ttkthemes",
        "PIL._tkinter_finder",
        "tkinter.messagebox"
    ],
    "include_msvcr": True,
    "excludes": [],
    "include_files": [
        "assets/",
        "settings.json",
        "sessions.json",
        "work_log.xlsx",
        (os.path.join(sys.base_prefix, "DLLs", "tcl86t.dll"), "tcl86t.dll"),
        (os.path.join(sys.base_prefix, "DLLs", "tk86t.dll"), "tk86t.dll")
    ]
}

# GUI applications require a different base on Windows
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Shortcut table configuration for MSI
shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "Work Timer",             # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]WorkTimer.exe",   # Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     "TARGETDIR"               # WkDir
     ),
    
    ("StartMenuShortcut",      # Shortcut
     "StartMenuFolder",        # Directory_
     "Work Timer",             # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]WorkTimer.exe",   # Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     "TARGETDIR"               # WkDir
     )
]

# MSI specific options
msi_data = {
    "Shortcut": shortcut_table
}

# Configure bdist_msi options
bdist_msi_options = {
    "data": msi_data,
    "initial_target_dir": r"[ProgramFilesFolder]\Work Timer",
    "add_to_path": True,
    "install_icon": "assets/app_icon.ico",
    "target_name": "WorkTimer_Setup",
    "upgrade_code": "{1c73d728-8f13-4591-b92c-6c94abb31401}"  # Unique identifier for your app
}

setup(
    name="Work Timer",
    version="1.0",
    description="A simple time tracking application",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
    },
    executables=[
        Executable(
            script="src/core/work_timer.py",
            base=base,
            icon="assets/app_icon.ico",
            target_name="WorkTimer.exe",
            shortcut_name="Work Timer",
            shortcut_dir="DesktopFolder"
        )
    ]
) 