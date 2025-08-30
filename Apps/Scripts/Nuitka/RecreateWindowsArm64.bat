@echo off
setlocal

rem Generate Main.py Hash
python Apps\Scripts\GenerateHash.py

powershell -c "Write-Host 'Rebuild OrangeBlox: Compiling OrangeBlox with Nuitka using Python..' -ForegroundColor Green"
rem Compile OrangeBlox
python -m nuitka ^
    --standalone ^
    --windows-console-mode=force ^
    --onefile ^
    --assume-yes-for-downloads ^
    --remove-output ^
    --enable-plugin=pylint-warnings ^
    --nofollow-import-to=unittest,test,distutils,setuptools,tkinter,urllib3,requests,numpy,site ^
    --include-data-files=PyKits.py=PyKits.py ^
    --include-data-files=Version.json=Version.json ^
    --msvc=latest ^
    --company-name=EfazDev ^
    --product-name=OrangeBlox ^
    --file-version=2.3.0 ^
    --product-version=2.3.0 ^
    --file-description="OrangeBlox" ^
    --copyright="Copyright (c) EfazDev" ^
    --output-dir="Apps/Building" ^
    --windows-icon-from-ico=./BootstrapImages/AppIcon.ico ^
    --target="OrangeBlox" ^
    "./Apps/Scripts/OrangeBlox.py"

rem Create OrangeBloxWindows Folder
set 'arch=arm64'
powershell -c "Write-Host 'Rebuild OrangeBlox: Creating OrangeBloxWindows.zip..' -ForegroundColor Green"
mkdir Apps\Building\OrangeBloxWindows
mkdir Apps\Building\OrangeBloxWindows\%arch%
if exist Apps\Building\OrangeBlox.exe (
    move /Y Apps\Building\OrangeBlox.exe Apps\Building\OrangeBloxWindows\%arch%\OrangeBlox.exe
)
if exist Apps\Building\OrangeBloxWindows\%arch%\OrangeBlox.exe (
    signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 "Apps\Building\OrangeBloxWindows\%arch%\OrangeBlox.exe"
)
powershell Compress-Archive -Path Apps\Building\OrangeBloxWindows\* -Update -DestinationPath Apps\OrangeBloxWindows.zip
rmdir /S /Q Apps\Building\OrangeBloxWindows

rem Cleaning Up
powershell -c "Write-Host 'Rebuild OrangeBlox: Cleaning Up..' -ForegroundColor Green"
rmdir /S /Q __pycache__ Apps\OrangeBlox build Apps\OrangeBlox.build Apps\OrangeBlox.dist Apps\OrangeBlox.onefile-build > NUL 2>&1

powershell -c "Write-Host 'Rebuild OrangeBlox: Successfully rebuilt OrangeBlox!' -ForegroundColor Green"
powershell -c "Write-Host 'Rebuild OrangeBlox: Check the Apps folder for the generated ZIP file! File: Apps\OrangeBloxWindows.zip' -ForegroundColor Green"
endlocal