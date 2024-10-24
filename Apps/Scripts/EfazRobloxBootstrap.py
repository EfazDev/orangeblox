import sys
import subprocess
import json
import threading
import os
import platform
import time
import traceback
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
    current_version = {"version": "1.3.0"}
    main_os = platform.system()
    direct_run = False
    args = sys.argv
    pip_class = pip()

    printWarnMessage("-----------")
    printWarnMessage("Welcome to Efaz's Roblox Bootstrap Loader!")
    printWarnMessage("Made by Efaz from efaz.dev!")
    printWarnMessage(f"v{current_version['version']}")
    printWarnMessage("-----------")
    printMainMessage("Determining System OS..")

    if main_os == "Darwin":
        filtered_args = ""
        loaded_json = True
        use_shell = False

        def displayMacOSNotification(title, message):
            import objc
            NSUserNotification = objc.lookUpClass("NSUserNotification")
            NSUserNotificationCenter = objc.lookUpClass("NSUserNotificationCenter")

            notification = NSUserNotification.alloc().init()
            notification.setTitle_(title)
            notification.setInformativeText_(message)
            center = NSUserNotificationCenter.defaultUserNotificationCenter()
            center.deliverNotification_(notification)

        printMainMessage(f"Loading Configuration File..")
        if os.path.exists("/Applications/EfazRobloxBootstrap.app/Contents/Resources/FastFlagConfiguration.json"):
            with open("/Applications/EfazRobloxBootstrap.app/Contents/Resources/FastFlagConfiguration.json", "r") as f:
                try:
                    fastFlagConfig = json.loads(f.read())
                except Exception as e:
                    loaded_json = False
        else:
            with open("FastFlagConfiguration.json", "r") as f:
                try:
                    fastFlagConfig = json.loads(f.read())
                except Exception as e:
                    loaded_json = False
                    
        if pip_class.pythonInstalled() == False: pip_class.pythonInstall()
        pythonExecutable = pip_class.findPython()
        if not pythonExecutable:
            printErrorMessage("Please install Python in order to run this bootstrap!")
            input("> ")
            sys.exit(1)

        execute_command = f'cd /Applications/EfazRobloxBootstrap.app/Contents/Resources/ && {pythonExecutable} Main.py && exit'
        printMainMessage(f"Loading Runner Command: {execute_command}")

        if len(args) > 1:
            filtered_args = args[1]
            if (("roblox-player:" in filtered_args) or ("roblox:" in filtered_args)) and not (loaded_json == True and fastFlagConfig.get("EFlagEnableDebugMode") == True):
                use_shell = True
                printMainMessage(f"Creating URL Exchange file..")
                if os.path.exists("/Applications/EfazRobloxBootstrap.app/Contents/Resources/"):
                    with open("/Applications/EfazRobloxBootstrap.app/Contents/Resources/URLSchemeExchange", "w") as f:
                        f.write(filtered_args)
                else:
                    with open("URLSchemeExchange", "w") as f:
                        f.write(filtered_args)

        if direct_run == False:
            applescript = f'''
            tell application "Terminal"
                set command to "{execute_command}"
                set py_window to do script command
                activate
                repeat
                    delay 1
                    try
                        if (busy of py_window) is false then
                            exit repeat
                        end if
                    on error errMsg number errNum
                        exit repeat
                    end try
                end repeat
                try
                    close py_window
                on error
                    set canCloseWindows to (every window whose processes = {"{}"})
                    repeat with windowToClose in canCloseWindows
                        close windowToClose
                    end repeat
                end try
            end tell
            '''
            try:
                ended = False
                def awake():
                    seconds = 0
                    printMainMessage("Starting Notification Loop..")
                    while True:
                        if ended == True:
                            break
                        if os.path.exists("/Applications/EfazRobloxBootstrap.app/Contents/Resources/MacOSNotification"):
                            with open("/Applications/EfazRobloxBootstrap.app/Contents/Resources/MacOSNotification", "r") as f:
                                try:
                                    notification = json.loads(f.read())
                                    if type(notification) is list:
                                        class InvalidNotificationException(Exception):
                                            pass
                                        raise InvalidNotificationException()
                                except Exception as e:
                                    printDebugMessage(str(e))
                                    notification = {"title": "Something went wrong.", "message": "An unexpected error occurred while loading this notification."}
                            os.remove("/Applications/EfazRobloxBootstrap.app/Contents/Resources/MacOSNotification")
                            if notification.get("title") and notification.get("message"):
                                displayMacOSNotification(notification["title"], notification["message"])
                                printSuccessMessage("Successfully pinged notification!")
                        seconds += 1
                        time.sleep(0.05)
                threading.Thread(target=awake).start() 
                printMainMessage(f"Starting Bootstrap..")
                result = subprocess.run(args=["osascript", "-e", applescript], check=True, capture_output=True)
                if result.returncode == 0:
                    printSuccessMessage(f"Bootstrap Run Success: {result.returncode}")
                else:
                    printErrorMessage(f"Bootstrap Run Failed: {result.returncode}")
                ended = True
            except Exception as e:
                traceback.print_exc()
                traceback_err_str = traceback.format_exc()
                printErrorMessage(f"Bootstrap Run Failed: {result.returncode}")
        else:
            try:
                ended = False
                def awake():
                    seconds = 0
                    printMainMessage("Starting Notification Loop..")
                    while True:
                        if ended == True:
                            break
                        if os.path.exists("/Applications/EfazRobloxBootstrap.app/Contents/Resources/MacOSNotification"):
                            with open("/Applications/EfazRobloxBootstrap.app/Contents/Resources/MacOSNotification", "r") as f:
                                try:
                                    notification = json.loads(f.read())
                                    if type(notification) is list:
                                        class InvalidNotificationException(Exception):
                                            pass
                                        raise InvalidNotificationException()
                                except Exception as e:
                                    printDebugMessage(str(e))
                                    notification = {"title": "Something went wrong.", "message": "An unexpected error occurred while loading this notification."}
                            if notification.get("title") and notification.get("message"):
                                displayMacOSNotification(notification["title"], notification["message"])
                                printSuccessMessage("Successfully pinged notification!")
                            if os.path.exists("/Applications/EfazRobloxBootstrap.app/Contents/Resources/MacOSNotification"):
                                try: 
                                    os.remove("/Applications/EfazRobloxBootstrap.app/Contents/Resources/MacOSNotification")
                                except Exception as e: 
                                    printErrorMessage(str(e))
                        seconds += 1
                        time.sleep(0.05)
                def main_process():
                    try:
                        printMainMessage(f"Starting Bootstrap..")
                        global ended
                        if not (filtered_args == "" or filtered_args == None):
                            result = subprocess.run([pythonExecutable, "Main.py", filtered_args], check=True, capture_output=True, shell=True)
                        else:
                            result = subprocess.run([pythonExecutable, "Main.py"], check=True, capture_output=True)
                        if result.returncode == 0:
                            printSuccessMessage(f"Bootstrap Run Success: {result.returncode}")
                        else:
                            printErrorMessage(f"Bootstrap Run Failed: {result.returncode}")
                        ended = True
                        sys.exit(0)
                    except Exception as e:
                        printErrorMessage(str(e))
                        sys.exit(1)
                threading.Thread(target=awake).start()
                main_process()
            except Exception as e:
                printErrorMessage(f"Bootstrap Run Failed: {str(e)}")
                sys.exit(1)
    elif main_os == "Windows":
        filtered_args = ""
        loaded_json = True
        local_app_data = os.path.expandvars(r'%LOCALAPPDATA%')
        
        if os.path.exists(os.path.join(local_app_data, "EfazRobloxBootstrap", "Main.py")):
            os.system("title Efaz's Roblox Bootstrap")
            printMainMessage(f"Loading Configuration File..")
            with open(os.path.join(local_app_data, "EfazRobloxBootstrap", "FastFlagConfiguration.json"), "r") as f:
                try:
                    fastFlagConfig = json.loads(f.read())
                except Exception as e:
                    loaded_json = False

            if len(args) > 1:
                cou = 0
                filtered_args = ""
                for i in args:
                    if cou > 0:
                        filtered_args = f"{i} "
                    cou += 1

            if pip_class.pythonInstalled() == False: pip_class.pythonInstall()
            pythonExecutable = pip_class.findPython()
            if not pythonExecutable:
                printErrorMessage("Please install Python in order to run this bootstrap!")
                input("> ")
                sys.exit(1)

            try:
                printMainMessage(f"Starting Bootstrap..")
                if filtered_args == "":
                    result = subprocess.run([pythonExecutable, os.path.join(local_app_data, "EfazRobloxBootstrap", "Main.py")], shell=True, cwd=os.path.join(local_app_data, "EfazRobloxBootstrap"))
                else:
                    result = subprocess.run([pythonExecutable, os.path.join(local_app_data, "EfazRobloxBootstrap", "Main.py"), filtered_args], shell=True, cwd=os.path.join(local_app_data, "EfazRobloxBootstrap"))
                if result.returncode == 0:
                    printSuccessMessage(f"Bootstrap Run Success: {result.returncode}")
                else:
                    printErrorMessage(f"Bootstrap Run Failed: {result.returncode}")
                sys.exit(0)
            except Exception as e:
                printErrorMessage(f"Bootstrap Run Failed: {str(e)}")
                sys.exit(1)
        else:
            printMainMessage("Please install the bootstrap using the Install.py command!!")
            input("> ")
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