import sys
import os
import subprocess
import platform
from PipHandler import pip

def printMainMessage(mes):
    print(f"\033[38;5;255m{mes}\033[0m")

def printErrorMessage(mes):
    print(f"\033[38;5;196m{mes}\033[0m")

def printSuccessMessage(mes):
    print(f"\033[38;5;82m{mes}\033[0m")

def printWarnMessage(mes):
    print(f"\033[38;5;202m{mes}\033[0m")

def printDebugMessage(mes):
    print(f"\033[38;5;226m{mes}\033[0m")

if __name__ == "__main__":
    current_version = {"version": "1.4.3"}
    main_os = platform.system()
    direct_run = False
    args = sys.argv

    printWarnMessage("-----------")
    printWarnMessage("Welcome to Efaz's Roblox Bootstrap Loader!")
    printWarnMessage("Made by Efaz from efaz.dev!")
    printWarnMessage(f"v{current_version['version']}")
    printWarnMessage("-----------")
    printMainMessage("Determining System OS..")

    if main_os == "Darwin":
        if os.path.exists("/Applications/EfazRobloxBootstrap.app/Contents/MacOS/Efaz\'s Roblox Bootstrap.app/"):
            url_scheme_path = "/Applications/EfazRobloxBootstrap.app/Contents/Resources/URLSchemeExchange"
            with open(url_scheme_path, "w") as f:
                f.write("efaz-bootstrap://continue")
            printMainMessage(f"Created URL Exchange File: {url_scheme_path}")
            printMainMessage("Loading EfazRobloxBootstrap executable!")
            result = subprocess.run(["open", "-n", "-a", "/Applications/EfazRobloxBootstrap.app/Contents/MacOS/Efaz\'s Roblox Bootstrap.app/Contents/MacOS/EfazRobloxBootstrapMain"], cwd="/Applications/EfazRobloxBootstrap.app/Contents/Resources/", stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            if result.returncode == 0:
                printSuccessMessage(f"Bootstrap Run Success: {result.returncode}")
            else:
                printErrorMessage(f"Bootstrap Run Failed: {result.returncode}")
            sys.exit(0)
        else:
            printErrorMessage("Bootstrap Run Failed: App is not installed.")
    elif main_os == "Windows":
        generated_app_path = os.path.join(pip().getLocalAppData(), "EfazRobloxBootstrap")
        if os.path.exists(os.path.join(generated_app_path, "EfazRobloxBootstrap.exe")):
            url_scheme_path = os.path.join(generated_app_path, "URLSchemeExchange")
            with open(url_scheme_path, "w") as f:
                f.write("efaz-bootstrap://continue")
            printMainMessage(f"Created URL Exchange File: {url_scheme_path}")
            printMainMessage("Loading EfazRobloxBootstrap.exe!")
            result = subprocess.run(f'{os.path.join(generated_app_path, "EfazRobloxBootstrap.exe")}', shell=True)
            sys.exit(0)
        else:
            printErrorMessage("Bootstrap Run Failed: App is not installed.")
else:
    class EfazRobloxBootstrapNotModule(Exception):
        def __init__(self):            
            super().__init__("Efaz's Roblox Bootstrap is only a runable instance, not a module.")
    class EfazRobloxBootstrapInstallerNotModule(Exception):
        def __init__(self):            
            super().__init__("The installer for Efaz's Roblox Bootstrap is only a runable instance, not a module.")
    class EfazRobloxBootstrapLoaderNotModule(Exception):
        def __init__(self):            
            super().__init__("The loader for Efaz's Roblox Bootstrap is only a runable instance, not a module.")
    raise EfazRobloxBootstrapLoaderNotModule()