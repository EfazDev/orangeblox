"""
OrangeBlox Pyinstaller Rebuild Module

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
        [PRINT, "Building Pyinstaller Package.."],
        [RUN, PYINSTALLER, ["./Apps/Scripts/Pyinstaller/OrangeBlox_Windows.spec", "--clean", "--distpath", "Apps/Building", "--noconfirm"]],
        [MAKE_DIR, os.path.join(variables["building_dir"], "OrangeBloxWindows")],
        [MAKE_DIR, os.path.join(variables["building_dir"], "OrangeBloxWindows", variables["arch"])],
        [MOVE, os.path.join(variables["building_dir"], "OrangeBlox.exe"), os.path.join(variables["building_dir"], "OrangeBloxWindows", variables["arch"], "OrangeBlox.exe")],
        [MOVE, os.path.join(variables["building_dir"], "_internal"), os.path.join(variables["building_dir"], "OrangeBloxWindows", variables["arch"], "_internal")],
        [MOVE, os.path.join(variables["building_dir"], "OrangeBlox", "OrangeBlox.exe"), os.path.join(variables["building_dir"], "OrangeBloxWindows", variables["arch"], "OrangeBlox.exe")],
        [MOVE, os.path.join(variables["building_dir"], "OrangeBlox", "_internal"), os.path.join(variables["building_dir"], "OrangeBloxWindows", variables["arch"], "_internal")],
    ] + s + [
        [PRINT, "Compressing Package.."],
        [RUN, REGULAR, [powershell, "Compress-Archive", "-Path", os.path.join(variables["building_dir"], "OrangeBloxWindows", "*"), "-Update", "-DestinationPath", os.path.join(cur_path, "Apps", "OrangeBloxWindows.zip")]],
        [PRINT, "Cleaning up.."],
        [RM_DIR, os.path.join(variables["building_dir"], "OrangeBloxWindows")],
        [RM_DIR, os.path.join(cur_path, "__pycache__")],
        [RM_DIR, os.path.join(variables["building_dir"], "OrangeBlox")],
        [RM_DIR, os.path.join(cur_path, "build")],
        [RM_DIR, os.path.join(cur_path, "Apps", "Scripts", "Nuitka", "__pycache__")]
    ]
macos = {
    "intel": [
        [PRINT, "Removing Existing OrangeBloxMacIntel.zip.."],
        [RUN, REGULAR, ["/bin/rm", "-f", "./Apps/OrangeBloxMacIntel.zip"]],
        [FUNCTION, generate_script_hash],
        [PRINT, "Building Pyinstaller Package.."],
        [RUN, PYINSTALLER, ["./Apps/Scripts/Pyinstaller/OrangeBlox_macOSIntel.spec", "--clean", "--distpath", "Apps/Building", "--noconfirm"]],
        [PRINT, "Signing Package.."],
        [LOOP, macos_codesign],
        [PRINT, "Creating OrangeBloxMacIntel.zip.."],
        [CD, "./Apps/Building"],
        [RUN, REGULAR, ["/usr/bin/zip", "-r", "-y", "../OrangeBloxMacIntel.zip", "OrangeBlox.app"]],
        [CD, "../Storage"],
        [RUN, REGULAR, ["/usr/bin/zip", "-r", "-y", "../OrangeBloxMacIntel.zip", "OrangePlayRoblox.app", "OrangeLoader.app", "OrangeRunStudio.app"]],
        [RESET_CD],
        [FUNCTION, macos_clean_up],
        [RM_DIR, "./Apps/Scripts/Pyinstaller/__pycache__"],
        [PRINT, "Successfully rebuilt OrangeBlox for Intel macOS!"],
        [PRINT, "Check the Apps folder for the generated ZIP file! File: ./Apps/OrangeBloxMacIntel.zip"]
    ],
    "arm": [
        [PRINT, "Removing Existing OrangeBloxMac.zip.."],
        [RUN, REGULAR, ["/bin/rm", "-f", "./Apps/OrangeBloxMac.zip"]],
        [FUNCTION, generate_script_hash],
        [PRINT, "Building Pyinstaller Package.."],
        [RUN, PYINSTALLER, ["./Apps/Scripts/Pyinstaller/OrangeBlox_macOS.spec", "--clean", "--distpath", "Apps/Building", "--noconfirm"]],
        [PRINT, "Signing Package.."],
        [LOOP, macos_codesign],
        [PRINT, "Creating OrangeBloxMac.zip.."],
        [CD, "./Apps/Building"],
        [RUN, REGULAR, ["/usr/bin/zip", "-r", "-y", "../OrangeBloxMac.zip", "OrangeBlox.app"]],
        [CD, "../Storage"],
        [RUN, REGULAR, ["/usr/bin/zip", "-r", "-y", "../OrangeBloxMac.zip", "OrangePlayRoblox.app", "OrangeLoader.app", "OrangeRunStudio.app"]],
        [RESET_CD],
        [FUNCTION, macos_clean_up],
        [RM_DIR, "./Apps/Scripts/Pyinstaller/__pycache__"],
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