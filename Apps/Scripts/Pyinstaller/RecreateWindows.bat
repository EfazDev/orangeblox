@echo off

rem Generate Main.py Hash
python Apps\Scripts\GenerateHash.py

rem Build Pyinstaller Package
powershell -c "Write-Host 'Rebuild OrangeBlox: Building Pyinstaller Package..' -ForegroundColor Green"
pyinstaller ./Apps/Scripts/Pyinstaller/OrangeBlox_Windows.spec --clean --distpath Apps/Building --noconfirm 
timeout 2

rem Create OrangeBloxWindows Folder
powershell -c "Write-Host 'Rebuild OrangeBlox: Creating OrangeBloxWindows.zip..' -ForegroundColor Green"
set "building_dir=Apps\Building"
set "arch=x64"
mkdir %building_dir%\OrangeBloxWindows
mkdir %building_dir%\OrangeBloxWindows\%arch%
if exist %building_dir%\OrangeBlox.exe (
    move /Y %building_dir%\OrangeBlox.exe %building_dir%\OrangeBloxWindows\%arch%\OrangeBlox.exe
)
if exist %building_dir%\_internal (
    move /Y %building_dir%\_internal %building_dir%\OrangeBloxWindows\%arch%\_internal
)
if exist %building_dir%\OrangeBlox (
    if exist %building_dir%\OrangeBlox\OrangeBlox.exe (
        move /Y %building_dir%\OrangeBlox\OrangeBlox.exe %building_dir%\OrangeBloxWindows\%arch%\OrangeBlox.exe
    )
    if exist %building_dir%\OrangeBlox\_internal (
        move /Y %building_dir%\OrangeBlox\_internal %building_dir%\OrangeBloxWindows\%arch%\_internal
    )
)
if exist %building_dir%\OrangeBloxWindows\%arch%\OrangeBlox.exe (
    signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 "%building_dir%\OrangeBloxWindows\%arch%\OrangeBlox.exe"
)
powershell Compress-Archive -Path %building_dir%\OrangeBloxWindows\* -Update -DestinationPath Apps\OrangeBloxWindows.zip
rmdir /S /Q %building_dir%\OrangeBloxWindows

rem Cleaning Up
powershell -c "Write-Host 'Rebuild OrangeBlox: Cleaning Up..' -ForegroundColor Green"
rmdir /S /Q __pycache__ %building_dir%\OrangeBlox.exe %building_dir%\OrangeBlox build > NUL 2>&1

powershell -c "Write-Host 'Rebuild OrangeBlox: Successfully rebuilt OrangeBlox!' -ForegroundColor Green"
powershell -c "Write-Host 'Rebuild OrangeBlox: Check the Apps folder for the generated ZIP file! File: Apps\OrangeBloxWindows.zip' -ForegroundColor Green"
@echo on