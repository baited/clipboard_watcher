import sys

from cx_Freeze import Executable, setup

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": [
    "pyperclip", "urlextract"], "excludes": ["tkinter"]}

# base="Win32GUI" should be used only for Windows GUI app
base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

shortcut_table = [
    (
        "DesktopShortcut",         # Shortcut
        "DesktopFolder",           # Directory_
        "Clipboard Watcher",       # Name
        "TARGETDIR",               # Component_
        "[TARGETDIR]clipper.exe",  # Target
        None,                      # Arguments
        None,                      # Description
        None,                      # Hotkey
        'icon.ico',                # Icon
        1,                         # IconIndex
        None,                      # ShowCmd
        'TARGETDIR'                # WkDir
    ),
]

msi_data = {"Shortcut": shortcut_table}

bdist_msi_options = {
    'add_to_path': True,
    'data': msi_data
}

setup(
    name="clipboard watcher",
    version="0.1",
    description="watches the clipboard",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options
    },
    executables=[Executable("clipper.py", base=base, icon="icon.ico")],
)
