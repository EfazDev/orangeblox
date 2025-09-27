"""
OrangeBlox Nuitka Rebuild Module

Contains metadata and commands for rebuilding OrangeBlox!
"""

# Modules
import os
import shutil

# Commands
PRINT = 0
RUN = 1
LOOP = 2
FUNCTION = 3
CD = 4
RESET_CD = 5
SET_VAR = 6
MAKE_DIR = 7
RM_DIR = 8
MOVE = 9
RM = 10

# Run Types
REGULAR = 1
PYTHON = 2
PYINSTALLER = 3
NUITKA = 4
CLANGPLUSPLUS = 5

args = ()
variables = {}
cur_path = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../", "../", "../"))
cwd = cur_path
prefix_print = "Rebuild OrangeBlox @ "
current_version = {"version": "2.3.1b"}

split_vers = current_version["version"].split(".")
letter_version = None
if len(split_vers[2]) > 1:
    letter_version = split_vers[2][1:]
    split_vers[2] = split_vers[2][:-1]
    formatted_version = f"{split_vers[0]}.{split_vers[1]}.{split_vers[2]}.{ord(letter_version)}"
else:
    formatted_version = f"{split_vers[0]}.{split_vers[1]}.{split_vers[2]}.0"

def init(*argv):
    global args
    args = argv
def getArg(num, default=None):
    if len(args) > num: return args[num]
    return default
def generate_script_hash():
    return [
        [PRINT, "Generating Script Hashes.."],
        [RUN, PYTHON, ["./Apps/Scripts/UpdateVersion.py"]]
    ]
def macos_clean_up():
    return [
        [PRINT, "Partial Cleaning.."],
        [RM_DIR, "./build/"],
        [PRINT, "Cleaning Up.."],
        [RUN, REGULAR, ["/bin/rm", "-rf", "./Apps/Building/OrangeBlox.app/", "./Apps/Building/OrangeBlox/", "./Apps/OrangeBloxMac/", "./__pycache__/"]],
    ]
def macos_codesign(): 
    return 4, [
        [RUN, REGULAR, ["/bin/rm", "-rf", "./Apps/Building/OrangeBlox.app/Contents/_CodeSignature/"]],
        [RUN, REGULAR, ["/usr/bin/xattr", "-dr", "com.apple.metadata:_kMDItemUserTags", "./Apps/Building/OrangeBlox.app"]],
        [RUN, REGULAR, ["/usr/bin/xattr", "-dr", "com.apple.FinderInfo", "./Apps/Building/OrangeBlox.app"]],
        [RUN, REGULAR, ["/usr/bin/xattr", "-cr", "./Apps/Building/OrangeBlox.app"]],
        [RUN, REGULAR, ["/usr/bin/codesign", "-s", getArg(0, "-"), "--force", "--all-architectures", "--timestamp", "--deep", "./Apps/Building/OrangeBlox.app", "--entitlements", "./Apps/Storage/Entitlements.plist"]]
    ]
