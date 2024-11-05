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
    current_version = {"version": "1.3.5"}
    main_os = platform.system()
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

        def displayMacOSNotification(title, message):
            import objc
            NSUserNotification = objc.lookUpClass("NSUserNotification")
            NSUserNotificationCenter = objc.lookUpClass("NSUserNotificationCenter")

            notification = NSUserNotification.alloc().init()
            notification.setTitle_(title)
            notification.setInformativeText_(message)
            center = NSUserNotificationCenter.defaultUserNotificationCenter()
            center.deliverNotification_(notification)

        if pip_class.pythonInstalled() == False: pip_class.pythonInstall()
        pythonExecutable = pip_class.findPython()
        if not pythonExecutable:
            printErrorMessage("Please install Python in order to run this bootstrap!")
            input("> ")
            sys.exit(1)
        else:
            printMainMessage(f"Detected Python Executable: {pythonExecutable}")

        execute_command = f'unset HISTFILE && cd /Applications/EfazRobloxBootstrap.app/Contents/Resources/ && {pythonExecutable} Main.py && exit'
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
            app = None
            app_root = None
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
            def startBootstrap():
                global ended
                global app
                printMainMessage(f"Starting Bootstrap..")
                result = subprocess.run(args=["osascript", "-e", applescript], check=True, capture_output=True)
                printMainMessage("Ending Bootstrap..")
                ended = True
                if result.returncode == 0:
                    printSuccessMessage(f"Bootstrap Run Success: {result.returncode}")
                    sys.exit(0)
                else:
                    printErrorMessage(f"Bootstrap Run Failed: {result.returncode}")
                    sys.exit(1)
            def createTkinterAppReplication():
                try:
                    printMainMessage(f"Starting Tkinter App Replication..")
                    time.sleep(1)
                    def getLatestTerminalID():
                        apple_script = '''
                        tell application "Terminal"
                            set targetWindow to missing value
                            repeat with w in every window
                                if (w's name contains "Efaz" and w's name contains "Roblox" and w's name contains "Bootstrap") or (w's name contains "Python Main.py") then
                                    set targetWindow to w
                                    exit repeat
                                end if
                            end repeat
                            
                            if targetWindow is not missing value then
                                return id of targetWindow
                            else
                                return "Unable to get terminal window ID"
                            end if
                        end tell
                        '''

                        def extract_window_id(error_message):
                            prefix = "window id "
                            start_index = error_message.find(prefix)

                            if start_index != -1:
                                start_index += len(prefix)
                                end_index = error_message.find('.', start_index)
                                window_id = error_message[start_index:end_index].strip()
                                return window_id
                            else:
                                return "No window ID found in the message."

                        try:
                            result = subprocess.run(
                                ['osascript', '-e', apple_script],
                                check=True,
                                capture_output=True,
                                text=True
                            )
                            
                            latest_window_id = result.stdout.strip()
                            if latest_window_id == "No Terminal windows are open.":
                                return None
                            else:
                                return latest_window_id
                        except subprocess.CalledProcessError as e:
                            return extract_window_id(e.stderr.strip())
                    associated_terminal_pid = getLatestTerminalID()
                    if associated_terminal_pid:
                        try:
                            if getattr(sys, 'frozen', False):
                                os.environ['TCL_LIBRARY'] = "/Applications/EfazRobloxBootstrap.app/Contents/MacOS/EfazRobloxBootstrap.app/Contents/Resources/_tcl_data"
                                os.environ['TK_LIBRARY'] = "/Applications/EfazRobloxBootstrap.app/Contents/MacOS/EfazRobloxBootstrap.app/Contents/Resources/_tk_data"
                            else:
                                os.environ['TCL_LIBRARY'] = "/Library/Frameworks/Python.framework/Versions/3.13/Frameworks/Tcl.framework/Versions/8.6/Resources/Scripts/"
                                os.environ['TK_LIBRARY'] = "/Library/Frameworks/Python.framework/Versions/3.13/Frameworks/Tk.framework/Versions/8.6/Resources/Scripts/"
                            import tkinter as tk
                            from tkinter import messagebox
                            global app_root
                            global app

                            class App:
                                def __init__(self, master: tk.Tk):
                                    try:
                                        self.master = master
                                        self.master.title("Efaz's Roblox Bootstrap")
                                        self.master.geometry("1x1")
                                        self.master.withdraw()
                                        self.master.resizable(False, False)
                                        self.master.attributes("-alpha", 0.0)
                                        self.button = tk.Button(master, text=f"Go to terminal", command=self.on_button_click)
                                        self.button.pack(pady=10)
                                        self.master.bind("<Activate>", self.on_window_activate)
                                        self.terminal_window = getLatestTerminalID()
                                        self.check_end()
                                        printMainMessage(f"Tkinter app finished launching! Terminal ID: {self.terminal_window}")
                                    except Exception as e:
                                        printErrorMessage(f"Tkinter App Failed! Error: {str(e)}")

                                def on_button_click(self):
                                    printMainMessage("Woo! Button has been clicked!")
                                    self.activate_terminal_window()

                                def on_window_activate(self, event):
                                    self.activate_terminal_window()

                                def check_end(self):
                                    try:
                                        global ended
                                        if ended == True:
                                            self.master.quit() 
                                            self.master.destroy()
                                        else:
                                            self.master.after(100, self.check_end)
                                    except Exception as e:
                                        printErrorMessage(f"Tkinter App Failed! Error: {str(e)}")

                                def activate_terminal_window(self):
                                    if self.terminal_window:
                                        apple_script = f'''
                                        tell application "Terminal"
                                            try
                                                set targetWindow to first window whose id is {self.terminal_window}
                                                set index of targetWindow to 1
                                                activate
                                            on error
                                                return "Error: Cannot find window with ID " & {self.terminal_window}
                                            end try
                                        end tell
                                        '''
                                        try:
                                            def sendReq():
                                                result = subprocess.run(
                                                    ["osascript", "-e", apple_script],
                                                    check=True,
                                                    capture_output=True,
                                                    text=True
                                                )
                                                if result.returncode == 0:
                                                    printMainMessage("Successfully activated terminal!")
                                                else:
                                                    printMainMessage("Failed to activate Terminal window.")  
                                            threading.Thread(target=sendReq, daemon=True).start()
                                        except Exception as e:
                                            printErrorMessage(f"Error activating Terminal window: {str(e)}")

                            try:
                                app_root = tk.Tk()
                                app = App(app_root)
                                app_root.after(1000, app_root.deiconify)
                                app_root.mainloop()
                            except Exception as e:
                                printErrorMessage(f"Error activating Terminal window: {str(e)}")
                        except Exception as e:
                            printErrorMessage(f"Tkinter App Failed! Error: {str(e)}")
                    else:
                        printErrorMessage(f"Unable to get terminal pid. Response: {associated_terminal_pid}")
                except Exception as e:
                    printErrorMessage(str(e))
            if not (fastFlagConfig.get("EFlagDisableCreatingTkinterApp") == True):
                threading.Thread(target=awake).start()
                threading.Thread(target=startBootstrap).start()
                createTkinterAppReplication()
            else:
                threading.Thread(target=awake).start()
                startBootstrap()
        except Exception as e:
            traceback.print_exc()
            traceback_err_str = traceback.format_exc()
            printErrorMessage(f"Bootstrap Run Failed: {traceback_err_str}")
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