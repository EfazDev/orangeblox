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
python3 -m nuitka \
    --standalone \
    --macos-create-app-bundle \
    --include-data-files=PyKits.py=PyKits.py \
    --include-data-files=Version.json=Version.json \
    --output-dir="./Apps/Building" \
    --include-package-data=objc,Cocoa,Quartz \
    --nofollow-import-to=cryptography,OpenSSL,urllib3,requests,plyer,site \
    --macos-app-icon=./BootstrapImages/AppIcon.icns \
    --disable-plugin=tk-inter \
    --clang \
    --lto=yes \
    --remove-output \
    --target="OrangeBlox" "./Apps/Scripts/OrangeBlox.py"
mv ./Apps/Building/OrangeBlox.app/Contents/MacOS/OrangeBlox ./Apps/Building/OrangeBlox.app/Contents/MacOS/OrangeBlox
cp ./Apps/Scripts/Nuitka/Info.plist ./Apps/Building/OrangeBlox.app/Contents/Info.plist

# Strip Package
printMessage "Stripping macOS Package.."
strip -S "./Apps/Building/OrangeBlox.app/Contents/MacOS/OrangeBlox" 2>/dev/null \;
strip -S "./Apps/Building/OrangeBlox.app/Contents/MacOS/Python" 2>/dev/null \;
find "./Apps/Building/OrangeBlox.app" -type f \( -name "*.so" -o -name "*.dylib" \) -exec strip -S {} 2>/dev/null \;

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
rm -rf ./Apps/Building/OrangeBlox.app/ ./Apps/Building/OrangeBlox.build/ ./Apps/Building/OrangeBlox.dist/ ./__pycache__/ ./Apps/Building/OrangeBlox/

# Done!
printMessage "Successfully rebuilt OrangeBlox!"
printMessage "Check the Apps folder for the generated ZIP file! File: ./Apps/OrangeBloxMac.zip"