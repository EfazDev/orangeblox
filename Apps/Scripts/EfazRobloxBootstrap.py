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
import hashlib
from PipHandler import pip

if __name__ == "__main__":
    current_version = {"version": "1.4.1"}
    main_os = platform.system()
    args = sys.argv
    generated_app_id = str(uuid.uuid4())
    pip_class = pip()
    logs = []

    COLOR_CODES = {
        0: "white",
        1: "red",
        2: "yellow",
        3: "orange",
        4: "green",
    }

    def printMainMessage(mes): 
        print(f"\033[38;5;255m{mes}\033[0m")
        logs.append((mes, 0))
    def printErrorMessage(mes): 
        print(f"\033[38;5;196m{mes}\033[0m")
        logs.append((mes, 1))
    def printSuccessMessage(mes): 
        print(f"\033[38;5;82m{mes}\033[0m")
        logs.append((mes, 4))
    def printWarnMessage(mes): 
        print(f"\033[38;5;202m{mes}\033[0m")
        logs.append((mes, 3))
    def printDebugMessage(mes): 
        print(f"\033[38;5;226m{mes}\033[0m")
        logs.append((mes, 2))

    printWarnMessage("-----------")
    printWarnMessage("Welcome to Efaz's Roblox Bootstrap Loader!")
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
                    from plyer import notification
                except Exception as e:
                    pip_class.install(["plyer"])
                    from plyer import notification
                notification.notify(
                    title = title,
                    message = message,
                    app_icon = os.path.join(local_app_data, "EfazRobloxBootstrap", "AppIcon.ico"),
                    timeout = 30,
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
    def generateFileHash(file_path, algorithm="sha256"):
        hasher = hashlib.new(algorithm)
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()
    
    with open(os.path.join(os.path.dirname(__file__), "GeneratedHash.json"), "r") as f:
        integrated_app_hashes = json.load(f)

    if main_os == "Darwin":
        filtered_args = ""
        loaded_json = True
        use_shell = False

        printMainMessage(f"Loading Configuration File..")
        if os.path.exists("/Applications/EfazRobloxBootstrap.app/Contents/Resources/FastFlagConfiguration.json"):
            with open("/Applications/EfazRobloxBootstrap.app/Contents/Resources/FastFlagConfiguration.json", "r") as f:
                try:
                    fflag_configuration = json.load(f)
                except Exception as e:
                    loaded_json = False
        else:
            with open("FastFlagConfiguration.json", "r") as f:
                try:
                    fflag_configuration = json.load(f)
                except Exception as e:
                    loaded_json = False

        def printDebugMessage(mes): 
            if fflag_configuration.get("EFlagEnableDebugMode") == True: 
                print(f"\033[38;5;226m{mes}\033[0m")
                logs.append((mes, 2))

        if pip_class.pythonInstalled() == False: pip_class.pythonInstall()
        pythonExecutable = pip_class.findPython()
        if not pythonExecutable:
            printErrorMessage("Please install Python in order to run this bootstrap!")
            input("> ")
            sys.exit(0)
        else:
            printMainMessage(f"Detected Python Executable: {pythonExecutable}")

        printMainMessage(f"Generated App Window Fetching ID: {generated_app_id}")

        execute_command = f"unset HISTFILE && cd /Applications/EfazRobloxBootstrap.app/Contents/Resources/ && {pythonExecutable} Main.py && exit"
        printMainMessage(f"Loading Runner Command: {execute_command}")

        if len(args) > 1:
            filtered_args = args[1]
            if (("roblox-player:" in filtered_args) or ("roblox:" in filtered_args)) and not (loaded_json == True and fflag_configuration.get("EFlagEnableDebugMode") == True):
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
            do shell script "echo " & terminal_id & " > " & quoted form of "/Applications/EfazRobloxBootstrap.app/Contents/Resources/Terminal_{generated_app_id}"
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
            associated_terminal_pid = None

            def awake():
                global associated_terminal_pid
                seconds = 0
                printMainMessage("Starting Notification Loop..")
                while True:
                    try:
                        if ended == True: break
                        if os.path.exists("/Applications/EfazRobloxBootstrap.app/Contents/Resources/AppNotification"):
                            with open("/Applications/EfazRobloxBootstrap.app/Contents/Resources/AppNotification", "r") as f:
                                try:
                                    notification = json.load(f)
                                    if type(notification) is list:
                                        class InvalidNotificationException(Exception):
                                            pass
                                        raise InvalidNotificationException("The following data for notification is not valid.")
                                except Exception as e:
                                    printDebugMessage(str(e))
                                    notification = {"title": "Something went wrong.", "message": "An unexpected error occurred while loading this notification."}
                            os.remove("/Applications/EfazRobloxBootstrap.app/Contents/Resources/AppNotification")
                            if notification.get("title") and notification.get("message"):
                                displayNotification(notification["title"], notification["message"])
                                printSuccessMessage("Successfully pinged notification!")
                        if os.path.exists(f"/Applications/EfazRobloxBootstrap.app/Contents/Resources/Terminal_{generated_app_id}"):
                            with open(f"/Applications/EfazRobloxBootstrap.app/Contents/Resources/Terminal_{generated_app_id}", "r") as f:
                                try:
                                    cont = f.read().replace(" ", "").replace("\n", "")
                                    if cont.isnumeric() and not cont == "0":
                                        associated_terminal_pid = int(cont)
                                except Exception as e:
                                    printDebugMessage(str(e))
                            os.remove(f"/Applications/EfazRobloxBootstrap.app/Contents/Resources/Terminal_{generated_app_id}")
                            printDebugMessage(f"Received Terminal ID from Receiver: {associated_terminal_pid}")
                        seconds += 1
                    except Exception as e:
                        printErrorMessage(f"There was an issue making a notification: {str(e)}")
                    time.sleep(0.05)
            def startBootstrap():
                global ended
                printMainMessage(f"Starting Bootstrap..")
                try:
                    a_file_hash = generateFileHash("/Applications/EfazRobloxBootstrap.app/Contents/Resources/Main.py")
                    b_file_hash = generateFileHash("/Applications/EfazRobloxBootstrap.app/Contents/Resources/RobloxFastFlagsInstaller.py")
                    c_file_hash = generateFileHash("/Applications/EfazRobloxBootstrap.app/Contents/Resources/Install.py")
                    d_file_hash = generateFileHash("/Applications/EfazRobloxBootstrap.app/Contents/Resources/Uninstall.py")
                    e_file_hash = generateFileHash("/Applications/EfazRobloxBootstrap.app/Contents/Resources/EfazRobloxBootstrapAPI.py")
                    f_file_hash = generateFileHash("/Applications/EfazRobloxBootstrap.app/Contents/Resources/DiscordPresenceHandler.py")

                    validated = True
                    unable_to_validate = []
                    if not (a_file_hash == integrated_app_hashes["main"]): 
                        validated = False
                        unable_to_validate.append("Main.py")
                    if not (b_file_hash == integrated_app_hashes["fflag_install"]):
                        validated = False
                        unable_to_validate.append("RobloxFastFlagsInstaller.py")
                    if not (c_file_hash == integrated_app_hashes["install"]):
                        validated = False
                        unable_to_validate.append("Install.py")
                    if not (d_file_hash == integrated_app_hashes["uninstall"]):
                        validated = False
                        unable_to_validate.append("Uninstall.py")
                    if not (e_file_hash == integrated_app_hashes["bootstrap_api"]):
                        validated = False
                        unable_to_validate.append("EfazRobloxBootstrapAPI.py")
                    if not (f_file_hash == integrated_app_hashes["discord_presence"]):
                        validated = False
                        unable_to_validate.append("DiscordPresenceHandler.py")

                    if validated == True or fflag_configuration.get("EFlagDisableSecureHashSecurity") == True:
                        if fflag_configuration.get("EFlagDisableSecureHashSecurity") == True: displayNotification("Security Notice", "Hash Verification is currently disabled. Please check your FFlag configuration and your mod scripts if this wasn't you!")
                        result = subprocess.run(args=["osascript", "-e", applescript], check=True, capture_output=True)
                        printMainMessage("Ending Bootstrap..")
                        ended = True
                        if result.returncode == 0:
                            printSuccessMessage(f"Bootstrap Run Success: {result.returncode}")
                            sys.exit(0)
                        else:
                            printErrorMessage(f"Bootstrap Run Failed: {result.returncode}")
                            sys.exit(0)
                    else:
                        printErrorMessage(f"Unable to validate hashes for files: {', '.join(unable_to_validate)}")
                        displayNotification("Uh oh!", "Your copy of Efaz's Roblox Bootstrap was unable to be validated and must be reinstalled! Please download a new copy from GitHub!")
                        sys.exit(0)
                except Exception as e:
                    ended = True
                    printErrorMessage(f"Bootstrap Run Failed: {str(e)}")
                    sys.exit(0)
            def createTkinterAppReplication():
                try:
                    printMainMessage(f"Starting Tkinter App Replication..")
                    while associated_terminal_pid == None and ended == False:
                       time.sleep(0.05)
                    if associated_terminal_pid:
                        try:
                            if getattr(sys, "frozen", False):
                                os.environ["TCL_LIBRARY"] = "/Applications/EfazRobloxBootstrap.app/Contents/MacOS/Efaz\'s Roblox Bootstrap.app/Contents/Resources/_tcl_data"
                                os.environ["TK_LIBRARY"] = "/Applications/EfazRobloxBootstrap.app/Contents/MacOS/Efaz\'s Roblox Bootstrap.app/Contents/Resources/_tk_data"
                            else:
                                os.environ["TCL_LIBRARY"] = "/Library/Frameworks/Python.framework/Versions/3.13/Frameworks/Tcl.framework/Versions/8.6/Resources/Scripts/"
                                os.environ["TK_LIBRARY"] = "/Library/Frameworks/Python.framework/Versions/3.13/Frameworks/Tk.framework/Versions/8.6/Resources/Scripts/"
                            import tkinter as tk
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

                                def __init__(self, master: tk.Tk):
                                    try:
                                        self.master = master
                                        self.master.title("Efaz's Roblox Bootstrap")
                                        self.master.geometry("1x1")
                                        self.master.withdraw()
                                        self.master.resizable(False, False)
                                        self.master.attributes("-alpha", 0.0)

                                        self.holding_frame = tk.Frame(self.master)
                                        self.holding_frame.pack(fill="both", expand=True)
                                        self.holding_frame.place(relx=0.5, rely=0.5, anchor="center")
                                        app_icon_url = "/Applications/EfazRobloxBootstrap.app/Contents/Resources/BootstrapImages/AppIcon64.png"
                                        if os.path.exists(app_icon_url):
                                            self.app_icon = tk.PhotoImage(file=app_icon_url)
                                        else:
                                            self.app_icon = tk.PhotoImage(file="/Applications/EfazRobloxBootstrap.app/Contents/Resources/AppIcon.icns")
                                        icon_label = tk.Label(self.holding_frame, image=self.app_icon)
                                        icon_label.image = self.app_icon
                                        icon_label.pack()
                                        self.label = tk.Label(self.holding_frame, text="Ooh! Hi there! Welcome to Efaz's Roblox Bootstrap!")
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

                                        for key, color in COLOR_CODES.items():
                                            self.output_area.tag_config(f"color_{key}", foreground=color)
                                        self.button = tk.Button(self.holding_frame, text=f"Go to bootstrap terminal window!", command=self.on_button_click)
                                        self.button.pack(pady=5)

                                        self.holding_frame.bind("<Activate>", self.on_window_activate)
                                        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
                                        self.master.protocol("WM_ICONIFY", self.prevent_minimize)
                                        self.terminal_window = associated_terminal_pid

                                        self.top_menu = tk.Menu(self.master)
                                        main_menu = tk.Menu(self.top_menu, name='apple')
                                        self.top_menu.add_cascade(menu=main_menu)
                                        main_menu.add_command(label="About Efaz's Roblox Bootstrap", command=self.show_about_menu)
                                        self.master.createcommand("tk::mac::Quit" , self.on_close)

                                        file_menu = tk.Menu(self.top_menu)
                                        self.top_menu.add_cascade(label="File", menu=file_menu)
                                        file_menu.add_command(label="New Bootstrap Window", command=self.new_bootstrap)
                                        file_menu.add_command(label="Open Debug Window", command=self.instant_debug_window)
                                        file_menu.add_separator()
                                        file_menu.add_command(label="Run Roblox in New Bootstrap Window", command=self.new_bootstrap_play_roblox)
                                        if fflag_configuration.get("EFlagEnableDuplicationOfClients") == True: file_menu.add_command(label="Multi-Run Roblox in New Bootstrap Window", command=self.new_bootstrap_play_multi_roblox)
                                        file_menu.add_command(label="Run Roblox Fast Flags Installer", command=self.new_bootstrap_run_fflag_installer)
                                        file_menu.add_command(label="Clear Roblox Logs", command=self.new_bootstrap_clear_roblox_logs)
                                        file_menu.add_command(label="Reinstall Roblox", command=self.new_bootstrap_reinstall_roblox)
                                        file_menu.add_command(label="End All Roblox Windows", command=self.new_bootstrap_end_roblox)
                                        file_menu.add_separator()
                                        file_menu.add_command(label="Open Mods Manager", command=self.new_bootstrap_open_mods_manager)
                                        file_menu.add_command(label="Open Settings", command=self.new_bootstrap_open_settings)
                                        file_menu.add_command(label="Open Credits", command=self.new_bootstrap_open_credits)

                                        shortcuts_menu = tk.Menu(self.top_menu)
                                        self.top_menu.add_cascade(label="Shortcuts", menu=shortcuts_menu)
                                        generated_ui_options = []
                                        if type(fflag_configuration.get("EFlagRobloxLinkShortcuts")) is dict:
                                            for i, v in fflag_configuration.get("EFlagRobloxLinkShortcuts").items():
                                                if v and v.get("name") and v.get("id") and v.get("url"):
                                                    generated_ui_options.append({"index": 1, "message": f"{v.get('name')} [{i}]", "shortcut_info": v})
                                        if len(generated_ui_options) > 0:
                                            for p in generated_ui_options:
                                                def hand():
                                                    self.new_bootstrap(f"shortcuts/{p['shortcut_info'].get('id')}", f"Open Shortcut ({p['message']})")
                                                shortcuts_menu.add_command(label=p["message"], command=hand)
                                            shortcuts_menu.add_separator()
                                        shortcuts_menu.add_command(label="Open Shortcuts Menu", command=self.new_bootstrap_open_shortcuts)

                                        options_menu = tk.Menu(self.top_menu)
                                        self.top_menu.add_cascade(label="Options", menu=options_menu)
                                        options_menu.add_command(label="Clear Debug Window Logs", command=self.clear_logs)
                                        options_menu.add_command(label="Close App", command=self.on_close)

                                        help_menu = tk.Menu(self.top_menu)
                                        self.top_menu.add_cascade(label="Help", menu=help_menu)
                                        help_menu.add_command(label="Efaz's Roblox Bootstrap Wiki", command=self.show_help_menu)
                                        help_menu.add_command(label="GitHub Issues", command=self.show_github_issues_menu)

                                        try:
                                            if self.top_menu and main_menu and help_menu:
                                                master.config(menu=self.top_menu)
                                        except Exception as e:
                                            printErrorMessage(f"Menu configuration error: {str(e)}")

                                        if not self.terminal_window:
                                            printErrorMessage(f"Unable to get terminal window ID!")
                                        else:
                                            try:
                                                if ended == False:
                                                    self.check_end()
                                                    self.reset_button_click()
                                                    self.load_logs()
                                                    threading.Thread(target=self.generate_dock_menu, daemon=True).start()
                                                else:
                                                    self.master.quit()
                                            except Exception as e:
                                                printErrorMessage(f"Something went wrong checking! Error: {str(e)}")
                                            printMainMessage(f"Tkinter app finished launching! Terminal ID: {self.terminal_window}")
                                    except Exception as e:
                                        printErrorMessage(f"Tkinter App Failed! Error: {str(e)}")
                                def on_button_click(self):
                                    self.activate_terminal_window()
                                def on_close(self):
                                    if ended == True:
                                        printMainMessage("Closing debug window..")
                                        self.master.quit()
                                    else:
                                        self.kill_bootstrap_window()
                                def prevent_minimize(self):
                                    printDebugMessage("Prevented minimizing main window in order to keep app running smoothly.")
                                def generate_dock_menu(self):
                                    from AppKit import NSApplication, NSMenu, NSMenuItem
                                    from Foundation import NSObject

                                    generated_ui_options = []
                                    if type(fflag_configuration.get("EFlagRobloxLinkShortcuts")) is dict:
                                        for i, v in fflag_configuration.get("EFlagRobloxLinkShortcuts").items():
                                            if v and v.get("name") and v.get("id") and v.get("url"):
                                                generated_ui_options.append({"index": 1, "message": f"{v.get('name')} [{i}]", "shortcut_info": v})

                                    main_app = self
                                    class DockAppDelegate(NSObject):
                                        def newBootstrapWindow_(self, sender):
                                            main_app.new_bootstrap()
                                        def runRoblox_(self, sender):
                                            main_app.new_bootstrap_play_roblox()
                                        def multiRunRoblox_(self, sender):
                                            main_app.new_bootstrap_play_multi_roblox()
                                        def reinstallRoblox_(self, sender):
                                            main_app.new_bootstrap_reinstall_roblox()
                                        def endAllRoblox_(self, sender):
                                            main_app.new_bootstrap_end_roblox()
                                        def runFFlagInstaller_(self, sender):
                                            main_app.new_bootstrap_run_fflag_installer()
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
                                    self.cocoa_app = NSApplication.sharedApplication()
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
                                    menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Run Roblox in New Bootstrap Window", "runRoblox:", "")
                                    menu_item.setEnabled_(True)
                                    self.dock_menu.addItem_(menu_item)
                                    if fflag_configuration.get("EFlagEnableDuplicationOfClients") == True: 
                                        menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Multi-Run Roblox in New Bootstrap Window", "multiRunRoblox:", "")
                                        menu_item.setEnabled_(True)
                                        self.dock_menu.addItem_(menu_item)
                                    menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Run Roblox Fast Flags Installer", "runFFlagInstaller:", "")
                                    menu_item.setEnabled_(True)
                                    self.dock_menu.addItem_(menu_item)
                                    menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Reinstall Roblox", "reinstallRoblox:", "")
                                    menu_item.setEnabled_(True)
                                    self.dock_menu.addItem_(menu_item)
                                    menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("End All Roblox Windows", "endAllRoblox:", "")
                                    menu_item.setEnabled_(True)
                                    self.dock_menu.addItem_(menu_item)
                                    self.dock_menu.addItem_(NSMenuItem.separatorItem())
                                    if len(generated_ui_options) > 0:
                                        for p in generated_ui_options:
                                            menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(p["message"], "shortcut:", "")
                                            menu_item.setEnabled_(True)
                                            self.dock_menu.addItem_(menu_item)
                                    menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Open Shortcuts Menu", "shortcutmenu:", "")
                                    menu_item.setEnabled_(True)
                                    self.dock_menu.addItem_(menu_item)
                                    self.cocoa_app.setDockMenu_(self.dock_menu)
                                    self.cocoa_app.run()
                                def new_bootstrap(self, action="", action_name=""):
                                    if not (action == "") and type(action) is str:
                                        url_scheme_path = "/Applications/EfazRobloxBootstrap.app/Contents/Resources/URLSchemeExchange"
                                        with open(url_scheme_path, "w") as f:
                                            f.write(f"efaz-bootstrap://{action}?quick-action=true")
                                    subprocess.Popen(f'open -n -a "/Applications/EfazRobloxBootstrap.app/Contents/MacOS/Efaz\'s Roblox Bootstrap.app/Contents/MacOS/EfazRobloxBootstrapMain"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                                    if not (action_name == "") and type(action_name) is str:
                                        printMainMessage(f"Launched Bootstrap with action: {action_name}")
                                    else:
                                        printMainMessage(f"Launched Bootstrap in new window!")
                                def new_bootstrap_play_roblox(self):
                                    self.new_bootstrap("continue", "Play Roblox")
                                def new_bootstrap_play_multi_roblox(self):
                                    self.new_bootstrap("new", "Multi-Play Roblox")
                                def new_bootstrap_clear_roblox_logs(self):
                                    self.new_bootstrap("clear-logs", "Clear Roblox Logs")
                                def new_bootstrap_reinstall_roblox(self):
                                    self.new_bootstrap("reinstall-roblox", "Reinstall Roblox")
                                def new_bootstrap_end_roblox(self):
                                    self.new_bootstrap("end-roblox", "End Roblox")
                                def new_bootstrap_run_fflag_installer(self):
                                    self.new_bootstrap("fflag-install", "Run RobloxFastFlagsInstaller")
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
                                    about_window.title("About Efaz's Roblox Bootstrap")
                                    about_window.geometry("350x200")

                                    about_frame = tk.Frame(about_window)
                                    about_frame.pack(fill="both", expand=True)
                                    about_frame.place(relx=0.5, rely=0.5, anchor="center")

                                    icon_label = tk.Label(about_frame, image=self.app_icon)
                                    icon_label.image = self.app_icon
                                    icon_label.pack()
                                    
                                    label = tk.Label(about_frame, text="Efaz's Roblox Bootstrap", font=("San Francisco", 16, "bold"))
                                    label.pack(pady=2)
                                    label2 = tk.Label(about_frame, text=f"Bootstrap Version {current_version.get('version')}\nMade by @EfazDev", font=("San Francisco", 12))
                                    label2.pack(pady=5)
                                def show_help_menu(self):
                                    import webbrowser
                                    webbrowser.open("https://github.com/EfazDev/roblox-bootstrap/wiki")
                                def show_github_issues_menu(self):
                                    import webbrowser
                                    webbrowser.open("https://github.com/EfazDev/roblox-bootstrap/issues")
                                def on_window_activate(self, event):
                                    try:
                                        self.button_click_count += 1
                                        self.requested_kill = False
                                        if not (event == "oranges") and ended == False: printMainMessage(f"Window was triggered! Current count: {self.button_click_count}")
                                        if self.button_click_count > 9:
                                            self.master.geometry("800x500")
                                            self.master.attributes("-alpha", 1.0)
                                            self.master.deiconify()
                                            if self.debug_mode_window_enabled == False:
                                                printDebugMessage("Debug Window Mode is now enabled! Now when clicking the taskbar icon, it will show this window instead of going to the terminal directly.")
                                                if not (event == "oranges"):
                                                    printWarnMessage("--- Hello Robloxian! ---")
                                                    printMainMessage("It seems like you found a secret easter egg!")
                                                    printMainMessage("Well, it's just a command line but is something!")
                                                    if random.randint(1, 150) == 1:
                                                        printSuccessMessage(f"Might as well gamble! 1/150 => JACKPOT!!")
                                                        printSuccessMessage("GG! You seek being lucky!")
                                                    else:
                                                        printErrorMessage(f"Might as well gamble! 1/150 => Aw :(")
                                                        printMainMessage("Try again next time!")
                                            self.debug_mode_window_enabled = True
                                        else:
                                            if ended == False: self.activate_terminal_window()
                                    except Exception as e: 
                                        printErrorMessage(f"Unable to activate window: {str(e)}")
                                def load_logs(self, e=""):
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
                                    try:
                                        if ended == True:
                                            if self.debug_mode_window_enabled == False or self.requested_kill == True: 
                                                self.master.quit()
                                            else:
                                                printSuccessMessage("Bootstrap window has been closed successfully! You may close this window normally!")
                                                self.button.destroy()
                                        else:
                                            self.master.after(100, self.check_end)
                                    except Exception as e:
                                        printErrorMessage(f"Tkinter App Closing Failed! Error: {str(e)}")
                                def activate_terminal_window(self, event=""): 
                                    try:
                                        if self.terminal_window and self.activate_cooldown == False:
                                            self.activate_cooldown = True
                                            apple_script = f'''tell application "Terminal"
                                                activate
                                                set targetWindow to first window whose id is {self.terminal_window}
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
                                            self.activate_cooldown = False
                                    except Exception as e:
                                        printErrorMessage(f"Error activating Terminal window.")
                            try:
                                app_root = tk.Tk()
                                app = App(app_root)
                                app_root.after(100, app_root.deiconify)
                                app_root.mainloop()
                            except Exception as e:
                                printErrorMessage(f"Tkinter App Failed! Error: {str(e)}")
                        except Exception as e:
                            printErrorMessage(f"Tkinter App Failed! Error: {str(e)}")
                    else:
                        printErrorMessage(f"Unable to get terminal pid. Response: {associated_terminal_pid}")
                except Exception as e:
                    printErrorMessage(str(e))
            if not (fflag_configuration.get("EFlagDisableCreatingTkinterApp") == True):
                threading.Thread(target=awake, daemon=False).start()
                threading.Thread(target=startBootstrap, daemon=False).start()
                createTkinterAppReplication()
            else:
                threading.Thread(target=awake).start()
                startBootstrap()
        except Exception as e:
            printErrorMessage(f"Bootstrap Run Failed: {str(e)}")
            sys.exit(0)
    elif main_os == "Windows":
        filtered_args = ""
        loaded_json = True
        local_app_data = pip_class.getLocalAppData()
        
        if os.path.exists(os.path.join(local_app_data, "EfazRobloxBootstrap", "Main.py")):
            os.system("title Efaz's Roblox Bootstrap")
            printMainMessage(f"Loading Configuration File..")
            with open(os.path.join(local_app_data, "EfazRobloxBootstrap", "FastFlagConfiguration.json"), "r") as f:
                try:
                    fflag_configuration = json.load(f)
                except Exception as e:
                    loaded_json = False

            if os.path.exists(os.path.join(local_app_data, "EfazRobloxBootstrap", "BootstrapCooldown")):
                if not fflag_configuration.get("EFlagDisableBootstrapCooldown") == True:
                    with open(os.path.join(local_app_data, "EfazRobloxBootstrap", "BootstrapCooldown"), "r") as f:
                        te = f.read()
                        if te.isnumeric():
                            if datetime.datetime.now(tz=datetime.UTC).timestamp() < int(te):
                                printErrorMessage("You're starting the booldown too fast! Please wait 3 seconds!")
                                printDebugMessage(f'If this message is still here after 3 seconds, delete the file "/Applications/EfazRobloxBootstrap.app/Contents/Resources/BootstrapCooldown"')
                                sys.exit(0)
            else:
                def cool():
                    with open(os.path.join(local_app_data, "EfazRobloxBootstrap", "BootstrapCooldown"), "w") as f:
                        f.write(str(int(datetime.datetime.now(tz=datetime.UTC).timestamp()) + 3))
                    time.sleep(fflag_configuration.get("EFlagBootstrapCooldownAmount", 3))
                    if os.path.exists(os.path.join(local_app_data, "EfazRobloxBootstrap", "BootstrapCooldown")):
                        os.remove(os.path.join(local_app_data, "EfazRobloxBootstrap", "BootstrapCooldown"))
                threading.Thread(target=cool).start()

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
                sys.exit(0)

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
                            if os.path.exists(os.path.join(local_app_data, "EfazRobloxBootstrap", "AppNotification")):
                                with open(os.path.join(local_app_data, "EfazRobloxBootstrap", "AppNotification"), "r") as f:
                                    try:
                                        notification = json.load(f)
                                        if type(notification) is list:
                                            class InvalidNotificationException(Exception):
                                                pass
                                            raise InvalidNotificationException("The following data for notification is not valid.")
                                    except Exception as e:
                                        printDebugMessage(str(e))
                                        notification = {"title": "Something went wrong.", "message": "An unexpected error occurred while loading this notification."}
                                os.remove(os.path.join(local_app_data, "EfazRobloxBootstrap", "AppNotification"))
                                if notification.get("title") and notification.get("message"):
                                    displayNotification(notification["title"], notification["message"])
                                    printSuccessMessage("Successfully pinged notification!")
                            seconds += 1
                        except Exception as e:
                            printErrorMessage(f"There was an issue making a notification: {str(e)}")
                        time.sleep(0.05)
                def startBootstrap():
                    global ended
                    try:
                        printMainMessage(f"Starting Bootstrap..")
                        a_file_hash = generateFileHash(os.path.join(local_app_data, "EfazRobloxBootstrap", "Main.py"))
                        b_file_hash = generateFileHash(os.path.join(local_app_data, "EfazRobloxBootstrap", "RobloxFastFlagsInstaller.py"))
                        c_file_hash = generateFileHash(os.path.join(local_app_data, "EfazRobloxBootstrap", "Install.py"))
                        d_file_hash = generateFileHash(os.path.join(local_app_data, "EfazRobloxBootstrap", "Uninstall.py"))
                        e_file_hash = generateFileHash(os.path.join(local_app_data, "EfazRobloxBootstrap", "EfazRobloxBootstrapAPI.py"))
                        f_file_hash = generateFileHash(os.path.join(local_app_data, "EfazRobloxBootstrap", "DiscordPresenceHandler.py"))

                        validated = True
                        unable_to_validate = []
                        if not (a_file_hash == integrated_app_hashes["main"]): 
                            validated = False
                            unable_to_validate.append("Main.py")
                        if not (b_file_hash == integrated_app_hashes["fflag_install"]):
                            validated = False
                            unable_to_validate.append("RobloxFastFlagsInstaller.py")
                        if not (c_file_hash == integrated_app_hashes["install"]):
                            validated = False
                            unable_to_validate.append("Install.py")
                        if not (d_file_hash == integrated_app_hashes["uninstall"]):
                            validated = False
                            unable_to_validate.append("Uninstall.py")
                        if not (e_file_hash == integrated_app_hashes["bootstrap_api"]):
                            validated = False
                            unable_to_validate.append("EfazRobloxBootstrapAPI.py")
                        if not (f_file_hash == integrated_app_hashes["discord_presence"]):
                            validated = False
                            unable_to_validate.append("DiscordPresenceHandler.py")

                        if validated == True or fflag_configuration.get("EFlagDisableSecureHashSecurity") == True:
                            if fflag_configuration.get("EFlagDisableSecureHashSecurity") == True: displayNotification("Security Notice", "Hash Verification is currently disabled. Please check your FFlag configuration and your mod scripts if this wasn't you!")
                            if filtered_args == "":
                                result = subprocess.run([pythonExecutable, os.path.join(local_app_data, "EfazRobloxBootstrap", "Main.py")], shell=True, cwd=os.path.join(local_app_data, "EfazRobloxBootstrap"))
                            else:
                                result = subprocess.run([pythonExecutable, os.path.join(local_app_data, "EfazRobloxBootstrap", "Main.py"), filtered_args], shell=True, cwd=os.path.join(local_app_data, "EfazRobloxBootstrap"))
                            printMainMessage("Ending Bootstrap..")
                            ended = True
                            if result.returncode == 0:
                                printSuccessMessage(f"Bootstrap Run Success: {result.returncode}")
                            else:
                                printErrorMessage(f"Bootstrap Run Failed: {result.returncode}")
                        else:
                            printErrorMessage(f"Unable to validate hashes for files: {', '.join(unable_to_validate)}")
                            displayNotification("Uh oh!", "Your copy of Efaz's Roblox Bootstrap was unable to be validated and must be reinstalled! Please download a new copy from GitHub!")
                        sys.exit(0)
                    except Exception as e:
                        printErrorMessage(f"Bootstrap Run Failed: {str(e)}")
                        sys.exit(0)
                threading.Thread(target=awake).start()
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