# 
# OrangeBlox 🍊
# Made by Efaz from efaz.dev
# v2.6.0k
# 

import os
import shutil
import json
import sys
import subprocess
import platform
import datetime
import logging
import hashlib
import typing
import time
import zlib
import re
import concurrent.futures
from urllib.parse import unquote, urlparse

from Modules.pkg import *
from Modules.printing import *
import Modules.config as cf

# Basic Functions
def isYes(text: str): return text.strip().lower() in cf._YES
def isNo(text: str): return text.strip().lower() in cf._NO
def isRequestClose(text: str): text = text.strip(); return text.lower() == "exit" or text.lower() == "exit()"
def makedirs(a: str): os.makedirs(a,exist_ok=True,mode=511)
    
# Awaiting Functions
if os.name == "nt":
    import msvcrt
    import ctypes
    def getNextKeyboardKey():
        key = msvcrt.getch()
        if key in (b'\x00', b'\xe0'):
            sub_key = msvcrt.getch()
            is_shift = bool(ctypes.windll.user32.GetAsyncKeyState(0x10) & 0x8000)
            if sub_key == b'H': return '_shift_up' if is_shift else '_up'
            elif sub_key == b'P': return '_shift_down' if is_shift else '_down'    
            elif sub_key == b'K': return '_shift_left' if is_shift else '_left'
            elif sub_key == b'M': return '_shift_right' if is_shift else '_right'
        elif key in (b'\r', b'\n'): return '_enter'
        elif key == b'\x03': raise KeyboardInterrupt
        elif key == b'\x08': return '_backspace'
        elif key == b'*': return '*'
        elif b'0' <= key <= b'9': return key.decode('utf-8')
        return None
else:
    import tty
    import termios
    import select
    def getNextKeyboardKey():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd) 
            select.select([fd], [], [])
            data = os.read(fd, 1024)
            if b'\x1b[1;2A' in data: return '_shift_up'
            if b'\x1b[1;2B' in data: return '_shift_down'
            if b'\x1b[1;2C' in data: return '_shift_right'
            if b'\x1b[1;2D' in data: return '_shift_left'
            if b'\x1b[A' in data: return '_up'
            if b'\x1b[B' in data: return '_down'
            if b'\x1b[C' in data: return '_right'
            if b'\x1b[D' in data: return '_left'
            if b'\r' in data or b'\n' in data: return '_enter'
            if b'\x03' in data: raise KeyboardInterrupt
            if b'\x7f' in data or b'\x08' in data: return '_backspace'
            if b'*' in data: return '*'
            if len(data) == 1 and b'0' <= data <= b'9': return data.decode('utf-8')
        finally: termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return None
def copyFile(pa, de):
    try:
        if os.path.exists(pa):
            destination_folder = f"{os.path.dirname(de)}"
            if os.path.exists(os.path.join(cf.cur_path, "ExportMode")):
                destination_dir = os.path.join(cf.cur_path, "ExportMode", os.path.dirname(de))
                if not os.path.exists(destination_dir):
                    makedirs(destination_dir)
                    printDebugMessage(f"Created directory: {destination_dir}")
                destination_path = os.path.join(cf.cur_path, "ExportMode", de)
                a = shutil.copy(pa, destination_path)
            if not os.path.exists(destination_folder):
                makedirs(destination_folder)
                printDebugMessage(f"Created directory: {destination_folder}")
            a = shutil.copy(pa, de)
            printDebugMessage(f"Copied File: {os.path.realpath(pa).replace(cf.cur_path, f'.')} => {os.path.realpath(de).replace(cf.cur_path, f'.')}")
            return a
        else:
            printDebugMessage(f"File not found: {os.path.realpath(pa)}")
            return None
    except Exception:
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
    return formatSize(total_size) if formatWithAbbreviation == True else total_size
def getFileSize(files, formatWithAbbreviation=True):
    total_size = 0
    for i in files: 
        if os.path.exists(i):
            if os.path.isdir(i): total_size += getFolderSize(i, formatWithAbbreviation=False)
            else: total_size += os.stat(i).st_size
    return formatSize(total_size) if formatWithAbbreviation == True else total_size
