# 
# OrangeBlox 🍊
# Made by Efaz from efaz.dev
# v2.6.0e
# 

import Modules.config as cf
from Modules.printing import *
from Modules.roblox import *
from Modules.utils import *
import os
import queue
import json
import datetime
import importlib.util
import re

# Mod Script Runtime
def setBaseVariables():
    OrangeAPI.cached_information = {}
    OrangeAPI.translators = {}
    OrangeAPI.debug_mode = (cf.main_config.get("EFlagEnableDebugMode")==True)
    OrangeAPI.studio_mode = cf.run_studio==True
    OrangeAPI.launched_from_bootstrap = True
    OrangeAPI.current_version["bootstrap_version"] = cf.current_version["version"]
def loadModScript(sel_mo: str):
    if os.path.exists(os.path.join(cf.mods_folder, "Mods", sel_mo, "Manifest.json")):
        rcf.mod_script_jsons[sel_mo] = readJSONFile(os.path.join(cf.mods_folder, "Mods", sel_mo, "Manifest.json"))
        if rcf.mod_script_jsons.get(sel_mo):
            if rcf.mods_manifest.get(sel_mo) and rcf.mods_manifest.get(sel_mo).get("mod_script") == True:
                printMainMessage(f"Preparing Mod Script ({sel_mo})..")
                mod_manifest = rcf.mods_manifest.get(sel_mo)
                if mod_manifest["mod_script_supports"] <= cf.current_version["version"] and mod_manifest["mod_script_end_support"] > cf.current_version["version"] and mod_manifest["mod_script_supports_operating_system"] == True and mod_manifest["python_version"] <= cf.pip_class.getCurrentPythonVersion():
                    def s(sel_mod):
                        nonlocal mod_manifest
                        with open(os.path.join(cf.mods_folder, "Mods", sel_mod, "ModScript.py"), "r", encoding="utf-8") as f: mod_script_text = f.read()
                        approved_items_list = cf.main_config.get('EFlagSelectedModScripts').get(sel_mod).get("permissions", [])
                        approved_through_scan = True

                        for i, v in cf.handler.roblox_event_info.items():
                            if v.get("detection") and v.get("detection") in mod_script_text and (not (i in approved_items_list)): approved_through_scan = False
                        if mod_manifest.get("permissions"):
                            for i in mod_manifest["permissions"]:
                                if not i in approved_items_list: approved_through_scan = False
                        if mod_manifest.get("python_modules"):
                            for i in mod_manifest["python_modules"]:
                                if not f"pip_{i}" in approved_items_list: approved_through_scan = False
                        mod_script_detail = cf.main_config.get('EFlagSelectedModScripts').get(sel_mo)
                        if mod_manifest["mod_script_hash"] != mod_script_detail.get("hash", ""): approved_through_scan = False; printDebugMessage(f"Unable to validate hash: {mod_manifest['mod_script_hash']} => {cf.main_config.get('EFlagSelectedModScripts').get(sel_mo).get('hash', '')}")
                        if approved_through_scan == True:
                            if mod_manifest.get("python_modules"):
                                printDebugMessage("Validating Installation of Mod Script Modules..")
                                if not cf.pip_class.installed(mod_manifest.get("python_modules", []), boolonly=True): cf.pip_class.install(mod_manifest.get("python_modules", []))
                            printDebugMessage("Initalizing Components..")
                            script_path = os.path.join(cf.mods_folder, "Mods", sel_mod, "ModScript.py")
                            try:
                                # Create API Copy
                                rcf.generated_secret_keys[sel_mod] = os.urandom(3).hex()
                                rcf.generated_api_instances[sel_mod] = OrangeAPI.OrangeAPI(OrangeAPI.OrangeAPIDetails(sel_mod, rcf.generated_secret_keys[sel_mod]))
                                OrangeAPI.request_queues[sel_mod] = queue.Queue()
                                
                                translation_path = os.path.join(cf.mods_folder, "Mods", sel_mod, "Translations", cf.main_config.get("EFlagSelectedBootstrapLanguage", "en") + ".json")
                                if os.path.exists(translation_path): OrangeAPI.translators[sel_mod] = PyKits.Translator(lang=translation_path)
                                else: OrangeAPI.translators[sel_mod] = cf.stdout.translation_obj
                                rcf.orangeapi_modules[sel_mod] = OrangeAPI

                                # Load Mod Script
                                with open(script_path, "r", encoding="utf-8") as f: org_content = f.read()
                                ms_contents = org_content
                                ms_contents = re.sub(r'^(import OrangeAPI|from OrangeAPI)', r'#\1', ms_contents, flags=re.MULTILINE)
                                ms_contents = ms_contents.replace("EfazRobloxBootstrapAPI", "OrangeAPI")
                                ms_contents = ms_contents.replace("from OrangeAPI import OrangeAPI;", "import OrangeAPI as orange; OrangeAPI = orange.OrangeAPI();").replace(" = OrangeAPI()", " = OrangeAPI")
                                modules_to_redirect = ["RobloxManager", "RobloxFastFlagsInstaller", "PipHandler", "PyKits", "Install", "Modules.", "Main", "builtins"]
                                for module in modules_to_redirect: ms_contents = ms_contents.replace(f"import {module}", "import OrangeAPI").replace(f"from {module}", "from OrangeAPI")
                                if ms_contents != org_content:
                                    with open(script_path, "w", encoding="utf-8") as f: f.write(ms_contents)
                                spec = importlib.util.spec_from_file_location(f"ModScript_{sel_mod}", script_path)
                                rcf.mod_script_modules[sel_mod] = importlib.util.module_from_spec(spec)
                                proxy_api = OrangeAPI.OrangeAPIProxy(rcf.generated_api_instances[sel_mod])
                                setattr(rcf.mod_script_modules[sel_mod], "OrangeAPI", proxy_api)
                                
                                undefined_func = {
                                    "endRoblox": cf.handler.endRobloxStudio if cf.run_studio==True else cf.handler.endRoblox,
                                    "endOppositeRoblox": cf.handler.endRoblox if cf.run_studio==True else cf.handler.endRobloxStudio,
                                    "getIfRobloxIsOpen": cf.handler.getIfRobloxStudioIsOpen if cf.run_studio==True else cf.handler.getIfRobloxIsOpen,
                                    "getInstalledRobloxVersion": cf.handler.getCurrentStudioClientVersion if cf.run_studio==True else cf.handler.getCurrentClientVersion,
                                    "getOppositeInstalledRobloxVersion": cf.handler.getCurrentClientVersion if cf.run_studio==True else cf.handler.getCurrentStudioClientVersion,
                                    "getInstalledRobloxStudioVersion": cf.handler.getCurrentStudioClientVersion,
                                    "getInstalledRobloxPlayerVersion": cf.handler.getCurrentClientVersion,
                                    "getRobloxInstallFolder": cf.handler.getRobloxInstallFolder,
                                    "getLatestRobloxPid": cf.handler.getLatestOpenedRobloxStudioPid if cf.run_studio==True else cf.handler.getLatestOpenedRobloxPid,
                                    "getOpenedRobloxPids": cf.handler.getOpenedRobloxStudioPids if cf.run_studio==True else cf.handler.getOpenedRobloxPids,
                                    "getIfOSSupported": cf.pip_class.osSupported,
                                    "getIfPythonSupported": cf.pip_class.pythonSupported,
                                    "getIfConnectedToInternet": cf.pip_class.getIfConnectedToInternet,
                                    "getIf32BitWindows": cf.pip_class.getIf32BitWindows,
                                    "getRequest": cf.requests.get,
                                    "postRequest": cf.requests.post,
                                    "deleteRequest": cf.requests.delete,
                                    "getOrangeBloxName": obName0,
                                    "getOrangeBloxEmoji": obName1,
                                    "getOrangeBloxColorAnsi": obColorA,
                                    "getOrangeBloxColorHex": obColorH,
                                }
                                func_list = dict(defined_func)
                                func_list.update(undefined_func)
                                
                                # Set and Handle API to Mod Script
                                def handleRequests(selected_mod_scriptt, approved_lis):
                                    queue_block = rcf.orangeapi_modules[selected_mod_scriptt].request_queues[selected_mod_scriptt]
                                    while True:
                                        try:
                                            v = queue_block.get()
                                            if v is None: break
                                            if type(v) is rcf.orangeapi_modules[selected_mod_scriptt].Request:
                                                identification = v.id.split("|")
                                                if identification[0] != selected_mod_scriptt:
                                                    queue_block.task_done()
                                                    continue
                                                try:
                                                    if ((v.requested in approved_lis) or (cf.handler.roblox_event_info.get(v.requested, {"free": False}).get("free") == True)) and (v.fulfilled == False):
                                                        if identification[1] == rcf.generated_secret_keys[identification[0]]:
                                                            if v and func_list.get(v.requested):
                                                                if v and v.fulfilled == False:
                                                                    try:
                                                                        if undefined_func.get(v.requested):
                                                                            if type(v.args) is list: val = func_list.get(v.requested)(*(v.args))
                                                                            elif type(v.args) is dict: val = func_list.get(v.requested)(**(v.args))
                                                                            else: val = func_list.get(v.requested)()
                                                                        else:
                                                                            if type(v.args) is list: val = func_list.get(v.requested)(identification[0], *(v.args))
                                                                            elif type(v.args) is dict: val = func_list.get(v.requested)(identification[0], **(v.args))
                                                                            else: val = func_list.get(v.requested)(identification[0])
                                                                        v.complete_request(code=0, value=val)
                                                                    except Exception: v.complete_request(code=1)
                                                                    queue_block.task_done()
                                                            else:
                                                                v.complete_request(code=3)
                                                                queue_block.task_done()
                                                        else:
                                                            v.complete_request(code=7)
                                                            queue_block.task_done()
                                                    else:
                                                        v.complete_request(code=2)
                                                        queue_block.task_done()
                                                        printDebugMessage(f"This mod script ({selected_mod_scriptt}) is requesting use of a function ({v.requested}) that is not permitted. Please check Manifest.json and verify using the Mod Manager!")
                                                except Exception:
                                                    v.complete_request(code=4)
                                                    queue_block.task_done()
                                                    printDebugMessage(f"Something went wrong with pinging the mod script {selected_mod_scriptt}: \n{trace()}")
                                        except Exception:
                                            resulting_err = trace()
                                            printDebugMessage(f"Error from Mod Script module: \n{resulting_err}")
                                            printErrorMessage(f"Ended accepting requests from Mod Scripts ({selected_mod_scriptt}) due to an issue. | Code: 1")
                                def setPythonAPIs(selected_mod_scripttt, apr_li):
                                    # Set and Handle Printing Functions
                                    def handlePrint(mes): printMainMessage(f"[MOD SCRIPT]: {mes}")
                                    def empty_str(*args, **kwargs): return ""
                                    def empty(*args, **kwargs): return None
                                    def open_config(*args, **kwargs):
                                        mod_script_config = {}
                                        config_path = os.path.join(cf.mods_folder, "Mods", selected_mod_scripttt, f"Configuration_{cf.user_folder_name}")
                                        if os.path.exists(config_path):
                                            try:
                                                with open(config_path, "r", encoding="utf-8") as f: mod_script_config = json.load(f)
                                            except Exception: printDebugMessage("Invalid Mod Script Configuration, returned blank.")
                                        return mod_script_config 
                                    if not (("grantMaximumAbility" in apr_li)):
                                        setattr(rcf.mod_script_modules[selected_mod_scripttt], "print", handlePrint)
                                        setattr(rcf.mod_script_modules[selected_mod_scripttt], "input", empty_str)
                                        setattr(rcf.mod_script_modules[selected_mod_scripttt], "write", empty)
                                        if not ("grantFileEditing" in apr_li or cf.handler.roblox_event_info.get("grantFileEditing", {"free": False}).get("free") == True): setattr(rcf.mod_script_modules[sel_mod], "open", open_config)
                                        setattr(rcf.mod_script_modules[selected_mod_scripttt], "exec", None)
                                        setattr(rcf.mod_script_modules[selected_mod_scripttt], "eval", None)
                                        setattr(rcf.mod_script_modules[selected_mod_scripttt], "setattr", empty)
                                        setattr(rcf.mod_script_modules[selected_mod_scripttt], "__import__", empty)

                                # Launch API
                                cf.pip_class.startThread(setPythonAPIs, True, sel_mod, list(approved_items_list))
                                cf.pip_class.startThread(handleRequests, True, sel_mod, list(approved_items_list))
                                printDebugMessage(f"Launched OrangeAPI v{OrangeAPI.current_version['version']}!")
                                
                                # Launch Script
                                printDebugMessage("Starting Mod Script..")
                                spec.loader.exec_module(rcf.mod_script_modules[sel_mod])
                                printSuccessMessage("Successfully connected to script!")
                            except Exception:
                                printDebugMessage(f"Error from Mod Script module: \n{trace()}")
                                printErrorMessage("Something went wrong while connecting to the Mod Script script!")
                        else:
                            if cf.skip_modification_mode: printErrorMessage("Please reverify this mod script in settings in order to continue!")
                            else:
                                printErrorMessage("Please reverify this mod script in order to continue!")
                                from Modules.menu import continueToModsManager
                                resb = continueToModsManager(reverify_mod_script=sel_mod)
                                if resb == 5: return
                                else: mod_manifest = generateModsManifest().get(sel_mod); s(sel_mod)
                    s(str(sel_mo))
                else:
                    printMainMessage("This mod script is no longer support because of the following reasons:")
                    if mod_manifest["mod_script_supports"] > cf.current_version["version"]: printYellowMessage(f"- This mod script requests a newer version of {obName0()}. Please update to {obName0()} v{mod_manifest['mod_script_supports']}")
                    if mod_manifest["python_version"] > cf.pip_class.getCurrentPythonVersion(): printYellowMessage(f"- This mod script requires a newer version of Python. Please update to {mod_manifest['python_version']}")
                    if mod_manifest["mod_script_supports_operating_system"] == False:
                        if cf.main_os == "Darwin": printYellowMessage(f"- This mod script is only supported for Windows!")
                        elif cf.main_os == "Windows": printYellowMessage(f"- This mod script is only supported for macOS!")
                        else: printYellowMessage(f"- This mod script is only supported for macOS or Windows!")
                    if mod_manifest["mod_script_supports"] > cf.current_version["version"] or mod_manifest["mod_script_end_support"] <= cf.current_version["version"]:
                        printYellowMessage(f"- This mod script has reached their end support! Creator Note:")
                        printYellowMessage(mod_manifest["mod_script_end_support_reasoning"])
            else: printErrorMessage("Unable to find mod script under manifest.")
