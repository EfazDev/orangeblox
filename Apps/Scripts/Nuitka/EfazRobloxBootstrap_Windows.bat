@echo off
setlocal

rem Variables
set ICON_FILE=./Apps/Scripts/AppIcon.ico
set OUTPUT_DIR=dist
set EF_BOOTSTRAP=EfazRobloxBootstrap.py
set EF_BOOTSTRAP_PLAY=EfazRobloxBootstrapPlayRoblox.py

rem Check if the Python files exist
if not exist "%EF_BOOTSTRAP%" (
    echo Error: %EF_BOOTSTRAP% not found.
    exit /b 1
)

if not exist "%EF_BOOTSTRAP_PLAY%" (
    echo Error: %EF_BOOTSTRAP_PLAY% not found.
    exit /b 1
)

rem Compile EfazRobloxBootstrap
python3.12 -m nuitka --standalone --windows-console-mode=force --onefile --include-data-files=./Apps/Scripts/PipHandler.py=PipHandler.py --output-dir="dist" --windows-icon-from-ico="./Apps/Scripts/AppIcon.ico" --target="EfazRobloxBootstrap" "./Apps/Scripts/EfazRobloxBootstrap.py"

rem Compile PlayRoblox (EfazRobloxBootstrapPlayRoblox.py)
python3.12 -m nuitka --standalone --windows-console-mode=force --onefile --include-data-files=./Apps/Scripts/PipHandler.py=PipHandler.py --output-dir="dist" --windows-icon-from-ico="./Apps/Scripts/AppIcon.ico" --target="EfazRobloxBootstrapPlayRoblox" "./Apps/Scripts/EfazRobloxBootstrapPlayRoblox.py"

rem Optionally combine both executables in one folder
mkdir "%OUTPUT_DIR%\EfazRobloxBootstrap"
copy "%OUTPUT_DIR%\EfazRobloxBootstrap.exe" "%OUTPUT_DIR%\EfazRobloxBootstrap\"
copy "%OUTPUT_DIR%\EfazRobloxBootstrapPlayRoblox.exe" "%OUTPUT_DIR%\EfazRobloxBootstrap\"

endlocal
