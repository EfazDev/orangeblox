from PyInstaller.utils.hooks import collect_data_files
import os
try:
    from PyInstaller.building.api import *
    from PyInstaller.building.build_main import *
    from PyInstaller.building.osx import *
except:
    print("Disabled Visual Studio Code Mode")

icon_file = "../../../BootstrapImages/AppIcon.icns"
current_version = {"version": "2.2.9"}

main_plist = {
    "CFBundleExecutable": "OrangeBlox",
    "CFBundleIdentifier": "dev.efaz.orangeblox",
    "CFBundleURLTypes": [],
    "CFBundleName": "OrangeBlox",
    "CFBundleDisplayName": "OrangeBlox",
    "CFBundleVersion": current_version["version"],
    "LSMinimumSystemVersion": "10.13",
    "CFBundleIconFile": "AppIcon.icns",
    "CFBundleShortVersionString": current_version["version"],
    "CFBundleSignature": "????",
    "LSApplicationCategoryType": "public.app-category.utilities",
    "LSMultipleInstancesProhibited": False,
    "NSAppSleepDisabled": True,
    "NSAppleEventsUsageDescription": "OrangeBlox uses the Terminal to open the bootstrap with a window!",
    "NSUserNotificationUsageDescription": "Enable Notifications for OrangeBlox in order to use Server Location notications!",
    "NSDownloadsFolderUsageDescription": "This may be used to find your installation folder if it was installed inside the Downloads folder!",
    "NSDocumentsFolderUsageDescription": "This may be used to find your installation folder if it was installed inside the Documents folder!",
    "NSDesktopFolderUsageDescription": "This may be used to find your installation folder if it was installed inside the Desktop folder!"
}
block_cipher = None

main_analysis = Analysis(
    ["../OrangeBlox.py", "../../../PyKits.py"],
    pathex=[],
    binaries=[],
    datas=collect_data_files("OrangeBlox") + [("../../../Version.json", ".")],
    hiddenimports=["Quartz", "AppKit", "Foundation"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["cryptography", "OpenSSL", "urllib3", "requests", "plyer"],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

main_pyz = PYZ(main_analysis.pure, main_analysis.zipped_data, cipher=block_cipher)

main_exe = EXE(
    main_pyz,
    [main_analysis.scripts[1]],
    exclude_binaries=True,
    name="OrangeBlox",
    debug=False,
    bootloader_ignore_signals=False,
    argv_emulation=False,
    strip=False,
    target_arch="arm64",
    windowed=True,
    upx=True,
    icon=icon_file,
)
main_collect = COLLECT(
    main_exe,
    main_analysis.binaries,
    main_analysis.zipfiles,
    main_analysis.datas,
    strip=True,
    upx=True,
    upx_exclude=[],
    name="OrangeBlox",
    distpath='Apps/Building',
)
main_app = BUNDLE(
    main_collect,
    name="OrangeBlox.app",
    icon=icon_file,
    bundle_identifier=main_plist["CFBundleIdentifier"],
    info_plist=main_plist,
    distpath="Apps/Building",
    codesign_identity=None
)