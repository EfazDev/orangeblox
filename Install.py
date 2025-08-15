# 
# OrangeBlox Installer 🍊
# Made by Efaz from efaz.dev
# v2.2.8
# 

# Modules
import subprocess
import traceback
import platform
import datetime
import builtins
import hashlib
import shutil
import ctypes
import time
import stat
import json
import zlib
import sys
import os

import PyKits; PyKits.BuiltinEditor(builtins)
import RobloxFastFlagsInstaller as RFFI

def ts(mes):
    mes = str(mes)
    if hasattr(sys.stdout, "translate"): mes = sys.stdout.translate(mes)
    return mes
def trace():
    _, tb_v, tb_b = sys.exc_info()
    tb_lines = traceback.extract_tb(tb_b)
    lines = []
    lines.append("\033[95mTraceback (most recent call last):\033[0m")
    for fn, ln, f, tx in tb_lines:
        lines.append(f'  File \033[95m"{fn}"\033[0m, line \033[95m{ln}\033[0m, in \033[95m{f}\033[0m')
        if tx: lines.append(f'    {tx}')
    exc_t = type(tb_v).__name__
    exc_m = str(tb_v)
    lines.append(f'\033[95m\033[1m{exc_t}:\033[0m\033[0m \033[35m{exc_m}\033[0m')
    return "\n".join(lines)
def printMainMessage(mes): print(f"\033[38;5;255m{ts(mes)}\033[0m")
def printErrorMessage(mes): print(f"\033[38;5;196m{ts(mes)}\033[0m")
def printSuccessMessage(mes): print(f"\033[38;5;82m{ts(mes)}\033[0m")
def printWarnMessage(mes): print(f"\033[38;5;202m{ts(mes)}\033[0m")
def printYellowMessage(mes): print(f"\033[38;5;226m{ts(mes)}\033[0m")
def printDebugMessage(mes): print(f"\033[38;5;226m{ts(mes)}\033[0m")

