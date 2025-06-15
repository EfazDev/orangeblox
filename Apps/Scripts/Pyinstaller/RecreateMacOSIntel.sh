#!/bin/bash

printMessage() {
    local message=$1
    echo "\033[38;5;202mRebuild OrangeBlox @ ${message}\033[0m"
}

# Remove Existing OrangeBloxMac.zip
printMessage "Removing Existing OrangeBloxMacIntel.zip.."
rm -f ./Apps/OrangeBloxMacIntel.zip

# Generate Hash
printMessage "Generating Script Hashes.."
python3.13 ./Apps/Scripts/GenerateHash.py

# Build Pyinstaller Package
printMessage "Building Pyinstaller Package.."
pyinstaller ./Apps/Scripts/Pyinstaller/OrangeBlox_macOSIntel.spec --clean --distpath Apps --noconfirm

# Sign Package
printMessage "Signing Package.."
codesig1() {
    while true; do
    rm -rf ./Apps/OrangeBlox.app/Contents/_CodeSignature/
    if [ "$1" != "nosudo" ]; then
        sudo xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/OrangeBlox.app"
        sudo xattr -dr com.apple.FinderInfo "./Apps/OrangeBlox.app"
        sudo xattr -cr "./Apps/OrangeBlox.app"
        sudo codesign -s ${3:-'-'} --force --all-architectures --timestamp --deep "./Apps/OrangeBlox.app" --entitlements "./Apps/Scripts/Resources/Entitlements.plist"
    else
        xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/OrangeBlox.app"
        xattr -dr com.apple.FinderInfo "./Apps/OrangeBlox.app"
        xattr -cr "./Apps/OrangeBlox.app"
        codesign -s ${3:-'-'} --force --all-architectures --timestamp --deep "./Apps/OrangeBlox.app" --entitlements "./Apps/Scripts/Resources/Entitlements.plist"
    fi
    STATUS=$?
        if [ $STATUS -eq 0 ]; then
            break
        fi
    done
}
codesig1 "$2"

# Create OrangeBloxMac.zip
printMessage "Creating OrangeBloxMacIntel.zip.."
zip -r -y ./Apps/OrangeBloxMacIntel.zip "./Apps/OrangeBlox.app" "./Apps/OrangePlayRoblox.app" "./Apps/OrangeLoader.app" "./Apps/OrangeRunStudio.app"

# Remove Build and OrangeLoader folder
printMessage "Partial Cleaning.."
rm -rf ./build/

# Install OrangeBlox
if [ "$1" != "installer" ]; then
    printMessage "Running Installer.."
    python3 Install.py --rebuild-mode
fi

# Clean Up Apps
printMessage "Cleaning Up.."
rm -rf ./Apps/OrangeBlox.app/ ./Apps/OrangeBlox/ ./__pycache__/

# Done!
printMessage "Successfully rebuilt OrangeBlox!"
printMessage "Check the Apps folder for the generated ZIP file! File: ./Apps/OrangeBloxMacIntel.zip"
if [ "$1" != "installer" ]; then
    read -p "> "
fi