import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os", "tkinter", "pandas", "PIL", "ttkthemes", "openpyxl"],
    "include_files": [
        ("config/settings.json", "settings.json"),
        ("assets/icons/app_icon.ico", "app_icon.ico"),
        ("assets/data/work_log.xlsx", "work_log.xlsx"),
        ("assets/data/sessions.json", "sessions.json")
    ],
    "excludes": [
        "curses", "lib2to3", "autocommand", "_distutils_hack",
        "test", "unittest", "pydoc_data", "setuptools",
        "pkg_resources", "distutils"
    ],
    "optimize": 2,  # Apply bytecode optimization
    "include_msvcr": True  # Include Visual C++ runtime
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="WorkTimer",
    version="1.0",
    description="Work Timer Application",
    options={"build_exe": build_exe_options},
    executables=[Executable("src/core/work_timer.py", base=base, icon="assets/icons/app_icon.ico")]
) 