@echo off
setlocal

rem Variables
set ICON_FILE=./Apps/Scripts/AppIcon.ico
set OUTPUT_DIR=dist
set EF_BOOTSTRAP=EfazRobloxBootstrap.py
set EF_BOOTSTRAP_PLAY=EfazRobloxBootstrapPlayRoblox.py

rem Check if the Python files exist
if not exist "%EF_BOOTSTRAP%" (
    echo %esc%[38;5;202mRebuild EfazRobloxBootstrap @ Error: %EF_BOOTSTRAP% not found.%esc%[0m
    exit /B 1
)

if not exist "%EF_BOOTSTRAP_PLAY%" (
    echo %esc%[38;5;202mRebuild EfazRobloxBootstrap @ Error: %EF_BOOTSTRAP_PLAY% not found.%esc%[0m
    exit /B 1
)

echo %esc%[38;5;202mRebuild EfazRobloxBootstrap @ Compiling EfazRobloxBootstrap with Nuitka using Python 3.12..%esc%[0m
rem Compile EfazRobloxBootstrap
python3.12 -m nuitka --standalone --windows-console-mode=force --onefile --include-data-files=./Apps/Scripts/PipHandler.py=PipHandler.py --output-dir="dist" --windows-icon-from-ico="./Apps/Scripts/AppIcon.ico" --target="EfazRobloxBootstrap" "./Apps/Scripts/EfazRobloxBootstrap.py"

echo %esc%[38;5;202mRebuild EfazRobloxBootstrap @ Compiling EfazRobloxBootstrapPlayRoblox with Nuitka using Python 3.12..%esc%[0m
rem Compile PlayRoblox (EfazRobloxBootstrapPlayRoblox.py)
python3.12 -m nuitka --standalone --windows-console-mode=force --onefile --include-data-files=./Apps/Scripts/PipHandler.py=PipHandler.py --output-dir="dist" --windows-icon-from-ico="./Apps/Scripts/AppIcon.ico" --target="EfazRobloxBootstrapPlayRoblox" "./Apps/Scripts/EfazRobloxBootstrapPlayRoblox.py"

echo %esc%[38;5;202mRebuild EfazRobloxBootstrap @ Combining PlayRoblox.exe and EfazRobloxBootstrap.exe into one folder..%esc%[0m
rem Optionally combine both executables in one folder
mkdir "%OUTPUT_DIR%\EfazRobloxBootstrap"
copy "%OUTPUT_DIR%\EfazRobloxBootstrap.exe" "%OUTPUT_DIR%\EfazRobloxBootstrap\"
copy "%OUTPUT_DIR%\EfazRobloxBootstrapPlayRoblox.exe" "%OUTPUT_DIR%\EfazRobloxBootstrap\"

endlocal
