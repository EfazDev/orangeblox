from PyInstaller.utils.hooks import collect_data_files
import os
import tempfile
import uuid
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
    exclude_binaries=True,
    name="OrangeBlox",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    console=True,
    upx=True,
    icon="../../../BootstrapImages/AppIcon.ico",
    version="../Resources/Version.txt",
    runtime_tmpdir=os.path.join(tempfile.gettempdir(), f"OrangeBlox_{uuid.uuid4().hex}")
)
play_roblox_exe = EXE(
    pyz,
    [a.scripts[2]],
    exclude_binaries=True,
    name="PlayRoblox",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    console=True,
    upx=True,
    icon="../../../BootstrapImages/AppIconPlayRoblox.ico",
    version="../Resources/VersionPlay.txt",
    runtime_tmpdir=os.path.join(tempfile.gettempdir(), f"OrangePlayRoblox_{uuid.uuid4().hex}")
)
run_studio_exe = EXE(
    pyz,
    [a.scripts[3]],
    exclude_binaries=True,
    name="RunStudio",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    console=True,
    upx=True,
    icon="../../../BootstrapImages/AppIconRunStudio.ico",
    version="../Resources/VersionStudio.txt",
    runtime_tmpdir=os.path.join(tempfile.gettempdir(), f"OrangeRunStudio_{uuid.uuid4().hex}")
)
combined_coll = COLLECT(
    main_exe,
    play_roblox_exe,
    run_studio_exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="OrangeBlox",
    distpath="dist",
)