def loadModScripts():
    if cf.main_config.get("EFlagEnableMods") == True:
        if rcf.selected_mod_scripts and cf.main_config.get("EFlagAllowActivityTracking") != False and len(rcf.selected_mod_scripts) > 0:
            setBaseVariables()
            for sel_mo in rcf.selected_mod_scripts: loadModScript(sel_mo)

# Mod Script Functions
def getMainConf(scri: str): 
    filtered_fflag = {}
    restricted_fflags = ["EFlagDiscordWebhookURL", "EFlagRobloxLinkShortcuts"]
    for i, v in cf.main_config.items():
        if not (i in restricted_fflags): filtered_fflag[i] = v
    return filtered_fflag
def getFF(scri: str): 
    if cf.run_studio == True: return cf.main_config.get("EFlagRobloxStudioFlags", {})
    else: return cf.main_config.get("EFlagRobloxPlayerFlags", {})
def setMainConf(scri: str, js: dict, full=False): 
    if type(js) is dict:
        before_config = cf.main_config
        if full == True: 
            cf.main_config = js
            for i in before_config.keys(): 
                if not cf.main_config.get(i): cf.modified_flags_from_mod_scripts.append(i)
        else:
            for i, v in js.items(): cf.main_config[i] = v
        for i in js.keys(): 
            if not i in cf.modified_flags_from_mod_scripts: cf.modified_flags_from_mod_scripts.append(i)
