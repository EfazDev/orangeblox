import sys
import os
import subprocess
import platform

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
    current_version = {"version": "1.3.0"}
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
        if os.path.exists("/Applications/EfazRobloxBootstrap.app/"):
            if len(args) > 1:
                url_scheme_path = "/Applications/EfazRobloxBootstrap.app/Contents/Resources/URLSchemeExchange"
                with open(url_scheme_path, "w") as f:
                    f.write(args[1])
                printMainMessage(f"Created URL Exchange File: {url_scheme_path}")
            printMainMessage("Loading EfazRobloxBootstrap executable!")
            os.system("open -n -a /Applications/EfazRobloxBootstrap.app")
            printSuccessMessage(f"Bootstrap Loader Run Success: 0")
            sys.exit(0)
        else:
            printErrorMessage("Bootstrap Run Failed: App is not installed.")
            sys.exit(1)
    elif main_os == "Windows":
        generated_app_path = os.path.join(os.getenv('LOCALAPPDATA'), "EfazRobloxBootstrap")
        if os.path.exists(os.path.join(generated_app_path, "EfazRobloxBootstrap.exe")):
            if len(args) > 1:
                url_scheme_path = os.path.join(generated_app_path, "URLSchemeExchange")
                with open(url_scheme_path, "w") as f:
                    f.write(args[1])
                printMainMessage(f"Created URL Exchange File: {url_scheme_path}")
            printMainMessage("Loading EfazRobloxBootstrap.exe!")
            os.system(f'start {os.path.join(generated_app_path, "EfazRobloxBootstrap.exe")}')
            sys.exit(0)
        else:
            printErrorMessage("Bootstrap Run Failed: App is not installed.")
            sys.exit(1)
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