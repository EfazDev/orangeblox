# 
# OrangeBlox 🍊
# Made by Efaz from efaz.dev
# v2.4.0k
# 

# Python Modules
import os
import shutil
import json
import sys
import platform
import datetime
import importlib.util
import importlib.machinery
import subprocess
import threading
import traceback
import logging
import hashlib
import builtins
import ctypes
import typing
import time
import zlib
import re

import OrangeAPI
import PyKits; PyKits.BuiltinEditor(builtins)
try: import RobloxFastFlagsInstaller as RFFI
except Exception as e: print("Restarting for module updates.."); PyKits.pip().restartScript("Main.py", sys.argv)
from urllib.parse import unquote, urlparse

if __name__ == "__main__":
    # Base Variables
    main_os: str = platform.system()
    pip_class: PyKits.pip = PyKits.pip()
    requests: PyKits.request = PyKits.request()
    plist_class: PyKits.plist = PyKits.plist()
    colors_class: PyKits.Colors = PyKits.Colors()
    submit_status: PyKits.ProgressBar = PyKits.ProgressBar()
    handler: RFFI.Handler = RFFI.Handler()
    cur_path: str = os.path.dirname(os.path.abspath(__file__))
    content_folder_paths: typing.Dict[str, str] = {}
    font_folder_paths: typing.Dict[str, str] = {}
    multi_instance_enabled: bool = False
    current_global_setting_type: bool = False
    modified_flags_from_mod_scripts: typing.List[str] = []
    skip_modification_mode: bool = False
    installed_update: bool = False
    connect_instead: bool = False
    run_studio: bool = False
    main_config: typing.Dict[str, typing.Union[str, int, bool, float, typing.Dict, typing.List]] = {}
    custom_cookies: typing.Dict[str, str] = {}
    stdout: PyKits.stdout = None
    current_version: typing.Dict[str, str] = {"version": "2.4.0k"}
    given_args: typing.List[str] = list(filter(None, sys.argv))
    user_folder_name: str = os.path.basename(pip_class.getUserFolder())
    mods_folder: str = os.path.join(cur_path, "Mods")
    macos_app_path: str = (os.path.realpath(os.path.join(cur_path, "../", "../") + "/")) if main_os == "Darwin" else cur_path
    user_folder: str = (os.path.expanduser("~") if main_os == "Darwin" else pip_class.getLocalAppData())
    orangeblox_library: str = os.path.join(user_folder, "Library", "OrangeBlox")
    flag_types: typing.Dict[str, str] = {
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
        "EFlagUseIXPFastFlagsMethod2": "bool",
        "EFlagLastModVersionMacOSCaching": "str",
        "EFlagRobloxChannelUpdateToken": "str",
        "EFlagRobloxSecurityCookieUsage": "bool",
        "EFlagUseEfazDevAPI": "bool"
    }
    language_names: typing.Dict[str, str] = {
        "en": "English",
        "ar": "Arabic (العربية)",
        "bn": "Bengali (বাংলা)",
        "zh-cn": "Chinese (Simplified) (简体中文)",
        "zh-tw": "Chinese (Traditional) (繁體中文)",
        "da": "Danish (Dansk)",
        "de": "German (Deutsch)",
        "el": "Greek (Ελληνικά)",
        "fr": "French (Français)",
        "tl": "Filipino (Filipino)",
        "ka": "Georgian (ქართული)",
        "hi": "Hindi (हिन्दी)",
        "id": "Indonesian (Bahasa Indonesia)",
        "it": "Italian (Italiano)",
        "ja": "Japanese (日本語)",
        "ko": "Korean (한국어)",
        "pt": "Portuguese (Português)",
        "ru": "Russian (русский)",
        "es": "Spanish (Español)",
        "th": "Thai (ไทย)",
        "tr": "Turkish (Türkçe)",
        "uk": "Ukrainian (Українська)",
        "ur": "Urdu (اُردُو)",
        "vi": "Vietnamese (Tiếng Việt)"
    }
    updating_mods: typing.Dict[str, typing.List[str]] = {
        "PlayerSounds": ["Old", "Outdated", "Current"], 
        "AvatarEditorMaps": ["Old.rbxl", "Original.rbxl", "BobTheBuilder.rbxl", "SubwaySurfers.rbxl", "Template.rbxl", "McDonaldsWar.rbxl", "MHA.rbxl", "Backrooms.rbxl"], 
        "RobloxBrand": ["Roblox2011", "Roblox2015Red", "Roblox2021", "OrangeBlox", "Original", "Roblox2015", "Roblox2025", "Roblox2008"], 
        "RobloxStudioBrand": ["OrangeBlox", "Studio2025", "Studio2013", "Original", "Studio2015", "Studio2008", "StudioBlue2011", "StudioBlue2008", "Studio2017", "Studio2011"], 
        "Mods": ["VoiceChatRecorder", "Original", "Template", "KlikoModTool", "OldFont", "OrangeBot"], 
        "Cursors": ["2013", "macOS", "Original", "2006"]
    }
    special_logo_mods: typing.Dict[str, typing.List[str]] = {
        "reg": updating_mods["RobloxBrand"],
        "studio": updating_mods["RobloxStudioBrand"]
    }
    main_host: str = ("https://obx.efaz.dev" if current_version["version"].split(".")[2].isdigit() else "https://obxbeta.efaz.dev")

    # Printing Functions
    def ts(mes: str):
        mes = str(mes)
        if hasattr(sys.stdout, "translate"): mes = stdout.translate(mes)
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
    def printMainMessage(mes): colors_class.print(ts(mes), 255)
    def printErrorMessage(mes): colors_class.print(ts(mes), 196)
    def printSuccessMessage(mes): colors_class.print(ts(mes), 82)
    def printWarnMessage(mes): colors_class.print(ts(mes), 202)
    def printYellowMessage(mes): colors_class.print(ts(mes), 226)
    def printDebugMessage(mes): 
        if main_config.get("EFlagEnableDebugMode"): colors_class.print(f"[DEBUG]: {ts(mes)}", 226); logging.debug(mes)

    # Basic Functions
    def isYes(text: str): text = text.strip(); return text.lower() == "y" or text.lower() == "yes" or text.lower() == "true" or text.lower() == "t"
    def isNo(text: str): text = text.strip(); return text.lower() == "n" or text.lower() == "no" or text.lower() == "false" or text.lower() == "f"
    def isRequestClose(text: str): text = text.strip(); return text.lower() == "exit" or text.lower() == "exit()"
    def makedirs(a: str): os.makedirs(a,exist_ok=True,mode=511)
      
    # Awaiting Functions
    def copyFile(pa, de):
        try:
            if os.path.exists(pa):
                destination_folder = f"{os.path.dirname(de)}"
                if os.path.exists(os.path.join(cur_path, "ExportMode")):
                    destination_dir = os.path.join(cur_path, "ExportMode", os.path.dirname(de))
                    if not os.path.exists(destination_dir):
                        makedirs(destination_dir)
                        printDebugMessage(f"Created directory: {destination_dir}")
                    destination_path = os.path.join(cur_path, "ExportMode", de)
                    a = shutil.copy(pa, destination_path)
                if not os.path.exists(destination_folder):
                    makedirs(destination_folder)
                    printDebugMessage(f"Created directory: {destination_folder}")
                a = shutil.copy(pa, de)
                printDebugMessage(f"Copied File: {os.path.realpath(pa).replace(cur_path, f'.')} => {os.path.realpath(de).replace(cur_path, f'.')}")
                return a
            else:
                printDebugMessage(f"File not found: {os.path.realpath(pa)}")
                return None
        except Exception as e:
            printDebugMessage(f"Error transferring file: \n{trace()}")
            return None
    def formatSize(size_bytes):
        if size_bytes == 0: return ts("0 Bytes")
        size_units = ["Bytes", "KB", "MB", "GB", "TB"]
        unit_index = 0
        while size_bytes >= 1024 and unit_index < len(size_units) - 1: size_bytes /= 1024; unit_index += 1
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
    def getFileSize(files, formatWithAbbreviation=True):
        total_size = 0
        for i in files: 
            if os.path.exists(i):
                if os.path.isdir(i): total_size += getFolderSize(i, formatWithAbbreviation=False)
                else: total_size += os.stat(i).st_size
        if formatWithAbbreviation == True:
            return formatSize(total_size)
        else:
            return total_size
    def getRobloxLogFolderSize(static=False):
        if main_os == "Darwin":
            log_path = os.path.join(os.path.expanduser("~"), "Library", "Logs", "Roblox")
            if os.path.exists(log_path):
                return getFolderSize(log_path, formatWithAbbreviation=(static == False))
            else:
                if static == False: return ts("0 Bytes")
                else: return 0
        elif main_os == "Windows":
            log_path = os.path.join(RFFI.windows_dir, "logs")
            if os.path.exists(log_path): return getFolderSize(log_path, formatWithAbbreviation=(static == False))
            else:
                if static == False: return ts("0 Bytes")
                else: return 0
        else:
            if static == False: return ts("0 Bytes")
            else: return 0
    def readJSONFile(path, listExpected=False):
        with open(path, "r", encoding="utf-8") as f:
            try:
                main_content = json.load(f)
                if listExpected == True:
                    if type(main_content) is list: return main_content
                    else: return None
                else:
                    if type(main_content) is dict: return main_content
                    else: return None
            except Exception as e: return None
        return None
    def displayNotification(title="Unknown Title", message="Unknown Message"):
        if main_os == "Darwin":
            if not os.path.exists(os.path.join(cur_path, "AppNotification")):
                try:
                    with open(os.path.join(cur_path, "AppNotification"), "w", encoding="utf-8") as f: json.dump({"title": title, "message": message}, f)
                except Exception as e:
                    try:
                        NSUserNotification = objc.lookUpClass("NSUserNotification")
                        NSUserNotificationCenter = objc.lookUpClass("NSUserNotificationCenter")
                        notification = NSUserNotification.alloc().init()
                        notification.setTitle_(title)
                        notification.setInformativeText_(message)
                        center = NSUserNotificationCenter.defaultUserNotificationCenter()
                        center.deliverNotification_(notification)
                    except Exception as e: printErrorMessage(f"There was an error sending a notification. Error: \n{trace()}")
        elif main_os == "Windows":
            if not os.path.exists(os.path.join(cur_path, "AppNotification")):
                try:
                    with open(os.path.join(cur_path, "AppNotification"), "w", encoding="utf-8") as f: json.dump({"title": title, "message": message}, f)
                except Exception as e:
                    try:
                        plyer.notification.notify(
                            title = title,
                            message = message,
                            app_icon = "Images/AppIcon.ico",
                            timeout = 30,
                        )
                    except Exception as e: printErrorMessage(f"There was an error sending a notification. Error: \n{trace()}")
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
    def generateModsManifest():
        generated_manifest = {}
        for i in os.listdir(os.path.join(mods_folder, "Mods")):
            mod_path = os.path.join(mods_folder, "Mods", i)
            if os.path.isfile(mod_path) and mod_path.endswith(".zip"):
                dow_tar = os.path.join(mods_folder, "Mods", i.split(".")[0])
                makedirs(dow_tar)
                zip_extract = pip_class.unzipFile(mod_path, dow_tar, look_for=["Manifest.json", "ModScript.py", "content", "ExtraContent"], either=True, check=True)
                if zip_extract.returncode == 0: os.remove(mod_path)
        for i in os.listdir(os.path.join(mods_folder, "Mods")):
            mod_info = {
                "name": i,
                "id": i,
                "version": "1.0.0",
                "mod_script": False,
                "mod_script_path": "",
                "mod_script_supports": "1.0.0",
                "mod_script_end_support": "99.99.99",
                "mod_script_end_support_reasoning": "",
                "mod_script_supports_operating_system": True,
                "mod_script_hash": "00000000000000000000000000",
                "manifest_path": "",
                "both_supported": False,
                "is_studio_mod": False,
                "list_in_normal_mods": True,
                "enabled": False,
                "permissions": [],
                "python_modules": []
            }
            mod_path = os.path.join(mods_folder, "Mods", i)
            if os.path.isdir(mod_path):
                manifest_path = os.path.join(mod_path, "Manifest.json")
                mod_script_path = os.path.join(mod_path, "ModScript.py")
                if not (main_config.get("EFlagEnabledMods") and type(main_config.get("EFlagEnabledMods")) is dict): main_config["EFlagEnabledMods"] = {}
                if main_config.get("EFlagEnabledMods").get(i) == True: mod_info["enabled"] = True
                if os.path.exists(os.path.join(mod_path, "StudioMod")): mod_info["is_studio_mod"] = True
                if os.path.exists(os.path.join(mod_path, "PlayerStudioSupported")): mod_info["both_supported"] = True
                if os.path.exists(manifest_path) and os.path.isfile(manifest_path):
                    res_json = readJSONFile(manifest_path)
                    if res_json:
                        if type(res_json.get("name")) is str: mod_info["name"] = res_json.get("name")
                        if type(res_json.get("version")) is str and len(res_json.get("version")) < 10: mod_info["version"] = res_json.get("version")
                        if type(res_json.get("mod_script")) is bool: mod_info["mod_script"] = res_json.get("mod_script")
                        if type(res_json.get("list_in_normal_mods")) is bool: mod_info["list_in_normal_mods"] = res_json.get("list_in_normal_mods")
                        if type(res_json.get("mod_script_requirements")) is list:
                            for req in res_json.get("mod_script_requirements"):
                                if type(req) is str: mod_info["permissions"].append(req)
                        if type(res_json.get("mod_script_supports")) is str and re.match(r'^\d+\.\d+\.\d+$', res_json.get("mod_script_supports")): mod_info["mod_script_supports"] = res_json.get("mod_script_supports")
                        if type(res_json.get("mod_script_end_support")) is str and re.match(r'^\d+\.\d+\.\d+$', res_json.get("mod_script_end_support")): mod_info["mod_script_end_support"] = res_json.get("mod_script_end_support")
                        if type(res_json.get("mod_script_end_support_reasoning")) is str and len(res_json.get("mod_script_end_support_reasoning")) < 250: mod_info["mod_script_end_support_reasoning"] = res_json.get("mod_script_end_support_reasoning")
                        if main_os == "Darwin" and res_json.get("mod_script_does_not_support_macos") == True: mod_info["mod_script_supports_operating_system"] = False
                        elif main_os == "Windows" and res_json.get("mod_script_does_not_support_windows") == True: mod_info["mod_script_supports_operating_system"] = False
                        if res_json.get("is_studio_mod") == True: mod_info["is_studio_mod"] = True
                        if res_json.get("player_studio_support") == True: mod_info["both_supported"] = True
                        if type(res_json.get("python_modules")) is list:
                            for pyt in res_json.get("python_modules"):
                                if type(pyt) is str: mod_info["python_modules"].append(pyt)
                        mod_info["manifest_path"] = manifest_path
                if os.path.exists(mod_script_path) and os.path.isfile(mod_script_path) and not os.path.islink(mod_script_path):
                    contains_other_python_scripts = False
                    for a, b, c in os.walk(mod_path):
                        for dsci in c:
                            if dsci.endswith(".py") and not (dsci == "ModScript.py"):  contains_other_python_scripts = True
                    if contains_other_python_scripts == True and not ("allowAccessingPythonFiles" in mod_info["permissions"]): mod_info["mod_script"] = False
                    else:
                        with open(mod_script_path, "r", encoding="utf-8") as f: mod_script_text = f.read()
                        for pe, va in handler.roblox_event_info.items():
                            if va.get("detection") and va.get("detection") in mod_script_text and not (pe in mod_info["permissions"]): mod_info["permissions"].append(pe)
                        if ("EfazRobloxBootstrapAPI" in mod_script_text) and mod_info.get("mod_script_supports") < "1.3.0": mod_info["mod_script_supports"] = "1.3.0"
                        elif ("OrangeAPI" in mod_script_text) and mod_info.get("mod_script_supports") < "2.0.0": mod_info["mod_script_supports"] = "2.0.0"
                        if "import OrangeAPI" in mod_script_text: 
                            for mod_line in mod_script_text.splitlines():
                                if mod_line.startswith("import OrangeAPI"): mod_script_text = mod_script_text.replace("import OrangeAPI", "#import OrangeAPI")
                                elif mod_line.startswith("from OrangeAPI"): mod_script_text = mod_script_text.replace("from OrangeAPI", "#from OrangeAPI")
                        if "from OrangeAPI import OrangeAPI;" in mod_script_text or " = OrangeAPI()" in mod_script_text: mod_script_text = mod_script_text.replace("from OrangeAPI import OrangeAPI;", "import OrangeAPI as orange; OrangeAPI = orange.OrangeAPI();").replace(" = OrangeAPI()", " = OrangeAPI")
                        if "import RobloxFastFlagsInstaller" in mod_script_text: mod_script_text = mod_script_text.replace("import RobloxFastFlagsInstaller", "import OrangeAPI")
                        if "import PipHandler" in mod_script_text: mod_script_text = mod_script_text.replace("import PipHandler", "import OrangeAPI")
                        if "import PyKits" in mod_script_text: mod_script_text = mod_script_text.replace("import PyKits", "import OrangeAPI")
                        if "import Install" in mod_script_text: mod_script_text = mod_script_text.replace("import Install", "import OrangeAPI")
                        if "import DiscordPresenceHandler" in mod_script_text: mod_script_text = mod_script_text.replace("import DiscordPresenceHandler", "import OrangeAPI")
                        if "import Main" in mod_script_text: mod_script_text = mod_script_text.replace("import Main", "import OrangeAPI")
                        if "import builtins" in mod_script_text: mod_script_text = mod_script_text.replace("import builtins", "import OrangeAPI")
                        with open(mod_script_path, "w", encoding="utf-8") as f: f.write(mod_script_text)
                        mod_info["mod_script_path"] = mod_script_path
                        mod_info["mod_script_hash"] = generateFileHash(mod_script_path)
                else: mod_info["mod_script"] = False
                generated_manifest[i] = mod_info
        return generated_manifest
    def getSettings(updating: bool=False):
        global main_config
        if main_os == "Darwin":
            if os.path.exists(os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.robloxbootstrap.plist")): os.remove(os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.robloxbootstrap.plist"))
            macos_preference_expected = os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.orangeblox.plist")
            if os.path.exists(macos_preference_expected):
                app_configuration = plist_class.readPListFile(macos_preference_expected)
                if app_configuration.get("Configuration"): main_config = app_configuration.get("Configuration")
                else: main_config = {}
            else: main_config = {}
        else:
            with open(os.path.join(cur_path, "Configuration.json"), "rb") as f: obfuscated_json = f.read()
            try: obfuscated_json = json.loads(obfuscated_json)
            except Exception as e: obfuscated_json = json.loads(zlib.decompress(obfuscated_json).decode("utf-8"))
            main_config = obfuscated_json
        if updating == False and main_config.get("EFlagUseConfigurationWebServer") == True and main_config.get("EFlagConfigurationWebServerURL"):
            try:
                req = requests.get(main_config.get("EFlagConfigurationWebServerURL") + requests.format_params({"script": "main"}), headers={"X-Bootstrap-Version": current_version["version"], "X-Python-Version": platform.python_version(), "X-Authorization-Key": main_config.get("EFlagConfigurationAuthorizationKey", "")})
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
    def saveSettings():
        global main_config
        respo = {
            "saved_normally": False,
            "sync_success": False
        }
        before_edit = main_config.copy()
        getSettings()
        remove_items = []
        for i, v in before_edit.items():
            if i in modified_flags_from_mod_scripts: before_edit[i] = main_config.get(i); v = main_config.get(i)
            if not (flag_types.get(i) is None):
                if flag_types.get(i) == "str" and type(v) is str: pass
                elif flag_types.get(i) == "path" and type(v) is str and os.path.exists(v): pass
                elif flag_types.get(i) == "int" and type(v) is int: pass
                elif flag_types.get(i) == "float" and type(v) is float: pass
                elif flag_types.get(i) == "dict" and type(v) is dict: pass
                elif flag_types.get(i) == "bool" and type(v) is bool: pass
                elif flag_types.get(i) == "list" and type(v) is list: pass
                elif flag_types.get(flag_types.get(i)): before_edit[flag_types.get(i)] = v; remove_items.append(i)
                else: remove_items.append(i)
            else: remove_items.append(i)
        for i in remove_items: before_edit.pop(i)
        main_config = before_edit
        if not (main_config.get("EFlagDisableAutosaveToInstallation") == True) and (main_config.get("EFlagOrangeBloxSyncDir") and os.path.exists(main_config.get("EFlagOrangeBloxSyncDir"))):
            if os.path.exists(os.path.join(main_config.get("EFlagOrangeBloxSyncDir"), 'Configuration.json')):
                with open(os.path.join(main_config.get("EFlagOrangeBloxSyncDir"), 'Configuration.json'), "w", encoding="utf-8") as f: json.dump(main_config, f, indent=4)
                respo["sync_success"] = True
            else: printErrorMessage("Bootstrap Sync is not supported since the original unextracted directory is not found.")
        if main_os == "Darwin":
            if os.path.exists(os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.robloxbootstrap.plist")): os.remove(os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.robloxbootstrap.plist"))
            macos_preference_expected = os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.orangeblox.plist")
            if os.path.exists(macos_preference_expected): app_configuration = plist_class.readPListFile(macos_preference_expected)
            else: app_configuration = {}
            app_configuration["InstalledAppPath"] = os.path.realpath(os.path.join(macos_app_path, "../") + "/")
            app_configuration["Configuration"] = main_config
            plist_class.writePListFile(macos_preference_expected, app_configuration, binary=True)
        else:
            data_in_string = zlib.compress(json.dumps(main_config).encode('utf-8'))
            with open(os.path.join(cur_path, "Configuration.json"), "wb") as f: f.write(data_in_string)
        if main_config.get("EFlagUseConfigurationWebServer") == True and main_config.get("EFlagConfigurationWebServerURL"):
            req = requests.post(main_config.get("EFlagConfigurationWebServerURL") + requests.format_params({"script": "main"}), main_config, headers={"X-Bootstrap-Version": current_version["version"], "X-Python-Version": platform.python_version(), "X-Authorization-Key": main_config.get("EFlagConfigurationAuthorizationKey", "")})
            if not req.ok: respo["saved_normally"] = False
        respo["saved_normally"] = True
        return respo
    def waitForInternet():
        if pip_class.getIfConnectedToInternet() == False:
            printWarnMessage("--- Waiting for Internet ---")
            printMainMessage("Please connect to your internet in order to continue! If you're connecting to a VPN, try reconnecting.")
            while pip_class.getIfConnectedToInternet() == False:
                time.sleep(0.05)
            return True
    def generateCodesignCommand(pa, iden, entitlements: str=None): return [["/usr/bin/xattr", "-dr", "com.apple.metadata:_kMDItemUserTags", pa], ["/usr/bin/xattr", "-dr", "com.apple.FinderInfo", pa], ["/usr/bin/xattr", "-cr", pa], ["/usr/bin/codesign", "-f", "--deep", "--timestamp=none"] + (["--entitlements", entitlements] if entitlements else []) + ["-s", iden, pa]]
    def pythonVersionStr(): return f"{pip_class.getCurrentPythonVersion()}{pip_class.getIfPythonVersionIsBeta() and ' (BETA)' or ''}"
    def validateInstallation(): return (main_os == "Darwin" and os.path.exists(os.path.join(macos_app_path, "Contents", "MacOS", "OrangeLoader"))) or (main_os == "Windows" and os.path.exists(os.path.join(cur_path, "OrangeBlox.exe")))
    def safeConvertNumber(testing: str, type: typing.Type=int):
        try: return type(testing)
        except: return None
    def createDownloadToken(studio: bool=None):
        if studio == None: studio = run_studio
        if main_config.get("EFlagRobloxSecurityCookieUsage") == True:
            requesting_channel = handler.getUserChannel(studio=studio, debug=(main_config.get("EFlagEnableDebugMode") == True))
            if requesting_channel.get("success") == True and requesting_channel.get("channel_name") != "LIVE":
                if requesting_channel.get("token"): main_config["EFlagRobloxChannelUpdateToken"] = requesting_channel.get("token")
                return requesting_channel.get("token")
        elif not (main_config.get("EFlagRobloxSecurityCookieUsage") == True) and main_config.get("EFlagRobloxChannelUpdateToken"):
            main_config.pop("EFlagRobloxChannelUpdateToken")
        return None
    def createCookieHeader():
        if main_config.get("EFlagRobloxSecurityCookieUsage") == True:
            cookie_path = handler.getRobloxCookieFileLocation()
            if not cookie_path: return {}
            founded_roblosecurity = handler.parseRobloxCookieFile(cookie_path)
            return {".ROBLOSECURITY": founded_roblosecurity}
        return {}
    def generateFileKey(id: str, ext: str="", dire: str=""): 
        if dire: return os.path.join(dire, f"{id}_{user_folder_name}{ext}")
        if main_os == "Darwin":
            makedirs(orangeblox_library)
            return os.path.join(orangeblox_library, f"{id}{ext}")
        return os.path.join(cur_path, f"{id}_{user_folder_name}{ext}")
    def generateMenuSelection(options: typing.Dict[str, str], before_input: str="", star_option: str="", send_input_response: bool=False): 
        main_ui_options = {}
        options = sorted(options, key=lambda x: x["index"])
        count = 0
        for i in options:
            count += 1
            if main_config.get("EFlagEnableSeeMoreAwaiting") == True and count % 13 == 0: input("[press enter to see more]")
            printMainMessage(f"[{str(count)}] = {i['message']}"); main_ui_options[str(count)] = i
            main_ui_options[str(count)] = i
        if not (star_option == ""): printMainMessage(f"[*] = {star_option}")
        if not (before_input == ""): printMainMessage(before_input)
        
        res = input("> ")
        if send_input_response == True: return res
        if main_ui_options.get(res): return main_ui_options.get(res)
        else: return None
    def setInstalledAppPath(install_app_path):
        if main_os == "Darwin":
            if os.path.exists(os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.robloxbootstrap.plist")): os.remove(os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.robloxbootstrap.plist"))
            macos_preference_expected = os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.orangeblox.plist")
            plist_info = {}
            if os.path.exists(macos_preference_expected): plist_info = plist_class.readPListFile(macos_preference_expected)
            plist_info["InstalledAppPath"] = install_app_path
            plist_class.writePListFile(macos_preference_expected, plist_info, binary=True)
        elif main_os == "Windows":
            import win32api # type: ignore
            import win32con # type: ignore
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
    def startMessage(first: bool=False, ignore_support: bool=False):
        stdout.clear()
        printWarnMessage("-----------")
        printWarnMessage("Welcome to OrangeBlox 🍊!")
        printWarnMessage("Made by Efaz from efaz.dev!")
        printWarnMessage(f"v{current_version['version']}")
        printWarnMessage("-----------")

        # Requirement Checks
        if main_os == "Windows": printMainMessage(f"System OS: {main_os} ({platform.version()}) | Python Version: {pythonVersionStr()}")
        elif main_os == "Darwin": printMainMessage(f"System OS: {main_os} (macOS {platform.mac_ver()[0]}) | Python Version: {pythonVersionStr()}")
        else:
            printErrorMessage("OrangeBlox is only supported for macOS and Windows.")
            input("> ")
            sys.exit(0)
        if ignore_support == False:
            if not pip_class.osSupported(windows_build=17763, macos_version=(10,13,0)):
                if main_os == "Windows": printErrorMessage("OrangeBlox is only supported for Windows 10.0.17763 (October 2018) or higher. Please update your operating system in order to continue!")
                elif main_os == "Darwin": printErrorMessage("OrangeBlox is only supported for macOS 10.13 (High Sierra) or higher. Please update your operating system in order to continue!")
                input("> ")
                sys.exit(0)
            if first == False:
                virutal_memory = psutil.virtual_memory()
                cpu_percent = psutil.cpu_percent(interval=0.1)
                printMainMessage(f"CPU Percentage: {round(cpu_percent, 2)}% | Memory Usage: {formatSize(virutal_memory.total-virutal_memory.available)}/{formatSize(virutal_memory.total)}")
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
        if first == False:
            if main_os == "Windows":
                content_folder_paths["Windows"] = handler.getRobloxInstallFolder()
                font_folder_paths["Windows"] = os.path.join(content_folder_paths['Windows'], "content", "fonts")
                if not os.path.exists(font_folder_paths["Windows"]):
                    printErrorMessage("Please restart OrangeBlox in order to reinstall Roblox!")
                    input("> ")
                    sys.exit(0)
            elif main_os == "Darwin":
                if not os.path.exists(RFFI.macOS_dir):
                    printErrorMessage("Please restart OrangeBlox in order to reinstall Roblox!")
                    input("> ")
                    sys.exit(0)
            installed_roblox_version = handler.getCurrentClientVersion()
            if installed_roblox_version["success"] == True:
                installed_roblox_studio_version = handler.getCurrentClientVersion(studio=True)
                if installed_roblox_studio_version["success"] == True:
                    if installed_roblox_studio_version['version'] == installed_roblox_version['version']: printMainMessage(f"Current Roblox & Roblox Studio Version: {installed_roblox_version['version']}")
                    else:
                        printMainMessage(f"Current Roblox Version: {installed_roblox_version['version']}")
                        printMainMessage(f"Current Roblox Studio Version: {installed_roblox_studio_version['version']}")
                else:
                    printMainMessage(f"Current Roblox Version: {installed_roblox_version['version']}")
            else:
                printErrorMessage("Something went wrong trying to determine your current Roblox version.")
                input("> ")
                sys.exit(0)
    def setLoggingHandler(handler_name):
        global main_os
        global stdout
        log_path = os.path.join(cur_path, "Logs")
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
        sys.stdout = PyKits.stdout(logger, logging.INFO, lang=main_config.get("EFlagSelectedBootstrapLanguage", "en"))
        sys.stderr = PyKits.stdout(logger, logging.ERROR, lang=main_config.get("EFlagSelectedBootstrapLanguage", "en"))
        stdout = sys.stdout
        return True
    
    # First Actions
    getSettings()
    setLoggingHandler("Main")
    if main_os == "Darwin": colors_class.set_console_title("OrangeBlox 🍊")

    # Requirement Checks
    try:
        if main_config and main_config.get("EFlagEnableDebugMode") == True: pip_class.debug = True
        if waitForInternet() == True: printWarnMessage("-----------")
        versions_folder = os.path.join(cur_path, "Versions")
        if main_os == "Darwin": 
            makedirs(orangeblox_library)
            versions_folder = os.path.join(orangeblox_library, "Versions")
            if not os.path.exists(os.path.join(orangeblox_library, "Mods")): shutil.copytree(os.path.join(cur_path, "Mods"), os.path.join(orangeblox_library, "Mods"))
            makedirs(versions_folder)
            mods_folder = os.path.join(orangeblox_library, "Mods")
        if not (main_os == "Windows" or main_os == "Darwin"):
            printErrorMessage("OrangeBlox is only supported for macOS and Windows.")
            input("> ")
            sys.exit(0)
        if not pip_class.osSupported(windows_build=17763, macos_version=(10,13,0)):
            if main_os == "Windows": printErrorMessage("OrangeBlox is only supported for Windows 10.0.17763 (October 2018) or higher. Please update your operating system in order to continue!")
            elif main_os == "Darwin": printErrorMessage("OrangeBlox is only supported for macOS 10.13 (High Sierra) or higher. Please update your operating system in order to continue!")
            input("> ")
            sys.exit(0)
        if not pip_class.pythonSupported(3, 11, 0):
            startMessage(first=True, ignore_support=True)
            if not pip_class.pythonSupported(3, 6, 0):
                printWarnMessage("--- Python Update Required ---")
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
        if pip_class.getIfRunningWindowsAdmin():
            printWarnMessage("--- Admin Permissions Not Required ---")
            printErrorMessage("Please run OrangeBlox under user permissions instead of running administrator!")
            input("> ")
            sys.exit(0)
    except (KeyboardInterrupt, Exception) as e:
        printErrorMessage("Uh oh! A Python exception that causes the script to end has occurred!")
        printErrorMessage(f"Exception: \n{trace()}")
        printErrorMessage(f"Location Code: 4")
        input("> ")
        sys.exit(0 if main_os == "Darwin" else 1)

    # Install Python Packages
    try:
        pypresence = pip_class.importModule("pypresence")
        psutil = pip_class.importModule("psutil")
        if main_os == "Darwin":
            posix_ipc = pip_class.importModule("posix_ipc")
            objc = pip_class.importModule("objc")
        elif main_os == "Windows": 
            win32com = pip_class.importModule("win32com")
            plyer = pip_class.importModule("plyer")
    except Exception as e:
        printWarnMessage("--- Installing Python Modules ---")
        pip_class.install(["pypresence", "psutil"])
        if main_os == "Darwin": pip_class.install(["posix-ipc", "pyobjc-core", "pyobjc-framework-Quartz"])
        elif main_os == "Windows": pip_class.install(["pywin32", "plyer"])
        pip_class.restartScript("Main.py", sys.argv)
        printSuccessMessage("Successfully installed modules!")

    # Python Modules (PyPi Installed)
    try:
        import psutil
        from DiscordPresenceHandler import Presence, StatusDisplayType
        if main_os == "Darwin": import objc
        elif main_os == "Windows":
            import plyer # type: ignore
            import win32api # type: ignore
            import win32con # type: ignore
    except (KeyboardInterrupt, Exception) as e:
        printErrorMessage("Uh oh! A Python exception that causes the script to end has occurred!")
        printErrorMessage(f"Exception: \n{trace()}")
        printErrorMessage(f"Location Code: 5")
        input("> ")
        sys.exit(0 if main_os == "Darwin" else 1) 

    # Roblox Installation Usage Check
    try:
        startMessage(first=True)
        RFFI.submit_status = submit_status
        RFFI.orangeblox_mode = True
        if not validateInstallation():
            printWarnMessage("--- Install Required! ---")
            printMainMessage("Please install OrangeBlox from running Install.py in order to continue!")
            input("> ")
            sys.exit(0)
        if (not os.path.exists(versions_folder)) and main_config.get("EFlagCompletedTutorial") == True:
            printWarnMessage("--- Hello Bootstrap User! ---")
            printMainMessage("We have updated Efaz's Roblox Bootstrap to feature a new brand (OrangeBlox) and also download Roblox into a separate folder and doesn't need vanilla Roblox to be installed!")
            printMainMessage("Your previous installation data was transferred and deleted after installation.")
            printYellowMessage("Once you continue, we will start reinstalling vanilla Roblox and then install a new separate Roblox into OrangeBlox!")
            con = input("> ")
            if isNo(con): sys.exit(0)
            printWarnMessage("--- Reinstalling Roblox ---")
            submit_status.start()
            res = handler.reinstallRoblox(debug=main_config.get("EFlagEnableDebugMode"), clearUserData=False, copyRobloxInstallerPath=(main_os == "Darwin" and os.path.join(cur_path, "RobloxPlayerInstaller.app") or os.path.join(cur_path, "RobloxPlayerInstaller.exe")), downloadInstaller=True, disableRobloxAutoOpen=True, downloadToken=createDownloadToken(studio=False))
            submit_status.end()
            if res and res["success"] == False:
                printErrorMessage("There is an issue while trying to install Roblox. Please try again by restarting this app!")
                input("> ")
                sys.exit(0)
        RFFI.windows_versions_dir = versions_folder
        RFFI.windows_player_folder_name = main_config.get("EFlagBootstrapRobloxInstallFolderName", "com.roblox.robloxplayer")
        RFFI.windows_studio_folder_name = main_config.get("EFlagBootstrapRobloxStudioInstallFolderName", "com.roblox.robloxstudio")
        RFFI.macOS_dir = os.path.join(versions_folder, "Roblox.app")
        RFFI.macOS_studioDir = os.path.join(versions_folder, "Roblox Studio.app")
        RFFI.macOS_installedPath = os.path.join(versions_folder)
        content_folder_paths["Darwin"] = os.path.join(RFFI.macOS_dir, "Contents", "Resources")
        font_folder_paths["Darwin"] = os.path.join(content_folder_paths['Darwin'], "content", "fonts")
        if not (os.path.exists(RFFI.macOS_dir) or os.path.exists(os.path.join(versions_folder, RFFI.windows_player_folder_name))):
            startMessage(first=True)
            printWarnMessage("--- Installing Roblox to Bootstrap ---")
            printMainMessage("Please wait while we install Roblox into OrangeBlox!")
            makedirs(os.path.join(versions_folder))
            submit_status.start()
            res = handler.installRoblox(debug=main_config.get("EFlagEnableDebugMode"))
            submit_status.end()
            if res and res["success"] == False:
                printErrorMessage("There is an issue while trying to install Roblox. Please try again by restarting this app!")
                input("> ")
                sys.exit(0)
            if main_os == "Windows":
                pip_class.copyTreeWithMetadata(os.path.join(cur_path, "_internal"), os.path.join(versions_folder, main_config.get("EFlagBootstrapRobloxInstallFolderName", RFFI.windows_player_folder_name), "_internal"), dirs_exist_ok=True, ignore_if_not_exist=True)
                shutil.copy(os.path.join(cur_path, "OrangeBlox.exe"), os.path.join(versions_folder, main_config.get("EFlagBootstrapRobloxInstallFolderName", RFFI.windows_player_folder_name), "RobloxPlayerInstaller.exe"))
                with open(os.path.join(versions_folder, main_config.get("EFlagBootstrapRobloxInstallFolderName", RFFI.windows_player_folder_name), "RobloxPlayerBetaPlayRobloxRestart.txt"), "w", encoding="utf-8") as f: f.write(cur_path)
            elif main_os == "Darwin":
                if os.path.exists(os.path.join(macos_app_path, "../", "Play Roblox.app")):
                    pip_class.copyTreeWithMetadata(os.path.join(macos_app_path, "../", "Play Roblox.app"), os.path.join(RFFI.macOS_dir, "Contents", "MacOS", "RobloxPlayerInstaller.app"), dirs_exist_ok=True)
                    with open(os.path.join(RFFI.macOS_dir, "Contents", "MacOS", "RobloxPlayerInstaller.app", "Contents", "Resources", "RobloxPlayerBetaPlayRobloxRestart"), "w", encoding="utf-8") as f: f.write(cur_path)
    except (KeyboardInterrupt, Exception) as e:
        printErrorMessage("Uh oh! A Python exception that causes the script to end has occurred!")
        printErrorMessage(f"Exception: \n{trace()}")
        printErrorMessage(f"Location Code: 6")
        input("> ")
        sys.exit(0 if main_os == "Darwin" else 1)

    # Update Mod Script Event Information
    try:
        mod_script_events = {
            # OrangeBlox Permissions
            "fastFlagConfiguration": {"message": ts("Edit or view your bootstrap configuration file"), "level": 3, "detection": "FastFlagConfiguration.json"},
            "configuration": {"message": ts("Edit or view your bootstrap configuration file"), "level": 3, "detection": "Configuration.json"},
            "editMainExecutable": {"message": ts("Edit the main bootstrap executable"), "level": 4, "detection": "Main.py"},
            "editRobloxFastFlagInstallerExecutable": {"message": ts("Edit the RobloxFastFlagInstaller executable"), "level": 4, "detection": "RobloxFastFlagInstaller.py"},
            "editOrangeAPIExecutable": {"message": ts("Edit the OrangeAPI executable"), "level": 4, "detection": "OrangeAPI.py"},
            "editModScript": {"message": ts("Edit ModScript.py executable"), "level": 4, "detection": "ModScript.py"},
            "usageOfRobloxFastFlagsInstaller": {"message": ts("Allow access to use RobloxFastFlagsInstaller directly"), "level": 3, "detection": "RobloxFastFlagsInstaller"},
            "notifications": {"message": ts("Configure or send notifications through Bootstrap"), "level": 1, "detection": "AppNotification"},
            "configureModModes": {"message": ts("Configure your mods"), "level": 2, "detection": "Mods"},
            "configureRobloxBranding": {"message": ts("Configure your Roblox Player's branding"), "level": 1, "detection": "RobloxBrand"},
            "configureRobloxStudioBranding": {"message": ts("Configure your Roblox Studio's branding"), "level": 1, "detection": "RobloxStudioBrand"},
            "configureAppTranslations": {"message": ts("Configure the bootstrap's translations"), "level": 2, "detection": "Translations"},
            "importOtherModules": {"message": ts("Import outside modules from source"), "level": 2, "detection": "importlib"},
            "runOtherScripts": {"message": ts("Run other scripts or commands"), "level": 2, "detection": "subprocess"},
            "configureDeathSounds": {"message": ts("Configure your player sounds"), "level": 1, "detection": "DeathSounds"},
            "configurePlayerSounds": {"message": ts("Configure your player sounds"), "level": 1, "detection": "PlayerSounds"},
            "configureCursors": {"message": ts("Configure your cursors"), "level": 1, "detection": "Cursors"},
            "configureAvatarMaps": {"message": ts("Configure your avatar maps"), "level": 1, "detection": "AvatarEditorMaps"},
            "generateModsManifest": {"message": ts("Get information about all your installed mods"), "level": 0},
            "displayNotification": {"message": ts("Send notifications through OrangeLoader"), "level": 1},
            "getRobloxAppSettings": {"message": ts("Get information about the Roblox client such as the logged in user, accessible policies and settings."), "level": 2},
            "getRobloxLogFolderSize": {"message": ts("Get current size of the Roblox Logs folder"), "level": 0},
            "grantFileEditing": {"message": ts("Grant permissions to read/edit other files"), "level": 3},
            "grantMaximumAbility": {"message": ts("Grant full control to Python APIs with no sense of security."), "level": 4},
            "allowAccessingPythonFiles": {"message": ts("Allow access to other Python files"), "level": 2},
            "sendDiscordWebhookMessage": {"message": ts("Send messages through your Discord Webhooks"), "level": 1},
            "sendBloxstrapRPC": {"message": ts("Send requests through Bloxstrap RPC"), "level": 2},
            "getLatestRobloxVersion": {"message": ts("Get the latest Roblox version"), "level": 0},
            "getInstalledRobloxVersion": {"message": ts("Get the currently installed Roblox version"), "level": 1},
            "getLatestOppositeRobloxVersion": {"message": ts("Get the latest version of the opposite application (Roblox Player -> Studio, Studio -> Player)"), "level": 1},
            "getOppositeInstalledRobloxVersion": {"message": ts("Get the current version of the opposite application (Roblox Player -> Studio, Studio -> Player)"), "level": 1},
            "getRobloxInstallationFolder": {"message": ts("Get the Roblox installation folder"), "level": 2},
            "getIfRobloxIsOpen": {"message": ts("Get if the Roblox client is open"), "level": 1},
            "getIfModIsEnabled": {"message": ts("Get if a mod is enabled or not."), "level": 1},
            "endRoblox": {"message": ts("End the Roblox Instance"), "level": 2},
            "endOppositeRoblox": {"message": ts("End the opposite of Roblox Instance (like Roblox Studio if running Roblox Player)"), "level": 2},
            "enableMod": {"message": ts("Enable a mod on your behalf."), "level": 2},
            "disableMod": {"message": ts("Disable a mod on your behalf."), "level": 1},
            "getFastFlagConfiguration": {"message": ts("Get and view your Roblox client flags"), "level": 1},
            "setFastFlagConfiguration": {"message": ts("Change your Roblox client flags"), "level": 2},
            "saveFastFlagConfiguration": {"message": ts("Change your Roblox client flags (with saving)"), "level": 2},
            "getMainConfiguration": {"message": ts("View your bootstrap configuration file"), "level": 1},
            "setMainConfiguration": {"message": ts("Set your bootstrap configuration within executable"), "level": 2},
            "saveMainConfiguration": {"message": ts("Edit and save your bootstrap configuration file"), "level": 3},
            "getIfRobloxLaunched": {"message": ts("Get if Roblox has launched from the bootstrap"), "level": 0, "free": True},
            "getLatestRobloxPid": {"message": ts("Get the current latest Roblox window's PID"), "level": 1},
            "getOpenedRobloxPids": {"message": ts("Get all the currently opened Roblox PIDs"), "level": 1},
            "getCurrentRobloxPid": {"message": ts("Get the current Roblox PID connected"), "level": 1},
            "getRobloxThumbnailURL": {"message": ts("Get the special logo mod image URL"), "level": 0},
            "changeRobloxWindowSizeAndPosition": {"message": ts("Change the Roblox Window Size and Position"), "level": 2},
            "setRobloxWindowTitle": {"message": ts("Set the Roblox Window Title [Windows Only]"), "level": 1},
            "setRobloxWindowIcon": {"message": ts("Set the Roblox Window Icon [Windows Only]"), "level": 1},
            "focusRobloxWindow": {"message": ts("Focus the Roblox Window to the top window"), "level": 2},
            "getIfOSSupported": {"message": ts("Get if your operating system version is within a certain version."), "level": 0},
            "getIfPythonSupported": {"message": ts("Get if your Python executable is supported."), "level": 0},
            "getIfConnectedToInternet": {"message": ts("Get if your computer is connected to the internet."), "level": 1},
            "getIf32BitWindows": {"message": ts("Get if your computer is 32 bit of Windows."), "level": 0, "free": True},
            "getConnectedUserInfo": {"message": ts("Get game user information from OrangeBlox"), "level": 1},
            "getIfConnectedToGame": {"message": ts("Get if you connected to a Roblox game"), "level": 0},
            "getCurrentPlaceInfo": {"message": ts("Get game information from internal OrangeBlox"), "level": 1},
            "createAppLock": {"message": ts("Create an app lock to use between mod script instances"), "level": 1},
            "unzipFile": {"message": ts("Gain access to unzip files that it may have access to."), "level": 2},
            "getRequest": {"message": ts("Make a GET request to any website."), "level": 1},
            "postRequest": {"message": ts("Make a POST request to any website."), "level": 2},
            "deleteRequest": {"message": ts("Make a DELETE request to any website."), "level": 2},
            "reprepareRoblox": {"message": ts("Receive the ability to restart preparation when Roblox is not opened."), "level": 2},
            "getConfiguration": {"message": ts("Get data in a separate configuration"), "level": 0, "free": True},
            "setConfiguration": {"message": ts("Store data in a separate configuration"), "level": 0, "free": True},
            "getDebugMode": {"message": ts("Get if the bootstrap is in Debug Mode"), "level": 0, "free": True},
            "getVersion": {"message": ts("Get the current version of itself."), "level": 0, "free": True},
            "getName": {"message": ts("Get the current displayed name of itself."), "level": 0, "free": True},
            "getModScriptId": {"message": ts("Get the current mod script id of itself."), "level": 0, "free": True},
            "printSuccessMessage": {"message": ts("Print a console in green (indicates success)"), "level": 0, "free": True},
            "printMainMessage": {"message": ts("Print a console in the standard white color"), "level": 0, "free": True},
            "printColoredMessage": {"message": ts("Print a message on the python console using an ANSI 256 bit color number."), "level": 0, "free": True},
            "printErrorMessage": {"message": ts("Print a console in red (indicates an error)"), "level": 0, "free": True},
            "printYellowMessage": {"message": ts("Print a console in a yellow text (indicates a warning)"), "level": 0, "free": True},
            "about": {"message": ts("Get bootstrap info"), "level": 0, "free": True}
        }
        handler.roblox_event_info.update(mod_script_events)
    except (KeyboardInterrupt, Exception) as e:
        printErrorMessage("Uh oh! A Python exception that causes the script to end has occurred!")
        printErrorMessage(f"Exception: \n{trace()}")
        printErrorMessage(f"Location Code: 7")
        input("> ")
        sys.exit(0 if main_os == "Darwin" else 1)

    # For macOS, Fetch Mods Folder
    try:
        if main_os == "Darwin" and not main_config.get("EFlagLastModVersionMacOSCaching") == current_version["version"]:
            printMainMessage("Syncing mods..")
            sync_folder_names = ["AvatarEditorMaps", "Cursors", "PlayerSounds", "RobloxBrand", "RobloxStudioBrand", "Mods"]
            for sync_folder_name in sync_folder_names:
                targeted_sync_location = os.path.join(cur_path, "Mods", sync_folder_name)
                if os.path.exists(targeted_sync_location) and os.path.isdir(targeted_sync_location):
                    for i in os.listdir(targeted_sync_location):
                        syncing_mod_path = os.path.join(targeted_sync_location, i)
                        if os.path.isdir(syncing_mod_path) and i in updating_mods[sync_folder_name]:
                            installed_mod_path = os.path.join(mods_folder, sync_folder_name, i)
                            if os.path.exists(installed_mod_path): 
                                for e in os.listdir(installed_mod_path):
                                    if not (e == f"Configuration_{user_folder_name}" or e == "__pycache__"): 
                                        if os.path.isdir(os.path.join(installed_mod_path, e)): shutil.rmtree(os.path.join(installed_mod_path, e), ignore_errors=True)
                                        else: os.remove(os.path.join(installed_mod_path, e))
                            def ignore_files_func(dir, files): 
                                config_files = [fi for fi in os.listdir(dir) if fi.startswith("Configuration_")]
                                return set(["__pycache__"] + config_files)
                            pip_class.copyTreeWithMetadata(syncing_mod_path, installed_mod_path, dirs_exist_ok=True, ignore=ignore_files_func)
                    printDebugMessage(f"Successfully synced mod type: {sync_folder_name}")
                else: printDebugMessage(f"There was an issue trying to copy files for mod type: {sync_folder_name}")
            printSuccessMessage("Successfully synced all mods from installation folder!")
            main_config["EFlagLastModVersionMacOSCaching"] = current_version["version"]
            saveSettings()
    except Exception as e:
        printErrorMessage("Uh oh! A Python exception that causes the script to end has occurred!")
        printErrorMessage(f"Exception: \n{trace()}")
        printErrorMessage(f"Location Code: 10")
        input("> ")
        sys.exit(0 if main_os == "Darwin" else 1)

    # Fetch or Install Roblox
    try:
        if main_os == "Windows":
            content_folder_paths["Windows"] = handler.getRobloxInstallFolder()
            if content_folder_paths.get("Windows"):
                font_folder_paths["Windows"] = os.path.join(content_folder_paths['Windows'], "content", "fonts")
                if not os.path.exists(font_folder_paths["Windows"]):
                    startMessage(first=True)
                    printWarnMessage("--- Installing Roblox ---")
                    printMainMessage("Please wait while we install Roblox into OrangeBlox!")
                    submit_status.start()
                    res = handler.installRoblox(debug=main_config.get("EFlagEnableDebugMode"), copyRobloxInstallerPath=os.path.join(cur_path, "RobloxPlayerInstaller.exe"), downloadInstaller=True, verifyInstall=not (main_config.get("EFlagVerifyRobloxHashAfterInstall")==False))
                    submit_status.end()
                    if res and res["success"] == False:
                        printErrorMessage("There is an issue while trying to install Roblox. Please try again by restarting this app!")
                        input("> ")
                        sys.exit(0)
            else:
                startMessage(first=True)
                printWarnMessage("--- Installing Roblox ---")
                printMainMessage("Please wait while we install Roblox into OrangeBlox!")
                submit_status.start()
                res = handler.installRoblox(debug=main_config.get("EFlagEnableDebugMode"), copyRobloxInstallerPath=os.path.join(cur_path, "RobloxPlayerInstaller.exe"), downloadInstaller=True, verifyInstall=not (main_config.get("EFlagVerifyRobloxHashAfterInstall")==False))
                submit_status.end()
                if res and res["success"] == False:
                    printErrorMessage("There is an issue while trying to install Roblox. Please try again by restarting this app!")
                    input("> ")
                    sys.exit(0)
        elif main_os == "Darwin":
            if not os.path.exists(RFFI.macOS_dir):
                startMessage(first=True)
                printWarnMessage("--- Installing Roblox ---")
                printMainMessage("Please wait while we install Roblox into OrangeBlox!")
                submit_status.start()
                res = handler.installRoblox(debug=main_config.get("EFlagEnableDebugMode"), copyRobloxInstallerPath=(main_os == "Darwin" and os.path.join(cur_path, "RobloxPlayerInstaller.app") or os.path.join(cur_path, "RobloxPlayerInstaller.exe")), downloadInstaller=True, verifyInstall=not (main_config.get("EFlagVerifyRobloxHashAfterInstall")==False))
                submit_status.end()
                if res and res["success"] == False:
                    printErrorMessage("There is an issue while trying to install Roblox. Please try again by restarting this app!")
                    input("> ")
                    sys.exit(0)
        installed_roblox_version = handler.getCurrentClientVersion()
        if not (installed_roblox_version["success"] == True):
            startMessage(first=True)
            printErrorMessage("Something went wrong trying to determine your current Roblox version.")
            input("> ")
            sys.exit(0)
    except (KeyboardInterrupt, Exception) as e:
        printErrorMessage("Uh oh! A Python exception that causes the script to end has occurred!")
        printErrorMessage(f"Exception: \n{trace()}")
        printErrorMessage(f"Location Code: 8")
        input("> ")
        sys.exit(0 if main_os == "Darwin" else 1)

    # URL Argument Exchange Between Loader and Main Script
    try:
        if os.path.exists(os.path.join(cur_path, "URLSchemeExchange")):
            with open(os.path.join(cur_path, "URLSchemeExchange"), "r", encoding="utf-8") as f: filtered_args = f.read()
            given_args = ["Main.py", filtered_args]
            os.remove(os.path.join(cur_path, "URLSchemeExchange"))
    except (KeyboardInterrupt, Exception) as e:
        printErrorMessage("Uh oh! A Python exception that causes the script to end has occurred!")
        printErrorMessage(f"Exception: \n{trace()}")
        printErrorMessage(f"Location Code: 9")
        input("> ")
        sys.exit(0 if main_os == "Darwin" else 1)

    # Handle Option Functions
    def continueToRoblox(studio=False): # Continue to Roblox
        global multi_instance_enabled
        global run_studio
        if studio == True:
            printWarnMessage("--- Continue to Roblox Studio ---")
            printMainMessage("Continuing to next stage!")
            run_studio = True
        else:
            printWarnMessage("--- Continue to Roblox ---")
            if main_config.get("EFlagEnableDuplicationOfClients") == True: printMainMessage("Running Roblox with Multiple Instances!"); multi_instance_enabled = True
            else: printMainMessage("Continuing to next stage!")
    def connectExistingRobloxWindow(studio=False): # Connect to Existing Roblox
        global connect_instead
        global run_studio
        printWarnMessage("--- Connect to Existing Roblox ---" if studio == False else "--- Connect to Existing Roblox Studio ---")
        if not (main_config.get("EFlagAllowActivityTracking") == False):
            if handler.getIfRobloxIsOpen(studio=studio):
                connect_instead = True
                if studio == True: run_studio = True
                printMainMessage("Continuing to next stage!")
            else:
                printErrorMessage("There's currently no open Roblox Windows to connect to.")
                input("> ")
                sys.exit(0)
        else:
            printErrorMessage("Activity Tracking is not enabled.")
            input("> ")
            sys.exit(0)
    def continueToFFlagInstaller(): # Run Fast Flag Installer
        global main_config
        if main_config.get("EFlagDisableFastFlagInstallAccess") == True:
            printWarnMessage("--- Fast Flags Installer ---")
            printErrorMessage("Access to editing FFlags settings was disabled by file. Please try again later!")
            input("> ")
            return ts("FFlag Settings was not saved!")
        printWarnMessage("--------------------")
        RFFI.main()
        getSettings(updating=True)
        saveSettings()
    def continueToOrangeBloxInstaller(): # Run OrangeBlox Installer
        global main_config
        printWarnMessage("--- Run OrangeBlox Installer ---")
        if (main_config.get("EFlagOrangeBloxSyncDir") and os.path.exists(main_config.get("EFlagOrangeBloxSyncDir"))):
            printMainMessage("Are you sure you want to run OrangeBlox installer from installation folder?")
            printMainMessage("[y/t] = Yes")
            printMainMessage("[r] = Download & Run")
            printMainMessage("[n/*] = No")
        else:
            printMainMessage("Are you sure you want to run OrangeBlox installer?")
            printMainMessage("[y/t] = Yes")
            printMainMessage("[n/*] = No")
        def download_option():
            if pip_class.getIfConnectedToInternet():
                printDebugMessage("Setting Installed App Path to Local User..") 
                if main_os == "Darwin": setInstalledAppPath(os.path.realpath(os.path.join(macos_app_path, "../") + "/"))
                elif main_os == "Windows": setInstalledAppPath(cur_path)
                printDebugMessage("Sending Request to Bootstrap Version Servers..") 
                version_server = main_config.get("EFlagBootstrapUpdateServer", "https://obx.efaz.dev/Version.json")
                if not (type(version_server) is str and version_server.startswith("https://")): version_server = "https://obx.efaz.dev/Version.json"
                try: latest_vers_res = requests.get(f"{version_server}", headers={"X-Bootstrap-Version": current_version["version"], "X-Python-Version": platform.python_version(), "X-Authorization-Key": main_config.get("EFlagUpdatesAuthorizationKey", "")})
                except Exception as e: latest_vers_res = PyKits.InstantRequestJSONResponse(ok=False)
                if latest_vers_res.ok:
                    latest_vers = latest_vers_res.json
                    download_location = latest_vers.get("download_location", "https://github.com/EfazDev/orangeblox/archive/refs/heads/main.zip")
                    possible_download_path = os.path.join(user_folder, f"OrangeBlox_v{latest_vers['latest_version']}.zip")
                    if download_location == "https://github.com/EfazDev/orangeblox/archive/refs/heads/main.zip":
                        download_location = f"https://github.com/EfazDev/orangeblox/releases/download/v{latest_vers['latest_version']}/OrangeBlox-v{latest_vers['latest_version']}.zip"
                        printSuccessMessage("✅ This version is a public update available on GitHub for viewing.")
                        printSuccessMessage("✅ For information about this update, use this link: https://github.com/EfazDev/orangeblox/releases")
                        printSuccessMessage(f"✅ Download location: {download_location} => {possible_download_path}")
                    elif download_location == "https://github.com/EfazDev/orangeblox/archive/refs/heads/beta.zip":
                        download_location = f"https://github.com/EfazDev/orangeblox/releases/download/v{latest_vers['latest_version']}/OrangeBlox-v{latest_vers['latest_version']}.zip"
                        printYellowMessage("⚠️ This version is a beta version of OrangeBlox and may cause issues with your installation.")
                        printYellowMessage("⚠️ For information about this update, use this link: https://github.com/EfazDev/orangeblox/releases")
                        printYellowMessage(f"⚠️ Download location: {download_location} => {possible_download_path}")
                    elif not (main_config.get("EFlagUpdatesAuthorizationKey", "") == ""):
                        printYellowMessage("🔨 This version is an update configured from an organization (this may still be a modified and an unofficial OrangeBlox version.)")
                        printYellowMessage("🔨 For information about this update, contact your administrator!")
                        printYellowMessage(f"🔨 Download location: {download_location} => {possible_download_path}")
                    else:
                        printErrorMessage("❌ The download location is different from the official GitHub link!")
                        printErrorMessage("❌ You may be downloading an unofficial OrangeBlox version! Download a copy from https://github.com/EfazDev/orangeblox!")
                        printErrorMessage(f"❌ Download location: {download_location} => {possible_download_path}")
                    printMainMessage("Are you sure you would like to continue through downloading OrangeBlox installer? (y/n)")
                    a = input("> ")
                    if (isYes(a) == True):
                        printDebugMessage(f"Saving Settings..")
                        saveSettings()
                        printMainMessage("Downloading Latest Version of OrangeBlox..")
                        late_v = latest_vers.get("latest_version")
                        download_update = requests.download(download_location, os.path.join(user_folder, f'OrangeBlox_v{late_v}.zip'))
                        if download_update.ok:
                            printMainMessage("Download Success! Extracting ZIP now!")
                            dow_tar = os.path.join(user_folder, f'OrangeBloxInstaller')
                            zip_extract = pip_class.unzipFile(os.path.join(user_folder, f'OrangeBlox_v{late_v}.zip'), dow_tar, ["Main.py", "RobloxFastFlagsInstaller.py", "OrangeAPI.py", "Configuration.json", "Apps"])
                            if zip_extract.returncode == 0:
                                printMainMessage("Removing ZIP File..")
                                if os.path.exists(os.path.join(user_folder, f'OrangeBlox_v{late_v}.zip')): os.remove(os.path.join(user_folder, f'OrangeBlox_v{late_v}.zip'))
                                temp_sync = False
                                if not (main_config.get("EFlagOrangeBloxSyncDir") and os.path.exists(main_config.get("EFlagOrangeBloxSyncDir"))):
                                    printMainMessage(f"Registering Sync Directory..")
                                    printDebugMessage(f'Sync Directory: {os.path.join(dow_tar)}')
                                    main_config["EFlagOrangeBloxSyncDir"] = os.path.join(dow_tar)
                                    saveSettings()
                                    temp_sync = True
                                printMainMessage("Running Installer..")
                                stdout.clear()
                                e = stdout.run_process(args=[sys.executable, os.path.join(dow_tar, "Install.py")], cwd=dow_tar)
                                if e.returncode == 0: printSuccessMessage("OrangeBlox Installer has succeeded successfully! Once you continue, this script will reload.")
                                else: printErrorMessage("The installer had a problem! Once you continue, this script will reload.")
                                if temp_sync == False and os.path.exists(dow_tar): 
                                    if os.path.exists(os.path.join(dow_tar, "Backup.obx")): shutil.move(os.path.join(dow_tar, "Backup.obx"), os.path.join(user_folder, "Documents", "OrangeBlox_Backup.obx"))
                                    shutil.rmtree(dow_tar, ignore_errors=True)
                                input("> ")
                                pip_class.restartScript("Main.py", sys.argv)
                                sys.exit(0)
                                return
                            else:
                                printErrorMessage("There was an issue trying to unpack the OrangeBlox installation folder!")
                                return ts("OrangeBlox Installer task was canceled!")
                        else:
                            printErrorMessage("There was an issue trying to download OrangeBlox from the download server!")
                            return ts("OrangeBlox Installer task was canceled!")
                    else: return ts("OrangeBlox Installer task was canceled!")
                else:
                    printErrorMessage("There was an issue trying to fetch OrangeBlox information!")
                    return ts("OrangeBlox Installer task was canceled!")
            else:
                printErrorMessage("Please connect to your internet in order to use this action!")
                return ts("OrangeBlox Installer task was canceled!")
        a = input("> ")
        if isYes(a) == True:
            if (main_config.get("EFlagOrangeBloxSyncDir") and os.path.exists(main_config.get("EFlagOrangeBloxSyncDir"))):
                printMainMessage("Running Installer..")
                stdout.clear()
                e = stdout.run_process(args=[sys.executable, os.path.join(main_config.get("EFlagOrangeBloxSyncDir"), "Install.py")], cwd=main_config.get("EFlagOrangeBloxSyncDir"))
                if e.returncode == 0: printSuccessMessage("OrangeBlox Installer has succeeded successfully! Once you continue, this script will reload.")
                else: printErrorMessage("The installer had a problem! Once you continue, this script will reload.")
                input("> ")
                pip_class.restartScript("Main.py", sys.argv)
                sys.exit(0)
                return
            else: return download_option()
        elif a == "r": return download_option()
        else: return ts("OrangeBlox Installer task was canceled!")
    def continueToClearTemporaryStorage(): # Clear Temporary Storage
        installer_paths = [os.path.join(cur_path, 'RobloxPlayerInstaller.exe'), os.path.join(cur_path, 'RobloxStudioInstaller.exe'), os.path.join(cur_path, 'RobloxPlayerInstaller.app'), os.path.join(cur_path, 'RobloxStudioInstaller.app')]
        bootstrap_image_needed_files = ["AppIcon.icns", "AppIcon.ico", "AppIcon.png", "OrangeBlox.terminal", "AppIconPlayRoblox.icns", "AppIconPlayRoblox.ico", "AppIconRunStudio.icns", "AppIconRunStudio.ico", "AppIcon64.png"]
        orangeblox_log_path = os.path.join(cur_path, "Logs")
        if main_os == "Darwin": orangeblox_log_path = os.path.join(pip_class.getLocalAppData(), "Logs", "OrangeBlox")
        def pythonCacheAvailableToClear():
            cache_detected = []
            for dirpath, dirnames, filenames in os.walk(cur_path):
                if "__pycache__" in dirnames: cache_detected.append(os.path.join(dirpath, "__pycache__"))
            if main_os == "Darwin" and os.path.exists(os.path.join(cur_path, "VirtualEnvironments")): cache_detected.append(os.path.join(cur_path, "VirtualEnvironments"))
            return cache_detected
        def appLocksAvailableToClear():
            locks_detected = []
            for i in os.listdir(cur_path):
                if i.endswith(f"_{user_folder_name}"): locks_detected.append(os.path.join(cur_path, i))
                elif i.startswith("Terminal_") or i == "BootstrapCooldown": locks_detected.append(os.path.join(cur_path, i))
            if main_os == "Darwin" and os.path.exists(orangeblox_library):
                for i in os.listdir(orangeblox_library):
                    if not "." in i and os.path.isfile(os.path.join(orangeblox_library, i)): locks_detected.append(os.path.join(orangeblox_library, i))
                    elif i.startswith("Terminal_") or i == "BootstrapCooldown": locks_detected.append(os.path.join(orangeblox_library, i))
            return locks_detected
        def bootstrapImagesAvailableToClear():
            images_detected = []
            for i in os.listdir(os.path.join(cur_path, "Images")):
                if not i in bootstrap_image_needed_files: images_detected.append(os.path.join(cur_path, "Images", i))
            return images_detected
        def unneededModsAvailableToClear():
            unneeded_detected = []
            for i in os.listdir(os.path.join(mods_folder, "Mods")):
                if os.path.isfile(os.path.join(mods_folder, "Mods", i)): unneeded_detected.append(os.path.join(mods_folder, "Mods", i))
                elif i == "GothamFont": unneeded_detected.append(os.path.join(mods_folder, "Mods", i))
            return unneeded_detected
        def robloxFilesAvailableToClear():
            files = []
            for i in os.listdir(versions_folder):
                if i.endswith(".zip"): files.append(os.path.join(versions_folder, i))
            if main_os == "Darwin" and os.path.exists(os.path.join(cur_path, "Versions")): files.append(os.path.join(cur_path, "Versions"))
            return files
        def getTotalClearableSize(): return getRobloxLogFolderSize(static=True) + getFolderSize(orangeblox_log_path, formatWithAbbreviation=False) + getFileSize(installer_paths, formatWithAbbreviation=False) + getFileSize(pythonCacheAvailableToClear(), formatWithAbbreviation=False) + getFileSize(bootstrapImagesAvailableToClear(), formatWithAbbreviation=False) + getFileSize(unneededModsAvailableToClear(), formatWithAbbreviation=False) + getFileSize(robloxFilesAvailableToClear(), formatWithAbbreviation=False) + getFileSize(appLocksAvailableToClear(), formatWithAbbreviation=False)
        def continueToClearLogs(clearAll=False): # Clear All Roblox Logs
            printWarnMessage("--- Clear All Roblox Logs ---")
            if handler.getIfRobloxIsOpen() == True:
                printErrorMessage("We can't clear logs if Roblox is currently open! Please close it before trying again!")
                input("> ")
                return ts("Clearing Logs failed.")
            else:
                printMainMessage(f"Are you sure you want to clear all Roblox logs ({getRobloxLogFolderSize()}) (y/n)?")
                if clearAll == True or isYes(input("> ")) == True:
                    if handler.getIfRobloxIsOpen() == True:
                        printErrorMessage("We can't clear logs if Roblox is currently open! Please close it before trying again!")
                        input("> ")
                        return ts("Clearing Logs failed.")
                    else:
                        if main_os == "Darwin":
                            log_path = os.path.join(os.path.expanduser("~"), "Library", "Logs", "Roblox")
                            if os.path.exists(log_path):
                                for item in os.listdir(log_path):
                                    item_path = os.path.join(log_path, item)
                                    try:
                                        if os.path.isfile(item_path) or os.path.islink(item_path): os.unlink(item_path)
                                        elif os.path.isdir(item_path): shutil.rmtree(item_path)
                                    except Exception as e: print(f"Error deleting {item_path}: {e}")
                                return ts("Roblox logs has been cleared!")
                            else: return ts("Clearing Logs failed.")
                        elif main_os == "Windows":
                            log_path = os.path.join(RFFI.windows_dir, "logs")
                            if os.path.exists(log_path):
                                for item in os.listdir(log_path):
                                    item_path = os.path.join(log_path, item)
                                    try:
                                        if os.path.isfile(item_path) or os.path.islink(item_path): os.unlink(item_path)
                                        elif os.path.isdir(item_path): shutil.rmtree(item_path)
                                    except Exception as e: print(f"Error deleting {item_path}: {e}")
                                return ts("Roblox logs has been cleared!")
                            else: return ts("Clearing Logs failed.")
                        else: return ts("Clearing Logs failed.")
                else: return ts("Clearing Logs canceled.")
        def continueToClearBootstrapLogs(clearAll=False): # Clear All OrangeBlox Logs
            printWarnMessage("--- Clear All OrangeBlox Logs ---")
            printMainMessage(f"Are you sure you want to clear all OrangeBlox logs ({getFolderSize(orangeblox_log_path)}) (y/n)?")
            if clearAll == True or isYes(input("> ")) == True:
                for i in os.listdir(orangeblox_log_path):
                    try:
                        if os.path.isfile(os.path.join(orangeblox_log_path, i)): os.remove(os.path.join(orangeblox_log_path, i))
                    except Exception as e: printDebugMessage(f"Unable to remove log: {i}")
                return ts("Successfully cleared OrangeBlox logs!")
            else: return ts("Clearing Logs canceled.")
        def continueToClearPyCache(clearAll=False): # Clear Python Cache
            printWarnMessage("--- Clear Python Cache ---")
            printMainMessage(f"Are you sure you want to clear Python cache ({getFileSize(pythonCacheAvailableToClear())}) (y/n)?")
            if clearAll == True or isYes(input("> ")) == True:
                for i in pythonCacheAvailableToClear():
                    if os.path.exists(i): 
                        if os.path.isdir(i): printDebugMessage(f"Removing {i}.."); shutil.rmtree(i, ignore_errors=True)
                        else: printDebugMessage(f"Removing {i}.."); os.remove(i)
                return ts("Successfully cleared Python cache!")
            else: return ts("Clearing cache canceled.")
        def continueToClearRobloxInstallers(clearAll=False): # Clear Roblox Installers
            printWarnMessage("--- Clear Roblox Installers ---")
            printMainMessage(f"Are you sure you want to clear Roblox Installers ({getFileSize(installer_paths)}) (y/n)?")
            if clearAll == True or isYes(input("> ")) == True:
                for i in installer_paths:
                    if os.path.exists(i): printDebugMessage(f"Removing {i}.."); shutil.rmtree(i, ignore_errors=True)
                return ts("Successfully cleared Roblox Installers!")
            else: return ts("Clearing installers canceled.")
        def continueToClearBootstrapImages(clearAll=False): # Clear Bootstrap Images
            printWarnMessage("--- Clear Bootstrap Images ---")
            printMainMessage(f"Are you sure you want to clear Bootstrap images ({getFileSize(bootstrapImagesAvailableToClear())}) (y/n)?")
            if clearAll == True or isYes(input("> ")) == True:
                for i in bootstrapImagesAvailableToClear():
                    if os.path.exists(i): 
                        if os.path.isdir(i): printDebugMessage(f"Removing {i}.."); shutil.rmtree(i, ignore_errors=True)
                        else: printDebugMessage(f"Removing {i}.."); os.remove(i)
                return ts("Successfully cleared Bootstrap Images!")
            else: return ts("Clearing bootstrap images canceled.")
        def continueToClearDownloadedRobloxFiles(clearAll=False): # Clear Downloaded Roblox Files
            printWarnMessage("--- Clear Downloaded Roblox Files ---")
            printMainMessage(f"Are you sure you want to clear downloaded Roblox files from OrangeBlox ({getFileSize(robloxFilesAvailableToClear())}) (y/n)?")
            if clearAll == True or isYes(input("> ")) == True:
                for i in robloxFilesAvailableToClear():
                    if os.path.exists(i): 
                        if os.path.isdir(i): printDebugMessage(f"Removing {i}.."); shutil.rmtree(i, ignore_errors=True)
                        else: printDebugMessage(f"Removing {i}.."); os.remove(i)
                return ts("Successfully cleared Downloaded Roblox Files from OrangeBlox!")
            else: return ts("Clearing files canceled.")
        def continueToClearUnneededMods(clearAll=False): # Clear Unneeded Mods
            printWarnMessage("--- Clear Unneeded Mods ---")
            printMainMessage(f"Are you sure you want to clear unneeded mods ({getFileSize(unneededModsAvailableToClear())}) (y/n)?")
            if clearAll == True or isYes(input("> ")) == True:
                for i in unneededModsAvailableToClear():
                    if os.path.exists(i): 
                        if os.path.isdir(i): printDebugMessage(f"Removing {i}.."); shutil.rmtree(i, ignore_errors=True)
                        else: printDebugMessage(f"Removing {i}.."); os.remove(i)
                return ts("Successfully cleared unneeded mods!")
            else: return ts("Clearing mods canceled.")
        def continueToClearAppLocks(clearAll=False): # Clear App Locks
            printWarnMessage("--- Clear App Locks ---")
            printMainMessage(f"Are you sure you want to clear app locks ({getFileSize(appLocksAvailableToClear())}) (y/n)?")
            if clearAll == True or isYes(input("> ")) == True:
                for i in appLocksAvailableToClear():
                    if os.path.exists(i): 
                        if os.path.isdir(i): printDebugMessage(f"Removing {i}.."); shutil.rmtree(i, ignore_errors=True)
                        else: printDebugMessage(f"Removing {i}.."); os.remove(i)
                return ts("Successfully cleared app locks!")
            else: return ts("Clearing app locks canceled.")
        def continueToClearAllUnneededFiles():
            printWarnMessage("--- Clear All Unneeded Files ---")
            printMainMessage(f"Are you sure you want to clear all unneeded files ({formatSize(getTotalClearableSize())}) (y/n)?")
            printYellowMessage("This just runs all the clear options at once.")
            if isYes(input("> ")) == True:
                continueToClearLogs(clearAll=True)
                continueToClearBootstrapLogs(clearAll=True)
                continueToClearPyCache(clearAll=True)
                continueToClearRobloxInstallers(clearAll=True)
                continueToClearDownloadedRobloxFiles(clearAll=True)
                continueToClearAppLocks(clearAll=True)
                continueToClearUnneededMods(clearAll=True)
                continueToClearBootstrapImages(clearAll=True)
        printWarnMessage("--- Clear Temporary Storage ---")
        printMainMessage(f"Select which option you would like to do! (Total Size of Clearable Files: {formatSize(getTotalClearableSize())})")
        generated_ui_options = []
        generated_ui_options.append({
            "index": 1, 
            "message": ts(f"Clear Roblox Logs ({getRobloxLogFolderSize()})"), 
            "func": continueToClearLogs,
        })
        generated_ui_options.append({
            "index": 2, 
            "message": ts(f"Clear OrangeBlox Logs ({getFolderSize(orangeblox_log_path)})"), 
            "func": continueToClearBootstrapLogs,
        })
        generated_ui_options.append({
            "index": 3, 
            "message": ts(f"Clear Python Cache ({getFileSize(pythonCacheAvailableToClear())})"), 
            "func": continueToClearPyCache,
        })
        generated_ui_options.append({
            "index": 4, 
            "message": ts(f"Clear Roblox Installers ({getFileSize(installer_paths)})"), 
            "func": continueToClearRobloxInstallers,
        })
        generated_ui_options.append({
            "index": 5, 
            "message": ts(f"Clear Downloaded Roblox Files ({getFileSize(robloxFilesAvailableToClear())})"), 
            "func": continueToClearDownloadedRobloxFiles,
        })
        generated_ui_options.append({
            "index": 6, 
            "message": ts(f"Clear App Locks ({getFileSize(appLocksAvailableToClear())})"), 
            "func": continueToClearAppLocks,
        })
        generated_ui_options.append({
            "index": 7, 
            "message": ts(f"Clear Unneeded Mods ({getFileSize(unneededModsAvailableToClear())})"), 
            "func": continueToClearUnneededMods,
        })
        generated_ui_options.append({
            "index": 8, 
            "message": ts(f"Clear Bootstrap Images ({getFileSize(bootstrapImagesAvailableToClear())})"), 
            "func": continueToClearBootstrapImages,
        })
        generated_ui_options.append({
            "index": 9, 
            "message": ts(f"Clear All Unneeded Files"), 
            "func": continueToClearAllUnneededFiles,
        })
        printMainMessage("[*] = Exit Storage Management")
        d = generateMenuSelection(generated_ui_options, star_option=ts("Exit Storage Management"))
        if d: d["func"](); return continueToClearTemporaryStorage()
        else: return ts("Temporary storage has been cleared!")
    def continueToEndRobloxInstances(studio=False): # End All Roblox Instances
        printWarnMessage("--- End All Roblox Instances ---" if studio == False else "--- End All Roblox Studio Instances ---")
        printMainMessage("Are you sure you want to end all currently open Roblox instances? (y/n)"if studio == False else "Are you sure you want to end all currently open Roblox Studio instances? (y/n)")
        a = input("> ")
        if isYes(a) == True:
            handler.endRoblox(studio=studio)
            return ts("Successfully closed all open Roblox windows!")
        else: return ts("Roblox closing task has been canceled!")  
    def continueToInstallRobloxOptions(reinstall=False): # Roblox Installer Options
        def goToReinstall(fullReset=0):
            printWarnMessage("--- Reinstall Roblox ---")
            if fullReset == 8: printMainMessage("Are you sure you want to reinstall Vanilla Roblox Studio? (y/n)")
            elif fullReset == 7: printMainMessage("Are you sure you want to reinstall Vanilla Roblox? (y/n)")
            elif fullReset == 6: printMainMessage("Are you sure you want to reinstall Roblox Studio? (y/n)")
            elif fullReset == 5: printMainMessage("...")
            elif fullReset == 4: printMainMessage("...")
            elif fullReset == 3: printMainMessage("Are you sure you want to fully reinstall Roblox and REMOVE your user data? (y/n)")
            elif fullReset == 2: printMainMessage("Are you sure you want to fully reinstall Roblox? (y/n)")
            else: printMainMessage("Are you sure you want to reinstall Roblox? (y/n)")
            if main_os == "Windows": printYellowMessage("WARNING! This may force-quit any open Roblox windows!")
            a = input("> ")
            if isYes(a) == True:
                if fullReset == 8:
                    cla = handler.temporaryResetCustomizableVariables()
                    submit_status.start()
                    res = handler.installRoblox(studio=True, debug=main_config.get("EFlagEnableDebugMode"), copyRobloxInstallerPath=(main_os == "Darwin" and os.path.join(cur_path, "RobloxStudioInstaller.app") or os.path.join(cur_path, "RobloxStudioInstaller.exe")), downloadInstaller=True, disableRobloxAutoOpen=True, downloadToken=createDownloadToken(studio=True))
                    submit_status.end()
                    cla.set()
                    return (ts("Vanilla Roblox Studio has been installed!") if res and res["success"] == True else ts("Vanilla Roblox Studio has not been installed!"))
                elif fullReset == 7:
                    cla = handler.temporaryResetCustomizableVariables()
                    submit_status.start()
                    res = handler.installRoblox(debug=main_config.get("EFlagEnableDebugMode"), copyRobloxInstallerPath=(main_os == "Darwin" and os.path.join(cur_path, "RobloxPlayerInstaller.app") or os.path.join(cur_path, "RobloxPlayerInstaller.exe")), downloadInstaller=True, disableRobloxAutoOpen=True, downloadToken=createDownloadToken(studio=False))
                    submit_status.end()
                    cla.set()
                    return (ts("Vanilla Roblox has been installed!") if res and res["success"] == True else ts("Vanilla Roblox has not been installed!"))
                elif fullReset == 6:
                    submit_status.start()
                    res = handler.installRoblox(studio=True, debug=main_config.get("EFlagEnableDebugMode"), copyRobloxInstallerPath=(main_os == "Darwin" and os.path.join(cur_path, "RobloxStudioInstaller.app") or os.path.join(cur_path, "RobloxStudioInstaller.exe")), downloadInstaller=True, disableRobloxAutoOpen=True, downloadToken=createDownloadToken(studio=True))
                    submit_status.end()
                    return (ts("Roblox Studio has been reinstalled!") if res and res["success"] == True else ts("Roblox Studio has not been installed!"))
                elif fullReset == 3:
                    submit_status.start()
                    res = handler.reinstallRoblox(debug=(main_config.get("EFlagEnableDebugMode") == True), copyRobloxInstallerPath=(main_os == "Darwin" and os.path.join(cur_path, "RobloxPlayerInstaller.app") or os.path.join(cur_path, "RobloxPlayerInstaller.exe")), clearUserData=True, downloadInstaller=True, disableRobloxAutoOpen=True, downloadToken=createDownloadToken(studio=False))
                    submit_status.end()
                    return (ts("Roblox has been reinstalled fully with user data removed!") if res and res["success"] == True else ts("Roblox has not been installed!"))
                elif fullReset == 2:
                    submit_status.start()
                    res = handler.reinstallRoblox(debug=(main_config.get("EFlagEnableDebugMode") == True), copyRobloxInstallerPath=(main_os == "Darwin" and os.path.join(cur_path, "RobloxPlayerInstaller.app") or os.path.join(cur_path, "RobloxPlayerInstaller.exe")), clearUserData=False, downloadInstaller=True, disableRobloxAutoOpen=True, downloadToken=createDownloadToken(studio=False))
                    submit_status.end()
                    return (ts("Roblox has been reinstalled fully with no user data removed!") if res and res["success"] == True else ts("Roblox has not been installed!"))
                else:
                    submit_status.start()
                    res = handler.installRoblox(debug=(main_config.get("EFlagEnableDebugMode") == True), copyRobloxInstallerPath=(main_os == "Darwin" and os.path.join(cur_path, "RobloxPlayerInstaller.app") or os.path.join(cur_path, "RobloxPlayerInstaller.exe")), downloadInstaller=True, verifyInstall=not (main_config.get("EFlagVerifyRobloxHashAfterInstall")==False), downloadToken=createDownloadToken(studio=False))
                    submit_status.end()
                    return (ts("Roblox has been reinstalled!") if res and res["success"] == True else ts("Roblox has not been installed!"))
            else: return ts("Roblox reinstallation has been canceled!")
        def goToUninstall(fullReset=0):
            printWarnMessage("--- Uninstall Roblox ---")
            if main_os == "Darwin":
                if not (os.path.exists(os.path.join(pip_class.getInstallableApplicationsFolder(), "Roblox.app"))) and fullReset == 7:
                    printErrorMessage("Vanilla Roblox is not installed right now! Please install it from the Roblox website to get it back!")
                    return ts("Roblox was not uninstalled.")
                elif not (os.path.exists(os.path.join(pip_class.getInstallableApplicationsFolder(), "RobloxStudio.app"))) and fullReset == 8:
                    printErrorMessage("Vanilla Roblox Studio is not installed right now! Please install it from the Roblox website to get it back!")
                    return ts("Roblox Studio was not uninstalled.")
            elif main_os == "Windows":
                if not (handler.getRobloxInstallFolder(directory=os.path.join(pip_class.getLocalAppData(), "Roblox", "Versions"))) and fullReset == 7:
                    printErrorMessage("Vanilla Roblox is not installed right now! Please install it from the Roblox website to get it back!")
                    return ts("Roblox was not uninstalled.")
                elif not (handler.getRobloxInstallFolder(directory=os.path.join(pip_class.getLocalAppData(), "Roblox", "Versions"), studio=True)) and fullReset == 8:
                    printErrorMessage("Vanilla Roblox Studio is not installed right now! Please install it from the Roblox website to get it back!")
                    return ts("Roblox Studio was not uninstalled.")
                
            if fullReset == 4: printMainMessage("Are you sure you want to uninstall Roblox? (y/n)")
            elif fullReset == 5: printMainMessage("Are you sure you want to uninstall Roblox and REMOVE your user data? (y/n)")
            elif fullReset == 6: printMainMessage("Are you sure you want to uninstall Roblox Studio from OrangeBlox? (y/n)")
            elif fullReset == 7: printMainMessage("Are you sure you want to uninstall Vanilla Roblox from your system? (y/n)")
            elif fullReset == 8: printMainMessage("Are you sure you want to uninstall Vanilla Roblox Studio from your system? (y/n)")
            else: printMainMessage("Are you sure you want to uninstall Roblox? (y/n)")
            printYellowMessage("WARNING! This will force-quit any open Roblox windows!")
            a = input("> ")
            if isYes(a) == True:
                if fullReset == 5:
                    submit_status.start()
                    handler.uninstallRoblox(debug=(main_config.get("EFlagEnableDebugMode") == True), clearUserData=True)
                    submit_status.end()
                    printSuccessMessage("Roblox has been uninstalled successfully! However, if you don't have vanilla Roblox installed, then you won't be able to play Roblox until you reopen OrangeBlox. Keep a mind at that!")
                    input("> ")
                    sys.exit(0)
                    return ts("Roblox has been uninstalled with user data removed!")
                elif fullReset == 6:
                    if not (handler.getRobloxInstallFolder(directory="", studio=True)):
                        printErrorMessage("Roblox Studio is not installed right now! Please enable Roblox Studio mode in Bootstrap Settings to reinstall back!")
                        return ts("Roblox Studio was not uninstalled.")
                    submit_status.start()
                    handler.uninstallRoblox(studio=True, debug=(main_config.get("EFlagEnableDebugMode") == True), clearUserData=False)
                    submit_status.end()
                    if main_os == "Windows":
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
                            except Exception:
                                return None
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
                            
                        cur_studio = handler.getRobloxInstallFolder(directory=os.path.join(pip_class.getLocalAppData(), "Roblox", "Versions"), studio=True)
                        if cur_studio:
                            rbx_studio_beta = os.path.join(cur_studio, "RobloxStudioBeta.exe")
                            set_url_scheme("roblox-studio", rbx_studio_beta)
                            set_url_scheme("roblox-studio-auth", rbx_studio_beta)
                            set_file_type_reg(".rbxl", rbx_studio_beta, "Roblox Place")
                            set_file_type_reg(".rbxlx", rbx_studio_beta, "Roblox Place")
                    return ts("Roblox Studio has been uninstalled!")
                elif fullReset == 7:
                    if main_os == "Darwin":
                        if not (os.path.exists(os.path.join(pip_class.getInstallableApplicationsFolder(), "Roblox.app"))):
                            printErrorMessage("Vanilla Roblox is not installed right now! Please install it from the Roblox website to get it back!")
                            return ts("Roblox was not uninstalled.")
                        shutil.rmtree(os.path.join(pip_class.getInstallableApplicationsFolder(), "Roblox.app"), ignore_errors=True)
                        printSuccessMessage("Vanilla Roblox has been uninstalled successfully!")
                        input("> ")
                        return ts("Vanilla Roblox has been uninstalled!")
                    elif main_os == "Windows":
                        org_dir = os.path.join(pip_class.getLocalAppData(), "Roblox", "Versions")
                        if not (handler.getRobloxInstallFolder(directory=org_dir)):
                            printErrorMessage("Vanilla Roblox is not installed right now! Please install it from the Roblox website to get it back!")
                            return ts("Roblox was not uninstalled.")
                        for i in os.listdir(org_dir):
                            if os.path.exists(os.path.join(org_dir, i)) and os.path.isdir(os.path.join(org_dir, i)):
                                if os.path.exists(os.path.join(org_dir, i, "RobloxPlayerBeta.exe")):     shutil.rmtree(os.path.join(org_dir, i), ignore_errors=True)
                        printSuccessMessage("Vanilla Roblox has been uninstalled successfully!")
                        input("> ")
                        return ts("Vanilla Roblox has been uninstalled!")
                elif fullReset == 8:
                    if main_os == "Darwin":
                        if not (os.path.exists(os.path.join(pip_class.getInstallableApplicationsFolder(), "RobloxStudio.app"))):
                            printErrorMessage("Vanilla Roblox Studio is not installed right now! Please install it from the Roblox website to get it back!")
                            return ts("Roblox Studio was not uninstalled.")
                        shutil.rmtree(os.path.join(pip_class.getInstallableApplicationsFolder(), "RobloxStudio.app"), ignore_errors=True)
                        printSuccessMessage("Vanilla Roblox Studio has been uninstalled successfully!")
                        input("> ")
                        return ts("Vanilla Roblox Studio has been uninstalled!")
                    elif main_os == "Windows":
                        org_dir = os.path.join(pip_class.getLocalAppData(), "Roblox", "Versions")
                        if not (handler.getRobloxInstallFolder(directory=org_dir, studio=True)):
                            printErrorMessage("Vanilla Roblox Studio is not installed right now! Please install it from the Roblox website to get it back!")
                            return ts("Roblox Studio was not uninstalled.")
                        for i in os.listdir(org_dir):
                            if os.path.exists(os.path.join(org_dir, i)) and os.path.isdir(os.path.join(org_dir, i)):
                                if os.path.exists(os.path.join(org_dir, i, "RobloxStudioBeta.exe")):     shutil.rmtree(os.path.join(org_dir, i), ignore_errors=True)
                        printSuccessMessage("Vanilla Roblox Studio has been uninstalled successfully!")
                        input("> ")
                        return ts("Vanilla Roblox Studio has been uninstalled!")
                else:
                    submit_status.start()
                    handler.uninstallRoblox(debug=(main_config.get("EFlagEnableDebugMode") == True), clearUserData=False)
                    submit_status.end()
                    printSuccessMessage("Roblox has been uninstalled successfully! However, if you don't have vanilla Roblox installed, then you won't be able to play Roblox until you reopen OrangeBlox. Keep a mind at that!")
                    input("> ")
                    sys.exit(0)
                    return ts("Roblox has been uninstalled!")
            else: return ts("Roblox reinstallation has been canceled!")
        if reinstall == True: return goToReinstall()
        else:
            printWarnMessage("--- Roblox Installer Options ---")
            li = {}
            co = 1
            printMainMessage(f"[{co}] = Reinstall Roblox")
            li[str(co)] = [goToReinstall, 1]
            co += 1
            printMainMessage(f"[{co}] = Full Reinstall Roblox [No Resetting]")
            li[str(co)] = [goToReinstall, 2]
            co += 1
            printMainMessage(f"[{co}] = Full Reinstall Roblox [Removes User Data]")
            li[str(co)] = [goToReinstall, 3]
            co += 1
            printMainMessage(f"[{co}] = Install Vanilla Roblox")
            li[str(co)] = [goToReinstall, 7]
            if main_config.get("EFlagRobloxStudioEnabled"):
                co += 1
                printMainMessage(f"[{co}] = Reinstall Roblox Studio")
                li[str(co)] = [goToReinstall, 6]
                if main_os == "Darwin":
                    co += 1
                    printMainMessage(f"[{co}] = Install Vanilla Roblox Studio")
                    li[str(co)] = [goToReinstall, 8]
                    if os.path.exists(os.path.join(pip_class.getInstallableApplicationsFolder(), "RobloxStudio.app")): 
                        co += 1
                        printMainMessage(f"[{co}] = Uninstall Vanilla Roblox Studio")
                        li[str(co)] = [goToUninstall, 8]
                elif main_os == "Windows":
                    co += 1
                    printMainMessage(f"[{co}] = Install Vanilla Roblox Studio")
                    li[str(co)] = [goToReinstall, 8]
                    if handler.getRobloxInstallFolder(directory=os.path.join(pip_class.getLocalAppData(), "Roblox", "Versions"), studio=True): 
                        co += 1
                        printMainMessage(f"[{co}] = Uninstall Vanilla Roblox Studio")
                        li[str(co)] = [goToUninstall, 8]
            co += 1
            printMainMessage(f"[{co}] = Uninstall Roblox")
            li[str(co)] = [goToUninstall, 4]
            co += 1
            printMainMessage(f"[{co}] = Uninstall Roblox [Removes User Data]")
            li[str(co)] = [goToUninstall, 5]
            current_studio_version = handler.getCurrentClientVersion(studio=True)
            if current_studio_version["success"] == True:
                co += 1
                printMainMessage(f"[{co}] = Uninstall Roblox Studio")
                li[str(co)] = [goToUninstall, 6]
            if main_os == "Darwin":
                if os.path.exists(os.path.join(pip_class.getInstallableApplicationsFolder(), "Roblox.app")): 
                    co += 1
                    printMainMessage(f"[{co}] = Uninstall Vanilla Roblox")
                    li[str(co)] = [goToUninstall, 7]
            elif main_os == "Windows":
                if handler.getRobloxInstallFolder(directory=os.path.join(pip_class.getLocalAppData(), "Roblox", "Versions")): 
                    co += 1
                    printMainMessage(f"[{co}] = Uninstall Vanilla Roblox")
                    li[str(co)] = [goToUninstall, 7]
            printMainMessage("[*] = Exit Options Menu")
            a = input("> ")
            if li.get(a): return li.get(a)[0](li.get(a)[1])
            else: return ts("Option invalid!")
    def syncToFFlagConfiguration(): # Sync to Configuration
        printWarnMessage("--- Sync to Configuration ---")
        printMainMessage(f"Are you sure you want to save your Configuration into the Configuration.json file in your installation folder (y/n)?")
        a = input("> ")
        if isYes(a) == True:
            global main_config
            printMainMessage("Validating Bootstrap Install Directory..")
            if (main_config.get("EFlagOrangeBloxSyncDir") and os.path.exists(main_config.get("EFlagOrangeBloxSyncDir"))):
                if os.path.exists(os.path.join(main_config.get("EFlagOrangeBloxSyncDir"), "Configuration.json")):
                    with open(os.path.join(main_config.get("EFlagOrangeBloxSyncDir"), "Configuration.json"), "w", encoding="utf-8") as f: json.dump(main_config, f, indent=4)
                    printSuccessMessage("Successfully synced Bootstrap Settings!")
                    return ts("Successfully synced settings!")
                else:
                    printErrorMessage("Bootstrap Sync is not supported since the original unextracted directory is not found.")
                    return ts("Syncing has failed!")
            else:
                printErrorMessage("Bootstrap Sync is not supported since the original unextracted directory is not found.")
                return ts("Syncing has failed!")
        else:
            printDebugMessage("Syncing was rejected by the user!")
            return ts("Syncing was rejected!")
    def syncFromFFlagConfiguration(): # Sync from Fast Flag Configuration
        printWarnMessage("--- Sync from Configuration ---")
        printMainMessage(f"Are you sure you want to load your Configuration from the Configuration.json file in your installation folder (y/n)?")
        printErrorMessage("This will override any configuration changes inside this state to this file.")
        a = input("> ")
        if isYes(a) == True:
            global main_config
            printMainMessage("Validating Bootstrap Install Directory..")
            if (main_config.get("EFlagOrangeBloxSyncDir") and os.path.exists(main_config.get("EFlagOrangeBloxSyncDir"))):
                if os.path.exists(os.path.join(main_config.get("EFlagOrangeBloxSyncDir"), "Configuration.json")):
                    with open(os.path.join(main_config.get("EFlagOrangeBloxSyncDir"), "Configuration.json"), "r", encoding="utf-8") as f: fromFastFlagConfig = json.load(f)
                    if len(fromFastFlagConfig) < 10:
                        printYellowMessage(f"This configuration contains less than 10 items. Are you REALLY sure that you want to sync with this file? (y/n)?")
                        printErrorMessage("This can make you lose existing data on this bootstrap which could affect your experience.")
                        if isYes(input("> ")) == False: return ts("Syncing was rejected!")
                    fromFastFlagConfig["EFlagOrangeBloxSyncDir"] = main_config.get("EFlagOrangeBloxSyncDir")
                    main_config = fromFastFlagConfig
                    saveSettings()
                    printSuccessMessage("Successfully synced Bootstrap Settings!")
                    return ts("Successfully synced settings!")
                else:
                    printErrorMessage("Bootstrap Sync is not supported since the original unextracted directory is not found.")
                    return ts("Syncing has failed!")
            else:
                printErrorMessage("Bootstrap Sync is not supported since the original unextracted directory is not found.")
                return ts("Roblox closing task has been canceled!")
        else:
            printDebugMessage("Syncing was rejected by the user!")
            return ts("Syncing was rejected!")
    def continueToSettings(): # Open Settings
        def mainSettings():
            generated_ui_options = []
            def handleBasicSetting(fflag, default, ex=True):
                printMainMessage(f'Current Setting: {(main_config.get(fflag, default)==ex)}')
                d = input("> ")
                if isYes(d) == True:
                    main_config[fflag] = True
                    printDebugMessage("User selected: True")
                elif isRequestClose(d) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
                elif isNo(d) == True:
                    main_config[fflag] = False
                    printDebugMessage("User selected: False")
            def robloxSettings():
                printWarnMessage("--- Roblox Settings ---")
                global main_config
                printMainMessage("Would you like to enable using Roblox Studio with OrangeBlox? (y/n)")
                d = handleBasicSetting("EFlagRobloxStudioEnabled", False)
                if d: return d

                printMainMessage("Would you like to allow duplication of Roblox Clients? (y/n)")
                printMainMessage(f'Current Setting: {main_config.get("EFlagEnableDuplicationOfClients", False)==True}')
                c = input("> ")
                if isYes(c) == True:
                    main_config["EFlagEnableDuplicationOfClients"] = True
                    printDebugMessage("User selected: True")
                    printYellowMessage("Notes to keep track of:")
                    printYellowMessage("1. Make sure all currently open instances are fully loaded in a game before going to an another account.")
                    printYellowMessage("2. If you get teleported or kicked out, you may teleport into the current logged in Roblox account stored which may be the last logged in account.")
                    printYellowMessage("3. After Roblox versions 0.677+, Roblox has issued a new patch on multi-instancing that closes Roblox after a certain unknown time.")
                    printYellowMessage("4. Multi-Instances may be deflicted depending if one of your accounts are assigned to a different Roblox version.")
                elif isRequestClose(c) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
                elif isNo(c) == True:
                    main_config["EFlagEnableDuplicationOfClients"] = False
                    printDebugMessage("User selected: False")

                if main_os == "Darwin":
                    printMainMessage("Would you like to remove the Dock shortcut that Roblox automatically adds? (y/n)")
                    d = handleBasicSetting("EFlagRemoveRobloxAppDockShortcut", False)
                    if d: return d

                printMainMessage("Would you like to reinstall a fresh copy of Roblox every launch? (y/n)")
                d = handleBasicSetting("EFlagFreshCopyRoblox", False)
                if d: return d

                printMainMessage("Would you like to set the URL Schemes for the Roblox Client and OrangeBlox? [Needed for Roblox Link Shortcuts and when Roblox updates] (y/n)")
                d = handleBasicSetting("EFlagDisableURLSchemeInstall", False, False)
                if d: return d

                printMainMessage("Would you like to set start arguments for Roblox Player? (y/n)")
                printMainMessage(f'Current Setting: {(main_config.get("EFlagRobloxPlayerArguments"))}')
                d = input("> ")
                if isYes(d) == True:
                    printMainMessage("Input the start arguments to use when running Roblox!")
                    main_config["EFlagRobloxPlayerArguments"] = input("> ")
                    printDebugMessage(f'User selected: {main_config.get("EFlagRobloxPlayerArguments")}')
                elif isRequestClose(d) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
                elif isNo(d) == True:
                    main_config["EFlagRobloxPlayerArguments"] = None
                    printDebugMessage("User selected: None")

                if main_config.get("EFlagRobloxStudioEnabled") == True:
                    printMainMessage("Would you like to set start arguments for Roblox Studio? (y/n)")
                    printMainMessage(f'Current Setting: {(main_config.get("EFlagRobloxStudioArguments"))}')
                    d = input("> ")
                    if isYes(d) == True:
                        printMainMessage("Input the start arguments to use when running Roblox Studio!")
                        main_config["EFlagRobloxStudioArguments"] = input("> ")
                        printDebugMessage(f'User selected: {main_config.get("EFlagRobloxStudioArguments")}')
                    elif isRequestClose(d) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
                    elif isNo(d) == True:
                        main_config["EFlagRobloxStudioArguments"] = None
                        printDebugMessage("User selected: None")

                printMainMessage("Would you like to enable Roblox Unfriend Checks? (y/n)")
                printYellowMessage("Warning! This may take way too long time due to Roblox ratelimits.")
                d = handleBasicSetting("EFlagRobloxUnfriendCheckEnabled", False)
                if d: return d

                printMainMessage("Would you like to enable install Fast Flags using the IXP Settings method? (y/n)")
                printYellowMessage("Warning! This method may be patched in future updates. Also, flags may collide with Roblox Studio.")
                printYellowMessage("This is the only method that is found to be usable to add fast flags using files.")
                printErrorMessage("HOWEVER, it can be bannable by Roblox for trying to bypass this. WE WONT BE RESPONSIBLE AFTER THIS POINT!")
                d = handleBasicSetting("EFlagUseIXPFastFlagsMethod2", False)
                if d: return d

                printMainMessage("Would you like to enable Roblox Security Cookie Usage? (y/n)")
                printYellowMessage("This is used for authentication with Roblox APIs such as Beta Programs.")
                printYellowMessage("Warning! This option will look for cookies automatically in your Roblox Data and may bring security issues.")
                d = handleBasicSetting("EFlagRobloxSecurityCookieUsage", False)
                if d: return d

                if main_config.get("EFlagRobloxUnfriendCheckEnabled") == True:
                    def req_int():
                        printMainMessage("Please enter your Roblox User ID to detect for unfriends!")
                        printMainMessage("If you don't want to enter a specific User ID, enter nothing to detect the current logged in user.")
                        re_in = input("> ")
                        if safeConvertNumber(re_in):
                            return re_in
                        elif re_in == "":
                            glob_settings = handler.getRobloxAppSettings()
                            if glob_settings.get("loggedInUser") and glob_settings.get("loggedInUser").get("id"):
                                return int(glob_settings.get("loggedInUser").get("id"))
                            else:
                                return req_int()
                        else:
                            return req_int()
                    if main_config.get("EFlagRobloxUnfriendCheckUserID"):
                        printMainMessage("Would you like to change your Roblox User ID for Unfriend Checks? (y/n)")
                        printMainMessage(f'Current Setting: {(main_config.get("EFlagRobloxUnfriendCheckUserID"))}')
                        d = input("> ")
                        if isYes(d) == True:
                            main_config["EFlagRobloxUnfriendCheckUserID"] = req_int()
                            printDebugMessage("User selected: True")
                        elif isRequestClose(d) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
                    else: main_config["EFlagRobloxUnfriendCheckUserID"] = req_int()

                if main_os == "Darwin":
                    printMainMessage("Would you like to enable Quick Modification mode? (y/n)")
                    printMainMessage("Quick Modification mode is an option to move the preparation process and Mod Script scripts to the background when you load from the webbrowser or when Roblox is currently active.")
                    printMainMessage(f'Current Setting: {(main_config.get("EFlagEnableSkipModificationMode")==True)}')
                    printYellowMessage("This may allow you to load Roblox faster but may still cause issues.")
                    printYellowMessage("This will only apply to Roblox Player and not Roblox Studio.")
                    d = input("> ")
                    if isYes(d) == True:
                        main_config["EFlagEnableSkipModificationMode"] = True
                        printDebugMessage("User selected: True")
                    elif isRequestClose(d) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
                    elif isNo(d) == True:
                        main_config["EFlagEnableSkipModificationMode"] = False
                        printDebugMessage("User selected: False")

                printMainMessage("Would you like to disable Roblox Reinstall checks? (y/n)")
                printMainMessage("This may ignore when a Roblox reinstall is needed due to signing.")
                d = handleBasicSetting("EFlagDisableRobloxReinstallNeededChecks", False)
                if d: return d

                if main_config.get("EFlagEnableDuplicationOfClients") == True:
                    printMainMessage("Would you like to enable Auto Reconnection for Multi-Instancing? (y/n)")
                    d = handleBasicSetting("EFlagEnableMultiAutoReconnect", False)
                    if d: return d
                
                if main_config.get("EFlagRobloxStudioEnabled") == True:
                    printMainMessage("Would you like to enable limiting Localized Studio Documentations to English (United States)? (Select your Roblox language to English (US) for this) (y/n)")
                    printMainMessage(f'Current Setting: {(main_config.get("EFlagLimitAPIDocsLocalization")=="en-us")}')
                    d = input("> ")
                    if isYes(d) == True:
                        main_config["EFlagLimitAPIDocsLocalization"] = "en-us"
                        printDebugMessage(f'User selected: {main_config.get("EFlagLimitAPIDocsLocalization")}')
                    elif isRequestClose(d) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
                    elif isNo(d) == True:
                        main_config["EFlagLimitAPIDocsLocalization"] = None
                        printDebugMessage("User selected: None")
                    printMainMessage("Would you like to enable deleting localized Studio fonts? (y/n)")
                    d = handleBasicSetting("EFlagOverwriteUnneededStudioFonts", False)
                    if d: return d
            def globalSettings():
                global main_config
                global current_global_setting_type
                printWarnMessage("--- Global Setting Modifications ---")
                printMainMessage("Welcome to the Roblox Global Settings menu! Select a setting to modify.")
                printYellowMessage("WARNING! There may be issues when setting this and values set may get reset by the client.")
                basic_settings = handler.getRobloxGlobalBasicSettings(studio=current_global_setting_type)
                if basic_settings["success"] == True:
                    global_settings = basic_settings["data"]
                    generated_basic_ui_options = []
                    cou = 0
                    for i, v in global_settings.items():
                        cou += 1
                        generated_basic_ui_options.append({
                            "index": cou, 
                            "message": f"{i} [{v['type']}] [CUR: {v['data']}]",
                            "data": [i, v]
                        })
                    generated_basic_ui_options.append({
                        "index": 99999, 
                        "message": ts(f"Switch to {'Studio' if current_global_setting_type == False else 'Player'}"),
                        "data": 69420
                    })
                    basic_selected_data = generateMenuSelection(generated_basic_ui_options, star_option=ts("Exit Global Settings Menu"))
                    if basic_selected_data:
                        if basic_selected_data.get("data") == 69420:
                            current_global_setting_type = not current_global_setting_type
                            globalSettings()
                        else:
                            var_data = basic_selected_data.get("data")
                            printMainMessage(f"Enter the value the setting \"{var_data[0]}\" should be:")
                            printMainMessage(f"Current Value: {var_data[1]['data']}")
                            if var_data[1]["type"] == "Vector2": printYellowMessage("For Vector2 values, input in this format: (x,y)")
                            def testVar(tex: str):
                                if var_data[1]["type"] == "bool": return isYes(tex)==True
                                elif var_data[1]["type"] == "string": return tex
                                elif var_data[1]["type"] == "token": return int(tex)
                                elif var_data[1]["type"] == "int": return int(tex)
                                elif var_data[1]["type"] == "float": return float(tex)
                                elif var_data[1]["type"] == "BinaryString": return tex
                                elif var_data[1]["type"] == "SecurityCapabilities": return int(tex)
                                elif var_data[1]["type"] == "Vector2":
                                    match = re.match(r"\((\-?\d+\.?\d*),\s*(\-?\d+\.?\d*)\)", tex)
                                    if match: return (float(match.group(1)), float(match.group(2)))
                                elif var_data[1]["type"] == "int64": return int(tex)
                                else: return None
                            try:
                                inputted_val = input("> ")
                                exported_val = testVar(inputted_val)
                                printDebugMessage(f"Saving new value: {exported_val}")
                                var_data[1]["data"] = exported_val
                                global_settings[var_data[0]] = var_data[1]
                                submit_status.start()
                                handler.installGlobalBasicSettings(global_settings, debug=main_config.get("EFlagEnableDebugMode")==True, studio=current_global_setting_type, endRobloxInstances=False)
                                submit_status.end()
                                globalSettings()
                            except:
                                printDebugMessage("Unable to format to a suitable value due to an error.")
                                globalSettings()
                    else:
                        printMainMessage("Exiting Global Settings Menu..")
                        return
                else: printErrorMessage(f"Unable to load current global settings.")
            def activityTracking():
                printWarnMessage("--- Activity Tracking ---")
                global main_config
                printMainMessage("Would you like to allow Activity Tracking on the Roblox client? (y/n)")
                printMainMessage("This will allow features like:")
                printMainMessage("- Server Locations")
                printMainMessage("- Multiple Instances")
                printMainMessage("- Discord Presence (+ BloxstrapRPC support)")
                printMainMessage("- Discord Webhooks")
                printMainMessage("- Mod Scripts")
                d = handleBasicSetting("EFlagAllowActivityTracking", True)
                if d: return d

                if not (main_config.get("EFlagAllowActivityTracking") == False):
                    printMainMessage("Would you like to enable Server Locations? (y/n)")
                    d = handleBasicSetting("EFlagNotifyServerLocation", False)
                    if d: return d

                    printMainMessage("Would you like to enable Discord RPC? (y/n)")
                    d = handleBasicSetting("EFlagEnableDiscordRPC", False)
                    if d: return d

                    if main_config.get("EFlagEnableDiscordRPC") == True:
                        printMainMessage("Would you like to enable joining from your Discord profile? (Everyone will be allowed to join depending on type of server.)")
                        d = handleBasicSetting("EFlagEnableDiscordRPCJoining", False)
                        if d: return d

                        printMainMessage("Would you like to enable showing your account's profile picture on the small image for default?")
                        d = handleBasicSetting("EFlagShowUserProfilePictureInsteadOfLogo", False)
                        if d: return d

                        printMainMessage("Would you like to enable showing your account's username in the small image for default?")
                        d = handleBasicSetting("EFlagShowUsernameInSmallImage", False)
                        if d: return d

                        printMainMessage("Would you like to enable games to use the Bloxstrap SDK? (y/n)")
                        d = handleBasicSetting("EFlagAllowBloxstrapSDK", False)
                        if d: return d

                        printMainMessage("Would you like to enable Idling Roblox RPC? (y/n)")
                        d = handleBasicSetting("EFlagEnableDefaultDiscordRPC", True)
                        if d: return d

                        printMainMessage("Would you like to enable showing playing game name in Status Bar? (y/n)")
                        printYellowMessage("This option requires pypresence v4.7.0+ to be installed")
                        d = handleBasicSetting("EFlagShowGameNameInStatusBar", False)
                        if d: return d

                        printMainMessage("Would you like to enable showing Editing Studio Game Name in Status Bar? (y/n)")
                        printYellowMessage("This option requires pypresence v4.7.0+ to be installed")
                        d = handleBasicSetting("EFlagShowStudioGameNameInStatusBar", False)
                        if d: return d

                        if main_config.get("EFlagRobloxStudioEnabled") == True:
                            printMainMessage("Would you like to enable Roblox Studio to use the Bloxstrap SDK? (y/n)")
                            d = handleBasicSetting("EFlagAllowBloxstrapStudioSDK", False)
                            if d: return d

                        printMainMessage("Would you like to enable access to private servers you connect to from Discord Presences? (users may be able to join or not) (y/n)")
                        d = handleBasicSetting("EFlagAllowPrivateServerJoining", False)
                        if d: return d

                    printMainMessage("Would you like to use a Discord Webhook? (link required) (y/n)")
                    printMainMessage(f'Current Setting: {(main_config.get("EFlagUseDiscordWebhook", False)==True)}')
                    d = input("> ")
                    if isYes(d) == True:
                        main_config["EFlagUseDiscordWebhook"] = True
                        printDebugMessage("User selected: True")
                        printMainMessage("Please enter your Discord Webhook Link here (https://discord.com/api/webhooks/XXXXXXX/XXXXXXX): ")
                        d = input("> ")
                        if d.startswith("https://discord.com/api/webhooks/"):
                            printDebugMessage("URL passed test.")
                            main_config["EFlagDiscordWebhookURL"] = d
                    elif isRequestClose(d) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
                    elif isNo(d) == True:
                        main_config["EFlagUseDiscordWebhook"] = False
                        printDebugMessage("User selected: False")
                    if main_config.get("EFlagDiscordWebhookURL", "").startswith("https://discord.com/api/webhooks/"):
                        printMainMessage("Enter your Discord User ID to ping you when a new notification is made (you will need Discord Developer Mode enabled in order to copy):")
                        printMainMessage(f'Current Setting: {(main_config.get("EFlagDiscordWebhookUserId"))}')
                        d = input("> ")
                        if safeConvertNumber(d): main_config["EFlagDiscordWebhookUserId"] = d
                        if safeConvertNumber(main_config.get("EFlagDiscordWebhookUserId", "")):
                            max_setti = 6
                            co = 1
                            if main_config.get("EFlagRobloxStudioEnabled") == True: max_setti += 2
                            printMainMessage("What should this Discord Webhook send?")
                            printMainMessage(f"[{co}/{max_setti}] Roblox Connecting Information (y/n)")
                            printMainMessage("When you join a Roblox game (or edit a Roblox Studio game), your webhook gets pinged with information such as Server Location and Joining Link.")
                            printMainMessage(f'Current Setting: {(main_config.get("EFlagDiscordWebhookConnect")==True)}')
                            d = input("> ")
                            if isYes(d) == True:
                                main_config["EFlagDiscordWebhookConnect"] = True
                                printDebugMessage("User selected: True")
                            elif isNo(d) == True:
                                main_config["EFlagDiscordWebhookConnect"] = False
                                printDebugMessage("User selected: False")
                            co += 1
                            printMainMessage(f"[{co}/{max_setti}] Roblox Disconnecting Information (y/n)")
                            printMainMessage("When you leave a Roblox game (or leave a Roblox Studio session), your webhook gets pinged with information such as Server Location and Joining Link.")
                            printMainMessage(f'Current Setting: {(main_config.get("EFlagDiscordWebhookDisconnect")==True)}')
                            d = input("> ")
                            if isYes(d) == True:
                                main_config["EFlagDiscordWebhookDisconnect"] = True
                                printDebugMessage("User selected: True")
                            elif isNo(d) == True:
                                main_config["EFlagDiscordWebhookDisconnect"] = False
                                printDebugMessage("User selected: False")
                            co += 1
                            printMainMessage(f"[{co}/{max_setti}] Roblox Opening Information (y/n)")
                            printMainMessage("When you open Roblox (or Roblox Studio), your webhook gets pinged with information such as Process ID and Log File Location.")
                            printMainMessage(f'Current Setting: {(main_config.get("EFlagDiscordWebhookRobloxAppStart")==True)}')
                            d = input("> ")
                            if isYes(d) == True:
                                main_config["EFlagDiscordWebhookRobloxAppStart"] = True
                                printDebugMessage("User selected: True")
                            elif isNo(d) == True:
                                main_config["EFlagDiscordWebhookRobloxAppStart"] = False
                                printDebugMessage("User selected: False")
                            co += 1
                            printMainMessage(f"[{co}/{max_setti}] Roblox Closing Information (y/n)")
                            printMainMessage("When you close Roblox (or Roblox Studio), your webhook gets pinged with information such as Process ID and Log File Location.")
                            printMainMessage(f'Current Setting: {(main_config.get("EFlagDiscordWebhookRobloxAppClose")==True)}')
                            d = input("> ")
                            if isYes(d) == True:
                                main_config["EFlagDiscordWebhookRobloxAppClose"] = True
                                printDebugMessage("User selected: True")
                            elif isNo(d) == True:
                                main_config["EFlagDiscordWebhookRobloxAppClose"] = False
                                printDebugMessage("User selected: False")
                            co += 1
                            printMainMessage(f"[{co}/{max_setti}] Roblox Crashing Information (y/n)")
                            printMainMessage("When Roblox (or Roblox Studio) crashes, your webhook gets pinged with the console log that shows the cause of the crash.")
                            printMainMessage(f'Current Setting: {(main_config.get("EFlagDiscordWebhookRobloxCrash")==True)}')
                            d = input("> ")
                            if isYes(d) == True:
                                main_config["EFlagDiscordWebhookRobloxCrash"] = True
                                printDebugMessage("User selected: True")
                            elif isNo(d) == True:
                                main_config["EFlagDiscordWebhookRobloxCrash"] = False
                                printDebugMessage("User selected: False")
                            co += 1
                            printMainMessage(f"[{co}/{max_setti}] BloxstrapRPC Information (y/n)")
                            printMainMessage("When BloxstrapRPC is triggered (if enabled), your webhook gets pinged with the changes given from the launched game.")
                            printMainMessage(f'Current Setting: {(main_config.get("EFlagDiscordWebhookBloxstrapRPC")==True)}')
                            d = input("> ")
                            if isYes(d) == True:
                                main_config["EFlagDiscordWebhookBloxstrapRPC"] = True
                                printDebugMessage("User selected: True")
                            elif isNo(d) == True:
                                main_config["EFlagDiscordWebhookBloxstrapRPC"] = False
                                printDebugMessage("User selected: False")
                            if main_config.get("EFlagRobloxStudioEnabled") == True:
                                co += 1
                                printMainMessage(f"[{co}/{max_setti}] Publishing Game Information (y/n)")
                                printMainMessage("When you publish a game from Roblox Studio, your webhook gets pinged with game information such as Server Location and Editing Link.")
                                printMainMessage(f'Current Setting: {(main_config.get("EFlagDiscordWebhookGamePublished")==True)}')
                                d = input("> ")
                                if isYes(d) == True:
                                    main_config["EFlagDiscordWebhookGamePublished"] = True
                                    printDebugMessage("User selected: True")
                                elif isNo(d) == True:
                                    main_config["EFlagDiscordWebhookGamePublished"] = False
                                    printDebugMessage("User selected: False")
                                co += 1
                                printMainMessage(f"[{co}/{max_setti}] Saving Game Information (y/n)")
                                printMainMessage("When you save a game from Roblox Studio, your webhook gets pinged with game information such as Server Location and Editing Link.")
                                printMainMessage(f'Current Setting: {(main_config.get("EFlagDiscordWebhookGameSaved")==True)}')
                                d = input("> ")
                                if isYes(d) == True:
                                    main_config["EFlagDiscordWebhookGameSaved"] = True
                                    printDebugMessage("User selected: True")
                                elif isNo(d) == True:
                                    main_config["EFlagDiscordWebhookGameSaved"] = False
                                    printDebugMessage("User selected: False")
                            printMainMessage("Would you like it to show the pid number in the webhook footer? (y/n)")
                            printMainMessage(f'Current Setting: {(main_config.get("EFlagDiscordWebhookShowPidInFooter")==True)}')
                            d = input("> ")
                            if isYes(d) == True:
                                main_config["EFlagDiscordWebhookShowPidInFooter"] = True
                                printDebugMessage("User selected: True")
                            elif isNo(d) == True:
                                main_config["EFlagDiscordWebhookShowPidInFooter"] = False
                                printDebugMessage("User selected: False")
                    else:
                        main_config["EFlagUseDiscordWebhook"] = False
                        printErrorMessage("The provided webhook link is not a valid format.")

                    if main_config.get("EFlagRobloxStudioEnabled") == True:
                        printMainMessage("Would you like to enable force reconnection when you disconnect from a Studio server? (y/n)")
                        d = handleBasicSetting("EFlagForceReconnectOnStudioLost", False)
                        if d: return d

                    if main_os == "Windows":
                        printMainMessage("Would you like to enable showing the Account Name in the Roblox title window? (y/n)")
                        d = handleBasicSetting("EFlagShowRunningAccountNameInTitle", False)
                        if d: return d
                        if not (main_config.get("EFlagShowRunningAccountNameInTitle") == True):
                            printMainMessage("Would you like to enable showing the Game Name in the Roblox title window instead? (y/n)")
                            d = handleBasicSetting("EFlagShowRunningGameInTitle", False)
                            if d: return d
                        else:
                            printMainMessage("Would you like to like to include the Display Name as apart of the title? (y/n)")
                            d = handleBasicSetting("EFlagShowDisplayNameInTitle", False)
                            if d: return d
            def bootstrapSettings():
                printWarnMessage("--- Bootstrap Settings ---")
                global main_config
                if os.path.exists(os.path.join(cur_path, "Translations")):
                    printMainMessage("Select your bootstrap language:")
                    langs_sel = []
                    co = 0
                    for i, v in language_names.items():
                        co += 1
                        langs_sel.append({
                            "index": co,
                            "message": v,
                            "code": i
                        })
                    selected_language = generateMenuSelection(langs_sel, before_input=ts(f"Current Language: {language_names[main_config.get('EFlagSelectedBootstrapLanguage', 'en')]}\n[WARNING! All messages are translated from Google Translate and may provide incorrect or malformed information.]"))
                    if selected_language:
                        main_config["EFlagSelectedBootstrapLanguage"] = selected_language["code"]
                        stdout.translation_obj.load_new_language(selected_language["code"])
                        printMainMessage(f"Successfully set language to {language_names[main_config.get('EFlagSelectedBootstrapLanguage', 'en')]}! All future messages are now translated in this language.")
                current_rebuilder = None
                if main_config.get("EFlagRebuildPyinstallerAppFromSourceDuringUpdates")==True: current_rebuilder = "Pyinstaller"
                elif main_config.get("EFlagRebuildNuitkaAppFromSourceDuringUpdates")==True: current_rebuilder = "Nuitka"
                printMainMessage("Would you like to enable rebuilding the OrangeBlox main loader? If so, what builder should it use? (y/n)")
                printMainMessage("[1] = Pyinstaller")
                printMainMessage("[2] = Nuitka [CAN TAKE A WHILE]")
                printMainMessage("[n] = None")
                printMainMessage(f'Current Setting: {current_rebuilder}')
                printYellowMessage("In order to use Pyinstaller, the module is needed to be installed.")
                printYellowMessage("In order to use Nuitka, the module and a C compiler is needed to be installed.")
                if main_os == "Darwin": printYellowMessage("For macOS users, it is suggested to install Xcode Command Line Tools from the official Apple website."); printYellowMessage("https://developer.apple.com/xcode/resources/")
                elif main_os == "Windows": printYellowMessage("For Windows, it is required to use Microsoft Visual Code 2022 compilation for using Nuitka."); printYellowMessage("https://nuitka.net/user-documentation/user-manual.html")
                a = input("> ")
                if a == "1":
                    main_config["EFlagRebuildPyinstallerAppFromSourceDuringUpdates"] = True
                    main_config["EFlagRebuildNuitkaAppFromSourceDuringUpdates"] = False
                elif a == "2":
                    main_config["EFlagRebuildPyinstallerAppFromSourceDuringUpdates"] = False
                    main_config["EFlagRebuildNuitkaAppFromSourceDuringUpdates"] = True
                elif isRequestClose(a) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
                elif isNo(a) == True:
                    main_config["EFlagRebuildPyinstallerAppFromSourceDuringUpdates"] = False
                    main_config["EFlagRebuildNuitkaAppFromSourceDuringUpdates"] = False
                    printDebugMessage("User selected: False")

                printMainMessage("Would you like to enable installing the latest version of EfazDev ECC Security CA? (y/n)")
                printMainMessage(f'Current Setting: {(main_config.get("EFlagInstallEfazDevECCCertificates")==True)}')
                printYellowMessage("This is apart of code-signing and may affect security.")
                a = input("> ")
                if isYes(a) == True:
                    main_config["EFlagInstallEfazDevECCCertificates"] = True
                    printDebugMessage("User selected: True")
                elif isRequestClose(a) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
                elif isNo(a) == True:
                    main_config["EFlagInstallEfazDevECCCertificates"] = False
                    printDebugMessage("User selected: False")

                if main_os == "Darwin":
                    printMainMessage("Would you like to rebuild OrangeLoader, Play Roblox, and Run Studio app based on source code? (y/n)")
                    printMainMessage(f'Current Setting: {(main_config.get("EFlagRebuildClangAppFromSourceDuringUpdates")==True)}')
                    printYellowMessage("Clang++ is required to be installed on your Mac in order to use.")
                    a = input("> ")
                    if isYes(a) == True:
                        main_config["EFlagRebuildClangAppFromSourceDuringUpdates"] = True
                        printDebugMessage("User selected: True")
                    elif isRequestClose(a) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
                    elif isNo(a) == True:
                        main_config["EFlagRebuildClangAppFromSourceDuringUpdates"] = False
                        printDebugMessage("User selected: False")

                printMainMessage("Would you like to enable See More Awaiting on List Selections? (y/n)")
                d = handleBasicSetting("EFlagEnableSeeMoreAwaiting", False)
                if d: return d

                printMainMessage("Would you like to enable 429 Loops when the Roblox server gives a 429 (Too much request) response? (y/n)")
                d = handleBasicSetting("EFlagEnableLoop429Requests", False)
                if d: return d

                printMainMessage("Would you like to disable Bootstrap Update Checks? (y/n)")
                d = handleBasicSetting("EFlagDisableBootstrapChecks", False)
                if d: return d

                printMainMessage("Would you like to disable Python Update Checks? (y/n)")
                d = handleBasicSetting("EFlagDisablePythonUpdateChecks", False)
                if d: return d

                printMainMessage("Would you like to disable Python Module Update Checks? (y/n)")
                d = handleBasicSetting("EFlagDisablePythonModuleUpdateChecks", False)
                if d: return d

                if main_config.get("EFlagDisablePythonUpdateChecks", False) == False:
                    printMainMessage("Would you like to enable slient Python installs instead of a prompt for python updates? (y/n)")
                    if main_os == "Darwin": printYellowMessage("For macOS users, admin permission is needed in order to install.")
                    d = handleBasicSetting("EFlagEnableSlientPythonInstalls", False)
                    if d: return d

                printMainMessage("Would you like to enable OrangeBlox Beta? (y/n)")
                printMainMessage(f'Current Setting: {(main_config.get("EFlagBootstrapUpdateServer")=="https://raw.githubusercontent.com/EfazDev/orangeblox/refs/heads/beta/Version.json" or main_config.get("EFlagBootstrapUpdateServer")=="https://obxbeta.efaz.dev/Version.json")}')
                printYellowMessage("Betas could contain bugs that could break your Roblox installation!")
                d = input("> ")
                if isYes(d) == True:
                    main_config["EFlagBootstrapUpdateServer"] = "https://obxbeta.efaz.dev/Version.json"
                    printDebugMessage("User selected: True")
                elif isRequestClose(d) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
                elif isNo(d) == True:
                    main_config["EFlagBootstrapUpdateServer"] = "https://obx.efaz.dev/Version.json"
                    printDebugMessage("User selected: False")

                printMainMessage("Would you like to disable automatically saving your OrangeBlox Configuration to your installation folder? (y/n)")
                d = handleBasicSetting("EFlagDisableAutosaveToInstallation", False)
                if d: return d

                if main_os == "Windows":
                    printMainMessage("Would you like to disable Bootstrap Cooldowns? (y/n)")
                    printMainMessage(f'Current Setting: {(main_config.get("EFlagDisableBootstrapCooldown")==True)}')
                    printYellowMessage("If your computer is laggy, this may prevent multiple windows opening.")
                    d = input("> ")
                    if isYes(d) == True:
                        main_config["EFlagDisableBootstrapCooldown"] = True
                        printDebugMessage("User selected: True")
                    elif isRequestClose(d) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
                    elif isNo(d) == True:
                        main_config["EFlagDisableBootstrapCooldown"] = False
                        printDebugMessage("User selected: False")

                printMainMessage("Would you like to use Python Virtual Environments for OrangeBlox? (y/n)")
                d = handleBasicSetting("EFlagEnablePythonVirtualEnvironments", False)
                if d: return d

                printMainMessage("Would you like to build Python cache on app start? (y/n)")
                d = handleBasicSetting("EFlagBuildPythonCacheOnStart", False)
                if d: return d
                    
                if main_os == "Windows":
                    printMainMessage("Would you like to make shortcuts for OrangeBlox? [Needed for launching through the Windows Start Menu and Desktop] (y/n)")
                    d = handleBasicSetting("EFlagDisableShortcutsInstall", False, False)
                    if d: return d
                elif main_os == "Darwin":
                    printMainMessage("Would you like to enable Dock Bar and System Tray options when right clicking the app icon? (y/n)")
                    d = handleBasicSetting("EFlagEnableGUIOptionMenus", True)
                    if d: return d
            def debugging():
                printWarnMessage("--- Debugging ---")
                global main_config
                printMainMessage("Would you like to enable Debug Mode? (y/n)")
                printMainMessage(f'Current Setting: {(main_config.get("EFlagEnableDebugMode")==True)}')
                printYellowMessage("[WARNING! This will expose information like login to Roblox.]")
                printYellowMessage("[DO NOT EVER ENABLE IF SOMEONE TOLD YOU SO OR YOU USUALLY RECORD!!]")
                d = input("> ")
                if isYes(d) == True:
                    main_config["EFlagEnableDebugMode"] = True
                    printDebugMessage("User selected: True")
                elif isRequestClose(d) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
                elif isNo(d) == True:
                    main_config["EFlagEnableDebugMode"] = False
                    printDebugMessage("User selected: False")
                pip_class.debug = main_config.get("EFlagEnableDebugMode") == True

                if main_config.get("EFlagEnableDebugMode") == True:
                    printMainMessage("Would you like to print unhandled Roblox client events? (y/n)")
                    d = handleBasicSetting("EFlagAllowFullDebugMode", False)
                    if d: return d

                printMainMessage("Would you like to enable saving Bootstrap logs? (y/n)")
                d = handleBasicSetting("EFlagMakeMainBootstrapLogFiles", False)
                if d: return d

                printMainMessage("Would you like to set a Roblox client channel? (y/n)")
                printMainMessage(f'Current Setting: {(main_config.get("EFlagRobloxClientChannel", "LIVE"))}')
                printYellowMessage("This will be used to determine the latest Roblox version.")
                d = input("> ")
                if isYes(d) == True:
                    def t():
                        printMainMessage("Please enter the channel in the input selection below! You may also use the link below to determine the channel for your account!")
                        printMainMessage(f"https://clientsettings.roblox.com/v2/user-channel?binaryType={'MacPlayer' if main_os == 'Darwin' else 'WindowsPlayer'}")
                        printMainMessage('Additionally, you may enter "A" to automatically determine or "D" to disable Roblox update checks.')
                        channel_inp = input("> ")
                        if channel_inp == "A":
                            main_config["EFlagRobloxClientChannel"] = None
                            main_config["EFlagDisableRobloxUpdateChecks"] = False
                            printSuccessMessage("Successfully set Roblox client channel to automatically determine!")
                        elif channel_inp == "D":
                            main_config["EFlagRobloxClientChannel"] = "LIVE"
                            main_config["EFlagDisableRobloxUpdateChecks"] = True
                            printSuccessMessage("Successfully disabled Roblox Update Checks for launching from OrangeBlox. Roblox may still check for updates though.")
                        else:
                            try:
                                a = handler.getLatestClientVersion(studio=False, debug=main_config.get("EFlagEnableDebugMode"), channel=channel_inp, token=createDownloadToken(False))
                                if a.get("success") == True and a.get("attempted_channel") == channel_inp:
                                    main_config["EFlagRobloxClientChannel"] = channel_inp
                                    main_config["EFlagDisableRobloxUpdateChecks"] = False
                                    printSuccessMessage("Successfully set Roblox client channel!")
                                else:
                                    printErrorMessage("Channel may not exist. Please try again or use LIVE!")
                                    t()
                            except Exception as e:
                                printErrorMessage("Something went wrong. Please try again or use LIVE!")
                                t()
                    t()
                elif isRequestClose(d) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
                elif isNo(d) == True:
                    main_config["EFlagRobloxClientChannel"] = "LIVE"
                    main_config["EFlagDisableRobloxUpdateChecks"] = False
                    printDebugMessage("User selected: False")

                if main_config.get("EFlagRobloxStudioEnabled") == True:
                    printMainMessage("Would you like to set a Roblox Studio client channel? (y/n)")
                    printMainMessage(f'Current Setting: {(main_config.get("EFlagRobloxStudioClientChannel", "LIVE"))}')
                    printYellowMessage("This will be used to determine the latest Roblox Studio version.")
                    d = input("> ")
                    if isYes(d) == True:
                        def t():
                            printMainMessage("Please enter the channel in the input selection below! You may also use the link below to determine the channel for your account!")
                            printMainMessage(f"https://clientsettings.roblox.com/v2/user-channel?binaryType={'MacStudio' if main_os == 'Darwin' else 'WindowsStudio'}")
                            printMainMessage('Additionally, you may enter "A" to automatically determine or "D" to disable Roblox Studio update checks.')
                            channel_inp = input("> ")
                            if channel_inp == "A":
                                main_config["EFlagRobloxStudioClientChannel"] = None
                                main_config["EFlagDisableRobloxUpdateChecks"] = False
                                printSuccessMessage("Successfully set Roblox Studio client channel to automatically determine!")
                            elif channel_inp == "D":
                                main_config["EFlagRobloxStudioClientChannel"] = "LIVE"
                                main_config["EFlagDisableRobloxUpdateChecks"] = True
                                printSuccessMessage("Successfully disabled Roblox Studio Update Checks for launching from OrangeBlox. Roblox may still check for updates though.")
                            else:
                                try:
                                    a = handler.getLatestClientVersion(studio=True, debug=main_config.get("EFlagEnableDebugMode"), channel=channel_inp, token=createDownloadToken(True))
                                    if a.get("success") == True and a.get("attempted_channel") == channel_inp:
                                        main_config["EFlagRobloxStudioClientChannel"] = channel_inp
                                        main_config["EFlagDisableRobloxUpdateChecks"] = False
                                        printSuccessMessage("Successfully set Roblox Studio client channel!")
                                    else:
                                        printErrorMessage("Channel may not exist. Please try again or use LIVE!")
                                        t()
                                except Exception as e:
                                    printErrorMessage("Something went wrong. Please try again or use LIVE!")
                                    t()
                        t()
                    elif isRequestClose(d) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
                    elif isNo(d) == True:
                        main_config["EFlagRobloxStudioClientChannel"] = "LIVE"
                        main_config["EFlagDisableRobloxUpdateChecks"] = False
                        printDebugMessage("User selected: False")

                printMainMessage("Would you like to disable Hash Verification in the OrangeLoader backend? (y/n)")
                printMainMessage(f'Current Setting: {(main_config.get("EFlagDisableSecureHashSecurity")==True)}')
                printYellowMessage("This is a security measure used to validate bootstrap scripts.")
                d = input("> ")
                if isYes(d) == True:
                    main_config["EFlagDisableSecureHashSecurity"] = True
                    printDebugMessage("User selected: True")
                elif isRequestClose(d) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
                elif isNo(d) == True:
                    main_config["EFlagDisableSecureHashSecurity"] = False
                    printDebugMessage("User selected: False")

                printMainMessage("Would you like to enable Hash Verification on Roblox Player and Studio after updates? (y/n)")
                printMainMessage(f'Current Setting: {(not (main_config.get("EFlagVerifyRobloxHashAfterInstall")==False))}')
                printYellowMessage("This is a security measure that be used to validate Roblox in case of insecure downloads.")
                d = input("> ")
                if isYes(d) == True:
                    main_config["EFlagVerifyRobloxHashAfterInstall"] = True
                    printDebugMessage("User selected: True")
                elif isRequestClose(d) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
                elif isNo(d) == True:
                    main_config["EFlagVerifyRobloxHashAfterInstall"] = False
                    printDebugMessage("User selected: False")
            printWarnMessage("--- Settings ---")
            generated_ui_options.append({
                "index": 1, 
                "message": ts("Roblox Modifications & Settings"), 
                "func": robloxSettings,
                "clear_console": True
            })
            generated_ui_options.append({
                "index": 2, 
                "message": ts("Global Setting Modifications"), 
                "func": globalSettings,
                "clear_console": True
            })
            generated_ui_options.append({
                "index": 3, 
                "message": ts("Activity Tracking"), 
                "func": activityTracking,
                "clear_console": True
            })
            generated_ui_options.append({
                "index": 4, 
                "message": ts("Bootstrap Settings"), 
                "func": bootstrapSettings,
                "clear_console": True
            })
            generated_ui_options.append({
                "index": 5, 
                "message": ts("Clear Temporary Storage"), 
                "func": continueToClearTemporaryStorage, 
                "go_to_rbx": True, 
                "end_mes": ts("Temporary storage has been removed!"),
                "clear_console": True
            })
            generated_ui_options.append({
                "index": 7, 
                "message": ts("Roblox Installer Options"), 
                "func": continueToInstallRobloxOptions, 
                "go_to_rbx": True, 
                "end_mes": ts("Roblox has been modified!"),
                "clear_console": True
            })
            generated_ui_options.append({
                "index": 8, 
                "message": ts("OrangeBlox Installer Options"), 
                "func": continueToOrangeBloxInstaller, 
                "go_to_rbx": True,  
                "end_mes": ts("OrangeBlox has been modified!"),
                "clear_console": True
            })
            generated_ui_options.append({
                "index": 10, 
                "message": ts("Debugging"), 
                "func": debugging,
                "clear_console": True
            })
            if (main_config.get("EFlagOrangeBloxSyncDir") and os.path.exists(main_config.get("EFlagOrangeBloxSyncDir"))):
                generated_ui_options.append({
                    "index": 97, 
                    "message": ts("Sync to Configuration"),
                    "func": syncToFFlagConfiguration, 
                    "go_to_rbx": True, 
                    "end_mes": ts("Sync finished!"),
                    "clear_console": True
                })
                generated_ui_options.append({
                    "index": 98, 
                    "message": ts("Sync from Configuration"), 
                    "func": syncFromFFlagConfiguration, 
                    "go_to_rbx": True, 
                    "end_mes": ts("Sync finished!"),
                    "clear_console": True
                })
            opt = generateMenuSelection(generated_ui_options, star_option=ts("Exit Settings"))
            if opt:
                if opt.get("clear_console") == True: startMessage()
                re = opt["func"]()
                if opt.get("go_to_rbx") == True: 
                    saveSettings()
                    printWarnMessage(f"{re} Would you like to return to settings or exit it?")
                    printMainMessage("[1] = Return to Settings")
                    printMainMessage("[*] = Exit Settings")
                    a = input("> ")
                    if a == "1": return mainSettings()
                    else: return ts("Successfully saved settings!")
                else:
                    if re == "Settings was closed.":
                        saveSettings()
                        printSuccessMessage("Successfully saved Bootstrap Settings!")
                        return ts("Successfully saved settings!")
                    else: return mainSettings()
            else:
                saveSettings()
                printSuccessMessage("Successfully saved Bootstrap Settings!")
                return ts("Successfully saved settings!")
        if main_config.get("EFlagDisableSettingsAccess") == True:
            printWarnMessage("--- Settings ---")
            printErrorMessage("Access to editing Settings was disabled by file. Please try again later!")
            input("> ")
            return ts("Settings was not saved!")
        return mainSettings()
    def continueToCredits(): # Credits
        quote = "'"
        printWarnMessage("--- Credits ---")
        printMainMessage(f"1. Made by {colors_class.wrap('@EfazDev 🍊', 202)}")
        printMainMessage(f"2. Old Player Sounds and Cursors were sourced from {colors_class.wrap('Bloxstrap 🎮 (https://github.com/pizzaboxer/bloxstrap)', 165)}")
        printMainMessage(f"3. Avatar Editor Maps were from {colors_class.wrap(f'Mielesgames{quote}s Map Files 🗺️ (https://github.com/Mielesgames/RobloxAvatarEditorMaps)', 197)} slightly edited to be usable for the current version of Roblox (as of the time of writing this)")
        printMainMessage(f"4. The Kliko's Mod Tool Mod Script was edited and made from {colors_class.wrap(f'Kliko{quote}s Mod Tool and Kliko{quote}s modloader 🎮 (https://github.com/klikos-modloader/klikos-modloader)', 196)}")
        printMainMessage("5. Python Module Creators:")
        printMainMessage(f" • {colors_class.wrap('qwertyquerty (pypresence) 🦖 (https://github.com/qwertyquerty/pypresence)', 34)}")
        printMainMessage(f" • {colors_class.wrap('Ronald Oussoren (pyobjc) 🔁 (https://github.com/ronaldoussoren/pyobjc)', 40)}")
        printMainMessage(f" • {colors_class.wrap('Philip Semanchuk (posix-ipc) 🙂 (https://github.com/osvenskan/posix_ipc)', 226)}")
        printMainMessage(f" • {colors_class.wrap('Mark Hammond (pywin32) 🪟 (https://github.com/mhammond/pywin32)', 129)}")
        printMainMessage(f" • {colors_class.wrap('Kivy (plyer) 🧰 (https://github.com/kivy/plyer)', 214)}")
        printMainMessage(f" • {colors_class.wrap('Giampaolo Rodola (psutil) 🔌 (https://github.com/giampaolo/psutil)', 97)}")
        printMainMessage(f"Licenses are listed in {'https://github.com/EfazDev/orangeblox/tree/main/Licenses'} or included with your installation in: {os.path.join(cur_path, 'Licenses')}")
        printMainMessage(f"6. The logo of OrangeBlox was made thanks of {colors_class.wrap('@CabledRblx 🦆', 226)}. Thanks :)")
        printMainMessage(f"7. Server Locations was made thanks to {colors_class.wrap('ipinfo.io 🌐', 39)} as it wouldn't be possible to convert ip addresses without them!")
        if main_os == "Darwin": 
            printMainMessage(f'8. macOS App was built using {colors_class.wrap("pyinstaller 📦", 39)} and {colors_class.wrap("clang 📦", 226)}. You can recreate and deploy using the following command! Use the README.md for more information.')
            printMainMessage(f"Command: \"{sys.executable}\" Install.py -r -rp -rc")
            printYellowMessage(f"Nuitka requires a C compiler in order to use. For more information, use this manual: https://nuitka.net/user-documentation/user-manual.html")
        elif main_os == "Windows": 
            printMainMessage(f'8. Windows App was built using {colors_class.wrap("pyinstaller 📦", 39)}. You can recreate and deploy using the following command! Use the README.md for more information.')
            printMainMessage(f"Command: \"{sys.executable}\" Install.py -r -rp")
        printDebugMessage(f"Operating System: {main_os}")
    def continueToUnfriendedFriends(): # View Unfriended Friends
        printWarnMessage(f"--- Unfriended Friends ---")
        unfriended_friends = []
        blank_user_ids = 0
        friend_check_id = main_config.get('EFlagRobloxUnfriendCheckUserID', 1)
        try:
            printMainMessage("Fetching Friends! This may take a moment.")
            reached_end = False
            friend_list_json = {"data": []}
            query = {"limit": "50", "findFriendsType": "0"}
            while reached_end == False:
                try:
                    if main_config.get("EFlagUseEfazDevAPI") == True: 
                        if query.get("limit"): query.pop("limit")
                        if query.get("findFriendsType"): query.pop("findFriendsType")
                        friend_list_req = requests.get(f"https://api.efaz.dev/api/roblox/user-friends-find/{friend_check_id}/50" + requests.format_params(query), timeout=5)
                        if friend_list_req and friend_list_req.json: friend_list_req.json = friend_list_req.json.get("response")
                    else: friend_list_req = requests.get(f"https://friends.roblox.com/v1/users/{friend_check_id}/friends/find" + requests.format_params(query), timeout=5, cookies=createCookieHeader())
                    friend_req_json = friend_list_req.json
                    printDebugMessage(f"Called ({friend_list_req.url}): {friend_list_req.json}")
                    if friend_list_req.ok and friend_req_json.get("PageItems"):
                        friend_list_json["data"] += friend_req_json.get("PageItems")
                        if friend_req_json.get("NextCursor"):  query["cursor"] = friend_req_json.get("NextCursor")
                        else: reached_end = True
                except Exception as e: pass
                time.sleep(1)
            
            last_pinged_friend_list = {}
            if os.path.exists(os.path.join(generateFileKey("CachedFriendsList", ext=".json"))):
                with open(os.path.join(cur_path, generateFileKey("CachedFriendsList", ext=".json")), "r", encoding="utf-8") as f: last_pinged_friend_list = json.load(f)
            if last_pinged_friend_list.get(str(friend_check_id)):
                for i in last_pinged_friend_list.get(str(friend_check_id)):
                    found_friend = False
                    for e in friend_list_json.get("data"):
                        if e["id"] == i["id"]: found_friend = True; break
                    if found_friend == False: unfriended_friends.append(i)
                    else: blank_user_ids += 1
                reached_end2 = False
                while reached_end2 == False:
                    try:
                        user_ids = []
                        for i in unfriended_friends: 
                            if not (i.get("id") == -1): user_ids.append(i.get("id"))
                        if len(user_ids) > 150:
                            chunked = []
                            for e in range(0, len(user_ids), 150): chunked.append(user_ids[e:e + 150])
                            unfriended_friends = []
                            for e in chunked:
                                reached_end3 = False
                                while reached_end3 == False:
                                    user_info_req = requests.post(f"https://users.roblox.com/v1/users", {"userIds": e, "excludeBannedUsers": False}, timeout=5, cookies=createCookieHeader())
                                    if user_info_req.ok: unfriended_friends += user_info_req.json.get("data"); reached_end3 = True
                                    printDebugMessage(f"Called ({user_info_req.url}): {user_info_req.json}")
                                    time.sleep(1)
                            reached_end2 = True
                        else:
                            user_info_req = requests.post(f"https://users.roblox.com/v1/users", {"userIds": user_ids, "excludeBannedUsers": False}, timeout=5, cookies=createCookieHeader())
                            if user_info_req.ok: unfriended_friends = user_info_req.json.get("data"); reached_end2 = True
                            printDebugMessage(f"Called ({user_info_req.url}): {user_info_req.json}")
                            time.sleep(1)
                    except Exception as e: pass
                last_pinged_friend_list[str(friend_check_id)] = friend_list_json.get("data")
            else: last_pinged_friend_list[str(friend_check_id)] = friend_list_json.get("data")
            with open(os.path.join(cur_path, generateFileKey("CachedFriendsList", ext=".json")), "w", encoding="utf-8") as f: json.dump(last_pinged_friend_list, f, indent=4)
        except Exception as e:
            printDebugMessage(f"Unable to fetch friends list! Exception: \n{trace()}")
            unfriended_friends = []
        if len(unfriended_friends) > 0:
            printMainMessage("The following friends have unfriended you from your friends list ;(")
            if blank_user_ids > 0: printYellowMessage("Warning! This could be falsified due to friend restrictions in view of other users!")
            c = 0
            for i in unfriended_friends:
                c += 1
                printMainMessage(f"{c}. @{i['name']} [ID: {i['id']}]")
        else: printMainMessage(f"There's currently no friends that have unfriended you on User ID [{friend_check_id}] since your last view.")
    def continueToUpdatePython(): # Update Python
        is_python_beta = pip_class.getIfPythonVersionIsBeta()
        current_python_version = pip_class.getCurrentPythonVersion()
        latest_python_version = pip_class.getLatestPythonVersion(beta=is_python_beta)
        printWarnMessage(f"--- Update to Python {latest_python_version} ---")
        if current_python_version == latest_python_version: printSuccessMessage(f"You're already in the latest version of Python!")
        else:
            printMainMessage(f"Would you like to update Python to {latest_python_version} using the official Python Installer? (y/n)")
            printMainMessage(f"{colors_class.wrap(f'[v{current_python_version} => v{latest_python_version}]', 226 if is_python_beta else 82)}")
            co = input("> ")
            if isYes(co) == True:
                if main_config.get("EFlagEnableSlientPythonInstalls") == True:
                    printMainMessage("Python may take a moment to install! Please wait!")
                    if main_os == "Darwin": printYellowMessage("For macOS users, admin permission is needed in order to install.")
                    pip_class.pythonInstall(latest_python_version, is_python_beta, silent=True)
                else:
                    printMainMessage("Python Installer should launch after a moment. Follow the prompts to install!")
                    pip_class.pythonInstall(latest_python_version, is_python_beta)
                printMainMessage("Validating Python Installation..")
                if pip_class.getMajorMinorVersion(current_python_version) < pip_class.getMajorMinorVersion(latest_python_version):
                    current_latest_python = latest_python_version
                else:
                    latest_pip_class = PyKits.pip()
                    latest_pip_class.ignore_same = True
                    current_latest_python = latest_pip_class.getCurrentPythonVersion()
                if current_latest_python == latest_python_version:
                    printSuccessMessage(f"Python {latest_python_version} has been successfully installed! Would you like to restart Python? (y/n)")
                    co = input("> ")
                    if isYes(co) == True: pip_class.restartScript("Main.py", sys.argv)
                    sys.exit(0)
                else: printErrorMessage("Python Installation was may be canceled or Python was not installed!")
    def continueToUpdatePythonModules(): # Update Python Modules
        printWarnMessage(f"--- Update Python Modules ---")
        can_be_updated_modules = ["pypresence", "psutil"]
        if main_os == "Windows": can_be_updated_modules += ["pywin32", "plyer"]
        elif main_os == "Darwin": can_be_updated_modules += ["pyobjc-core", "pyobjc-framework-Quartz", "pyobjc-framework-Cocoa", "posix-ipc"]
        for mod_info in generateModsManifest().values():
            if mod_info.get("mod_script") == True and mod_info.get("enabled") == True and mod_info.get("python_modules"): can_be_updated_modules += [str(module_needed) for module_needed in mod_info.get("python_modules", []) if not module_needed in can_be_updated_modules]
        updating_python_modules = pip_class.updates(can_be_updated_modules)
        if updating_python_modules and updating_python_modules["success"] == True:
            if len(updating_python_modules["packages"]) > 0:
                strs = []
                only_package_names = []
                for i in updating_python_modules["packages"]: vers1 = i['version']; vers2 = i['latest_version']; strs.append(f"{i['name']} {colors_class.wrap(f'(v{vers1} => v{vers2})', 82)}"); only_package_names.append(i["name"])
                printMainMessage("The following modules are available to be updated!")
                printMainMessage(", ".join(strs))
                printMainMessage("Would you like to install the updates to them now?")
                co = input("> ")
                if isYes(co) == True:
                    printMainMessage("Please wait while the modules are being updated!")
                    update_modules = pip_class.install(only_package_names, upgrade=True)
                    if update_modules["success"] == True: 
                        printSuccessMessage("Successfully updated all Python modules!")
                        if os.path.exists(generateFileKey("PythonModuleUpdate")): os.remove(generateFileKey("PythonModuleUpdate"))
                    else: printErrorMessage("Unable to update all Python modules.")
                else: return ts("Python Module updating was canceled!")
            elif os.path.exists(generateFileKey("PythonModuleUpdate")): 
                os.remove(generateFileKey("PythonModuleUpdate"))
                printMainMessage("No Python module updates are available right now!"); return ts("No updates for Python Modules were available!")
            else: printMainMessage("No Python module updates are available right now!"); return ts("No updates for Python Modules were available!")
        else: printErrorMessage("There was an issue trying to fetch for module updates!"); return ts("Python Module updating was canceled!")
    def continueToLinkShortcuts(url_scheme=None): # Roblox Link Shortcuts
        global run_studio
        global custom_cookies
        printWarnMessage("--- Roblox Link Shortcuts ---")
        if main_config.get("EFlagDisableSettingsAccess") == True:
            printErrorMessage("Access to using Link Shortcuts was disabled by file. Please try again later!")
            input("> ")
            handleOptionSelect(mes="Link Shortcuts was not used!")
            return
        if type(url_scheme) is str and not (url_scheme == "efaz-bootstrap://shortcuts/?quick-action=true" or url_scheme == "orangeblox://shortcuts/?quick-action=true"):
            if '://' in url_scheme: path = url_scheme.split('://', 1)[1]
            else: path = url_scheme.split(':', 1)[1]
            generated_shortcut_id = path.replace("shortcuts/", "").replace("?quick-action=true", "")
            if type(main_config.get("EFlagRobloxLinkShortcuts")) is dict:
                if main_config.get("EFlagRobloxLinkShortcuts").get(generated_shortcut_id):
                    shortcut_info = main_config.get("EFlagRobloxLinkShortcuts").get(generated_shortcut_id)
                    running = False
                    if type(shortcut_info.get("url")) is str and (shortcut_info.get("url").startswith("roblox:") or shortcut_info.get("url").startswith("roblox-player:") or shortcut_info.get("url").startswith("roblox-studio:") or shortcut_info.get("url").startswith("roblox-studio-auth:")):
                        if len(given_args) > 1: given_args[1] = shortcut_info["url"]
                        else: given_args.append(shortcut_info["url"])
                        if shortcut_info["url"].startswith("roblox-studio"): run_studio = True
                        running = True
                    if type(shortcut_info.get("cookie_paths")) is dict:
                        for i, v in shortcut_info.get("cookie_paths").items():
                            if main_os == "Darwin" and (i.startswith(os.path.join(pip_class.getLocalAppData(), "HTTPStorages", "com.roblox.")) and v.startswith(os.path.join(pip_class.getLocalAppData(), "Roblox", "RBXCookies"))): custom_cookies[i] = v
                            elif main_os == "Windows" and (i == os.path.join(pip_class.getLocalAppData(), "Roblox", "LocalStorage", "RobloxCookies.dat") and v.startswith(os.path.join(pip_class.getLocalAppData(), "Roblox", "RBXCookies"))): custom_cookies[i] = v
                        running = True
                    if running == True: printSuccessMessage(f'Starting shortcut "{shortcut_info.get("name")}"!'); continueToRoblox()
                    else:
                        printErrorMessage(f'You were redirected to a link shortcut with id "{generated_shortcut_id}" but it doesn\'t exist under your settings.')
                        input("> ")
                        continueToLinkShortcuts()
                else:
                    printErrorMessage(f'You were redirected to a link shortcut with id "{generated_shortcut_id}" but it doesn\'t exist under your settings.')
                    input("> ")
                    continueToLinkShortcuts()
            else:
                printErrorMessage(f'You were redirected to a link shortcut with id "{generated_shortcut_id}" but it doesn\'t exist under your settings.')
                input("> ")
                continueToLinkShortcuts()
        else:
            def linkLoop():
                global run_studio
                global custom_cookies
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
                generated_ui_options.append({"index": 999999, "message": ts("Create a new shortcut")})
                generated_ui_options.append({"index": 999999.5, "message": ts("Create a new user shortcut")})
                generated_ui_options.append({"index": 1000000, "message": ts("Generate a new shortcut app")})
                generated_ui_options.append({"index": 1000000.5, "message": ts("Run a shortcut in a new instance")})
                generated_ui_options.append({"index": 1000001, "message": ts("Delete a shortcut")})
                generated_ui_options = sorted(generated_ui_options, key=lambda x: x["index"])
                opt = generateMenuSelection(generated_ui_options)
                if opt:
                    if opt["index"] == 999999:
                        def loo():
                            printMainMessage("Enter the name to use for the shortcut: ")
                            name = input("> ")
                            printMainMessage("Enter the url to use for the shortcut (starts with \"roblox:\" or \"roblox-player:\" or \"roblox-studio:\" or \"roblox-studio-auth:\"): ")
                            printMainMessage("Use this guide to help create it: https://github.com/bloxstraplabs/bloxstrap/wiki/A-deep-dive-on-how-the-Roblox-bootstrapper-works#starting-roblox")
                            def urll():
                                ura = input("> ")
                                if ura.startswith("roblox:") or ura.startswith("roblox-player:") or ura.startswith("roblox-studio:") or ura.startswith("roblox-studio-auth:"): return ura
                                else:
                                    printErrorMessage("This is not a valid Roblox URL Scheme. Please try again!")
                                    return urll()
                            ur = urll()
                            printMainMessage("Enter the key to be defined for this shortcut, this will be used for a url scheme: ")
                            key = input("> ") 
                            printMainMessage("Confirm the shortcut below? (y/n)")
                            printMainMessage(f"Name: {name}")
                            printMainMessage(f"URL: {ur}")
                            printMainMessage(f"Key: {key}")
                            if isYes(input("> ")) == True:
                                if main_config.get("EFlagRobloxLinkShortcuts"): main_config.get("EFlagRobloxLinkShortcuts")[key] = {"url": ur, "name": name, "id": key}
                                else:
                                    main_config["EFlagRobloxLinkShortcuts"] = {}
                                    main_config["EFlagRobloxLinkShortcuts"][key] = {"url": ur, "name": name, "id": key}
                                printSuccessMessage(f'Successfully created shortcut "{name}"! You may use this link using your browser or go through the main menu to use this shortcut: orangeblox://shortcuts/{key}')
                            saveSettings()
                            printMainMessage("Would you like to create an another shortcut? (y/n)")
                            if isYes(input("> ")) == True: loo()
                        loo()
                        linkLoop()
                    elif opt["index"] == 999999.5:
                        printYellowMessage("Important Notes:")
                        printYellowMessage("This option will automatically fetch your cookies and save them into the Roblox folder so you can login quicker.")
                        printYellowMessage("This option cannot be backed up to an another computer using OrangeBlox installer due to cookie locations are saved.")
                        printYellowMessage("Launching Roblox from the web will automatically log out the user. Please know that.")
                        printYellowMessage("Log into the account you want to save as a shortcut before you continue.")
                        if not handler.getIfRobloxIsOpen():
                            printMainMessage("Would you like to open Roblox without user data in order to login and create a cookie? (y/n)")
                            printYellowMessage("Warning! The cookies before this may be brought back after setup.")
                            printYellowMessage("But, it may be best to prevent the log out issue.")
                            if isYes(input("> ")) == True:
                                if main_os == "Darwin":
                                    httpStorages = os.path.join(pip_class.getLocalAppData(), "HTTPStorages")
                                    if os.path.exists(os.path.join(httpStorages, "com.roblox.RobloxPlayer.binarycookies")): 
                                        shutil.copy(os.path.join(httpStorages, "com.roblox.RobloxPlayer.binarycookies"), os.path.join(httpStorages, "dev.efaz.temp.RobloxPlayer.binarycookies"))
                                        os.remove(os.path.join(httpStorages, "com.roblox.RobloxPlayer.binarycookies"))
                                elif main_os == "Windows":
                                    if os.path.exists(os.path.join(pip_class.getLocalAppData(), "Roblox", "LocalStorage", "RobloxCookies.dat")): 
                                        shutil.copy(os.path.join(pip_class.getLocalAppData(), "Roblox", "LocalStorage", "RobloxCookies.dat"), os.path.join(pip_class.getLocalAppData(), "Roblox", "LocalStorage", "TempRobloxCookies.dat")); 
                                        os.remove(os.path.join(pip_class.getLocalAppData(), "Roblox", "LocalStorage", "RobloxCookies.dat"))
                                s = handler.openRoblox(forceQuit=True, attachInstance=True)
                                def endRbx(log): 
                                    while True: 
                                        if main_os == "Darwin":
                                            if os.path.exists(os.path.join(httpStorages, "com.roblox.RobloxPlayer.binarycookies")): 
                                                with open(os.path.join(httpStorages, "com.roblox.RobloxPlayer.binarycookies"), "rb") as f: cookie_data = f.read()
                                                if "Sharing-this-will-allow-someone-to-log-in".encode("utf-8") in cookie_data: break
                                        else:
                                            if os.path.exists(os.path.join(pip_class.getLocalAppData(), "Roblox", "LocalStorage", "RobloxCookies.dat")):
                                                with open(os.path.join(pip_class.getLocalAppData(), "Roblox", "LocalStorage", "RobloxCookies.dat"), "r", encoding="utf-8") as f: cookie_data = f.read()
                                                if "CookiesData" in cookie_data: break
                                        time.sleep(1)
                                    s.endInstance()
                                s.addRobloxEventCallback("onUserLogin", endRbx)
                                printMainMessage("Login to the Roblox account you would like to use!")
                                printMainMessage("(The windows may automatically close once the login is successful.)")
                                s.awaitRobloxClosing()
                        user_info = handler.getRobloxAppSettings().get("loggedInUser", {})
                        if user_info.get("id") and user_info.get("name"):
                            printMainMessage("Enter the name to use for the shortcut: ")
                            name = input("> ")
                            printMainMessage("Enter the url to use for the shortcut (starts with \"roblox:\" or \"roblox-player:\" or \"roblox-studio:\" or \"roblox-studio-auth:\"): ")
                            printMainMessage("Use this guide to help create it: https://github.com/bloxstraplabs/bloxstrap/wiki/A-deep-dive-on-how-the-Roblox-bootstrapper-works#starting-roblox")
                            printMainMessage("For no url needing, enter nothing and continue.")
                            def urll():
                                ura = input("> ")
                                if ura.startswith("roblox:") or ura.startswith("roblox-player:") or ura.startswith("roblox-studio:") or ura.startswith("roblox-studio-auth:"): return ura
                                elif ura == "": return ura
                                else:
                                    printErrorMessage("This is not a valid Roblox URL Scheme. Please try again!")
                                    return urll()
                            ur = urll()
                            printMainMessage("Enter the key to be defined for this shortcut, this will be used for a url scheme: ")
                            key = input("> ") 
                            printMainMessage("Confirm the shortcut below? (y/n)")
                            printMainMessage(f"Name: {name}")
                            if not (ur == ""): printMainMessage(f"URL: {ur}")
                            printMainMessage(f"User: @{user_info.get('name')} [{user_info.get('id')}]")
                            printMainMessage(f"Key: {key}")
                            if isYes(input("> ")) == True:
                                paths_generated = {}
                                if main_os == "Darwin":
                                    makedirs(os.path.join(pip_class.getLocalAppData(), "Roblox", "RBXCookies", key))
                                    httpStorages = os.path.join(pip_class.getLocalAppData(), "HTTPStorages")
                                    if os.path.exists(os.path.join(httpStorages, "com.roblox.RobloxPlayer.binarycookies")):
                                        t = os.path.join(httpStorages, "com.roblox.RobloxPlayer.binarycookies")
                                        paths_generated[t] = os.path.join(pip_class.getLocalAppData(), "Roblox", "RBXCookies", key, "com.roblox.RobloxPlayer.binarycookies")
                                        shutil.copy(t, paths_generated[t], follow_symlinks=False)
                                    if os.path.exists(os.path.join(httpStorages, "com.roblox.RobloxStudio.binarycookies")):
                                        t = os.path.join(httpStorages, "com.roblox.RobloxStudio.binarycookies")
                                        paths_generated[t] = os.path.join(pip_class.getLocalAppData(), "Roblox", "RBXCookies", key, "com.roblox.RobloxStudio.binarycookies")
                                        shutil.copy(t, paths_generated[t], follow_symlinks=False)
                                elif main_os == "Windows":
                                    makedirs(os.path.join(pip_class.getLocalAppData(), "Roblox", "RBXCookies", key))
                                    if os.path.exists(os.path.join(pip_class.getLocalAppData(), "Roblox", "LocalStorage", "RobloxCookies.dat")):
                                        t = os.path.join(pip_class.getLocalAppData(), "Roblox", "LocalStorage", "RobloxCookies.dat")
                                        paths_generated[t] = os.path.join(pip_class.getLocalAppData(), "Roblox", "RBXCookies", key, "RobloxCookies.dat")
                                        shutil.copy(t, paths_generated[t], follow_symlinks=False)
                                if main_config.get("EFlagRobloxLinkShortcuts"): main_config.get("EFlagRobloxLinkShortcuts")[key] = {"cookie_paths": paths_generated, "cookie_id": user_info.get("id"), "cookie_user": user_info.get("name"), "url": ur if not (ur == "") else None, "name": name, "id": key}
                                else:
                                    main_config["EFlagRobloxLinkShortcuts"] = {}
                                    main_config["EFlagRobloxLinkShortcuts"][key] = {"cookie_paths": paths_generated, "cookie_id": user_info.get("id"), "cookie_user": user_info.get("name"), "url": ur if not (ur == "") else None, "name": name, "id": key}
                                printSuccessMessage(f'Successfully created shortcut "{name}"! You may use this link using your browser or go through the main menu to use this shortcut: orangeblox://shortcuts/{key}')
                                saveSettings()
                            if main_os == "Darwin":
                                httpStorages = os.path.join(pip_class.getLocalAppData(), "HTTPStorages")
                                if os.path.exists(os.path.join(httpStorages, "dev.efaz.temp.RobloxPlayer.binarycookies")): 
                                    shutil.copy(os.path.join(httpStorages, "dev.efaz.temp.RobloxPlayer.binarycookies"), os.path.join(httpStorages, "com.roblox.RobloxPlayer.binarycookies"))
                                    os.remove(os.path.join(httpStorages, "dev.efaz.temp.RobloxPlayer.binarycookies"))
                            elif main_os == "Windows":
                                if os.path.exists(os.path.join(pip_class.getLocalAppData(), "Roblox", "LocalStorage", "TempRobloxCookies.dat")): 
                                    shutil.copy(os.path.join(pip_class.getLocalAppData(), "Roblox", "LocalStorage", "TempRobloxCookies.dat"), os.path.join(pip_class.getLocalAppData(), "Roblox", "LocalStorage", "RobloxCookies.dat")); 
                                    os.remove(os.path.join(pip_class.getLocalAppData(), "Roblox", "LocalStorage", "TempRobloxCookies.dat"))
                        else: printErrorMessage("Log in was not detected in the client!")
                        linkLoop()
                    elif opt["index"] == 1000000:
                        if type(main_config.get("EFlagRobloxLinkShortcuts")) is dict:
                            def loo():
                                if type(main_config.get("EFlagRobloxLinkShortcuts")) is dict:
                                    generated_ui_options = []
                                    printWarnMessage("--- Select Link Shortcut ---")
                                    for i, v in main_config.get("EFlagRobloxLinkShortcuts").items():
                                        if v and v.get("name") and v.get("id"): 
                                            approved = False
                                            cookie_added_str = ""
                                            if v.get("cookie_paths"):
                                                for c, k in v.get("cookie_paths").items():
                                                    if os.path.exists(k): approved = True; cookie_added_str = f" [User: @{v.get('cookie_user')}]"
                                            if v.get("url") or approved == True: generated_ui_options.append({"message": f"{v.get('name')} [{i}]{cookie_added_str}", "index": 1, "id": i})
                                    key = generateMenuSelection(generated_ui_options, star_option=ts("Exit Selection"))
                                    if key:
                                        key = key["id"]
                                        info = main_config.get("EFlagRobloxLinkShortcuts")[key]
                                        printMainMessage("Confirm the shortcut below? (y/n)")
                                        printMainMessage(f"Name: {info['name']}")
                                        printMainMessage(f"URL: {info['url']}")
                                        if info.get("cookie_id"): printMainMessage(f"User: @{info.get('cookie_user')} [{info.get('cookie_id')}]")
                                        printMainMessage(f"Key: {key}")
                                        if isYes(input("> ")) == True: 
                                            info['name'] = info['name'].replace("../", "").replace("./", "")
                                            printMainMessage("Generating Shortcut App..")
                                            if main_os == "Windows":
                                                try:
                                                    import win32com.client as win32client # type: ignore
                                                    def create_shortcut(target_path, shortcut_path, working_directory=None, icon_path=None, arguments=None):
                                                        shell = win32client.Dispatch('WScript.Shell')
                                                        if not os.path.exists(os.path.dirname(shortcut_path)): os.makedirs(os.path.dirname(shortcut_path),mode=511)
                                                        shortcut = shell.CreateShortcut(shortcut_path)
                                                        shortcut.TargetPath = target_path
                                                        if arguments: shortcut.Arguments = arguments
                                                        if working_directory: shortcut.WorkingDirectory = working_directory
                                                        if icon_path: shortcut.IconLocation = icon_path
                                                        shortcut.Save()
                                                    create_shortcut(os.path.join(cur_path, "OrangeBlox.exe"), os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), f"{info['name']}.lnk"), arguments=f"orangeblox://shortcuts/{key}")
                                                    create_shortcut(os.path.join(cur_path, "OrangeBlox.exe"), os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs'), f"{info['name']}.lnk"), arguments=f"orangeblox://shortcuts/{key}", icon_path=os.path.join(cur_path, "Images", "AppIconRunStudio.ico"))
                                                    create_shortcut(os.path.join(cur_path, "OrangeBlox.exe"), os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Roblox'), f"{info['name']}.lnk"), arguments=f"orangeblox://shortcuts/{key}", icon_path=os.path.join(cur_path, "Images", "AppIconRunStudio.ico"))     
                                                    printSuccessMessage("Generated Shortcut App!")
                                                except Exception as e: printErrorMessage(f"Unable to create shortcuts: {str(e)}")
                                            elif main_os == "Darwin":
                                                if os.path.exists(os.path.join(macos_app_path, "../", "Play Roblox.app")):
                                                    if not (os.path.exists(os.path.join(pip_class.getInstallableApplicationsFolder(), f"{info['name']}.app")) and not os.path.exists(os.path.join(pip_class.getInstallableApplicationsFolder(), f"{info['name']}.app", "Contents", "Resources", "AlternativeLink"))):
                                                        pip_class.copyTreeWithMetadata(os.path.join(macos_app_path, "../", "Play Roblox.app"), os.path.join(pip_class.getInstallableApplicationsFolder(), f"{info['name']}.app"), dirs_exist_ok=True)
                                                        with open(os.path.join(pip_class.getInstallableApplicationsFolder(), f"{info['name']}.app", "Contents", "Resources", "AlternativeLink"), "w", encoding="utf-8") as f: f.write(f"orangeblox://shortcuts/{key}")
                                                        for i in generateCodesignCommand(os.path.join(pip_class.getInstallableApplicationsFolder(), f"{info['name']}.app"), main_config.get("EFlagRobloxCodesigningName", "-")): 
                                                            if i[0] == "/usr/bin/xattr": subprocess.run(i, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                                                            else: subprocess.Popen(i, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                                                        printSuccessMessage("Generated Shortcut App!")
                                                    else: printErrorMessage("Unable to generate a shortcut app because this path for the shortcut is non-OrangeBlox and exists!")
                                                else: printErrorMessage("Unable to generate a shortcut app because Play Roblox app is not available!")
                                        saveSettings()
                                        printMainMessage("Would you like to generate an another shortcut app? (y/n)")
                                        if isYes(input("> ")) == True: loo()
                            loo()
                        else: printErrorMessage("You have no shortcuts created!")
                        linkLoop()
                    elif opt["index"] == 1000000.5:
                        if type(main_config.get("EFlagRobloxLinkShortcuts")) is dict:
                            generated_ui_options = []
                            printWarnMessage("--- Select Link Shortcut ---")
                            for i, v in main_config.get("EFlagRobloxLinkShortcuts").items():
                                if v and v.get("name") and v.get("id"): 
                                    approved = False
                                    cookie_added_str = ""
                                    if v.get("cookie_paths"):
                                        for c, k in v.get("cookie_paths").items():
                                            if os.path.exists(k): approved = True; cookie_added_str = f" [User: @{v.get('cookie_user')}]"
                                    if v.get("url") or approved == True: generated_ui_options.append({"message": f"{v.get('name')} [{i}]{cookie_added_str}", "index": 1, "id": i})
                            key = generateMenuSelection(generated_ui_options, star_option=ts("Exit Selection"))
                            if key:
                                key = key["id"]
                                if main_os == "Darwin": subprocess.run(["/usr/bin/open", f"orangeblox://shortcuts/{key}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cur_path)
                                else: subprocess.run(["start", f"orangeblox://shortcuts/{key}"], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cur_path)
                                printSuccessMessage("Successfully called to open a new instance! Please wait for Roblox to open and run a game before continuing the next account!")
                            else: printErrorMessage("Shortcut not found!")
                        else: printErrorMessage("You have no shortcuts created!")
                        linkLoop()
                    elif opt["index"] == 1000001:
                        if type(main_config.get("EFlagRobloxLinkShortcuts")) is dict:
                            def loo():
                                if type(main_config.get("EFlagRobloxLinkShortcuts")) is dict:
                                    generated_ui_options = []
                                    printWarnMessage("--- Select Link Shortcut ---")
                                    for i, v in main_config.get("EFlagRobloxLinkShortcuts").items():
                                        if v and v.get("name") and v.get("id"): 
                                            approved = False
                                            cookie_added_str = ""
                                            if v.get("cookie_paths"):
                                                for c, k in v.get("cookie_paths").items():
                                                    if os.path.exists(k): approved = True; cookie_added_str = f" [User: @{v.get('cookie_user')}]"
                                            if v.get("url") or approved == True: generated_ui_options.append({"message": f"{v.get('name')} [{i}]{cookie_added_str}", "index": 1, "id": i})
                                    key = generateMenuSelection(generated_ui_options, star_option=ts("Exit Selection"))
                                    if key:
                                        key = key["id"]
                                        info = main_config.get("EFlagRobloxLinkShortcuts")[key]
                                        printMainMessage("Confirm the shortcut below? (y/n)")
                                        printMainMessage(f"Name: {info['name']}")
                                        printMainMessage(f"URL: {info['url']}")
                                        if info.get("cookie_id"): printMainMessage(f"User: @{info.get('cookie_user')} [{info.get('cookie_id')}]")
                                        printMainMessage(f"Key: {key}")
                                        if isYes(input("> ")) == True: main_config["EFlagRobloxLinkShortcuts"].pop(key)
                                        saveSettings()
                                        printMainMessage("Would you like to delete an another shortcut? (y/n)")
                                        if isYes(input("> ")) == True: loo()
                                    else: printErrorMessage("Shortcut not found!")
                            loo()
                        else: printErrorMessage("You have no shortcuts created!")
                        linkLoop()
                    else:
                        running = False
                        if type(opt["shortcut_info"].get("cookie_paths")) is dict:
                            for i, v in opt["shortcut_info"].get("cookie_paths").items():
                                if main_os == "Darwin" and (i.startswith(os.path.join(pip_class.getLocalAppData(), "HTTPStorages", "com.roblox.")) and v.startswith(os.path.join(pip_class.getLocalAppData(), "Roblox", "RBXCookies"))): custom_cookies[i] = v
                                elif main_os == "Windows" and (i == os.path.join(pip_class.getLocalAppData(), "Roblox", "LocalStorage", "RobloxCookies.dat") and v.startswith(os.path.join(pip_class.getLocalAppData(), "Roblox", "RBXCookies"))): custom_cookies[i] = v
                            running = True
                        if type(opt["shortcut_info"].get("url")) is str and (opt["shortcut_info"].get("url").startswith("roblox:") or opt["shortcut_info"].get("url").startswith("roblox-player:") or opt["shortcut_info"].get("url").startswith("roblox-studio:") or opt["shortcut_info"].get("url").startswith("roblox-studio-auth:")):
                            if len(given_args) > 1: given_args[1] = opt["shortcut_info"]["url"]
                            else: given_args.append(opt["shortcut_info"]["url"])
                            if opt["shortcut_info"]["url"].startswith("roblox-studio"): run_studio = True
                            running = True
                        if running == True: printSuccessMessage(f"Starting shortcut \"{opt['shortcut_info']['name']}\"!"); continueToRoblox()
                        else: sys.exit(0)
                else:
                    if not url_scheme or not ("?quick-action=true" in url_scheme): handleOptionSelect(mes="Link Shortcuts has closed!")
                    else: sys.exit(0)
            linkLoop()
    def continueToModsManager(reverify_mod_script=None): # Mods Manager
        global main_config
        if main_config.get("EFlagEnableMods") == True:
            def mainModManager():
                if reverify_mod_script == None: printWarnMessage("--- Mods Manager ---")
                if reverify_mod_script == None:
                    printSuccessMessage(f"Mods Enabled: Yes")
                    if main_config.get("EFlagAllowActivityTracking") == False:
                        printMainMessage("Would you like to allow Activity Tracking on the Roblox client? (y/n)")
                        printMainMessage("This will allow features like:")
                        printMainMessage("- Server Locations")
                        printMainMessage("- Multiple Instances")
                        printMainMessage("- Discord Presence (+ BloxstrapRPC support)")
                        printMainMessage("- Discord Webhooks")
                        printMainMessage("- Mod Scripts")
                        d = input("> ")
                        if isYes(d) == True:
                            main_config["EFlagAllowActivityTracking"] = True
                            saveSettings()
                            printDebugMessage("User selected: True")
                        elif isNo(d) == True:
                            main_config["EFlagAllowActivityTracking"] = False
                            saveSettings()
                            printDebugMessage("User selected: False")
                            return
                    if not main_config.get("EFlagSelectedModScripts"): main_config["EFlagSelectedModScripts"] = {}; saveSettings()
                    s = [i for i, v in main_config.get('EFlagSelectedModScripts').items() if os.path.exists(os.path.join(mods_folder, "Mods", i, "ModScript.py")) and v.get("enabled") == True]
                    if main_config.get('EFlagSelectedModScripts') and len(s) > 0: printMainMessage(f"Selected Mod Scripts: {', '.join(s)}")
                    else: printMainMessage(f"Selected Mod Scripts: None")
                    printMainMessage("Select an option or a mod to enable/disable!")
                    generated_ui_options = []
                    mods_manifest = generateModsManifest()
                    for i, v in mods_manifest.items():
                        if i == "Original" or i == "OldFont" or i == "GothamFont": continue
                        final_vers = "1.0.0"
                        final_name = ""
                        final_enabled = "❌"
                        final_mod_enabled = "❌"
                        if v.get("version"): final_vers = v.get("version")
                        if v.get("enabled") == True: final_enabled = "✅"
                        else: final_enabled = "❌"
                        if v.get("name") == i: final_name = f"{i}"
                        elif type(v.get("name")) is str: final_name = f"{v.get('name')} [{i}]"
                        else: final_name = f"{i}"
                        if v.get("enabled") == False and v.get("list_in_normal_mods") == False: continue
                        generated_ui_options.append({"index": 1, "message": f"[{final_enabled}] {final_name} [v{final_vers}]", "final_name": final_name, "mod_info": v, "mod_id": i})
                    generated_ui_options.append({"index": 999998, "message": ts("Mod Script Settings")})
                    generated_ui_options.append({"index": 999998.5, "message": ts("Special Mod Settings")})
                    if (main_config.get("EFlagOrangeBloxSyncDir") and os.path.exists(os.path.join(main_config.get("EFlagOrangeBloxSyncDir"), "Mods", "Mods"))): generated_ui_options.append({"index": 999999, "message": ts("Sync Mods from Installation Folder")})
                    generated_ui_options.append({"index": 1000000, "message": ts("Open Mods Folder")})
                    generated_ui_options.append({"index": 1000001, "message": ts("Disable Appling Mods")})
                    generated_ui_options.append({"index": 1000002, "message": ts("Clear Installed Mods [Reinstall Roblox]")})
                    opt = generateMenuSelection(generated_ui_options, star_option=ts("Exit Mods Manager"))
                else:
                    mods_manifest = generateModsManifest()
                    opt = {"index": 999998, "message": ts("Mod Script Settings")}
                if opt:
                    if reverify_mod_script == None: startMessage()
                    printWarnMessage(f"--- {opt['message']} ---")
                    if opt["index"] == 999998:
                        def modScriptsLoop(se):
                            if se == 0: se += 1
                            else: printWarnMessage(f"--- Mod Script Settings ---")
                            if reverify_mod_script == None:
                                printMainMessage("Select the mod scripts you want to be used!")
                                mod_script_generated_ui_options = []
                                for i, v in mods_manifest.items():
                                    if v["mod_script"] == True:
                                        if i == "Original" or i == "OldFont" or i == "GothamFont": continue
                                        final_vers = "1.0.0"
                                        final_name = ""
                                        final_enabled = "❌"
                                        if main_config.get('EFlagSelectedModScripts') and main_config.get('EFlagSelectedModScripts').get(i) and main_config.get('EFlagSelectedModScripts').get(i).get("enabled") == True: final_mod_enabled = "✅"
                                        else: final_mod_enabled = "❌"
                                        if v.get("version"): final_vers = v.get("version")
                                        if v.get("name") == i: final_name = f"{i}"
                                        elif type(v.get("name")) is str: final_name = f"{v.get('name')} [{i}]"
                                        else: final_name = f"{i}"
                                        if v["mod_script_supports"] <= current_version["version"] and v["mod_script_end_support"] > current_version["version"] and v["mod_script_supports_operating_system"] == True: mod_script_generated_ui_options.append({"index": 1, "message": f"[{final_mod_enabled}] {final_name} [v{final_vers}]", "final_name": final_name, "mod_info": v, "mod_id": i})
                                        else: mod_script_generated_ui_options.append({"index": 2, "message": f"[🔒] {final_name} [v{final_vers}]", "final_name": final_name, "mod_info": v, "mod_id": i})
                                mod_script_generated_ui_options.append({"index": 999999, "message": ts(f"Disable Mod Scripts")})
                                mod_script_generated_ui_options.append({"index": 1000000, "message": ts("Reset All Mod Script Configurations")})
                                mod_script_generated_ui_options.append({"index": 1000001, "message": ts("Reset One Mod Script Configuration")})
                                mod_script_generated_ui_options = sorted(mod_script_generated_ui_options, key=lambda x: x["index"])
                            else:
                                mod_script_generated_ui_options = []
                                if mods_manifest and mods_manifest.get(reverify_mod_script):
                                    v = mods_manifest.get(reverify_mod_script)
                                    if v["mod_script"] == True:
                                        final_vers = "1.0.0"
                                        final_name = ""
                                        final_enabled = "❌"
                                        final_mod_enabled = "❌"
                                        if v.get("version"): final_vers = v.get("version")
                                        if main_config.get('EFlagSelectedModScripts') and main_config.get('EFlagSelectedModScripts').get(reverify_mod_script) and main_config.get('EFlagSelectedModScripts').get(reverify_mod_script).get("enabled") == True: final_mod_enabled = "✅"
                                        else: final_mod_enabled = "❌"
                                        if v.get("name") == reverify_mod_script: final_name = f"{reverify_mod_script}"
                                        elif type(v.get("name")) is str: final_name = f"{v.get('name')} [{reverify_mod_script}]"
                                        else: final_name = f"{reverify_mod_script}"
                                        if v["mod_script_supports"] <= current_version["version"] and v["mod_script_end_support"] > current_version["version"] and v["mod_script_supports_operating_system"] == True: mod_script_generated_ui_options.append({"index": 1, "message": f"[{final_mod_enabled}] {final_name} [v{final_vers}]", "final_name": final_name, "mod_info": v, "mod_id": reverify_mod_script})
                                        else: mod_script_generated_ui_options.append({"index": 2, "message": f"[🔒] {final_name} [v{final_vers}]", "final_name": final_name, "mod_info": v, "mod_id": reverify_mod_script})
                                mod_script_generated_ui_options = sorted(mod_script_generated_ui_options, key=lambda x: x["index"])
                            if len(mod_script_generated_ui_options) < 1:
                                if reverify_mod_script == None: printErrorMessage("No Mod Scripts available. Please sync mods with a mod script in order for it to show here!")
                                else: printErrorMessage("There was an issue finding the requested mod script!")
                            else:
                                if reverify_mod_script == None: sel_mod_script = generateMenuSelection(mod_script_generated_ui_options, star_option=ts("Exit Mod Script Settings"))
                                else: sel_mod_script = mod_script_generated_ui_options[0] if len(mod_script_generated_ui_options) > 0 else None
                                if sel_mod_script:
                                    if sel_mod_script["index"] == 999999:
                                        main_config["EFlagSelectedModScripts"] = {}
                                        printSuccessMessage(f'Successfully disabled all mod scripts!')
                                    elif sel_mod_script["index"] == 1000000:
                                        printMainMessage("Are you sure you want to reset ALL Mod Script Configurations? This may cause damage to the scripts if run. (y/n)")
                                        d = input("> ")
                                        if isYes(d) == True:
                                            printMainMessage("Starting Clearing Operation..")
                                            for i, v in mods_manifest.items():
                                                if v["mod_script"] == True and os.path.exists(os.path.join(mods_folder, "Mods", i, f"Configuration_{user_folder_name}")):
                                                    os.remove(os.path.join(mods_folder, "Mods", i, f"Configuration_{user_folder_name}"))
                                                    printMainMessage(f"Removed Mod Script Configuration for {i}")
                                            printSuccessMessage("Successfully cleared all Mod Script Configurations!")
                                        else: printErrorMessage("Canceled Clearing Operation.")
                                    elif sel_mod_script["index"] == 1000001:
                                        mod_script_generated_ui_options2 = []
                                        for i, v in mods_manifest.items():
                                            if v["mod_script"] == True:
                                                if i == "Original" or i == "OldFont" or i == "GothamFont": continue
                                                final_vers = "1.0.0"
                                                final_name = ""
                                                final_enabled = "❌"
                                                if main_config.get('EFlagSelectedModScripts') and main_config.get('EFlagSelectedModScripts').get(i) and main_config.get('EFlagSelectedModScripts').get(i).get("enabled") == True: final_mod_enabled = "✅"
                                                else: final_mod_enabled = "❌"
                                                if v.get("version"): final_vers = v.get("version")
                                                if v.get("name") == i: final_name = f"{i}"
                                                elif type(v.get("name")) is str: final_name = f"{v.get('name')} [{i}]"
                                                else: final_name = f"{i}"
                                                if v["mod_script_supports"] <= current_version["version"] and v["mod_script_end_support"] > current_version["version"] and v["mod_script_supports_operating_system"] == True: mod_script_generated_ui_options2.append({"index": 1, "message": f"[{final_mod_enabled}] {final_name} [v{final_vers}]", "final_name": final_name, "mod_info": v, "mod_id": i})
                                                else: mod_script_generated_ui_options2.append({"index": 2, "message": f"[🔒] {final_name} [v{final_vers}]", "final_name": final_name, "mod_info": v, "mod_id": i})
                                        printMainMessage("Select the mod script you want to reset!")
                                        mod_script_generated_ui_options2 = sorted(mod_script_generated_ui_options2, key=lambda x: x["index"])
                                        sel_mod_script2 = generateMenuSelection(mod_script_generated_ui_options2, star_option=ts("Exit Option"))
                                        if sel_mod_script2 and sel_mod_script2.get("mod_id"):
                                            printMainMessage("Are you sure you want to reset this Mod Script's Configurations? This may cause damage to the scripts if run. (y/n)")
                                            d = input("> ")
                                            if isYes(d) == True:
                                                printMainMessage("Starting Clearing Operation..")
                                                mod_script_id = sel_mod_script2.get("mod_id")
                                                mod_script_info = sel_mod_script2.get("mod_info")
                                                if mod_script_info["mod_script"] == True and os.path.exists(os.path.join(mods_folder, "Mods", mod_script_id, f"Configuration_{user_folder_name}")):
                                                    os.remove(os.path.join(mods_folder, "Mods", mod_script_id, f"Configuration_{user_folder_name}"))
                                                    printMainMessage(f"Removed Mod Script Configuration for {mod_script_id}")
                                                printSuccessMessage(f"Successfully cleared {sel_mod_script2.get('final_name')}'s Mod Script Configurations!")
                                            else: printErrorMessage("Canceled Clearing Operation.")
                                    elif sel_mod_script["index"] == 2:
                                        if sel_mod_script["mod_info"]["mod_script_supports"] > current_version["version"]: printErrorMessage(f"This mod script is unsupported! Please update to OrangeBlox v{sel_mod_script['mod_info']['mod_script_supports']} in order to use!")
                                        else:
                                            printErrorMessage(f"This mod script has reached their end support! Creator Note:")
                                            printErrorMessage(v['mod_info']["mod_script_end_support_reasoning"])
                                    elif sel_mod_script["index"] == 1:
                                        set_mod_script = sel_mod_script["mod_id"]
                                        if sel_mod_script["mod_info"].get("mod_script") == True and os.path.exists(os.path.join(mods_folder, "Mods", set_mod_script, "ModScript.py")) and not (main_config.get("EFlagAllowActivityTracking") == False):
                                            if reverify_mod_script == None and main_config.get("EFlagSelectedModScripts").get(set_mod_script) and main_config.get("EFlagSelectedModScripts").get(set_mod_script).get("enabled") == True: main_config["EFlagSelectedModScripts"][set_mod_script] = {"enabled": False}
                                            else:
                                                printMainMessage("You will enable the following permissions for this script: ")
                                                printMainMessage(sel_mod_script["message"].replace("[✅] ", "", 1).replace("[❌] ", "", 1))
                                                python_modules = sel_mod_script["mod_info"].get("python_modules", [])
                                                permissions_needed = sel_mod_script["mod_info"].get("permissions", [])
                                                sorted_perms_1 = []
                                                for i in permissions_needed:
                                                    if type(i) is str and handler.roblox_event_info.get(i):
                                                        mai = handler.roblox_event_info.get(i)
                                                        sorted_perms_1.append({"level": mai.get("level", 0), "perm": i, "message": mai.get('message')})
                                                    else:
                                                        sorted_perms_1.append({"level": 3, "perm": i, "message": ts("Unknown Requirement")})
                                                        printErrorMessage(f"- Unknown Requirement")
                                                sorted_perms_2 = sorted(sorted_perms_1, key=lambda a: a["level"], reverse=True)
                                                extreme_included = False
                                                for i in sorted_perms_2:
                                                    if i.get("level") == 4:
                                                        print(colors_class.wrap(f"- {i.get('message')}", 201))
                                                        extreme_included = True
                                                    elif i.get("level") == 3: printErrorMessage(f"- {i.get('message')}")
                                                    elif i.get("level") == 2: printWarnMessage(f"- {i.get('message')}")
                                                    elif i.get("level") == 1: printYellowMessage(f"- {i.get('message')}")
                                                    else: printMainMessage(f"- {i.get('message')}")
                                                if len(python_modules) > 0: printYellowMessage(f"- Install and Use Python Modules: {', '.join(python_modules)}")
                                                printYellowMessage("Please check the scripts, permissions above and developer of this mod before using!")
                                                printMainMessage(f"Color Key: {colors_class.wrap(ts('[Extreme]'), 201)} {colors_class.wrap(ts('[Dangerous]'), 196)} {colors_class.wrap(ts('[Caution]'), 202)} {colors_class.wrap(ts('[Warning]'), 226)} {colors_class.wrap(ts('[Normal]'), 255)}")
                                                PyKits.TimerBar(5, "Are you sure you want to use this mod script? (y/n)", False).start()
                                                a = input("> ")
                                                if isYes(a) == True:
                                                    con = True
                                                    if extreme_included == True:
                                                        con = False
                                                        printYellowMessage("THIS SCRIPT WILL BE GRANTED THE EXTREME LEVEL PERMISSIONS LISTED! ARE YOU SURE?")
                                                        for i in sorted_perms_2:
                                                            if i.get("level") == 4: print(colors_class.wrap(f"- {i.get('message')}", 201))
                                                        PyKits.TimerBar(5, "ARE YOU SURE? (y/n)", False).start()
                                                        a = input("> ")
                                                        if isYes(a) == True: con = True
                                                    if con == True:
                                                        actual_permissions = []
                                                        if type(permissions_needed) is list: actual_permissions = permissions_needed
                                                        if type(python_modules) is list and len(python_modules) > 0:
                                                            if not pip_class.installed(python_modules, boolonly=True): pip_class.install(python_modules)
                                                            s = []
                                                            for pyt in python_modules:
                                                                if type(pyt) is str: s.append(f"pip_{pyt}")
                                                            actual_permissions += s
                                                        main_config["EFlagSelectedModScripts"][set_mod_script] = {
                                                            "enabled": True,
                                                            "permissions": actual_permissions,
                                                            "hash": generateFileHash(os.path.join(mods_folder, "Mods", set_mod_script, "ModScript.py"))
                                                        }
                                                        printSuccessMessage(f'Successfully enabled mod script to "{sel_mod_script["final_name"]}"!')
                                                    else:
                                                        if not reverify_mod_script == None: main_config["EFlagSelectedModScripts"][set_mod_script] = {"enabled": False}
                                                else:
                                                    if not reverify_mod_script == None: main_config["EFlagSelectedModScripts"][set_mod_script] = {"enabled": False}
                                        else:
                                            if not reverify_mod_script == None: main_config["EFlagSelectedModScripts"][set_mod_script] = {"enabled": False}
                                    else:
                                        saveSettings()
                                        printSuccessMessage("Successfully saved Mod Script settings!")
                                        return
                                    saveSettings()
                                else:
                                    saveSettings()
                                    printSuccessMessage("Successfully saved Mod Script settings!")
                                    return
                            if reverify_mod_script == None: return modScriptsLoop(se)
                        modScriptsLoop(0)
                    elif opt["index"] == 999998.5:
                        printMainMessage("Would you like to revert the Builder Sans and Monsterrat Fonts and use the old Gotham font instead? (y/n)")
                        printMainMessage(f'Current Setting: {main_config.get("EFlagRemoveBuilderFont", False) == True}')
                        a = input("> ")
                        if isYes(a) == True:
                            main_config["EFlagRemoveBuilderFont"] = True
                            printDebugMessage("User selected: True")
                        elif isNo(a) == True:
                            main_config["EFlagRemoveBuilderFont"] = False
                            printDebugMessage("User selected: False")

                        printMainMessage("Would you like to change the background of the Avatar Editor? (y/n)")
                        printMainMessage(f'Current Setting: {main_config.get("EFlagAvatarEditorBackground")}')
                        c = input("> ")
                        if isYes(c) == True:
                            main_config["EFlagEnableChangeAvatarEditorBackground"] = True
                            def scan_name(a): return os.path.exists(os.path.join(mods_folder, "AvatarEditorMaps", f"{a}.rbxl"))
                            def getName():
                                got_backgrounds = []
                                for i in os.listdir(os.path.join(mods_folder, "AvatarEditorMaps")):
                                    if os.path.isfile(os.path.join(mods_folder, "AvatarEditorMaps", i)) and i.endswith(".rbxl"): got_backgrounds.append(i)
                                printWarnMessage("Select the number that is associated with the map you want to use.")
                                got_backgrounds = sorted(got_backgrounds)
                                count = 1
                                for i in got_backgrounds:
                                    printMainMessage(f"[{str(count)}] = {i}")
                                    count += 1
                                if main_os == "Darwin":
                                    printYellowMessage("[Some avatar maps may not able to run on macOS due to missing objects that are expected in macOS than Windows.]")
                                    printYellowMessage("[Also, if you just added a new map folder into the AvatarEditorMaps folder, please rerun Install.py in order for it to seen.]")
                                a = input("> ")
                                if safeConvertNumber(a):
                                    c = int(a)-1
                                    if c < len(got_backgrounds) and c >= 0:
                                        if got_backgrounds[c]:
                                            b = got_backgrounds[c]
                                            if scan_name(b) == True:
                                                return b
                                            else:
                                                printDebugMessage("Directory is not valid.")
                                                return "Original"
                                        else:
                                            printDebugMessage("User gave a number which is somehow not on the list..?")
                                            return "Original"
                                    else:
                                        printDebugMessage("User gave a number which is out of reach.")
                                        return "Original"
                                else:
                                    printDebugMessage("User gave a response which is not a number.")
                                    return "Original"
                            set_avatar_editor_location = getName()
                            main_config["EFlagAvatarEditorBackground"] = set_avatar_editor_location
                            printSuccessMessage(f"Set avatar background: {set_avatar_editor_location}")
                        elif isNo(c) == True:
                            main_config["EFlagEnableChangeAvatarEditorBackground"] = False
                            printDebugMessage("User selected: False")

                        printMainMessage("Would you like to change the Roblox cursor? (y/n)")
                        printMainMessage(f'Current Setting: {main_config.get("EFlagSelectedCursor")}')
                        c = input("> ")
                        if isYes(c) == True:
                            main_config["EFlagEnableChangeCursor"] = True
                            def scan_name(a): return os.path.exists(os.path.join(mods_folder, "Cursors", a, "ArrowCursor.png")) and os.path.exists(os.path.join(mods_folder, "Cursors", a, "ArrowFarCursor.png"))
                            def getName():
                                got_cursors = []
                                for i in os.listdir(os.path.join(mods_folder, "Cursors")):
                                    if os.path.isdir(os.path.join(mods_folder, "Cursors", i)): got_cursors.append(i)
                                got_cursors = sorted(got_cursors)
                                printWarnMessage("Select the number that is associated with the cursor you want to use.")
                                count = 1
                                for i in got_cursors:
                                    printMainMessage(f"[{str(count)}] = {i}")
                                    count += 1
                                if main_os == "Darwin": printYellowMessage("[Also, if you just added a new cursor folder into the Cursors folder, please rerun Install.py in order for it to seen.]")
                                a = input("> ")
                                if safeConvertNumber(a):
                                    c = int(a)-1
                                    if c < len(got_cursors) and c >= 0:
                                        if got_cursors[c]:
                                            b = got_cursors[c]
                                            if scan_name(b) == True:
                                                return b
                                            else:
                                                printDebugMessage("Directory is not valid.")
                                                return "Original"
                                        else:
                                            printDebugMessage("User gave a number which is somehow not on the list..?")
                                            return "Original"
                                    else:
                                        printDebugMessage("User gave a number which is out of reach.")
                                        return "Original"
                                else:
                                    printDebugMessage("User gave a response which is not a number.")
                                    return "Original"
                            set_cursor_location = getName()
                            main_config["EFlagSelectedCursor"] = set_cursor_location
                            printSuccessMessage(f"Set cursor folder: {set_cursor_location}")
                        elif isNo(c) == True:
                            main_config["EFlagEnableChangeCursor"] = False
                            printDebugMessage("User selected: False")

                        printMainMessage("Would you like to change the Roblox logo on the Roblox Player? (y/n)")
                        printMainMessage(f'Current Setting: {main_config.get("EFlagSelectedBrandLogo")}')
                        c = input("> ")
                        if isYes(c) == True:
                            main_config["EFlagEnableChangeBrandIcons"] = True
                            def scan_name(a): return os.path.exists(os.path.join(mods_folder, "RobloxBrand", a, "AppIcon.icns")) or os.path.exists(os.path.join(mods_folder, "RobloxBrand", a, "AppIcon.ico"))
                            def getName():
                                got_icons = []
                                for i in os.listdir(os.path.join(mods_folder, "RobloxBrand")):
                                    if os.path.isdir(os.path.join(mods_folder, "RobloxBrand", i)): got_icons.append(i)
                                got_icons = sorted(got_icons)
                                printWarnMessage("Select the number that is associated with the icon you want to use.")
                                count = 1
                                for i in got_icons:
                                    printMainMessage(f"[{str(count)}] = {i}")
                                    count += 1
                                if main_os == "Darwin": printYellowMessage("[Also, if you just added a new icon folder into the RobloxBrand folder, please rerun Install.py in order for it to seen.]")
                                a = input("> ")
                                if safeConvertNumber(a):
                                    c = int(a)-1
                                    if c < len(got_icons) and c >= 0:
                                        if got_icons[c]:
                                            b = got_icons[c]
                                            if scan_name(b) == True:
                                                return b
                                            else:
                                                printDebugMessage("Directory is not valid.")
                                                return "Original"
                                        else:
                                            printDebugMessage("User gave a number which is somehow not on the list..?")
                                            return "Original"
                                    else:
                                        printDebugMessage("User gave a number which is out of reach.")
                                        return "Original"
                                else:
                                    printDebugMessage("User gave a response which is not a number.")
                                    return "Original"
                            set_app_icon_location = getName()
                            main_config["EFlagSelectedBrandLogo"] = set_app_icon_location
                            printSuccessMessage(f"Set logo folder: {set_app_icon_location}")
                        elif isNo(c) == True:
                            main_config["EFlagEnableChangeBrandIcons"] = False
                            printDebugMessage("User selected: False")

                        if main_config.get("EFlagRobloxStudioEnabled") == True:
                            printMainMessage("Would you like to change the Roblox logo on Roblox Studio? (y/n)")
                            printMainMessage(f'Current Setting: {main_config.get("EFlagSelectedBrandLogo2")}')
                            if main_os == "Windows": printYellowMessage("The app icon would not change, rather, just the shortcut icon. Enable the Shortcut Icon Changing in order for this work.")
                            c = input("> ")
                            if isYes(c) == True:
                                main_config["EFlagEnableChangeBrandIcons2"] = True
                                def scan_name(a): return os.path.exists(os.path.join(mods_folder, "RobloxStudioBrand", a, "AppIcon.icns")) or os.path.exists(os.path.join(mods_folder, "RobloxStudioBrand", a, "AppIcon.ico"))
                                def getName():
                                    got_icons = []
                                    for i in os.listdir(os.path.join(mods_folder, "RobloxStudioBrand")):
                                        if os.path.isdir(os.path.join(mods_folder, "RobloxStudioBrand", i)): got_icons.append(i)
                                    got_icons = sorted(got_icons)
                                    printWarnMessage("Select the number that is associated with the icon you want to use.")
                                    count = 1
                                    for i in got_icons:
                                        printMainMessage(f"[{str(count)}] = {i}")
                                        count += 1
                                    if main_os == "Darwin": printYellowMessage("[Also, if you just added a new icon folder into the RobloxStudioBrand folder, please rerun Install.py in order for it to seen.]")
                                    a = input("> ")
                                    if safeConvertNumber(a):
                                        c = int(a)-1
                                        if c < len(got_icons) and c >= 0:
                                            if got_icons[c]:
                                                b = got_icons[c]
                                                if scan_name(b) == True: return b
                                                else:
                                                    printDebugMessage("Directory is not valid.")
                                                    return "Original"
                                            else:
                                                printDebugMessage("User gave a number which is somehow not on the list..?")
                                                return "Original"
                                        else:
                                            printDebugMessage("User gave a number which is out of reach.")
                                            return "Original"
                                    else:
                                        printDebugMessage("User gave a response which is not a number.")
                                        return "Original"
                                set_app_icon_location = getName()
                                main_config["EFlagSelectedBrandLogo2"] = set_app_icon_location
                                printSuccessMessage(f"Set logo folder: {set_app_icon_location}")
                            elif isNo(c) == True:
                                main_config["EFlagEnableChangeBrandIcons2"] = False
                                printDebugMessage("User selected: False")

                        if main_os == "Windows": 
                            printMainMessage("Would you like to use the Roblox Brand Icon as the Shortcut Icon? (y/n)")
                            printMainMessage(f'Current Setting: {main_config.get("EFlagUseRobloxAppIconAsShortcutIcon", False) == True}')
                            a = input("> ")
                            if isYes(a) == True:
                                main_config["EFlagUseRobloxAppIconAsShortcutIcon"] = True
                                printDebugMessage("User selected: True")
                            elif isNo(a) == True:
                                main_config["EFlagUseRobloxAppIconAsShortcutIcon"] = False
                                printDebugMessage("User selected: False")

                            printMainMessage("Would you like to enable selected Roblox icon for when Roblox Player/Studio is running? (y/n)")
                            printMainMessage(f'Current Setting: {main_config.get("EFlagReplaceRobloxRuntimeIconWithModIcon", False) == True}')
                            printYellowMessage('Warning! This setting may cause issues and will take a moment for the handler to settle!')
                            a = input("> ")
                            if isYes(a) == True:
                                main_config["EFlagReplaceRobloxRuntimeIconWithModIcon"] = True
                                printDebugMessage("User selected: True")
                            elif isNo(a) == True:
                                main_config["EFlagReplaceRobloxRuntimeIconWithModIcon"] = False
                                printDebugMessage("User selected: False")

                        printMainMessage("Would you like to change your Roblox player sounds? (y/n)")
                        printMainMessage(f'Current Setting: {main_config.get("EFlagSelectedPlayerSounds")}')
                        c = input("> ")
                        if isYes(c) == True:
                            main_config["EFlagEnableChangePlayerSound"] = True
                            def scan_name(a): return os.path.exists(os.path.join(mods_folder, "PlayerSounds", a))
                            def getName():
                                got_sounds = []
                                for i in os.listdir(os.path.join(mods_folder, "PlayerSounds")):
                                    if os.path.isdir(os.path.join(mods_folder, "PlayerSounds", i)): got_sounds.append(i)
                                got_sounds = sorted(got_sounds)
                                printWarnMessage("Select the number that is associated with the player sounds you want to use.")
                                count = 1
                                for i in got_sounds:
                                    printMainMessage(f"[{str(count)}] = {i}")
                                    count += 1
                                if main_os == "Darwin": printYellowMessage("[Also, if you just added a new sound pack into the PlayerSounds folder, please rerun Install.py in order for it to seen.]")
                                a = input("> ")
                                if safeConvertNumber(a):
                                    c = int(a)-1
                                    if c < len(got_sounds) and c >= 0:
                                        if got_sounds[c]:
                                            b = got_sounds[c]
                                            if scan_name(b) == True:
                                                return b
                                            else:
                                                printDebugMessage("Directory is not valid.")
                                                return "Current"
                                        else:
                                            printDebugMessage("User gave a number which is somehow not on the list..?")
                                            return "Current"
                                    else:
                                        printDebugMessage("User gave a number which is out of reach.")
                                        return "Current"
                                else:
                                    printDebugMessage("User gave a response which is not a number.")
                                    return "Current"
                            set_player_sounds = getName()
                            main_config["EFlagSelectedPlayerSounds"] = set_player_sounds
                            printSuccessMessage(f"Set player sounds: {set_player_sounds}")
                        elif isNo(c) == True:
                            main_config["EFlagEnableChangePlayerSound"] = False
                            printDebugMessage("User selected: False")
                        saveSettings()
                    elif opt["index"] == 999999:
                        printMainMessage("Syncing mods..")
                        sync_folder_names = ["AvatarEditorMaps", "Cursors", "PlayerSounds", "RobloxBrand", "RobloxStudioBrand", "Mods"]
                        for sync_folder_name in sync_folder_names:
                            targeted_sync_location = os.path.join(main_config.get("EFlagOrangeBloxSyncDir"), "Mods", sync_folder_name)
                            if os.path.exists(targeted_sync_location) and os.path.isdir(targeted_sync_location):
                                for i in os.listdir(targeted_sync_location):
                                    syncing_mod_path = os.path.join(targeted_sync_location, i)
                                    if os.path.isdir(syncing_mod_path):
                                        installed_mod_path = os.path.join(mods_folder, sync_folder_name, i)
                                        if os.path.exists(installed_mod_path): 
                                            for e in os.listdir(installed_mod_path):
                                                if not (e == f"Configuration_{user_folder_name}" or e == "__pycache__"): 
                                                    if os.path.isdir(os.path.join(installed_mod_path, e)): shutil.rmtree(os.path.join(installed_mod_path, e), ignore_errors=True)
                                                    else: os.remove(os.path.join(installed_mod_path, e))
                                        def ignore_files_func(dir, files): 
                                            config_files = [fi for fi in os.listdir(dir) if fi.startswith("Configuration_")]
                                            return set(["__pycache__"] + config_files)
                                        pip_class.copyTreeWithMetadata(syncing_mod_path, installed_mod_path, dirs_exist_ok=True, ignore=ignore_files_func)
                                printDebugMessage(f"Successfully synced mod type: {sync_folder_name}")
                            else: printDebugMessage(f"There was an issue trying to copy files for mod type: {sync_folder_name}")
                        printSuccessMessage("Successfully synced all mods from installation folder!")
                    elif opt["index"] == 1000000:
                        printMainMessage("Opening Mods Folder..")
                        if main_os == "Darwin": re = subprocess.run(["/usr/bin/open", os.path.join(mods_folder)])
                        else: re = subprocess.run(f"start {os.path.join(mods_folder)}", shell=True)
                        if re.returncode == 0: printSuccessMessage("Successfully opened Mods folder!")
                        else: printErrorMessage("Unable to open Mods folder!")
                    elif opt["index"] == 1000001:
                        printMainMessage("Disabling mods..")
                        main_config["EFlagEnableMods"] = False
                        saveSettings()
                        printSuccessMessage("Successfully disabled Mods! Would you like to reinstall Roblox to clear existing mods or continue with partial setup?")
                        if main_os == "Windows": printYellowMessage("WARNING! This will quit any open Roblox windows!")
                        d = input("> ")
                        if isYes(d) == True:
                            submit_status.start()
                            res = handler.installRoblox(forceQuit=main_os == "Windows", debug=(main_config.get("EFlagEnableDebugMode") == True), copyRobloxInstallerPath=(main_os == "Darwin" and os.path.join(cur_path, "RobloxPlayerInstaller.app") or os.path.join(cur_path, "RobloxPlayerInstaller.exe")), downloadInstaller=True, verifyInstall=not (main_config.get("EFlagVerifyRobloxHashAfterInstall")==False), downloadToken=createDownloadToken(studio=False))
                            submit_status.end()
                            if res and res["success"] == False: printErrorMessage("There is an issue while trying to install Roblox. Please try again by restarting this app!")
                        elif isNo(d) == True:
                            saveSettings()
                            printDebugMessage("User selected: False")
                            return
                        printMainMessage("Exiting Mods Manager..")
                        return
                    elif opt["index"] == 1000002: continueToInstallRobloxOptions(reinstall=True)
                    else:
                        if not (main_config.get("EFlagEnabledMods") and type(main_config.get("EFlagEnabledMods")) is dict): main_config["EFlagEnabledMods"] = {}
                        if opt.get("mod_info"):
                            if opt["mod_info"]["enabled"] == True:
                                main_config["EFlagEnabledMods"][opt["mod_id"]] = False
                                printSuccessMessage(f"Successfully disabled mod {opt.get('final_name')}!")
                            else:
                                main_config["EFlagEnabledMods"][opt["mod_id"]] = True
                                printSuccessMessage(f"Successfully enabled mod {opt.get('final_name')}!")
                        saveSettings()
                    if reverify_mod_script == None: mainModManager()
                    else: printMainMessage("Exiting Mods Manager.."); return 5
                else: return
            if not (main_config.get("EFlagDisableModsManagerAccess") == True): mainModManager()
            else:
                printWarnMessage("--- Mods Manager ---")
                printErrorMessage("Access to editing Mods was disabled by file. Please try again later!")
                input("> ")
                return ts("Mods Settings was not saved!")
        else:
            printWarnMessage("--- Mods Manager ---")
            printErrorMessage("Mods Enabled: No")
            printMainMessage("Would you like to enable Mods? (y/n)")
            b = input("> ")
            if isYes(b) == True:
                main_config["EFlagEnableMods"] = True
                saveSettings()
                continueToModsManager(reverify_mod_script)
    def continueToUpdates(): # Check for Updates
        printWarnMessage("--- Checking for Bootstrap Updates ---")
        printDebugMessage("Setting Installed App Path to Local User..") 
        if main_os == "Darwin": setInstalledAppPath(os.path.realpath(os.path.join(macos_app_path, "../") + "/"))
        elif main_os == "Windows": setInstalledAppPath(os.path.realpath(cur_path))
        printDebugMessage("Sending Request to Bootstrap Version Servers..") 
        version_server = main_config.get("EFlagBootstrapUpdateServer", "https://obx.efaz.dev/Version.json")
        if not (type(version_server) is str and version_server.startswith("https://")): version_server = "https://obx.efaz.dev/Version.json"
        try: latest_vers_res = requests.get(f"{version_server}", headers={"X-Bootstrap-Version": current_version["version"], "X-Python-Version": platform.python_version(), "X-Authorization-Key": main_config.get("EFlagUpdatesAuthorizationKey", "")})
        except Exception as e: latest_vers_res = PyKits.InstantRequestJSONResponse(ok=False)
        if latest_vers_res.ok:
            latest_vers = latest_vers_res.json
            if current_version.get("version"):
                printDebugMessage(f'Called ({version_server}): {latest_vers}') 
                if current_version.get("version", "1.0.0") < latest_vers.get("latest_version", "1.0.0"):
                    download_location = latest_vers.get("download_location", "https://github.com/EfazDev/orangeblox/archive/refs/heads/main.zip")
                    printDebugMessage(f"Update v{latest_vers['latest_version']} detected!")
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
                        printYellowMessage("⚠️ For information about this update, use this link: https://github.com/EfazDev/orangeblox/releases")
                        printSuccessMessage(f"⚠️ Download Location: {download_location}")
                    elif not (main_config.get("EFlagUpdatesAuthorizationKey", "") == ""):
                        printYellowMessage("🔨 This version is an update configured from an organization (this may still be a modified and an unofficial OrangeBlox version.)")
                        printYellowMessage("🔨 For information about this update, contact your administrator!")
                        printSuccessMessage(f"🔨 Download Location: {download_location}")
                    else:
                        printErrorMessage("❌ The download location is different from the official GitHub link!")
                        printErrorMessage("❌ You may be downloading an unofficial OrangeBlox version! Download a copy from https://github.com/EfazDev/orangeblox!")
                        printSuccessMessage(f"❌ Download Location: {download_location}")
                    printSuccessMessage(f"v{current_version.get('version', '1.0.0')} [Current] => v{latest_vers['latest_version']} [Latest]")
                    if isYes(input("> ")) == True:
                        printDebugMessage(f"Saving Settings..")
                        saveSettings()
                        printMainMessage("Downloading latest version..")
                        printDebugMessage(f"Download location: {download_location} => {os.path.join(cur_path, 'Update.zip')}")
                        try:
                            download_update = requests.download(download_location, os.path.join(cur_path, 'Update.zip'))
                            if download_update.ok:
                                printMainMessage("Download Success! Extracting ZIP now!")
                                zip_extract = pip_class.unzipFile(os.path.join(cur_path, "Update.zip"), os.path.join(cur_path, 'Update'), ["Main.py", "RobloxFastFlagsInstaller.py", "OrangeAPI.py", "Configuration.json", "Apps"])
                                if zip_extract.returncode == 0:
                                    printMainMessage("Extracted successfully! Installing Files!")
                                    try:
                                        for file in os.listdir(os.path.join(cur_path, 'Update')):
                                            src_path = os.path.join(os.path.join(cur_path, 'Update'), file)
                                            dest_path = os.path.join(cur_path, file)
                                            if os.path.isdir(src_path):
                                                try: pip_class.copyTreeWithMetadata(src_path, dest_path, dirs_exist_ok=True)
                                                except Exception as e: printDebugMessage(f"Update Error for directory ({src_path}): \n{trace()}")
                                            else:
                                                if (not file.endswith(".json")) or file == "Version.json":
                                                    try: shutil.copy2(src_path, dest_path)
                                                    except Exception as e: printDebugMessage(f"Update Error for file ({src_path}): \n{trace()}")
                                        if main_config.get("EFlagOrangeBloxSyncDir") and os.path.exists(main_config.get("EFlagOrangeBloxSyncDir")):
                                            printMainMessage("Extending Changes to Installation Folder..")
                                            for file in os.listdir(os.path.join(cur_path, 'Update')):
                                                src_path = os.path.join(os.path.join(cur_path, 'Update'), file)
                                                dest_path = os.path.join(main_config.get("EFlagOrangeBloxSyncDir"), file)
                                                if os.path.isdir(src_path):
                                                    try: pip_class.copyTreeWithMetadata(src_path, dest_path, dirs_exist_ok=True)
                                                    except Exception as e: printDebugMessage(f"Update Error for directory ({src_path}): \n{trace()}")
                                                else:
                                                    if (not file.endswith(".json")) or file == "Version.json":
                                                        try: shutil.copy2(src_path, dest_path)
                                                        except Exception as e: printDebugMessage(f"Update Error for file ({src_path}): \n{trace()}")
                                        if os.path.exists(generateFileKey("OrangeBloxUpdate")): os.remove(generateFileKey("OrangeBloxUpdate"))
                                        printMainMessage("Running Installer..")
                                        if main_os == "Windows":
                                            if len(given_args) > 1:
                                                filtered_args = given_args[1]
                                                if (("roblox-player:" in filtered_args) or ("roblox-studio:" in filtered_args) or ("roblox-studio-auth:" in filtered_args) or ("roblox:" in filtered_args) or ("efaz-bootstrap:" in filtered_args) or ("orangeblox:" in filtered_args)):
                                                    printMainMessage(f"Creating URL Exchange file..")
                                                    with open(os.path.join(cur_path, "URLSchemeExchange"), "w", encoding="utf-8") as f: f.write(filtered_args)
                                            silent_install = subprocess.run(f'start cmd.exe /c ""{sys.executable}" "{os.path.join(cur_path, "Install.py")}" --update-mode"', shell=True, cwd=cur_path)
                                            if not (silent_install.returncode == 0): printErrorMessage("Bootstrap Installer failed.")
                                            try:
                                                printMainMessage("Cleaning up files..")
                                                os.remove(os.path.join(cur_path, 'Update.zip'))
                                                shutil.rmtree(os.path.join(cur_path, 'Update'))
                                            except Exception as e:
                                                printErrorMessage("Something went wrong while cleaning the files for OrangeBlox update!")
                                                printDebugMessage(f"Cleaning Error: \n{trace()}")
                                            sys.exit(0)
                                        else:
                                            silent_install = stdout.run_process(args=[sys.executable, "Install.py", "--update-mode"], cwd=cur_path)
                                            if not (silent_install.returncode == 0): printErrorMessage("Bootstrap Installer failed.")
                                    except Exception as e:
                                        printErrorMessage("Something went wrong while updating the files for OrangeBlox!")
                                        printDebugMessage(f"Updating Error: \n{trace()}")
                                    try:
                                        printMainMessage("Cleaning up files..")
                                        os.remove(os.path.join(cur_path, 'Update.zip'))
                                        shutil.rmtree(os.path.join(cur_path, 'Update'), ignore_errors=True)
                                    except Exception as e:
                                        printErrorMessage("Something went wrong while cleaning the files for OrangeBlox update!")
                                        printDebugMessage(f"Cleaning Error: \n{trace()}")
                                    printSuccessMessage(f"Update to v{latest_vers['version']} was finished successfully! Restarting bootstrap..")
                                    pip_class.restartScript("Main.py", given_args)
                                    sys.exit(0)
                                else:
                                    try:
                                        printMainMessage("Cleaning up files..")
                                        os.remove(os.path.join(cur_path, 'Update.zip'))
                                        shutil.rmtree(os.path.join(cur_path, 'Update'), ignore_errors=True)
                                    except Exception as e:
                                        printErrorMessage("Something went wrong while cleaning the files for OrangeBlox update!")
                                        printDebugMessage(f"Update Error: \n{trace()}")
                                    printErrorMessage("There was an issue extracting the update due to an error!")
                                    return ts("Update was unable to be installed!")
                            else:
                                printErrorMessage("There was an issue downloading the update due to an curl error!")
                                return ts("Update was unable to be installed!")
                        except Exception as e:
                            printErrorMessage("There was an issue downloading the update due to an curl error!")
                            return ts("Update was unable to be installed!")
                    else:
                        printDebugMessage("User rejected update.")
                        return ts("Update was cancelled!")
                elif current_version.get("version", "1.0.0") > latest_vers.get("latest_version", "1.0.0"):
                    printSuccessMessage("OrangeBlox is in a beta version! No updates are needed!")
                    return ts("No updates are needed!")
                else:
                    printMainMessage("OrangeBlox is currently on the latest version! No updates are needed!")
                    return ts("No updates are needed!")
            else:
                printDebugMessage("There was an error reading the latest version.")
                return ts("There was an issue while checking for updates.")
        else:
            printDebugMessage("Update Check Response failed.")
            return ts("There was an issue while checking for updates.")

    # Main Menu
    try:
        def main_menu():
            global main_config
            global given_args
            global run_studio
            global skip_modification_mode
            if (not (main_config.get("EFlagRemoveMenuAndSkipToRoblox") == True)) or (len(given_args) > 1 and "efaz-bootstrap:" in given_args[1]) or (len(given_args) > 1 and "orangeblox:" in given_args[1]):
                startMessage()
                if os.path.exists(os.path.join(cur_path, "Backup.obx")):
                    printWarnMessage("--- OrangeBlox Backup Assistant ---")
                    printMainMessage("It seems that you have installed OrangeBlox with a backup file included.")
                    printMainMessage(f"Path: {os.path.join(cur_path, 'Backup.obx')}")
                    printMainMessage("Would you like to restore the data on it? (y/n)")
                    printYellowMessage("This will overwrite your current configuration and mods!!")
                    back = input("> ")
                    if isYes(back) == True:
                        backup_path = os.path.join(cur_path, "Backup")
                        backup_file = os.path.join(cur_path, "Backup.obx")
                        try:
                            printMainMessage("Unwrapping OrangeBlox file..")
                            makedirs(backup_path)
                            zip_extract = pip_class.unzipFile(backup_file, backup_path, ["FastFlagConfiguration.json", "Cursors", "Mods", "RobloxBrand"])
                            if zip_extract.returncode == 0:
                                printMainMessage("Copying Configuration.json..")
                                if os.path.exists(os.path.join(backup_path, "FastFlagConfiguration.json")):
                                    with open(os.path.join(backup_path, "FastFlagConfiguration.json"), "r", encoding="utf-8") as f: main_config = json.load(f)
                                else:
                                    with open(os.path.join(backup_path, "Configuration.json"), "rb") as f: obfuscated_json = f.read()
                                    try: obfuscated_json = json.loads(obfuscated_json)
                                    except Exception as e: obfuscated_json = json.loads(zlib.decompress(obfuscated_json).decode("utf-8"))
                                    main_config = obfuscated_json
                                saveSettings()
                                printMainMessage("Copying AvatarEditorMaps..")
                                pip_class.copyTreeWithMetadata(os.path.join(backup_path, "AvatarEditorMaps"), os.path.join(mods_folder, "AvatarEditorMaps"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                printMainMessage("Copying Cursors..")
                                pip_class.copyTreeWithMetadata(os.path.join(backup_path, "Cursors"), os.path.join(mods_folder, "Cursors"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                if os.path.exists(os.path.join(backup_path, "PlayerSounds")):
                                    printMainMessage("Copying PlayerSounds..")
                                    pip_class.copyTreeWithMetadata(os.path.join(backup_path, "PlayerSounds"), os.path.join(mods_folder, "PlayerSounds"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                else:
                                    printMainMessage("Copying DeathSounds..")
                                    pip_class.copyTreeWithMetadata(os.path.join(backup_path, "DeathSounds"), os.path.join(mods_folder, "DeathSounds"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                    if os.path.exists(os.path.join(mods_folder, "DeathSounds")):
                                        for i in os.listdir(os.path.join(mods_folder, "DeathSounds")):
                                            if os.path.isfile(os.path.join(mods_folder, "DeathSounds", i)):
                                                possible_name = i.split(".")
                                                if len(possible_name) > 1: possible_name = possible_name[0]
                                                else: possible_name = i
                                                makedirs(os.path.join(backup_path, "PlayerSounds", possible_name))
                                                shutil.copy(os.path.join(mods_folder, "DeathSounds", i), os.path.join(mods_folder, "PlayerSounds", possible_name, "ouch.ogg"), follow_symlinks=False)
                                        shutil.rmtree(os.path.join(mods_folder, "DeathSounds"), ignore_errors=True)
                                printMainMessage("Copying Mods..")
                                pip_class.copyTreeWithMetadata(os.path.join(backup_path, "Mods"), os.path.join(mods_folder, "Mods"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                printMainMessage("Copying RobloxBrand..")
                                pip_class.copyTreeWithMetadata(os.path.join(backup_path, "RobloxBrand"), os.path.join(mods_folder, "RobloxBrand"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                printMainMessage("Copying RobloxStudioBrand..")
                                pip_class.copyTreeWithMetadata(os.path.join(backup_path, "RobloxStudioBrand"), os.path.join(mods_folder, "RobloxStudioBrand"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                printMainMessage("Finished transferring! Deleting backup data..")
                                if os.path.exists(backup_path): shutil.rmtree(backup_path, ignore_errors=True)
                                if os.path.exists(os.path.join(cur_path, "Backup.obx")): os.remove(os.path.join(cur_path, "Backup.obx"))
                                printSuccessMessage("Successfully restored OrangeBlox data! Would you to restart the app? (y/n)")
                                a = input("> ")
                                if isYes(a) == True: pip_class.restartScript("Main.py", sys.argv)
                                else: sys.exit(0)
                            else: raise Exception("There was an issue trying to open the OrangeBlox file! Make sure it's readable before trying again!")
                        except Exception as e:
                            printErrorMessage("There was an error trying to restore your OrangeBlox files!")
                            printErrorMessage(f"Python Exception: \n{trace()}")
                            input("> ")
                            sys.exit(0)
                            return
                if not (main_config.get("EFlagCompletedTutorial") == True): # Tutorial        
                    printWarnMessage("--- Tutorial ---")
                    printMainMessage("Welcome to OrangeBlox 🍊!")
                    printMainMessage("OrangeBlox is a Roblox bootstrap that allows you to add modifications to your Roblox client using files, activity tracking and Python!")
                    printMainMessage("Before we get started, there's some information that may be needed to know.")
                    if validateInstallation(): printSuccessMessage("Installation Valid! You may continue! [✅]")
                    else:
                        printErrorMessage("Installation Invalid! Please use Install.py! [❌]")
                        input("> ")
                        sys.exit(0)
                    information_num = 1
                    printWarnMessage(f"--- Info #{information_num} ---")
                    printMainMessage("There's lot of permissions that are needed to be set in order for this bootstrap to work.")
                    printMainMessage("For example, it may ask you to allow access to the Roblox app files or allow access to a Terminal. Please put it in always allow in order to allow OrangeBlox to function properly!")
                    input("> ")
                    information_num += 1
                    printWarnMessage(f"--- Info #{information_num} ---")
                    printMainMessage("Since this bootstrap is made using Python, anti-viruses may report this app as a virus.")
                    printMainMessage("For example, Windows Defender may detect OrangeBlox with Win32/Wacapew.C!ml. You may need to authorize the app through your anti-virus or build the app directly in order to allow use.")
                    input("> ")
                    information_num += 1
                    printWarnMessage(f"--- Info #{information_num} ---")
                    printMainMessage("Most features are based on Activity Tracking, a watching system based on watching Roblox logs in response of actions.")
                    printMainMessage("This app will use your Roblox logs to track data such as Game Join Data, Discord Presences, BloxstrapRPC and a lot more!")
                    printMainMessage("If you wish to change these settings, once you get to the settings menu, go to the Activity Tracking settings!")
                    printYellowMessage("This will not get you banned as this is based on files, not interrupting the client.")
                    input("> ")
                    information_num += 1
                    printWarnMessage(f"--- Info #{information_num} ---")
                    displayNotification(ts("Hello!"), ts("If you see this, your notifications are set up! Great job!"))
                    printMainMessage("We have just sent a notification to your computer, so that you can allow notifications")
                    printYellowMessage("Depending on your OS (Windows or macOS), you may be able to select Allow for features like Server Locations to work!")
                    input("> ")
                    information_num += 1
                    printWarnMessage(f"--- Info #{information_num} ---")
                    printMainMessage("If you haven't noticed, we have also installed a Play Roblox and Run Studio app into your system!")
                    printMainMessage("This will allow you to skip the main menu and launch Roblox instantly through OrangeBlox!")
                    if main_os == "Darwin": printMainMessage("You may find this in your Applications folder or through Launchpad!")
                    elif main_os == "Windows": printMainMessage("You may find this in your Start Menu or Desktop!")
                    input("> ")
                    information_num += 1
                    printWarnMessage(f"--- Info #{information_num} ---")
                    printMainMessage("If you have issues with OrangeBlox, you may report it on GitHub using the issues page:")
                    printMainMessage("https://github.com/EfazDev/orangeblox/issues")
                    printErrorMessage("However, please check if you're on the latest bootstrap version first before continuing. If you don't have the latest version, please do!")
                    printYellowMessage("If you want to uninstall this bootstrap, you may run the Install.py script which you ran to be here and select Uninstall!")
                    printYellowMessage("Additionally, you can use the Reinstall Roblox option in the settings menu to prevent uninstalling this.")
                    printWarnMessage("--- Step 1 ---")
                    printMainMessage("Alright, now that you have read all the needed information, let's get started! First, it's important that you best understand on how the choosing works.")
                    printMainMessage("Let\'s say you want to enable an option (use the prompt here for the example), just type \"y\" and hit enter!")
                    printMainMessage("For example in this case:")
                    printMainMessage("--------------------")
                    printMainMessage("Are you sure you want to use this flag? (y/n)")
                    printMainMessage("> y")
                    printMainMessage("Enabled!")
                    printMainMessage("--------------------")
                    printMainMessage('Let\'s start off with a quick input! ')
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
                    printMainMessage("--------------------")
                    printMainMessage("Are you sure you want to use this flag? (y/n)")
                    printMainMessage("> n")
                    printMainMessage("Disabled!")
                    printMainMessage("--------------------")
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
                    printMainMessage("The list contains a number that can be used to select which option to choose!")
                    printMainMessage("--------------------")
                    printMainMessage("What option to choose? (y/n)")
                    printMainMessage("[1] = Do jumping-jacks")
                    printMainMessage("[2] = Do push-ups")
                    printMainMessage("[3] = Do all of the above")
                    printMainMessage("> 2")
                    printMainMessage("Selected Do push-ups!")
                    printMainMessage("--------------------")
                    printMainMessage("Now, try for yourself!")
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
                    printWarnMessage("--- Step 4 ---")
                    if os.path.exists(os.path.join(cur_path, "Translations")):
                        printMainMessage("Alright! Now, select the bootstrap language you want to use! (English is default, you can just continue)")
                        langs_sel = []
                        co = 0
                        for i, v in language_names.items():
                            co += 1
                            langs_sel.append({
                                "index": co,
                                "message": v,
                                "code": i
                            })
                        selected_language = generateMenuSelection(langs_sel, before_input=ts(f"Current Language: {language_names[main_config.get('EFlagSelectedBootstrapLanguage', 'en')]}\n[WARNING! All messages are translated from Google Translate and may provide incorrect or malformed information.]"))
                        if selected_language:
                            main_config["EFlagSelectedBootstrapLanguage"] = selected_language["code"]
                            stdout.translation_obj.load_new_language(selected_language["code"])
                            printMainMessage(f"Successfully set language to {language_names[main_config.get('EFlagSelectedBootstrapLanguage', 'en')]}! All future messages are now translated in this language.")
                    if not (main_config.get("EFlagDisableSettingsAccess") == True):
                        printWarnMessage("--- Step 5 ---")
                        printMainMessage("Nice job! Oh yea, during the tutorial, it repeated with a \"Not quite\" if you gave an incorrect input or response. However, it will close the window in future prompts like in main menu.")
                        printYellowMessage("Additionally, if you do meet with an option with a *, this means that any input will result with that option.")
                        printMainMessage("Anyways, welcome to step 4! Here, you can select your settings!")
                        printMainMessage("In the settings menu, you can just input nothing or anything else instead of y or n to skip the option without affecting the current state of it.")
                        printMainMessage("See you after a little bit!")
                        input("> ")
                        continueToSettings()
                    if not (main_config.get("EFlagDisableFastFlagInstallAccess") == True):
                        printWarnMessage("--- Step 6 ---")
                        printMainMessage("Welcome back! I hope you have enabled some things you may want!")
                        printMainMessage("Now, let's get more customizable! Next, you will be able to select your fast flags.")
                        printYellowMessage("But before, prepare yourself your Roblox User ID (if you're not currently logged in). It will be used for some settings depending on what you select.")
                        input("> ")
                        continueToFFlagInstaller()
                    if not (main_config.get("EFlagDisableModsManagerAccess") == True):
                        printWarnMessage("--- Step 7 ---")
                        printMainMessage("Hey! You made it through the list again!")
                        printMainMessage("Now, let's explore the Mods category. Mods are files that can be used to edit your Roblox client such as a custom theme or font. Today, you will be configuring that.")
                        printYellowMessage("If you want to get your own mods and install them, open the Mods Manager and use the open folder command! This will help you where to put the extracted mod.")
                        input("> ")
                        continueToModsManager()
                    printWarnMessage("--- Final Touches ---")
                    printSuccessMessage("Woo hoo! You finally reached the end of this tutorial!")
                    printSuccessMessage("I hope you learned from this and how you may use Roblox using this bootstrap!")
                    printSuccessMessage("For now, before you continue, I hope you have a great day!")
                    input("> ")
                    getSettings()
                    main_config["EFlagCompletedTutorial"] = True
                    saveSettings()
                    startMessage()
                if (len(given_args) < 2):
                    if not validateInstallation():
                        printWarnMessage("--- Install Required! ---")
                        printMainMessage("Please install OrangeBlox from running Install.py in order to continue!")
                        input("> ")
                        sys.exit(0)
                    generated_ui_options = []
                    generated_ui_options.append({
                        "index": 1, 
                        "message": ts("Continue to Roblox [Multi-Instance]") if main_config.get("EFlagEnableDuplicationOfClients") == True else ts("Continue to Roblox"), 
                        "func": continueToRoblox, 
                        "go_to_rbx": False
                    })
                    if main_config.get("EFlagRobloxStudioEnabled") == True:
                        generated_ui_options.append({
                            "index": 2, 
                            "message": ts("Continue to Roblox Studio"),
                            "func": continueToRoblox, 
                            "go_to_rbx": False,
                            "studio": True
                        })
                    if not (main_config.get("EFlagAllowActivityTracking") == False):
                        if handler.getIfRobloxIsOpen():
                            generated_ui_options.append({
                                "index": 3, 
                                "message": ts("Connect to Existing Roblox"), 
                                "func": connectExistingRobloxWindow, 
                                "go_to_rbx": False
                            })
                        if main_config.get("EFlagRobloxStudioEnabled") == True and handler.getIfRobloxIsOpen(studio=True):
                            generated_ui_options.append({
                                "index": 4, 
                                "message": ts("Connect to Existing Roblox Studio"), 
                                "func": connectExistingRobloxWindow, 
                                "go_to_rbx": False,
                                "studio": True
                            })
                    if not (main_config.get("EFlagDisableFastFlagInstallAccess") == True):
                        generated_ui_options.append({
                            "index": 5, 
                            "message": ts("Run Fast Flag Installer"), 
                            "func": continueToFFlagInstaller, 
                            "go_to_rbx": True,
                            "end_mes": ts("FFlag Installer has finished!"),
                            "clear_console": True
                        })
                    if not (main_config.get("EFlagDisableModsManagerAccess") == True):
                        generated_ui_options.append({
                            "index": 6, 
                            "message": ts("Open Mods Manager"), 
                            "func": continueToModsManager, 
                            "go_to_rbx": True, 
                            "end_mes": ts("Mod Settings has been saved!"),
                            "clear_console": True
                        })
                    if not (main_config.get("EFlagDisableSettingsAccess") == True):
                        generated_ui_options.append({
                            "index": 7, 
                            "message": ts("Open Settings"), 
                            "func": continueToSettings, 
                            "go_to_rbx": True, 
                            "end_mes": ts("Settings has been saved!"),
                            "clear_console": True
                        })
                    if not (main_config.get("EFlagDisableLinkShortcutsAccess") == True):
                        generated_ui_options.append({
                            "index": 8, 
                            "message": ts("Roblox Link Shortcuts"), 
                            "func": continueToLinkShortcuts, 
                            "go_to_rbx": False, 
                            "end_mes": ts("Roblox Link Shortcut Settings are now saved!"),
                            "clear_console": True
                        })
                    if not (main_config.get("EFlagDisablePythonUpdateChecks") == True):
                        current_python_version = pip_class.getCurrentPythonVersion()
                        is_python_beta = pip_class.getIfPythonVersionIsBeta()
                        def python_update_check():
                            latest_python_version = pip_class.getLatestPythonVersion(beta=is_python_beta)
                            if (not (current_python_version == latest_python_version)) and latest_python_version:
                                if os.path.exists(generateFileKey("PythonUpdate")):
                                    with open(generateFileKey("PythonUpdate"), "r") as f: ss = f.read()
                                    if ss == latest_python_version: return
                                with open(generateFileKey("PythonUpdate"), "w", encoding="utf-8") as f: f.write(latest_python_version)
                            elif latest_python_version and os.path.exists(generateFileKey("PythonUpdate")): os.remove(generateFileKey("PythonUpdate"))
                        threading.Thread(target=python_update_check, daemon=True).start()
                        if os.path.exists(generateFileKey("PythonUpdate")):
                            with open(generateFileKey("PythonUpdate"), "r") as f: latest_python_version = f.read()
                            if (not (current_python_version == latest_python_version)) and latest_python_version:
                                generated_ui_options.append({
                                    "index": 8.5, 
                                    "message": ts(f"Update Python {colors_class.wrap(f'[v{current_python_version} => v{latest_python_version}]', 226 if is_python_beta else 82)}"), 
                                    "func": continueToUpdatePython, 
                                    "go_to_rbx": True, 
                                    "end_mes": ts("Python has been updated!"),
                                    "clear_console": True
                                })
                                displayNotification(ts("Python Update Available!"), ts(f'Python {latest_python_version} is now available for download! Install the update by opening the main menu, checking for Python updates and then install!'))
                            else: os.remove(generateFileKey("PythonUpdate"))
                    if not (main_config.get("EFlagDisablePythonModuleUpdateChecks") == True):
                        can_be_updated_modules = ["pypresence", "psutil"]
                        if main_os == "Windows": can_be_updated_modules += ["pywin32", "plyer"]
                        elif main_os == "Darwin": can_be_updated_modules += ["pyobjc-core", "pyobjc-framework-Quartz", "pyobjc-framework-Cocoa", "posix-ipc"]
                        for mod_info in generateModsManifest().values():
                            if mod_info.get("mod_script") == True and mod_info.get("enabled") == True and mod_info.get("python_modules"): can_be_updated_modules += [str(module_needed) for module_needed in mod_info.get("python_modules", []) if not module_needed in can_be_updated_modules]
                        def python_module_update_check():
                            updating_python_modules = pip_class.updates(can_be_updated_modules)
                            if updating_python_modules and updating_python_modules["success"] == True:
                                if len(updating_python_modules["packages"]) > 0:
                                    dumped = json.dumps(updating_python_modules["packages"], ensure_ascii=False)
                                    if os.path.exists(generateFileKey("PythonModuleUpdate")):
                                        with open(generateFileKey("PythonModuleUpdate"), "r") as f: ss = f.read()
                                        if ss == dumped: return
                                    with open(generateFileKey("PythonModuleUpdate"), "w", encoding="utf-8") as f: f.write(dumped)
                                    displayNotification(ts("Python Module Updates Available!"), ts(f'{len(updating_python_modules["packages"])} Python module{"" if len(updating_python_modules["packages"]) == 1 else "s"} are now available to be updated! Install the update by opening the main menu, checking for Python Module updates and then install!'))
                                elif os.path.exists(generateFileKey("PythonModuleUpdate")): os.remove(generateFileKey("PythonModuleUpdate"))
                        threading.Thread(target=python_module_update_check, daemon=True).start()
                        if os.path.exists(generateFileKey("PythonModuleUpdate")):
                            with open(generateFileKey("PythonModuleUpdate"), "r") as f: modules_updating = json.load(f)
                            if len(modules_updating) > 0:
                                generated_ui_options.append({
                                    "index": 8.75, 
                                    "message": ts(f"Update Python Modules {colors_class.wrap(f'[+{len(modules_updating)}]', 82)}"), 
                                    "func": continueToUpdatePythonModules, 
                                    "go_to_rbx": True, 
                                    "end_mes": ts("Python Modules has been updated!"),
                                    "clear_console": True
                                })
                            else: os.remove(generateFileKey("PythonModuleUpdate"))
                    if not (main_config.get("EFlagDisableBootstrapChecks") == True):
                        def bootstrap_update_check():
                            get_updates_anyway = True
                            emoji_to_define_update = ""
                            unic = ""
                            version_server = main_config.get("EFlagBootstrapUpdateServer", "https://obx.efaz.dev/Version.json")
                            if version_server == "https://obx.efaz.dev/Version.json": emoji_to_define_update = "✅"; get_updates_anyway = True; unic = "82"
                            elif version_server == "https://obxbeta.efaz.dev/Version.json" or version_server == "https://raw.githubusercontent.com/EfazDev/orangeblox/refs/heads/beta/Version.json": emoji_to_define_update = "⚠️"; get_updates_anyway = True; unic = "226"
                            elif not (main_config.get("EFlagUpdatesAuthorizationKey", "") == ""): emoji_to_define_update = "🔨"; get_updates_anyway = True; unic = "226"
                            else: emoji_to_define_update = "❌"; get_updates_anyway = False; unic = "196"
                            if get_updates_anyway == True:
                                if not (type(version_server) is str and version_server.startswith("https://")): version_server = "https://obx.efaz.dev/Version.json"
                                try: latest_vers_res = requests.get(f"{version_server}", headers={"X-Bootstrap-Version": current_version["version"], "X-Python-Version": platform.python_version(), "X-Authorization-Key": main_config.get("EFlagUpdatesAuthorizationKey", "")})
                                except Exception as e: latest_vers_res = PyKits.InstantRequestJSONResponse(ok=False)
                                if latest_vers_res.ok:
                                    latest_vers = latest_vers_res.json
                                    if current_version.get("version"):
                                        if current_version.get("version", "1.0.0") < latest_vers.get("latest_version", "1.0.0"):
                                            versio_name = colors_class.wrap(ts(f'New Updates Available! [v{current_version.get("version", "1.0.0")} => v{latest_vers.get("latest_version", "1.0.0")}] [{emoji_to_define_update}{" " if main_os == "Darwin" else ""}]'), unic)
                                            if os.path.exists(generateFileKey("OrangeBloxUpdate")):
                                                with open(generateFileKey("OrangeBloxUpdate"), "r", encoding="utf-8") as f: ss = f.read()
                                                if ss == versio_name: return
                                            with open(generateFileKey("OrangeBloxUpdate"), "w", encoding="utf-8") as f: f.write(versio_name)
                                            displayNotification(ts("OrangeBlox Update Available!"), ts(f'OrangeBlox v{latest_vers.get("latest_version", "1.0.0")} is now available for download! Install the update by opening the main menu, checking for updates and then install!'))
                                        else:
                                            if os.path.exists(generateFileKey("OrangeBloxUpdate")): os.remove(generateFileKey("OrangeBloxUpdate"))
                        threading.Thread(target=bootstrap_update_check, daemon=True).start()
                    if os.path.exists(generateFileKey("OrangeBloxUpdate")):
                        with open(generateFileKey("OrangeBloxUpdate"), "r", encoding="utf-8") as f: versio_name = f.read()
                        generated_ui_options.append({
                            "index": 9, 
                            "message": versio_name, 
                            "func": continueToUpdates, 
                            "go_to_rbx": True, 
                            "end_mes": ts("Finished checking for updates!"),
                            "clear_console": True
                        })
                    else:
                        version_server = main_config.get("EFlagBootstrapUpdateServer", "https://obx.efaz.dev/Version.json")
                        if version_server == "https://obx.efaz.dev/Version.json": emoji_to_define_update = "✅"; unic = "82"
                        elif version_server == "https://obxbeta.efaz.dev/Version.json" or version_server == "https://raw.githubusercontent.com/EfazDev/orangeblox/refs/heads/beta/Version.json": emoji_to_define_update = "⚠️"; unic = "226"
                        elif not (main_config.get("EFlagUpdatesAuthorizationKey", "") == ""): emoji_to_define_update = "🔨"; unic = "226"
                        else: emoji_to_define_update = "❌"; unic = "196"
                        generated_ui_options.append({
                            "index": 9, 
                            "message": colors_class.wrap(ts(f"Check for Updates [{emoji_to_define_update}{' ' if main_os == 'Darwin' else ''}]"), unic), 
                            "func": continueToUpdates, 
                            "go_to_rbx": True, 
                            "end_mes": ts("Finished checking for updates!"),
                            "clear_console": True
                        })
                    if handler.getIfRobloxIsOpen():
                        generated_ui_options.append({
                            "index": 10, 
                            "message": ts("End All Roblox Instances"), 
                            "func": continueToEndRobloxInstances, 
                            "go_to_rbx": True, 
                            "end_mes": ts("Roblox Instances have been ended!"),
                            "clear_console": True
                        })
                    if main_config.get("EFlagRobloxStudioEnabled") == True and handler.getIfRobloxIsOpen(studio=True):
                        generated_ui_options.append({
                            "index": 11, 
                            "message": ts("End All Roblox Studio Instances"), 
                            "func": continueToEndRobloxInstances, 
                            "go_to_rbx": True, 
                            "end_mes": ts("Roblox Instances have been ended!"),
                            "clear_console": True,
                            "studio": True
                        })
                    if main_config.get("EFlagRobloxUnfriendCheckEnabled") == True:
                        generated_ui_options.append({
                            "index": 12, 
                            "message": ts(f"Unfriended Friends"), 
                            "func": continueToUnfriendedFriends, 
                            "go_to_rbx": True, 
                            "end_mes": ts("Listed all unfriended friends!"),
                            "clear_console": True
                        })                        
                    generated_ui_options.append({
                        "index": 100, 
                        "message": ts("Credits"), 
                        "func": continueToCredits, 
                        "go_to_rbx": True, 
                        "end_mes": ts("Would you like to go to Roblox?"),
                        "clear_console": True
                    })
                    printWarnMessage("--- Main Menu ---")
                    opt = generateMenuSelection(generated_ui_options, star_option=ts("Exit Bootstrap"))
                    if opt:
                        try:
                            if opt.get("clear_console") == True: startMessage()
                            if opt.get("studio") == True: re = opt["func"](studio=True)
                            else: re = opt["func"]()
                            if opt.get("go_to_rbx") == True: 
                                if type(re) is str: handleOptionSelect(re)
                                else: handleOptionSelect(opt.get("end_mes"))
                        except BaseException as e:
                            if type(e) is SystemExit: raise e
                            printErrorMessage("Uh oh! A Python exception that causes the script to end has occurred!")
                            printErrorMessage(f"Exception: \n{trace()}")
                            printErrorMessage(f"Location Code: 1")
                            handleOptionSelect(ts("An error occurred!"))
                    else: sys.exit(0)
                    getSettings()
                elif len(given_args) > 1: # URL Scheme Handler
                    url = given_args[1]
                    if ("efaz-bootstrap" in url or url.startswith("obx-launch") or ("orangeblox" in url and not url.endswith(".obx"))) and not (url.startswith("obx-launch-studio") or url.startswith("obx-launch-player")) and not os.path.isfile(url):
                        try:
                            if "obx-launch" in url: given_args[1] = given_args[1].replace("obx-launch ", "").replace("obx-launch", "")
                            if "continue" in url: continueToRoblox()
                            elif "run-studio" in url: continueToRoblox(studio=True)
                            elif "new" in url: continueToRoblox()
                            elif "reconnect-studio" in url: connectExistingRobloxWindow(studio=True)
                            elif "reconnect" in url: connectExistingRobloxWindow()
                            elif "python-updates" in url: 
                                continueToUpdatePython()
                                if not ("?quick-action=true" in url): handleOptionSelect()
                                else: handleOptionSelect(isRedirectedFromApp=True)
                            elif "python-module-updates" in url: 
                                continueToUpdatePythonModules()
                                if not ("?quick-action=true" in url): handleOptionSelect()
                                else: handleOptionSelect(isRedirectedFromApp=True)
                            elif "fflag-install" in url:
                                continueToFFlagInstaller()
                                if not ("?quick-action=true" in url): handleOptionSelect()
                                else: handleOptionSelect(isRedirectedFromApp=True)
                            elif "settings" in url:
                                continueToSettings()
                                if not ("?quick-action=true" in url): handleOptionSelect()
                                else: handleOptionSelect(isRedirectedFromApp=True)
                            elif "sync-to-install" in url:
                                syncToFFlagConfiguration()
                                if not ("?quick-action=true" in url): handleOptionSelect()
                                else: handleOptionSelect(isRedirectedFromApp=True)
                            elif "sync-from-install" in url:
                                syncFromFFlagConfiguration()
                                if not ("?quick-action=true" in url): handleOptionSelect()
                                else: handleOptionSelect(isRedirectedFromApp=True)
                            elif "end-roblox-studio" in url:
                                continueToEndRobloxInstances(studio=True)
                                if not ("?quick-action=true" in url): handleOptionSelect()
                                else: handleOptionSelect(isRedirectedFromApp=True)
                            elif "end-roblox" in url:
                                continueToEndRobloxInstances()
                                if not ("?quick-action=true" in url): handleOptionSelect()
                                else: handleOptionSelect(isRedirectedFromApp=True)
                            elif "reinstall-roblox" in url:
                                continueToInstallRobloxOptions(reinstall=True)
                                if not ("?quick-action=true" in url): handleOptionSelect()
                                else: handleOptionSelect(isRedirectedFromApp=True)
                            elif "roblox-installer-options" in url:
                                continueToInstallRobloxOptions()
                                if not ("?quick-action=true" in url): handleOptionSelect()
                                else:  handleOptionSelect(isRedirectedFromApp=True)
                            elif ("credits" in url) or ("about" in url):
                                continueToCredits()
                                if not ("?quick-action=true" in url): handleOptionSelect()
                                else: handleOptionSelect(isRedirectedFromApp=True)
                            elif "mods" in url:
                                continueToModsManager()
                                if not ("?quick-action=true" in url): handleOptionSelect()
                                else: handleOptionSelect(isRedirectedFromApp=True)
                            elif "temporary-storage" in url or "clear-logs" in url:
                                continueToClearTemporaryStorage()
                                if not ("?quick-action=true" in url): handleOptionSelect()
                                else: handleOptionSelect(isRedirectedFromApp=True)
                            elif ("shortcuts/" in url): continueToLinkShortcuts(url)
                            else:
                                printWarnMessage("--- Unknown URL ---")
                                printMainMessage("There was an issue trying to parse your URL scheme. Please select an option below to continue:")
                                printDebugMessage(f"URL Scheme Requested: {url}")
                                printDebugMessage(f"Arguments Received: {given_args}")
                                printMainMessage("[1] = Return to Main Menu")
                                printMainMessage("[2] = Continue to Roblox")
                                printMainMessage("[*] = End Process")
                                res = input("> ")
                                if res == "1":
                                    given_args = ["Main.py"]
                                    main_menu()
                                elif res == "2":
                                    given_args = ["orangeblox://continue"]
                                    continueToRoblox()
                                else: sys.exit(0)
                        except BaseException as e:
                            if type(e) is SystemExit: raise e
                            printErrorMessage("Uh oh! A Python exception that causes the script to end has occurred!")
                            printErrorMessage(f"Exception: \n{trace()}")
                            printErrorMessage(f"Location Code: 2")
                            if not ("?quick-action=true" in url): handleOptionSelect()
                            else: handleOptionSelect(isRedirectedFromApp=True)
                    elif "roblox-studio" in url or url.startswith("obx-launch-studio"):
                        printWarnMessage("--- Redirecting to Roblox Studio! ---")
                        printMainMessage("Successfully loaded Roblox Studio URL Scheme! Continuing to Roblox Studio..")
                        run_studio = True
                        if "obx-launch-studio" in url: given_args[1] = given_args[1].replace("obx-launch-studio ", "").replace("obx-launch-studio", "")
                    elif "roblox" in url or url.startswith("obx-launch-player"):
                        printWarnMessage("--- Redirecting to Roblox! ---")
                        if main_config.get("EFlagEnableDuplicationOfClients") == True: printMainMessage("Successfully loaded Roblox URL Scheme! Continuing to Roblox [Multi-Instance]..")
                        else: printMainMessage("Successfully loaded Roblox URL Scheme! Continuing to Roblox..")
                        if main_config.get("EFlagEnableSkipModificationMode") == True: skip_modification_mode = True
                        if "obx-launch-player" in url: given_args[1] = given_args[1].replace("obx-launch-player ", "").replace("obx-launch-player", "")
                    elif os.path.isfile(url):
                        if url.endswith(".rbxl") or url.endswith(".rbxlx"):
                            printWarnMessage("--- Redirecting to Roblox Studio! ---")
                            printMainMessage("Successfully loaded Roblox URL Scheme! Continuing to Roblox Studio..")
                            run_studio = True
                        elif url.endswith(".obx"):
                            if os.path.exists(url):
                                try:
                                    printWarnMessage("--- OrangeBlox Backup Assistant ---")
                                    printMainMessage("Are you sure you want to restore your OrangeBlox files using the following OrangeBlox file?")
                                    printMainMessage(f"File: {url}")
                                    printErrorMessage("This operation is dangerous to use if not used carefully and will overwrite your Mods and Configuration.")
                                    printErrorMessage("If someone that you have recently met sent you this file, do not use!!")
                                    printErrorMessage("Please backup your Fast Flag Configurations and Mods as this may break before continuing!")
                                    PyKits.TimerBar(30, "Are you sure you want to continue with this file? (y/n)", False).start()
                                    d = input("> ")
                                    if isYes(d) == True:
                                        backup_path = os.path.join(cur_path, "Backup")
                                        backup_file = url
                                        try:
                                            printMainMessage("Unwrapping OrangeBlox file..")
                                            makedirs(backup_path)
                                            zip_extract = pip_class.unzipFile(backup_file, backup_path, ["FastFlagConfiguration.json", "Cursors", "Mods", "RobloxBrand"])
                                            if zip_extract.returncode == 0:
                                                printMainMessage("Validating Backup Metadata..")
                                                back_metadata = {
                                                    "installer_version": "0.0.0",
                                                    "bootstrap_version": "0.0.0",
                                                    "script_hash": "",
                                                }
                                                if os.path.exists(os.path.join(backup_path, "Metadata.json")):
                                                    with open(os.path.join(backup_path, "Metadata.json"), "r", encoding="utf-8") as f: back_metadata = json.load(f)
                                                if back_metadata.get("bootstrap_version") == "0.0.0":
                                                    printWarnMessage("--- Attention Needed! ---")
                                                    printMainMessage("This backup is created in a version before OrangeBlox v2.0.1. Are you sure you want to continue with this backup? (y/n)")
                                                    a = input("> ")
                                                    if isYes(a) == False: sys.exit(0); return
                                                elif back_metadata.get("bootstrap_version") > current_version["version"]:
                                                    printWarnMessage("--- Attention Needed! ---")
                                                    printMainMessage(f"This backup is created in a version (v{back_metadata.get('bootstrap_version')}) after OrangeBlox v{current_version['version']}. Are you sure you want to continue with this backup? (y/n)")
                                                    a = input("> ")
                                                    if isYes(a) == False: sys.exit(0); return
                                                elif back_metadata.get("bootstrap_version") < current_version["version"]:
                                                    printWarnMessage("--- Attention Needed! ---")
                                                    printMainMessage(f"This backup is created in a version (v{back_metadata.get('bootstrap_version')}) before OrangeBlox v{current_version['version']}. Are you sure you want to continue with this backup? (y/n)")
                                                    a = input("> ")
                                                    if isYes(a) == False: sys.exit(0); return
                                                printMainMessage("Copying Configuration.json..")
                                                if os.path.exists(os.path.join(backup_path, "FastFlagConfiguration.json")):
                                                    with open(os.path.join(backup_path, "FastFlagConfiguration.json"), "r", encoding="utf-8") as f: main_config = json.load(f)
                                                else:
                                                    with open(os.path.join(backup_path, "Configuration.json"), "rb") as f: obfuscated_json = f.read()
                                                    try: obfuscated_json = json.loads(obfuscated_json)
                                                    except Exception as e: obfuscated_json = json.loads(zlib.decompress(obfuscated_json).decode("utf-8"))
                                                    main_config = obfuscated_json
                                                saveSettings()
                                                printMainMessage("Copying AvatarEditorMaps..")
                                                pip_class.copyTreeWithMetadata(os.path.join(backup_path, "AvatarEditorMaps"), os.path.join(mods_folder, "AvatarEditorMaps"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                                printMainMessage("Copying Cursors..")
                                                pip_class.copyTreeWithMetadata(os.path.join(backup_path, "Cursors"), os.path.join(mods_folder, "Cursors"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                                if os.path.exists(os.path.join(backup_path, "PlayerSounds")):
                                                    printMainMessage("Copying PlayerSounds..")
                                                    pip_class.copyTreeWithMetadata(os.path.join(backup_path, "PlayerSounds"), os.path.join(mods_folder, "PlayerSounds"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                                else:
                                                    printMainMessage("Copying DeathSounds..")
                                                    pip_class.copyTreeWithMetadata(os.path.join(backup_path, "DeathSounds"), os.path.join(mods_folder, "DeathSounds"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                                    if os.path.exists(os.path.join(cur_path, "DeathSounds")):
                                                        for i in os.listdir(os.path.join(cur_path, "DeathSounds")):
                                                            if os.path.isfile(os.path.join(cur_path, "DeathSounds", i)):
                                                                possible_name = i.split(".")
                                                                if len(possible_name) > 1: possible_name = possible_name[0]
                                                                else: possible_name = i
                                                                makedirs(os.path.join(backup_path, "PlayerSounds", possible_name))
                                                                shutil.copy(os.path.join(cur_path, "DeathSounds", i), os.path.join(mods_folder, "PlayerSounds", possible_name, "ouch.ogg"), follow_symlinks=False)
                                                        shutil.rmtree(os.path.join(cur_path, "DeathSounds"), ignore_errors=True)
                                                printMainMessage("Copying Mods..")
                                                pip_class.copyTreeWithMetadata(os.path.join(backup_path, "Mods"), os.path.join(mods_folder, "Mods"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                                printMainMessage("Copying RobloxBrand..")
                                                pip_class.copyTreeWithMetadata(os.path.join(backup_path, "RobloxBrand"), os.path.join(mods_folder, "RobloxBrand"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                                printMainMessage("Copying RobloxStudioBrand..")
                                                pip_class.copyTreeWithMetadata(os.path.join(backup_path, "RobloxStudioBrand"), os.path.join(mods_folder, "RobloxStudioBrand"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                                printMainMessage("Finished transferring! Deleting backup data..")
                                                if os.path.exists(backup_path): shutil.rmtree(backup_path, ignore_errors=True)
                                                printSuccessMessage("Successfully restored OrangeBlox data! Would you to restart the app? (y/n)")
                                                a = input("> ")
                                                if isYes(a) == True: pip_class.restartScript("Main.py", sys.argv)
                                                else: sys.exit(0)
                                            else: raise Exception("There was an issue trying to open the OrangeBlox file! Make sure it's readable before trying again!")
                                        except Exception as e:
                                            printErrorMessage("There was an error trying to restore your OrangeBlox files!")
                                            printErrorMessage(f"Python Exception: \n{trace()}")
                                            input("> ")
                                            sys.exit(0)
                                            return
                                    else: sys.exit(0)
                                except Exception as e:
                                    printWarnMessage("--- OrangeBlox Backup Assistant ---")
                                    printErrorMessage(f"Something went wrong: \n{trace()}")
                                    input("> ")
                                    sys.exit(0)
                            else:
                                printWarnMessage("--- OrangeBlox Backup Assistant ---")
                                printErrorMessage(f"Unable to read OrangeBlox file due to the file not existing or unable to be accessed.")
                                input("> ")
                                sys.exit(0)
                        else:
                            printWarnMessage("--- Unknown file ---")
                            printErrorMessage(f"Unable to read OrangeBlox file due to the file handler not added.")
                            input("> ")
                            sys.exit(0)
                    else:
                        printWarnMessage("--- Unknown URL ---")
                        printMainMessage("There was an issue trying to parse your URL scheme. Please select an option below to continue:")
                        printDebugMessage(f"URL Scheme Requested: {url}")
                        printDebugMessage(f"Arguments Received: {given_args}")
                        printMainMessage("[1] = Return to Main Menu")
                        printMainMessage("[2] = Continue to Roblox")
                        printMainMessage("[*] = End Process")
                        res = input("> ")
                        if res == "1":
                            given_args = []
                            main_menu()
                        elif res == "2":
                            given_args = ["orangeblox://continue"]
                            continueToRoblox()
                        else: sys.exit(0)
        def handleOptionSelect(mes=None, isRedirectedFromApp=False): # Handle Continue to Roblox
            new_menu_mode = False
            if mes == None:
                mes = ts("Option finished! Would you like to return to the main menu or would you like to continue to Roblox?")
                new_menu_mode = True
            else:
                if mes == "": mes = ts(f"Would you like to return to the main menu or would you like to continue to Roblox?")
                else: mes = ts(f"{mes} Would you like to return to the main menu or would you like to continue to Roblox?")
                new_menu_mode = True
            if new_menu_mode == True:
                if not (main_config.get("EFlagReturnToMainMenuInstant") == True):
                    if isRedirectedFromApp == False:
                        printWarnMessage(mes)
                        printMainMessage("[1] = Return to Main Menu")
                        printMainMessage("[2] = Exit Bootstrap")
                        if main_config.get("EFlagRobloxStudioEnabled") == True: printMainMessage("[3] = Continue to Roblox Studio")
                        printMainMessage("[*] = Continue to Roblox")
                        a = input("> ")
                        if a == "1": main_menu()
                        elif a == "2": sys.exit(0)
                        elif a == "3" and main_config.get("EFlagRobloxStudioEnabled") == True: continueToRoblox(studio=True)
                    else:
                        printWarnMessage(mes)
                        printMainMessage("[1] = Continue to Roblox")
                        if main_config.get("EFlagRobloxStudioEnabled") == True: printMainMessage("[2] = Continue to Roblox Studio")
                        printMainMessage("[*] = Exit Bootstrap")
                        a = input("> ")
                        if a == "1": continueToRoblox()
                        elif a == "2" and main_config.get("EFlagRobloxStudioEnabled") == True: continueToRoblox(studio=True)
                        else: sys.exit(0)
                elif isRedirectedFromApp == False: main_menu()
                else: global given_args; given_args = ["Main.py"]; main_menu()
            else:
                printWarnMessage(mes)
                a = input("> ")
                if isYes(a) == False: sys.exit(0)
        main_menu()
    except (KeyboardInterrupt, Exception) as e:
        printErrorMessage("Uh oh! A Python exception that causes the script to end has occurred!")
        printErrorMessage(f"Exception: \n{trace()}")
        printErrorMessage(f"Location Code: 0")
        input("> ")
        sys.exit(0 if main_os == "Darwin" else 1)

    # Run Roblox
    try:
        # Check for Permissions
        if run_studio == True and not main_config.get("EFlagRobloxStudioEnabled") == True:
            printWarnMessage("--- Roblox Studio Permission ---")
            printMainMessage("Roblox Studio with OrangeBlox is currently disabled right now! Would you like to enable it or would you want to exit? (y/n)")
            if isYes(input("> ")) == True:
                main_config["EFlagRobloxStudioEnabled"] = True
                saveSettings()
            else: sys.exit(0)
        if run_studio == True:
            # Validate Roblox Studio
            def validateInstallation():
                if main_os == "Windows":
                    target_install_name = main_config.get("EFlagBootstrapRobloxStudioInstallFolderName", "com.roblox.robloxstudio")
                    if not os.path.exists(os.path.join(versions_folder, target_install_name)): return False
                    for i, v in handler.roblox_studio_bundle_files.items(): 
                        if not (v == "/" or v == "/Qml") and not os.path.exists(f"{os.path.join(versions_folder, target_install_name)}{v}"): return False
                elif main_os == "Darwin":
                    if not os.path.exists(RFFI.macOS_studioDir): return False
                    roblox_bundle_folders = ["/content", "/ssl", "/PlatformContent", "/StudioContent", "/ExtraContent", "/shaders", "/RibbonConfig", "/StudioFonts", "/BuiltInStandalonePlugins", "/BuiltInPlugins", "/ApplicationConfig"]
                    for i in roblox_bundle_folders: 
                        if not os.path.exists(f"{os.path.join(RFFI.macOS_studioDir, 'Contents', 'Resources')}{i}"): return False
                return True
            studio_can_be_used = validateInstallation()
            # Install Roblox Studio
            if not (studio_can_be_used == True):
                printWarnMessage("--- Installing Roblox Studio to Bootstrap ---")
                printMainMessage("Please wait while we install Roblox Studio into OrangeBlox!")
                submit_status.start()
                res = handler.installRoblox(studio=True, debug=main_config.get("EFlagEnableDebugMode"))
                submit_status.end()
                if res and res["success"] == False:
                    printErrorMessage("There is an issue while trying to install Roblox Studio. Please try again by restarting this app!")
                    input("> ")
                    sys.exit(0)
                if main_os == "Windows":
                    pip_class.copyTreeWithMetadata(os.path.join(cur_path, "_internal"), os.path.join(versions_folder, main_config.get("EFlagBootstrapRobloxStudioInstallFolderName", "com.roblox.robloxstudio"), "_internal"), dirs_exist_ok=True, ignore_if_not_exist=True)
                    shutil.copy(os.path.join(cur_path, "OrangeBlox.exe"), os.path.join(versions_folder, main_config.get("EFlagBootstrapRobloxStudioInstallFolderName", "com.roblox.robloxstudio"), "RobloxStudioInstaller.exe"))
                    with open(os.path.join(versions_folder, main_config.get("EFlagBootstrapRobloxStudioInstallFolderName", "com.roblox.robloxstudio"), "RobloxStudioBetaPlayRobloxRestart.txt"), "w", encoding="utf-8") as f: f.write(cur_path)
                elif main_os == "Darwin":
                    if os.path.exists(os.path.join(macos_app_path, "../", "Play Roblox.app")):
                        pip_class.copyTreeWithMetadata(os.path.join(macos_app_path, "../", "Play Roblox.app"), os.path.join(RFFI.macOS_dir, "Contents", "MacOS", "RobloxPlayerInstaller.app"), dirs_exist_ok=True)
                        shutil.copy(os.path.join(macos_app_path, "../", "Play Roblox.app", "Contents", "MacOS", "OrangePlayRoblox"), os.path.join(RFFI.macOS_dir, "Contents", "MacOS", "RobloxPlayerInstaller.app", "Contents", "MacOS", "RobloxPlayerInstaller"))
                        with open(os.path.join(RFFI.macOS_dir, "Contents", "MacOS", "RobloxPlayerInstaller.app", "Contents", "Resources", "RobloxPlayerBetaPlayRobloxRestart"), "w", encoding="utf-8") as f: f.write(cur_path)
                        for i in generateCodesignCommand(os.path.join(RFFI.macOS_dir, "Contents", "MacOS", "RobloxPlayerInstaller.app"), main_config.get("EFlagRobloxCodesigningName", "-")): 
                            if i[0] == "/usr/bin/xattr": subprocess.run(i, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                            else: subprocess.Popen(i, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    if os.path.exists(os.path.join(macos_app_path, "../", "Run Studio.app")):
                        pip_class.copyTreeWithMetadata(os.path.join(macos_app_path, "../", "Run Studio.app"), os.path.join(RFFI.macOS_studioDir, "Contents", "MacOS", "RobloxStudioInstaller.app"), dirs_exist_ok=True)
                        shutil.copy(os.path.join(macos_app_path, "../", "Run Studio.app", "Contents", "MacOS", "OrangeRunStudio"), os.path.join(RFFI.macOS_studioDir, "Contents", "MacOS", "RobloxStudioInstaller.app", "Contents", "MacOS", "RobloxStudioInstaller"))
                        with open(os.path.join(RFFI.macOS_studioDir, "Contents", "MacOS", "RobloxStudioInstaller.app", "Contents", "Resources", "RobloxStudioBetaPlayRobloxRestart"), "w", encoding="utf-8") as f: f.write(cur_path)
                        for i in generateCodesignCommand(os.path.join(RFFI.macOS_studioDir, "Contents", "MacOS", "RobloxStudioInstaller.app"), main_config.get("EFlagRobloxCodesigningName", "-")): 
                            if i[0] == "/usr/bin/xattr": subprocess.run(i, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                            else: subprocess.Popen(i, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            # Check for Updates
            if (not (connect_instead == True)) and (not (main_config.get("EFlagDisableRobloxUpdateChecks") == True)):
                waitForInternet()
                printWarnMessage("--- Checking for Roblox Studio Updates ---")
                current_roblox_version = handler.getCurrentClientVersion(studio=True)
                if current_roblox_version["success"] == True:
                    url_channel = None
                    try:
                        if len(given_args) > 1:
                            if main_os == "Darwin":
                                url_str = unquote(given_args[1])
                                if url_str: url = unquote(url_str)
                                else: url = ""
                            elif main_os == "Windows": url = given_args[1]
                            if "-channel " in url:
                                s = url.split(" ")
                                url_channel = s[s.index("-channel") + 1]
                                given_args = ["Main.py", "orangeblox://run-studio"]
                            elif "-RobloxChannel " in url:
                                s = url.split(" ")
                                url_channel = s[s.index("-RobloxChannel") + 1]
                                given_args = ["Main.py", "orangeblox://run-studio"]
                            elif url.startswith("roblox-studio"):
                                url_data = handler.parseRobloxLauncherURL(url=url)
                                if url_data and url_data.get("channel"): url_channel = url_data.get("channel")
                        if main_config.get("EFlagRobloxSecurityCookieUsage") == True and (not url_channel or url_channel == "LIVE"):
                            requesting_channel = handler.getUserChannel(studio=run_studio, debug=(main_config.get("EFlagEnableDebugMode") == True))
                            if requesting_channel.get("success") == True and requesting_channel.get("channel_name") != "LIVE":
                                url_channel = requesting_channel.get("channel_name")
                                if requesting_channel.get("token"): main_config["EFlagRobloxChannelUpdateToken"] = requesting_channel.get("token")
                        elif not (main_config.get("EFlagRobloxSecurityCookieUsage") == True) and main_config.get("EFlagRobloxChannelUpdateToken"):
                            main_config.pop("EFlagRobloxChannelUpdateToken")
                        if url_channel:
                            printDebugMessage(f"Setting Channel Based on URL: {url_channel}")
                            if url_channel == "production" or url_channel == "LIVE": url_channel = ""; current_roblox_version["channel"] = "LIVE"
                            else: current_roblox_version["channel"] = url_channel
                            if main_os == "Darwin":
                                res = plist_class.writePListFile(os.path.join(user_folder, "Library", "Preferences", "com.roblox.RobloxStudioChannel.plist"), {"www.roblox.com": url_channel}, binary=True, ns_mode=True)
                                printDebugMessage(f"Channel Set Result: {res}")
                            elif main_os == "Windows":
                                try: registry_key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, r"Software\ROBLOX Corporation\Environments\RobloxStudio\Channel", 0, win32con.KEY_SET_VALUE)
                                except Exception: registry_key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, r"Software\ROBLOX Corporation\Environments\RobloxStudio\Channel")
                                win32api.RegSetValueEx(registry_key, "www.roblox.com", 0, win32con.REG_SZ, url_channel)
                                win32api.RegCloseKey(registry_key)
                    except Exception as e: printDebugMessage(f"Unable to find channel from URL. Exception: \n{trace()}")
                    latest_roblox_version = handler.getLatestClientVersion(studio=True, debug=(main_config.get("EFlagEnableDebugMode") == True), channel=url_channel if url_channel else main_config.get("EFlagRobloxStudioClientChannel", current_roblox_version.get("channel", "LIVE")), token=main_config.get("EFlagRobloxChannelUpdateToken"))
                    if latest_roblox_version["success"] == True:
                        download_channel = latest_roblox_version["attempted_channel"]
                        if current_roblox_version["client_version"] == latest_roblox_version["client_version"]: printMainMessage("Running latest version of Roblox Studio!")
                        else:
                            continue_to_update = True
                            printSuccessMessage(f"A new version of Roblox Studio is available! Versions: {current_roblox_version['version']} => {latest_roblox_version['hash']}")
                            printWarnMessage("--- Installing Latest Roblox Studio Version ---")
                            if continue_to_update == True:
                                printMainMessage("Please wait while we install a newer version of Roblox Studio into OrangeBlox!")
                                submit_status.start()
                                res = handler.installRoblox(studio=True, debug=(main_config.get("EFlagEnableDebugMode") == True), copyRobloxInstallerPath=(main_os == "Darwin" and os.path.join(cur_path, "RobloxStudioInstaller.app") or os.path.join(cur_path, "RobloxStudioInstaller.exe")), downloadInstaller=True, downloadChannel=download_channel, downloadToken=main_config.get("EFlagRobloxChannelUpdateToken"))
                                submit_status.end()
                                if res and res["success"] == False:
                                    printErrorMessage("There is an issue while trying to install Roblox Studio. Please try again by restarting this app!")
                                    input("> ")
                                    sys.exit(0)
                                if main_os == "Darwin":
                                    while not os.path.exists(RFFI.macOS_studioDir): time.sleep(0.1)
                                new_latest_roblox_version = handler.getCurrentClientVersion(studio=True)
                                printSuccessMessage(f"Successfully updated Roblox Studio to {new_latest_roblox_version.get('version')}!")
                                installed_update = True
                                skip_modification_mode = False
                            else: printErrorMessage("The download for this update is unavailable at this time! Try again later!")
                        if not (download_channel == (url_channel if url_channel else main_config.get("EFlagRobloxStudioClientChannel", current_roblox_version.get("channel", "LIVE")))):
                            printDebugMessage(f"Setting Channel Based on Channel Difference: {download_channel}")
                            if download_channel == "production" or download_channel == "LIVE": download_channel = ""
                            if main_os == "Darwin":
                                res = plist_class.writePListFile(os.path.join(user_folder, "Library", "Preferences", "com.roblox.RobloxStudioChannel.plist"), {"www.roblox.com": download_channel}, binary=True, ns_mode=True)
                                printDebugMessage(f"Channel Set Result: {res}")
                            elif main_os == "Windows":
                                try: registry_key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, r"Software\ROBLOX Corporation\Environments\RobloxStudio\Channel", 0, win32con.KEY_SET_VALUE)
                                except Exception: registry_key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, r"Software\ROBLOX Corporation\Environments\RobloxStudio\Channel")
                                win32api.RegSetValueEx(registry_key, "www.roblox.com", 0, win32con.REG_SZ, download_channel)
                                win32api.RegCloseKey(registry_key)
                    else:
                        printDebugMessage(latest_roblox_version)
                        printErrorMessage("There was an issue while checking for updates.")
                else: printErrorMessage("There was an issue while checking for updates.")
        else:
            # Validate Roblox Player
            def validateInstallation():
                if main_os == "Windows":
                    target_install_name = main_config.get("EFlagBootstrapRobloxInstallFolderName", "com.roblox.robloxplayer")
                    if not os.path.exists(os.path.join(versions_folder, target_install_name)): return False
                    for i, v in handler.roblox_bundle_files.items(): 
                        if not (v == "/") and not os.path.exists(f"{os.path.join(versions_folder, target_install_name)}{v}"): return False
                elif main_os == "Darwin":
                    if not os.path.exists(RFFI.macOS_dir): return False
                    roblox_bundle_folders = ["/content", "/ssl", "/PlatformContent", "/ExtraContent", "/shaders"]
                    for i in roblox_bundle_folders: 
                        if not os.path.exists(f"{os.path.join(RFFI.macOS_dir, 'Contents', 'Resources')}{i}"): return False
                return True
            player_can_be_used = validateInstallation()
            # Check for Updates
            if (not (main_config.get("EFlagDisableRobloxUpdateChecks") == True)):
                waitForInternet()
                printWarnMessage("--- Checking for Roblox Updates ---")
                current_roblox_version = handler.getCurrentClientVersion()
                if (main_config.get("EFlagFreshCopyRoblox") == True and not skip_modification_mode == True) or player_can_be_used == False:
                    url_channel = None
                    try:
                        if len(given_args) > 1:
                            if main_os == "Darwin":
                                url_str = unquote(given_args[1])
                                if url_str: url = unquote(url_str)
                                else: url = ""
                            elif main_os == "Windows": url = given_args[1]
                            if "-channel " in url:
                                s = url.split(" ")
                                url_channel = s[s.index("-channel") + 1]
                                given_args = ["Main.py", "orangeblox://continue"]
                            elif "-RobloxChannel " in url:
                                s = url.split(" ")
                                url_channel = s[s.index("-RobloxChannel") + 1]
                                given_args = ["Main.py", "orangeblox://continue"]
                            elif url.startswith("roblox-player:"):
                                url_data = handler.parseRobloxLauncherURL(url=url)
                                if url_data and url_data.get("channel"): url_channel = url_data.get("channel")
                        if main_config.get("EFlagRobloxSecurityCookieUsage") == True and (not url_channel or url_channel == "LIVE"):
                            requesting_channel = handler.getUserChannel(studio=run_studio, debug=(main_config.get("EFlagEnableDebugMode") == True))
                            if requesting_channel.get("success") == True and requesting_channel.get("channel_name") != "LIVE":
                                url_channel = requesting_channel.get("channel_name")
                                if requesting_channel.get("token"): main_config["EFlagRobloxChannelUpdateToken"] = requesting_channel.get("token")
                        elif not (main_config.get("EFlagRobloxSecurityCookieUsage") == True) and main_config.get("EFlagRobloxChannelUpdateToken"):
                            main_config.pop("EFlagRobloxChannelUpdateToken")
                        if url_channel:
                            printDebugMessage(f"Setting Channel Based on URL: {url_channel}")
                            if url_channel == "production" or url_channel == "LIVE": url_channel = ""; current_roblox_version["channel"] = "LIVE"
                            else: current_roblox_version["channel"] = url_channel
                            if main_os == "Darwin":
                                res = plist_class.writePListFile(os.path.join(user_folder, "Library", "Preferences", "com.roblox.RobloxPlayerChannel.plist"), {"www.roblox.com": url_channel}, binary=True, ns_mode=True)
                                printDebugMessage(f"Channel Set Result: {res}")
                            elif main_os == "Windows":
                                try: registry_key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, r"Software\ROBLOX Corporation\Environments\RobloxPlayer\Channel", 0, win32con.KEY_SET_VALUE)
                                except Exception: registry_key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, r"Software\ROBLOX Corporation\Environments\RobloxPlayer\Channel")
                                win32api.RegSetValueEx(registry_key, "www.roblox.com", 0, win32con.REG_SZ, url_channel)
                                win32api.RegCloseKey(registry_key)
                    except Exception as e: printDebugMessage(f"Unable to find channel from URL. Exception: \n{trace()}")
                    latest_roblox_version = handler.getLatestClientVersion(debug=(main_config.get("EFlagEnableDebugMode") == True), channel=url_channel if url_channel else main_config.get("EFlagRobloxClientChannel", current_roblox_version.get("channel", "LIVE")), token=main_config.get("EFlagRobloxChannelUpdateToken"))
                    if latest_roblox_version["success"] == True:
                        download_channel = latest_roblox_version["attempted_channel"]
                        if main_os == "Windows":
                            if (multi_instance_enabled == True or main_config.get("EFlagEnableDuplicationOfClients") == True) and handler.getIfRobloxIsOpen(): printMainMessage("Skipping Roblox Reinstall due to Multi-Instancing enabled.")
                            else:
                                printMainMessage(f"Fresh copy was enabled! Therefore, starting Roblox install!")
                                printWarnMessage("--- Installing Latest Roblox Version ---")
                                submit_status.start()
                                res = handler.installRoblox(forceQuit=True, debug=(main_config.get("EFlagEnableDebugMode") == True), copyRobloxInstallerPath=(main_os == "Darwin" and os.path.join(cur_path, "RobloxPlayerInstaller.app") or os.path.join(cur_path, "RobloxPlayerInstaller.exe")), downloadInstaller=True, downloadChannel=download_channel, downloadToken=main_config.get("EFlagRobloxChannelUpdateToken"), verifyInstall=not (main_config.get("EFlagVerifyRobloxHashAfterInstall")==False))
                                submit_status.end()
                                if res and res["success"] == False:
                                    printErrorMessage("There is an issue while trying to install Roblox. Please try again by restarting this app!")
                                    input("> ")
                                    sys.exit(0)
                                installed_update = True
                                time.sleep(3)
                        else:
                            printMainMessage(f"Fresh copy was enabled! Therefore, starting Roblox install!")
                            printWarnMessage("--- Installing Latest Roblox Version ---")
                            submit_status.start()
                            res = handler.installRoblox(forceQuit=False, debug=(main_config.get("EFlagEnableDebugMode") == True), copyRobloxInstallerPath=(main_os == "Darwin" and os.path.join(cur_path, "RobloxPlayerInstaller.app") or os.path.join(cur_path, "RobloxPlayerInstaller.exe")), downloadInstaller=True, downloadChannel=download_channel, downloadToken=main_config.get("EFlagRobloxChannelUpdateToken"), verifyInstall=not (main_config.get("EFlagVerifyRobloxHashAfterInstall")==False))
                            submit_status.end()
                            if res and res["success"] == False:
                                printErrorMessage("There is an issue while trying to install Roblox. Please try again by restarting this app!")
                                input("> ")
                                sys.exit(0)
                            installed_update = True
                            time.sleep(3)
                    else: printErrorMessage("There was an issue while checking for updates.")
                elif current_roblox_version["success"] == True:
                    url_channel = None
                    try:
                        if len(given_args) > 1:
                            if main_os == "Darwin":
                                url_str = unquote(given_args[1])
                                if url_str: url = unquote(url_str)
                                else: url = ""
                            elif main_os == "Windows": url = given_args[1]
                            if "-channel " in url:
                                s = url.split(" ")
                                url_channel = s[s.index("-channel") + 1]
                                given_args = ["Main.py", "orangeblox://continue"]
                            elif "-RobloxChannel " in url:
                                s = url.split(" ")
                                url_channel = s[s.index("-RobloxChannel") + 1]
                                given_args = ["Main.py", "orangeblox://continue"]
                            elif url.startswith("roblox-player:"):
                                url_data = handler.parseRobloxLauncherURL(url=url)
                                if url_data and url_data.get("channel"): url_channel = url_data.get("channel")
                        if main_config.get("EFlagRobloxSecurityCookieUsage") == True and (not url_channel or url_channel == "LIVE"):
                            requesting_channel = handler.getUserChannel(studio=run_studio, debug=(main_config.get("EFlagEnableDebugMode") == True))
                            if requesting_channel.get("success") == True and requesting_channel.get("channel_name") != "LIVE":
                                url_channel = requesting_channel.get("channel_name")
                                if requesting_channel.get("token"): main_config["EFlagRobloxChannelUpdateToken"] = requesting_channel.get("token")
                        elif not (main_config.get("EFlagRobloxSecurityCookieUsage") == True) and main_config.get("EFlagRobloxChannelUpdateToken"):
                            main_config.pop("EFlagRobloxChannelUpdateToken")
                        if url_channel:
                            printDebugMessage(f"Setting Channel Based on URL: {url_channel}")
                            if url_channel == "production" or url_channel == "LIVE": url_channel = ""; current_roblox_version["channel"] = "LIVE"
                            else: current_roblox_version["channel"] = url_channel
                            if main_os == "Darwin":
                                res = plist_class.writePListFile(os.path.join(user_folder, "Library", "Preferences", "com.roblox.RobloxPlayerChannel.plist"), {"www.roblox.com": url_channel}, binary=True, ns_mode=True)
                                printDebugMessage(f"Channel Set Result: {res}")
                            elif main_os == "Windows":
                                try: registry_key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, r"Software\ROBLOX Corporation\Environments\RobloxPlayer\Channel", 0, win32con.KEY_SET_VALUE)
                                except Exception: registry_key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, r"Software\ROBLOX Corporation\Environments\RobloxPlayer\Channel")
                                win32api.RegSetValueEx(registry_key, "www.roblox.com", 0, win32con.REG_SZ, url_channel)
                                win32api.RegCloseKey(registry_key)
                    except Exception as e: printDebugMessage(f"Unable to find channel from URL. Exception: \n{trace()}")
                    latest_roblox_version = handler.getLatestClientVersion(debug=(main_config.get("EFlagEnableDebugMode") == True), channel=url_channel if url_channel else main_config.get("EFlagRobloxClientChannel", current_roblox_version.get("channel", "LIVE")), token=main_config.get("EFlagRobloxChannelUpdateToken"))
                    if latest_roblox_version["success"] == True:
                        download_channel = latest_roblox_version["attempted_channel"]
                        if current_roblox_version["client_version"] == latest_roblox_version["client_version"]: printMainMessage("Running latest version of Roblox!")
                        else:
                            continue_to_update = True
                            printSuccessMessage(f"A new version of Roblox is available! Versions: {current_roblox_version['version']} => {latest_roblox_version['hash']}")
                            printWarnMessage("--- Installing Latest Roblox Version ---")
                            if continue_to_update == True:
                                printMainMessage("Please wait while we install a newer version of Roblox into OrangeBlox!")
                                submit_status.start()
                                res = handler.installRoblox(debug=(main_config.get("EFlagEnableDebugMode") == True), copyRobloxInstallerPath=(main_os == "Darwin" and os.path.join(cur_path, "RobloxPlayerInstaller.app") or os.path.join(cur_path, "RobloxPlayerInstaller.exe")), downloadInstaller=True, downloadToken=main_config.get("EFlagRobloxChannelUpdateToken"), downloadChannel=download_channel)
                                submit_status.end()
                                if res and res["success"] == False:
                                    printErrorMessage("There is an issue while trying to install Roblox. Please try again by restarting this app!")
                                    input("> ")
                                    sys.exit(0)
                                if main_os == "Darwin":
                                    while not os.path.exists(RFFI.macOS_dir): time.sleep(0.1)
                                new_latest_roblox_version = handler.getCurrentClientVersion()
                                printSuccessMessage(f"Successfully updated Roblox to {new_latest_roblox_version.get('version')}!")
                                installed_update = True
                                skip_modification_mode = False
                            else: printErrorMessage("The download for this update is unavailable at this time! Try again later!")
                        if not (download_channel == (url_channel if url_channel else main_config.get("EFlagRobloxClientChannel", current_roblox_version.get("channel", "LIVE")))):
                            printDebugMessage(f"Setting Channel Based on Channel Difference: {download_channel}")
                            if download_channel == "production" or download_channel == "LIVE": download_channel = ""
                            if main_os == "Darwin":
                                res = plist_class.writePListFile(os.path.join(user_folder, "Library", "Preferences", "com.roblox.RobloxPlayerChannel.plist"), {"www.roblox.com": download_channel}, binary=True, ns_mode=True)
                                printDebugMessage(f"Channel Set Result: {res}")
                            elif main_os == "Windows":
                                try: registry_key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, r"Software\ROBLOX Corporation\Environments\RobloxPlayer\Channel", 0, win32con.KEY_SET_VALUE)
                                except Exception: registry_key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, r"Software\ROBLOX Corporation\Environments\RobloxPlayer\Channel")
                                win32api.RegSetValueEx(registry_key, "www.roblox.com", 0, win32con.REG_SZ, download_channel)
                                win32api.RegCloseKey(registry_key)
                    else:
                        printErrorMessage("There was an issue while checking for updates.")
                        printDebugMessage(latest_roblox_version)
                else: printErrorMessage("There was an issue while checking for updates.")
        
        # Prepare Roblox
        def prepareRobloxClient():
            global main_config
            global run_studio
            global installed_update
            printWarnMessage("--- Preparing Roblox Studio ---" if run_studio == True else "--- Preparing Roblox ---")
            if main_os == "Windows":
                content_folder_paths["Windows"] = handler.getRobloxInstallFolder(studio=run_studio)
                font_folder_paths["Windows"] = os.path.join(content_folder_paths['Windows'], "content", "fonts")
            elif main_os == "Darwin":
                content_folder_paths["Darwin"] = os.path.join(RFFI.macOS_studioDir if run_studio == True else RFFI.macOS_dir, "Contents", "Resources")
                font_folder_paths["Darwin"] = os.path.join(content_folder_paths['Darwin'], "content", "fonts")
            if not os.path.exists(font_folder_paths[main_os]):
                printErrorMessage("Please restart OrangeBlox in order to reinstall Roblox Studio!")
                input("> ")
                sys.exit(0)
                return
            if connect_instead == True: printMainMessage("Skipping Preparation because you're connecting instead of launching a new window!"); return
            
            try:
                # Debug
                printDebugMessage(f"Roblox Resources Location: {content_folder_paths[main_os]}")

                # Remove Builder Font
                if main_config.get("EFlagRemoveBuilderFont") == True:
                    printMainMessage("Changing Font Files..")
                    # Copy All Builder/Monsterrat Files to Separate Files
                    if not os.path.exists(os.path.join(font_folder_paths[main_os], "BuilderSansLock")):
                        copyFile(os.path.join(font_folder_paths[main_os], "BuilderSans-ExtraBold.otf"), os.path.join(font_folder_paths[main_os], "BuilderSans-ExtraBold-Locked.otf"))
                        copyFile(os.path.join(font_folder_paths[main_os], "BuilderSans-Bold.otf"), os.path.join(font_folder_paths[main_os], "BuilderSans-Bold-Locked.otf"))
                        copyFile(os.path.join(font_folder_paths[main_os], "BuilderSans-Medium.otf"), os.path.join(font_folder_paths[main_os], "BuilderSans-Medium-Locked.otf"))
                        copyFile(os.path.join(font_folder_paths[main_os], "BuilderSans-Regular.otf"), os.path.join(font_folder_paths[main_os], "BuilderSans-Regular-Locked.otf"))
                        copyFile(os.path.join(font_folder_paths[main_os], "BuilderExtended-Bold.otf"), os.path.join(font_folder_paths[main_os], "BuilderExtended-Bold-Locked.otf"))
                        copyFile(os.path.join(font_folder_paths[main_os], "BuilderExtended-SemiBold.otf"), os.path.join(font_folder_paths[main_os], "BuilderExtended-SemiBold-Locked.otf"))
                        copyFile(os.path.join(font_folder_paths[main_os], "BuilderExtended-Regular.otf"), os.path.join(font_folder_paths[main_os], "BuilderExtended-Regular-Locked.otf"))
                        copyFile(os.path.join(font_folder_paths[main_os], "Montserrat-Black.ttf"), os.path.join(font_folder_paths[main_os], "Montserrat-Black-Locked.ttf"))
                        copyFile(os.path.join(font_folder_paths[main_os], "Montserrat-Bold.ttf"), os.path.join(font_folder_paths[main_os], "Montserrat-Bold-Locked.ttf"))
                        copyFile(os.path.join(font_folder_paths[main_os], "Montserrat-Medium.ttf"), os.path.join(font_folder_paths[main_os], "Montserrat-Medium-Locked.ttf"))
                        copyFile(os.path.join(font_folder_paths[main_os], "Montserrat-Regular.ttf"), os.path.join(font_folder_paths[main_os], "Montserrat-Regular-Locked.ttf"))
                        copyFile(os.path.join(font_folder_paths[main_os], "BuilderMono-Regular.otf"), os.path.join(font_folder_paths[main_os], "BuilderMono-Regular-Locked.otf"))
                        copyFile(os.path.join(font_folder_paths[main_os], "BuilderMono-Light.otf"), os.path.join(font_folder_paths[main_os], "BuilderMono-Light-Locked.otf"))
                        copyFile(os.path.join(font_folder_paths[main_os], "BuilderMono-Bold.otf"), os.path.join(font_folder_paths[main_os], "BuilderMono-Bold-Locked.otf"))
                        copyFile(os.path.join(font_folder_paths[main_os], "Arimo-Regular.ttf"), os.path.join(font_folder_paths[main_os], "Arimo-Regular-Locked.ttf"))
                        copyFile(os.path.join(font_folder_paths[main_os], "Arimo-Bold.ttf"), os.path.join(font_folder_paths[main_os], "Arimo-Bold-Locked.ttf"))
                        with open(os.path.join(font_folder_paths[main_os], "BuilderSansLock"), "w", encoding="utf-8") as f: f.write("EnabledGothamFontMode")
                    if not main_config.get("EFlagEnabledMods"): main_config["EFlagEnabledMods"] = {}
                    main_config["EFlagEnabledMods"]["OldFont"] = True
                    main_config["EFlagEnableMods"] = True
                    printSuccessMessage("Successfully prepared change for Builder Sans/Monsterrat files to GothamSSm!")
                else:
                    if os.path.exists(os.path.join(font_folder_paths[main_os], "BuilderSansLock")):
                        copyFile(os.path.join(font_folder_paths[main_os], "BuilderSans-ExtraBold-Locked.otf"), os.path.join(font_folder_paths[main_os], "BuilderSans-ExtraBold.otf"))
                        copyFile(os.path.join(font_folder_paths[main_os], "BuilderSans-Bold-Locked.otf"), os.path.join(font_folder_paths[main_os], "BuilderSans-Bold.otf"))
                        copyFile(os.path.join(font_folder_paths[main_os], "BuilderSans-Medium-Locked.otf"), os.path.join(font_folder_paths[main_os], "BuilderSans-Medium.otf"))
                        copyFile(os.path.join(font_folder_paths[main_os], "BuilderSans-Regular-Locked.otf"), os.path.join(font_folder_paths[main_os], "BuilderSans-Regular.otf"))
                        copyFile(os.path.join(font_folder_paths[main_os], "Montserrat-Black-Locked.ttf"), os.path.join(font_folder_paths[main_os], "Montserrat-Black.ttf"))
                        copyFile(os.path.join(font_folder_paths[main_os], "Montserrat-Bold-Locked.ttf"), os.path.join(font_folder_paths[main_os], "Montserrat-Bold.ttf"))
                        copyFile(os.path.join(font_folder_paths[main_os], "Montserrat-Medium-Locked.ttf"), os.path.join(font_folder_paths[main_os], "Montserrat-Medium.ttf"))
                        copyFile(os.path.join(font_folder_paths[main_os], "Montserrat-Regular-Locked.ttf"), os.path.join(font_folder_paths[main_os], "Montserrat-Regular.ttf"))
                        copyFile(os.path.join(font_folder_paths[main_os], "BuilderMono-Regular-Locked.otf"), os.path.join(font_folder_paths[main_os], "BuilderMono-Regular.otf"))
                        copyFile(os.path.join(font_folder_paths[main_os], "BuilderMono-Light-Locked.otf"), os.path.join(font_folder_paths[main_os], "BuilderMono-Light.otf"))
                        copyFile(os.path.join(font_folder_paths[main_os], "BuilderMono-Bold-Locked.otf"), os.path.join(font_folder_paths[main_os], "BuilderMono-Bold.otf"))
                        copyFile(os.path.join(font_folder_paths[main_os], "Arimo-Regular-Locked.ttf"), os.path.join(font_folder_paths[main_os], "Arimo-Regular.ttf"))
                        copyFile(os.path.join(font_folder_paths[main_os], "Arimo-Bold-Locked.ttf"), os.path.join(font_folder_paths[main_os], "Arimo-Bold.ttf"))
                        copyFile(os.path.join(font_folder_paths[main_os], "BuilderExtended-Bold-Locked.otf"), os.path.join(font_folder_paths[main_os], "BuilderExtended-Bold.otf"))
                        copyFile(os.path.join(font_folder_paths[main_os], "BuilderExtended-SemiBold-Locked.otf"), os.path.join(font_folder_paths[main_os], "BuilderExtended-SemiBold.otf"))
                        copyFile(os.path.join(font_folder_paths[main_os], "BuilderExtended-Regular-Locked.otf"), os.path.join(font_folder_paths[main_os], "BuilderExtended-Regular.otf"))
                        with open(os.path.join(font_folder_paths[main_os], "BuilderSansLock"), "w", encoding="utf-8") as f: f.write("EnabledGothamFontMode")
                        printSuccessMessage("Successfully reverted Builder Sans/Monsterrat files!")
                    else: printDebugMessage("Builder Sans are already being used!")
                
                # Avatar Background
                if main_config.get("EFlagEnableChangeAvatarEditorBackground") == True:
                    printMainMessage("Changing Current Avatar Editor to Set Avatar Background..")
                    copyFile(os.path.join(mods_folder, "AvatarEditorMaps", f"{main_config.get('EFlagAvatarEditorBackground')}.rbxl"), os.path.join(content_folder_paths[main_os], "ExtraContent", "places", "Mobile.rbxl"))
                    printSuccessMessage("Successfully changed current avatar editor with a set background!")
                else:
                    printMainMessage("Changing Current Avatar Editor to Original Avatar Background..")
                    copyFile(os.path.join(mods_folder, "AvatarEditorMaps", "Original.rbxl"), os.path.join(content_folder_paths[main_os], "ExtraContent", "places", "Mobile.rbxl"))
                    printSuccessMessage("Successfully changed current avatar editor to original background!")
                
                # Cursors
                if main_config.get("EFlagEnableChangeCursor") == True:
                    printMainMessage("Changing Current Cursor to Set Cursor..")
                    copyFile(os.path.join(mods_folder, "Cursors", main_config.get('EFlagSelectedCursor'), "ArrowCursor.png"), os.path.join(content_folder_paths[main_os], "content", "textures", "Cursors", "KeyboardMouse", "ArrowCursor.png"))
                    copyFile(os.path.join(mods_folder, "Cursors", main_config.get('EFlagSelectedCursor'), "ArrowFarCursor.png"), os.path.join(content_folder_paths[main_os], "content", "textures", "Cursors", "KeyboardMouse", "ArrowFarCursor.png"))
                    copyFile(os.path.join(mods_folder, "Cursors", main_config.get('EFlagSelectedCursor'), "IBeamCursor.png"), os.path.join(content_folder_paths[main_os], "content", "textures", "Cursors", "KeyboardMouse", "IBeamCursor.png"))
                    printSuccessMessage("Successfully changed current cursor with a set cursor image!")
                else:
                    printMainMessage("Changing Current Cursor to Original Cursor..")
                    copyFile(os.path.join(mods_folder, "Cursors", "Original", "ArrowCursor.png"), os.path.join(content_folder_paths[main_os], "content", "textures", "Cursors", "KeyboardMouse", "ArrowCursor.png"))
                    copyFile(os.path.join(mods_folder, "Cursors", "Original", "ArrowFarCursor.png"), os.path.join(content_folder_paths[main_os], "content", "textures", "Cursors", "KeyboardMouse", "ArrowFarCursor.png"))
                    copyFile(os.path.join(mods_folder, "Cursors", "Original", "IBeamCursor.png"), os.path.join(content_folder_paths[main_os], "content", "textures", "Cursors", "KeyboardMouse", "IBeamCursor.png"))
                    printSuccessMessage("Successfully changed current cursor with original cursor image!")
                
                # Player Sounds
                if main_config.get("EFlagEnableChangePlayerSound") == True:
                    printMainMessage("Changing Current Player Sounds to Set Sound Files..")
                    sounds_folder = os.path.join(mods_folder, "PlayerSounds", main_config.get('EFlagSelectedPlayerSounds'))
                    copyFile(os.path.join(sounds_folder, "ouch.ogg"), os.path.join(content_folder_paths[main_os], "content", "sounds", "ouch.ogg"))
                    copyFile(os.path.join(sounds_folder, "action_falling.ogg"), os.path.join(content_folder_paths[main_os], "content", "sounds", "action_falling.ogg"))
                    copyFile(os.path.join(sounds_folder, "action_footsteps_plastic.mp3"), os.path.join(content_folder_paths[main_os], "content", "sounds", "action_footsteps_plastic.mp3"))
                    copyFile(os.path.join(sounds_folder, "action_get_up.mp3"), os.path.join(content_folder_paths[main_os], "content", "sounds", "action_get_up.mp3"))
                    copyFile(os.path.join(sounds_folder, "action_jump_land.mp3"), os.path.join(content_folder_paths[main_os], "content", "sounds", "action_jump_land.mp3"))
                    copyFile(os.path.join(sounds_folder, "action_jump.mp3"), os.path.join(content_folder_paths[main_os], "content", "sounds", "action_jump.mp3"))
                    copyFile(os.path.join(sounds_folder, "action_swim.mp3"), os.path.join(content_folder_paths[main_os], "content", "sounds", "action_swim.mp3"))
                    copyFile(os.path.join(sounds_folder, "impact_explosion_03.mp3"), os.path.join(content_folder_paths[main_os], "content", "sounds", "impact_explosion_03.mp3"))
                    copyFile(os.path.join(sounds_folder, "impact_water.mp3"), os.path.join(content_folder_paths[main_os], "content", "sounds", "impact_water.mp3"))
                    copyFile(os.path.join(sounds_folder, "volume_slider.ogg"), os.path.join(content_folder_paths[main_os], "content", "sounds", "volume_slider.ogg"))
                    printSuccessMessage("Successfully changed current player sounds with a set of sound files!")
                else:
                    printMainMessage("Changing Current Death Sound to Original Sound Files..")
                    sounds_folder = os.path.join(mods_folder, "PlayerSounds", "Current")
                    copyFile(os.path.join(sounds_folder, "ouch.ogg"), os.path.join(content_folder_paths[main_os], "content", "sounds", "ouch.ogg"))
                    copyFile(os.path.join(sounds_folder, "action_falling.ogg"), os.path.join(content_folder_paths[main_os], "content", "sounds", "action_falling.ogg"))
                    copyFile(os.path.join(sounds_folder, "action_footsteps_plastic.mp3"), os.path.join(content_folder_paths[main_os], "content", "sounds", "action_footsteps_plastic.mp3"))
                    copyFile(os.path.join(sounds_folder, "action_get_up.mp3"), os.path.join(content_folder_paths[main_os], "content", "sounds", "action_get_up.mp3"))
                    copyFile(os.path.join(sounds_folder, "action_jump_land.mp3"), os.path.join(content_folder_paths[main_os], "content", "sounds", "action_jump_land.mp3"))
                    copyFile(os.path.join(sounds_folder, "action_jump.mp3"), os.path.join(content_folder_paths[main_os], "content", "sounds", "action_jump.mp3"))
                    copyFile(os.path.join(sounds_folder, "action_swim.mp3"), os.path.join(content_folder_paths[main_os], "content", "sounds", "action_swim.mp3"))
                    copyFile(os.path.join(sounds_folder, "impact_explosion_03.mp3"), os.path.join(content_folder_paths[main_os], "content", "sounds", "impact_explosion_03.mp3"))
                    copyFile(os.path.join(sounds_folder, "impact_water.mp3"), os.path.join(content_folder_paths[main_os], "content", "sounds", "impact_water.mp3"))
                    copyFile(os.path.join(sounds_folder, "volume_slider.ogg"), os.path.join(content_folder_paths[main_os], "content", "sounds", "volume_slider.ogg"))
                    printSuccessMessage("Successfully changed current player sounds with original sound files!")
                
                # App Icons
                printMainMessage("Changing Brand Images..")
                if run_studio == True:
                    if main_config.get("EFlagEnableChangeBrandIcons2") == True: brand_fold = os.path.join(mods_folder, "RobloxStudioBrand", main_config.get('EFlagSelectedBrandLogo2'))
                    else: brand_fold = os.path.join(mods_folder, "RobloxStudioBrand", "Original")
                else:
                    if main_config.get("EFlagEnableChangeBrandIcons") == True: brand_fold = os.path.join(mods_folder, "RobloxBrand", main_config.get('EFlagSelectedBrandLogo'))
                    else: brand_fold = os.path.join(mods_folder, "RobloxBrand", "Original")
                if run_studio == False:
                    if os.path.exists(os.path.join(brand_fold, "MenuIcon.png")): copyFile(os.path.join(brand_fold, "MenuIcon.png"), os.path.join(content_folder_paths[main_os], "content", "textures", "ui", "TopBar", "coloredlogo.png"))
                    if os.path.exists(os.path.join(brand_fold, "MenuIcon@2x.png")): copyFile(os.path.join(brand_fold, "MenuIcon@2x.png"), os.path.join(content_folder_paths[main_os], "content", "textures", "ui", "TopBar", "coloredlogo@2x.png"))
                    if os.path.exists(os.path.join(brand_fold, "MenuIcon@3x.png")): copyFile(os.path.join(brand_fold, "MenuIcon@3x.png"), os.path.join(content_folder_paths[main_os], "content", "textures", "ui", "TopBar", "coloredlogo@3x.png"))
                    if os.path.exists(os.path.join(brand_fold, "RobloxLogo.png")): copyFile(os.path.join(brand_fold, "RobloxLogo.png"), os.path.join(content_folder_paths[main_os], "content", "textures", "ui", "ScreenshotHud", "RobloxLogo.png"))
                    if os.path.exists(os.path.join(brand_fold, "RobloxLogo@2x.png")): copyFile(os.path.join(brand_fold, "RobloxLogo@2x.png"), os.path.join(content_folder_paths[main_os], "content", "textures", "ui", "ScreenshotHud", "RobloxLogo@2x.png"))
                    if os.path.exists(os.path.join(brand_fold, "RobloxLogo@3x.png")): copyFile(os.path.join(brand_fold, "RobloxLogo@3x.png"), os.path.join(content_folder_paths[main_os], "content", "textures", "ui", "ScreenshotHud", "RobloxLogo@3x.png"))
                    if os.path.exists(os.path.join(brand_fold, "RobloxLogoBanner.png")): copyFile(os.path.join(brand_fold, "RobloxLogoBanner.png"), os.path.join(content_folder_paths[main_os], "ExtraContent", "textures", "ui", "LuaApp", "graphic", "Auth", "logo_white_1x.png"))
                    if os.path.exists(os.path.join(brand_fold, "RobloxLogoBannerLuobu.png")): copyFile(os.path.join(brand_fold, "RobloxLogoBannerLuobu.png"), os.path.join(content_folder_paths[main_os], "ExtraContent", "textures", "ui", "LuaApp", "graphic", "Auth", "logo_white_luobu.png"))
                    if os.path.exists(os.path.join(brand_fold, "RobloxNameIcon.png")): copyFile(os.path.join(brand_fold, "RobloxNameIcon.png"), os.path.join(content_folder_paths[main_os], "content", "textures", "ui", "RobloxNameIcon.png"))
                    if os.path.exists(os.path.join(brand_fold, "AdminIcon.png")): copyFile(os.path.join(brand_fold, "AdminIcon.png"), os.path.join(content_folder_paths[main_os], "content", "textures", "ui", "icon_admin-16.png"))
                    if os.path.exists(os.path.join(brand_fold, "RobloxTilt.png")): copyFile(os.path.join(brand_fold, "RobloxTilt.png"), os.path.join(content_folder_paths[main_os], "content", "textures", "loading", "robloxTilt.png")); copyFile(os.path.join(brand_fold, "RobloxTilt.png"), os.path.join(content_folder_paths[main_os], "content", "textures", "loading", "robloxTiltRed.png"))
                if main_os == "Darwin":
                    printMainMessage("Changing Current App Icon..")
                    if os.path.exists(os.path.join(brand_fold, "AppIcon.icns")): 
                        copyFile(os.path.join(brand_fold, "AppIcon.icns"), os.path.join(content_folder_paths[main_os], "AppIcon.icns"))
                        copyFile(os.path.join(brand_fold, "AppIcon.icns"), os.path.join(content_folder_paths[main_os], "../", "MacOS", "RobloxStudio.app" if run_studio == True else "Roblox.app", "Contents", "Resources", "AppIcon.icns"))
                        targ_app = os.path.join(content_folder_paths[main_os], '../', '../')
                        try:
                            subprocess.run(["/usr/bin/touch", targ_app], stdout=not main_config.get("EFlagEnableDebugMode") and subprocess.DEVNULL, stderr=not main_config.get("EFlagEnableDebugMode") and subprocess.DEVNULL)
                            subprocess.run(["/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister", "-f", targ_app], stdout=not main_config.get("EFlagEnableDebugMode") and subprocess.DEVNULL, stderr=not main_config.get("EFlagEnableDebugMode") and subprocess.DEVNULL)
                        except Exception as e: printDebugMessage("Something went wrong trying to set icon fully!")
                        printSuccessMessage("Successfully changed current app icon! It may take a moment for macOS to identify it!")
                elif main_os == "Windows":
                    printMainMessage("Changing App Shortcuts Icon..")
                    if os.path.exists(os.path.join(brand_fold, "AppIcon.ico")): 
                        try:
                            import win32com.client as win32client # type: ignore
                            def create_shortcut(target_path, shortcut_path, working_directory=None, icon_path=None, arguments=None):
                                shell = win32client.Dispatch('WScript.Shell')
                                if not os.path.exists(os.path.dirname(shortcut_path)): os.makedirs(os.path.dirname(shortcut_path),mode=511)
                                shortcut = shell.CreateShortcut(shortcut_path)
                                shortcut.TargetPath = target_path
                                if arguments: shortcut.Arguments = arguments
                                if working_directory: shortcut.WorkingDirectory = working_directory
                                if icon_path: shortcut.IconLocation = icon_path
                                shortcut.Save()
                            bootstrap_path = os.path.join(cur_path, "OrangeBlox.exe")
                            create_shortcut(bootstrap_path, os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs'), "OrangeBlox.lnk"))
                            create_shortcut(bootstrap_path, os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), "OrangeBlox.lnk"))
                            if run_studio == True:
                                create_shortcut(os.path.join(cur_path, "OrangeBlox.exe"), os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), "Roblox Studio.lnk"), icon_path=os.path.join(brand_fold, "AppIcon.ico") if main_config.get("EFlagUseRobloxAppIconAsShortcutIcon") else "", arguments="orangeblox://run-studio")
                                create_shortcut(os.path.join(cur_path, "OrangeBlox.exe"), os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs'), 'Run Studio.lnk'), icon_path=os.path.join(brand_fold, "AppIcon.ico") if main_config.get("EFlagUseRobloxAppIconAsShortcutIcon") else "", arguments="orangeblox://run-studio")
                                create_shortcut(os.path.join(cur_path, "OrangeBlox.exe"), os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Roblox'), 'Roblox Studio.lnk'), icon_path=os.path.join(brand_fold, "AppIcon.ico") if main_config.get("EFlagUseRobloxAppIconAsShortcutIcon") else "", arguments="orangeblox://run-studio")
                            else:
                                create_shortcut(os.path.join(cur_path, "OrangeBlox.exe"), os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), "Roblox Player.lnk"), icon_path=os.path.join(brand_fold, "AppIcon.ico") if main_config.get("EFlagUseRobloxAppIconAsShortcutIcon") else "", arguments="orangeblox://continue")
                                create_shortcut(os.path.join(cur_path, "OrangeBlox.exe"), os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs'), 'Play Roblox.lnk'), icon_path=os.path.join(brand_fold, "AppIcon.ico") if main_config.get("EFlagUseRobloxAppIconAsShortcutIcon") else "", arguments="orangeblox://continue")
                                create_shortcut(os.path.join(cur_path, "OrangeBlox.exe"), os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Roblox'), 'Roblox Player.lnk'), icon_path=os.path.join(brand_fold, "AppIcon.ico") if main_config.get("EFlagUseRobloxAppIconAsShortcutIcon") else "", arguments="orangeblox://continue")
                            printSuccessMessage("Successfully changed current shortcut icons! It may take a moment for Windows to identify it!")
                        except Exception as e: printErrorMessage(f"Unable to create shortcuts: {str(e)}")
                if (run_studio == True and main_config.get("EFlagEnableChangeBrandIcons2") == True) or (run_studio == False and main_config.get("EFlagEnableChangeBrandIcons") == True): printSuccessMessage("Successfully changed brand images!")
                else: printSuccessMessage("Successfully changed brand images to original!")
                
                # Installer Apps
                printMainMessage("Installing Updater Apps..")
                try:
                    if main_os == "Windows":
                        pip_class.copyTreeWithMetadata(os.path.join(cur_path, "_internal"), os.path.join(content_folder_paths[main_os], "_internal"), dirs_exist_ok=True, ignore_if_not_exist=True)
                        shutil.copy(os.path.join(cur_path, "OrangeBlox.exe" if run_studio == True else "OrangeBlox.exe"), os.path.join(content_folder_paths[main_os], "RobloxStudioInstaller.exe" if run_studio == True else "RobloxPlayerInstaller.exe"))
                        with open(os.path.join(content_folder_paths[main_os], "RobloxStudioBetaPlayRobloxRestart.txt" if run_studio == True else "RobloxPlayerBetaPlayRobloxRestart.txt"), "w", encoding="utf-8") as f: f.write(cur_path)
                    elif main_os == "Darwin":
                        backspacing = os.path.join(macos_app_path, "../")
                        if os.path.exists(os.path.join(backspacing, "Play Roblox.app")):
                            pip_class.copyTreeWithMetadata(os.path.join(backspacing, "Play Roblox.app"), os.path.join(RFFI.macOS_dir, "Contents", "MacOS", "RobloxPlayerInstaller.app"), dirs_exist_ok=True)
                            shutil.copy(os.path.join(backspacing, "Play Roblox.app", "Contents", "MacOS", "OrangePlayRoblox"), os.path.join(RFFI.macOS_dir, "Contents", "MacOS", "RobloxPlayerInstaller.app", "Contents", "MacOS", "RobloxPlayerInstaller"))
                            with open(os.path.join(RFFI.macOS_dir, "Contents", "MacOS", "RobloxPlayerInstaller.app", "Contents", "Resources", "RobloxPlayerBetaPlayRobloxRestart"), "w", encoding="utf-8") as f: f.write(cur_path)
                            for i in generateCodesignCommand(os.path.join(RFFI.macOS_dir, "Contents", "MacOS", "RobloxPlayerInstaller.app"), main_config.get("EFlagRobloxCodesigningName", "-")): 
                                if i[0] == "/usr/bin/xattr": subprocess.run(i, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                                else: subprocess.Popen(i, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        if os.path.exists(RFFI.macOS_studioDir) and run_studio == True and os.path.exists(os.path.join(backspacing, "Run Studio.app")):
                            pip_class.copyTreeWithMetadata(os.path.join(backspacing, "Run Studio.app"), os.path.join(RFFI.macOS_studioDir, "Contents", "MacOS", "RobloxStudioInstaller.app"), dirs_exist_ok=True)
                            shutil.copy(os.path.join(backspacing, "Run Studio.app", "Contents", "MacOS", "OrangeRunStudio"), os.path.join(RFFI.macOS_studioDir, "Contents", "MacOS", "RobloxStudioInstaller.app", "Contents", "MacOS", "RobloxStudioInstaller"))
                            with open(os.path.join(RFFI.macOS_studioDir, "Contents", "MacOS", "RobloxStudioInstaller.app", "Contents", "Resources", "RobloxStudioBetaPlayRobloxRestart"), "w", encoding="utf-8") as f: f.write(cur_path)
                            for i in generateCodesignCommand(os.path.join(RFFI.macOS_studioDir, "Contents", "MacOS", "RobloxStudioInstaller.app"), main_config.get("EFlagRobloxCodesigningName", "-")): 
                                if i[0] == "/usr/bin/xattr": subprocess.run(i, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                                else: subprocess.Popen(i, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    printSuccessMessage("Successfully installed updater apps!")
                except Exception as e: printErrorMessage(f"Unable to update installer apps! Recorded Error: \n{trace()}")

                # Studio Documentations and Fonts
                try:
                    api_doc = os.path.join(content_folder_paths[main_os], "content", "api_docs")
                    if run_studio == True and main_config.get("EFlagLimitAPIDocsLocalization") and os.path.exists(api_doc):
                        printMainMessage(f"Clearing API Docs Localization to {main_config.get('EFlagLimitAPIDocsLocalization')}.json")
                        for i in os.listdir(api_doc):
                            if i == f'{main_config.get("EFlagLimitAPIDocsLocalization")}.json': continue
                            if os.path.isfile(os.path.join(api_doc, i)): os.remove(os.path.join(api_doc, i))
                        printSuccessMessage("Cleared Localization Set!")
                    studio_fonts = os.path.join(content_folder_paths[main_os], "StudioFonts")
                    if run_studio == True and main_config.get("EFlagOverwriteUnneededStudioFonts") and os.path.exists(studio_fonts):
                        printMainMessage(f"Overwriting Studio Fonts to None..")
                        for i in os.listdir(studio_fonts):
                            if not i.startswith("NotoSans"): continue
                            if os.path.isfile(os.path.join(studio_fonts, i)): 
                                with open(os.path.join(studio_fonts, i), "w", encoding="utf-8") as f: f.write("")
                        printSuccessMessage("Overwritten Studio Fonts!")
                except Exception as e: printErrorMessage(f"Unable to overwrite API Documentation and Studio Fonts. Recorded Error: \n{trace()}")
                
                # Custom Mods
                if main_config.get("EFlagEnableMods") == True:
                    printMainMessage("Applying Mods..")
                    if type(main_config.get("EFlagEnabledMods")) is dict:
                        for i, v in main_config.get("EFlagEnabledMods").items():
                            if v == True:
                                try:
                                    mod_path = os.path.join(os.path.join(mods_folder, "Mods"), i)
                                    is_studio = False
                                    if os.path.exists(mod_path) and os.path.isdir(mod_path):
                                        ignore_given_files = []
                                        if os.path.exists(os.path.join(mod_path, "Manifest.json")):
                                            manife = readJSONFile(os.path.join(mod_path, "Manifest.json"))
                                            if manife and manife.get("ignore_transfer_of_files") and type(manife.get("ignore_transfer_of_files")) is list: ignore_given_files = manife.get("ignore_transfer_of_files")
                                            if manife and (manife.get("is_studio_mod") == True or (run_studio == True and manife.get("player_studio_support") == True)): is_studio = True
                                        if os.path.exists(os.path.join(mod_path, "StudioMod")): is_studio = True
                                        if is_studio == run_studio:
                                            def ignore_files_here(dir, files): return set(["ModScript.py", "Manifest.json", "Translations", f"Configuration_{user_folder_name}", "__pycache__"] + ignore_given_files) & set(files)
                                            pip_class.copyTreeWithMetadata(mod_path, content_folder_paths[main_os], dirs_exist_ok=True, ignore=ignore_files_here)
                                            printDebugMessage(f'Successfully applied "{i}" mod!')
                                except Exception as e: printErrorMessage(f"Unable to apply mod files of {i}. Recorded Error: \n{trace()}")
                        printSuccessMessage("Successfully applied all enabled mods!")
                
                # FFlags
                printMainMessage("Installing Fast Flags..")
                try:
                    filtered_fast_flags = {}
                    if run_studio == True and main_config.get("EFlagRobloxStudioFlags"):
                        for i, v in main_config.get("EFlagRobloxStudioFlags").items():
                            if i and (not i.startswith("EFlag")): filtered_fast_flags[i] = v
                    elif run_studio == False and main_config.get("EFlagRobloxPlayerFlags"):
                        for i, v in main_config.get("EFlagRobloxPlayerFlags").items():
                            if i and (not i.startswith("EFlag")): filtered_fast_flags[i] = v
                    submit_status.start()
                    handler.installFastFlags(filtered_fast_flags, debug=(main_config.get("EFlagEnableDebugMode") == True), endRobloxInstances=False, studio=run_studio, merge=True, ixp=main_config.get("EFlagUseIXPFastFlagsMethod2")==True)
                    submit_status.end()
                    printSuccessMessage("Successfully installed FFlags to the Roblox files!")
                except Exception as e: printErrorMessage(f"Unable to install Fast Flags to the client! Recorded Error: \n{trace()}")

                # Registration
                if main_os == "Darwin":
                    try:
                        if run_studio == True:
                            if os.path.exists(os.path.join(RFFI.macOS_studioDir, "Contents", "Info.plist")):
                                plist_data = plist_class.readPListFile(os.path.join(RFFI.macOS_studioDir, "Contents", "Info.plist"))
                                if plist_data.get("CFBundleName"):
                                    printMainMessage("Editing Roblox Studio Info.plist..")
                                    plist_data["CFBundleURLTypes"] = []
                                    plist_data["CFBundleDocumentTypes"] = []
                                    plist_data["UTExportedTypeDeclarations"] = []
                                    plist_data["NSDisableAutomaticTermination"] = True
                                    plist_data["NSPersistentStoreRebuildDisallowed"] = True
                                    plist_data["CFBundleIconFile"] = "AppIcon.icns"
                                    plist_data["CFBundleIconName"] = "AppIcon.icns"
                                    printDebugMessage(f"Successfully removed all URL Schemes for Roblox Studio.app!")
                                    s = plist_class.writePListFile(os.path.join(RFFI.macOS_studioDir, "Contents", "Info.plist"), plist_data)
                                    if s["success"] == True:
                                        subprocess.run([f"/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister", "-f", os.path.join(content_folder_paths[main_os], '../', '../')], stdout=not main_config.get("EFlagEnableDebugMode") and subprocess.DEVNULL, stderr=not main_config.get("EFlagEnableDebugMode") and subprocess.DEVNULL)
                                        printSuccessMessage("Successfully wrote to Info.plist!")
                                    else: printErrorMessage(f"Something went wrong saving Roblox Info.plist: {s['message']}")
                                    if main_config.get("EFlagRemoveCodeSigningMacOS") == True:
                                        printMainMessage("Checking for Code Signatures..")
                                        if os.path.exists(f"{RFFI.macOS_studioDir}/Contents/_CodeSignature/"):
                                            shutil.rmtree(f"{RFFI.macOS_studioDir}/Contents/_CodeSignature/", ignore_errors=True)
                                            printSuccessMessage("Removed Code-signing on Roblox Studio.app!")
                                        else: printSuccessMessage("Removing Code-signing is not needed because it doesn't exist!")
                                    def check_codesign():
                                        try:
                                            result = subprocess.run(
                                                f"cat '{os.path.join(RFFI.macOS_studioDir, 'Contents', 'MacOS', 'RobloxStudio')}' > /dev/null && \
                                                    codesign -v --no-strict '{os.path.join(RFFI.macOS_studioDir, 'Contents', 'MacOS', 'RobloxStudio')}'",
                                                shell=True, cwd=cur_path
                                            )   
                                            printDebugMessage(f"Code Signing Validation Response: {result.returncode}")
                                            if result.returncode == 0: return True
                                            else: return False
                                        except Exception as e:
                                            printDebugMessage(f"Unable to validate codesign: \n{trace()}")
                                            return False
                                    printMainMessage("Validating code-sign..")
                                    if main_config.get("EFlagRemoveCodeSigningMacOS") == True or check_codesign() == False:
                                        printMainMessage("Signing Roblox Studio.app..")
                                        def req_codesign(co=0):
                                            plist_class.writePListFile(os.path.join(cur_path, "RbxStudioEntitlements.plist"), {
                                                "com.apple.security.cs.allow-jit": True,
                                                "com.apple.security.cs.disable-executable-page-protection": True,
                                                "com.apple.security.device.audio-input": True,
                                                "com.apple.security.device.camera": True,
                                                "com.apple.security.network.client": True
                                            })
                                            for i in generateCodesignCommand(RFFI.macOS_studioDir, main_config.get("EFlagRobloxCodesigningName", "-"), entitlements=os.path.join(cur_path, "RbxStudioEntitlements.plist")): result = subprocess.run(i, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                                            os.remove(os.path.join(cur_path, "RbxStudioEntitlements.plist"))
                                            printDebugMessage(f"Code Signing Response: {result.returncode}")
                                            if result.returncode == 0: printSuccessMessage("Successfully signed Roblox Studio.app!")
                                            else:
                                                printErrorMessage(f"Unable to sign Roblox Studio.app: {result.returncode}")
                                                if co == 0: printMainMessage("Attempting Resign! Please wait!")
                                                if os.path.exists(os.path.join(RFFI.macOS_studioDir, "Contents", "_CodeSignature")): shutil.rmtree(os.path.join(RFFI.macOS_studioDir, "Contents", "_CodeSignature"), ignore_errors=True)
                                                req_codesign(co=co+1)
                                        req_codesign()
                                    else: printSuccessMessage("Code-signing is valid for use!")
                                else: printErrorMessage(f"Something went wrong reading Roblox Studio Info.plist: Bundle name not found")
                            else: printErrorMessage(f"Something went wrong reading Roblox Studio Info.plist: Bundle not found")
                        else:
                            if os.path.exists(os.path.join(RFFI.macOS_dir, "Contents", "Info.plist")):
                                plist_data = plist_class.readPListFile(os.path.join(RFFI.macOS_dir, "Contents", "Info.plist"))
                                if plist_data.get("CFBundleName"):
                                    printMainMessage("Editing Roblox Info.plist..")
                                    plist_data["CFBundleIconFile"] = "AppIcon.icns"
                                    plist_data["CFBundleIconName"] = "AppIcon.icns"
                                    if (main_config.get("EFlagEnableDuplicationOfClients") == True):
                                        if plist_data.get("LSMultipleInstancesProhibited") == True:
                                            plist_data["LSMultipleInstancesProhibited"] = False
                                            printDebugMessage(f"Successfully set plist key LSMultipleInstancesProhibited to False!")
                                    else:
                                        if plist_data.get("LSMultipleInstancesProhibited") == False:
                                            plist_data["LSMultipleInstancesProhibited"] = True
                                            printDebugMessage(f"Successfully set plist key LSMultipleInstancesProhibited to True!")
                                    if plist_data.get("CFBundleURLTypes"):
                                        plist_data["CFBundleURLTypes"] = []
                                        plist_data["NSDisableAutomaticTermination"] = True
                                        plist_data["NSPersistentStoreRebuildDisallowed"] = True
                                        printDebugMessage(f"Successfully removed all URL Schemes for Roblox.app!")
                                    s = plist_class.writePListFile(os.path.join(RFFI.macOS_dir, "Contents", "Info.plist"), plist_data)
                                    if s["success"] == True:
                                        subprocess.run([f"/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister", "-f", os.path.join(content_folder_paths[main_os], '../', '../')], stdout=not main_config.get("EFlagEnableDebugMode") and subprocess.DEVNULL, stderr=not main_config.get("EFlagEnableDebugMode") and subprocess.DEVNULL)
                                        printSuccessMessage("Successfully wrote to Info.plist!")
                                    else: printErrorMessage(f"Something went wrong saving Roblox Info.plist: {s['message']}")
                                    if main_config.get("EFlagRemoveCodeSigningMacOS") == True:
                                        printMainMessage("Checking for Code Signatures..")
                                        if os.path.exists(os.path.join(RFFI.macOS_dir, "Contents", "_CodeSignature")):
                                            shutil.rmtree(os.path.join(RFFI.macOS_dir, "Contents", "_CodeSignature"), ignore_errors=True)
                                            printSuccessMessage("Removed Code-signing on Roblox.app!")
                                        else: printSuccessMessage("Removing Code-signing is not needed because it doesn't exist!")
                                    def check_codesign():
                                        try:
                                            result = subprocess.run(
                                                f"cat {os.path.join(RFFI.macOS_dir, 'Contents', 'MacOS', 'RobloxPlayer')} > /dev/null && \
                                                    codesign -v --no-strict {os.path.join(RFFI.macOS_dir, 'Contents', 'MacOS', 'RobloxPlayer')}",
                                                shell=True, cwd=cur_path
                                            )   
                                            printDebugMessage(f"Code Signing Validation Response: {result.returncode}")
                                            if result.returncode == 0: return True
                                            else: return False
                                        except Exception as e:
                                            printDebugMessage(f"Unable to validate codesign: \n{trace()}")
                                            return False
                                    printMainMessage("Validating code-sign..")
                                    if main_config.get("EFlagRemoveCodeSigningMacOS") == True or check_codesign() == False:
                                        printMainMessage("Signing Roblox.app..")
                                        def req_codesign(co=0):
                                            plist_class.writePListFile(os.path.join(cur_path, "RbxEntitlements.plist"), {
                                                "com.apple.security.cs.allow-jit": True,
                                                "com.apple.security.cs.disable-executable-page-protection": True,
                                                "com.apple.security.device.audio-input": True,
                                                "com.apple.security.device.camera": True,
                                                "com.apple.security.network.client": True
                                            })
                                            for i in generateCodesignCommand(RFFI.macOS_dir, main_config.get("EFlagRobloxCodesigningName", "-"), entitlements=os.path.join(cur_path, "RbxEntitlements.plist")): result = subprocess.run(i, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cur_path)
                                            os.remove(os.path.join(cur_path, "RbxEntitlements.plist"))
                                            printDebugMessage(f"Code Signing Response: {result.returncode}")
                                            if result.returncode == 0: printSuccessMessage("Successfully signed Roblox.app!")
                                            else:
                                                printErrorMessage(f"Unable to sign Roblox.app: {result.returncode}")
                                                if co == 0: printMainMessage("Attempting Resign! Please wait!")
                                                if os.path.exists(os.path.join(RFFI.macOS_dir, "Contents", "_CodeSignature")): shutil.rmtree(os.path.join(RFFI.macOS_dir, "Contents", "_CodeSignature"), ignore_errors=True)
                                                req_codesign(co=co+1)
                                        req_codesign()
                                    else: printSuccessMessage("Code-signing is valid for use!")
                                else: printErrorMessage(f"Something went wrong reading Roblox Info.plist: Bundle name not found")
                            else: printErrorMessage(f"Something went wrong reading Roblox Info.plist: Bundle not found")
                    except Exception as e: printErrorMessage(f"Something went wrong modifying Info.plist of Roblox client: \n{trace()}")

                    try:
                        if main_config.get("EFlagRemoveRobloxAppDockShortcut") == True:
                            dock_path = os.path.join(os.path.expanduser("~"), "Library", "Preferences", "com.apple.dock.plist")
                            dock_data = {}
                            shortcut_replaced = False
                            if os.path.exists(dock_path):
                                dock_data = plist_class.readPListFile(dock_path)
                                printMainMessage("Overwriting Dock..")
                                if dock_data.get("persistent-apps"):
                                    for i in dock_data["persistent-apps"]:
                                        if i and i.get("tile-data"):
                                            if i["tile-data"].get("bundle-identifier") == ("com.Roblox.RobloxStudio" if run_studio == True else "com.roblox.RobloxPlayer"):
                                                dock_data["persistent-apps"].remove(i)
                                                shortcut_replaced = True
                            if shortcut_replaced == True:
                                plist_class.writePListFile(dock_path, dock_data)
                                time.sleep(1)
                                subprocess.run(["/usr/bin/killall", "cfprefsd"], cwd=cur_path)
                                subprocess.run(["/usr/bin/killall", "Dock"], cwd=cur_path)
                                printSuccessMessage("Successfully removed RobloxStudio.app Dock Shortcut!" if run_studio == True else "Successfully removed Roblox.app Dock Shortcut!")
                            else: printSuccessMessage("No changes were made to the dock!")
                    except Exception as e: printErrorMessage(f"Unable to make changes to the dock: \n{trace()}")
                elif main_os == "Windows" and os.path.exists(os.path.join(cur_path, "OrangeBlox.exe")):
                    # Reapply URL Schemes
                    if not (main_config.get("EFlagDisableURLSchemeInstall") == True):
                        bootstrap_folder_path = cur_path
                        bootstrap_path = os.path.join(bootstrap_folder_path, "OrangeBlox.exe")
                        try:
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
                            set_url_scheme("efaz-bootstrap", bootstrap_path)
                            set_url_scheme("orangeblox", bootstrap_path)
                            set_url_scheme("roblox-player", bootstrap_path)
                            if run_studio == True:
                                set_url_scheme("roblox-studio", bootstrap_path)
                                set_url_scheme("roblox-studio-auth", os.path.join(content_folder_paths["Windows"], "RobloxStudioBeta.exe"))
                            set_url_scheme("roblox", bootstrap_path)
                            set_file_type_reg(".rbxl", bootstrap_path, "Roblox Place")
                            set_file_type_reg(".rbxlx", bootstrap_path, "Roblox Place")
                            set_file_type_reg(".obx", bootstrap_path, "OrangeBlox Backup")
                        except Exception as e: printErrorMessage(f"Something went wrong setting up URL schemes: \n{trace()}")

                    # Reapply Shortcuts
                    if not (main_config.get("EFlagDisableShortcutsInstall") == True):
                        try:
                            printMainMessage("Setting up shortcuts..")
                            import win32com.client as win32client # type: ignore
                            def create_shortcut(target_path, shortcut_path, working_directory=None, icon_path=None, arguments=None):
                                shell = win32client.Dispatch('WScript.Shell')
                                if not os.path.exists(os.path.dirname(shortcut_path)): os.makedirs(os.path.dirname(shortcut_path),mode=511)
                                shortcut = shell.CreateShortcut(shortcut_path)
                                shortcut.TargetPath = target_path
                                if arguments: shortcut.Arguments = arguments
                                if working_directory: shortcut.WorkingDirectory = working_directory
                                if icon_path: shortcut.IconLocation = icon_path
                                shortcut.Save()
                            create_shortcut(bootstrap_path, os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs'), "OrangeBlox.lnk"))
                            create_shortcut(bootstrap_path, os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), "OrangeBlox.lnk"))
                        except Exception as e: printErrorMessage(f"Something went wrong setting up shortcuts: \n{trace()}")

                    # Reapply Installation to Windows
                    try:
                        printMainMessage("Marking Program Installation into Windows..")
                        app_reg_path = "Software\\OrangeBlox"
                        app_key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, app_reg_path)
                        win32api.RegSetValueEx(app_key, "InstallPath", 0, win32con.REG_SZ, bootstrap_folder_path)
                        win32api.RegSetValueEx(app_key, "Installed", 0, win32con.REG_DWORD, 1)
                        win32api.RegCloseKey(app_key)
                        registry_path = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\OrangeBlox"
                        registry_key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, registry_path)
                        win32api.RegSetValueEx(registry_key, "UninstallString", 0, win32con.REG_SZ, f"\"{sys.executable}\" \"{os.path.join(bootstrap_folder_path, 'Install.py')}\" -un")
                        win32api.RegSetValueEx(registry_key, "ModifyPath", 0, win32con.REG_SZ, f"\"{sys.executable}\" \"{os.path.join(bootstrap_folder_path, 'Install.py')}\"")
                        win32api.RegSetValueEx(registry_key, "DisplayName", 0, win32con.REG_SZ, "OrangeBlox")
                        win32api.RegSetValueEx(registry_key, "DisplayVersion", 0, win32con.REG_SZ, current_version["version"])
                        win32api.RegSetValueEx(registry_key, "DisplayIcon", 0, win32con.REG_SZ, os.path.join(bootstrap_folder_path, "Images", "AppIcon.ico"))
                        win32api.RegSetValueEx(registry_key, "HelpLink", 0, win32con.REG_SZ, "https://github.com/efazdev/orangeblox")
                        win32api.RegSetValueEx(registry_key, "URLUpdateInfo", 0, win32con.REG_SZ, "https://github.com/efazdev/orangeblox")
                        win32api.RegSetValueEx(registry_key, "URLInfoAbout", 0, win32con.REG_SZ, "https://github.com/efazdev/orangeblox")
                        win32api.RegSetValueEx(registry_key, "InstallLocation", 0, win32con.REG_SZ, bootstrap_folder_path)
                        win32api.RegSetValueEx(registry_key, "Publisher", 0, win32con.REG_SZ, "EfazDev")
                        win32api.RegSetValueEx(registry_key, "EstimatedSize", 0, win32con.REG_DWORD, min(getFolderSize(bootstrap_folder_path, formatWithAbbreviation=False) // 1024, 0xFFFFFFFF))
                        win32api.RegCloseKey(registry_key)
                    except Exception as e: printErrorMessage(f"Something went wrong setting up registry: \n{trace()}")
            except Exception as e:
                printErrorMessage(f"There was a problem applying mods to the Roblox Client!")
                printDebugMessage(f"Error Message: \n{trace()}")
        def prepareRobloxClientWithErrorCatcher():
            try: prepareRobloxClient()
            except Exception as e: printErrorMessage(f"There was an error preparing Roblox: \n{trace()}")
        if main_config.get("EFlagEnableSkipModificationMode") == True and main_os == "Darwin" and handler.getIfRobloxIsOpen(studio=run_studio): skip_modification_mode = True
        if skip_modification_mode == False: prepareRobloxClientWithErrorCatcher()
        else: threading.Thread(target=prepareRobloxClientWithErrorCatcher, daemon=True).start()

        # Event Variables
        rpc = None
        rpc_info = None
        current_place_info = None
        is_teleport = False
        is_app_login_fail = False
        connected_user_info = None
        updated_count = 0
        set_server_type = 0
        connected_to_game = False
        is_connection_lost = False
        set_current_private_server_key = None
        connected_roblox_instance = None
        skip_disconnect_notification = False

        # Mod Scripts
        mod_script_modules: dict[str, importlib.machinery.ModuleSpec] = {}
        generated_api_instances = {}
        generated_secret_keys = {}
        orangeapi_modules = {}
        mod_script_jsons = {}
        mods_manifest = generateModsManifest()
        selected_mod_scripts = [i for i, v in main_config.get('EFlagSelectedModScripts', {}).items() if os.path.exists(os.path.join(mods_folder, "Mods", i, "ModScript.py")) and v.get("enabled") == True]
        roblox_launched_affect_mod_script = False
        def loadModScripts():
            global mod_script_modules
            global mod_script_jsons
            global selected_mod_scripts
            global main_config
            if main_config.get("EFlagEnableMods") == True:
                if selected_mod_scripts and not (main_config.get("EFlagAllowActivityTracking") == False) and len(selected_mod_scripts) > 0:
                    OrangeAPI.requested_functions = {}
                    OrangeAPI.cached_information = {}
                    OrangeAPI.translators = {}
                    OrangeAPI.debug_mode = (main_config.get("EFlagEnableDebugMode")==True)
                    OrangeAPI.studio_mode = run_studio==True
                    OrangeAPI.launched_from_bootstrap = True
                    OrangeAPI.current_version["bootstrap_version"] = current_version["version"]
                    for sel_mo in selected_mod_scripts:
                        if os.path.exists(os.path.join(mods_folder, "Mods", sel_mo, "Manifest.json")):
                            mod_script_jsons[sel_mo] = readJSONFile(os.path.join(mods_folder, "Mods", sel_mo, "Manifest.json"))
                            if mod_script_jsons.get(sel_mo):
                                if mods_manifest.get(sel_mo) and mods_manifest.get(sel_mo).get("mod_script") == True:
                                    printMainMessage(f"Preparing Mod Script ({sel_mo})..")
                                    mod_manifest = mods_manifest.get(sel_mo)
                                    if mod_manifest["mod_script_supports"] <= current_version["version"] and mod_manifest["mod_script_end_support"] > current_version["version"] and mod_manifest["mod_script_supports_operating_system"] == True:
                                        def s(sel_mod):
                                            nonlocal mod_manifest
                                            global mod_script_modules
                                            global mod_script_jsons
                                            global selected_mod_scripts

                                            with open(os.path.join(mods_folder, "Mods", sel_mod, "ModScript.py"), "r", encoding="utf-8") as f: mod_script_text = f.read()
                                            approved_items_list = main_config.get('EFlagSelectedModScripts').get(sel_mod).get("permissions", [])
                                            approved_through_scan = True

                                            for i, v in handler.roblox_event_info.items():
                                                if v.get("detection") and v.get("detection") in mod_script_text and (not (i in approved_items_list)): approved_through_scan = False
                                            if mod_manifest.get("permissions"):
                                                for i in mod_manifest["permissions"]:
                                                    if not i in approved_items_list: approved_through_scan = False
                                            if mod_manifest.get("python_modules"):
                                                for i in mod_manifest["python_modules"]:
                                                    if not f"pip_{i}" in approved_items_list: approved_through_scan = False
                                            mod_script_detail = main_config.get('EFlagSelectedModScripts').get(sel_mo)
                                            if not (mod_manifest["mod_script_hash"] == mod_script_detail.get("hash", "")): approved_through_scan = False; printDebugMessage(f"Unable to validate hash: {mod_manifest['mod_script_hash']} => {main_config.get('EFlagSelectedModScripts').get(sel_mo).get('hash', '')}")
                                            if approved_through_scan == True:
                                                if mod_manifest.get("python_modules"):
                                                    printDebugMessage("Validating Installation of Mod Script Modules..")
                                                    if not pip_class.installed(mod_manifest.get("python_modules", []), boolonly=True): pip_class.install(mod_manifest.get("python_modules", []))
                                                printDebugMessage("Initalizing Components..")
                                                script_path = os.path.join(mods_folder, "Mods", sel_mod, "ModScript.py")
                                                api_handled_requests = {}
                                                try:
                                                    # Create API Copy
                                                    generated_secret_keys[sel_mod] = os.urandom(3).hex()
                                                    generated_api_instances[sel_mod] = OrangeAPI.OrangeAPI(OrangeAPI.OrangeAPIDetails(sel_mod, generated_secret_keys[sel_mod]))
                                                    
                                                    translation_path = os.path.join(mods_folder, "Mods", sel_mod, "Translations", main_config.get("EFlagSelectedBootstrapLanguage", "en") + ".json")
                                                    if os.path.exists(translation_path): OrangeAPI.translators[sel_mod] = PyKits.Translator(lang=translation_path)
                                                    else: OrangeAPI.translators[sel_mod] = stdout.translation_obj
                                                    orangeapi_modules[sel_mod] = OrangeAPI

                                                    # Load Mod Script
                                                    with open(script_path, "r", encoding="utf-8") as f: mod_script_contents = f.read()
                                                    if "import OrangeAPI" in mod_script_contents: 
                                                        for i in mod_script_contents.splitlines():
                                                            if i.startswith("import OrangeAPI"): mod_script_contents = mod_script_contents.replace("import OrangeAPI", "#import OrangeAPI")
                                                            elif i.startswith("from OrangeAPI"): mod_script_contents = mod_script_contents.replace("from OrangeAPI", "#from OrangeAPI")
                                                    if "EfazRobloxBootstrapAPI()" in mod_script_contents or "import EfazRobloxBootstrapAPI" in mod_script_contents or "from EfazRobloxBootstrapAPI" in mod_script_contents: mod_script_contents = mod_script_contents.replace("EfazRobloxBootstrapAPI()", "OrangeAPI()").replace("from EfazRobloxBootstrapAPI", "from OrangeAPI").replace("import EfazRobloxBootstrapAPI", "import OrangeAPI")
                                                    if "from OrangeAPI import OrangeAPI;" in mod_script_contents or " = OrangeAPI()" in mod_script_contents: mod_script_contents = mod_script_contents.replace("from OrangeAPI import OrangeAPI;", "import OrangeAPI as orange; OrangeAPI = orange.OrangeAPI();").replace(" = OrangeAPI()", " = OrangeAPI")
                                                    if "import RobloxFastFlagsInstaller" in mod_script_contents: mod_script_contents = mod_script_contents.replace("import RobloxFastFlagsInstaller", "import OrangeAPI")
                                                    if "import PipHandler" in mod_script_contents: mod_script_contents = mod_script_contents.replace("import PipHandler", "import OrangeAPI")
                                                    if "import PyKits" in mod_script_contents: mod_script_contents = mod_script_contents.replace("import PyKits", "import OrangeAPI")
                                                    if "import Install" in mod_script_contents: mod_script_contents = mod_script_contents.replace("import Install", "import OrangeAPI")
                                                    if "import DiscordPresenceHandler" in mod_script_contents: mod_script_contents = mod_script_contents.replace("import DiscordPresenceHandler", "import OrangeAPI")
                                                    if "import Main" in mod_script_contents: mod_script_contents = mod_script_contents.replace("import Main", "import OrangeAPI")
                                                    if "import builtins" in mod_script_contents: mod_script_contents = mod_script_contents.replace("import builtins", "import OrangeAPI")
                                                    with open(script_path, "w", encoding="utf-8") as f: f.write(mod_script_contents)
                                                    spec = importlib.util.spec_from_file_location(f"ModScript_{sel_mod}", script_path)
                                                    mod_script_modules[sel_mod] = importlib.util.module_from_spec(spec)
                                                    setattr(mod_script_modules[sel_mod], "OrangeAPI", generated_api_instances[sel_mod])
                                                    
                                                    # Set and Handle API to Mod Script
                                                    def checkGeneratedInstances(selected_mod_scriptttt, api_name):
                                                        while True:
                                                            try:
                                                                if hasattr(mod_script_modules[selected_mod_scriptttt], api_name):
                                                                    generated_api_instances[f"{selected_mod_scriptttt}"] = getattr(mod_script_modules[selected_mod_scriptttt], api_name)
                                                                else:
                                                                    printDebugMessage(f"Ended accepting requests from mod script {selected_mod_scriptttt} due to an issue. | Code: 2")
                                                                    generated_api_instances[f"{selected_mod_scriptttt}"] = None
                                                                    return
                                                            except Exception as e:
                                                                resulting_err = trace()
                                                                if "dictionary changed size during iteration" in resulting_err:
                                                                    if main_config.get("EFlagModScriptRequestTooFastMessage") == True: printDebugMessage("Mod Script is requesting data too fast!")
                                                                else:
                                                                    printDebugMessage(f"Error from Mod Script module: \n{resulting_err}")
                                                                    printErrorMessage(f"Ended accepting requests from Mod Scripts ({selected_mod_scriptttt}) due to an issue. | Code: 1")
                                                                    generated_api_instances[f"{selected_mod_scriptttt}"] = None
                                                                    return
                                                            time.sleep(main_config.get("EFlagModScriptAPIRefreshTime", 0.05))
                                                    def handleRequests(selected_mod_scriptt, approved_lis):
                                                        while True:
                                                            try:
                                                                for i, v in orangeapi_modules[selected_mod_scriptt].requested_functions.items():
                                                                    if type(v) is orangeapi_modules[selected_mod_scriptt].Request:
                                                                        identification = v.id.split("|")
                                                                        if not (api_handled_requests.get(i) == True):
                                                                            if identification[0] != selected_mod_scriptt: continue
                                                                            try:
                                                                                if ((v.requested in approved_lis) or (handler.roblox_event_info.get(v.requested, {"free": False}).get("free") == True)) and (v.fulfilled == False):
                                                                                    def getMainConf(scri: str): 
                                                                                        filtered_fflag = {}
                                                                                        restricted_fflags = ["EFlagDiscordWebhookURL", "EFlagRobloxLinkShortcuts"]
                                                                                        for i, v in main_config.items():
                                                                                            if not (i in restricted_fflags): filtered_fflag[i] = v
                                                                                        return filtered_fflag
                                                                                    def getFF(scri: str): 
                                                                                        if run_studio == True: return main_config.get("EFlagRobloxStudioFlags", {})
                                                                                        else: return main_config.get("EFlagRobloxPlayerFlags", {})
                                                                                    def setMainConf(scri: str, js: dict, full=False): 
                                                                                        if type(js) is dict:
                                                                                            global main_config
                                                                                            before_config = main_config
                                                                                            if full == True: 
                                                                                                main_config = js
                                                                                                for i in before_config.keys(): 
                                                                                                    if not main_config.get(i): modified_flags_from_mod_scripts.append(i)
                                                                                            else:
                                                                                                for i, v in js.items(): main_config[i] = v
                                                                                            for i in js.keys(): 
                                                                                                if not i in modified_flags_from_mod_scripts: modified_flags_from_mod_scripts.append(i)
                                                                                    def setFF(scri: str, js: dict, full=False): 
                                                                                        if type(js) is dict:
                                                                                            if full == True: 
                                                                                                if run_studio == True: main_config["EFlagRobloxStudioFlags"] = js
                                                                                                else: main_config["EFlagRobloxPlayerFlags"] = js
                                                                                            else:
                                                                                                main_config["EFlagRobloxPlayerFlags"] = main_config.get("EFlagRobloxPlayerFlags", {})
                                                                                                main_config["EFlagRobloxStudioFlags"] = main_config.get("EFlagRobloxStudioFlags", {})
                                                                                                for i, v in js.items(): 
                                                                                                    if run_studio == True: main_config["EFlagRobloxStudioFlags"][i] = v
                                                                                                    else: main_config["EFlagRobloxPlayerFlags"][i] = v
                                                                                            if run_studio == True and not "EFlagRobloxStudioFlags" in modified_flags_from_mod_scripts: modified_flags_from_mod_scripts.append("EFlagRobloxStudioFlags")
                                                                                            elif not "EFlagRobloxPlayerFlags" in modified_flags_from_mod_scripts: modified_flags_from_mod_scripts.append("EFlagRobloxPlayerFlags")
                                                                                            filtered_fast_flags = {}
                                                                                            if run_studio == True and main_config.get("EFlagRobloxStudioFlags"):
                                                                                                for i, v in main_config.get("EFlagRobloxStudioFlags").items():
                                                                                                    if i and (not i.startswith("EFlag")): filtered_fast_flags[i] = v
                                                                                            elif run_studio == False and main_config.get("EFlagRobloxPlayerFlags"):
                                                                                                for i, v in main_config.get("EFlagRobloxPlayerFlags").items():
                                                                                                    if i and (not i.startswith("EFlag")): filtered_fast_flags[i] = v
                                                                                            handler.installFastFlags(filtered_fast_flags, debug=(main_config.get("EFlagEnableDebugMode") == True), endRobloxInstances=False, studio=run_studio, ixp=main_config.get("EFlagUseIXPFastFlagsMethod2")==True)
                                                                                    def saveMainConf(scri: str, js: dict, full=False): 
                                                                                        if type(js) is dict:
                                                                                            global main_config
                                                                                            if full == True:
                                                                                                filtered_fflag = {}
                                                                                                filtered_fflag["EFlagRobloxPlayerFlags"] = main_config.get("EFlagRobloxPlayerFlags", {})
                                                                                                filtered_fflag["EFlagRobloxStudioFlags"] = main_config.get("EFlagRobloxStudioFlags", {})
                                                                                                for i, v in js.items():
                                                                                                    if not ("EFlag" in i): 
                                                                                                        if run_studio == True: filtered_fflag["EFlagRobloxStudioFlags"][i] = v
                                                                                                        else: filtered_fflag["EFlagRobloxPlayerFlags"][i] = v
                                                                                                    else: main_config[i] = v
                                                                                                main_config = filtered_fflag
                                                                                            else:
                                                                                                main_config["EFlagRobloxPlayerFlags"] = main_config.get("EFlagRobloxPlayerFlags", {})
                                                                                                main_config["EFlagRobloxStudioFlags"] = main_config.get("EFlagRobloxStudioFlags", {})
                                                                                                for i, v in js.items():
                                                                                                    if not ("EFlag" in i):
                                                                                                        if run_studio == True: main_config["EFlagRobloxStudioFlags"][i] = v
                                                                                                        else: main_config["EFlagRobloxPlayerFlags"][i] = v
                                                                                                    else: main_config[i] = v
                                                                                            if run_studio == True and "EFlagRobloxStudioFlags" in modified_flags_from_mod_scripts: modified_flags_from_mod_scripts.remove("EFlagRobloxStudioFlags")
                                                                                            elif "EFlagRobloxPlayerFlags" in modified_flags_from_mod_scripts: modified_flags_from_mod_scripts.remove("EFlagRobloxPlayerFlags")
                                                                                            saveSettings()
                                                                                    def saveFF(scri: str, js: dict, full=False):
                                                                                        if type(js) is dict:
                                                                                            if full == True: 
                                                                                                if run_studio == True: main_config["EFlagRobloxStudioFlags"] = js
                                                                                                else: main_config["EFlagRobloxPlayerFlags"] = js
                                                                                            else:
                                                                                                main_config["EFlagRobloxPlayerFlags"] = main_config.get("EFlagRobloxPlayerFlags", {})
                                                                                                main_config["EFlagRobloxStudioFlags"] = main_config.get("EFlagRobloxStudioFlags", {})
                                                                                                for i, v in js.items(): 
                                                                                                    if run_studio == True: main_config["EFlagRobloxStudioFlags"][i] = v
                                                                                                    else: main_config["EFlagRobloxPlayerFlags"][i] = v
                                                                                            filtered_fast_flags = {}
                                                                                            if run_studio == True and main_config.get("EFlagRobloxStudioFlags"):
                                                                                                for i, v in main_config.get("EFlagRobloxStudioFlags").items():
                                                                                                    if i and (not i.startswith("EFlag")): filtered_fast_flags[i] = v
                                                                                            elif run_studio == False and main_config.get("EFlagRobloxPlayerFlags"):
                                                                                                for i, v in main_config.get("EFlagRobloxPlayerFlags").items():
                                                                                                    if i and (not i.startswith("EFlag")): filtered_fast_flags[i] = v
                                                                                            handler.installFastFlags(filtered_fast_flags, debug=(main_config.get("EFlagEnableDebugMode") == True), endRobloxInstances=False, studio=run_studio, ixp=main_config.get("EFlagUseIXPFastFlagsMethod2")==True)
                                                                                            saveSettings()
                                                                                    def sendBloxstrapRPC(scri: str, info: dict, disableWebhook: bool=True): onBloxstrapMessage(info, disableWebhook)
                                                                                    def getDebugMode(scri: str): return (main_config.get("EFlagEnableDebugMode") == True)
                                                                                    def getConfiguration(scri: str, name: str="*"):
                                                                                        if type(name) is str:
                                                                                            mod_script_config = {}
                                                                                            config_path = os.path.join(mods_folder, "Mods", scri, f"Configuration_{user_folder_name}")
                                                                                            if os.path.exists(config_path):
                                                                                                try:
                                                                                                    with open(config_path, "r", encoding="utf-8") as f: mod_script_config = json.load(f)
                                                                                                except Exception as e: printDebugMessage("Invalid mod script configuration, returned blank.")
                                                                                            if name == "*": return mod_script_config
                                                                                            else: return mod_script_config.get(name)
                                                                                        else: return None
                                                                                    def setRobloxWindowTitle(scri: str, title: str):
                                                                                        if type(title) is str:
                                                                                            if connected_roblox_instance:
                                                                                                windows_opened = connected_roblox_instance.getWindowsOpened()
                                                                                                if len(windows_opened) > 0:
                                                                                                    for win in windows_opened: win.setWindowTitle(title)
                                                                                                else: raise Exception("No Roblox Windows found!")
                                                                                            else: raise Exception("Connected Roblox Instance is not found!")
                                                                                        else: raise Exception("Provided arguments are invalid!")
                                                                                    def setRobloxWindowIcon(scri: str, icon: str):
                                                                                        if type(icon) is str:
                                                                                            if connected_roblox_instance:
                                                                                                windows_opened = connected_roblox_instance.getWindowsOpened()
                                                                                                if len(windows_opened) > 0:
                                                                                                    for win in windows_opened: win.setWindowIcon(icon)
                                                                                                else: raise Exception("No Roblox Windows found!")
                                                                                            else: raise Exception("Connected Roblox Instance is not found!")
                                                                                        else: raise Exception("Provided arguments are invalid!")
                                                                                    def focusRobloxWindow(scri: str):
                                                                                        if connected_roblox_instance:
                                                                                            windows_opened = connected_roblox_instance.getWindowsOpened()
                                                                                            if len(windows_opened) > 0:
                                                                                                for win in windows_opened: win.focusWindow()
                                                                                            else: raise Exception("No Roblox Windows found!")
                                                                                        else: raise Exception("Connected Roblox Instance is not found!")
                                                                                    def getIfRobloxLaunched(scri: str): return roblox_launched_affect_mod_script == True
                                                                                    def getRobloxAppSettings(scri: str):
                                                                                        a = handler.getRobloxAppSettings()
                                                                                        return {
                                                                                            "success": a.get("success", False),
                                                                                            "loggedInUser": a.get("loggedInUser", {}),
                                                                                            "policyServiceResponse": a.get("policyServiceResponse", {}),
                                                                                            "outputDeviceGUID": a.get("outputDeviceGUID", None),
                                                                                            "robloxLocaleId": a.get("robloxLocaleId", "en_us"),
                                                                                            "appConfiguration": a.get("appConfiguration", {})
                                                                                        }
                                                                                    def changeRobloxWindowSizeAndPosition(scri: str, size_x: int, size_y: int, position_x: int, position_y: int):
                                                                                        if type(size_x) is int and type(size_y) is int and type(position_x) is int and type(position_y) is int:
                                                                                            if connected_roblox_instance:
                                                                                                windows_opened = connected_roblox_instance.getWindowsOpened()
                                                                                                if len(windows_opened) > 0:
                                                                                                    for win in windows_opened:
                                                                                                        win.setWindowPositionAndSize(size_x, size_y, position_x, position_y)
                                                                                                else: raise Exception("No Roblox Windows found!")
                                                                                            else: raise Exception("Connected Roblox Instance is not found!")
                                                                                        else: raise Exception("Provided arguments are invalid!")
                                                                                    def setConfiguration(scri: str, name: str="*", data=None):
                                                                                        if type(name) is str:
                                                                                            mod_script_config = {}
                                                                                            config_path = os.path.join(mods_folder, "Mods", scri, f"Configuration_{user_folder_name}")
                                                                                            if os.path.exists(config_path):
                                                                                                try:
                                                                                                    with open(config_path, "r", encoding="utf-8") as f: mod_script_config = json.load(f)
                                                                                                except Exception as e: printDebugMessage("Invalid Mod Script Configuration, returned blank.")
                                                                                            if name == "*":
                                                                                                if type(data) is dict:
                                                                                                    try:
                                                                                                        dumped = json.dumps(data)
                                                                                                        for i, v in data.items(): mod_script_config[i] = v
                                                                                                    except Exception as e: printDebugMessage(f"Something went wrong saving Mod Script Configuration requested by mod script {scri}.")
                                                                                                else: printDebugMessage(f"Something went wrong saving Mod Script Configuration requested by mod script {scri}.")
                                                                                            else:
                                                                                                try:
                                                                                                    dumped = json.dumps(data)
                                                                                                    mod_script_config[name] = data
                                                                                                except Exception as e: printDebugMessage(f"Something went wrong saving Mod Script Configuration requested by mod script {scri}.")
                                                                                            with open(config_path, "w", encoding="utf-8") as f:  json.dump(mod_script_config, f, indent=4)
                                                                                        else: return None
                                                                                    def unzipFile(scri: str, path: str, output: str, look_for: list=[], export_out: list=[], either: bool=False, check: bool=True):
                                                                                        path = str(path)
                                                                                        path = path.replace("../", "").replace("..\\", "")
                                                                                        path = os.path.join(mods_folder, "Mods", scri, path)
                                                                                        output = str(output)
                                                                                        output = output.replace("../", "").replace("..\\", "")
                                                                                        output = os.path.join(mods_folder, "Mods", scri, output)
                                                                                        if path.startswith(os.path.join(mods_folder, "Mods", scri)) and output.startswith(os.path.join(mods_folder, "Mods", selected_mod_scriptt)): return pip_class.unzipFile(path, output, look_for=look_for, export_out=export_out, either=either, check=check)
                                                                                    def sendDiscordWebhookMessage(scri: str, title: str="Message from Mod Script", description: str=None, color: int=0, fields: list=[], image=f"{main_host}/Images/DiscordIcon.png"):
                                                                                        if main_config.get("EFlagUseDiscordWebhook") == True:
                                                                                            for i in fields: 
                                                                                                if not (type(i) is generated_api_instances[scri].DiscordWebhookField): return False
                                                                                            if main_config.get("EFlagDiscordWebhookURL"):
                                                                                                generated_body = {
                                                                                                    "content": f"<@{main_config.get('EFlagDiscordWebhookUserId')}>",
                                                                                                    "embeds": [
                                                                                                        {
                                                                                                            "title": title,
                                                                                                            "description": description or "",
                                                                                                            "color": color,
                                                                                                            "fields": [i.convert() for i in fields],
                                                                                                            "author": { "name": "OrangeBlox", "icon_url": f"{main_host}/Images/DiscordIcon.png" },
                                                                                                            "thumbnail": { "url": image },
                                                                                                            "footer": { "text": ts(f"Made by @EfazDev | PID: {connected_roblox_instance.pid}") if main_config.get("EFlagDiscordWebhookShowPidInFooter") == True and connected_roblox_instance and connected_roblox_instance.pid else ts("Made by @EfazDev"), "icon_url": "https://cdn.efaz.dev/cdn/png/logo.png" },
                                                                                                            "timestamp": datetime.datetime.now(tz=datetime.UTC).strftime('%Y-%m-%dT%H:%M:%S.000Z')
                                                                                                        }
                                                                                                    ],
                                                                                                    "attachments": []
                                                                                                }
                                                                                                try:
                                                                                                    def sen():
                                                                                                        waitForInternet()
                                                                                                        req = requests.post(main_config.get("EFlagDiscordWebhookURL"), data=generated_body)
                                                                                                        if req.ok: printDebugMessage("Successfully sent webhook! Event: onModScript")
                                                                                                        else: printErrorMessage(f"There was an issue sending your webhook message. Status Code: {req.status_code}")
                                                                                                    if pip_class.getIfConnectedToInternet() == True: sen()
                                                                                                    else: threading.Thread(target=sen, daemon=True).start()
                                                                                                except Exception as e: printDebugMessage(f"There was an issue sending your webhook message. Exception: \n{trace()}")
                                                                                    def startPrepareRoblox(scri: str): 
                                                                                        if not (roblox_launched_affect_mod_script == True): prepareRobloxClient()
                                                                                    def current_ver_func(scri: str): return current_version
                                                                                    def modScriptName(scri: str): 
                                                                                        cur_mod_manifest = generateModsManifest()
                                                                                        return cur_mod_manifest.get(scri).get("name") if cur_mod_manifest.get(scri) and cur_mod_manifest.get(scri).get("name") else None
                                                                                    def modScriptId(scri: str): return scri
                                                                                    def modScriptVersion(scri: str): 
                                                                                        cur_mod_manifest = generateModsManifest()
                                                                                        return cur_mod_manifest.get(scri).get("version") if cur_mod_manifest.get(scri) and cur_mod_manifest.get(scri).get("version") else None
                                                                                    def getConnectedUserInfo(scri: str): return connected_user_info
                                                                                    def getIfConnectedToGame(scri: str): return connected_to_game
                                                                                    def getCurrentPlaceInfo(scri: str): return current_place_info
                                                                                    def createAppLock(scri: str, name: str="ScriptLock"):
                                                                                        name = os.path.basename(name)
                                                                                        if name == "Configuration": return
                                                                                        script_lock_key = generateFileKey(name, dire=os.path.join(mods_folder, "Mods", scri))
                                                                                        if os.path.exists(script_lock_key):
                                                                                            with open(script_lock_key, "r", encoding="utf-8") as f: pid_str = f.read()
                                                                                            if safeConvertNumber(pid_str) and pip_class.getIfProcessIsOpened(pid=pid_str):
                                                                                                return False
                                                                                            else:
                                                                                                with open(script_lock_key, "w", encoding="utf-8") as f: f.write(str(os.getpid()))
                                                                                                return True
                                                                                        else: 
                                                                                            with open(script_lock_key, "w", encoding="utf-8") as f: f.write(str(os.getpid()))
                                                                                            return True
                                                                                    def getIfModIsEnabled(scri: str, mod_name: str): 
                                                                                        cur_mod_manifest = generateModsManifest()
                                                                                        if cur_mod_manifest.get(mod_name) and cur_mod_manifest.get(mod_name).get("enabled") == True: return True
                                                                                        return False
                                                                                    def enableMod(scri: str, mod_name: str): 
                                                                                        cur_mod_manifest = generateModsManifest()
                                                                                        if not (main_config.get("EFlagEnabledMods") and type(main_config.get("EFlagEnabledMods")) is dict): main_config["EFlagEnabledMods"] = {}
                                                                                        if cur_mod_manifest.get(mod_name): main_config["EFlagEnabledMods"][mod_name] = True
                                                                                        saveSettings()
                                                                                    def disableMod(scri: str, mod_name: str): 
                                                                                        cur_mod_manifest = generateModsManifest()
                                                                                        if not (main_config.get("EFlagEnabledMods") and type(main_config.get("EFlagEnabledMods")) is dict): main_config["EFlagEnabledMods"] = {}
                                                                                        if cur_mod_manifest.get(mod_name): main_config["EFlagEnabledMods"][mod_name] = False
                                                                                        saveSettings()
                                                                                    def getCurrentRobloxPid(scri: str): 
                                                                                        return connected_roblox_instance and connected_roblox_instance.pid
                                                                                    def getLatestRobloxVersion(scri: str, channel: str="LIVE"):
                                                                                        return handler.getLatestClientVersion(studio=run_studio==True, channel=channel, token=createDownloadToken(run_studio==True))
                                                                                    def getLatestOppositeRobloxVersion(scri: str, channel: str="LIVE"):
                                                                                        return handler.getLatestClientVersion(studio=not run_studio==True, channel=channel, token=createDownloadToken(not run_studio==True))
                                                                                    def getRobloxThumbnailURLl(scri: str, studio: bool=None):
                                                                                        return getRobloxThumbnailURL(studio)

                                                                                    defined_func = {
                                                                                        "generateModsManifest": generateModsManifest,
                                                                                        "displayNotification": displayNotification,
                                                                                        "getRobloxLogFolderSize": getRobloxLogFolderSize,
                                                                                        "sendBloxstrapRPC": sendBloxstrapRPC,
                                                                                        "unzipFile": unzipFile,
                                                                                        "changeRobloxWindowSizeAndPosition": changeRobloxWindowSizeAndPosition,
                                                                                        "setRobloxWindowTitle": setRobloxWindowTitle,
                                                                                        "setRobloxWindowIcon": setRobloxWindowIcon,
                                                                                        "getRobloxAppSettings": getRobloxAppSettings,
                                                                                        "focusRobloxWindow": focusRobloxWindow,
                                                                                        "getIfRobloxLaunched": getIfRobloxLaunched,
                                                                                        "sendDiscordWebhookMessage": sendDiscordWebhookMessage,
                                                                                        "getLatestOppositeRobloxVersion": getLatestOppositeRobloxVersion,
                                                                                        "getLatestRobloxVersion": getLatestRobloxVersion,
                                                                                        "reprepareRoblox": startPrepareRoblox,
                                                                                        "enableMod": enableMod,
                                                                                        "disableMod": disableMod,
                                                                                        "getIfModIsEnabled": getIfModIsEnabled,
                                                                                        "getFastFlagConfiguration": getFF,
                                                                                        "setFastFlagConfiguration": setFF,
                                                                                        "saveFastFlagConfiguration": saveFF,
                                                                                        "getMainConfiguration": getMainConf,
                                                                                        "setMainConfiguration": setMainConf,
                                                                                        "saveMainConfiguration": saveMainConf,
                                                                                        "getDebugMode": getDebugMode,
                                                                                        "getConfiguration": getConfiguration,
                                                                                        "setConfiguration": setConfiguration,
                                                                                        "getModScriptId": modScriptId,
                                                                                        "getName": modScriptName,
                                                                                        "getVersion": modScriptVersion,
                                                                                        "getConnectedUserInfo": getConnectedUserInfo,
                                                                                        "getIfConnectedToGame": getIfConnectedToGame,
                                                                                        "getCurrentPlaceInfo": getCurrentPlaceInfo,
                                                                                        "createAppLock": createAppLock,
                                                                                        "getCurrentRobloxPid": getCurrentRobloxPid,
                                                                                        "getRobloxThumbnailURL": getRobloxThumbnailURLl,
                                                                                        "about": current_ver_func
                                                                                    }
                                                                                    undefined_func = {
                                                                                        "endRoblox": handler.endRobloxStudio if run_studio==True else handler.endRoblox,
                                                                                        "endOppositeRoblox": handler.endRoblox if run_studio==True else handler.endRobloxStudio,
                                                                                        "getIfRobloxIsOpen": handler.getIfRobloxStudioIsOpen if run_studio==True else handler.getIfRobloxIsOpen,
                                                                                        "getInstalledRobloxVersion": handler.getCurrentStudioClientVersion if run_studio==True else handler.getCurrentClientVersion,
                                                                                        "getOppositeInstalledRobloxVersion": handler.getCurrentClientVersion if run_studio==True else handler.getCurrentStudioClientVersion,
                                                                                        "getRobloxInstallFolder": handler.getRobloxInstallFolder,
                                                                                        "getLatestRobloxPid": handler.getLatestOpenedRobloxStudioPid if run_studio==True else handler.getLatestOpenedRobloxPid,
                                                                                        "getOpenedRobloxPids": handler.getOpenedRobloxStudioPids if run_studio==True else handler.getOpenedRobloxPids,
                                                                                        "getIfOSSupported": pip_class.osSupported,
                                                                                        "getIfPythonSupported": pip_class.pythonSupported,
                                                                                        "getIfConnectedToInternet": pip_class.getIfConnectedToInternet,
                                                                                        "getIf32BitWindows": pip_class.getIf32BitWindows,
                                                                                        "getRequest": requests.get,
                                                                                        "postRequest": requests.post,
                                                                                        "deleteRequest": requests.delete,
                                                                                    }
                                                                                    func_list = dict(defined_func)
                                                                                    func_list.update(undefined_func)
                                                                                    
                                                                                    if not (api_handled_requests.get(i) == True):
                                                                                        splited_id = i.split("|")
                                                                                        if splited_id[1] == generated_secret_keys[splited_id[0]]:
                                                                                            if v and func_list.get(v.requested):
                                                                                                if v and v.fulfilled == False:
                                                                                                    try:
                                                                                                        if undefined_func.get(v.requested):
                                                                                                            if type(v.args) is list: val = func_list.get(v.requested)(*(v.args))
                                                                                                            elif type(v.args) is dict: val = func_list.get(v.requested)(**(v.args))
                                                                                                            else: val = func_list.get(v.requested)()
                                                                                                        else:
                                                                                                            if type(v.args) is list: val = func_list.get(v.requested)(splited_id[0], *(v.args))
                                                                                                            elif type(v.args) is dict: val = func_list.get(v.requested)(splited_id[0], **(v.args))
                                                                                                            else: val = func_list.get(v.requested)()
                                                                                                        if v:
                                                                                                            if not type(val) is None: v.value = val
                                                                                                            v.success = True
                                                                                                            v.code = 0
                                                                                                    except Exception as e:
                                                                                                        if v:
                                                                                                            v.success = False
                                                                                                            v.code = 1
                                                                                                    if v: v.fulfilled = True
                                                                                                    orangeapi_modules[selected_mod_scriptt].requested_functions[i] = v
                                                                                                    api_handled_requests[i] = True
                                                                                            else:
                                                                                                if v:
                                                                                                    v.value = None
                                                                                                    v.success = False
                                                                                                    v.code = 3
                                                                                                    v.fulfilled = True
                                                                                                    orangeapi_modules[selected_mod_scriptt].requested_functions[i] = v
                                                                                                    api_handled_requests[i] = True
                                                                                        else:
                                                                                            if v:
                                                                                                v.value = None
                                                                                                v.success = False
                                                                                                v.code = 7
                                                                                                v.fulfilled = True
                                                                                                orangeapi_modules[selected_mod_scriptt].requested_functions[i] = v
                                                                                                api_handled_requests[i] = True
                                                                                    else:
                                                                                        if v:
                                                                                            v.value = None
                                                                                            v.success = False
                                                                                            v.code = 6
                                                                                            v.fulfilled = True
                                                                                            orangeapi_modules[selected_mod_scriptt].requested_functions[i] = v
                                                                                            api_handled_requests[i] = True
                                                                                else:
                                                                                    if v and v.fulfilled == False:
                                                                                        v.value = None
                                                                                        v.success = False
                                                                                        v.code = 2
                                                                                        v.fulfilled = True
                                                                                        orangeapi_modules[selected_mod_scriptt].requested_functions[i] = v
                                                                                        api_handled_requests[i] = True
                                                                                        printDebugMessage(f"This mod script ({selected_mod_scriptt}) is requesting use of a function ({v.requested}) that is not permitted. Please check Manifest.json and verify using the Mod Manager!")
                                                                            except Exception as e:
                                                                                if v:
                                                                                    v.value = None
                                                                                    v.success = False
                                                                                    v.code = 4
                                                                                    v.fulfilled = True
                                                                                    orangeapi_modules[selected_mod_scriptt].requested_functions[i] = v
                                                                                    api_handled_requests[i] = True
                                                                                    printDebugMessage(f"Something went wrong with pinging the mod script {selected_mod_scriptt}: \n{trace()}")
                                                            except Exception as e:
                                                                resulting_err = trace()
                                                                if "dictionary changed size during iteration" in resulting_err:
                                                                    if main_config.get("EFlagModScriptRequestTooFastMessage") == True: printDebugMessage("Mod Script is requesting data too fast!")
                                                                else:
                                                                    printDebugMessage(f"Error from Mod Script module: \n{resulting_err}")
                                                                    printErrorMessage(f"Ended accepting requests from Mod Scripts ({selected_mod_scriptt}) due to an issue. | Code: 1")
                                                                    return
                                                            time.sleep(main_config.get("EFlagModScriptAPIRefreshTime", 0.05))
                                                    def setPythonAPIs(selected_mod_scripttt, apr_li):
                                                        # Set and Handle Printing Functions
                                                        def handlePrint(mes): printMainMessage(f"[MOD SCRIPT]: {mes}")
                                                        def empty_str(*args, **kwargs): return ""
                                                        def empty(*args, **kwargs): return None
                                                        def open_config(*args, **kwargs):
                                                            mod_script_config = {}
                                                            config_path = os.path.join(mods_folder, "Mods", selected_mod_scripttt, f"Configuration_{user_folder_name}")
                                                            if os.path.exists(config_path):
                                                                try:
                                                                    with open(config_path, "r", encoding="utf-8") as f: mod_script_config = json.load(f)
                                                                except Exception as e: printDebugMessage("Invalid Mod Script Configuration, returned blank.")
                                                            return mod_script_config 
                                                        if not (("grantMaximumAbility" in apr_li)):
                                                            setattr(mod_script_modules[selected_mod_scripttt], "print", handlePrint)
                                                            setattr(mod_script_modules[selected_mod_scripttt], "input", empty_str)
                                                            setattr(mod_script_modules[selected_mod_scripttt], "write", empty)
                                                            if not (("grantFileEditing" in apr_li) or (handler.roblox_event_info.get("grantFileEditing", {"free": False}).get("free") == True)): setattr(mod_script_modules[sel_mod], "open", open_config)
                                                            setattr(mod_script_modules[selected_mod_scripttt], "exec", None)
                                                            setattr(mod_script_modules[selected_mod_scripttt], "eval", None)
                                                            setattr(mod_script_modules[selected_mod_scripttt], "setattr", empty)
                                                            setattr(mod_script_modules[selected_mod_scripttt], "__import__", empty)

                                                    # Launch API
                                                    threading.Thread(target=checkGeneratedInstances, daemon=True, args=[sel_mod, "OrangeAPI"]).start()
                                                    threading.Thread(target=setPythonAPIs, daemon=True, args=[sel_mod, list(approved_items_list)]).start()
                                                    threading.Thread(target=handleRequests, daemon=True, args=[sel_mod, list(approved_items_list)]).start()
                                                    printDebugMessage(f"Launched OrangeAPI v{OrangeAPI.current_version['version']}!")
                                                    
                                                    # Launch Script
                                                    printDebugMessage("Starting Mod Script..")
                                                    spec.loader.exec_module(mod_script_modules[sel_mod])
                                                    printSuccessMessage("Successfully connected to script!")
                                                except Exception as e:
                                                    printDebugMessage(f"Error from Mod Script module: \n{trace()}")
                                                    printErrorMessage("Something went wrong while connecting to the Mod Script script!")
                                            else:
                                                printErrorMessage("Please reverify this mod script in order to continue!")
                                                resb = continueToModsManager(reverify_mod_script=sel_mod)
                                                if resb == 5: return
                                                else: mod_manifest = generateModsManifest().get(sel_mod); s(sel_mod)
                                        s(str(sel_mo))
                                    else:
                                        if mod_manifest["mod_script_supports"] > current_version["version"]: printYellowMessage(f"This mod script is not supported. Please update to OrangeBlox v{mod_manifest['mod_script_supports']}")
                                        elif mod_manifest["mod_script_supports_operating_system"] == False:
                                            if main_os == "Darwin": printYellowMessage(f"This mod script is only supported for Windows!")
                                            elif main_os == "Windows": printYellowMessage(f"This mod script is only supported for macOS!")
                                            else: printYellowMessage(f"This mod script is only supported for macOS or Windows!")
                                        else:
                                            printYellowMessage(f"This mod script has reached their end support! Creator Note:")
                                            printYellowMessage(mod_manifest["mod_script_end_support_reasoning"])
                                else: printErrorMessage("Unable to find mod script under manifest.")
        if not (main_config.get("EFlagDisableModScriptsAccess", False) == True):
            mod_script_thread = threading.Thread(target=loadModScripts, daemon=True)
            mod_script_thread.start()
            if skip_modification_mode == False: mod_script_thread.join()

        # Extra Functions
        def unfriendCheckLoop():
            alleged_path = generateFileKey("UnfriendCheckLoopLock")
            if os.path.exists(alleged_path):
                with open(alleged_path, "r") as f: pid_str = f.read()
                if safeConvertNumber(pid_str) and pip_class.getIfProcessIsOpened(pid=pid_str):
                    while os.path.exists(alleged_path) and pip_class.getIfProcessIsOpened(pid=pid_str): time.sleep(0.5)
                    return unfriendCheckLoop()
                else:
                    with open(alleged_path, "w", encoding="utf-8") as f: f.write(str(os.getpid()))
            else: 
                with open(alleged_path, "w", encoding="utf-8") as f: f.write(str(os.getpid()))
            printDebugMessage("Starting Unfriend Detector Loop..")
            while True:
                unfriended_friends = []
                blank_user_ids = 0
                friend_check_id = main_config.get('EFlagRobloxUnfriendCheckUserID', 1)
                try:
                    reached_end = False
                    friend_list_json = {"data": []}
                    query = {"limit": "50", "findFriendsType": "0"}
                    while reached_end == False:
                        try:
                            if main_config.get("EFlagUseEfazDevAPI") == True: 
                                if query.get("limit"): query.pop("limit")
                                if query.get("findFriendsType"): query.pop("findFriendsType")
                                friend_list_req = requests.get(f"https://api.efaz.dev/api/roblox/user-friends-find/{friend_check_id}/50" + requests.format_params(query), timeout=5)
                                if friend_list_req and friend_list_req.json: friend_list_req.json = friend_list_req.json.get("response")
                            else: friend_list_req = requests.get(f"https://friends.roblox.com/v1/users/{friend_check_id}/friends/find" + requests.format_params(query), timeout=5, cookies=createCookieHeader())
                            friend_req_json = friend_list_req.json
                            if friend_list_req.ok and friend_req_json.get("PageItems"):
                                friend_list_json["data"] += friend_req_json.get("PageItems")
                                if friend_req_json.get("NextCursor"): query["cursor"] = friend_req_json.get("NextCursor")
                                else: reached_end = True
                        except Exception as e: printDebugMessage(f"There was an error on getting friends! Error: {str(e)}")
                        time.sleep(5)
                    if friend_list_req.ok:
                        last_pinged_friend_list = {}
                        if os.path.exists(os.path.join(cur_path, generateFileKey("CachedFriendsList", ext=".json"))):
                            with open(os.path.join(cur_path, generateFileKey("CachedFriendsList", ext=".json")), "r", encoding="utf-8") as f: last_pinged_friend_list = json.load(f)
                        if last_pinged_friend_list.get(str(friend_check_id)):
                            for i in last_pinged_friend_list.get(str(friend_check_id)):
                                found_friend = False
                                for e in friend_list_json.get("data"):
                                    if e["id"] == i["id"]: found_friend = True; break
                                if found_friend == False: unfriended_friends.append(i)
                            reached_end2 = False
                            while reached_end2 == False:
                                try:
                                    user_ids = []
                                    for i in unfriended_friends: 
                                        if not (i.get("id") == -1): user_ids.append(i.get("id"))
                                        else: blank_user_ids += 1
                                    if len(user_ids) > 150:
                                        chunked = []
                                        for e in range(0, len(user_ids), 150): chunked.append(user_ids[e:e + 150])
                                        unfriended_friends = []
                                        for e in chunked:
                                            reached_end3 = False
                                            while reached_end3 == False:
                                                user_info_req = requests.post(f"https://users.roblox.com/v1/users", {"userIds": e, "excludeBannedUsers": False}, timeout=5, cookies=createCookieHeader())
                                                if user_info_req.ok: unfriended_friends += user_info_req.json.get("data"); reached_end3 = True
                                                time.sleep(1)
                                        reached_end2 = True
                                    else:
                                        user_info_req = requests.post(f"https://users.roblox.com/v1/users", {"userIds": user_ids, "excludeBannedUsers": False}, timeout=5, cookies=createCookieHeader())
                                        if user_info_req.ok: unfriended_friends = user_info_req.json.get("data"); reached_end2 = True
                                        time.sleep(1)
                                except Exception as e: pass
                            last_pinged_friend_list[str(friend_check_id)] = friend_list_json.get("data")
                        else: last_pinged_friend_list[str(friend_check_id)] = friend_list_json.get("data")
                        with open(os.path.join(cur_path, generateFileKey("CachedFriendsList", ext=".json")), "w", encoding="utf-8") as f: json.dump(last_pinged_friend_list, f, indent=4)
                except Exception as e:
                    printDebugMessage(f"Unable to fetch friends list! Exception: \n{trace()}")
                    unfriended_friends = []
                if len(unfriended_friends) > 0:
                    for i in unfriended_friends:
                        if roblox_launched_affect_mod_script == True: displayNotification(ts("Unfriend Detected!"), ts(f"Oh! @{i['name']} has unfriended you! ;("))
                        else: displayNotification(ts("Unfriend Detected!"), ts(f"Oh! @{i['name']} has unfriended you while you were away! ;("))
                        printDebugMessage(f"Unable to find friend @{i['name']} in list! User must be unfriended!")
                        time.sleep(1)
                time.sleep(main_config.get("EFlagRobloxUnfriendCheckCooldown", 600))
        def setRuntimeIconLoop():
            while True:
                if run_studio == True: 
                    if main_config.get("EFlagEnableChangeBrandIcons") == True: brand_fold = os.path.join(mods_folder, "RobloxStudioBrand", main_config.get('EFlagSelectedBrandLogo2'))
                    else: brand_fold = os.path.join(mods_folder, "RobloxStudioBrand", "Original")
                else:
                    if main_config.get("EFlagEnableChangeBrandIcons") == True: brand_fold = os.path.join(mods_folder, "RobloxBrand", main_config.get('EFlagSelectedBrandLogo'))
                    else: brand_fold = os.path.join(mods_folder, "RobloxBrand", "Original")
                icon = os.path.join(brand_fold, "AppIcon.ico")
                if connected_roblox_instance:
                    windows = connected_roblox_instance.getWindowsOpened()
                    if windows:
                        for i in windows:
                            if os.path.exists(icon): i.setWindowIcon(icon)
                            else: printDebugMessage(f"Setting Windows Icon on Roblox Runtime with an icon that doesn't exist?")
                time.sleep(2)
        def generateEmbedField(name, value, inline=True): return {"name": name, "value": str(value), "inline": inline}
        def generateDiscordPayload(title, color, fields, thumbnail_url): return {"content": f"<@{main_config.get('EFlagDiscordWebhookUserId')}>", "embeds": [{"title": title, "color": color, "fields": fields, "author": { "name": "OrangeBlox", "icon_url": f"{main_host}/Images/DiscordIcon.png" }, "thumbnail": { "url": thumbnail_url }, "footer": { "text": ts(f"Made by @EfazDev | PID: {connected_roblox_instance.pid}") if main_config.get("EFlagDiscordWebhookShowPidInFooter") == True and connected_roblox_instance and connected_roblox_instance.pid else ts("Made by @EfazDev"), "icon_url": "https://cdn.efaz.dev/cdn/png/logo.png" }, "timestamp": datetime.datetime.now(tz=datetime.UTC).strftime('%Y-%m-%dT%H:%M:%S.000Z')}], "attachments": []}
        def getRobloxThumbnailURL(studio: bool=None):
            if studio == None: studio = run_studio
            thumbnail_url = f"{main_host}/Images/RobloxStudioLogo.png" if studio == True else f"{main_host}/Images/RobloxLogo.png"
            selected_brand = main_config.get(f"EFlagSelectedBrandLogo{'2' if studio == True else ''}", '')
            if selected_brand in special_logo_mods["studio" if studio == True else "reg"]:
                thumbnail_url = f"{main_host}/Mods/Roblox{'Studio' if studio == True else ''}Brand/{selected_brand}/{'AppIcon' if studio == True else 'RobloxTilt'}.png"
            return thumbnail_url
        def clearDiscordRPC():
            if main_config.get("EFlagEnableDiscordRPC") == True: pass
        def sendDiscordWebhook(webhook_json, name):
            def sen():
                waitForInternet()
                req = requests.post(main_config.get("EFlagDiscordWebhookURL"), data=webhook_json)
                if req.ok: printDebugMessage(f"Successfully sent webhook! Event: {name}")
                else: printErrorMessage(f"There was an issue sending your webhook message. Status Code: {req.status_code}")
            if pip_class.getIfConnectedToInternet() == True: sen()
            else: threading.Thread(target=sen, daemon=True).start()
        if main_config.get("EFlagRobloxUnfriendCheckEnabled") == True: threading.Thread(target=unfriendCheckLoop, daemon=True).start()
        if main_config.get("EFlagReplaceRobloxRuntimeIconWithModIcon") == True and main_os == "Windows": threading.Thread(target=setRuntimeIconLoop, daemon=True).start()

        # Roblox Ready Message
        if run_studio == True:
            printSuccessMessage("Done! Roblox Studio is ready!")
            printWarnMessage("--- Running Roblox Studio ---")
        else:
            printSuccessMessage("Done! Roblox is ready!")
            printWarnMessage("--- Running Roblox ---")
        if waitForInternet() == True: printWarnMessage("-----------")

        # Activity Tracking Functions
        if run_studio == True:
            def onGameJoined(info):
                global connected_to_game
                connected_to_game = True
                generated_location = "Unknown Location"
                if info.get("ip"):
                    printDebugMessage(f"Roblox IP Address Detected! IP: {info.get('ip')}")
                    allocated_roblox_ip = info.get("ip")
                    server_info_res = requests.get(f"https://ipinfo.io/{allocated_roblox_ip}/json")
                    if server_info_res.ok:
                        server_info_json = server_info_res.json
                        if server_info_json.get("city") and server_info_json.get("country"):
                            if not (server_info_json.get("region") == None or server_info_json.get("region") == ""): generated_location = f"{server_info_json['city']}, {server_info_json['region']}, {server_info_json['country']}"
                            else: generated_location = f"{server_info_json['city']}, {server_info_json['country']}"
                        else:
                            if main_config.get("EFlagEnableDebugMode"): printDebugMessage(server_info_res.text)
                            printDebugMessage("Failed to get server information: IP Request resulted with no information.")
                    else:
                        if main_config.get("EFlagEnableDebugMode"): printDebugMessage(server_info_res.text)
                        printDebugMessage("Failed to get server information: IP Request Rejected.")

                    if main_config.get("EFlagNotifyServerLocation") == True:
                        printSuccessMessage(f"Roblox is currently connecting to a studio server in: {generated_location} [{allocated_roblox_ip}]!")
                        displayNotification(ts("Joining Studio Server"), ts(f"You have connected to a studio server from {generated_location}!"))
                        printDebugMessage("Sent Notification to Bootstrap for Notification Center shipping!")

                global current_place_info
                global connected_user_info
                if not connected_user_info:
                    sss = handler.getRobloxAppSettings()
                    if sss.get("name") and sss.get("id"): connected_user_info = {"name": sss.get("name"), "id": sss.get("id"), "display": sss.get("displayName")}
                if current_place_info:
                    if generated_location: current_place_info["server_location"] = generated_location
                    if current_place_info.get('place_identifier') and safeConvertNumber(current_place_info.get('place_identifier')):
                        current_place_info["placeId"] = int(current_place_info.get('place_identifier'))
                        if main_config.get("EFlagUseEfazDevAPI") == True: 
                            generated_universe_id_res = requests.get(f"https://api.efaz.dev/api/roblox/universeId/{current_place_info.get('place_identifier')}", loop_429=main_config.get("EFlagEnableLoop429Requests")==True)
                            if generated_universe_id_res and generated_universe_id_res.json: generated_universe_id_res.json = generated_universe_id_res.json.get("response")
                        else: generated_universe_id_res = requests.get(f"https://apis.roblox.com/universes/v1/places/{current_place_info.get('place_identifier')}/universe", loop_429=main_config.get("EFlagEnableLoop429Requests")==True, cookies=createCookieHeader())
                        if generated_universe_id_res.ok:
                            generated_universe_id_json = generated_universe_id_res.json
                            if generated_universe_id_json and not (generated_universe_id_json.get("universeId") == None):
                                if current_place_info: current_place_info["universeId"] = generated_universe_id_json.get("universeId")
                            else: current_place_info = None
                        else: current_place_info = None
                    else:
                        current_place_info["placeId"] = None
                        current_place_info["universeId"] = -100
                    if current_place_info:
                        universeId = current_place_info.get('universeId')
                        if universeId == -100:
                            generated_thumbnail_api_res = PyKits.InstantRequestJSONResponse({ "data": [] })
                            generated_place_api_res = PyKits.InstantRequestJSONResponse({"data": [
                                {
                                    "name": os.path.basename(current_place_info.get('place_identifier', '')),
                                    "id": None,
                                    "universeId": -100,
                                    "description": ""
                                }
                            ]})
                            generated_universe_api_res = PyKits.InstantRequestJSONResponse({"data": [
                                {
                                    "name": os.path.basename(current_place_info.get('place_identifier', '')),
                                    "id": None,
                                    "rootPlaceName": os.path.basename(current_place_info.get('place_identifier', '')),
                                    "rootPlaceId": None,
                                    "creator": {
                                        "id": 0,
                                        "name": "Local File",
                                        "type": "User",
                                        "isRNVAccount": True,
                                        "hasVerifiedBadge": False
                                    }
                                }
                            ]})
                        else:
                            if main_config.get("EFlagUseEfazDevAPI") == True: 
                                generated_thumbnail_api_res = requests.get(f"https://api.efaz.dev/api/roblox/game-thumbnail/{universeId}", loop_429=main_config.get("EFlagEnableLoop429Requests")==True)
                                generated_place_api_res = requests.get(f"https://api.efaz.dev/api/roblox/places-in-universe/{universeId}", loop_429=main_config.get("EFlagEnableLoop429Requests")==True)
                                generated_universe_api_res = requests.get(f"https://api.efaz.dev/api/roblox/game-info/{universeId}", loop_429=main_config.get("EFlagEnableLoop429Requests")==True)
                                if generated_thumbnail_api_res and generated_thumbnail_api_res.json: generated_thumbnail_api_res.json = generated_thumbnail_api_res.json.get("response")
                                if generated_place_api_res and generated_place_api_res.json: generated_place_api_res.json = generated_place_api_res.json.get("response")
                                if generated_universe_api_res and generated_universe_api_res.json: generated_universe_api_res.json = generated_universe_api_res.json.get("response")
                            else: 
                                generated_thumbnail_api_res = requests.get(f"https://thumbnails.roblox.com/v1/games/icons?universeIds={universeId}&returnPolicy=PlaceHolder&size=512x512&format=Png&isCircular=false", loop_429=main_config.get("EFlagEnableLoop429Requests")==True, cookies=createCookieHeader())
                                generated_place_api_res = requests.get(f"https://develop.roblox.com/v1/universes/{universeId}/places?isUniverseCreation=false&limit=50&sortOrder=Asc", loop_429=main_config.get("EFlagEnableLoop429Requests")==True, cookies=createCookieHeader())
                                generated_universe_api_res = requests.get(f"https://games.roblox.com/v1/games?universeIds={universeId}", loop_429=main_config.get("EFlagEnableLoop429Requests")==True, cookies=createCookieHeader())
                        if generated_thumbnail_api_res.ok and generated_place_api_res.ok and generated_universe_api_res.ok:
                            generated_thumbnail_api_json = generated_thumbnail_api_res.json
                            generated_place_api_json = generated_place_api_res.json
                            generated_universe_api_json = generated_universe_api_res.json
                            thumbnail_url = f"{main_host}/Images/AppIconRunStudio.png"
                            if generated_thumbnail_api_json.get("data"):
                                if len(generated_thumbnail_api_json.get("data")) > 0: thumbnail_url = generated_thumbnail_api_json.get("data")[0]["imageUrl"]
                            if current_place_info: current_place_info["thumbnail_url"] = thumbnail_url
                            if len(generated_place_api_json.get("data", [])) > 0 and len(generated_universe_api_json.get("data", [])) > 0:
                                generated_universe_api_json = generated_universe_api_json.get("data")[0]
                                place_info = {}
                                for place_under_experience in generated_place_api_json.get("data"):
                                    if current_place_info and str(place_under_experience.get("id")) == str(current_place_info.get("placeId")): place_info = place_under_experience
                                if current_place_info:
                                    if place_info:
                                        generated_universe_api_json["rootPlaceName"] = generated_universe_api_json["name"]
                                        for i in generated_universe_api_json.keys():
                                            if not place_info.get(i) and (not (i == "id" or i == "name" or i == "description" or i == "universeId")): place_info[i] = generated_universe_api_json[i]
                                        if current_place_info: current_place_info["place_info"] = place_info
                                try:
                                    if main_os == "Windows" and connected_roblox_instance:
                                        if main_config.get("EFlagShowRunningAccountNameInTitle") == True:
                                            windows_opened = connected_roblox_instance.getWindowsOpened()
                                            for i in windows_opened:
                                                if connected_user_info:
                                                    if main_config.get("EFlagShowDisplayNameInTitle") == True: i.setWindowTitle(ts(f"Roblox Studio - Opened @{connected_user_info.get('name', 'Unknown')} [ID: {connected_user_info.get('id', 'Unknown')}] as {connected_user_info.get('display', 'Unknown')}!"))
                                                    else: i.setWindowTitle(ts(f"Roblox Studio - Opened @{connected_user_info.get('name', 'Unknown')} [ID: {connected_user_info.get('id', 'Unknown')}]!"))
                                        elif main_config.get("EFlagShowRunningGameInTitle") == True:
                                            windows_opened = connected_roblox_instance.getWindowsOpened()
                                            for i in windows_opened: i.setWindowTitle(ts(f"Roblox Studio - Opened {place_info.get('name', 'Unknown')}"))
                                except Exception as e: printDebugMessage(f"Something went wrong setting the Window Title: \n{trace()}")
                                try:
                                    start_time = int(datetime.datetime.now(tz=datetime.UTC).timestamp())
                                    if main_config.get("EFlagSetDiscordRPCStart") and (type(main_config.get("EFlagSetDiscordRPCStart")) is float or type(main_config.get("EFlagSetDiscordRPCStart")) is int): start_time = main_config.get("EFlagSetDiscordRPCStart")
                                    if current_place_info: current_place_info["start_time"] = start_time
                                    if main_config.get("EFlagEnableDiscordRPC") == True:
                                        # Handle User Thumbnail
                                        app_settings = handler.getRobloxAppSettings()
                                        logged_in_user: dict = app_settings.get("loggedInUser")
                                        if logged_in_user.get("name") and logged_in_user.get("id"):
                                            connected_user_info = {"name": logged_in_user.get("name"), "id": logged_in_user.get("id"), "display": logged_in_user.get("displayName")}
                                            if main_config.get("EFlagShowUserProfilePictureInsteadOfLogo") == True:
                                                thumbnail_res = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={logged_in_user.get('id')}&size=100x100&format=Png&isCircular=false", loop_429=main_config.get("EFlagEnableLoop429Requests")==True, cookies=createCookieHeader())
                                                if thumbnail_res.ok:
                                                    thumbnail_json = thumbnail_res.json
                                                    if thumbnail_json and len(thumbnail_json.get("data", [])) > 0:
                                                        user_thumbnail = thumbnail_json["data"][0].get("imageUrl")
                                                        if user_thumbnail:
                                                            if connected_user_info:
                                                                connected_user_info["thumbnail"] = user_thumbnail
                                                                printSuccessMessage(f"Successfully loaded user thumbnail of @{logged_in_user.get('name')} [User ID: {logged_in_user.get('id')}]!")
                                                                printDebugMessage(f"Loaded thumbnail: {user_thumbnail}")
                                                        else: printDebugMessage(f"Failed to load thumbnail for @{logged_in_user.get('name')} [User ID: {logged_in_user.get('id')}]! Status Code: {thumbnail_res.status_code}")
                                                    else: printDebugMessage(f"Failed to load thumbnail for @{logged_in_user.get('name')} [User ID: {logged_in_user.get('id')}]! Status Code: {thumbnail_res.status_code}")
                                                else: printDebugMessage(f"Failed to load thumbnail for @{logged_in_user.get('name')} [User ID: {logged_in_user.get('id')}]! Status Code: {thumbnail_res.status_code}")
                                        
                                        def embed():
                                            try:
                                                global rpc
                                                global rpc_info
                                                global set_current_private_server_key

                                                err_count = 0
                                                loop_key = rpc.generate_loop_key()
                                                while True:
                                                    if (not rpc) or (not rpc.connected) or (not rpc.current_loop_id == loop_key): printDebugMessage("Invalid RPC Loop Information Detected! Broken Loop!"); break
                                                    if rpc_info == None: rpc_info = {}
                                                    playing_game_name = place_info['name']
                                                    if place_info['creator']['name'] == "Local File" and place_info['creator']['id'] == 0: creator_name = ts(f"Opened as Local File!")
                                                    else:
                                                        creator_name = ts(f"Made by {'@' if place_info['creator'].get('type') == 'User' else ''}{place_info['creator']['name']}").replace("✅", "")
                                                        if place_info.get("creator").get("hasVerifiedBadge") == True: creator_name = f"{creator_name} ✅!"
                                                        else: creator_name = f"{creator_name}!"
                                                    if not (place_info.get("rootPlaceId") == place_info.get("id")): playing_game_name = f"{playing_game_name} ({place_info['rootPlaceName']})"
                                                    formatted_info = {
                                                        "details": rpc_info.get("details") if rpc_info.get("details") else f"Editing {playing_game_name}",
                                                        "state": rpc_info.get("state") if rpc_info.get("state") else creator_name,
                                                        "start": rpc_info.get("start") if rpc_info.get("start") else start_time,
                                                        "stop": rpc_info.get("stop") if rpc_info.get("stop") and rpc_info.get("stop") > 1000 else None,
                                                        "large_image": rpc_info.get("large_image") if rpc_info.get("large_image") else thumbnail_url,
                                                        "large_text": rpc_info.get("large_text") if rpc_info.get("large_text") else playing_game_name,
                                                        "large_image_url": f"https://www.roblox.com",
                                                        "small_image": rpc_info.get("small_image") if rpc_info.get("small_image") else f"{main_host}/Images/AppIconRunStudioDiscord.png",
                                                        "small_image_url": f"{main_host}/",
                                                        "small_text": rpc_info.get("small_text") if rpc_info.get("small_text") else "OrangeBlox",
                                                        "buttons": [],
                                                        "state_url": None,
                                                        "launch_data": rpc_info.get("launch_data") if rpc_info.get("launch_data") else ""
                                                    }
                                                    if formatted_info["small_image"] == f"{main_host}/Images/AppIconRunStudioDiscord.png" and main_config.get("EFlagShowUserProfilePictureInsteadOfLogo") == True and connected_user_info and connected_user_info.get("thumbnail"): 
                                                        formatted_info["small_image"] = connected_user_info.get("thumbnail")
                                                    if formatted_info["small_text"] == "OrangeBlox" and main_config.get("EFlagShowUsernameInSmallImage") == True and connected_user_info and connected_user_info.get("display") and connected_user_info.get("name"): 
                                                        formatted_info["small_text"] = ts(f"Opened Studio as {connected_user_info.get('display')} (@{connected_user_info.get('name')})!")
                                                        formatted_info["buttons"].append({
                                                            "label": ts("Open User Page 🌐"), 
                                                            "url": f"https://www.roblox.com/users/{logged_in_user.get('id')}/profile"
                                                        })
                                                        formatted_info["smart_image_url"] = f"https://www.roblox.com/users/{logged_in_user.get('id')}/profile"
                                                    if place_info.get("creator").get("id") != 0 and current_place_info:
                                                        formatted_info["buttons"].append({
                                                            "label": ts("Open Game Page 🕹️"), 
                                                            "url": f"https://www.roblox.com/games/{current_place_info['placeId']}"
                                                        })
                                                        if formatted_info["state"] == creator_name and place_info and place_info['creator']['id'] > 0:
                                                            if place_info['creator'].get('type') == 'User': formatted_info["state_url"] = f"https://www.roblox.com/users/{place_info['creator']['id']}/profile"
                                                            else: formatted_info["state_url"] = f"https://www.roblox.com/groups/{place_info['creator']['id']}"
                                                        formatted_info["large_image_url"] = f"https://www.roblox.com/games/{current_place_info['placeId']}"
                                                    cur_time = int(datetime.datetime.now(tz=datetime.UTC).timestamp())
                                                    if formatted_info.get("stop") and formatted_info.get("stop") < cur_time:
                                                        formatted_info["stop"] = None
                                                        formatted_info["start"] = None
                                                    if formatted_info.get("start") and formatted_info.get("start") > cur_time:
                                                        formatted_info["start"] = None
                                                        formatted_info["stop"] = None
                                                    try:
                                                        isInstance = False
                                                        if formatted_info.get("start") and formatted_info.get("end"): isInstance = True
                                                        if rpc:
                                                            try:
                                                                req = rpc.update(
                                                                    loop_key=loop_key, 
                                                                    details=formatted_info["details"], 
                                                                    state=formatted_info["state"], 
                                                                    start=formatted_info["start"], 
                                                                    end=formatted_info["stop"], 
                                                                    large_image=formatted_info["large_image"], 
                                                                    large_url=formatted_info["large_image_url"],
                                                                    large_text=formatted_info["large_text"], 
                                                                    state_url=formatted_info["state_url"],
                                                                    instance=isInstance, 
                                                                    small_image=formatted_info["small_image"], 
                                                                    small_url=formatted_info["small_image_url"],
                                                                    small_text=formatted_info["small_text"], 
                                                                    name=playing_game_name if main_config.get("EFlagShowStudioGameNameInStatusBar") else "Roblox Studio 🔨",
                                                                    buttons=formatted_info["buttons"]
                                                                )
                                                                if req.get("code") == 2: printDebugMessage("Invalid RPC Loop Information Detected! Broken Loop!"); break
                                                            except Exception as e:
                                                                if err_count > 9:
                                                                    printDebugMessage("Discord RPC Session may be broken. Loop has been broken.")
                                                                    break
                                                                else: err_count += 1
                                                    except Exception as e:
                                                        if err_count > 9:
                                                            printDebugMessage("Discord RPC Session may be broken. Loop has been broken.")
                                                            break
                                                        else:
                                                            err_count += 1
                                                            printDebugMessage(f"There was an error updating Discord RPC: \n{trace()}")
                                                    time.sleep(0.1)
                                            except Exception as e: printDebugMessage(f"There was an error updating Discord RPC: \n{trace()}")
                                        embed_thread = threading.Thread(target=embed, daemon=True)
                                        embed_thread.daemon = True
                                        embed_thread.start()
                                        printDebugMessage("Successfully attached Discord RPC!")
                                except Exception as e: printDebugMessage("Unable to insert Discord Rich Presence. Please make sure Discord is open.")
                                try:
                                    if main_config.get("EFlagUseDiscordWebhook") == True and main_config.get("EFlagDiscordWebhookConnect") == True:
                                        if main_config.get("EFlagDiscordWebhookURL"):
                                            title = ts("Joined Studio Server!")
                                            color = 65280
                                            user_connected_text = ts("Unknown User")
                                            if connected_user_info: user_connected_text = f'[@{connected_user_info["name"]} [{connected_user_info["id"]}]](https://www.roblox.com/users/{connected_user_info["id"]}/profile)'
                                            buttons = []
                                            if universeId == -100:
                                                buttons = [
                                                    generateEmbedField(ts("Is Local File"), f"True"),
                                                    generateEmbedField(ts("Local File Path"), f"{current_place_info.get('place_identifier')}")
                                                ]
                                            else:
                                                buttons = [
                                                    generateEmbedField(ts("Is Local File"), f"False"),
                                                    generateEmbedField(ts("Connected Game"), f"[{place_info['name']}](https://www.roblox.com/games/{current_place_info.get('placeId')})"),
                                                    generateEmbedField(ts("Edit Link"), f"[{ts('Edit Now!')}](https://rbx.efaz.dev/studio?info=1+task:EditPlace+placeId:{current_place_info.get('placeId')}+universeId:{current_place_info.get('universeId')})")
                                                ]
                                            generated_body = generateDiscordPayload(title, color, buttons + [
                                                generateEmbedField(ts("Started"), f"<t:{int(start_time)}:R>"),
                                                generateEmbedField(ts("User Connected"), user_connected_text),
                                                generateEmbedField(ts("Server Location"), f"{generated_location}")
                                            ], thumbnail_url) 
                                            try: sendDiscordWebhook(generated_body, "onGameJoined")
                                            except Exception as e: printDebugMessage(f"There was an issue sending your webhook message. Exception: \n{trace()}")
                                except Exception as e: printDebugMessage("Unable to send Discord Webhook. Please check if the link is valid.")
                            else: printDebugMessage("Provided place info is not found.")
                        else: printDebugMessage(f"Place responses rejected by Roblox. [{generated_thumbnail_api_res.ok},{generated_thumbnail_api_res.status_code} | {generated_place_api_res.ok},{generated_place_api_res.status_code}]")
            def onOpeningGame(info):
                global current_place_info
                if not current_place_info: current_place_info = info
                elif info.get("placeId") and info.get("jobId"): 
                    for i, v in info.items(): current_place_info[i] = v
            def onGameLoaded(info):
                global connected_to_game
                if connected_to_game == False: onGameJoined({})
            def onLostConnection(info):
                global is_connection_lost
                is_connection_lost = True
                if main_config.get("EFlagForceReconnectOnStudioLost") == True and connected_roblox_instance.loading_existing_logs == False:
                    placeId = current_place_info and current_place_info.get('place_identifier')
                    universeId = current_place_info and current_place_info.get('universeId')
                    if placeId and universeId:
                        connected_roblox_instance.endInstance()
                        url = f"roblox-studio:1+task:EditPlace+placeId:{placeId}+universeId:{universeId}"
                        if main_os == "Darwin": subprocess.run(["/usr/bin/open", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cur_path)
                        else: subprocess.run(f"start {url}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cur_path)
            def onClosingGame(info):
                global connected_to_game
                global current_place_info
                global connected_user_info
                global is_connection_lost
                synced_place_info = None
                connected_to_game = False
                if current_place_info:
                    synced_place_info = dict(current_place_info)
                    current_place_info = None
                printErrorMessage("User has disconnected from the server!")
                try:
                    if main_os == "Windows" and connected_roblox_instance and main_config.get("EFlagShowRunningGameInTitle") == True:
                        windows_opened = connected_roblox_instance.getWindowsOpened()
                        for i in windows_opened: i.setWindowTitle(ts(f"Roblox Studio"))
                except Exception as e: printDebugMessage(f"Something went wrong setting the Window Title: \n{trace()}")
                if main_config.get("EFlagUseDiscordWebhook") == True and main_config.get("EFlagDiscordWebhookDisconnect") == True:
                    if main_config.get("EFlagDiscordWebhookURL"):
                        thumbnail_url = f"{main_host}/Images/DiscordIcon.png"
                        server_location = ts("Unknown Location")
                        start_time = 0
                        place_info = {"name": "???"}

                        if synced_place_info:
                            if synced_place_info.get("start_time"): start_time = synced_place_info.get("start_time")
                            if synced_place_info.get("server_location"): server_location = synced_place_info.get("server_location")
                            if synced_place_info.get("place_info"): place_info = synced_place_info.get("place_info")
                            if synced_place_info.get("thumbnail_url"): thumbnail_url = synced_place_info.get("thumbnail_url")

                            title = ts(f"Disconnected from Studio Server!")
                            color = 16711680

                            if is_connection_lost == True: title = ts(f"Lost Connection from Studio Server!"); color = 16776960
                            user_connected_text = ts("Unknown User")
                            if connected_user_info: user_connected_text = f'[@{connected_user_info["name"]} [{connected_user_info["id"]}]](https://www.roblox.com/users/{connected_user_info["id"]}/profile)'

                            buttons = []
                            if synced_place_info.get("universeId") == -100: 
                                buttons = [
                                    generateEmbedField(ts("Is Local File"), "True"), 
                                    generateEmbedField(ts("Local File Path"), f"{synced_place_info.get('place_identifier')}")
                                ]
                            else:
                                buttons = [
                                    generateEmbedField(ts("Is Local File"), f"False"),
                                    generateEmbedField(ts("Disconnected Game"), f"[{place_info['name']}](https://www.roblox.com/games/{synced_place_info.get('placeId')})"),
                                    generateEmbedField(ts("Edit Link"), f"[{ts('Edit Now!')}](https://rbx.efaz.dev/studio?info=1+task:EditPlace+placeId:{synced_place_info.get('placeId')}+universeId:{synced_place_info.get('universeId')})")
                                ]

                            generated_body = generateDiscordPayload(title, color, buttons + [
                                generateEmbedField(ts("Started"), f"<t:{int(start_time)}:R>"),
                                generateEmbedField(ts("User Connected"), user_connected_text),
                                generateEmbedField(ts("Server Location"), f"{server_location}")
                            ], thumbnail_url)
                            try: sendDiscordWebhook(generated_body, "onGameDisconnected")
                            except Exception as e: printDebugMessage(f"There was an issue sending your webhook message. Exception: \n{trace()}")
                if main_config.get("EFlagEnableDiscordRPC") == True:
                    global rpc
                    global rpc_info
                    try: 
                        if rpc: rpc.clear()
                    except Exception as e: printDebugMessage(f"There was an error clearing Discord RPC: \n{trace()}")
                    rpc_info = None
                if main_config.get("EFlagEndStudioPlaceWhenDisconnected") == True and connected_roblox_instance and handler.getIfRobloxIsOpen(studio=run_studio, pid=connected_roblox_instance.pid): connected_roblox_instance.endInstance()
            def onRobloxPublishing(info):
                printSuccessMessage("Roblox Game has been successfully published to Roblox!")
                if main_config.get("EFlagUseDiscordWebhook") == True and main_config.get("EFlagDiscordWebhookGamePublished") == True:
                    if main_config.get("EFlagDiscordWebhookURL"):
                        thumbnail_url = f"{main_host}/Images/DiscordIcon.png"
                        server_location = ts("Unknown Location")
                        start_time = 0
                        place_info = {"name": "???"}
                        if current_place_info:
                            if current_place_info.get("start_time"): start_time = current_place_info.get("start_time")
                            if current_place_info.get("server_location"): server_location = current_place_info.get("server_location")
                            if current_place_info.get("place_info"): place_info = current_place_info.get("place_info")
                            if current_place_info.get("thumbnail_url"): thumbnail_url = current_place_info.get("thumbnail_url")

                        title = ts(f"Roblox Game Published!")
                        color = 16748547
                        user_connected_text = ts("Unknown User")
                        if connected_user_info: user_connected_text = f'[@{connected_user_info["name"]} [{connected_user_info["id"]}]](https://www.roblox.com/users/{connected_user_info["id"]}/profile)'

                        buttons = []
                        if current_place_info.get("universeId") == -100:
                            buttons = [
                                generateEmbedField(ts("Is Local File"), f"True"),
                                generateEmbedField(ts("Local File Path"), f"{current_place_info.get('place_identifier')}")
                            ]
                        else:
                            buttons = [
                                generateEmbedField(ts("Is Local File"), f"False"),
                                generateEmbedField(ts("Published Game"), f"[{place_info['name']}](https://www.roblox.com/games/{current_place_info.get('placeId')})"),
                                generateEmbedField(ts("Edit Link"), f"[{ts('Edit Now!')}](https://rbx.efaz.dev/studio?info=1+task:EditPlace+placeId:{current_place_info.get('placeId')}+universeId:{current_place_info.get('universeId')})")
                            ]

                        generated_body = generateDiscordPayload(title, color, buttons + [
                            generateEmbedField(ts("Started"), f"<t:{int(start_time)}:R>"),
                            generateEmbedField(ts("User Connected"), user_connected_text),
                            generateEmbedField(ts("Server Location"), f"{server_location}")
                        ], thumbnail_url)
                        try: sendDiscordWebhook(generated_body, "onRobloxPublishing")
                        except Exception as e: printDebugMessage(f"There was an issue sending your webhook message. Exception: \n{trace()}")
            def onRobloxSaving(info):
                printSuccessMessage("Roblox Game has been successfully saved to Roblox!")
                if main_config.get("EFlagUseDiscordWebhook") == True and main_config.get("EFlagDiscordWebhookGameSaved") == True:
                    if main_config.get("EFlagDiscordWebhookURL"):
                        thumbnail_url = f"{main_host}/Images/DiscordIcon.png"
                        server_location = ts("Unknown Location")
                        start_time = 0
                        place_info = {"name": "???"}
                        if current_place_info:
                            if current_place_info.get("start_time"): start_time = current_place_info.get("start_time")
                            if current_place_info.get("server_location"): server_location = current_place_info.get("server_location")
                            if current_place_info.get("place_info"): place_info = current_place_info.get("place_info")
                            if current_place_info.get("thumbnail_url"): thumbnail_url = current_place_info.get("thumbnail_url")

                        title = ts(f"Roblox Game Saved!")
                        color = 16745942
                        user_connected_text = ts("Unknown User")
                        if connected_user_info: user_connected_text = f'[@{connected_user_info["name"]} [{connected_user_info["id"]}]](https://www.roblox.com/users/{connected_user_info["id"]}/profile)'

                        buttons = []
                        if current_place_info.get("universeId") == -100:
                            buttons = [
                                generateEmbedField(ts("Is Local File"), f"True"),
                                generateEmbedField(ts("Local File Path"), f"{current_place_info.get('place_identifier')}")
                            ]
                        else:
                            buttons = [
                                generateEmbedField(ts("Is Local File"), f"False"),
                                generateEmbedField(ts("Saved Game"), f"[{place_info['name']}](https://www.roblox.com/games/{current_place_info.get('placeId')})"),
                                generateEmbedField(ts("Edit Link"), f"[{ts('Edit Now!')}](https://rbx.efaz.dev/studio?info=1+task:EditPlace+placeId:{current_place_info.get('placeId')}+universeId:{current_place_info.get('universeId')})")
                            ]

                        generated_body = generateDiscordPayload(title, color, buttons + [
                            generateEmbedField(ts("Started"), f"<t:{int(start_time)}:R>"),
                            generateEmbedField(ts("User Connected"), user_connected_text),
                            generateEmbedField(ts("Server Location"), f"{server_location}")
                        ], thumbnail_url)
                        try: sendDiscordWebhook(generated_body, "onRobloxSaving")
                        except Exception as e: printDebugMessage(f"There was an issue sending your webhook message. Exception: \n{trace()}")
            def onPlayTestStart(info):
                global current_place_info
                if not current_place_info: current_place_info = info
                elif info.get("placeId") and info.get("jobId"): 
                    for i, v in info.items(): current_place_info[i] = v
            def onNewRobloxStudio(info):
                if main_os == "Darwin": subprocess.run(["/usr/bin/open", "orangeblox://reconnect-studio"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cur_path)
                else: subprocess.run("start orangeblox://reconnect-studio", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cur_path)
            def onStudioInstallerLaunched(info): connected_roblox_instance.endInstance()
            def onPlayTestDisconnected(info): pass
            def onTeamCreateConnect(info): pass
            def onTeamCreateDisconnect(info): pass
        else:
            def onGameJoined(info):
                if info.get("ip"):
                    printDebugMessage(f"Roblox IP Address Detected! IP: {info.get('ip')}")
                    allocated_roblox_ip = info.get("ip")
                    generated_location = "Unknown Location"
                    server_info_res = requests.get(f"https://ipinfo.io/{allocated_roblox_ip}/json")
                    if server_info_res.ok:
                        server_info_json = server_info_res.json
                        if server_info_json.get("city") and server_info_json.get("country"):
                            if not (server_info_json.get("region") == None or server_info_json.get("region") == ""): generated_location = f"{server_info_json['city']}, {server_info_json['region']}, {server_info_json['country']}"
                            else: generated_location = f"{server_info_json['city']}, {server_info_json['country']}"
                        else:
                            if main_config.get("EFlagEnableDebugMode"): printDebugMessage(server_info_res.text)
                            printDebugMessage("Failed to get server information: IP Request resulted with no information.")
                    else:
                        if main_config.get("EFlagEnableDebugMode"): printDebugMessage(server_info_res.text)
                        printDebugMessage("Failed to get server information: IP Request Rejected.")

                    if main_config.get("EFlagNotifyServerLocation") == True:
                        if set_server_type == 0:
                            printSuccessMessage(f"Roblox is currently connecting to a public server in: {generated_location} [{allocated_roblox_ip}]!")
                            displayNotification(ts("Joining Server"), ts(f"You have connected to a server from {generated_location}!"))
                        elif set_server_type == 1:
                            printSuccessMessage(f"Roblox is currently connecting to a private server in: {generated_location} [{allocated_roblox_ip}]!")
                            displayNotification(ts("Joining Private Server"), ts(f"You have connected to a private server from {generated_location}!"))
                        elif set_server_type == 2:
                            printSuccessMessage(f"Roblox is currently connecting to a reserved server in: {generated_location} [{allocated_roblox_ip}]!")
                            displayNotification(ts("Joining Reserved Server"), ts(f"You have connected to a reserved server from {generated_location}!"))
                        elif set_server_type == 3:
                            printSuccessMessage(f"Roblox is currently connecting to a party in: {generated_location} [{allocated_roblox_ip}]!")
                            displayNotification(ts("Joining Party Server"), ts(f"You have connected to a party server from {generated_location}!"))
                        else:
                            printSuccessMessage(f"Roblox is currently connecting to a server in: {generated_location} [{allocated_roblox_ip}]!")
                            displayNotification(ts("Joining Server"), ts(f"You have connected to a server from {generated_location}!"))
                        printDebugMessage("Sent Notification to Bootstrap for Notification Center shipping!")

                    global current_place_info
                    global connected_user_info
                    global connected_to_game
                    if current_place_info:
                        current_place_info["server_location"] = generated_location
                        connected_to_game = True
                        if main_config.get("EFlagUseEfazDevAPI") == True: 
                            generated_universe_id_res = requests.get(f"https://api.efaz.dev/api/roblox/universeId/{current_place_info.get('placeId')}", loop_429=main_config.get("EFlagEnableLoop429Requests")==True)
                            if generated_universe_id_res and generated_universe_id_res.json: generated_universe_id_res.json = generated_universe_id_res.json.get("response")
                        else: generated_universe_id_res = requests.get(f"https://apis.roblox.com/universes/v1/places/{current_place_info.get('placeId')}/universe", loop_429=main_config.get("EFlagEnableLoop429Requests")==True, cookies=createCookieHeader())
                        if generated_universe_id_res.ok:
                            generated_universe_id_json = generated_universe_id_res.json
                            if generated_universe_id_json and not (generated_universe_id_json.get("universeId") == None):
                                if current_place_info: current_place_info["universeId"] = generated_universe_id_json.get("universeId")
                            else: current_place_info = None
                        else: current_place_info = None
                        if current_place_info:
                            universeId = current_place_info.get('universeId')
                            if main_config.get("EFlagUseEfazDevAPI") == True: 
                                generated_thumbnail_api_res = requests.get(f"https://api.efaz.dev/api/roblox/game-thumbnail/{universeId}", loop_429=main_config.get("EFlagEnableLoop429Requests")==True)
                                generated_place_api_res = requests.get(f"https://api.efaz.dev/api/roblox/places-in-universe/{universeId}", loop_429=main_config.get("EFlagEnableLoop429Requests")==True)
                                generated_universe_api_res = requests.get(f"https://api.efaz.dev/api/roblox/game-info/{universeId}", loop_429=main_config.get("EFlagEnableLoop429Requests")==True)
                                if generated_thumbnail_api_res and generated_thumbnail_api_res.json: generated_thumbnail_api_res.json = generated_thumbnail_api_res.json.get("response")
                                if generated_place_api_res and generated_place_api_res.json: generated_place_api_res.json = generated_place_api_res.json.get("response")
                                if generated_universe_api_res and generated_universe_api_res.json: generated_universe_api_res.json = generated_universe_api_res.json.get("response")
                            else: 
                                generated_thumbnail_api_res = requests.get(f"https://thumbnails.roblox.com/v1/games/icons?universeIds={universeId}&returnPolicy=PlaceHolder&size=512x512&format=Png&isCircular=false", loop_429=main_config.get("EFlagEnableLoop429Requests")==True, cookies=createCookieHeader())
                                generated_place_api_res = requests.get(f"https://develop.roblox.com/v1/universes/{universeId}/places?isUniverseCreation=false&limit=50&sortOrder=Asc", loop_429=main_config.get("EFlagEnableLoop429Requests")==True, cookies=createCookieHeader())
                                generated_universe_api_res = requests.get(f"https://games.roblox.com/v1/games?universeIds={universeId}", loop_429=main_config.get("EFlagEnableLoop429Requests")==True, cookies=createCookieHeader())
                            if generated_thumbnail_api_res.ok and generated_place_api_res.ok and generated_universe_api_res.ok:
                                generated_thumbnail_api_json = generated_thumbnail_api_res.json
                                generated_place_api_json = generated_place_api_res.json
                                generated_universe_api_json = generated_universe_api_res.json

                                thumbnail_url = f"{main_host}/Images/AppIconPlayRoblox.png"
                                if generated_thumbnail_api_json.get("data"):
                                    if len(generated_thumbnail_api_json.get("data")) > 0: thumbnail_url = generated_thumbnail_api_json.get("data")[0]["imageUrl"]
                                if current_place_info: current_place_info["thumbnail_url"] = thumbnail_url

                                if len(generated_place_api_json.get("data", [])) > 0 and len(generated_universe_api_json.get("data", [])) > 0:
                                    generated_universe_api_json = generated_universe_api_json.get("data")[0]
                                    place_info = {}
                                    for place_under_experience in generated_place_api_json.get("data"):
                                        if current_place_info and str(place_under_experience.get("id")) == str(current_place_info.get("placeId")): place_info = place_under_experience
                                    if current_place_info:
                                        if place_info:
                                            generated_universe_api_json["rootPlaceName"] = generated_universe_api_json["name"]
                                            for i in generated_universe_api_json.keys():
                                                if not place_info.get(i) and (not (i == "id" or i == "name" or i == "description" or i == "universeId")): place_info[i] = generated_universe_api_json[i]
                                            if current_place_info: current_place_info["place_info"] = place_info
                                    try:
                                        if main_os == "Windows" and connected_roblox_instance:
                                            if main_config.get("EFlagShowRunningAccountNameInTitle") == True:
                                                windows_opened = connected_roblox_instance.getWindowsOpened()
                                                for i in windows_opened:
                                                    if connected_user_info:
                                                        if main_config.get("EFlagShowDisplayNameInTitle") == True: i.setWindowTitle(ts(f"Roblox - Playing @{connected_user_info.get('name', 'Unknown')} [ID: {connected_user_info.get('id', 'Unknown')}] as {connected_user_info.get('display', 'Unknown')}!"))
                                                        else: i.setWindowTitle(ts(f"Roblox - Playing @{connected_user_info.get('name', 'Unknown')} [ID: {connected_user_info.get('id', 'Unknown')}]!"))
                                            elif main_config.get("EFlagShowRunningGameInTitle") == True:
                                                windows_opened = connected_roblox_instance.getWindowsOpened()
                                                for i in windows_opened: i.setWindowTitle(ts(f"Roblox - Playing {place_info.get('name', 'Unknown')}"))
                                    except Exception as e: printDebugMessage(f"Something went wrong setting the Window Title: \n{trace()}")
                                    try:
                                        start_time = int(datetime.datetime.now(tz=datetime.UTC).timestamp())
                                        if main_config.get("EFlagSetDiscordRPCStart") and (type(main_config.get("EFlagSetDiscordRPCStart")) is float or type(main_config.get("EFlagSetDiscordRPCStart")) is int): start_time = main_config.get("EFlagSetDiscordRPCStart")
                                        if current_place_info: current_place_info["start_time"] = start_time
                                        if main_config.get("EFlagEnableDiscordRPC") == True:
                                            # Handle User Thumbnail
                                            app_settings = handler.getRobloxAppSettings()
                                            logged_in_user: dict = app_settings.get("loggedInUser")
                                            if logged_in_user.get("name") and logged_in_user.get("id"):
                                                connected_user_info = {"name": logged_in_user.get("name"), "id": logged_in_user.get("id"), "display": logged_in_user.get("displayName")}
                                                if main_config.get("EFlagShowUserProfilePictureInsteadOfLogo") == True:
                                                    thumbnail_res = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={logged_in_user.get('id')}&size=100x100&format=Png&isCircular=false", loop_429=main_config.get("EFlagEnableLoop429Requests")==True, cookies=createCookieHeader())
                                                    if thumbnail_res.ok:
                                                        thumbnail_json = thumbnail_res.json
                                                        if thumbnail_json and len(thumbnail_json.get("data", [])) > 0:
                                                            user_thumbnail = thumbnail_json["data"][0].get("imageUrl")
                                                            if user_thumbnail:
                                                                if connected_user_info:
                                                                    connected_user_info["thumbnail"] = user_thumbnail
                                                                    printSuccessMessage(f"Successfully loaded user thumbnail of @{logged_in_user.get('name')} [User ID: {logged_in_user.get('id')}]!")
                                                                    printDebugMessage(f"Loaded thumbnail: {user_thumbnail}")
                                                            else: printDebugMessage(f"Failed to load thumbnail for @{logged_in_user.get('name')} [User ID: {logged_in_user.get('id')}]! Status Code: {thumbnail_res.status_code}")
                                                        else: printDebugMessage(f"Failed to load thumbnail for @{logged_in_user.get('name')} [User ID: {logged_in_user.get('id')}]! Status Code: {thumbnail_res.status_code}")
                                                    else: printDebugMessage(f"Failed to load thumbnail for @{logged_in_user.get('name')} [User ID: {logged_in_user.get('id')}]! Status Code: {thumbnail_res.status_code}")
                                            
                                            def embed():
                                                try:
                                                    global rpc
                                                    global rpc_info
                                                    global set_current_private_server_key

                                                    err_count = 0
                                                    loop_key = rpc.generate_loop_key()
                                                    while True:
                                                        if (not rpc) or (not rpc.connected) or (not rpc.current_loop_id == loop_key): break
                                                        if rpc_info == None: rpc_info = {}
                                                        playing_game_name = place_info['name']
                                                        creator_name = ts(f"Made by {'@' if place_info['creator'].get('type') == 'User' else ''}{place_info['creator']['name']}")
                                                        creator_name = creator_name.replace("✅", "")
                                                        if place_info.get("creator").get("hasVerifiedBadge") == True: creator_name = f"{creator_name} ✅!"
                                                        else: creator_name = f"{creator_name}!"
                                                        if not (place_info.get("rootPlaceId") == place_info.get("id")): playing_game_name = f"{playing_game_name} ({place_info['rootPlaceName']})"
                                                        formatted_info = {
                                                            "details": rpc_info.get("details") if rpc_info.get("details") else f"Playing {playing_game_name}",
                                                            "state": rpc_info.get("state") if rpc_info.get("state") else creator_name,
                                                            "start": rpc_info.get("start") if rpc_info.get("start") else start_time,
                                                            "stop": rpc_info.get("stop") if rpc_info.get("stop") and rpc_info.get("stop") > 1000 else None,
                                                            "large_image_url": f"https://www.roblox.com/",
                                                            "large_image": rpc_info.get("large_image") if rpc_info.get("large_image") else thumbnail_url,
                                                            "large_text": rpc_info.get("large_text") if rpc_info.get("large_text") else playing_game_name,
                                                            "small_image_url": f"{main_host}/",
                                                            "state_url": None,
                                                            "buttons": [],
                                                            "small_image": rpc_info.get("small_image") if rpc_info.get("small_image") else f"{main_host}/Images/AppIconPlayRobloxDiscord.png",
                                                            "small_text": rpc_info.get("small_text") if rpc_info.get("small_text") else "OrangeBlox",
                                                            "launch_data": rpc_info.get("launch_data") if rpc_info.get("launch_data") else ""
                                                        }
                                                        launch_data = ""
                                                        add_exam = False
                                                        if not formatted_info["launch_data"] == "": formatted_info["launch_data"] = f"&launchData={formatted_info['launch_data']}"; add_exam = False
                                                        if formatted_info["small_image"] == f"{main_host}/Images/AppIconPlayRobloxDiscord.png" and formatted_info["small_text"] == "OrangeBlox" and main_config.get("EFlagShowUserProfilePictureInsteadOfLogo") == True and connected_user_info and connected_user_info.get("thumbnail"): formatted_info["small_image"] = connected_user_info.get("thumbnail")
                                                        if formatted_info["small_text"] == "OrangeBlox" and main_config.get("EFlagShowUsernameInSmallImage") == True and connected_user_info and connected_user_info.get("display") and connected_user_info.get("name"): 
                                                            formatted_info["small_text"] = ts(f"Playing @{connected_user_info.get('name')} as {connected_user_info.get('display')}!")
                                                            formatted_info["smart_image_url"] = f"https://www.roblox.com/users/{logged_in_user.get('id')}/profile"
                                                        if current_place_info:
                                                            formatted_info["buttons"] = [{
                                                                "label": ts("Open Game Page 🕹️"), 
                                                                "url": f"https://www.roblox.com/games/{current_place_info.get('placeId')}"
                                                            }]
                                                            formatted_info["large_image_url"] = f"https://www.roblox.com/games/{current_place_info.get('placeId')}"
                                                            if formatted_info["state"] == creator_name and place_info and place_info['creator']['id'] > 0:
                                                                if place_info['creator'].get('type') == 'User': formatted_info["state_url"] = f"https://www.roblox.com/users/{place_info['creator']['id']}/profile"
                                                                else: formatted_info["state_url"] = f"https://www.roblox.com/groups/{place_info['creator']['id']}"
                                                            if (set_server_type == 1 or set_server_type == 2 or set_server_type == 3) and main_config.get("EFlagAllowPrivateServerJoining") == True and set_current_private_server_key:
                                                                if add_exam == True: launch_data = f'{launch_data}?gameInstanceId={current_place_info.get("jobId")}?accessCode={set_current_private_server_key}'
                                                                else: launch_data = f'{launch_data}&gameInstanceId={current_place_info.get("jobId")}&accessCode={set_current_private_server_key}'
                                                            else:
                                                                if add_exam == True: launch_data = f'{launch_data}?gameInstanceId={current_place_info.get("jobId")}'
                                                                else: launch_data = f'{launch_data}&gameInstanceId={current_place_info.get("jobId")}'
                                                            cur_time = int(datetime.datetime.now(tz=datetime.UTC).timestamp())
                                                            if formatted_info.get("stop") and formatted_info.get("stop") < cur_time:
                                                                formatted_info["stop"] = None
                                                                formatted_info["start"] = None
                                                            if formatted_info.get("start") and formatted_info.get("start") > cur_time:
                                                                formatted_info["start"] = None
                                                                formatted_info["stop"] = None
                                                            formatted_info["launch_data"] = launch_data
                                                            try:
                                                                isInstance = False
                                                                if formatted_info.get("start") and formatted_info.get("end"): isInstance = True
                                                                if main_config.get("EFlagEnableDiscordRPCJoining") == True:
                                                                    formatted_info["buttons"].append({
                                                                        "label": ts("Join Server! 🚀"),
                                                                        "url": f"roblox://experiences/start?placeId={current_place_info['placeId']}{formatted_info['launch_data']}"
                                                                    })
                                                                if rpc:
                                                                    try:
                                                                        req = rpc.update(
                                                                            loop_key=loop_key, 
                                                                            details=formatted_info["details"], 
                                                                            state=formatted_info["state"], 
                                                                            start=formatted_info["start"], 
                                                                            end=formatted_info["stop"], 
                                                                            large_image=formatted_info["large_image"], 
                                                                            large_text=formatted_info["large_text"], 
                                                                            large_url=formatted_info["large_image_url"],
                                                                            state_url=formatted_info["state_url"],
                                                                            instance=isInstance, 
                                                                            small_image=formatted_info["small_image"], 
                                                                            small_text=formatted_info["small_text"], 
                                                                            small_url=formatted_info["small_image_url"],
                                                                            name=playing_game_name if main_config.get("EFlagShowGameNameInStatusBar") else "Roblox",
                                                                            buttons=formatted_info["buttons"]
                                                                        )
                                                                        if req.get("code") == 2: break
                                                                    except Exception as e:
                                                                        if err_count > 9:
                                                                            printDebugMessage("Discord RPC Session may be broken. Loop has been broken.")
                                                                            break
                                                                        else: err_count += 1
                                                            except Exception as e:
                                                                if err_count > 9:
                                                                    printDebugMessage("Discord RPC Session may be broken. Loop has been broken.")
                                                                    break
                                                                else:
                                                                    err_count += 1
                                                                    printDebugMessage(f"There was an error updating Discord RPC: \n{trace()}")
                                                        else: break
                                                        time.sleep(0.1)
                                                except Exception as e: printDebugMessage(f"There was an error updating Discord RPC: \n{trace()}")
                                            embed_thread = threading.Thread(target=embed, daemon=True)
                                            embed_thread.daemon = True
                                            embed_thread.start()
                                            printDebugMessage("Successfully attached Discord RPC!")
                                    except Exception as e: printDebugMessage("Unable to insert Discord Rich Presence. Please make sure Discord is open.")
                                    try:
                                        if main_config.get("EFlagUseDiscordWebhook") == True and main_config.get("EFlagDiscordWebhookConnect") == True:
                                            if main_config.get("EFlagDiscordWebhookURL"):
                                                title = "Joined Server!"
                                                color = 65280
                                                if set_server_type == 0: title = ts("Joined Public Server!")
                                                elif set_server_type == 1: title = ts("Joined Private Server!")
                                                elif set_server_type == 2: title = ts("Joined Reserved Server!")
                                                elif set_server_type == 3: title = ts("Joined Party Server!"); color = 5570815
                                                else: title = ts("Joined Server!")
                                                launch_data = ""
                                                add_exam = False
                                                if not launch_data == "":
                                                    launch_data = f"&launchData={launch_data}"
                                                    add_exam = False
                                                if (set_server_type == 1 or set_server_type == 2 or set_server_type == 3) and main_config.get("EFlagAllowPrivateServerJoining") == True and set_current_private_server_key:
                                                    if add_exam == True: launch_data = f'{launch_data}?gameInstanceId={current_place_info["jobId"]}&accessCode={set_current_private_server_key}'
                                                    else: launch_data = f'{launch_data}&gameInstanceId={current_place_info["jobId"]}&accessCode={set_current_private_server_key}'
                                                else:
                                                    if add_exam == True: launch_data = f'{launch_data}?gameInstanceId={current_place_info["jobId"]}'
                                                    else: launch_data = f'{launch_data}&gameInstanceId={current_place_info["jobId"]}'
                                                user_connected_text = ts("Unknown User")
                                                if connected_user_info: user_connected_text = f'[@{connected_user_info["name"]} [{connected_user_info["id"]}]](https://www.roblox.com/users/{connected_user_info["id"]}/profile)'

                                                generated_body = generateDiscordPayload(title, color, [
                                                    generateEmbedField(ts("Connected Game"), f"[{place_info['name']}](https://www.roblox.com/games/{current_place_info.get('placeId')})"),
                                                    generateEmbedField(ts("Join Link"), f"[{ts('Join Now!')}](https://rbx.efaz.dev/join?placeId={current_place_info.get('placeId')}{launch_data})"),
                                                    generateEmbedField(ts("Started"), f"<t:{int(start_time)}:R>"),
                                                    generateEmbedField(ts("User Connected"), user_connected_text),
                                                    generateEmbedField(ts("Server Location"), f"{generated_location}")
                                                ], thumbnail_url)
                                                try: sendDiscordWebhook(generated_body, "onGameJoined")
                                                except Exception as e: printDebugMessage(f"There was an issue sending your webhook message. Exception: \n{trace()}")
                                    except Exception as e: printDebugMessage("Unable to send Discord Webhook. Please check if the link is valid.")
                                else: printDebugMessage("Provided place info is not found.")
                            else: printDebugMessage(f"Place responses rejected by Roblox. [{generated_thumbnail_api_res.ok},{generated_thumbnail_api_res.status_code} | {generated_place_api_res.ok},{generated_place_api_res.status_code}]")
            def onGameDisconnected(info):
                global current_place_info
                global connected_to_game
                global skip_disconnect_notification
                global is_teleport
                global connected_user_info
                it_is_teleport = False
                connected_to_game = False
                synced_place_info = None
                if skip_disconnect_notification == True: skip_disconnect_notification = False; return
                if current_place_info: synced_place_info = dict(current_place_info); current_place_info = None
                if is_teleport == True:
                    printYellowMessage("User has been teleported!")
                    it_is_teleport = True
                    is_teleport = False
                else: printErrorMessage("User has disconnected from the server!")
                try:
                    if main_os == "Windows" and connected_roblox_instance and main_config.get("EFlagShowRunningGameInTitle") == True:
                        windows_opened = connected_roblox_instance.getWindowsOpened()
                        for i in windows_opened: i.setWindowTitle(ts(f"Roblox"))
                except Exception as e: printDebugMessage(f"Something went wrong setting the Window Title: \n{trace()}")
                if main_config.get("EFlagUseDiscordWebhook") == True and main_config.get("EFlagDiscordWebhookDisconnect") == True:
                    if main_config.get("EFlagDiscordWebhookURL"):
                        thumbnail_url = f"{main_host}/Images/DiscordIcon.png"
                        server_location = ts("Unknown Location")
                        start_time = 0
                        place_info = {"name": "???"}

                        if synced_place_info:
                            if synced_place_info.get("start_time"): start_time = synced_place_info.get("start_time")
                            if synced_place_info.get("server_location"): server_location = synced_place_info.get("server_location")
                            if synced_place_info.get("place_info"): place_info = synced_place_info.get("place_info")
                            if synced_place_info.get("thumbnail_url"): thumbnail_url = synced_place_info.get("thumbnail_url")

                            server_type = ts("Public Server")
                            if set_server_type == 0: server_type = ts("Public Server")
                            elif set_server_type == 1: server_type = ts("Private Server")
                            elif set_server_type == 2: server_type = ts("Reserved Server")
                            elif set_server_type == 3: server_type = ts("Party Server")
                            else: server_type = ts("Public Server")

                            title = f"{ts('Disconnected from')} {server_type}!"
                            color = 16711680
                            if it_is_teleport == True: title = f"{ts('Teleported to')} {server_type}!"; color = 16776960

                            launch_data = ""
                            add_exam = False
                            if not launch_data == "":
                                launch_data = f"&launchData={launch_data}"
                                add_exam = False
                            if (set_server_type == 1 or set_server_type == 2 or set_server_type == 3) and main_config.get("EFlagAllowPrivateServerJoining") == True and set_current_private_server_key:
                                if add_exam == True: launch_data = f'{launch_data}?gameInstanceId={synced_place_info["jobId"]}?accessCode={set_current_private_server_key}'
                                else: launch_data = f'{launch_data}&gameInstanceId={synced_place_info["jobId"]}&accessCode={set_current_private_server_key}'
                            else:
                                if add_exam == True: launch_data = f'{launch_data}?gameInstanceId={synced_place_info["jobId"]}'
                                else: launch_data = f'{launch_data}&gameInstanceId={synced_place_info["jobId"]}'

                            user_connected_text = ts("Unknown User")
                            if connected_user_info: user_connected_text = f'[@{connected_user_info["name"]} [{connected_user_info["id"]}]](https://www.roblox.com/users/{connected_user_info["id"]}/profile)'
                            generated_body = generateDiscordPayload(title, color, [
                                generateEmbedField(ts("Disconnected Game"), f"[{place_info['name']}](https://www.roblox.com/games/{synced_place_info.get('placeId')})"),
                                generateEmbedField(ts("Join Link"), f"[{ts('Join Again!')}](https://rbx.efaz.dev/join?placeId={synced_place_info.get('placeId')}{launch_data})"),
                                generateEmbedField(ts("Started"), f"<t:{int(start_time)}:R>"),
                                generateEmbedField(ts("User Connected"), user_connected_text),
                                generateEmbedField(ts("Server Location"), f"{server_location}"),
                                generateEmbedField(ts("Closing Reason"), f"{info.get('message')} (Code: {info.get('code')})")
                            ], thumbnail_url)
                            try: sendDiscordWebhook(generated_body, "onGameDisconnected")
                            except Exception as e:  printDebugMessage(f"There was an issue sending your webhook message. Exception: \n{trace()}")
                if main_config.get("EFlagEnableDiscordRPC") == True:
                    global rpc
                    global rpc_info
                    try: 
                        if rpc: rpc.clear()
                    except Exception as e: printDebugMessage(f"There was an error clearing Discord RPC: \n{trace()}")
                    rpc_info = None
            def onGameStart(info):
                global current_place_info
                global skip_disconnect_notification
                if current_place_info: onGameDisconnected({"code": "285", "message": "Client/User issued disconnect."}); skip_disconnect_notification = True
                if info.get("placeId") and info.get("jobId"): current_place_info = info
            def onTeleport(consoleLine):
                global is_teleport
                is_teleport = True
            def onRobloxAppLoginFailed(consoleLine):
                global is_app_login_fail
                is_app_login_fail = True
            def onPrivateServer(data):
                global set_server_type
                global set_current_private_server_key
                set_server_type = 1
                if main_config.get("EFlagAllowPrivateServerJoining") == True and data and data.get("data"): set_current_private_server_key = data["data"].get("accessCode")
                else: set_current_private_server_key = None
            def onReservedServer(data):
                global set_server_type
                global set_current_private_server_key
                set_server_type = 2
                if main_config.get("EFlagAllowPrivateServerJoining") == True and data and data.get("data"): set_current_private_server_key = data["data"].get("accessCode")
                else: set_current_private_server_key = None
            def onPartyServer(data):
                global set_server_type
                global set_current_private_server_key
                set_server_type = 3
                if main_config.get("EFlagAllowPrivateServerJoining") == True and data and data.get("data"): set_current_private_server_key = data["data"].get("accessCode")
                else: set_current_private_server_key = None
            def onMainServer(consoleLine):
                global set_server_type
                global set_current_private_server_key
                set_server_type = 0
                set_current_private_server_key = None
            def onLoadedFFlags(data): printSuccessMessage("Roblox client has successfully loaded FFlags from local file!")
            def onRobloxVoiceChatMute(data): printDebugMessage("Voice Chat microphone has been muted!")
            def onRobloxVoiceChatUnmute(data): printDebugMessage("Voice Chat microphone has been unmuted!")
        def onRobloxAppStart(consoleLine):
            global rpc
            thumbnail_url = getRobloxThumbnailURL()
            if main_config.get("EFlagEnableDiscordRPC") == True:
                need_new_rpc = True
                try: 
                    if rpc and rpc.connected == True: need_new_rpc = False
                except Exception as e: printDebugMessage(f"There was an error checking Discord RPC: \n{trace()}")
                if need_new_rpc == True:
                    rpc = Presence("1367683523338698863" if run_studio == True else "1297668920349823026")
                    rpc.set_debug_mode(main_config.get("EFlagEnableDebugMode") == True)
                    rpc.connect()
                    if not (main_config.get("EFlagEnableDefaultDiscordRPC") == False):
                        start_time = int(datetime.datetime.now(tz=datetime.UTC).timestamp())
                        if main_config.get("EFlagSetDiscordRPCStart") and (type(main_config.get("EFlagSetDiscordRPCStart")) is float or type(main_config.get("EFlagSetDiscordRPCStart")) is int): start_time = main_config.get("EFlagSetDiscordRPCStart")
                        rpc.update(
                            details=f"Idling Roblox{' Studio' if run_studio == True else ''}",
                            start=start_time,
                            large_image=thumbnail_url, 
                            large_url="https://www.roblox.com/",
                            large_text=f"Roblox{' Studio' if run_studio == True else ''}", 
                            small_image=f"{main_host}/Images/AppIcon{'RunStudio' if run_studio == True else 'PlayRoblox'}Discord.png", 
                            small_url=main_host,
                            small_text="OrangeBlox", 
                            buttons=[
                                {
                                    "label": ts("Go to Roblox! 🌐"), 
                                    "url": f"https://www.roblox.com/"
                                }
                            ]
                        )
                        rpc.default_presence = rpc.current_presence
            if main_config.get("EFlagUseDiscordWebhook") == True and main_config.get("EFlagDiscordWebhookRobloxAppStart") == True:
                if main_config.get("EFlagDiscordWebhookURL"):
                    embed_fields = [
                        generateEmbedField(ts("Connected PID"), connected_roblox_instance.pid),
                        generateEmbedField(ts("Log Location"), connected_roblox_instance.log_file)
                    ]
                    if run_studio == False and main_os == "Windows" and main_config.get("EFlagEnableDuplicationOfClients") == True: embed_fields.append(generateEmbedField(ts("Handles Roblox Multi-Instance"), str(connected_roblox_instance.created_mutex == True)))
                    generated_body = generateDiscordPayload((ts("Roblox Studio Started!") if run_studio == True else ts("Roblox Started!")), (65535 if run_studio == True else 6225823), embed_fields, thumbnail_url)
                    try: sendDiscordWebhook(generated_body, "onRobloxStart")
                    except Exception as e: printDebugMessage(f"There was an issue sending your webhook message. Exception: \n{trace()}")
        def onRobloxCrash(consoleLine):
            global updated_count
            global connected_to_game
            connected_to_game = False
            updated_count = 999
            global rpc
            global rpc_info
            try: 
                if rpc: rpc.close()
            except Exception as e: printDebugMessage(f"There was an error closing Discord RPC: \n{trace()}")
            rpc = None
            rpc_info = None
            printErrorMessage(f"There was an error inside the {'RobloxStudio' if run_studio == True else 'RobloxPlayer'} that has caused it to crash! Sorry!")
            printDebugMessage(f"Crashed Data: {consoleLine}")
            if main_config.get("EFlagUseDiscordWebhook") == True and main_config.get("EFlagDiscordWebhookRobloxCrash") == True and main_config.get("EFlagDiscordWebhookURL"):
                thumbnail_url = getRobloxThumbnailURL()
                generated_body = generateDiscordPayload((ts(f"Uh oh! Roblox Studio Crashed!") if run_studio == True else ts(f"Uh oh! Roblox Crashed!")), 0, [generateEmbedField(ts("Console Log"), consoleLine)], thumbnail_url)
                try: sendDiscordWebhook(generated_body, "onRobloxCrash")
                except Exception as e: printDebugMessage(f"There was an issue sending your webhook message. Exception: \n{trace()}")
        def onRobloxExit(consoleLine):
            global is_app_login_fail
            global current_place_info
            if is_app_login_fail == True: printDebugMessage(f"Roblox{' Studio' if run_studio == True else ''} failed to launch login!")
            else: printDebugMessage(f"User has closed the Roblox{' Studio' if run_studio == True else ''} window!")
            if connected_roblox_instance and connected_roblox_instance.created_mutex == True: printYellowMessage("This process is handling multi-instance for all open Roblox windows. If you close this window, all Roblox windows may close.")
            else: printErrorMessage(f"Roblox{' Studio' if run_studio == True else ''} window was closed! Closing Bootstrap App..")
            if main_config.get("EFlagEnableDiscordRPC") == True:
                global rpc
                global rpc_info
                try: 
                    if rpc: rpc.close()
                except Exception as e: printDebugMessage(f"There was an error closing Discord RPC: \n{trace()}")
                rpc = None
                rpc_info = None
            if run_studio == False and main_config.get("EFlagEnableMultiAutoReconnect") == True and current_place_info and current_place_info.get("place_info") and current_place_info.get("placeId"): 
                global set_current_private_server_key
                global given_args
                printYellowMessage("Reconnecting Roblox..")
                if type(main_config.get("EFlagRobloxLinkShortcuts")) is dict and connected_user_info and connected_user_info.get("id"):
                    for i, v in main_config.get("EFlagRobloxLinkShortcuts").items():
                        if type(v.get("cookie_paths")) is dict and v.get("cookie_id") == connected_user_info.get("id"):
                            for d, k in v.get("cookie_paths").items():
                                if main_os == "Darwin" and (d.startswith(os.path.join(pip_class.getLocalAppData(), "HTTPStorages", "com.roblox.")) and k.startswith(os.path.join(pip_class.getLocalAppData(), "Roblox", "RBXCookies"))): custom_cookies[d] = k
                                elif main_os == "Windows" and (d == os.path.join(pip_class.getLocalAppData(), "Roblox", "LocalStorage", "RobloxCookies.dat") and k.startswith(os.path.join(pip_class.getLocalAppData(), "Roblox", "RBXCookies"))): custom_cookies[d] = k
                if (set_server_type == 1 or set_server_type == 2 or set_server_type == 3) and set_current_private_server_key: launch_data = f'&accessCode={set_current_private_server_key}'
                else: launch_data = f''
                given_args = ["Main.py", f"roblox://experiences/start?placeId={current_place_info.get('placeId')}&universeId={current_place_info.get('universeId')}&gameInstanceId={current_place_info['jobId']}{launch_data}"]
                current_place_info = None
                connected_roblox_instance.requestThreadClosing()
                runRobloxClient()
                return
            current_place_info = None
            if main_config.get("EFlagUseDiscordWebhook") == True and main_config.get("EFlagDiscordWebhookRobloxAppClose") == True:
                if connected_roblox_instance and not (connected_roblox_instance.log_file == "") and main_config.get("EFlagDiscordWebhookURL"):
                    title = ts("Roblox Studio Closed!") if run_studio == True else ts("Roblox Closed!")
                    color = 12076614 if run_studio == True else 16735838
                    thumbnail_url = getRobloxThumbnailURL()
                    embed_fields = [
                        generateEmbedField(ts("Disconnected PID"), connected_roblox_instance.pid),
                        generateEmbedField(ts("Log Location"), connected_roblox_instance.log_file)
                    ]
                    if run_studio == False and main_os == "Windows" and (main_config.get("EFlagEnableDuplicationOfClients") == True): embed_fields.append(generateEmbedField(ts("Handles Roblox Multi-Instance"), str(connected_roblox_instance.created_mutex == True)))
                    if is_app_login_fail == True: title = ts("Roblox Failed Login!"); color = 13172807
                    generated_body = generateDiscordPayload(title, color, embed_fields, thumbnail_url)
                    try: sendDiscordWebhook(generated_body, "onRobloxExit")
                    except Exception as e: printDebugMessage(f"There was an issue sending your webhook message. Exception: \n{trace()}")
        def onBloxstrapMessage(info, disableWebhook=False):
            if (run_studio == True and main_config.get("EFlagAllowBloxstrapStudioSDK") == True) or (run_studio == False and main_config.get("EFlagAllowBloxstrapSDK") == True):
                global rpc
                global rpc_info
                if info.get("command"):
                    went_through = False
                    data_names = {
                        "details": ts("Details"),
                        "state": ts("State"),
                        "timeStart": ts("Round Starting"),
                        "timeEnd": ts("Round Ending"),
                        "largeImage": ts("Large Image"),
                        "smallImage": ts("Small Image"),
                        "launch_data": ts("URL Launch Data")
                    }
                    before_data = {}
                    passed_data = {}
                    if rpc_info == None: rpc_info = {}
                    for i,v in rpc_info.items(): before_data[i] = v
                    if info["command"] == "SetRichPresence":
                        if rpc:
                            if rpc_info == None: rpc_info = {}
                            if type(info["data"]) is dict:
                                if info["data"].get("clear") == True or info["data"].get("reset") == True: rpc_info = {}
                                if type(info["data"].get("details")) is str or type(info["data"].get("details")) is None: 
                                    rpc_info["details"] = info["data"].get("details")
                                    passed_data[data_names["details"]] = info["data"].get("details")
                                if type(info["data"].get("state")) is str or type(info["data"].get("state")) is None: 
                                    rpc_info["state"] = info["data"].get("state")
                                    passed_data[data_names["state"]] = info["data"].get("state")
                                if type(info["data"].get("timeStart")) is int or type(info["data"].get("timeStart")) is None or type(info["data"].get("timeStart")) is float: 
                                    rpc_info["start"] = info["data"].get("timeStart")
                                    if type(info["data"].get("timeStart")) is None: passed_data[data_names["timeStart"]] = f'None'
                                    else: passed_data[data_names["timeStart"]] = f'<t:{int(info["data"].get("timeStart"))}:R>'
                                if type(info["data"].get("timeEnd")) is int or type(info["data"].get("timeEnd")) is None or type(info["data"].get("timeEnd")) is float: 
                                    rpc_info["stop"] = info["data"].get("timeEnd")
                                    if type(info["data"].get("timeEnd")) is None: passed_data[data_names["timeEnd"]] = f'None'
                                    else: passed_data[data_names["timeEnd"]] = f'<t:{int(info["data"].get("timeEnd"))}:R>'
                                def getImageUrlFromAsset(assetId):
                                    url = f"https://thumbnails.roblox.com/v1/assets?assetIds={assetId}&returnPolicy=PlaceHolder&size=420x420&format=Png&isCircular=false"
                                    thumb_req = requests.get(url, loop_429=main_config.get("EFlagEnableLoop429Requests")==True, cookies=createCookieHeader())
                                    if thumb_req.ok:
                                        thumb_js = thumb_req.json
                                        if thumb_js and thumb_js.get("data"):
                                            if len(thumb_js.get("data")) > 0: return thumb_js.get("data")[0].get("imageUrl")
                                            else: return None
                                        else: return None
                                    else: return None
                                if type(info["data"].get("largeImage")) is dict: 
                                    if info["data"]["largeImage"].get("clear") == True or info["data"]["largeImage"].get("reset") == True:
                                        rpc_info["large_image"] = None
                                        rpc_info["large_text"] = None
                                        passed_data[data_names["largeImage"]] = f'None'
                                    else:
                                        link = info["data"]["largeImage"].get("assetId")
                                        approved_image = None
                                        if link and type(link) is int:
                                            approved_image = getImageUrlFromAsset(link)
                                            if approved_image: link = f"[Image]({approved_image})"
                                            else: link = "None"
                                        elif link and type(link) is str:
                                            try:
                                                parsed_link = urlparse(link)
                                                if parsed_link.netloc.endswith("roblox.com") or parsed_link.netloc.endswith("rbxcdn.com"):
                                                    approved_image = link
                                                    link = f"[Image]({link})"
                                                else: link = "None"
                                            except Exception as e: link = "None"
                                        else: link = "None"
                                        if approved_image: rpc_info["small_image"] = approved_image
                                        if type(info["data"]["largeImage"].get("hoverText")) is str: rpc_info["large_text"] = info["data"]["largeImage"]["hoverText"]
                                        passed_data[data_names["largeImage"]] = f'{info["data"]["largeImage"].get("hoverText", None)} | {link}'
                                elif type(info["data"].get("largeImage")) is None:
                                    rpc_info["large_image"] = None
                                    rpc_info["large_text"] = None
                                    passed_data[data_names["largeImage"]] = f'None'
                                if type(info["data"].get("smallImage")) is dict: 
                                    if info["data"]["smallImage"].get("clear") == True or info["data"]["smallImage"].get("reset") == True:
                                        rpc_info["small_image"] = None
                                        rpc_info["small_text"] = None
                                        passed_data[data_names["smallImage"]] = f'None'
                                    else:
                                        link = info["data"]["smallImage"].get("assetId")
                                        approved_image = None
                                        if link and type(link) is int:
                                            approved_image = getImageUrlFromAsset(link)
                                            if approved_image: link = f"[Image]({approved_image})"
                                            else: link = "None"
                                        elif link and type(link) is str:
                                            try:
                                                parsed_link = urlparse(link)
                                                if parsed_link.netloc.endswith("roblox.com") or parsed_link.netloc.endswith("rbxcdn.com"):
                                                    approved_image = link
                                                    link = f"[Image]({link})"
                                                else: link = "None"
                                            except Exception as e: link = "None"
                                        else: link = "None"
                                        if approved_image: rpc_info["small_image"] = approved_image
                                        if type(info["data"]["smallImage"].get("hoverText")) is str: rpc_info["small_text"] = info["data"]["smallImage"]["hoverText"]
                                        passed_data[data_names["smallImage"]] = f'{info["data"]["smallImage"].get("hoverText", None)} | {link}'
                                elif type(info["data"].get("smallImage")) is None:
                                    rpc_info["small_image"] = None
                                    rpc_info["small_text"] = None
                                    passed_data[data_names["smallImage"]] = f'None'
                                went_through = True
                    elif info["command"] == "SetLaunchData":
                        if rpc:
                            if rpc_info == None: rpc_info = {}
                            if type(info["data"]) is str: 
                                rpc_info["launch_data"] = info["data"]
                                passed_data[data_names["launch_data"]] = info["data"]
                            went_through = True
                    if went_through == True and disableWebhook == False and main_config.get("EFlagUseDiscordWebhook") == True and main_config.get("EFlagDiscordWebhookBloxstrapRPC") == True:
                        is_different = False
                        for i,v in before_data.items():
                            if not (before_data.get(i) == rpc_info.get(i)): is_different = True
                        for i,v in rpc_info.items():
                            if not (before_data.get(i) == rpc_info.get(i)): is_different = True
                        if is_different == False: return
                        if main_config.get("EFlagDiscordWebhookURL"):
                            thumbnail_url = f"{main_host}/Images/Bloxstrap.png"
                            embed_fields = [generateEmbedField(ts("Requested Command"), info["command"])]
                            for i, v in passed_data.items(): embed_fields.append(generateEmbedField(i, v))
                            generated_body = generateDiscordPayload(ts("Bloxstrap RPC Changed"), 12517631, embed_fields, thumbnail_url)
                            try: sendDiscordWebhook(generated_body, "onBloxstrapMessage")
                            except Exception as e: printDebugMessage(f"There was an issue sending your webhook message. Exception: \n{trace()}")
        def onAllRobloxEvents(data):
            if main_config.get("EFlagEnableMods") == True and main_config.get("EFlagSelectedModScripts") and len(selected_mod_scripts) > 0:
                for s in selected_mod_scripts:
                    if os.path.exists(os.path.join(mods_folder, "Mods", s, "Manifest.json")) and mods_manifest.get(s):
                        if mods_manifest[s].get("mod_script") == True:
                            try:
                                allowed_permissions = mods_manifest[s].get("permissions")
                                if "onRobloxLog" in allowed_permissions and hasattr(mod_script_modules[s], "onRobloxLog"): threading.Thread(target=getattr(mod_script_modules[s], "onRobloxLog"), args=[data], daemon=True).start()
                                if data.get("eventName") in allowed_permissions and hasattr(mod_script_modules[s], data.get("eventName")): threading.Thread(target=getattr(mod_script_modules[s], data.get("eventName")), args=[data["data"]], daemon=True).start()
                            except Exception as e: printDebugMessage(f"Something went wrong with pinging the Mod Script script: \n{trace()}")
        def onRobloxChannel(data):
            if data["channel"] == "production" or data["channel"] == "LIVE": url_channel = ""
            else: url_channel = data["channel"]
            printDebugMessage(f"Setting Channel Based on Client: {'production' if url_channel == '' else url_channel}")
            if main_os == "Darwin":
                res = plist_class.writePListFile(os.path.join(user_folder, "Library", "Preferences", "com.roblox.RobloxStudioChannel.plist" if run_studio == True else "com.roblox.RobloxPlayerChannel.plist"), {"www.roblox.com": url_channel}, binary=True, ns_mode=True)
                printDebugMessage(f"Channel Set Result: {res}")
            elif main_os == "Windows":
                reg = r"Software\ROBLOX Corporation\Environments\RobloxStudio\Channel" if run_studio == True else r"Software\ROBLOX Corporation\Environments\RobloxPlayer\Channel"
                try: registry_key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, reg, 0, win32con.KEY_SET_VALUE)
                except Exception: registry_key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, reg)
                win32api.RegSetValueEx(registry_key, "www.roblox.com", 0, win32con.REG_SZ, url_channel)
                win32api.RegCloseKey(registry_key)

        # Launch Roblox Client
        def runRobloxClient():
            global roblox_launched_affect_mod_script
            global connected_roblox_instance
            global connect_instead
            global custom_cookies
            roblox_launched_affect_mod_script = True
            def connectCallEvents(cri):
                if type(cri) is handler.RobloxInstance:
                    if run_studio == True:
                        cri.addRobloxEventCallback("onOpeningGame", onOpeningGame)
                        cri.addRobloxEventCallback("onRobloxExit", onRobloxExit)
                        cri.addRobloxEventCallback("onPlayTestStart", onPlayTestStart)
                        cri.addRobloxEventCallback("onGameJoined", onGameJoined)
                        cri.addRobloxEventCallback("onClosingGame", onClosingGame)
                        cri.addRobloxEventCallback("onRobloxAppStart", onRobloxAppStart)
                        cri.addRobloxEventCallback("onGameLoaded", onGameLoaded)
                        cri.addRobloxEventCallback("onLostConnection", onLostConnection)
                        cri.addRobloxEventCallback("onStudioInstallerLaunched", onStudioInstallerLaunched)
                        cri.addRobloxEventCallback("onRobloxCrash", onRobloxCrash)
                        cri.addRobloxEventCallback("onRobloxLog", onAllRobloxEvents)
                        cri.setRobloxEventCallback("onRobloxChannel", onRobloxChannel)
                        cri.addRobloxEventCallback("onPlayTestDisconnected", onPlayTestDisconnected)
                        cri.addRobloxEventCallback("onRobloxPublishing", onRobloxPublishing)
                        cri.addRobloxEventCallback("onRobloxSaved", onRobloxSaving)
                        cri.addRobloxEventCallback("onTeamCreateDisconnect", onTeamCreateDisconnect)
                        cri.addRobloxEventCallback("onTeamCreateConnect", onTeamCreateConnect)
                        cri.addRobloxEventCallback("onBloxstrapSDK", onBloxstrapMessage)
                        if not (main_config.get("EFlagDisableAutoOpenOrangeBloxFromStudio") == True): cri.addRobloxEventCallback("onNewStudioLaunching", onNewRobloxStudio)
                    else:
                        cri.setRobloxEventCallback("onRobloxAppStart", onRobloxAppStart)
                        cri.setRobloxEventCallback("onRobloxAppLoginFailed", onRobloxAppLoginFailed)
                        cri.setRobloxEventCallback("onRobloxExit", onRobloxExit)
                        cri.setRobloxEventCallback("onRobloxCrash", onRobloxCrash)
                        cri.setRobloxEventCallback("onRobloxLog", onAllRobloxEvents)
                        cri.setRobloxEventCallback("onBloxstrapSDK", onBloxstrapMessage)
                        cri.setRobloxEventCallback("onLoadedFFlags", onLoadedFFlags)
                        cri.setRobloxEventCallback("onGameStart", onGameStart)
                        cri.setRobloxEventCallback("onGameJoined", onGameJoined)
                        cri.setRobloxEventCallback("onGameDisconnected", onGameDisconnected)
                        cri.setRobloxEventCallback("onGameLoading", onMainServer)
                        cri.setRobloxEventCallback("onGameLoadingNormal", onMainServer)
                        cri.setRobloxEventCallback("onGameLoadingPrivate", onPrivateServer)
                        cri.setRobloxEventCallback("onRobloxChannel", onRobloxChannel)
                        cri.setRobloxEventCallback("onGameLoadingReserved", onReservedServer)
                        cri.setRobloxEventCallback("onGameLoadingParty", onPartyServer)
                        cri.setRobloxEventCallback("onGameTeleport", onTeleport)
                        cri.setRobloxEventCallback("onRobloxVoiceChatMute", onRobloxVoiceChatMute)
                        cri.setRobloxEventCallback("onRobloxVoiceChatUnmute", onRobloxVoiceChatUnmute)
                else: printDebugMessage("No RobloxInstance class was registered")
            if main_config.get("EFlagEnableEndingRobloxCrashHandler") == True: handler.endRobloxCrashHandler()
            if run_studio == True:
                if connect_instead == True:
                    connected_roblox_instance = handler.RobloxInstance(handler, handler.getLatestOpenedRobloxPid(studio=True), debug_mode=(main_config.get("EFlagEnableDebugMode") == True), allow_other_logs=(main_config.get("EFlagAllowFullDebugMode") == True), created_mutex=False, studio=True, await_log_creation=False)
                    if connected_roblox_instance:
                        connectCallEvents(connected_roblox_instance)
                        printSuccessMessage("Connected to Roblox Instance from log file for Activity Tracking!")
                        if connected_roblox_instance.created_mutex == True and main_os == "Windows": printSuccessMessage("Successfully connected for multi-instancing! Please know that this effect is active until all Roblox windows are closed or this bootstrap window is closed.")
                    else: printDebugMessage("No RobloxInstance class was registered")
                elif len(given_args) > 1:
                    url = given_args[1]
                    """
                    if main_os == "Darwin":
                        url_str = unquote(given_args[1])
                        if url_str:
                            url = unquote(url_str)
                        else:
                            url = ""
                    elif main_os == "Windows":
                        url = given_args[1]
                    """
                    if url:
                        for i, v in custom_cookies.items():
                            if os.path.exists(v): shutil.copy(v, i, follow_symlinks=False)
                        if url.startswith("efaz-bootstrap:") or url.startswith("orangeblox:"):
                            connected_roblox_instance = handler.openRoblox(
                                studio=True,
                                makeDupe=True, 
                                debug=(main_config.get("EFlagEnableDebugMode") == True), 
                                startData=f"{'--args ' if main_os == 'Darwin' and main_config.get('EFlagRobloxStudioArguments', '') != '' else ''}{main_config.get('EFlagRobloxStudioArguments', '')}",
                                attachInstance=(not (main_config.get("EFlagAllowActivityTracking") == False)), 
                                allowRobloxOtherLogDebug=(main_config.get("EFlagAllowFullDebugMode") == True)
                            )
                        else:
                            if main_os == "Windows" and "'" in url and os.path.exists(url): url = f"\"{url}\""
                            connected_roblox_instance = handler.openRoblox(
                                studio=True,
                                makeDupe=False if url.startswith("roblox-studio-auth:") else True, 
                                debug=(main_config.get("EFlagEnableDebugMode") == True), 
                                startData=f"{f'{url}' if main_os == 'Windows' else f'--args {url}'}{f' ' + main_config.get('EFlagRobloxStudioArguments', '') if main_config.get('EFlagRobloxStudioArguments') else ''}", 
                                attachInstance=False if url.startswith("roblox-studio-auth:") else (not (main_config.get("EFlagAllowActivityTracking") == False)), 
                                allowRobloxOtherLogDebug=(main_config.get("EFlagAllowFullDebugMode") == True)
                            )
                        if connected_roblox_instance:
                            connectCallEvents(connected_roblox_instance)
                            printSuccessMessage("Connected to Roblox Instance from log file for Activity Tracking!")
                            if connected_roblox_instance.created_mutex == True and main_os == "Windows": printSuccessMessage("Successfully connected for multi-instancing! Please know that this effect is active until all Roblox windows are closed or this bootstrap window is closed.")
                        else: printDebugMessage("No RobloxInstance class was registered")
                        check_update_thread = threading.Thread(target=checkIfUpdateWasNeeded)
                        check_update_thread.start()
                    else: printDebugMessage(f"Unable to format url scheme due to an issue.")
                else:
                    for i, v in custom_cookies.items():
                        if os.path.exists(v): shutil.copy(v, i, follow_symlinks=False)
                    connected_roblox_instance = handler.openRoblox(
                        studio=True,
                        makeDupe=True,
                        debug=(main_config.get("EFlagEnableDebugMode") == True), 
                        startData=f"{'--args ' if main_os == 'Darwin' and main_config.get('EFlagRobloxStudioArguments', '') != '' else ''}{main_config.get('EFlagRobloxStudioArguments', '')}",
                        attachInstance=(not (main_config.get("EFlagAllowActivityTracking") == False)), 
                        allowRobloxOtherLogDebug=(main_config.get("EFlagAllowFullDebugMode") == True)
                    )
                    if connected_roblox_instance:
                        connectCallEvents(connected_roblox_instance)
                        printSuccessMessage("Connected to Roblox Instance from log file for Activity Tracking!")
                    else: printDebugMessage("No RobloxInstance class was registered")
            else:
                if connect_instead == True:
                    connected_roblox_instance = handler.RobloxInstance(handler, handler.getLatestOpenedRobloxPid(), debug_mode=(main_config.get("EFlagEnableDebugMode") == True), allow_other_logs=(main_config.get("EFlagAllowFullDebugMode") == True), created_mutex=False, studio=False, await_log_creation=False)
                    if connected_roblox_instance:
                        connectCallEvents(connected_roblox_instance)
                        printSuccessMessage("Connected to Roblox Instance from log file for Activity Tracking!")
                        if connected_roblox_instance.created_mutex == True and main_os == "Windows": printSuccessMessage("Successfully connected for multi-instancing! Please know that this effect is active until all Roblox windows are closed or this bootstrap window is closed.")
                    else: printDebugMessage("No RobloxInstance class was registered")
                elif len(given_args) > 1:
                    url = given_args[1]
                    """
                    if main_os == "Darwin":
                        url_str = unquote(given_args[1])
                        if url_str: url = unquote(url_str)
                        else: url = ""
                    elif main_os == "Windows": url = given_args[1]
                    """
                    if url:
                        for i, v in custom_cookies.items():
                            if os.path.exists(v): shutil.copy(v, i, follow_symlinks=False)
                        if url.startswith("efaz-bootstrap:") or url.startswith("orangeblox:"):
                            connected_roblox_instance = handler.openRoblox(
                                forceQuit=(not (main_config.get("EFlagEnableDuplicationOfClients") == True)), 
                                makeDupe=(main_config.get("EFlagEnableDuplicationOfClients") == True), 
                                debug=(main_config.get("EFlagEnableDebugMode") == True), 
                                startData=f"{'--args ' if main_os == 'Darwin' and main_config.get('EFlagRobloxPlayerArguments', '') != '' else ''}{main_config.get('EFlagRobloxPlayerArguments', '')}",
                                attachInstance=(not (main_config.get("EFlagAllowActivityTracking") == False)), 
                                allowRobloxOtherLogDebug=(main_config.get("EFlagAllowFullDebugMode") == True)
                            )
                        else:
                            if main_os == "Windows" and "'" in url and os.path.exists(url): url = f"\"{url}\""
                            connected_roblox_instance = handler.openRoblox(
                                forceQuit=(not (main_config.get("EFlagEnableDuplicationOfClients") == True)), 
                                makeDupe=(main_config.get("EFlagEnableDuplicationOfClients") == True), 
                                debug=(main_config.get("EFlagEnableDebugMode") == True),
                                startData=f"{url}{'--args' if main_os == 'Darwin' and main_config.get('EFlagRobloxPlayerArguments', '') != '' else ''}{f' ' + main_config.get('EFlagRobloxPlayerArguments', '') if main_config.get('EFlagRobloxPlayerArguments') else ''}", 
                                attachInstance=(not (main_config.get("EFlagAllowActivityTracking") == False)), 
                                allowRobloxOtherLogDebug=(main_config.get("EFlagAllowFullDebugMode") == True)
                            )
                        if connected_roblox_instance:
                            connectCallEvents(connected_roblox_instance)
                            printSuccessMessage("Connected to Roblox Instance from log file for Activity Tracking!")
                            if connected_roblox_instance.created_mutex == True and main_os == "Windows": printSuccessMessage("Successfully connected for multi-instancing! Please know that this effect is active until all Roblox windows are closed or this bootstrap window is closed.")
                        else: printDebugMessage("No RobloxInstance class was registered")
                        check_update_thread = threading.Thread(target=checkIfUpdateWasNeeded)
                        check_update_thread.start()
                    else: printDebugMessage(f"Unable to format url scheme due to an issue.")
                elif multi_instance_enabled == True:
                    printDebugMessage(f"Opening extra Roblox window..")
                    for i, v in custom_cookies.items():
                        if os.path.exists(v): shutil.copy(v, i, follow_symlinks=False)
                    connected_roblox_instance = handler.openRoblox(
                        forceQuit=False,
                        makeDupe=True, 
                        startData=f"{'--args ' if main_os == 'Darwin' and main_config.get('EFlagRobloxPlayerArguments', '') != '' else ''}{main_config.get('EFlagRobloxPlayerArguments', '')}",
                        debug=(main_config.get("EFlagEnableDebugMode") == True), 
                        attachInstance=(not (main_config.get("EFlagAllowActivityTracking") == False)), 
                        allowRobloxOtherLogDebug=(main_config.get("EFlagAllowFullDebugMode") == True)
                    )
                    if connected_roblox_instance:
                        connectCallEvents(connected_roblox_instance)
                        printSuccessMessage("Connected to Roblox Instance from log file for Activity Tracking!")
                        if connected_roblox_instance.created_mutex == True and main_os == "Windows": printSuccessMessage("Successfully connected for multi-instancing! Please know that this effect is active until all Roblox windows are closed or this bootstrap window is closed.")
                    else: printDebugMessage("No RobloxInstance class was registered")
                    check_update_thread = threading.Thread(target=checkIfUpdateWasNeeded)
                    check_update_thread.start()
                else:
                    if handler.getIfRobloxIsOpen():
                        printMainMessage("An existing Roblox Window is currently open. Would you like to restart it in order for changes to take effect? (y/n)")
                        c = input("> ")
                        if isYes(c) == True: handler.endRoblox()
                        else: sys.exit(0)
                    for i, v in custom_cookies.items():
                        if os.path.exists(v): shutil.copy(v, i, follow_symlinks=False)
                    connected_roblox_instance = handler.openRoblox(
                        forceQuit=True, 
                        makeDupe=False,
                        startData=f"{'--args ' if main_os == 'Darwin' and main_config.get('EFlagRobloxPlayerArguments', '') != '' else ''}{main_config.get('EFlagRobloxPlayerArguments', '')}",
                        debug=(main_config.get("EFlagEnableDebugMode") == True), 
                        attachInstance=(not (main_config.get("EFlagAllowActivityTracking") == False)), 
                        allowRobloxOtherLogDebug=(main_config.get("EFlagAllowFullDebugMode") == True)
                    )
                    if connected_roblox_instance:
                        connectCallEvents(connected_roblox_instance)
                        printSuccessMessage("Connected to Roblox Instance from log file for Activity Tracking!")
                    else: printDebugMessage("No RobloxInstance class was registered")
                    check_update_thread = threading.Thread(target=checkIfUpdateWasNeeded)
                    check_update_thread.start()
        def checkIfUpdateWasNeeded():
            if main_config.get("EFlagDisableRobloxReinstallNeededChecks") == True: return
            global updated_count
            global skip_modification_mode
            global installed_update
            updated_count += 1
            if updated_count < 3:
                printMainMessage("Waiting 5 seconds to check if Roblox needs a reinstall..")
                time.sleep(5)
                if not (handler.getIfRobloxIsOpen(studio=run_studio)):
                    printMainMessage(f"Uh oh! An fresh reinstall is needed. Downloading a fresh copy of Roblox{' Studio' if run_studio == True else ''}!")
                    submit_status.start()
                    if run_studio == True: res = handler.installRoblox(studio=True, debug=(main_config.get("EFlagEnableDebugMode") == True), copyRobloxInstallerPath=(main_os == "Darwin" and os.path.join(cur_path, "RobloxStudioInstaller.app") or os.path.join(cur_path, "RobloxStudioInstaller.exe")), downloadInstaller=True, downloadToken=createDownloadToken(), verifyInstall=not (main_config.get("EFlagVerifyRobloxHashAfterInstall")==False))
                    else: res = handler.installRoblox(forceQuit=(not (main_config.get("EFlagEnableDuplicationOfClients") == True)), debug=(main_config.get("EFlagEnableDebugMode") == True), copyRobloxInstallerPath=(main_os == "Darwin" and os.path.join(cur_path, "RobloxPlayerInstaller.app") or os.path.join(cur_path, "RobloxPlayerInstaller.exe")), downloadToken=createDownloadToken(), downloadInstaller=True, verifyInstall=not (main_config.get("EFlagVerifyRobloxHashAfterInstall")==False))
                    submit_status.end()
                    if res and res["success"] == False:
                        printErrorMessage(f"There is an issue while trying to install Roblox{' Studio' if run_studio == True else ''}. Please try again by restarting this app!")
                        input("> ")
                        sys.exit(0)
                    time.sleep(5)
                    skip_modification_mode = False
                    installed_update = True
                    prepareRobloxClientWithErrorCatcher()
                    printSuccessMessage(f"Done! Roblox{' Studio' if run_studio == True else ''} is ready!")
                    time.sleep(2)
                    printWarnMessage(f"--- Running Roblox{' Studio' if run_studio == True else ''} ---")
                    runRobloxClient()
                else: printSuccessMessage(f"Roblox{' Studio' if run_studio == True else ''} doesn't require any updates!")
            else: printErrorMessage(f"Is {'Roblox Studio' if run_studio == True else 'Roblox Player'} crashing instantly..? Well, ending script here.")
        runRobloxClient()
        
        # End Script
        sys.exit(0)
    except (KeyboardInterrupt, Exception) as e:
        printErrorMessage("Uh oh! A Python exception that causes the script to end has occurred!")
        printErrorMessage(f"Exception: \n{trace()}")
        printErrorMessage(f"Location Code: 3")
        input("> ")
        sys.exit(0 if main_os == "Darwin" else 1)
else:
    # Detected as Module, Return with Exception
    class OrangeBloxNotModule(Exception):
        def __init__(self): super().__init__("OrangeBlox is only a runable instance, not a module.")
    class OrangeBloxInstallerNotModule(Exception):
        def __init__(self): super().__init__("The installer for OrangeBlox is only a runable instance, not a module.")
    class OrangeBloxLoaderNotModule(Exception):
        def __init__(self): super().__init__("The loader for OrangeBlox is only a runable instance, not a module.")
    raise OrangeBloxNotModule()