def getRobloxLogFolderSize(static=False):
    if cf.main_os == "Darwin":
        log_path = os.path.join(os.path.expanduser("~"), "Library", "Logs", "Roblox")
        if os.path.exists(log_path):
            return getFolderSize(log_path, formatWithAbbreviation=(static == False))
        else:
            if static == False: return ts("0 Bytes")
            else: return 0
    elif cf.main_os == "Windows":
        log_path = os.path.join(rbx.windows_dir, "logs")
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
                if isinstance(main_content, list): return main_content
                else: return None
            else:
                if isinstance(main_content, dict): return main_content
                else: return None
        except Exception: return None
    return None
def checkSyncFolder(path: typing.Optional[str]=None):
    sync_folder = path if path else cf.main_config.get("EFlagOrangeBloxSyncDir")
    return sync_folder and os.path.exists(sync_folder) and os.path.isdir(sync_folder) and not os.path.samefile(sync_folder, os.path.join(cf.cur_path)) and os.path.exists(os.path.join(sync_folder, "Configuration.json")) and os.path.exists(os.path.join(sync_folder, "Mods"))
def displayNotification(title="Unknown Title", message="Unknown Message"):
    try: cf.notification_socket.send("OrangeBloxAppNotification", {"title": title, "message": message, "authorization": cf.socket_authorization})
    except Exception: printErrorMessage(f"There was an error sending a notification. Error: \n{trace()}")
def generateFileHash(file_path: str, is_text: bool=False):
    try:
        sha_256 = hashlib.sha256()
        if is_text:
            with open(file_path, "r", encoding="utf-8", errors="ignore", newline="") as f:
                while True:
                    chunk = f.read(8192)
                    if not chunk: break
                    sha_256.update(chunk.encode("utf-8"))
        else:
            with open(file_path, "rb") as f:
                while True:
                    chunk = f.read(8192)
                    if not chunk: break
                    sha_256.update(chunk)
        return sha_256.hexdigest()
    except Exception: return None
