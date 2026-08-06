# 
# OrangeBlox 🍊
# Made by Efaz from efaz.dev
# v2.6.0j
# 

import Modules.config as cf
from Modules.printing import *
from Modules.startup import *
from Modules.utils import *
from Modules.options import *
import os
import sys

def specialMods():
    printMainMessage("Would you like to revert the Builder Sans and Monsterrat Fonts and use the old Gotham font instead? (y/n)")
    printMainMessage(f'Current Setting: {cf.main_config.get("EFlagRemoveBuilderFont", False) == True}')
    a = input("> ")
    if isYes(a) == True:
        cf.main_config["EFlagRemoveBuilderFont"] = True
        printDebugMessage("User selected: True")
    elif isNo(a) == True:
        cf.main_config["EFlagRemoveBuilderFont"] = False
        printDebugMessage("User selected: False")

    printMainMessage("Would you like to change the background of the Avatar Editor? (y/n)")
    printMainMessage(f'Current Setting: {cf.main_config.get("EFlagAvatarEditorBackground")}')
    c = input("> ")
    if isYes(c) == True:
        cf.main_config["EFlagEnableChangeAvatarEditorBackground"] = True
        def scan_name(a): return os.path.exists(os.path.join(cf.mods_folder, "AvatarEditorMaps", a))
        def getName():
            got_backgrounds = []
            for i in os.listdir(os.path.join(cf.mods_folder, "AvatarEditorMaps")):
                if os.path.isfile(os.path.join(cf.mods_folder, "AvatarEditorMaps", i)) and i.endswith(".rbxl"): got_backgrounds.append(i)
            printSystemMessage("Select the number that is associated with the map you want to use.")
            got_backgrounds = sorted(got_backgrounds)
            count = 1
            for i in got_backgrounds:
                printMainMessage(f"[{str(count)}] {i}")
                count += 1
            if cf.main_os == "Darwin":
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
        cf.main_config["EFlagAvatarEditorBackground"] = set_avatar_editor_location[:set_avatar_editor_location.rfind(".rbxl")]
        printSuccessMessage(f"Set avatar background: {set_avatar_editor_location}")
    elif isNo(c) == True:
        cf.main_config["EFlagEnableChangeAvatarEditorBackground"] = False
        printDebugMessage("User selected: False")

    printMainMessage("Would you like to change the Roblox cursor? (y/n)")
    printMainMessage(f'Current Setting: {cf.main_config.get("EFlagSelectedCursor")}')
    c = input("> ")
    if isYes(c) == True:
        cf.main_config["EFlagEnableChangeCursor"] = True
        def scan_name(a): return os.path.exists(os.path.join(cf.mods_folder, "Cursors", a, "ArrowCursor.png")) and os.path.exists(os.path.join(cf.mods_folder, "Cursors", a, "ArrowFarCursor.png"))
        def getName():
            got_cursors = []
            for i in os.listdir(os.path.join(cf.mods_folder, "Cursors")):
                if os.path.isdir(os.path.join(cf.mods_folder, "Cursors", i)): got_cursors.append(i)
            got_cursors = sorted(got_cursors)
            printSystemMessage("Select the number that is associated with the cursor you want to use.")
            count = 1
            for i in got_cursors:
                printMainMessage(f"[{str(count)}] {i}")
                count += 1
            if cf.main_os == "Darwin": printYellowMessage("[Also, if you just added a new cursor folder into the Cursors folder, please rerun Install.py in order for it to seen.]")
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
        cf.main_config["EFlagSelectedCursor"] = set_cursor_location
        printSuccessMessage(f"Set cursor folder: {set_cursor_location}")
    elif isNo(c) == True:
        cf.main_config["EFlagEnableChangeCursor"] = False
        printDebugMessage("User selected: False")

    printMainMessage("Would you like to change the Roblox logo on the Roblox Player? (y/n)")
    printMainMessage(f'Current Setting: {cf.main_config.get("EFlagSelectedBrandLogo")}')
    c = input("> ")
    if isYes(c) == True:
        cf.main_config["EFlagEnableChangeBrandIcons"] = True
        def scan_name(a): return os.path.exists(os.path.join(cf.mods_folder, "RobloxBrand", a, "AppIcon.icns")) or os.path.exists(os.path.join(cf.mods_folder, "RobloxBrand", a, "AppIcon.ico"))
        def getName():
            got_icons = []
            for i in os.listdir(os.path.join(cf.mods_folder, "RobloxBrand")):
                if os.path.isdir(os.path.join(cf.mods_folder, "RobloxBrand", i)): got_icons.append(i)
            got_icons = sorted(got_icons)
            printSystemMessage("Select the number that is associated with the icon you want to use.")
            count = 1
            for i in got_icons:
                printMainMessage(f"[{str(count)}] {i}")
                count += 1
            if cf.main_os == "Darwin": printYellowMessage("[Also, if you just added a new icon folder into the RobloxBrand folder, please rerun Install.py in order for it to seen.]")
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
        cf.main_config["EFlagSelectedBrandLogo"] = set_app_icon_location
        printSuccessMessage(f"Set logo folder: {set_app_icon_location}")
    elif isNo(c) == True:
        cf.main_config["EFlagEnableChangeBrandIcons"] = False
        printDebugMessage("User selected: False")

    if cf.main_config.get("EFlagRobloxStudioEnabled") == True:
        printMainMessage("Would you like to change the Roblox logo on Roblox Studio? (y/n)")
        printMainMessage(f'Current Setting: {cf.main_config.get("EFlagSelectedBrandLogo2")}')
        if cf.main_os == "Windows": printYellowMessage("The app icon would not change, rather, just the shortcut icon. Enable the Shortcut Icon Changing in order for this work.")
        c = input("> ")
        if isYes(c) == True:
            cf.main_config["EFlagEnableChangeBrandIcons2"] = True
            def scan_name(a): return os.path.exists(os.path.join(cf.mods_folder, "RobloxStudioBrand", a, "AppIcon.icns")) or os.path.exists(os.path.join(cf.mods_folder, "RobloxStudioBrand", a, "AppIcon.ico"))
            def getName():
                got_icons = []
                for i in os.listdir(os.path.join(cf.mods_folder, "RobloxStudioBrand")):
                    if os.path.isdir(os.path.join(cf.mods_folder, "RobloxStudioBrand", i)): got_icons.append(i)
                got_icons = sorted(got_icons)
                printSystemMessage("Select the number that is associated with the icon you want to use.")
                count = 1
                for i in got_icons:
                    printMainMessage(f"[{str(count)}] {i}")
                    count += 1
                if cf.main_os == "Darwin": printYellowMessage("[Also, if you just added a new icon folder into the RobloxStudioBrand folder, please rerun Install.py in order for it to seen.]")
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
            cf.main_config["EFlagSelectedBrandLogo2"] = set_app_icon_location
            printSuccessMessage(f"Set logo folder: {set_app_icon_location}")
        elif isNo(c) == True:
            cf.main_config["EFlagEnableChangeBrandIcons2"] = False
            printDebugMessage("User selected: False")

    if cf.main_os == "Windows": 
        printMainMessage("Would you like to use the Roblox Brand Icon as the Shortcut Icon? (y/n)")
        printMainMessage(f'Current Setting: {cf.main_config.get("EFlagUseRobloxAppIconAsShortcutIcon", False) == True}')
        a = input("> ")
        if isYes(a) == True:
            cf.main_config["EFlagUseRobloxAppIconAsShortcutIcon"] = True
            printDebugMessage("User selected: True")
        elif isNo(a) == True:
            cf.main_config["EFlagUseRobloxAppIconAsShortcutIcon"] = False
            printDebugMessage("User selected: False")

        printMainMessage("Would you like to enable selected Roblox icon for when Roblox Player/Studio is running? (y/n)")
        printMainMessage(f'Current Setting: {cf.main_config.get("EFlagReplaceRobloxRuntimeIconWithModIcon", False) == True}')
        printYellowMessage('Warning! This setting may cause issues and will take a moment for the handler to settle!')
        a = input("> ")
        if isYes(a) == True:
            cf.main_config["EFlagReplaceRobloxRuntimeIconWithModIcon"] = True
            printDebugMessage("User selected: True")
        elif isNo(a) == True:
            cf.main_config["EFlagReplaceRobloxRuntimeIconWithModIcon"] = False
            printDebugMessage("User selected: False")

    printMainMessage("Would you like to change your Roblox player sounds? (y/n)")
    printMainMessage(f'Current Setting: {cf.main_config.get("EFlagSelectedPlayerSounds")}')
    c = input("> ")
    if isYes(c) == True:
        cf.main_config["EFlagEnableChangePlayerSound"] = True
        def scan_name(a): return os.path.exists(os.path.join(cf.mods_folder, "PlayerSounds", a))
        def getName():
            got_sounds = []
            for i in os.listdir(os.path.join(cf.mods_folder, "PlayerSounds")):
                if os.path.isdir(os.path.join(cf.mods_folder, "PlayerSounds", i)): got_sounds.append(i)
            got_sounds = sorted(got_sounds)
            printSystemMessage("Select the number that is associated with the player sounds you want to use.")
            count = 1
            for i in got_sounds:
                printMainMessage(f"[{str(count)}] {i}")
                count += 1
            if cf.main_os == "Darwin": printYellowMessage("[Also, if you just added a new sound pack into the PlayerSounds folder, please rerun Install.py in order for it to seen.]")
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
        cf.main_config["EFlagSelectedPlayerSounds"] = set_player_sounds
        printSuccessMessage(f"Set player sounds: {set_player_sounds}")
    elif isNo(c) == True:
        cf.main_config["EFlagEnableChangePlayerSound"] = False
        printDebugMessage("User selected: False")
    saveSettings()
