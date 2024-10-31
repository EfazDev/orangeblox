from PyInstaller.utils.hooks import collect_data_files
import os

icon_file = "../AppIcon.icns"
current_version = {"version": "1.3.1"}

main_plist = {
    "CFBundleExecutable": "EfazRobloxBootstrap",
    "CFBundleIdentifier": "dev.efaz.robloxbootstrap",
    "CFBundleURLTypes": [],
    "CFBundleName": "EfazRobloxBootstrap",
    "CFBundleDisplayName": "Efaz's Roblox Bootstrap",
    "CFBundleVersion": current_version["version"],
    "LSMinimumSystemVersion": "10.9",
    "CFBundleIconFile": "AppIcon.icns",
    "CFBundleShortVersionString": current_version["version"],
    "CFBundleSignature": "????",
    "LSApplicationCategoryType": "public.app-category.utilities",
    "LSMultipleInstancesProhibited": False,
    "NSAppSleepDisabled": True,
}
loader_plist = {
    "CFBundleExecutable": "EfazRobloxBootstrapLoad",
    "CFBundleIdentifier": "dev.efaz.robloxbootstrap",
    "CFBundleURLTypes": [
        {
            "CFBundleTypeRole": "Viewer",
            "CFBundleURLName": "ReplicateRobloxPlayer",
            "CFBundleURLSchemes": ["roblox-player", "roblox", "efaz-bootstrap"],
        }
    ],
    "CFBundleName": "EfazRobloxBootstrapLoad",
    "CFBundleDisplayName": "Load Efaz's Roblox Bootstrap",
    "CFBundleVersion": current_version["version"],
    "CFBundleDevelopmentRegion": "en-US",
    "LSMinimumSystemVersion": "10.9",
    "CFBundleIconFile": "AppIcon.icns",
    "CFBundleShortVersionString": current_version["version"],
    "CFBundleSignature": "????",
    "LSApplicationCategoryType": "public.app-category.utilities",
    "LSMultipleInstancesProhibited": False,
    "NSAppSleepDisabled": True,
}
block_cipher = None

a = Analysis(
    ["../EfazRobloxBootstrap.py", "../EfazRobloxBootstrapLoad.py", "../PipHandler.py"],
    pathex=[],
    binaries=[],
    datas=collect_data_files("EfazRobloxBootstrap"),
    hiddenimports=["sys", "subprocess", "json", "threading", "os", "platform", "time", "traceback", "importlib", "glob", "tempfile", "pyobjc", "subprocess"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter", "unittest", "email", "matplotlib"],
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
    name="EfazRobloxBootstrap",
    debug=False,
    bootloader_ignore_signals=False,
    argv_emulation=True,
    strip=False,
    target_arch="universal2",
    console=False,
    upx=True,
    icon=os.path.join(os.getcwd(), icon_file),
)
loader_exe = EXE(
    pyz,
    [a.scripts[2]],
    exclude_binaries=True,
    name="EfazRobloxBootstrapLoad",
    debug=False,
    bootloader_ignore_signals=False,
    argv_emulation=True,
    strip=False,
    target_arch="universal2",
    upx=True,
    console=False,
    icon=os.path.join(os.getcwd(), icon_file),
)
main_collect = COLLECT(
    main_exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="EfazRobloxBootstrap",
    distpath='Apps',
)
loader_collect = COLLECT(
    loader_exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="EfazRobloxBootstrapLoad",
    distpath='Apps',
)
main_app = BUNDLE(
    main_collect,
    name="EfazRobloxBootstrap.app",
    icon=icon_file,
    bundle_identifier=main_plist["CFBundleIdentifier"],
    info_plist=main_plist,
    distpath='Apps',
    codesign_identity=None
)
loader_app = BUNDLE(
    loader_collect,
    name="EfazRobloxBootstrapLoad.app",
    icon=icon_file,
    bundle_identifier=loader_plist["CFBundleIdentifier"],
    info_plist=loader_plist,
    distpath='Apps',
    codesign_identity=None
)