from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs
import os
import tempfile
import uuid
try:
    from PyInstaller.building.api import *
    from PyInstaller.building.build_main import *
    from PyInstaller.building.osx import *
except: print("Disabled Visual Studio Code Mode")

block_cipher = None

a = Analysis(
    ["../OrangeBlox.py", "../../../PyKits.py"],
    pathex=[],
    binaries=collect_dynamic_libs("ssl"),
    datas=collect_data_files("OrangeBlox") + [("../../../Version.json", ".")],
    hiddenimports=["plyer.platforms.win.notification"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "tkinter",
        "urllib3", 
        "requests",
        "numpy",
        "site"
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
    console=True,
    upx=True,
    icon="../../../Images/AppIcon.ico",
    version="../../Storage/Version.txt",
    strip=True
)
combined_coll = COLLECT(
    main_exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    upx=True,
    upx_exclude=[],
    name="OrangeBlox",
    strip=True,
    distpath="dist",
)