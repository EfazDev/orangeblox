#!/bin/bash
printMessage() {
    local message=$1
    echo "\033[38;5;202mInstall Python @ ${message}\033[0m"
}

ma_os=$(uname)
arch=$(uname -m)
if [ "$ma_os" = "Darwin" ]; then
    url="https://www.python.org/ftp/python/3.14.6/python-3.14.6-macos11.pkg"
    tmp_pkg=$(mktemp /tmp/python-installer.XXXXXX.pkg)
    curl -o "$tmp_pkg" "$url"
    if [ $? -eq 0 ]; then
        open "$tmp_pkg"
        printMessage "Python installer has been executed: $tmp_pkg"
    else
        printMessage "Failed to download Python installer."
    fi
else
    printMessage "This script is for macOS only."
fi