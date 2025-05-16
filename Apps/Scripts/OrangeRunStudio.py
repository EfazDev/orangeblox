import sys
import os
import subprocess
import platform
import uuid
import logging
import datetime
from PipHandler import pip

def printMainMessage(mes): print(f"\033[38;5;255m{mes}\033[0m"); logging.info(mes)
def printErrorMessage(mes): print(f"\033[38;5;196m{mes}\033[0m"); logging.error(mes)
def printSuccessMessage(mes): print(f"\033[38;5;82m{mes}\033[0m"); logging.info(mes)
def printWarnMessage(mes): print(f"\033[38;5;202m{mes}\033[0m"); logging.warning(mes)
def printDebugMessage(mes): print(f"\033[38;5;226m{mes}\033[0m"); logging.debug(mes)
def setLoggingHandler(handler_name):
    global app_path
    global main_os
    log_path = os.path.join(app_path, "Logs")
    if main_os == "Darwin": log_path = os.path.join(pip_class.getLocalAppData(), "Logs", "OrangeBlox")
    if not os.path.exists(log_path): os.makedirs(log_path)
    sys.stdout.reconfigure(encoding='utf-8')
    logging.basicConfig(filename=os.path.join(log_path, f'OrangeBlox_{handler_name}_{datetime.datetime.now().strftime("%B_%d_%Y_%H_%M_%S_%f")}.log'), level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
    return True

if __name__ == "__main__":
    current_version = {"version": "2.0.1"}
    main_os = platform.system()
    direct_run = False
    args = sys.argv
    generated_app_id = str(uuid.uuid4())
    app_path = ""
    pip_class = pip()
    logging_config = setLoggingHandler("OrangeRunStudio")

    printWarnMessage("-----------")
    printWarnMessage("Welcome to OrangeBlox Loader (Run Studio) 🍊!")
    printWarnMessage("Made by Efaz from efaz.dev!")
    printWarnMessage(f"v{current_version['version']}")
    printWarnMessage("-----------")
    printMainMessage("Determining System OS..")

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        if main_os == "Windows": app_path = os.path.dirname(sys.executable)
        else: app_path = os.path.abspath(os.path.join("../", os.path.dirname(sys.executable)))
    else:
        if main_os == "Windows": app_path = os.path.dirname(sys.argv[0])
        else: app_path = os.path.abspath(os.path.join("../", os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    if main_os == "Darwin":
        if os.path.exists(os.path.join(app_path, "LocatedAppDirectory")):
            with open(os.path.join(app_path, "LocatedAppDirectory"), "r", encoding="utf-8") as f:
                app_path = f.read()
        if os.path.exists(os.path.join(app_path, "/Contents/MacOS/OrangeBlox.app/")):
            url_scheme_path = os.path.join(app_path, "/Resources/URLSchemeExchange")
            with open(url_scheme_path, "w", encoding="utf-8") as f:
                f.write("orangeblox://run-studio")
            printMainMessage(f"Created URL Exchange File: {url_scheme_path}")
            if not pip_class.getIfProcessIsOpened("/Terminal.app/Contents/MacOS/Terminal"):
                printMainMessage("Opening Terminal.app in order for console to show..")
                subprocess.Popen(f'open -j -F -a /System/Applications/Utilities/Terminal.app', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

            printMainMessage("Loading OrangeBlox executable!")
            result = subprocess.run(f'open -n -a "{app_path}/Contents/MacOS/OrangeBlox.app/Contents/MacOS/OrangeBloxMain"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, shell=True)
            if result.returncode == 0:
                printSuccessMessage(f"Bootstrap Launch Success: {result.returncode}")
            else:
                printErrorMessage(f"Bootstrap Launch Failed: {result.returncode}")
            sys.exit(0)
        else:
            printErrorMessage("Bootstrap Launch Failed: App is not installed.")
            sys.exit(1)
    elif main_os == "Windows":
        local_app_data = pip_class.getLocalAppData()
        if os.path.exists(os.path.join(app_path, "OrangeBlox.exe")):
            url_scheme_path = os.path.join(app_path, "URLSchemeExchange")
            with open(url_scheme_path, "w", encoding="utf-8") as f:
                f.write("orangeblox://run-studio")
            printMainMessage(f"Created URL Exchange File: {url_scheme_path}")
            printMainMessage("Loading OrangeBlox.exe!")
            result = subprocess.run(f'{os.path.join(app_path, "OrangeBlox.exe")}')
            sys.exit(0)
        elif os.path.exists(os.path.join(app_path, "RobloxStudioBetaPlayRobloxRestart.txt")):
            installed_path = open(os.path.join(app_path, "RobloxStudioBetaPlayRobloxRestart.txt"), "r", encoding="utf-8").read()
            url_scheme_path = os.path.join(installed_path, "URLSchemeExchange")
            with open(url_scheme_path, "w", encoding="utf-8") as f:
                f.write("orangeblox://run-studio")
            printMainMessage(f"Created URL Exchange File: {url_scheme_path}")
            printMainMessage("Loading OrangeBlox.exe!")
            result = subprocess.run(f'{os.path.join(installed_path, "OrangeBlox.exe")}')
            sys.exit(0)
        else:
            printErrorMessage("Bootstrap Launch Failed: App is not installed.")
            sys.exit(1)
else:
    class OrangeBloxNotModule(Exception):
        def __init__(self): super().__init__("OrangeBlox is only a runable instance, not a module.")
    class OrangeBloxInstallerNotModule(Exception):
        def __init__(self): super().__init__("The installer for OrangeBlox is only a runable instance, not a module.")
    class OrangeBloxLoaderNotModule(Exception):
        def __init__(self): super().__init__("The loader for OrangeBlox is only a runable instance, not a module.")
    raise OrangeBloxLoaderNotModule()