def windows_rebuild():
    s = []
    if shutil.which("signtool"):
        signtool = shutil.which("signtool")
        s = [
            [PRINT, "Signing Pyinstaller Package.."],
            [RUN, REGULAR, [signtool, "sign", "/a", "/fd", "SHA256", "/tr", "http://timestamp.digicert.com", "/td", "SHA256", os.path.join(variables["building_dir"], "OrangeBloxWindows", variables["arch"], "OrangeBlox.exe")]],
        ]
    powershell = shutil.which("powershell")
    return [
        [FUNCTION, generate_script_hash],
        [PRINT, "Building Nuitka Package.."],
        [RUN, NUITKA, [
            "--standalone",
            "--windows-console-mode=force",
            "--onefile",
            "--assume-yes-for-downloads",
            "--remove-output",
            "--enable-plugin=pylint-warnings",
            "--nofollow-import-to=unittest,test,distutils,setuptools,tkinter,urllib3,requests,numpy,site",
            "--include-data-files=PyKits.py=PyKits.py",
            "--include-data-files=Version.json=Version.json",
            "--msvc=latest",
            "--company-name=EfazDev",
            "--product-name=OrangeBlox",
            f"--file-version={formatted_version}",
            f"--product-version={formatted_version}",
            "--file-description=OrangeBlox",
            '--copyright="Copyright (c) EfazDev"',
            "--output-dir=Apps/Building",
            "--windows-icon-from-ico=./Images/AppIcon.ico",
            "--target=OrangeBlox",
            "./Apps/Scripts/OrangeBlox.py"
        ]],
        [MAKE_DIR, os.path.join(variables["building_dir"], "OrangeBloxWindows")],
        [MAKE_DIR, os.path.join(variables["building_dir"], "OrangeBloxWindows", variables["arch"])],
        [MOVE, os.path.join(variables["building_dir"], "OrangeBlox.exe"), os.path.join(variables["building_dir"], "OrangeBloxWindows", variables["arch"], "OrangeBlox.exe")]
    ] + s + [
        [PRINT, "Compressing Package.."],
        [RUN, REGULAR, [powershell, "Compress-Archive", "-Path", os.path.join(variables["building_dir"], "OrangeBloxWindows", "*"), "-Update", "-DestinationPath", os.path.join(cur_path, "Apps", "OrangeBloxWindows.zip")]],
        [PRINT, "Cleaning up.."],
        [RM_DIR, os.path.join(variables["building_dir"], "OrangeBloxWindows")],
        [RM_DIR, os.path.join(cur_path, "__pycache__")],
        [RM_DIR, os.path.join(variables["building_dir"], "OrangeBlox.build")],
        [RM_DIR, os.path.join(variables["building_dir"], "OrangeBlox.dist")],
        [RM_DIR, os.path.join(variables["building_dir"], "OrangeBlox.onefile-build")],
        [RM_DIR, os.path.join(variables["building_dir"], "OrangeBlox")],
        [RM_DIR, os.path.join(cur_path, "build")],
        [RM_DIR, os.path.join(cur_path, "Apps", "Scripts", "Nuitka", "__pycache__")]
    ]