def setFF(scri: str, js: dict, full=False): 
    if type(js) is dict:
        if full == True: 
            if cf.run_studio == True: cf.main_config["EFlagRobloxStudioFlags"] = js
            else: cf.main_config["EFlagRobloxPlayerFlags"] = js
        else:
            cf.main_config["EFlagRobloxPlayerFlags"] = cf.main_config.get("EFlagRobloxPlayerFlags", {})
            cf.main_config["EFlagRobloxStudioFlags"] = cf.main_config.get("EFlagRobloxStudioFlags", {})
            for i, v in js.items(): 
                if cf.run_studio == True: cf.main_config["EFlagRobloxStudioFlags"][i] = v
                else: cf.main_config["EFlagRobloxPlayerFlags"][i] = v
        if cf.run_studio == True and not "EFlagRobloxStudioFlags" in cf.modified_flags_from_mod_scripts: cf.modified_flags_from_mod_scripts.append("EFlagRobloxStudioFlags")
        elif not "EFlagRobloxPlayerFlags" in cf.modified_flags_from_mod_scripts: cf.modified_flags_from_mod_scripts.append("EFlagRobloxPlayerFlags")
        filtered_fast_flags = {}
        if cf.run_studio == True and cf.main_config.get("EFlagRobloxStudioFlags"):
            for i, v in cf.main_config.get("EFlagRobloxStudioFlags").items():
                if i and (not i.startswith("EFlag")): filtered_fast_flags[i] = v
        elif cf.run_studio == False and cf.main_config.get("EFlagRobloxPlayerFlags"):
            for i, v in cf.main_config.get("EFlagRobloxPlayerFlags").items():
                if i and (not i.startswith("EFlag")): filtered_fast_flags[i] = v
        cf.handler.installFastFlags(filtered_fast_flags, debug=(cf.main_config.get("EFlagEnableDebugMode") == True), endRobloxInstances=False, studio=cf.run_studio)
