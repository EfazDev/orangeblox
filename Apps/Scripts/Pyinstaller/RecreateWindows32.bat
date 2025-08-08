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
mkdir OrangeBloxWindows\x86
if exist Apps\OrangeBlox.exe (
    move /Y Apps\OrangeBlox.exe OrangeBloxWindows\x86\OrangeBlox.exe
)
if exist Apps\_internal (
    move /Y Apps\_internal OrangeBloxWindows\x86\_internal
)
if exist Apps\OrangeBlox (
    if exist Apps\OrangeBlox\OrangeBlox.exe (
        move /Y Apps\OrangeBlox\OrangeBlox.exe OrangeBloxWindows\x86\OrangeBlox.exe
    )
    if exist Apps\OrangeBlox\_internal (
        move /Y Apps\OrangeBlox\_internal OrangeBloxWindows\x86\_internal
    )
)
if exist OrangeBloxWindows\x86\OrangeBlox.exe (
    signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 "OrangeBloxWindows\x86\OrangeBlox.exe"
)
powershell Compress-Archive -Path OrangeBloxWindows\* -Update -DestinationPath Apps\OrangeBloxWindows.zip
rmdir /S /Q OrangeBloxWindows

rem Cleaning Up
powershell -c "Write-Host 'Rebuild OrangeBlox: Cleaning Up..' -ForegroundColor Green"
rmdir /S /Q __pycache__ Apps\OrangeBlox.exe Apps\OrangeBlox build > NUL 2>&1

powershell -c "Write-Host 'Rebuild OrangeBlox: Successfully rebuilt OrangeBlox!' -ForegroundColor Green"
powershell -c "Write-Host 'Rebuild OrangeBlox: Check the Apps folder for the generated ZIP file! File: Apps\OrangeBloxWindows.zip' -ForegroundColor Green"
@echo on