def generateModsManifest():
    generated_manifest = {}
    mods_dir = os.path.join(cf.mods_folder, "Mods")
    if not os.path.exists(mods_dir): return generated_manifest
    if not (cf.main_config.get("EFlagEnabledMods") and isinstance(cf.main_config.get("EFlagEnabledMods"), dict)): cf.main_config["EFlagEnabledMods"] = {}
    enabled_mod_config = cf.main_config["EFlagEnabledMods"]
    zip_files_to_extract = []
    with os.scandir(mods_dir) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith(".zip"): zip_files_to_extract.append(entry.path)
    def extract_mod_zip(mod_path):
        file = os.path.basename(mod_path)
        dow_tar = os.path.join(mods_dir, file.split(".")[0])
        makedirs(dow_tar)
        zip_extract = cf.pip_class.unzipFile(
            mod_path, dow_tar, 
            look_for=["Manifest.json", "ModScript.py", "content", "ExtraContent"], 
            either=True, check=True
        )
        if zip_extract.returncode == 0:
            try: os.remove(mod_path)
            except OSError: pass
    if zip_files_to_extract:
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor: executor.map(extract_mod_zip, zip_files_to_extract)
    with os.scandir(mods_dir) as entries:
        for entry in entries:
            if not entry.is_dir(): continue
            i = entry.name
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
                "enabled": enabled_mod_config.get(i, False),
                "permissions": [],
                "python_modules": [],
                "python_version": "3.0.0"
            }
            mod_path = os.path.join(cf.mods_folder, "Mods", i)
            manifest_path = os.path.join(mod_path, "Manifest.json")
            mod_script_path = os.path.join(mod_path, "ModScript.py")
            if os.path.exists(os.path.join(mod_path, "StudioMod")): mod_info["is_studio_mod"] = True
            if os.path.exists(os.path.join(mod_path, "PlayerStudioSupported")): mod_info["both_supported"] = True
            if os.path.isfile(manifest_path):
                res_json = readJSONFile(manifest_path)
                if res_json:
                    if isinstance(res_json.get("name"), str): mod_info["name"] = res_json.get("name")
                    if isinstance(res_json.get("version"), str) and len(res_json.get("version")) < 10: mod_info["version"] = res_json.get("version")
                    if isinstance(res_json.get("mod_script"), bool): mod_info["mod_script"] = res_json.get("mod_script")
                    if isinstance(res_json.get("list_in_normal_mods"), bool): mod_info["list_in_normal_mods"] = res_json.get("list_in_normal_mods")
                    if isinstance(res_json.get("mod_script_requirements"), list):
                        for req in res_json.get("mod_script_requirements"):
                            if isinstance(req, str): mod_info["permissions"].append(req)
                    if isinstance(res_json.get("mod_script_supports"), str) and re.match(r'^\d+\.\d+\.\d+$', res_json.get("mod_script_supports")): mod_info["mod_script_supports"] = res_json.get("mod_script_supports")
                    if isinstance(res_json.get("mod_script_end_support"), str) and re.match(r'^\d+\.\d+\.\d+$', res_json.get("mod_script_end_support")): mod_info["mod_script_end_support"] = res_json.get("mod_script_end_support")
                    if isinstance(res_json.get("mod_script_end_support_reasoning"), str) and len(res_json.get("mod_script_end_support_reasoning")) < 250: mod_info["mod_script_end_support_reasoning"] = res_json.get("mod_script_end_support_reasoning")
                    if isinstance(res_json.get("python_version"), str) and re.match(r'^\d+\.\d+\.\d+(a\d+|b\d+|rc\d+)?$', res_json.get("python_version")): mod_info["python_version"] = res_json.get("python_version")
                    if cf.main_os == "Darwin" and res_json.get("mod_script_does_not_support_macos") == True: mod_info["mod_script_supports_operating_system"] = False
                    elif cf.main_os == "Windows" and res_json.get("mod_script_does_not_support_windows") == True: mod_info["mod_script_supports_operating_system"] = False
                    if res_json.get("is_studio_mod") == True: mod_info["is_studio_mod"] = True
                    if res_json.get("player_studio_support") == True: mod_info["both_supported"] = True
                    if isinstance(res_json.get("python_modules"), list):
                        for pyt in res_json.get("python_modules"):
                            if isinstance(pyt, str): mod_info["python_modules"].append(pyt)
                    mod_info["manifest_path"] = manifest_path
            if os.path.isfile(mod_script_path) and not os.path.islink(mod_script_path):
                contains_other_python_scripts = False
                for root, dirs, files in os.walk(mod_path):
                    for file in files:
                        if file.endswith(".py") and file != "ModScript.py":
                            contains_other_python_scripts = True
                            break
                    if contains_other_python_scripts: break
                if contains_other_python_scripts == True and not ("allowAccessingPythonFiles" in mod_info["permissions"]): mod_info["mod_script"] = False
                else:
                    with open(mod_script_path, "r", encoding="utf-8") as f: org_content = f.read()
                    for pe, va in rbx.roblox_event_info.items():
                        if va.get("detection") and va.get("detection") in org_content and not (pe in mod_info["permissions"]): mod_info["permissions"].append(pe)
                    if ("EfazRobloxBootstrapAPI" in org_content) and mod_info.get("mod_script_supports") < "1.3.0": mod_info["mod_script_supports"] = "1.3.0"
                    elif ("OrangeAPI" in org_content) and mod_info.get("mod_script_supports") < "2.0.0": mod_info["mod_script_supports"] = "2.0.0"
                    ms_contents = org_content
                    ms_contents = re.sub(r'^(import OrangeAPI|from OrangeAPI)', r'#\1', ms_contents, flags=re.MULTILINE)
                    ms_contents = ms_contents.replace("EfazRobloxBootstrapAPI", "OrangeAPI")
                    ms_contents = ms_contents.replace("from OrangeAPI import OrangeAPI;", "import OrangeAPI as orange; OrangeAPI = orange.OrangeAPI();").replace(" = OrangeAPI()", " = OrangeAPI")
                    modules_to_redirect = ["RobloxFastFlagsInstaller", "RobloxManager", "PipHandler", "PyKits", "Install", "Modules.", "Main", "builtins"]
                    for module in modules_to_redirect: ms_contents = ms_contents.replace(f"import {module}", "import OrangeAPI").replace(f"from {module}", "from OrangeAPI")
                    if ms_contents != org_content:
                        with open(mod_script_path, "w", encoding="utf-8") as f: f.write(ms_contents)
                    mod_info["mod_script_path"] = mod_script_path
                    mod_info["mod_script_hash"] = generateFileHash(mod_script_path, is_text=True)
            else: mod_info["mod_script"] = False
            generated_manifest[i] = mod_info
    return generated_manifest
