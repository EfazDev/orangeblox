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

# Build Pyinstaller Package
printMessage "Building Pyinstaller Package.."
pyinstaller ./Apps/Scripts/Pyinstaller/OrangeBlox_macOS.spec --clean --distpath Apps/Building --noconfirm

# Sign Package
printMessage "Signing Package.."
codesig1() {
    while true; do
        rm -rf ./Apps/Building/OrangeBlox.app/Contents/_CodeSignature/
        xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/Building/OrangeBlox.app"
        xattr -dr com.apple.FinderInfo "./Apps/Building/OrangeBlox.app"
        xattr -cr "./Apps/Building/OrangeBlox.app"
        codesign -s ${1:-'-'} --force --all-architectures --timestamp --deep "./Apps/Building/OrangeBlox.app" --entitlements "./Apps/Storage/Entitlements.plist"
        STATUS=$?
        if [ $STATUS -eq 0 ]; then
            break
        fi
    done
}
codesig1 "$1"

# Create OrangeBloxMac.zip
printMessage "Creating OrangeBloxMac.zip.."
cd "./Apps/Building"
zip -r -y ../OrangeBloxMac.zip "OrangeBlox.app"
cd "../Storage"
zip -r -y ../OrangeBloxMac.zip "OrangePlayRoblox.app" "OrangeLoader.app" "OrangeRunStudio.app"
cd ../../

# Remove Build and OrangeLoader folder
printMessage "Partial Cleaning.."
rm -rf ./build/

# Clean Up Apps
printMessage "Cleaning Up.."
rm -rf ./Apps/Building/OrangeBlox.app/ ./Apps/Building/OrangeBlox/ ./Apps/OrangeBloxMac/ ./__pycache__/

# Done!
printMessage "Successfully rebuilt OrangeBlox!"
printMessage "Check the Apps folder for the generated ZIP file! File: ./Apps/OrangeBloxMac.zip"