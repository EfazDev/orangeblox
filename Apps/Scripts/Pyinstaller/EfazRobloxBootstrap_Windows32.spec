from PyInstaller.utils.hooks import collect_data_files
import os
block_cipher = None

a = Analysis(
    ["../EfazRobloxBootstrap.py", "../EfazRobloxBootstrapPlayRoblox.py", "../PipHandler.py"],
    pathex=[],
    binaries=[],
    datas=collect_data_files("EfazRobloxBootstrap"),
    hiddenimports=["pyobjc", "tkinter"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
main_exe = EXE(
    pyz,
    [a.scripts[2]],
    exclude_binaries=True,
    name="EfazRobloxBootstrap32",
    debug=False,
    bootloader_ignore_signals=False,
    argv_emulation=True,
    strip=False,
    console=True,
    upx=True,
    icon=os.path.join(os.getcwd(), "AppIcon.ico"),
)
play_roblox_exe = EXE(
    pyz,
    [a.scripts[3]],
    exclude_binaries=True,
    name="PlayRoblox32",
    debug=False,
    bootloader_ignore_signals=False,
    argv_emulation=True,
    strip=False,
    console=True,
    upx=True,
    icon=os.path.join(os.getcwd(), "AppIcon.ico"),
)
combined_coll = COLLECT(
    main_exe,
    play_roblox_exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="EfazRobloxBootstrap32",
    distpath="dist",
)