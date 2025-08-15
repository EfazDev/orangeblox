#!/bin/bash

printMessage() {
    local message=$1
    echo "\033[38;5;202mRebuild OrangeBlox @ ${message}\033[0m"
}

# Build Package
printMessage "Building Clang Package for OrangeLoader.."
clang++ -framework Cocoa -std=c++17 -arch x86_64 -g0 -arch arm64 -o "./Apps/Storage/OrangeLoader.app/Contents/MacOS/OrangeLoader" ./Apps/Scripts/Clang/OrangeLoader.mm
strip -S "./Apps/Storage/OrangeLoader.app/Contents/MacOS/OrangeLoader" 2>/dev/null \;

printMessage "Building Clang Package for OrangePlayRoblox.."
cp "./Apps/Storage/OrangeLoader.app/Contents/MacOS/OrangeLoader" "./Apps/Storage/OrangePlayRoblox.app/Contents/MacOS/OrangePlayRoblox"
strip -S "./Apps/Storage/OrangePlayRoblox.app/Contents/MacOS/OrangePlayRoblox" 2>/dev/null \;

printMessage "Building Clang Package for OrangeRunStudio.."
cp "./Apps/Storage/OrangeLoader.app/Contents/MacOS/OrangeLoader" "./Apps/Storage/OrangeRunStudio.app/Contents/MacOS/OrangeRunStudio"
strip -S "./Apps/Storage/OrangeRunStudio.app/Contents/MacOS/OrangeRunStudio" 2>/dev/null \;

# Sign Package
printMessage "Signing Package.."
rm -rf "./Apps/Storage/OrangeLoader.app/Contents/_CodeSignature/"
rm -rf "./Apps/Storage/OrangePlayRoblox.app/Contents/_CodeSignature/"
rm -rf "./Apps/Storage/OrangeRunStudio.app/Contents/_CodeSignature/"
codesig() {
    while true; do
        if [ "$1" != "sudo" ]; then
            xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/Storage/OrangeLoader.app"
            xattr -dr com.apple.FinderInfo "./Apps/Storage/OrangeLoader.app"
            xattr -cr "./Apps/Storage/OrangeLoader.app"
            codesign -s ${1:-'-'} --force --all-architectures --timestamp --deep "./Apps/Storage/OrangeLoader.app" --entitlements "./Apps/Storage/Entitlements.plist"
        else
            sudo xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/Storage/OrangeLoader.app"
            sudo xattr -dr com.apple.FinderInfo "./Apps/Storage/OrangeLoader.app"
            sudo xattr -cr "./Apps/Storage/OrangeLoader.app"
            sudo codesign -s ${1:-'-'} --force --all-architectures --timestamp --deep "./Apps/Storage/OrangeLoader.app" --entitlements "./Apps/Storage/Entitlements.plist"
        fi
        STATUS=$?
        if [ $STATUS -eq 0 ]; then
            break
        fi
    done
    while true; do
        if [ "$1" != "sudo" ]; then
            xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/Storage/OrangePlayRoblox.app"
            xattr -dr com.apple.FinderInfo "./Apps/Storage/OrangePlayRoblox.app"
            xattr -cr "./Apps/Storage/OrangePlayRoblox.app"
            codesign -s ${1:-'-'} --force --all-architectures --timestamp --deep "./Apps/Storage/OrangePlayRoblox.app" --entitlements "./Apps/Storage/Entitlements.plist"
        else
            sudo xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/Storage/OrangePlayRoblox.app"
            sudo xattr -dr com.apple.FinderInfo "./Apps/Storage/OrangePlayRoblox.app"
            sudo xattr -cr "./Apps/Storage/OrangePlayRoblox.app"
            sudo codesign -s ${1:-'-'} --force --all-architectures --timestamp --deep "./Apps/Storage/OrangePlayRoblox.app" --entitlements "./Apps/Storage/Entitlements.plist"
        fi
        STATUS=$?
        if [ $STATUS -eq 0 ]; then
            break
        fi
    done
    while true; do
        if [ "$1" != "sudo" ]; then
            xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/Storage/OrangeRunStudio.app"
            xattr -dr com.apple.FinderInfo "./Apps/Storage/OrangeRunStudio.app"
            xattr -cr "./Apps/Storage/OrangeRunStudio.app"
            codesign -s ${1:-'-'} --force --all-architectures --timestamp --deep "./Apps/Storage/OrangeRunStudio.app" --entitlements "./Apps/Storage/Entitlements.plist"
        else
            sudo xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/Storage/OrangeRunStudio.app"
            sudo xattr -dr com.apple.FinderInfo "./Apps/Storage/OrangeRunStudio.app"
            sudo xattr -cr "./Apps/Storage/OrangeRunStudio.app"
            sudo codesign -s ${1:-'-'} --force --all-architectures --timestamp --deep "./Apps/Storage/OrangeRunStudio.app" --entitlements "./Apps/Storage/Entitlements.plist"
        fi
        STATUS=$?
        if [ $STATUS -eq 0 ]; then
            break
        fi
    done
}
codesig "$1"

# Done!
printMessage "Successfully rebuilt OrangeLoader, OrangePlayRoblox and OrangeRunStudio!"
printMessage "The executables have been moved to their assigned bundles and are ready for RecreateMacOS.sh!"