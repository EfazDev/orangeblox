#!/bin/bash

printMessage() {
    local message=$1
    echo "\033[38;5;202mRebuild EfazRobloxBootstrap @ ${message}\033[0m"
}

printMessage "Building Clang Package for EfazRobloxBootstrapPlayRoblox.."
clang++ -std=c++17 -arch x86_64 -arch arm64 -o EfazRobloxBootstrapPlayRoblox EfazRobloxBootstrapPlayRoblox.cpp
printMessage "Successfully rebuilt EfazRobloxBootstrapPlayRoblox!"