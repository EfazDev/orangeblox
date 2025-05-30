#!/bin/bash

printMessage() {
    local message=$1
    echo "\033[38;5;202mRebuild OrangeBlox @ ${message}\033[0m"
}

# Build Package
printMessage "Building Clang Package for OrangeLoader.."
clang++ -framework Cocoa -std=c++17 -arch x86_64 -g -o "./Apps/OrangeLoader.app/Contents/MacOS/OrangeLoader" ./Apps/Scripts/Clang/OrangeLoader.mm -g0

printMessage "Building Clang Package for OrangePlayRoblox.."
clang++ -framework Cocoa -std=c++17 -arch x86_64 -g -o "./Apps/OrangePlayRoblox.app/Contents/MacOS/OrangePlayRoblox" ./Apps/Scripts/Clang/OrangePlayRoblox.mm -g0

printMessage "Building Clang Package for OrangeRunStudio.."
clang++ -framework Cocoa -std=c++17 -arch x86_64 -g -o "./Apps/OrangeRunStudio.app/Contents/MacOS/OrangeRunStudio" ./Apps/Scripts/Clang/OrangeRunStudio.mm -g0

# Sign Package
printMessage "Signing Package.."
rm -rf "./Apps/OrangeLoader.app/Contents/_CodeSignature/"
rm -rf "./Apps/OrangePlayRoblox.app/Contents/_CodeSignature/"
rm -rf "./Apps/OrangeRunStudio.app/Contents/_CodeSignature/"
codesig() {
    while true; do
        if [ "$1" != "nosudo" ]; then
            sudo xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/OrangeLoader.app"
            sudo xattr -dr com.apple.FinderInfo "./Apps/OrangeLoader.app"
            sudo xattr -cr "./Apps/OrangeLoader.app"
            sudo codesign -s ${3:-'-'} --force --all-architectures --timestamp --deep "./Apps/OrangeLoader.app"
        else
            xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/OrangeLoader.app"
            xattr -dr com.apple.FinderInfo "./Apps/OrangeLoader.app"
            xattr -cr "./Apps/OrangeLoader.app"
            codesign -s ${3:-'-'} --force --all-architectures --timestamp --deep "./Apps/OrangeLoader.app"
        fi
        STATUS=$?
        if [ $STATUS -eq 0 ]; then
            break
        fi
    done
    while true; do
        if [ "$1" != "nosudo" ]; then
            sudo xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/OrangePlayRoblox.app"
            sudo xattr -dr com.apple.FinderInfo "./Apps/OrangePlayRoblox.app"
            sudo xattr -cr "./Apps/OrangePlayRoblox.app"
            sudo codesign -s ${3:-'-'} --force --all-architectures --timestamp --deep "./Apps/OrangePlayRoblox.app"
        else
            xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/OrangePlayRoblox.app"
            xattr -dr com.apple.FinderInfo "./Apps/OrangePlayRoblox.app"
            xattr -cr "./Apps/OrangePlayRoblox.app"
            codesign -s ${3:-'-'} --force --all-architectures --timestamp --deep "./Apps/OrangePlayRoblox.app"
        fi
        STATUS=$?
        if [ $STATUS -eq 0 ]; then
            break
        fi
    done
    while true; do
        if [ "$1" != "nosudo" ]; then
            sudo xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/OrangeRunStudio.app"
            sudo xattr -dr com.apple.FinderInfo "./Apps/OrangeRunStudio.app"
            sudo xattr -cr "./Apps/OrangeRunStudio.app"
            sudo codesign -s ${3:-'-'} --force --all-architectures --timestamp --deep "./Apps/OrangeRunStudio.app"
        else
            xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/OrangeRunStudio.app"
            xattr -dr com.apple.FinderInfo "./Apps/OrangeRunStudio.app"
            xattr -cr "./Apps/OrangeRunStudio.app"
            codesign -s ${3:-'-'} --force --all-architectures --timestamp --deep "./Apps/OrangeRunStudio.app"
        fi
        STATUS=$?
        if [ $STATUS -eq 0 ]; then
            break
        fi
    done
}
codesig "$2"

# Done!
printMessage "Successfully rebuilt OrangeLoader, OrangePlayRoblox and OrangeRunStudio!"
printMessage "The executables have been moved to their assigned bundles and are ready for RecreateMacOS.sh!"
if [ "$1" != "installer" ]; then
    read -p "> "
fi