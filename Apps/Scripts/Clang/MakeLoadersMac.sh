#!/bin/bash

printMessage() {
    local message=$1
    echo "\033[38;5;202mRebuild EfazRobloxBootstrap @ ${message}\033[0m"
}

# Build Package
printMessage "Building Clang Package for EfazRobloxBootstrapLoad.."
clang++ -framework Cocoa -framework Foundation -std=c++17 -arch x86_64 -g -arch arm64 -o "./Apps/EfazRobloxBootstrapLoad.app/Contents/MacOS/EfazRobloxBootstrapLoad" ./Apps/Scripts/Clang/EfazRobloxBootstrapLoad.mm -g0

printMessage "Building Clang Package for EfazRobloxBootstrapPlayRoblox.."
clang++ -framework Cocoa -framework Foundation -std=c++17 -arch x86_64 -g -arch arm64 -o "./Apps/Play Roblox.app/Contents/MacOS/EfazRobloxBootstrapPlayRoblox" ./Apps/Scripts/Clang/EfazRobloxBootstrapPlayRoblox.cpp -g0

# Sign Package
printMessage "Signing Package.."
rm -rf "./Apps/EfazRobloxBootstrapLoad.app/Contents/_CodeSignature/"
rm -rf "./Apps/Play Roblox.app/Contents/_CodeSignature/"
codesig() {
    while true; do
        if [ "$1" != "nosudo" ]; then
            sudo xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/EfazRobloxBootstrapLoad.app"
            sudo xattr -dr com.apple.FinderInfo "./Apps/EfazRobloxBootstrapLoad.app"
            sudo xattr -cr "./Apps/EfazRobloxBootstrapLoad.app"
            sudo codesign -s - --force --all-architectures --timestamp --deep "./Apps/EfazRobloxBootstrapLoad.app"
        else
            xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/EfazRobloxBootstrapLoad.app"
            xattr -dr com.apple.FinderInfo "./Apps/EfazRobloxBootstrapLoad.app"
            xattr -cr "./Apps/EfazRobloxBootstrapLoad.app"
            codesign -s - --force --all-architectures --timestamp --deep "./Apps/EfazRobloxBootstrapLoad.app"
        fi
        STATUS=$?
        if [ $STATUS -eq 0 ]; then
            break
        fi
    done
    while true; do
        if [ "$1" != "nosudo" ]; then
            sudo xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/Play Roblox.app"
            sudo xattr -dr com.apple.FinderInfo "./Apps/Play Roblox.app"
            sudo xattr -cr "./Apps/Play Roblox.app"
            sudo codesign -s - --force --all-architectures --timestamp --deep "./Apps/Play Roblox.app"
        else
            xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/Play Roblox.app"
            xattr -dr com.apple.FinderInfo "./Apps/Play Roblox.app"
            xattr -cr "./Apps/Play Roblox.app"
            codesign -s - --force --all-architectures --timestamp --deep "./Apps/Play Roblox.app"
        fi
        STATUS=$?
        if [ $STATUS -eq 0 ]; then
            break
        fi
    done
}
codesig "$2"

# Done!
printMessage "Successfully rebuilt EfazRobloxBootstrapLoad and EfazRobloxBootstrapPlayRoblox!"
printMessage "The executables have been moved to their assigned bundles and are ready for RecreateMacOS.sh!"
if [ "$1" != "installer" ]; then
    read -p "> "
fi