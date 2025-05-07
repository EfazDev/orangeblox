@echo off
setlocal

rem Generate Main.py Hash
python Apps\Scripts\GenerateHash.py

powershell -c "Write-Host 'Rebuild OrangeBlox: Compiling OrangeBlox with Nuitka using Python..' -ForegroundColor Green"
rem Compile OrangeBlox
call python -m nuitka --standalone --windows-console-mode=force --onefile --include-data-files=PipHandler.py=PipHandler.py --include-data-files=Version.json=Version.json --output-dir="Apps" --windows-icon-from-ico=./BootstrapImages/AppIcon.ico --target="OrangeBlox" "./Apps/Scripts/OrangeBlox.py"

powershell -c "Write-Host 'Rebuild OrangeBlox: Compiling OrangePlayRoblox with Nuitka using Python..' -ForegroundColor Green"
rem Compile PlayRoblox (OrangePlayRoblox.py)
call python -m nuitka --standalone --windows-console-mode=force --onefile --include-data-files=PipHandler.py=PipHandler.py --include-data-files=Version.json=Version.json --output-dir="Apps" --windows-icon-from-ico=./BootstrapImages/AppIconPlayRoblox.ico --target="OrangePlayRoblox" "./Apps/Scripts/OrangePlayRoblox.py"

powershell -c "Write-Host 'Rebuild OrangeBlox: Compiling OrangeRunStudio with Nuitka using Python..' -ForegroundColor Green"
rem Compile RunStudio (OrangeRunStudio.py)
call python -m nuitka --standalone --windows-console-mode=force --onefile --include-data-files=PipHandler.py=PipHandler.py --include-data-files=Version.json=Version.json --output-dir="Apps" --windows-icon-from-ico=./BootstrapImages/AppIconRunStudio.ico --target="OrangeRunStudio" "./Apps/Scripts/OrangeRunStudio.py"

rem Create OrangeBloxWindows Folder
powershell -c "Write-Host 'Rebuild OrangeBlox: Creating OrangeBloxWindows.zip..' -ForegroundColor Green"
mkdir OrangeBloxWindows
if exist Apps\OrangeBlox.exe (
    move /Y Apps\OrangeBlox.exe OrangeBloxWindows\OrangeBlox32.exe
)
if exist Apps\OrangePlayRoblox.exe (
    move /Y Apps\OrangePlayRoblox.exe OrangeBloxWindows\PlayRoblox32.exe
)
if exist Apps\OrangeRunStudio.exe (
    move /Y Apps\OrangeRunStudio.exe OrangeBloxWindows\RunStudio32.exe
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
    python Install.py --rebuild-mode
)

rem Cleaning Up
powershell -c "Write-Host 'Rebuild OrangeBlox: Cleaning Up..' -ForegroundColor Green"
rmdir /S /Q __pycache__ Apps\OrangeBlox Apps\OrangeBlox32 build Apps\OrangeBlox32 Apps\OrangeBlox.build Apps\OrangeBlox.dist Apps\OrangeBlox.onefile-build Apps\OrangePlayRoblox.build Apps\OrangePlayRoblox.dist Apps\OrangePlayRoblox.onefile-build Apps\OrangeRunStudio.build Apps\OrangeRunStudio.dist Apps\OrangeRunStudio.onefile-build

powershell -c "Write-Host 'Rebuild OrangeBlox: Successfully rebuilt OrangeBlox!' -ForegroundColor Green"
powershell -c "Write-Host 'Rebuild OrangeBlox: Check the Apps folder for the generated ZIP file! File: Apps\OrangeBloxWindows.zip' -ForegroundColor Green"
endlocal