def saveMainConf(scri: str, js: dict, full=False): 
    if type(js) is dict:
        if full == True:
            filtered_fflag = {}
            filtered_fflag["EFlagRobloxPlayerFlags"] = cf.main_config.get("EFlagRobloxPlayerFlags", {})
            filtered_fflag["EFlagRobloxStudioFlags"] = cf.main_config.get("EFlagRobloxStudioFlags", {})
            for i, v in js.items():
                if not ("EFlag" in i): 
                    if cf.run_studio == True: filtered_fflag["EFlagRobloxStudioFlags"][i] = v
                    else: filtered_fflag["EFlagRobloxPlayerFlags"][i] = v
                else: cf.main_config[i] = v
            cf.main_config = filtered_fflag
        else:
            cf.main_config["EFlagRobloxPlayerFlags"] = cf.main_config.get("EFlagRobloxPlayerFlags", {})
            cf.main_config["EFlagRobloxStudioFlags"] = cf.main_config.get("EFlagRobloxStudioFlags", {})
            for i, v in js.items():
                if not ("EFlag" in i):
                    if cf.run_studio == True: cf.main_config["EFlagRobloxStudioFlags"][i] = v
                    else: cf.main_config["EFlagRobloxPlayerFlags"][i] = v
                else: cf.main_config[i] = v
        if cf.run_studio == True and "EFlagRobloxStudioFlags" in cf.modified_flags_from_mod_scripts: cf.modified_flags_from_mod_scripts.remove("EFlagRobloxStudioFlags")
        elif "EFlagRobloxPlayerFlags" in cf.modified_flags_from_mod_scripts: cf.modified_flags_from_mod_scripts.remove("EFlagRobloxPlayerFlags")
        saveSettings()
