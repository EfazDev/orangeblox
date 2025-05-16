import sys
import subprocess
import json
import threading
import os
import platform
import uuid
import time
import traceback
import datetime
import logging
import hashlib
from PipHandler import pip

if __name__ == "__main__":
    current_version = {"version": "2.0.1"}
    main_os = platform.system()
    args = sys.argv
    generated_app_id = str(uuid.uuid4())
    pip_class = pip()
    app_path = ""
    macos_path = ""
    logs = []

    pip_class.executable = pip_class.findPython()
    COLOR_CODES = {
        0: "white",
        1: "red",
        2: "yellow",
        3: "orange",
        4: "green",
    }

    def printMainMessage(mes): print(f"\033[38;5;255m{mes}\033[0m"); logs.append((mes, 0)); logging.info(mes)
    def printErrorMessage(mes): print(f"\033[38;5;196m{mes}\033[0m"); logs.append((mes, 1)); logging.error(mes)
    def printDebugMessage(mes): print(f"\033[38;5;226m{mes}\033[0m"); logs.append((mes, 2)); logging.debug(mes)
    def printWarnMessage(mes): print(f"\033[38;5;202m{mes}\033[0m"); logs.append((mes, 3)); logging.warning(mes)
    def printSuccessMessage(mes): print(f"\033[38;5;82m{mes}\033[0m"); logs.append((mes, 4)); logging.info(mes)
    def setLoggingHandler(handler_name):
        global app_path
        global main_os
        log_path = os.path.join(app_path, "Logs")
        if main_os == "Darwin": log_path = os.path.join(pip_class.getLocalAppData(), "Logs", "OrangeBlox")
        if not os.path.exists(log_path): os.makedirs(log_path)
        sys.stdout.reconfigure(encoding='utf-8')
        logging.basicConfig(filename=os.path.join(log_path, f'OrangeBlox_{handler_name}_{datetime.datetime.now().strftime("%B_%d_%Y_%H_%M_%S_%f")}.log'), level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
        return True
    def isYes(text): return text.lower() == "y" or text.lower() == "yes" or text.lower() == "true" or text.lower() == "t"
    def isNo(text): return text.lower() == "n" or text.lower() == "no" or text.lower() == "false" or text.lower() == "f"
    def isRequestClose(text): return text.lower() == "exit" or text.lower() == "exit()"

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        if main_os == "Windows": app_path = os.path.dirname(sys.executable); macos_path = os.path.join(os.path.dirname(sys.executable), "MacOS")
        else: app_path = os.path.join(os.sep.join(os.path.dirname(sys.executable).split(os.sep)[:-4]), "Resources"); macos_path = os.path.join(os.sep.join(os.path.dirname(sys.executable).split(os.sep)[:-4]), "MacOS")
    else:
        if main_os == "Windows": app_path = os.path.dirname(sys.argv[0]); macos_path = os.path.dirname(sys.argv[0])
        else: current_path_location = os.path.dirname(os.path.abspath(__file__)); app_path = os.path.join(os.sep.join(os.path.dirname(current_path_location).split(os.sep)[:-3]), "Resources"); macos_path = os.path.join(os.sep.join(os.path.dirname(current_path_location).split(os.sep)[:-3]), "MacOS")
    setLoggingHandler("Bootloader")

    printWarnMessage("-----------")
    printWarnMessage("Welcome to OrangeBlox Loader 🍊!")
    printWarnMessage("Made by Efaz from efaz.dev!")
    printWarnMessage(f"v{current_version['version']}")
    printWarnMessage("-----------")
    printMainMessage("Determining System OS..")

    def displayNotification(title="Unknown Title", message="Unknown Message"):
        if main_os == "Darwin":
            try:
                import objc
                NSUserNotification = objc.lookUpClass("NSUserNotification")
                NSUserNotificationCenter = objc.lookUpClass("NSUserNotificationCenter")

                notification = NSUserNotification.alloc().init()
                notification.setTitle_(title)
                notification.setInformativeText_(message)
                center = NSUserNotificationCenter.defaultUserNotificationCenter()
                center.deliverNotification_(notification)
            except Exception as e:
                printErrorMessage(f"Something went wrong pinging Control Center: {str(e)}")
        elif main_os == "Windows":
            try:
                try:
                    from plyer.platforms.win.notification import WindowsNotification
                except Exception as e:
                    pip_class.install(["plyer"])
                    WindowsNotification = pip_class.importModule("plyer.platforms.win.notification").WindowsNotification
                WindowsNotification().notify(
                    title=title,
                    message=message,
                    app_name="OrangeBlox",
                    app_icon=os.path.join(app_path, "BootstrapImages", "AppIcon.ico")
                )
            except Exception as e:
                printErrorMessage(f"Something went wrong pinging Windows Notification Center: {str(e)}")
    def getIfProcessIsOpened(process_name="", pid=""):
        if main_os == "Windows":
            process = subprocess.Popen(["tasklist"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif main_os == "Darwin":
            process = subprocess.Popen(["ps", "aux"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            printMainMessage("Get if process is opened is only supported for macOS and Windows.")
            return

        output, _ = process.communicate()
        process_list = output.decode("utf-8")

        if pid == "":
            if process_list.rfind(process_name) == -1:
                return False
            else:
                return True
        else:
            if process_list.rfind(pid) == -1:
                return False
            else:
                return True
    def generateFileHash(file_path):
        try:
            with open(file_path, "rb") as f:
                hasher = hashlib.md5()
                chunk = f.read(8192)
                while chunk: 
                    hasher.update(chunk)
                    chunk = f.read(8192)
            return hasher.hexdigest()
        except Exception as e:
            return None
    
    with open(os.path.join(os.path.dirname(__file__), "Version.json"), "r", encoding="utf-8") as f:
        current_version = json.load(f)
        f.close()

    if main_os == "Darwin":
        filtered_args = ""
        loaded_json = True
        use_shell = False
        main_config = {}
        user_folder_name = os.path.basename(os.path.expanduser("~"))

        class plist:
            def readPListFile(self, path: str):
                if os.path.exists(path) and path.endswith(".plist"):
                    import plistlib
                    with open(path, "rb") as f:
                        plist_data = plistlib.load(f)
                    return plist_data
                else:
                    return {}
            def writePListFile(self, path: str, data):
                if path.endswith(".plist"):
                    try:
                        import plistlib
                        with open(path, "wb") as f:
                            plistlib.dump(data, f)
                        return {"success": True, "message": "Success!", "data": data}
                    except Exception as e:
                        return {"success": False, "message": "Something went wrong.", "data": ""}
                else:
                    return {"success": False, "message": "Path doesn't end with .plist", "data": path}

        def loadConfiguration():
            global main_config
            global loaded_json
            printMainMessage("Getting User Configuration..")
            if main_os == "Darwin":
                if os.path.exists(f'{os.path.expanduser("~")}/Library/Preferences/dev.efaz.robloxbootstrap.plist'): os.remove(f'{os.path.expanduser("~")}/Library/Preferences/dev.efaz.robloxbootstrap.plist')
                macos_preference_expected = f'{os.path.expanduser("~")}/Library/Preferences/dev.efaz.orangeblox.plist'
                if os.path.exists(macos_preference_expected):
                    app_configuration = plist().readPListFile(macos_preference_expected)
                    if app_configuration.get("Configuration"):
                        main_config = app_configuration.get("Configuration")
                        loaded_json = True
                    else:
                        main_config = {}
                        loaded_json = True
                else:
                    main_config = {}
                    loaded_json = True
                return main_config
            else:
                with open("Configuration.json", "r", encoding="utf-8") as f:
                    main_config = json.load(f)
                loaded_json = True
                return main_config

        def printDebugMessage(mes): 
            if main_config.get("EFlagEnableDebugMode") == True: 
                print(f"\033[38;5;226m{mes}\033[0m")
                logs.append((mes, 2))

        loadConfiguration()
        printMainMessage("Finding Python Executable..")
        if pip_class.pythonInstalled(computer=True) == False: pip_class.pythonInstall()
        pythonExecutable = pip_class.findPython()
        if main_config.get("EFlagSpecifyPythonExecutable"): pythonExecutable = main_config.get("EFlagSpecifyPythonExecutable")
        if not os.path.exists(pythonExecutable):
            printErrorMessage("Please install Python in order to run this bootstrap!")
            input("> ")
            sys.exit(0)
        else:
            printMainMessage(f"Detected Python Executable: {pythonExecutable}")

        printMainMessage(f"Generated App Window Fetching ID: {generated_app_id}")

        execute_command = f"unset HISTFILE && ulimit -n 2048 && cd {app_path}/ && {pythonExecutable} Main.py && exit"
        printMainMessage(f"Loading Runner Command: {execute_command}")

        if len(args) > 1:
            filtered_args = args[1]
            if (("roblox-player:" in filtered_args) or ("roblox-studio:" in filtered_args) or ("roblox-studio-auth:" in filtered_args) or ("roblox:" in filtered_args) or ("efaz-bootstrap:" in filtered_args) or ("orangeblox:" in filtered_args) or os.path.isfile(filtered_args)):
                use_shell = True
                printMainMessage(f"Creating URL Exchange file..")
                if os.path.exists(f"{app_path}/"):
                    with open(f"{app_path}/URLSchemeExchange", "w", encoding="utf-8") as f:
                        f.write(filtered_args)
                else:
                    with open("URLSchemeExchange", "w", encoding="utf-8") as f:
                        f.write(filtered_args)

        applescript = f'''
        tell application "Terminal"
            activate
            set py_window to do script "{execute_command}"
            try
                set terminal_id to (id of py_window) as string
            on error err_message number err_num
                if err_num = -1728 and err_message contains "window id" then
                    try
                        set terminal_id to word -1 of err_message
                    on error
                        set terminal_id to "0"
                    end try
                else if err_message contains "window id" then
                    set AppleScript's text item delimiters to "window id "
                    set parts to text items of err_message
                    set AppleScript's text item delimiters to space
                    set terminal_id to text item 1 of (text items of (item 2 of parts))
                    set AppleScript's text item delimiters to ""
                else
                    set terminal_id to "0"
                end if
            end try
            activate
            do shell script "echo " & terminal_id & " > " & quoted form of "{app_path}/Terminal_{generated_app_id}"
            activate
            
            repeat
                delay 1
                try
                    if (busy of py_window) is false then
                        exit repeat
                    end if
                on error err_mess number err_num
                    exit repeat
                end try
            end repeat
            try
                close py_window
            on error
                set can_close_windows to (every window whose processes = {"{}"})
                repeat with window_to_close in can_close_windows
                    close window_to_close
                end repeat
            end try
        end tell
        '''
        try:
            ended = False
            validated = None
            associated_terminal_pid = None
            activate_cooldown = False
            unable_to_validate = []

            def notificationLoop():
                global ended
                printMainMessage("Starting Notification Loop..")
                while ended == False:
                    try:
                        if os.path.exists(f"{app_path}/AppNotification"):
                            with open(f"{app_path}/AppNotification", "r", encoding="utf-8") as f:
                                try:
                                    notification = json.load(f)
                                    if not (type(notification) is dict):
                                        class InvalidNotificationException(Exception):
                                            pass
                                        raise InvalidNotificationException("The following data for notification is not valid.")
                                except Exception as e:
                                    printDebugMessage(str(e))
                                    notification = {"title": "Something went wrong.", "message": "An unexpected error occurred while loading this notification."}
                            if os.path.exists(f"{app_path}/AppNotification"): os.remove(f"{app_path}/AppNotification")
                            if notification.get("title") and notification.get("message"):
                                displayNotification(notification["title"], notification["message"])
                                printSuccessMessage(f"Successfully pinged app notification! Title: {notification['title']}, Message: {notification['message']}")
                    except Exception as e:
                        printErrorMessage(f"There was an issue making a notification: {str(e)}")
                    time.sleep(0.05)
            def terminalAwaitLoop():
                global associated_terminal_pid
                printMainMessage("Starting Terminal ID Loop..")
                while ended == False:
                    try:
                        if os.path.exists(f"{app_path}/Terminal_{generated_app_id}"):
                            with open(f"{app_path}/Terminal_{generated_app_id}", "r", encoding="utf-8") as f:
                                try:
                                    cont = f.read().replace(" ", "").replace("\n", "")
                                    if cont.isnumeric() and not cont == "0":
                                        associated_terminal_pid = int(cont)
                                        activateTerminalWindow()
                                except Exception as e:
                                    printDebugMessage(str(e))
                            if os.path.exists(f"{app_path}/Terminal_{generated_app_id}"): os.remove(f"{app_path}/Terminal_{generated_app_id}")
                    except Exception as e:
                        printErrorMessage(f"There was an issue getting Terminal ID: {str(e)}")
                    time.sleep(0.05)
            def loadConfigurationLoop():
                seconds = 0
                printMainMessage("Starting Configuration Loop..")
                while ended == False:
                    try:
                        seconds += 1
                        if seconds % 15 == 0: loadConfiguration()
                    except Exception as e:
                        printErrorMessage(f"There was an issue during the configuration loop: {str(e)}")
                    time.sleep(1)
            def activateTerminalWindow(event=""): 
                global activate_cooldown
                global associated_terminal_pid
                try:
                    if associated_terminal_pid and activate_cooldown == False:
                        activate_cooldown = True
                        apple_script = f'''tell application "Terminal"
                            activate
                            set targetWindow to first window whose id is {associated_terminal_pid}
                            set index of targetWindow to 1
                            activate
                        end tell'''
                        result = subprocess.run(
                            ["osascript", "-e", apple_script],
                            check=True,
                            capture_output=True,
                            text=True
                        )
                        if result.returncode == 0:
                            if event == "": printMainMessage("Successfully activated terminal!")
                        else:
                            printErrorMessage("Failed to activate Terminal window.")
                        activate_cooldown = False
                except Exception as e:
                    printErrorMessage(f"Error activating Terminal window.")
            def startBootstrap():
                global ended
                global validated
                global unable_to_validate
                global associated_terminal_pid
                try:
                    printMainMessage(f"Validating Bootstrap Scripts..")
                    a_file_hash = generateFileHash(f"{app_path}/Main.py")
                    b_file_hash = generateFileHash(f"{app_path}/RobloxFastFlagsInstaller.py")
                    c_file_hash = generateFileHash(f"{app_path}/Install.py")
                    d_file_hash = generateFileHash(f"{app_path}/OrangeAPI.py")
                    e_file_hash = generateFileHash(f"{app_path}/DiscordPresenceHandler.py")
                    f_file_hash = generateFileHash(f"{app_path}/PipHandler.py")

                    validated = True
                    integrated_app_hashes = current_version.get("hashes", {})
                    if not (a_file_hash == integrated_app_hashes.get("main")): validated = False; unable_to_validate.append("Main.py")
                    if not (b_file_hash == integrated_app_hashes.get("fflag_install")): validated = False; unable_to_validate.append("RobloxFastFlagsInstaller.py")
                    if not (c_file_hash == integrated_app_hashes.get("install")): validated = False; unable_to_validate.append("Install.py")
                    if not (d_file_hash == integrated_app_hashes.get("bootstrap_api")): validated = False; unable_to_validate.append("OrangeAPI.py")
                    if not (e_file_hash == integrated_app_hashes.get("discord_presence")): validated = False; unable_to_validate.append("DiscordPresenceHandler.py")
                    if not (f_file_hash == integrated_app_hashes.get("pip_handler")): validated = False; unable_to_validate.append("PipHandler.py")

                    if validated == True or main_config.get("EFlagDisableSecureHashSecurity") == True:
                        printMainMessage(f"Running Bootstrap..")
                        if main_config.get("EFlagDisableSecureHashSecurity") == True: displayNotification("Security Notice", "Hash Verification is currently disabled. Please check your configuration and mod scripts if you didn't disable this!")
                        try:
                            result = subprocess.run(args=["osascript", "-e", applescript], check=True, capture_output=True)
                        except Exception as e:
                            printErrorMessage(f"An error was issued by subprocess: {str(e)}")
                        printMainMessage("Ending Bootstrap..")
                        ended = True
                        if result.returncode == 0:
                            printSuccessMessage(f"Bootstrap Run Success: {result.returncode}")
                            sys.exit(0)
                        else:
                            printErrorMessage(f"Bootstrap Run Failed: {result.returncode}")
                            sys.exit(0)
                    else:
                        displayNotification("Uh oh!", "Your copy of OrangeBlox was unable to be validated and might be tampered with!")
                        printErrorMessage(f"Uh oh! There was an issue trying to validate hashes for the following files: {', '.join(unable_to_validate)}")
                        if main_config.get("EFlagDisableCreatingTkinterApp") == True: 
                            printErrorMessage(f"Please download a new copy from GitHub or disable hash security by manually editting your configuration file!")
                        else:
                            printErrorMessage(f"Requested validation failed window from Tkinter.")
                        if not (a_file_hash == integrated_app_hashes["main"]):  printMainMessage(f'Main.py | {integrated_app_hashes["main"]} => {a_file_hash}')
                        if not (b_file_hash == integrated_app_hashes["fflag_install"]): printMainMessage(f'RobloxFastFlagsInstaller.py | {integrated_app_hashes["fflag_install"]} => {b_file_hash}')
                        if not (c_file_hash == integrated_app_hashes["install"]): printMainMessage(f'Install.py | {integrated_app_hashes["install"]} => {c_file_hash}')
                        if not (d_file_hash == integrated_app_hashes["bootstrap_api"]): printMainMessage(f'OrangeAPI.py | {integrated_app_hashes["bootstrap_api"]} => {d_file_hash}')
                        if not (e_file_hash == integrated_app_hashes["discord_presence"]): printMainMessage(f'DiscordPresenceHandler.py | {integrated_app_hashes["discord_presence"]} => {e_file_hash}')
                        if not (f_file_hash == integrated_app_hashes["pip_handler"]): printMainMessage(f'PipHandler.py | {integrated_app_hashes["pip_handler"]} => {f_file_hash}')
                        ended = True
                        sys.exit(0)
                except Exception as e:
                    ended = True
                    printErrorMessage(f"Bootstrap Run Failed: {str(e)}")
                    sys.exit(0)
            def createTkinterAppReplication():
                global associated_terminal_pid
                global unable_to_validate
                global validated
                global ended
                try:
                    printMainMessage(f"Starting Tkinter App Replication..")
                    while validated == None:
                       time.sleep(0)
                    try:
                        if getattr(sys, "frozen", False):
                            os.environ["TCL_LIBRARY"] = f"{macos_path}/OrangeBlox.app/Contents/Resources/_tcl_data"
                            os.environ["TK_LIBRARY"] = f"{macos_path}/OrangeBlox.app/Contents/Resources/_tk_data"
                        else:
                            os.environ["TCL_LIBRARY"] = "/Library/Frameworks/Python.framework/Versions/3.13/Frameworks/Tcl.framework/Versions/8.6/Resources/Scripts/"
                            os.environ["TK_LIBRARY"] = "/Library/Frameworks/Python.framework/Versions/3.13/Frameworks/Tk.framework/Versions/8.6/Resources/Scripts/"
                        import tkinter as tk
                        from Cocoa import NSApplication, NSMenu, NSMenuItem, NSApplicationActivationPolicyRegular
                        from Foundation import NSObject
                        import random
                        class App:
                            terminal_window = None
                            master = None
                            button = None
                            top_menu = None
                            holding_frame = None
                            app_icon = None
                            label = None
                            label_2 = None
                            debug_mode_window_enabled = False
                            is_at_bottom = True
                            output_area = None
                            button_click_count = 0
                            last_checked_index = 0
                            activate_cooldown = False
                            requested_kill = False
                            cocoa_app = None
                            dock_menu = None
                            validation_window = None
                            validation_frame = None

                            def __init__(self, master: tk.Tk):
                                try:
                                    self.master = master
                                    self.master.title("OrangeBlox")
                                    self.master.geometry("1x1")
                                    self.master.withdraw()
                                    self.master.resizable(False, False)
                                    self.master.attributes("-alpha", 0.0)

                                    self.holding_frame = tk.Frame(self.master)
                                    self.holding_frame.pack(fill="both", expand=True)
                                    self.holding_frame.place(relx=0.5, rely=0.5, anchor="center")
                                    app_icon_url = f"{app_path}/BootstrapImages/AppIcon64.png"
                                    if os.path.exists(app_icon_url): self.app_icon = tk.PhotoImage(file=app_icon_url)
                                    else: self.app_icon = tk.PhotoImage(file=f"{app_path}/BootstrapImages/AppIcon.icns")
                                    icon_label = tk.Label(self.holding_frame, image=self.app_icon)
                                    icon_label.image = self.app_icon
                                    icon_label.pack()
                                    self.label = tk.Label(self.holding_frame, text="Ooh! Hi there! Welcome to OrangeBlox 🍊!")
                                    self.label.pack(pady=10)
                                    self.label_2 = tk.Label(self.holding_frame, text="Bootstrap Loader Logs: ")
                                    self.label_2.pack(pady=3)
                                    self.output_area = tk.Text(self.holding_frame, height=18, font=("Menlo", 12), bg="#1e1e1e", fg="#ffffff", insertbackground='white', relief="flat", wrap="none")
                                    self.output_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
                                    scrollbar = tk.Scrollbar(self.master, command=self.output_area.yview)
                                    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                                    scrollbar.config(width=0)
                                    self.output_area.bind("<MouseWheel>", self.on_mouse_wheel)
                                    self.output_area.config(yscrollcommand=scrollbar.set)
                                    self.output_area.config(state=tk.DISABLED)

                                    self.output_area.tag_configure("white", foreground="#ffffff")
                                    self.output_area.tag_configure("red", foreground="#ff0000")
                                    self.output_area.tag_configure("yellow", foreground="#ffff00")
                                    self.output_area.tag_configure("orange", foreground="#f4792c")
                                    self.output_area.tag_configure("green", foreground="#00ff00")

                                    for key, color in COLOR_CODES.items(): self.output_area.tag_config(f"color_{key}", foreground=color)
                                    self.button = tk.Button(self.holding_frame, text=f"Go to bootstrap terminal window!", command=self.on_button_click)
                                    self.button.pack(pady=5)

                                    self.holding_frame.bind("<Activate>", self.on_window_activate)
                                    self.master.protocol("WM_DELETE_WINDOW", self.on_close)
                                    self.master.protocol("WM_ICONIFY", self.prevent_minimize)
                                    def awaitTerminal():
                                        global associated_terminal_pid
                                        while associated_terminal_pid == None: time.sleep(0.05)
                                        printDebugMessage(f"Received Terminal ID from Receiver: {associated_terminal_pid}")
                                        self.terminal_window = associated_terminal_pid
                                        self.activate_terminal_window()
                                    threading.Thread(target=awaitTerminal, daemon=True).start()

                                    self.top_menu = tk.Menu(self.master)
                                    main_menu = tk.Menu(self.top_menu, name='apple')
                                    self.top_menu.add_cascade(menu=main_menu)
                                    main_menu.add_command(label="About OrangeBlox", command=self.show_about_menu)
                                    main_menu.add_separator()
                                    main_menu.add_command(label="New Bootstrap Window", command=self.new_bootstrap)
                                    main_menu.add_command(label="Open Debug Window", command=self.instant_debug_window)
                                    main_menu.add_separator()
                                    main_menu.add_command(label="Open Mods Manager", command=self.new_bootstrap_open_mods_manager)
                                    main_menu.add_command(label="Open Settings", command=self.new_bootstrap_open_settings)
                                    main_menu.add_command(label="Open Credits", command=self.new_bootstrap_open_credits)
                                    self.master.createcommand("tk::mac::Quit" , self.on_close)

                                    file_menu = tk.Menu(self.top_menu)
                                    self.top_menu.add_cascade(label="File", menu=file_menu)
                                    file_menu.add_separator()
                                    if main_config.get("EFlagEnableDuplicationOfClients") == True:
                                        file_menu.add_command(label="Open Roblox [Multi-Instance Mode]", command=self.new_bootstrap_play_multi_roblox)
                                    else:
                                        file_menu.add_command(label="Open Roblox", command=self.new_bootstrap_play_roblox)
                                    if main_config.get("EFlagRobloxStudioEnabled") == True: file_menu.add_command(label="Run Roblox Studio", command=self.new_bootstrap_play_roblox_studio)
                                    file_menu.add_separator()
                                    if not (main_config.get("EFlagAllowActivityTracking") == False): 
                                        file_menu.add_command(label="Connect to Existing Roblox", command=self.new_bootstrap_play_reconnect)
                                        if main_config.get("EFlagRobloxStudioEnabled") == True: file_menu.add_command(label="Connect to Existing Roblox Studio", command=self.new_bootstrap_play_reconnect_studio)
                                    file_menu.add_separator()
                                    file_menu.add_command(label="Run Fast Flags Installer", command=self.new_bootstrap_run_fflag_installer)
                                    file_menu.add_command(label="Clear Roblox Logs", command=self.new_bootstrap_clear_roblox_logs)
                                    file_menu.add_command(label="Roblox Installer Options", command=self.new_bootstrap_roblox_installer)
                                    file_menu.add_command(label="End All Roblox Windows", command=self.new_bootstrap_end_roblox)
                                    if main_config.get("EFlagRobloxStudioEnabled") == True: file_menu.add_command(label="End All Roblox Studio Windows", command=self.new_bootstrap_end_roblox_studio)

                                    shortcuts_menu = tk.Menu(self.top_menu)
                                    self.top_menu.add_cascade(label="Shortcuts", menu=shortcuts_menu)
                                    generated_ui_options = []
                                    if type(main_config.get("EFlagRobloxLinkShortcuts")) is dict:
                                        for i, v in main_config.get("EFlagRobloxLinkShortcuts").items():
                                            if v and v.get("name") and v.get("id") and v.get("url"): generated_ui_options.append({"index": 1, "message": f"{v.get('name')} [{i}]", "shortcut_info": v})
                                    if len(generated_ui_options) > 0:
                                        for p in generated_ui_options:
                                            def hand(): self.new_bootstrap(f"shortcuts/{p['shortcut_info'].get('id')}", f"Open Shortcut ({p['message']})")
                                            shortcuts_menu.add_command(label=p["message"], command=hand)
                                        shortcuts_menu.add_separator()
                                    shortcuts_menu.add_command(label="Open Shortcuts Menu", command=self.new_bootstrap_open_shortcuts)

                                    options_menu = tk.Menu(self.top_menu)
                                    self.top_menu.add_cascade(label="Options", menu=options_menu)
                                    options_menu.add_command(label="Clear Debug Window Logs", command=self.clear_logs)
                                    options_menu.add_command(label="Force Load Debug Window Logs", command=self.force_load_logs)
                                    if (main_config.get("EFlagNumberOfTkinterAppsAllowed", 1)) > 0 and os.path.exists(os.path.join(app_path, f"TkinterAppOpened_{user_folder_name}")): options_menu.add_command(label="Unlock Tkinter App Lock", command=self.unlock_tkinter_lock)
                                    options_menu.add_command(label="Close Tkinter App", command=self.on_close)

                                    help_menu = tk.Menu(self.top_menu)
                                    self.top_menu.add_cascade(label="Help", menu=help_menu)
                                    help_menu.add_command(label="OrangeBlox Wiki", command=self.show_help_menu)
                                    help_menu.add_command(label="GitHub Issues", command=self.show_github_issues_menu)

                                    try:
                                        if self.top_menu and main_menu and help_menu:
                                            master.config(menu=self.top_menu)
                                    except Exception as e:
                                        printErrorMessage(f"Menu configuration error: {str(e)}")

                                    if ended == True:
                                        self.master.quit()
                                        self.master.destroy()
                                        return
                                    else:
                                        try:
                                            if ended == False:
                                                self.check_end()
                                                self.reset_button_click()
                                                self.load_logs()
                                                if validated == False:
                                                    self.show_validation_failed_menu()
                                            else:
                                                self.master.quit()
                                                self.master.destroy()
                                        except Exception as e:
                                            printErrorMessage(f"Something went wrong with running functions! Error: {str(e)}")
                                        printMainMessage(f"Tkinter app finished launching! Terminal ID: {self.terminal_window}")
                                except Exception as e:
                                    printErrorMessage(f"Tkinter App Failed! Error: {str(e)}")
                            def on_button_click(self):
                                self.activate_terminal_window()
                            def on_close(self):
                                global ended
                                if ended == True:
                                    printMainMessage("Closing debug window..")
                                    self.master.withdraw()
                                    self.master.quit()
                                    self.master.destroy()
                                    printSuccessMessage("Successfully ended Tkinter app!")
                                else:
                                    if self.terminal_window:
                                        self.kill_bootstrap_window()
                                    else:
                                        ended = True
                                        self.master.withdraw()
                                        self.master.destroy()
                                        printSuccessMessage("Successfully ended Tkinter app!")
                            def prevent_minimize(self):
                                printDebugMessage("Prevented minimizing main window in order to keep app running smoothly.")
                            def generate_dock_menu(self):
                                generated_ui_options = []
                                generated_menu_items = []

                                class DockAppDelegate(NSObject):
                                    def newBootstrapWindow_(self, sender):
                                        main_app.new_bootstrap()
                                    def runRoblox_(self, sender):
                                        main_app.new_bootstrap_play_roblox()
                                    def multiRunRoblox_(self, sender):
                                        main_app.new_bootstrap_play_multi_roblox()
                                    def runRobloxStudio_(self, sender):
                                        main_app.new_bootstrap_play_roblox_studio()
                                    def openRobloxInstallerOptions_(self, sender):
                                        main_app.new_bootstrap_roblox_installer()
                                    def endAllRoblox_(self, sender):
                                        main_app.new_bootstrap_end_roblox()
                                    def endAllRobloxStudio_(self, sender):
                                        main_app.new_bootstrap_end_roblox_studio()
                                    def runFFlagInstaller_(self, sender):
                                        main_app.new_bootstrap_run_fflag_installer()
                                    def reconnectRoblox_(self, sender):
                                        main_app.new_bootstrap_play_reconnect()
                                    def reconnectRobloxStudio_(self, sender):
                                        main_app.new_bootstrap_play_reconnect_studio()
                                    def enterDebugWindowMode_(self, sender):
                                        main_app.instant_debug_window()
                                    def shortcutmenu_(self, sender):
                                        main_app.new_bootstrap_open_shortcuts()
                                    def shortcut_(self, sender):
                                        menu_title = sender.title()
                                        for p in generated_ui_options:
                                            if p["message"] == menu_title:
                                                main_app.new_bootstrap(f"shortcuts/{p['shortcut_info'].get('id')}", f"Open Shortcut ({p['message']})")
                                                break
                                    def validateMenuItem_(self, menuItem):
                                        return True
                        
                                if type(main_config.get("EFlagRobloxLinkShortcuts")) is dict:
                                    for i, v in main_config.get("EFlagRobloxLinkShortcuts").items():
                                        if v and v.get("name") and v.get("id") and v.get("url"):
                                            generated_ui_options.append({"index": 1, "message": f"{v.get('name')} [{i}]", "shortcut_info": v})

                                main_app = self
                                self.cocoa_app = NSApplication.sharedApplication()
                                self.cocoa_app.setActivationPolicy_(NSApplicationActivationPolicyRegular)
                                delegate = DockAppDelegate.alloc().init()
                                self.cocoa_app.setDelegate_(delegate)

                                self.dock_menu = NSMenu.alloc().init()
                                menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("New Bootstrap Window", "newBootstrapWindow:", "")
                                menu_item.setEnabled_(True)
                                self.dock_menu.addItem_(menu_item)
                                menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Open Debug Window", "enterDebugWindowMode:", "")
                                menu_item.setEnabled_(True)
                                self.dock_menu.addItem_(menu_item)
                                self.dock_menu.addItem_(NSMenuItem.separatorItem())

                                if main_config.get("EFlagEnableDuplicationOfClients") == True:
                                    menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Open Roblox [Multi-Instance Mode]", "multiRunRoblox:", "")
                                    menu_item.setEnabled_(True)
                                    self.dock_menu.addItem_(menu_item)
                                else:
                                    menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Open Roblox", "runRoblox:", "")
                                    menu_item.setEnabled_(True)
                                    self.dock_menu.addItem_(menu_item)
                                if main_config.get("EFlagRobloxStudioEnabled") == True:
                                    menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Run Roblox Studio", "runRobloxStudio:", "")
                                    menu_item.setEnabled_(True)
                                    self.dock_menu.addItem_(menu_item)
                                self.dock_menu.addItem_(NSMenuItem.separatorItem())
                                menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Run Fast Flags Installer", "runFFlagInstaller:", "")
                                menu_item.setEnabled_(True)
                                self.dock_menu.addItem_(menu_item)
                                menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Roblox Installer Options", "openRobloxInstallerOptions:", "")
                                menu_item.setEnabled_(True)
                                self.dock_menu.addItem_(menu_item)
                                menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("End All Roblox Windows", "endAllRoblox:", "")
                                menu_item.setEnabled_(True)
                                self.dock_menu.addItem_(menu_item)
                                if main_config.get("EFlagRobloxStudioEnabled") == True:
                                    menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("End All Roblox Studio Windows", "endAllRobloxStudio:", "")
                                    menu_item.setEnabled_(True)
                                    self.dock_menu.addItem_(menu_item)
                                self.dock_menu.addItem_(NSMenuItem.separatorItem())
                                if len(generated_ui_options) > 0:
                                    for p in generated_ui_options:
                                        menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(p["message"], "shortcut:", "")
                                        menu_item.setEnabled_(True)
                                        self.dock_menu.addItem_(menu_item)
                                        generated_menu_items.append(menu_item)
                                menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Open Shortcuts Menu", "shortcutmenu:", "")
                                menu_item.setEnabled_(True)
                                self.dock_menu.addItem_(menu_item)
                                self.cocoa_app.setDockMenu_(self.dock_menu)
                                self.cocoa_app.activateIgnoringOtherApps_(True)
                                # self.cocoa_app.run()
                            def new_bootstrap(self, action="", action_name=""):
                                if not (action == "") and type(action) is str:
                                    url_scheme_path = f"{app_path}/URLSchemeExchange"
                                    with open(url_scheme_path, "w", encoding="utf-8") as f:
                                        f.write(f"orangeblox://{action}?quick-action=true")
                                subprocess.Popen(f'open -n -a "{macos_path}/OrangeBlox.app/Contents/MacOS/OrangeBloxMain"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                                if not (action_name == "") and type(action_name) is str:
                                    printMainMessage(f"Launched Bootstrap with action: {action_name}")
                                else:
                                    printMainMessage(f"Launched Bootstrap in new window!")
                            def new_bootstrap_play_roblox(self):
                                self.new_bootstrap("continue", "Play Roblox")
                            def new_bootstrap_play_roblox_studio(self):
                                self.new_bootstrap("run-studio", "Run Roblox Studio")
                            def new_bootstrap_play_multi_roblox(self):
                                self.new_bootstrap("new", "Multi-Play Roblox")
                            def new_bootstrap_play_reconnect(self):
                                self.new_bootstrap("reconnect", "Connect to Existing Roblox Window")
                            def new_bootstrap_play_reconnect_studio(self):
                                self.new_bootstrap("reconnect-studio", "Connect to Existing Roblox Studio Window")
                            def new_bootstrap_clear_roblox_logs(self):
                                self.new_bootstrap("clear-logs", "Clear Roblox Logs")
                            def new_bootstrap_roblox_installer(self):
                                self.new_bootstrap("roblox-installer-options", "Open Roblox Installer Options")
                            def new_bootstrap_end_roblox(self):
                                self.new_bootstrap("end-roblox", "End Roblox")
                            def new_bootstrap_end_roblox_studio(self):
                                self.new_bootstrap("end-roblox-studio", "End Roblox Studio")
                            def new_bootstrap_run_fflag_installer(self):
                                self.new_bootstrap("fflag-install", "Run Fast Flag Installer")
                            def new_bootstrap_open_settings(self):
                                self.new_bootstrap("settings", "Open Settings")
                            def new_bootstrap_open_mods_manager(self):
                                self.new_bootstrap("mods", "Open Mods Manager")
                            def new_bootstrap_open_credits(self):
                                self.new_bootstrap("credits", "Open Credits")
                            def new_bootstrap_open_shortcuts(self):
                                self.new_bootstrap("shortcuts/", "Open Shortcuts Menu")
                            def clear_logs(self):
                                global logs
                                logs = []
                                self.output_area.config(state=tk.NORMAL)
                                self.output_area.delete("1.0", tk.END)
                                self.output_area.config(state=tk.DISABLED)
                            def force_load_logs(self):
                                self.load_logs("oranges")
                            def unlock_tkinter_lock(self):
                                if os.path.exists(os.path.join(app_path, f"TkinterAppOpened_{user_folder_name}")): os.remove(os.path.join(app_path, f"TkinterAppOpened_{user_folder_name}"))
                            def kill_bootstrap_window(self, event=""):
                                try:
                                    if self.terminal_window:
                                        self.requested_kill = True
                                        self.activate_terminal_window()
                                        apple_script = f'''on run
                                            tell application "Terminal"
                                                set targetWindow to (first window whose id is {self.terminal_window})
                                                close targetWindow
                                            end tell
                                        end run'''
                                        result = subprocess.run(
                                            ["osascript", "-e", apple_script],
                                            check=True,
                                            capture_output=True,
                                            text=True
                                        )
                                        if result.returncode == 0:
                                            if event == "": printErrorMessage("Please close the console window in order to close this window!!")
                                except Exception as e:
                                    printErrorMessage(f"Error while trying to request kill of Terminal window.")
                            def instant_debug_window(self):
                                self.button_click_count = 10
                                self.master.focus_force()
                                self.on_window_activate("oranges")
                            def show_about_menu(self):
                                about_window = tk.Toplevel(self.master)
                                about_window.title("About OrangeBlox")
                                about_window.geometry("350x200")

                                about_frame = tk.Frame(about_window)
                                about_frame.pack(fill="both", expand=True)
                                about_frame.place(relx=0.5, rely=0.5, anchor="center")

                                icon_label = tk.Label(about_frame, image=self.app_icon)
                                icon_label.image = self.app_icon
                                icon_label.pack()
                                
                                label = tk.Label(about_frame, text="OrangeBlox", font=("San Francisco", 16, "bold"))
                                label.pack(pady=2)
                                label2 = tk.Label(about_frame, text=f"Bootstrap Version {current_version.get('version')}\nMade by @EfazDev", font=("San Francisco", 12))
                                label2.pack(pady=5)
                            def show_validation_failed_menu(self):
                                self.master.title("Bootstrap Verification Failed")
                                self.master.geometry("500x400")
                                self.master.withdraw()
                                self.master.resizable(False, False)
                                self.master.attributes("-alpha", 1.0)

                                self.validation_frame = tk.Frame(self.master)
                                self.validation_frame.pack(fill="both", expand=True)
                                self.validation_frame.place(relx=0.5, rely=0.5, anchor="center")
                                self.holding_frame.place_forget()
                                self.master.update_idletasks()

                                icon_label = tk.Label(self.validation_frame, image=self.app_icon)
                                icon_label.image = self.app_icon
                                icon_label.pack()
                                
                                label = tk.Label(self.validation_frame, text="OrangeBlox", font=("San Francisco", 16, "bold"))
                                label.pack(pady=2)
                                label2 = tk.Label(self.validation_frame, text=f"Uh oh! There was an issue trying to validate hashes for the following files:", font=("San Francisco", 12))
                                label2.pack(pady=5)
                                label3 = tk.Label(self.validation_frame, text=f"{', '.join(unable_to_validate)}", font=("San Francisco", 12))
                                label3.pack(pady=5)
                                button = tk.Button(self.validation_frame, text=f"Continue without validation", command=self.start_bootstrap_without_validation)
                                button.pack(pady=5)
                            def show_help_menu(self):
                                import webbrowser
                                webbrowser.open("https://github.com/EfazDev/orangeblox/wiki")
                            def show_github_issues_menu(self):
                                import webbrowser
                                webbrowser.open("https://github.com/EfazDev/orangeblox/issues")
                            def on_window_activate(self, event):
                                try:
                                    self.button_click_count += 1
                                    self.requested_kill = False
                                    if not (event == "oranges") and ended == False: printMainMessage(f"Window was triggered! Current count: {self.button_click_count}")
                                    if self.button_click_count > 9:
                                        self.master.title("OrangeBlox")
                                        self.master.geometry("800x500")
                                        self.master.attributes("-alpha", 1.0)
                                        self.master.deiconify()

                                        if self.validation_frame: self.validation_frame.place_forget()
                                        self.holding_frame.pack(fill="both", expand=True)
                                        self.holding_frame.place(relx=0.5, rely=0.5, anchor="center")
                                        self.master.update_idletasks()
                                        if self.debug_mode_window_enabled == False:
                                            printDebugMessage("Debug Window Mode is now enabled! Now when clicking the taskbar icon, it will show this window instead of going to the terminal directly.")
                                            if not (event == "oranges"):
                                                printWarnMessage("--- Hello Robloxian! ---")
                                                printMainMessage("It seems like you found a secret easter egg!")
                                                printMainMessage("Well, it's just a command line but is something!")
                                                if not (main_config.get("EFlagEnableSecretJackpot") == False):
                                                    jackpot = random.randint(1, 100)
                                                    if jackpot == 1:
                                                        printSuccessMessage(f"Are you going to hit the jackpot? 1/100 => JACKPOT!! ({jackpot})")
                                                        printSuccessMessage("GG! You seek being lucky!")
                                                    else:
                                                        printErrorMessage(f"Are you going to hit the jackpot? 1/100 => Aw ({jackpot}) :(")
                                                        printErrorMessage("Try again next time!")
                                        self.debug_mode_window_enabled = True
                                    else:
                                        if ended == False: self.activate_terminal_window()
                                except Exception as e: 
                                    printErrorMessage(f"Unable to activate window: {str(e)}")
                            def load_logs(self, e=""):
                                try:
                                    new_logs = logs[self.last_checked_index:]
                                    for log, color_code in new_logs:
                                        lines = [(log[i:i+75]) for i in range(0, len(log), 75)]
                                        for line in lines:
                                            color_tag = COLOR_CODES.get(color_code, "white")
                                            self.output_area.config(state=tk.NORMAL)
                                            self.output_area.insert(tk.END, f" {line}\n", color_tag)
                                            self.output_area.config(state=tk.DISABLED)
                                    self.last_checked_index = len(logs)
                                    
                                    if self.is_at_bottom:
                                        self.output_area.see(tk.END)

                                except Exception as e:
                                    printErrorMessage(f"There was an error loading logs! Error: {str(e)}")
                                if e == "": self.master.after(100, self.load_logs)
                            def on_mouse_wheel(self, event):
                                if event.delta > 0:
                                    self.is_at_bottom = False
                                    self.output_area.yview_scroll(-1, "units")
                                elif event.delta < 0:
                                    self.is_at_bottom = True
                                    self.output_area.yview_scroll(1, "units")
                                scrollbar_position = self.output_area.yview()
                                if scrollbar_position[1] == 1.0:
                                    self.is_at_bottom = True
                                else:
                                    self.is_at_bottom = False
                            def reset_button_click(self):
                                if self.debug_mode_window_enabled == False:
                                    self.button_click_count = 0
                                    self.master.after(10000, self.reset_button_click)
                            def check_end(self):
                                global ended
                                try:
                                    if ended == True:
                                        if self.debug_mode_window_enabled == False or self.requested_kill == True: 
                                            self.master.withdraw()
                                            self.master.quit()
                                            self.master.destroy()
                                            printSuccessMessage("Successfully ended Tkinter app!")
                                        else:
                                            printSuccessMessage("Bootstrap window has been closed successfully! You may close this window normally!")
                                            self.button.destroy()
                                    else:
                                        self.master.after(100, self.check_end)
                                except Exception as e:
                                    printErrorMessage(f"Tkinter App Closing Failed! Error: {str(e)}")
                            def start_bootstrap_without_validation(self):
                                if self.validation_frame: 
                                    self.validation_frame.destroy()
                                    self.validation_frame = None
                                main_config["EFlagDisableSecureHashSecurity"] = True
                                def sta():
                                    global associated_terminal_pid
                                    global ended
                                    ended = False
                                    threading.Thread(target=startBootstrap, daemon=False).start()
                                threading.Thread(target=sta, daemon=True).start()
                                self.holding_frame.place(relx=0.5, rely=0.5, anchor="center")
                                self.master.title("OrangeBlox")
                                self.master.geometry("1x1")
                                self.master.resizable(False, False)
                                self.master.attributes("-alpha", 0.0)
                            def activate_terminal_window(self, event=""): 
                                activateTerminalWindow(event)
                        try:
                            app_root = tk.Tk()
                            app = App(app_root)
                            if main_config.get("EFlagEnableTkinterDockMenu") == True: threading.Thread(target=app.generate_dock_menu, daemon=True).start()
                            app_root.after(100, app_root.deiconify)
                            app_root.mainloop()
                        except Exception as e:
                            printErrorMessage(f"Tkinter App Failed! Error: {str(e)}")
                    except Exception as e:
                        printErrorMessage(f"Tkinter App Failed! Error: {str(e)}")
                except Exception as e:
                    printErrorMessage(str(e))
            
            if not (main_config.get("EFlagDisableCreatingTkinterApp") == True):
                threading.Thread(target=notificationLoop, daemon=False).start()
                threading.Thread(target=terminalAwaitLoop, daemon=True).start()
                if (main_config.get("EFlagNumberOfTkinterAppsAllowed", 1)) > 0:
                    threading.Thread(target=startBootstrap, daemon=False).start()
                    app_count = pip_class.getAmountOfProcesses("OrangeBloxMain")
                    if app_count < main_config.get("EFlagNumberOfTkinterAppsAllowed", 1): 
                        with open(os.path.join(app_path, f"TkinterAppOpened_{user_folder_name}"), "w", encoding="utf-8") as f:
                            f.write(str(datetime.datetime.now(datetime.timezone.utc).timestamp()))
                        createTkinterAppReplication()
                        try:
                            os.remove(os.path.join(app_path, f"TkinterAppOpened_{user_folder_name}"))
                        except Exception:
                            printMainMessage("Unable to remove tkinter app holder")
                    else:
                        while ended == False and os.path.exists(os.path.join(app_path, f"TkinterAppOpened_{user_folder_name}")):
                            time.sleep(0.5)
                        if ended == False: 
                            with open(os.path.join(app_path, f"TkinterAppOpened_{user_folder_name}"), "w", encoding="utf-8") as f:
                                f.write(str(datetime.datetime.now(datetime.timezone.utc).timestamp()))
                            createTkinterAppReplication()
                            try:
                                os.remove(os.path.join(app_path, f"TkinterAppOpened_{user_folder_name}"))
                            except Exception:
                                printMainMessage("Unable to remove tkinter app holder")
                else:
                    threading.Thread(target=startBootstrap, daemon=False).start()
                    createTkinterAppReplication()
            else:
                threading.Thread(target=terminalAwaitLoop, daemon=True).start()
                threading.Thread(target=notificationLoop, daemon=False).start()
                startBootstrap()
        except Exception as e:
            printErrorMessage(f"Bootstrap Run Failed: {str(e)}")
            sys.exit(0)
    elif main_os == "Windows":
        filtered_args = ""
        loaded_json = True
        local_app_data = pip_class.getLocalAppData()
        
        if os.path.exists(os.path.join(app_path, "Main.py")):
            os.system("title OrangeBlox 🍊")
            os.system("chcp 65001")
            printMainMessage(f"Loading Configuration File..")
            with open(os.path.join(app_path, "Configuration.json"), "r", encoding="utf-8") as f:
                try:
                    main_config = json.load(f)
                except Exception as e:
                    loaded_json = False

            if os.path.exists(os.path.join(app_path, "BootstrapCooldown")):
                if not main_config.get("EFlagDisableBootstrapCooldown") == True:
                    with open(os.path.join(app_path, "BootstrapCooldown"), "r", encoding="utf-8") as f:
                        te = f.read()
                        if te.isnumeric():
                            if datetime.datetime.now(tz=datetime.UTC).timestamp() < int(te):
                                printErrorMessage("You're starting the booldown too fast! Please wait 1 seconds!")
                                printDebugMessage(f'If this message is still here after 1 seconds, delete the file "{app_path}/Resources/BootstrapCooldown"')
                                sys.exit(0)
            else:
                def cool():
                    with open(os.path.join(app_path, "BootstrapCooldown"), "w", encoding="utf-8") as f:
                        f.write(str(int(datetime.datetime.now(tz=datetime.UTC).timestamp()) + 1))
                    time.sleep(main_config.get("EFlagBootstrapCooldownAmount", 1))
                    if os.path.exists(os.path.join(app_path, "BootstrapCooldown")):
                        os.remove(os.path.join(app_path, "BootstrapCooldown"))
                threading.Thread(target=cool, daemon=True).start()

            if len(args) > 1:
                filtered_args = args[1]
                if (("roblox-player:" in filtered_args) or ("roblox-studio:" in filtered_args) or ("roblox-studio-auth:" in filtered_args) or ("roblox:" in filtered_args) or ("efaz-bootstrap:" in filtered_args) or ("orangeblox:" in filtered_args) or os.path.isfile(filtered_args)):
                    printMainMessage(f"Creating URL Exchange file..")
                    if os.path.exists(app_path):
                        with open(os.path.join(app_path, "URLSchemeExchange"), "w", encoding="utf-8") as f:
                            f.write(filtered_args)
                    else:
                        with open("URLSchemeExchange", "w", encoding="utf-8") as f:
                            f.write(filtered_args)

            printMainMessage("Finding Python Executable..")
            if pip_class.pythonInstalled(computer=True) == False: pip_class.pythonInstall()
            pythonExecutable = pip_class.findPython()
            if main_config.get("EFlagSpecifyPythonExecutable"): pythonExecutable = main_config.get("EFlagSpecifyPythonExecutable")
            if not os.path.exists(pythonExecutable):
                printErrorMessage("Please install Python in order to run this bootstrap!")
                input("> ")
                sys.exit(0)
            else:
                printMainMessage(f"Detected Python Executable: {pythonExecutable}")

            try:
                ended = False
                def awake():
                    global ended
                    seconds = 0
                    printMainMessage("Starting Notification Loop..")
                    while True:
                        try:
                            if ended == True:
                                break
                            if os.path.exists(os.path.join(app_path, "AppNotification")):
                                with open(os.path.join(app_path, "AppNotification"), "r", encoding="utf-8") as f:
                                    try:
                                        notification = json.load(f)
                                        if type(notification) is list:
                                            class InvalidNotificationException(Exception):
                                                pass
                                            raise InvalidNotificationException("The following data for notification is not valid.")
                                    except Exception as e:
                                        printDebugMessage(str(e))
                                        notification = {"title": "Something went wrong.", "message": "An unexpected error occurred while loading this notification."}
                                if os.path.exists(os.path.join(app_path, "AppNotification")): os.remove(os.path.join(app_path, "AppNotification"))
                                if notification.get("title") and notification.get("message"):
                                    displayNotification(notification["title"], notification["message"])
                                    printSuccessMessage("Successfully pinged app notification!")
                            seconds += 1
                        except Exception as e:
                            printErrorMessage(f"There was an issue making a notification: {str(e)}")
                        time.sleep(0.05)
                def startBootstrap():
                    global ended
                    try:
                        printMainMessage(f"Validating Bootstrap Scripts..")
                        a_file_hash = generateFileHash(os.path.join(app_path, "Main.py"))
                        b_file_hash = generateFileHash(os.path.join(app_path, "RobloxFastFlagsInstaller.py"))
                        c_file_hash = generateFileHash(os.path.join(app_path, "Install.py"))
                        d_file_hash = generateFileHash(os.path.join(app_path, "OrangeAPI.py"))
                        e_file_hash = generateFileHash(os.path.join(app_path, "DiscordPresenceHandler.py"))
                        f_file_hash = generateFileHash(os.path.join(app_path, "PipHandler.py"))

                        validated = True
                        unable_to_validate = []
                        integrated_app_hashes = current_version.get("hashes", {})
                        if not (a_file_hash == integrated_app_hashes.get("main")): validated = False; unable_to_validate.append("Main.py")
                        if not (b_file_hash == integrated_app_hashes.get("fflag_install")): validated = False; unable_to_validate.append("RobloxFastFlagsInstaller.py")
                        if not (c_file_hash == integrated_app_hashes.get("install")): validated = False; unable_to_validate.append("Install.py")
                        if not (d_file_hash == integrated_app_hashes.get("bootstrap_api")): validated = False; unable_to_validate.append("OrangeAPI.py")
                        if not (e_file_hash == integrated_app_hashes.get("discord_presence")): validated = False; unable_to_validate.append("DiscordPresenceHandler.py")
                        if not (f_file_hash == integrated_app_hashes.get("pip_handler")): validated = False; unable_to_validate.append("PipHandler.py")

                        if not (validated == True or main_config.get("EFlagDisableSecureHashSecurity") == True):
                            printErrorMessage(f"Uh oh! There was an issue trying to validate hashes for the following files: {', '.join(unable_to_validate)}")
                            printErrorMessage(f"Would you like to skip verification? Hashes that are unable to be validated are listed below:")
                            if not (a_file_hash == integrated_app_hashes["main"]):  printMainMessage(f'Main.py | {integrated_app_hashes["main"]} => {a_file_hash}')
                            if not (b_file_hash == integrated_app_hashes["fflag_install"]): printMainMessage(f'RobloxFastFlagsInstaller.py | {integrated_app_hashes["fflag_install"]} => {b_file_hash}')
                            if not (c_file_hash == integrated_app_hashes["install"]): printMainMessage(f'Install.py | {integrated_app_hashes["install"]} => {c_file_hash}')
                            if not (d_file_hash == integrated_app_hashes["bootstrap_api"]): printMainMessage(f'OrangeAPI.py | {integrated_app_hashes["bootstrap_api"]} => {d_file_hash}')
                            if not (e_file_hash == integrated_app_hashes["discord_presence"]): printMainMessage(f'DiscordPresenceHandler.py | {integrated_app_hashes["discord_presence"]} => {e_file_hash}')
                            if not (f_file_hash == integrated_app_hashes["pip_handler"]): printMainMessage(f'PipHandler.py | {integrated_app_hashes["pip_handler"]} => {f_file_hash}')
                            if isYes(input("> ")) == False: ended = True; sys.exit(0)
                            displayNotification("Uh oh!", "Your copy of OrangeBlox was unable to be validated!")
                        printMainMessage(f"Running Bootstrap..")
                        os.system("cls" if os.name == "nt" else 'echo "\033c\033[3J"; clear')
                        if main_config.get("EFlagDisableSecureHashSecurity") == True: displayNotification("Security Notice", "Hash Verification is currently disabled. Please check your configuration and mod scripts if you didn't disable this!")
                        result = subprocess.run([pythonExecutable, os.path.join(app_path, "Main.py")], shell=True, cwd=os.path.join(app_path))
                        printMainMessage("Ending Bootstrap..")
                        ended = True
                        if result.returncode == 0: printSuccessMessage(f"Bootstrap Run Success: {result.returncode}")
                        else: printErrorMessage(f"Bootstrap Run Failed: {result.returncode}")
                        sys.exit(0)
                    except Exception as e:
                        printErrorMessage(f"Bootstrap Run Failed: {str(e)}")
                        sys.exit(0)
                threading.Thread(target=awake, daemon=True).start()
                startBootstrap()
            except Exception as e:
                traceback.print_exc()
                traceback_err_str = traceback.format_exc()
                printErrorMessage(f"Bootstrap Run Failed: {traceback_err_str}")
                sys.exit(0)
        else:
            printMainMessage("Please install the bootstrap using the Install.py command!!")
            input("> ")
            sys.exit(0)
else:
    class OrangeBloxNotModule(Exception):
        def __init__(self): super().__init__("OrangeBlox is only a runable instance, not a module.")
    class OrangeBloxInstallerNotModule(Exception):
        def __init__(self): super().__init__("The installer for OrangeBlox is only a runable instance, not a module.")
    class OrangeBloxLoaderNotModule(Exception):
        def __init__(self): super().__init__("The loader for OrangeBlox is only a runable instance, not a module.")
    raise OrangeBloxLoaderNotModule()