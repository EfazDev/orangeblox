@echo off
setlocal enabledelayedexpansion
for /f "tokens=2 delims==" %%a in ('wmic os get caption /value 2^>nul') do (
    set "os_name=%%a"
)
for /f "tokens=*" %%i in ("%os_name%") do set "os_name=%%i"

set "arch=%PROCESSOR_ARCHITECTURE%"
echo "!os_name!" | find /i "Windows" >nul
if !errorlevel! equ 0 (
    if "%arch%"=="AMD64" (
        if "%PROCESSOR_ARCHITEW6432%"=="ARM64" (
            set "url=https://www.python.org/ftp/python/3.13.0/python-3.13.0-arm64.exe"
        ) else (
            set "url=https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe"
        )
    ) else (
        set "url=https://www.python.org/ftp/python/3.13.0/python-3.13.0.exe"
    )
    echo %esc%[38;5;202mInstall Python @ Download URL: !url!%esc%[0m
    if defined url (
        set "tmp_exe=%TEMP%\python-installer-%RANDOM%.exe"
        echo %esc%[38;5;202mInstall Python @ Generated Python Temp Path: !tmp_exe!%esc%[0m
        powershell -Command "(New-Object Net.WebClient).DownloadFile('!url!', '!tmp_exe!')"
        if exist "!tmp_exe!" (
            start "" "!tmp_exe!"
            echo %esc%[38;5;202mInstall Python @ Python installer has been executed: !tmp_exe!%esc%[0m
        ) else (
            echo %esc%[38;5;202mInstall Python @ Failed to download Python installer.%esc%[0m
        )
	timeout 5
    ) else (
        echo %esc%[38;5;202mInstall Python @ Failed to set download URL.%esc%[0m
    )
) else (
    echo %esc%[38;5;202mInstall Python @ Unsupported operating system: !os_name!%esc%[0m
)

endlocal