def saveFF(scri: str, js: dict, full=False):
    if type(js) is dict:
        if full == True: 
            if cf.run_studio == True: cf.main_config["EFlagRobloxStudioFlags"] = js
            else: cf.main_config["EFlagRobloxPlayerFlags"] = js
        else:
            cf.main_config["EFlagRobloxPlayerFlags"] = cf.main_config.get("EFlagRobloxPlayerFlags", {})
            cf.main_config["EFlagRobloxStudioFlags"] = cf.main_config.get("EFlagRobloxStudioFlags", {})
            for i, v in js.items(): 
                if cf.run_studio == True: cf.main_config["EFlagRobloxStudioFlags"][i] = v
                else: cf.main_config["EFlagRobloxPlayerFlags"][i] = v
        filtered_fast_flags = {}
        if cf.run_studio == True and cf.main_config.get("EFlagRobloxStudioFlags"):
            for i, v in cf.main_config.get("EFlagRobloxStudioFlags").items():
                if i and (not i.startswith("EFlag")): filtered_fast_flags[i] = v
        elif cf.run_studio == False and cf.main_config.get("EFlagRobloxPlayerFlags"):
            for i, v in cf.main_config.get("EFlagRobloxPlayerFlags").items():
                if i and (not i.startswith("EFlag")): filtered_fast_flags[i] = v
        cf.handler.installFastFlags(filtered_fast_flags, debug=(cf.main_config.get("EFlagEnableDebugMode") == True), endRobloxInstances=False, studio=cf.run_studio)
        saveSettings()
def sendBloxstrapRPC(scri: str, info: dict, disableWebhook: bool=True): onBloxstrapMessage(info, disableWebhook)
def getDebugMode(scri: str): return (cf.main_config.get("EFlagEnableDebugMode") == True)
def getConfiguration(scri: str, name: str="*"):
    if type(name) is str:
        mod_script_config = {}
        config_path = os.path.join(cf.mods_folder, "Mods", scri, f"Configuration_{cf.user_folder_name}")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f: mod_script_config = json.load(f)
            except Exception: printDebugMessage("Invalid mod script configuration, returned blank.")
        if name == "*": return mod_script_config
        else: return mod_script_config.get(name)
    else: return None
def setRobloxWindowTitle(scri: str, title: str):
    if type(title) is str:
        if rcf.connected_roblox_instance:
            windows_opened = rcf.connected_roblox_instance.getWindowsOpened()
            if len(windows_opened) > 0:
                for win in windows_opened: win.setWindowTitle(title)
            else: raise Exception("No Roblox Windows found!")
        else: raise Exception("Connected Roblox Instance is not found!")
    else: raise Exception("Provided arguments are invalid!")
