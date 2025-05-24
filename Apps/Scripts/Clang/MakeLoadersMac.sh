#!/bin/bash

printMessage() {
    local message=$1
    echo "\033[38;5;202mRebuild OrangeBlox @ ${message}\033[0m"
}

# Build Package
printMessage "Building Clang Package for OrangeBloxLoad.."
clang++ -framework Cocoa -std=c++17 -arch x86_64 -g -arch arm64 -o "./Apps/OrangeBloxLoad.app/Contents/MacOS/OrangeBloxLoad" ./Apps/Scripts/Clang/OrangeBloxLoad.mm -g0

printMessage "Building Clang Package for OrangePlayRoblox.."
clang++ -framework Cocoa -std=c++17 -arch x86_64 -g -arch arm64 -o "./Apps/Play Roblox.app/Contents/MacOS/OrangePlayRoblox" ./Apps/Scripts/Clang/OrangePlayRoblox.mm -g0

printMessage "Building Clang Package for OrangeRunStudio.."
clang++ -framework Cocoa -std=c++17 -arch x86_64 -g -arch arm64 -o "./Apps/Run Studio.app/Contents/MacOS/OrangeRunStudio" ./Apps/Scripts/Clang/OrangeRunStudio.mm -g0

# Sign Package
printMessage "Signing Package.."
rm -rf "./Apps/OrangeBloxLoad.app/Contents/_CodeSignature/"
rm -rf "./Apps/Play Roblox.app/Contents/_CodeSignature/"
rm -rf "./Apps/Run Studio.app/Contents/_CodeSignature/"
codesig() {
    while true; do
        if [ "$1" != "nosudo" ]; then
            sudo xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/OrangeBloxLoad.app"
            sudo xattr -dr com.apple.FinderInfo "./Apps/OrangeBloxLoad.app"
            sudo xattr -cr "./Apps/OrangeBloxLoad.app"
            sudo codesign -s ${3:-'-'} --force --all-architectures --timestamp --deep "./Apps/OrangeBloxLoad.app"
        else
            xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/OrangeBloxLoad.app"
            xattr -dr com.apple.FinderInfo "./Apps/OrangeBloxLoad.app"
            xattr -cr "./Apps/OrangeBloxLoad.app"
            codesign -s ${3:-'-'} --force --all-architectures --timestamp --deep "./Apps/OrangeBloxLoad.app"
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
            sudo codesign -s ${3:-'-'} --force --all-architectures --timestamp --deep "./Apps/Play Roblox.app"
        else
            xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/Play Roblox.app"
            xattr -dr com.apple.FinderInfo "./Apps/Play Roblox.app"
            xattr -cr "./Apps/Play Roblox.app"
            codesign -s ${3:-'-'} --force --all-architectures --timestamp --deep "./Apps/Play Roblox.app"
        fi
        STATUS=$?
        if [ $STATUS -eq 0 ]; then
            break
        fi
    done
    while true; do
        if [ "$1" != "nosudo" ]; then
            sudo xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/Run Studio.app"
            sudo xattr -dr com.apple.FinderInfo "./Apps/Run Studio.app"
            sudo xattr -cr "./Apps/Run Studio.app"
            sudo codesign -s ${3:-'-'} --force --all-architectures --timestamp --deep "./Apps/Run Studio.app"
        else
            xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/Run Studio.app"
            xattr -dr com.apple.FinderInfo "./Apps/Run Studio.app"
            xattr -cr "./Apps/Run Studio.app"
            codesign -s ${3:-'-'} --force --all-architectures --timestamp --deep "./Apps/Run Studio.app"
        fi
        STATUS=$?
        if [ $STATUS -eq 0 ]; then
            break
        fi
    done
}
codesig "$2"

# Done!
printMessage "Successfully rebuilt OrangeBloxLoad, OrangePlayRoblox and OrangeRunStudio!"
printMessage "The executables have been moved to their assigned bundles and are ready for RecreateMacOS.sh!"
if [ "$1" != "installer" ]; then
    read -p "> "
fi