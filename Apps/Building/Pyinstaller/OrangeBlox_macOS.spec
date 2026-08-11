from PyInstaller.utils.hooks import collect_data_files
import os
try:
    from PyInstaller.building.api import *
    from PyInstaller.building.build_main import *
    from PyInstaller.building.osx import *
except:
    print("Disabled Visual Studio Code Mode")

icon_file = "../../../Images/AppIcon.icns"
current_version = {"version": "2.6.0l"}
main_plist = {
    "CFBundleDevelopmentRegion": "en-US",
    "CFBundleDisplayName": "OrangeBlox",
    "CFBundleExecutable": "OrangeBlox",
    "CFBundleIconFile": "AppIcon.icns",
    "CFBundleIdentifier": "dev.efaz.orangeblox",
    "CFBundleInfoDictionaryVersion": "6.0",
    "CFBundleName": "OrangeBlox",
    "CFBundlePackageType": "APPL",
    "CFBundleShortVersionString": current_version["version"],
    "CFBundleURLTypes": [
        {
            "CFBundleTypeRole": "Viewer",
            "CFBundleURLName": "ReplicateRobloxPlayer",
            "CFBundleURLSchemes": [
                "roblox-player",
                "roblox-studio",
                "roblox-studio-auth",
                "roblox"
            ]
        },
        {
            "CFBundleTypeRole": "Viewer",
            "CFBundleURLName": "BootstrapURLScheme",
            "CFBundleURLSchemes": [
                "efaz-bootstrap",
                "orangeblox"
            ]
        }
    ],
    "CFBundleDocumentTypes": [
        {
            "CFBundleTypeIconSystemGenerated": 1,
            "CFBundleTypeName": "Roblox Place",
            "CFBundleTypeRole": "Editor",
            "LSHandlerRank": "Owner",
            "LSItemContentTypes": [
                "com.Roblox.RobloxStudio-document"
            ],
            "CFBundleTypeExtensions": [
                "rbxl",
                "rbxlx"
            ]
        },
        {
            "CFBundleTypeIconSystemGenerated": 1,
            "CFBundleTypeName": "OrangeBlox File",
            "CFBundleTypeRole": "Editor",
            "LSHandlerRank": "Owner",
            "LSItemContentTypes": [
                "dev.efaz.orangeblox.filetype"
            ],
            "CFBundleTypeExtensions": [
                "obx"
            ]
        }
    ],
    "UTExportedTypeDeclarations": [
        {
            "UTTypeConformsTo": [
                "public.data"
            ],
            "UTTypeDescription": "Roblox Place",
            "UTTypeIconFile": "",
            "UTTypeIcons": {
                "UTTypeIconText": ""
            },
            "UTTypeIdentifier": "com.Roblox.RobloxStudio-document",
            "UTTypeTagSpecification": {
                "public.filename-extension": [
                    "rbxl",
                    "rbxlx"
                ]
            }
        },
        {
            "UTTypeConformsTo": [
                "public.data"
            ],
            "UTTypeDescription": "OrangeBlox File",
            "UTTypeIconFile": "",
            "UTTypeIcons": {
                "UTTypeIconText": ""
            },
            "UTTypeIdentifier": "dev.efaz.orangeblox.filetype",
            "UTTypeTagSpecification": {
                "public.filename-extension": [
                    "obx"
                ]
            }
        }
    ],
    "CFBundleVersion": current_version["version"],
    "LSApplicationCategoryType": "public.app-category.utilities",
    "LSMinimumSystemVersion": "10.15",
    "LSMultipleInstancesProhibited": True,
    "NSSupportsSuddenTermination": False,
    "NSAppSleepDisabled": True,
    "NSHighResolutionCapable": True
}
block_cipher = None

main_analysis = Analysis(
    ["../OrangeBlox.py", "../../../PyKits.py"],
    pathex=[],
    binaries=[],
    datas=collect_data_files("OrangeBlox") + [("../../../Version.json", ".")],
    hiddenimports=["Quartz", "AppKit", "Foundation", "truststore"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["cryptography", "OpenSSL", "urllib3", "requests", "plyer", "site", "certifi", "setuptools"],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

main_pyz = PYZ(main_analysis.pure, main_analysis.zipped_data, cipher=block_cipher)
main_script = next(s for s in main_analysis.scripts if s[0] == "OrangeBlox")

main_exe = EXE(
    main_pyz,
    [main_script],
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
    distpath="Apps/Building",
)
main_app = BUNDLE(
    main_collect,
    name="OrangeBlox.app",
    icon=icon_file,
    bundle_identifier=main_plist["CFBundleIdentifier"],
    info_plist=main_plist,
    distpath="Apps/Building",
    codesign_identity="-"
)