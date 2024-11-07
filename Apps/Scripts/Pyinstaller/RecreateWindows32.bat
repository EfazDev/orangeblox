@echo off

rem Build Pyinstaller Package
echo \033[38;5;202mRebuild EfazRobloxBootstrap @ Building Pyinstaller Package..\033[0m
pyinstaller ./Apps/Scripts/Pyinstaller/EfazRobloxBootstrap_Windows32.spec --clean --distpath Apps --noconfirm
timeout 3

rem Create EfazRobloxBootstrapWindows Folder
echo \033[38;5;202mRebuild EfazRobloxBootstrap @ Creating EfazRobloxBootstrapWindows.zip..\033[0m
mkdir EfazRobloxBootstrapWindows
if exist Apps\EfazRobloxBootstrap\ (
    xcopy /e Apps\EfazRobloxBootstrap\ EfazRobloxBootstrapWindows\EfazRobloxBootstrap\
)
if exist Apps\EfazRobloxBootstrap32\ (
    xcopy /e Apps\EfazRobloxBootstrap32\ EfazRobloxBootstrapWindows\EfazRobloxBootstrap32\
)
if exist EfazRobloxBootstrapWindows\EfazRobloxBootstrap\PlayRoblox.exe (
    move /Y EfazRobloxBootstrapWindows\EfazRobloxBootstrap\PlayRoblox.exe EfazRobloxBootstrapWindows\PlayRoblox.exe
)
if exist EfazRobloxBootstrapWindows\EfazRobloxBootstrap32\PlayRoblox32.exe (
    move /Y EfazRobloxBootstrapWindows\EfazRobloxBootstrap32\PlayRoblox32.exe EfazRobloxBootstrapWindows\PlayRoblox32.exe
)
powershell Compress-Archive -Path EfazRobloxBootstrapWindows\* -Update -DestinationPath Apps\EfazRobloxBootstrapWindows.zip
rmdir /S /Q EfazRobloxBootstrapWindows

rem Run Installer
echo \033[38;5;202mRebuild EfazRobloxBootstrap @ Running Installer..\033[0m
python Install.py --rebuild-mode

rem Cleaning Up
echo \033[38;5;202mRebuild EfazRobloxBootstrap @ Cleaning Up..\033[0m
rmdir /S /Q __pycache__ Apps\EfazRobloxBootstrap Apps\EfazRobloxBootstrap32 build

echo \033[38;5;202mRebuild EfazRobloxBootstrap @ Successfully rebuilt EfazRobloxBootstrap!\033[0m
echo \033[38;5;202mRebuild EfazRobloxBootstrap @ Check the Apps folder for the generated ZIP file! File: Apps\EfazRobloxBootstrapWindows.zip\033[0m
set /p aaaaaa="> "

@echo on