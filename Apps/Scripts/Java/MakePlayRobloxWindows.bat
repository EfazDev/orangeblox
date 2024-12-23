@echo off
setlocal

rem Variables
set ICON_FILE=./Apps/Scripts/AppIcon.ico
set EF_BOOTSTRAP_PLAY=EfazRobloxBootstrapPlayRoblox.java

rem Check if the Java files exist
if not exist "%EF_BOOTSTRAP_PLAY%" (
    powershell -c "Write-Host 'Rebuild EfazRobloxBootstrap: Error: %EF_BOOTSTRAP_PLAY% not found.' -ForegroundColor Green"
    exit /B 1
)

powershell -c "Write-Host 'Rebuild EfazRobloxBootstrap: Creating a Temporary Folder..' -ForegroundColor Green"
rem Create a Temporary Folder
mkdir "Apps\Scripts\Java\Temporary"

powershell -c "Write-Host 'Rebuild EfazRobloxBootstrap: Compiling EfazRobloxBootstrapPlayRoblox with Java..' -ForegroundColor Green"
rem Compile PlayRoblox (EfazRobloxBootstrapPlayRoblox.java)
javac ./Apps/Scripts/Java/EfazRobloxBootstrapPlayRoblox.java
copy "Apps\Scripts\Java\EfazRobloxBootstrapPlayRoblox.class" "Apps\Scripts\Java\Temporary\EfazRobloxBootstrapPlayRoblox.class"
jar cfe Apps\Scripts\Java\Temporary\EfazRobloxBootstrapPlayRoblox.jar EfazRobloxBootstrapPlayRoblox Apps\Scripts\Java\Temporary\EfazRobloxBootstrapPlayRoblox.class
jpackage --type exe --name EfazRobloxBootstrapPlayRoblox --dest ..\..\..\..\Apps\Scripts\EfazRobloxBootstrapPlayRoblox.exe --input . --main-jar Apps\Scripts\Java\Temporary\EfazRobloxBootstrapPlayRoblox.jar --main-class EfazRobloxBootstrapPlayRoblox --java-options "-Xmx512m"

endlocal