macos = {
    "intel": [
        [PRINT, "Removing Existing OrangeBloxMacIntel.zip.."],
        [RUN, REGULAR, ["/bin/rm", "-f", "./Apps/OrangeBloxMacIntel.zip"]],
        [PRINT, "Generating Script Hash.."],
        [FUNCTION, generate_script_hash],
        [PRINT, "Building Nuitka Package.."],
        [RUN, NUITKA, [
            "--standalone", 
            "--macos-create-app-bundle", 
            "--include-data-files=PyKits.py=PyKits.py", 
            "--include-data-files=Version.json=Version.json", 
            "--output-dir=./Apps/Building", 
            "--include-package-data=objc,Cocoa,Quartz", 
            "--nofollow-import-to=cryptography,OpenSSL,urllib3,requests,plyer,site", 
            "--macos-app-icon=./Images/AppIcon.icns", 
            "--disable-plugin=tk-inter", 
            "--clang", 
            "--lto=yes", 
            "--remove-output", 
            "--target=OrangeBlox", 
            "./Apps/Scripts/OrangeBlox.py"
        ]],
        [RUN, REGULAR, ["/bin/cp", "./Apps/Scripts/Nuitka/Info.plist", "./Apps/Building/OrangeBlox.app/Contents/Info.plist"]],
        [RUN, REGULAR, ["/usr/bin/strip", "-S", "./Apps/Building/OrangeBlox.app/Contents/MacOS/OrangeBlox"]],
        [RUN, REGULAR, ["/usr/bin/strip", "-S", "./Apps/Building/OrangeBlox.app/Contents/MacOS/Python"]],
        [RUN, REGULAR, 'find "./Apps/Building/OrangeBlox.app" -type f \\( -name "*.so" -o -name "*.dylib" \\) -exec strip -S {} + 2>/dev/null \\'],
        [PRINT, "Signing Package.."],
        [LOOP, macos_codesign],
        [PRINT, "Creating OrangeBloxMacIntel.zip.."],
        [CD, "./Apps/Building"],
        [RUN, REGULAR, ["/usr/bin/zip", "-r", "-y", "../OrangeBloxMacIntel.zip", "OrangeBlox.app"]],
        [CD, "../Storage"],
        [RUN, REGULAR, ["/usr/bin/zip", "-r", "-y", "../OrangeBloxMacIntel.zip", "OrangePlayRoblox.app", "OrangeLoader.app", "OrangeRunStudio.app"]],
        [RESET_CD],
        [FUNCTION, macos_clean_up],
        [RM_DIR, "./Apps/Scripts/Nuitka/__pycache__"],
        [PRINT, "Successfully rebuilt OrangeBlox for Intel macOS!"],
        [PRINT, "Check the Apps folder for the generated ZIP file! File: ./Apps/OrangeBloxMacIntel.zip"]
    ],
    "arm": [
        [PRINT, "Removing Existing OrangeBloxMac.zip.."],
        [RUN, REGULAR, ["/bin/rm", "-f", "./Apps/OrangeBloxMac.zip"]],
        [PRINT, "Generating Script Hash.."],
        [FUNCTION, generate_script_hash],
        [PRINT, "Building Nuitka Package.."],
        [RUN, NUITKA, [
            "--standalone", 
            "--macos-create-app-bundle", 
            "--include-data-files=PyKits.py=PyKits.py", 
            "--include-data-files=Version.json=Version.json", 
            "--output-dir=./Apps/Building", 
            "--include-package-data=objc,Cocoa,Quartz", 
            "--nofollow-import-to=cryptography,OpenSSL,urllib3,requests,plyer,site", 
            "--macos-app-icon=./Images/AppIcon.icns", 
            "--disable-plugin=tk-inter", 
            "--clang", 
            "--lto=yes", 
            "--remove-output", 
            "--target=OrangeBlox", 
            "./Apps/Scripts/OrangeBlox.py"
        ]],
        [RUN, REGULAR, ["/bin/cp", "./Apps/Scripts/Nuitka/Info.plist", "./Apps/Building/OrangeBlox.app/Contents/Info.plist"]],
        [RUN, REGULAR, ["/usr/bin/strip", "-S", "./Apps/Building/OrangeBlox.app/Contents/MacOS/OrangeBlox"]],
        [RUN, REGULAR, ["/usr/bin/strip", "-S", "./Apps/Building/OrangeBlox.app/Contents/MacOS/Python"]],
        [RUN, REGULAR, 'find "./Apps/Building/OrangeBlox.app" -type f \\( -name "*.so" -o -name "*.dylib" \\) -exec strip -S {} + 2>/dev/null \\'],
        [PRINT, "Signing Package.."],
        [LOOP, macos_codesign],
        [PRINT, "Creating OrangeBloxMac.zip.."],
        [CD, "./Apps/Building"],
        [RUN, REGULAR, ["/usr/bin/zip", "-r", "-y", "../OrangeBloxMac.zip", "OrangeBlox.app"]],
        [CD, "../Storage"],
        [RUN, REGULAR, ["/usr/bin/zip", "-r", "-y", "../OrangeBloxMac.zip", "OrangePlayRoblox.app", "OrangeLoader.app", "OrangeRunStudio.app"]],
        [RESET_CD],
        [FUNCTION, macos_clean_up],
        [RM_DIR, "./Apps/Scripts/Nuitka/__pycache__"],
        [PRINT, "Successfully rebuilt OrangeBlox for arm64 macOS!"],
        [PRINT, "Check the Apps folder for the generated ZIP file! File: ./Apps/OrangeBloxMac.zip"]
    ]
}
windows = {
    "x64": [
        [SET_VAR, "arch", "x64"],
        [SET_VAR, "building_dir", os.path.join(cur_path, "Apps", "Building")],
        [FUNCTION, windows_rebuild],
        [PRINT, "Successfully rebuilt OrangeBlox for x64!"],
        [PRINT, "Check the Apps folder for the generated ZIP file! File: ./Apps/OrangeBloxWindows.zip"]
    ],
    "x86": [
        [SET_VAR, "arch", "x86"],
        [SET_VAR, "building_dir", os.path.join(cur_path, "Apps", "Building")],
        [FUNCTION, windows_rebuild],
        [PRINT, "Successfully rebuilt OrangeBlox for x86!"],
        [PRINT, "Check the Apps folder for the generated ZIP file! File: ./Apps/OrangeBloxWindows.zip"]
    ],
    "arm": [
        [SET_VAR, "arch", "arm64"],
        [SET_VAR, "building_dir", os.path.join(cur_path, "Apps", "Building")],
        [FUNCTION, windows_rebuild],
        [PRINT, "Successfully rebuilt OrangeBlox for arm64!"],
        [PRINT, "Check the Apps folder for the generated ZIP file! File: ./Apps/OrangeBloxWindows.zip"]
    ]
}

if __name__ == "__main__": raise Exception("Please don't run this script! This is only rebuild metadata!")