def generateModOrder():
    mod_order = []
    if not cf.main_config.get("EFlagEnabledModOrder") or not isinstance(cf.main_config.get("EFlagEnabledModOrder"), list): cf.main_config["EFlagEnabledModOrder"] = []
    mod_order = cf.main_config["EFlagEnabledModOrder"]
    mods_manifest = generateModsManifest()
    for mod_id in mod_order:
        if not mods_manifest.get(mod_id) or not mods_manifest[mod_id].get("enabled", False):
            mod_order.remove(mod_id)
    for mod_id, mod_inf in mods_manifest.items():
        if mod_id not in mod_order and mod_inf.get("enabled", False):
            mod_order.append(mod_id)
    return mod_order
def getSettings(updating: bool=False):
    if cf.main_os == "Darwin":
        if os.path.exists(os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.robloxbootstrap.plist")): os.remove(os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.robloxbootstrap.plist"))
        macos_preference_expected = os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.orangeblox.plist")
        if os.path.exists(macos_preference_expected):
            app_configuration = cf.plist_class.readPListFile(macos_preference_expected)
            if app_configuration.get("Configuration"): cf.main_config = app_configuration.get("Configuration")
            else: cf.main_config = {}
        else: cf.main_config = {}
    else:
        with open(os.path.join(cf.cur_path, "Configuration.json"), "rb") as f: obfuscated_json = f.read()
        try: obfuscated_json = json.loads(obfuscated_json)
        except Exception: obfuscated_json = json.loads(zlib.decompress(obfuscated_json))
        cf.main_config = obfuscated_json
    if updating == False and cf.main_config.get("EFlagUseConfigurationWebServer") == True and cf.main_config.get("EFlagConfigurationWebServerURL"):
        try:
            req = cf.requests.get(cf.main_config.get("EFlagConfigurationWebServerURL") + cf.requests.format_params({"script": "main"}), headers={"X-Bootstrap-Version": cf.current_version["version"], "X-Python-Version": platform.python_version(), "X-Authorization-Key": cf.main_config.get("EFlagConfigurationAuthorizationKey", "")})
            if req.ok: 
                for i, v in req.json.items():
                    flag_type = cf.flag_types.get(i)
                    if flag_type and "_local" not in flag_type and not flag_type.startswith("path"): cf.main_config[i] = v
        except: pass
    cf.main_config = {
        i: v for i, v in cf.main_config.items() 
        if i in cf.flag_types and (
            (cf.flag_types[i] == "str" and isinstance(v, str)) or
            (cf.flag_types[i] == "path" and isinstance(v, str) and os.path.exists(v)) or
            (cf.flag_types[i] == "int" and isinstance(v, int)) or
            (cf.flag_types[i] == "float" and isinstance(v, float)) or
            (cf.flag_types[i] == "dict" and isinstance(v, dict)) or
            (cf.flag_types[i] == "bool" and isinstance(v, bool)) or
            (cf.flag_types[i] == "list" and isinstance(v, list))
        )
    }
    return cf.main_config