def setRobloxWindowIcon(scri: str, icon: str):
    if type(icon) is str:
        if rcf.connected_roblox_instance:
            windows_opened = rcf.connected_roblox_instance.getWindowsOpened()
            if len(windows_opened) > 0:
                for win in windows_opened: win.setWindowIcon(icon)
            else: raise Exception("No Roblox Windows found!")
        else: raise Exception("Connected Roblox Instance is not found!")
    else: raise Exception("Provided arguments are invalid!")
def focusRobloxWindow(scri: str):
    if rcf.connected_roblox_instance:
        windows_opened = rcf.connected_roblox_instance.getWindowsOpened()
        if len(windows_opened) > 0:
            for win in windows_opened: win.focusWindow()
        else: raise Exception("No Roblox Windows found!")
    else: raise Exception("Connected Roblox Instance is not found!")
def getIfRobloxLaunched(scri: str): return rcf.roblox_launched_affect_mod_script == True
def getRobloxAppSettings(scri: str):
    a = cf.handler.getRobloxAppSettings()
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
        if rcf.connected_roblox_instance:
            windows_opened = rcf.connected_roblox_instance.getWindowsOpened()
            if len(windows_opened) > 0:
                for win in windows_opened:
                    win.setWindowPositionAndSize(size_x, size_y, position_x, position_y)
            else: raise Exception("No Roblox Windows found!")
        else: raise Exception("Connected Roblox Instance is not found!")
    else: raise Exception("Provided arguments are invalid!")
def setConfiguration(scri: str, name: str="*", data=None):
    if type(name) is str:
        mod_script_config = {}
        config_path = os.path.join(cf.mods_folder, "Mods", scri, f"Configuration_{cf.user_folder_name}")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f: mod_script_config = json.load(f)
            except Exception: printDebugMessage("Invalid Mod Script Configuration, returned blank.")
        if name == "*":
            if type(data) is dict:
                try:
                    dumped = json.dumps(data)
                    for i, v in data.items(): mod_script_config[i] = v
                except Exception: printDebugMessage(f"Something went wrong saving Mod Script Configuration requested by mod script {scri}.")
            else: printDebugMessage(f"Something went wrong saving Mod Script Configuration requested by mod script {scri}.")
        else:
            try:
                dumped = json.dumps(data)
                mod_script_config[name] = data
            except Exception: printDebugMessage(f"Something went wrong saving Mod Script Configuration requested by mod script {scri}.")
        with open(config_path, "w", encoding="utf-8") as f:  json.dump(mod_script_config, f, indent=4)
    else: return None
def unzipFile(scri: str, path: str, output: str, look_for: list=[], export_out: list=[], either: bool=False, check: bool=True):
    path = str(path)
    path = path.replace("../", "").replace("..\\", "")
    path = os.path.join(cf.mods_folder, "Mods", scri, path)
    output = str(output)
    output = output.replace("../", "").replace("..\\", "")
    output = os.path.join(cf.mods_folder, "Mods", scri, output)
    if path.startswith(os.path.join(cf.mods_folder, "Mods", scri)) and output.startswith(os.path.join(cf.mods_folder, "Mods", scri)): return cf.pip_class.unzipFile(path, output, look_for=look_for, export_out=export_out, either=either, check=check)
def sendDiscordWebhookMessage(scri: str, title: str="Message from Mod Script", description: str=None, color: int=0, fields: list=[], image=f"{cf.main_host}/Images/DiscordIcon.png"):
    if cf.main_config.get("EFlagUseDiscordWebhook") == True:
        for i in fields: 
            if not (type(i) is rcf.generated_api_instances[scri].DiscordWebhookField): return False
        if cf.main_config.get("EFlagDiscordWebhookURL"):
            generated_body = {
                "content": f"<@{cf.main_config.get('EFlagDiscordWebhookUserId')}>",
                "embeds": [
                    {
                        "title": title,
                        "description": description or "",
                        "color": color,
                        "fields": [i.convert() for i in fields],
                        "author": { "name": obName0(), "icon_url": cf.main_config.get("EFlagCustomBootstrapInternetURL", f"{cf.main_host}/Images/DiscordIcon.png") },
                        "thumbnail": { "url": image },
                        "footer": { "text": (ts(f"Made by @EfazDev | PID: {rcf.connected_roblox_instance.pid}") if cf.main_config.get("EFlagDiscordWebhookShowPidInFooter") == True and rcf.connected_roblox_instance and rcf.connected_roblox_instance.pid else ts("Made by @EfazDev")) + (" | Custom Theme" if obName0() != "OrangeBlox" or obName1() != "🍊" else ""), "icon_url": "https://cdn.efaz.dev/cdn/png/logo.png" },
                        "timestamp": datetime.datetime.now(tz=datetime.UTC).strftime('%Y-%m-%dT%H:%M:%S.000Z')
                    }
                ],
                "attachments": []
            }
            try:
                def sen():
                    waitForInternet()
                    req = cf.requests.post(cf.main_config.get("EFlagDiscordWebhookURL"), data=generated_body)
                    if req.ok: printDebugMessage("Successfully sent webhook! Event: onModScript")
                    else: printErrorMessage(f"There was an issue sending your webhook message. Status Code: {req.status_code}")
                if cf.pip_class.getIfConnectedToInternet() == True: sen()
                else: cf.pip_class.startThread(func=sen, daemon=True)
            except Exception: printDebugMessage(f"There was an issue sending your webhook message. Exception: \n{trace()}")
