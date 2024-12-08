#!/bin/bash

printMessage() {
    local message=$1
    echo "\033[38;5;202mRebuild EfazRobloxBootstrap @ ${message}\033[0m"
}

# Remove Existing EfazRobloxBootstrapMac.zip
printMessage "Removing Existing EfazRobloxBootstrapMac.zip.."
rm -f ./Apps/EfazRobloxBootstrapMac.zip

# Generate Hash
printMessage "Generating Main.py Hash.."
python3 ./Apps/Scripts/GenerateMainHash.py

# Build Pyinstaller Package
printMessage "Building Pyinstaller Package.."
pyinstaller ./Apps/Scripts/Pyinstaller/EfazRobloxBootstrap_macOS.spec --distpath Apps --noconfirm

# Sign Package
printMessage "Signing Package.."
codesig1() {
    while true; do
    rm -rf ./Apps/EfazRobloxBootstrapMain.app/Contents/_CodeSignature/
    if [ "$1" != "nosudo" ]; then
        sudo xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/EfazRobloxBootstrapMain.app"
        sudo xattr -dr com.apple.FinderInfo "./Apps/EfazRobloxBootstrapMain.app"
        sudo xattr -cr "./Apps/EfazRobloxBootstrapMain.app"
        sudo codesign -s - --force --all-architectures --timestamp --deep "./Apps/EfazRobloxBootstrapMain.app"
    else
        xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/EfazRobloxBootstrapMain.app"
        xattr -dr com.apple.FinderInfo "./Apps/EfazRobloxBootstrapMain.app"
        xattr -cr "./Apps/EfazRobloxBootstrapMain.app"
        codesign -s - --force --all-architectures --timestamp --deep "./Apps/EfazRobloxBootstrapMain.app"
    fi
    STATUS=$?
        if [ $STATUS -eq 0 ]; then
            break
        else
            printMessage "Main Codesign Attempt Failed. Retrying.."
        fi
    done
}
codesig1 "$2"
codesig2() {
    while true; do
        rm -rf ./Apps/EfazRobloxBootstrapLoad.app/Contents/_CodeSignature/
        if [ "$1" != "nosudo" ]; then
            sudo xattr -dr com.apple.FinderInfo "./Apps/EfazRobloxBootstrapLoad.app"
            sudo xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/EfazRobloxBootstrapLoad.app"
            sudo xattr -cr "./Apps/EfazRobloxBootstrapLoad.app"
            sudo codesign -s - --force --all-architectures --timestamp --deep "./Apps/EfazRobloxBootstrapLoad.app"
        else
            xattr -dr com.apple.FinderInfo "./Apps/EfazRobloxBootstrapLoad.app"
            xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/EfazRobloxBootstrapLoad.app"
            xattr -cr "./Apps/EfazRobloxBootstrapLoad.app"
            codesign -s - --force --all-architectures --timestamp --deep "./Apps/EfazRobloxBootstrapLoad.app"
        fi
        STATUS=$?
        if [ $STATUS -eq 0 ]; then
            break
        else
            printMessage "Loader Codesign Attempt Failed. Retrying.."
        fi
    done
}
codesig2 "$2"

# Create EfazRobloxBootstrapMac.zip
printMessage "Creating EfazRobloxBootstrapMac.zip.."
zip -r -y ./Apps/EfazRobloxBootstrapMac.zip "./Apps/EfazRobloxBootstrapMain.app" "./Apps/Play Roblox.app" "./Apps/EfazRobloxBootstrapLoad.app" 

# Remove Build and EfazRobloxBootstrapLoad folder
printMessage "Partial Cleaning.."
rm -rf ./build/ ./Apps/EfazRobloxBootstrapLoad/ 

# Install EfazRobloxBootstrap
if [ "$1" != "installer" ]; then
    printMessage "Running Installer.."
    python3 Install.py --rebuild-mode
fi

# Clean Up Apps
printMessage "Cleaning Up.."
rm -rf ./Apps/EfazRobloxBootstrapMain.app/ ./Apps/EfazRobloxBootstrapLoad.app/ ./Apps/EfazRobloxBootstrapMain/ ./__pycache__/

# Done!
printMessage "Successfully rebuilt EfazRobloxBootstrap!"
printMessage "Check the Apps folder for the generated ZIP file! File: ./Apps/EfazRobloxBootstrapMac.zip"
if [ "$1" != "installer" ]; then
    read -p "> "
fi