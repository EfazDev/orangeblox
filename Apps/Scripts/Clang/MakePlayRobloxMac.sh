#!/bin/bash

printMessage() {
    local message=$1
    echo "\033[38;5;202mRebuild EfazRobloxBootstrapPlayRoblox @ ${message}\033[0m"
}

# Build Package
printMessage "Building Clang Package for EfazRobloxBootstrapPlayRoblox.."
clang++ -std=c++17 -arch x86_64 -g -arch arm64 -o "./Apps/Play Roblox.app/Contents/MacOS/EfazRobloxBootstrapPlayRoblox" ./Apps/Scripts/Clang/EfazRobloxBootstrapPlayRoblox.cpp

# Remove dSYM
printMessage "Removing dSYM.."
rm -rf "./Apps/Play Roblox.app/Contents/MacOS/EfazRobloxBootstrapPlayRoblox.dSYM/"

# Sign Package
printMessage "Signing Package.."
rm -rf "./Apps/Play Roblox.app/Contents/_CodeSignature/"
sudo xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/Play Roblox.app"
sudo xattr -dr com.apple.FinderInfo "./Apps/Play Roblox.app"
sudo xattr -cr "./Apps/Play Roblox.app"
sudo codesign -s - --force --all-architectures --timestamp --deep "./Apps/Play Roblox.app"

# Done!
printMessage "Successfully rebuilt EfazRobloxBootstrapPlayRoblox!"
printMessage "The executable has been moved to the Play Roblox.app bundle and is ready for RecreateMacOS.sh!"
read -p "> "