if __name__ == "__main__":
    main_os = platform.system()
    pip_class = PyKits.pip()
    requests = PyKits.request()
    plist_class = PyKits.plist()
    stored_main_app = {
        "OverallInstall": main_os == "Darwin" and pip_class.getInstallableApplicationsFolder() or f"{pip_class.getLocalAppData()}",
        "Darwin": [
            os.path.join(pip_class.getInstallableApplicationsFolder(), "OrangeBlox.app", "Contents", "MacOS", "OrangeBlox.app"), 
            os.path.join(pip_class.getInstallableApplicationsFolder(), "OrangeBlox.app"),
            os.path.join(pip_class.getInstallableApplicationsFolder(), "Play Roblox.app"),
            os.path.join(pip_class.getInstallableApplicationsFolder(), "Run Studio.app")
        ],
        "Windows": [
            os.path.join(f"{pip_class.getLocalAppData()}", "OrangeBlox"), 
            os.path.join(f"{pip_class.getLocalAppData()}", "OrangeBlox", "OrangeBlox.exe"), 
            os.path.join(f"{pip_class.getLocalAppData()}", "OrangeBlox"), 
            os.path.join(f"{pip_class.getLocalAppData()}", "OrangeBlox")
        ]
    }
    ignore_files = [
        "dist", 
        ".git",
        "build",
        "CNAME", 
        ".github",
        "LICENSE", 
        "README.md",
        ".gitignore",
        "RepairData", 
        ".DS_Store",
        "__pycache__", 
        "InstallPython.sh", 
        "InstallPython.bat",
        "Configuration.json", 
        "RobloxFastFlagLogFilesAttached.json"
    ]
    remove_found_files = [
        "dist", 
        ".git",
        "build",
        "CNAME", 
        ".github",
        "LICENSE", 
        "README.md",
        ".gitignore",
        ".DS_Store",
        "__pycache__", 
        "PlayRoblox.exe",
        "RunStudio.exe",
        "Downloads",
        "LocalStorage",
        "OTAPatchBackups",
        "RobloxPlayerInstaller.exe",
        "RobloxStudioInstaller.exe",
        "InstallPython.sh", 
        "InstallPython.bat",
    ]
    current_version = {"version": "2.2.8"}
    cur_path = os.path.dirname(os.path.abspath(__file__))
    rebuild_target = []
    repair_mode = False
    silent_mode = False
    update_mode = False
    backup_mode = False
    rebuild_mode = False
    uninstall_mode = False
    instant_install = False
    use_x86_windows = False
    repair_argv_mode = False
    full_rebuild_mode = False
    rebuild_from_source = None
    use_sudo_for_codesign = False
    use_installation_syncing = True
    remove_unneeded_messages = True
    rebuild_from_source_clang = False
    disabled_shortcuts_installation = None
    disabled_url_scheme_installation = None
    disable_remove_other_operating_systems = False
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
        "EFlagDisableDeleteOtherOSApps": "bool",
        "EFlagAvailableInstalledDirectories": "dict",
        "EFlagDisableURLSchemeInstall": "bool",
        "EFlagDisableShortcutsInstall": "bool",
        "EFlagRobloxBootstrapUpdatesAuthorizationKey": "EFlagUpdatesAuthorizationKey",
        "EFlagUpdatesAuthorizationKey": "str",
        "EFlagEnableDebugMode": "bool",
        "EFlagEnabledMods": "dict",
        "EFlagMakeMainBootstrapLogFiles": "bool",
        "EFlagUseVanillaRobloxApp": "bool",
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
        "EFlagDiscordWebhookShowPidInFooter": "bool",
        "EFlagForceReconnectOnStudioLost": "bool",
        "EFlagShowRunningAccountNameInTitle": "bool",
        "EFlagShowRunningGameInTitle": "bool",
        "EFlagShowDisplayNameInTitle": "bool",
        "EFlagSimplifiedEfazRobloxBootstrapPromptUI": "bool",
        "EFlagSkipEfazRobloxBootstrapPromptUI": "bool",
        "EFlagDisableBootstrapChecks": "bool",
        "EFlagDisablePythonUpdateChecks": "bool",
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
        "EFlagDisableEfazRobloxBootstrapAPIReplication": "bool",
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
        "EFlagUseEfazDevAPI": "bool"
    }
    handler = RFFI.Handler()

    def ignore_files_func(dir, files): return set(ignore_files) & set(files)
    def isYes(text): return text.lower() == "y" or text.lower() == "yes" or text.lower() == "true" or text.lower() == "t"
    def isNo(text): return text.lower() == "n" or text.lower() == "no" or text.lower() == "false" or text.lower() == "f"
    def isRequestClose(text): return text.lower() == "exit" or text.lower() == "exit()"
    def makedirs(a): os.makedirs(a,mode=511,exist_ok=True)
    def copyTreeWithSymlinks(src, dest, ignore_files=[]):
        if os.path.exists(src):
            try:
                for i in ignore_files:
                    if i in src: return
                if os.path.lexists(dest):
                    if os.path.isdir(dest) and not os.path.islink(dest): pass
                    else: os.remove(dest)
                if os.path.islink(src): os.symlink(os.readlink(src), dest)
                elif os.path.isdir(src):
                    makedirs(dest)
                    for item in os.listdir(src):
                        if item in ignore_files: continue
                        copyTreeWithSymlinks(os.path.join(src, item), os.path.join(dest, item))
                    os.chmod(dest, os.stat(src).st_mode)
                    os.chmod(dest, os.stat(dest).st_mode | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)
                else:
                    shutil.copy(src, dest)
                    os.chmod(dest, os.stat(src).st_mode)
                    os.chmod(dest, os.stat(dest).st_mode | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)
            except Exception as e: printDebugMessage(f"An error occurred while transferring a file, a reinstallation may be needed: {str(e)}")
    def getOriginalInstalledAppPath():
        if main_os == "Darwin":
            macos_preference_expected = os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.robloxbootstrap.plist")
            if os.path.exists(macos_preference_expected):
                plist_info = plist_class.readPListFile(macos_preference_expected)
                if plist_info: return plist_info.get("InstalledAppPath", None), None
                else: return None, None
            else: return None, None
        elif main_os == "Windows":
            try:
                reg_key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, r"SOFTWARE\\EfazRobloxBootstrap")
                value_data, _ = win32api.RegQueryValueEx(reg_key, "InstalledAppPath")
                win32api.RegCloseKey(reg_key)
                if value_data and type(value_data) is str: return value_data, pip_class.getLocalAppData()
                else: return None, None
            except Exception as e: return None, None
    def getSettings(directory=""):
        if main_os == "Darwin":
            if os.path.exists(os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.robloxbootstrap.plist")): os.remove(os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.robloxbootstrap.plist"))
            macos_preference_expected = os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.orangeblox.plist")
            if os.path.exists(macos_preference_expected):
                app_configuration = plist_class.readPListFile(macos_preference_expected)
                if app_configuration.get("Configuration"): main_config = app_configuration.get("Configuration")
                else:
                    with open(os.path.join(cur_path, "Configuration.json")) as f: main_config = json.load(f)
            else:
                with open(os.path.join(cur_path, "Configuration.json")) as f: main_config = json.load(f)
        else:
            try:
                with open(directory, "rb") as f: obfuscated_json = f.read()
                try: obfuscated_json = json.loads(obfuscated_json)
                except Exception as e: obfuscated_json = json.loads(zlib.decompress(obfuscated_json).decode("utf-8"))
                main_config = obfuscated_json
            except Exception as e:
                with open(os.path.join(cur_path, "Configuration.json")) as f: main_config = json.load(f)
        if main_config.get("EFlagUseConfigurationWebServer") == True and main_config.get("EFlagConfigurationWebServerURL"):
            try:
                req = requests.get(main_config.get("EFlagConfigurationWebServerURL") + requests.format_params({"script": "installer"}), headers={"X-Bootstrap-Version": current_version["version"], "X-Python-Version": platform.python_version(), "X-Authorization-Key": main_config.get("EFlagConfigurationAuthorizationKey", "")})
                if req.ok: 
                    for i, v in req.json.items():
                        if flag_types.get(i) == "path": continue
                        else: main_config[i] = v
            except: pass
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
    def saveSettings(main_config, directory=""):
        respo = {
            "saved_normally": False,
            "sync_success": False
        }
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
        if not (main_config.get("EFlagDisableAutosaveToInstallation") == True) and (main_config.get("EFlagOrangeBloxSyncDir") and os.path.exists(main_config.get("EFlagOrangeBloxSyncDir"))):
            if os.path.exists(os.path.join(main_config.get("EFlagOrangeBloxSyncDir"), 'FastFlagConfiguration.json')):
                with open(os.path.join(main_config.get("EFlagOrangeBloxSyncDir"), 'FastFlagConfiguration.json'), "w", encoding="utf-8") as f: json.dump(main_config, f, indent=4)
                respo["sync_success"] = True
            elif os.path.exists(os.path.join(main_config.get("EFlagOrangeBloxSyncDir"), 'Configuration.json')):
                with open(os.path.join(main_config.get("EFlagOrangeBloxSyncDir"), 'Configuration.json'), "w", encoding="utf-8") as f: json.dump(main_config, f, indent=4)
                respo["sync_success"] = True
            else:
                printErrorMessage("Bootstrap Sync is not supported since the original unextracted directory is not found.")
        if main_os == "Darwin":
            if os.path.exists(os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.robloxbootstrap.plist")): os.remove(os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.robloxbootstrap.plist"))
            macos_preference_expected = os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.orangeblox.plist")
            if os.path.exists(macos_preference_expected): app_configuration = plist_class.readPListFile(macos_preference_expected)
            else: app_configuration = {}
            app_configuration["Configuration"] = main_config
            plist_class.writePListFile(macos_preference_expected, app_configuration, binary=True)
        else:
            data_in_string = zlib.compress(json.dumps(main_config).encode('utf-8'))
            with open(directory, "wb") as f: f.write(data_in_string)
        if main_config.get("EFlagUseConfigurationWebServer") == True and main_config.get("EFlagConfigurationWebServerURL"):
            req = requests.post(main_config.get("EFlagConfigurationWebServerURL") + requests.format_params({"script": "installer"}), main_config, headers={"X-Bootstrap-Version": current_version["version"], "X-Python-Version": platform.python_version(), "X-Authorization-Key": main_config.get("EFlagConfigurationAuthorizationKey", "")})
            if not req.ok: respo["saved_normally"] = False
        respo["saved_normally"] = True
        return respo
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
    def getInstalledAppPath():
        if main_os == "Darwin":
            macos_preference_expected = os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.orangeblox.plist")
            if os.path.exists(macos_preference_expected):
                plist_info = plist_class.readPListFile(macos_preference_expected)
                if plist_info: return plist_info.get("InstalledAppPath", pip_class.getInstallableApplicationsFolder()), pip_class.getInstallableApplicationsFolder()
                else: return pip_class.getInstallableApplicationsFolder(), pip_class.getInstallableApplicationsFolder()
            else: return pip_class.getInstallableApplicationsFolder(), pip_class.getInstallableApplicationsFolder()
        elif main_os == "Windows":
            try:
                reg_key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, r"SOFTWARE\\OrangeBlox")
                value_data, _ = win32api.RegQueryValueEx(reg_key, "InstalledAppPath")
                win32api.RegCloseKey(reg_key)
                if value_data and type(value_data) is str:
                    if os.path.exists(os.path.join(value_data, "OrangeBlox")): return os.path.join(value_data, "OrangeBlox"), pip_class.getLocalAppData()
                    else: return value_data, pip_class.getLocalAppData()
                else: return pip_class.getLocalAppData(), pip_class.getLocalAppData()
            except Exception as e: return pip_class.getLocalAppData(), pip_class.getLocalAppData()
    def setInstalledAppPath(install_app_path):
        if main_os == "Darwin":
            if os.path.exists(os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.robloxbootstrap.plist")): os.remove(os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.robloxbootstrap.plist"))
            macos_preference_expected = os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.orangeblox.plist")
            plist_info = {}
            if os.path.exists(macos_preference_expected): plist_info = plist_class.readPListFile(macos_preference_expected)
            plist_info["InstalledAppPath"] = install_app_path
            plist_class.writePListFile(macos_preference_expected, plist_info, binary=True)
        elif main_os == "Windows":
            app_key = r"Software\EfazRobloxBootstrap"
            uninstall_key = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\EfazRobloxBootstrap"
            try:
                win32api.RegDeleteKey(win32con.HKEY_CURRENT_USER, uninstall_key)
                win32api.RegDeleteKey(win32con.HKEY_CURRENT_USER, app_key)
            except Exception: pass
            try:
                reg_key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, r"SOFTWARE\\OrangeBlox")
                win32api.RegSetValueEx(reg_key, "InstalledAppPath", 0, win32con.REG_SZ, install_app_path)
                win32api.RegCloseKey(reg_key)
            except Exception as e: printErrorMessage("There was an error saving the assigned installed path!")
    def formatSize(size_bytes):
        if size_bytes == 0: return "0 Bytes"
        size_units = ["Bytes", "KB", "MB", "GB", "TB"]
        unit_index = 0
        while size_bytes >= 1024 and unit_index < len(size_units) - 1:
            size_bytes /= 1024
            unit_index += 1
        return f"{size_bytes:.2f} {size_units[unit_index]}"
    def getFolderSize(folder_path, formatWithAbbreviation=True):
        total_size = 0
        stack = [folder_path]
        while stack:
            current = stack.pop()
            try:
                with os.scandir(current) as it:
                    for entry in it:
                        try:
                            if entry.is_file(follow_symlinks=False): total_size += entry.stat(follow_symlinks=False).st_size
                            elif entry.is_dir(follow_symlinks=False): stack.append(entry.path)
                        except Exception: pass
            except Exception: pass
        if formatWithAbbreviation == True: return formatSize(total_size)
        else: return total_size
    def convertPythonExecutablesInFileToPaths(path: str, python_instance: PyKits.pip):
        splits = os.path.basename(path).split(".")
        with open(path, "r", encoding="utf-8") as f: fi = f.read()
        if main_os == "Darwin":
            fi = fi.replace("pyinstaller ", f'\"{os.path.join(os.path.dirname(python_instance.executable), "pyinstaller")}\" ')
            if "OrangeBloxMacIntel" in fi and "nuitka" in fi and platform.machine() == "arm64": fi = fi.replace("python3 -m nuitka", "arch -x86_64 python3 -m nuitka", 1)
            fi = fi.replace("python3 ", f'\"{python_instance.executable}\" ')
        else:
            pos = os.path.join(pip_class.getLocalAppData(), "..", "Roaming", "Python", os.path.basename(os.path.dirname(python_instance.executable)))
            if os.path.exists(pos) and os.path.exists(os.path.join(pos, "Scripts", "pyinstaller.exe")): fi = fi.replace("pyinstaller ", f'\"{os.path.realpath(os.path.join(pos, "Scripts", "pyinstaller.exe"))}\" ')
            else: fi = fi.replace("pyinstaller ", f'\"{os.path.realpath(os.path.join(os.path.dirname(python_instance.executable), "Scripts", "pyinstaller.exe"))}\" ')
            fi = fi.replace("python ", f'\"{os.path.join(os.path.dirname(python_instance.executable), "python.exe")}\" ')
        tar = os.path.join(os.path.dirname(path), f'{splits[0]}Converted.{splits[1]}')
        with open(tar, "w", encoding="utf-8") as f: f.write(fi)
        return tar
    def waitForInternet():
        if pip_class.getIfConnectedToInternet() == False:
            printWarnMessage("--- Waiting for Internet ---")
            printMainMessage("Please connect to your internet in order to continue! If you're connecting to a VPN, try reconnecting.")
            while pip_class.getIfConnectedToInternet() == False: time.sleep(0.05)
            return True

    if "--rebuild-mode" in sys.argv or "-r" in sys.argv:
        rebuild_mode = True
        disable_remove_other_operating_systems = True
        instant_install = True
    elif "--update-mode" in sys.argv or "-u" in sys.argv:
        silent_mode = True
        instant_install = True
        disable_remove_other_operating_systems = True
        update_mode = True
    else:
        if "--install" in sys.argv or "-i" in sys.argv: instant_install = True
        if "--silent" in sys.argv or "-s" in sys.argv:
            silent_mode = True
            def printMainMessage(mes): silent_mode = True
            def printErrorMessage(mes): print(f"\033[38;5;196m{ts(mes)}\033[0m")
            def printSuccessMessage(mes): silent_mode = True
            def printWarnMessage(mes): silent_mode = True
            def printDebugMessage(mes): silent_mode = True
        else:
            if not ("--no-clear" in sys.argv or "-nc" in sys.argv): os.system("cls" if os.name == "nt" else 'echo "\033c\033[3J"; clear')
        if "--disable-remove" in sys.argv: disable_remove_other_operating_systems = True
    if "--disable-installation-sync" in sys.argv or "-ds" in sys.argv: use_installation_syncing = False
    if "--enable-unneeded-messages" in sys.argv or "-eu" in sys.argv: remove_unneeded_messages = False
    if "--disable-url-schemes" in sys.argv or "-du" in sys.argv: disabled_url_scheme_installation = True
    if "--disable-shortcuts" in sys.argv or "-ds" in sys.argv: disabled_shortcuts_installation = True
    if "--rebuild-pyinstaller" in sys.argv or "-rp" in sys.argv: rebuild_from_source = 1
    if "--rebuild-nuitka" in sys.argv or "-rn" in sys.argv: rebuild_from_source = 2
    if "--full-rebuild" in sys.argv or "-fb" in sys.argv: full_rebuild_mode = True
    if "--uninstall-mode" in sys.argv or "-un" in sys.argv: uninstall_mode = True
    if "--repair-mode" in sys.argv or "-k" in sys.argv: repair_argv_mode = True
    if "--backup-mode" in sys.argv or "-b" in sys.argv: backup_mode = True
    if "--use-sudo-for-codesign" in sys.argv or "-s" in sys.argv: use_sudo_for_codesign = True
    if "--rebuild-clang" in sys.argv or "-rc" in sys.argv: rebuild_from_source_clang = True
    if "--use-x86-windows" in sys.argv or "-x86" in sys.argv: use_x86_windows = True

    def startMessage():
        printWarnMessage("-----------")
        printWarnMessage("Welcome to OrangeBlox Installer 🍊!")
        printWarnMessage("Made by Efaz from efaz.dev!")
        printWarnMessage(f"v{current_version['version']}")
        printWarnMessage("-----------")
        # Requirement Checks
        if waitForInternet() == True: printWarnMessage("-----------")
        if main_os == "Windows": printMainMessage(f"System OS: {main_os} ({platform.version()}) | Python Version: {pip_class.getCurrentPythonVersion()}{pip_class.getIfPythonVersionIsBeta() and ' (BETA)' or ''}")
        elif main_os == "Darwin": printMainMessage(f"System OS: {main_os} (macOS {platform.mac_ver()[0]}) | Python Version: {pip_class.getCurrentPythonVersion()}{pip_class.getIfPythonVersionIsBeta() and ' (BETA)' or ''}")
        else:
            printErrorMessage("OrangeBlox is only supported for macOS and Windows.")
            input("> ")
            sys.exit(0)
        if not pip_class.osSupported(windows_build=17763, macos_version=(10,13,0)):
            if main_os == "Windows": printErrorMessage("OrangeBlox is only supported for Windows 10.0.17763 (October 2018) or higher. Please update your operating system in order to continue!")
            elif main_os == "Darwin": printErrorMessage("OrangeBlox is only supported for macOS 10.13 (High Sierra) or higher. Please update your operating system in order to continue!")
            input("> ")
            sys.exit(0)
        if not pip_class.pythonSupported(3, 11, 0):
            if not pip_class.pythonSupported(3, 6, 0):
                printErrorMessage("Please update your current installation of Python above 3.11.0")
                input("> ")
                sys.exit(0)
            else:
                latest_python = pip_class.getLatestPythonVersion()
                printWarnMessage("--- Python Update Required ---")
                printMainMessage("Hello! In order to use OrangeBlox, you'll need to install Python 3.11 or higher in order to continue. ")
                printMainMessage(f"If you wish, you may install Python {latest_python} by typing \"y\" and continue.")
                printMainMessage("Otherwise, you may close the app by just continuing without typing.")
                if isYes(input("> ")) == True:
                    pip_class.pythonInstall(latest_python)
                    printSuccessMessage(f"If installed correctly, Python {latest_python} should be available to be used!")
                    printSuccessMessage("Please restart the script to install!")
                    input("> ")
                sys.exit(0)
    startMessage()

    if pip_class.getIfRunningWindowsAdmin():
        printWarnMessage("--- Admin Permissions Not Required ---")
        printErrorMessage("Please run OrangeBlox under user permissions instead of running administrator!")
        input("> ")
        sys.exit(0)
    try:
        pypresence = pip_class.importModule("pypresence")
        psutil = pip_class.importModule("psutil")
        if main_os == "Darwin":
            posix_ipc = pip_class.importModule("posix_ipc")
            objc = pip_class.importModule("objc")
        elif main_os == "Windows": 
            win32com = pip_class.importModule("win32com")
            plyer = pip_class.importModule("plyer")
        if rebuild_from_source == 1: rebuild_target = ["pyinstaller"]
        if rebuild_from_source == 2: rebuild_target = ["Nuitka"]
        if len(rebuild_target) > 0 and not pip_class.installed(rebuild_target, boolonly=True): raise Exception(f"Please install {rebuild_target[0]} for this mode!")
        if len(rebuild_target) > 0 and full_rebuild_mode == True: 
            def check(s): return not s.installed(rebuild_target + ["pyobjc-core", "pyobjc-framework-Quartz", "pyobjc-framework-Cocoa"] if main_os == "Darwin" else ["plyer"], boolonly=True)
            if pip_class.getArchitecture() == "arm":
                if main_os == "Windows":
                    x64_python = PyKits.pip(arch="x64")
                    if x64_python.pythonInstalled() and check(x64_python): raise Exception(f"Requesting install for x64 python!")
                    x86_python = PyKits.pip(arch="x86")
                    if x86_python.pythonInstalled() and check(x86_python): raise Exception(f"Requesting install for x86 python!")
                else:
                    intel_python = PyKits.pip(arch="intel")
                    if intel_python.pythonInstalled() and check(intel_python): raise Exception(f"Requesting install for Intel python!")
            elif pip_class.getArchitecture() == "x64":
                x86_python = PyKits.pip(arch="x86")
                if x86_python.pythonInstalled() and check(x86_python): raise Exception(f"Requesting install for x86 python!")
    except Exception as e:
        pip_class.debug = True
        if rebuild_from_source == 1: rebuild_target = ["pyinstaller"]
        if rebuild_from_source == 2: rebuild_target = ["Nuitka"]
        pip_class.install(["pypresence", "psutil"] + rebuild_target)
        if main_os == "Darwin": pip_class.install(["posix-ipc", "pyobjc-core", "pyobjc-framework-Quartz", "pyobjc-framework-Cocoa"])
        elif main_os == "Windows": pip_class.install(["pywin32", "plyer"])
        if len(rebuild_target) > 0 and full_rebuild_mode == True: 
            if pip_class.getArchitecture() == "arm":
                if main_os == "Windows":
                    x64_python = PyKits.pip(arch="x64")
                    if x64_python.pythonInstalled():
                        x64_python.debug = True
                        x64_python.install(["pypresence", "psutil"] + rebuild_target)
                        if main_os == "Darwin": x64_python.install(["posix-ipc", "pyobjc-core", "pyobjc-framework-Quartz", "pyobjc-framework-Cocoa"])
                        elif main_os == "Windows": x64_python.install(["pywin32", "plyer"])
                    x86_python = PyKits.pip(arch="x86")
                    if x86_python.pythonInstalled():
                        x86_python.debug = True
                        x86_python.install(["pypresence", "psutil"] + rebuild_target)
                        if main_os == "Darwin": x86_python.install(["posix-ipc", "pyobjc-core", "pyobjc-framework-Quartz", "pyobjc-framework-Cocoa"])
                        elif main_os == "Windows": x86_python.install(["pywin32", "plyer"])
                else:
                    intel_python = PyKits.pip(arch="intel")
                    if intel_python.pythonInstalled():
                        intel_python.debug = True
                        intel_python.install(["pypresence", "psutil"] + rebuild_target)
                        if main_os == "Darwin": intel_python.install(["posix-ipc", "pyobjc-core", "pyobjc-framework-Quartz", "pyobjc-framework-Cocoa"])
                        elif main_os == "Windows": intel_python.install(["pywin32", "plyer"])
            elif pip_class.getArchitecture() == "x64":
                x86_python = PyKits.pip(arch="x86")
                if x86_python.pythonInstalled():
                    x86_python.debug = True
                    x86_python.install(["pypresence", "psutil"] + rebuild_target)
                    if main_os == "Darwin": x86_python.install(["posix-ipc", "pyobjc-core", "pyobjc-framework-Quartz", "pyobjc-framework-Cocoa"])
                    elif main_os == "Windows": x86_python.install(["pywin32", "plyer"])
        os.system("cls" if os.name == "nt" else 'echo "\033c\033[3J"; clear')
        pip_class.restartScript("Install.py", sys.argv)
    
    # Python Modules (Pypi Installed)
    import psutil
    if main_os == "Windows":
        import win32com.client as win32client # type: ignore
        import win32api # type: ignore
        import win32con # type: ignore

    virutal_memory = psutil.virtual_memory()
    cpu_percent = psutil.cpu_percent(interval=0.1)
    printMainMessage(f"CPU Percentage: {round(cpu_percent, 2)}% | Memory Usage: {formatSize(virutal_memory.total-virutal_memory.available)}/{formatSize(virutal_memory.total)}")
    
    expected_app_path, default_app_path = getInstalledAppPath()
    expected_app_paths = {}
    org_expected_app_path, org_default_app_path = getOriginalInstalledAppPath()
    if org_expected_app_path:
        expected_app_paths["OverallInstall"] = org_expected_app_path
        if main_os == "Darwin":
            expected_app_paths["Darwin"] = [
                os.path.join(org_expected_app_path, "OrangeBlox.app/Contents/MacOS/OrangeBlox.app"), 
                os.path.join(org_expected_app_path, "OrangeBlox.app"), 
                os.path.join(org_expected_app_path, "Play Roblox.app"), 
                os.path.join(org_expected_app_path, "Run Studio.app")
            ]
        elif main_os == "Windows":
            expected_app_paths["Windows"] = [
                os.path.join(org_expected_app_path), 
                os.path.join(org_expected_app_path, "OrangeBlox.exe"), 
                os.path.join(org_expected_app_path), 
                os.path.join(org_expected_app_path)
            ]
    else:
        if expected_app_path:
            expected_app_paths["OverallInstall"] = expected_app_path
            if main_os == "Darwin":
                expected_app_paths["Darwin"] = [
                    os.path.join(expected_app_path, "OrangeBlox.app/Contents/MacOS/OrangeBlox.app"), 
                    os.path.join(expected_app_path, "OrangeBlox.app"), 
                    os.path.join(expected_app_path, "Play Roblox.app"), 
                    os.path.join(expected_app_path, "Run Studio.app")
                ]
            elif main_os == "Windows":
                expected_app_paths["Windows"] = [
                    os.path.join(expected_app_path), 
                    os.path.join(expected_app_path, "OrangeBlox.exe"), 
                    os.path.join(expected_app_path), 
                    os.path.join(expected_app_path)
                ]
        else: expected_app_paths = stored_main_app
    RFFI.orangeblox_mode = True
    if expected_app_path and (main_os == "Darwin" and os.path.exists(os.path.join(expected_app_paths[main_os][1], "Contents", "Resources", "Versions")) or os.path.exists(os.path.join(expected_app_paths[main_os][0], "Versions"))):
        versions_folder = os.path.join(expected_app_paths[main_os][0], "Versions")
        if main_os == "Darwin": versions_folder = os.path.join(expected_app_paths[main_os][1], "Contents", "Resources", "Versions")
        main_config = getSettings(directory=os.path.join(expected_app_paths[main_os][0], "Configuration.json"))
        RFFI.windows_versions_dir = versions_folder
        RFFI.windows_player_folder_name = main_config.get("EFlagBootstrapRobloxInstallFolderName", "com.roblox.robloxplayer")
        RFFI.windows_studio_folder_name = main_config.get("EFlagBootstrapRobloxStudioInstallFolderName", "com.roblox.robloxstudio")
        if not os.path.exists(os.path.join(versions_folder, 'DisableRobloxOverlapping')) and main_os == "Darwin":
            user_folder_name = os.path.basename(os.path.expanduser("~"))
            versions_folder = os.path.join(versions_folder, user_folder_name)
            RFFI.macOS_dir = os.path.join(versions_folder, "Roblox.app")
            RFFI.macOS_studioDir = os.path.join(versions_folder, "Roblox Studio.app")
            RFFI.macOS_installedPath = os.path.join(versions_folder)
        else:
            RFFI.macOS_dir = os.path.join(versions_folder, "Roblox.app")
            RFFI.macOS_studioDir = os.path.join(versions_folder, "Roblox Studio.app")
            RFFI.macOS_installedPath = os.path.join(versions_folder)
        installed_roblox_version = handler.getCurrentClientVersion()
        if installed_roblox_version["success"] == True:
            installed_roblox_studio_version = handler.getCurrentClientVersion(studio=True)
            if installed_roblox_studio_version["success"] == True:
                if installed_roblox_studio_version['version'] == installed_roblox_version['version']: printMainMessage(f"Current Roblox & Roblox Studio Version: {installed_roblox_version['version']}")
                else:
                    printMainMessage(f"Current Roblox Version: {installed_roblox_version['version']}")
                    printMainMessage(f"Current Roblox Studio Version: {installed_roblox_studio_version['version']}")
            else: printMainMessage(f"Current Roblox Version: {installed_roblox_version['version']}")
    printMainMessage(f"Installation Folder: {cur_path}")
    overwrited = False

    if os.path.exists(expected_app_paths[main_os][0]) and os.path.exists(expected_app_paths[main_os][1]):
        overwrited = True
        stored_main_app = expected_app_paths
    elif os.path.exists(os.path.join(expected_app_paths["OverallInstall"], "EfazRobloxBootstrap")) or os.path.exists(os.path.join(expected_app_paths["OverallInstall"], "EfazRobloxBootstrap.app")):
        overwrited = True
        stored_main_app = expected_app_paths
    def install():
        global disabled_url_scheme_installation
        global use_x86_windows
        global rebuild_from_source
        global rebuild_from_source_clang
        global disable_remove_other_operating_systems
        global disabled_shortcuts_installation
        global use_installation_syncing
        global rebuild_target
        started_build_time = datetime.datetime.now().timestamp()
        if os.path.exists(os.path.join(cur_path, "Apps")):
            if main_os == "Darwin":
                # Get FastFlagConfiguration.json Data
                if overwrited == True:
                    printMainMessage("Getting Configuration File Data..")
                    fast_config_path = os.path.join(stored_main_app[main_os][1], "Contents", "Resources", "FastFlagConfiguration.json")
                    if os.path.exists(os.path.join(stored_main_app["OverallInstall"], "EfazRobloxBootstrap.app")): fast_config_path = os.path.join(stored_main_app["OverallInstall"], "EfazRobloxBootstrap.app", "Contents", "Resources", "FastFlagConfiguration.json")
                    if os.path.exists(fast_config_path):
                        with open(fast_config_path, "r", encoding="utf-8") as f: main_config = json.load(f)
                    else: main_config = getSettings(directory=fast_config_path)
                else:
                    main_config = {}
                    if os.path.exists(os.path.join(cur_path, "FastFlagConfiguration.json")):
                        with open(os.path.join(cur_path, "FastFlagConfiguration.json"), "r", encoding="utf-8") as f: main_config = json.load(f)

                # Adapt Fast Flags from Efaz's Roblox Bootstrap
                if not main_config.get("EFlagRobloxPlayerFlags"):
                    printMainMessage("Converting Fast Flags..")
                    player_flags = {}
                    for i, v in main_config.items():
                        if not i.startswith("EFlag"): player_flags[i] = v
                    for i, v in player_flags.items(): main_config.pop(i)
                    main_config["EFlagRobloxPlayerFlags"] = player_flags
                    main_config["EFlagRobloxStudioFlags"] = {}

                # Rebuild Clang Apps from Source
                if rebuild_from_source_clang == True or (main_config.get("EFlagRebuildClangAppFromSourceDuringUpdates") == True and update_mode == True):
                    printMainMessage("Running Clang++ Rebuild..")
                    extra_detail = []
                    if use_sudo_for_codesign == True: extra_detail = []
                    if os.path.exists(os.path.join(cur_path, "SigningCertificateName")): 
                        with open(os.path.join(cur_path, "SigningCertificateName")) as f: extra_detail.append("'" + f.read() + "'")
                    pa = convertPythonExecutablesInFileToPaths(os.path.join(cur_path, 'Apps', 'Scripts', 'Clang', 'MakeLoadersMac.sh') if platform.machine() == "arm64" else os.path.join(cur_path, 'Apps', 'Scripts', 'Clang', 'MakeLoadersMacIntel.sh'), pip_class)
                    rebuild_status = subprocess.run(["/bin/sh", pa] + extra_detail, cwd=cur_path)
                    if rebuild_status.returncode == 0:
                        printSuccessMessage(f"Rebuilding Clang App succeeded! Continuing to installation..")
                        os.remove(pa)
                    else:
                        printErrorMessage(f"Rebuild failed! Status code: {rebuild_status.returncode}")
                        os.remove(pa)
                        return

                # Rebuild Pyinstaller & Nuitka Apps
                if rebuild_from_source == 1 or (main_config.get("EFlagRebuildPyinstallerAppFromSourceDuringUpdates") == True and update_mode == True):
                    extra_detail = []
                    if use_sudo_for_codesign == True: extra_detail = []
                    if os.path.exists(os.path.join(cur_path, "SigningCertificateName")): 
                        with open(os.path.join(cur_path, "SigningCertificateName")) as f: extra_detail = extra_detail.append("'" + f.read() + "'")
                    printMainMessage("Running Pyinstaller Rebuild..")
                    pa = convertPythonExecutablesInFileToPaths(os.path.join(cur_path, 'Apps', 'Scripts', 'Pyinstaller', 'RecreateMacOS.sh') if platform.machine() == "arm64" else os.path.join(cur_path, 'Apps', 'Scripts', 'Pyinstaller', 'RecreateMacOSIntel.sh'), pip_class)
                    rebuild_status = subprocess.run(["/bin/sh", pa] + extra_detail, cwd=cur_path)
                    if rebuild_status.returncode == 0:
                        printSuccessMessage(f"Rebuilding Pyinstaller App succeeded! Continuing to installation..")
                        os.remove(pa)
                    else:
                        printErrorMessage(f"Rebuild failed! Status code: {rebuild_status.returncode}")
                        os.remove(pa)
                        return
                    if full_rebuild_mode == True and platform.machine() == "arm64":
                        printMainMessage("Running Intel Pyinstaller Rebuild..")
                        pa = convertPythonExecutablesInFileToPaths(os.path.join(cur_path, 'Apps', 'Scripts', 'Pyinstaller', 'RecreateMacOSIntel.sh'), pip_class)
                        rebuild_status = subprocess.run(["/bin/sh", pa] + extra_detail, cwd=cur_path)
                        if rebuild_status.returncode == 0: printSuccessMessage(f"Rebuilding Intel Pyinstaller App succeeded! Continuing to installation..")
                        else: printErrorMessage(f"Rebuild failed! Status code: {rebuild_status.returncode}")
                        os.remove(pa)
                elif rebuild_from_source == 2 or (main_config.get("EFlagRebuildNuitkaAppFromSourceDuringUpdates") == True and update_mode == True):
                    extra_detail = []
                    if use_sudo_for_codesign == True: extra_detail = []
                    if os.path.exists(os.path.join(cur_path, "SigningCertificateName")): 
                        with open(os.path.join(cur_path, "SigningCertificateName")) as f: extra_detail.append("'" + f.read() + "'")
                    printMainMessage("Running Nuitka Rebuild..")
                    pa = convertPythonExecutablesInFileToPaths(os.path.join(cur_path, 'Apps', 'Scripts', 'Nuitka', 'RecreateMacOS.sh') if platform.machine() == "arm64" else os.path.join(cur_path, 'Apps', 'Scripts', 'Pyinstaller', 'RecreateMacOSIntel.sh'), pip_class)
                    rebuild_status = subprocess.run(["/bin/sh", pa] + extra_detail, cwd=cur_path)
                    if rebuild_status.returncode == 0:
                        printSuccessMessage(f"Rebuilding Nuitka App succeeded! Continuing to installation..")
                        os.remove(pa)
                    else:
                        printErrorMessage(f"Rebuild failed! Status code: {rebuild_status.returncode}")
                        os.remove(pa)
                        return
                    if full_rebuild_mode == True and platform.machine() == "arm64":
                        printMainMessage("Running Intel Nuitka Rebuild..")
                        pa = convertPythonExecutablesInFileToPaths(os.path.join(cur_path, 'Apps', 'Scripts', 'Nuitka', 'RecreateMacOSIntel.sh'), pip_class)
                        rebuild_status = subprocess.run(["/bin/sh", pa] + extra_detail, cwd=cur_path)
                        if rebuild_status.returncode == 0: printSuccessMessage(f"Rebuilding Intel Nuitka App succeeded! Continuing to installation..")
                        else: printErrorMessage(f"Rebuild failed! Status code: {rebuild_status.returncode}")
                        os.remove(pa)

                if platform.machine() == "arm64":
                    if os.path.exists(os.path.join(cur_path, "Apps", "OrangeBloxMac.zip")):
                        # Unzip Installation ZIP
                        printMainMessage("Unzipping Installation ZIP File..")
                        try: zip_extract = pip_class.unzipFile(f'{cur_path}/Apps/OrangeBloxMac.zip', f'{cur_path}/Apps/OrangeBloxMac/', ["OrangeBlox.app", "OrangePlayRoblox.app", "OrangeRunStudio.app"])
                        except Exception as e: printErrorMessage(f"Something went wrong while trying to unzip macOS apps file: {str(e)}")
                        time.sleep(1)
                    else: printYellowMessage("Something went wrong finding OrangeBloxMac.zip. It will require a OrangeBloxMac folder in order for installation to finish.")
                else:
                    if os.path.exists(os.path.join(cur_path, "Apps", "OrangeBloxMacIntel.zip")):
                        # Unzip Installation ZIP
                        printMainMessage("Unzipping Installation ZIP File..")
                        try: zip_extract = pip_class.unzipFile(f'{cur_path}/Apps/OrangeBloxMacIntel.zip', f'{cur_path}/Apps/OrangeBloxMac/', ["OrangeBlox.app", "OrangePlayRoblox.app", "OrangeRunStudio.app"])
                        except Exception as e: printErrorMessage(f"Something went wrong while trying to unzip macOS apps file: {str(e)}")
                        time.sleep(1)
                    else: printYellowMessage("Something went wrong finding OrangeBloxMacIntel.zip. It will require a OrangeBloxMac folder in order for installation to finish.")
                if os.path.exists(os.path.join(cur_path, "Apps", "OrangeBloxMac")):
                    # Delete Other Operating System Files
                    if not (disable_remove_other_operating_systems == True or main_config.get("EFlagDisableDeleteOtherOSApps") == True):
                        deleted_other_os = False
                        if os.path.exists(os.path.join(cur_path, "Apps", "OrangeBloxWindows.zip")):
                            os.remove(os.path.join(cur_path, "Apps", "OrangeBloxWindows.zip"))
                            deleted_other_os = True
                        if deleted_other_os == True: printMainMessage("To help save space, the script has automatically deleted files made for other operating systems!")

                    # Remove Old Versions of Loader
                    if os.path.exists(f"/Applications/EfazRobloxBootstrapLoader.app/"):
                        printMainMessage("Removing Older Versions of Bootstrap Loader..")
                        shutil.rmtree(f"/Applications/EfazRobloxBootstrapLoader.app/", ignore_errors=True)
                    elif os.path.exists(os.path.join(stored_main_app[main_os][1], "Contents", "MacOS", "OrangeBlox.app")):
                        printMainMessage("Clearing Bootstrap App..")
                        shutil.rmtree(os.path.join(stored_main_app[main_os][1], "Contents", "MacOS", "OrangeBlox.app"), ignore_errors=True)
                    
                    # Remove Installed Bootstrap
                    if os.path.exists(stored_main_app[main_os][0]):
                        try:
                            printMainMessage("Removing Installed Bootstrap..")
                            shutil.rmtree(stored_main_app[main_os][0])
                        except Exception as e: printErrorMessage("Something went wrong removing installed bootstrap!")

                    # Delete frameworks if there's extra
                    del_fram = False
                    if os.path.exists(f"{stored_main_app[main_os][1]}/Contents/MacOS/OrangeBlox.app/Contents/Frameworks/"):
                        if del_fram == False: printMainMessage("Clearing App Frameworks.."); del_fram = True
                        shutil.rmtree(f"{stored_main_app[main_os][1]}/Contents/MacOS/OrangeBlox.app/Contents/Frameworks/", ignore_errors=True)
                    if os.path.exists(f"{stored_main_app[main_os][1]}/Contents/Frameworks/"):
                        if del_fram == False: printMainMessage("Clearing App Frameworks.."); del_fram = True
                        shutil.rmtree(f"{stored_main_app[main_os][1]}/Contents/Frameworks/", ignore_errors=True)
                    if os.path.exists(f"{stored_main_app[main_os][2]}/Contents/Frameworks/"):
                        if del_fram == False: printMainMessage("Clearing App Frameworks.."); del_fram = True
                        shutil.rmtree(f"{stored_main_app[main_os][2]}/Contents/Frameworks/", ignore_errors=True)
                    if os.path.exists(f"{stored_main_app[main_os][3]}/Contents/Frameworks/"):
                        if del_fram == False: printMainMessage("Clearing App Frameworks.."); del_fram = True
                        shutil.rmtree(f"{stored_main_app[main_os][3]}/Contents/Frameworks/", ignore_errors=True)

                    # Convert All Mod Modes to Mods
                    if os.path.exists(f"{cur_path}/ModModes/"):
                        printMainMessage("Converting Mod Modes to Mods..")
                        for i in os.listdir(f"{cur_path}/ModModes/"):
                            mod_mode_path = os.path.join(f"{cur_path}/ModModes/", i)
                            if os.path.isdir(mod_mode_path):
                                if not os.path.exists(f"{cur_path}/Mods/{i}/"): makedirs(f"{cur_path}/Mods/{i}/")
                                pip_class.copyTreeWithMetadata(mod_mode_path, f"{cur_path}/Mods/{i}/", dirs_exist_ok=True)
                        shutil.rmtree(f"{cur_path}/ModModes/")
                    if os.path.exists(f"{stored_main_app[main_os][1]}/Contents/Resources/ModModes/"):
                        printMainMessage("Converting Mod Modes to Mods..")
                        for i in os.listdir(f"{stored_main_app[main_os][1]}/Contents/Resources/ModModes/"):
                            mod_mode_path = os.path.join(f"{stored_main_app[main_os][1]}/Contents/Resources/ModModes/", i)
                            if os.path.isdir(mod_mode_path):
                                if not os.path.exists(f"{stored_main_app[main_os][1]}/Contents/Resources/Mods/{i}/"): makedirs(f"{stored_main_app[main_os][1]}/Contents/Resources/Mods/{i}/")
                                pip_class.copyTreeWithMetadata(mod_mode_path, f"{stored_main_app[main_os][1]}/Contents/Resources/Mods/{i}/", dirs_exist_ok=True)
                        shutil.rmtree(f"{stored_main_app[main_os][1]}/Contents/Resources/ModModes/")
                    
                    # Install to /Applications/
                    printMainMessage("Installing to Applications Folder..")
                    copyTreeWithSymlinks(f"{cur_path}/Apps/OrangeBloxMac/OrangeLoader.app", stored_main_app[main_os][1])
                    if os.path.exists(stored_main_app[main_os][0]): copyTreeWithSymlinks(f"{cur_path}/Apps/OrangeBloxMac/OrangeBlox.app", stored_main_app[main_os][0], ignore_files=ignore_files)
                    else: copyTreeWithSymlinks(f"{cur_path}/Apps/OrangeBloxMac/OrangeBlox.app", stored_main_app[main_os][0])
                    copyTreeWithSymlinks(f"{cur_path}/Apps/OrangeBloxMac/OrangePlayRoblox.app", stored_main_app[main_os][2])
                    copyTreeWithSymlinks(f"{cur_path}/Apps/OrangeBloxMac/OrangeRunStudio.app", stored_main_app[main_os][3])

                    # Prepare Contents of .app files
                    printMainMessage("Fetching App Folder..")
                    if os.path.exists(stored_main_app[main_os][0]):
                        # Removing Python Scripts
                        if os.path.exists(f"{stored_main_app[main_os][1]}/Contents/Resources/"):
                            printMainMessage("Removing Old Scripts..")
                            resources_fold = f"{stored_main_app[main_os][1]}/Contents/Resources/"
                            for i in os.listdir(resources_fold):
                                if i.endswith(".py") and not os.path.exists(os.path.join(cur_path, i)): os.remove(f"{stored_main_app[main_os][1]}/Contents/Resources/{i}")
                            for i in remove_found_files:
                                if os.path.exists(os.path.join(resources_fold, i)):
                                    if os.path.isdir(os.path.join(resources_fold, i)): shutil.rmtree(os.path.join(resources_fold, i), ignore_errors=True)
                                    elif os.path.isfile(os.path.join(resources_fold, i)): os.remove(os.path.join(resources_fold, i))
                        if update_mode == False:
                            # Export ./ to /Contents/Resources/
                            printMainMessage("Copying Main Resources..")
                            if os.path.exists(os.path.join(stored_main_app["OverallInstall"], "EfazRobloxBootstrap.app", "Contents", "Resources")): pip_class.copyTreeWithMetadata(os.path.join(stored_main_app["OverallInstall"], "EfazRobloxBootstrap.app", "Contents", "Resources"), f"{stored_main_app[main_os][1]}/Contents/Resources/", dirs_exist_ok=True, ignore=ignore_files_func)
                            pip_class.copyTreeWithMetadata(f"{cur_path}/", f"{stored_main_app[main_os][1]}/Contents/Resources/", dirs_exist_ok=True, ignore=ignore_files_func)
                            
                        # Reduce Download Safety Measures
                        # This can prevent messages like: Apple could not verify “OrangeBlox.app” is free of malware that may harm your Mac or compromise your privacy.
                        printMainMessage("Reducing Download Safety Measures..")
                        subprocess.run(["/usr/bin/xattr", "-rd", "com.apple.quarantine", os.path.join(stored_main_app[main_os][1])], stdout=subprocess.DEVNULL)
                        subprocess.run(["/usr/bin/xattr", "-rd", "com.apple.quarantine", os.path.join(stored_main_app[main_os][2])], stdout=subprocess.DEVNULL)
                        subprocess.run(["/usr/bin/xattr", "-rd", "com.apple.quarantine", os.path.join(stored_main_app[main_os][3])], stdout=subprocess.DEVNULL)
                        
                        # Remove Apps Folder in /Contents/Resources/
                        printMainMessage("Cleaning App..")
                        if os.path.exists(os.path.join(stored_main_app[main_os][0], "Contents", "Resources", "Apps")): shutil.rmtree(os.path.join(stored_main_app[main_os][0], "Contents", "Resources", "Apps"))
                        if os.path.exists(os.path.join(stored_main_app[main_os][1], "Contents", "Resources", "Apps")): shutil.rmtree(os.path.join(stored_main_app[main_os][1], "Contents", "Resources", "Apps"))
                        if os.path.exists(os.path.join(stored_main_app[main_os][2], "Contents", "Resources", "Apps")): shutil.rmtree(os.path.join(stored_main_app[main_os][2], "Contents", "Resources", "Apps"))
                        if os.path.exists(os.path.join(stored_main_app[main_os][3], "Contents", "Resources", "Apps")): shutil.rmtree(os.path.join(stored_main_app[main_os][3], "Contents", "Resources", "Apps"))

                        # Sync Configuration Files
                        printMainMessage("Configurating App Data..")
                        if not ("OrangeBlox.app" in cur_path): main_config["EFlagOrangeBloxSyncDir"] = cur_path
                        main_config["EFlagAvailableInstalledDirectories"] = stored_main_app
                        saveSettings(main_config, directory=os.path.join(stored_main_app[main_os][1], "Contents", "Resources", "FastFlagConfiguration.json"))
                        with open(os.path.join(stored_main_app[main_os][2], "Contents", "Resources", "LocatedAppDirectory"), "w", encoding="utf-8") as f: f.write(os.path.join(stored_main_app[main_os][1], "Contents"))
                        with open(os.path.join(stored_main_app[main_os][3], "Contents", "Resources", "LocatedAppDirectory"), "w", encoding="utf-8") as f: f.write(os.path.join(stored_main_app[main_os][1], "Contents"))
                        if stored_main_app.get("OverallInstall"): setInstalledAppPath(os.path.realpath(stored_main_app.get("OverallInstall")))
                        if os.path.exists(os.path.join(stored_main_app[main_os][1], "Contents", "Resources", "FastFlagConfiguration.json")): os.remove(os.path.join(stored_main_app[main_os][1], "Contents", "Resources", "FastFlagConfiguration.json"))
                        if os.path.exists(os.path.join(stored_main_app[main_os][1], "Contents", "Resources", "Configuration.json")): os.remove(os.path.join(stored_main_app[main_os][1], "Contents", "Resources", "Configuration.json"))

                        # Handle Avatar Maps
                        map_folder_contained = []
                        avatar_editor_path = os.path.join(stored_main_app[main_os][1], "Contents", "Resources", "AvatarEditorMaps")
                        for ava_map in os.listdir(avatar_editor_path):
                            if os.path.isdir(os.path.join(avatar_editor_path, ava_map)): map_folder_contained.append(ava_map)
                        if len(map_folder_contained) > 0:
                            printMainMessage("Converting Old Avatar Maps..")
                            for ava_map_fold in map_folder_contained:
                                if os.path.exists(os.path.join(avatar_editor_path, ava_map_fold, "AvatarBackground.rbxl")): shutil.copy(os.path.join(avatar_editor_path, ava_map_fold, "AvatarBackground.rbxl"), os.path.join(avatar_editor_path, f"{ava_map_fold}.rbxl"))
                                shutil.rmtree(os.path.join(avatar_editor_path, ava_map_fold), ignore_errors=True)

                        # Handle Death Sounds
                        death_sound_folder_contained = []
                        death_sound_path = os.path.join(stored_main_app[main_os][1], "Contents", "Resources", "DeathSounds")
                        if os.path.exists(death_sound_path):
                            for death_sound in os.listdir(death_sound_path):
                                if os.path.isfile(os.path.join(death_sound_path, death_sound)): death_sound_folder_contained.append(death_sound)
                            if len(death_sound_folder_contained) > 0:
                                printMainMessage("Converting Old Death Sounds..")
                                for death_sound in death_sound_folder_contained:
                                    possible_name = death_sound.split(".")
                                    if len(possible_name) > 1: possible_name = possible_name[0]
                                    else: possible_name = death_sound
                                    makedirs(os.path.join(death_sound_path, "..", "PlayerSounds", possible_name))
                                    shutil.copy(os.path.join(death_sound_path, death_sound), os.path.join(death_sound_path, "..", "PlayerSounds", possible_name, "ouch.ogg"), follow_symlinks=False)
                                shutil.rmtree(death_sound_path, ignore_errors=True)

                        # Finalize Branding
                        if os.path.exists(os.path.join(stored_main_app["OverallInstall"], "EfazRobloxBootstrap.app", "Contents", "Resources")):
                            printMainMessage("Finalizing App Branding..")
                            shutil.rmtree(os.path.join(stored_main_app["OverallInstall"], "EfazRobloxBootstrap.app"), ignore_errors=True)

                        # Success!
                        end_build_time = datetime.datetime.now().timestamp()
                        if overwrited == True: printSuccessMessage(f"Successfully updated OrangeBlox in {round(end_build_time-started_build_time, 3)}s!")
                        else: printSuccessMessage(f"Successfully installed OrangeBlox in {round(end_build_time-started_build_time, 3)}s!")
                    else: printErrorMessage("Something went wrong trying to find the application folder.")
                    shutil.rmtree(f"{cur_path}/Apps/OrangeBloxMac/", ignore_errors=True)
                else: printErrorMessage("Something went wrong trying to find the installation folder.")
            elif main_os == "Windows":
                # Get FastFlagConfiguration.json Data
                if overwrited == True:
                    printMainMessage("Getting Configuration File Data..")
                    fast_config_path = os.path.join(f"{stored_main_app[main_os][0]}", "Configuration.json")
                    if os.path.exists(os.path.join(stored_main_app["OverallInstall"], "EfazRobloxBootstrap", "FastFlagConfiguration.json")): fast_config_path = os.path.join(stored_main_app["OverallInstall"], "EfazRobloxBootstrap", "FastFlagConfiguration.json")
                    elif os.path.exists(os.path.join(stored_main_app[main_os][0], "FastFlagConfiguration.json")): fast_config_path = os.path.join(stored_main_app[main_os][0], "FastFlagConfiguration.json")
                    main_config = getSettings(directory=fast_config_path if os.path.exists(fast_config_path) else os.path.join(cur_path, "Configuration.json"))
                else:
                    main_config = {}
                    if os.path.exists(os.path.join(cur_path, "Configuration.json")):
                        with open(os.path.join(cur_path, "Configuration.json"), "r", encoding="utf-8") as f: main_config = json.load(f)

                # Adapt Fast Flags from Efaz's Roblox Bootstrap
                if not main_config.get("EFlagRobloxPlayerFlags"):
                    printMainMessage("Converting Fast Flags..")
                    player_flags = {}
                    for i, v in main_config.items():
                        if not i.startswith("EFlag"): player_flags[i] = v
                    for i, v in player_flags.items(): main_config.pop(i)
                    main_config["EFlagRobloxPlayerFlags"] = player_flags
                    main_config["EFlagRobloxStudioFlags"] = {}

                # Rebuild Pyinstaller & Nuitka Apps
                if rebuild_from_source == 1 or (main_config.get("EFlagRebuildPyinstallerAppFromSourceDuringUpdates") == True and update_mode == True):
                    def build(arch=None):
                        build_pip_class = PyKits.pip(arch=arch)
                        if build_pip_class.pythonInstalled() and build_pip_class.installed(["pyinstaller"]):
                            target_arch = build_pip_class.getArchitecture()
                            printMainMessage(f"Running Pyinstaller Rebuild for {target_arch}..")
                            pa = convertPythonExecutablesInFileToPaths(os.path.join(cur_path, "Apps", "Scripts", "Pyinstaller", f"RecreateWindows{'32' if arch == 'x86' else ('Arm64' if arch == 'arm' else '')}.bat"), build_pip_class)
                            rebuild_status = subprocess.run([pa], cwd=cur_path)
                            os.remove(pa)
                            if rebuild_status.returncode == 0: printSuccessMessage("Pyinstaller Rebuild Success!")
                            else:
                                printErrorMessage(f"Pyinstaller Rebuild failed! Status code: {rebuild_status.returncode}")
                                return
                    build(pip_class.getArchitecture())
                    if full_rebuild_mode == True and pip_class.getArchitecture() == "arm": build("x64"); build("x86")
                    elif full_rebuild_mode == True and pip_class.getArchitecture() == "x64": build("x86")
                elif rebuild_from_source == 2 or (main_config.get("EFlagRebuildNuitkaAppFromSourceDuringUpdates") == True and update_mode == True):
                    def build(arch=None):
                        build_pip_class = PyKits.pip(arch=arch)
                        if build_pip_class.pythonInstalled() and build_pip_class.installed(["pyinstaller"]):
                            target_arch = build_pip_class.getArchitecture()
                            printMainMessage(f"Running Nuitka Rebuild for {target_arch}..")
                            pa = convertPythonExecutablesInFileToPaths(os.path.join(cur_path, "Apps", "Scripts", "Nuitka", f"RecreateWindows{'32' if arch == 'x86' else ('Arm64' if arch == 'arm' else '')}.bat"), build_pip_class)
                            rebuild_status = subprocess.run([pa], cwd=cur_path)
                            os.remove(pa)
                            if rebuild_status.returncode == 0: printSuccessMessage("Nuitka Rebuild success!")
                            else:
                                printErrorMessage(f"Nuitka Rebuild failed! Status code: {rebuild_status.returncode}")
                                return
                    build(pip_class.getArchitecture())
                    if full_rebuild_mode == True and pip_class.getArchitecture() == "arm": build("x64"); build("x86")
                    elif full_rebuild_mode == True and pip_class.getArchitecture() == "x64": build("x86")
                if os.path.exists(f"{cur_path}/Apps/OrangeBloxWindows.zip"):
                    # Unzip Installation ZIP
                    printMainMessage("Unzipping Installation ZIP File..")
                    try: zip_extract = pip_class.unzipFile(f'{cur_path}/Apps/OrangeBloxWindows.zip', f'{cur_path}/Apps/OrangeBloxWindows/', ["x86"] if pip_class.getIf32BitWindows() else ["x64", "x86"])
                    except Exception as e: printErrorMessage(f"Something went wrong while trying to unzip Windows apps file: {str(e)}")
                    time.sleep(1)
                else: printYellowMessage("Something went wrong finding OrangeBloxWindows.zip. It will require a OrangeBloxWindows folder in order for installation to finish.")
                if os.path.exists(f"{cur_path}/Apps/OrangeBloxWindows/"):
                    # Delete Other Operating System Files
                    deleted_other_os = False
                    if not (disable_remove_other_operating_systems == True or main_config.get("EFlagDisableDeleteOtherOSApps") == True):
                        if os.path.exists(os.path.join(cur_path, "/Apps/OrangeBloxMac.zip")):
                            os.remove(os.path.join(cur_path, "/Apps/OrangeBloxMac.zip"))
                            deleted_other_os = True
                        if os.path.exists(os.path.join(cur_path, "/Apps/OrangeBloxMacIntel.zip")):
                            os.remove(os.path.join(cur_path, "/Apps/OrangeBloxMacIntel.zip"))
                            deleted_other_os = True
                        if deleted_other_os == True: printMainMessage("To help save space, the script has automatically deleted files made for other operating systems!")

                    # Convert All Mod Modes to Mods
                    if os.path.exists(os.path.join(cur_path, "/ModModes/")):
                        printMainMessage("Converting Mod Modes to Mods..")
                        for i in os.listdir(os.path.join(cur_path, "/ModModes/")):
                            mod_mode_path = os.path.join(os.path.join(cur_path, "/ModModes/"), i)
                            if os.path.isdir(mod_mode_path):
                                if not os.path.exists(os.path.join(cur_path, f"/Mods/{i}/")): makedirs(os.path.join(cur_path, f"/Mods/{i}/"))
                                pip_class.copyTreeWithMetadata(mod_mode_path, f"{cur_path}/Mods/{i}/")
                        shutil.rmtree(os.path.join(cur_path, "/ModModes/"))
                    if os.path.exists(os.path.join(stored_main_app[main_os][0], "ModModes")):
                        printMainMessage("Converting Mod Modes to Mods..")
                        for i in os.listdir(os.path.join(stored_main_app[main_os][0], "ModModes")):
                            mod_mode_path = os.path.join(os.path.join(stored_main_app[main_os][0], "ModModes"), i)
                            if os.path.isdir(mod_mode_path):
                                if not os.path.exists(os.path.join(stored_main_app[main_os][0], "Mods", i)): makedirs(os.path.join(stored_main_app[main_os][0], "Mods", i))
                                pip_class.copyTreeWithMetadata(mod_mode_path, os.path.join(stored_main_app[main_os][0], "Mods", i), dirs_exist_ok=True)
                        shutil.rmtree(os.path.join(stored_main_app[main_os][0], "ModModes"))

                    # Copy Apps
                    printMainMessage("Creating paths..")
                    makedirs(stored_main_app[main_os][0])

                    # Copy EfazRobloxBootstrap
                    if os.path.exists(os.path.join(stored_main_app["OverallInstall"], "EfazRobloxBootstrap")): 
                        printMainMessage("Copying EfazRobloxBootstrap App..")
                        pip_class.copyTreeWithMetadata(os.path.join(stored_main_app["OverallInstall"], "EfazRobloxBootstrap"), stored_main_app[main_os][0], dirs_exist_ok=True, ignore=ignore_files_func)

                    # Install EXE File
                    if pip_class.getIfProcessIsOpened("OrangeBlox.exe"):
                        printMainMessage("Closing OrangeBlox executable in order to install EXE file..")
                        pip_class.endProcess("OrangeBlox.exe")
                    printMainMessage("Installing EXE File..")
                    try:
                        if pip_class.getIf32BitWindows() or use_x86_windows == True:
                            shutil.copy(os.path.join(cur_path, "Apps", "OrangeBloxWindows", "x86", "OrangeBlox.exe"), stored_main_app[main_os][1])
                            pip_class.copyTreeWithMetadata(os.path.join(cur_path, "Apps", "OrangeBloxWindows", "x86", "_internal"), os.path.join(stored_main_app[main_os][0], "_internal"), dirs_exist_ok=True, symlinks=True, ignore_if_not_exist=True)
                        else:
                            if pip_class.getIfArmWindows() and os.path.exists(os.path.join(cur_path, "Apps", "OrangeBloxWindows", "arm64", "OrangeBlox.exe")):
                                shutil.copy(os.path.join(cur_path, "Apps", "OrangeBloxWindows", "arm64", "OrangeBlox.exe"), stored_main_app[main_os][1])
                                pip_class.copyTreeWithMetadata(os.path.join(cur_path, "Apps", "OrangeBloxWindows", "arm64", "_internal"), os.path.join(stored_main_app[main_os][0], "_internal"), dirs_exist_ok=True, symlinks=True, ignore_if_not_exist=True)
                            elif os.path.exists(os.path.join(cur_path, "Apps", "OrangeBloxWindows", "x64", "OrangeBlox.exe")):
                                shutil.copy(os.path.join(cur_path, "Apps", "OrangeBloxWindows", "x64", "OrangeBlox.exe"), stored_main_app[main_os][1])
                                pip_class.copyTreeWithMetadata(os.path.join(cur_path, "Apps", "OrangeBloxWindows", "x64", "_internal"), os.path.join(stored_main_app[main_os][0], "_internal"), dirs_exist_ok=True, symlinks=True, ignore_if_not_exist=True)
                            else:
                                printErrorMessage("There was an issue trying to find the x64 version of the Windows app. Would you like to install the 32-bit version? [32-bit Python is not needed.]")
                                a = input("> ")
                                if not (a.lower() == "n"):
                                    shutil.copy(os.path.join(cur_path, "Apps", "OrangeBloxWindows", "x86", "OrangeBlox.exe"), stored_main_app[main_os][1])
                                    pip_class.copyTreeWithMetadata(os.path.join(cur_path, "Apps", "OrangeBloxWindows", "x86", "_internal"), os.path.join(stored_main_app[main_os][0], "_internal"), dirs_exist_ok=True, symlinks=True, ignore_if_not_exist=True)
                                else: sys.exit(0)
                    except Exception as e: printErrorMessage(f"There was an issue installing the EXE file: {str(e)}")

                    # Reduce Download Safety Measures
                    # This can prevent messages from Microsoft Smartscreen
                    printMainMessage("Reducing Download Safety Measures..")
                    unblock_1 = subprocess.run(["powershell", "-Command", f'Unblock-File -Path "{stored_main_app[main_os][1]}"'], shell=True, stdout=subprocess.DEVNULL)
                    if not (unblock_1.returncode == 0): printErrorMessage(f"Unable to unblock main bootstrap app: {unblock_1.returncode}")
                    
                    # Setup URL Schemes
                    if instant_install == False:
                        if not (disabled_url_scheme_installation == True):
                            printMainMessage("Setting up URL Schemes..")
                            def set_url_scheme(protocol, exe_path):
                                protocol_key = r"Software\Classes\{}".format(protocol)
                                command_key = r"Software\Classes\{}\shell\open\command".format(protocol)
                                try:
                                    key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, protocol_key)
                                    win32api.RegSetValue(key, "", win32con.REG_SZ, "URL:{}".format(protocol))
                                    win32api.RegSetValueEx(key, "URL Protocol", 0, win32con.REG_SZ, protocol)
                                    win32api.RegCloseKey(key)
                                    key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, command_key)
                                    win32api.RegSetValueEx(key, "", 0, win32con.REG_SZ, '"{}" "%1"'.format(exe_path))
                                    win32api.RegCloseKey(key)
                                    printDebugMessage(f'URL scheme "{protocol}" has been set for "{exe_path}"')
                                except Exception as e: printErrorMessage(f"An error occurred: {e}")
                            def get_file_type_reg(extension):
                                try:
                                    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, extension)
                                    file_type, _ = win32api.RegQueryValueEx(key, "")
                                    win32api.RegCloseKey(key)
                                    return file_type
                                except Exception: return None
                            def set_file_type_reg(extension, exe_path, file_type):
                                try:
                                    extension = extension if extension.startswith('.') else f'.{extension}'
                                    key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, f"Software\\Classes\\{extension}")
                                    win32api.RegSetValue(key, "", win32con.REG_SZ, file_type)
                                    win32api.RegCloseKey(key)
                                    key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, f"Software\\Classes\\{file_type}\\shell\\open\\command")
                                    win32api.RegSetValue(key, "", win32con.REG_SZ, f'"{exe_path}" "%1"')
                                    win32api.RegCloseKey(key)
                                    key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, f"Software\\Classes\\{file_type}\\DefaultIcon")
                                    win32api.RegSetValue(key, "", win32con.REG_SZ, f"{exe_path},0")
                                    win32api.RegCloseKey(key)
                                    ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x0000, None, None)
                                    printDebugMessage(f'File Handling "{extension}" has been set for "{exe_path}"')
                                except Exception as e: printErrorMessage(f"An error occurred: {e}")
                            set_url_scheme("efaz-bootstrap", stored_main_app[main_os][1])
                            set_url_scheme("orangeblox", stored_main_app[main_os][1])
                            set_url_scheme("roblox-player", stored_main_app[main_os][1])
                            set_url_scheme("roblox", stored_main_app[main_os][1])
                            set_file_type_reg(".obx", stored_main_app[main_os][1], "OrangeBlox Backup")
                            # set_file_type_reg(".rbxl", stored_main_app[main_os][1], "Roblox Place")
                            # set_file_type_reg(".rbxlx", stored_main_app[main_os][1], "Roblox Place")
                            # set_url_scheme("roblox-studio", stored_main_app[main_os][1])
                            # set_url_scheme("roblox-studio-auth", stored_main_app[main_os][1])
                    else:
                        if not (main_config.get("EFlagDisableURLSchemeInstall") == True):
                            printMainMessage("Setting up URL Schemes..")
                            def set_url_scheme(protocol, exe_path):
                                protocol_key = r"Software\Classes\{}".format(protocol)
                                command_key = r"Software\Classes\{}\shell\open\command".format(protocol)
                                try:
                                    key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, protocol_key)
                                    win32api.RegSetValue(key, "", win32con.REG_SZ, "URL:{}".format(protocol))
                                    win32api.RegSetValueEx(key, "URL Protocol", 0, win32con.REG_SZ, protocol)
                                    win32api.RegCloseKey(key)
                                    key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, command_key)
                                    win32api.RegSetValueEx(key, "", 0, win32con.REG_SZ, '"{}" "%1"'.format(exe_path))
                                    win32api.RegCloseKey(key)
                                    printDebugMessage(f'URL scheme "{protocol}" has been set for "{exe_path}"')
                                except Exception as e: printErrorMessage(f"An error occurred: {e}")
                            def get_file_type_reg(extension):
                                try:
                                    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, extension)
                                    file_type, _ = win32api.RegQueryValueEx(key, "")
                                    win32api.RegCloseKey(key)
                                    return file_type
                                except Exception: return None
                            def set_file_type_reg(extension, exe_path, file_type):
                                try:
                                    extension = extension if extension.startswith('.') else f'.{extension}'
                                    key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, f"Software\\Classes\\{extension}")
                                    win32api.RegSetValue(key, "", win32con.REG_SZ, file_type)
                                    win32api.RegCloseKey(key)
                                    key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, f"Software\\Classes\\{file_type}\\shell\\open\\command")
                                    win32api.RegSetValue(key, "", win32con.REG_SZ, f'"{exe_path}" "%1"')
                                    win32api.RegCloseKey(key)
                                    key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, f"Software\\Classes\\{file_type}\\DefaultIcon")
                                    win32api.RegSetValue(key, "", win32con.REG_SZ, f"{exe_path},0")
                                    win32api.RegCloseKey(key)
                                    ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x0000, None, None)
                                    printDebugMessage(f'File Handling "{extension}" has been set for "{exe_path}"')
                                except Exception as e: printErrorMessage(f"An error occurred: {e}")
                            set_url_scheme("efaz-bootstrap", stored_main_app[main_os][1])
                            set_url_scheme("orangeblox", stored_main_app[main_os][1])
                            set_url_scheme("roblox-player", stored_main_app[main_os][1])
                            set_url_scheme("roblox", stored_main_app[main_os][1])
                            set_file_type_reg(".obx", stored_main_app[main_os][1], "OrangeBlox Backup")
                            # set_file_type_reg(".rbxl", stored_main_app[main_os][1], "Roblox Place")
                            # set_file_type_reg(".rbxlx", stored_main_app[main_os][1], "Roblox Place")
                            # set_url_scheme("roblox-studio", stored_main_app[main_os][1])
                            # set_url_scheme("roblox-studio-auth", stored_main_app[main_os][1])

                    # Setup Shortcuts
                    if not (disabled_shortcuts_installation == True or main_config.get("EFlagDisableShortcutsInstall") == True):
                        printMainMessage("Setting up shortcuts..")
                        try:
                            def create_shortcut(target_path, shortcut_path, working_directory=None, icon_path=None, arguments=None):
                                shell = win32client.Dispatch('WScript.Shell')
                                if not os.path.exists(os.path.dirname(shortcut_path)): os.makedirs(os.path.dirname(shortcut_path),mode=511)
                                shortcut = shell.CreateShortcut(shortcut_path)
                                shortcut.TargetPath = target_path
                                if arguments: shortcut.Arguments = arguments
                                if working_directory: shortcut.WorkingDirectory = working_directory
                                if icon_path: shortcut.IconLocation = icon_path
                                shortcut.Save()
                            create_shortcut(stored_main_app[main_os][1], os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs'), "OrangeBlox.lnk"))
                            create_shortcut(stored_main_app[main_os][1], os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), "OrangeBlox.lnk"))
                            create_shortcut(stored_main_app[main_os][1], os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), "Roblox Player.lnk"), arguments="orangeblox://continue", icon_path=os.path.join(stored_main_app[main_os][0], "BootstrapImages", "AppIconPlayRoblox.ico"))
                            create_shortcut(stored_main_app[main_os][1], os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs'), 'Play Roblox.lnk'), arguments="orangeblox://continue", icon_path=os.path.join(stored_main_app[main_os][0], "BootstrapImages", "AppIconPlayRoblox.ico"))
                            create_shortcut(stored_main_app[main_os][1], os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Roblox'), 'Roblox Player.lnk'), arguments="orangeblox://continue", icon_path=os.path.join(stored_main_app[main_os][0], "BootstrapImages", "AppIconPlayRoblox.ico"))
                            create_shortcut(stored_main_app[main_os][1], os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), "Roblox Studio.lnk"), arguments="orangeblox://run-studio", icon_path=os.path.join(stored_main_app[main_os][0], "BootstrapImages", "AppIconRunStudio.ico"))
                            create_shortcut(stored_main_app[main_os][1], os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs'), 'Run Studio.lnk'), arguments="orangeblox://run-studio", icon_path=os.path.join(stored_main_app[main_os][0], "BootstrapImages", "AppIconRunStudio.ico"))
                            create_shortcut(stored_main_app[main_os][1], os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Roblox'), 'Roblox Studio.lnk'), arguments="orangeblox://run-studio", icon_path=os.path.join(stored_main_app[main_os][0], "BootstrapImages", "AppIconRunStudio.ico"))
                        except Exception as e: printYellowMessage(f"There was an issue setting shortcuts and may be caused due to OneDrive. Error: {str(e)}")

                    # Copy App Resources
                    printMainMessage("Fetching App Folder..")
                    if os.path.exists(stored_main_app[main_os][1]):
                        # Removing Python Scripts
                        if os.path.exists(stored_main_app[main_os][0]):
                            printMainMessage("Removing Old Scripts..")
                            for i in os.listdir(stored_main_app[main_os][0]):
                                if i.endswith(".py") and not os.path.exists(os.path.join(cur_path, i)): os.remove(os.path.join(stored_main_app[main_os][0], i))
                            for i in remove_found_files:
                                if os.path.exists(os.path.join(stored_main_app[main_os][0], i)):
                                    if os.path.isdir(os.path.join(stored_main_app[main_os][0], i)): shutil.rmtree(os.path.join(stored_main_app[main_os][0], i), ignore_errors=True)
                                    elif os.path.isfile(os.path.join(stored_main_app[main_os][0], i)): os.remove(os.path.join(stored_main_app[main_os][0], i))
                        if update_mode == False:
                            # Export ./ to {app_path}/
                            printMainMessage("Copying Main Resources..")
                            pip_class.copyTreeWithMetadata(cur_path, stored_main_app[main_os][0], dirs_exist_ok=True, ignore=ignore_files_func)

                        # Handle Existing Configuration Files
                        printMainMessage("Configurating App Data..")
                        if disabled_url_scheme_installation == True: main_config["EFlagDisableURLSchemeInstall"] = True
                        elif disabled_url_scheme_installation == False: main_config["EFlagDisableURLSchemeInstall"] = False
                        if disabled_shortcuts_installation == True: main_config["EFlagDisableShortcutsInstall"] = True
                        elif disabled_shortcuts_installation == False: main_config["EFlagDisableShortcutsInstall"] = False

                        if use_installation_syncing == True and not ("/Local/OrangeBlox/" in cur_path): main_config["EFlagOrangeBloxSyncDir"] = cur_path
                        main_config["EFlagAvailableInstalledDirectories"] = stored_main_app
                        data_in_string = zlib.compress(json.dumps(main_config).encode('utf-8'))
                        with open(os.path.join(f"{stored_main_app[main_os][0]}", "Configuration.json"), "wb") as f: f.write(data_in_string)
                        if os.path.exists(os.path.join(f"{stored_main_app[main_os][0]}", "FastFlagConfiguration.json")): os.remove(os.path.join(f"{stored_main_app[main_os][0]}", "FastFlagConfiguration.json"))

                        # Handle Avatar Maps
                        map_folder_contained = []
                        avatar_editor_path = os.path.join(stored_main_app[main_os][0], "AvatarEditorMaps")
                        for ava_map in os.listdir(avatar_editor_path):
                            if os.path.isdir(os.path.join(avatar_editor_path, ava_map)): map_folder_contained.append(ava_map)
                        if len(map_folder_contained) > 0:
                            printMainMessage("Converting Old Avatar Maps..")
                            for ava_map_fold in map_folder_contained:
                                if os.path.exists(os.path.join(avatar_editor_path, ava_map_fold, "AvatarBackground.rbxl")): shutil.copy(os.path.join(avatar_editor_path, ava_map_fold, "AvatarBackground.rbxl"), os.path.join(avatar_editor_path, f"{ava_map_fold}.rbxl"))
                                shutil.rmtree(os.path.join(avatar_editor_path, ava_map_fold), ignore_errors=True)

                        # Handle Death Sounds
                        death_sound_folder_contained = []
                        death_sound_path = os.path.join(stored_main_app[main_os][0], "DeathSounds")
                        if os.path.exists(death_sound_path):
                            for death_sound in os.listdir(death_sound_path):
                                if os.path.isfile(os.path.join(death_sound_path, death_sound)): death_sound_folder_contained.append(death_sound)
                            if len(death_sound_folder_contained) > 0:
                                printMainMessage("Converting Old Death Sounds..")
                                for death_sound in death_sound_folder_contained:
                                    possible_name = death_sound.split(".")
                                    if len(possible_name) > 1: possible_name = possible_name[0]
                                    else: possible_name = death_sound
                                    makedirs(os.path.join(death_sound_path, "..", "PlayerSounds", possible_name))
                                    shutil.copy(os.path.join(death_sound_path, death_sound), os.path.join(death_sound_path, "..", "PlayerSounds", possible_name, "ouch.ogg"), follow_symlinks=False)
                                shutil.rmtree(death_sound_path, ignore_errors=True)

                        # Remove Apps Folder in Installed Folder
                        if os.path.exists(os.path.join(stored_main_app[main_os][0], "Apps")):
                            printMainMessage("Cleaning App..")
                            shutil.rmtree(os.path.join(stored_main_app[main_os][0], "Apps"))

                        # Mark Installation in Windows
                        printMainMessage("Marking Program Installation into Windows..")
                        app_key = "Software\\OrangeBlox"
                        key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, app_key)
                        win32api.RegSetValueEx(key, "InstallPath", 0, win32con.REG_SZ, stored_main_app[main_os][0])
                        win32api.RegSetValueEx(key, "Installed", 0, win32con.REG_DWORD, 1)
                        win32api.RegCloseKey(key)

                        registry_path = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\OrangeBlox"
                        key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, registry_path)
                        win32api.RegSetValueEx(key, "UninstallString", 0, win32con.REG_SZ, f"{sys.executable} {os.path.join(stored_main_app[main_os][0], 'Install.py')} -un")
                        win32api.RegSetValueEx(key, "ModifyPath", 0, win32con.REG_SZ, f"{sys.executable} {os.path.join(stored_main_app[main_os][0], 'Install.py')}")
                        win32api.RegSetValueEx(key, "DisplayName", 0, win32con.REG_SZ, "OrangeBlox")
                        win32api.RegSetValueEx(key, "DisplayVersion", 0, win32con.REG_SZ, current_version["version"])
                        win32api.RegSetValueEx(key, "DisplayIcon", 0, win32con.REG_SZ, os.path.join(stored_main_app[main_os][0], "BootstrapImages", "AppIcon.ico"))
                        win32api.RegSetValueEx(key, "HelpLink", 0, win32con.REG_SZ, "https://github.com/efazdev/orangeblox")
                        win32api.RegSetValueEx(key, "URLUpdateInfo", 0, win32con.REG_SZ, "https://github.com/efazdev/orangeblox")
                        win32api.RegSetValueEx(key, "URLInfoAbout", 0, win32con.REG_SZ, "https://github.com/efazdev/orangeblox")
                        win32api.RegSetValueEx(key, "InstallLocation", 0, win32con.REG_SZ, stored_main_app[main_os][0])
                        win32api.RegSetValueEx(key, "Publisher", 0, win32con.REG_SZ, "EfazDev")
                        win32api.RegSetValueEx(key, "EstimatedSize", 0, win32con.REG_DWORD, min(getFolderSize(stored_main_app[main_os][0], formatWithAbbreviation=False) // 1024, 0xFFFFFFFF))
                        win32api.RegCloseKey(key)

                        # Finalize Branding
                        if os.path.exists(os.path.join(stored_main_app["OverallInstall"], "EfazRobloxBootstrap")):
                            printMainMessage("Finalizing App Branding..")
                            shutil.rmtree(os.path.join(stored_main_app["OverallInstall"], "EfazRobloxBootstrap"), ignore_errors=True)
                            app_key = r"Software\EfazRobloxBootstrap"
                            uninstall_key = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\EfazRobloxBootstrap"
                            try: win32api.RegDeleteKey(win32con.HKEY_CURRENT_USER, app_key)
                            except Exception: printErrorMessage(f'Registry key "{app_key}" not found.')
                            try: win32api.RegDeleteKey(win32con.HKEY_CURRENT_USER, uninstall_key)
                            except Exception: printErrorMessage(f'Registry key "{uninstall_key}" not found.')
                            try:
                                def remove_path(pat):
                                    if os.path.exists(pat): os.remove(pat)
                                remove_path(os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), "Efaz\'s Roblox Bootstrap.lnk"))
                                remove_path(os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs'), "Efaz\'s Roblox Bootstrap.lnk"))
                            except Exception as e: printErrorMessage(f"Unable to remove shortcuts: {str(e)}")

                        # Finalize App Location
                        if stored_main_app.get("OverallInstall"): setInstalledAppPath(os.path.realpath(stored_main_app.get("OverallInstall")))

                        # Success!
                        end_build_time = datetime.datetime.now().timestamp()
                        if overwrited == True: printSuccessMessage(f"Successfully updated OrangeBlox in {round(end_build_time-started_build_time, 3)}s!")
                        else: printSuccessMessage(f"Successfully installed OrangeBlox in {round(end_build_time-started_build_time, 3)}s!")
                        shutil.rmtree(f"{cur_path}/Apps/OrangeBloxWindows/", ignore_errors=True)
                    else: printErrorMessage("Something went wrong trying to find the installation folder.")
                else: printErrorMessage("Something went wrong trying to find the installation folder.")
            else: printErrorMessage("OrangeBlox is only supported for macOS and Windows.")
        else: printErrorMessage("There was an issue while finding the Apps folder for installation.")
    if silent_mode == True:
        instant_install = True
        try: install()
        except Exception as e: printErrorMessage(f"Something went wrong during installation: {str(e)}")
    else:
        if overwrited == True: printWarnMessage("--- Updater ---")
        else: printWarnMessage("--- Installer ---")
        if instant_install == True:
            try: install()
            except Exception as e: printErrorMessage(f"Something went wrong during installation: {str(e)}")
            if rebuild_mode == False: input("> ")
        else:
            printMainMessage("Welcome to OrangeBlox Installer 🍊!")
            printMainMessage("OrangeBlox is a Roblox bootstrap that allows you to add modifications to your Roblox client using files, activity tracking and Python!")
            if overwrited == False:
                printMainMessage("Before we continue to installing, you must follow this guide on how to navigate, so you can use for when you're using the bootstrap!")
                printWarnMessage("--- Step 1 ---")
                printMainMessage("First, it's important that you best understand on how the choosing works.")
                printMainMessage('Let\'s start off with a quick input! Let\'s say you want to enable this option (use the prompt here for the example), enter "y"!')
                def a():
                    b = input("> ")
                    if isYes(b) == True: return
                    else:
                        printErrorMessage("Uhm, not quite. Try again!")
                        a()
                a()
                printWarnMessage("--- Step 2 ---")
                printMainMessage("Congrats! You completed the first step!")
                printMainMessage('Now, let\'s try that again! But instead, enter "n" for you don\'t want this option!')
                def a():
                    b = input("> ")
                    if isNo(b) == True: return
                    else:
                        printErrorMessage("Uhm, not quite. Try again!")
                        a()
                a()
                printWarnMessage("--- Step 3 ---")
                printMainMessage("You're getting good at this!")
                printMainMessage('Now, let\'s learn about how you select from a list. Take the list below for an example.')
                printMainMessage("Try selecting a number that is next to that option!")
                generated_ui_options = []
                main_ui_options = {}
                generated_ui_options.append({"index": 1, "message": ts("Do jumping-jacks")})
                generated_ui_options.append({"index": 2, "message": ts("Do push-ups")})
                generated_ui_options.append({"index": 3, "message": ts("Do curl-ups")})
                generated_ui_options.append({"index": 4, "message": ts("Do weight-lifting")})
                generated_ui_options.append({"index": 5, "message": ts("Do neither")})
                generated_ui_options.append({"index": 6, "message": ts("Do all of the above")})
                generated_ui_options = sorted(generated_ui_options, key=lambda x: x["index"])
                printWarnMessage("--- Select Option ---")
                count = 1
                for i in generated_ui_options:
                    printMainMessage(f"[{str(count)}] = {i['message']}")
                    main_ui_options[str(count)] = i
                    count += 1
                def a():
                    res = input("> ")
                    if main_ui_options.get(res):
                        opt = main_ui_options[res]
                        printSuccessMessage(f"You have selected {opt.get('message')}!")
                    else:
                        printErrorMessage("Uhm, not quite an option here, try again!")
                        return a()
                a()
                printMainMessage("And now you're ready on how to navigate! You will have to repeat this again once you install it but at least you know how to do it!")
                printMainMessage("Anyway, here's some questions to answer regarding the install.")
                printMainMessage("Would you like to check for any new bootstrap updates right now? (y/n)")
                a = input("> ")
                if isYes(a) == True:
                    version_server = "https://obx.efaz.dev/Version.json"
                    if not (type(version_server) is str and version_server.startswith("https://")): version_server = "https://obx.efaz.dev/Version.json"
                    latest_vers_res = requests.get(f"{version_server}")
                    if latest_vers_res.ok:
                        latest_vers = latest_vers_res.json
                        if current_version.get("version"):
                            if current_version.get("version", "1.0.0") < latest_vers.get("latest_version", "1.0.0"):
                                download_location = latest_vers.get("download_location", "https://github.com/EfazDev/orangeblox/archive/refs/heads/main.zip")
                                printWarnMessage("--- New Bootstrap Update ---")
                                printMainMessage(f"We have detected a new version of OrangeBlox! Would you like to install it? (y/n)")
                                if download_location == "https://github.com/EfazDev/orangeblox/archive/refs/heads/main.zip":
                                    download_location = f"https://github.com/EfazDev/orangeblox/releases/download/v{latest_vers['latest_version']}/OrangeBlox-v{latest_vers['latest_version']}.zip"
                                    printSuccessMessage("✅ This version is a public update available on GitHub for viewing.")
                                    printSuccessMessage("✅ For information about this update, use this link: https://github.com/EfazDev/orangeblox/releases")
                                    printSuccessMessage(f"✅ Download Location: {download_location}")
                                elif download_location == "https://github.com/EfazDev/orangeblox/archive/refs/heads/beta.zip":
                                    download_location = f"https://github.com/EfazDev/orangeblox/releases/download/v{latest_vers['latest_version']}/OrangeBlox-v{latest_vers['latest_version']}.zip"
                                    printYellowMessage("⚠️ This version is a beta version of OrangeBlox and may cause issues with your installation.")
                                    printYellowMessage("⚠️ For information about this update, use this link to go to the EfazDev Discord server: https://discord.efaz.dev")
                                    printSuccessMessage(f"⚠️ Download Location: {download_location}")
                                elif not (main_config.get("EFlagRobloxBootstrapUpdatesAuthorizationKey", "") == ""):
                                    printYellowMessage("🔨 This version is an update configured from an organization (this may still be a modified and an unofficial OrangeBlox version.)")
                                    printYellowMessage("🔨 For information about this update, contact your administrator!")
                                    printSuccessMessage(f"🔨 Download Location: {download_location}")
                                else:
                                    printErrorMessage("❌ The download location is different from the official GitHub link!")
                                    printErrorMessage("❌ You may be downloading an unofficial OrangeBlox version! Download a copy from https://github.com/EfazDev/orangeblox!")
                                    printSuccessMessage(f"❌ Download Location: {download_location}")
                                printSuccessMessage(f"v{current_version.get('version', '1.0.0')} [Current] => v{latest_vers['latest_version']} [Latest]")
                                if isYes(input("> ")) == True:
                                    printMainMessage("Downloading latest version..")
                                    download_update = requests.download(download_location, os.path.join(cur_path, 'Update.zip'))
                                    if download_update.ok:
                                        printMainMessage("Download Success! Extracting ZIP now!")
                                        makedirs(f"{cur_path}/Update/")
                                        zip_extract = pip_class.unzipFile(os.path.join(cur_path, "Update.zip"), f"{cur_path}/Update/", ["Main.py", "RobloxFastFlagsInstaller.py", "OrangeAPI.py", "Configuration.json", "Apps"])
                                        if zip_extract.returncode == 0:
                                            printMainMessage("Extracted successfully! Installing Files!")
                                            for file in os.listdir(f"{cur_path}/Update/"):
                                                src_path = os.path.join(f"{cur_path}/Update/", file)
                                                dest_path = os.path.join(cur_path, file)
                                                if os.path.isdir(src_path): pip_class.copyTreeWithMetadata(src_path, dest_path, dirs_exist_ok=True)
                                                else:
                                                    if not file.endswith(".json"): shutil.copy2(src_path, dest_path)
                                            printMainMessage("Cleaning up files..")
                                            os.remove("Update.zip")
                                            shutil.rmtree(f"{cur_path}/Update/")
                                            printSuccessMessage(f"Update to v{latest_vers['version']} was finished successfully! Restarting installer..")
                                            subprocess.run(args=[sys.executable] + sys.argv)
                                            sys.exit(0)
                                        else:
                                            printMainMessage("Cleaning up files..")
                                            os.remove("Update.zip")
                                            shutil.rmtree(f"{cur_path}/Update/")
                                            printErrorMessage("Extracting ZIP File failed. Would you like to continue without updating? (y/n)")
                                            if isYes(input("> ")) == False: sys.exit(0)
                                    else:
                                        printErrorMessage("Downloading ZIP File failed. Would you like to continue without updating? (y/n)")
                                        if isYes(input("> ")) == False: sys.exit(0)
                            elif current_version.get("version", "1.0.0") > latest_vers.get("latest_version", "1.0.0"): printSuccessMessage("The bootstrap is a beta version! No updates are needed!")
                            else: printMainMessage("The bootstrap is currently on the latest version! No updates are needed!")
                    else: printErrorMessage("There was an issue while checking for updates.")
                if main_os == "Windows":
                    printMainMessage("Would you like to set the URL Schemes for the Roblox Client and the bootstrap? [Needed for Roblox Link Shortcuts and when Roblox updates] (y/n)")
                    a = input("> ")
                    if isYes(a) == False: disabled_url_scheme_installation = True
                    printMainMessage("Would you like to make shortcuts for the bootstrap? [Needed for launching through the Windows Start Menu and Desktop] (y/n)")
                    a = input("> ")
                    if isYes(a) == False: disabled_shortcuts_installation = True
                printMainMessage("Install Information!")
                printMainMessage("In order to allow running for the first time, we're gonna reduce download securities for the app bundle. [This won't affect other apps or downloaded files]")
                printMainMessage("This will not bypass scans by your anti-virus software. It will only allow running by the operating system.")
                a = input("> ")
                printMainMessage("Would you like to allow syncing configurations and mods from this folder to the app? (Only 1 installation folder can be used) (y/n)")
                a = input("> ")
                if isYes(a) == False: use_installation_syncing = False
                printMainMessage("Would you like to rebuild the main app based on source code? (y/n)")
                printYellowMessage("Pyinstaller is required to be installed for this to work.")
                a = input("> ")
                if isYes(a) == True:
                    if not pip_class.installed(["pyinstaller"], boolonly=True): pip_class.install(["pyinstaller"])
                    rebuild_from_source = 1
                if main_os == "Darwin":
                    printMainMessage("Would you like to rebuild the Bootstrap Loader, Play Roblox app and Run Studio app based on source code? (y/n)")
                    printYellowMessage("Clang++ is required to be installed on your Mac in order to use.")
                    a = input("> ")
                    if isYes(a) == True: rebuild_from_source_clang = True
                if main_os == "Windows":
                    printMainMessage("Would you like to set an install location for the bootstrap? (y/n)")
                    a = input("> ")
                    if isYes(a) == True:
                        try:
                            unable_to_use_tkinter = False
                            try:
                                import tkinter as tk
                                from tkinter import filedialog
                            except Exception as e:
                                try:
                                    pip_class.install(["tk"])
                                    tk = pip_class.importModule("tkinter")
                                    filedialog = pip_class.importModule("tkinter").filedialog
                                except Exception as e: unable_to_use_tkinter = True
                            if unable_to_use_tkinter == False:
                                root = tk.Tk()
                                root.withdraw()
                                folder_path = filedialog.askdirectory(title="Select an installation path to install the Bootstrap!", initialdir=default_app_path)
                                if folder_path and os.path.isdir(folder_path):
                                    printMainMessage(f"You have selected the following folder to install the bootstrap into: {folder_path}")
                                    printMainMessage(f"Example Resemblance: {os.path.join(folder_path, 'OrangeBlox', 'OrangeBlox.exe') if main_os == 'Windows' else os.path.join(folder_path, 'OrangeBlox.app')}")
                                    printMainMessage("Would you like to install into this folder? (y/n)")
                                    if isYes(input("> ")):
                                        if folder_path and os.path.isdir(folder_path):
                                            if os.path.exists(os.path.join(folder_path, "OrangeBlox")): printErrorMessage("An OrangeBlox instance already exists in this folder!")
                                            else:
                                                if main_os == "Darwin":
                                                    stored_main_app["OverallInstall"] = folder_path
                                                    stored_main_app["Darwin"] = [
                                                        os.path.join(folder_path, "OrangeBlox.app/Contents/MacOS/OrangeBlox.app"), 
                                                        os.path.join(folder_path, "OrangeBlox.app"), 
                                                        os.path.join(folder_path, "Play Roblox.app"), 
                                                        os.path.join(folder_path, "Run Studio.app")
                                                    ]
                                                elif main_os == "Windows":
                                                    stored_main_app["OverallInstall"] = folder_path
                                                    stored_main_app["Windows"] = [
                                                        os.path.join(folder_path, "OrangeBlox"), 
                                                        os.path.join(folder_path, "OrangeBlox", "OrangeBlox.exe"), 
                                                        os.path.join(folder_path, "OrangeBlox"), 
                                                        os.path.join(folder_path, "OrangeBlox")
                                                    ]
                                        else: printMainMessage("Alright, it's your choice! In order to reselect, please restart setup!")
                                    else: printMainMessage("Alright, it's your choice! In order to reselect, please restart setup!")
                                else: printMainMessage("No folder was selected.")
                            else: printErrorMessage("There was an error selecting a folder because tkinter may not be installed properly!")
                        except Exception as e: printErrorMessage("There was an error selecting a folder!")
                    
                printMainMessage("Would you like to delete other operating system versions? (This may save 30MB+ of space) (y/n)")
                a = input("> ")
                if isYes(a) == False: disable_remove_other_operating_systems = True
                if remove_unneeded_messages == False: printMainMessage("Alright now, last question, select carefully!")
                if overwrited == True: printMainMessage("Do you want to update OrangeBlox? (This will reupdate all files based on this Installation folder.) (y/n)")
                else: printMainMessage("Do you want to install OrangeBlox into your system? (y/n)")
                res = input("> ")
                if isYes(res) == True:
                    if remove_unneeded_messages == False: printMainMessage("Yippieee!!!")
                    try: install()
                    except Exception as e: printErrorMessage(f"Something went wrong during installation: {str(e)}")
                    input("> ")
                else:
                    if remove_unneeded_messages == False: printMainMessage("Aw, well, better next time! (..maybe)")
            else:
                def requestUpdate():
                    global disable_remove_other_operating_systems
                    printMainMessage("Would you like to delete other operating system versions? (This may save 30MB+ of space) (y/n)")
                    a = input("> ")
                    if isYes(a) == False: disable_remove_other_operating_systems = True
                    printMainMessage("Do you want to update OrangeBlox? (This will reupdate all files based on this Installation folder.) (y/n)")
                    res = input("> ")
                    if isYes(res) == True:
                        if remove_unneeded_messages == False: printMainMessage("Yippieee!!!")
                        try: install()
                        except Exception as e: printErrorMessage(f"Something went wrong during installation: {str(e)}")
                        input("> ")
                    else:
                        if remove_unneeded_messages == False: printMainMessage("Aw, well, better next time! (..maybe)")
                def requestUninstall():
                    if main_os == "Darwin":
                        if not os.path.exists(f"{stored_main_app[main_os][1]}/Contents/MacOS/OrangeBlox.app/"):
                            printMainMessage("OrangeBlox is not installed on this system.")
                            input("> ")
                            sys.exit(0)
                    elif main_os == "Windows":
                        if not os.path.exists(f"{stored_main_app[main_os][0]}"):
                            printMainMessage("OrangeBlox is not installed on this system.")
                            input("> ")
                            sys.exit(0)
                    if repair_mode == False: 
                        printMainMessage("Are you sure you want to uninstall OrangeBlox from your system? (This will remove the app from your system and reinstall Roblox.) (y/n)")
                        res = input("> ")
                    else: res = "y"
                    if isYes(res) == True:
                        if main_os == "Darwin":
                            if pip_class.getIfProcessIsOpened("OrangeBlox.app"):
                                printErrorMessage("Please close OrangeBlox.app first before continuing to uninstall!")
                                input("> ")
                                sys.exit(0)
                            else:
                                # Remove Apps
                                if os.path.exists(stored_main_app[main_os][1]):
                                    printMainMessage("Removing from Applications Folder (Main Bootstrap)..")
                                    shutil.rmtree(stored_main_app[main_os][1])
                                if os.path.exists(stored_main_app[main_os][2]):
                                    printMainMessage("Removing from Applications Folder (Play Roblox)..")
                                    shutil.rmtree(stored_main_app[main_os][2])
                                if os.path.exists(stored_main_app[main_os][3]):
                                    printMainMessage("Removing from Applications Folder (Run Studio)..")
                                    shutil.rmtree(stored_main_app[main_os][3])
                        elif main_os == "Windows":
                            if pip_class.getIfProcessIsOpened("OrangeBlox.exe"): 
                                printMainMessage("Ending OrangeBlox.exe in order to uninstall..")
                                pip_class.endProcess("OrangeBlox.exe")
                            # Remove URL Schemes
                            printMainMessage("Resetting URL Schemes..")
                            try:
                                def set_url_scheme(protocol, exe_path):
                                    protocol_key = r"Software\Classes\{}".format(protocol)
                                    command_key = r"Software\Classes\{}\shell\open\command".format(protocol)
                                    try:
                                        key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, protocol_key)
                                        win32api.RegSetValue(key, "", win32con.REG_SZ, "URL:{}".format(protocol))
                                        win32api.RegSetValueEx(key, "URL Protocol", 0, win32con.REG_SZ, protocol)
                                        win32api.RegCloseKey(key)
                                        key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, command_key)
                                        win32api.RegSetValueEx(key, "", 0, win32con.REG_SZ, '"{}" "%1"'.format(exe_path))
                                        win32api.RegCloseKey(key)
                                        printDebugMessage(f'URL scheme "{protocol}" has been set for "{exe_path}"')
                                    except Exception as e: printErrorMessage(f"An error occurred: {e}")
                                def get_file_type_reg(extension):
                                    try:
                                        key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, extension)
                                        file_type, _ = win32api.RegQueryValueEx(key, "")
                                        win32api.RegCloseKey(key)
                                        return file_type
                                    except Exception: return None
                                def set_file_type_reg(extension, exe_path, file_type):
                                    try:
                                        extension = extension if extension.startswith('.') else f'.{extension}'
                                        key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, f"Software\\Classes\\{extension}")
                                        win32api.RegSetValue(key, "", win32con.REG_SZ, file_type)
                                        win32api.RegCloseKey(key)
                                        key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, f"Software\\Classes\\{file_type}\\shell\\open\\command")
                                        win32api.RegSetValue(key, "", win32con.REG_SZ, f'"{exe_path}" "%1"')
                                        win32api.RegCloseKey(key)
                                        key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, f"Software\\Classes\\{file_type}\\DefaultIcon")
                                        win32api.RegSetValue(key, "", win32con.REG_SZ, f"{exe_path},0")
                                        win32api.RegCloseKey(key)
                                        ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x0000, None, None)
                                        printDebugMessage(f'File Handling "{extension}" has been set for "{exe_path}"')
                                    except Exception as e: printErrorMessage(f"An error occurred: {e}")
                                set_url_scheme("efaz-bootstrap", "")
                                set_url_scheme("orangeblox", "")
                                set_file_type_reg(".obx", "", "Uninstalled OrangeBlox")
                                cur = handler.getCurrentClientVersion()
                                cur_studio = handler.getRobloxInstallFolder(studio=True, directory=f"{pip_class.getLocalAppData()}\\Roblox\\Versions")
                                if cur:
                                    if cur["success"] == True:
                                        set_url_scheme("roblox-player", f"{pip_class.getLocalAppData()}\\Roblox\\Versions\\{cur['version']}\\RobloxPlayerBeta.exe")
                                        set_url_scheme("roblox", f"{pip_class.getLocalAppData()}\\Roblox\\Versions\\{cur['version']}\\RobloxPlayerBeta.exe")
                                if cur_studio:
                                    rbx_studio_beta = f"{cur_studio}\\RobloxStudioBeta.exe"
                                    set_url_scheme("roblox-studio", rbx_studio_beta)
                                    set_url_scheme("roblox-studio-auth", rbx_studio_beta)
                                    set_file_type_reg(".rbxl", rbx_studio_beta, "Roblox Place")
                                    set_file_type_reg(".rbxlx", rbx_studio_beta, "Roblox Place")
                            except Exception as e: printErrorMessage(f"Unable to reset URL schemes: {str(e)}")

                            # Remove Shortcuts
                            printMainMessage("Removing shortcuts..")
                            try:
                                def remove_path(pat):
                                    if os.path.exists(pat):  os.remove(pat)
                                def create_shortcut(target_path, shortcut_path, working_directory=None, icon_path=None, arguments=None):
                                    shell = win32client.Dispatch('WScript.Shell')
                                    if not os.path.exists(os.path.dirname(shortcut_path)): os.makedirs(os.path.dirname(shortcut_path),mode=511)
                                    shortcut = shell.CreateShortcut(shortcut_path)
                                    shortcut.TargetPath = target_path
                                    if arguments: shortcut.Arguments = arguments
                                    if working_directory: shortcut.WorkingDirectory = working_directory
                                    if icon_path: shortcut.IconLocation = icon_path
                                    shortcut.Save()
                                remove_path(os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), 'Play Roblox.lnk'))
                                remove_path(os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), 'Run Studio.lnk'))
                                remove_path(os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), "OrangeBlox.lnk"))
                                remove_path(os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs'), 'Play Roblox.lnk'))
                                remove_path(os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs'), 'Run Studio.lnk'))
                                remove_path(os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs'), "OrangeBlox.lnk"))
                                if cur:
                                    if cur["success"] == True:
                                        create_shortcut(f"{pip_class.getLocalAppData()}\\Roblox\\Versions\\{cur['version']}\\RobloxPlayerBeta.exe", os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), 'Roblox Player.lnk'))
                                        create_shortcut(f"{pip_class.getLocalAppData()}\\Roblox\\Versions\\{cur['version']}\\RobloxPlayerBeta.exe", os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Roblox'), 'Roblox Player.lnk'))
                                if cur_studio:
                                    if cur_studio["success"] == True:
                                        create_shortcut(f"{pip_class.getLocalAppData()}\\Roblox\\Versions\\{cur_studio['version']}\\RobloxStudioBeta.exe", os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), 'Roblox Studio.lnk'))
                                        create_shortcut(f"{pip_class.getLocalAppData()}\\Roblox\\Versions\\{cur_studio['version']}\\RobloxStudioBeta.exe", os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Roblox'), 'Roblox Studio.lnk'))
                            except Exception as e: printErrorMessage(f"Unable to remove shortcuts: {str(e)}")

                            # Remove from Windows' Program List
                            printMainMessage("Unmarking from Windows Program List..")
                            app_key = r"Software\OrangeBlox"
                            uninstall_key = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\OrangeBlox"
                            try: win32api.RegDeleteKey(win32con.HKEY_CURRENT_USER, app_key)
                            except Exception: printErrorMessage(f'Registry key "{app_key}" not found.')
                            try: win32api.RegDeleteKey(win32con.HKEY_CURRENT_USER, uninstall_key)
                            except Exception: printErrorMessage(f'Registry key "{uninstall_key}" not found.')

                            # Remove App
                            if os.path.exists(stored_main_app[main_os][0]):
                                printMainMessage("Removing App Folder..")
                                shutil.rmtree(stored_main_app[main_os][0], ignore_errors=True)
                        if repair_mode == False:
                            printMainMessage("Preparing to reinstall Roblox..")
                            handler.temporaryResetCustomizableVariables()
                            handler.installRoblox(debug=True, downloadInstaller=True, downloadChannel=None, copyRobloxInstallerPath=(f"{RFFI.windows_dir}\\RobloxPlayerInstaller.exe" if main_os == "Windows" else f"{RFFI.macOS_dir}{RFFI.macOS_beforeClientServices}RobloxPlayerInstaller.app"))
                            printSuccessMessage("Successfully uninstalled OrangeBlox and reinstalled Roblox!")
                            input("> ")
                    else:
                        if remove_unneeded_messages == False: printMainMessage("Aw, well, better next time! (..maybe)")
                def requestRepair():
                    global instant_install
                    global repair_mode
                    global overwrited
                    printMainMessage("Are you sure you want to repair/reinstall the bootstrap? (y/n)")
                    res = input("> ")
                    if isYes(res) == True:
                        repair_mode = True
                        if not os.path.exists(f"{cur_path}/Apps/"):
                            printErrorMessage("Please use an installation folder to install a new version from before continuing to repair!")
                            input("> ")
                            sys.exit(0)
                        if main_os == "Darwin":
                            if pip_class.getIfProcessIsOpened("OrangeBlox.app"):
                                printErrorMessage("Please close OrangeBlox.app first before continuing to repair!")
                                input("> ")
                                sys.exit(0)
                        elif main_os == "Windows":
                            if pip_class.getIfProcessIsOpened("OrangeBlox.exe"):
                                printErrorMessage("Please close OrangeBlox.exe first before continuing to repair!")
                                input("> ")
                                sys.exit(0)
                        app_location = f"{cur_path}/"
                        repair_path = f"{cur_path}/RepairData/"
                        if os.path.exists(repair_path):
                            printYellowMessage("Repair Data already exists!")
                            shutil.rmtree(repair_path, ignore_errors=True)
                        else:
                            printMainMessage("Making Repair Data Folder..")
                            os.mkdir(repair_path)
                        printMainMessage("Finding app..")
                        if main_os == "Darwin": app_location = f"{stored_main_app[main_os][1]}/Contents/Resources/"
                        elif main_os == "Windows": app_location = f"{stored_main_app[main_os][0]}"
                        if not os.path.exists(app_location):
                            printErrorMessage("OrangeBlox is not installed!")
                            input("> ")
                            sys.exit(0)
                        printMainMessage("Copying Configuration.json..")
                        main_config = getSettings(os.path.join(app_location, "Configuration.json"))
                        data_in_string = zlib.compress(json.dumps(main_config).encode('utf-8'))
                        with open(os.path.join(repair_path, "Configuration.json"), "wb") as f: f.write(data_in_string)
                        printMainMessage("Copying AvatarEditorMaps..")
                        pip_class.copyTreeWithMetadata(os.path.join(app_location, "AvatarEditorMaps"), os.path.join(repair_path, "AvatarEditorMaps"), dirs_exist_ok=True, ignore_if_not_exist=True)
                        printMainMessage("Copying Cursors..")
                        pip_class.copyTreeWithMetadata(os.path.join(app_location, "Cursors"), os.path.join(repair_path, "Cursors"), dirs_exist_ok=True, ignore_if_not_exist=True)
                        printMainMessage("Copying PlayerSounds..")
                        pip_class.copyTreeWithMetadata(os.path.join(app_location, "PlayerSounds"), os.path.join(repair_path, "PlayerSounds"), dirs_exist_ok=True, ignore_if_not_exist=True)
                        printMainMessage("Copying Mods..")
                        pip_class.copyTreeWithMetadata(os.path.join(app_location, "Mods"), os.path.join(repair_path, "Mods"), dirs_exist_ok=True, ignore_if_not_exist=True)
                        printMainMessage("Copying RobloxBrand..")
                        pip_class.copyTreeWithMetadata(os.path.join(app_location, "RobloxBrand"), os.path.join(repair_path, "RobloxBrand"), dirs_exist_ok=True, ignore_if_not_exist=True)
                        printMainMessage("Copying RobloxStudioBrand..")
                        pip_class.copyTreeWithMetadata(os.path.join(app_location, "RobloxStudioBrand"), os.path.join(repair_path, "RobloxStudioBrand"), dirs_exist_ok=True, ignore_if_not_exist=True)
                        printMainMessage("Creating Metadata..")
                        ver = current_version["version"]
                        if os.path.exists(os.path.join(app_location, "Version.json")):
                            ver_js = None
                            with open(os.path.join(app_location, "Version.json"), "r", encoding="utf-8") as f: ver_js = json.load(f)
                            if ver_js: ver = ver_js["version"]
                        with open(os.path.join(repair_path, "Metadata.json"), "w", encoding="utf-8") as f:
                            json.dump({
                                "installer_version": current_version["version"],
                                "bootstrap_version": ver,
                                "script_hash": generateFileHash(os.path.join(app_location, "Main.py")),
                                "operating_system": main_os
                            }, f, indent=4)
                        printMainMessage("Uninstalling Bootstrap..")
                        try:
                            requestUninstall()
                            printMainMessage("Redirecting to install mode.")
                            instant_install = True
                            overwrited = False
                            try:
                                install()
                                printMainMessage("Installation was a success! Preparing data..")
                                printMainMessage("Copying Configuration.json..")
                                if os.path.exists(os.path.join(repair_path, "FastFlagConfiguration.json")):
                                    with open(os.path.join(repair_path, "FastFlagConfiguration.json"), "r", encoding="utf-8") as f: main_config = json.load(f)
                                else:
                                    with open(os.path.join(repair_path, "Configuration.json"), "rb") as f: obfuscated_json = f.read()
                                    try: obfuscated_json = json.loads(obfuscated_json)
                                    except Exception as e: obfuscated_json = json.loads(zlib.decompress(obfuscated_json).decode("utf-8"))
                                    main_config = obfuscated_json
                                saveSettings(main_config, directory=os.path.join(app_location, "Configuration.json"))
                                shutil.copy(os.path.join(repair_path, "Configuration.json"), os.path.join(app_location, "Configuration.json"))
                                printMainMessage("Copying AvatarEditorMaps..")
                                pip_class.copyTreeWithMetadata(os.path.join(repair_path, "AvatarEditorMaps"), os.path.join(app_location, "AvatarEditorMaps"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                printMainMessage("Copying Cursors..")
                                pip_class.copyTreeWithMetadata(os.path.join(repair_path, "Cursors"), os.path.join(app_location, "Cursors"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                printMainMessage("Copying PlayerSounds..")
                                pip_class.copyTreeWithMetadata(os.path.join(repair_path, "PlayerSounds"), os.path.join(app_location, "PlayerSounds"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                printMainMessage("Copying Mods..")
                                pip_class.copyTreeWithMetadata(os.path.join(repair_path, "Mods"), os.path.join(app_location, "Mods"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                printMainMessage("Copying RobloxBrand..")
                                pip_class.copyTreeWithMetadata(os.path.join(repair_path, "RobloxBrand"), os.path.join(app_location, "RobloxBrand"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                printMainMessage("Copying RobloxStudioBrand..")
                                pip_class.copyTreeWithMetadata(os.path.join(repair_path, "RobloxStudioBrand"), os.path.join(app_location, "RobloxStudioBrand"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                printMainMessage("Finished transferring! Deleting repair data..")
                                if os.path.exists(repair_path): shutil.rmtree(repair_path, ignore_errors=True)
                                printSuccessMessage("Successfully repaired OrangeBlox!")
                                input("> ")
                            except Exception as e:
                                printErrorMessage(f"Something went wrong during installation: {str(e)}")
                                printErrorMessage("Your data is saved inside the RepairData folder.")
                                input("> ")
                        except Exception as e:
                            printErrorMessage(f"Something went wrong during uninstallation: {str(e)}")
                            printErrorMessage("Your data is saved inside the RepairData folder.")
                            input("> ")
                def requestBackup():
                    global instant_install
                    global repair_mode
                    global overwrited
                    printMainMessage("Are you sure you want to backup bootstrap data? This will save to a new file called Backup.obx (y/n)")
                    res = input("> ")
                    if isYes(res) == True:
                        if main_os == "Darwin":
                            if pip_class.getIfProcessIsOpened("OrangeBlox.app"):
                                printErrorMessage("Please close OrangeBlox.app first before continuing to repair!")
                                input("> ")
                                sys.exit(0)
                        elif main_os == "Windows":
                            if pip_class.getIfProcessIsOpened("OrangeBlox.exe"):
                                printErrorMessage("Please close OrangeBlox.exe first before continuing to repair!")
                                input("> ")
                                sys.exit(0)
                        app_location = f"{cur_path}/"
                        backup_path = f"{cur_path}/Backup/"
                        if os.path.exists(backup_path):
                            printYellowMessage("Backup Folder already exists!")
                            shutil.rmtree(backup_path, ignore_errors=True)
                        else:
                            printMainMessage("Making Backup Folder..")
                            os.mkdir(backup_path)
                        printMainMessage("Finding app..")
                        if main_os == "Darwin": app_location = f"{stored_main_app[main_os][1]}/Contents/Resources/"
                        elif main_os == "Windows": app_location = f"{stored_main_app[main_os][0]}"
                        if not os.path.exists(app_location):
                            printErrorMessage("OrangeBlox is not installed!")
                            input("> ")
                            sys.exit(0)
                        printMainMessage("Copying Configuration.json..")
                        main_config = getSettings(os.path.join(app_location, "Configuration.json"))
                        data_in_string = zlib.compress(json.dumps(main_config).encode('utf-8'))
                        with open(os.path.join(backup_path, "Configuration.json"), "wb") as f: f.write(data_in_string)
                        printMainMessage("Copying AvatarEditorMaps..")
                        pip_class.copyTreeWithMetadata(os.path.join(app_location, "AvatarEditorMaps"), os.path.join(backup_path, "AvatarEditorMaps"), dirs_exist_ok=True, ignore_if_not_exist=True)
                        printMainMessage("Copying Cursors..")
                        pip_class.copyTreeWithMetadata(os.path.join(app_location, "Cursors"), os.path.join(backup_path, "Cursors"), dirs_exist_ok=True, ignore_if_not_exist=True)
                        printMainMessage("Copying PlayerSounds..")
                        pip_class.copyTreeWithMetadata(os.path.join(app_location, "PlayerSounds"), os.path.join(backup_path, "PlayerSounds"), dirs_exist_ok=True, ignore_if_not_exist=True)
                        printMainMessage("Copying Mods..")
                        pip_class.copyTreeWithMetadata(os.path.join(app_location, "Mods"), os.path.join(backup_path, "Mods"), dirs_exist_ok=True, ignore_if_not_exist=True)
                        printMainMessage("Copying RobloxBrand..")
                        pip_class.copyTreeWithMetadata(os.path.join(app_location, "RobloxBrand"), os.path.join(backup_path, "RobloxBrand"), dirs_exist_ok=True, ignore_if_not_exist=True)
                        printMainMessage("Copying RobloxStudioBrand..")
                        pip_class.copyTreeWithMetadata(os.path.join(app_location, "RobloxStudioBrand"), os.path.join(backup_path, "RobloxStudioBrand"), dirs_exist_ok=True, ignore_if_not_exist=True)
                        printMainMessage("Creating Metadata..")
                        ver = current_version["version"]
                        if os.path.exists(os.path.join(app_location, "Version.json")):
                            ver_js = None
                            with open(os.path.join(app_location, "Version.json"), "r", encoding="utf-8") as f: ver_js = json.load(f)
                            if ver_js: ver = ver_js["version"]
                        with open(os.path.join(backup_path, "Metadata.json"), "w", encoding="utf-8") as f:
                            json.dump({
                                "installer_version": current_version["version"],
                                "bootstrap_version": ver,
                                "script_hash": generateFileHash(os.path.join(app_location, "Main.py")),
                                "operating_system": main_os
                            }, f, indent=4)
                        printMainMessage("Archiving Backup..")
                        file_dir = ""
                        for i in os.listdir(backup_path): 
                            file_dir = file_dir + f' "{i}"'
                        if main_os == "Darwin": subprocess.run(["/usr/bin/zip", "-r", "-y", os.path.join(cur_path, "Backup.zip")+file_dir], cwd=backup_path)
                        elif main_os == "Windows": 
                            s = subprocess.run(f'powershell Compress-Archive -Path * -Update -DestinationPath "{os.path.join(cur_path, "Backup.zip")}"', cwd=backup_path, shell=True)
                            if s.returncode == 0: os.rename(os.path.join(cur_path, "Backup.zip"), os.path.join(cur_path, 'Backup.obx'))
                        printMainMessage("Cleaning up..")
                        shutil.rmtree(backup_path, ignore_errors=True)
                        printSuccessMessage(f"Successfully backed up OrangeBlox data!")
                        printSuccessMessage(f"Application Path: {app_location}")
                        printSuccessMessage(f"File Path: {os.path.join(cur_path, 'Backup.obx')}")
                        input("> ")
                if uninstall_mode == True: requestUninstall()
                elif repair_argv_mode == True: requestRepair()
                elif backup_mode == True: requestBackup()
                else:
                    printMainMessage("Please select an installer option you want to do!")
                    printMainMessage("[1] = Update Bootstrap")
                    printMainMessage("[2] = Uninstall Bootstrap")
                    printMainMessage("[3] = Repair Bootstrap")
                    printMainMessage("[4] = Backup Bootstrap")
                    printMainMessage("[*] = Exit Installer")
                    res = input("> ")
                    if res == "1": requestUpdate()
                    elif res == "2": requestUninstall()
                    elif res == "3": requestRepair()
                    elif res == "4": requestBackup()
    if update_mode == True:
        if main_os == "Darwin":
            if os.path.exists(f"{stored_main_app[main_os][1]}/Contents/MacOS/OrangeBlox.app/"):
                if not pip_class.getIfProcessIsOpened("/Terminal.app/Contents/MacOS/Terminal"):
                    printMainMessage("Opening Terminal.app in order for console to show..")
                    subprocess.Popen(["/usr/bin/open", "-j", "-F", "-a", "/System/Applications/Utilities/Terminal.app"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                printMainMessage("Loading OrangeBlox executable!")
                subprocess.Popen(["/usr/bin/open", "-n", "-a", os.path.join(stored_main_app[main_os][1], "Contents", "MacOS", "OrangeBlox.app", "Contents", "MacOS", "OrangeBlox")], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else: printErrorMessage("Bootstrap Launch Failed: App is not installed.")
        elif main_os == "Windows":
            generated_app_path = stored_main_app[main_os][0]
            if os.path.exists(os.path.join(generated_app_path, "OrangeBlox.exe")):
                printMainMessage("Loading OrangeBlox.exe!")
                subprocess.Popen(f'{os.path.join(generated_app_path, "OrangeBlox.exe")}')
            else: printErrorMessage("Bootstrap Launch Failed: App is not installed.")
    sys.exit(0)
else:
    class OrangeBloxNotModule(Exception):
        def __init__(self): super().__init__("OrangeBlox is only a runable instance, not a module.")
    class OrangeBloxInstallerNotModule(Exception):
        def __init__(self): super().__init__("The installer for OrangeBlox is only a runable instance, not a module.")
    class OrangeBloxLoaderNotModule(Exception):
        def __init__(self): super().__init__("The loader for OrangeBlox is only a runable instance, not a module.")
    raise OrangeBloxInstallerNotModule()