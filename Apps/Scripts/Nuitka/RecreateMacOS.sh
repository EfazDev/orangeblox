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
    --output-dir="./Apps" \
    --include-package-data=objc,Cocoa,Quartz \
    --nofollow-import-to=cryptography,OpenSSL,urllib3,requests,plyer \
    --macos-app-icon=./BootstrapImages/AppIcon.icns \
    --disable-plugin=tk-inter \
    --clang \
    --lto=yes \
    --remove-output \
    --target="OrangeBlox" "./Apps/Scripts/OrangeBlox.py"
mv ./Apps/OrangeBlox.app/Contents/MacOS/OrangeBlox ./Apps/OrangeBlox.app/Contents/MacOS/OrangeBlox
cp ./Apps/Scripts/Nuitka/Info.plist ./Apps/OrangeBlox.app/Contents/Info.plist

# Add Tkinter Data (Deprecated)
# printMessage "Adding Tk-inter Data.."
# ditto -xk './Apps/Scripts/Nuitka/macos_tkinter_data.zip' './Apps/Scripts/Nuitka/macos_tkinter_data'
# cp -R ./Apps/Scripts/Nuitka/macos_tkinter_data/_tcl_data ./Apps/OrangeBlox.app/Contents/Resources/_tcl_data
# cp -R ./Apps/Scripts/Nuitka/macos_tkinter_data/_tk_data ./Apps/OrangeBlox.app/Contents/Resources/_tk_data
# rm -rf './Apps/Scripts/Nuitka/macos_tkinter_data'

# Strip Package
printMessage "Stripping macOS Package.."
strip -S "./Apps/OrangeBlox.app/Contents/MacOS/OrangeBlox" 2>/dev/null \;
# strip -S "./Apps/OrangeBlox.app/Contents/MacOS/Tcl" 2>/dev/null \;
# strip -S "./Apps/OrangeBlox.app/Contents/MacOS/Tk" 2>/dev/null \;
strip -S "./Apps/OrangeBlox.app/Contents/MacOS/Python" 2>/dev/null \;
find "./Apps/OrangeBlox.app" -type f \( -name "*.so" -o -name "*.dylib" \) -exec strip -S {} 2>/dev/null \;

# Sign Package
printMessage "Signing Package.."
codesig1() {
    while true; do
    rm -rf ./Apps/OrangeBlox.app/Contents/_CodeSignature/
    if [ "$1" != "sudo" ]; then
        xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/OrangeBlox.app"
        xattr -dr com.apple.FinderInfo "./Apps/OrangeBlox.app"
        xattr -cr "./Apps/OrangeBlox.app"
        codesign -s ${1:-'-'} --force --all-architectures --timestamp --deep "./Apps/OrangeBlox.app" --entitlements "./Apps/Scripts/Resources/Entitlements.plist"
    else
        sudo xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/OrangeBlox.app"
        sudo xattr -dr com.apple.FinderInfo "./Apps/OrangeBlox.app"
        sudo xattr -cr "./Apps/OrangeBlox.app"
        sudo codesign -s ${1:-'-'} --force --all-architectures --timestamp --deep "./Apps/OrangeBlox.app" --entitlements "./Apps/Scripts/Resources/Entitlements.plist"
    fi
    STATUS=$?
        if [ $STATUS -eq 0 ]; then
            break
        fi
    done
}
codesig1 "$1"

# Create OrangeBloxMac.zip
printMessage "Creating OrangeBloxMac.zip.."
zip -r -y ./Apps/OrangeBloxMac.zip "./Apps/OrangeBlox.app" "./Apps/OrangePlayRoblox.app" "./Apps/OrangeLoader.app" "./Apps/OrangeRunStudio.app"

# Remove Build and OrangeLoader folder
printMessage "Partial Cleaning.."
rm -rf ./build/

# Clean Up Apps
printMessage "Cleaning Up.."
rm -rf ./Apps/OrangeBlox.app/ ./Apps/OrangeBlox.build/ ./Apps/OrangeBlox.dist/ ./__pycache__/ ./Apps/OrangeBlox/

# Done!
printMessage "Successfully rebuilt OrangeBlox!"
printMessage "Check the Apps folder for the generated ZIP file! File: ./Apps/OrangeBloxMac.zip"
