"""
OrangeBlox Clang Rebuild Module

Contains metadata and commands for rebuilding OrangeBlox!
"""

# Modules
import os

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
CLANG = 6

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
def macos_codesign(): 
    return 4, [
        [RUN, REGULAR, ["/bin/rm", "-rf", os.path.join(variables["pkg"], "Contents", "_CodeSignature")]],
        [RUN, REGULAR, ["/usr/bin/xattr", "-dr", "com.apple.metadata:_kMDItemUserTags", variables["pkg"]]],
        [RUN, REGULAR, ["/usr/bin/xattr", "-dr", "com.apple.FinderInfo", variables["pkg"]]],
        [RUN, REGULAR, ["/usr/bin/xattr", "-cr", variables["pkg"]]],
        [RUN, REGULAR, ["/usr/bin/codesign", "-s", getArg(0, "-"), "--force", "--all-architectures", "--timestamp", "--deep", variables["pkg"], "--entitlements", "./Apps/Storage/Entitlements.plist"]]
    ]
macos = {
    "intel": [
        [PRINT, "Building Clang Package for OrangeLoader.."],
        [RUN, CLANGPLUSPLUS, ["-framework", "Cocoa", "-std=c++17", "-arch", "x86_64", "-g0", "-o", "./Apps/Storage/OrangeLoader.app/Contents/MacOS/OrangeLoader", "./Apps/Scripts/Clang/OrangeLoader.mm"]],
        [RUN, REGULAR, ["/usr/bin/strip", "-S", "./Apps/Storage/OrangeLoader.app/Contents/MacOS/OrangeLoader"]],
        [PRINT, "Building Clang Package for OrangePlayRoblox.."],
        [RUN, REGULAR, ["/bin/cp", "./Apps/Storage/OrangeLoader.app/Contents/MacOS/OrangeLoader", "./Apps/Storage/OrangePlayRoblox.app/Contents/MacOS/OrangePlayRoblox"]],
        [PRINT, "Building Clang Package for OrangeRunStudio.."],
        [RUN, REGULAR, ["/bin/cp", "./Apps/Storage/OrangeLoader.app/Contents/MacOS/OrangeLoader", "./Apps/Storage/OrangeRunStudio.app/Contents/MacOS/OrangeRunStudio"]],
        [PRINT, "Signing Package.."],
        [SET_VAR, "pkg", "./Apps/Storage/OrangeLoader.app/"],
        [LOOP, macos_codesign],
        [SET_VAR, "pkg", "./Apps/Storage/OrangePlayRoblox.app/"],
        [LOOP, macos_codesign],
        [SET_VAR, "pkg", "./Apps/Storage/OrangeRunStudio.app/"],
        [LOOP, macos_codesign],
        [RM_DIR, "./Apps/Scripts/Clang/__pycache__"],
        [PRINT, "Successfully rebuilt OrangeLoader, OrangePlayRoblox and OrangeRunStudio!"],
        [PRINT, "The executables have been moved to their assigned bundles and are ready for RecreateMacOS.sh!"]
    ],
    "arm": [
        [PRINT, "Building Clang Package for OrangeLoader.."],
        [RUN, CLANGPLUSPLUS, ["-framework", "Cocoa", "-std=c++17", "-arch", "x86_64", "-g0", "-arch", "arm64", "-o", "./Apps/Storage/OrangeLoader.app/Contents/MacOS/OrangeLoader", "./Apps/Scripts/Clang/OrangeLoader.mm"]],
        [RUN, REGULAR, ["/usr/bin/strip", "-S", "./Apps/Storage/OrangeLoader.app/Contents/MacOS/OrangeLoader"]],
        [PRINT, "Building Clang Package for OrangePlayRoblox.."],
        [RUN, REGULAR, ["/bin/cp", "./Apps/Storage/OrangeLoader.app/Contents/MacOS/OrangeLoader", "./Apps/Storage/OrangePlayRoblox.app/Contents/MacOS/OrangePlayRoblox"]],
        [PRINT, "Building Clang Package for OrangeRunStudio.."],
        [RUN, REGULAR, ["/bin/cp", "./Apps/Storage/OrangeLoader.app/Contents/MacOS/OrangeLoader", "./Apps/Storage/OrangeRunStudio.app/Contents/MacOS/OrangeRunStudio"]],
        [PRINT, "Signing Package.."],
        [SET_VAR, "pkg", "./Apps/Storage/OrangeLoader.app/"],
        [LOOP, macos_codesign],
        [SET_VAR, "pkg", "./Apps/Storage/OrangePlayRoblox.app/"],
        [LOOP, macos_codesign],
        [SET_VAR, "pkg", "./Apps/Storage/OrangeRunStudio.app/"],
        [LOOP, macos_codesign],
        [RM_DIR, "./Apps/Scripts/Clang/__pycache__"],
        [PRINT, "Successfully rebuilt OrangeLoader, OrangePlayRoblox and OrangeRunStudio!"],
        [PRINT, "The executables have been moved to their assigned bundles and are ready for RecreateMacOS.sh!"]
    ]
}
windows = {
    "x64": [],
    "x86": [],
    "arm": []
}

if __name__ == "__main__": raise Exception("Please don't run this script! This is only rebuild metadata!")