def saveSettings():
    respo = {
        "saved_normally": False,
        "sync_success": False
    }
    before_edit = cf.main_config.copy()
    getSettings()
    TYPE_MAP = {"str": str, "path": str, "int": int, "float": float, "dict": dict, "bool": bool, "list": list}
    new_dict = {}
    for k, v in before_edit.items():
        if k in cf.modified_flags_from_mod_scripts: v = cf.main_config.get(k)
        flag_type = cf.flag_types.get(k)
        if flag_type is None: continue
        expected_py_type = TYPE_MAP.get(flag_type)
        if expected_py_type and isinstance(v, expected_py_type):
            if flag_type == "path" and not os.path.exists(v): continue
            new_dict[k] = v
        elif cf.flag_types.get(flag_type) is not None: new_dict[flag_type] = v
    before_edit = new_dict
    cf.main_config = before_edit
    if cf.main_config.get("EFlagDisableAutosaveToInstallation") != True and checkSyncFolder():
        if os.path.exists(os.path.join(cf.main_config.get("EFlagOrangeBloxSyncDir"), 'Configuration.json')):
            with open(os.path.join(cf.main_config.get("EFlagOrangeBloxSyncDir"), 'Configuration.json'), "w", encoding="utf-8") as f: json.dump(cf.main_config, f, indent=4)
            respo["sync_success"] = True
        else: printErrorMessage("Bootstrap Sync is not supported since the original unextracted directory is not found.")
    if cf.main_os == "Darwin":
        if os.path.exists(os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.robloxbootstrap.plist")): os.remove(os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.robloxbootstrap.plist"))
        macos_preference_expected = os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.orangeblox.plist")
        if os.path.exists(macos_preference_expected): app_configuration = cf.plist_class.readPListFile(macos_preference_expected)
        else: app_configuration = {}
        app_configuration["InstalledAppPath"] = os.path.realpath(os.path.join(cf.macos_app_path, "../") + "/")
        app_configuration["Configuration"] = cf.main_config
        cf.plist_class.writePListFile(macos_preference_expected, app_configuration, binary=True)
    else:
        data_in_string = zlib.compress(json.dumps(cf.main_config).encode('utf-8'))
        with open(os.path.join(cf.cur_path, "Configuration.json"), "wb") as f: f.write(data_in_string)
    if cf.main_config.get("EFlagUseConfigurationWebServer") == True and cf.main_config.get("EFlagConfigurationWebServerURL"):
        req = cf.requests.post(cf.main_config.get("EFlagConfigurationWebServerURL") + cf.requests.format_params({"script": "main"}), cf.main_config, headers={"X-Bootstrap-Version": cf.current_version["version"], "X-Python-Version": platform.python_version(), "X-Authorization-Key": cf.main_config.get("EFlagConfigurationAuthorizationKey", "")})
        if not req.ok: respo["saved_normally"] = False
    respo["saved_normally"] = True
    return respo
def waitForInternet():
    if cf.pip_class.getIfConnectedToInternet() == False:
        printSystemMessage("--- Waiting for Internet ---")
        printMainMessage("Please connect to your internet in order to continue! If you're connecting to a VPN, try reconnecting.")
        while cf.pip_class.getIfConnectedToInternet() == False:
            time.sleep(0.05)
        return True
def generateCodesignCommand(pa, iden, entitlements: str=None, is_roblox: bool=False):
    commands = [["/usr/bin/xattr", "-cr", pa]]
    codesign_cmd = ["/usr/bin/codesign", "-f", "--deep", "--timestamp=none"]
    if entitlements: codesign_cmd.extend(["--entitlements", entitlements])
    codesign_cmd.extend(["-s", iden, pa])
    commands.append(codesign_cmd)
    return commands
def pythonVersionStr(): return f"{cf.pip_class.getCurrentPythonVersion()}{cf.pip_class.getIfPythonVersionIsBeta() and ' (BETA)' or ''}"
def validateInstallation(): return (cf.main_os == "Darwin" and os.path.exists(os.path.join(cf.macos_app_path, "Contents", "MacOS", "OrangeBlox"))) or (cf.main_os == "Windows" and os.path.exists(os.path.join(cf.cur_path, "OrangeBlox.exe")))
def safeConvertNumber(testing: str, type: typing.Type=int):
    try: return type(testing)
    except: return None
def createDownloadToken(studio: bool=None, binary_type: str="*"):
    if studio == None: studio = cf.run_studio
    if binary_type == "*": binary_type = cf.handler.getSystemBinaryType(studio=studio)
    if cf.main_config.get("EFlagRobloxSecurityCookieUsage") == True:
        requesting_channel = cf.handler.getUserChannel(studio=studio, debug=(cf.main_config.get("EFlagEnableDebugMode") == True), binary_type=binary_type)
        if requesting_channel.get("success") == True and requesting_channel.get("channel_name") != "LIVE":
            if requesting_channel.get("token"): cf.main_config["EFlagRobloxChannelUpdateToken"] = requesting_channel.get("token")
            return requesting_channel.get("token")
    elif cf.main_config.get("EFlagRobloxSecurityCookieUsage") != True and cf.main_config.get("EFlagRobloxChannelUpdateToken"):
        cf.main_config.pop("EFlagRobloxChannelUpdateToken")
    return None
