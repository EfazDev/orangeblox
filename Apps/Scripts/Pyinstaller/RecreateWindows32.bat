@echo off

rem Generate Main.py Hash
py Apps\Scripts\GenerateHash.py

rem Build Pyinstaller Package
powershell -c "Write-Host 'Rebuild OrangeBlox: Building Pyinstaller Package..' -ForegroundColor Green"
pyinstaller ./Apps/Scripts/Pyinstaller/OrangeBlox_Windows32.spec --clean --distpath Apps --noconfirm
timeout 2

rem Create OrangeBloxWindows Folder
powershell -c "Write-Host 'Rebuild OrangeBlox: Creating OrangeBloxWindows.zip..' -ForegroundColor Green"
mkdir OrangeBloxWindows
if exist Apps\OrangeBlox.exe (
    move /Y Apps\OrangeBlox.exe OrangeBloxWindows\OrangeBlox.exe
)
if exist Apps\OrangeBlox32.exe (
    move /Y Apps\OrangeBlox32.exe OrangeBloxWindows\OrangeBlox32.exe
)
if exist Apps\PlayRoblox.exe (
    move /Y Apps\PlayRoblox.exe OrangeBloxWindows\PlayRoblox.exe
)
if exist Apps\PlayRoblox32.exe (
    move /Y Apps\PlayRoblox32.exe OrangeBloxWindows\PlayRoblox32.exe
)
if exist Apps\RunStudio.exe (
    move /Y Apps\RunStudio.exe OrangeBloxWindows\RunStudio.exe
)
if exist Apps\RunStudio32.exe (
    move /Y Apps\RunStudio32.exe OrangeBloxWindows\RunStudio32.exe
)
if exist Apps\_internal (
    move /Y Apps\_internal OrangeBloxWindows\_internal
)
if exist Apps\OrangeBlox (
    if exist Apps\OrangeBlox\OrangeBlox.exe (
        move /Y Apps\OrangeBlox\OrangeBlox.exe OrangeBloxWindows\OrangeBlox.exe
    )
    if exist Apps\OrangeBlox\PlayRoblox.exe (
        move /Y Apps\OrangeBlox\PlayRoblox.exe OrangeBloxWindows\PlayRoblox.exe
    )
    if exist Apps\OrangeBlox\RunStudio.exe (
        move /Y Apps\OrangeBlox\RunStudio.exe OrangeBloxWindows\RunStudio.exe
    )
    if exist Apps\OrangeBlox\_internal (
        move /Y Apps\OrangeBlox\_internal OrangeBloxWindows\_internal
    )
)
if exist Apps\OrangeBlox32 (
    if exist Apps\OrangeBlox32\OrangeBlox32.exe (
        move /Y Apps\OrangeBlox32\OrangeBlox32.exe OrangeBloxWindows\OrangeBlox32.exe
    )
    if exist Apps\OrangeBlox32\PlayRoblox32.exe (
        move /Y Apps\OrangeBlox32\PlayRoblox32.exe OrangeBloxWindows\PlayRoblox32.exe
    )
    if exist Apps\OrangeBlox32\RunStudio32.exe (
        move /Y Apps\OrangeBlox32\RunStudio32.exe OrangeBloxWindows\RunStudio32.exe
    )
    if exist Apps\OrangeBlox32\_internal (
        move /Y Apps\OrangeBlox32\_internal OrangeBloxWindows\_internal32
    )
)
if "%2"=="signexe" (
    if exist OrangeBloxWindows\OrangeBlox.exe (
        signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 "OrangeBloxWindows\OrangeBlox.exe"
    )
    if exist OrangeBloxWindows\OrangeBlox32.exe (
        signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 "OrangeBloxWindows\OrangeBlox32.exe"
    )
    if exist OrangeBloxWindows\PlayRoblox.exe (
        signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 "OrangeBloxWindows\PlayRoblox.exe"
    )
    if exist OrangeBloxWindows\PlayRoblox32.exe (
        signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 "OrangeBloxWindows\PlayRoblox32.exe"
    )
    if exist OrangeBloxWindows\RunStudio.exe (
        signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 "OrangeBloxWindows\RunStudio.exe"
    )
    if exist OrangeBloxWindows\RunStudio32.exe (
        signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 "OrangeBloxWindows\RunStudio32.exe"
    )
)
powershell Compress-Archive -Path OrangeBloxWindows\* -Update -DestinationPath Apps\OrangeBloxWindows.zip
rmdir /S /Q OrangeBloxWindows

if not "%1"=="installer" (
    rem Run Installer
    powershell -c "Write-Host 'Rebuild OrangeBlox: Running Installer..' -ForegroundColor Green"
    py Install.py --rebuild-mode
)

rem Cleaning Up
powershell -c "Write-Host 'Rebuild OrangeBlox: Cleaning Up..' -ForegroundColor Green"
rmdir /S /Q __pycache__ Apps\OrangeBlox.exe Apps\OrangeBlox32.exe Apps\PlayRoblox.exe Apps\PlayRoblox32.exe Apps\RunStudio.exe Apps\RunStudio32.exe Apps\OrangeBlox Apps\OrangeBlox32 build > NUL 2>&1

powershell -c "Write-Host 'Rebuild OrangeBlox: Successfully rebuilt OrangeBlox!' -ForegroundColor Green"
powershell -c "Write-Host 'Rebuild OrangeBlox: Check the Apps folder for the generated ZIP file! File: Apps\OrangeBloxWindows.zip' -ForegroundColor Green"
@echo on