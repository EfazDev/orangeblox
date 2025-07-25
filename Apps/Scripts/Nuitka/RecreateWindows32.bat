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
    --nofollow-import-to=unittest,test,distutils,setuptools,tkinter,urllib3,requests,numpy ^
    --include-data-files=PyKits.py=PyKits.py ^
    --include-data-files=Version.json=Version.json ^
    --msvc=latest ^
    --company-name=EfazDev ^
    --product-name=OrangeBlox ^
    --file-version=2.2.0 ^
    --product-version=2.2.0 ^
    --file-description="OrangeBlox" ^
    --copyright="Copyright (c) EfazDev" ^
    --output-dir="Apps" ^
    --windows-icon-from-ico=./BootstrapImages/AppIcon.ico ^
    --target="OrangeBlox" ^
    "./Apps/Scripts/OrangeBlox.py"

powershell -c "Write-Host 'Rebuild OrangeBlox: Compiling OrangePlayRoblox with Nuitka using Python..' -ForegroundColor Green"
rem Compile PlayRoblox (OrangePlayRoblox.py)
python -m nuitka ^
    --standalone ^
    --windows-console-mode=force ^
    --onefile ^
    --assume-yes-for-downloads ^
    --remove-output ^
    --enable-plugin=pylint-warnings ^
    --nofollow-import-to=unittest,test,distutils,setuptools,tkinter,urllib3,requests,numpy ^
    --include-data-files=PyKits.py=PyKits.py ^
    --include-data-files=Version.json=Version.json ^
    --msvc=latest ^
    --company-name=EfazDev ^
    --product-name="Play Roblox (OrangeBlox)" ^
    --file-version=2.2.0 ^
    --product-version=2.2.0 ^
    --file-description="Play Roblox" ^
    --copyright="Copyright (c) EfazDev" ^
    --output-dir="Apps" ^
    --windows-icon-from-ico=./BootstrapImages/AppIconPlayRoblox.ico ^
    --target="OrangePlayRoblox" ^
    "./Apps/Scripts/OrangePlayRoblox.py"

powershell -c "Write-Host 'Rebuild OrangeBlox: Compiling OrangeRunStudio with Nuitka using Python..' -ForegroundColor Green"
rem Compile RunStudio (OrangeRunStudio.py)
python -m nuitka ^
    --standalone ^
    --windows-console-mode=force ^
    --onefile ^
    --assume-yes-for-downloads ^
    --remove-output ^
    --enable-plugin=pylint-warnings ^
    --nofollow-import-to=unittest,test,distutils,setuptools,tkinter,urllib3,requests,numpy ^
    --include-data-files=PyKits.py=PyKits.py ^
    --include-data-files=Version.json=Version.json ^
    --msvc=latest ^
    --output-dir="Apps" ^
    --windows-icon-from-ico=./BootstrapImages/AppIconRunStudio.ico ^
    --company-name=EfazDev ^
    --product-name="Run Studio (OrangeBlox)" ^
    --file-version=2.2.0 ^
    --product-version=2.2.0 ^
    --file-description="Run Studio" ^
    --copyright="Copyright (c) EfazDev" ^
    --target="OrangeRunStudio" ^
    "./Apps/Scripts/OrangeRunStudio.py"

rem Create OrangeBloxWindows Folder
powershell -c "Write-Host 'Rebuild OrangeBlox: Creating OrangeBloxWindows.zip..' -ForegroundColor Green"
mkdir OrangeBloxWindows
mkdir OrangeBloxWindows\x86
if exist Apps\OrangeBlox.exe (
    move /Y Apps\OrangeBlox.exe OrangeBloxWindows\x86\OrangeBlox.exe
)
if exist Apps\OrangePlayRoblox.exe (
    move /Y Apps\OrangePlayRoblox.exe OrangeBloxWindows\x86\PlayRoblox.exe
)
if exist Apps\OrangeRunStudio.exe (
    move /Y Apps\OrangeRunStudio.exe OrangeBloxWindows\x86\RunStudio.exe
)
if "%1"=="signexe" (
    if exist OrangeBloxWindows\x86\OrangeBlox.exe (
        signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 "OrangeBloxWindows\x86\OrangeBlox.exe"
    )
    if exist OrangeBloxWindows\x86\PlayRoblox.exe (
        signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 "OrangeBloxWindows\x86\PlayRoblox.exe"
    )
    if exist OrangeBloxWindows\x86\RunStudio.exe (
        signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 "OrangeBloxWindows\x86\RunStudio.exe"
    )
)
powershell Compress-Archive -Path OrangeBloxWindows\* -Update -DestinationPath Apps\OrangeBloxWindows.zip
rmdir /S /Q OrangeBloxWindows

rem Cleaning Up
powershell -c "Write-Host 'Rebuild OrangeBlox: Cleaning Up..' -ForegroundColor Green"
rmdir /S /Q __pycache__ Apps\OrangeBlox build Apps\OrangeBlox.build Apps\OrangeBlox.dist Apps\OrangeBlox.onefile-build Apps\OrangePlayRoblox.build Apps\OrangePlayRoblox.dist Apps\OrangePlayRoblox.onefile-build Apps\OrangeRunStudio.build Apps\OrangeRunStudio.dist Apps\OrangeRunStudio.onefile-build > NUL 2>&1

powershell -c "Write-Host 'Rebuild OrangeBlox: Successfully rebuilt OrangeBlox!' -ForegroundColor Green"
powershell -c "Write-Host 'Rebuild OrangeBlox: Check the Apps folder for the generated ZIP file! File: Apps\OrangeBloxWindows.zip' -ForegroundColor Green"
endlocal