def startPrepareRoblox(scri: str): 
    if rcf.roblox_launched_affect_mod_script != True: prepareRobloxClient()
def current_ver_func(scri: str): return cf.current_version
def modScriptName(scri: str): 
    cur_mod_manifest = generateModsManifest()
    return cur_mod_manifest.get(scri).get("name") if cur_mod_manifest.get(scri) and cur_mod_manifest.get(scri).get("name") else None
def modScriptId(scri: str): return scri
def modScriptVersion(scri: str): 
    cur_mod_manifest = generateModsManifest()
    return cur_mod_manifest.get(scri).get("version") if cur_mod_manifest.get(scri) and cur_mod_manifest.get(scri).get("version") else None
def getConnectedUserInfo(scri: str): return rcf.connected_user_info
def getIfConnectedToGame(scri: str): return rcf.connected_to_game
def getCurrentPlaceInfo(scri: str): return rcf.current_place_info
def createAppLock(scri: str, name: str="ScriptLock"):
    name = os.path.basename(name)
    if name == "Configuration" or name.startswith("Configuration"): return
    script_lock_key = generateFileKey(name, dire=os.path.join(cf.mods_folder, "Mods", scri))
    app_lock = PyKits.Lock(script_lock_key)
    if app_lock.exists(): return False
    if app_lock.acquire(timeout=0.1):
        rcf.mod_script_locks[script_lock_key] = app_lock
        return True
    else: return False
def getIfModIsEnabled(scri: str, mod_name: str): 
    cur_mod_manifest = generateModsManifest()
    if cur_mod_manifest.get(mod_name) and cur_mod_manifest.get(mod_name).get("enabled") == True: return True
    return False
def enableMod(scri: str, mod_name: str): 
    cur_mod_manifest = generateModsManifest()
    if not (cf.main_config.get("EFlagEnabledMods") and type(cf.main_config.get("EFlagEnabledMods")) is dict): cf.main_config["EFlagEnabledMods"] = {}
    if cur_mod_manifest.get(mod_name): cf.main_config["EFlagEnabledMods"][mod_name] = True
    saveSettings()
def disableMod(scri: str, mod_name: str): 
    cur_mod_manifest = generateModsManifest()
    if not (cf.main_config.get("EFlagEnabledMods") and type(cf.main_config.get("EFlagEnabledMods")) is dict): cf.main_config["EFlagEnabledMods"] = {}
    if cur_mod_manifest.get(mod_name): cf.main_config["EFlagEnabledMods"][mod_name] = False
    saveSettings()
def getCurrentRobloxPid(scri: str): 
    return rcf.connected_roblox_instance and rcf.connected_roblox_instance.pid
def getRbxChannel(studio: bool=False):
    if cf.main_config.get("EFlagRobloxSecurityCookieUsage") == True:
        requesting_channel = cf.handler.getUserChannel(studio=cf.run_studio, debug=(cf.main_config.get("EFlagEnableDebugMode") == True))
        if requesting_channel.get("success") == True and requesting_channel.get("channel_name") != "LIVE": return requesting_channel.get("channel_name")
    r = cf.handler.getCurrentClientVersion(studio=studio)
    if r and r["success"] == True: return r["channel"]
    else: return "LIVE"
def getLatestRobloxVersion(scri: str, channel: str="*"):
    if channel == "*": channel = getRbxChannel(studio=cf.run_studio==True)
    res = cf.handler.getLatestClientVersion(studio=cf.run_studio==True, channel=channel, token=createDownloadToken(cf.run_studio==True))
    if res and res.get("attempted_channel"): res["channel"] = res["attempted_channel"]; res.pop("attempted_channel")
    return res
