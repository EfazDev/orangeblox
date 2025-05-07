from PyInstaller.utils.hooks import collect_data_files
import os
try:
    from PyInstaller.building.api import *
    from PyInstaller.building.build_main import *
    from PyInstaller.building.osx import *
except:
    print("Disabled Visual Studio Code Mode")

block_cipher = None

a = Analysis(
    ["../OrangeBlox.py", "../OrangePlayRoblox.py", "../OrangeRunStudio.py", "../../../PipHandler.py"],
    pathex=[],
    binaries=[],
    datas=collect_data_files("OrangeBlox") + [("../../../Version.json", ".")],
    hiddenimports=[
        "plyer",
        "plyer.platforms",
        "plyer.platforms.win.notification",
        "plyer.platforms.win",
        "ctypes._layout"
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "tkinter"
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
main_exe = EXE(
    pyz,
    [a.scripts[1]],
    a.binaries,
    a.zipfiles,
    a.datas,
    name="OrangeBlox",
    debug=False,
    bootloader_ignore_signals=False,
    argv_emulation=True,
    strip=False,
    console=True,
    upx=True,
    icon="../../../BootstrapImages/AppIcon.ico",
    runtime_tmpdir=None,
    onefile=True
)
play_roblox_exe = EXE(
    pyz,
    [a.scripts[2]],
    a.binaries,
    a.zipfiles,
    a.datas,
    name="PlayRoblox",
    debug=False,
    bootloader_ignore_signals=False,
    argv_emulation=True,
    strip=False,
    console=True,
    upx=True,
    icon="../../../BootstrapImages/AppIconPlayRoblox.ico",
    runtime_tmpdir=None,
    onefile=True
)
run_studio_exe = EXE(
    pyz,
    [a.scripts[3]],
    a.binaries,
    a.zipfiles,
    a.datas,
    name="RunStudio",
    debug=False,
    bootloader_ignore_signals=False,
    argv_emulation=True,
    strip=False,
    console=True,
    upx=True,
    icon="../../../BootstrapImages/AppIconRunStudio.ico",
    runtime_tmpdir=None,
    onefile=True
)
build = [main_exe, play_roblox_exe, run_studio_exe]