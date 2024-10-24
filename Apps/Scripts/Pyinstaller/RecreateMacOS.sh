#!/bin/bash

printMessage() {
    local message=$1
    echo "\033[38;5;202mRebuild EfazRobloxBootstrap @ ${message}\033[0m"
}

# Remove Existing EfazRobloxBootstrapMac.zip
printMessage "Removing Existing EfazRobloxBootstrapMac.zip.."
rm ./Apps/EfazRobloxBootstrapMac.zip

# Build Pyinstaller Package
printMessage "Building Pyinstaller Package.."
pyinstaller ./Apps/Scripts/Pyinstaller/EfazRobloxBootstrap.spec --distpath Apps --noconfirm

# Create EfazRobloxBootstrapMac.zip
printMessage "Creating EfazRobloxBootstrapMac.zip.."
zip -r -y ./Apps/EfazRobloxBootstrapMac.zip "./Apps/EfazRobloxBootstrap.app" "./Apps/Play Roblox.app" "./Apps/EfazRobloxBootstrapLoad.app" 

# Remove Build and EfazRobloxBootstrapLoad folder
rm -rf ./build/ ./Apps/EfazRobloxBootstrapLoad/ 

# Install EfazRobloxBootstrap
printMessage "Running Installer.."
python3 Install.py --rebuild-mode

# Clean Up Apps
printMessage "Cleaning Up.."
rm -rf ./Apps/EfazRobloxBootstrap.app/ ./Apps/EfazRobloxBootstrapLoad.app/ ./Apps/EfazRobloxBootstrap/ ./__pycache__/

printMessage "Successfully rebuilt EfazRobloxBootstrap!"
printMessage "Check the Apps folder for the generated ZIP file! File: ./Apps/EfazRobloxBootstrapMac.zip"
read -p "> "