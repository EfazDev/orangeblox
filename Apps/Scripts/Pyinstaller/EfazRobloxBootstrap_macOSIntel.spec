from PyInstaller.utils.hooks import collect_data_files
import os
try:
    from PyInstaller.building.api import *
    from PyInstaller.building.build_main import *
    from PyInstaller.building.osx import *
except:
    print("Disabled Visual Studio Code Mode")

icon_file = "../AppIcon.icns"
current_version = {"version": "1.4.3"}

main_plist = {
    "CFBundleExecutable": "EfazRobloxBootstrapMain",
    "CFBundleIdentifier": "dev.efaz.robloxbootstrap",
    "CFBundleURLTypes": [],
    "CFBundleName": "Efaz's Roblox Bootstrap",
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
    "CFBundleIdentifier": "dev.efaz.robloxbootstrap.loader",
    "CFBundleURLTypes": [
        {
            "CFBundleTypeRole": "Viewer",
            "CFBundleURLName": "ReplicateRobloxPlayer",
            "CFBundleURLSchemes": ["roblox-player", "roblox"],
        },
        {
            "CFBundleTypeRole": "Viewer",
            "CFBundleURLName": "BootstrapURLScheme",
            "CFBundleURLSchemes": ["efaz-bootstrap"],
        }
    ],
    "CFBundleName": "Efaz's Roblox Bootstrap",
    "CFBundleDisplayName": "Efaz's Roblox Bootstrap",
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

main_analysis = Analysis(
    ["../EfazRobloxBootstrap.py", "../PipHandler.py"],
    pathex=[],
    binaries=[],
    datas=collect_data_files("EfazRobloxBootstrapMain") + [("../../../GeneratedHash.json", ".")],
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
loader_analysis = Analysis(
    ["../EfazRobloxBootstrapLoad.py"],
    pathex=[],
    binaries=[],
    datas=collect_data_files("EfazRobloxBootstrapLoad"),
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["pyobjc", "tkinter"],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

main_pyz = PYZ(main_analysis.pure, main_analysis.zipped_data, cipher=block_cipher)
loader_pyz = PYZ(loader_analysis.pure, loader_analysis.zipped_data, cipher=block_cipher)

main_exe = EXE(
    main_pyz,
    [main_analysis.scripts[2]],
    exclude_binaries=True,
    name="EfazRobloxBootstrapMain",
    debug=False,
    bootloader_ignore_signals=False,
    argv_emulation=False,
    strip=False,
    target_arch="x86_64",
    windowed=True,
    upx=True,
    icon=os.path.join(os.getcwd(), icon_file),
)
loader_exe = EXE(
    loader_pyz,
    [loader_analysis.scripts[1]],
    exclude_binaries=True,
    name="EfazRobloxBootstrapLoad",
    debug=False,
    bootloader_ignore_signals=False,
    argv_emulation=True,
    strip=False,
    target_arch="x86_64",
    upx=True,
    console=False,
    icon=os.path.join(os.getcwd(), icon_file),
)
main_collect = COLLECT(
    main_exe,
    main_analysis.binaries,
    main_analysis.zipfiles,
    main_analysis.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="EfazRobloxBootstrapMain",
    distpath='Apps',
)
loader_collect = COLLECT(
    loader_exe,
    loader_analysis.binaries,
    loader_analysis.zipfiles,
    loader_analysis.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="EfazRobloxBootstrapLoad",
    distpath="Apps",
)
main_app = BUNDLE(
    main_collect,
    name="EfazRobloxBootstrapMain.app",
    icon=icon_file,
    bundle_identifier=main_plist["CFBundleIdentifier"],
    info_plist=main_plist,
    distpath="Apps",
    codesign_identity=None
)
loader_app = BUNDLE(
    loader_collect,
    name="EfazRobloxBootstrapLoad.app",
    icon=icon_file,
    bundle_identifier=loader_plist["CFBundleIdentifier"],
    info_plist=loader_plist,
    distpath="Apps",
    codesign_identity=None
)