@echo off
setlocal

rem Variables
set ICON_FILE=./BootstrapImages/AppIcon.ico
set EF_BOOTSTRAP_PLAY=OrangePlayRoblox.java

rem Check if the Java files exist
if not exist "%EF_BOOTSTRAP_PLAY%" (
    powershell -c "Write-Host 'Rebuild OrangeBlox: Error: %EF_BOOTSTRAP_PLAY% not found.' -ForegroundColor Green"
    exit /B 1
)

powershell -c "Write-Host 'Rebuild OrangeBlox: Creating a Temporary Folder..' -ForegroundColor Green"
rem Create a Temporary Folder
mkdir "Apps\Scripts\Java\Temporary"

powershell -c "Write-Host 'Rebuild OrangeBlox: Compiling OrangeRunStudio with Java..' -ForegroundColor Green"
rem Compile PlayRoblox (OrangeRunStudio.java)
javac ./Apps/Scripts/Java/OrangeRunStudio.java
copy "Apps\Scripts\Java\OrangeRunStudio.class" "Apps\Scripts\Java\Temporary\OrangeRunStudio.class"
jar cfe Apps\Scripts\Java\Temporary\OrangeRunStudio.jar OrangeRunStudio Apps\Scripts\Java\Temporary\OrangeRunStudio.class
jpackage --type exe --name OrangeRunStudio --dest ..\..\..\..\Apps\Scripts\OrangeRunStudio.exe --input . --main-jar Apps\Scripts\Java\Temporary\OrangeRunStudio.jar --main-class OrangeRunStudio --java-options "-Xmx512m"

endlocal
