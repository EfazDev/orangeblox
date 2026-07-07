import sys
import subprocess
import json
import os
import re
import threading
import codecs
import select
import zlib
import platform
import time
import uuid
import shutil
import traceback
import datetime
import textwrap
import logging
import hashlib
import webbrowser
import PyKits

current_version = {"version": "2.6.0d"}
main_os = platform.system()
args = sys.argv
generated_app_id = os.urandom(3).hex()
pip_class = PyKits.pip(find=True)
colors_class = PyKits.Colors()
app_path = ""
macos_path = ""
orangeblox_library = None
logs = []

COLOR_CODES = {
    0: "#ffffff",
    1: "#ff0000",
    2: "#ffff00",
    3: "#ff4b00",
    4: "#00ff00",
    5: "#ff4b00"
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
    "EFlagEnabledModOrder": "list",
    "EFlagMakeMainBootstrapLogFiles": "bool",
    "EFlagCompletedTutorial": "bool",
    "EFlagVerifyRobloxHashAfterInstall": "bool",
    "EFlagEnableDuplicationOfClients": "bool",
    "EFlagAllowActivityTracking": "bool",
    "EFlagDisableFastFlagInstallAccess": "bool",
    "EFlagBootstrapUpdateServer": "str",
    "EFlagLinkedComputerID": "str_local",
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
    "EFlagEnableURLQuickLaunch": "bool",
    "EFlagEnableCPUMemoryUsageViewer": "bool",
    "EFlagNotifyServerLocation": "bool",
    "EFlagEnableDiscordRPC": "bool",
    "EFlagEnableDiscordRPCStudio": "bool",
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
    "EFlagEnableRoValraServerUptime": "bool",
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
    "EFlagUseIXPFastFlagsMethod": "EFlagUseIXPFastFlagsMethod2",
    "EFlagUseIXPFastFlagsMethod2": "bool",
    "EFlagLastModVersionMacOSCaching": "str",
    "EFlagRobloxChannelUpdateToken": "str",
    "EFlagRobloxSecurityCookieUsage": "bool",
    "EFlagCustomBootstrapName": "str",
    "EFlagCustomBootstrapEmoji": "str",
    "EFlagCustomBootstrapColor": "str",
    "EFlagCustomBootstrapInternetURL": "str",
    "EFlagCustomBootstrapIconPath": "path",
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
def obName0(): return main_config.get("EFlagCustomBootstrapName", "OrangeBlox").strip()
def obName1(): return main_config.get("EFlagCustomBootstrapEmoji", "🍊").strip()
def obColorA(): return colors_class.hex_to_ansi(main_config.get("EFlagCustomBootstrapColor", "#ff4b00"))
def obColorH(): return main_config.get("EFlagCustomBootstrapColor", "#ff4b00")
def printMainMessage(mes): colors_class.print(ts(mes), 255); logs.append((ts(mes), 0))
def printErrorMessage(mes): colors_class.print(ts(mes), 196); logs.append((ts(mes), 1))
def printSuccessMessage(mes): colors_class.print(ts(mes), 82); logs.append((ts(mes), 4))
def printWarnMessage(mes): colors_class.print(ts(mes), 202); logs.append((ts(mes), 3))
def printSystemMessage(mes): colors_class.print(ts(mes), obColorA()); logs.append((ts(mes), 5))
def printYellowMessage(mes): colors_class.print(ts(mes), 226); logs.append((ts(mes), 2))
def printDebugMessage(mes): 
    if main_config.get("EFlagEnableDebugMode"): colors_class.print(f"[DEBUG]: {ts(mes)}", 226); logs.append((ts(mes), 2))
def pythonVersionStr(): return f"{pip_class.getCurrentPythonVersion()}{pip_class.getIfPythonVersionIsBeta() and ' (BETA)' or ''}"
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
def getIfCertainPlayer():
    if main_os == "Windows":
        if os.path.exists(os.path.join(app_path, "RobloxStudioBetaPlayRobloxRestart.txt")): 
            with open(os.path.join(app_path, "RobloxStudioBetaPlayRobloxRestart.txt"), "r") as f: return f.read(), "studio"
        elif os.path.exists(os.path.join(app_path, "RobloxPlayerBetaPlayRobloxRestart.txt")): 
            with open(os.path.join(app_path, "RobloxPlayerBetaPlayRobloxRestart.txt"), "r") as f: return f.read(), "player"
        else: return None, None
    else: return None, None
def generateFileKey(id: str, ext: str=""): 
    if main_os == "Darwin": return os.path.join(orangeblox_library, f"{id}{ext}")
    user_folder_name = os.path.basename(pip_class.getUserFolder())
    return os.path.join(app_path, f"{id}_{user_folder_name}{ext}")
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
            try: from plyer.platforms.win.notification import instance # type: ignore
            except Exception as e:
                pip_class.install(["plyer"])
                instance = pip_class.importModule("plyer.platforms.win.notification").instance
            instance().notify(
                title=title,
                message=message,
                app_name=obName0(),
                app_icon=os.path.join(app_path, "Images", "AppIcon.ico"),
                toast=True
            )
        except Exception as e: printErrorMessage(f"Something went wrong pinging Windows Notification Center: \n{trace()}")
def generateFileHash(file_path):
    try:
        hasher = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                if main_os == "Windows": chunk = chunk.replace(b"\r\n", b"\n")
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception: return None
if __name__ == "__main__":  
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        if main_os == "Windows": app_path = os.path.dirname(sys.executable); macos_path = os.path.join(app_path, "MacOS")
        else: macos_path = os.path.dirname(sys.executable); contents_path = os.path.dirname(macos_path); app_path = os.path.join(contents_path, "Resources")
    else:
        if main_os == "Windows":  app_path = os.path.dirname(sys.argv[0]); macos_path = app_path
        else: cur_path = os.path.dirname(os.path.abspath(__file__)); app_path = cur_path; macos_path = cur_path

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
            except Exception as e: obfuscated_json = json.loads(zlib.decompress(obfuscated_json).decode("utf-8", errors="ignore"))
            main_config = obfuscated_json
            loaded_json = True
        
    setLoggingHandler("Bootloader")
    printSystemMessage("-----------")
    printSystemMessage(f"Welcome to {obName0()} Loader {obName1()}!")
    if obName0() != "OrangeBlox" or obName1() != "🍊":
        printSystemMessage("Custom Theme of OrangeBlox 🍊")
    printSystemMessage("Made by Efaz from efaz.dev!")
    printSystemMessage(f"v{current_version['version']}")
    printSystemMessage("-----------")
    if main_os == "Windows": printMainMessage(f"System OS: {main_os} ({platform.version()}) | Python Version: {pythonVersionStr()}")
    elif main_os == "Darwin": printMainMessage(f"System OS: {main_os} (macOS {platform.mac_ver()[0]}) | Python Version: {pythonVersionStr()}")
    else:
        printErrorMessage(f"{obName0()} is only supported for macOS and Windows.")
        input("> ")
        sys.exit(0)
    if not pip_class.osSupported(windows_build=17763, macos_version=(10,15,0)):
        if main_os == "Windows": printErrorMessage(f"{obName0()} is only supported for Windows 10.0.17763 (October 2018) or higher. Please update your operating system in order to continue!")
        elif main_os == "Darwin": printErrorMessage(f"{obName0()} is only supported for macOS 10.15 (Catalina) or higher. Please update your operating system in order to continue!")
        input("> ")
        sys.exit(0)
    printSystemMessage("-----------")

    with open(os.path.join(os.path.dirname(__file__), "Version.json"), "r", encoding="utf-8") as f:
        current_version = json.load(f)
        f.close()

    if main_os == "Darwin":
        import pty
        filtered_args = ""
        loaded_json = True
        use_shell = False
        gui_app_lock = None
        user_folder = pip_class.getUserFolder()
        user_folder_name = os.path.basename(pip_class.getUserFolder())
        orangeblox_library = os.path.join(user_folder, "Library", "OrangeBlox")

        if not os.path.exists(orangeblox_library): os.makedirs(orangeblox_library)
        if main_config.get("EFlagEnableURLQuickLaunch") == True and os.path.exists(os.path.join(generateFileKey("URLQuickLaunch"))) and os.path.exists(os.path.join(orangeblox_library, f"GUIAppLock")):
            printMainMessage(f"Detected URL Quick Launch Attempt! Stopped App Launch.")
            sys.exit(0)

        printMainMessage("Finding Python Executable..")
        pythonExecutable = None
        if main_config.get("EFlagSpecifyPythonExecutable"): 
            pythonExecutable = main_config.get("EFlagSpecifyPythonExecutable")
            pip_class.executable = pythonExecutable
            if not os.path.exists(pythonExecutable) or not pip_class.pythonSupported(3, 11, 0): pythonExecutable = None
        if not pythonExecutable:
            if pip_class.pythonInstalled(computer=True) == False: pip_class.pythonInstall()
            pythonExecutable = pip_class.findPython(path=True)
        pip_class.executable = pythonExecutable
        if not os.path.exists(pythonExecutable) or not pip_class.pythonSupported(3, 11, 0): 
            pip_class.pythonInstall()
            pythonExecutable = pip_class.findPython(path=True)
            pip_class.executable = pythonExecutable
            if not os.path.exists(pythonExecutable) or not pip_class.pythonSupported(3, 11, 0):
                printErrorMessage(f"Please install Python 3.11 or later in order to use {obName0()}!")
                input("> ")
                sys.exit(0)
        printMainMessage(f"Generated App Window Fetching ID: {generated_app_id}")
        venv_path = ""
        if main_config.get("EFlagEnablePythonVirtualEnvironments") == True:
            printMainMessage("Checking Virtual Environments..")
            venv_path = os.path.join(orangeblox_library, "VirtualEnvironment")
            venv_class = PyKits.pip(executable=os.path.join(venv_path, "bin", "python3"))
            if not os.path.exists(venv_path) or not (venv_class.getArchitecture() == pip_class.getArchitecture() and venv_class.getCurrentPythonVersion() == pip_class.getCurrentPythonVersion()):
                if os.path.exists(venv_path) and not venv_class.getCurrentPythonVersion() == pip_class.getCurrentPythonVersion():
                    shutil.rmtree(venv_path, ignore_errors=True)
                generate_venv_process = subprocess.run([pythonExecutable, "-m", "venv", "--upgrade", venv_path], cwd=app_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if generate_venv_process.returncode == 0: printSuccessMessage("Generated Virtual Environment!")
                else: printErrorMessage(f"Failed to create virtual environment. Response Code: {generate_venv_process.returncode}"); venv_path = None
            else: printSuccessMessage("Found Virtual Environment!")
        command = f"/usr/bin/caffeinate -i {pythonExecutable if venv_path == '' else os.path.join(venv_path, 'bin', 'python3')} Main.py"
        cwd_tar = app_path
        printMainMessage(f"Loading Runner Command: {command}")

        if len(args) > 1:
            filtered_args = args[1]
            if (("roblox-player:" in filtered_args) or ("roblox-studio:" in filtered_args) or ("roblox-studio-auth:" in filtered_args) or ("roblox:" in filtered_args) or ("efaz-bootstrap:" in filtered_args) or ("orangeblox:" in filtered_args) or os.path.isfile(filtered_args)):
                use_shell = True
                printMainMessage(f"Creating URL Exchange file..")
                with open(f"{orangeblox_library}/URLLaunchExchange", "w", encoding="utf-8") as f: f.write(filtered_args)

        try:
            validated = None
            event_info = {}
            unable_to_validate = []
            unable_to_validate2 = []
            socket_authorization = []
            app_to_script_socket = PyKits.Socket(port=61239)

            def notification(payload):
                if not payload or payload.get("authorization") not in socket_authorization: return
                if payload.get("title") and payload.get("message"): 
                    displayNotification(payload["title"], payload["message"])
                    printSuccessMessage(f"Successfully pinged app notification! Title: {payload['title']}, Message: {payload['message']}")
            def eventInfo(payload):
                global event_info
                if not payload or payload.get("authorization") not in socket_authorization: return
                key = payload.get("authorization")
                payload.pop("authorization")
                event_info[key] = payload
                printDebugMessage(f"Received Event Info: {payload}")
            def createObjcAppReplication():
                global unable_to_validate
                global validated
                try:
                    printMainMessage(f"Starting GUI App Replication..")
                    try:
                        # Import and Modify Foundation
                        import objc
                        from Foundation import (
                            NSBundle,
                            NSObject, 
                            NSNotificationCenter, 
                            NSSize,
                            NSBackwardsSearch, 
                            NSNotFound
                        )
                        try:
                            if main_config.get("EFlagCustomBootstrapName"):
                                try:
                                    bundle = NSBundle.mainBundle()
                                    if bundle:
                                        app_info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
                                        if app_info: app_info["CFBundleName"] = main_config.get("EFlagCustomBootstrapName")
                                except ImportError: pass
                        except Exception as e: printDebugMessage(f"Failed to modify Foundation bundle info: \n{trace()}")
                        
                        # Import Other Modules
                        from AppKit import (
                            NSApplication, 
                            NSApp, 
                            NSColor, 
                            NSAttributedString, 
                            NSForegroundColorAttributeName, 
                            NSParagraphStyleAttributeName,
                            NSMutableParagraphStyle,
                            NSFontAttributeName, 
                            NSFont, 
                            NSWindow, 
                            NSWindowController, 
                            NSScrollView, 
                            NSTextView, 
                            NSTextStorage, 
                            NSLayoutManager, 
                            NSTextContainer, 
                            NSView, 
                            NSButton, 
                            NSImageView, 
                            NSImage, 
                            NSTextField, 
                            NSMenu, 
                            NSMenuItem, 
                            NSStatusBar, 
                            NSScreen, 
                            NSAlertFirstButtonReturn,
                            NSLayoutConstraint,
                            NSMaxY,
                            NSAlert,
                            NSViewWidthSizable, 
                            NSViewHeightSizable, 
                            NSWindowStyleMaskTitled, 
                            NSWindowStyleMaskClosable, 
                            NSWindowStyleMaskMiniaturizable, 
                            NSWindowStyleMaskResizable, 
                            NSBackingStoreBuffered, 
                            NSLayoutAttributeTop, 
                            NSLayoutAttributeBottom, 
                            NSLayoutAttributeLeading, 
                            NSLayoutAttributeTrailing, 
                            NSLayoutAttributeCenterX, 
                            NSLayoutAttributeWidth, 
                            NSLayoutAttributeHeight, 
                            NSLayoutRelationEqual, 
                            NSImageScaleProportionallyUpOrDown, 
                            NSCenterTextAlignment, 
                            NSFontWeightRegular, 
                            NSScrollElasticityNone, 
                            NSMutableAttributedString,
                            NSViewBoundsDidChangeNotification, 
                            NSRoundedBezelStyle, 
                            NSModalPanelWindowLevel, 
                            NSLineBreakByWordWrapping, 
                            NSVariableStatusItemLength, 
                            NSApplicationActivationPolicyRegular,
                            NSPasteboardTypeString,
                            NSPasteboard
                        )
                        import random
                        class TerminalTextView(NSTextView):
                            def setAppDelegate_(self, delegate): self.delegate = delegate
                            def keyDown_(self, event):
                                if not self.delegate.master_fd: return
                                mod = event.modifierFlags()
                                char_unmod = event.charactersIgnoringModifiers()
                                char_unmod_low = char_unmod.lower() if char_unmod else ""
                                char = event.characters()
                                kc = event.keyCode()
                                CMD_MASK = 1 << 20
                                if (mod & CMD_MASK) and char_unmod_low == "c":
                                    sel_range = self.selectedRange()
                                    if sel_range.length > 0:
                                        selected_text = self.string().substringWithRange_(sel_range)
                                        pb = NSPasteboard.generalPasteboard()
                                        pb.clearContents()
                                        pb.setString_forType_(selected_text, NSPasteboardTypeString)
                                    return
                                if (mod & CMD_MASK) and char_unmod_low == "v":
                                    pb = NSPasteboard.generalPasteboard()
                                    pasted_text = pb.stringForType_(NSPasteboardTypeString)
                                    if pasted_text:
                                        try: os.write(self.delegate.master_fd, pasted_text.encode("utf-8"))
                                        except OSError: pass
                                    return
                                if (mod & CMD_MASK) and char_unmod_low == "f":
                                    if hasattr(self, "setUsesFindBar_"): self.setUsesFindBar_(True)
                                    else: self.setUsesFindPanel_(True)
                                    self.performFindPanelAction_(self)
                                    return
                                if mod & CMD_MASK: return
                                try:
                                    if kc == 51: os.write(self.delegate.master_fd, b"\x7f") # Backspace
                                    elif kc == 36: os.write(self.delegate.master_fd, b"\r") # Return
                                    elif kc == 126: os.write(self.delegate.master_fd, b"\x1b[A") # Up Arrow
                                    elif kc == 125: os.write(self.delegate.master_fd, b"\x1b[B") # Down Arrow
                                    elif kc == 124: os.write(self.delegate.master_fd, b"\x1b[C") # Right Arrow
                                    elif kc == 123: os.write(self.delegate.master_fd, b"\x1b[D") # Left Arrow
                                    elif char: os.write(self.delegate.master_fd, char.encode("utf-8"))
                                except OSError: pass
                            def replaceCharactersInRange_withString_(self, affectedCharRange, replacementString): return False
                        class TerminalInstance(NSObject):
                            def init(self):
                                self = objc.super(TerminalInstance, self).init()
                                if self is None: return None
                                self.master_fd = None
                                self.process = None
                                self.cursor_id = 0 
                                self.clr_cache = {}
                                self.def_color = self.get_color("#FFFFFF") 
                                r,g,b = colors_class.hex_to_rgb(obColorH())
                                self.bg_color = self.get_color(colors_class.rgb_to_hex(int(r*0.35), int(g*0.35), int(b*0.35)))
                                self.cur_color = self.def_color
                                return self
                            def windowShouldClose_(self, sender):
                                try:
                                    if not hasattr(self, "process") or not self.process: return False
                                    if self.process.poll() is None:
                                        alert = NSAlert.alloc().init()
                                        alert.setMessageText_("OrangeBlox is still running")
                                        alert.setInformativeText_("Are you sure you want to close this terminal? Any unsaved data will be lost.")
                                        alert.addButtonWithTitle_("Close")
                                        alert.addButtonWithTitle_("Cancel")
                                        alert.setAlertStyle_(2)
                                        if alert.runModal() != NSAlertFirstButtonReturn: return False
                                    printMainMessage("Closing terminal..")
                                    try: self.process.terminate()
                                    except: pass
                                    app_delegate = NSApp().delegate()
                                    active_list = getattr(app_delegate, "active_terminals", [])
                                    if self in active_list: active_list.remove(self)
                                    if len(active_list) == 0 and not getattr(app_delegate, "debug_mode_window_enabled", False): NSApp().terminate_(None)
                                    return True
                                except Exception as e:
                                    printErrorMessage(f"windowShouldClose Error: \n{trace()}")
                                    return True
                            def terminalAppInit(self):
                                try:
                                    rect = ((100, 100), (620, 380))
                                    mask = NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskMiniaturizable | NSWindowStyleMaskResizable
                                    self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(rect, mask, NSBackingStoreBuffered, False)
                                    self.window.setTitle_(f"{obName0()} {obName1()}")
                                    self.window.setBackgroundColor_(self.bg_color)
                                    self.window.setDocumentEdited_(True) 
                                    self.window.setDelegate_(self) 
                                    self.window.setReleasedWhenClosed_(False)
                                    self.scroll_view = NSScrollView.alloc().initWithFrame_(self.window.contentView().bounds())
                                    self.scroll_view.setHasVerticalScroller_(True)
                                    self.scroll_view.setAutoresizingMask_(NSViewWidthSizable | NSViewHeightSizable)
                                    self.text_view = TerminalTextView.alloc().initWithFrame_(self.scroll_view.bounds())
                                    self.text_view.setAutoresizingMask_(NSViewWidthSizable | NSViewHeightSizable)
                                    self.text_view.setBackgroundColor_(self.bg_color)
                                    self.text_view.setInsertionPointColor_(self.def_color)
                                    font = NSFont.userFixedPitchFontOfSize_(13.0)
                                    if not font: font = NSFont.fontWithName_size_("SF Mono", 13.0)
                                    if not font: font = NSFont.fontWithName_size_("Menlo", 13.0)
                                    self.text_view.setFont_(font)
                                    self.paragraph_style = NSMutableParagraphStyle.alloc().init()
                                    self.paragraph_style.setMinimumLineHeight_(16.0)
                                    self.paragraph_style.setMaximumLineHeight_(16.0)
                                    self.paragraph_style.setLineSpacing_(0.0)
                                    self.paragraph_style.setParagraphSpacing_(0.0)
                                    self.paragraph_style.setParagraphSpacingBefore_(0.0)
                                    self.text_view.layoutManager().setUsesFontLeading_(False)
                                    self.text_view.setAutomaticQuoteSubstitutionEnabled_(False)
                                    self.text_view.setAutomaticDashSubstitutionEnabled_(False)
                                    self.text_view.setEditable_(True)
                                    self.text_view.setAppDelegate_(self)
                                    self.scroll_view.setDocumentView_(self.text_view)
                                    self.window.contentView().addSubview_(self.scroll_view)
                                    self.window.makeKeyAndOrderFront_(None)
                                    self.window.makeMainWindow()
                                    self.window.makeKeyWindow()
                                    NSApp.activateIgnoringOtherApps_(True)
                                except Exception as e: printErrorMessage(f"PyObjc Terminal App Failed! Error: \n{trace()}")
                            def start_process(self):
                                global validated
                                global unable_to_validate
                                global unable_to_validate2

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
                                        randomized_key = str(uuid.uuid4()).split("-")[0]
                                        socket_authorization.append(randomized_key)
                                        self.master_fd, sl_fd = pty.openpty()
                                        self.process = subprocess.Popen(
                                            ["/bin/zsh", "-c", command + " " + randomized_key],
                                            cwd=cwd_tar,
                                            stdin=sl_fd,
                                            stdout=sl_fd,
                                            stderr=sl_fd,
                                            close_fds=True
                                        )
                                        os.close(sl_fd)
                                        threading.Thread(target=self.read_output, daemon=True).start()
                                    else:
                                        displayNotification(ts("Uh oh!"), ts(f"Your copy of {obName0()} was unable to be validated and might be tampered with!"))
                                        printErrorMessage(f"Uh oh! There was an issue trying to validate hashes for the following files: {', '.join(unable_to_validate2)}")
                                        for i in unable_to_validate: printErrorMessage(f"{i[0]} | {i[2]} => {i[1]}")
                                        printErrorMessage(f"Requested validation failed window from pyobjc.")
                                except Exception as e: printErrorMessage(f"Failed to start process: {e}")
                            def read_output(self):
                                decoder = codecs.getincrementaldecoder("utf8")()
                                text_buffer = ""
                                last_flush_time = time.time()
                                try:
                                    while True:
                                        with objc.autorelease_pool():
                                            r, _, _ = select.select([self.master_fd], [], [], 0.05)
                                            if r:
                                                data = os.read(self.master_fd, 4096)
                                                if not data: break
                                                text = decoder.decode(data)
                                                if text: text_buffer += text
                                            elif self.process and self.process.poll() is not None: break
                                            current_time = time.time()
                                            if text_buffer and (current_time - last_flush_time >= 0.05 or len(text_buffer) > 10000):
                                                self.performSelectorOnMainThread_withObject_waitUntilDone_("processOutputChunk:", text_buffer, False)
                                                text_buffer = ""
                                                last_flush_time = current_time
                                except OSError: pass 
                                except Exception: pass
                                exit_message = "\r\n\033[38;5;82m[OrangeBlox is now closing]\033[0m"
                                self.performSelectorOnMainThread_withObject_waitUntilDone_("processOutputChunk:", exit_message, True)
                                if self.process: self.process.wait()
                                time.sleep(0.1)
                                self.performSelectorOnMainThread_withObject_waitUntilDone_("forceCloseApp:", None, False)
                            def forceCloseApp_(self, sender):
                                try:
                                    if hasattr(self, "text_view") and self.text_view: self.text_view.setAppDelegate_(None)
                                    if self.master_fd is not None:
                                        try: os.close(self.master_fd)
                                        except OSError: pass
                                        self.master_fd = None
                                    if hasattr(self, "window") and self.window: self.window.close()
                                    if hasattr(self, "process") and self.process and self.process.poll() is None:
                                        try: self.process.terminate()
                                        except: pass
                                    app_delegate = NSApp().delegate()
                                    active_list = getattr(app_delegate, "active_terminals", [])
                                    if self in active_list: active_list.remove(self)
                                    if len(active_list) == 0 and not getattr(app_delegate, "debug_mode_window_enabled", False): NSApp().terminate_(None)
                                except Exception as e: printErrorMessage(f"forceCloseApp Error: \n{trace()}")
                            def processOutputChunk_(self, text):
                                storage = self.text_view.textStorage()
                                storage.beginEditing() 
                                try:
                                    tokens = re.split(r"(\x1B\[[0-?]*[ -/]*[@-~]|\r|\n|\x08|\x7f)", text)
                                    for token in tokens:
                                        if not token: continue
                                        if token.startswith("\x1b"): self.parseAnsi(token)
                                        elif token == "\r": self.handleCarriageReturn()
                                        elif token == "\n": self.handleNewline()
                                        elif token in ("\x08", "\x7f"): self.handleBackspace()
                                        else: self.appendRaw(token)
                                finally:
                                    storage.endEditing() 
                                    self.text_view.setSelectedRange_((self.cursor_id, 0))
                                    self.scrollToBottomIfNeeded()
                            @objc.python_method
                            def get_color(self, hex_str):
                                hex_str = str(hex_str).upper()
                                if hex_str in self.clr_cache: return self.clr_cache[hex_str]
                                r, g, b = 255, 255, 255
                                try:
                                    rgb = colors_class.hex_to_rgb(hex_str)
                                    if isinstance(rgb, (list, tuple)) and len(rgb) >= 3: r, g, b = rgb[0], rgb[1], rgb[2]
                                except Exception: pass
                                r_norm = r / 255.0
                                g_norm = g / 255.0
                                b_norm = b / 255.0
                                color = NSColor.colorWithSRGBRed_green_blue_alpha_(r_norm, g_norm, b_norm, 1.0)
                                self.clr_cache[hex_str] = color
                                return color
                            @objc.python_method
                            def handleCarriageReturn(self):
                                ns_string = self.text_view.textStorage().string()
                                range_nl = ns_string.rangeOfString_options_range_("\n", NSBackwardsSearch, (0, self.cursor_id))
                                self.cursor_id = range_nl.location + 1 if range_nl.location != NSNotFound else 0
                            @objc.python_method
                            def handleNewline(self):
                                storage = self.text_view.textStorage()
                                ns_string = storage.string()
                                length = storage.length()
                                if self.cursor_id < length:
                                    range_nl = ns_string.rangeOfString_options_range_("\n", 0, (self.cursor_id, length - self.cursor_id))
                                    if range_nl.location != NSNotFound:
                                        self.cursor_id = range_nl.location + 1
                                        return
                                attrs = {NSForegroundColorAttributeName: self.cur_color, NSFontAttributeName: self.text_view.font(), NSParagraphStyleAttributeName: self.paragraph_style}
                                attr_str = NSAttributedString.alloc().initWithString_attributes_("\n", attrs)
                                storage.appendAttributedString_(attr_str)
                                self.cursor_id = storage.length()
                            @objc.python_method
                            def handleBackspace(self):
                                ns_string = self.text_view.textStorage().string()
                                range_nl = ns_string.rangeOfString_options_range_("\n", NSBackwardsSearch, (0, self.cursor_id))
                                line_start = range_nl.location + 1 if range_nl.location != NSNotFound else 0
                                if self.cursor_id > line_start:
                                    char_range = ns_string.rangeOfComposedCharacterSequenceAtIndex_(self.cursor_id - 1)
                                    self.cursor_id = char_range.location
                            @objc.python_method
                            def appendRaw(self, text):
                                try:
                                    storage = self.text_view.textStorage()
                                    ns_string = storage.string()
                                    length = storage.length()
                                    if self.cursor_id > length: self.cursor_id = length
                                    attrs = {
                                        NSForegroundColorAttributeName: self.cur_color,
                                        NSFontAttributeName: self.text_view.font(),
                                        NSParagraphStyleAttributeName: self.paragraph_style
                                    }
                                    attr_str = NSAttributedString.alloc().initWithString_attributes_(text, attrs)
                                    text_len = attr_str.length() 
                                    range_nl = ns_string.rangeOfString_options_range_("\n", 0, (self.cursor_id, length - self.cursor_id))
                                    next_nl = range_nl.location if range_nl.location != NSNotFound else length
                                    avail_space = next_nl - self.cursor_id
                                    if text_len <= avail_space:
                                        storage.replaceCharactersInRange_withAttributedString_(
                                            (self.cursor_id, text_len), attr_str
                                        )
                                        self.cursor_id += text_len
                                    else:
                                        storage.replaceCharactersInRange_withAttributedString_(
                                            (self.cursor_id, avail_space), attr_str
                                        )
                                        self.cursor_id += text_len
                                except Exception: pass
                            @objc.python_method
                            def parseAnsi(self, seq):
                                try:
                                    storage = self.text_view.textStorage()
                                    ns_string = storage.string()
                                    length = storage.length()
                                    if seq.endswith("A") or seq.endswith("F"):
                                        codes = re.findall(r"\d+", seq)
                                        n = int(codes[0]) if codes else 1
                                        for _ in range(n):
                                            ns_string = storage.string() 
                                            range_cur = ns_string.rangeOfString_options_range_("\n", NSBackwardsSearch, (0, self.cursor_id))
                                            cur_line_start = range_cur.location + 1 if range_cur.location != NSNotFound else 0
                                            current_col = self.cursor_id - cur_line_start
                                            if cur_line_start > 0:
                                                range_prev = ns_string.rangeOfString_options_range_("\n", NSBackwardsSearch, (0, cur_line_start - 1))
                                                prev_line_start = range_prev.location + 1 if range_prev.location != NSNotFound else 0
                                                if seq.endswith("A"):
                                                    prev_line_len = (cur_line_start - 1) - prev_line_start
                                                    self.cursor_id = prev_line_start + min(current_col, prev_line_len)
                                                else: self.cursor_id = prev_line_start
                                            else: break
                                        return
                                    if seq.endswith("K"):
                                        range_cur = ns_string.rangeOfString_options_range_("\n", NSBackwardsSearch, (0, self.cursor_id))
                                        cur_line_start = range_cur.location + 1 if range_cur.location != NSNotFound else 0
                                        range_next = ns_string.rangeOfString_options_range_("\n", 0, (self.cursor_id, length - self.cursor_id))
                                        next_nl = range_next.location if range_next.location != NSNotFound else length
                                        if "2K" in seq:
                                            if next_nl > cur_line_start:
                                                storage.deleteCharactersInRange_((cur_line_start, next_nl - cur_line_start))
                                                self.cursor_id = cur_line_start
                                        elif "K" in seq:
                                            if next_nl > self.cursor_id: storage.deleteCharactersInRange_((self.cursor_id, next_nl - self.cursor_id))
                                        return
                                    if "2J" in seq or "c" in seq:
                                        storage.deleteCharactersInRange_((0, storage.length()))
                                        self.cursor_id = 0
                                        return
                                    elif "J" in seq:
                                        if storage.length() > self.cursor_id: storage.deleteCharactersInRange_((self.cursor_id, storage.length() - self.cursor_id))
                                        return
                                    if seq.endswith("m"):
                                        codes = re.findall(r"\d+", seq)
                                        if not codes or "0" in codes:
                                            self.cur_color = self.def_color
                                            return
                                        if "38" in codes and "5" in codes and len(codes) >= 3:
                                            try:
                                                color_index = int(codes[2])
                                                hex_val = colors_class.ansi_to_hex_table.get(color_index, "#FFFFFF")
                                                self.cur_color = self.get_color(hex_val)
                                            except Exception: pass
                                        elif "31" in codes: self.cur_color = self.get_color("#FF3B30") 
                                        elif "32" in codes: self.cur_color = self.get_color("#34C759") 
                                        elif "33" in codes: self.cur_color = self.get_color("#FFCC00") 
                                        elif "34" in codes: self.cur_color = self.get_color("#007AFF") 
                                        elif "35" in codes: self.cur_color = self.get_color("#AF52DE") 
                                        elif "36" in codes: self.cur_color = self.get_color("#5AC8FA") 
                                except Exception: pass
                            @objc.python_method
                            def scrollToBottomIfNeeded(self):
                                try:
                                    doc_vis = self.scroll_view.documentVisibleRect()
                                    doc_bounds = self.scroll_view.documentView().bounds()
                                    if NSMaxY(doc_vis) >= NSMaxY(doc_bounds) - 20.0:
                                        self.text_view.scrollToEndOfDocument_(None)
                                except Exception: pass
                        class AppDelegate(NSObject):
                            def init(self):
                                self = objc.super(AppDelegate, self).init()
                                if self is None: return None

                                # Terminal App
                                self.active_terminals = []
                                self.closing_approved = False

                                # PyObjc App Debug Window
                                self.debug_win = None
                                self.debug_win_controller = None
                                self.debug_mode_window_enabled = False
                                self.debug_holding_frame = None
                                self.debug_output_scroll_view = None
                                self.debug_output_area = None
                                self.debug_icon_view = None
                                self.debug_label1 = None
                                self.debug_label2 = None
                                self.debug_is_at_bottom = True
                                self.debug_last_checked_index = 0
                                self.debug_button = False

                                # Validation Window
                                self.validation_failed_window = None
                                self.validation_frame = None

                                # Menus and Configuration
                                self.main_menu = None
                                self.top_menu = None
                                self.dock_menu = None
                                self.app_icon = None
                                self.status_item = None
                                self.terminating = False
                                self.requested_kill = False
                                self.already_activated = False
                                self.top_menu_options = {}
                                self.dock_menu_options = {}
                                self.shortcut_options = []
                                self.config_reload_period = False
                                return self
                            def applicationDidFinishLaunching_(self, notification):
                                try:
                                    printMainMessage("macOS Application finished launching..")
                                    app_icon_url = main_config.get("EFlagCustomBootstrapIconPath", f"{app_path}/Images/AppIcon.png")
                                    if main_config.get("EFlagUseFollowingAppIconPath"): app_icon_url = main_config.get("EFlagUseFollowingAppIconPath")
                                    if os.path.exists(app_icon_url): 
                                        self.app_icon = NSImage.alloc().initByReferencingFile_(app_icon_url)
                                        if app_icon_url.lower().endswith(".png"): self.app_icon.setSize_((512, 512))
                                    else: self.app_icon = NSImage.alloc().initByReferencingFile_(f"{app_path}/Images/AppIcon.icns")
                                    NSApp().setApplicationIconImage_(self.app_icon)
                                    self.generate_top_menu()
                                    if not (main_config.get("EFlagEnableGUIOptionMenus") == False): self.generate_dock_menu()
                                    if len(self.active_terminals) == 0: self.createNewTerminal()
                                    self.debugWindowInit()

                                    try:
                                        pip_class.startThread(func=self.config_reload_period_func, daemon=True)
                                        if validated == False: self.show_validation_failed_menu()
                                        self.threadingloop_(None)
                                    except Exception as e: printErrorMessage(f"Something went wrong with running functions! Error: \n{trace()}")
                                    printMainMessage(f"PyObjc app finished launching!")
                                except Exception: printErrorMessage(f"PyObjc App Failed! Error: \n{trace()}")
                            def applicationShouldTerminate_(self, sender): return self.on_close(should=True)
                            def windowWillMiniaturize_(self, notification): self.prevent_minimize()
                            def onButtonClick_(self, sender): self.createNewTerminal()
                            def application_openURLs_(self, application, urls):
                                try:
                                    for url in urls:
                                        if url.isFileURL(): url_scheme = str(url.path())
                                        else: url_scheme = str(url.absoluteString())
                                        printMainMessage(f"Found URL: {url_scheme}")
                                        url_scheme_path = f"{orangeblox_library}/URLLaunchExchange"
                                        with open(url_scheme_path, "w", encoding="utf-8") as f: f.write(url_scheme)
                                        printMainMessage(f"Created URL Exchange File: {url_scheme_path}")
                                        if len(self.active_terminals) >= 1: self.createNewTerminal()
                                except Exception as e: printErrorMessage(f"Failed to process URL: {e}")
                            def application_openFile_(self, sender, filename):
                                try:
                                    printMainMessage(f"Found File: {filename}")
                                    url_scheme_path = f"{orangeblox_library}/URLLaunchExchange"
                                    with open(url_scheme_path, "w", encoding="utf-8") as f: f.write(filename)
                                    printMainMessage(f"Created URL Exchange File: {url_scheme_path}")
                                    if len(self.active_terminals) >= 1: self.createNewTerminal()
                                    return True
                                except Exception as e:
                                    printErrorMessage(f"Failed to process opened file: {e}")
                                    return False
                            def windowDidBecomeMain_(self, notification): 
                                if notification.object() == self.debug_win and self.already_activated == False: self.already_activated = True; self.on_window_activate(None)
                            def windowDidResignMain_(self, notification):
                                if notification.object() == self.debug_win: self.already_activated = False
                            def windowShouldClose_(self, sender):
                                if sender == self.debug_win:
                                    self.disable_debug_mode_window()
                                    return False 
                                elif self.validation_frame and sender == self.validation_failed_window: return self.on_close(should=True)
                                return True
                            def windowDidMiniaturize_(self, notification): self.debug_win.deminiaturize_(None); self.prevent_minimize()
                            def appendBatchLogs_(self, batch_string):
                                storage = self.debug_output_area.textStorage()
                                storage.beginEditing()
                                try:
                                    storage.appendAttributedString_(batch_string)
                                finally: storage.endEditing()
                                lm = self.debug_output_area.layoutManager()
                                tc = self.debug_output_area.textContainer()
                                lm.ensureLayoutForTextContainer_(tc)
                                if self.debug_is_at_bottom: self.debug_output_area.scrollRangeToVisible_((storage.length(), 0))
                                self.updateScrollingLogsHeight()
                            def threadingloop_(self, obj):
                                try:
                                    COLOR_CODES[5] = obColorH()
                                    new_logs = logs[self.debug_last_checked_index:]
                                    if new_logs:
                                        batch_string = NSMutableAttributedString.alloc().init()
                                        font = self.debug_output_area.font()
                                        for log, color_code in new_logs:
                                            lines = textwrap.wrap(log, width=75)
                                            for line in lines:
                                                color_hex = COLOR_CODES.get(color_code, "#ffffff")
                                                color_ns = self.get_color(color_hex)
                                                attr_str = NSAttributedString.alloc().initWithString_attributes_(
                                                    f" {line}\n",
                                                    {NSForegroundColorAttributeName: color_ns, NSFontAttributeName: font}
                                                )
                                                batch_string.appendAttributedString_(attr_str)
                                        self.debug_last_checked_index = len(logs)
                                        self.performSelectorOnMainThread_withObject_waitUntilDone_("appendBatchLogs:", batch_string, False)
                                    if self.config_reload_period: self.config_reload_period = False
                                    if obj != "oranges":
                                        def delayed_loop(): self.performSelectorOnMainThread_withObject_waitUntilDone_("threadingloop:", obj, False)
                                        pip_class.delayedThread(func=delayed_loop, time=0.1, daemon=True)
                                except Exception as e: printErrorMessage(f"There was an error loading loop! Error: \n{trace()}")
                            def scrollingLogs_(self, notification):
                                content_view = self.debug_output_scroll_view.contentView()
                                document_view = self.debug_output_scroll_view.documentView()
                                visible_rect = content_view.bounds()
                                document_rect = document_view.bounds()
                                max_y = document_rect.size.height - visible_rect.size.height
                                current_y = visible_rect.origin.y
                                if max_y <= 0: self.debug_is_at_bottom = True
                                elif abs(current_y - max_y) < 8.0: self.debug_is_at_bottom = True
                                else: self.debug_is_at_bottom = False
                            def debugWindowInit(self):
                                try:
                                    self.debug_win = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
                                        ((100.0, 100.0), (780.0, 500.0)),
                                        NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskResizable,
                                        NSBackingStoreBuffered,
                                        False
                                    ).autorelease()
                                    self.debug_win_controller = NSWindowController.alloc().initWithWindow_(self.debug_win)
                                    self.debug_win_controller.setShouldCascadeWindows_(False)
                                    self.debug_win.setTitle_(obName0())
                                    self.debug_win.setOpaque_(False)
                                    self.debug_win.setAlphaValue_(0.0)
                                    self.debug_win.setDelegate_(self)
                                    self.debug_win.setContentMinSize_(NSSize(780, 500))
                                    self.debug_win.setReleasedWhenClosed_(False)

                                    content_view = self.debug_win.contentView()
                                    self.debug_holding_frame = NSView.alloc().initWithFrame_(content_view.frame())
                                    self.debug_holding_frame.setTranslatesAutoresizingMaskIntoConstraints_(False)
                                    content_view.addSubview_(self.debug_holding_frame)
                                    constraints = [
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.debug_holding_frame, NSLayoutAttributeTop,
                                            NSLayoutRelationEqual,
                                            content_view, NSLayoutAttributeTop,
                                            1, 0
                                        ),
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.debug_holding_frame, NSLayoutAttributeBottom,
                                            NSLayoutRelationEqual,
                                            content_view, NSLayoutAttributeBottom,
                                            1, 0
                                        ),
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.debug_holding_frame, NSLayoutAttributeLeading,
                                            NSLayoutRelationEqual,
                                            content_view, NSLayoutAttributeLeading,
                                            1, 0
                                        ),
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.debug_holding_frame, NSLayoutAttributeTrailing,
                                            NSLayoutRelationEqual,
                                            content_view, NSLayoutAttributeTrailing,
                                            1, 0
                                        ),
                                    ]
                                    content_view.addConstraints_(constraints)

                                    self.debug_icon_view = NSImageView.alloc().init()
                                    self.debug_icon_view.setImage_(self.app_icon)
                                    self.debug_icon_view.setImageScaling_(NSImageScaleProportionallyUpOrDown)
                                    self.debug_icon_view.setTranslatesAutoresizingMaskIntoConstraints_(False)
                                    self.debug_holding_frame.addSubview_(self.debug_icon_view)

                                    self.debug_label1 = NSTextField.alloc().init()
                                    self.debug_label1.setStringValue_(ts(f"Ooh! Hi there! Welcome to {obName0()} {obName1()}!"))
                                    self.debug_label1.setFont_(NSFont.systemFontOfSize_(16))
                                    self.debug_label1.setBezeled_(False)
                                    self.debug_label1.setDrawsBackground_(False)
                                    self.debug_label1.setEditable_(False)
                                    self.debug_label1.setSelectable_(False)
                                    self.debug_label1.setAlignment_(NSCenterTextAlignment)
                                    self.debug_label1.setTranslatesAutoresizingMaskIntoConstraints_(False)
                                    self.debug_holding_frame.addSubview_(self.debug_label1)

                                    self.debug_label2 = NSTextField.alloc().init()
                                    self.debug_label2.setStringValue_(ts("Bootstrap Loader Logs:"))
                                    self.debug_label2.setFont_(NSFont.systemFontOfSize_(13))
                                    self.debug_label2.setBezeled_(False)
                                    self.debug_label2.setDrawsBackground_(False)
                                    self.debug_label2.setEditable_(False)
                                    self.debug_label2.setSelectable_(False)
                                    self.debug_label2.setAlignment_(NSCenterTextAlignment)
                                    self.debug_label2.setTranslatesAutoresizingMaskIntoConstraints_(False)
                                    self.debug_holding_frame.addSubview_(self.debug_label2)

                                    self.debug_output_scroll_view = NSScrollView.alloc().init()
                                    self.debug_output_scroll_view.setHasVerticalScroller_(True)
                                    self.debug_output_scroll_view.setAutohidesScrollers_(True)
                                    self.debug_output_scroll_view.setTranslatesAutoresizingMaskIntoConstraints_(False)
                                    self.debug_output_scroll_view.setVerticalScrollElasticity_(NSScrollElasticityNone)
                                    self.debug_output_scroll_view.setHorizontalScrollElasticity_(NSScrollElasticityNone)
                                    text_storage = NSTextStorage.alloc().init()
                                    layout_manager = NSLayoutManager.alloc().init()
                                    text_container = NSTextContainer.alloc().initWithContainerSize_((800, float("inf")))
                                    layout_manager.addTextContainer_(text_container)
                                    text_storage.addLayoutManager_(layout_manager)
                                    self.debug_output_area = NSTextView.alloc().initWithFrame_textContainer_(((0, 0), (800, 500)), text_container)
                                    if pip_class.osSupported(macos_version=(10, 15, 0)): self.debug_output_area.setFont_(NSFont.monospacedSystemFontOfSize_weight_(13, NSFontWeightRegular))
                                    else: self.debug_output_area.setFont_(NSFont.systemFontOfSize_(13))
                                    self.debug_output_area.setEditable_(False)
                                    self.debug_output_area.setSelectable_(True)
                                    self.debug_output_area.setDrawsBackground_(True)
                                    self.debug_output_area.setBackgroundColor_(NSColor.colorWithCalibratedRed_green_blue_alpha_(0.12, 0.12, 0.12, 1))
                                    self.debug_output_area.setTextColor_(NSColor.whiteColor())
                                    self.debug_output_area.setInsertionPointColor_(NSColor.whiteColor())
                                    self.debug_output_area.setTranslatesAutoresizingMaskIntoConstraints_(False)
                                    self.debug_output_scroll_view.setDocumentView_(self.debug_output_area)
                                    self.debug_output_area.setVerticallyResizable_(True)
                                    self.debug_output_area.setHorizontallyResizable_(False)
                                    self.debug_output_area.setAutoresizingMask_(NSViewWidthSizable)
                                    text_container = self.debug_output_area.textContainer()
                                    text_container.setWidthTracksTextView_(True)
                                    text_container.setContainerSize_((800, float("inf")))
                                    self.debug_output_area.setMinSize_((0.0, 0.0))
                                    self.debug_output_area.setMaxSize_((float("inf"), float("inf")))
                                    content_height = self.debug_output_area.layoutManager().usedRectForTextContainer_(text_container).size.height
                                    self.debug_output_area.setFrameSize_((800, content_height))
                                    self.debug_output_area.setTextContainerInset_((4, 8))
                                    self.debug_holding_frame.addSubview_(self.debug_output_scroll_view)
                                    NSNotificationCenter.defaultCenter().addObserver_selector_name_object_(
                                        self,
                                        "scrollingLogs:",
                                        NSViewBoundsDidChangeNotification,
                                        self.debug_output_scroll_view.contentView()
                                    )

                                    self.debug_button = NSButton.alloc().init()
                                    self.debug_button.setTitle_(ts("Create bootstrap window!"))
                                    self.debug_button.setBezelStyle_(NSRoundedBezelStyle)
                                    self.debug_button.setTarget_(self)
                                    self.debug_button.setAction_(objc.selector(self.onButtonClick_, signature=b"v@:@"))
                                    self.debug_button.setTranslatesAutoresizingMaskIntoConstraints_(False)
                                    self.debug_holding_frame.addSubview_(self.debug_button)

                                    constraints = [
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.debug_icon_view, NSLayoutAttributeCenterX,
                                            NSLayoutRelationEqual, self.debug_holding_frame, NSLayoutAttributeCenterX, 1, 0),
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.debug_icon_view, NSLayoutAttributeTop,
                                            NSLayoutRelationEqual, self.debug_holding_frame, NSLayoutAttributeTop, 1, 20),
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.debug_icon_view, NSLayoutAttributeWidth,
                                            NSLayoutRelationEqual, None, 0, 1, 64),
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.debug_icon_view, NSLayoutAttributeHeight,
                                            NSLayoutRelationEqual, None, 0, 1, 64),
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.debug_label1, NSLayoutAttributeTop,
                                            NSLayoutRelationEqual, self.debug_icon_view, NSLayoutAttributeBottom, 1, 20),
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.debug_label1, NSLayoutAttributeCenterX,
                                            NSLayoutRelationEqual, self.debug_holding_frame, NSLayoutAttributeCenterX, 1, 0),
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.debug_label2, NSLayoutAttributeTop,
                                            NSLayoutRelationEqual, self.debug_label1, NSLayoutAttributeBottom, 1, 15),
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.debug_label2, NSLayoutAttributeCenterX,
                                            NSLayoutRelationEqual, self.debug_holding_frame, NSLayoutAttributeCenterX, 1, 0),
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.debug_output_scroll_view, NSLayoutAttributeTop,
                                            NSLayoutRelationEqual, self.debug_label2, NSLayoutAttributeBottom, 1, 15),
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.debug_output_scroll_view, NSLayoutAttributeCenterX,
                                            NSLayoutRelationEqual, self.debug_holding_frame, NSLayoutAttributeCenterX, 1, 0),
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.debug_output_scroll_view, NSLayoutAttributeWidth,
                                            NSLayoutRelationEqual, self.debug_holding_frame, NSLayoutAttributeWidth, 0.9, 0),
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.debug_output_scroll_view, NSLayoutAttributeHeight,
                                            NSLayoutRelationEqual, None, 0, 1, 260),
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.debug_button, NSLayoutAttributeTop,
                                            NSLayoutRelationEqual, self.debug_output_scroll_view, NSLayoutAttributeBottom, 1, 15),
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.debug_button, NSLayoutAttributeCenterX,
                                            NSLayoutRelationEqual, self.debug_holding_frame, NSLayoutAttributeCenterX, 1, 0),
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.debug_button, NSLayoutAttributeWidth,
                                            NSLayoutRelationEqual, None, 0, 1, 260),
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            self.debug_button, NSLayoutAttributeHeight,
                                            NSLayoutRelationEqual, None, 0, 1, 30)
                                    ]
                                    self.debug_holding_frame.addConstraints_(constraints)
                                    self.debug_holding_frame.layoutSubtreeIfNeeded()
                                    self.debug_win.display()
                                except Exception: printErrorMessage(f"PyObjc Debug App Failed! Error: \n{trace()}")
                            def prevent_minimize(self): printDebugMessage("Prevented minimizing main window in order to keep app running smoothly.")
                            def updateScrollingLogsHeight(self):
                                layout_manager = self.debug_output_area.layoutManager()
                                text_container = self.debug_output_area.textContainer()
                                used_rect = layout_manager.usedRectForTextContainer_(text_container)
                                content_height = used_rect.size.height + 20
                                self.debug_output_area.setFrameSize_((800, content_height))
                            def on_close(self, should: bool=False):
                                try:
                                    if self.terminating == True or self.closing_approved == True: return True
                                    running_terminals = [t for t in getattr(self, "active_terminals", []) if t.process and t.process.poll() is None]
                                    if len(running_terminals) > 0:
                                        alert = NSAlert.alloc().init()
                                        alert.setMessageText_("OrangeBlox is still running")
                                        alert.setInformativeText_(f"You have {len(running_terminals)} active OrangeBlox windows open. Are you sure you want to close all of them? Any unsaved data will be lost.")
                                        alert.addButtonWithTitle_("Close Anyway")
                                        alert.addButtonWithTitle_("Cancel")
                                        alert.setAlertStyle_(2)
                                        response = alert.runModal()
                                        if response == 1000:
                                            self.closing_approved = True
                                            for term in running_terminals:
                                                try: term.process.terminate()
                                                except: pass
                                            self.terminating = True
                                            self.unlock_app_lock()
                                            if not should: NSApp().terminate_(None)
                                            return True
                                        else: return False
                                    self.terminating = True
                                    self.unlock_app_lock()
                                    if not should: NSApp().terminate_(None)
                                    return True
                                except Exception as e:
                                    printErrorMessage(f"Error ending app: \n{trace()}")
                                    return True
                            
                            # macOS Menus
                            def generate_top_menu(self):
                                if not self.top_menu: self.top_menu = NSMenu.alloc().init()
                                self.main_menu = NSMenu.alloc().init()
                                self.top_menu.removeAllItems()
                                main_menu_item = NSMenuItem.alloc().init()
                                self.top_menu.addItem_(main_menu_item)
                                self.top_menu.setSubmenu_forItem_(self.main_menu, main_menu_item)
                                def add_menu_item(menu, title, action_name, option=""):
                                    if hasattr(self, action_name):
                                        sel = objc.selector(getattr(self, action_name), signature=b"v@:@")
                                        item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(title, sel, option)
                                        item.setTarget_(self)
                                    else: item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(title, None, option)
                                    self.top_menu_options[title] = item
                                    menu.addItem_(item)
                                    return item
                                add_menu_item(self.main_menu, ts(f"About {obName0()}"), "showAboutMenu_", "]")
                                self.main_menu.addItem_(NSMenuItem.separatorItem())
                                add_menu_item(self.main_menu, ts("New Bootstrap Window"), "newBootstrapWindow_", "n")
                                add_menu_item(self.main_menu, ts("Refresh App Configuration"), "refreshConfig_", "r")
                                if main_config.get("EFlagEnableDebugMode") == True: 
                                    s = add_menu_item(self.main_menu, ts("Open Debug Window"), "debugWindowButton_", "d")
                                    s.setTitle_(ts("Open Debug Window") if self.debug_mode_window_enabled == False else ts("Close Debug Window"))
                                self.main_menu.addItem_(NSMenuItem.separatorItem())
                                add_menu_item(self.main_menu, ts("Open Mods Manager"), "openModsManager_", "m")
                                add_menu_item(self.main_menu, ts("Open Settings"), "openSettings_", ",")
                                add_menu_item(self.main_menu, ts("Open Credits"), "openCredits_", "[")
                                quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(ts(f"Quit {obName0()}"), "terminate:", "q")
                                self.main_menu.addItem_(quit_item)

                                file_menu = NSMenu.alloc().initWithTitle_("File")
                                file_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("File", None, "")
                                self.top_menu.addItem_(file_menu_item)
                                self.top_menu.setSubmenu_forItem_(file_menu, file_menu_item)
                                file_menu.addItem_(NSMenuItem.separatorItem())
                                add_menu_item(file_menu, ts("New Bootstrap Window"), "newBootstrapWindow_", "n")
                                add_menu_item(file_menu, ts("Open Roblox"), "runRoblox_")
                                if main_config.get("EFlagRobloxStudioEnabled") == True: add_menu_item(file_menu, ts("Run Roblox Studio"), "runRobloxStudio_")
                                file_menu.addItem_(NSMenuItem.separatorItem())
                                if not (main_config.get("EFlagAllowActivityTracking") == False): 
                                    add_menu_item(file_menu, ts("Connect to Existing Roblox"), "reconnectRoblox_")
                                    if main_config.get("EFlagRobloxStudioEnabled") == True: add_menu_item(file_menu, ts("Connect to Existing Roblox Studio"), "reconnectRobloxStudio_")
                                file_menu.addItem_(NSMenuItem.separatorItem())
                                add_menu_item(file_menu, ts("Run Fast Flags Installer"), "runFFlagInstaller_")
                                add_menu_item(file_menu, ts("Clear Temporary Storage"), "clearRobloxLogs_")
                                add_menu_item(file_menu, ts("Roblox Installer Options"), "openRobloxInstallerOptions_")
                                add_menu_item(file_menu, ts("End All Roblox Windows"), "endAllRoblox_")
                                if main_config.get("EFlagRobloxStudioEnabled") == True: add_menu_item(file_menu, ts("End All Roblox Studio Windows"), "endAllRobloxStudio_")
                                if main_config.get("EFlagEnableURLQuickLaunch") == True: add_menu_item(file_menu, ts("URL Quick Launch"), "urlQuickLaunch_")
                                
                                edit_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Edit", None, "")
                                edit_menu = NSMenu.alloc().initWithTitle_("Edit")
                                self.top_menu.addItem_(edit_menu_item)
                                self.top_menu.setSubmenu_forItem_(edit_menu, edit_menu_item)
                                def add_standard_edit(menu, title, selector, option=""):
                                    item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(title, selector, option)
                                    menu.addItem_(item)
                                add_standard_edit(edit_menu, ts("Undo"), "undo:", "z")
                                add_standard_edit(edit_menu, ts("Redo"), "redo:", "Z")
                                edit_menu.addItem_(NSMenuItem.separatorItem())
                                add_standard_edit(edit_menu, ts("Cut"), "cut:", "x")
                                add_standard_edit(edit_menu, ts("Copy"), "copy:", "c")
                                add_standard_edit(edit_menu, ts("Paste"), "paste:", "v")
                                edit_menu.addItem_(NSMenuItem.separatorItem())
                                add_standard_edit(edit_menu, ts("Select All"), "selectAll:", "a")
                                find_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Find", None, "")
                                find_menu = NSMenu.alloc().initWithTitle_("Find")
                                edit_menu.addItem_(find_menu_item)
                                edit_menu.setSubmenu_forItem_(find_menu, find_menu_item)
                                find_action = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Find...", "performFindPanelAction:", "f")
                                find_action.setTag_(1)
                                find_menu.addItem_(find_action)
                                find_next = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Find Next", "performFindPanelAction:", "g")
                                find_next.setTag_(2)
                                find_menu.addItem_(find_next)
                                find_prev = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Find Previous", "performFindPanelAction:", "G")
                                find_prev.setTag_(3)
                                find_menu.addItem_(find_prev)
                                edit_menu_item.setSubmenu_(edit_menu)

                                shortcuts_menu = NSMenu.alloc().initWithTitle_(ts("Shortcuts"))
                                shortcuts_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(ts("Shortcuts"), None, "")
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
                                        item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(p["message"], objc.selector(self.shortcut_, signature=b"v@:@"), "")
                                        item.setTarget_(self)
                                        self.shortcut_options.append((shortcuts_menu, item))
                                        shortcuts_menu.addItem_(item)
                                    shortcuts_menu.addItem_(NSMenuItem.separatorItem())
                                self.shortcut_options.append((shortcuts_menu, add_menu_item(shortcuts_menu, ts("Open Shortcuts Menu"), "shortcutmenu_")))

                                options_menu = NSMenu.alloc().initWithTitle_(ts("Options"))
                                options_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(ts("Options"), None, "")
                                self.top_menu.addItem_(options_menu_item)
                                self.top_menu.setSubmenu_forItem_(options_menu, options_menu_item)
                                add_menu_item(options_menu, ts("Clear Debug Window Logs"), "clearLogs_")
                                add_menu_item(options_menu, ts("Force Load Debug Window Logs"), "forceLoadLogs_")
                                if gui_app_lock and gui_app_lock.exists(): add_menu_item(options_menu, ts("Unlock App Lock"), "unlockAppLock_")
                                add_menu_item(options_menu, ts("Close App"), "closeApp_")

                                view_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("View", None, "")
                                self.top_menu.addItem_(view_menu_item)
                                view_menu = NSMenu.alloc().initWithTitle_("View")
                                view_menu_item.setSubmenu_(view_menu)

                                window_menu_item = NSMenuItem.alloc().init()
                                self.top_menu.addItem_(window_menu_item)
                                window_menu = NSMenu.alloc().initWithTitle_("Window")
                                window_menu_item.setSubmenu_(window_menu)
                                NSApp.setWindowsMenu_(window_menu)

                                help_menu = NSMenu.alloc().initWithTitle_("Help")
                                help_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Help", None, "")
                                self.top_menu.addItem_(help_menu_item)
                                self.top_menu.setSubmenu_forItem_(help_menu, help_menu_item)
                                add_menu_item(help_menu, ts(f"{obName0()} Wiki"), "showHelpMenu_")
                                add_menu_item(help_menu, ts("GitHub Issues"), "showGitHubIssuesMenu_")
                                help_menu_item.setSubmenu_(help_menu)

                                try:
                                    if self.top_menu and self.main_menu and help_menu: NSApp().setMainMenu_(self.top_menu)
                                except Exception as e: printErrorMessage(f"Menu configuration error: \n{trace()}")
                            def generate_dock_menu(self):
                                generated_ui_options = []
                                generated_menu_items = []
                                if not self.dock_menu: self.dock_menu = NSMenu.alloc().init()
                                if not self.status_item:
                                    self.status_item = NSStatusBar.systemStatusBar().statusItemWithLength_(NSVariableStatusItemLength)
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
                                    menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(title, action + ":", "")
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
                                self.dock_menu.addItem_(NSMenuItem.separatorItem())

                                add_menu_item(self.dock_menu, ts("Open Roblox"), "runRoblox")
                                if main_config.get("EFlagRobloxStudioEnabled") == True: add_menu_item(self.dock_menu, ts("Run Roblox Studio"), "runRobloxStudio")
                                self.dock_menu.addItem_(NSMenuItem.separatorItem())
                                add_menu_item(self.dock_menu, ts("Run Fast Flags Installer"), "runFFlagInstaller")
                                add_menu_item(self.dock_menu, ts("Roblox Installer Options"), "openRobloxInstallerOptions")
                                add_menu_item(self.dock_menu, ts("End All Roblox Windows"), "endAllRoblox")
                                if main_config.get("EFlagRobloxStudioEnabled") == True: add_menu_item(self.dock_menu, ts("End All Roblox Studio Windows"), "endAllRobloxStudio")
                                if main_config.get("EFlagEnableURLQuickLaunch") == True: add_menu_item(self.dock_menu, ts("URL Quick Launch"), "urlQuickLaunch")
                                self.dock_menu.addItem_(NSMenuItem.separatorItem())
                                if len(generated_ui_options) > 0:
                                    for p in generated_ui_options:
                                        menu_item = add_menu_item(self.dock_menu, p["message"], "shortcut")
                                        self.shortcut_options.append((self.dock_menu, menu_item))
                                        generated_menu_items.append(menu_item)
                                self.shortcut_options.append((self.dock_menu, add_menu_item(self.dock_menu, ts("Open Shortcuts Menu"), "shortcutmenu")))
                                self.status_item.setMenu_(self.dock_menu)
                                NSApp().setDockMenu_(self.dock_menu)
                            
                            # OrangeBlox Management Functions
                            def new_bootstrap(self, action="", action_name=""):
                                if not (action == "") and type(action) is str:
                                    url_scheme_path = f"{orangeblox_library}/URLLaunchExchange"
                                    with open(url_scheme_path, "w", encoding="utf-8") as f: f.write(f"orangeblox://{action}?quick-action=true")
                                self.createNewTerminal()
                                if not (action_name == "") and type(action_name) is str: printMainMessage(f"Launched Bootstrap with action: {action_name}")
                                else: printMainMessage(f"Launched Bootstrap in new window!")
                            def new_bootstrap_play_roblox(self): self.new_bootstrap("continue", ts("Play Roblox"))
                            def new_bootstrap_play_roblox_studio(self): self.new_bootstrap("run-studio", ts("Run Roblox Studio"))
                            def new_bootstrap_play_multi_roblox(self): self.new_bootstrap("new", ts("Multi-Play Roblox"))
                            def new_bootstrap_play_reconnect(self): self.new_bootstrap("reconnect", ts("Connect to Existing Roblox Window"))
                            def new_bootstrap_play_reconnect_studio(self): self.new_bootstrap("reconnect-studio", ts("Connect to Existing Roblox Studio Window"))
                            def new_bootstrap_url_quick_launch(self): self.new_bootstrap("url-quick-launch", ts("URL Quick Launch"))
                            def new_bootstrap_clear_roblox_logs(self): self.new_bootstrap("clear-logs", ts("Clear Temporary Storage"))
                            def new_bootstrap_roblox_installer(self): self.new_bootstrap("roblox-installer-options", ts("Open Roblox Installer Options"))
                            def new_bootstrap_end_roblox(self): self.new_bootstrap("end-roblox", ts("End Roblox"))
                            def new_bootstrap_end_roblox_studio(self): self.new_bootstrap("end-roblox-studio", ts("End Roblox Studio"))
                            def new_bootstrap_run_fflag_installer(self): self.new_bootstrap("fflag-install", ts("Run Fast Flag Installer"))
                            def new_bootstrap_open_settings(self): self.new_bootstrap("settings", ts("Open Settings"))
                            def new_bootstrap_open_mods_manager(self): self.new_bootstrap("mods", ts("Open Mods Manager"))
                            def new_bootstrap_open_credits(self): self.new_bootstrap("credits", ts("Open Credits"))
                            def new_bootstrap_open_shortcuts(self): self.new_bootstrap("shortcuts/", ts("Open Shortcuts Menu"))
                            def startBootstrapWithoutValidation_(self, sender):
                                if not (self.validation_frame == None):
                                    self.validation_frame.removeFromSuperview()
                                    self.validation_frame = None
                                if not (self.validation_failed_window == None):
                                    self.validation_failed_window.close()
                                    self.validation_failed_window = None
                                main_config["EFlagDisableSecureHashSecurity"] = True
                                for terminal in self.active_terminals:
                                    try:
                                        if terminal.process and terminal.process.poll() is None: terminal.process.kill(); terminal.process.wait()
                                    except Exception: pass
                                    try:
                                        if terminal.window: terminal.window.performSelectorOnMainThread_withObject_waitUntilDone_("close", None, False)
                                    except Exception: pass
                                self.active_terminals = []
                                self.createNewTerminal()
                            def activate_terminal_window(self, event=""): NSApp.activateIgnoringOtherApps_(True)
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
                            def urlQuickLaunch_(self, sender): self.new_bootstrap_url_quick_launch()
                            def clearLogs_(self, sender): self.clear_logs()
                            def forceLoadLogs_(self, sender): self.force_load_logs()
                            def unlockAppLock_(self, sender): self.unlock_app_lock()
                            def closeApp_(self, sender): self.on_close()
                            def showHelpMenu_(self, sender): self.show_help_menu()
                            def showGitHubIssuesMenu_(self, sender): self.show_github_issues_menu()
                            def enterDebugWindowMode_(self, sender): self.instant_debug_window()
                            def shortcutmenu_(self, sender): self.new_bootstrap_open_shortcuts()
                            def menu_copy(self, sender): self.debug_output_area.copy_(sender)
                            def menu_cut(self, sender): pass
                            def menu_paste(self, sender): pass
                            def menu_select_all(self, sender): self.debug_output_area.selectAll_(sender)
                            def menu_undo(self, sender): self.debug_output_area.undoManager().undo()
                            def menu_redo(self, sender): self.debug_output_area.undoManager().redo()
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
                            def createNewTerminal(self):
                                new_terminal = TerminalInstance.alloc().init()
                                new_terminal.terminalAppInit()
                                pip_class.startThread(func=new_terminal.start_process, daemon=True)
                                self.active_terminals.append(new_terminal)
                            def clear_logs(self):
                                global logs
                                logs = []
                                self.debug_output_area.setEditable_(True)
                                self.debug_output_area.setString_("")
                                self.debug_output_area.setEditable_(False)
                            def force_load_logs(self): self.threadingloop_("oranges")
                            def validateMenuItem_(self, menuItem): return True
                            def unlock_app_lock(self):
                                if gui_app_lock and gui_app_lock.exists(): gui_app_lock.release()
                            def instant_debug_window(self): self.on_window_activate("openDebug")
                            def show_about_menu(self):
                                try:
                                    if hasattr(self, "about_window") and self.about_window is not None:
                                        self.about_window.makeKeyAndOrderFront_(None)
                                        self.about_window.orderFrontRegardless()
                                        return
                                    width, height = 350, 200
                                    screen_frame = NSScreen.mainScreen().frame()
                                    origin_x = (screen_frame.size.width - width) / 2
                                    origin_y = (screen_frame.size.height - height) / 2
                                    about_rect = ((origin_x, origin_y), (width, height))

                                    about_window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
                                        about_rect, 
                                        NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskMiniaturizable, 
                                        NSBackingStoreBuffered, 
                                        False
                                    )
                                    about_window.setReleasedWhenClosed_(False)
                                    about_controller = NSWindowController.alloc().initWithWindow_(about_window)
                                    about_controller.setShouldCascadeWindows_(False)
                                    about_controller.showWindow_(about_window)
                                    about_window.setDelegate_(self)
                                    about_window.setTitle_(ts(f"About {obName0()}"))
                                    about_window.setLevel_(NSModalPanelWindowLevel)
                                    about_window.center()
                                    
                                    content_view = about_window.contentView()
                                    about_frame = NSView.alloc().initWithFrame_(((0, 0), (width, height)))
                                    content_view.addSubview_(about_frame)
                                    
                                    icon_nsimage = self.app_icon
                                    icon_view = NSImageView.alloc().initWithFrame_(((140, 100), (70, 70)))
                                    icon_view.setImage_(icon_nsimage)
                                    icon_view.setImageScaling_(NSImageScaleProportionallyUpOrDown)
                                    about_frame.addSubview_(icon_view)
                                    
                                    label1 = NSTextField.alloc().initWithFrame_(((100, 70), (150, 24)))
                                    label1.setStringValue_(obName0())
                                    label1.setFont_(NSFont.boldSystemFontOfSize_(16))
                                    label1.setBezeled_(False)
                                    label1.setDrawsBackground_(False)
                                    label1.setEditable_(False)
                                    label1.setSelectable_(False)
                                    label1.setAlignment_(NSCenterTextAlignment)
                                    about_frame.addSubview_(label1)
                                    
                                    version_text = ts(f"Bootstrap Version {current_version.get('version')}\nMade by @EfazDev")
                                    version_lines = 2
                                    if obName0() != "OrangeBlox" or obName1() != "🍊":
                                        version_text += "\n" + ts(f"Custom Theme of OrangeBlox 🍊")
                                        version_lines += 1
                                    label2 = NSTextField.alloc().initWithFrame_(((50, 50-15*version_lines), (250, 20*version_lines)))
                                    label2.setStringValue_(version_text)
                                    label2.setFont_(NSFont.systemFontOfSize_(12))
                                    label2.setBezeled_(False)
                                    label2.setDrawsBackground_(False)
                                    label2.setEditable_(False)
                                    label2.setSelectable_(False)
                                    label2.setAlignment_(NSCenterTextAlignment)
                                    label2.setLineBreakMode_(NSLineBreakByWordWrapping)
                                    label2.setMaximumNumberOfLines_(version_lines)
                                    about_frame.addSubview_(label2)

                                    about_window.orderFrontRegardless()
                                    self.about_window = about_window
                                except Exception as e:
                                    printErrorMessage(f"Unable to show about menu: \n{trace()}")
                            def show_validation_failed_menu(self):
                                try:
                                    width, height = 500, 350
                                    screen_frame = NSScreen.mainScreen().frame()
                                    origin_x = (screen_frame.size.width - width) / 2
                                    origin_y = (screen_frame.size.height - height) / 2
                                    validation_rect = ((origin_x, origin_y), (width, height))

                                    self.validation_failed_window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
                                        validation_rect, 
                                        NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskMiniaturizable, 
                                        NSBackingStoreBuffered, 
                                        False
                                    )
                                    self.validation_failed_controller = NSWindowController.alloc().initWithWindow_(self.validation_failed_window)
                                    self.validation_failed_controller.setShouldCascadeWindows_(False)
                                    self.validation_failed_controller.showWindow_(self.validation_failed_window)
                                    self.validation_failed_window.setDelegate_(self)
                                    self.validation_failed_window.setTitle_(ts("Bootstrap Verification Failed"))
                                    self.validation_failed_window.setReleasedWhenClosed_(False)
                                    self.validation_failed_window.setLevel_(NSModalPanelWindowLevel)
                                    self.validation_failed_window.center()
                                    
                                    content_view = self.validation_failed_window.contentView()
                                    self.validation_frame = NSView.alloc().initWithFrame_(((0, 0), (width, height)))
                                    content_view.addSubview_(self.validation_frame)
                                    
                                    icon_nsimage = self.app_icon
                                    icon_view = NSImageView.alloc().initWithFrame_(((220, 255), (70, 70)))
                                    icon_view.setImage_(icon_nsimage)
                                    icon_view.setImageScaling_(NSImageScaleProportionallyUpOrDown)
                                    self.validation_frame.addSubview_(icon_view)
                                    
                                    label1 = NSTextField.alloc().initWithFrame_(((175, 205), (150, 30)))
                                    label1.setStringValue_(obName0())
                                    label1.setFont_(NSFont.boldSystemFontOfSize_(20))
                                    label1.setBezeled_(False)
                                    label1.setDrawsBackground_(False)
                                    label1.setEditable_(False)
                                    label1.setSelectable_(False)
                                    label1.setAlignment_(NSCenterTextAlignment)
                                    self.validation_frame.addSubview_(label1)
                                    
                                    label2 = NSTextField.alloc().initWithFrame_(((75, 105), (350, 90)))
                                    label2.setStringValue_(ts("Uh oh! There was an issue trying to validate hashes for the following files:"))
                                    label2.setFont_(NSFont.systemFontOfSize_(15))
                                    label2.setBezeled_(False)
                                    label2.setDrawsBackground_(False)
                                    label2.setEditable_(False)
                                    label2.setSelectable_(False)
                                    label2.setAlignment_(NSCenterTextAlignment)
                                    self.validation_frame.addSubview_(label2)
                                    
                                    file_list = ", ".join(unable_to_validate2)
                                    label3 = NSTextField.alloc().initWithFrame_(((75, 70), (350, 60)))
                                    label3.setStringValue_(file_list)
                                    label3.setFont_(NSFont.systemFontOfSize_(15))
                                    label3.setBezeled_(False)
                                    label3.setDrawsBackground_(False)
                                    label3.setEditable_(False)
                                    label3.setSelectable_(False)
                                    label3.setAlignment_(NSCenterTextAlignment)
                                    self.validation_frame.addSubview_(label3)
                                    
                                    button = NSButton.alloc().initWithFrame_(((150, 45), (200, 40)))
                                    button.setTitle_(ts("Continue without validation"))
                                    button.setTarget_(self)
                                    button.setAction_(objc.selector(self.startBootstrapWithoutValidation_, signature=b"v@:@"))
                                    self.validation_frame.addSubview_(button)

                                    constraints = [
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            icon_view, NSLayoutAttributeCenterX,
                                            NSLayoutRelationEqual, self.validation_frame, NSLayoutAttributeCenterX, 1, 0),
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            icon_view, NSLayoutAttributeTop,
                                            NSLayoutRelationEqual, self.validation_frame, NSLayoutAttributeTop, 1, 20),
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            icon_view, NSLayoutAttributeWidth,
                                            NSLayoutRelationEqual, None, 0, 1, 64),
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            icon_view, NSLayoutAttributeHeight,
                                            NSLayoutRelationEqual, None, 0, 1, 64),
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            label1, NSLayoutAttributeTop,
                                            NSLayoutRelationEqual, icon_view, NSLayoutAttributeBottom, 1, 20),
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            label1, NSLayoutAttributeCenterX,
                                            NSLayoutRelationEqual, self.validation_frame, NSLayoutAttributeCenterX, 1, 0),
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            label2, NSLayoutAttributeTop,
                                            NSLayoutRelationEqual, label1, NSLayoutAttributeBottom, 1, 15),
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            label2, NSLayoutAttributeCenterX,
                                            NSLayoutRelationEqual, self.validation_frame, NSLayoutAttributeCenterX, 1, 0),
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            label3, NSLayoutAttributeTop,
                                            NSLayoutRelationEqual, label2, NSLayoutAttributeBottom, 1, 15),
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            label3, NSLayoutAttributeCenterX,
                                            NSLayoutRelationEqual, self.validation_frame, NSLayoutAttributeCenterX, 1, 0),
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            button, NSLayoutAttributeTop,
                                            NSLayoutRelationEqual, label3, NSLayoutAttributeBottom, 1, 15),
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            button, NSLayoutAttributeCenterX,
                                            NSLayoutRelationEqual, self.validation_frame, NSLayoutAttributeCenterX, 1, 0),
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            button, NSLayoutAttributeWidth,
                                            NSLayoutRelationEqual, None, 0, 1, 260),
                                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                                            button, NSLayoutAttributeHeight,
                                            NSLayoutRelationEqual, None, 0, 1, 30)
                                    ]
                                    self.validation_failed_window.orderFrontRegardless()
                                    self.validation_frame.addConstraints_(constraints)
                                except Exception as e: printErrorMessage(f"Unable to show validation menu: \n{trace()}")
                            def on_window_activate(self, event):
                                try:
                                    self.requested_kill = False
                                    if not (event == "oranges"): printMainMessage(f"Window was triggered!")
                                    if event == "openDebug":
                                        self.debug_win.setTitle_(obName0())
                                        self.debug_win.setContentSize_((800, 500))
                                        self.debug_win.setOpaque_(True)
                                        self.debug_win.setAlphaValue_(1.0)
                                        self.debug_win.makeKeyAndOrderFront_(None)

                                        self.debug_holding_frame.setHidden_(False)
                                        content_view = self.debug_win.contentView()
                                        holding_frame_size = self.debug_holding_frame.frame().size
                                        content_size = content_view.frame().size
                                        new_origin_x = (content_size.width - holding_frame_size.width) / 2
                                        new_origin_y = (content_size.height - holding_frame_size.height) / 2
                                        self.debug_holding_frame.setFrameOrigin_((new_origin_x, new_origin_y))
                                        self.debug_win.displayIfNeeded()
                                        if self.debug_mode_window_enabled == False:
                                            printDebugMessage("Debug Window Mode is now enabled! Now when clicking the taskbar icon, it will show this window instead of going to the terminal directly.")
                                            if not (event == "oranges"):
                                                printSystemMessage("--- Hello Robloxian! ---")
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
                                    else: self.activate_terminal_window()
                                except Exception as e:  printErrorMessage(f"Unable to activate window: \n{trace()}")
                            def disable_debug_mode_window(self):
                                if self.debug_mode_window_enabled == True:
                                    self.debug_mode_window_enabled = False
                                    self.debug_win.setTitle_(obName0())
                                    self.debug_win.setOpaque_(False)
                                    self.debug_win.setAlphaValue_(0.0)
                                    self.debug_win.orderOut_(None)
                                    if self.top_menu_options.get(ts("Open Debug Window")): self.top_menu_options[ts("Open Debug Window")].setTitle_(ts("Open Debug Window"))
                                    if self.dock_menu_options.get(ts("Open Debug Window")): self.dock_menu_options[ts("Open Debug Window")].setTitle_(ts("Open Debug Window"))
                            def config_reload_period_func(self):
                                while True:
                                    time.sleep(20)
                                    self.refreshConfig_(None)
                            @objc.python_method
                            def get_color(self, hex_str):
                                hex_str = str(hex_str).upper()
                                r, g, b = 255, 255, 255
                                try:
                                    rgb = colors_class.hex_to_rgb(hex_str)
                                    if isinstance(rgb, (list, tuple)) and len(rgb) >= 3: r, g, b = rgb[0], rgb[1], rgb[2]
                                except Exception: pass
                                r_norm = r / 255.0
                                g_norm = g / 255.0
                                b_norm = b / 255.0
                                color = NSColor.colorWithSRGBRed_green_blue_alpha_(r_norm, g_norm, b_norm, 1.0)
                                return color
                        try:
                            app = NSApplication.sharedApplication()
                            delegate = AppDelegate.alloc().init()
                            app.setActivationPolicy_(NSApplicationActivationPolicyRegular)
                            app.activateIgnoringOtherApps_(True)
                            app.setDelegate_(delegate)
                            setattr(sys, "_app_delegate", delegate)
                            app.run()
                        except Exception as e: printErrorMessage(f"PyObjc App Failed! Error: \n{trace()}")
                    except Exception as e: printErrorMessage(f"PyObjc App Failed! Error: \n{trace()}")
                except Exception as e: printErrorMessage(str(e))
            if app_to_script_socket.exists(): app_to_script_socket.wait_till_free()
            app_to_script_socket.subscribe("OrangeBloxAppNotification", notification)
            #app_to_script_socket.subscribe("OrangeBloxEvents", eventInfo)
            app_to_script_socket.listen()
            createObjcAppReplication()
        except Exception as e:
            printErrorMessage(f"Bootstrap Run Failed: \n{trace()}")
            sys.exit(0)
    elif main_os == "Windows":
        filtered_args = ""
        loaded_json = True
        local_app_data = pip_class.getLocalAppData()
        colors_class.set_console_title(f"{obName0()} {obName1()}")
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
                pip_class.startThread(func=cool, daemon=True)

            if len(args) > 1:
                if certain_player: 
                    filtered_args = f"obx-launch-{certain_type} " + " ".join(args)
                    if os.path.exists(app_path):
                        with open(os.path.join(app_path, "URLLaunchExchange"), "w", encoding="utf-8") as f: f.write(filtered_args)
                    else:
                        with open("URLLaunchExchange", "w", encoding="utf-8") as f: f.write(filtered_args)
                else:
                    filtered_args = args[1]
                    if (("roblox-player:" in filtered_args) or ("roblox-studio:" in filtered_args) or ("roblox-studio-auth:" in filtered_args) or ("roblox:" in filtered_args) or ("efaz-bootstrap:" in filtered_args) or ("orangeblox:" in filtered_args) or os.path.isfile(filtered_args)):
                        printMainMessage(f"Creating URL Exchange file..")
                        if os.path.exists(app_path):
                            with open(os.path.join(app_path, "URLLaunchExchange"), "w", encoding="utf-8") as f: f.write(filtered_args)
                        else:
                            with open("URLLaunchExchange", "w", encoding="utf-8") as f: f.write(filtered_args)
            elif certain_player:
                filtered_args = f"obx-launch-{certain_type}"
                if os.path.exists(app_path):
                    with open(os.path.join(app_path, "URLLaunchExchange"), "w", encoding="utf-8") as f: f.write(filtered_args)
                else:
                    with open("URLLaunchExchange", "w", encoding="utf-8") as f: f.write(filtered_args)

            if main_config.get("EFlagEnableURLQuickLaunch") == True and os.path.exists(os.path.join(generateFileKey("URLQuickLaunch"))) and pip_class.getAmountOfProcesses("python") > 0:
                printMainMessage(f"Detected URL Quick Launch Attempt! Stopped App Launch.")
                sys.exit(0)

            if pip_class.getIfRunningWindowsAdmin():
                printErrorMessage(f"Please run {obName0()} under user permissions instead of running administrator!")
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
                    printErrorMessage(f"Please install Python 3.11 or later in order to use {obName0()}!")
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
                    if os.path.exists(venv_path) and not venv_class.getCurrentPythonVersion() == pip_class.getCurrentPythonVersion():
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
                    notifier = PyKits.Socket(port=61239)
                    def listener(payload):
                        if payload.get("title") and payload.get("message"): displayNotification(payload["title"], payload["message"])
                    if notifier.exists(): notifier.wait_till_free()
                    notifier.subscribe("OrangeBloxAppNotification", listener)
                    notifier.listen()
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
                        randomized_key = str(uuid.uuid4()).split("-")[0]
                        result = subprocess.run([pythonExecutable, os.path.join(app_path, "Main.py"), randomized_key], cwd=os.path.join(app_path))
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
                pip_class.startThread(func=awake, daemon=True)
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
    class OrangeBloxLoaderNotModule(Exception): pass
    raise OrangeBloxLoaderNotModule("The loader for OrangeBlox is only a runable instance, not a module.")