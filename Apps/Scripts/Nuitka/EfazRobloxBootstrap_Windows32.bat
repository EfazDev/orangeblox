@echo off
setlocal

rem Variables
set ICON_FILE=./Apps/Scripts/AppIcon.ico
set OUTPUT_DIR=dist
set EF_BOOTSTRAP=EfazRobloxBootstrap.py
set EF_BOOTSTRAP_PLAY=EfazRobloxBootstrapPlayRoblox.py

rem Check if the Python files exist
if not exist "%EF_BOOTSTRAP%" (
    powershell -c "Write-Host 'Rebuild EfazRobloxBootstrap: Error: %EF_BOOTSTRAP% not found.' -ForegroundColor Green"
    exit /B 1
)

if not exist "%EF_BOOTSTRAP_PLAY%" (
    powershell -c "Write-Host 'Rebuild EfazRobloxBootstrap: Error: %EF_BOOTSTRAP_PLAY% not found.' -ForegroundColor Green"
    exit /B 1
)

powershell -c "Write-Host 'Rebuild EfazRobloxBootstrap: Compiling EfazRobloxBootstrap with Nuitka using Python 3.12..' -ForegroundColor Green"
rem Compile EfazRobloxBootstrap
python3.12 -m nuitka --standalone --windows-console-mode=force --onefile --include-data-files=./Apps/Scripts/PipHandler.py=PipHandler.py+./Version.json=Version.json --output-dir="dist" --windows-icon-from-ico="./Apps/Scripts/AppIcon.ico" --target="EfazRobloxBootstrap" "./Apps/Scripts/EfazRobloxBootstrap.py"

powershell -c "Write-Host 'Rebuild EfazRobloxBootstrap: Compiling EfazRobloxBootstrapPlayRoblox with Nuitka using Python 3.12..' -ForegroundColor Green"
rem Compile PlayRoblox (EfazRobloxBootstrapPlayRoblox.py)
python3.12 -m nuitka --standalone --windows-console-mode=force --onefile --include-data-files=./Apps/Scripts/PipHandler.py=PipHandler.py+./Version.json=Version.json --output-dir="dist" --windows-icon-from-ico="./Apps/Scripts/AppIcon.ico" --target="EfazRobloxBootstrapPlayRoblox" "./Apps/Scripts/EfazRobloxBootstrapPlayRoblox.py"

powershell -c "Write-Host 'Rebuild EfazRobloxBootstrap: Combining PlayRoblox.exe and EfazRobloxBootstrap.exe into one folder..' -ForegroundColor Green"
rem Optionally combine both executables in one folder
mkdir "%OUTPUT_DIR%\EfazRobloxBootstrap"
copy "%OUTPUT_DIR%\EfazRobloxBootstrap.exe" "%OUTPUT_DIR%\EfazRobloxBootstrap\"
copy "%OUTPUT_DIR%\EfazRobloxBootstrapPlayRoblox.exe" "%OUTPUT_DIR%\EfazRobloxBootstrap\"

endlocal
