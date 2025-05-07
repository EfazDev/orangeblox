#!/bin/bash

printMessage() {
    local message=$1
    echo "\033[38;5;202mRebuild OrangeBlox @ ${message}\033[0m"
}

# Remove Existing OrangeBloxMac.zip
printMessage "Removing Existing OrangeBloxMac.zip.."
rm -f ./Apps/OrangeBloxMac.zip

# Generate Hash
printMessage "Generating Script Hashes.."
python3 ./Apps/Scripts/GenerateHash.py

# Build Nuitka Package
printMessage "Building Nuitka Package.."
python3.12 -m nuitka --macos-create-app-bundle --enable-plugin=tk-inter --include-data-files=PipHandler.py=PipHandler.py --include-data-files=Version.json=Version.json --output-dir="./Apps" --macos-app-icon=./BootstrapImages/AppIcon.icns --include-package-data=pyobjc --include-package-data=Cocoa --include-package-data=Quartz --target="OrangeBlox" "./Apps/Scripts/OrangeBlox.py"
rm -rf ./Apps/OrangeBloxMain.app
mv ./Apps/OrangeBlox.app ./Apps/OrangeBloxMain.app
mv ./Apps/OrangeBloxMain.app/Contents/MacOS/OrangeBlox ./Apps/OrangeBloxMain.app/Contents/MacOS/OrangeBloxMain
cp ./Apps/Scripts/Nuitka/Info.plist ./Apps/OrangeBloxMain.app/Contents/Info.plist

# Sign Package
printMessage "Signing Package.."
codesig1() {
    while true; do
    rm -rf ./Apps/OrangeBloxMain.app/Contents/_CodeSignature/
    if [ "$1" != "nosudo" ]; then
        sudo xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/OrangeBloxMain.app"
        sudo xattr -dr com.apple.FinderInfo "./Apps/OrangeBloxMain.app"
        sudo xattr -cr "./Apps/OrangeBloxMain.app"
        sudo codesign -s ${3:-'-'} --force --all-architectures --timestamp --deep "./Apps/OrangeBloxMain.app"
    else
        xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/OrangeBloxMain.app"
        xattr -dr com.apple.FinderInfo "./Apps/OrangeBloxMain.app"
        xattr -cr "./Apps/OrangeBloxMain.app"
        codesign -s ${3:-'-'} --force --all-architectures --timestamp --deep "./Apps/OrangeBloxMain.app"
    fi
    STATUS=$?
        if [ $STATUS -eq 0 ]; then
            break
        fi
    done
}
codesig1 "$2"

# Create OrangeBloxMac.zip
printMessage "Creating OrangeBloxMac.zip.."
zip -r -y ./Apps/OrangeBloxMac.zip "./Apps/OrangeBloxMain.app" "./Apps/Play Roblox.app" "./Apps/OrangeBloxLoad.app" "./Apps/Run Studio.app"

# Remove Build and OrangeBloxLoad folder
printMessage "Partial Cleaning.."
rm -rf ./build/

# Install OrangeBlox
if [ "$1" != "installer" ]; then
    printMessage "Running Installer.."
    python3 Install.py --rebuild-mode
fi

# Clean Up Apps
printMessage "Cleaning Up.."
rm -rf ./Apps/OrangeBloxMain.app/ ./Apps/OrangeBlox.build/ ./Apps/OrangeBlox.dist/ ./__pycache__/

# Done!
printMessage "Successfully rebuilt OrangeBlox!"
printMessage "Check the Apps folder for the generated ZIP file! File: ./Apps/OrangeBloxMac.zip"
if [ "$1" != "installer" ]; then
    read -p "> "
fi