def fetchRbxChannel(studio: bool=False):
    if cf.main_config.get("EFlagRobloxSecurityCookieUsage") == True:
        requesting_channel = cf.handler.getUserChannel(studio=cf.run_studio, debug=(cf.main_config.get("EFlagEnableDebugMode") == True))
        if requesting_channel.get("success") == True and requesting_channel.get("channel_name") != "LIVE": return requesting_channel.get("channel_name")
    r = cf.handler.getCurrentClientVersion(studio=studio)
    if r and r["success"] == True: return r["channel"]
    else: return "LIVE"
def createCookieHeader(studio: bool=None):
    if studio == None: studio = cf.run_studio
    if cf.main_config.get("EFlagRobloxSecurityCookieUsage") == True:
        return cf.handler.getRobloxCookieHeader(studio=studio)
    return {}
def generateFileKey(id: str, ext: str="", dire: str=""): 
    if dire: return os.path.join(dire, f"{id}_{cf.user_folder_name}{ext}")
    if cf.main_os == "Darwin":
        makedirs(cf.orangeblox_library)
        return os.path.join(cf.orangeblox_library, f"{id}{ext}")
    return os.path.join(cf.cur_path, f"{id}_{cf.user_folder_name}{ext}")
def generateMenuSelection(options: typing.List[typing.Dict[str, str]], before_input: str="", star_option: str="", send_input_response: bool=False, scripted_responses: typing.Dict[str, str]=None, start_index: int=None): 
    if scripted_responses is None: scripted_responses = {}
    options = sorted(options, key=lambda x: x.get("index", 0))
    sel_index = start_index if start_index is not None else (0 if star_option == "" or cf.main_config.get("EFlagBeginMenuCursorAtStart") else len(options))
    total_options = len(options)
    max_index = total_options if star_option != "" else total_options - 1
    sel_buffer = ""
    first_run = True
    if start_index is not None: sel_buffer = str(start_index + 1)
    while True:
        output_lines = []
        if before_input != "":
            output_lines.append(before_input)
            output_lines.append("") 
        for i, opt in enumerate(options):
            prefix = "[>] " if i == sel_index else f"[{i+1}] "
            output_lines.append(f"{prefix}{opt['message']}")
        if star_option != "":
            if sel_index == total_options: output_lines.append(f"[>] {star_option}")
            else: output_lines.append(f"[*] {star_option}")
        output_lines.append(f"> {sel_buffer}")
        lines_printed = len(output_lines) - 1 
        menu_text = "\n".join([f"\r\033[2K{cf.colors_class.wrap(line, 255)}" for line in output_lines])
        if not first_run: sys.__stdout__.write(f"\033[{lines_printed}A")
        first_run = False
        sys.__stdout__.write(menu_text)
        sys.__stdout__.flush()
        key = getNextKeyboardKey()
        if isinstance(key, bytes):
            try: key = key.decode("utf-8")
            except Exception: pass
        if key in scripted_responses:
            sys.__stdout__.write("\n")
            sys.__stdout__.flush()
            mode = scripted_responses[key]
            if sel_index == total_options:
                if send_input_response: return "*"
                return None
            else:
                if send_input_response: return str(sel_index + 1)
                ret = options[sel_index].copy()
                ret["target_mode"] = mode
                ret["current_index"] = sel_index
                return ret
        if key == "*":
            if star_option != "":
                sel_buffer = "*"
                sel_index = total_options
        elif key and key.isdigit():
            sel_buffer += key
            val = int(sel_buffer)
            sel_index = min(max_index, max(0, val - 1))
            if sel_buffer == "0":
                sel_buffer = ""
                sel_index = total_options
        elif key in ("_backspace", "\x7f", "\x08"):
            if sel_buffer:
                sel_buffer = sel_buffer[:-1]
                if sel_buffer:
                    val = int(sel_buffer)
                    sel_index = min(max_index, max(0, val - 1))
                else: sel_index = total_options
        if key == "_up": 
            if sel_index - 1 < 0: sel_index = max_index
            else: sel_index = max(0, sel_index - 1)
        elif key == "_down": 
            if sel_index + 1 > max_index: sel_index = 0
            else: sel_index = min(max_index, sel_index + 1)
        elif key == "_enter":
            sys.__stdout__.write("\n")
            sys.__stdout__.flush()
            if sel_index == total_options:
                if send_input_response: return "*"
                return None
            else:
                if send_input_response: return str(sel_index + 1)
                options[sel_index]["current_index"] = sel_index
                return options[sel_index]    
        sel_buffer = str(sel_index + 1) if sel_index < total_options else ""  
