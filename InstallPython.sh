#!/bin/bash
printMessage() {
    local message=$1
    echo "\033[38;5;202mInstall Python @ ${message}\033[0m"
}

ma_os=$(uname)
arch=$(uname -m)
if [ "$ma_os" = "Darwin" ]; then
    url="https://www.python.org/ftp/python/3.13.5/python-3.13.5-macos11.pkg"
    tmp_pkg=$(mktemp /tmp/python-installer.XXXXXX.pkg)
    curl -o "$tmp_pkg" "$url"
    if [ $? -eq 0 ]; then
        open "$tmp_pkg"
        printMessage "Python installer has been executed: $tmp_pkg"
    else
        printMessage "Failed to download Python installer."
    fi
elif [[ "$ma_os" == *"MINGW"* || "$ma_os" == *"CYGWIN"* || "$ma_os" == *"MSYS"* ]]; then
    if [ "$arch" = "x86_64" ]; then
        if [ "$PROCESSOR_ARCHITEW6432" == "ARM64" ]; then
            url="https://www.python.org/ftp/python/3.13.5/python-3.13.5-arm64.exe"
        else
            url="https://www.python.org/ftp/python/3.13.5/python-3.13.5-amd64.exe"
        fi
    else
        url="https://www.python.org/ftp/python/3.13.5/python-3.13.5.exe"
    fi
    tmp_exe=$(mktemp /tmp/python-installer.XXXXXX.exe)
    curl -o "$tmp_exe" "$url"
    if [ $? -eq 0 ]; then
        "$tmp_exe"
        printMessage "Python installer has been executed: $tmp_exe"
    else
        printMessage "Failed to download Python installer."
    fi
else
    printMessage "Unsupported operating system."
fi