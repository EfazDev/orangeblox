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

powershell -c "Write-Host 'Rebuild OrangeBlox: Compiling OrangePlayRoblox with Java..' -ForegroundColor Green"
rem Compile PlayRoblox (OrangePlayRoblox.java)
javac ./Apps/Scripts/Java/OrangePlayRoblox.java
copy "Apps\Scripts\Java\OrangePlayRoblox.class" "Apps\Scripts\Java\Temporary\OrangePlayRoblox.class"
jar cfe Apps\Scripts\Java\Temporary\OrangePlayRoblox.jar OrangePlayRoblox Apps\Scripts\Java\Temporary\OrangePlayRoblox.class
jpackage --type exe --name OrangePlayRoblox --dest ..\..\..\..\Apps\Scripts\OrangePlayRoblox.exe --input . --main-jar Apps\Scripts\Java\Temporary\OrangePlayRoblox.jar --main-class OrangePlayRoblox --java-options "-Xmx512m"

endlocal