def syncMods():
    printMainMessage("Syncing mods..")
    sync_folder_names = ["AvatarEditorMaps", "Cursors", "PlayerSounds", "RobloxBrand", "RobloxStudioBrand", "Mods"]
    for sync_folder_name in sync_folder_names:
        targeted_sync_location = os.path.join(cf.main_config.get("EFlagOrangeBloxSyncDir"), "Mods", sync_folder_name)
        if os.path.exists(targeted_sync_location) and os.path.isdir(targeted_sync_location):
            for i in os.listdir(targeted_sync_location):
                syncing_mod_path = os.path.join(targeted_sync_location, i)
                if os.path.isdir(syncing_mod_path):
                    installed_mod_path = os.path.join(cf.mods_folder, sync_folder_name, i)
                    if os.path.exists(installed_mod_path): 
                        for e in os.listdir(installed_mod_path):
                            if e != f"Configuration_{cf.user_folder_name}" and e != "__pycache__": 
                                if os.path.isdir(os.path.join(installed_mod_path, e)): shutil.rmtree(os.path.join(installed_mod_path, e), ignore_errors=True)
                                else: os.remove(os.path.join(installed_mod_path, e))
                    def ignore_files_func(dir, files): 
                        config_files = [fi for fi in os.listdir(dir) if fi.startswith("Configuration_")]
                        return set(["__pycache__"] + config_files)
                    cf.pip_class.copyTreeWithMetadata(syncing_mod_path, installed_mod_path, dirs_exist_ok=True, ignore=ignore_files_func)
            printDebugMessage(f"Successfully synced mod type: {sync_folder_name}")
        else: printDebugMessage(f"There was an issue trying to copy files for mod type: {sync_folder_name}")
    printSuccessMessage("Successfully synced all mods from installation folder!")