def setInstalledAppPath(install_app_path):
    if cf.main_os == "Darwin":
        if os.path.exists(os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.robloxbootstrap.plist")): os.remove(os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.robloxbootstrap.plist"))
        macos_preference_expected = os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.orangeblox.plist")
        plist_info = {}
        if os.path.exists(macos_preference_expected): plist_info = cf.plist_class.readPListFile(macos_preference_expected)
        plist_info["InstalledAppPath"] = install_app_path
        cf.plist_class.writePListFile(macos_preference_expected, plist_info, binary=True)
    elif cf.main_os == "Windows":
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
        except Exception: printErrorMessage("There was an error saving the assigned installed path!")
def startMessage(first: bool=False, ignore_support: bool=False):
    cf.stdout.clear()
    printSystemMessage("-----------")
    printSystemMessage(f"Welcome to {obName0()} {obName1()}!")
    if obName0() != "OrangeBlox" or obName1() != "🍊":
        printSystemMessage("Custom Theme of OrangeBlox 🍊")
    printSystemMessage("Made by Efaz from efaz.dev!")
    printSystemMessage(f"v{cf.current_version['version']}")
    printSystemMessage("-----------")

    # Requirement Checks
    if cf.main_os == "Windows": printMainMessage(f"System OS: {cf.main_os} ({platform.version()}) | Python Version: {pythonVersionStr()}")
    elif cf.main_os == "Darwin": printMainMessage(f"System OS: {cf.main_os} (macOS {platform.mac_ver()[0]}) | Python Version: {pythonVersionStr()}")
    else:
        printErrorMessage(f"{obName0()} is only supported for macOS and Windows.")
        input("> ")
        sys.exit(0)
    if ignore_support == False:
        if not cf.pip_class.osSupported(windows_build=17763, macos_version=(10,15,0)):
            if cf.main_os == "Windows": printErrorMessage(f"{obName0()} is only supported for Windows 10.0.17763 (October 2018) or higher. Please update your operating system in order to continue!")
            elif cf.main_os == "Darwin": printErrorMessage(f"{obName0()} is only supported for macOS 10.15 (Catalina) or higher. Please update your operating system in order to continue!")
            input("> ")
            sys.exit(0)
        if first == False and cf.main_config.get("EFlagEnableCPUMemoryUsageViewer", True) == True:
            try:
                virutal_memory = psutil.virtual_memory()
                cpu_percent = psutil.cpu_percent(interval=0.1)
                printMainMessage(f"CPU Percentage: {round(cpu_percent, 2)}% | Memory Usage: {formatSize(virutal_memory.total-virutal_memory.available)}/{formatSize(virutal_memory.total)}")
            except: printErrorMessage("CPU Percentage: Error | Memory Usage: Error")
        if not cf.pip_class.pythonSupported(3, 11, 0):
            if not cf.pip_class.pythonSupported(3, 6, 0):
                printErrorMessage("Please update your current installation of Python above 3.11.0")
                input("> ")
                sys.exit(0)
            else:
                latest_python = cf.pip_class.getLatestPythonVersion()
                printSystemMessage("--- Python Update Required ---")
                printMainMessage(f"Hello! In order to use {obName0()}, you'll need to install Python 3.11 or higher in order to continue. ")
                printMainMessage(f"If you wish, you may install Python {latest_python} by typing \"y\" and continue.")
                printMainMessage("Otherwise, you may close the app by just continuing without typing.")
                if isYes(input("> ")) == True:
                    cf.pip_class.pythonInstall(latest_python)
                    printSuccessMessage(f"If installed correctly, Python {latest_python} should be available to be used!")
                    printSuccessMessage("Please restart the script to install!")
                    input("> ")
                sys.exit(0)
    if first == False:
        if cf.main_os == "Windows":
            cf.content_folder_paths["Windows"] = cf.handler.getRobloxInstallFolder()
            cf.font_folder_paths["Windows"] = os.path.join(cf.content_folder_paths['Windows'], "content", "fonts")
            if not os.path.exists(cf.font_folder_paths["Windows"]):
                printErrorMessage(f"Please restart {obName0()} in order to reinstall Roblox!")
                input("> ")
                sys.exit(0)
        elif cf.main_os == "Darwin":
            if not os.path.exists(rbx.macOS_dir):
                printErrorMessage(f"Please restart {obName0()} in order to reinstall Roblox!")
                input("> ")
                sys.exit(0)
        installed_roblox_version = cf.handler.getCurrentClientVersion()
        if installed_roblox_version["success"] == True:
            installed_roblox_studio_version = cf.handler.getCurrentClientVersion(studio=True)
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
    def silent_logging_error_handler(self, record):
        try: sys.__stderr__.write(f"--- Logging Error: {record.getMessage()} ---\n")
        except Exception: pass
    logging.Handler.handleError = silent_logging_error_handler
    log_path = os.path.join(cf.cur_path, "Logs")
    if cf.main_os == "Darwin": log_path = os.path.join(cf.pip_class.getLocalAppData(), "Logs", "OrangeBlox")
    if not os.path.exists(log_path): os.makedirs(log_path,mode=511)
    generated_file_name = f'OrangeBlox_{handler_name}_{datetime.datetime.now().strftime("%B_%d_%Y_%H_%M_%S_%f")}.log' 
    if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding='utf-8')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    if cf.main_config.get("EFlagMakeMainBootstrapLogFiles") == True:
        file_handler = logging.FileHandler(os.path.join(log_path, generated_file_name), encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    stdout_stream = logging.StreamHandler(sys.stdout)
    stdout_stream.setLevel(logging.INFO)
    stdout_stream.setFormatter(logging.Formatter("%(message)s"))
    if cf.main_config.get("EFlagMakeMainBootstrapLogFiles") == True: logger.addHandler(file_handler)
    logger.addHandler(stdout_stream)
    sys.stdout = PyKits.stdout(logger, logging.INFO, lang=cf.main_config.get("EFlagSelectedBootstrapLanguage", "en"))
    sys.stderr = PyKits.stdout(logger, logging.ERROR, lang=cf.main_config.get("EFlagSelectedBootstrapLanguage", "en"))
    cf.stdout = sys.stdout
    if cf.main_os == "Windows": cf.colors_class.fix_windows_ansi()
    return True
def createWindowsShortcut(shell, target_path, shortcut_path, working_directory=None, icon_path=None, arguments=None):
    if not os.path.exists(os.path.dirname(shortcut_path)): os.makedirs(os.path.dirname(shortcut_path),mode=511)
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = target_path
    if arguments: shortcut.Arguments = arguments
    if working_directory: shortcut.WorkingDirectory = working_directory
    if icon_path: shortcut.IconLocation = icon_path
    shortcut.Save()
    del shortcut
def checkMacOSCodesign(app_path: str=None, silent: bool=False):
    try:
        if not app_path or not os.path.isfile(app_path): return False
        result = subprocess.run(
            ["/usr/bin/codesign", "-v", app_path],
            stdout=subprocess.DEVNULL if silent else subprocess.PIPE,
            stderr=subprocess.DEVNULL if silent else subprocess.PIPE
        )   
        printDebugMessage(f"Code Signing Validation Response: {result.returncode}")
        return result.returncode == 0
    except Exception:
        printDebugMessage(f"Unable to validate codesign: \n{trace()}")
        return False
def createMacOSCodesign(app_path: str=None, identity: str=None, entitlements: str=None, run_only: bool=False, is_roblox: bool=False):
    if not app_path: return None
    result = None
    for i in generateCodesignCommand(app_path, identity, entitlements=entitlements, is_roblox=is_roblox): 
        if i[0] == "/usr/bin/xattr" or run_only: result = subprocess.run(i, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else: result = subprocess.Popen(i, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); result.wait()
    return result
if __name__ == "__main__":
    print("This module is not a runable instance.")
    sys.exit(1)