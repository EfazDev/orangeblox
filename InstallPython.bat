@echo off
setlocal enabledelayedexpansion
for /f "tokens=2 delims==" %%a in ('wmic os get caption /value 2\033>nul') do (
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
    powershell -c "Write-Host 'Install Python: Download URL: !url!' -ForegroundColor Green"
    if defined url (
        set "tmp_exe=%TEMP%\python-installer-%RANDOM%.exe"
        powershell -c "Write-Host 'Install Python: Generated Python Temp Path: !tmp_exe!' -ForegroundColor Green"
        powershell -Command "(New-Object Net.WebClient).DownloadFile('!url!', '!tmp_exe!')"
        if exist "!tmp_exe!" (
            start "" "!tmp_exe!"
            powershell -c "Write-Host 'Install Python: Python installer has been executed: !tmp_exe!' -ForegroundColor Green"
        ) else (
            powershell -c "Write-Host 'Install Python: Failed to download Python installer.' -ForegroundColor Green"
        )
	timeout 5
    ) else (
        powershell -c "Write-Host 'Install Python: Failed to set download URL.' -ForegroundColor Green"
    )
) else (
    powershell -c "Write-Host 'Install Python: Unsupported operating system: !os_name!' -ForegroundColor Green"
)

endlocal