def openModsFolder():
    printMainMessage("Opening Mods Folder..")
    if cf.main_os == "Darwin": re = subprocess.run([cf.pip_class.getPathFile("/usr/bin/open"), os.path.join(cf.mods_folder)])
    else: re = subprocess.run(f"start {os.path.join(cf.mods_folder)}", shell=True)
    if re.returncode == 0: printSuccessMessage("Successfully opened Mods folder!")
    else: printErrorMessage("Unable to open Mods folder!")
def modScriptSettings(se, reverify_mod_script, mods_manifest, mod_order):
    if se == 0: se += 1
    else: printSystemMessage(f"--- Mod Script Settings ---")
    if reverify_mod_script == None:
        printMainMessage("Select the mod scripts you want to be used!")
        mod_script_generated_ui_options = []
        for i, v in sorted(mods_manifest.items(), key=lambda x: mod_order.index(x[0]) if x[0] in mod_order else len(mod_order)):
            if v["mod_script"] == True:
                if i == "Original" or i == "OldFont" or i == "GothamFont": continue
                final_vers = "1.0.0"
                final_name = ""
                final_enabled = "❌"
                if cf.main_config.get('EFlagSelectedModScripts') and cf.main_config.get('EFlagSelectedModScripts').get(i) and cf.main_config.get('EFlagSelectedModScripts').get(i).get("enabled") == True: final_mod_enabled = "✅"
                else: final_mod_enabled = "❌"
                if v.get("version"): final_vers = v.get("version")
                if v.get("name") == i: final_name = f"{i}"
                elif isinstance(v.get("name"), str): final_name = f"{v.get('name')} [{i}]"
                else: final_name = f"{i}"
                if v["mod_script_supports"] <= cf.current_version["version"] and v["mod_script_end_support"] > cf.current_version["version"] and v["mod_script_supports_operating_system"] == True: mod_script_generated_ui_options.append({"index": 1, "message": f"[{final_mod_enabled}] {final_name} [v{final_vers}]", "final_name": final_name, "mod_info": v, "mod_id": i})
                else: mod_script_generated_ui_options.append({"index": 2, "message": f"[🔒] {final_name} [v{final_vers}]", "final_name": final_name, "mod_info": v, "mod_id": i})
        mod_script_generated_ui_options.append({"index": 1000000, "message": ts(f"Disable Mod Scripts")})
        mod_script_generated_ui_options.append({"index": 1000001, "message": ts("Reset All Mod Script Configurations")})
        mod_script_generated_ui_options.append({"index": 1000002, "message": ts("Reset One Mod Script Configuration")})
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
                if cf.main_config.get('EFlagSelectedModScripts') and cf.main_config.get('EFlagSelectedModScripts').get(reverify_mod_script) and cf.main_config.get('EFlagSelectedModScripts').get(reverify_mod_script).get("enabled") == True: final_mod_enabled = "✅"
                else: final_mod_enabled = "❌"
                if v.get("name") == reverify_mod_script: final_name = f"{reverify_mod_script}"
                elif isinstance(v.get("name"), str): final_name = f"{v.get('name')} [{reverify_mod_script}]"
                else: final_name = f"{reverify_mod_script}"
                if v["mod_script_supports"] <= cf.current_version["version"] and v["mod_script_end_support"] > cf.current_version["version"] and v["mod_script_supports_operating_system"] == True and v["python_version"] <= cf.pip_class.getCurrentPythonVersion(): mod_script_generated_ui_options.append({"index": 1, "message": f"[{final_mod_enabled}] {final_name} [v{final_vers}]", "final_name": final_name, "mod_info": v, "mod_id": reverify_mod_script})
                else: mod_script_generated_ui_options.append({"index": 2, "message": f"[🔒] {final_name} [v{final_vers}]", "final_name": final_name, "mod_info": v, "mod_id": reverify_mod_script})
        mod_script_generated_ui_options = sorted(mod_script_generated_ui_options, key=lambda x: x["index"])
    if len(mod_script_generated_ui_options) < 1:
        if reverify_mod_script == None: printErrorMessage("No Mod Scripts available. Please sync mods with a mod script in order for it to show here!")
        else: printErrorMessage("There was an issue finding the requested mod script!")
    else:
        if reverify_mod_script == None: sel_mod_script = generateMenuSelection(mod_script_generated_ui_options, star_option=ts("Exit Mod Script Settings"))
        else: sel_mod_script = mod_script_generated_ui_options[0] if len(mod_script_generated_ui_options) > 0 else None
        if sel_mod_script:
            if sel_mod_script["index"] == 1000000:
                cf.main_config["EFlagSelectedModScripts"] = {}
                printSuccessMessage(f'Successfully disabled all mod scripts!')
            elif sel_mod_script["index"] == 1000001:
                printMainMessage("Are you sure you want to reset ALL Mod Script Configurations? This may cause damage to the scripts if run. (y/n)")
                d = input("> ")
                if isYes(d) == True:
                    printMainMessage("Starting Clearing Operation..")
                    for i, v in mods_manifest.items():
                        if v["mod_script"] == True and os.path.exists(os.path.join(cf.mods_folder, "Mods", i, f"Configuration_{cf.user_folder_name}")):
                            os.remove(os.path.join(cf.mods_folder, "Mods", i, f"Configuration_{cf.user_folder_name}"))
                            printMainMessage(f"Removed Mod Script Configuration for {i}")
                    printSuccessMessage("Successfully cleared all Mod Script Configurations!")
                else: printErrorMessage("Canceled Clearing Operation.")
            elif sel_mod_script["index"] == 1000002:
                mod_script_generated_ui_options2 = []
                for i, v in mods_manifest.items():
                    if v["mod_script"] == True:
                        if i == "Original" or i == "OldFont" or i == "GothamFont": continue
                        final_vers = "1.0.0"
                        final_name = ""
                        final_enabled = "❌"
                        if cf.main_config.get('EFlagSelectedModScripts') and cf.main_config.get('EFlagSelectedModScripts').get(i) and cf.main_config.get('EFlagSelectedModScripts').get(i).get("enabled") == True: final_mod_enabled = "✅"
                        else: final_mod_enabled = "❌"
                        if v.get("version"): final_vers = v.get("version")
                        if v.get("name") == i: final_name = f"{i}"
                        elif isinstance(v.get("name"), str): final_name = f"{v.get('name')} [{i}]"
                        else: final_name = f"{i}"
                        if v["mod_script_supports"] <= cf.current_version["version"] and v["mod_script_end_support"] > cf.current_version["version"] and v["mod_script_supports_operating_system"] == True and v["python_version"] <= cf.pip_class.getCurrentPythonVersion(): mod_script_generated_ui_options2.append({"index": 1, "message": f"[{final_mod_enabled}] {final_name} [v{final_vers}]", "final_name": final_name, "mod_info": v, "mod_id": i})
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
                        if mod_script_info["mod_script"] == True and os.path.exists(os.path.join(cf.mods_folder, "Mods", mod_script_id, f"Configuration_{cf.user_folder_name}")):
                            os.remove(os.path.join(cf.mods_folder, "Mods", mod_script_id, f"Configuration_{cf.user_folder_name}"))
                            printMainMessage(f"Removed Mod Script Configuration for {mod_script_id}")
                        printSuccessMessage(f"Successfully cleared {sel_mod_script2.get('final_name')}'s Mod Script Configurations!")
                    else: printErrorMessage("Canceled Clearing Operation.")
            elif sel_mod_script["index"] == 2:
                if sel_mod_script["mod_info"]["mod_script_supports"] > cf.current_version["version"]: printErrorMessage(f"This mod script is unsupported! Please update to {obName0()} v{sel_mod_script['mod_info']['mod_script_supports']} in order to use!")
                else:
                    printErrorMessage(f"This mod script has reached their end support! Creator Note:")
                    printErrorMessage(v['mod_info']["mod_script_end_support_reasoning"])
            elif sel_mod_script["index"] == 1:
                set_mod_script = sel_mod_script["mod_id"]
                if sel_mod_script["mod_info"].get("mod_script") == True and os.path.exists(os.path.join(cf.mods_folder, "Mods", set_mod_script, "ModScript.py")) and cf.main_config.get("EFlagAllowActivityTracking") != False:
                    if reverify_mod_script == None and cf.main_config.get("EFlagSelectedModScripts").get(set_mod_script) and cf.main_config.get("EFlagSelectedModScripts").get(set_mod_script).get("enabled") == True: cf.main_config["EFlagSelectedModScripts"][set_mod_script] = {"enabled": False}
                    else:
                        printMainMessage("You will enable the following permissions for this script: ")
                        printMainMessage(sel_mod_script["message"].replace("[✅] ", "", 1).replace("[❌] ", "", 1))
                        python_modules = sel_mod_script["mod_info"].get("python_modules", [])
                        permissions_needed = sel_mod_script["mod_info"].get("permissions", [])
                        sorted_perms_1 = []
                        for i in permissions_needed:
                            if isinstance(i, str) and rbx.roblox_event_info.get(i):
                                mai = rbx.roblox_event_info.get(i)
                                sorted_perms_1.append({"level": mai.get("level", 0), "perm": i, "message": mai.get('message')})
                            else:
                                sorted_perms_1.append({"level": 3, "perm": i, "message": ts("Unknown Requirement")})
                                printErrorMessage(f"- Unknown Requirement")
                        sorted_perms_2 = sorted(sorted_perms_1, key=lambda a: a["level"], reverse=True)
                        extreme_included = False
                        for i in sorted_perms_2:
                            if i.get("level") == 4:
                                print(cf.colors_class.wrap(f"- {i.get('message')}", 201))
                                extreme_included = True
                            elif i.get("level") == 3: printErrorMessage(f"- {i.get('message')}")
                            elif i.get("level") == 2: printWarnMessage(f"- {i.get('message')}")
                            elif i.get("level") == 1: printYellowMessage(f"- {i.get('message')}")
                            else: printMainMessage(f"- {i.get('message')}")
                        if len(python_modules) > 0: printYellowMessage(f"- Install and Use Python Modules: {', '.join(python_modules)}")
                        printYellowMessage("Please check the scripts, permissions above and developer of this mod before using!")
                        printMainMessage(f"Color Key: {cf.colors_class.wrap(ts('[Extreme]'), 201)} {cf.colors_class.wrap(ts('[Dangerous]'), 196)} {cf.colors_class.wrap(ts('[Caution]'), 202)} {cf.colors_class.wrap(ts('[Warning]'), 226)} {cf.colors_class.wrap(ts('[Normal]'), 255)}")
                        PyKits.TimerBar(5, "Are you sure you want to use this mod script? (y/n)", False).start()
                        a = input("> ")
                        if isYes(a) == True:
                            con = True
                            if extreme_included == True:
                                con = False
                                printYellowMessage("THIS SCRIPT WILL BE GRANTED THE EXTREME LEVEL PERMISSIONS LISTED! ARE YOU SURE?")
                                for i in sorted_perms_2:
                                    if i.get("level") == 4: print(cf.colors_class.wrap(f"- {i.get('message')}", 201))
                                PyKits.TimerBar(5, "ARE YOU SURE? (y/n)", False).start()
                                a = input("> ")
                                if isYes(a) == True: con = True
                            if con == True:
                                actual_permissions = []
                                if isinstance(permissions_needed, list): actual_permissions = permissions_needed
                                if isinstance(python_modules, list) and len(python_modules) > 0:
                                    if not cf.pip_class.installed(python_modules, boolonly=True): cf.pip_class.install(python_modules)
                                    s = []
                                    for pyt in python_modules:
                                        if isinstance(pyt, str): s.append(f"pip_{pyt}")
                                    actual_permissions += s
                                cf.main_config["EFlagSelectedModScripts"][set_mod_script] = {
                                    "enabled": True,
                                    "permissions": actual_permissions,
                                    "hash": generateFileHash(os.path.join(cf.mods_folder, "Mods", set_mod_script, "ModScript.py"), is_text=True)
                                }
                                printSuccessMessage(f'Successfully enabled mod script to "{sel_mod_script["final_name"]}"!')
                            else:
                                if reverify_mod_script != None: cf.main_config["EFlagSelectedModScripts"][set_mod_script] = {"enabled": False}
                        else:
                            if reverify_mod_script != None: cf.main_config["EFlagSelectedModScripts"][set_mod_script] = {"enabled": False}
                else:
                    if reverify_mod_script != None: cf.main_config["EFlagSelectedModScripts"][set_mod_script] = {"enabled": False}
            else:
                saveSettings()
                printSuccessMessage("Successfully saved Mod Script settings!")
                return
            saveSettings()
        else:
            saveSettings()
            printSuccessMessage("Successfully saved Mod Script settings!")
            return
    if reverify_mod_script == None: return modScriptSettings(se, reverify_mod_script, mods_manifest, mod_order)
