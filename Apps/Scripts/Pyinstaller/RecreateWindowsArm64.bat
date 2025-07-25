@echo off

rem Generate Main.py Hash
python Apps\Scripts\GenerateHash.py

rem Build Pyinstaller Package
powershell -c "Write-Host 'Rebuild OrangeBlox: Building Pyinstaller Package..' -ForegroundColor Green"
pyinstaller ./Apps/Scripts/Pyinstaller/OrangeBlox_Windows.spec --clean --distpath Apps --noconfirm 
timeout 2

rem Create OrangeBloxWindows Folder
powershell -c "Write-Host 'Rebuild OrangeBlox: Creating OrangeBloxWindows.zip..' -ForegroundColor Green"
mkdir OrangeBloxWindows
mkdir OrangeBloxWindows\arm64
if exist Apps\OrangeBlox.exe (
    move /Y Apps\OrangeBlox.exe OrangeBloxWindows\arm64\OrangeBlox.exe
)
if exist Apps\PlayRoblox.exe (
    move /Y Apps\PlayRoblox.exe OrangeBloxWindows\arm64\PlayRoblox.exe
)
if exist Apps\RunStudio.exe (
    move /Y Apps\RunStudio.exe OrangeBloxWindows\arm64\RunStudio.exe
)
if exist Apps\_internal (
    move /Y Apps\_internal OrangeBloxWindows\arm64\_internal
)
if exist Apps\OrangeBlox (
    if exist Apps\OrangeBlox\OrangeBlox.exe (
        move /Y Apps\OrangeBlox\OrangeBlox.exe OrangeBloxWindows\arm64\OrangeBlox.exe
    )
    if exist Apps\OrangeBlox\PlayRoblox.exe (
        move /Y Apps\OrangeBlox\PlayRoblox.exe OrangeBloxWindows\arm64\PlayRoblox.exe
    )
    if exist Apps\OrangeBlox\RunStudio.exe (
        move /Y Apps\OrangeBlox\RunStudio.exe OrangeBloxWindows\arm64\RunStudio.exe
    )
    if exist Apps\OrangeBlox\_internal (
        move /Y Apps\OrangeBlox\_internal OrangeBloxWindows\arm64\_internal
    )
)
if "%1"=="signexe" (
    if exist OrangeBloxWindows\arm64\OrangeBlox.exe (
        signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 "OrangeBloxWindows\arm64\OrangeBlox.exe"
    )
    if exist OrangeBloxWindows\arm64\PlayRoblox.exe (
        signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 "OrangeBloxWindows\arm64\PlayRoblox.exe"
    )
    if exist OrangeBloxWindows\arm64\RunStudio.exe (
        signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 "OrangeBloxWindows\arm64\RunStudio.exe"
    )
)
powershell Compress-Archive -Path OrangeBloxWindows\* -Update -DestinationPath Apps\OrangeBloxWindows.zip
rmdir /S /Q OrangeBloxWindows

rem Cleaning Up
powershell -c "Write-Host 'Rebuild OrangeBlox: Cleaning Up..' -ForegroundColor Green"
rmdir /S /Q __pycache__ Apps\OrangeBlox.exe Apps\PlayRoblox.exe Apps\RunStudio.exe Apps\OrangeBlox build > NUL 2>&1

powershell -c "Write-Host 'Rebuild OrangeBlox: Successfully rebuilt OrangeBlox!' -ForegroundColor Green"
powershell -c "Write-Host 'Rebuild OrangeBlox: Check the Apps folder for the generated ZIP file! File: Apps\OrangeBloxWindows.zip' -ForegroundColor Green"
@echo on