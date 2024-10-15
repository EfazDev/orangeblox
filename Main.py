import os
import shutil
import json
import sys
import platform
import datetime
import importlib.util
import subprocess
import threading
import time
from urllib.parse import unquote
import RobloxFastFlagsInstaller
from PipHandler import pip

if __name__ == "__main__":
    main_os = platform.system()
    windows_dir = os.path.join(f"{os.getenv('LOCALAPPDATA')}", "Roblox")
    stored_content_folder_destinations = {
        "Darwin": "/Applications/Roblox.app/Contents/Resources/"
    }
    stored_font_folder_destinations = {
        "Darwin": f"{stored_content_folder_destinations['Darwin']}content/fonts/"
    }
    stored_robux_folder_destinations = {
        "Darwin": f"{stored_content_folder_destinations['Darwin']}content/textures/ui/common/"
    }
    handler = RobloxFastFlagsInstaller.Main()
    fast_config_loaded = True
    multi_instance_enabled = False
    current_version = {"version": "1.2.3"}
    given_args = list(filter(None, sys.argv))
    pip_class = pip()

    with open("FastFlagConfiguration.json", "r") as f:
        try:
            fflag_configuration = json.load(f)
        except Exception as e:
            fast_config_loaded = False

    def printMainMessage(mes): print(f"\033[38;5;255m{mes}\033[0m")
    def printErrorMessage(mes): print(f"\033[38;5;196m{mes}\033[0m")
    def printSuccessMessage(mes): print(f"\033[38;5;82m{mes}\033[0m")
    def printWarnMessage(mes): print(f"\033[38;5;202m{mes}\033[0m")
    def printYellowMessage(mes): print(f"\033[38;5;226m{mes}\033[0m")
    def printDebugMessage(mes): 
        if fast_config_loaded and fflag_configuration.get("EFlagEnableDebugMode"): printYellowMessage(mes)

    def isYes(text): return text.lower() == "y" or text.lower() == "yes"
    def isNo(text): return text.lower() == "n" or text.lower() == "no"
    def isRequestClose(text): return text.lower() == "exit" or text.lower() == "exit()"
    def copyFile(pa, de):
        if os.path.exists(pa):
            if os.path.exists("./ExportMode/"):
                destination_dir = f"./ExportMode{os.path.dirname(de)}"
                if not os.path.exists(destination_dir):
                    os.makedirs(destination_dir)
                    printDebugMessage(f"Created directory: {destination_dir}")
                destination_path = f"./ExportMode{de}"
                a = shutil.copy(pa, destination_path)
            a = shutil.copy(pa, de)
            printDebugMessage(f"Copied File: {pa} => {de}")
            return a
        else:
            printDebugMessage(f"File not found: {pa}")
            return None
    def readJSONFile(path, listExpected=False):
        with open(path, "r") as f:
            try:
                main_content = json.load(f)
                if listExpected == True:
                    if type(main_content) is list:
                        return main_content
                    else:
                        return None
                else:
                    if type(main_content) is dict:
                        return main_content
                    else:
                        return None
            except Exception as e:
                return None
        return None
    def displayNotification(title, message):
        if main_os == "Darwin":
            if os.path.exists("/Applications/EfazRobloxBootstrap.app/Contents/Resources/"):
                with open("/Applications/EfazRobloxBootstrap.app/Contents/Resources/MacOSNotification", "w") as f:
                    json.dump({"title": title, "message": message}, f)
        elif main_os == "Windows":
            try:
                from plyer import notification
            except Exception as e:
                pip_class.install(["plyer"])
                from plyer import notification
            notification.notify(
                title = title,
                message = message,
                app_icon = "AppIcon.ico",
                timeout = 30,
            )
    def generateModsManifest():
        generated_manifest = {}
        for i in os.listdir("./Mods/"):
            mod_info = {
                "name": i,
                "id": i,
                "version": "1.0.0",
                "mod_script": False,
                "mod_script_path": "",
                "manifest_path": "",
                "enabled": False,
                "permissions": []
            }
            mod_path = os.path.join("./Mods/", i)
            if os.path.isdir(mod_path):
                manifest_path = os.path.join(mod_path, "Manifest.json")
                mod_script_path = os.path.join(mod_path, "ModScript.py")
                if not (fflag_configuration.get("EFlagEnabledMods") and type(fflag_configuration["EFlagEnabledMods"]) is dict):
                    fflag_configuration["EFlagEnabledMods"] = {}
                if fflag_configuration["EFlagEnabledMods"].get(i) == True:
                    mod_info["enabled"] = True
                if os.path.exists(manifest_path) and os.path.isfile(manifest_path):
                    res_json = readJSONFile(manifest_path)
                    if res_json:
                        if type(res_json.get("name")) is str:
                            mod_info["name"] = res_json.get("name")
                        if type(res_json.get("version")) is str and len(res_json.get("version")) < 10:
                            mod_info["version"] = res_json.get("version")
                        if type(res_json.get("mod_script")) is bool:
                            mod_info["mod_script"] = res_json.get("mod_script")
                        if type(res_json.get("mod_script_requirements")) is list:
                            mod_info["permissions"] = res_json.get("mod_script_requirements")
                        mod_info["manifest_path"] = manifest_path
                if os.path.exists(mod_script_path) and os.path.isfile(mod_script_path):
                    with open(mod_script_path, "r") as f:
                        mod_mode_script_text = f.read()
                    if "FastFlagConfiguration.json" in mod_mode_script_text and not ("fastFlagConfiguration" in mod_info["permissions"]): mod_info["permissions"].append("fastFlagConfiguration")
                    if "Main.py" in mod_mode_script_text and not ("editMainExecutable" in mod_info["permissions"]): mod_info["permissions"].append("editMainExecutable")
                    if "ModScript.py" in mod_mode_script_text and not ("editModScript" in mod_info["permissions"]): mod_info["permissions"].append("editModScript")
                    if "MacOSNotification" in mod_mode_script_text and not ("macNotification" in mod_info["permissions"]): mod_info["permissions"].append("macNotification")
                    if "Mods" in mod_mode_script_text and not ("configureMods" in mod_info["permissions"]): mod_info["permissions"].append("configureMods")
                    if "RobloxBrand" in mod_mode_script_text and not ("configureRobloxBranding" in mod_info["permissions"]): mod_info["permissions"].append("configureRobloxBranding")
                    if "DeathSounds" in mod_mode_script_text and not ("configureDeathSounds" in mod_info["permissions"]): mod_info["permissions"].append("configureDeathSounds")
                    if "Cursors" in mod_mode_script_text and not ("configureCursors" in mod_info["permissions"]): mod_info["permissions"].append("configureCursors")
                    if "AvatarEditorMaps" in mod_mode_script_text and not ("configureAvatarMaps" in mod_info["permissions"]): mod_info["permissions"].append("configureAvatarMaps")
                    mod_info["mod_script_path"] = mod_script_path
                else:
                    mod_info["mod_script"] = False
                generated_manifest[i] = mod_info
        return generated_manifest
    
    os.system("cls" if os.name == "nt" else "clear")
    printWarnMessage("-----------")
    printWarnMessage("Welcome to Efaz's Roblox Bootstrap!")
    printWarnMessage("Made by Efaz from efaz.dev!")
    printWarnMessage(f"v{current_version['version']}")
    printWarnMessage("-----------")

    # Requirement Checks
    if main_os == "Windows":
        printMainMessage(f"System OS: {main_os}")
        found_platform = "Windows"
    elif main_os == "Darwin":
        printMainMessage(f"System OS: {main_os} (macOS)")
        found_platform = "Darwin"
    else:
        printErrorMessage("Efaz's Roblox Bootstrap is only supported for macOS or Windows.")
        input("> ")
        sys.exit(0)
    current_python_version = platform.python_version_tuple()
    if current_python_version < ("3", "10", "0"):
        printErrorMessage("Please update your current installation of Python above 3.10.0")
        input("> ")
        sys.exit(0)
    else:
        printMainMessage(f"Python Version: {platform.python_version()}")
    if main_os == "Windows":
        stored_content_folder_destinations["Windows"] = f"{handler.getRobloxInstallFolder()}\\"
        stored_font_folder_destinations["Windows"] = f"{stored_content_folder_destinations['Windows']}content\\fonts\\"
        stored_robux_folder_destinations["Windows"] = f"{stored_content_folder_destinations['Windows']}content\\textures\\ui\\common\\"
        if not os.path.exists(stored_font_folder_destinations["Windows"]):
            printErrorMessage("Please install Roblox from the Roblox website in order to use this bootstrap!")
            input("> ")
            sys.exit(0)
        else:
            cur_vers = handler.getCurrentClientVersion()
            if cur_vers["success"] == True:
                printMainMessage(f"Current Roblox Version: {cur_vers['version']}")
            else:
                printErrorMessage("Something went wrong trying to determine your current Roblox version.")
                input("> ")
                sys.exit(0)
    elif main_os == "Darwin":
        if os.path.exists("/Applications/Roblox.app/"):
            cur_vers = handler.getCurrentClientVersion()
            if cur_vers["success"] == True:
                printMainMessage(f"Current Roblox Version: {cur_vers['version']}")
            else:
                printErrorMessage("Something went wrong trying to determine your current Roblox version.")
                input("> ")
                sys.exit(0)
        else:
            printErrorMessage("Please install Roblox from the Roblox website in order to use this bootstrap!")
            input("> ")
            sys.exit(0)

    # URL Scheme Exchange between Loader and Main.py
    if main_os == "Darwin":
        if os.path.exists("/Applications/EfazRobloxBootstrap.app/Contents/Resources/URLSchemeExchange"):
            with open("/Applications/EfazRobloxBootstrap.app/Contents/Resources/URLSchemeExchange", "r") as f:
                filtered_args = f.read()
            if (("roblox-player:" in filtered_args) or ("roblox:" in filtered_args) or ("efaz-bootstrap:" in filtered_args)) and not (fast_config_loaded == True and fflag_configuration.get("EFlagEnableDebugMode") == True):
                if fflag_configuration.get("EFlagEnableDebugMode"): printDebugMessage("Moved command execution to file args to prevent user from showing the command with private info.")
            given_args = ["Main.py", filtered_args]
            os.remove("/Applications/EfazRobloxBootstrap.app/Contents/Resources/URLSchemeExchange")
    elif main_os == "Windows":
        generated_app_path = os.path.join(os.getenv('LOCALAPPDATA'), "EfazRobloxBootstrap")
        if os.path.exists(os.path.join(generated_app_path, "URLSchemeExchange")):
            with open(os.path.join(generated_app_path, "URLSchemeExchange"), "r") as f:
                filtered_args = f.read()
            if (("roblox-player:" in filtered_args) or ("roblox:" in filtered_args) or ("efaz-bootstrap:" in filtered_args)) and not (fast_config_loaded == True and fflag_configuration.get("EFlagEnableDebugMode") == True):
                if fflag_configuration.get("EFlagEnableDebugMode"): printDebugMessage("Moved command execution to file args to prevent user from showing the command with private info.")
            given_args = ["Main.py", filtered_args]
            os.remove("./URLSchemeExchange")

    # Handle Option Functions
    def handleOption1(): # Continue to Roblox
        printWarnMessage("--- Continue to Roblox ---")
        printMainMessage("Continuing to next stage!")
    def handleOption2(): # Multiple Instances
        global multi_instance_enabled
        printWarnMessage("--- Multiple Instances ---")
        if main_os == "Windows":
            if True:
                multi_instance_enabled = True
                printMainMessage("Enabled Multiple Instances!")
            else:
                printErrorMessage("Multiple Roblox Instances on Efaz's Roblox Bootstrap is not available for Windows. [Currently, only for macOS.]")
                input("> ")
                sys.exit(0)
        elif main_os == "Darwin":
            multi_instance_enabled = True
            printMainMessage("Enabled Multiple Instances!")
    def handleOption3(): # Run Fast Flag Installer
        printWarnMessage("--- Running Installer ---")
        subprocess.run(args=[sys.executable, "RobloxFastFlagsInstaller.py"])

        global fast_config_loaded
        fast_config_loaded = True
        with open("FastFlagConfiguration.json", "r") as f:
            try:
                fflag_configuration = json.load(f)
            except Exception as e:
                fast_config_loaded = False

        if (fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir") and os.path.exists(fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir"))):
            if main_os == "Windows":
                if os.path.exists(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}\\FastFlagConfiguration.json'):
                    with open(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}\\FastFlagConfiguration.json', "w") as f:
                        json.dump(fflag_configuration, f, indent=4)
                    printSuccessMessage("Successfully synced Bootstrap Settings!")
                else:
                    printErrorMessage("Bootstrap Sync is not supported since the original unextracted directory is not found.")
            elif main_os == "Darwin":
                if os.path.exists(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}/FastFlagConfiguration.json'):
                    with open(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}/FastFlagConfiguration.json', "w") as f:
                        json.dump(fflag_configuration, f, indent=4)
                    printSuccessMessage("Successfully synced Bootstrap Settings!")
                else:
                    printErrorMessage("Bootstrap Sync is not supported since the original unextracted directory is not found.")
    def handleOption4(): # Set Settings
        printWarnMessage("--- Settings ---")
        global fflag_configuration
        printMainMessage("Would you like to remove the Builder Font and use the old one? (y/n)")
        a = input("> ")
        if isYes(a) == True:
            fflag_configuration["EFlagRemoveBuilderFont"] = True
            printDebugMessage("User selected: True")
        elif isNo(a) == True:
            fflag_configuration["EFlagRemoveBuilderFont"] = False
            printDebugMessage("User selected: False")

        printMainMessage("Would you like to change the background of the Avatar Editor? (y/n)")
        c = input("> ")
        if isYes(c) == True:
            fflag_configuration["EFlagEnableChangeAvatarEditorBackground"] = True
            def scan_name(a):
                if main_os == "Windows":
                    if os.path.exists(f"{os.path.curdir}\\AvatarEditorMaps\\{a}\\AvatarBackground.rbxl"):
                        return True
                    else:
                        return False
                elif main_os == "Darwin":
                    if os.path.exists(f"{os.path.curdir}/AvatarEditorMaps/{a}/AvatarBackground.rbxl"):
                        return True
                    else:
                        return False
            def getName():
                got_backgrounds = []
                for i in os.listdir("./AvatarEditorMaps/"):
                    if os.path.isdir(f"./AvatarEditorMaps/{i}/"):
                        got_backgrounds.append(i)
                printWarnMessage("Select the number that is associated with the map you want to use.")
                got_backgrounds = sorted(got_backgrounds)
                count = 1
                for i in got_backgrounds:
                    printMainMessage(f"[{str(count)}] = {i}")
                    count += 1
                if main_os == "Darwin":
                    printYellowMessage("[Please know specific maps may not support macOS.]")
                    printYellowMessage("[Also, if you just added a new map folder into the AvatarEditorMaps folder, please rerun Install.py in order for it to seen.]")
                a = input("> ")
                if a.isnumeric():
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
            fflag_configuration["EFlagAvatarEditorBackground"] = set_avatar_editor_location
            printSuccessMessage(f"Set avatar background: {set_avatar_editor_location}")
        elif isNo(c) == True:
            fflag_configuration["EFlagEnableChangeAvatarEditorBackground"] = False
            printDebugMessage("User selected: False")

        printMainMessage("Would you like to change the Roblox cursor? (y/n)")
        c = input("> ")
        if isYes(c) == True:
            fflag_configuration["EFlagEnableChangeCursor"] = True
            def scan_name(a):
                if main_os == "Windows":
                    if os.path.exists(f"{os.path.curdir}\\Cursors\\{a}\\ArrowCursor.png") and os.path.exists(f"{os.path.curdir}\\Cursors\\{a}\\ArrowFarCursor.png"):
                        return True
                    else:
                        return False
                elif main_os == "Darwin":
                    if os.path.exists(f"{os.path.curdir}/Cursors/{a}/ArrowCursor.rbxl") and os.path.exists(f"{os.path.curdir}/Cursors/{a}/ArrowFarCursor.rbxl"):
                        return True
                    else:
                        return False
            def getName():
                got_cursors = []
                for i in os.listdir("./Cursors/"):
                    if os.path.isdir(f"./Cursors/{i}/"):
                        got_cursors.append(i)
                got_cursors = sorted(got_cursors)
                printWarnMessage("Select the number that is associated with the cursor you want to use.")
                count = 1
                for i in got_cursors:
                    printMainMessage(f"[{str(count)}] = {i}")
                    count += 1
                if main_os == "Darwin":
                    printYellowMessage("[Also, if you just added a new cursor folder into the Cursors folder, please rerun Install.py in order for it to seen.]")
                a = input("> ")
                if a.isnumeric():
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
            fflag_configuration["EFlagSelectedCursor"] = set_cursor_location
            printSuccessMessage(f"Set cursor folder: {set_cursor_location}")
        elif isNo(c) == True:
            fflag_configuration["EFlagEnableChangeCursor"] = False
            printDebugMessage("User selected: False")

        printMainMessage("Would you like to change the Roblox logo? (y/n)")
        c = input("> ")
        if isYes(c) == True:
            fflag_configuration["EFlagEnableChangeBrandIcons"] = True
            def scan_name(a):
                if main_os == "Windows":
                    if os.path.exists(f"{os.path.curdir}\\RobloxBrand\\{a}\\AppIcon.icns"):
                        return True
                    else:
                        return False
                elif main_os == "Darwin":
                    if os.path.exists(f"{os.path.curdir}/RobloxBrand/{a}/AppIcon.icns"):
                        return True
                    else:
                        return False
            def getName():
                got_icons = []
                for i in os.listdir("./RobloxBrand/"):
                    if os.path.isdir(f"./RobloxBrand/{i}/"):
                        got_icons.append(i)
                got_icons = sorted(got_icons)
                printWarnMessage("Select the number that is associated with the icon you want to use.")
                count = 1
                for i in got_icons:
                    printMainMessage(f"[{str(count)}] = {i}")
                    count += 1
                if main_os == "Darwin":
                    printYellowMessage("[Also, if you just added a new icon folder into the RobloxBrand folder, please rerun Install.py in order for it to seen.]")
                a = input("> ")
                if a.isnumeric():
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
            fflag_configuration["EFlagSelectedBrandLogo"] = set_app_icon_location
            printSuccessMessage(f"Set logo folder: {set_app_icon_location}")
        elif isNo(c) == True:
            fflag_configuration["EFlagEnableChangeBrandIcons"] = False
            printDebugMessage("User selected: False")

        printMainMessage("Would you like to change the Roblox death sound? (y/n)")
        c = input("> ")
        if isYes(c) == True:
            fflag_configuration["EFlagEnableChangeDeathSound"] = True
            def scan_name(a):
                if main_os == "Windows":
                    if os.path.exists(f"{os.path.curdir}\\DeathSounds\\{a}"):
                        return True
                    else:
                        return False
                elif main_os == "Darwin":
                    if os.path.exists(f"{os.path.curdir}/DeathSounds/{a}"):
                        return True
                    else:
                        return False
            def getName():
                got_sounds = []
                for i in os.listdir("./DeathSounds/"):
                    if os.path.isfile(f"./DeathSounds/{i}") and i.endswith(".ogg"):
                        got_sounds.append(i)
                got_sounds = sorted(got_sounds)
                printWarnMessage("Select the number that is associated with the sound you want to use.")
                count = 1
                for i in got_sounds:
                    printMainMessage(f"[{str(count)}] = {i}")
                    count += 1
                if main_os == "Darwin":
                    printYellowMessage("[Also, if you just added a new sound file into the DeathSounds folder, please rerun Install.py in order for it to seen.]")
                a = input("> ")
                if a.isnumeric():
                    c = int(a)-1
                    if c < len(got_sounds) and c >= 0:
                        if got_sounds[c]:
                            b = got_sounds[c]
                            if scan_name(b) == True:
                                return b
                            else:
                                printDebugMessage("Directory is not valid.")
                                return "New"
                        else:
                            printDebugMessage("User gave a number which is somehow not on the list..?")
                            return "New"
                    else:
                        printDebugMessage("User gave a number which is out of reach.")
                        return "New"
                else:
                    printDebugMessage("User gave a response which is not a number.")
                    return "New"
            set_death_sound = getName()
            fflag_configuration["EFlagSelectedDeathSound"] = set_death_sound
            printSuccessMessage(f"Set death sound: {set_death_sound}")
        elif isNo(c) == True:
            fflag_configuration["EFlagEnableChangeDeathSound"] = False
            printDebugMessage("User selected: False")

        if main_os == "Darwin" or main_os == "Windows":
            printMainMessage("Would you like to allow duplication of Roblox Clients? (y/n)")
            c = input("> ")
            if isYes(c) == True:
                fflag_configuration["EFlagEnableDuplicationOfClients"] = True
                printDebugMessage("User selected: True")
                printYellowMessage("Notes to keep track of:")
                printYellowMessage("1. Make sure all currently open instances are fully loaded in a game before going to an another account.")
                printYellowMessage("2. Use only the bootstrap to load Roblox since macOS will try to validate a check and fail.")
                printYellowMessage("3. If you get teleported or kicked out, you may teleport into the current logged in Roblox account stored which may be the last logged in account.")
            elif isNo(c) == True:
                fflag_configuration["EFlagEnableDuplicationOfClients"] = False
                printDebugMessage("User selected: False")

        printMainMessage("Would you like to allow Activity Tracking on the Roblox client? (y/n)")
        printMainMessage("This will allow features like:")
        printMainMessage("- Server Locations")
        printMainMessage("- BloxstrapRPC")
        printMainMessage("- Discord Presence")
        printMainMessage("- Discord Webhooks")
        printMainMessage("- Mod Mode Scripts")
        if main_os == "Windows":
            printMainMessage("- Multiple Instances")
        d = input("> ")
        if isYes(d) == True:
            fflag_configuration["EFlagAllowActivityTracking"] = True
            printDebugMessage("User selected: True")
        elif isNo(d) == True:
            fflag_configuration["EFlagAllowActivityTracking"] = False
            printDebugMessage("User selected: False")

        if not (fflag_configuration.get("EFlagAllowActivityTracking") == False):
            printMainMessage("Would you like to enable Server Locations? (y/n)")
            d = input("> ")
            if isYes(d) == True:
                fflag_configuration["EFlagNotifyServerLocation"] = True
                printDebugMessage("User selected: True")
            elif isNo(d) == True:
                fflag_configuration["EFlagNotifyServerLocation"] = False
                printDebugMessage("User selected: False")

            printMainMessage("Would you like to enable Discord RPC? (extra modules may be installed when said yes) (y/n)")
            d = input("> ")
            if isYes(d) == True:
                fflag_configuration["EFlagEnableDiscordRPC"] = True
                try:
                    from DiscordPresenceHandler import Presence
                    import requests
                except Exception as e:
                    pip_class.install(["pypresence", "requests"])
                    from DiscordPresenceHandler import Presence
                    import requests
                    printSuccessMessage("Successfully installed presence modules!")
                printDebugMessage("User selected: True")
                printMainMessage("Would you like to enable joining from your Discord profile? (Everyone will be allowed to join depending on type of server.)")
                d = input("> ")
                if isYes(d) == True:
                    fflag_configuration["EFlagEnableDiscordRPCJoining"] = True
                    printDebugMessage("User selected: True")
                elif isNo(d) == True:
                    fflag_configuration["EFlagEnableDiscordRPCJoining"] = False
                    printDebugMessage("User selected: False")
            elif isNo(d) == True:
                fflag_configuration["EFlagEnableDiscordRPCJoining"] = False
                fflag_configuration["EFlagEnableDiscordRPC"] = False
                printDebugMessage("User selected: False")

            if fflag_configuration.get("EFlagEnableDiscordRPC") == True:
                printMainMessage("Would you like to enable games to use the Bloxstrap SDK? (y/n)")
                d = input("> ")
                if isYes(d) == True:
                    fflag_configuration["EFlagAllowBloxstrapSDK"] = True
                    printDebugMessage("User selected: True")
                elif isNo(d) == True:
                    fflag_configuration["EFlagAllowBloxstrapSDK"] = False
                    printDebugMessage("User selected: False")

                printMainMessage("Would you like to enable access to private servers you connect to from Discord Presences? (users may be able to join or not) (y/n)")
                d = input("> ")
                if isYes(d) == True:
                    fflag_configuration["EFlagAllowPrivateServerJoining"] = True
                    printDebugMessage("User selected: True")
                elif isNo(d) == True:
                    fflag_configuration["EFlagAllowPrivateServerJoining"] = False
                    printDebugMessage("User selected: False")

            printMainMessage("Would you like to use a Discord Webhook? (link required) (y/n)")
            d = input("> ")
            if isYes(d) == True:
                fflag_configuration["EFlagUseDiscordWebhook"] = True
                try:
                    import requests
                except Exception as e:
                    pip_class.install(["requests"])
                    import requests
                printDebugMessage("User selected: True")
                printMainMessage("Please enter your Discord Webhook Link here (https://discord.com/api/webhooks/XXXXXXX/XXXXXXX): ")
                d = input("> ")
                if d.startswith("https://discord.com/api/webhooks/"):
                    printDebugMessage("URL passed test.")
                    fflag_configuration["EFlagDiscordWebhookURL"] = d
                if fflag_configuration.get("EFlagDiscordWebhookURL", "").startswith("https://discord.com/api/webhooks/"):
                    printMainMessage("Enter your Discord User ID (you may need Developer Mode in order to copy):")
                    d = input("> ")
                    if d.isnumeric():
                        fflag_configuration["EFlagDiscordWebhookUserId"] = d
                    printMainMessage("When should this Discord Webhook be notified?")
                    printMainMessage("[1/6] It should be notified when the client connects to a Roblox server. (y/n)")
                    d = input("> ")
                    if isYes(d) == True:
                        fflag_configuration["EFlagDiscordWebhookConnect"] = True
                        printDebugMessage("User selected: True")
                    elif isNo(d) == True:
                        fflag_configuration["EFlagDiscordWebhookConnect"] = False
                        printDebugMessage("User selected: False")
                    printMainMessage("[2/6] It should be notified when the client disconnects from a server. (y/n)")
                    d = input("> ")
                    if isYes(d) == True:
                        fflag_configuration["EFlagDiscordWebhookDisconnect"] = True
                        printDebugMessage("User selected: True")
                    elif isNo(d) == True:
                        fflag_configuration["EFlagDiscordWebhookDisconnect"] = False
                        printDebugMessage("User selected: False")
                    printMainMessage("[3/6] It should be notified when Roblox opens. [Process ID and Log File Location (includes username in computer) is revealed in message] (y/n)")
                    d = input("> ")
                    if isYes(d) == True:
                        fflag_configuration["EFlagDiscordWebhookRobloxAppStart"] = True
                        printDebugMessage("User selected: True")
                    elif isNo(d) == True:
                        fflag_configuration["EFlagDiscordWebhookRobloxAppStart"] = False
                        printDebugMessage("User selected: False")
                    printMainMessage("[4/6] It should be notified when Roblox closes. [Process ID and Log File Location (includes username in computer) is revealed in message] (y/n)")
                    d = input("> ")
                    if isYes(d) == True:
                        fflag_configuration["EFlagDiscordWebhookRobloxAppClose"] = True
                        printDebugMessage("User selected: True")
                    elif isNo(d) == True:
                        fflag_configuration["EFlagDiscordWebhookRobloxAppClose"] = False
                        printDebugMessage("User selected: False")
                    printMainMessage("[5/6] It should be notified when Roblox crashes. [Console Log is revealed] (y/n)")
                    d = input("> ")
                    if isYes(d) == True:
                        fflag_configuration["EFlagDiscordWebhookRobloxCrash"] = True
                        printDebugMessage("User selected: True")
                    elif isNo(d) == True:
                        fflag_configuration["EFlagDiscordWebhookRobloxCrash"] = False
                        printDebugMessage("User selected: False")
                    printMainMessage("[6/6] It should be notified when Bloxstrap RPC is triggered. (y/n)")
                    d = input("> ")
                    if isYes(d) == True:
                        fflag_configuration["EFlagDiscordWebhookBloxstrapRPC"] = True
                        printDebugMessage("User selected: True")
                    elif isNo(d) == True:
                        fflag_configuration["EFlagDiscordWebhookBloxstrapRPC"] = False
                        printDebugMessage("User selected: False")
                    printMainMessage("Would you like it to show the pid number in the webhook footer? (y/n)")
                    d = input("> ")
                    if isYes(d) == True:
                        fflag_configuration["EFlagDiscordWebhookShowPidInFooter"] = True
                        printDebugMessage("User selected: True")
                    elif isNo(d) == True:
                        fflag_configuration["EFlagDiscordWebhookShowPidInFooter"] = False
                        printDebugMessage("User selected: False")
                else:
                    fflag_configuration["EFlagUseDiscordWebhook"] = False
                    printErrorMessage("The provided webhook link is not a valid format.")
            elif isNo(d) == True:
                fflag_configuration["EFlagUseDiscordWebhook"] = False
                printDebugMessage("User selected: False")

        printMainMessage("Would you like to enable Debug Mode? (y/n)")
        printYellowMessage("[WARNING! This will expose information like login to Roblox.]")
        printYellowMessage("[DO NOT EVER ENABLE IF SOMEONE TOLD YOU SO OR YOU USUALLY RECORD!!]")
        d = input("> ")
        if isYes(d) == True:
            fflag_configuration["EFlagEnableDebugMode"] = True
            printDebugMessage("User selected: True")
        elif isNo(d) == True:
            fflag_configuration["EFlagEnableDebugMode"] = False
            printDebugMessage("User selected: False")

        if fflag_configuration.get("EFlagEnableDebugMode") == True:
            printMainMessage("Would you like to print unhandled Roblox client events? (y/n)")
            d = input("> ")
            if isYes(d) == True:
                fflag_configuration["EFlagAllowFullDebugMode"] = True
                printDebugMessage("User selected: True")
            elif isNo(d) == True:
                fflag_configuration["EFlagAllowFullDebugMode"] = False
                printDebugMessage("User selected: False")

        printMainMessage("Would you like to reinstall a fresh copy of Roblox every launch? (y/n)")
        d = input("> ")
        if isYes(d) == True:
            fflag_configuration["EFlagFreshCopyRoblox"] = True
            printDebugMessage("User selected: True")
        elif isNo(d) == True:
            fflag_configuration["EFlagFreshCopyRoblox"] = False
            printDebugMessage("User selected: False")

        printMainMessage("Would you like to skip the Bootstrap Start UI in the future? (y/n)")
        d = input("> ")
        if isYes(d) == True:
            fflag_configuration["EFlagSkipEfazRobloxBootstrapPromptUI"] = True
            printDebugMessage("User selected: True")
        elif isNo(d) == True:
            fflag_configuration["EFlagSkipEfazRobloxBootstrapPromptUI"] = False
            printDebugMessage("User selected: False")

        printMainMessage("Would you like to disable Bootstrap Update Checks? (y/n)")
        d = input("> ")
        if isYes(d) == True:
            fflag_configuration["EFlagDisableBootstrapChecks"] = True
            printDebugMessage("User selected: True")
        elif isNo(d) == True:
            fflag_configuration["EFlagDisableBootstrapChecks"] = False
            printDebugMessage("User selected: False")

        if (fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir") and os.path.exists(fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir"))):
            if main_os == "Windows":
                if os.path.exists(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}\\FastFlagConfiguration.json'):
                    with open(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}\\FastFlagConfiguration.json', "w") as f:
                        json.dump(fflag_configuration, f, indent=4)
                else:
                    printErrorMessage("Bootstrap Sync is not supported since the original unextracted directory is not found.")
            elif main_os == "Darwin":
                if os.path.exists(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}/FastFlagConfiguration.json'):
                    with open(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}/FastFlagConfiguration.json', "w") as f:
                        json.dump(fflag_configuration, f, indent=4)
                else:
                    printErrorMessage("Bootstrap Sync is not supported since the original unextracted directory is not found.")

        with open("FastFlagConfiguration.json", "w") as f:
            json.dump(fflag_configuration, f, indent=4)

        printSuccessMessage("Successfully saved Bootstrap Settings!")
    def handleOption5(): # Sync to Fast Flag Configuration
        printWarnMessage("--- Sync to Fast Flag Configuration ---")
        global fflag_configuration
        printMainMessage("Validating Bootstrap Install Directory..")
        if (fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir") and os.path.exists(fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir"))):
            if main_os == "Windows":
                if os.path.exists(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}\\FastFlagConfiguration.json'):
                    with open(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}\\FastFlagConfiguration.json', "w") as f:
                        json.dump(fflag_configuration, f, indent=4)
                    printSuccessMessage("Successfully synced Bootstrap Settings!")
                else:
                    printErrorMessage("Bootstrap Sync is not supported since the original unextracted directory is not found.")
            elif main_os == "Darwin":
                if os.path.exists(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}/FastFlagConfiguration.json'):
                    with open(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}/FastFlagConfiguration.json', "w") as f:
                        json.dump(fflag_configuration, f, indent=4)
                    printSuccessMessage("Successfully synced Bootstrap Settings!")
                else:
                    printErrorMessage("Bootstrap Sync is not supported since the original unextracted directory is not found.")
        else:
            printErrorMessage("Bootstrap Sync is not supported since the original unextracted directory is not found.")
    def handleOption6(): # Sync from Fast Flag Configuration
        printWarnMessage("--- Sync from Fast Flag Configuration ---")
        global fflag_configuration
        printMainMessage("Validating Bootstrap Install Directory..")
        if (fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir") and os.path.exists(fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir"))):
            if main_os == "Windows":
                if os.path.exists(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}\\FastFlagConfiguration.json'):
                    with open(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}\\FastFlagConfiguration.json', "r") as f:
                        fromFastFlagConfig = json.load(f)
                    fromFastFlagConfig["EFlagEfazRobloxBootStrapSyncDir"] = fflag_configuration["EFlagEfazRobloxBootStrapSyncDir"]
                    with open(f'FastFlagConfiguration.json', "w") as f:
                        json.dump(fromFastFlagConfig, f, indent=4)
                    printSuccessMessage("Successfully synced Bootstrap Settings!")
                else:
                    printErrorMessage("Bootstrap Sync is not supported since the original unextracted directory is not found.")
            elif main_os == "Darwin":
                if os.path.exists(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}/FastFlagConfiguration.json'):
                    with open(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}/FastFlagConfiguration.json', "r") as f:
                        fromFastFlagConfig = json.load(f)
                    fromFastFlagConfig["EFlagEfazRobloxBootStrapSyncDir"] = fflag_configuration["EFlagEfazRobloxBootStrapSyncDir"]
                    with open(f'FastFlagConfiguration.json', "w") as f:
                        json.dump(fromFastFlagConfig, f, indent=4)
                    printSuccessMessage("Successfully synced Bootstrap Settings!")
                else:
                    printErrorMessage("Bootstrap Sync is not supported since the original unextracted directory is not found.")
        else:
            printErrorMessage("Bootstrap Sync is not supported since the original unextracted directory is not found.")
    def handleOption7(): # Credits
        printWarnMessage("--- Credits ---")
        printMainMessage("1. Made by \033[38;5;202m@EfazDev\033[0m")
        printMainMessage("2. Old Death Sound and Cursors were sourced from \033[38;5;165mBloxstrap files (https://github.com/pizzaboxer/bloxstrap)\033[0m")
        printMainMessage("3. AvatarEditorMaps were from \033[38;5;197mMielesgames's Map Files (https://github.com/Mielesgames/RobloxAvatarEditorMaps)\033[0m slightly edited to be usable for the current version of Roblox (as of the time of writing this)")
        printMainMessage("4. Some files were exported from the main macOS Roblox.app files. \033[38;5;202m(Logo was from the Apple Pages icon, recolored and then added the Roblox Logo)\033[0m")
        if main_os == "Darwin":
            printMainMessage(f'5. macOS App was built using \033[38;5;39mpyinstaller\033[0m. You can recreate and deploy using this command (macOS only): \033[38;5;39mpyinstaller ./Apps/Scripts/Pyinstaller/EfazRobloxBootstrap.spec --distpath Apps --noconfirm && zip -r -y ./Apps/EfazRobloxBootstrapMac.zip "./Apps/EfazRobloxBootstrap.app" "./Apps/PlayRoblox" "./Apps/EfazRobloxBootstrapLoad.app" && rm -rf ./build/ ./Apps/EfazRobloxBootstrapLoad/ && {sys.executable} Install.py --install --disable-remove\033[0m')
        elif main_os == "Windows":
            if platform.architecture()[0] == "32bit":
                printMainMessage(f"5. Windows App was also built using \033[38;5;39mpyinstaller\033[0m. You can recreate and deploy using this command (windows only): \033[38;5;39mpyinstaller ./Apps/Scripts/Pyinstaller/EfazRobloxBootstrap_Windows32.spec --distpath Apps --noconfirm && move Apps\\EfazRobloxBootstrap32\\PlayRoblox32.exe Apps\\PlayRoblox\\ && {sys.executable} Install.py --install --disable-remove\033[0m")
            else:
                printMainMessage(f"5. Windows App was also built using \033[38;5;39mpyinstaller\033[0m. You can recreate and deploy using this command (windows only): \033[38;5;39mpyinstaller ./Apps/Scripts/Pyinstaller/EfazRobloxBootstrap_Windows.spec --distpath Apps --noconfirm && move Apps\\EfazRobloxBootstrap\\PlayRoblox.exe Apps\\PlayRoblox\\ && {sys.executable} Install.py --install --disable-remove\033[0m")
        printDebugMessage(f"Operating System: {main_os}")
    def handleOption8(): # End All Roblox Instances
        printWarnMessage("--- End All Roblox Instances ---")
        printMainMessage("Are you sure you want to end all currently open Roblox instances?")
        a = input("> ")
        if isYes(a) == True:
            handler.endRoblox()
    def handleOption9(): # Reinstall Roblox
        printWarnMessage("--- Reinstall Roblox ---")
        printMainMessage("Are you sure you want to reinstall Roblox?")
        if main_os == "Windows":
            printYellowMessage("WARNING! This will force-quit any open Roblox windows!")
        a = input("> ")
        if isYes(a) == True:
            handler.installRoblox(forceQuit=main_os == "Windows")
    def handleOption10(url_scheme=None): # Roblox Link Shortcuts
        printWarnMessage("--- Roblox Link Shortcuts ---")
        if type(url_scheme) is str:
            if '://' in url_scheme:
                path = url_scheme.split('://', 1)[1]
            else:
                path = url_scheme.split(':', 1)[1]
            generated_shortcut_id = path.replace("shortcuts/", "")
            if type(fflag_configuration.get("EFlagRobloxLinkShortcuts")) is dict:
                if fflag_configuration["EFlagRobloxLinkShortcuts"].get(generated_shortcut_id):
                    shortcut_info = fflag_configuration["EFlagRobloxLinkShortcuts"].get(generated_shortcut_id)
                    if type(shortcut_info.get("url")) is str and (shortcut_info.get("url").startswith("roblox:") or shortcut_info.get("url").startswith("roblox-player:")):
                        printSuccessMessage(f'Starting shortcut "{shortcut_info.get('name')}"!')
                        if len(given_args) > 1:
                            given_args[1] = shortcut_info["url"]
                        else:
                            given_args.append(shortcut_info["url"])
                    else:
                        printErrorMessage(f'You were redirected to a link shortcut with id "{generated_shortcut_id}" but it doesn\'t have a valid url.')
                        input("> ")
                        sys.exit(0)
                else:
                    printErrorMessage(f'You were redirected to a link shortcut with id "{generated_shortcut_id}" but it doesn\'t exist under your settings.')
                    input("> ")
                    sys.exit(0)
            else:
                printErrorMessage(f'You were redirected to a link shortcut with id "{generated_shortcut_id}" but it doesn\'t exist under your settings.')
                input("> ")
                sys.exit(0)
        else:
            generated_ui_options = []
            main_ui_options = {}
            if type(fflag_configuration.get("EFlagRobloxLinkShortcuts")) is dict:
                for i, v in fflag_configuration.get("EFlagRobloxLinkShortcuts").items():
                    if v and v.get("name") and v.get("id") and v.get("url"):
                        generated_ui_options.append({"index": 1, "message": f"{v.get('name')} [{i}]", "shortcut_info": v})
            generated_ui_options.append({"index": 999999, "message": "Create a new shortcut"})
            generated_ui_options.append({"index": 1000000, "message": "Delete a shortcut"})
            generated_ui_options = sorted(generated_ui_options, key=lambda x: x["index"])
            count = 1
            for i in generated_ui_options:
                printMainMessage(f"[{str(count)}] = {i['message']}")
                main_ui_options[str(count)] = i
                count += 1
            res = input("> ")
            if main_ui_options.get(res):
                opt = main_ui_options[res]
                if opt["index"] == 999999:
                    def loo():
                        printMainMessage("Enter the name to use for the shortcut: ")
                        name = input("> ")
                        printMainMessage("Enter the url to use for the shortcut (starts with \"roblox:\" or \"roblox-player:\"): ")
                        printMainMessage("Use this guide to help create it: https://github.com/pizzaboxer/bloxstrap/wiki/A-deep-dive-on-how-the-Roblox-bootstrapper-works#starting-roblox")
                        def urll():
                            ura = input("> ")
                            if ura.startswith("roblox:") or ura.startswith("roblox-player:"):
                                return ura
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
                            if fflag_configuration.get("EFlagRobloxLinkShortcuts"):
                                fflag_configuration.get("EFlagRobloxLinkShortcuts")[key] = {"url": ur, "name": name, "id": key}
                            else:
                                fflag_configuration["EFlagRobloxLinkShortcuts"] = {}
                                fflag_configuration["EFlagRobloxLinkShortcuts"][key] = {"url": ur, "name": name, "id": key}
                            printSuccessMessage(f'Successfully created shortcut "{name}"! You may use this link using your browser or go through the main menu to use this shortcut: efaz-bootstrap://shortcuts/{key}')
                        if (fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir") and os.path.exists(fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir"))):
                            if main_os == "Windows":
                                if os.path.exists(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}\\FastFlagConfiguration.json'):
                                    with open(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}\\FastFlagConfiguration.json', "w") as f:
                                        json.dump(fflag_configuration, f, indent=4)
                                else:
                                    printErrorMessage("Bootstrap Sync is not supported since the original unextracted directory is not found.")
                            elif main_os == "Darwin":
                                if os.path.exists(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}/FastFlagConfiguration.json'):
                                    with open(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}/FastFlagConfiguration.json', "w") as f:
                                        json.dump(fflag_configuration, f, indent=4)
                                else:
                                    printErrorMessage("Bootstrap Sync is not supported since the original unextracted directory is not found.")

                        with open("FastFlagConfiguration.json", "w") as f:
                            json.dump(fflag_configuration, f, indent=4)
                        printMainMessage("Would you like to create an another shortcut? (y/n)")
                        if isYes(input("> ")) == True:
                            loo()
                    loo()
                    handleOptionSelect(mes="Link Creation has finished! Would you like to continue to Roblox?")
                elif opt["index"] == 1000000:
                    if type(fflag_configuration.get("EFlagRobloxLinkShortcuts")) is dict:
                        def loo():
                            if type(fflag_configuration.get("EFlagRobloxLinkShortcuts")) is dict:
                                printMainMessage("Enter the key of the shortcut to delete: ")
                                key = input("> ")
                                if fflag_configuration.get("EFlagRobloxLinkShortcuts").get(key):
                                    info = fflag_configuration.get("EFlagRobloxLinkShortcuts")
                                    printMainMessage("Confirm the shortcut below? (y/n)")
                                    printMainMessage(f"Name: {info['name']}")
                                    printMainMessage(f"URL: {info['url']}")
                                    printMainMessage(f"Key: {key}")
                                    if isYes(input("> ")) == True:
                                        fflag_configuration["EFlagRobloxLinkShortcuts"][key] = {}
                                    if (fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir") and os.path.exists(fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir"))):
                                        if main_os == "Windows":
                                            if os.path.exists(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}\\FastFlagConfiguration.json'):
                                                with open(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}\\FastFlagConfiguration.json', "w") as f:
                                                    json.dump(fflag_configuration, f, indent=4)
                                            else:
                                                printErrorMessage("Bootstrap Sync is not supported since the original unextracted directory is not found.")
                                        elif main_os == "Darwin":
                                            if os.path.exists(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}/FastFlagConfiguration.json'):
                                                with open(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}/FastFlagConfiguration.json', "w") as f:
                                                    json.dump(fflag_configuration, f, indent=4)
                                            else:
                                                printErrorMessage("Bootstrap Sync is not supported since the original unextracted directory is not found.")

                                    with open("FastFlagConfiguration.json", "w") as f:
                                        json.dump(fflag_configuration, f, indent=4)
                                    printMainMessage("Would you like to delete an another shortcut? (y/n)")
                                    if isYes(input("> ")) == True:
                                        loo()
                                else:
                                    printErrorMessage("Key doesn't exist! Let's try again!")
                                    loo()
                        loo()
                        handleOptionSelect(mes="Link Deletion has finished! Would you like to continue to Roblox?")
                    else:
                        printErrorMessage("You have no shortcuts created!")
                        handleOptionSelect(mes="Link Deletion has finished! Would you like to continue to Roblox?")
                else:
                    if type(opt["shortcut_info"]["url"]) is str and (opt["shortcut_info"].get("url").startswith("roblox:") or opt["shortcut_info"].get("url").startswith("roblox-player:")):
                        printSuccessMessage(f"Starting shortcut \"{opt['shortcut_info']['name']}\"!")
                        if len(given_args) > 1:
                            given_args[1] = opt["shortcut_info"]["url"]
                        else:
                            given_args.append(opt["shortcut_info"]["url"])
                    else:
                        sys.exit(0)
            else:
                sys.exit(0)
    def handleOption11(): # Mods Manager
        global fflag_configuration
        def saveSettings():
            if (fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir") and os.path.exists(fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir"))):
                if main_os == "Windows":
                    if os.path.exists(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}\\FastFlagConfiguration.json'):
                        with open(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}\\FastFlagConfiguration.json', "w") as f:
                            json.dump(fflag_configuration, f, indent=4)
                    else:
                        printErrorMessage("Bootstrap Sync is not supported since the original unextracted directory is not found.")
                elif main_os == "Darwin":
                    if os.path.exists(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}/FastFlagConfiguration.json'):
                        with open(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}/FastFlagConfiguration.json', "w") as f:
                            json.dump(fflag_configuration, f, indent=4)
                    else:
                        printErrorMessage("Bootstrap Sync is not supported since the original unextracted directory is not found.")
            with open("FastFlagConfiguration.json", "w") as f:
                json.dump(fflag_configuration, f, indent=4)
        if fflag_configuration.get("EFlagEnableModModes") == True:
            def mainModManager():
                printWarnMessage("--- Mods Manager ---")
                printSuccessMessage(f"Mods Enabled: Yes")
                if (not (fflag_configuration.get("EFlagAllowActivityTracking") == True) or (fflag_configuration.get("EFlagAllowActivityTracking") == None)):
                    printMainMessage("Would you like to allow Activity Tracking on the Roblox client? (y/n)")
                    printMainMessage("This will allow features like:")
                    printMainMessage("- Server Locations")
                    printMainMessage("- BloxstrapRPC")
                    printMainMessage("- Discord Presence")
                    printMainMessage("- Discord Webhooks")
                    printMainMessage("- Mod Mode Scripts")
                    d = input("> ")
                    if isYes(d) == True:
                        fflag_configuration["EFlagAllowActivityTracking"] = True
                        saveSettings()
                        printDebugMessage("User selected: True")
                    elif isNo(d) == True:
                        fflag_configuration["EFlagAllowActivityTracking"] = False
                        saveSettings()
                        printDebugMessage("User selected: False")
                        return
                if os.path.exists(f"./Mods/{fflag_configuration.get('EFlagSelectedModMode')}/ModScript.py"):
                    printMainMessage(f"Selected Mod Script: {fflag_configuration.get('EFlagSelectedModMode')}")
                else:
                    printMainMessage(f"Selected Mod Script: None")
                printMainMessage("Select an option or a mod to enable/disable!")
                generated_ui_options = []
                main_ui_options = {}
                mods_manifest = generateModsManifest()
                for i, v in mods_manifest.items():
                    final_vers = "1.0.0"
                    final_name = ""
                    final_enabled = "❌"
                    final_mod_enabled = "❌"
                    if v.get("version"):
                        final_vers = v.get("version")
                    if v.get("enabled") == True:
                        final_enabled = "✅"
                    else:
                        final_enabled = "❌"
                    if v.get("name") == i:
                        final_name = f"{i}"
                    elif type(v.get("name")) is str:
                        final_name = f"{v.get('name')} [{i}]"
                    else:
                        final_name = f"{i}"
                    generated_ui_options.append({"index": 1, "message": f"[{final_enabled}] {final_name} [v{final_vers}]", "final_name": final_name, "mod_info": v, "mod_id": i})
                generated_ui_options.append({"index": 999998, "message": "Select Mod Script"})
                if (fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir") and os.path.exists(os.path.join(fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir"), "Mods"))):
                    generated_ui_options.append({"index": 999999, "message": "Sync Mods from Installation Folder"})
                generated_ui_options.append({"index": 1000000, "message": "Disable Appling Mods"})
                generated_ui_options.append({"index": 1000001, "message": "Exit Mods Manager"})
                generated_ui_options = sorted(generated_ui_options, key=lambda x: x["index"])
                count = 1
                for i in generated_ui_options:
                    printMainMessage(f"[{str(count)}] = {i['message']}")
                    main_ui_options[str(count)] = i
                    count += 1
                res = input("> ")
                if main_ui_options.get(res):
                    opt = main_ui_options[res]
                    if opt["index"] == 999998:
                        printMainMessage("Select a mod mode script to be used!")
                        mod_mode_script_generated_ui_options = []
                        mod_mode_script_ui_options = {}
                        for i, v in mods_manifest.items():
                            if v["mod_script"] == True:
                                if fflag_configuration.get('EFlagSelectedModMode') == i:
                                    final_mod_enabled = "✅"
                                else:
                                    final_mod_enabled = "❌"
                                if v.get("name") == i:
                                    final_name = f"{i}"
                                elif type(v.get("name")) is str:
                                    final_name = f"{v.get('name')} [{i}]"
                                else:
                                    final_name = f"{i}"
                                mod_mode_script_generated_ui_options.append({"index": 1, "message": f"[{final_mod_enabled}] {final_name} [v{final_vers}]", "final_name": final_name, "mod_info": v, "mod_id": i})
                        mod_mode_script_generated_ui_options.append({"index": 9999, "message": f"Disable Mod Mode Scripts"})
                        mod_mode_script_generated_ui_options = sorted(mod_mode_script_generated_ui_options, key=lambda x: x["index"])
                        mod_count = 1
                        if len(mod_mode_script_generated_ui_options) < 1:
                            printErrorMessage("No Mod Mode Scripts available. Please sync mods with a mod script in order for it to show here!")
                        else:
                            for i in mod_mode_script_generated_ui_options:
                                printMainMessage(f"[{str(mod_count)}] = {i['message']}")
                                mod_mode_script_ui_options[str(mod_count)] = i
                                mod_count += 1
                            res = input("> ")
                            if mod_mode_script_ui_options.get(res):
                                sel_mod_script = mod_mode_script_ui_options[res]
                                if sel_mod_script["index"] == 9999:
                                    fflag_configuration["EFlagSelectedModMode"] = None
                                    fflag_configuration["EFlagModModeAllowedDetectments"] = []
                                    fflag_configuration["EFlagEnableModModeScripts"] = False
                                    printSuccessMessage(f'Successfully changed current mod script to "{final_name}"!')
                                else:
                                    set_mod_mode = sel_mod_script["mod_id"]
                                    if sel_mod_script["mod_info"].get("mod_script") == True and os.path.exists(os.path.join(os.path.curdir, "Mods", set_mod_mode, "ModScript.py")) and fflag_configuration.get("EFlagAllowActivityTracking") == True:
                                        printMainMessage("You will enable the following for this item: ")
                                        with open(os.path.join(os.path.curdir, "Mods", set_mod_mode, "ModScript.py"), "r") as f:
                                            mod_mode_script_text = f.read()
                                        if not (sel_mod_script["mod_info"].get("permissions")):
                                            sel_mod_script["mod_info"]["permissions"] = []

                                        if "FastFlagConfiguration.json" in mod_mode_script_text and not ("fastFlagConfiguration" in sel_mod_script["mod_info"]["permissions"]): sel_mod_script["mod_info"]["permissions"].append("fastFlagConfiguration")
                                        if "Main.py" in mod_mode_script_text and not ("editMainExecutable" in sel_mod_script["mod_info"]["permissions"]): sel_mod_script["mod_info"]["permissions"].append("editMainExecutable")
                                        if "ModScript.py" in mod_mode_script_text and not ("editModScript" in sel_mod_script["mod_info"]["permissions"]): sel_mod_script["mod_info"]["permissions"].append("editModScript")
                                        if "MacOSNotification" in mod_mode_script_text and not ("macNotification" in sel_mod_script["mod_info"]["permissions"]): sel_mod_script["mod_info"]["permissions"].append("macNotification")
                                        if "Mods" in mod_mode_script_text and not ("configureMods" in sel_mod_script["mod_info"]["permissions"]): sel_mod_script["mod_info"]["permissions"].append("configureMods")
                                        if "RobloxBrand" in mod_mode_script_text and not ("configureRobloxBranding" in sel_mod_script["mod_info"]["permissions"]): sel_mod_script["mod_info"]["permissions"].append("configureRobloxBranding")
                                        if "DeathSounds" in mod_mode_script_text and not ("configureDeathSounds" in sel_mod_script["mod_info"]["permissions"]): sel_mod_script["mod_info"]["permissions"].append("configureDeathSounds")
                                        if "Cursors" in mod_mode_script_text and not ("configureCursors" in sel_mod_script["mod_info"]["permissions"]): sel_mod_script["mod_info"]["permissions"].append("configureCursors")
                                        if "AvatarEditorMaps" in mod_mode_script_text and not ("configureAvatarMaps" in sel_mod_script["mod_info"]["permissions"]): sel_mod_script["mod_info"]["permissions"].append("configureAvatarMaps")

                                        for i in sel_mod_script["mod_info"].get("permissions", []):
                                            if type(i) is str and handler.robloxInstanceInfoNames.get(i):
                                                mai = handler.robloxInstanceInfoNames.get(i)
                                                if "Allow detecting every Roblox event" in mai or "Edit the main bootstrap executable" in mai:
                                                    printErrorMessage(f"- {handler.robloxInstanceInfoNames.get(i)}")
                                                elif "Allow detecting when Roblox HttpResponses are ran" in mai or "Allow detecting when Unknown Roblox Handlers are detected" in mai or "Edit or view your bootstrap configuration file" in mai or "Configure your mod modes" in mai or "Configure your Roblox client's branding" in mai or "Configure your death sounds" in mai or "Configure your cursors" in mai or "Configure your avatar maps" in mai or "Edit ModScript.py executable" in mai:
                                                    printWarnMessage(f"- {handler.robloxInstanceInfoNames.get(i)}")
                                                elif "Allow getting Job ID, Place ID and Roblox IP" in mai or "Allow detecting when loading " in mai or "Configure or send macOS Notifications through Bootstrap" in mai:
                                                    printYellowMessage(f"- {handler.robloxInstanceInfoNames.get(i)}")
                                                else:
                                                    printMainMessage(f"- {handler.robloxInstanceInfoNames.get(i)}")
                                            else:
                                                printErrorMessage(f"- Unknown Requirement")
                                        printYellowMessage("Please check the insides of the script before enabling even if someone asked you to install this!!")
                                        printYellowMessage("We won't be responsible for any damages by it! This includes if your Roblox Account or your computer are compromised!!")
                                        printYellowMessage("(y/n)")
                                        a = input("> ")
                                        if isYes(a) == True:
                                            if type(sel_mod_script["mod_info"].get("permissions", [])) is list:
                                                fflag_configuration["EFlagModModeAllowedDetectments"] = sel_mod_script["mod_info"].get("permissions", [])
                                            else:
                                                fflag_configuration["EFlagModModeAllowedDetectments"] = []
                                            fflag_configuration["EFlagSelectedModMode"] = set_mod_mode
                                            fflag_configuration["EFlagEnableModModeScripts"] = True
                                            printSuccessMessage(f'Successfully changed current mod script to "{sel_mod_script['final_name']}"!')
                                        else:
                                            fflag_configuration["EFlagModModeAllowedDetectments"] = []
                                            fflag_configuration["EFlagEnableModModeScripts"] = False
                                    else:
                                        fflag_configuration["EFlagModModeAllowedDetectments"] = []
                                        fflag_configuration["EFlagEnableModModeScripts"] = False
                                saveSettings()
                    elif opt["index"] == 999999:
                        printMainMessage("Syncing mods..")
                        targeted_sync_location = os.path.join(fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir"), "Mods")
                        if os.path.exists(targeted_sync_location) and os.path.isdir(targeted_sync_location):
                            for i in os.listdir(targeted_sync_location):
                                syncing_mod_path = os.path.join(targeted_sync_location, i)
                                if os.path.isdir(syncing_mod_path):
                                    shutil.copytree(syncing_mod_path, f"./Mods/{i}/", dirs_exist_ok=True)
                            printSuccessMessage("Successfully synced all mods from installation folder!")
                        else:
                            printErrorMessage("Something went wrong.")
                    elif opt["index"] == 1000000:
                        printMainMessage("Disabling mods..")
                        fflag_configuration["EFlagEnableModModes"] = False
                        saveSettings()
                        printSuccessMessage("Successfully disabled Mods! Would you like to reinstall Roblox to clear existing mods or continue with partial setup?")
                        if main_os == "Windows":
                            printYellowMessage("WARNING! This will quit any open Roblox windows!")
                        d = input("> ")
                        if isYes(d) == True:
                            if main_os == "Windows":
                                handler.installRoblox(forceQuit=True)
                            else:
                                handler.installRoblox()
                        elif isNo(d) == True:
                            saveSettings()
                            printDebugMessage("User selected: False")
                            return
                        printMainMessage("Exiting Mods Manager..")
                        return
                    elif opt["index"] == 1000001:
                        printMainMessage("Exiting Mods Manager..")
                        return
                    else:
                        if not (fflag_configuration.get("EFlagEnabledMods") and type(fflag_configuration["EFlagEnabledMods"]) is dict):
                            fflag_configuration["EFlagEnabledMods"] = {}
                        if opt.get("mod_info"):
                            if opt["mod_info"]["enabled"] == True:
                                fflag_configuration["EFlagEnabledMods"][opt["mod_id"]] = False
                                printSuccessMessage(f"Successfully disabled mod {opt.get('final_name')}!")
                            else:
                                fflag_configuration["EFlagEnabledMods"][opt["mod_id"]] = True
                                printSuccessMessage(f"Successfully enabled mod {opt.get('final_name')}!")
                        saveSettings()
                    mainModManager()
                else:
                    return
            mainModManager()
        else:
            printWarnMessage("--- Mods Manager ---")
            printErrorMessage("Mods Enabled: No")
            printMainMessage("Would you like to enable Mods? (y/n)")
            b = input("> ")
            if isYes(b) == True:
                fflag_configuration["EFlagEnableModModes"] = True
                saveSettings()
                handleOption11()

    def handleOptionSelect(mes="Option finished! Would you like to continue to Roblox? (y/n)"): # Handle Continue to Roblox
        printWarnMessage(mes)
        a = input("> ")
        if isYes(a) == False:
            sys.exit(0)

    # Continue to Menu or URL Handler
    continue_to_url_handler = False
    if len(given_args) > 1:
        if "efaz-bootstrap:" in given_args[1]:
            continue_to_url_handler = True

    # Main Menu
    if (not (fflag_configuration.get("EFlagRemoveMenuAndSkipToRoblox") == True)) or continue_to_url_handler == True:
        if (len(given_args) < 2):
            if not (fflag_configuration.get("EFlagCompletedTutorial") == True): # Tutorial
                printWarnMessage("--- Tutorial ---")
                printMainMessage("Welcome to Efaz's Roblox Bootstrap!")
                printMainMessage("Efaz's Roblox Bootstrap is a Roblox bootstrap that allows you to add modifications to your Roblox client using files, activity tracking and Python!")
                if main_os == "Darwin":
                    if os.path.exists("/Applications/EfazRobloxBootstrap.app"):
                        printSuccessMessage("It seems like everything is working, so you can reach the next part!")
                    else:
                        printErrorMessage("I'm sorry, but you're not quite finished yet. Please run Install.py instead of Main.py!!")
                        input("> ")
                        sys.exit(0)
                elif main_os == "Windows":
                    if os.path.exists(f"{os.getenv('LOCALAPPDATA')}\\EfazRobloxBootstrap\\"):
                        printSuccessMessage("It seems like everything is working, so you can reach the next part!")
                    else:
                        printErrorMessage("I'm sorry, but you're not quite finished yet. Please run Install.py instead of Main.py!!")
                        input("> ")
                        sys.exit(0)

                printMainMessage("Before we get started, there's some information you may need to know.")
                printWarnMessage("--- Information 1 ---")
                if main_os == "Darwin":
                    printMainMessage("First, you may need to know that after you go to Roblox through this bootstrap, Roblox will not be able to be opened normally.")
                    printMainMessage("This is because of macOS trying to scan signatures but failing.")
                    printMainMessage("Don't worry though, you will be able to join through your web browser since the app will sync.")
                    printYellowMessage("Additionally, if you want to uninstall this bootstrap, you may run Uninstall.py which is located in the same folder as the Install.py you ran to be here! However, you can use the Reinstall Roblox option in the bootstrap menu to prevent uninstalling this.")
                else:
                    printMainMessage("This info is only for macOS and you may continue!")
                input("> ")
                printWarnMessage("--- Information 2 ---")
                printMainMessage("Second, some features are based on Activity Tracking on your Roblox Client.")
                printMainMessage("This app will use your Roblox logs to track data such as Game Join Data, Discord Presences, BloxstrapRPC and more!")
                printYellowMessage("Don't worry, your Roblox account is safely secured and this won't get you banned.")
                input("> ")
                printWarnMessage("--- Information 3 ---")
                displayNotification("Hello!", "If you see this, your notifications are set up! Good job!")
                printMainMessage("We have just sent a notification to your device so that you can enable notifications.")
                printYellowMessage("Depending on your OS (Windows or macOS), you may be able to select Allow for features like Server Locations to work!")
                input("> ")
                printWarnMessage("--- Information 4 ---")
                printMainMessage("If you haven't noticed, we have installed a Play Roblox app into your system!")
                printMainMessage("This will allow you to skip the main menu and launch Roblox instantly through the bootstrap!")
                if main_os == "Darwin":
                    printMainMessage("You may find this in your Applications folder!")
                elif main_os == "Windows":
                    printMainMessage("You may find this in your Start Menu or Desktop!")
                input("> ")
                printWarnMessage("--- Step 1 ---")
                printMainMessage("Alright, now to the actual stuff, firstly, it's important you best understand on how the choosing works.")
                printMainMessage('Let\'s start off with a quick input! Let\'s say you want to enable this option (use the prompt here for the example), enter "y" or "yes"!')
                def a():
                    b = input("> ")
                    if isYes(b) == True:
                        return
                    else:
                        printErrorMessage("Uhm, not quite, try again!")
                        a()
                a()
                printWarnMessage("--- Step 2 ---")
                printMainMessage("Congrats! You completed the first step!")
                printMainMessage('Now, let\'s try that again! But instead, enter "n" or "no" for you don\'t want this feature!')
                def a():
                    b = input("> ")
                    if isNo(b) == True:
                        return
                    else:
                        printErrorMessage("Uhm, not quite, try again!")
                        a()
                a()
                printWarnMessage("--- Step 3 ---")
                printMainMessage("You're getting good at this!")
                printMainMessage('Now, let\'s learn about how you select from a list. Take the list below for an example.')
                printMainMessage("Try selecting a number that is next to that option!")
                generated_ui_options = []
                main_ui_options = {}
                generated_ui_options.append({"index": 1, "message": "Do jumping-jacks", "func": handleOption1})
                generated_ui_options.append({"index": 2, "message": "Do push-ups", "func": handleOption1})
                generated_ui_options.append({"index": 3, "message": "Do curl-ups", "func": handleOption1})
                generated_ui_options.append({"index": 4, "message": "Do weight-lifting", "func": handleOption1})
                generated_ui_options.append({"index": 5, "message": "Do neither", "func": handleOption1})
                generated_ui_options.append({"index": 6, "message": "Do all of the above", "func": handleOption1})
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
                printMainMessage("Nice job! Oh yea, during the tutorial, it will repeat with a \"Not quite\". However, it will close the window in future prompts like in main menu.")
                printYellowMessage("Additionally, if you do meet with an option with a *, this means that any input will result with that option.")
                printMainMessage("Anyways, welcome to step 4! Here, you can select your settings!")
                printMainMessage("[In the settings area, you can just input nothing or anything else instead of y or n to skip the option without affecting the current state of it.]")
                printMainMessage("See you after a little bit!")
                input("> ")
                handleOption4()
                printWarnMessage("--- Step 5 ---")
                printMainMessage("Welcome back! I hope you have enabled some things you may want!")
                printMainMessage("Now, let's get more customizable! Next, you will be able to select your fast flags.")
                printYellowMessage("But before, prepare yourself your Roblox User ID. It will be used for some settings depending on what you select.")
                input("> ")
                handleOption3()
                printWarnMessage("--- Final Touches ---")
                printSuccessMessage("Woo hoo! You finally reached the end of this tutorial!")
                printSuccessMessage("I hope you learned from this and how you may use Roblox using this bootstrap!")
                printSuccessMessage("For now, before you exit, I hope you have a great day!")
                input("> ")
                with open("FastFlagConfiguration.json", "r") as f:
                    try:
                        fflag_configuration = json.load(f)
                    except Exception as e:
                        fast_config_loaded = False
                fflag_configuration["EFlagCompletedTutorial"] = True
                if (fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir") and os.path.exists(fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir"))):
                    if main_os == "Windows":
                        if os.path.exists(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}\\FastFlagConfiguration.json'):
                            with open(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}\\FastFlagConfiguration.json', "w") as f:
                                json.dump(fflag_configuration, f, indent=4)
                        else:
                            printErrorMessage("Bootstrap Sync is not supported since the original unextracted directory is not found.")
                    elif main_os == "Darwin":
                        if os.path.exists(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}/FastFlagConfiguration.json'):
                            with open(f'{fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir")}/FastFlagConfiguration.json', "w") as f:
                                json.dump(fflag_configuration, f, indent=4)
                        else:
                            printErrorMessage("Bootstrap Sync is not supported since the original unextracted directory is not found.")
                with open("FastFlagConfiguration.json", "w") as f:
                    json.dump(fflag_configuration, f, indent=4)
            if not (fflag_configuration.get("EFlagSkipEfazRobloxBootstrapPromptUI") == True): # Main Menu
                generated_ui_options = []
                main_ui_options = {}
                generated_ui_options.append({"index": 1, "message": "Continue to Roblox", "func": handleOption1, "include_go_to_roblox": False})
                generated_ui_options.append({"index": 3, "message": "Run Fast Flag Installer", "func": handleOption3, "include_go_to_roblox": True, "include_message": "Installer has finished! Would you like to go to Roblox? (y/n)"})
                generated_ui_options.append({"index": 4, "message": "Open Mods Manager", "func": handleOption11, "include_go_to_roblox": True, "include_message": "Mod Settings has been saved! Would you like to go to Roblox? (y/n)"})
                generated_ui_options.append({"index": 5, "message": "Set Settings", "func": handleOption4, "include_go_to_roblox": True, "include_message": "Settings has been saved! Would you like to go to Roblox? (y/n)"})
                generated_ui_options.append({"index": 6, "message": "Roblox Link Shortcuts", "func": handleOption10, "include_go_to_roblox": False, "include_message": "Roblox Start Shortcut is set! Would you like to run it now? (y/n)"})
                generated_ui_options.append({"index": 7, "message": "End All Roblox Instances", "func": handleOption8, "include_go_to_roblox": True, "include_message": "Roblox Instances have been ended! Would you like to rerun it? (y/n)"})
                generated_ui_options.append({"index": 8, "message": "Reinstall Roblox", "func": handleOption9, "include_go_to_roblox": True, "include_message": "Roblox has been reinstalled! Would you like to run it now? (y/n)"})
                generated_ui_options.append({"index": 99, "message": "Credits", "func": handleOption7, "include_go_to_roblox": True, "include_message": "Would you like to go to Roblox? (y/n)"})
                if main_os == "Darwin" or main_os == "Windows":
                    if (fflag_configuration.get("EFlagEnableDuplicationOfClients") == True):
                        generated_ui_options.append({"index": 2, "message": "Generate Another Roblox Instance", "func": handleOption2, "include_go_to_roblox": False})
                if (fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir") and os.path.exists(fflag_configuration.get("EFlagEfazRobloxBootStrapSyncDir"))):
                    generated_ui_options.append({"index": 97, "message": "Sync to Fast Flag Configuration", "func": handleOption5, "include_go_to_roblox": True, "include_message": "Sync finished! Would you like to run Roblox now? (y/n)"})
                    generated_ui_options.append({"index": 98, "message": "Sync from Fast Flag Configuration", "func": handleOption6, "include_go_to_roblox": True, "include_message": "Sync finished! Would you like to run Roblox now? (y/n)"})

                generated_ui_options = sorted(generated_ui_options, key=lambda x: x["index"])
                printWarnMessage("--- Main Menu ---")
                count = 1
                for i in generated_ui_options:
                    printMainMessage(f"[{str(count)}] = {i['message']}")
                    main_ui_options[str(count)] = i
                    count += 1

                res = input("> ")
                if main_ui_options.get(res):
                    opt = main_ui_options[res]
                    opt["func"]()
                    if opt.get("include_go_to_roblox") == True: handleOptionSelect(opt.get("include_message"))
                else:
                    sys.exit(0)

                fast_config_loaded = True
                with open("FastFlagConfiguration.json", "r") as f:
                    try:
                        fflag_configuration = json.load(f)
                    except Exception as e:
                        fast_config_loaded = False

                if fflag_configuration.get("EFlagSkipEfazRobloxBootstrapPromptUI") == None:
                    printMainMessage("Would you like to skip the Bootstrap Start UI in the future? (y/n)")
                    skipInFuture = input("> ")
                    
                    if isYes(skipInFuture) == True:
                        fflag_configuration["EFlagSkipEfazRobloxBootstrapPromptUI"] = True
                    else:
                        fflag_configuration["EFlagSkipEfazRobloxBootstrapPromptUI"] = False

                    with open("FastFlagConfiguration.json", "w") as f:
                        json.dump(fflag_configuration, f, indent=4)
            else: # Skip Efaz's Roblox Bootstrap Prompt UI
                printWarnMessage("--- Continue to Roblox? ---")
                printMainMessage("[1/*] = Continue")
                printMainMessage("[2] = Revert Remove UI")
                printMainMessage("[3] = End Process")
                res = input("> ")
                if res == "2":
                    fflag_configuration["EFlagSkipEfazRobloxBootstrapPromptUI"] = False
                    with open("FastFlagConfiguration.json", "w") as f:
                        json.dump(fflag_configuration, f, indent=4)
                    printSuccessMessage("Reverted successfully!")
                    input("> ")
                    sys.exit(0)
                elif res == "3":
                    sys.exit(0)
        elif len(given_args) > 1: # URL Scheme Handler
            url = given_args[1]
            if "efaz-bootstrap" in url:
                if "continue" in url:
                    handleOption1()
                elif "new" in url:
                    handleOption2()
                elif "fflag-install" in url:
                    handleOption3()
                    handleOptionSelect()
                elif "settings" in url:
                    handleOption4()
                    handleOptionSelect()
                elif "sync-to-install" in url:
                    handleOption5()
                    handleOptionSelect()
                elif "sync-from-install" in url:
                    handleOption6()
                    handleOptionSelect()
                elif "end-roblox" in url:
                    handleOption8()
                    handleOptionSelect()
                elif "reinstall-roblox" in url:
                    handleOption9()
                    handleOptionSelect()
                elif ("credits" in url) or ("about" in url):
                    handleOption7()
                    handleOptionSelect()
                elif "mods" in url:
                    handleOption11()
                    handleOptionSelect()
                elif ("shortcuts/" in url):
                    handleOption10(url)
                else:
                    printDebugMessage(f"Unknown command: {url}")
                    printWarnMessage("--- Continue to Roblox? ---")
                    printMainMessage("[1] = Continue")
                    printMainMessage("[69] = Remove Skip UI")
                    printMainMessage("[*] = End Process")
                    res = input("> ")
                    if res == "1":
                        handleOption1()
                    elif res == "69":
                        fflag_configuration["EFlagSkipEfazRobloxBootstrapPromptUI"] = False
                        with open("FastFlagConfiguration.json", "w") as f:
                            json.dump(fflag_configuration, f, indent=4)
                        printSuccessMessage("Reverted successfully!")
                        printWarnMessage("Option finished! Would you like to continue to Roblox? (y/n)")
                        a = input("> ")
                        if isYes(a) == False:
                            sys.exit(0)
                    else:
                        sys.exit(0)
    
    # Check for Updates
    if (not (fflag_configuration.get("EFlagDisableBootstrapChecks") == True)) and os.path.exists("Version.json"):
        printWarnMessage("--- Checking for Bootstrap Updates ---")
        skip_check = False
        try:
            import requests
        except Exception as e:
            printMainMessage("Some modules are not installed. Do you want to install all the modules required now? (y/n)")
            pip_class.install(["requests"])
            import requests
            printSuccessMessage("Successfully installed modules!")
        if skip_check == False:
            latest_vers_res = requests.get("https://raw.githubusercontent.com/EfazDev/roblox-bootstrap/main/Version.json")
            if latest_vers_res.ok:
                latest_vers = latest_vers_res.json()
                if current_version.get("version"):
                    if current_version.get("version", "1.0.0") < latest_vers.get("latest_version", "1.0.0"):
                        printDebugMessage(f"Update v{latest_vers['latest_version']} detected!")
                        printWarnMessage("--- New Bootstrap Update ---")
                        printMainMessage(f"We have detected a new version of Efaz's Roblox Bootstrap! Would you like to install it? (y/n)")
                        printSuccessMessage(f"v{current_version.get('version', '1.0.0')} [Current] => v{latest_vers['latest_version']} [Latest]")
                        if isYes(input("> ")) == True:
                            printMainMessage("Downloading latest version..")
                            download_update = subprocess.run(["curl", "-L", "https://github.com/EfazDev/roblox-bootstrap/archive/refs/heads/main.zip", "-o", "./Update.zip"], check=True)
                            if download_update.returncode == 0:
                                printMainMessage("Download Success! Extracting ZIP now!")
                                if main_os == "Darwin":
                                    zip_extract = subprocess.run(["unzip", "-o", "Update.zip", "-d", "./Update/"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                                elif main_os == "Windows":
                                    zip_extract = subprocess.run(["powershell", "-command", f"Expand-Archive -Path 'Update.zip' -DestinationPath './Update/' -Force"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                                if zip_extract.returncode == 0:
                                    printMainMessage("Extracted successfully! Installing Files!")
                                    for file in os.listdir("./Update/roblox-bootstrap-main/"):
                                        src_path = os.path.join("./Update/roblox-bootstrap-main/", file)
                                        dest_path = os.path.join("./", file)
                                        
                                        if os.path.isdir(src_path):
                                            shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
                                        else:
                                            if not file.endswith(".json"):
                                                shutil.copy2(src_path, dest_path)
                                    if latest_vers.get("versions_required_install"):
                                        if latest_vers.get("versions_required_install").get(current_version.get('version', '1.0.0')) == True:
                                            printMainMessage("Updating Files..")
                                            silent_install = subprocess.run(args=[sys.executable, "Install.py", "--install", "--silent"])
                                            if not (silent_install.returncode == 0): printErrorMessage("Updating Files failed.")
                                    printMainMessage("Cleaning up files..")
                                    os.remove("Update.zip")
                                    shutil.rmtree("./Update/")
                                    printSuccessMessage(f"Update to v{latest_vers['version']} was finished successfully! Restarting bootstrap..")
                                    subprocess.run(args=[sys.executable] + given_args)
                                    sys.exit(0)
                                else:
                                    printMainMessage("Cleaning up files..")
                                    os.remove("Update.zip")
                                    shutil.rmtree("./Update/")
                                    printErrorMessage("Extracting ZIP File failed.")
                            else:
                                printErrorMessage("Downloading ZIP File failed.")
                        else:
                            printDebugMessage("User rejected update.")
                    else:
                        printMainMessage("Running latest version of Bootstrap!")
                else:
                    printDebugMessage("There was an error reading the latest version.")
            else:
                printErrorMessage("There was an issue while checking for updates.")
                printDebugMessage("Update Check Response failed.")
    if (not (fflag_configuration.get("EFlagDisableRobloxUpdateChecks") == True)):
        printWarnMessage("--- Checking for Roblox Updates ---")
        latest_roblox_version = handler.getLatestClientVersion(debug=(fflag_configuration.get("EFlagEnableDebugMode") == True))
        current_roblox_version = handler.getCurrentClientVersion()

        if fflag_configuration.get("EFlagFreshCopyRoblox") == True:
            if main_os == "Windows":
                if (multi_instance_enabled == True or fflag_configuration.get("EFlagEnableDuplicationOfClients") == True) and handler.getIfRobloxIsOpen():
                    printMainMessage("Skipping Roblox Reinstall due to Multi-Instancing enabled.")
                else:
                    printWarnMessage("--- Installing Latest Roblox Version ---")
                    handler.installRoblox(forceQuit=True, debug=(fflag_configuration.get("EFlagEnableDebugMode") == True))
            else:
                printWarnMessage("--- Installing Latest Roblox Version ---")
                handler.installRoblox(forceQuit=False, debug=(fflag_configuration.get("EFlagEnableDebugMode") == True))
            time.sleep(3)
        elif latest_roblox_version["success"] == True and current_roblox_version["success"] == True:
            if current_roblox_version["isClientVersion"] == True:
                if current_roblox_version["version"] == latest_roblox_version["client_version"]:
                    printMainMessage("Running latest version of Roblox!")
                else:
                    printWarnMessage("--- Installing Latest Roblox Version ---")
                    handler.installRoblox(forceQuit=main_os == "Windows", debug=(fflag_configuration.get("EFlagEnableDebugMode") == True))
                    time.sleep(3)
            else:
                if current_roblox_version["version"] == latest_roblox_version["short_version"]:
                    printMainMessage("Running latest version of Roblox!")
                else:
                    printWarnMessage("--- Installing Latest Roblox Version ---")
                    handler.installRoblox(forceQuit=main_os == "Windows", debug=(fflag_configuration.get("EFlagEnableDebugMode") == True))
                    time.sleep(3)
        else:
            printErrorMessage("There was an issue while checking for updates.")
    
    # Reinstate Windows Shortcuts
    if main_os == "Windows":
        if os.path.exists(os.path.join(f"{os.getenv('LOCALAPPDATA')}", "EfazRobloxBootstrap", "EfazRobloxBootstrap.exe")):
            if not (fflag_configuration.get("EFlagDisableURLSchemeInstall") == True):
                printWarnMessage("--- Configuring Windows Registry ---")
                bootstrap_folder_path = os.path.join(f"{os.getenv('LOCALAPPDATA')}", "EfazRobloxBootstrap")
                bootstrap_path = os.path.join(bootstrap_folder_path, "EfazRobloxBootstrap.exe")
                try:
                    import requests
                    import winreg
                    import win32com.client
                except Exception as e:
                    pip_class.install(["requests"])
                    pip_class.install(["pywin32"])
                    import requests
                    import winreg
                    import win32com.client
                # Reapply URL Schemes
                printMainMessage("Setting up URL Schemes..")
                def set_url_scheme(protocol, exe_path):
                    protocol_key = r"Software\Classes\{}".format(protocol)
                    command_key = r"Software\Classes\{}\shell\open\command".format(protocol)
                    try:
                        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, protocol_key) as key:
                            winreg.SetValue(key, "", winreg.REG_SZ, "URL:{}".format(protocol))
                            winreg.SetValueEx(key, "URL Protocol", 0, winreg.REG_SZ, protocol)
                        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, command_key) as key:
                            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, '"{}" "%1"'.format(exe_path))
                        printDebugMessage(f'URL scheme "{protocol}" has been set for "{exe_path}"')
                    except Exception as e:
                        printErrorMessage(f"An error occurred: {e}")
                set_url_scheme("efaz-bootstrap", bootstrap_path)
                set_url_scheme("roblox-player", bootstrap_path)
                set_url_scheme("roblox", bootstrap_path)

            # Reapply Shortcuts
            printMainMessage("Setting up shortcuts..")
            def create_shortcut(target_path, shortcut_path, working_directory=None, icon_path=None):
                shell = win32com.client.Dispatch('WScript.Shell')
                shortcut = shell.CreateShortcut(shortcut_path)
                shortcut.TargetPath = target_path
                if working_directory: shortcut.WorkingDirectory = working_directory
                if icon_path: shortcut.IconLocation = icon_path
                shortcut.save()
            create_shortcut(bootstrap_path, os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), "Efaz's Roblox Bootstrap.lnk"))
            create_shortcut(bootstrap_path, os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs'), "Efaz's Roblox Bootstrap.lnk"))

            # Reapply Installation to Windows
            printMainMessage("Marking Program Installation into Windows..")
            app_key = "Software\\EfazRobloxBootstrap"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, app_key) as key:
                winreg.SetValueEx(key, "InstallPath", 0, winreg.REG_SZ, bootstrap_folder_path)
                winreg.SetValueEx(key, "Installed", 0, winreg.REG_DWORD, 1)
            registry_path = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\EfazRobloxBootstrap"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, registry_path) as key:
                winreg.SetValueEx(key, "UninstallString", 0, winreg.REG_SZ, f"py {os.path.join(bootstrap_folder_path, "Uninstall.py")}")
                winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, "Efaz's Roblox Bootstrap")
                winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, current_version["version"])
                winreg.SetValueEx(key, "DisplayIcon", 0, winreg.REG_SZ, os.path.join(bootstrap_folder_path, "AppIcon.ico"))

    # Prepare Roblox
    printWarnMessage("--- Preparing Roblox ---")
    def prepareRoblox():
        global fflag_configuration
        if handler.getIfRobloxIsOpen():
            if main_os == "Windows":
                if multi_instance_enabled == True or len(given_args) > 1:
                    printYellowMessage("Roblox is currently open which prevents file changing by Windows or the hard drive's file system.")
                    return
                else:
                    handler.endRoblox()
                    time.sleep(2)

        if fflag_configuration.get("EFlagRemoveBuilderFont") == True or (fflag_configuration.get("EFlagEnableNewFontNameMappingABTest2") and fflag_configuration.get("EFlagEnableNewFontNameMappingABTest2").lower() == "false"):
            printMainMessage("Changing Font Files..")
            copyFile(f"{stored_font_folder_destinations[found_platform]}GothamSSm-Black.otf", f"{stored_font_folder_destinations[found_platform]}BuilderSans-ExtraBold.otf")
            copyFile(f"{stored_font_folder_destinations[found_platform]}GothamSSm-Medium.otf", f"{stored_font_folder_destinations[found_platform]}BuilderSans-Bold.otf")
            copyFile(f"{stored_font_folder_destinations[found_platform]}GothamSSm-Medium.otf", f"{stored_font_folder_destinations[found_platform]}BuilderSans-Medium.otf")
            copyFile(f"{stored_font_folder_destinations[found_platform]}GothamSSm-Book.otf", f"{stored_font_folder_destinations[found_platform]}BuilderSans-Regular.otf")
            copyFile(f"{stored_font_folder_destinations[found_platform]}GothamSSm-Black.otf", f"{stored_font_folder_destinations[found_platform]}Montserrat-Black.ttf")
            copyFile(f"{stored_font_folder_destinations[found_platform]}GothamSSm-Bold.otf", f"{stored_font_folder_destinations[found_platform]}Montserrat-Bold.ttf")
            copyFile(f"{stored_font_folder_destinations[found_platform]}GothamSSm-Medium.otf", f"{stored_font_folder_destinations[found_platform]}Montserrat-Medium.ttf")
            copyFile(f"{stored_font_folder_destinations[found_platform]}GothamSSm-Book.otf", f"{stored_font_folder_destinations[found_platform]}Montserrat-Regular.ttf")
            printSuccessMessage("Successfully changed Builder San files to GothamSSm!")
        
        if fflag_configuration.get("EFlagEnableModModes") == True:
            printMainMessage("Applying Mods..")
            for i in fflag_configuration.get("EFlagEnabledMods", []):
                mod_path = os.path.join("./Mods/", i)
                if os.path.exists(mod_path) and os.path.isdir(mod_path):
                    def ignore_files_here(dir, files): return set(["ModScript.py", "Manifest.json"]) & set(files)
                    if main_os == "Windows":
                        shutil.copytree(mod_path, f"{stored_content_folder_destinations[found_platform]}\\", dirs_exist_ok=True, ignore=ignore_files_here)
                    elif main_os == "Darwin":
                        shutil.copytree(mod_path, f"{stored_content_folder_destinations[found_platform]}/", dirs_exist_ok=True, ignore=ignore_files_here)
                    printDebugMessage(f'Successfully applied "{i}" mod!')
            printSuccessMessage("Successfully applied all enabled mods!")

        if fflag_configuration.get("EFlagEnableChangeAvatarEditorBackground") == True:
            printMainMessage("Changing Current Avatar Editor to Set Avatar Background..")
            if main_os == "Windows":
                copyFile(f"{os.path.curdir}\\AvatarEditorMaps\\{fflag_configuration['EFlagAvatarEditorBackground']}\\AvatarBackground.rbxl", f"{stored_content_folder_destinations[found_platform]}ExtraContent\\places\\Mobile.rbxl")
            elif main_os == "Darwin":
                copyFile(f"{os.path.curdir}/AvatarEditorMaps/{fflag_configuration['EFlagAvatarEditorBackground']}/AvatarBackground.rbxl", f"{stored_content_folder_destinations[found_platform]}ExtraContent/places/Mobile.rbxl")
            printSuccessMessage("Successfully changed current avatar editor with a set background!")
        else:
            printMainMessage("Changing Current Avatar Editor to Original Avatar Background..")
            if main_os == "Windows":
                copyFile(f"{os.path.curdir}\\AvatarEditorMaps\\Original\\AvatarBackground.rbxl", f"{stored_content_folder_destinations[found_platform]}ExtraContent\\places\\Mobile.rbxl")
            elif main_os == "Darwin":
                copyFile(f"{os.path.curdir}/AvatarEditorMaps/Original/AvatarBackground.rbxl", f"{stored_content_folder_destinations[found_platform]}ExtraContent/places/Mobile.rbxl")
            printSuccessMessage("Successfully changed current avatar editor to original background!")

        if fflag_configuration.get("EFlagEnableChangeCursor") == True:
            printMainMessage("Changing Current Cursor to Set Cursor..")
            if main_os == "Windows":
                copyFile(f"{os.path.curdir}\\Cursors\\{fflag_configuration['EFlagSelectedCursor']}\\ArrowCursor.png", f"{stored_content_folder_destinations[found_platform]}content\\textures\\Cursors\\KeyboardMouse\\ArrowCursor.png")
                copyFile(f"{os.path.curdir}\\Cursors\\{fflag_configuration['EFlagSelectedCursor']}\\ArrowFarCursor.png", f"{stored_content_folder_destinations[found_platform]}content\\textures\\Cursors\\KeyboardMouse\\ArrowFarCursor.png")
            elif main_os == "Darwin":
                copyFile(f"{os.path.curdir}/Cursors/{fflag_configuration['EFlagSelectedCursor']}/ArrowCursor.png", f"{stored_content_folder_destinations[found_platform]}content/textures/Cursors/KeyboardMouse/ArrowCursor.png")
                copyFile(f"{os.path.curdir}/Cursors/{fflag_configuration['EFlagSelectedCursor']}/ArrowFarCursor.png", f"{stored_content_folder_destinations[found_platform]}content/textures/Cursors/KeyboardMouse/ArrowFarCursor.png")
            printSuccessMessage("Successfully changed current cursor with a set cursor image!")
        else:
            printMainMessage("Changing Current Cursor to Original Cursor..")
            if main_os == "Windows":
                copyFile(f"{os.path.curdir}\\Cursors\\Original\\ArrowCursor.png", f"{stored_content_folder_destinations[found_platform]}content\\textures\\Cursors\\KeyboardMouse\\ArrowCursor.png")
                copyFile(f"{os.path.curdir}\\Cursors\\Original\\ArrowFarCursor.png", f"{stored_content_folder_destinations[found_platform]}content\\textures\\Cursors\\KeyboardMouse\\ArrowFarCursor.png")
            elif main_os == "Darwin":
                copyFile(f"{os.path.curdir}/Cursors/Original/ArrowCursor.png", f"{stored_content_folder_destinations[found_platform]}content/textures/Cursors/KeyboardMouse/ArrowCursor.png")
                copyFile(f"{os.path.curdir}/Cursors/Original/ArrowFarCursor.png", f"{stored_content_folder_destinations[found_platform]}content/textures/Cursors/KeyboardMouse/ArrowFarCursor.png")
            printSuccessMessage("Successfully changed current cursor with original cursor image!")

        if fflag_configuration.get("EFlagEnableChangeDeathSound") == True:
            printMainMessage("Changing Current Death Sound to Set Sound File..")
            if main_os == "Windows":
                copyFile(f"{os.path.curdir}\\DeathSounds\\{fflag_configuration['EFlagSelectedDeathSound']}", f"{stored_content_folder_destinations[found_platform]}content\\sounds\\ouch.ogg")
            elif main_os == "Darwin":
                copyFile(f"{os.path.curdir}/DeathSounds/{fflag_configuration['EFlagSelectedDeathSound']}", f"{stored_content_folder_destinations[found_platform]}content/sounds/ouch.ogg")
            printSuccessMessage("Successfully changed current death sound with a set sound file!")
        else:
            printMainMessage("Changing Current Death Sound to Original Sound File..")
            if main_os == "Windows":
                copyFile(f"{os.path.curdir}\\DeathSounds\\New.ogg", f"{stored_content_folder_destinations[found_platform]}content\\sounds\\ouch.ogg")
            elif main_os == "Darwin":
                copyFile(f"{os.path.curdir}/DeathSounds/New.ogg", f"{stored_content_folder_destinations[found_platform]}content/sounds/ouch.ogg")
            printSuccessMessage("Successfully changed current death sound with original sound file!")

        if fflag_configuration.get("EFlagEnableChangeBrandIcons") == True:
            if main_os == "Darwin":
                printMainMessage("Changing Current App Icon..")
                if os.path.exists(f"{os.path.curdir}/RobloxBrand/{fflag_configuration['EFlagSelectedBrandLogo']}/AppIcon.icns"):
                    copyFile(f"{os.path.curdir}/RobloxBrand/{fflag_configuration['EFlagSelectedBrandLogo']}/AppIcon.icns", f"{stored_content_folder_destinations[found_platform]}AppIcon.icns")
                if os.path.exists(f"{os.path.curdir}/RobloxBrand/{fflag_configuration['EFlagSelectedBrandLogo']}/MenuIcon.png"):
                    copyFile(f"{os.path.curdir}/RobloxBrand/{fflag_configuration['EFlagSelectedBrandLogo']}/MenuIcon.png", f"{stored_content_folder_destinations[found_platform]}content/textures/ui/TopBar/coloredlogo.png")
                if os.path.exists(f"{os.path.curdir}/RobloxBrand/{fflag_configuration['EFlagSelectedBrandLogo']}/MenuIcon@2x.png"):
                    copyFile(f"{os.path.curdir}/RobloxBrand/{fflag_configuration['EFlagSelectedBrandLogo']}/MenuIcon@2x.png", f"{stored_content_folder_destinations[found_platform]}content/textures/ui/TopBar/coloredlogo@2x.png")
                if os.path.exists(f"{os.path.curdir}/RobloxBrand/{fflag_configuration['EFlagSelectedBrandLogo']}/MenuIcon@3x.png"):
                    copyFile(f"{os.path.curdir}/RobloxBrand/{fflag_configuration['EFlagSelectedBrandLogo']}/MenuIcon@3x.png", f"{stored_content_folder_destinations[found_platform]}content/textures/ui/TopBar/coloredlogo@3x.png")
                if os.path.exists(f"{os.path.curdir}/RobloxBrand/{fflag_configuration['EFlagSelectedBrandLogo']}/RobloxLogo.png"):
                    copyFile(f"{os.path.curdir}/RobloxBrand/{fflag_configuration['EFlagSelectedBrandLogo']}/RobloxLogo.png", f"{stored_content_folder_destinations[found_platform]}content/textures/ui/ScreenshotHud/RobloxLogo.png")
                if os.path.exists(f"{os.path.curdir}/RobloxBrand/{fflag_configuration['EFlagSelectedBrandLogo']}/RobloxLogo@2x.png"):
                    copyFile(f"{os.path.curdir}/RobloxBrand/{fflag_configuration['EFlagSelectedBrandLogo']}/RobloxLogo@2x.png", f"{stored_content_folder_destinations[found_platform]}content/textures/ui/ScreenshotHud/RobloxLogo@2x.png")
                if os.path.exists(f"{os.path.curdir}/RobloxBrand/{fflag_configuration['EFlagSelectedBrandLogo']}/RobloxLogo@3x.png"):
                    copyFile(f"{os.path.curdir}/RobloxBrand/{fflag_configuration['EFlagSelectedBrandLogo']}/RobloxLogo@3x.png", f"{stored_content_folder_destinations[found_platform]}content/textures/ui/ScreenshotHud/RobloxLogo@3x.png")
                if os.path.exists(f"{os.path.curdir}/RobloxBrand/{fflag_configuration['EFlagSelectedBrandLogo']}/RobloxNameIcon.png"):
                    copyFile(f"{os.path.curdir}/RobloxBrand/{fflag_configuration['EFlagSelectedBrandLogo']}/RobloxNameIcon.png", f"{stored_content_folder_destinations[found_platform]}content/textures/ui/RobloxNameIcon.png")
                if os.path.exists(f"{os.path.curdir}/RobloxBrand/{fflag_configuration['EFlagSelectedBrandLogo']}/RobloxTilt.png"):
                    copyFile(f"{os.path.curdir}/RobloxBrand/{fflag_configuration['EFlagSelectedBrandLogo']}/RobloxTilt.png", f"{stored_content_folder_destinations[found_platform]}content/textures/loading/robloxTilt.png")
                if os.path.exists(f"{os.path.curdir}/RobloxBrand/{fflag_configuration['EFlagSelectedBrandLogo']}/RobloxTilt.png"):
                    copyFile(f"{os.path.curdir}/RobloxBrand/{fflag_configuration['EFlagSelectedBrandLogo']}/RobloxTilt.png", f"{stored_content_folder_destinations[found_platform]}content/textures/loading/robloxTiltRed.png")
                printSuccessMessage("Successfully changed current app icon! It may take a moment for macOS to identify it!")
            else:
                printDebugMessage("Change App Icon while on an another operating system..?")
        else:
            if main_os == "Darwin":
                printMainMessage("Changing Current App Icon..")
                if os.path.exists(f"{os.path.curdir}/RobloxBrand/Original/AppIcon.icns"):
                    copyFile(f"{os.path.curdir}/RobloxBrand/Original/AppIcon.icns", f"{stored_content_folder_destinations[found_platform]}AppIcon.icns")
                if os.path.exists(f"{os.path.curdir}/RobloxBrand/Original/MenuIcon.png"):
                    copyFile(f"{os.path.curdir}/RobloxBrand/Original/MenuIcon.png", f"{stored_content_folder_destinations[found_platform]}content/textures/ui/TopBar/coloredlogo.png")
                if os.path.exists(f"{os.path.curdir}/RobloxBrand/Original/MenuIcon@2x.png"):
                    copyFile(f"{os.path.curdir}/RobloxBrand/Original/MenuIcon@2x.png", f"{stored_content_folder_destinations[found_platform]}content/textures/ui/TopBar/coloredlogo@2x.png")
                if os.path.exists(f"{os.path.curdir}/RobloxBrand/Original/MenuIcon@3x.png"):
                    copyFile(f"{os.path.curdir}/RobloxBrand/Original/MenuIcon@3x.png", f"{stored_content_folder_destinations[found_platform]}content/textures/ui/TopBar/coloredlogo@3x.png")
                if os.path.exists(f"{os.path.curdir}/RobloxBrand/Original/RobloxLogo.png"):
                    copyFile(f"{os.path.curdir}/RobloxBrand/Original/RobloxLogo.png", f"{stored_content_folder_destinations[found_platform]}content/textures/ui/ScreenshotHud/RobloxLogo.png")
                if os.path.exists(f"{os.path.curdir}/RobloxBrand/Original/RobloxLogo@2x.png"):
                    copyFile(f"{os.path.curdir}/RobloxBrand/Original/RobloxLogo@2x.png", f"{stored_content_folder_destinations[found_platform]}content/textures/ui/ScreenshotHud/RobloxLogo@2x.png")
                if os.path.exists(f"{os.path.curdir}/RobloxBrand/Original/RobloxLogo@3x.png"):
                    copyFile(f"{os.path.curdir}/RobloxBrand/Original/RobloxLogo@3x.png", f"{stored_content_folder_destinations[found_platform]}content/textures/ui/ScreenshotHud/RobloxLogo@3x.png")
                if os.path.exists(f"{os.path.curdir}/RobloxBrand/Original/RobloxNameIcon.png"):
                    copyFile(f"{os.path.curdir}/RobloxBrand/Original/RobloxNameIcon.png", f"{stored_content_folder_destinations[found_platform]}content/textures/ui/RobloxNameIcon.png")
                if os.path.exists(f"{os.path.curdir}/RobloxBrand/Original/RobloxTilt.png"):
                    copyFile(f"{os.path.curdir}/RobloxBrand/Original/RobloxTilt.png", f"{stored_content_folder_destinations[found_platform]}content/textures/loading/robloxTilt.png")
                if os.path.exists(f"{os.path.curdir}/RobloxBrand/Original/RobloxTilt.png"):
                    copyFile(f"{os.path.curdir}/RobloxBrand/Original/RobloxTilt.png", f"{stored_content_folder_destinations[found_platform]}content/textures/loading/robloxTiltRed.png")
                printSuccessMessage("Successfully changed current app icon! It may take a moment for macOS to identify it!")

        if main_os == "Darwin":
            if os.path.exists("/Applications/Roblox.app/Contents/Info.plist"):
                plist_data = handler.readPListFile("/Applications/Roblox.app/Contents/Info.plist")
                if plist_data.get("CFBundleName"):
                    printMainMessage("Editing Roblox Info.plist..")
                    if (fflag_configuration.get("EFlagEnableDuplicationOfClients") == True):
                        if plist_data.get("LSMultipleInstancesProhibited"):
                            plist_data["LSMultipleInstancesProhibited"] = False
                    else:
                        if plist_data.get("LSMultipleInstancesProhibited"):
                            plist_data["LSMultipleInstancesProhibited"] = True
                    if plist_data.get("CFBundleURLTypes"):
                        plist_data["CFBundleURLTypes"] = []
                    s = handler.writePListFile("/Applications/Roblox.app/Contents/Info.plist", plist_data)
                    if s["success"] == True:
                        printSuccessMessage("Successfully wrote to Info.plist!")
                    else:
                        printErrorMessage(f"Something went wrong saving Roblox Info.plist: {s['message']}")

        printMainMessage("Installing Fast Flags..")
        if fast_config_loaded == True:
            filtered_fast_flags = {}
            for i, v in fflag_configuration.items():
                if not i.startswith("EFlag"):
                    filtered_fast_flags[i] = v
            if not (fflag_configuration.get("EFlagEnableDuplicationOfClients") == True or multi_instance_enabled == True):
                if handler.getIfRobloxIsOpen():
                    handler.endRoblox()
                handler.installFastFlagsJSON(filtered_fast_flags, debug=(fflag_configuration.get("EFlagEnableDebugMode") == True))
            else:
                filtered_fast_flags["FFlagEnableSingleInstanceRobloxClient"] = False
                handler.installFastFlagsJSON(filtered_fast_flags, debug=(fflag_configuration.get("EFlagEnableDebugMode") == True), endRobloxInstances=False)
                if False:
                    handler.installFastFlagsJSON({ "FFlagEnableSingleInstanceRobloxClient": False }, debug=(fflag_configuration.get("EFlagEnableDebugMode") == True), endRobloxInstances=False)
        else:
            printErrorMessage("There was an error reading your configuration file.")
    prepareRoblox()

    # Mod Mode Scripts
    mod_mode_module = None
    mod_mode_json = None
    if fflag_configuration.get("EFlagEnableModModes") == True:
        if fflag_configuration.get("EFlagSelectedModMode") and not (fflag_configuration.get("EFlagAllowActivityTracking") == False) and fflag_configuration.get("EFlagEnableModModeScripts") == True and os.path.exists(os.path.join(os.path.curdir, "Mods", fflag_configuration.get("EFlagSelectedModMode"), "ModScript.py")):
            if os.path.exists(os.path.join(os.path.curdir, "Mods", fflag_configuration.get("EFlagSelectedModMode"), "Manifest.json")):
                mod_mode_json = readJSONFile(f"./Mods/{fflag_configuration.get('EFlagSelectedModMode')}/Manifest.json")
                if mod_mode_json:
                    if mod_mode_json.get("mod_script") == True:
                        printMainMessage("Preparing Mod Mode Script..")
                        with open(os.path.join(os.path.curdir, "Mods", fflag_configuration.get("EFlagSelectedModMode"), "ModScript.py"), "r") as f:
                            mod_mode_script_text = f.read()
                        approved_items_list = fflag_configuration.get("EFlagModModeAllowedDetectments")
                        approved_through_scan = True
                        if "FastFlagConfiguration.json" in mod_mode_script_text: 
                            if not ("fastFlagConfiguration" in approved_items_list):
                                approved_through_scan = False
                        if "Main.py" in mod_mode_script_text:
                            if not ("editMainExecutable" in approved_items_list):
                                approved_through_scan = False
                        if "ModScript.py" in mod_mode_script_text:
                            if not ("editModScript" in approved_items_list):
                                approved_through_scan = False
                        if "MacOSNotification" in mod_mode_script_text:
                            if not ("macNotification" in approved_items_list):
                                approved_through_scan = False
                        if "Mods" in mod_mode_script_text:
                            if not ("configureMods" in approved_items_list):
                                approved_through_scan = False
                        if "RobloxBrand" in mod_mode_script_text:
                            if not ("configureRobloxBranding" in approved_items_list):
                                approved_through_scan = False
                        if "DeathSounds" in mod_mode_script_text:
                            if not ("configureDeathSounds" in approved_items_list):
                                approved_through_scan = False
                        if "Cursors" in mod_mode_script_text:
                            if not ("configureCursors" in approved_items_list):
                                approved_through_scan = False
                        if "AvatarEditorMaps" in mod_mode_script_text:
                            if not ("configureAvatarMaps" in approved_items_list):
                                approved_through_scan = False

                        if approved_through_scan == True:
                            printDebugMessage("Connecting to mod mode script..")
                            script_path = os.path.join(os.path.curdir, "Mods", fflag_configuration.get("EFlagSelectedModMode"), "ModScript.py")
                            try:
                                spec = importlib.util.spec_from_file_location("ModScript", script_path)
                                mod_mode_module = importlib.util.module_from_spec(spec)
                                spec.loader.exec_module(mod_mode_module)
                                printSuccessMessage("Successfully connected to script!")
                            except Exception as e:
                                printDebugMessage(f"Error from mod mode module: {str(e)}")
                                printErrorMessage("Something went wrong while connecting to the mod mode module!")
                        else:
                            printErrorMessage("Mod script failed user approval inspection.")
    
    # Roblox is ready!
    printSuccessMessage("Done! Roblox is ready!")
    printWarnMessage("--- Running Roblox ---")

    # Event Variables
    setTypeOfServer = 0
    rpc = None
    rpc_info = None
    set_current_private_server_key = None
    current_place_info = None
    is_teleport = False
    connected_user_info = None
    updated_count = 0
    connected_roblox_instance = None

    # Event Functions
    def onGameJoined(info):
        if info.get("ip"):
            printDebugMessage(f"Roblox IP Address Detected! IP: {info.get("ip")}")
            allocated_roblox_ip = info.get("ip")
            generated_location = "Unknown Location"
            try:
                import requests
            except Exception as e:
                pip_class.install(["requests"])
                import requests
                printSuccessMessage("Successfully installed modules!")
            server_info_res = requests.get(f"https://ipinfo.io/{allocated_roblox_ip}/json")
            if server_info_res.ok:
                server_info_json = server_info_res.json()
                if server_info_json.get("city") and server_info_json.get("country"):
                    if not (server_info_json.get("region") == None or server_info_json.get("region") == ""):
                        generated_location = f"{server_info_json['city']}, {server_info_json['region']}, {server_info_json['country']}"
                    else:
                        generated_location = f"{server_info_json['city']}, {server_info_json['country']}"
                else:
                    if fflag_configuration.get("EFlagEnableDebugMode"): printDebugMessage(server_info_res.text)
                    printDebugMessage("Failed to get server information: IP Request resulted with no information.")
            else:
                if fflag_configuration.get("EFlagEnableDebugMode"): printDebugMessage(server_info_res.text)
                printDebugMessage("Failed to get server information: IP Request Rejected.")

            if fflag_configuration.get("EFlagNotifyServerLocation") == True:
                printSuccessMessage(f"Roblox is connecting to a server in: {generated_location} [{allocated_roblox_ip}]")
                if setTypeOfServer == 0:
                    displayNotification("Joining Server", f"You have connected to a server from {generated_location}!")
                elif setTypeOfServer == 1:
                    displayNotification("Joining Private Server", f"You have connected to a private server from {generated_location}!")
                elif setTypeOfServer == 2:
                    displayNotification("Joining Reserved Server", f"You have connected to a reserved server from {generated_location}!")
                elif setTypeOfServer == 3:
                    displayNotification("Joining Party", f"You have connected to a party server from {generated_location}!")
                else:
                    displayNotification("Joining Server", f"You have connected to a server from {generated_location}!")
                printDebugMessage("Sent Notification to Bootstrap for Notification Center shipping!")

            global current_place_info
            global connected_user_info
            if current_place_info:
                current_place_info["server_location"] = generated_location

                generated_universe_id_res = requests.get(f"https://apis.roblox.com/universes/v1/places/{current_place_info.get('placeId')}/universe")
                if generated_universe_id_res.ok:
                    generated_universe_id_json = generated_universe_id_res.json()
                    if generated_universe_id_json and not (generated_universe_id_json.get("universeId") == None):
                        current_place_info["universeId"] = generated_universe_id_json.get("universeId")
                    else:
                        current_place_info = None
                else:
                    current_place_info = None
                if current_place_info:
                    generated_thumbnail_api_res = requests.get(f"https://thumbnails.roblox.com/v1/games/icons?universeIds={current_place_info['universeId']}&returnPolicy=PlaceHolder&size=512x512&format=Png&isCircular=false")
                    generated_place_api_res = requests.get(f"https://develop.roblox.com/v1/universes/{current_place_info['universeId']}/places?isUniverseCreation=false&limit=50&sortOrder=Asc")
                    generated_universe_api_res = requests.get(f"https://games.roblox.com/v1/games?universeIds={current_place_info['universeId']}")
                    if generated_thumbnail_api_res.ok and generated_place_api_res.ok and generated_universe_api_res.ok:
                        generated_thumbnail_api_json = generated_thumbnail_api_res.json()
                        generated_place_api_json = generated_place_api_res.json()
                        generated_universe_api_json = generated_universe_api_res.json()

                        thumbnail_url = "https://raw.githubusercontent.com/EfazDev/roblox-bootstrap/main/BootstrapImages/DiscordIcon.png"
                        if generated_thumbnail_api_json.get("data"):
                            if len(generated_thumbnail_api_json.get("data")) > 0:
                                thumbnail_url = generated_thumbnail_api_json.get("data")[0]["imageUrl"]
                        if current_place_info:
                            current_place_info["thumbnail_url"] = thumbnail_url

                        if len(generated_place_api_json.get("data", [])) > 0 and len(generated_universe_api_json.get("data", [])) > 0:
                            generated_universe_api_json = generated_universe_api_json.get("data")[0]
                            place_info = {}
                            for place_under_experience in generated_place_api_json.get("data"):
                                if str(place_under_experience.get("id")) == str(current_place_info.get("placeId")):
                                    place_info = place_under_experience
                            if current_place_info:
                                if place_info:
                                    generated_universe_api_json["rootPlaceName"] = generated_universe_api_json["name"]
                                    for i in generated_universe_api_json.keys():
                                        if not place_info.get(i) and (not (i == "id" or i == "name" or i == "description" or i == "universeId")):
                                            place_info[i] = generated_universe_api_json[i]
                                    current_place_info["place_info"] = place_info
                            try:
                                start_time = datetime.datetime.now(tz=datetime.UTC).timestamp()
                                if fflag_configuration.get("EFlagSetDiscordRPCStart") and (type(fflag_configuration.get("EFlagSetDiscordRPCStart")) is float or type(fflag_configuration.get("EFlagSetDiscordRPCStart")) is int):
                                    start_time = fflag_configuration.get("EFlagSetDiscordRPCStart")
                                if current_place_info:
                                    current_place_info["start_time"] = start_time
                                if fflag_configuration.get("EFlagEnableDiscordRPC") == True:
                                    try:
                                        from DiscordPresenceHandler import Presence
                                        import requests
                                    except Exception as e:
                                        pip_class.install(["pypresence", "requests"])
                                        from DiscordPresenceHandler import Presence
                                        import requests
                                        printSuccessMessage("Successfully installed presence modules!")
                                    global rpc
                                    need_new_rpc = True
                                    try: 
                                        if rpc and rpc.connected == True:
                                            need_new_rpc = False
                                    except Exception as e:
                                        printDebugMessage(f"There was an error setting your Discord Embed: {str(e)}")
                                    if need_new_rpc == True:
                                        rpc = Presence("1005469189907173486")
                                        rpc.connect()
                                    def embed():
                                        try:
                                            global rpc
                                            global rpc_info
                                            global set_current_private_server_key

                                            err_count = 0
                                            loop_key = rpc.generate_loop_key()
                                            while True:
                                                if (not rpc) or (not rpc.connected) or (not rpc.current_loop_id == loop_key):
                                                    break
                                                if rpc_info == None:
                                                    rpc_info = {}
                                                playing_game_name = place_info['name']
                                                creator_name = f"Made by {place_info['creator']['name']}"
                                                creator_name = creator_name.replace("✅", "")
                                                if place_info.get("creator").get("hasVerifiedBadge") == True:
                                                    creator_name = f"{creator_name} ✅!"
                                                else:
                                                    creator_name = f"{creator_name}!"
                                                if not (place_info.get("rootPlaceId") == place_info.get("id")):
                                                    playing_game_name = f"{playing_game_name} ({place_info['rootPlaceName']})"
                                                formatted_info = {
                                                    "details": rpc_info.get("details") if rpc_info.get("details") else f"Playing {playing_game_name}",
                                                    "state": rpc_info.get("state") if rpc_info.get("state") else creator_name,
                                                    "start": rpc_info.get("start") if rpc_info.get("start") else start_time,
                                                    "stop": rpc_info.get("stop") if rpc_info.get("stop") and rpc_info.get("stop") > 1000 else None,
                                                    "large_image": rpc_info.get("large_image") if rpc_info.get("large_image") else thumbnail_url,
                                                    "large_text": rpc_info.get("large_text") if rpc_info.get("large_text") else playing_game_name,
                                                    "launch_data": rpc_info.get("launch_data") if rpc_info.get("launch_data") else ""
                                                }
                                                launch_data = ""
                                                add_exam = False
                                                if not formatted_info["launch_data"] == "":
                                                    formatted_info["launch_data"] = f"&launchData={formatted_info['launch_data']}"
                                                    add_exam = False
                                                if (setTypeOfServer == 1 or setTypeOfServer == 2 or setTypeOfServer == 3) and fflag_configuration.get("EFlagAllowPrivateServerJoining") == True and set_current_private_server_key:
                                                    if add_exam == True:
                                                        launch_data = f'{launch_data}?gameInstanceId={current_place_info["jobId"]}?accessCode={set_current_private_server_key}'
                                                    else:
                                                        launch_data = f'{launch_data}&gameInstanceId={current_place_info["jobId"]}&accessCode={set_current_private_server_key}'
                                                else:
                                                    if add_exam == True:
                                                        launch_data = f'{launch_data}?gameInstanceId={current_place_info["jobId"]}'
                                                    else:
                                                        launch_data = f'{launch_data}&gameInstanceId={current_place_info["jobId"]}'
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
                                                    if formatted_info.get("start") and formatted_info.get("end"):
                                                        isInstance = True
                                                    if rpc:
                                                        try:
                                                            if fflag_configuration.get("EFlagEnableDiscordRPCJoining") == True:
                                                                req = rpc.update(
                                                                    loop_key=loop_key, 
                                                                    details=formatted_info["details"], 
                                                                    state=formatted_info["state"], 
                                                                    start=formatted_info["start"], 
                                                                    end=formatted_info["stop"], 
                                                                    large_image=formatted_info["large_image"], 
                                                                    large_text=formatted_info["large_text"], 
                                                                    instance=isInstance, 
                                                                    small_image="https://raw.githubusercontent.com/EfazDev/roblox-bootstrap/main/BootstrapImages/DiscordIcon.png", 
                                                                    small_text="Efaz's Roblox Bootstrap", 
                                                                    buttons=[
                                                                        {
                                                                            "label": "Join Server! 🚀",
                                                                            "url": f"roblox://experiences/start?placeId={current_place_info['placeId']}{formatted_info['launch_data']}"
                                                                        }, 
                                                                        {
                                                                            "label": "Open Game Page 🌐", 
                                                                            "url": f"https://www.roblox.com/games/{current_place_info['placeId']}"
                                                                        }
                                                                    ]
                                                                )
                                                            else:
                                                                req = rpc.update(
                                                                    loop_key=loop_key, 
                                                                    details=formatted_info["details"], 
                                                                    state=formatted_info["state"], 
                                                                    start=formatted_info["start"], 
                                                                    end=formatted_info["stop"], 
                                                                    large_image=formatted_info["large_image"], 
                                                                    large_text=formatted_info["large_text"], 
                                                                    instance=isInstance, 
                                                                    small_image="https://raw.githubusercontent.com/EfazDev/roblox-bootstrap/main/BootstrapImages/DiscordIcon.png", 
                                                                    small_text="Efaz's Roblox Bootstrap", 
                                                                    buttons=[{
                                                                        "label": "Open Game Page 🌐", 
                                                                        "url": f"https://www.roblox.com/games/{current_place_info['placeId']}"
                                                                    }]
                                                                )
                                                            if req.get("code") == 2:
                                                                break
                                                        except Exception as e:
                                                            if err_count > 9:
                                                                printDebugMessage("Discord RPC Session may be broken. Loop has been broken.")
                                                                break
                                                            else:
                                                                err_count += 1
                                                except Exception as e:
                                                    if err_count > 9:
                                                        printDebugMessage("Discord RPC Session may be broken. Loop has been broken.")
                                                        break
                                                    else:
                                                        err_count += 1
                                                        printDebugMessage(f"There was an error setting your Discord Embed: {str(e)}")
                                                time.sleep(0.1)
                                        except Exception as e:
                                            printDebugMessage(f"There was an error setting your Discord Embed: {str(e)}")
                                    embed_thread = threading.Thread(target=embed)
                                    embed_thread.daemon = True
                                    embed_thread.start()
                                    printDebugMessage("Successfully attached Discord RPC!")
                                if fflag_configuration.get("EFlagUseDiscordWebhook") == True and fflag_configuration.get("EFlagDiscordWebhookConnect") == True:
                                    try:
                                        import requests
                                    except Exception as e:
                                        pip_class.install(["requests"])
                                        import requests
                                        printSuccessMessage("Successfully installed modules!")
                                    if fflag_configuration.get("EFlagDiscordWebhookURL"):
                                        title = "Joined Server!"
                                        color = 65280
                                        if setTypeOfServer == 0:
                                            title = "Joined Public Server!"
                                        elif setTypeOfServer == 1:
                                            title = "Joined Private Server!"
                                        elif setTypeOfServer == 2:
                                            title = "Joined Reserved Server!"
                                        elif setTypeOfServer == 3:
                                            title = "Joined Party!"
                                            color = 5570815
                                        else:
                                            title = "Joined Server!"
                                        launch_data = ""
                                        add_exam = False
                                        if not launch_data == "":
                                            launch_data = f"&launchData={launch_data}"
                                            add_exam = False
                                        if (setTypeOfServer == 1 or setTypeOfServer == 2 or setTypeOfServer == 3) and fflag_configuration.get("EFlagAllowPrivateServerJoining") == True and set_current_private_server_key:
                                            if add_exam == True:
                                                launch_data = f'{launch_data}?gameInstanceId={current_place_info["jobId"]}&accessCode={set_current_private_server_key}'
                                            else:
                                                launch_data = f'{launch_data}&gameInstanceId={current_place_info["jobId"]}&accessCode={set_current_private_server_key}'
                                        else:
                                            if add_exam == True:
                                                launch_data = f'{launch_data}?gameInstanceId={current_place_info["jobId"]}'
                                            else:
                                                launch_data = f'{launch_data}&gameInstanceId={current_place_info["jobId"]}'

                                        user_connected_text = "Unknown User"
                                        if connected_user_info:
                                            user_connected_text = f'[@{connected_user_info["name"]} [{connected_user_info["id"]}]](https://www.roblox.com/users/{connected_user_info["id"]}/profile)'

                                        generated_body = {
                                            "content": f"<@{fflag_configuration.get('EFlagDiscordWebhookUserId')}>",
                                            "embeds": [
                                                {
                                                    "title": title,
                                                    "color": color,
                                                    "fields": [
                                                        {
                                                            "name": "Connected Game",
                                                            "value": f"[{place_info['name']}](https://www.roblox.com/games/{current_place_info.get('placeId')})",
                                                            "inline": True
                                                        },
                                                        {
                                                            "name": "Join Link",
                                                            "value": f"[Join Now!](https://rbx.efaz.dev/join?placeId={current_place_info.get('placeId')}{launch_data})",
                                                            "inline": True
                                                        },
                                                        {
                                                            "name": "Started",
                                                            "value": f"<t:{int(start_time)}:R>",
                                                            "inline": True
                                                        },
                                                        {
                                                            "name": "User Connected",
                                                            "value": user_connected_text,
                                                            "inline": True
                                                        },
                                                        {
                                                            "name": "Server Location",
                                                            "value": f"{generated_location}",
                                                            "inline": True
                                                        }
                                                    ],
                                                    "author": {
                                                        "name": "Efaz's Roblox Bootstrap",
                                                        "icon_url": "https://raw.githubusercontent.com/EfazDev/roblox-bootstrap/main/BootstrapImages/DiscordIcon.png"
                                                    },
                                                    "thumbnail": {
                                                        "url": thumbnail_url
                                                    },
                                                    "footer": {
                                                        "text": f"Made by @EfazDev | PID: {connected_roblox_instance.pid}" if fflag_configuration.get("EFlagDiscordWebhookShowPidInFooter") == True else "Made by @EfazDev",
                                                        "icon_url": "https://cdn.efaz.dev/cdn/png/logo.png"
                                                    },
                                                    "timestamp": datetime.datetime.now(tz=datetime.UTC).strftime('%Y-%m-%dT%H:%M:%S.000Z')
                                                }
                                            ],
                                            "attachments": [],
                                        }
                                        try:
                                            req = requests.post(fflag_configuration.get("EFlagDiscordWebhookURL"), json=generated_body)
                                            if req.ok:
                                                printDebugMessage("Successfully sent webhook! Event: onGameJoined")
                                            else:
                                                printErrorMessage("There was an issue sending your webhook message. Is the webhook link valid?")
                                                printDebugMessage(f"Response: {req.text} | Status Code: {req.status_code}")
                                        except Exception as e:
                                            printErrorMessage("There was an issue sending your webhook message. Is the webhook link valid?")
                            except Exception as e:
                                rpc = None
                                printDebugMessage("Unable to insert Discord Rich Presence. Please make sure Discord is open.")
                        else:
                            printDebugMessage("Provided place info is not found.")
                    else:
                        printDebugMessage(f"Place responses rejected by Roblox. [{generated_thumbnail_api_res.ok},{generated_thumbnail_api_res.status_code} | {generated_place_api_res.ok},{generated_place_api_res.status_code}]")
    def onGameStart(info):
        global current_place_info
        if info.get("placeId") and info.get("jobId"):
            current_place_info = info
    def onGameDisconnected(info):
        global current_place_info
        global is_teleport
        global connected_user_info
        it_is_teleport = False
        synced_place_info = None
        if current_place_info:
            synced_place_info = current_place_info
            current_place_info = None
        if is_teleport == True:
            printYellowMessage("User has been teleported!")
            it_is_teleport = True
            is_teleport = False
        else:
            printErrorMessage("User has disconnected from the server!")
        if fflag_configuration.get("EFlagUseDiscordWebhook") == True and fflag_configuration.get("EFlagDiscordWebhookDisconnect") == True:
            try:
                import requests
            except Exception as e:
                pip_class.install(["requests"])
                import requests
                printSuccessMessage("Successfully installed modules!")
            if fflag_configuration.get("EFlagDiscordWebhookURL"):
                thumbnail_url = "https://raw.githubusercontent.com/EfazDev/roblox-bootstrap/main/BootstrapImages/DiscordIcon.png"
                server_location = "Unknown Location"
                start_time = 0
                place_info = {"name": "???"}

                if synced_place_info:
                    if synced_place_info.get("start_time"):
                        start_time = synced_place_info.get("start_time")
                    if synced_place_info.get("server_location"):
                        server_location = synced_place_info.get("server_location")
                    if synced_place_info.get("place_info"):
                        place_info = synced_place_info.get("place_info")
                    if synced_place_info.get("thumbnail_url"):
                        thumbnail_url = synced_place_info.get("thumbnail_url")

                    server_type = "Public Server"
                    if setTypeOfServer == 0:
                        server_type = "Public Server"
                    elif setTypeOfServer == 1:
                        server_type = "Private Server"
                    elif setTypeOfServer == 2:
                        server_type = "Reserved Server"
                    elif setTypeOfServer == 3:
                        server_type = "Party"
                    else:
                        server_type = "Public Server"

                    title = f"Disconnected from {server_type}!"
                    color = 16711680

                    if it_is_teleport == True:
                        title = f"Teleported to {server_type}!"
                        color = 16776960

                    launch_data = ""
                    add_exam = False
                    if not launch_data == "":
                        launch_data = f"&launchData={launch_data}"
                        add_exam = False
                    if (setTypeOfServer == 1 or setTypeOfServer == 2 or setTypeOfServer == 3) and fflag_configuration.get("EFlagAllowPrivateServerJoining") == True and set_current_private_server_key:
                        if add_exam == True:
                            launch_data = f'{launch_data}?gameInstanceId={synced_place_info["jobId"]}?accessCode={set_current_private_server_key}'
                        else:
                            launch_data = f'{launch_data}&gameInstanceId={synced_place_info["jobId"]}&accessCode={set_current_private_server_key}'
                    else:
                        if add_exam == True:
                            launch_data = f'{launch_data}?gameInstanceId={synced_place_info["jobId"]}'
                        else:
                            launch_data = f'{launch_data}&gameInstanceId={synced_place_info["jobId"]}'

                    user_connected_text = "Unknown User"
                    if connected_user_info:
                        user_connected_text = f'[@{connected_user_info["name"]} [{connected_user_info["id"]}]](https://www.roblox.com/users/{connected_user_info["id"]}/profile)'

                    generated_body = {
                        "content": f"<@{fflag_configuration.get('EFlagDiscordWebhookUserId')}>",
                        "embeds": [
                            {
                                "title": title,
                                "color": color,
                                "fields": [
                                    {
                                        "name": "Disconnected Game",
                                        "value": f"[{place_info['name']}](https://www.roblox.com/games/{synced_place_info.get('placeId')})",
                                        "inline": True
                                    },
                                    {
                                        "name": "Join Link",
                                        "value": f"[Join Again!](https://rbx.efaz.dev/join?placeId={synced_place_info.get('placeId')}{launch_data})",
                                        "inline": True
                                    },
                                    {
                                        "name": "Started",
                                        "value": f"<t:{int(start_time)}:R>",
                                        "inline": True
                                    },
                                    {
                                        "name": "User Connected",
                                        "value": user_connected_text,
                                        "inline": True
                                    },
                                    {
                                        "name": "Server Location",
                                        "value": f"{server_location}",
                                        "inline": True
                                    },
                                    {
                                        "name": "Closing Reason",
                                        "value": f"{info.get('message')} (Code: {info.get('code')})",
                                        "inline": True
                                    }
                                ],
                                "author": {
                                    "name": "Efaz's Roblox Bootstrap",
                                    "icon_url": "https://raw.githubusercontent.com/EfazDev/roblox-bootstrap/main/BootstrapImages/DiscordIcon.png"
                                },
                                "thumbnail": {
                                    "url": thumbnail_url
                                },
                                "footer": {
                                    "text": f"Made by @EfazDev | PID: {connected_roblox_instance.pid}" if fflag_configuration.get("EFlagDiscordWebhookShowPidInFooter") == True else "Made by @EfazDev",
                                    "icon_url": "https://cdn.efaz.dev/cdn/png/logo.png"
                                },
                                "timestamp": datetime.datetime.now(tz=datetime.UTC).strftime('%Y-%m-%dT%H:%M:%S.000Z')
                            }
                        ],
                        "attachments": []
                    }
                    try:
                        req = requests.post(fflag_configuration.get("EFlagDiscordWebhookURL"), json=generated_body)
                        if req.ok:
                            printDebugMessage("Successfully sent webhook!  Event: onGameDisconnected")
                        else:
                            printErrorMessage("There was an issue sending your webhook message. Is the webhook link valid?")
                            printDebugMessage(f"Response: {req.text} | Status Code: {req.status_code}")
                    except Exception as e:
                        printErrorMessage("There was an issue sending your webhook message. Is the webhook link valid?")
        if fflag_configuration.get("EFlagEnableDiscordRPC") == True:
            global rpc
            global rpc_info
            try: 
                if rpc:
                    rpc.clear()
            except Exception as e:
                printDebugMessage(f"There was an error setting your Discord Embed: {str(e)}")
            rpc_info = None
    def onTeleport(consoleLine):
        global is_teleport
        is_teleport = True
    def onBloxstrapMessage(info):
        if fflag_configuration.get("EFlagAllowBloxstrapSDK") == True:
            printMainMessage("Received Bloxstrap Message!")
            global rpc
            global rpc_info
            if info.get("command"):
                went_through = False
                data_names = {
                    "details": "Details",
                    "state": "State",
                    "timeStart": "Round Starting",
                    "timeEnd": "Round Ending",
                    "largeImage": "Large Image",
                    "launch_data": "URL Launch Data"
                }
                passed_data = {}
                if info["command"] == "SetRichPresence":
                    if rpc:
                        if rpc_info == None:
                            rpc_info = {}
                        if type(info["data"]) is dict:
                            if type(info["data"].get("details")) is str or type(info["data"].get("details")) is None: 
                                rpc_info["details"] = info["data"].get("details")
                                passed_data[data_names["details"]] = info["data"].get("details")
                            if type(info["data"].get("state")) is str or type(info["data"].get("state")) is None: 
                                rpc_info["state"] = info["data"].get("state")
                                passed_data[data_names["state"]] = info["data"].get("state")
                            if type(info["data"].get("timeStart")) is int or type(info["data"].get("timeStart")) is None or type(info["data"].get("timeStart")) is float: 
                                rpc_info["start"] = info["data"].get("timeStart")
                                passed_data[data_names["timeStart"]] = f'<t:{info["data"].get("timeStart")}:R>'
                            if type(info["data"].get("timeEnd")) is int or type(info["data"].get("timeEnd")) is None or type(info["data"].get("timeEnd")) is float: 
                                rpc_info["stop"] = info["data"].get("timeEnd")
                                passed_data[data_names["timeEnd"]] = f'<t:{info["data"].get("timeEnd")}:R>'
                            if type(info["data"].get("largeImage")) is dict: 
                                link = info["data"]["largeImage"].get("assetId")
                                if link and type(link) is int:
                                    link = f"[Image](https://assetdelivery.roblox.com/v1/asset/?id={link})"
                                else:
                                    link = "None"
                                if type(info["data"]["largeImage"].get("assetId")) is int: 
                                    rpc_info["large_image"] = f'https://assetdelivery.roblox.com/v1/asset/?id={info["data"]["largeImage"]["assetId"]}'
                                if type(info["data"]["largeImage"].get("hoverText")) is str: 
                                    rpc_info["large_text"] = info["data"]["largeImage"]["hoverText"]
                                passed_data[data_names["largeImage"]] = f'{info["data"]["largeImage"].get("hoverText", None)} | {link}'
                            elif type(info["data"].get("largeImage")) is None:
                                rpc_info["large_image"] = None
                                rpc_info["large_text"] = None
                                passed_data[data_names["largeImage"]] = f'None'
                            went_through = True
                elif info["command"] == "SetLaunchData":
                    if rpc:
                        if rpc_info == None:
                            rpc_info = {}
                        if type(info["data"]) is str: 
                            rpc_info["launch_data"] = info["data"].get("launch_data")
                            passed_data[data_names["launch_data"]] = info["data"].get("launch_data")
                        went_through = True
                if went_through == True and fflag_configuration.get("EFlagUseDiscordWebhook") == True and fflag_configuration.get("EFlagDiscordWebhookBloxstrapRPC") == True:
                    try:
                        
                        import requests
                    except Exception as e:
                        pip_class.install(["requests"])
                        import requests
                        printSuccessMessage("Successfully installed modules!")
                    if fflag_configuration.get("EFlagDiscordWebhookURL"):
                        thumbnail_url = "https://raw.githubusercontent.com/EfazDev/roblox-bootstrap/main/BootstrapImages/Bloxstrap.png"
                        embed_fields = [
                            {
                                "name": "Requested Command",
                                "value": info["command"],
                                "inline": True
                            }
                        ]
                        for i, v in passed_data.items():
                            embed_fields.append({
                                "name": i,
                                "value": v,
                                "inline": True
                            })
                        generated_body = {
                            "content": f"<@{fflag_configuration.get('EFlagDiscordWebhookUserId')}>",
                            "embeds": [
                                {
                                    "title": "Bloxstrap RPC Changed",
                                    "color": 12517631,
                                    "fields": embed_fields,
                                    "author": {
                                        "name": "Efaz's Roblox Bootstrap",
                                        "icon_url": "https://raw.githubusercontent.com/EfazDev/roblox-bootstrap/main/BootstrapImages/DiscordIcon.png"
                                    },
                                    "thumbnail": {
                                        "url": thumbnail_url
                                    },
                                    "footer": {
                                        "text": f"Made by @EfazDev | PID: {connected_roblox_instance.pid}" if fflag_configuration.get("EFlagDiscordWebhookShowPidInFooter") == True else "Made by @EfazDev",
                                        "icon_url": "https://cdn.efaz.dev/cdn/png/logo.png"
                                    },
                                    "timestamp": datetime.datetime.now(tz=datetime.UTC).strftime('%Y-%m-%dT%H:%M:%S.000Z')
                                }
                            ],
                            "attachments": []
                        }
                        try:
                            req = requests.post(fflag_configuration.get("EFlagDiscordWebhookURL"), json=generated_body)
                            if req.ok:
                                printDebugMessage("Successfully sent webhook!  Event: onRobloxStart")
                            else:
                                printErrorMessage("There was an issue sending your webhook message. Is the webhook link valid?")
                                printDebugMessage(f"Response: {req.text} | Status Code: {req.status_code}")
                        except Exception as e:
                            printErrorMessage("There was an issue sending your webhook message. Is the webhook link valid?")
    def onRobloxExit(consoleLine):
        printDebugMessage("User has closed the Roblox window!")
        if connected_roblox_instance.created_mutex == True and handler.getIfRobloxIsOpen(pid=connected_roblox_instance.pid):
            printYellowMessage("This process is handling multi-instance for all open Roblox windows. If you close this window, all Roblox windows may close.")
        else:
            printErrorMessage("Roblox window was closed! Closing Bootstrap App..")
        if fflag_configuration.get("EFlagEnableDiscordRPC") == True:
            global rpc
            global rpc_info
            global current_place_info
            try: 
                if rpc: rpc.close()
            except Exception as e:
                printDebugMessage(f"There was an error setting your Discord Embed: {str(e)}")
            rpc = None
            rpc_info = None
            current_place_info = None
        if fflag_configuration.get("EFlagUseDiscordWebhook") == True and fflag_configuration.get("EFlagDiscordWebhookRobloxAppClose") == True:
            try:
                import requests
            except Exception as e:
                pip_class.install(["requests"])
                import requests
                printSuccessMessage("Successfully installed modules!")
            if fflag_configuration.get("EFlagDiscordWebhookURL"):
                thumbnail_url = "https://raw.githubusercontent.com/EfazDev/roblox-bootstrap/main/BootstrapImages/RobloxLogo.png"
                embed_fields = [
                    {
                        "name": "Disconnected PID",
                        "value": connected_roblox_instance.pid,
                        "inline": True
                    },
                    {
                        "name": "Log Location",
                        "value": connected_roblox_instance.main_log_file,
                        "inline": True
                    }
                ]
                if main_os == "Windows" and (fflag_configuration.get("EFlagEnableDuplicationOfClients") == True):
                    embed_fields.append({
                        "name": "Handles Roblox Multi-Instance",
                        "value": str(connected_roblox_instance.created_mutex == True),
                        "inline": True
                    })
                generated_body = {
                    "content": f"<@{fflag_configuration.get('EFlagDiscordWebhookUserId')}>",
                    "embeds": [
                        {
                            "title": "Roblox Closed!",
                            "color": 16735838,
                            "fields": embed_fields,
                            "author": {
                                "name": "Efaz's Roblox Bootstrap",
                                "icon_url": "https://raw.githubusercontent.com/EfazDev/roblox-bootstrap/main/BootstrapImages/DiscordIcon.png"
                            },
                            "thumbnail": {
                                "url": thumbnail_url
                            },
                            "footer": {
                                "text": f"Made by @EfazDev | PID: {connected_roblox_instance.pid}" if fflag_configuration.get("EFlagDiscordWebhookShowPidInFooter") == True else "Made by @EfazDev",
                                "icon_url": "https://cdn.efaz.dev/cdn/png/logo.png"
                            },
                            "timestamp": datetime.datetime.now(tz=datetime.UTC).strftime('%Y-%m-%dT%H:%M:%S.000Z')
                        }
                    ],
                    "attachments": []
                }
                try:
                    req = requests.post(fflag_configuration.get("EFlagDiscordWebhookURL"), json=generated_body)
                    if req.ok:
                        printDebugMessage("Successfully sent webhook! Event: onRobloxExit")
                    else:
                        printErrorMessage("There was an issue sending your webhook message. Is the webhook link valid?")
                        printDebugMessage(f"Response: {req.text} | Status Code: {req.status_code}")
                except Exception as e:
                    printErrorMessage("There was an issue sending your webhook message. Is the webhook link valid?")
        sys.exit(0)
    def onGameUserInfo(data):
        global connected_user_info
        if data.get("username") and data.get("userId"):
            connected_user_info = {"name": data.get("username"), "id": data.get("userId"), "display": data.get("displayName")}
    def onRobloxCrash(consoleLine):
        global updated_count
        updated_count = 999
        printErrorMessage("There was an error inside the RobloxPlayer that has caused it to crash! Sorry!")
        printDebugMessage(f"Crashed Data: {consoleLine}")
        if fflag_configuration.get("EFlagUseDiscordWebhook") == True and fflag_configuration.get("EFlagDiscordWebhookRobloxCrash") == True:
            try:
                import requests
            except Exception as e:
                pip_class.install(["requests"])
                import requests
                printSuccessMessage("Successfully installed modules!")
            if fflag_configuration.get("EFlagDiscordWebhookURL"):
                thumbnail_url = "https://raw.githubusercontent.com/EfazDev/roblox-bootstrap/main/BootstrapImages/RobloxLogo.png"
                title = f"Uh oh! Roblox Crashed!"
                color = 0
                generated_body = {
                    "content": f"<@{fflag_configuration.get('EFlagDiscordWebhookUserId')}>",
                    "embeds": [
                        {
                            "title": title,
                            "color": color,
                            "fields": [
                                {
                                    "name": "Console Log",
                                    "value": consoleLine,
                                    "inline": True
                                }
                            ],
                            "author": {
                                "name": "Efaz's Roblox Bootstrap",
                                "icon_url": "https://raw.githubusercontent.com/EfazDev/roblox-bootstrap/main/BootstrapImages/DiscordIcon.png"
                            },
                            "thumbnail": {
                                "url": thumbnail_url
                            },
                            "footer": {
                                "text": f"Made by @EfazDev | PID: {connected_roblox_instance.pid}" if fflag_configuration.get("EFlagDiscordWebhookShowPidInFooter") == True else "Made by @EfazDev",
                                "icon_url": "https://cdn.efaz.dev/cdn/png/logo.png"
                            },
                            "timestamp": datetime.datetime.now(tz=datetime.UTC).strftime('%Y-%m-%dT%H:%M:%S.000Z')
                        }
                    ],
                    "attachments": []
                }
                try:
                    req = requests.post(fflag_configuration.get("EFlagDiscordWebhookURL"), json=generated_body)
                    if req.ok:
                        printDebugMessage("Successfully sent webhook! Event: onRobloxCrash")
                    else:
                        printErrorMessage("There was an issue sending your webhook message. Is the webhook link valid?")
                        printDebugMessage(f"Response: {req.text} | Status Code: {req.status_code}")
                except Exception as e:
                    printErrorMessage("There was an issue sending your webhook message. Is the webhook link valid?")
    def onRobloxAppStart(consoleLine):
        if fflag_configuration.get("EFlagUseDiscordWebhook") == True and fflag_configuration.get("EFlagDiscordWebhookRobloxAppStart") == True:
            try:
                import requests
            except Exception as e:
                pip_class.install(["requests"])
                import requests
                printSuccessMessage("Successfully installed modules!")
            if fflag_configuration.get("EFlagDiscordWebhookURL"):
                thumbnail_url = "https://raw.githubusercontent.com/EfazDev/roblox-bootstrap/main/BootstrapImages/RobloxLogo.png"
                embed_fields = [
                    {
                        "name": "Connected PID",
                        "value": connected_roblox_instance.pid,
                        "inline": True
                    },
                    {
                        "name": "Log Location",
                        "value": connected_roblox_instance.main_log_file,
                        "inline": True
                    }
                ]
                if main_os == "Windows" and (fflag_configuration.get("EFlagEnableDuplicationOfClients") == True):
                    embed_fields.append({
                        "name": "Handles Roblox Multi-Instance",
                        "value": str(connected_roblox_instance.created_mutex == True),
                        "inline": True
                    })
                generated_body = {
                    "content": f"<@{fflag_configuration.get('EFlagDiscordWebhookUserId')}>",
                    "embeds": [
                        {
                            "title": "Roblox Started!",
                            "color": 6225823,
                            "fields": embed_fields,
                            "author": {
                                "name": "Efaz's Roblox Bootstrap",
                                "icon_url": "https://raw.githubusercontent.com/EfazDev/roblox-bootstrap/main/BootstrapImages/DiscordIcon.png"
                            },
                            "thumbnail": {
                                "url": thumbnail_url
                            },
                            "footer": {
                                "text": f"Made by @EfazDev | PID: {connected_roblox_instance.pid}" if fflag_configuration.get("EFlagDiscordWebhookShowPidInFooter") == True else "Made by @EfazDev",
                                "icon_url": "https://cdn.efaz.dev/cdn/png/logo.png"
                            },
                            "timestamp": datetime.datetime.now(tz=datetime.UTC).strftime('%Y-%m-%dT%H:%M:%S.000Z')
                        }
                    ],
                    "attachments": []
                }
                try:
                    req = requests.post(fflag_configuration.get("EFlagDiscordWebhookURL"), json=generated_body)
                    if req.ok:
                        printDebugMessage("Successfully sent webhook!  Event: onRobloxStart")
                    else:
                        printErrorMessage("There was an issue sending your webhook message. Is the webhook link valid?")
                        printDebugMessage(f"Response: {req.text} | Status Code: {req.status_code}")
                except Exception as e:
                    printErrorMessage("There was an issue sending your webhook message. Is the webhook link valid?")
    def onAllRobloxEvents(data):
        if fflag_configuration.get("EFlagEnableModModes") == True:
            if fflag_configuration.get("EFlagSelectedModMode") and fflag_configuration.get("EFlagEnableModModeScripts") == True and os.path.exists(os.path.join(os.path.curdir, "Mods", fflag_configuration.get("EFlagSelectedModMode"), "ModScript.py")):
                if os.path.exists(os.path.join(os.path.curdir, "Mods", fflag_configuration.get("EFlagSelectedModMode"), "Manifest.json")):
                    if mod_mode_json:
                        if mod_mode_json.get("mod_script") == True:
                            try:
                                if type(fflag_configuration.get("EFlagModModeAllowedDetectments")) is list:
                                    if "onRobloxLog" in fflag_configuration.get("EFlagModModeAllowedDetectments"):
                                        if hasattr(mod_mode_module, "onRobloxLog"):
                                            threading.Thread(target=getattr(mod_mode_module, "onRobloxLog"), args=[data]).start()
                                    if data.get("eventName") in fflag_configuration.get("EFlagModModeAllowedDetectments"):
                                        if hasattr(mod_mode_module, data.get("eventName")):
                                            threading.Thread(target=getattr(mod_mode_module, data.get("eventName")), args=[data["data"]]).start()
                            except Exception as e:
                                printDebugMessage(f"Something went wrong with pinging the mod mode script: {str(e)}")
    def onLoadedFFlags(data):
        printSuccessMessage("Roblox client has successfully loaded FFlags from local file!")
    def onPrivateServer(data):
        global setTypeOfServer
        global set_current_private_server_key
        setTypeOfServer = 1
        if fflag_configuration.get("EFlagAllowPrivateServerJoining") == True and data and data.get("data"):
            set_current_private_server_key = data["data"].get("accessCode")
        else:
            set_current_private_server_key = None
        printSuccessMessage("Roblox is currently pending to a private server!")
    def onReservedServer(data):
        global setTypeOfServer
        global set_current_private_server_key
        setTypeOfServer = 2
        if fflag_configuration.get("EFlagAllowPrivateServerJoining") == True and data and data.get("data"):
            set_current_private_server_key = data["data"].get("accessCode")
        else:
            set_current_private_server_key = None
        printSuccessMessage("Roblox is currently pending to a reserved server!")
    def onPartyServer(data):
        global setTypeOfServer
        global set_current_private_server_key
        setTypeOfServer = 3
        if fflag_configuration.get("EFlagAllowPrivateServerJoining") == True and data and data.get("data"):
            set_current_private_server_key = data["data"].get("accessCode")
        else:
            set_current_private_server_key = None
        printSuccessMessage("Roblox is currently pending to a party!")
    def onMainServer(consoleLine):
        global setTypeOfServer
        global set_current_private_server_key
        setTypeOfServer = 0
        set_current_private_server_key = None
        printSuccessMessage("Roblox is currently pending to a public server!")

    # Launch Roblox
    def runRoblox():
        global connected_roblox_instance
        if multi_instance_enabled == True:
            printDebugMessage(f"Opening extra Roblox window..")
            connected_roblox_instance = handler.openRoblox(
                forceQuit=False,
                makeDupe=True, 
                debug=(fflag_configuration.get("EFlagEnableDebugMode") == True), 
                attachInstance=(not (fflag_configuration.get("EFlagAllowActivityTracking") == False)), 
                allowRobloxOtherLogDebug=(fflag_configuration.get("EFlagAllowFullDebugMode") == True)
            )
            if connected_roblox_instance:
                connected_roblox_instance.setRobloxEventCallback("onRobloxAppStart", onRobloxAppStart)
                connected_roblox_instance.setRobloxEventCallback("onRobloxExit", onRobloxExit)
                connected_roblox_instance.setRobloxEventCallback("onRobloxCrash", onRobloxCrash)
                connected_roblox_instance.setRobloxEventCallback("onRobloxLog", onAllRobloxEvents)
                connected_roblox_instance.setRobloxEventCallback("onBloxstrapSDK", onBloxstrapMessage)
                connected_roblox_instance.setRobloxEventCallback("onLoadedFFlags", onLoadedFFlags)
                connected_roblox_instance.setRobloxEventCallback("onGameStart", onGameStart)
                connected_roblox_instance.setRobloxEventCallback("onGameJoined", onGameJoined)
                connected_roblox_instance.setRobloxEventCallback("onGameJoinInfo", onGameUserInfo)
                connected_roblox_instance.setRobloxEventCallback("onGameDisconnected", onGameDisconnected)
                connected_roblox_instance.setRobloxEventCallback("onGameLoading", onMainServer)
                connected_roblox_instance.setRobloxEventCallback("onGameLoadingPrivate", onPrivateServer)
                connected_roblox_instance.setRobloxEventCallback("onGameLoadingReserved", onReservedServer)
                connected_roblox_instance.setRobloxEventCallback("onGameLoadingParty", onPartyServer)
                connected_roblox_instance.setRobloxEventCallback("onGameTeleport", onTeleport)
                printSuccessMessage("Connected to Roblox Instance from log file for Activity Tracking!")
                if connected_roblox_instance.created_mutex == True:
                    printSuccessMessage("Successfully connected for multi-instancing! Please know that this effect is active until all Roblox windows are closed or this bootstrap window is closed.")
            else:
                printDebugMessage("No RobloxInstance class was registered")
            check_update_thread = threading.Thread(target=checkIfUpdateWasNeeded)
            check_update_thread.start()
        elif len(given_args) > 1:
            if main_os == "Darwin":
                url_str = unquote(given_args[1])
                if url_str:
                    url = unquote(url_str)
            elif main_os == "Windows":
                url = given_args[1]
            if url:
                if ("roblox-player:" in url) or ("roblox:" in url) or ("efaz-bootstrap" in url and "continue" in url) or ("efaz-bootstrap" in url and "new" in url) or ("efaz-bootstrap" in url and "menu" in url):
                    printDebugMessage(f"Running using Roblox URL: {url}")
                    connected_roblox_instance = handler.openRoblox(
                        forceQuit=(not (fflag_configuration.get("EFlagEnableDuplicationOfClients") == True)), 
                        makeDupe=(fflag_configuration.get("EFlagEnableDuplicationOfClients") == True), 
                        debug=(fflag_configuration.get("EFlagEnableDebugMode") == True), 
                        startData=url, 
                        attachInstance=(not (fflag_configuration.get("EFlagAllowActivityTracking") == False)), 
                        allowRobloxOtherLogDebug=(fflag_configuration.get("EFlagAllowFullDebugMode") == True)
                    )
                    if connected_roblox_instance:
                        connected_roblox_instance.setRobloxEventCallback("onRobloxAppStart", onRobloxAppStart)
                        connected_roblox_instance.setRobloxEventCallback("onRobloxExit", onRobloxExit)
                        connected_roblox_instance.setRobloxEventCallback("onRobloxCrash", onRobloxCrash)
                        connected_roblox_instance.setRobloxEventCallback("onRobloxLog", onAllRobloxEvents)
                        connected_roblox_instance.setRobloxEventCallback("onBloxstrapSDK", onBloxstrapMessage)
                        connected_roblox_instance.setRobloxEventCallback("onLoadedFFlags", onLoadedFFlags)
                        connected_roblox_instance.setRobloxEventCallback("onGameStart", onGameStart)
                        connected_roblox_instance.setRobloxEventCallback("onGameJoined", onGameJoined)
                        connected_roblox_instance.setRobloxEventCallback("onGameJoinInfo", onGameUserInfo)
                        connected_roblox_instance.setRobloxEventCallback("onGameDisconnected", onGameDisconnected)
                        connected_roblox_instance.setRobloxEventCallback("onGameLoading", onMainServer)
                        connected_roblox_instance.setRobloxEventCallback("onGameLoadingPrivate", onPrivateServer)
                        connected_roblox_instance.setRobloxEventCallback("onGameLoadingReserved", onReservedServer)
                        connected_roblox_instance.setRobloxEventCallback("onGameLoadingParty", onPartyServer)
                        connected_roblox_instance.setRobloxEventCallback("onGameTeleport", onTeleport)
                        printSuccessMessage("Connected to Roblox Instance from log file for Activity Tracking!")
                        if connected_roblox_instance.created_mutex == True:
                            printSuccessMessage("Successfully connected for multi-instancing! Please know that this effect is active until all Roblox windows are closed or this bootstrap window is closed.")
                    else:
                        printDebugMessage("No RobloxInstance class was registered")
                    check_update_thread = threading.Thread(target=checkIfUpdateWasNeeded)
                    check_update_thread.start()
                else:
                    printDebugMessage(f"Unknown scheme: {url}")
        else:
            if handler.getIfRobloxIsOpen():
                printMainMessage("An existing Roblox Window is currently open. Would you like to restart it in order for changes to take effect?")
                c = input("> ")
                if isYes(c) == True:
                    handler.endRoblox()
                else:
                    sys.exit(0)
            connected_roblox_instance = handler.openRoblox(
                forceQuit=True, 
                makeDupe=False,
                debug=(fflag_configuration.get("EFlagEnableDebugMode") == True), 
                attachInstance=(not (fflag_configuration.get("EFlagAllowActivityTracking") == False)), 
                allowRobloxOtherLogDebug=(fflag_configuration.get("EFlagAllowFullDebugMode") == True)
            )
            if connected_roblox_instance:
                connected_roblox_instance.setRobloxEventCallback("onRobloxAppStart", onRobloxAppStart)
                connected_roblox_instance.setRobloxEventCallback("onRobloxExit", onRobloxExit)
                connected_roblox_instance.setRobloxEventCallback("onRobloxCrash", onRobloxCrash)
                connected_roblox_instance.setRobloxEventCallback("onRobloxLog", onAllRobloxEvents)
                connected_roblox_instance.setRobloxEventCallback("onBloxstrapSDK", onBloxstrapMessage)
                connected_roblox_instance.setRobloxEventCallback("onLoadedFFlags", onLoadedFFlags)
                connected_roblox_instance.setRobloxEventCallback("onGameStart", onGameStart)
                connected_roblox_instance.setRobloxEventCallback("onGameJoined", onGameJoined)
                connected_roblox_instance.setRobloxEventCallback("onGameJoinInfo", onGameUserInfo)
                connected_roblox_instance.setRobloxEventCallback("onGameDisconnected", onGameDisconnected)
                connected_roblox_instance.setRobloxEventCallback("onGameLoading", onMainServer)
                connected_roblox_instance.setRobloxEventCallback("onGameLoadingPrivate", onPrivateServer)
                connected_roblox_instance.setRobloxEventCallback("onGameLoadingReserved", onReservedServer)
                connected_roblox_instance.setRobloxEventCallback("onGameLoadingParty", onPartyServer)
                connected_roblox_instance.setRobloxEventCallback("onGameTeleport", onTeleport)
                printSuccessMessage("Connected to Roblox Instance from log file for Activity Tracking!")
            else:
                printDebugMessage("No RobloxInstance class was registered")
            check_update_thread = threading.Thread(target=checkIfUpdateWasNeeded)
            check_update_thread.start()
    def checkIfUpdateWasNeeded():
        global updated_count
        updated_count += 1
        if updated_count < 3:
            printMainMessage("Waiting 1 second to check if Roblox needs a reinstall..")
            time.sleep(1)
            if not (handler.getIfRobloxIsOpen()):
                printMainMessage("Uh oh! An fresh reinstall is needed. Downloading a fresh copy of Roblox!")
                handler.installRoblox(forceQuit=(not (fflag_configuration.get("EFlagEnableDuplicationOfClients") == True)), debug=(fflag_configuration.get("EFlagEnableDebugMode") == True))
                time.sleep(2)
                printWarnMessage("--- Preparing Roblox ---")
                prepareRoblox()
                printSuccessMessage("Done! Roblox is ready!")
                time.sleep(2)
                printWarnMessage("--- Running Roblox ---")
                runRoblox()
            else:
                printSuccessMessage("Roblox doesn't require any updates!")
        else:
            printErrorMessage("Is Roblox crashing instantly..? Well, ending script here.")
    runRoblox()

    # End Script
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
    raise EfazRobloxBootstrapNotModule()