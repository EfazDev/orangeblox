import sys
import subprocess
import json
import threading
import os
import zlib
import platform
import time
import shutil
import traceback
import datetime
import textwrap
import logging
import hashlib
import webbrowser
import PyKits

if __name__ == "__main__":
    current_version = {"version": "2.4.0e"}
    main_os = platform.system()
    args = sys.argv
    generated_app_id = os.urandom(3).hex()
    pip_class = PyKits.pip(find=True)
    colors_class = PyKits.Colors()
    app_path = ""
    macos_path = ""
    logs = []

    COLOR_CODES = {
        0: "#ffffff",
        1: "#ff0000",
        2: "#ffff00",
        3: "#ff4b00",
        4: "#00ff00",
    }
    flag_types = {
        "EFlagRobloxStudioFlags": "dict",
        "EFlagRobloxPlayerFlags": "dict",
        "EFlagDisableAutosaveToInstallation": "bool",
        "EFlagOrangeBloxSyncDir": "path",
        "EFlagBootstrapRobloxInstallFolderName": "str",
        "EFlagBootstrapRobloxStudioInstallFolderName": "str",
        "EFlagRebuildClangAppFromSourceDuringUpdates": "bool",
        "EFlagRebuildPyinstallerAppFromSourceDuringUpdates": "bool",
        "EFlagRebuildNuitkaAppFromSourceDuringUpdates": "bool",
        "EFlagInstallEfazDevECCCertificates": "bool",
        "EFlagDisableDeleteOtherOSApps": "bool",
        "EFlagAvailableInstalledDirectories": "dict",
        "EFlagDisableURLSchemeInstall": "bool",
        "EFlagDisableShortcutsInstall": "bool",
        "EFlagRobloxBootstrapUpdatesAuthorizationKey": "EFlagUpdatesAuthorizationKey",
        "EFlagUpdatesAuthorizationKey": "str",
        "EFlagEnableDebugMode": "bool",
        "EFlagEnabledMods": "dict",
        "EFlagMakeMainBootstrapLogFiles": "bool",
        "EFlagCompletedTutorial": "bool",
        "EFlagVerifyRobloxHashAfterInstall": "bool",
        "EFlagEnableDuplicationOfClients": "bool",
        "EFlagAllowActivityTracking": "bool",
        "EFlagDisableFastFlagInstallAccess": "bool",
        "EFlagBootstrapUpdateServer": "str",
        "EFlagRobloxStudioEnabled": "bool",
        "EFlagRemoveRobloxAppDockShortcut": "bool",
        "EFlagFreshCopyRoblox": "bool",
        "EFlagRobloxPlayerArguments": "str",
        "EFlagRobloxStudioArguments": "str",
        "EFlagRobloxUnfriendCheckEnabled": "bool",
        "EFlagRobloxUnfriendCheckUserID": "int",
        "EFlagEnableSkipModificationMode": "bool",
        "EFlagDisableRobloxReinstallNeededChecks": "bool",
        "EFlagEnableMultiAutoReconnect": "bool",
        "EFlagNotifyServerLocation": "bool",
        "EFlagEnableDiscordRPC": "bool",
        "EFlagEnableDiscordRPCJoining": "bool",
        "EFlagShowUserProfilePictureInsteadOfLogo": "bool",
        "EFlagShowUsernameInSmallImage": "bool",
        "EFlagAllowBloxstrapSDK": "bool",
        "EFlagAllowBloxstrapStudioSDK": "bool",
        "EFlagAllowPrivateServerJoining": "bool",
        "EFlagUseDiscordWebhook": "bool",
        "EFlagDiscordWebhookURL": "str",
        "EFlagDiscordWebhookUserId": "str",
        "EFlagDiscordWebhookConnect": "bool",
        "EFlagDiscordWebhookDisconnect": "bool",
        "EFlagDiscordWebhookRobloxAppStart": "bool",
        "EFlagDiscordWebhookRobloxAppClose": "bool",
        "EFlagDiscordWebhookRobloxCrash": "bool",
        "EFlagDiscordWebhookBloxstrapRPC": "bool",
        "EFlagDiscordWebhookGamePublished": "bool",
        "EFlagDiscordWebhookGameSaved": "bool",
        "EFlagDiscordWebhookShowPidInFooter": "bool",
        "EFlagForceReconnectOnStudioLost": "bool",
        "EFlagShowRunningAccountNameInTitle": "bool",
        "EFlagShowRunningGameInTitle": "bool",
        "EFlagShowDisplayNameInTitle": "bool",
        "EFlagSimplifiedEfazRobloxBootstrapPromptUI": "bool",
        "EFlagSkipEfazRobloxBootstrapPromptUI": "bool",
        "EFlagDisableBootstrapChecks": "bool",
        "EFlagDisablePythonUpdateChecks": "bool",
        "EFlagDisablePythonModuleUpdateChecks": "bool",
        "EFlagDisableBootstrapCooldown": "bool",
        "EFlagEnableTkinterDockMenu": "EFlagEnableGUIOptionMenus",
        "EFlagEnableGUIOptionMenus": "bool",
        "EFlagAllowFullDebugMode": "bool",
        "EFlagRobloxClientChannel": "str",
        "EFlagDisableRobloxUpdateChecks": "bool",
        "EFlagRobloxStudioClientChannel": "str",
        "EFlagDisableSecureHashSecurity": "bool",
        "EFlagDisableSettingsAccess": "bool",
        "EFlagRobloxLinkShortcuts": "dict",
        "EFlagRobloxCodesigningName": "str",
        "EFlagEnableMods": "bool",
        "EFlagSelectedModScripts": "dict",
        "EFlagRemoveBuilderFont": "bool",
        "EFlagAvatarEditorBackground": "str",
        "EFlagEnableChangeAvatarEditorBackground": "bool",
        "EFlagSelectedCursor": "str",
        "EFlagEnableChangeCursor": "bool",
        "EFlagSelectedBrandLogo": "str",
        "EFlagEnableChangeBrandIcons": "bool",
        "EFlagSelectedBrandLogo2": "str",
        "EFlagEnableChangeBrandIcons2": "bool",
        "EFlagShowGameNameInStatusBar": "bool",
        "EFlagShowStudioGameNameInStatusBar": "bool",
        "EFlagUseRobloxAppIconAsShortcutIcon": "bool",
        "EFlagReplaceRobloxRuntimeIconWithModIcon": "bool",
        "EFlagSelectedPlayerSounds": "str",
        "EFlagEnableChangePlayerSound": "bool",
        "EFlagDisableModsManagerAccess": "bool",
        "EFlagDisableModScriptsAccess": "bool",
        "EFlagRemoveMenuAndSkipToRoblox": "bool",
        "EFlagDisableLinkShortcutsAccess": "bool",
        "EFlagReturnToMainMenuInstant": "bool",
        "EFlagRemoveCodeSigningMacOS": "bool",
        "EFlagModScriptRequestTooFastMessage": "bool",
        "EFlagModScriptAPIRefreshTime": "float",
        "EFlagRobloxUnfriendCheckCooldown": "int",
        "EFlagSetDiscordRPCStart": "int",
        "EFlagEndStudioPlaceWhenDisconnected": "bool",
        "EFlagDisableAutoOpenOrangeBloxFromStudio": "bool",
        "EFlagSpecifyPythonExecutable": "path",
        "EFlagEnableSecretJackpot": "bool",
        "EFlagBootstrapCooldownAmount": "int",
        "EFlagSelectedBootstrapLanguage": "str",
        "EFlagUseFollowingAppIconPath": "path",
        "EFlagUseConfigurationWebServer": "bool",
        "EFlagConfigurationWebServerURL": "str",
        "EFlagConfigurationAuthorizationKey": "str",
        "EFlagLimitAPIDocsLocalization": "str",
        "EFlagOverwriteUnneededStudioFonts": "bool",
        "EFlagEnableSeeMoreAwaiting": "bool",
        "EFlagEnableLoop429Requests": "bool",
        "EFlagEnableEndingRobloxCrashHandler": "bool",
        "EFlagEnablePythonVirtualEnvironments": "bool",
        "EFlagBuildPythonCacheOnStart": "bool",
        "EFlagEnableSlientPythonInstalls": "bool",
        "EFlagEnableDefaultDiscordRPC": "bool",
        "EFlagLastModVersionMacOSCaching": "str",
        "EFlagRobloxChannelUpdateToken": "str",
        "EFlagRobloxSecurityCookieUsage": "bool",
        "EFlagUseEfazDevAPI": "bool"
    }
    main_config = {}

    def ts(mes):
        mes = str(mes)
        if hasattr(sys.stdout, "translate"): mes = sys.stdout.translate(mes)
        return mes
    def trace():
        _, tb_v, tb_b = sys.exc_info()
        tb_lines = traceback.extract_tb(tb_b)
        lines = []
        lines.append(colors_class.foreground("Traceback (most recent call last):", color="Magenta", bright=True))
        for fn, ln, f, tx in tb_lines:
            lines.append(f'  File {colors_class.foreground(fn, color="Magenta", bright=True)}, line {colors_class.foreground(ln, color="Magenta", bright=True)}, in {colors_class.foreground(f, color="Magenta", bright=True)}')
            if tx: lines.append(f'    {tx}')
        exc_t = type(tb_v).__name__
        exc_m = str(tb_v)
        lines.append(f'{colors_class.foreground(colors_class.bold(f"{exc_t}:"), color="Magenta", bright=True)} {colors_class.foreground(exc_m, color="Magenta", bright=False)}')
        return "\n".join(lines)
    def printMainMessage(mes): colors_class.print(ts(mes), 255); logs.append((ts(mes), 0))
    def printErrorMessage(mes): colors_class.print(ts(mes), 196); logs.append((ts(mes), 1))
    def printSuccessMessage(mes): colors_class.print(ts(mes), 82); logs.append((ts(mes), 4))
    def printWarnMessage(mes): colors_class.print(ts(mes), 202); logs.append((ts(mes), 3))
    def printYellowMessage(mes): colors_class.print(ts(mes), 226); logs.append((ts(mes), 2))
    def printDebugMessage(mes): 
        if main_config.get("EFlagEnableDebugMode"): colors_class.print(f"[DEBUG]: {ts(mes)}", 226); logs.append((ts(mes), 2))
    def setLoggingHandler(handler_name):
        global app_path
        global main_os
        log_path = os.path.join(app_path, "Logs")
        if main_os == "Darwin": log_path = os.path.join(pip_class.getLocalAppData(), "Logs", "OrangeBlox")
        if not os.path.exists(log_path): os.makedirs(log_path,mode=511)
        generated_file_name = f'OrangeBlox_{handler_name}_{datetime.datetime.now().strftime("%B_%d_%Y_%H_%M_%S_%f")}.log' 
        if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding='utf-8')
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        if main_config.get("EFlagMakeMainBootstrapLogFiles") == True:
            file_handler = logging.FileHandler(os.path.join(log_path, generated_file_name), encoding="utf-8")
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        stdout_stream = logging.StreamHandler(sys.stdout)
        stdout_stream.setLevel(logging.INFO)
        stdout_stream.setFormatter(logging.Formatter("%(message)s"))
        if main_config.get("EFlagMakeMainBootstrapLogFiles") == True: logger.addHandler(file_handler)
        logger.addHandler(stdout_stream)
        sys.stdout = PyKits.stdout(logger, logging.INFO, lang=(os.path.join(app_path, "Translations", main_config.get("EFlagSelectedBootstrapLanguage") + ".json")) if main_config.get("EFlagSelectedBootstrapLanguage") and not (main_config.get("EFlagSelectedBootstrapLanguage", "en") == "en") else None)
        sys.stderr = PyKits.stdout(logger, logging.ERROR, lang=(os.path.join(app_path, "Translations", main_config.get("EFlagSelectedBootstrapLanguage") + ".json")) if main_config.get("EFlagSelectedBootstrapLanguage") and not (main_config.get("EFlagSelectedBootstrapLanguage", "en") == "en") else None)
        if main_os == "Windows": colors_class.fix_windows_ansi()
        return True
    def isYes(text): return text.lower() == "y" or text.lower() == "yes" or text.lower() == "true" or text.lower() == "t"
    def isNo(text): return text.lower() == "n" or text.lower() == "no" or text.lower() == "false" or text.lower() == "f"
    def isRequestClose(text): return text.lower() == "exit" or text.lower() == "exit()"

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        if main_os == "Windows": app_path = os.path.dirname(sys.executable); macos_path = os.path.join(os.path.dirname(sys.executable), "MacOS")
        else: app_path = os.path.join(os.sep.join(os.path.dirname(sys.executable).split(os.sep)[:-4]), "Resources"); macos_path = os.path.join(os.sep.join(os.path.dirname(sys.executable).split(os.sep)[:-4]), "MacOS")
    else:
        if main_os == "Windows": app_path = os.path.dirname(sys.argv[0]); macos_path = os.path.dirname(sys.argv[0])
        else: cur_path = os.path.dirname(os.path.abspath(__file__)); app_path = os.path.join(os.sep.join(os.path.dirname(cur_path).split(os.sep)[:-3]), "Resources"); macos_path = os.path.join(os.sep.join(os.path.dirname(cur_path).split(os.sep)[:-3]), "MacOS")
    
    def getIfCertainPlayer():
        if main_os == "Windows":
            if os.path.exists(os.path.join(app_path, "RobloxStudioBetaPlayRobloxRestart.txt")): 
                with open(os.path.join(app_path, "RobloxStudioBetaPlayRobloxRestart.txt"), "r") as f: return f.read(), "studio"
            elif os.path.exists(os.path.join(app_path, "RobloxPlayerBetaPlayRobloxRestart.txt")): 
                with open(os.path.join(app_path, "RobloxPlayerBetaPlayRobloxRestart.txt"), "r") as f: return f.read(), "player"
            else: return None, None
        else: return None, None
    certain_player, certain_type = getIfCertainPlayer()
    if certain_player: app_path = certain_player
    if main_os == "Darwin":
        def loadConfiguration():
            global main_config
            global loaded_json
            if os.path.exists(f'{os.path.expanduser("~")}/Library/Preferences/dev.efaz.robloxbootstrap.plist'): os.remove(f'{os.path.expanduser("~")}/Library/Preferences/dev.efaz.robloxbootstrap.plist')
            macos_preference_expected = f'{os.path.expanduser("~")}/Library/Preferences/dev.efaz.orangeblox.plist'
            if os.path.exists(macos_preference_expected):
                app_configuration = PyKits.plist().readPListFile(macos_preference_expected)
                if app_configuration.get("Configuration"):
                    main_config = app_configuration.get("Configuration")
                    loaded_json = True
                else:
                    main_config = {}
                    loaded_json = True
            else:
                main_config = {}
                loaded_json = True
            remove_items = []
            for i, v in main_config.items():
                if not (flag_types.get(i) is None):
                    if flag_types.get(i) == "str" and type(v) is str: pass
                    elif flag_types.get(i) == "path" and type(v) is str and os.path.exists(v): pass
                    elif flag_types.get(i) == "int" and type(v) is int: pass
                    elif flag_types.get(i) == "float" and type(v) is float: pass
                    elif flag_types.get(i) == "dict" and type(v) is dict: pass
                    elif flag_types.get(i) == "bool" and type(v) is bool: pass
                    elif flag_types.get(i) == "list" and type(v) is list: pass
                    elif flag_types.get(flag_types.get(i)): main_config[flag_types.get(i)] = v; remove_items.append(i)
                    else: remove_items.append(i)
                else: remove_items.append(i)
            for i in remove_items: main_config.pop(i)
            return main_config
        loadConfiguration()
    elif main_os == "Windows":
        if os.path.exists(os.path.join(app_path, "Main.py")):
            with open(os.path.join(app_path, "Configuration.json"), "rb") as f: obfuscated_json = f.read()
            try: obfuscated_json = json.loads(obfuscated_json)
            except Exception as e: obfuscated_json = json.loads(zlib.decompress(obfuscated_json).decode("utf-8"))
            main_config = obfuscated_json
            loaded_json = True
        
    setLoggingHandler("Bootloader")
    printWarnMessage("-----------")
    printWarnMessage("Welcome to OrangeBlox Loader 🍊!")
    printWarnMessage("Made by Efaz from efaz.dev!")
    printWarnMessage(f"v{current_version['version']}")
    printWarnMessage("-----------")
    if main_os == "Windows": printMainMessage(f"System OS: {main_os} ({platform.version()})")
    elif main_os == "Darwin": printMainMessage(f"System OS: {main_os} (macOS {platform.mac_ver()[0]})")
    else:
        printErrorMessage("OrangeBlox is only supported for macOS and Windows.")
        input("> ")
        sys.exit(0)
    if not pip_class.osSupported(windows_build=17763, macos_version=(10,13,0)):
        if main_os == "Windows": printErrorMessage("OrangeBlox is only supported for Windows 10.0.17763 (October 2018) or higher. Please update your operating system in order to continue!")
        elif main_os == "Darwin": printErrorMessage("OrangeBlox is only supported for macOS 10.13 (High Sierra) or higher. Please update your operating system in order to continue!")
        input("> ")
        sys.exit(0)
    printWarnMessage("-----------")

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
            except Exception as e: printErrorMessage(f"Something went wrong pinging Control Center: \n{trace()}")
        elif main_os == "Windows":
            try:
                try: from plyer.platforms.win.notification import instance
                except Exception as e:
                    pip_class.install(["plyer"])
                    instance = pip_class.importModule("plyer.platforms.win.notification").instance
                instance().notify(
                    title=title,
                    message=message,
                    app_name="OrangeBlox",
                    app_icon=os.path.join(app_path, "Images", "AppIcon.ico"),
                    toast=True
                )
            except Exception as e: printErrorMessage(f"Something went wrong pinging Windows Notification Center: \n{trace()}")
    def generateFileHash(file_path):
        try:
            tmp_path = None
            if main_os == "Windows":
                import tempfile
                with open(file_path, "r", encoding="utf-8-sig") as f: sig_content = f.read()
                with tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8", newline="") as tmp: tmp.write(sig_content); tmp_path = tmp.name
            with open(tmp_path if tmp_path else file_path, "rb") as f:
                hasher = hashlib.md5()
                chunk = f.read(8192)
                while chunk: 
                    hasher.update(chunk)
                    chunk = f.read(8192)
            if tmp_path: os.remove(tmp_path)
            return hasher.hexdigest()
        except Exception as e: return None
    
    with open(os.path.join(os.path.dirname(__file__), "Version.json"), "r", encoding="utf-8") as f:
        current_version = json.load(f)
        f.close()

    if main_os == "Darwin":
        filtered_args = ""
        loaded_json = True
        use_shell = False
        user_folder = pip_class.getUserFolder()
        user_folder_name = os.path.basename(pip_class.getUserFolder())
        orangeblox_library = os.path.join(user_folder, "Library", "OrangeBlox")

        if not os.path.exists(orangeblox_library): os.makedirs(orangeblox_library)
        printMainMessage("Finding Python Executable..")
        if main_config.get("EFlagSpecifyPythonExecutable"): pythonExecutable = main_config.get("EFlagSpecifyPythonExecutable")
        else:
            if pip_class.pythonInstalled(computer=True) == False: pip_class.pythonInstall()
            pythonExecutable = pip_class.findPython(path=True)
        pip_class.executable = pythonExecutable
        if not os.path.exists(pythonExecutable) or not pip_class.pythonSupported(3, 11, 0): 
            pip_class.pythonInstall()
            pythonExecutable = pip_class.findPython(path=True)
            pip_class.executable = pythonExecutable
            if not os.path.exists(pythonExecutable) or not pip_class.pythonSupported(3, 11, 0):
                printErrorMessage("Please install Python 3.11 or later in order to use OrangeBlox!")
                input("> ")
                sys.exit(0)
        printMainMessage(f"Generated App Window Fetching ID: {generated_app_id}")
        sour_path = ""
        venv_path = ""
        if main_config.get("EFlagEnablePythonVirtualEnvironments") == True:
            printMainMessage("Checking Virtual Environments..")
            venv_path = os.path.join(orangeblox_library, "VirtualEnvironment")
            venv_class = PyKits.pip(executable=os.path.join(venv_path, "bin", "python3"))
            if not os.path.exists(venv_path) or not (venv_class.getArchitecture() == pip_class.getArchitecture() and venv_class.getCurrentPythonVersion() == pip_class.getCurrentPythonVersion()):
                if os.path.exists(venv_path) and not pip_class.getMajorMinorVersion(venv_class.getCurrentPythonVersion()) == pip_class.getMajorMinorVersion(pip_class.getCurrentPythonVersion()):
                    shutil.rmtree(venv_path, ignore_errors=True)
                generate_venv_process = subprocess.run([pythonExecutable, "-m", "venv", "--upgrade", venv_path], cwd=app_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if generate_venv_process.returncode == 0: printSuccessMessage("Generated Virtual Environment!"); sour_path = os.path.join(venv_path, "bin", "activate")
                else: printErrorMessage(f"Failed to create virtual environment. Response Code: {generate_venv_process.returncode}"); venv_path = None
            else: printSuccessMessage("Found Virtual Environment!"); sour_path = os.path.join(venv_path, "bin", "activate")
        execute_command = f"unset HISTFILE && clear && cd '{app_path}/' {'' if sour_path == '' else f'&& source {sour_path} '}&& {pythonExecutable if venv_path == '' else os.path.join(venv_path, 'bin', 'python3')} Main.py && exit"
        printMainMessage(f"Loading Runner Command: {execute_command}")

        if len(args) > 1:
            filtered_args = args[1]
            if (("roblox-player:" in filtered_args) or ("roblox-studio:" in filtered_args) or ("roblox-studio-auth:" in filtered_args) or ("roblox:" in filtered_args) or ("efaz-bootstrap:" in filtered_args) or ("orangeblox:" in filtered_args) or os.path.isfile(filtered_args)):
                use_shell = True
                printMainMessage(f"Creating URL Exchange file..")
                if os.path.exists(f"{app_path}/"):
                    with open(f"{app_path}/URLSchemeExchange", "w", encoding="utf-8") as f: f.write(filtered_args)
                else:
                    with open("URLSchemeExchange", "w", encoding="utf-8") as f: f.write(filtered_args)

        applescript = f'''
        tell application "Terminal"
            activate
            set existing_profile to false
            repeat with s in settings sets
                if name of s is equal to "OrangeBlox" then
                    set existing_profile to true
                    exit repeat
                end if
            end repeat
            if existing_profile is false then
                open POSIX file "{os.path.join(app_path, "Images", f"OrangeBlox.terminal")}"
            end if
            set py_window to do script "{execute_command}"
            set current settings of py_window to settings set "OrangeBlox"
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
            do shell script "echo " & terminal_id & " > " & quoted form of "{orangeblox_library}/Terminal_{generated_app_id}"
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
                    if name of window_to_close contains "OrangeBlox" then
                        close window_to_close
                    end if
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
            unable_to_validate2 = []

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
                                        class InvalidNotificationException(Exception): pass
                                        raise InvalidNotificationException("The following data for notification is not valid.")
                                except Exception as e:
                                    printDebugMessage(str(e))
                                    notification = {"title": "Something went wrong.", "message": "An unexpected error occurred while loading this notification."}
                            if os.path.exists(f"{app_path}/AppNotification"): os.remove(f"{app_path}/AppNotification")
                            if notification.get("title") and notification.get("message"):
                                displayNotification(notification["title"], notification["message"])
                                printSuccessMessage(f"Successfully pinged app notification! Title: {notification['title']}, Message: {notification['message']}")
                    except Exception as e: printErrorMessage(f"There was an issue making a notification: \n{trace()}")
                    time.sleep(0.05)
            def terminalAwaitLoop():
                global associated_terminal_pid
                printMainMessage("Starting Terminal ID Loop..")
                while ended == False:
                    try:
                        if os.path.exists(f"{orangeblox_library}/Terminal_{generated_app_id}"):
                            with open(f"{orangeblox_library}/Terminal_{generated_app_id}", "r", encoding="utf-8") as f:
                                try:
                                    cont = f.read().replace(" ", "").replace("\n", "")
                                    if cont.isdigit() and not cont == "0":
                                        associated_terminal_pid = int(cont)
                                        activateTerminalWindow()
                                except Exception as e: printDebugMessage(str(e))
                            if os.path.exists(f"{orangeblox_library}/Terminal_{generated_app_id}"): os.remove(f"{orangeblox_library}/Terminal_{generated_app_id}")
                    except Exception as e: printErrorMessage(f"There was an issue getting Terminal ID: \n{trace()}")
                    time.sleep(0.05)
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
                        else: printErrorMessage("Failed to activate Terminal window.")
                        activate_cooldown = False
                except Exception as e: printErrorMessage(f"Error activating Terminal window.")
            def startBootstrap():
                global ended
                global validated
                global unable_to_validate
                global unable_to_validate2
                global associated_terminal_pid
                try:
                    printMainMessage(f"Validating Bootstrap Scripts..")
                    integrated_app_hashes = current_version.get("hashes", {})
                    for i, v in integrated_app_hashes.items():
                        if i == "OrangeBlox.py": continue
                        file_hash = generateFileHash(os.path.join(app_path, i))
                        if not file_hash == v: validated = False; unable_to_validate.append([i, file_hash, v]); unable_to_validate2.append(i)
                    if not (validated == False) or main_config.get("EFlagDisableSecureHashSecurity") == True:
                        validated = True
                        if main_config.get("EFlagBuildPythonCacheOnStart") == True:
                            printMainMessage("Building Python Cache..")
                            build_cache_process = subprocess.run([pythonExecutable, "-m", "compileall", app_path], cwd=app_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                            if build_cache_process.returncode == 0: printSuccessMessage("Successfully built Python cache!")
                            else: printErrorMessage(f"Unable to build python cache. Return code: {build_cache_process.returncode}")
                        printMainMessage(f"Running Bootstrap..")
                        if main_config.get("EFlagDisableSecureHashSecurity") == True: displayNotification(ts("Security Notice"), ts("Hash Verification is currently disabled. Please check your configuration and mod scripts if you didn't disable this!"))
                        result = subprocess.run(args=["osascript", "-e", applescript], capture_output=True)
                        printMainMessage("Ending Bootstrap..")
                        ended = True
                        if result.returncode == 0:
                            printSuccessMessage(f"Bootstrap Run Success: {result.returncode}")
                            sys.exit(0)
                        else:
                            printErrorMessage(f"Bootstrap Run Failed: {result.returncode}")
                            sys.exit(0)
                    else:
                        displayNotification(ts("Uh oh!"), ts("Your copy of OrangeBlox was unable to be validated and might be tampered with!"))
                        printErrorMessage(f"Uh oh! There was an issue trying to validate hashes for the following files: {', '.join(unable_to_validate2)}")
                        for i in unable_to_validate: printErrorMessage(f"{i[0]} | {i[2]} => {i[1]}")
                        printErrorMessage(f"Requested validation failed window from pyobjc.")
                except Exception as e:
                    ended = True
                    printErrorMessage(f"Bootstrap Run Failed: \n{trace()}")
                    sys.exit(0)
            def createObjcAppReplication():
                global associated_terminal_pid
                global unable_to_validate
                global validated
                global ended
                try:
                    printMainMessage(f"Starting GUI App Replication..")
                    while validated == None: time.sleep(0)
                    try:
                        import objc
                        import AppKit
                        import Foundation
                        import random
                        class AppDelegate(Foundation.NSObject):
                            terminal_window = None
                            button = None
                            top_menu = None
                            holding_frame = None
                            app_icon = None
                            icon_view = None
                            label1 = None
                            label2 = None
                            debug_mode_window_enabled = False
                            is_at_bottom = True
                            output_area = None
                            output_scroll_view = None
                            button_click_count = 0
                            last_checked_index = 0
                            requested_kill = False
                            dock_menu = None
                            status_item = None
                            validation_failed_window = None
                            validation_frame = None
                            menu_menu = None
                            terminating = False
                            already_activated = False
                            top_menu_options = {}
                            dock_menu_options = {}
                            shortcut_options = []
                            config_reload_period = False

                            # Create Window App
                            def applicationDidFinishLaunching_(self, notification):
                                try:
                                    printMainMessage("macOS Application finished launching..")
                                    self.master = AppKit.NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
                                        AppKit.NSMakeRect(100.0, 100.0, 780.0, 500.0),
                                        AppKit.NSWindowStyleMaskTitled | AppKit.NSWindowStyleMaskClosable | AppKit.NSWindowStyleMaskResizable,
                                        AppKit.NSBackingStoreBuffered,
                                        False
                                    ).autorelease()
                                    self.master_controller = AppKit.NSWindowController.alloc().initWithWindow_(self.master)
                                    self.master_controller.setShouldCascadeWindows_(False)
                                    self.master_controller.showWindow_(self.master)
                                    self.master.setTitle_("OrangeBlox")
                                    self.master.setOpaque_(False)
                                    self.master.setAlphaValue_(0.0)
                                    self.master.setDelegate_(self)
                                    self.master.setContentMinSize_(AppKit.NSSize(780, 500))
                                    self.master.setReleasedWhenClosed_(False)

                                    content_view = self.master.contentView()
                                    self.holding_frame = AppKit.NSView.alloc().initWithFrame_(content_view.frame())
                                    self.holding_frame.setTranslatesAutoresizingMaskIntoConstraints_(False)
                                    content_view.addSubview_(self.holding_frame)
                                    constraints = [
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.holding_frame, AppKit.NSLayoutAttributeTop,
                                            AppKit.NSLayoutRelationEqual,
                                            content_view, AppKit.NSLayoutAttributeTop,
                                            1, 0
                                        ),
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.holding_frame, AppKit.NSLayoutAttributeBottom,
                                            AppKit.NSLayoutRelationEqual,
                                            content_view, AppKit.NSLayoutAttributeBottom,
                                            1, 0
                                        ),
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.holding_frame, AppKit.NSLayoutAttributeLeading,
                                            AppKit.NSLayoutRelationEqual,
                                            content_view, AppKit.NSLayoutAttributeLeading,
                                            1, 0
                                        ),
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.holding_frame, AppKit.NSLayoutAttributeTrailing,
                                            AppKit.NSLayoutRelationEqual,
                                            content_view, AppKit.NSLayoutAttributeTrailing,
                                            1, 0
                                        ),
                                    ]
                                    content_view.addConstraints_(constraints)

                                    app_icon_url = f"{app_path}/Images/AppIcon64.png"
                                    if main_config.get("EFlagUseFollowingAppIconPath"): app_icon_url = main_config.get("EFlagUseFollowingAppIconPath")
                                    if os.path.exists(app_icon_url): self.app_icon = AppKit.NSImage.alloc().initByReferencingFile_(app_icon_url)
                                    else: self.app_icon = AppKit.NSImage.alloc().initByReferencingFile_(f"{app_path}/Images/AppIcon.icns")
                                    self.icon_view = AppKit.NSImageView.alloc().init()
                                    self.icon_view.setImage_(self.app_icon)
                                    self.icon_view.setImageScaling_(AppKit.NSImageScaleProportionallyUpOrDown)
                                    self.icon_view.setTranslatesAutoresizingMaskIntoConstraints_(False)
                                    self.holding_frame.addSubview_(self.icon_view)

                                    self.label1 = AppKit.NSTextField.alloc().init()
                                    self.label1.setStringValue_(ts("Ooh! Hi there! Welcome to OrangeBlox 🍊!"))
                                    self.label1.setFont_(AppKit.NSFont.systemFontOfSize_(16))
                                    self.label1.setBezeled_(False)
                                    self.label1.setDrawsBackground_(False)
                                    self.label1.setEditable_(False)
                                    self.label1.setSelectable_(False)
                                    self.label1.setAlignment_(AppKit.NSCenterTextAlignment)
                                    self.label1.setTranslatesAutoresizingMaskIntoConstraints_(False)
                                    self.holding_frame.addSubview_(self.label1)

                                    self.label2 = AppKit.NSTextField.alloc().init()
                                    self.label2.setStringValue_(ts("Bootstrap Loader Logs:"))
                                    self.label2.setFont_(AppKit.NSFont.systemFontOfSize_(13))
                                    self.label2.setBezeled_(False)
                                    self.label2.setDrawsBackground_(False)
                                    self.label2.setEditable_(False)
                                    self.label2.setSelectable_(False)
                                    self.label2.setAlignment_(AppKit.NSCenterTextAlignment)
                                    self.label2.setTranslatesAutoresizingMaskIntoConstraints_(False)
                                    self.holding_frame.addSubview_(self.label2)

                                    self.output_scroll_view = AppKit.NSScrollView.alloc().init()
                                    self.output_scroll_view.setHasVerticalScroller_(True)
                                    self.output_scroll_view.setAutohidesScrollers_(True)
                                    self.output_scroll_view.setTranslatesAutoresizingMaskIntoConstraints_(False)
                                    self.output_scroll_view.setVerticalScrollElasticity_(AppKit.NSScrollElasticityNone)
                                    self.output_scroll_view.setHorizontalScrollElasticity_(AppKit.NSScrollElasticityNone)
                                    text_storage = AppKit.NSTextStorage.alloc().init()
                                    layout_manager = AppKit.NSLayoutManager.alloc().init()
                                    text_container = AppKit.NSTextContainer.alloc().initWithContainerSize_((800, float('inf')))
                                    layout_manager.addTextContainer_(text_container)
                                    text_storage.addLayoutManager_(layout_manager)
                                    self.output_area = AppKit.NSTextView.alloc().initWithFrame_textContainer_(((0, 0), (800, 500)), text_container)
                                    if pip_class.osSupported(macos_version=(10, 15, 0)): self.output_area.setFont_(AppKit.NSFont.monospacedSystemFontOfSize_weight_(13, AppKit.NSFontWeightRegular))
                                    else: self.output_area.setFont_(AppKit.NSFont.systemFontOfSize_(13))
                                    self.output_area.setEditable_(False)
                                    self.output_area.setSelectable_(True)
                                    self.output_area.setDrawsBackground_(True)
                                    self.output_area.setBackgroundColor_(AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.12, 0.12, 0.12, 1))
                                    self.output_area.setTextColor_(AppKit.NSColor.whiteColor())
                                    self.output_area.setInsertionPointColor_(AppKit.NSColor.whiteColor())
                                    self.output_area.setTranslatesAutoresizingMaskIntoConstraints_(False)
                                    self.output_scroll_view.setDocumentView_(self.output_area)
                                    self.output_area.setVerticallyResizable_(True)
                                    self.output_area.setHorizontallyResizable_(False)
                                    self.output_area.setAutoresizingMask_(AppKit.NSViewWidthSizable)
                                    text_container = self.output_area.textContainer()
                                    text_container.setWidthTracksTextView_(True)
                                    text_container.setContainerSize_((800, float("inf")))
                                    self.output_area.setMinSize_((0.0, 0.0))
                                    self.output_area.setMaxSize_((float('inf'), float('inf')))
                                    content_height = self.output_area.layoutManager().usedRectForTextContainer_(text_container).size.height
                                    self.output_area.setFrameSize_((800, content_height))
                                    self.output_area.setTextContainerInset_((4, 8))
                                    self.holding_frame.addSubview_(self.output_scroll_view)
                                    AppKit.NSNotificationCenter.defaultCenter().addObserver_selector_name_object_(
                                        self,
                                        "scrollingLogs:",
                                        AppKit.NSViewBoundsDidChangeNotification,
                                        self.output_scroll_view.contentView()
                                    )

                                    self.button = AppKit.NSButton.alloc().init()
                                    self.button.setTitle_(ts("Go to bootstrap terminal window!"))
                                    self.button.setBezelStyle_(AppKit.NSRoundedBezelStyle)
                                    self.button.setTarget_(self)
                                    self.button.setAction_(objc.selector(self.onButtonClick_, signature=b'v@:@'))
                                    self.button.setTranslatesAutoresizingMaskIntoConstraints_(False)
                                    self.holding_frame.addSubview_(self.button)

                                    constraints = [
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.icon_view, AppKit.NSLayoutAttributeCenterX,
                                            AppKit.NSLayoutRelationEqual, self.holding_frame, AppKit.NSLayoutAttributeCenterX, 1, 0),
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.icon_view, AppKit.NSLayoutAttributeTop,
                                            AppKit.NSLayoutRelationEqual, self.holding_frame, AppKit.NSLayoutAttributeTop, 1, 20),
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.icon_view, AppKit.NSLayoutAttributeWidth,
                                            AppKit.NSLayoutRelationEqual, None, 0, 1, 64),
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.icon_view, AppKit.NSLayoutAttributeHeight,
                                            AppKit.NSLayoutRelationEqual, None, 0, 1, 64),
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.label1, AppKit.NSLayoutAttributeTop,
                                            AppKit.NSLayoutRelationEqual, self.icon_view, AppKit.NSLayoutAttributeBottom, 1, 20),
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.label1, AppKit.NSLayoutAttributeCenterX,
                                            AppKit.NSLayoutRelationEqual, self.holding_frame, AppKit.NSLayoutAttributeCenterX, 1, 0),
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.label2, AppKit.NSLayoutAttributeTop,
                                            AppKit.NSLayoutRelationEqual, self.label1, AppKit.NSLayoutAttributeBottom, 1, 15),
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.label2, AppKit.NSLayoutAttributeCenterX,
                                            AppKit.NSLayoutRelationEqual, self.holding_frame, AppKit.NSLayoutAttributeCenterX, 1, 0),
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.output_scroll_view, AppKit.NSLayoutAttributeTop,
                                            AppKit.NSLayoutRelationEqual, self.label2, AppKit.NSLayoutAttributeBottom, 1, 15),
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.output_scroll_view, AppKit.NSLayoutAttributeCenterX,
                                            AppKit.NSLayoutRelationEqual, self.holding_frame, AppKit.NSLayoutAttributeCenterX, 1, 0),
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.output_scroll_view, AppKit.NSLayoutAttributeWidth,
                                            AppKit.NSLayoutRelationEqual, self.holding_frame, AppKit.NSLayoutAttributeWidth, 0.9, 0),
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.output_scroll_view, AppKit.NSLayoutAttributeHeight,
                                            AppKit.NSLayoutRelationEqual, None, 0, 1, 260),
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.button, AppKit.NSLayoutAttributeTop,
                                            AppKit.NSLayoutRelationEqual, self.output_scroll_view, AppKit.NSLayoutAttributeBottom, 1, 15),
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.button, AppKit.NSLayoutAttributeCenterX,
                                            AppKit.NSLayoutRelationEqual, self.holding_frame, AppKit.NSLayoutAttributeCenterX, 1, 0),
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.button, AppKit.NSLayoutAttributeWidth,
                                            AppKit.NSLayoutRelationEqual, None, 0, 1, 260),
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.button, AppKit.NSLayoutAttributeHeight,
                                            AppKit.NSLayoutRelationEqual, None, 0, 1, 30)
                                    ]
                                    self.holding_frame.addConstraints_(constraints)
                                    self.master.makeKeyAndOrderFront_(None)
                                    self.master.makeMainWindow()
                                    self.master.makeKeyWindow()
                                    self.holding_frame.layoutSubtreeIfNeeded()
                                    self.master.display()

                                    def awaitTerminal():
                                        global associated_terminal_pid
                                        while associated_terminal_pid == None: time.sleep(0.05)
                                        printDebugMessage(f"Received Terminal ID from Receiver: {associated_terminal_pid}")
                                        self.terminal_window = associated_terminal_pid
                                        self.activate_terminal_window()
                                    threading.Thread(target=awaitTerminal, daemon=True).start()

                                    self.generate_top_menu()
                                    if not (main_config.get("EFlagEnableGUIOptionMenus") == False): self.generate_dock_menu()

                                    if ended == True:
                                        self.terminating = True
                                        self.unlock_app_lock()
                                        AppKit.NSApp().stop_(None)
                                        AppKit.NSApp().terminate_(None)
                                        sys.exit(0)
                                        return
                                    else:
                                        try:
                                            if ended == False:
                                                threading.Thread(target=self.reset_button_click, daemon=True).start()
                                                threading.Thread(target=self.config_reload_period_func, daemon=True).start()
                                                if validated == False: self.show_validation_failed_menu()
                                                self.master.setDocumentEdited_(True)
                                                self.threadingloop_(None)
                                            else:
                                                self.terminating = True
                                                self.unlock_app_lock()
                                                AppKit.NSApp().stop_(None)
                                                AppKit.NSApp().terminate_(None)
                                                sys.exit(0)
                                        except Exception as e: printErrorMessage(f"Something went wrong with running functions! Error: \n{trace()}")
                                        printMainMessage(f"PyObjc app finished launching! Terminal ID: {self.terminal_window}")
                                except Exception as e: printErrorMessage(f"PyObjc App Failed! Error: \n{trace()}")
                            def applicationShouldTerminate_(self, sender): return self.on_close()
                            
                            # Control Window
                            def windowWillMiniaturize_(self, notification): self.prevent_minimize()
                            def prevent_minimize(self): printDebugMessage("Prevented minimizing main window in order to keep app running smoothly.")
                            def windowDidBecomeMain_(self, notification): 
                                if notification.object() == self.master and self.already_activated == False: self.already_activated = True; self.on_window_activate(None)
                            def windowDidResignMain_(self, notification):
                                if notification.object() == self.master: self.already_activated = False
                            def windowShouldClose_(self, sender):
                                if self.terminating == True: return
                                if sender == self.master: return self.on_close()
                                elif self.validation_frame: return self.on_close()
                                else: return True
                            def windowDidMiniaturize_(self, notification): self.master.deminiaturize_(None); self.prevent_minimize()
                            def threadingloop_(self, obj):
                                global ended
                                try:
                                    def nscolor_from_hex(hex_str):
                                        hex_str = hex_str.lstrip("#")
                                        if len(hex_str) == 3: hex_str = "".join(c * 2 for c in hex_str)
                                        if len(hex_str) != 6: return AppKit.NSColor.whiteColor()
                                        r = int(hex_str[0:2], 16) / 255.0
                                        g = int(hex_str[2:4], 16) / 255.0
                                        b = int(hex_str[4:6], 16) / 255.0
                                        return AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(r, g, b, 1.0)
                                    def update_ui_on_main_thread():
                                        try:
                                            new_logs = logs[self.last_checked_index:]
                                            for log, color_code in new_logs:
                                                lines = textwrap.wrap(log, width=75)
                                                for line in lines:
                                                    color_hex = COLOR_CODES.get(color_code, "#ffffff")
                                                    color_ns = nscolor_from_hex(color_hex)
                                                    attr_str = AppKit.NSAttributedString.alloc().initWithString_attributes_(
                                                        f" {line}\n",
                                                        {AppKit.NSForegroundColorAttributeName: color_ns, AppKit.NSFontAttributeName: self.output_area.font()}
                                                    )
                                                    self.output_area.textStorage().appendAttributedString_(attr_str)
                                            self.last_checked_index = len(logs)
                                            if self.is_at_bottom: self.output_area.scrollRangeToVisible_(AppKit.NSMakeRange(self.output_area.string().length(), 0))
                                            self.updateScrollingLogsHeight()
                                        except Exception as e: printErrorMessage(f"UI update error: \n{trace()}")
                                    update_ui_on_main_thread()
                                    if ended == True:
                                        self.master.setDocumentEdited_(False)
                                        if self.debug_mode_window_enabled == False or self.requested_kill == True:
                                            self.on_close()
                                            printSuccessMessage("Successfully ended PyObjc app!")
                                            update_ui_on_main_thread()
                                            return
                                        else:
                                            printSuccessMessage("Bootstrap window has been closed successfully! You may close this window normally!")
                                            if self.button: self.button.removeFromSuperview(); self.button = None
                                            update_ui_on_main_thread()
                                            return
                                    if self.config_reload_period == True: 
                                        self.generate_top_menu()
                                        if not (main_config.get("EFlagEnableGUIOptionMenus") == False): self.generate_dock_menu()
                                        self.config_reload_period = False
                                    if not ended and not (obj == "oranges"):
                                        def delayed_loop(): time.sleep(0.1); self.pyobjc_performSelectorOnMainThread_withObject_('threadingloop:', obj)
                                        threading.Thread(target=delayed_loop, daemon=True).start()
                                except Exception as e: printErrorMessage(f"There was an error loading loop! Error: \n{trace()}")
                            def scrollingLogs_(self, notification):
                                content_view = self.output_scroll_view.contentView()
                                document_view = self.output_scroll_view.documentView()
                                visible_rect = content_view.bounds()
                                document_rect = document_view.bounds()
                                max_y = document_rect.size.height - visible_rect.size.height
                                current_y = visible_rect.origin.y
                                if max_y <= 0: self.is_at_bottom = True
                                elif abs(current_y - max_y) < 2: self.is_at_bottom = True
                                else: self.is_at_bottom = False
                            def updateScrollingLogsHeight(self):
                                layout_manager = self.output_area.layoutManager()
                                text_container = self.output_area.textContainer()
                                used_rect = layout_manager.usedRectForTextContainer_(text_container)
                                content_height = used_rect.size.height + 20
                                self.output_area.setFrameSize_((800, content_height))
                            def onButtonClick_(self, sender): self.activate_terminal_window()
                            def on_close(self):
                                try:
                                    global ended
                                    if self.terminating == True: return True
                                    if ended == True:
                                        printSuccessMessage("Successfully ended PyObjc app!")
                                        self.terminating = True
                                        self.unlock_app_lock()
                                        AppKit.NSApp().stop_(None)
                                        AppKit.NSApp().terminate_(None)
                                        sys.exit(0)
                                        return True
                                    else:
                                        if self.terminal_window: self.kill_bootstrap_window(); return False
                                        else:
                                            ended = True
                                            printSuccessMessage("Successfully ended PyObjc app!")
                                            self.terminating = True
                                            self.unlock_app_lock()
                                            AppKit.NSApp().stop_(None)
                                            AppKit.NSApp().terminate_(None)
                                            sys.exit(0)
                                            return True
                                except Exception as e:
                                    printErrorMessage(f"Error ending app: \n{trace()}")
                                    return True
                            
                            # macOS Menus
                            def generate_top_menu(self):
                                if not self.top_menu: self.top_menu = AppKit.NSMenu.alloc().init()
                                if not self.menu_menu: self.main_menu = AppKit.NSMenu.alloc().init()
                                self.top_menu.removeAllItems()
                                main_menu_item = AppKit.NSMenuItem.alloc().init()
                                self.top_menu.addItem_(main_menu_item)
                                self.top_menu.setSubmenu_forItem_(self.main_menu, main_menu_item)
                                def add_menu_item(menu, title, action_name, option=""):
                                    item = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(title, objc.selector(getattr(self, action_name), signature=b'v@:@'), option)
                                    item.setTarget_(self)
                                    self.top_menu_options[title] = item
                                    menu.addItem_(item)
                                    return item
                                add_menu_item(self.main_menu, ts("About OrangeBlox"), "showAboutMenu_", "]")
                                self.main_menu.addItem_(AppKit.NSMenuItem.separatorItem())
                                add_menu_item(self.main_menu, ts("New Bootstrap Window"), "newBootstrapWindow_", "n")
                                add_menu_item(self.main_menu, ts("Refresh App Configuration"), "refreshConfig_", "r")
                                if main_config.get("EFlagEnableDebugMode") == True: 
                                    s = add_menu_item(self.main_menu, ts("Open Debug Window"), "debugWindowButton_", "d")
                                    s.setTitle_(ts("Open Debug Window") if self.debug_mode_window_enabled == False else ts("Close Debug Window"))
                                self.main_menu.addItem_(AppKit.NSMenuItem.separatorItem())
                                add_menu_item(self.main_menu, ts("Open Mods Manager"), "openModsManager_", "m")
                                add_menu_item(self.main_menu, ts("Open Settings"), "openSettings_", ",")
                                add_menu_item(self.main_menu, ts("Open Credits"), "openCredits_", "[")
                                quit_item = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(ts("Quit OrangeBlox"), "terminate:", "q")
                                self.main_menu.addItem_(quit_item)

                                file_menu = AppKit.NSMenu.alloc().initWithTitle_("File")
                                file_menu_item = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("File", None, "")
                                self.top_menu.addItem_(file_menu_item)
                                self.top_menu.setSubmenu_forItem_(file_menu, file_menu_item)
                                file_menu.addItem_(AppKit.NSMenuItem.separatorItem())
                                if main_config.get("EFlagEnableDuplicationOfClients") == True: add_menu_item(file_menu, ts("Open Roblox [Multi-Instance]"), "multiRunRoblox_")
                                else: add_menu_item(file_menu, ts("Open Roblox"), "runRoblox_")
                                if main_config.get("EFlagRobloxStudioEnabled") == True: add_menu_item(file_menu, ts("Run Roblox Studio"), "runRobloxStudio_")
                                file_menu.addItem_(AppKit.NSMenuItem.separatorItem())
                                if not (main_config.get("EFlagAllowActivityTracking") == False): 
                                    add_menu_item(file_menu, ts("Connect to Existing Roblox"), "reconnectRoblox_")
                                    if main_config.get("EFlagRobloxStudioEnabled") == True: add_menu_item(file_menu, ts("Connect to Existing Roblox Studio"), "reconnectRobloxStudio_")
                                file_menu.addItem_(AppKit.NSMenuItem.separatorItem())
                                add_menu_item(file_menu, ts("Run Fast Flags Installer"), "runFFlagInstaller_")
                                add_menu_item(file_menu, ts("Clear Temporary Storage"), "clearRobloxLogs_")
                                add_menu_item(file_menu, ts("Roblox Installer Options"), "openRobloxInstallerOptions_")
                                add_menu_item(file_menu, ts("End All Roblox Windows"), "endAllRoblox_")
                                if main_config.get("EFlagRobloxStudioEnabled") == True: add_menu_item(file_menu, ts("End All Roblox Studio Windows"), "endAllRobloxStudio_")

                                edit_menu_item = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Edit", None, "")
                                edit_menu = AppKit.NSMenu.alloc().initWithTitle_("Edit")
                                self.top_menu.addItem_(edit_menu_item)
                                self.top_menu.setSubmenu_forItem_(edit_menu, edit_menu_item)
                                add_menu_item(edit_menu, ts("Undo"), "menu_undo", "z")
                                add_menu_item(edit_menu, ts("Redo"), "menu_redo", "Z")
                                edit_menu.addItem_(AppKit.NSMenuItem.separatorItem())
                                add_menu_item(edit_menu, ts("Cut"), "menu_cut", "x")
                                add_menu_item(edit_menu, ts("Copy"), "menu_copy", "c")
                                add_menu_item(edit_menu, ts("Paste"), "menu_paste", "v")
                                edit_menu.addItem_(AppKit.NSMenuItem.separatorItem())
                                add_menu_item(edit_menu, ts("Select All"), "menu_select_all", "a")
                                edit_menu_item.setSubmenu_(edit_menu)

                                shortcuts_menu = AppKit.NSMenu.alloc().initWithTitle_(ts("Shortcuts"))
                                shortcuts_menu_item = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(ts("Shortcuts"), None, "")
                                self.top_menu.addItem_(shortcuts_menu_item)
                                self.top_menu.setSubmenu_forItem_(shortcuts_menu, shortcuts_menu_item)
                                generated_ui_options = []
                                if type(main_config.get("EFlagRobloxLinkShortcuts")) is dict:
                                    for i, v in main_config.get("EFlagRobloxLinkShortcuts").items():
                                        if v and v.get("name") and v.get("id"): 
                                            approved = False
                                            cookie_added_str = ""
                                            if v.get("cookie_paths"):
                                                for c, k in v.get("cookie_paths").items():
                                                    if os.path.exists(k): approved = True; cookie_added_str = f" [User: @{v.get('cookie_user')}]"
                                            if v.get("url") or approved == True: generated_ui_options.append({"index": 1, "message": f"{v.get('name')} [{i}]{cookie_added_str}", "shortcut_info": v})
                                if len(generated_ui_options) > 0:
                                    for p in generated_ui_options:
                                        item = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(p["message"], objc.selector(self.shortcut_, signature=b'v@:@'), "")
                                        item.setTarget_(self)
                                        self.shortcut_options.append((shortcuts_menu, item))
                                        shortcuts_menu.addItem_(item)
                                    shortcuts_menu.addItem_(AppKit.NSMenuItem.separatorItem())
                                self.shortcut_options.append((shortcuts_menu, add_menu_item(shortcuts_menu, ts("Open Shortcuts Menu"), "shortcutmenu_")))

                                options_menu = AppKit.NSMenu.alloc().initWithTitle_(ts("Options"))
                                options_menu_item = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(ts("Options"), None, "")
                                self.top_menu.addItem_(options_menu_item)
                                self.top_menu.setSubmenu_forItem_(options_menu, options_menu_item)
                                add_menu_item(options_menu, ts("Clear Debug Window Logs"), "clearLogs_")
                                add_menu_item(options_menu, ts("Force Load Debug Window Logs"), "forceLoadLogs_")
                                if os.path.exists(os.path.join(orangeblox_library, f"GUIAppLock")): add_menu_item(options_menu, ts("Unlock App Lock"), "unlockAppLock_")
                                add_menu_item(options_menu, ts("Close App"), "closeApp_")

                                view_menu_item = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("View", None, "")
                                self.top_menu.addItem_(view_menu_item)
                                view_menu = AppKit.NSMenu.alloc().initWithTitle_("View")
                                view_menu_item.setSubmenu_(view_menu)

                                window_menu_item = AppKit.NSMenuItem.alloc().init()
                                self.top_menu.addItem_(window_menu_item)
                                window_menu = AppKit.NSMenu.alloc().initWithTitle_("Window")
                                window_menu_item.setSubmenu_(window_menu)
                                AppKit.NSApp.setWindowsMenu_(window_menu)

                                help_menu = AppKit.NSMenu.alloc().initWithTitle_("Help")
                                help_menu_item = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Help", None, "")
                                self.top_menu.addItem_(help_menu_item)
                                self.top_menu.setSubmenu_forItem_(help_menu, help_menu_item)
                                add_menu_item(help_menu, ts("OrangeBlox Wiki"), "showHelpMenu_")
                                add_menu_item(help_menu, ts("GitHub Issues"), "showGitHubIssuesMenu_")
                                help_menu_item.setSubmenu_(help_menu)

                                try:
                                    if self.top_menu and self.main_menu and help_menu: AppKit.NSApp().setMainMenu_(self.top_menu)
                                except Exception as e: printErrorMessage(f"Menu configuration error: \n{trace()}")
                            def generate_dock_menu(self):
                                generated_ui_options = []
                                generated_menu_items = []
                                if not self.dock_menu: self.dock_menu = AppKit.NSMenu.alloc().init()
                                if not self.status_item:
                                    self.status_item = AppKit.NSStatusBar.systemStatusBar().statusItemWithLength_(AppKit.NSVariableStatusItemLength)
                                    icon = self.app_icon
                                    icon.setSize_((18, 18))
                                    self.status_item.button().setImage_(icon)
                                self.dock_menu.removeAllItems()

                                if type(main_config.get("EFlagRobloxLinkShortcuts")) is dict:
                                    for i, v in main_config.get("EFlagRobloxLinkShortcuts").items():
                                        if v and v.get("name") and v.get("id"): 
                                            approved = False
                                            cookie_added_str = ""
                                            if v.get("cookie_paths"):
                                                for c, k in v.get("cookie_paths").items():
                                                    if os.path.exists(k): approved = True; cookie_added_str = f" [User: @{v.get('cookie_user')}]"
                                            if v.get("url") or approved == True: generated_ui_options.append({"index": 1, "message": f"{v.get('name')} [{i}]{cookie_added_str}", "shortcut_info": v})
                                def add_menu_item(menu, title, action, enabled=True):
                                    menu_item = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(title, action + ":", "")
                                    menu_item.setEnabled_(enabled)
                                    menu_item.setTarget_(self)
                                    self.dock_menu_options[title] = menu_item
                                    menu.addItem_(menu_item)
                                    return menu_item
                                add_menu_item(self.dock_menu, ts("New Bootstrap Window"), "newBootstrapWindow")
                                add_menu_item(self.dock_menu, ts("Refresh App Configuration"), "refreshConfig")
                                if main_config.get("EFlagEnableDebugMode") == True: 
                                    s = add_menu_item(self.dock_menu, ts("Open Debug Window"), "debugWindowButton")
                                    s.setTitle_(ts("Open Debug Window") if self.debug_mode_window_enabled == False else ts("Close Debug Window"))
                                add_menu_item(self.dock_menu, ts("Open Settings"), "openSettings")
                                self.dock_menu.addItem_(AppKit.NSMenuItem.separatorItem())

                                if main_config.get("EFlagEnableDuplicationOfClients") == True: add_menu_item(self.dock_menu, ts("Open Roblox [Multi-Instance]"), "multiRunRoblox")
                                else: add_menu_item(self.dock_menu, ts("Open Roblox"), "runRoblox")
                                if main_config.get("EFlagRobloxStudioEnabled") == True: add_menu_item(self.dock_menu, ts("Run Roblox Studio"), "runRobloxStudio")
                                self.dock_menu.addItem_(AppKit.NSMenuItem.separatorItem())
                                add_menu_item(self.dock_menu, ts("Run Fast Flags Installer"), "runFFlagInstaller")
                                add_menu_item(self.dock_menu, ts("Roblox Installer Options"), "openRobloxInstallerOptions")
                                add_menu_item(self.dock_menu, ts("End All Roblox Windows"), "endAllRoblox")
                                if main_config.get("EFlagRobloxStudioEnabled") == True: add_menu_item(self.dock_menu, ts("End All Roblox Studio Windows"), "endAllRobloxStudio")
                                self.dock_menu.addItem_(AppKit.NSMenuItem.separatorItem())
                                if len(generated_ui_options) > 0:
                                    for p in generated_ui_options:
                                        menu_item = add_menu_item(self.dock_menu, p["message"], "shortcut")
                                        self.shortcut_options.append((self.dock_menu, menu_item))
                                        generated_menu_items.append(menu_item)
                                self.shortcut_options.append((self.dock_menu, add_menu_item(self.dock_menu, ts("Open Shortcuts Menu"), "shortcutmenu")))
                                self.status_item.setMenu_(self.dock_menu)
                                AppKit.NSApp().setDockMenu_(self.dock_menu)
                            
                            # OrangeBlox Management Functions
                            def new_bootstrap(self, action="", action_name=""):
                                if not (action == "") and type(action) is str:
                                    url_scheme_path = f"{app_path}/URLSchemeExchange"
                                    with open(url_scheme_path, "w", encoding="utf-8") as f: f.write(f"orangeblox://{action}?quick-action=true")
                                subprocess.Popen(["/usr/bin/open", "-n", "-a", os.path.join(macos_path, "OrangeBlox.app", "Contents", "MacOS", "OrangeBlox")], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                if not (action_name == "") and type(action_name) is str: printMainMessage(f"Launched Bootstrap with action: {action_name}")
                                else: printMainMessage(f"Launched Bootstrap in new window!")
                            def new_bootstrap_play_roblox(self): self.new_bootstrap("continue", ts("Play Roblox"))
                            def new_bootstrap_play_roblox_studio(self): self.new_bootstrap("run-studio", ts("Run Roblox Studio"))
                            def new_bootstrap_play_multi_roblox(self): self.new_bootstrap("new", ts("Multi-Play Roblox"))
                            def new_bootstrap_play_reconnect(self): self.new_bootstrap("reconnect", ts("Connect to Existing Roblox Window"))
                            def new_bootstrap_play_reconnect_studio(self): self.new_bootstrap("reconnect-studio", ts("Connect to Existing Roblox Studio Window"))
                            def new_bootstrap_clear_roblox_logs(self): self.new_bootstrap("clear-logs", ts("Clear Temporary Storage"))
                            def new_bootstrap_roblox_installer(self): self.new_bootstrap("roblox-installer-options", ts("Open Roblox Installer Options"))
                            def new_bootstrap_end_roblox(self): self.new_bootstrap("end-roblox", ts("End Roblox"))
                            def new_bootstrap_end_roblox_studio(self): self.new_bootstrap("end-roblox-studio", ts("End Roblox Studio"))
                            def new_bootstrap_run_fflag_installer(self): self.new_bootstrap("fflag-install", ts("Run Fast Flag Installer"))
                            def new_bootstrap_open_settings(self): self.new_bootstrap("settings", ts("Open Settings"))
                            def new_bootstrap_open_mods_manager(self): self.new_bootstrap("mods", ts("Open Mods Manager"))
                            def new_bootstrap_open_credits(self): self.new_bootstrap("credits", ts("Open Credits"))
                            def new_bootstrap_open_shortcuts(self): self.new_bootstrap("shortcuts/", ts("Open Shortcuts Menu"))
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
                                        if result.returncode == 0 and event == "": printErrorMessage("Please close the console window in order to close this window!!")
                                except Exception as e: printErrorMessage(f"Error while trying to request kill of Terminal window.")
                            def startBootstrapWithoutValidation_(self, sender):
                                if not (self.validation_frame == None):
                                    self.validation_frame.removeFromSuperview()
                                    self.validation_frame = None
                                if not (self.validation_failed_window == None):
                                    self.validation_failed_window.close()
                                    self.validation_failed_window = None
                                main_config["EFlagDisableSecureHashSecurity"] = True
                                def sta():
                                    global associated_terminal_pid
                                    global ended
                                    ended = False
                                    threading.Thread(target=startBootstrap, daemon=False).start()
                                threading.Thread(target=sta, daemon=True).start()
                            def activate_terminal_window(self, event=""): activateTerminalWindow(event)
                            def show_help_menu(self): webbrowser.open("https://github.com/EfazDev/orangeblox/wiki")
                            def show_github_issues_menu(self): webbrowser.open("https://github.com/EfazDev/orangeblox/issues")

                            # Top Menu Options
                            def newBootstrapWindow_(self, sender): self.new_bootstrap()
                            def showAboutMenu_(self, sender): self.show_about_menu()
                            def newBootstrap_(self, sender): self.new_bootstrap()
                            def openModsManager_(self, sender): self.new_bootstrap_open_mods_manager()
                            def openSettings_(self, sender): self.new_bootstrap_open_settings()
                            def openCredits_(self, sender): self.new_bootstrap_open_credits()
                            def runRoblox_(self, sender): self.new_bootstrap_play_roblox()
                            def multiRunRoblox_(self, sender): self.new_bootstrap_play_multi_roblox()
                            def runRobloxStudio_(self, sender): self.new_bootstrap_play_roblox_studio()
                            def openRobloxInstallerOptions_(self, sender): self.new_bootstrap_roblox_installer()
                            def endAllRoblox_(self, sender): self.new_bootstrap_end_roblox()
                            def endAllRobloxStudio_(self, sender): self.new_bootstrap_end_roblox_studio()
                            def runFFlagInstaller_(self, sender): self.new_bootstrap_run_fflag_installer()
                            def reconnectRoblox_(self, sender): self.new_bootstrap_play_reconnect()
                            def reconnectRobloxStudio_(self, sender): self.new_bootstrap_play_reconnect_studio()
                            def clearRobloxLogs_(self, sender): self.new_bootstrap_clear_roblox_logs()
                            def clearLogs_(self, sender): self.clear_logs()
                            def forceLoadLogs_(self, sender): self.force_load_logs()
                            def unlockAppLock_(self, sender): self.unlock_app_lock()
                            def closeApp_(self, sender): self.on_close()
                            def showHelpMenu_(self, sender): self.show_help_menu()
                            def showGitHubIssuesMenu_(self, sender): self.show_github_issues_menu()
                            def enterDebugWindowMode_(self, sender): self.instant_debug_window()
                            def shortcutmenu_(self, sender): self.new_bootstrap_open_shortcuts()
                            def menu_copy(self, sender): self.output_area.copy_(sender)
                            def menu_cut(self, sender): pass
                            def menu_paste(self, sender): pass
                            def menu_select_all(self, sender): self.output_area.selectAll_(sender)
                            def menu_undo(self, sender): self.output_area.undoManager().undo()
                            def menu_redo(self, sender): self.output_area.undoManager().redo()
                            def refreshConfig_(self, sender):
                                loadConfiguration()
                                self.config_reload_period = True
                            def debugWindowButton_(self, sender):
                                if self.debug_mode_window_enabled == False: self.instant_debug_window()
                                else: self.disable_debug_mode_window()
                                if self.top_menu_options.get(ts("Open Debug Window")): self.top_menu_options[ts("Open Debug Window")].setTitle_(ts("Open Debug Window") if self.debug_mode_window_enabled == False else ts("Close Debug Window"))
                                if self.dock_menu_options.get(ts("Open Debug Window")): self.dock_menu_options[ts("Open Debug Window")].setTitle_(ts("Open Debug Window") if self.debug_mode_window_enabled == False else ts("Close Debug Window"))
                            def shortcut_(self, sender):
                                menu_title = sender.title()
                                generated_ui_options = []
                                if type(main_config.get("EFlagRobloxLinkShortcuts")) is dict:
                                    for i, v in main_config.get("EFlagRobloxLinkShortcuts").items():
                                        if v and v.get("name") and v.get("id"): 
                                            approved = False
                                            cookie_added_str = ""
                                            if v.get("cookie_paths"):
                                                for c, k in v.get("cookie_paths").items():
                                                    if os.path.exists(k): approved = True; cookie_added_str = f" [User: @{v.get('cookie_user')}]"
                                            if v.get("url") or approved == True: generated_ui_options.append({"index": 1, "message": f"{v.get('name')} [{i}]{cookie_added_str}", "shortcut_info": v})
                                for p in generated_ui_options:
                                    if p["message"] == menu_title:
                                        self.new_bootstrap(f"shortcuts/{p['shortcut_info'].get('id')}", f"Open Shortcut ({p['message']})")
                                        break
                            
                            # Window App Management
                            def clear_logs(self):
                                global logs
                                logs = []
                                self.output_area.setEditable_(True)
                                self.output_area.setString_("")
                                self.output_area.setEditable_(False)
                            def force_load_logs(self): self.threadingloop_("oranges")
                            def validateMenuItem_(self, menuItem): return True
                            def unlock_app_lock(self):
                                if os.path.exists(os.path.join(orangeblox_library, f"GUIAppLock")): os.remove(os.path.join(orangeblox_library, f"GUIAppLock"))
                            def instant_debug_window(self): self.button_click_count = 9; self.on_window_activate("oranges")
                            def show_about_menu(self):
                                try:
                                    width, height = 350, 200
                                    screen_frame = AppKit.NSScreen.mainScreen().frame()
                                    origin_x = (screen_frame.size.width - width) / 2
                                    origin_y = (screen_frame.size.height - height) / 2
                                    about_rect = AppKit.NSMakeRect(origin_x, origin_y, width, height)

                                    about_window = AppKit.NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
                                        about_rect, 
                                        AppKit.NSTitledWindowMask | AppKit.NSClosableWindowMask | AppKit.NSMiniaturizableWindowMask, 
                                        AppKit.NSBackingStoreBuffered, 
                                        False
                                    ).autorelease()
                                    about_controller = AppKit.NSWindowController.alloc().initWithWindow_(about_window)
                                    about_controller.setShouldCascadeWindows_(False)
                                    about_controller.showWindow_(about_window)
                                    about_window.setDelegate_(self)
                                    about_window.setTitle_(ts("About OrangeBlox"))
                                    about_window.setReleasedWhenClosed_(False)
                                    about_window.setLevel_(AppKit.NSModalPanelWindowLevel)
                                    about_window.center()
                                    
                                    content_view = about_window.contentView()
                                    about_frame = AppKit.NSView.alloc().initWithFrame_(AppKit.NSMakeRect(0, 0, width, height))
                                    content_view.addSubview_(about_frame)
                                    
                                    icon_nsimage = self.app_icon
                                    icon_view = AppKit.NSImageView.alloc().initWithFrame_(AppKit.NSMakeRect(140, 100, 70, 70))
                                    icon_view.setImage_(icon_nsimage)
                                    icon_view.setImageScaling_(AppKit.NSImageScaleProportionallyUpOrDown)
                                    about_frame.addSubview_(icon_view)
                                    
                                    label1 = AppKit.NSTextField.alloc().initWithFrame_(AppKit.NSMakeRect(100, 70, 150, 24))
                                    label1.setStringValue_("OrangeBlox")
                                    label1.setFont_(AppKit.NSFont.boldSystemFontOfSize_(16))
                                    label1.setBezeled_(False)
                                    label1.setDrawsBackground_(False)
                                    label1.setEditable_(False)
                                    label1.setSelectable_(False)
                                    label1.setAlignment_(AppKit.NSCenterTextAlignment)
                                    about_frame.addSubview_(label1)
                                    
                                    version_text = ts(f"Bootstrap Version {current_version.get('version')}\nMade by @EfazDev")
                                    label2 = AppKit.NSTextField.alloc().initWithFrame_(AppKit.NSMakeRect(50, 30, 250, 40))
                                    label2.setStringValue_(version_text)
                                    label2.setFont_(AppKit.NSFont.systemFontOfSize_(12))
                                    label2.setBezeled_(False)
                                    label2.setDrawsBackground_(False)
                                    label2.setEditable_(False)
                                    label2.setSelectable_(False)
                                    label2.setAlignment_(AppKit.NSCenterTextAlignment)
                                    label2.setLineBreakMode_(AppKit.NSLineBreakByWordWrapping)
                                    label2.setMaximumNumberOfLines_(2)
                                    about_frame.addSubview_(label2)
                                    
                                    about_window.orderFrontRegardless()
                                    self.about_window = about_window
                                except Exception as e:
                                    printErrorMessage(f"Unable to show about menu: \n{trace()}")
                            def show_validation_failed_menu(self):
                                try:
                                    width, height = 500, 350
                                    screen_frame = AppKit.NSScreen.mainScreen().frame()
                                    origin_x = (screen_frame.size.width - width) / 2
                                    origin_y = (screen_frame.size.height - height) / 2
                                    validation_rect = AppKit.NSMakeRect(origin_x, origin_y, width, height)

                                    self.validation_failed_window = AppKit.NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
                                        validation_rect, 
                                        AppKit.NSTitledWindowMask | AppKit.NSClosableWindowMask | AppKit.NSMiniaturizableWindowMask, 
                                        AppKit.NSBackingStoreBuffered, 
                                        False
                                    )
                                    self.validation_failed_controller = AppKit.NSWindowController.alloc().initWithWindow_(self.validation_failed_window)
                                    self.validation_failed_controller.setShouldCascadeWindows_(False)
                                    self.validation_failed_controller.showWindow_(self.validation_failed_window)
                                    self.validation_failed_window.setDelegate_(self)
                                    self.validation_failed_window.setTitle_(ts("Bootstrap Verification Failed"))
                                    self.validation_failed_window.setReleasedWhenClosed_(False)
                                    self.validation_failed_window.setLevel_(AppKit.NSModalPanelWindowLevel)
                                    self.validation_failed_window.center()
                                    
                                    content_view = self.validation_failed_window.contentView()
                                    self.validation_frame = AppKit.NSView.alloc().initWithFrame_(AppKit.NSMakeRect(0, 0, width, height))
                                    content_view.addSubview_(self.validation_frame)
                                    
                                    icon_nsimage = self.app_icon
                                    icon_view = AppKit.NSImageView.alloc().initWithFrame_(AppKit.NSMakeRect(220, 255, 70, 70))
                                    icon_view.setImage_(icon_nsimage)
                                    icon_view.setImageScaling_(AppKit.NSImageScaleProportionallyUpOrDown)
                                    self.validation_frame.addSubview_(icon_view)
                                    
                                    label1 = AppKit.NSTextField.alloc().initWithFrame_(AppKit.NSMakeRect(175, 205, 150, 30))
                                    label1.setStringValue_("OrangeBlox")
                                    label1.setFont_(AppKit.NSFont.boldSystemFontOfSize_(20))
                                    label1.setBezeled_(False)
                                    label1.setDrawsBackground_(False)
                                    label1.setEditable_(False)
                                    label1.setSelectable_(False)
                                    label1.setAlignment_(AppKit.NSCenterTextAlignment)
                                    self.validation_frame.addSubview_(label1)
                                    
                                    label2 = AppKit.NSTextField.alloc().initWithFrame_(AppKit.NSMakeRect(75, 105, 350, 90))
                                    label2.setStringValue_(ts("Uh oh! There was an issue trying to validate hashes for the following files:"))
                                    label2.setFont_(AppKit.NSFont.systemFontOfSize_(15))
                                    label2.setBezeled_(False)
                                    label2.setDrawsBackground_(False)
                                    label2.setEditable_(False)
                                    label2.setSelectable_(False)
                                    label2.setAlignment_(AppKit.NSCenterTextAlignment)
                                    self.validation_frame.addSubview_(label2)
                                    
                                    file_list = ", ".join(unable_to_validate2)
                                    label3 = AppKit.NSTextField.alloc().initWithFrame_(AppKit.NSMakeRect(75, 70, 350, 60))
                                    label3.setStringValue_(file_list)
                                    label3.setFont_(AppKit.NSFont.systemFontOfSize_(15))
                                    label3.setBezeled_(False)
                                    label3.setDrawsBackground_(False)
                                    label3.setEditable_(False)
                                    label3.setSelectable_(False)
                                    label3.setAlignment_(AppKit.NSCenterTextAlignment)
                                    self.validation_frame.addSubview_(label3)
                                    
                                    button = AppKit.NSButton.alloc().initWithFrame_(AppKit.NSMakeRect(150, 45, 200, 40))
                                    button.setTitle_(ts("Continue without validation"))
                                    button.setTarget_(self)
                                    button.setAction_(objc.selector(self.startBootstrapWithoutValidation_, signature=b'v@:@'))
                                    self.validation_frame.addSubview_(button)

                                    constraints = [
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            icon_view, AppKit.NSLayoutAttributeCenterX,
                                            AppKit.NSLayoutRelationEqual, self.validation_frame, AppKit.NSLayoutAttributeCenterX, 1, 0),
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            icon_view, AppKit.NSLayoutAttributeTop,
                                            AppKit.NSLayoutRelationEqual, self.validation_frame, AppKit.NSLayoutAttributeTop, 1, 20),
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            icon_view, AppKit.NSLayoutAttributeWidth,
                                            AppKit.NSLayoutRelationEqual, None, 0, 1, 64),
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            icon_view, AppKit.NSLayoutAttributeHeight,
                                            AppKit.NSLayoutRelationEqual, None, 0, 1, 64),
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            label1, AppKit.NSLayoutAttributeTop,
                                            AppKit.NSLayoutRelationEqual, icon_view, AppKit.NSLayoutAttributeBottom, 1, 20),
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            label1, AppKit.NSLayoutAttributeCenterX,
                                            AppKit.NSLayoutRelationEqual, self.validation_frame, AppKit.NSLayoutAttributeCenterX, 1, 0),
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            label2, AppKit.NSLayoutAttributeTop,
                                            AppKit.NSLayoutRelationEqual, label1, AppKit.NSLayoutAttributeBottom, 1, 15),
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            label2, AppKit.NSLayoutAttributeCenterX,
                                            AppKit.NSLayoutRelationEqual, self.validation_frame, AppKit.NSLayoutAttributeCenterX, 1, 0),
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            label3, AppKit.NSLayoutAttributeTop,
                                            AppKit.NSLayoutRelationEqual, label2, AppKit.NSLayoutAttributeBottom, 1, 15),
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            label3, AppKit.NSLayoutAttributeCenterX,
                                            AppKit.NSLayoutRelationEqual, self.validation_frame, AppKit.NSLayoutAttributeCenterX, 1, 0),
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            button, AppKit.NSLayoutAttributeTop,
                                            AppKit.NSLayoutRelationEqual, label3, AppKit.NSLayoutAttributeBottom, 1, 15),
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            button, AppKit.NSLayoutAttributeCenterX,
                                            AppKit.NSLayoutRelationEqual, self.validation_frame, AppKit.NSLayoutAttributeCenterX, 1, 0),
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            button, AppKit.NSLayoutAttributeWidth,
                                            AppKit.NSLayoutRelationEqual, None, 0, 1, 260),
                                        AppKit.NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            button, AppKit.NSLayoutAttributeHeight,
                                            AppKit.NSLayoutRelationEqual, None, 0, 1, 30)
                                    ]
                                    self.validation_failed_window.orderFrontRegardless()
                                    self.validation_frame.addConstraints_(constraints)
                                except Exception as e: printErrorMessage(f"Unable to show validation menu: \n{trace()}")
                            def on_window_activate(self, event):
                                try:
                                    self.button_click_count += 1
                                    self.requested_kill = False
                                    if not (event == "oranges") and ended == False: printMainMessage(f"Window was triggered! Current count: {self.button_click_count}")
                                    if self.button_click_count > 9:
                                        self.master.setTitle_("OrangeBlox")
                                        self.master.setContentSize_((800, 500))
                                        self.master.setOpaque_(True)
                                        self.master.setAlphaValue_(1.0)
                                        self.master.makeKeyAndOrderFront_(None)

                                        self.holding_frame.setHidden_(False)
                                        content_view = self.master.contentView()
                                        holding_frame_size = self.holding_frame.frame().size
                                        content_size = content_view.frame().size
                                        new_origin_x = (content_size.width - holding_frame_size.width) / 2
                                        new_origin_y = (content_size.height - holding_frame_size.height) / 2
                                        self.holding_frame.setFrameOrigin_((new_origin_x, new_origin_y))
                                        self.master.displayIfNeeded()
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
                                        if self.top_menu_options.get(ts("Open Debug Window")): self.top_menu_options[ts("Open Debug Window")].setTitle_(ts("Open Debug Window") if self.debug_mode_window_enabled == False else ts("Close Debug Window"))
                                        if self.dock_menu_options.get(ts("Open Debug Window")): self.dock_menu_options[ts("Open Debug Window")].setTitle_(ts("Open Debug Window") if self.debug_mode_window_enabled == False else ts("Close Debug Window"))
                                    elif ended == False: self.activate_terminal_window()
                                except Exception as e:  printErrorMessage(f"Unable to activate window: \n{trace()}")
                            def disable_debug_mode_window(self):
                                if self.debug_mode_window_enabled == True:
                                    self.debug_mode_window_enabled = False
                                    self.button_click_count = 0
                                    self.master.setTitle_("OrangeBlox")
                                    self.master.setOpaque_(False)
                                    self.master.setAlphaValue_(0.0)
                                    self.master.orderOut_(None)
                            def reset_button_click(self):
                                if self.debug_mode_window_enabled == False: self.button_click_count = 0
                                time.sleep(10)
                                self.reset_button_click()
                            def config_reload_period_func(self):
                                time.sleep(20)
                                self.refreshConfig_(None)
                                self.config_reload_period_func()
                        try:
                            app = AppKit.NSApplication.sharedApplication()
                            delegate = AppDelegate.alloc().init()
                            app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyRegular)
                            app.activateIgnoringOtherApps_(True)
                            app.setDelegate_(delegate)
                            setattr(sys, "_app_delegate", delegate)
                            app.run()
                        except Exception as e: printErrorMessage(f"PyObjc App Failed! Error: \n{trace()}")
                    except Exception as e: printErrorMessage(f"PyObjc App Failed! Error: \n{trace()}")
                except Exception as e: printErrorMessage(str(e))
            threading.Thread(target=notificationLoop, daemon=False).start()
            threading.Thread(target=terminalAwaitLoop, daemon=True).start()
            threading.Thread(target=startBootstrap, daemon=False).start()
            app_count = pip_class.getAmountOfProcesses(os.path.realpath(os.path.join(app_path, "..", "MacOS", "OrangeBlox")))
            if app_count < 1: 
                with open(os.path.join(orangeblox_library, f"GUIAppLock"), "w", encoding="utf-8") as f: f.write(str(datetime.datetime.now(datetime.timezone.utc).timestamp()))
                createObjcAppReplication()
                try: os.remove(os.path.join(orangeblox_library, f"GUIAppLock"))
                except Exception: printMainMessage("Unable to remove GUI app holder")
            else:
                while ended == False and os.path.exists(os.path.join(orangeblox_library, f"GUIAppLock")): time.sleep(0.5)
                if ended == False: 
                    with open(os.path.join(orangeblox_library, f"GUIAppLock"), "w", encoding="utf-8") as f: f.write(str(datetime.datetime.now(datetime.timezone.utc).timestamp()))
                    createObjcAppReplication()
                    try: os.remove(os.path.join(orangeblox_library, f"GUIAppLock"))
                    except Exception: printMainMessage("Unable to remove GUI app holder")
        except Exception as e:
            printErrorMessage(f"Bootstrap Run Failed: \n{trace()}")
            sys.exit(0)
    elif main_os == "Windows":
        filtered_args = ""
        loaded_json = True
        local_app_data = pip_class.getLocalAppData()
        colors_class.set_console_title("OrangeBlox 🍊")
        if os.path.exists(os.path.join(app_path, "Main.py")):
            if os.path.exists(os.path.join(app_path, "BootstrapCooldown")):
                if not main_config.get("EFlagDisableBootstrapCooldown") == True:
                    with open(os.path.join(app_path, "BootstrapCooldown"), "r", encoding="utf-8") as f:
                        te = f.read()
                        if te.isdigit():
                            if datetime.datetime.now(tz=datetime.UTC).timestamp() < int(te):
                                printErrorMessage("You're starting the booldown too fast! Please wait 1 seconds!")
                                printDebugMessage(f'If this message is still here after 1 seconds, delete the file "{app_path}/Resources/BootstrapCooldown"')
                                sys.exit(0)
            else:
                def cool():
                    with open(os.path.join(app_path, "BootstrapCooldown"), "w", encoding="utf-8") as f: f.write(str(int(datetime.datetime.now(tz=datetime.UTC).timestamp()) + 1))
                    time.sleep(main_config.get("EFlagBootstrapCooldownAmount", 1))
                    if os.path.exists(os.path.join(app_path, "BootstrapCooldown")): os.remove(os.path.join(app_path, "BootstrapCooldown"))
                threading.Thread(target=cool, daemon=True).start()

            if len(args) > 1:
                if certain_player: 
                    filtered_args = f"obx-launch-{certain_type} " + " ".join(args)
                    if os.path.exists(app_path):
                        with open(os.path.join(app_path, "URLSchemeExchange"), "w", encoding="utf-8") as f: f.write(filtered_args)
                    else:
                        with open("URLSchemeExchange", "w", encoding="utf-8") as f: f.write(filtered_args)
                else:
                    filtered_args = args[1]
                    if (("roblox-player:" in filtered_args) or ("roblox-studio:" in filtered_args) or ("roblox-studio-auth:" in filtered_args) or ("roblox:" in filtered_args) or ("efaz-bootstrap:" in filtered_args) or ("orangeblox:" in filtered_args) or os.path.isfile(filtered_args)):
                        printMainMessage(f"Creating URL Exchange file..")
                        if os.path.exists(app_path):
                            with open(os.path.join(app_path, "URLSchemeExchange"), "w", encoding="utf-8") as f: f.write(filtered_args)
                        else:
                            with open("URLSchemeExchange", "w", encoding="utf-8") as f: f.write(filtered_args)
            elif certain_player:
                filtered_args = f"obx-launch-{certain_type}"
                if os.path.exists(app_path):
                    with open(os.path.join(app_path, "URLSchemeExchange"), "w", encoding="utf-8") as f: f.write(filtered_args)
                else:
                    with open("URLSchemeExchange", "w", encoding="utf-8") as f: f.write(filtered_args)

            if pip_class.getIfRunningWindowsAdmin():
                printErrorMessage("Please run OrangeBlox under user permissions instead of running administrator!")
                input("> ")
                sys.exit(0)
            printMainMessage("Finding Python Executable..")
            if main_config.get("EFlagSpecifyPythonExecutable"): pythonExecutable = main_config.get("EFlagSpecifyPythonExecutable")
            else:
                if pip_class.pythonInstalled(computer=True) == False: pip_class.pythonInstall()
                pythonExecutable = pip_class.findPython(path=True)
            pip_class.executable = pythonExecutable
            if not os.path.exists(pythonExecutable) or not pip_class.pythonSupported(3, 11, 0): 
                pip_class.pythonInstall()
                pythonExecutable = pip_class.findPython(path=True)
                pip_class.executable = pythonExecutable
                if not os.path.exists(pythonExecutable) or not pip_class.pythonSupported(3, 11, 0):
                    printErrorMessage("Please install Python 3.11 or later in order to use OrangeBlox!")
                    input("> ")
                    sys.exit(0)

            if main_config.get("EFlagEnablePythonVirtualEnvironments") == True:
                printMainMessage("Checking Virtual Environments..")
                user_folder_name = os.path.basename(PyKits.pip().getUserFolder())
                venv_path = os.path.join(app_path, "VirtualEnvironments")
                if not os.path.exists(venv_path): os.makedirs(venv_path)
                venv_path = os.path.join(venv_path, user_folder_name)
                venv_class = PyKits.pip(executable=os.path.join(venv_path, "Scripts", "python.exe"))
                if not os.path.exists(venv_path) or not (venv_class.getArchitecture() == pip_class.getArchitecture() and venv_class.getCurrentPythonVersion() == pip_class.getCurrentPythonVersion()):
                    if os.path.exists(venv_path) and not pip_class.getMajorMinorVersion(venv_class.getCurrentPythonVersion()) == pip_class.getMajorMinorVersion(pip_class.getCurrentPythonVersion()):
                        shutil.rmtree(venv_path, ignore_errors=True)
                    generate_venv_process = subprocess.run([pythonExecutable, "-m", "venv", "--upgrade", f"VirtualEnvironments/{user_folder_name}"], cwd=app_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    if generate_venv_process.returncode == 0: 
                        printSuccessMessage("Generated Virtual Environment!"); pythonExecutable = os.path.join(venv_path, "Scripts", "python.exe")
                    else: printErrorMessage(f"Failed to create virtual environment. Response Code: {generate_venv_process.returncode}")
                else: printSuccessMessage("Found Virtual Environment!"); pythonExecutable = os.path.join(venv_path, "Scripts", "python.exe")
            printMainMessage(f"Detected Python Executable: {pythonExecutable}")

            try:
                ended = False
                def awake():
                    global ended
                    seconds = 0
                    while True:
                        try:
                            if ended == True: break
                            if os.path.exists(os.path.join(app_path, "AppNotification")):
                                with open(os.path.join(app_path, "AppNotification"), "r", encoding="utf-8") as f:
                                    try:
                                        notification = json.load(f)
                                        if type(notification) is list:
                                            class InvalidNotificationException(Exception): pass
                                            raise InvalidNotificationException("The following data for notification is not valid.")
                                    except Exception as e: notification = {"title": "Something went wrong.", "message": "An unexpected error occurred while loading this notification."}
                                if os.path.exists(os.path.join(app_path, "AppNotification")): os.remove(os.path.join(app_path, "AppNotification"))
                                if notification.get("title") and notification.get("message"): displayNotification(notification["title"], notification["message"])
                            seconds += 1
                        except Exception as e: pass
                        time.sleep(0.05)
                def startBootstrap():
                    global ended
                    try:
                        printMainMessage(f"Validating Bootstrap Scripts..")
                        unable_to_validate = []
                        unable_to_validate2 = []
                        validated = None
                        integrated_app_hashes = current_version.get("hashes", {})
                        for i, v in integrated_app_hashes.items():
                            if i == "OrangeBlox.py": continue
                            file_hash = generateFileHash(os.path.join(app_path, i))
                            if not file_hash == v: validated = False; unable_to_validate.append([i, file_hash, v]); unable_to_validate2.append(i)
                        if validated == False and not (main_config.get("EFlagDisableSecureHashSecurity") == True):
                            printErrorMessage(f"Uh oh! There was an issue trying to validate hashes for the following files: {', '.join(unable_to_validate2)}")
                            printErrorMessage(f"Would you like to skip verification? Hashes that are unable to be validated are listed below:")
                            for i in unable_to_validate: printErrorMessage(f"{i[0]} | {i[2]} => {i[1]}")
                            if isYes(input("> ")) == False: ended = True; sys.exit(0); return
                        validated = True
                        printMainMessage(f"Running Bootstrap..")
                        if main_config.get("EFlagDisableSecureHashSecurity") == True: displayNotification(ts("Security Notice"), ts("Hash Verification is currently disabled. Please check your configuration and mod scripts if you didn't disable this!"))
                        if main_config.get("EFlagBuildPythonCacheOnStart") == True:
                            printMainMessage("Building Python Cache..")
                            build_cache_process = subprocess.run([pythonExecutable, "-m", "compileall", app_path], cwd=app_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                            if build_cache_process.returncode == 0: printSuccessMessage("Successfully built Python cache!")
                            else: printErrorMessage(f"Unable to build python cache. Return code: {build_cache_process.returncode}")
                        colors_class.clear_console()
                        result = subprocess.run([pythonExecutable, os.path.join(app_path, "Main.py")], cwd=os.path.join(app_path))
                        printMainMessage("Ending Bootstrap..")
                        ended = True
                        if result.returncode == 0: 
                            printSuccessMessage(f"Bootstrap Run Success: {result.returncode}")
                            sys.exit(0)
                        else: 
                            printErrorMessage(f"Uh oh! The bootstrap script failed! (Status Code: {result.returncode})")
                            printMainMessage("Hit enter to continue and close this window.")
                            input("> ")
                            sys.exit(0)
                    except Exception as e:
                        printErrorMessage(f"Bootstrap Run Failed: \n{trace()}")
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