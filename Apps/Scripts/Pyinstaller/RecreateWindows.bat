@echo off

rem Build Pyinstaller Package
powershell -c "Write-Host 'Rebuild EfazRobloxBootstrap: Building Pyinstaller Package..' -ForegroundColor Green"
pyinstaller ./Apps/Scripts/Pyinstaller/EfazRobloxBootstrap_Windows.spec --clean --distpath Apps --noconfirm 
timeout 3

rem Create EfazRobloxBootstrapWindows Folder
powershell -c "Write-Host 'Rebuild EfazRobloxBootstrap: Creating EfazRobloxBootstrapWindows.zip..' -ForegroundColor Green"
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
powershell -c "Write-Host 'Rebuild EfazRobloxBootstrap: Running Installer..' -ForegroundColor Green"
python Install.py --rebuild-mode

rem Cleaning Up
powershell -c "Write-Host 'Rebuild EfazRobloxBootstrap: Cleaning Up..' -ForegroundColor Green"
rmdir /S /Q __pycache__ Apps\EfazRobloxBootstrap Apps\EfazRobloxBootstrap32 build

powershell -c "Write-Host 'Rebuild EfazRobloxBootstrap: Successfully rebuilt EfazRobloxBootstrap!' -ForegroundColor Green"
powershell -c "Write-Host 'Rebuild EfazRobloxBootstrap: Check the Apps folder for the generated ZIP file! File: Apps\EfazRobloxBootstrapWindows.zip' -ForegroundColor Green"
set /p aaaaaa="> "

@echo on