def mainModManager(reverify_mod_script=None, mods_manifest=None, mod_order=None, start_index=None, use_already=False):
    if reverify_mod_script == None:
        if not use_already:
            printSystemMessage("--- Mods Manager ---")
            printSuccessMessage(f"Mods Enabled: Yes")
        if cf.main_config.get("EFlagAllowActivityTracking") == False:
            printMainMessage("Would you like to allow Activity Tracking on the Roblox client? (y/n)")
            printMainMessage("This will allow features like:")
            printMainMessage("- Server Locations")
            printMainMessage("- Multiple Instances")
            printMainMessage("- Discord Presence (+ BloxstrapRPC support)")
            printMainMessage("- Discord Webhooks")
            printMainMessage("- Mod Scripts")
            d = input("> ")
            if isYes(d) == True:
                cf.main_config["EFlagAllowActivityTracking"] = True
                saveSettings()
                printDebugMessage("User selected: True")
            elif isNo(d) == True:
                cf.main_config["EFlagAllowActivityTracking"] = False
                saveSettings()
                printDebugMessage("User selected: False")
                return
        if not cf.main_config.get("EFlagSelectedModScripts"): cf.main_config["EFlagSelectedModScripts"] = {}; saveSettings()
        s = [i for i, v in cf.main_config.get('EFlagSelectedModScripts').items() if os.path.exists(os.path.join(cf.mods_folder, "Mods", i, "ModScript.py")) and v.get("enabled") == True]
        if not use_already:
            if cf.main_config.get('EFlagSelectedModScripts') and len(s) > 0: printMainMessage(f"Selected Mod Scripts: {', '.join(s)}")
            else: printMainMessage(f"Selected Mod Scripts: None")
            printMainMessage("Select an option or a mod to enable/disable!")
            printMainMessage("Hold shift and press the up/down arrow keys to move a mod up or down in the order! (Top is first, Bottom is last)")
        generated_ui_options = []
        if not mods_manifest: mods_manifest = generateModsManifest()
        if not mod_order: mod_order = generateModOrder()
        for i, v in sorted(mods_manifest.items(), key=lambda x: mod_order.index(x[0]) if x[0] in mod_order else len(mod_order)):
            if i == "Original" or i == "OldFont" or i == "GothamFont": continue
            final_vers = "1.0.0"
            final_name = ""
            final_enabled = "❌"
            final_mod_enabled = "❌"
            if v.get("version"): final_vers = v.get("version")
            if v.get("enabled") == True: final_enabled = "✅"
            else: final_enabled = "❌"
            if v.get("name") == i: final_name = f"{i}"
            elif isinstance(v.get("name"), str): final_name = f"{v.get('name')} [{i}]"
            else: final_name = f"{i}"
            if v.get("enabled") == False and v.get("list_in_normal_mods") == False: continue
            generated_ui_options.append({"index": 1, "message": f"[{final_enabled}] {final_name} [v{final_vers}]", "final_name": final_name, "mod_info": v, "mod_id": i})
        generated_ui_options.append({"index": 1000000, "message": ts("Mod Script Settings")})
        generated_ui_options.append({"index": 1000001, "message": ts("Special Mod Settings")})
        if checkSyncFolder(): generated_ui_options.append({"index": 1000002, "message": ts("Sync Mods from Installation Folder")})
        generated_ui_options.append({"index": 1000003, "message": ts("Open Mods Folder")})
        generated_ui_options.append({"index": 1000004, "message": ts("Disable Applying Mods")})
        generated_ui_options.append({"index": 1000005, "message": ts("Clear Installed Mods [Reinstall Roblox]")})
        opt = generateMenuSelection(generated_ui_options, star_option=ts("Exit Mods Manager"), scripted_responses={"_shift_up": "u", "_shift_down": "d"}, start_index=start_index)
    else:
        generated_ui_options = []
        mods_manifest = generateModsManifest()
        mod_order = generateModOrder()
        opt = {"index": 1000000, "message": ts("Mod Script Settings")}
    if opt:
        if not use_already and not (opt["index"] < 1000000 and opt.get("target_mode")):
            if reverify_mod_script == None: startMessage()
            printSystemMessage(f"--- {opt['message']} ---")
        if opt["index"] == 1000000: modScriptSettings(0, reverify_mod_script, mods_manifest, mod_order)
        elif opt["index"] == 1000001: specialMods()
        elif opt["index"] == 1000002: syncMods()
        elif opt["index"] == 1000003: openModsFolder()
        elif opt["index"] == 1000004:
            printMainMessage("Disabling mods..")
            cf.main_config["EFlagEnableMods"] = False
            saveSettings()
            printSuccessMessage("Successfully disabled Mods! Would you like to reinstall Roblox to clear existing mods or continue with partial setup?")
            if cf.main_os == "Windows": printYellowMessage("WARNING! This will quit any open Roblox windows!")
            d = input("> ")
            if isYes(d) == True:
                cf.submit_status.start()
                res = cf.handler.installRoblox(forceQuit=cf.main_os == "Windows", debug=(cf.main_config.get("EFlagEnableDebugMode") == True), verifyInstall=cf.main_config.get("EFlagVerifyRobloxHashAfterInstall")!=False, downloadToken=createDownloadToken(studio=False))
                cf.submit_status.end()
                if res and res["success"] == False: printErrorMessage("There is an issue while trying to install Roblox. Please try again by restarting this app!")
            elif isNo(d) == True:
                saveSettings()
                printDebugMessage("User selected: False")
                return
            printMainMessage("Exiting Mods Manager..")
            return
        elif opt["index"] == 1000005: continueToInstallRobloxOptions(reinstall=True)
        else:
            if not (cf.main_config.get("EFlagEnabledMods") and isinstance(cf.main_config.get("EFlagEnabledMods"), dict)): cf.main_config["EFlagEnabledMods"] = {}
            if opt.get("mod_info"):
                if opt.get("target_mode") and opt["mod_info"]["enabled"] == True:
                    mod_order = generateModOrder()
                    cur_org = mod_order.index(opt["mod_id"]) if opt["mod_id"] in mod_order else -1
                    if cur_org == -1: printErrorMessage(f"Mod {opt.get('final_name')} not found in order!")
                    else:
                        org_adjust = 0
                        if opt["target_mode"] == "u":
                            if cur_org > 0: 
                                mod_order[cur_org], mod_order[cur_org - 1] = mod_order[cur_org - 1], mod_order[cur_org]
                                org_adjust -= 1
                        elif opt["target_mode"] == "d":
                            if cur_org < len(mod_order) - 1:
                                mod_order[cur_org], mod_order[cur_org + 1] = mod_order[cur_org + 1], mod_order[cur_org]
                                org_adjust += 1
                        next_start_index = opt.get("current_index", 0)+org_adjust
                        sys.__stdout__.write(f"\033[{len(generated_ui_options)+2}A")
                        sys.__stdout__.flush()
                        cf.main_config["EFlagEnabledModOrder"] = mod_order
                        saveSettings()
                        return mainModManager(reverify_mod_script=reverify_mod_script, mods_manifest=mods_manifest, mod_order=mod_order, start_index=next_start_index, use_already=True)
                else:
                    if opt["mod_info"]["enabled"] == True:
                        cf.main_config["EFlagEnabledMods"][opt["mod_id"]] = False
                        printSuccessMessage(f"Successfully disabled mod {opt.get('final_name')}!")
                    else:
                        cf.main_config["EFlagEnabledMods"][opt["mod_id"]] = True
                        printSuccessMessage(f"Successfully enabled mod {opt.get('final_name')}!")
            saveSettings()
            if reverify_mod_script == None: return mainModManager(start_index=opt.get("current_index", 0))
            else: printMainMessage("Exiting Mods Manager.."); return 5
        if reverify_mod_script == None: mainModManager()
        else: printMainMessage("Exiting Mods Manager.."); return 5
    else: return
def continueToModsManager(reverify_mod_script=None): # Mods Manager
    if cf.main_config.get("EFlagEnableMods") == True:
        if cf.main_config.get("EFlagDisableModsManagerAccess") != True: mainModManager(reverify_mod_script=reverify_mod_script)
        else:
            printSystemMessage("--- Mods Manager ---")
            printErrorMessage("Access to editing Mods was disabled by file. Please try again later!")
            input("> ")
            return ts("Mods Settings was not saved!")
    else:
        printSystemMessage("--- Mods Manager ---")
        printErrorMessage("Mods Enabled: No")
        printMainMessage("Would you like to enable Mods? (y/n)")
        b = input("> ")
        if isYes(b) == True:
            cf.main_config["EFlagEnableMods"] = True
            saveSettings()
            continueToModsManager(reverify_mod_script)

if __name__ == "__main__":
    print("This module is not a runable instance.")
    sys.exit(1)