def getLatestOppositeRobloxVersion(scri: str, channel: str="*"):
    if channel == "*": channel = getRbxChannel(studio=cf.run_studio!=True)
    res = cf.handler.getLatestClientVersion(studio=cf.run_studio!=True, channel=channel, token=createDownloadToken(cf.run_studio!=True))
    if res and res.get("attempted_channel"): res["channel"] = res["attempted_channel"]; res.pop("attempted_channel")
    return res
def getLatestRobloxPlayerVersion(scri: str, channel: str="*"):
    if channel == "*": channel = getRbxChannel(studio=False)
    res = cf.handler.getLatestClientVersion(studio=False, channel=channel, token=createDownloadToken(False))
    if res and res.get("attempted_channel"): res["channel"] = res["attempted_channel"]; res.pop("attempted_channel")
    return res
def getLatestRobloxStudioVersion(scri: str, channel: str="*"):
    if channel == "*": channel = getRbxChannel(studio=True)
    res = cf.handler.getLatestClientVersion(studio=True, channel=channel, token=createDownloadToken(True))
    if res and res.get("attempted_channel"): res["channel"] = res["attempted_channel"]; res.pop("attempted_channel")
    return res
def getRobloxThumbnailURLl(scri: str, studio: bool=None): return getRobloxThumbnailURL(studio)
def restartRbx(scri: str):
    if not rcf.connected_roblox_instance: return False
    printDebugMessage(f"Mod script \"{scri}\" has requested to restart Roblox.")
    cf.handler.endRoblox(studio=cf.run_studio)
    cf.preserve_roblox = True
    cf.pip_class.startThread(cf.restartRoblox, True)
    return True
def joinGame(scri: str, place_id: int, game_instance_id: str=None, launch_data: str=""):
    if not rcf.connected_roblox_instance: return False
    if cf.run_studio == True: return False
    if cf.main_config.get("EFlagUseEfazDevAPI") == True: 
        generated_universe_id_res = cf.requests.get(f"https://api.efaz.dev/api/roblox/universeId/{place_id}", loop_429=cf.main_config.get("EFlagEnableLoop429Requests")==True)
        if generated_universe_id_res and generated_universe_id_res.json: generated_universe_id_res.json = generated_universe_id_res.json.get("response")
    else: generated_universe_id_res = cf.requests.get(f"https://apis.roblox.com/universes/v1/places/{place_id}/universe", loop_429=cf.main_config.get("EFlagEnableLoop429Requests")==True, cookies=createCookieHeader())
    universe_id = None
    if generated_universe_id_res.ok:
        generated_universe_id_json = generated_universe_id_res.json
        if generated_universe_id_json and generated_universe_id_json.get("universeId") != None:
            universe_id = generated_universe_id_json.get("universeId")
    if not universe_id: return False
    url = f"roblox://experiences/start?placeId={place_id}&universeId={universe_id}"
    if game_instance_id: url += f"&gameInstanceId={game_instance_id}"
    if launch_data: url += f"&{launch_data}"
    cf.given_args = ["Main.py", url]
    printDebugMessage(f"Mod script \"{scri}\" has requested to join a Roblox game: {place_id}.")
    cf.preserve_roblox = True
    cf.pip_class.startThread(cf.restartRoblox, True, False)
    return True

defined_func = {
    "generateModsManifest": generateModsManifest,
    "generateModOrder": generateModOrder,
    "displayNotification": displayNotification,
    "getRobloxLogFolderSize": getRobloxLogFolderSize,
    "sendBloxstrapRPC": sendBloxstrapRPC,
    "unzipFile": unzipFile,
    "restartRoblox": restartRbx,
    "joinRobloxGame": joinGame,
    "changeRobloxWindowSizeAndPosition": changeRobloxWindowSizeAndPosition,
    "setRobloxWindowTitle": setRobloxWindowTitle,
    "setRobloxWindowIcon": setRobloxWindowIcon,
    "getRobloxAppSettings": getRobloxAppSettings,
    "focusRobloxWindow": focusRobloxWindow,
    "getIfRobloxLaunched": getIfRobloxLaunched,
    "sendDiscordWebhookMessage": sendDiscordWebhookMessage,
    "getLatestOppositeRobloxVersion": getLatestOppositeRobloxVersion,
    "getLatestRobloxVersion": getLatestRobloxVersion,
    "getLatestRobloxPlayerVersion": getLatestRobloxPlayerVersion,
    "getLatestRobloxStudioVersion": getLatestRobloxStudioVersion,
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

if __name__ == "__main__":
    print("This module is not a runable instance.")
    sys.exit(1)