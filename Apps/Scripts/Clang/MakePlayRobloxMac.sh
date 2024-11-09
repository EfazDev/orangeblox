#!/bin/bash

printMessage() {
    local message=$1
    echo "\033[38;5;202mRebuild EfazRobloxBootstrapPlayRoblox @ ${message}\033[0m"
}

printMessage "Building Clang Package for EfazRobloxBootstrapPlayRoblox.."
clang++ -std=c++17 -arch x86_64 -g -arch arm64 -o EfazRobloxBootstrapPlayRoblox ./Apps/Scripts/Clang/EfazRobloxBootstrapPlayRoblox.cpp
mv EfazRobloxBootstrapPlayRoblox "./Apps/Play Roblox.app/Contents/MacOS/EfazRobloxBootstrapPlayRoblox"

printMessage "Cleaning Up.."
rm -rf ./EfazRobloxBootstrapPlayRoblox.dSYM/

printMessage "Successfully rebuilt EfazRobloxBootstrapPlayRoblox!"
printMessage "The executable has been moved to the Play Roblox.app bundle"
read -p "> "