import sys
import os
import subprocess
import platform
import uuid
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
    current_version = {"version": "1.5.8"}
    main_os = platform.system()
    direct_run = False
    args = sys.argv
    generated_app_id = str(uuid.uuid4())
    app_path = ""
    pip_class = pip()

    printWarnMessage("-----------")
    printWarnMessage("Welcome to Efaz's Roblox Bootstrap Loader (Play Roblox)!")
    printWarnMessage("Made by Efaz from efaz.dev!")
    printWarnMessage(f"v{current_version['version']}")
    printWarnMessage("-----------")
    printMainMessage("Determining System OS..")

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        if main_os == "Windows":
            app_path = os.path.dirname(sys.executable)
        else:
            app_path = os.path.abspath(os.path.join("../", os.path.dirname(sys.executable)))

    if main_os == "Darwin":
        if os.path.exists(os.path.join(app_path, "LocatedAppDirectory")):
            with open(os.path.join(app_path, "LocatedAppDirectory"), "r") as f:
                app_path = f.read()
        if os.path.exists(os.path.join(app_path, "/MacOS/Efaz\'s Roblox Bootstrap.app/")):
            url_scheme_path = os.path.join(app_path, "/Resources/URLSchemeExchange")
            with open(url_scheme_path, "w") as f:
                f.write("efaz-bootstrap://continue")
            printMainMessage(f"Created URL Exchange File: {url_scheme_path}")
            if not pip_class.getIfProcessIsOpened("/Terminal.app/Contents/MacOS/Terminal"):
                printMainMessage("Opening Terminal.app in order for console to show..")
                subprocess.Popen(f'open -j -F -a /System/Applications/Utilities/Terminal.app', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

            printMainMessage("Loading EfazRobloxBootstrap executable!")
            result = subprocess.run(f'open -n -a "{app_path}/MacOS/Efaz\'s Roblox Bootstrap.app/Contents/MacOS/EfazRobloxBootstrapMain"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, shell=True)
            if result.returncode == 0:
                printSuccessMessage(f"Bootstrap Launch Success: {result.returncode}")
            else:
                printErrorMessage(f"Bootstrap Launch Failed: {result.returncode}")
            sys.exit(0)
        else:
            printErrorMessage("Bootstrap Launch Failed: App is not installed.")
            sys.exit(1)
    elif main_os == "Windows":
        if os.path.exists(os.path.join(app_path, "EfazRobloxBootstrap.exe")):
            url_scheme_path = os.path.join(app_path, "URLSchemeExchange")
            with open(url_scheme_path, "w") as f:
                f.write("efaz-bootstrap://continue")
            printMainMessage(f"Created URL Exchange File: {url_scheme_path}")
            printMainMessage("Loading EfazRobloxBootstrap.exe!")
            result = subprocess.run(f'{os.path.join(app_path, "EfazRobloxBootstrap.exe")}')
            sys.exit(0)
        else:
            printErrorMessage("Bootstrap Launch Failed: App is not installed.")
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