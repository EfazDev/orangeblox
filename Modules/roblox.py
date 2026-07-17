# 
# OrangeBlox 🍊
# Made by Efaz from efaz.dev
# v2.6.0f
# 

import Modules.config as cf
from Modules.printing import *
from Modules.utils import *
import os
import shutil
import json
import sys
import shlex
import datetime
import importlib.machinery
import subprocess
import ctypes
import time
import re

class RobloxClientData:
    def __init__(self):
        # Event Variables
        self.current_place_info = None
        self.is_teleport = False
        self.is_app_login_fail = False
        self.connected_user_info = None
        self.updated_count = 0
        self.set_server_type = 0
        self.connected_to_game = False
        self.is_connection_lost = False
        self.set_current_private_server_key = None
        self.connected_roblox_instance = None
        self.skip_disconnect_notification = False

        # Mod Scripts
        self.mod_script_modules: dict[str, importlib.machinery.ModuleSpec] = {}
        self.generated_api_instances = {}
        self.generated_secret_keys = {}
        self.orangeapi_modules = {}
        self.mod_script_jsons = {}
        self.mod_script_locks = {}
        self.roblox_launched_affect_mod_script = False
        self.mods_manifest = generateModsManifest()
        self.mod_order = generateModOrder()
        self.selected_mod_scripts = sorted(
            [i for i, v in cf.main_config.get('EFlagSelectedModScripts', {}).items() if os.path.exists(os.path.join(cf.mods_folder, "Mods", i, "ModScript.py")) and v.get("enabled") == True],
            key=lambda x: self.mod_order.index(x) if x in self.mod_order else len(self.mod_order)
        )
rcf = None

# Base Roblox Functions
def prepareRobloxClient():
    printSystemMessage(ts("--- Preparing Roblox Studio ---") if cf.run_studio == True else ts("--- Preparing Roblox ---"))
    if cf.main_os == "Windows":
        cf.content_folder_paths["Windows"] = cf.handler.getRobloxInstallFolder(studio=cf.run_studio)
        cf.font_folder_paths["Windows"] = os.path.join(cf.content_folder_paths['Windows'], "content", "fonts")
    elif cf.main_os == "Darwin":
        cf.content_folder_paths["Darwin"] = os.path.join(rbx.macOS_studioDir if cf.run_studio == True else rbx.macOS_dir, "Contents", "Resources")
        cf.font_folder_paths["Darwin"] = os.path.join(cf.content_folder_paths['Darwin'], "content", "fonts")
    if not os.path.exists(cf.font_folder_paths[cf.main_os]):
        printErrorMessage(f"Please restart OrangeBlox in order to reinstall {'Roblox Studio' if cf.run_studio == True else 'Roblox'}!")
        input("> ")
        sys.exit(0)
        return
    if cf.connect_instead == True: printMainMessage("Skipping Preparation because you're connecting instead of launching a new window!"); return

    try:
        printDebugMessage(f"Roblox Resources Location: {cf.content_folder_paths[cf.main_os]}")
        applyRemoveBuilder() # Remove Builder Font
        applyAvatarEditorBG() # Avatar Background
        applyCursors() # Cursors
        applyPlayerSounds() # Player Sounds
        applyAppIcons() # App Icons
        applyInstallerApps() # Installer Apps
        applyStudioDocumentation() # Studio Documentations and Fonts
        applyCustomMods() # Custom Mods
        applyFastFlags() # FFlags
        applyOSRegistration() # Registration
    except Exception:
        printErrorMessage(f"There was a problem applying mods to the Roblox Client!")
        printDebugMessage(f"Error Message: \n{trace()}")
def applyRemoveBuilder():
    cf.submit_status.start()
    font_list = ["BuilderSans-ExtraBold.otf", "BuilderSans-Bold.otf", "BuilderSans-Medium.otf", "BuilderSans-Regular.otf", "BuilderExtended-Bold.otf", "BuilderExtended-SemiBold.otf", "BuilderExtended-Regular.otf", "Montserrat-Black.ttf", "Montserrat-Bold.ttf", "Montserrat-Medium.ttf", "Montserrat-Regular.ttf", "BuilderMono-Regular.otf", "BuilderMono-Light.otf", "BuilderMono-Bold.otf", "Arimo-Regular.ttf", "Arimo-Bold.ttf"]
    if cf.main_config.get("EFlagRemoveBuilderFont") == True:
        cf.submit_status.submit(ts("Changing Font Files.."), 10)
        # Copy All Builder/Monsterrat Files to Separate Files
        if not os.path.exists(os.path.join(cf.font_folder_paths[cf.main_os], "BuilderSansLock")):
            for i, font_file in enumerate(font_list):
                cf.submit_status.submit(ts(f"Locking font: {font_file}"), 10 + int((i / len(font_list)) * 70))
                src_font = os.path.join(cf.font_folder_paths[cf.main_os], font_file)
                if os.path.exists(src_font):
                    name, ext = os.path.splitext(font_file)
                    locked_font = os.path.join(cf.font_folder_paths[cf.main_os], f"{name}-Locked{ext}")
                    copyFile(src_font, locked_font)
            with open(os.path.join(cf.font_folder_paths[cf.main_os], "BuilderSansLock"), "w", encoding="utf-8") as f: f.write("EnabledGothamFontMode")
        if not cf.main_config.get("EFlagEnabledMods"): cf.main_config["EFlagEnabledMods"] = {}
        cf.main_config["EFlagEnabledMods"]["OldFont"] = True
        cf.main_config["EFlagEnableMods"] = True
        cf.submit_status.submit(ts("Successfully prepared change for Builder Sans/Monsterrat files to GothamSSm!"), 100)
    else:
        if os.path.exists(os.path.join(cf.font_folder_paths[cf.main_os], "BuilderSansLock")):
            for i, font_file in enumerate(font_list):
                cf.submit_status.submit(ts(f"Reverting font: {font_file}"), 10 + int((i / len(font_list)) * 70))
                src_font = os.path.join(cf.font_folder_paths[cf.main_os], font_file)
                if os.path.exists(src_font):
                    name, ext = os.path.splitext(font_file)
                    locked_font = os.path.join(cf.font_folder_paths[cf.main_os], f"{name}-Locked{ext}")
                    copyFile(locked_font, src_font)
            with open(os.path.join(cf.font_folder_paths[cf.main_os], "BuilderSansLock"), "w", encoding="utf-8") as f: f.write("EnabledGothamFontMode")
            cf.submit_status.submit(ts("Successfully reverted fonts!"), 100)
        else: cf.submit_status.submit(ts("Builder Sans is already being used!"), 100)
    cf.submit_status.end()
def applyAvatarEditorBG():
    cf.submit_status.start()
    avatar_editor_map = os.path.join(cf.content_folder_paths[cf.main_os], "content", "places", "AvatarEditor.rbxl")
    if cf.main_config.get("EFlagEnableChangeAvatarEditorBackground") == True:
        cf.submit_status.submit(ts("Changing Current Avatar Editor to Set Avatar Background.."), 0)
        avatar_editor_map = f"{cf.main_config.get('EFlagAvatarEditorBackground')}.rbxl"
    else:
        cf.submit_status.submit(ts("Changing Current Avatar Editor to Original Avatar Background.."), 0)
        avatar_editor_map = f"Original.rbxl"
    cf.submit_status.submit(ts("Applying map files..."), 60)
    copyFile(os.path.join(cf.mods_folder, "AvatarEditorMaps", avatar_editor_map), os.path.join(cf.content_folder_paths[cf.main_os], "ExtraContent", "places", "Mobile.rbxl"))
    copyFile(os.path.join(cf.mods_folder, "AvatarEditorMaps", avatar_editor_map), os.path.join(cf.content_folder_paths[cf.main_os], "content", "places", "AvatarEditor.rbxl"))
    cf.submit_status.submit(ts("Successfully changed avatar editor!"), 100)
    cf.submit_status.end()
def applyCursors():
    cf.submit_status.start()
    texture_dir = os.path.join(cf.content_folder_paths[cf.main_os], "content", "textures")
    if cf.main_config.get("EFlagEnableChangeCursor") == True:
        cf.submit_status.submit(ts("Changing Current Cursor to Set Cursor.."), 10)
        cursor_folder = os.path.join(cf.mods_folder, "Cursors", cf.main_config.get('EFlagSelectedCursor'))
    else:
        cf.submit_status.submit(ts("Changing Current Cursor to Original Cursor.."), 10)
        cursor_folder = os.path.join(cf.mods_folder, "Cursors", "Original")
    cf.submit_status.submit(ts("Copying cursor assets..."), 50)
    copyFile(os.path.join(cursor_folder, "ArrowCursor.png"), os.path.join(texture_dir, "Cursors", "KeyboardMouse", "ArrowCursor.png"))
    copyFile(os.path.join(cursor_folder, "ArrowFarCursor.png"), os.path.join(texture_dir, "Cursors", "KeyboardMouse", "ArrowFarCursor.png"))
    copyFile(os.path.join(cursor_folder, "IBeamCursor.png"), os.path.join(texture_dir, "Cursors", "KeyboardMouse", "IBeamCursor.png"))
    cf.submit_status.submit(ts("Successfully changed cursors!"), 100)
    cf.submit_status.end()
def applyPlayerSounds():
    cf.submit_status.start()
    if cf.main_config.get("EFlagEnableChangePlayerSound") == True:
        cf.submit_status.submit(ts("Changing Current Player Sounds to Set Sound Files.."), 5)
        sounds_folder = os.path.join(cf.mods_folder, "PlayerSounds", cf.main_config.get('EFlagSelectedPlayerSounds'))
    else:
        cf.submit_status.submit(ts("Changing Current Player Sounds to Original Sound Files.."), 5)
        sounds_folder = os.path.join(cf.mods_folder, "PlayerSounds", "Current")
    sound_files = ["ouch.ogg", "action_falling.ogg", "action_footsteps_plastic.mp3", "action_get_up.mp3", "action_jump_land.mp3", "action_jump.mp3", "action_swim.mp3", "impact_explosion_03.mp3", "impact_water.mp3", "volume_slider.ogg"]
    for i, filename in enumerate(sound_files):
        current_percent = 10 + int((i / len(sound_files)) * 80)
        cf.submit_status.submit(ts(f"Copying {filename}.."), current_percent)
        copyFile(os.path.join(sounds_folder, filename), os.path.join(cf.content_folder_paths[cf.main_os], "content", "sounds", filename))
    cf.submit_status.submit(ts("Successfully changed player sounds!"), 100)
    cf.submit_status.end()
def applyAppIcons():
    cf.submit_status.start()
    cf.submit_status.submit(ts("Changing Brand Images.."), 10)
    if cf.run_studio == True:
        if cf.main_config.get("EFlagEnableChangeBrandIcons2") == True: brand_fold = os.path.join(cf.mods_folder, "RobloxStudioBrand", cf.main_config.get('EFlagSelectedBrandLogo2'))
        else: brand_fold = os.path.join(cf.mods_folder, "RobloxStudioBrand", "Original")
    else:
        if cf.main_config.get("EFlagEnableChangeBrandIcons") == True: brand_fold = os.path.join(cf.mods_folder, "RobloxBrand", cf.main_config.get('EFlagSelectedBrandLogo'))
        else: brand_fold = os.path.join(cf.mods_folder, "RobloxBrand", "Original")
    if cf.run_studio == False:
        cf.submit_status.submit(ts("Copying brand assets.."), 30)
        for path, filename in {
            "content/textures/ui/TopBar/coloredlogo.png": "MenuIcon.png",
            "content/textures/ui/TopBar/coloredlogo@2x.png": "MenuIcon@2x.png",
            "content/textures/ui/TopBar/coloredlogo@3x.png": "MenuIcon@3x.png",
            "content/textures/ui/ScreenshotHud/RobloxLogo.png": "RobloxLogo.png",
            "content/textures/ui/ScreenshotHud/RobloxLogo@2x.png": "RobloxLogo@2x.png",
            "content/textures/ui/ScreenshotHud/RobloxLogo@3x.png": "RobloxLogo@3x.png",
            "ExtraContent/textures/ui/LuaApp/graphic/Auth/logo_white_1x.png": "RobloxLogoBanner.png",
            "ExtraContent/textures/ui/LuaApp/graphic/Auth/logo_white_luobu.png": "RobloxLogoBannerLuobu.png",
            "content/textures/ui/RobloxNameIcon.png": "RobloxNameIcon.png",
            "content/textures/ui/icon_admin-16.png": "AdminIcon.png",
            "content/textures/loading/robloxTilt.png": "RobloxTilt.png",
            "content/textures/loading/robloxTiltRed.png": "RobloxTilt.png"
        }.items():
            if os.path.exists(os.path.join(brand_fold, filename)): copyFile(os.path.join(brand_fold, filename), os.path.join(cf.content_folder_paths[cf.main_os], path))
    if cf.main_os == "Darwin":
        cf.submit_status.submit(ts("Changing Current App Icon.."), 60)
        if os.path.exists(os.path.join(brand_fold, "AppIcon.icns")): 
            copyFile(os.path.join(brand_fold, "AppIcon.icns"), os.path.join(cf.content_folder_paths[cf.main_os], "AppIcon.icns"))
            if os.path.exists(os.path.join(cf.content_folder_paths[cf.main_os], "../", "MacOS", "RobloxStudio.app" if cf.run_studio == True else "Roblox.app")): copyFile(os.path.join(brand_fold, "AppIcon.icns"), os.path.join(cf.content_folder_paths[cf.main_os], "../", "MacOS", "RobloxStudio.app" if cf.run_studio == True else "Roblox.app", "Contents", "Resources", "AppIcon.icns"))
            targ_app = os.path.join(cf.content_folder_paths[cf.main_os], '../', '../')
            try:
                subprocess.run([cf.pip_class.getPathFile("/usr/bin/touch"), targ_app], stdout=None if cf.main_config.get("EFlagEnableDebugMode") else subprocess.DEVNULL, stderr=None if cf.main_config.get("EFlagEnableDebugMode") else subprocess.DEVNULL)
                subprocess.run(["/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister", "-f", targ_app], stdout=None if cf.main_config.get("EFlagEnableDebugMode") else subprocess.DEVNULL, stderr=None if cf.main_config.get("EFlagEnableDebugMode") else subprocess.DEVNULL)
            except Exception: printDebugMessage("Something went wrong trying to set icon fully!")
            printSuccessMessage("Successfully changed current app icon! It may take a moment for macOS to identify it!")
    elif cf.main_os == "Windows":
        cf.submit_status.submit(ts("Changing App Shortcuts Icon.."), 60)
        if os.path.exists(os.path.join(brand_fold, "AppIcon.ico")): 
            try:
                import win32com.client as win32client # type: ignore
                import pythoncom # type: ignore
                pythoncom.CoInitialize()
                try:
                    shell = win32client.Dispatch('WScript.Shell')
                    bootstrap_path = os.path.join(cf.cur_path, "OrangeBlox.exe")
                    icon = os.path.join(brand_fold, "AppIcon.ico") if cf.main_config.get("EFlagUseRobloxAppIconAsShortcutIcon") else ""
                    desktop_dir = os.path.join(os.environ['USERPROFILE'], 'Desktop')
                    start_menu_dir = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs')
                    roblox_start_dir = os.path.join(start_menu_dir, 'Roblox')
                    createWindowsShortcut(shell, bootstrap_path, os.path.join(start_menu_dir, "OrangeBlox.lnk"))
                    createWindowsShortcut(shell, bootstrap_path, os.path.join(desktop_dir, "OrangeBlox.lnk"))
                    if cf.run_studio == True:
                        shortcuts = [
                            (os.path.join(desktop_dir, "Roblox Studio.lnk"), "orangeblox://run-studio"),
                            (os.path.join(start_menu_dir, 'Run Studio.lnk'), "orangeblox://run-studio"),
                            (os.path.join(roblox_start_dir, 'Roblox Studio.lnk'), "orangeblox://run-studio")
                        ]
                    else:
                        shortcuts = [
                            (os.path.join(desktop_dir, "Roblox Player.lnk"), "orangeblox://continue"),
                            (os.path.join(start_menu_dir, 'Play Roblox.lnk'), "orangeblox://continue"),
                            (os.path.join(roblox_start_dir, 'Roblox Player.lnk'), "orangeblox://continue")
                        ]
                    for shortcut_path, arg in shortcuts: createWindowsShortcut(shell, bootstrap_path, shortcut_path, icon_path=icon, arguments=arg)
                    printSuccessMessage("Successfully changed current shortcut icons! It may take a moment for Windows to identify it!")
                    del shell
                finally: pythoncom.CoUninitialize()
            except Exception as e: printErrorMessage(f"Unable to create shortcuts: {str(e)}")
    if (cf.run_studio == True and cf.main_config.get("EFlagEnableChangeBrandIcons2") == True) or (cf.run_studio == False and cf.main_config.get("EFlagEnableChangeBrandIcons") == True): 
        cf.submit_status.submit(ts("Successfully changed brand images!"), 100)
    else: cf.submit_status.submit(ts("Successfully changed brand images to original!"), 100)
    cf.submit_status.end()
def applyInstallerApps():
    cf.submit_status.start()
    cf.submit_status.submit(ts("Installing Updater Apps.."), 10)
    try:
        if cf.main_os == "Windows":
            cf.submit_status.submit(ts("Deploying Installers.."), 40)
            cf.pip_class.copyTreeWithMetadata(os.path.join(cf.cur_path, "_internal"), os.path.join(cf.content_folder_paths[cf.main_os], "_internal"), dirs_exist_ok=True, ignore_if_not_exist=True)
            shutil.copy(os.path.join(cf.cur_path, "OrangeBlox.exe" if cf.run_studio == True else "OrangeBlox.exe"), os.path.join(cf.content_folder_paths[cf.main_os], "RobloxStudioInstaller.exe" if cf.run_studio == True else "RobloxPlayerInstaller.exe"))
            with open(os.path.join(cf.content_folder_paths[cf.main_os], "RobloxStudioBetaPlayRobloxRestart.txt" if cf.run_studio == True else "RobloxPlayerBetaPlayRobloxRestart.txt"), "w", encoding="utf-8") as f: f.write(cf.cur_path)
        elif cf.main_os == "Darwin":
            backspacing = os.path.join(cf.macos_app_path, "../")
            if os.path.exists(os.path.join(backspacing, "Play Roblox.app")):
                cf.submit_status.submit(ts("Deploying Player Installer.."), 30)
                cf.pip_class.copyTreeWithMetadata(os.path.join(backspacing, "Play Roblox.app"), os.path.join(rbx.macOS_dir, "Contents", "MacOS", "RobloxPlayerInstaller.app"), dirs_exist_ok=True)
                shutil.copy(os.path.join(backspacing, "Play Roblox.app", "Contents", "MacOS", "OrangePlayRoblox"), os.path.join(rbx.macOS_dir, "Contents", "MacOS", "RobloxPlayerInstaller.app", "Contents", "MacOS", "RobloxPlayerInstaller"))
                with open(os.path.join(rbx.macOS_dir, "Contents", "MacOS", "RobloxPlayerInstaller.app", "Contents", "Resources", "RobloxPlayerBetaPlayRobloxRestart"), "w", encoding="utf-8") as f: f.write(cf.cur_path)
                createMacOSCodesign(os.path.join(rbx.macOS_dir, "Contents", "MacOS", "RobloxPlayerInstaller.app"), cf.main_config.get("EFlagRobloxCodesigningName", "-"))
            if os.path.exists(rbx.macOS_studioDir) and cf.run_studio == True and os.path.exists(os.path.join(backspacing, "Run Studio.app")):
                cf.submit_status.submit(ts("Deploying Studio Installer.."), 60)
                cf.pip_class.copyTreeWithMetadata(os.path.join(backspacing, "Run Studio.app"), os.path.join(rbx.macOS_studioDir, "Contents", "MacOS", "RobloxStudioInstaller.app"), dirs_exist_ok=True)
                shutil.copy(os.path.join(backspacing, "Run Studio.app", "Contents", "MacOS", "OrangeRunStudio"), os.path.join(rbx.macOS_studioDir, "Contents", "MacOS", "RobloxStudioInstaller.app", "Contents", "MacOS", "RobloxStudioInstaller"))
                with open(os.path.join(rbx.macOS_studioDir, "Contents", "MacOS", "RobloxStudioInstaller.app", "Contents", "Resources", "RobloxStudioBetaPlayRobloxRestart"), "w", encoding="utf-8") as f: f.write(cf.cur_path)
                createMacOSCodesign(os.path.join(rbx.macOS_studioDir, "Contents", "MacOS", "RobloxStudioInstaller.app"), cf.main_config.get("EFlagRobloxCodesigningName", "-"))
        cf.submit_status.submit(ts("Successfully installed updater apps!"), 100)
    except Exception: printErrorMessage(f"Unable to update installer apps! Recorded Error: \n{trace()}")
    cf.submit_status.end()
def applyStudioDocumentation():
    cf.submit_status.start()
    try:
        api_doc = os.path.join(cf.content_folder_paths[cf.main_os], "content", "api_docs")
        if cf.run_studio == True and cf.main_config.get("EFlagLimitAPIDocsLocalization") and os.path.exists(api_doc):
            localization_file = f'{cf.main_config.get("EFlagLimitAPIDocsLocalization")}.json'
            cf.submit_status.submit(ts(f"Clearing API Docs Localization to {localization_file}"), 30)
            for i in os.listdir(api_doc):
                if i == localization_file: continue
                if os.path.isfile(os.path.join(api_doc, i)): os.remove(os.path.join(api_doc, i))
        studio_fonts = os.path.join(cf.content_folder_paths[cf.main_os], "StudioFonts")
        if cf.run_studio == True and cf.main_config.get("EFlagOverwriteUnneededStudioFonts") and os.path.exists(studio_fonts):
            cf.submit_status.submit(ts("Overwriting Studio Fonts to None.."), 70)
            for i in os.listdir(studio_fonts):
                if not i.startswith("NotoSans"): continue
                if os.path.isfile(os.path.join(studio_fonts, i)): open(os.path.join(studio_fonts, i), "w").close()
        cf.submit_status.submit(ts("Finished handling documentation and fonts."), 100)
    except Exception: printErrorMessage(f"Unable to overwrite API Documentation and Studio Fonts. Recorded Error: \n{trace()}")
    cf.submit_status.end()
def applyCustomMods():
    cf.submit_status.start()
    if cf.main_config.get("EFlagEnableMods") == True:
        cf.submit_status.submit(ts("Applying Mods.."), 10)
        if type(cf.main_config.get("EFlagEnabledMods")) is dict:
            mod_order = generateModOrder()
            mod_order_map = {m: i for i, m in enumerate(mod_order)}
            fallback_id = len(mod_order)
            sorted_mods = sorted(
                cf.main_config.get("EFlagEnabledMods").items(), 
                key=lambda x: mod_order_map.get(x[0], fallback_id)
            )
            for step, (i, v) in enumerate(sorted_mods):
                if v == True:
                    cf.submit_status.submit(ts(f"Applying Custom Mod: {i}.."), 20 + int((step / len(sorted_mods)) * 75) if len(sorted_mods) > 0 else 50)
                    try:
                        mod_path = os.path.join(os.path.join(cf.mods_folder, "Mods"), i)
                        is_studio = False
                        if os.path.exists(mod_path) and os.path.isdir(mod_path):
                            ignore_given_files = []
                            if os.path.exists(os.path.join(mod_path, "Manifest.json")):
                                manife = readJSONFile(os.path.join(mod_path, "Manifest.json"))
                                if manife and manife.get("ignore_transfer_of_files") and type(manife.get("ignore_transfer_of_files")) is list: ignore_given_files = manife.get("ignore_transfer_of_files")
                                if manife and (manife.get("is_studio_mod") == True or (cf.run_studio == True and manife.get("player_studio_support") == True)): is_studio = True
                            if os.path.exists(os.path.join(mod_path, "StudioMod")): is_studio = True
                            if is_studio == cf.run_studio:
                                def ignore_files_here(dir, files): return set(["ModScript.py", "Manifest.json", "Translations", f"Configuration_{cf.user_folder_name}", "__pycache__"] + ignore_given_files) & set(files)
                                cf.pip_class.copyTreeWithMetadata(mod_path, cf.content_folder_paths[cf.main_os], dirs_exist_ok=True, ignore=ignore_files_here)
                                cf.submit_status.submit(ts(f'Successfully applied "{i}" mod!'), 20 + int((step / len(sorted_mods)) * 75) if len(sorted_mods) > 0 else 50)
                    except Exception: printErrorMessage(f"Unable to apply mod files of {i}. Recorded Error: \n{trace()}")
            cf.submit_status.submit(ts("Successfully applied all enabled mods!"), 100)
    cf.submit_status.end()
def applyFastFlags():
    printMainMessage("Installing Fast Flags..")
    try:
        filtered_fast_flags = {}
        if cf.run_studio == True and cf.main_config.get("EFlagRobloxStudioFlags"):
            for i, v in cf.main_config.get("EFlagRobloxStudioFlags").items():
                if i and (not i.startswith("EFlag")): filtered_fast_flags[i] = v
        elif cf.run_studio == False and cf.main_config.get("EFlagRobloxPlayerFlags"):
            current_channel = fetchRbxChannel(studio=False)
            fflag_allowlist = cf.handler.getFastFlagsAllowlist(debug=(cf.main_config.get("EFlagEnableDebugMode") == True), bucket=current_channel).get("allowlist", [])
            if not fflag_allowlist: printErrorMessage("Unable to get Fast Flags Allowlist! Please check your internet connection and try again!"); return
            for i, v in cf.main_config.get("EFlagRobloxPlayerFlags").items():
                if i and (not i.startswith("EFlag")) and i in fflag_allowlist: filtered_fast_flags[i] = v
        cf.submit_status.start()
        cf.handler.installFastFlags(filtered_fast_flags, debug=(cf.main_config.get("EFlagEnableDebugMode") == True), endRobloxInstances=False, studio=cf.run_studio, merge=False)
        cf.submit_status.end()
        printSuccessMessage("Successfully installed FFlags to the Roblox files!")
    except Exception: printErrorMessage(f"Unable to install Fast Flags to the client! Recorded Error: \n{trace()}")
def applyOSRegistration():
    cf.submit_status.start()
    if cf.main_os == "Darwin":
        try:
            if cf.run_studio == True:
                if os.path.exists(os.path.join(rbx.macOS_studioDir, "Contents", "Info.plist")):
                    plist_data = cf.plist_class.readPListFile(os.path.join(rbx.macOS_studioDir, "Contents", "Info.plist"))
                    if plist_data.get("CFBundleName"):
                        cf.submit_status.submit(ts("Editing Roblox Studio Info.plist.."), 15)
                        plist_data["CFBundleURLTypes"] = []
                        plist_data["CFBundleDocumentTypes"] = []
                        plist_data["UTExportedTypeDeclarations"] = []
                        plist_data["NSDisableAutomaticTermination"] = True
                        plist_data["NSPersistentStoreRebuildDisallowed"] = True
                        plist_data["CFBundleIconFile"] = "AppIcon.icns"
                        plist_data["CFBundleIconName"] = "AppIcon.icns"
                        cf.submit_status.submit(ts("Successfully removed all URL Schemes for Roblox Studio.app!"), 20)
                        s = cf.plist_class.writePListFile(os.path.join(rbx.macOS_studioDir, "Contents", "Info.plist"), plist_data)
                        if s["success"] == True:
                            subprocess.run([f"/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister", "-f", os.path.join(cf.content_folder_paths[cf.main_os], '../', '../')], stdout=None if cf.main_config.get("EFlagEnableDebugMode") else subprocess.DEVNULL, stderr=None if cf.main_config.get("EFlagEnableDebugMode") else subprocess.DEVNULL)
                            cf.submit_status.submit(ts("Successfully wrote to Info.plist!"), 25)
                        else: printErrorMessage(f"Something went wrong saving Roblox Info.plist: {s['message']}")
                        if cf.main_config.get("EFlagRemoveCodeSigningMacOS") == True:
                            cf.submit_status.submit(ts("Checking for Code Signatures.."), 30)
                            if os.path.exists(f"{rbx.macOS_studioDir}/Contents/_CodeSignature/"):
                                shutil.rmtree(f"{rbx.macOS_studioDir}/Contents/_CodeSignature/", ignore_errors=True)
                                printSuccessMessage("Removed Code-signing on Roblox Studio.app!")
                            else: printSuccessMessage("Removing Code-signing is not needed because it doesn't exist!")
                        cf.submit_status.submit(ts("Validating code-sign.."), 45)
                        if cf.main_config.get("EFlagRemoveCodeSigningMacOS") == True or checkMacOSCodesign(os.path.join(rbx.macOS_studioDir, "Contents", "MacOS", "RobloxStudio"), silent=cf.main_config.get("EFlagEnableDebugMode", False)) == False:
                            cf.submit_status.submit(ts("Signing Roblox Studio.app.."), 50)
                            def req_codesign(co=0):
                                cf.plist_class.writePListFile(os.path.join(cf.orangeblox_library, "RbxStudioEntitlements.plist"), {
                                    "com.apple.security.cs.allow-jit": True,
                                    "com.apple.security.cs.disable-executable-page-protection": True,
                                    "com.apple.security.device.audio-input": True,
                                    "com.apple.security.device.camera": True,
                                    "com.apple.security.network.client": True
                                })
                                result = createMacOSCodesign(rbx.macOS_studioDir, cf.main_config.get("EFlagRobloxCodesigningName", "-"), entitlements=os.path.join(cf.orangeblox_library, "RbxStudioEntitlements.plist"), run_only=True)
                                os.remove(os.path.join(cf.orangeblox_library, "RbxStudioEntitlements.plist"))
                                printDebugMessage(f"Code Signing Response: {result.returncode}")
                                if result.returncode == 0: printSuccessMessage("Successfully signed Roblox Studio.app!")
                                else:
                                    printErrorMessage(f"Unable to sign Roblox Studio.app: {result.returncode}")
                                    if co == 0: printMainMessage("Attempting Resign! Please wait!")
                                    if os.path.exists(os.path.join(rbx.macOS_studioDir, "Contents", "_CodeSignature")): shutil.rmtree(os.path.join(rbx.macOS_studioDir, "Contents", "_CodeSignature"), ignore_errors=True)
                                    req_codesign(co=co+1)
                            req_codesign()
                        else: printSuccessMessage("Code-signing is valid for use!")
                    else: printErrorMessage(f"Something went wrong reading Roblox Studio Info.plist: Bundle name not found")
                else: printErrorMessage(f"Something went wrong reading Roblox Studio Info.plist: Bundle not found")
            else:
                if os.path.exists(os.path.join(rbx.macOS_dir, "Contents", "Info.plist")):
                    plist_data = cf.plist_class.readPListFile(os.path.join(rbx.macOS_dir, "Contents", "Info.plist"))
                    if plist_data.get("CFBundleName"):
                        cf.submit_status.submit(ts("Editing Roblox Info.plist.."), 15)
                        plist_data["CFBundleIconFile"] = "AppIcon.icns"
                        plist_data["CFBundleIconName"] = "AppIcon.icns"
                        if plist_data.get("LSMultipleInstancesProhibited") == False:
                            plist_data["LSMultipleInstancesProhibited"] = True
                            printDebugMessage(f"Successfully set plist key LSMultipleInstancesProhibited to True!")
                        if plist_data.get("CFBundleURLTypes"):
                            plist_data["CFBundleURLTypes"] = []
                            plist_data["NSDisableAutomaticTermination"] = True
                            plist_data["NSPersistentStoreRebuildDisallowed"] = True
                            printDebugMessage(f"Successfully removed all URL Schemes for Roblox.app!")
                        s = cf.plist_class.writePListFile(os.path.join(rbx.macOS_dir, "Contents", "Info.plist"), plist_data)
                        if s["success"] == True:
                            subprocess.run([f"/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister", "-f", os.path.join(cf.content_folder_paths[cf.main_os], '../', '../')], stdout=None if cf.main_config.get("EFlagEnableDebugMode") else subprocess.DEVNULL, stderr=None if cf.main_config.get("EFlagEnableDebugMode") else subprocess.DEVNULL)
                            printSuccessMessage("Successfully wrote to Info.plist!")
                        else: printErrorMessage(f"Something went wrong saving Roblox Info.plist: {s['message']}")
                        if cf.main_config.get("EFlagDisableRobloxReopenAfterRestart") == True:
                            cf.submit_status.submit(ts("Disabling Roblox Reopen.."), 20)
                            subprocess.run([f"/usr/bin/defaults", "write", "com.roblox.RobloxPlayer", "NSQuitAlwaysKeepsWindows", "-bool", "false"], stdout=None if cf.main_config.get("EFlagEnableDebugMode") else subprocess.DEVNULL, stderr=None if cf.main_config.get("EFlagEnableDebugMode") else subprocess.DEVNULL)
                        if cf.main_config.get("EFlagRemoveCodeSigningMacOS") == True:
                            cf.submit_status.submit(ts("Checking for Code Signatures.."), 30)
                            if os.path.exists(os.path.join(rbx.macOS_dir, "Contents", "_CodeSignature")):
                                shutil.rmtree(os.path.join(rbx.macOS_dir, "Contents", "_CodeSignature"), ignore_errors=True)
                                printSuccessMessage("Removed Code-signing on Roblox.app!")
                            else: printSuccessMessage("Removing Code-signing is not needed because it doesn't exist!")
                        cf.submit_status.submit(ts("Validating code-sign.."), 45)
                        if cf.main_config.get("EFlagRemoveCodeSigningMacOS") == True or checkMacOSCodesign(os.path.join(rbx.macOS_dir, "Contents", "MacOS", "RobloxPlayer"), silent=cf.main_config.get("EFlagEnableDebugMode", False)) == False:
                            cf.submit_status.submit(ts("Signing Roblox.app.."), 50)
                            def req_codesign(co=0):
                                cf.plist_class.writePListFile(os.path.join(cf.orangeblox_library, "RbxEntitlements.plist"), {
                                    "com.apple.security.cs.allow-jit": True,
                                    "com.apple.security.cs.disable-executable-page-protection": True,
                                    "com.apple.security.device.audio-input": True,
                                    "com.apple.security.device.camera": True,
                                    "com.apple.security.network.client": True
                                })
                                result = createMacOSCodesign(rbx.macOS_dir, cf.main_config.get("EFlagRobloxCodesigningName", "-"), entitlements=os.path.join(cf.orangeblox_library, "RbxEntitlements.plist"), run_only=True)
                                os.remove(os.path.join(cf.orangeblox_library, "RbxEntitlements.plist"))
                                printDebugMessage(f"Code Signing Response: {result.returncode}")
                                if result.returncode == 0: printSuccessMessage("Successfully signed Roblox.app!")
                                else:
                                    printErrorMessage(f"Unable to sign Roblox.app: {result.returncode}")
                                    if co == 0: printMainMessage("Attempting Resign! Please wait!")
                                    if os.path.exists(os.path.join(rbx.macOS_dir, "Contents", "_CodeSignature")): shutil.rmtree(os.path.join(rbx.macOS_dir, "Contents", "_CodeSignature"), ignore_errors=True)
                                    req_codesign(co=co+1)
                            req_codesign()
                        else: printSuccessMessage("Code-signing is valid for use!")
                    else: printErrorMessage(f"Something went wrong reading Roblox Info.plist: Bundle name not found")
                else: printErrorMessage(f"Something went wrong reading Roblox Info.plist: Bundle not found")
        except Exception: printErrorMessage(f"Something went wrong modifying Info.plist of Roblox client: \n{trace()}")

        try:
            if cf.main_config.get("EFlagRemoveRobloxAppDockShortcut") == True:
                dock_path = os.path.join(os.path.expanduser("~"), "Library", "Preferences", "com.apple.dock.plist")
                dock_data = {}
                shortcut_replaced = False
                if os.path.exists(dock_path):
                    cf.submit_status.submit(ts("Overwriting Dock Preferences.."), 75)
                    dock_data = cf.plist_class.readPListFile(dock_path)
                    if dock_data.get("persistent-apps"):
                        for i in dock_data["persistent-apps"]:
                            if i and i.get("tile-data"):
                                if i["tile-data"].get("bundle-identifier") == ("com.Roblox.RobloxStudio" if cf.run_studio == True else "com.roblox.RobloxPlayer"):
                                    dock_data["persistent-apps"].remove(i)
                                    shortcut_replaced = True
                if shortcut_replaced == True:
                    cf.plist_class.writePListFile(dock_path, dock_data)
                    time.sleep(1)
                    subprocess.run([cf.pip_class.getPathFile("/usr/bin/killall"), "cfprefsd"], cwd=cf.cur_path)
                    subprocess.run([cf.pip_class.getPathFile("/usr/bin/killall"), "Dock"], cwd=cf.cur_path)
                    printSuccessMessage("Successfully removed RobloxStudio.app Dock Shortcut!" if cf.run_studio == True else "Successfully removed Roblox.app Dock Shortcut!")
                else: printSuccessMessage("No changes were made to the dock!")
        except Exception: printErrorMessage(f"Unable to make changes to the dock: \n{trace()}")
    elif cf.main_os == "Windows" and os.path.exists(os.path.join(cf.cur_path, "OrangeBlox.exe")):
        # Reapply URL Schemes
        if cf.main_config.get("EFlagDisableURLSchemeInstall") != True:
            bootstrap_folder_path = cf.cur_path
            bootstrap_path = os.path.join(bootstrap_folder_path, "OrangeBlox.exe")
            try:
                cf.submit_status.submit(ts("Setting up URL Schemes.."), 20)
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
                if cf.run_studio == True:
                    set_url_scheme("roblox-studio", bootstrap_path)
                    set_url_scheme("roblox-studio-auth", os.path.join(cf.content_folder_paths["Windows"], "RobloxStudioBeta.exe"))
                set_url_scheme("roblox", bootstrap_path)
                set_file_type_reg(".rbxl", bootstrap_path, "Roblox Place")
                set_file_type_reg(".rbxlx", bootstrap_path, "Roblox Place")
                set_file_type_reg(".obx", bootstrap_path, "OrangeBlox Backup")
            except Exception: printErrorMessage(f"Something went wrong setting up URL schemes: \n{trace()}")

        # Reapply Shortcuts
        if cf.main_config.get("EFlagDisableShortcutsInstall") != True:
            try:
                cf.submit_status.submit(ts("Setting up shortcuts.."), 50)
                import win32com.client as win32client # type: ignore
                import pythoncom # type: ignore
                pythoncom.CoInitialize()
                try:
                    shell = win32client.Dispatch('WScript.Shell')
                    createWindowsShortcut(shell, bootstrap_path, os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs'), "OrangeBlox.lnk"))
                    createWindowsShortcut(shell, bootstrap_path, os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), "OrangeBlox.lnk"))
                    del shell
                finally: pythoncom.CoUninitialize()
            except Exception: printErrorMessage(f"Something went wrong setting up shortcuts: \n{trace()}")

        # Reapply Installation to Windows
        try:
            cf.submit_status.submit(ts("Marking Program Installation into Windows.."), 75)
            app_reg_path = "Software\\OrangeBlox"
            app_key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, app_reg_path)
            win32api.RegSetValueEx(app_key, "InstallPath", 0, win32con.REG_SZ, bootstrap_folder_path)
            win32api.RegSetValueEx(app_key, "Installed", 0, win32con.REG_DWORD, 1)
            win32api.RegCloseKey(app_key)
            registry_path = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\OrangeBlox"
            registry_key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, registry_path)
            win32api.RegSetValueEx(registry_key, "UninstallString", 0, win32con.REG_SZ, f"\"{sys.executable}\" \"{os.path.join(bootstrap_folder_path, 'Install.py')}\" -un")
            win32api.RegSetValueEx(registry_key, "ModifyPath", 0, win32con.REG_SZ, f"\"{sys.executable}\" \"{os.path.join(bootstrap_folder_path, 'Install.py')}\" -dm")
            win32api.RegSetValueEx(registry_key, "DisplayName", 0, win32con.REG_SZ, obName0())
            win32api.RegSetValueEx(registry_key, "DisplayVersion", 0, win32con.REG_SZ, cf.current_version["version"])
            win32api.RegSetValueEx(registry_key, "DisplayIcon", 0, win32con.REG_SZ, os.path.join(bootstrap_folder_path, "Images", "AppIcon.ico"))
            win32api.RegSetValueEx(registry_key, "HelpLink", 0, win32con.REG_SZ, "https://github.com/efazdev/orangeblox")
            win32api.RegSetValueEx(registry_key, "URLUpdateInfo", 0, win32con.REG_SZ, "https://github.com/efazdev/orangeblox")
            win32api.RegSetValueEx(registry_key, "URLInfoAbout", 0, win32con.REG_SZ, "https://github.com/efazdev/orangeblox")
            win32api.RegSetValueEx(registry_key, "InstallLocation", 0, win32con.REG_SZ, bootstrap_folder_path)
            win32api.RegSetValueEx(registry_key, "Publisher", 0, win32con.REG_SZ, "EfazDev")
            win32api.RegSetValueEx(registry_key, "EstimatedSize", 0, win32con.REG_DWORD, min(getFolderSize(bootstrap_folder_path, formatWithAbbreviation=False) // 1024, 2147483647))
            win32api.RegCloseKey(registry_key)
        except Exception: printErrorMessage(f"Something went wrong setting up registry: \n{trace()}")
    cf.submit_status.submit(ts("OS registration complete."), 100)
    cf.submit_status.end()
def prepareRobloxClientWithErrorCatcher():
    try: prepareRobloxClient()
    except Exception: printErrorMessage(f"There was an error preparing Roblox: \n{trace()}")
def validateRobloxPlayerInstallation():
    if cf.main_os == "Windows":
        target_install_name = cf.main_config.get("EFlagBootstrapRobloxInstallFolderName", "com.roblox.robloxplayer")
        if not os.path.exists(os.path.join(cf.versions_folder, target_install_name)): return False
        for i, v in cf.handler.roblox_bundle_files.items(): 
            if v != "/" and not os.path.exists(os.path.join(cf.versions_folder, target_install_name, v.lstrip('/\\'))): return False
    elif cf.main_os == "Darwin":
        if not os.path.exists(rbx.macOS_dir): return False
        roblox_bundle_folders = ["/content", "/ssl", "/PlatformContent", "/ExtraContent", "/shaders"]
        for i in roblox_bundle_folders: 
            if not os.path.exists(f"{os.path.join(rbx.macOS_dir, 'Contents', 'Resources')}{i}"): return False
    return True
def validateRobloxStudioInstallation():
    if cf.main_os == "Windows":
        target_install_name = cf.main_config.get("EFlagBootstrapRobloxStudioInstallFolderName", "com.roblox.robloxstudio")
        if not os.path.exists(os.path.join(cf.versions_folder, target_install_name)): return False
        for v in ("content", "content\\fonts", "PlatformContent", "StudioContent", "ExtraContent", "shaders", "StudioFonts", "BuiltInStandalonePlugins", "BuiltInPlugins", "ApplicationConfig"): 
            if not os.path.exists(os.path.join(cf.versions_folder, target_install_name, v)): return False
    elif cf.main_os == "Darwin":
        if not os.path.exists(rbx.macOS_studioDir): return False
        roblox_bundle_folders = ["/content", "/PlatformContent", "/StudioContent", "/ExtraContent", "/shaders", "/StudioFonts", "/BuiltInStandalonePlugins", "/BuiltInPlugins", "/ApplicationConfig"]
        for i in roblox_bundle_folders: 
            if not os.path.exists(f"{os.path.join(rbx.macOS_studioDir, 'Contents', 'Resources')}{i}"): return False
    return True
def checkRoblox():
    if cf.run_studio == True and cf.main_config.get("EFlagRobloxStudioEnabled") != True:
        printSystemMessage("--- Roblox Studio Permission ---")
        printMainMessage(f"Roblox Studio with {obName0()} is currently disabled right now! Would you like to enable it or would you want to exit? (y/n)")
        if isYes(input("> ")) == True:
            cf.main_config["EFlagRobloxStudioEnabled"] = True
            saveSettings()
        else: sys.exit(0)
    if cf.run_studio == True:
        # Validate Roblox Studio
        if not validateRobloxStudioInstallation():
            printSystemMessage("--- Installing Roblox Studio to Bootstrap ---")
            printMainMessage(f"Please wait while we install Roblox Studio into {obName0()}!")
            cf.submit_status.start()
            res = cf.handler.installRoblox(studio=True, debug=cf.main_config.get("EFlagEnableDebugMode"))
            cf.submit_status.end()
            if res and res["success"] == False:
                printErrorMessage("There is an issue while trying to install Roblox Studio. Please try again by restarting this app!")
                input("> ")
                sys.exit(0)
            if cf.main_os == "Windows":
                cf.pip_class.copyTreeWithMetadata(os.path.join(cf.cur_path, "_internal"), os.path.join(cf.versions_folder, cf.main_config.get("EFlagBootstrapRobloxStudioInstallFolderName", "com.roblox.robloxstudio"), "_internal"), dirs_exist_ok=True, ignore_if_not_exist=True)
                shutil.copy(os.path.join(cf.cur_path, "OrangeBlox.exe"), os.path.join(cf.versions_folder, cf.main_config.get("EFlagBootstrapRobloxStudioInstallFolderName", "com.roblox.robloxstudio"), "RobloxStudioInstaller.exe"))
                with open(os.path.join(cf.versions_folder, cf.main_config.get("EFlagBootstrapRobloxStudioInstallFolderName", "com.roblox.robloxstudio"), "RobloxStudioBetaPlayRobloxRestart.txt"), "w", encoding="utf-8") as f: f.write(cf.cur_path)
            elif cf.main_os == "Darwin":
                if os.path.exists(os.path.join(cf.macos_app_path, "../", "Play Roblox.app")):
                    cf.pip_class.copyTreeWithMetadata(os.path.join(cf.macos_app_path, "../", "Play Roblox.app"), os.path.join(rbx.macOS_dir, "Contents", "MacOS", "RobloxPlayerInstaller.app"), dirs_exist_ok=True)
                    shutil.copy(os.path.join(cf.macos_app_path, "../", "Play Roblox.app", "Contents", "MacOS", "OrangePlayRoblox"), os.path.join(rbx.macOS_dir, "Contents", "MacOS", "RobloxPlayerInstaller.app", "Contents", "MacOS", "RobloxPlayerInstaller"))
                    with open(os.path.join(rbx.macOS_dir, "Contents", "MacOS", "RobloxPlayerInstaller.app", "Contents", "Resources", "RobloxPlayerBetaPlayRobloxRestart"), "w", encoding="utf-8") as f: f.write(cf.cur_path)
                    createMacOSCodesign(os.path.join(rbx.macOS_dir, "Contents", "MacOS", "RobloxPlayerInstaller.app"), cf.main_config.get("EFlagRobloxCodesigningName", "-"))
                if os.path.exists(os.path.join(cf.macos_app_path, "../", "Run Studio.app")):
                    cf.pip_class.copyTreeWithMetadata(os.path.join(cf.macos_app_path, "../", "Run Studio.app"), os.path.join(rbx.macOS_studioDir, "Contents", "MacOS", "RobloxStudioInstaller.app"), dirs_exist_ok=True)
                    shutil.copy(os.path.join(cf.macos_app_path, "../", "Run Studio.app", "Contents", "MacOS", "OrangeRunStudio"), os.path.join(rbx.macOS_studioDir, "Contents", "MacOS", "RobloxStudioInstaller.app", "Contents", "MacOS", "RobloxStudioInstaller"))
                    with open(os.path.join(rbx.macOS_studioDir, "Contents", "MacOS", "RobloxStudioInstaller.app", "Contents", "Resources", "RobloxStudioBetaPlayRobloxRestart"), "w", encoding="utf-8") as f: f.write(cf.cur_path)
                    createMacOSCodesign(os.path.join(rbx.macOS_studioDir, "Contents", "MacOS", "RobloxStudioInstaller.app"), cf.main_config.get("EFlagRobloxCodesigningName", "-"))
        
        # Check for Updates
        if cf.connect_instead != True and cf.main_config.get("EFlagDisableRobloxUpdateChecks") != True:
            waitForInternet()
            printSystemMessage("--- Checking for Roblox Studio Updates ---")
            current_roblox_version = cf.handler.getCurrentClientVersion(studio=True)
            if current_roblox_version["success"] == True:
                url_channel = None
                try:
                    if len(cf.given_args) > 1:
                        if cf.main_os == "Darwin":
                            url_str = unquote(cf.given_args[1])
                            if url_str: url = unquote(url_str)
                            else: url = ""
                        elif cf.main_os == "Windows": url = cf.given_args[1]
                        if "-channel " in url:
                            s = url.split(" ")
                            url_channel = s[s.index("-channel") + 1]
                            cf.given_args = ["Main.py", "orangeblox://run-studio"]
                        elif "-RobloxChannel " in url:
                            s = url.split(" ")
                            url_channel = s[s.index("-RobloxChannel") + 1]
                            cf.given_args = ["Main.py", "orangeblox://run-studio"]
                        elif url.startswith("roblox-studio"):
                            url_data = cf.handler.parseRobloxLauncherURL(url=url)
                            if url_data and url_data.get("channel"): url_channel = url_data.get("channel")
                    if cf.main_config.get("EFlagRobloxSecurityCookieUsage") == True and (not url_channel or url_channel == "LIVE"):
                        requesting_channel = cf.handler.getUserChannel(studio=cf.run_studio, debug=(cf.main_config.get("EFlagEnableDebugMode") == True))
                        if requesting_channel.get("success") == True and requesting_channel.get("channel_name") != "LIVE":
                            url_channel = requesting_channel.get("channel_name")
                            if requesting_channel.get("token"): cf.main_config["EFlagRobloxChannelUpdateToken"] = requesting_channel.get("token")
                    elif cf.main_config.get("EFlagRobloxSecurityCookieUsage") != True and cf.main_config.get("EFlagRobloxChannelUpdateToken"):
                        cf.main_config.pop("EFlagRobloxChannelUpdateToken")
                    if url_channel:
                        printDebugMessage(f"Setting Channel Based on URL: {url_channel}")
                        if url_channel == "production" or url_channel == "LIVE": url_channel = ""; current_roblox_version["channel"] = "LIVE"
                        else: current_roblox_version["channel"] = url_channel
                        if cf.main_os == "Darwin":
                            res = cf.plist_class.writePListFile(os.path.join(cf.user_folder, "Library", "Preferences", "com.roblox.RobloxStudioChannel.plist"), {"www.roblox.com": url_channel}, binary=True, ns_mode=True)
                            printDebugMessage(f"Channel Set Result: {res}")
                        elif cf.main_os == "Windows":
                            try: registry_key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, r"Software\ROBLOX Corporation\Environments\RobloxStudio\Channel", 0, win32con.KEY_SET_VALUE)
                            except Exception: registry_key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, r"Software\ROBLOX Corporation\Environments\RobloxStudio\Channel")
                            win32api.RegSetValueEx(registry_key, "www.roblox.com", 0, win32con.REG_SZ, url_channel)
                            win32api.RegCloseKey(registry_key)
                except Exception: printDebugMessage(f"Unable to find channel from URL. Exception: \n{trace()}")
                latest_roblox_version = cf.handler.getLatestClientVersion(studio=True, debug=(cf.main_config.get("EFlagEnableDebugMode") == True), channel=url_channel if url_channel else cf.main_config.get("EFlagRobloxStudioClientChannel", current_roblox_version.get("channel", "LIVE")), token=cf.main_config.get("EFlagRobloxChannelUpdateToken"))
                if latest_roblox_version["success"] == True:
                    download_channel = latest_roblox_version["attempted_channel"]
                    if current_roblox_version["client_version"] == latest_roblox_version["client_version"]: printMainMessage("Running latest version of Roblox Studio!")
                    else:
                        printSuccessMessage(f"A new version of Roblox Studio is available! Versions: {current_roblox_version['version']} => {latest_roblox_version['hash']}")
                        printSystemMessage("--- Installing Latest Roblox Studio Version ---")
                        printMainMessage(f"Please wait while we install a newer version of Roblox Studio into {obName0()}!")
                        cf.submit_status.start()
                        res = cf.handler.installRoblox(studio=True, debug=(cf.main_config.get("EFlagEnableDebugMode") == True), downloadChannel=download_channel, downloadToken=cf.main_config.get("EFlagRobloxChannelUpdateToken"))
                        cf.submit_status.end()
                        if res and res["success"] == False:
                            printErrorMessage("There is an issue while trying to install Roblox Studio. Please try again by restarting this app!")
                            input("> ")
                            sys.exit(0)
                        if cf.main_os == "Darwin":
                            while not os.path.exists(rbx.macOS_studioDir): time.sleep(0.1)
                        new_latest_roblox_version = cf.handler.getCurrentClientVersion(studio=True)
                        printSuccessMessage(f"Successfully updated Roblox Studio to {new_latest_roblox_version.get('version')}!")
                        cf.installed_update = True
                        cf.skip_modification_mode = False
                    if download_channel != (url_channel if url_channel else cf.main_config.get("EFlagRobloxStudioClientChannel", current_roblox_version.get("channel", "LIVE"))):
                        printDebugMessage(f"Setting Channel Based on Channel Difference: {download_channel}")
                        if download_channel == "production" or download_channel == "LIVE": download_channel = ""
                        if cf.main_os == "Darwin":
                            res = cf.plist_class.writePListFile(os.path.join(cf.user_folder, "Library", "Preferences", "com.roblox.RobloxStudioChannel.plist"), {"www.roblox.com": download_channel}, binary=True, ns_mode=True)
                            printDebugMessage(f"Channel Set Result: {res}")
                        elif cf.main_os == "Windows":
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
        player_can_be_used = validateRobloxPlayerInstallation()
        # Check for Updates
        if cf.main_config.get("EFlagDisableRobloxUpdateChecks") != True:
            waitForInternet()
            printSystemMessage("--- Checking for Roblox Updates ---")
            current_roblox_version = cf.handler.getCurrentClientVersion()
            if (cf.main_config.get("EFlagFreshCopyRoblox") == True and cf.skip_modification_mode != True) or player_can_be_used == False:
                url_channel = None
                try:
                    if len(cf.given_args) > 1:
                        if cf.main_os == "Darwin":
                            url_str = unquote(cf.given_args[1])
                            if url_str: url = unquote(url_str)
                            else: url = ""
                        elif cf.main_os == "Windows": url = cf.given_args[1]
                        if "-channel " in url:
                            s = url.split(" ")
                            url_channel = s[s.index("-channel") + 1]
                            cf.given_args = ["Main.py", "orangeblox://continue"]
                        elif "-RobloxChannel " in url:
                            s = url.split(" ")
                            url_channel = s[s.index("-RobloxChannel") + 1]
                            cf.given_args = ["Main.py", "orangeblox://continue"]
                        elif url.startswith("roblox-player:"):
                            url_data = cf.handler.parseRobloxLauncherURL(url=url)
                            if url_data and url_data.get("channel"): url_channel = url_data.get("channel")
                    if cf.main_config.get("EFlagRobloxSecurityCookieUsage") == True and (not url_channel or url_channel == "LIVE"):
                        requesting_channel = cf.handler.getUserChannel(studio=cf.run_studio, debug=(cf.main_config.get("EFlagEnableDebugMode") == True))
                        if requesting_channel.get("success") == True and requesting_channel.get("channel_name") != "LIVE":
                            url_channel = requesting_channel.get("channel_name")
                            if requesting_channel.get("token"): cf.main_config["EFlagRobloxChannelUpdateToken"] = requesting_channel.get("token")
                    elif cf.main_config.get("EFlagRobloxSecurityCookieUsage") != True and cf.main_config.get("EFlagRobloxChannelUpdateToken"):
                        cf.main_config.pop("EFlagRobloxChannelUpdateToken")
                    if url_channel:
                        printDebugMessage(f"Setting Channel Based on URL: {url_channel}")
                        if url_channel == "production" or url_channel == "LIVE": url_channel = ""; current_roblox_version["channel"] = "LIVE"
                        else: current_roblox_version["channel"] = url_channel
                        if cf.main_os == "Darwin":
                            res = cf.plist_class.writePListFile(os.path.join(cf.user_folder, "Library", "Preferences", "com.roblox.RobloxPlayerChannel.plist"), {"www.roblox.com": url_channel}, binary=True, ns_mode=True)
                            printDebugMessage(f"Channel Set Result: {res}")
                        elif cf.main_os == "Windows":
                            try: registry_key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, r"Software\ROBLOX Corporation\Environments\RobloxPlayer\Channel", 0, win32con.KEY_SET_VALUE)
                            except Exception: registry_key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, r"Software\ROBLOX Corporation\Environments\RobloxPlayer\Channel")
                            win32api.RegSetValueEx(registry_key, "www.roblox.com", 0, win32con.REG_SZ, url_channel)
                            win32api.RegCloseKey(registry_key)
                except Exception: printDebugMessage(f"Unable to find channel from URL. Exception: \n{trace()}")
                latest_roblox_version = cf.handler.getLatestClientVersion(debug=(cf.main_config.get("EFlagEnableDebugMode") == True), channel=url_channel if url_channel else cf.main_config.get("EFlagRobloxClientChannel", current_roblox_version.get("channel", "LIVE")), token=cf.main_config.get("EFlagRobloxChannelUpdateToken"))
                if latest_roblox_version["success"] == True:
                    download_channel = latest_roblox_version["attempted_channel"]
                    if cf.main_os == "Windows":
                        printMainMessage(f"Fresh copy was enabled! Therefore, starting Roblox install!")
                        printSystemMessage("--- Installing Latest Roblox Version ---")
                        cf.submit_status.start()
                        res = cf.handler.installRoblox(forceQuit=True, debug=(cf.main_config.get("EFlagEnableDebugMode") == True), downloadChannel=download_channel, downloadToken=cf.main_config.get("EFlagRobloxChannelUpdateToken"), verifyInstall=cf.main_config.get("EFlagVerifyRobloxHashAfterInstall")!=False)
                        cf.submit_status.end()
                        if res and res["success"] == False:
                            printErrorMessage("There is an issue while trying to install Roblox. Please try again by restarting this app!")
                            input("> ")
                            sys.exit(0)
                        cf.installed_update = True
                        time.sleep(3)
                    else:
                        printMainMessage(f"Fresh copy was enabled! Therefore, starting Roblox install!")
                        printSystemMessage("--- Installing Latest Roblox Version ---")
                        cf.submit_status.start()
                        res = cf.handler.installRoblox(forceQuit=False, debug=(cf.main_config.get("EFlagEnableDebugMode") == True), downloadChannel=download_channel, downloadToken=cf.main_config.get("EFlagRobloxChannelUpdateToken"), verifyInstall=cf.main_config.get("EFlagVerifyRobloxHashAfterInstall")!=False)
                        cf.submit_status.end()
                        if res and res["success"] == False:
                            printErrorMessage("There is an issue while trying to install Roblox. Please try again by restarting this app!")
                            input("> ")
                            sys.exit(0)
                        cf.installed_update = True
                        time.sleep(3)
                else: printErrorMessage("There was an issue while checking for updates.")
            elif current_roblox_version["success"] == True:
                url_channel = None
                try:
                    if len(cf.given_args) > 1:
                        if cf.main_os == "Darwin":
                            url_str = unquote(cf.given_args[1])
                            if url_str: url = unquote(url_str)
                            else: url = ""
                        elif cf.main_os == "Windows": url = cf.given_args[1]
                        if "-channel " in url:
                            s = url.split(" ")
                            url_channel = s[s.index("-channel") + 1]
                            cf.given_args = ["Main.py", "orangeblox://continue"]
                        elif "-RobloxChannel " in url:
                            s = url.split(" ")
                            url_channel = s[s.index("-RobloxChannel") + 1]
                            cf.given_args = ["Main.py", "orangeblox://continue"]
                        elif url.startswith("roblox-player:"):
                            url_data = cf.handler.parseRobloxLauncherURL(url=url)
                            if url_data and url_data.get("channel"): url_channel = url_data.get("channel")
                    if cf.main_config.get("EFlagRobloxSecurityCookieUsage") == True and (not url_channel or url_channel == "LIVE"):
                        requesting_channel = cf.handler.getUserChannel(studio=cf.run_studio, debug=(cf.main_config.get("EFlagEnableDebugMode") == True))
                        if requesting_channel.get("success") == True and requesting_channel.get("channel_name") != "LIVE":
                            url_channel = requesting_channel.get("channel_name")
                            if requesting_channel.get("token"): cf.main_config["EFlagRobloxChannelUpdateToken"] = requesting_channel.get("token")
                    elif cf.main_config.get("EFlagRobloxSecurityCookieUsage") != True and cf.main_config.get("EFlagRobloxChannelUpdateToken"):
                        cf.main_config.pop("EFlagRobloxChannelUpdateToken")
                    if url_channel:
                        printDebugMessage(f"Setting Channel Based on URL: {url_channel}")
                        if url_channel == "production" or url_channel == "LIVE": url_channel = ""; current_roblox_version["channel"] = "LIVE"
                        else: current_roblox_version["channel"] = url_channel
                        if cf.main_os == "Darwin":
                            res = cf.plist_class.writePListFile(os.path.join(cf.user_folder, "Library", "Preferences", "com.roblox.RobloxPlayerChannel.plist"), {"www.roblox.com": url_channel}, binary=True, ns_mode=True)
                            printDebugMessage(f"Channel Set Result: {res}")
                        elif cf.main_os == "Windows":
                            try: registry_key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, r"Software\ROBLOX Corporation\Environments\RobloxPlayer\Channel", 0, win32con.KEY_SET_VALUE)
                            except Exception: registry_key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, r"Software\ROBLOX Corporation\Environments\RobloxPlayer\Channel")
                            win32api.RegSetValueEx(registry_key, "www.roblox.com", 0, win32con.REG_SZ, url_channel)
                            win32api.RegCloseKey(registry_key)
                except Exception: printDebugMessage(f"Unable to find channel from URL. Exception: \n{trace()}")
                latest_roblox_version = cf.handler.getLatestClientVersion(debug=(cf.main_config.get("EFlagEnableDebugMode") == True), channel=url_channel if url_channel else cf.main_config.get("EFlagRobloxClientChannel", current_roblox_version.get("channel", "LIVE")), token=cf.main_config.get("EFlagRobloxChannelUpdateToken"))
                if latest_roblox_version["success"] == True:
                    download_channel = latest_roblox_version["attempted_channel"]
                    if current_roblox_version["client_version"] == latest_roblox_version["client_version"]: printMainMessage("Running latest version of Roblox!")
                    else:
                        printSuccessMessage(f"A new version of Roblox is available! Versions: {current_roblox_version['version']} => {latest_roblox_version['hash']}")
                        printSystemMessage("--- Installing Latest Roblox Version ---")
                        printMainMessage(f"Please wait while we install a newer version of Roblox into {obName0()}!")
                        cf.submit_status.start()
                        res = cf.handler.installRoblox(debug=(cf.main_config.get("EFlagEnableDebugMode") == True), downloadChannel=download_channel, downloadToken=cf.main_config.get("EFlagRobloxChannelUpdateToken"))
                        cf.submit_status.end()
                        if res and res["success"] == False:
                            printErrorMessage("There is an issue while trying to install Roblox. Please try again by restarting this app!")
                            input("> ")
                            sys.exit(0)
                        if cf.main_os == "Darwin":
                            while not os.path.exists(rbx.macOS_dir): time.sleep(0.1)
                        new_latest_roblox_version = cf.handler.getCurrentClientVersion()
                        printSuccessMessage(f"Successfully updated Roblox to {new_latest_roblox_version.get('version')}!")
                        cf.installed_update = True
                        cf.skip_modification_mode = False
                    if download_channel != (url_channel if url_channel else cf.main_config.get("EFlagRobloxClientChannel", current_roblox_version.get("channel", "LIVE"))):
                        printDebugMessage(f"Setting Channel Based on Channel Difference: {download_channel}")
                        if download_channel == "production" or download_channel == "LIVE": download_channel = ""
                        if cf.main_os == "Darwin":
                            res = cf.plist_class.writePListFile(os.path.join(cf.user_folder, "Library", "Preferences", "com.roblox.RobloxPlayerChannel.plist"), {"www.roblox.com": download_channel}, binary=True, ns_mode=True)
                            printDebugMessage(f"Channel Set Result: {res}")
                        elif cf.main_os == "Windows":
                            try: registry_key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, r"Software\ROBLOX Corporation\Environments\RobloxPlayer\Channel", 0, win32con.KEY_SET_VALUE)
                            except Exception: registry_key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, r"Software\ROBLOX Corporation\Environments\RobloxPlayer\Channel")
                            win32api.RegSetValueEx(registry_key, "www.roblox.com", 0, win32con.REG_SZ, download_channel)
                            win32api.RegCloseKey(registry_key)
                else:
                    printErrorMessage("There was an issue while checking for updates.")
                    printDebugMessage(latest_roblox_version)
            else: printErrorMessage("There was an issue while checking for updates.")
def getStartData():
    config_key = "EFlagRobloxStudioArguments" if cf.run_studio else "EFlagRobloxPlayerArguments"
    user_args_str = cf.main_config.get(config_key, "")
    user_args = shlex.split(user_args_str) if user_args_str else []
    url = cf.given_args[1] if len(cf.given_args) > 1 else None
    if not url or url.startswith("efaz-bootstrap:") or url.startswith("orangeblox:"):
        if cf.main_os == "Darwin" and user_args: return ["--args"] + user_args
        return user_args
    if cf.run_studio:
        if cf.main_os == "Windows": return [url] + user_args
        else: return ["--args", url] + user_args
    else:
        if url.startswith("-"):
            if cf.main_os == "Darwin": return ["--args", url] + user_args
            return [url] + user_args
        else:
            if cf.main_os == "Darwin" and user_args: return [url, "--args"] + user_args
            return [url] + user_args
def runRobloxClient():
    rcf.roblox_launched_affect_mod_script = True
    def connectCallEvents(cri):
        if type(cri) is cf.handler.RobloxInstance:
            if cf.run_studio == True:
                cri.addRobloxEventCallback("onOpeningGame", onOpeningGameStudio)
                cri.addRobloxEventCallback("onRobloxExit", onRobloxExit)
                cri.addRobloxEventCallback("onPlayTestStart", onPlayTestStartStudio)
                cri.addRobloxEventCallback("onGameJoined", onGameJoinedStudio)
                cri.addRobloxEventCallback("onClosingGame", onClosingGameStudio)
                cri.addRobloxEventCallback("onRobloxAppStart", onRobloxAppStart)
                cri.addRobloxEventCallback("onGameLoaded", onGameLoadedStudio)
                cri.addRobloxEventCallback("onLostConnection", onLostConnectionStudio)
                cri.addRobloxEventCallback("onStudioInstallerLaunched", onStudioInstallerLaunchedStudio)
                cri.addRobloxEventCallback("onRobloxCrash", onRobloxCrash)
                cri.addRobloxEventCallback("onRobloxLog", onAllRobloxEvents)
                cri.setRobloxEventCallback("onRobloxChannel", onRobloxChannel)
                cri.addRobloxEventCallback("onPlayTestDisconnected", onPlayTestDisconnectedStudio)
                cri.addRobloxEventCallback("onRobloxPublishing", onRobloxPublishingStudio)
                cri.addRobloxEventCallback("onRobloxSaved", onRobloxSavingStudio)
                cri.addRobloxEventCallback("onTeamCreateDisconnect", onTeamCreateDisconnectStudio)
                cri.addRobloxEventCallback("onTeamCreateConnect", onTeamCreateConnectStudio)
                cri.addRobloxEventCallback("onBloxstrapSDK", onBloxstrapMessage)
                if cf.main_config.get("EFlagDisableAutoOpenOrangeBloxFromStudio") != True: cri.addRobloxEventCallback("onNewStudioLaunching", onNewRobloxStudio)
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
    if cf.main_config.get("EFlagEnableEndingRobloxCrashHandler") == True: cf.handler.endRobloxCrashHandler()
    if cf.run_studio == True:
        if cf.connect_instead == True:
            rcf.connected_roblox_instance = cf.handler.RobloxInstance(cf.handler, cf.handler.getLatestOpenedRobloxPid(studio=True), debug_mode=(cf.main_config.get("EFlagEnableDebugMode") == True), allow_other_logs=(cf.main_config.get("EFlagAllowFullDebugMode") == True), created_mutex=False, studio=True, await_log_creation=False)
            if rcf.connected_roblox_instance:
                connectCallEvents(rcf.connected_roblox_instance)
                printSuccessMessage("Connected to Roblox Instance from log file for Activity Tracking!")
                if rcf.connected_roblox_instance.created_mutex == True and cf.main_os == "Windows": printSuccessMessage("Successfully connected for multi-instancing! Please know that this effect is active until all Roblox windows are closed or this bootstrap window is closed.")
            else: printDebugMessage("No RobloxInstance class was registered")
            cf.roblox_launched = True
        elif len(cf.given_args) > 1:
            url = cf.given_args[1]
            if not url.strip(): url = "roblox-studio://"
            if url:
                for i, v in cf.custom_cookies.items():
                    if os.path.exists(v): shutil.copy(v, i, follow_symlinks=False)
                if url.startswith("efaz-bootstrap:") or url.startswith("orangeblox:"):
                    rcf.connected_roblox_instance = cf.handler.openRoblox(
                        studio=True,
                        debug=(cf.main_config.get("EFlagEnableDebugMode") == True), 
                        startData=getStartData(),
                        attachInstance=cf.main_config.get("EFlagAllowActivityTracking") != False, 
                        allowRobloxOtherLogDebug=(cf.main_config.get("EFlagAllowFullDebugMode") == True)
                    )
                else:
                    if cf.main_os == "Windows" and "'" in url and os.path.exists(url): url = f"\"{url}\""
                    rcf.connected_roblox_instance = cf.handler.openRoblox(
                        studio=True,
                        debug=(cf.main_config.get("EFlagEnableDebugMode") == True), 
                        startData=getStartData(),
                        attachInstance=False if url.startswith("roblox-studio-auth:") else (cf.main_config.get("EFlagAllowActivityTracking") != False), 
                        allowRobloxOtherLogDebug=(cf.main_config.get("EFlagAllowFullDebugMode") == True)
                    )
                if rcf.connected_roblox_instance:
                    connectCallEvents(rcf.connected_roblox_instance)
                    printSuccessMessage("Connected to Roblox Instance from log file for Activity Tracking!")
                    if rcf.connected_roblox_instance.created_mutex == True and cf.main_os == "Windows": printSuccessMessage("Successfully connected for multi-instancing! Please know that this effect is active until all Roblox windows are closed or this bootstrap window is closed.")
                else: printDebugMessage("No RobloxInstance class was registered")
                cf.roblox_launched = True
                if not cf.main_config.get("EFlagDisableRobloxReinstallNeededChecks"): cf.pip_class.startThread(func=checkIfUpdateWasNeeded)
            else: printDebugMessage(f"Unable to format url scheme due to an issue.")
        else:
            for i, v in cf.custom_cookies.items():
                if os.path.exists(v): shutil.copy(v, i, follow_symlinks=False)
            rcf.connected_roblox_instance = cf.handler.openRoblox(
                studio=True,
                debug=(cf.main_config.get("EFlagEnableDebugMode") == True), 
                startData=getStartData(),
                attachInstance=cf.main_config.get("EFlagAllowActivityTracking") != False, 
                allowRobloxOtherLogDebug=(cf.main_config.get("EFlagAllowFullDebugMode") == True)
            )
            if rcf.connected_roblox_instance:
                connectCallEvents(rcf.connected_roblox_instance)
                printSuccessMessage("Connected to Roblox Instance from log file for Activity Tracking!")
            else: printDebugMessage("No RobloxInstance class was registered")
            cf.roblox_launched = True
    else:
        if cf.connect_instead == True:
            rcf.connected_roblox_instance = cf.handler.RobloxInstance(cf.handler, cf.handler.getLatestOpenedRobloxPid(), debug_mode=(cf.main_config.get("EFlagEnableDebugMode") == True), allow_other_logs=(cf.main_config.get("EFlagAllowFullDebugMode") == True), created_mutex=False, studio=False, await_log_creation=False)
            if rcf.connected_roblox_instance:
                connectCallEvents(rcf.connected_roblox_instance)
                printSuccessMessage("Connected to Roblox Instance from log file for Activity Tracking!")
                if rcf.connected_roblox_instance.created_mutex == True and cf.main_os == "Windows": printSuccessMessage("Successfully connected for multi-instancing! Please know that this effect is active until all Roblox windows are closed or this bootstrap window is closed.")
            else: printDebugMessage("No RobloxInstance class was registered")
            cf.roblox_launched = True
        elif len(cf.given_args) > 1:
            url = cf.given_args[1]
            if not url.strip(): url = "roblox://"
            if url:
                for i, v in cf.custom_cookies.items():
                    if os.path.exists(v): shutil.copy(v, i, follow_symlinks=False)
                if url.startswith("efaz-bootstrap:") or url.startswith("orangeblox:"):
                    rcf.connected_roblox_instance = cf.handler.openRoblox(
                        forceQuit=False, 
                        debug=(cf.main_config.get("EFlagEnableDebugMode") == True), 
                        startData=getStartData(),
                        attachInstance=cf.main_config.get("EFlagAllowActivityTracking") != False, 
                        allowRobloxOtherLogDebug=(cf.main_config.get("EFlagAllowFullDebugMode") == True)
                    )
                elif url.startswith("-"):
                    rcf.connected_roblox_instance = cf.handler.openRoblox(
                        forceQuit=False, 
                        debug=(cf.main_config.get("EFlagEnableDebugMode") == True),
                        startData=getStartData(),
                        attachInstance=cf.main_config.get("EFlagAllowActivityTracking") != False, 
                        allowRobloxOtherLogDebug=(cf.main_config.get("EFlagAllowFullDebugMode") == True)
                    )
                else:
                    if cf.main_os == "Windows" and "'" in url and os.path.exists(url): url = f"\"{url}\""
                    rcf.connected_roblox_instance = cf.handler.openRoblox(
                        forceQuit=cf.preserve_roblox == False, 
                        debug=(cf.main_config.get("EFlagEnableDebugMode") == True),
                        startData=getStartData(),
                        attachInstance=cf.main_config.get("EFlagAllowActivityTracking") != False, 
                        allowRobloxOtherLogDebug=(cf.main_config.get("EFlagAllowFullDebugMode") == True)
                    )
                if rcf.connected_roblox_instance:
                    connectCallEvents(rcf.connected_roblox_instance)
                    printSuccessMessage("Connected to Roblox Instance from log file for Activity Tracking!")
                    if rcf.connected_roblox_instance.created_mutex == True and cf.main_os == "Windows": printSuccessMessage("Successfully connected for multi-instancing! Please know that this effect is active until all Roblox windows are closed or this bootstrap window is closed.")
                else: printDebugMessage("No RobloxInstance class was registered")
                cf.roblox_launched = True
                if not cf.main_config.get("EFlagDisableRobloxReinstallNeededChecks"): cf.pip_class.startThread(func=checkIfUpdateWasNeeded)
            else: printDebugMessage(f"Unable to format url scheme due to an issue.")
        else:
            #if cf.handler.getIfRobloxIsOpen():
            #    printMainMessage("An existing Roblox Window is currently open. Would you like to restart it in order for changes to take effect? (y/n)")
            #    c = input("> ")
            #    if isYes(c) == True: cf.handler.endRoblox()
            #        else: sys.exit(0)
            for i, v in cf.custom_cookies.items():
                if os.path.exists(v): shutil.copy(v, i, follow_symlinks=False)
            rcf.connected_roblox_instance = cf.handler.openRoblox(
                forceQuit=True, 
                startData=f"{'--args ' if cf.main_os == 'Darwin' and cf.main_config.get('EFlagRobloxPlayerArguments', '') != '' else ''}{cf.main_config.get('EFlagRobloxPlayerArguments', '')}",
                debug=(cf.main_config.get("EFlagEnableDebugMode") == True), 
                attachInstance=cf.main_config.get("EFlagAllowActivityTracking") != False, 
                allowRobloxOtherLogDebug=(cf.main_config.get("EFlagAllowFullDebugMode") == True)
            )
            if rcf.connected_roblox_instance:
                connectCallEvents(rcf.connected_roblox_instance)
                printSuccessMessage("Connected to Roblox Instance from log file for Activity Tracking!")
            else: printDebugMessage("No RobloxInstance class was registered")
            cf.roblox_launched = True
            if not cf.main_config.get("EFlagDisableRobloxReinstallNeededChecks"): cf.pip_class.startThread(func=checkIfUpdateWasNeeded)
def restartRoblox(request_thread_close: bool=True):
    rcf.current_place_info = None
    if rcf.connected_roblox_instance and request_thread_close: rcf.connected_roblox_instance.requestThreadClosing()
    runRobloxClient()
def checkIfUpdateWasNeeded():
    rcf.updated_count += 1
    if rcf.updated_count < 3:
        printMainMessage("Waiting 5 seconds to check if Roblox needs a reinstall..")
        time.sleep(5)
        if not (cf.handler.getIfRobloxIsOpen(studio=cf.run_studio)):
            printMainMessage(f"Uh oh! An fresh reinstall is needed. Downloading a fresh copy of Roblox{' Studio' if cf.run_studio == True else ''}!")
            cf.submit_status.start()
            if cf.run_studio == True: res = cf.handler.installRoblox(studio=True, debug=(cf.main_config.get("EFlagEnableDebugMode") == True), downloadToken=createDownloadToken(), verifyInstall=cf.main_config.get("EFlagVerifyRobloxHashAfterInstall")!=False)
            else: res = cf.handler.installRoblox(forceQuit=True, debug=(cf.main_config.get("EFlagEnableDebugMode") == True), downloadToken=createDownloadToken(), verifyInstall=cf.main_config.get("EFlagVerifyRobloxHashAfterInstall")!=False)
            cf.submit_status.end()
            if res and res["success"] == False:
                printErrorMessage(f"There is an issue while trying to install Roblox{' Studio' if cf.run_studio == True else ''}. Please try again by restarting this app!")
                input("> ")
                sys.exit(0)
            time.sleep(5)
            cf.skip_modification_mode = False
            cf.installed_update = True
            prepareRobloxClientWithErrorCatcher()
            printSuccessMessage(f"Done! Roblox{' Studio' if cf.run_studio == True else ''} is ready!")
            time.sleep(2)
            printSystemMessage(f"--- Running Roblox{' Studio' if cf.run_studio == True else ''} ---")
            runRobloxClient()
        else: printSuccessMessage(f"Roblox{' Studio' if cf.run_studio == True else ''} doesn't require any updates!")
    else: printErrorMessage(f"Is {'Roblox Studio' if cf.run_studio == True else 'Roblox Player'} crashing instantly..? Well, ending script here.")
def runRoblox():
    try:
        global rcf

        # Check for Permissions
        checkRoblox()

        # Prepare Roblox
        if cf.main_config.get("EFlagEnableSkipModificationMode") == True and cf.main_os == "Darwin" and cf.handler.getIfRobloxIsOpen(studio=cf.run_studio): cf.skip_modification_mode = True
        if cf.skip_modification_mode == False: prepareRobloxClientWithErrorCatcher()
        else: cf.pip_class.startThread(func=prepareRobloxClientWithErrorCatcher, daemon=True)

        # Prepare Client Data and Mod Scripts
        rcf = RobloxClientData()
        if cf.main_config.get("EFlagDisableModScriptsAccess", False) != True:
            from Modules.modscripts import loadModScripts 
            mod_script_thread = cf.pip_class.startThread(func=loadModScripts, daemon=True)
            if cf.skip_modification_mode == False: mod_script_thread.join()
        if cf.main_config.get("EFlagRobloxUnfriendCheckEnabled") == True: cf.pip_class.startThread(func=unfriendCheckLoop, daemon=True)
        if cf.main_config.get("EFlagReplaceRobloxRuntimeIconWithModIcon") == True and cf.main_os == "Windows": cf.pip_class.startThread(func=setRuntimeIconLoop, daemon=True)

        # Roblox Ready Message
        if cf.run_studio == True:
            printSuccessMessage("Done! Roblox Studio is ready!")
            printSystemMessage("--- Running Roblox Studio ---")
        else:
            printSuccessMessage("Done! Roblox is ready!")
            printSystemMessage("--- Running Roblox ---")
        if waitForInternet() == True: printSystemMessage("-----------")
        
        # Launch Roblox Client
        runRobloxClient()
        
        # End Script
        sys.exit(0)
    except (KeyboardInterrupt, Exception) as e:
        printErrorMessage("Uh oh! A Python exception that causes the script to end has occurred!")
        printErrorMessage(f"Exception: \n{trace()}")
        printErrorMessage(f"Location Code: 3")
        input("> ")
        sys.exit(0 if cf.main_os == "Darwin" else 1)
def unfriendCheckLoop():
    alleged_path = generateFileKey("UnfriendCheckLoopLock")
    loop_lock = PyKits.Lock(alleged_path)
    with loop_lock:
        printDebugMessage("Starting Unfriend Detector Loop..")
        while True:
            unfriended_friends = []
            blank_user_ids = 0
            friend_check_id = cf.main_config.get('EFlagRobloxUnfriendCheckUserID', 1)
            try:
                reached_end = False
                friend_list_json = {"data": []}
                query = {"limit": "50", "findFriendsType": "0"}
                while reached_end == False:
                    try:
                        if cf.main_config.get("EFlagUseEfazDevAPI") == True: 
                            if query.get("limit"): query.pop("limit")
                            if query.get("findFriendsType"): query.pop("findFriendsType")
                            friend_list_req = cf.requests.get(f"https://api.efaz.dev/api/roblox/user-friends-find/{friend_check_id}/50" + cf.requests.format_params(query), timeout=5)
                            if friend_list_req and friend_list_req.json: friend_list_req.json = friend_list_req.json.get("response")
                        else: friend_list_req = cf.requests.get(f"https://friends.roblox.com/v1/users/{friend_check_id}/friends/find" + cf.requests.format_params(query), timeout=5, cookies=createCookieHeader())
                        friend_req_json = friend_list_req.json
                        if friend_list_req.ok and friend_req_json.get("PageItems"):
                            friend_list_json["data"] += friend_req_json.get("PageItems")
                            if friend_req_json.get("NextCursor"): query["cursor"] = friend_req_json.get("NextCursor")
                            else: reached_end = True
                    except Exception as e: printDebugMessage(f"There was an error on getting friends! Error: {str(e)}")
                    time.sleep(5)
                if friend_list_req.ok:
                    last_pinged_friend_list = {}
                    if os.path.exists(os.path.join(generateFileKey("CachedFriendsList", ext=".json"))):
                        with open(os.path.join(generateFileKey("CachedFriendsList", ext=".json")), "r", encoding="utf-8") as f: last_pinged_friend_list = json.load(f)
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
                                    if i.get("id") != -1: user_ids.append(i.get("id"))
                                    else: blank_user_ids += 1
                                if len(user_ids) > 150:
                                    chunked = []
                                    for e in range(0, len(user_ids), 150): chunked.append(user_ids[e:e + 150])
                                    unfriended_friends = []
                                    for e in chunked:
                                        reached_end3 = False
                                        while reached_end3 == False:
                                            user_info_req = cf.requests.post(f"https://users.roblox.com/v1/users", {"userIds": e, "excludeBannedUsers": False}, timeout=5, cookies=createCookieHeader())
                                            if user_info_req.ok: unfriended_friends += user_info_req.json.get("data"); reached_end3 = True
                                            time.sleep(1)
                                    reached_end2 = True
                                else:
                                    user_info_req = cf.requests.post(f"https://users.roblox.com/v1/users", {"userIds": user_ids, "excludeBannedUsers": False}, timeout=5, cookies=createCookieHeader())
                                    if user_info_req.ok: unfriended_friends = user_info_req.json.get("data"); reached_end2 = True
                                    time.sleep(1)
                            except Exception: pass
                        last_pinged_friend_list[str(friend_check_id)] = friend_list_json.get("data")
                    else: last_pinged_friend_list[str(friend_check_id)] = friend_list_json.get("data")
                    with open(os.path.join(generateFileKey("CachedFriendsList", ext=".json")), "w", encoding="utf-8") as f: json.dump(last_pinged_friend_list, f, indent=4)
            except Exception:
                printDebugMessage(f"Unable to fetch friends list! Exception: \n{trace()}")
                unfriended_friends = []
            if len(unfriended_friends) > 0:
                for i in unfriended_friends:
                    if rcf.roblox_launched_affect_mod_script == True: displayNotification(ts("Unfriend Detected!"), ts(f"Oh! @{i['name']} has unfriended you! ;("))
                    else: displayNotification(ts("Unfriend Detected!"), ts(f"Oh! @{i['name']} has unfriended you while you were away! ;("))
                    printDebugMessage(f"Unable to find friend @{i['name']} in list! User must be unfriended!")
                    time.sleep(1)
            time.sleep(cf.main_config.get("EFlagRobloxUnfriendCheckCooldown", 600))
def setRuntimeIconLoop():
    while True:
        try:
            if cf.run_studio == True: 
                if cf.main_config.get("EFlagEnableChangeBrandIcons") == True: brand_fold = os.path.join(cf.mods_folder, "RobloxStudioBrand", cf.main_config.get('EFlagSelectedBrandLogo2'))
                else: brand_fold = os.path.join(cf.mods_folder, "RobloxStudioBrand", "Original")
            else:
                if cf.main_config.get("EFlagEnableChangeBrandIcons") == True: brand_fold = os.path.join(cf.mods_folder, "RobloxBrand", cf.main_config.get('EFlagSelectedBrandLogo'))
                else: brand_fold = os.path.join(cf.mods_folder, "RobloxBrand", "Original")
            icon = os.path.join(brand_fold, "AppIcon.ico")
            if rcf.connected_roblox_instance and os.path.exists(icon):
                windows = rcf.connected_roblox_instance.getWindowsOpened()
                if windows:
                    for i in windows: i.setWindowIcon(icon)
        except Exception: printDebugMessage(f"Something went wrong with setting the Roblox Runtime Icon: \n{trace()}")
        time.sleep(3)
def startDiscordRPC(thumbnail_url: str=None):
    need_new_rpc = True
    try: 
        if cf.discord_rpc and cf.discord_rpc.connected == True: need_new_rpc = False
    except Exception: printDebugMessage(f"There was an error checking Discord RPC: \n{trace()}")
    if need_new_rpc == True:
        if (cf.run_studio == False and cf.main_config.get("EFlagEnableDiscordRPC") == True) or (cf.run_studio == True and cf.main_config.get("EFlagEnableDiscordRPCStudio") == True):
            cf.discord_rpc = Presence("1367683523338698863" if cf.run_studio == True else "1297668920349823026")
            cf.discord_rpc.set_debug_mode(cf.main_config.get("EFlagEnableDebugMode") == True)
            cf.discord_rpc.connect()
            if cf.main_config.get("EFlagEnableDefaultDiscordRPC") != False:
                if not thumbnail_url: thumbnail_url = getRobloxThumbnailURL()
                start_time = int(datetime.datetime.now(tz=datetime.UTC).timestamp())
                if cf.main_config.get("EFlagSetDiscordRPCStart") and (type(cf.main_config.get("EFlagSetDiscordRPCStart")) is float or type(cf.main_config.get("EFlagSetDiscordRPCStart")) is int): start_time = cf.main_config.get("EFlagSetDiscordRPCStart")
                cf.discord_rpc.update(
                    details=f"Idling Roblox{' Studio' if cf.run_studio == True else ''}",
                    start=start_time,
                    large_image=thumbnail_url, 
                    large_url="https://www.roblox.com/",
                    large_text=f"Roblox{' Studio' if cf.run_studio == True else ''}", 
                    small_image=f"{cf.main_host}/Images/AppIcon{'RunStudio' if cf.run_studio == True else 'PlayRoblox'}Discord.png", 
                    small_url=cf.main_host,
                    small_text=obName0(), 
                    buttons=[
                        {
                            "label": ts("Go to Roblox! 🌐"), 
                            "url": f"https://www.roblox.com/"
                        }
                    ]
                )
                cf.discord_rpc.default_presence = cf.discord_rpc.current_presence
def generateEmbedField(name, value, inline=True): return {"name": name, "value": str(value), "inline": inline}
def generateDiscordPayload(title, color, fields, thumbnail_url): return {"content": f"<@{cf.main_config.get('EFlagDiscordWebhookUserId')}>", "embeds": [{"title": title, "color": color, "fields": fields, "author": { "name": obName0(), "icon_url": cf.main_config.get("EFlagCustomBootstrapInternetURL", f"{cf.main_host}/Images/DiscordIcon.png") }, "thumbnail": { "url": thumbnail_url }, "footer": { "text": (ts(f"Made by @EfazDev | PID: {rcf.connected_roblox_instance.pid}") if cf.main_config.get("EFlagDiscordWebhookShowPidInFooter") == True and rcf.connected_roblox_instance and rcf.connected_roblox_instance.pid else ts("Made by @EfazDev")) + (" | Custom Theme" if obName0() != "OrangeBlox" or obName1() != "🍊" else ""), "icon_url": "https://cdn.efaz.dev/cdn/png/logo.png" }, "timestamp": datetime.datetime.now(tz=datetime.UTC).strftime('%Y-%m-%dT%H:%M:%S.000Z')}], "attachments": []}
def getRobloxThumbnailURL(studio: bool=None):
    if studio == None: studio = cf.run_studio
    thumbnail_url = f"{cf.main_host}/Images/RobloxStudioLogo.png" if studio == True else f"{cf.main_host}/Images/RobloxLogo.png"
    selected_brand = cf.main_config.get(f"EFlagSelectedBrandLogo{'2' if studio == True else ''}", '')
    if selected_brand in cf.special_logo_mods["studio" if studio == True else "reg"]:
        thumbnail_url = f"{cf.main_host}/Mods/Roblox{'Studio' if studio == True else ''}Brand/{selected_brand}/{'AppIcon' if studio == True else 'RobloxTilt'}.png"
    return thumbnail_url
def sendDiscordWebhook(webhook_json, name):
    def sen():
        waitForInternet()
        req = cf.requests.post(cf.main_config.get("EFlagDiscordWebhookURL"), data=webhook_json)
        if req.ok: printDebugMessage(f"Successfully sent webhook! Event: {name}")
        else: printErrorMessage(f"There was an issue sending your webhook message. Status Code: {req.status_code}")
    if cf.pip_class.getIfConnectedToInternet() == True: sen()
    else: cf.pip_class.startThread(func=sen, daemon=True)
cf.restartRoblox = restartRoblox

# Activity Tracking Functions
def onGameJoinedStudio(info):
    rcf.connected_to_game = True
    generated_location = "Unknown Location"
    if info.get("ip"):
        printDebugMessage(f"Roblox IP Address Detected! IP: {info.get('ip')}")
        try:
            allocated_roblox_ip = info.get("ip")
            server_info_res = cf.requests.get(f"https://free.freeipapi.com/api/json/{allocated_roblox_ip}")
            if server_info_res.ok:
                server_info_json = server_info_res.json
                city_name = server_info_json.get("cityName", "")
                region_name = server_info_json.get("regionName", "")
                country_code = server_info_json.get("countryCode", "")
                if not city_name: city_name = ""
                if not region_name: region_name = ""
                if not country_code: country_code = ""
                if city_name and country_code:
                    city_name = re.sub(r'\s*\([^)]*\)', '', city_name)
                    region_name = re.sub(r'\s*\([^)]*\)', '', region_name if region_name else "")
                    if region_name != None and region_name != "": generated_location = f"{city_name}, {region_name}, {country_code}"
                    else: generated_location = f"{city_name}, {country_code}"
                else:
                    printDebugMessage(server_info_res.text)
                    printDebugMessage("Failed to get server information: IP Request resulted with no information.")
            else:
                printDebugMessage(server_info_res.text)
                printDebugMessage("Failed to get server information: IP Request Rejected.")
        except Exception as e:
            printDebugMessage(f"Failed to get server information: {e}")
            return
        if cf.main_config.get("EFlagNotifyServerLocation") == True:
            printSuccessMessage(f"Roblox is currently connecting to a studio server in: {generated_location} [{allocated_roblox_ip}]!")
            displayNotification(ts("Joining Studio Server"), ts(f"You have connected to a studio server from {generated_location}!"))
            printDebugMessage("Sent Notification to Bootstrap for Notification Center shipping!")
    app_settings = cf.handler.getRobloxAppSettings()
    logged_in_user: dict = app_settings.get("loggedInUser")
    if logged_in_user.get("name") and logged_in_user.get("id"):
        rcf.connected_user_info = {"name": logged_in_user.get("name"), "id": logged_in_user.get("id"), "display": logged_in_user.get("displayName")}
    if rcf.current_place_info:
        if generated_location: rcf.current_place_info["server_location"] = generated_location
        if rcf.current_place_info.get('place_identifier') and safeConvertNumber(rcf.current_place_info.get('place_identifier')):
            rcf.current_place_info["placeId"] = int(rcf.current_place_info.get('place_identifier'))
            if cf.main_config.get("EFlagUseEfazDevAPI") == True: 
                generated_universe_id_res = cf.requests.get(f"https://api.efaz.dev/api/roblox/universeId/{rcf.current_place_info.get('place_identifier')}", loop_429=cf.main_config.get("EFlagEnableLoop429Requests")==True)
                if generated_universe_id_res and generated_universe_id_res.json: generated_universe_id_res.json = generated_universe_id_res.json.get("response")
            else: generated_universe_id_res = cf.requests.get(f"https://apis.roblox.com/universes/v1/places/{rcf.current_place_info.get('place_identifier')}/universe", loop_429=cf.main_config.get("EFlagEnableLoop429Requests")==True, cookies=createCookieHeader())
            if generated_universe_id_res.ok:
                generated_universe_id_json = generated_universe_id_res.json
                if generated_universe_id_json and generated_universe_id_json.get("universeId") != None:
                    if rcf.current_place_info: rcf.current_place_info["universeId"] = generated_universe_id_json.get("universeId")
                else: rcf.current_place_info = None
            else: rcf.current_place_info = None
        else:
            rcf.current_place_info["placeId"] = None
            rcf.current_place_info["universeId"] = -100
        if rcf.current_place_info:
            universeId = rcf.current_place_info.get('universeId')
            if universeId == -100:
                generated_thumbnail_api_res = PyKits.InstantRequestJSONResponse({ "data": [] })
                generated_place_api_res = PyKits.InstantRequestJSONResponse({"data": [
                    {
                        "name": os.path.basename(rcf.current_place_info.get('place_identifier', '')),
                        "id": None,
                        "universeId": -100,
                        "description": ""
                    }
                ]})
                generated_universe_api_res = PyKits.InstantRequestJSONResponse({"data": [
                    {
                        "name": os.path.basename(rcf.current_place_info.get('place_identifier', '')),
                        "id": None,
                        "rootPlaceName": os.path.basename(rcf.current_place_info.get('place_identifier', '')),
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
                if cf.main_config.get("EFlagUseEfazDevAPI") == True: 
                    generated_thumbnail_api_res = cf.requests.get(f"https://api.efaz.dev/api/roblox/game-thumbnail/{universeId}", loop_429=cf.main_config.get("EFlagEnableLoop429Requests")==True)
                    generated_place_api_res = cf.requests.get(f"https://api.efaz.dev/api/roblox/places-in-universe/{universeId}", loop_429=cf.main_config.get("EFlagEnableLoop429Requests")==True)
                    generated_universe_api_res = cf.requests.get(f"https://api.efaz.dev/api/roblox/game-info/{universeId}", loop_429=cf.main_config.get("EFlagEnableLoop429Requests")==True)
                    if generated_thumbnail_api_res and generated_thumbnail_api_res.json: generated_thumbnail_api_res.json = generated_thumbnail_api_res.json.get("response")
                    if generated_place_api_res and generated_place_api_res.json: generated_place_api_res.json = generated_place_api_res.json.get("response")
                    if generated_universe_api_res and generated_universe_api_res.json: generated_universe_api_res.json = generated_universe_api_res.json.get("response")
                else: 
                    generated_thumbnail_api_res = cf.requests.get(f"https://thumbnails.roblox.com/v1/games/icons?universeIds={universeId}&returnPolicy=PlaceHolder&size=512x512&format=Png&isCircular=false", loop_429=cf.main_config.get("EFlagEnableLoop429Requests")==True, cookies=createCookieHeader())
                    generated_place_api_res = cf.requests.get(f"https://develop.roblox.com/v1/universes/{universeId}/places?isUniverseCreation=false&limit=50&sortOrder=Asc", loop_429=cf.main_config.get("EFlagEnableLoop429Requests")==True, cookies=createCookieHeader())
                    generated_universe_api_res = cf.requests.get(f"https://games.roblox.com/v1/games?universeIds={universeId}", loop_429=cf.main_config.get("EFlagEnableLoop429Requests")==True, cookies=createCookieHeader())
            if generated_thumbnail_api_res.ok and generated_place_api_res.ok and generated_universe_api_res.ok:
                generated_thumbnail_api_json = generated_thumbnail_api_res.json
                generated_place_api_json = generated_place_api_res.json
                generated_universe_api_json = generated_universe_api_res.json
                thumbnail_url = f"{cf.main_host}/Images/AppIconRunStudio.png"
                if generated_thumbnail_api_json.get("data"):
                    if len(generated_thumbnail_api_json.get("data")) > 0: thumbnail_url = generated_thumbnail_api_json.get("data")[0]["imageUrl"]
                if rcf.current_place_info: rcf.current_place_info["thumbnail_url"] = thumbnail_url
                if len(generated_place_api_json.get("data", [])) > 0 and len(generated_universe_api_json.get("data", [])) > 0:
                    generated_universe_api_json = generated_universe_api_json.get("data")[0]
                    place_info = {}
                    for place_under_experience in generated_place_api_json.get("data"):
                        if rcf.current_place_info and str(place_under_experience.get("id")) == str(rcf.current_place_info.get("placeId")): place_info = place_under_experience
                    if rcf.current_place_info:
                        if place_info:
                            generated_universe_api_json["rootPlaceName"] = generated_universe_api_json["name"]
                            for i in generated_universe_api_json.keys():
                                if not place_info.get(i) and i != "id" and i != "name" and i != "description" and i != "universeId": place_info[i] = generated_universe_api_json[i]
                            if rcf.current_place_info: rcf.current_place_info["place_info"] = place_info
                    try:
                        if cf.main_os == "Windows" and rcf.connected_roblox_instance:
                            if cf.main_config.get("EFlagShowRunningAccountNameInTitle") == True:
                                windows_opened = rcf.connected_roblox_instance.getWindowsOpened()
                                for i in windows_opened:
                                    if rcf.connected_user_info:
                                        if cf.main_config.get("EFlagShowDisplayNameInTitle") == True: i.setWindowTitle(ts(f"Roblox Studio - Opened @{rcf.connected_user_info.get('name', 'Unknown')} [ID: {rcf.connected_user_info.get('id', 'Unknown')}] as {rcf.connected_user_info.get('display', 'Unknown')}!"))
                                        else: i.setWindowTitle(ts(f"Roblox Studio - Opened @{rcf.connected_user_info.get('name', 'Unknown')} [ID: {rcf.connected_user_info.get('id', 'Unknown')}]!"))
                            elif cf.main_config.get("EFlagShowRunningGameInTitle") == True:
                                windows_opened = rcf.connected_roblox_instance.getWindowsOpened()
                                for i in windows_opened: i.setWindowTitle(ts(f"Roblox Studio - Opened {place_info.get('name', 'Unknown')}"))
                    except Exception: printDebugMessage(f"Something went wrong setting the Window Title: \n{trace()}")
                    try:
                        start_time = int(datetime.datetime.now(tz=datetime.UTC).timestamp())
                        if cf.main_config.get("EFlagSetDiscordRPCStart") and (type(cf.main_config.get("EFlagSetDiscordRPCStart")) is float or type(cf.main_config.get("EFlagSetDiscordRPCStart")) is int): start_time = cf.main_config.get("EFlagSetDiscordRPCStart")
                        if rcf.current_place_info: rcf.current_place_info["start_time"] = start_time
                        if cf.main_config.get("EFlagEnableDiscordRPCStudio") == True:
                            # Handle User Thumbnail
                            if rcf.connected_user_info and cf.main_config.get("EFlagShowUserProfilePictureInsteadOfLogo") == True:
                                thumbnail_res = cf.requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={rcf.connected_user_info.get('id')}&size=100x100&format=Png&isCircular=false", loop_429=cf.main_config.get("EFlagEnableLoop429Requests")==True, cookies=createCookieHeader())
                                if thumbnail_res.ok:
                                    thumbnail_json = thumbnail_res.json
                                    if thumbnail_json and len(thumbnail_json.get("data", [])) > 0:
                                        user_thumbnail = thumbnail_json["data"][0].get("imageUrl")
                                        if user_thumbnail:
                                            if rcf.connected_user_info:
                                                rcf.connected_user_info["thumbnail"] = user_thumbnail
                                                printSuccessMessage(f"Successfully loaded user thumbnail of @{rcf.connected_user_info.get('name')} [User ID: {rcf.connected_user_info.get('id')}]!")
                                                printDebugMessage(f"Loaded thumbnail: {user_thumbnail}")
                                        else: printDebugMessage(f"Failed to load thumbnail for @{rcf.connected_user_info.get('name')} [User ID: {rcf.connected_user_info.get('id')}]! Status Code: {thumbnail_res.status_code}")
                                    else: printDebugMessage(f"Failed to load thumbnail for @{rcf.connected_user_info.get('name')} [User ID: {rcf.connected_user_info.get('id')}]! Status Code: {thumbnail_res.status_code}")
                                else: printDebugMessage(f"Failed to load thumbnail for @{rcf.connected_user_info.get('name')} [User ID: {rcf.connected_user_info.get('id')}]! Status Code: {thumbnail_res.status_code}")
                        
                            def embed():
                                try:
                                    if not cf.discord_rpc: startDiscordRPC()
                                    err_count = 0
                                    loop_key = cf.discord_rpc.generate_loop_key()
                                    while True:
                                        if (not cf.discord_rpc) or (not cf.discord_rpc.connected) or cf.discord_rpc.current_loop_id != loop_key: printDebugMessage("Invalid RPC Loop Information Detected! Broken Loop!"); break
                                        if cf.discord_rpc_info == None: cf.discord_rpc_info = {}
                                        playing_game_name = place_info['name']
                                        if place_info['creator']['name'] == "Local File" and place_info['creator']['id'] == 0: creator_name = ts(f"Opened as Local File!")
                                        else:
                                            creator_name = ts(f"Made by {'@' if place_info['creator'].get('type') == 'User' else ''}{place_info['creator']['name']}").replace("✅", "")
                                            if place_info.get("creator").get("hasVerifiedBadge") == True: creator_name = f"{creator_name} ✅!"
                                            else: creator_name = f"{creator_name}!"
                                        if place_info.get("rootPlaceId") != place_info.get("id"): playing_game_name = f"{playing_game_name} ({place_info['rootPlaceName']})"
                                        formatted_info = {
                                            "details": cf.discord_rpc_info.get("details") if cf.discord_rpc_info.get("details") else f"Editing {playing_game_name}",
                                            "state": cf.discord_rpc_info.get("state") if cf.discord_rpc_info.get("state") else creator_name,
                                            "start": cf.discord_rpc_info.get("start") if cf.discord_rpc_info.get("start") else start_time,
                                            "stop": cf.discord_rpc_info.get("stop") if cf.discord_rpc_info.get("stop") and cf.discord_rpc_info.get("stop") > 1000 else None,
                                            "large_image": cf.discord_rpc_info.get("large_image") if cf.discord_rpc_info.get("large_image") else thumbnail_url,
                                            "large_text": cf.discord_rpc_info.get("large_text") if cf.discord_rpc_info.get("large_text") else playing_game_name,
                                            "large_image_url": f"https://www.roblox.com",
                                            "small_image": cf.discord_rpc_info.get("small_image") if cf.discord_rpc_info.get("small_image") else f"{cf.main_host}/Images/AppIconRunStudioDiscord.png",
                                            "small_image_url": f"{cf.main_host}/",
                                            "small_text": cf.discord_rpc_info.get("small_text") if cf.discord_rpc_info.get("small_text") else obName0(),
                                            "buttons": [],
                                            "state_url": None,
                                            "launch_data": cf.discord_rpc_info.get("launch_data") if cf.discord_rpc_info.get("launch_data") else ""
                                        }
                                        if formatted_info["small_image"] == f"{cf.main_host}/Images/AppIconRunStudioDiscord.png" and cf.main_config.get("EFlagShowUserProfilePictureInsteadOfLogo") == True and rcf.connected_user_info and rcf.connected_user_info.get("thumbnail"): 
                                            formatted_info["small_image"] = rcf.connected_user_info.get("thumbnail")
                                        if formatted_info["small_text"] == obName0() and cf.main_config.get("EFlagShowUsernameInSmallImage") == True and rcf.connected_user_info and rcf.connected_user_info.get("display") and rcf.connected_user_info.get("name"): 
                                            formatted_info["small_text"] = ts(f"Opened Studio as {rcf.connected_user_info.get('display')} (@{rcf.connected_user_info.get('name')})!")
                                            formatted_info["buttons"].append({
                                                "label": ts("Open User Page 🌐"), 
                                                "url": f"https://www.roblox.com/users/{logged_in_user.get('id')}/profile"
                                            })
                                            formatted_info["smart_image_url"] = f"https://www.roblox.com/users/{logged_in_user.get('id')}/profile"
                                        if place_info.get("creator").get("id") != 0 and rcf.current_place_info:
                                            formatted_info["buttons"].append({
                                                "label": ts("Open Game Page 🕹️"), 
                                                "url": f"https://www.roblox.com/games/{rcf.current_place_info['placeId']}"
                                            })
                                            if formatted_info["state"] == creator_name and place_info and place_info['creator']['id'] > 0:
                                                if place_info['creator'].get('type') == 'User': formatted_info["state_url"] = f"https://www.roblox.com/users/{place_info['creator']['id']}/profile"
                                                else: formatted_info["state_url"] = f"https://www.roblox.com/groups/{place_info['creator']['id']}"
                                            formatted_info["large_image_url"] = f"https://www.roblox.com/games/{rcf.current_place_info['placeId']}"
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
                                            if cf.discord_rpc:
                                                try:
                                                    req = cf.discord_rpc.update(
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
                                                        name=playing_game_name if cf.main_config.get("EFlagShowStudioGameNameInStatusBar") else "Roblox Studio 🔨",
                                                        buttons=formatted_info["buttons"]
                                                    )
                                                    if req.get("code") == 2: printDebugMessage("Invalid RPC Loop Information Detected! Broken Loop!"); break
                                                except Exception:
                                                    if err_count > 9:
                                                        printDebugMessage("Discord RPC Session may be broken. Loop has been broken.")
                                                        break
                                                    else: err_count += 1
                                        except Exception:
                                            if err_count > 9:
                                                printDebugMessage("Discord RPC Session may be broken. Loop has been broken.")
                                                break
                                            else:
                                                err_count += 1
                                                printDebugMessage(f"There was an error updating Discord RPC: \n{trace()}")
                                        time.sleep(0.1)
                                except Exception: printDebugMessage(f"There was an error updating Discord RPC: \n{trace()}")
                            cf.pip_class.startThread(func=embed, daemon=True)
                            printDebugMessage("Successfully attached Discord RPC!")
                    except Exception: printDebugMessage("Unable to insert Discord Rich Presence. Please make sure Discord is open.")
                    try:
                        if cf.main_config.get("EFlagUseDiscordWebhook") == True and cf.main_config.get("EFlagDiscordWebhookConnect") == True:
                            if cf.main_config.get("EFlagDiscordWebhookURL"):
                                title = ts("Joined Studio Server!")
                                color = 65280
                                user_connected_text = ts("Unknown User")
                                if rcf.connected_user_info: user_connected_text = f'[@{rcf.connected_user_info["name"]} [{rcf.connected_user_info["id"]}]](https://www.roblox.com/users/{rcf.connected_user_info["id"]}/profile)'
                                buttons = []
                                if universeId == -100:
                                    buttons = [
                                        generateEmbedField(ts("Is Local File"), f"True"),
                                        generateEmbedField(ts("Local File Path"), f"{rcf.current_place_info.get('place_identifier')}")
                                    ]
                                else:
                                    buttons = [
                                        generateEmbedField(ts("Is Local File"), f"False"),
                                        generateEmbedField(ts("Connected Game"), f"[{place_info['name']}](https://www.roblox.com/games/{rcf.current_place_info.get('placeId')})"),
                                        generateEmbedField(ts("Edit Link"), f"[{ts('Edit Now!')}](https://rbx.efaz.dev/studio?info=1+task:EditPlace+placeId:{rcf.current_place_info.get('placeId')}+universeId:{rcf.current_place_info.get('universeId')})")
                                    ]
                                generated_body = generateDiscordPayload(title, color, buttons + [
                                    generateEmbedField(ts("Started"), f"<t:{int(start_time)}:R>"),
                                    generateEmbedField(ts("User Connected"), user_connected_text),
                                    generateEmbedField(ts("Server Location"), f"{generated_location}")
                                ], thumbnail_url) 
                                try: sendDiscordWebhook(generated_body, "onGameJoined")
                                except Exception: printDebugMessage(f"There was an issue sending your webhook message. Exception: \n{trace()}")
                    except Exception: printDebugMessage("Unable to send Discord Webhook. Please check if the link is valid.")
                else: printDebugMessage("Provided place info is not found.")
            else: printDebugMessage(f"Place responses rejected by Roblox. [{generated_thumbnail_api_res.ok},{generated_thumbnail_api_res.status_code} | {generated_place_api_res.ok},{generated_place_api_res.status_code}]")
def onOpeningGameStudio(info):
    if not rcf.current_place_info: rcf.current_place_info = info
    elif info.get("placeId") and info.get("jobId"): 
        for i, v in info.items(): rcf.current_place_info[i] = v
def onGameLoadedStudio(info):
    if rcf.connected_to_game == False: onGameJoinedStudio({})
def onLostConnectionStudio(info):
    rcf.is_connection_lost = True
    if cf.main_config.get("EFlagForceReconnectOnStudioLost") == True and rcf.connected_roblox_instance.loading_existing_logs == False:
        placeId = rcf.current_place_info and rcf.current_place_info.get('place_identifier')
        universeId = rcf.current_place_info and rcf.current_place_info.get('universeId')
        if placeId and universeId:
            rcf.connected_roblox_instance.endInstance()
            url = f"roblox-studio:1+task:EditPlace+placeId:{placeId}+universeId:{universeId}"
            if cf.main_os == "Darwin": subprocess.run([cf.pip_class.getPathFile("/usr/bin/open"), url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cf.cur_path)
            else: subprocess.run(f"start {url}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cf.cur_path)
def onClosingGameStudio(info):
    synced_place_info = None
    rcf.connected_to_game = False
    if rcf.current_place_info:
        synced_place_info = dict(rcf.current_place_info)
        rcf.current_place_info = None
    printErrorMessage("User has disconnected from the server!")
    try:
        if cf.main_os == "Windows" and rcf.connected_roblox_instance and cf.main_config.get("EFlagShowRunningGameInTitle") == True:
            windows_opened = rcf.connected_roblox_instance.getWindowsOpened()
            for i in windows_opened: i.setWindowTitle(ts(f"Roblox Studio"))
    except Exception: printDebugMessage(f"Something went wrong setting the Window Title: \n{trace()}")
    if cf.main_config.get("EFlagUseDiscordWebhook") == True and cf.main_config.get("EFlagDiscordWebhookDisconnect") == True:
        if cf.main_config.get("EFlagDiscordWebhookURL"):
            thumbnail_url = cf.main_config.get("EFlagCustomBootstrapInternetURL", f"{cf.main_host}/Images/DiscordIcon.png")
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

                if rcf.is_connection_lost == True: title = ts(f"Lost Connection from Studio Server!"); color = 16776960
                user_connected_text = ts("Unknown User")
                if rcf.connected_user_info: user_connected_text = f'[@{rcf.connected_user_info["name"]} [{rcf.connected_user_info["id"]}]](https://www.roblox.com/users/{rcf.connected_user_info["id"]}/profile)'

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
                except Exception: printDebugMessage(f"There was an issue sending your webhook message. Exception: \n{trace()}")
    if cf.main_config.get("EFlagEnableDiscordRPCStudio") == True:
        try: 
            if cf.discord_rpc: cf.discord_rpc.clear()
        except Exception: printDebugMessage(f"There was an error clearing Discord RPC: \n{trace()}")
        cf.discord_rpc_info = None
    if cf.main_config.get("EFlagEndStudioPlaceWhenDisconnected") == True and rcf.connected_roblox_instance and cf.handler.getIfRobloxIsOpen(studio=cf.run_studio, pid=rcf.connected_roblox_instance.pid): rcf.connected_roblox_instance.endInstance()
def onRobloxPublishingStudio(info):
    printSuccessMessage("Roblox Game has been successfully published to Roblox!")
    if cf.main_config.get("EFlagUseDiscordWebhook") == True and cf.main_config.get("EFlagDiscordWebhookGamePublished") == True:
        if cf.main_config.get("EFlagDiscordWebhookURL"):
            thumbnail_url = cf.main_config.get("EFlagCustomBootstrapInternetURL", f"{cf.main_host}/Images/DiscordIcon.png")
            server_location = ts("Unknown Location")
            start_time = 0
            place_info = {"name": "???"}
            if rcf.current_place_info:
                if rcf.current_place_info.get("start_time"): start_time = rcf.current_place_info.get("start_time")
                if rcf.current_place_info.get("server_location"): server_location = rcf.current_place_info.get("server_location")
                if rcf.current_place_info.get("place_info"): place_info = rcf.current_place_info.get("place_info")
                if rcf.current_place_info.get("thumbnail_url"): thumbnail_url = rcf.current_place_info.get("thumbnail_url")

            title = ts(f"Roblox Game Published!")
            color = 16748547
            user_connected_text = ts("Unknown User")
            if rcf.connected_user_info: user_connected_text = f'[@{rcf.connected_user_info["name"]} [{rcf.connected_user_info["id"]}]](https://www.roblox.com/users/{rcf.connected_user_info["id"]}/profile)'

            buttons = []
            if rcf.current_place_info.get("universeId") == -100:
                buttons = [
                    generateEmbedField(ts("Is Local File"), f"True"),
                    generateEmbedField(ts("Local File Path"), f"{rcf.current_place_info.get('place_identifier')}")
                ]
            else:
                buttons = [
                    generateEmbedField(ts("Is Local File"), f"False"),
                    generateEmbedField(ts("Published Game"), f"[{place_info['name']}](https://www.roblox.com/games/{rcf.current_place_info.get('placeId')})"),
                    generateEmbedField(ts("Edit Link"), f"[{ts('Edit Now!')}](https://rbx.efaz.dev/studio?info=1+task:EditPlace+placeId:{rcf.current_place_info.get('placeId')}+universeId:{rcf.current_place_info.get('universeId')})")
                ]

            generated_body = generateDiscordPayload(title, color, buttons + [
                generateEmbedField(ts("Started"), f"<t:{int(start_time)}:R>"),
                generateEmbedField(ts("User Connected"), user_connected_text),
                generateEmbedField(ts("Server Location"), f"{server_location}")
            ], thumbnail_url)
            try: sendDiscordWebhook(generated_body, "onRobloxPublishing")
            except Exception: printDebugMessage(f"There was an issue sending your webhook message. Exception: \n{trace()}")
def onRobloxSavingStudio(info):
    printSuccessMessage("Roblox Game has been successfully saved to Roblox!")
    if cf.main_config.get("EFlagUseDiscordWebhook") == True and cf.main_config.get("EFlagDiscordWebhookGameSaved") == True:
        if cf.main_config.get("EFlagDiscordWebhookURL"):
            thumbnail_url = cf.main_config.get("EFlagCustomBootstrapInternetURL", f"{cf.main_host}/Images/DiscordIcon.png")
            server_location = ts("Unknown Location")
            start_time = 0
            place_info = {"name": "???"}
            if rcf.current_place_info:
                if rcf.current_place_info.get("start_time"): start_time = rcf.current_place_info.get("start_time")
                if rcf.current_place_info.get("server_location"): server_location = rcf.current_place_info.get("server_location")
                if rcf.current_place_info.get("place_info"): place_info = rcf.current_place_info.get("place_info")
                if rcf.current_place_info.get("thumbnail_url"): thumbnail_url = rcf.current_place_info.get("thumbnail_url")

            title = ts(f"Roblox Game Saved!")
            color = 16745942
            user_connected_text = ts("Unknown User")
            if rcf.connected_user_info: user_connected_text = f'[@{rcf.connected_user_info["name"]} [{rcf.connected_user_info["id"]}]](https://www.roblox.com/users/{rcf.connected_user_info["id"]}/profile)'

            buttons = []
            if rcf.current_place_info.get("universeId") == -100:
                buttons = [
                    generateEmbedField(ts("Is Local File"), f"True"),
                    generateEmbedField(ts("Local File Path"), f"{rcf.current_place_info.get('place_identifier')}")
                ]
            else:
                buttons = [
                    generateEmbedField(ts("Is Local File"), f"False"),
                    generateEmbedField(ts("Saved Game"), f"[{place_info['name']}](https://www.roblox.com/games/{rcf.current_place_info.get('placeId')})"),
                    generateEmbedField(ts("Edit Link"), f"[{ts('Edit Now!')}](https://rbx.efaz.dev/studio?info=1+task:EditPlace+placeId:{rcf.current_place_info.get('placeId')}+universeId:{rcf.current_place_info.get('universeId')})")
                ]

            generated_body = generateDiscordPayload(title, color, buttons + [
                generateEmbedField(ts("Started"), f"<t:{int(start_time)}:R>"),
                generateEmbedField(ts("User Connected"), user_connected_text),
                generateEmbedField(ts("Server Location"), f"{server_location}")
            ], thumbnail_url)
            try: sendDiscordWebhook(generated_body, "onRobloxSaving")
            except Exception: printDebugMessage(f"There was an issue sending your webhook message. Exception: \n{trace()}")
def onPlayTestStartStudio(info):
    if not rcf.current_place_info: rcf.current_place_info = info
    elif info.get("placeId") and info.get("jobId"): 
        for i, v in info.items(): rcf.current_place_info[i] = v
def onNewRobloxStudio(info):
    if cf.main_os == "Darwin": subprocess.run([cf.pip_class.getPathFile("/usr/bin/open"), "orangeblox://reconnect-studio"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cf.cur_path)
    else: subprocess.run("start orangeblox://reconnect-studio", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cf.cur_path)
def onStudioInstallerLaunchedStudio(info): rcf.connected_roblox_instance.endInstance()
def onPlayTestDisconnectedStudio(info): pass
def onTeamCreateConnectStudio(info): pass
def onTeamCreateDisconnectStudio(info): pass

def onGameJoined(info):
    if info.get("ip"):
        printDebugMessage(f"Roblox IP Address Detected! IP: {info.get('ip')}")
        allocated_roblox_ip = info.get("ip")
        generated_location = "Unknown Location"
        try:
            server_info_res = cf.requests.get(f"https://free.freeipapi.com/api/json/{allocated_roblox_ip}")
            if server_info_res.ok:
                server_info_json = server_info_res.json
                city_name = server_info_json.get("cityName", "")
                region_name = server_info_json.get("regionName", "")
                country_code = server_info_json.get("countryCode", "")
                if not city_name: city_name = ""
                if not region_name: region_name = ""
                if not country_code: country_code = ""
                if city_name and country_code:
                    city_name = re.sub(r'\s*\([^)]*\)', '', city_name)
                    region_name = re.sub(r'\s*\([^)]*\)', '', region_name if region_name else "")
                    if region_name != None and region_name != "": generated_location = f"{city_name}, {region_name}, {country_code}"
                    else: generated_location = f"{city_name}, {country_code}"
                else:
                    printDebugMessage(server_info_res.text)
                    printDebugMessage("Failed to get server information: IP Request resulted with no information.")
            else:
                printDebugMessage(server_info_res.text)
                printDebugMessage("Failed to get server information: IP Request Rejected.")
        except Exception as e:
            printDebugMessage(f"Failed to get server information: An error occurred while fetching the information. Error: {e}")
        
        if cf.main_config.get("EFlagEnableRoValraServerUptime") == True and rcf.current_place_info:
            try:
                if rcf.current_place_info.get("jobId") and rcf.current_place_info.get("placeId"):
                    jobId = rcf.current_place_info.get("jobId")
                    placeId = rcf.current_place_info.get("placeId")
                    uptime_res = cf.handler.getServerInformation(placeId, jobId, debug=(cf.main_config.get("EFlagEnableDebugMode") == True))
                    if uptime_res and uptime_res.get("success"):
                        server_info = uptime_res.get("server")
                        if server_info.get("first_seen") != None:
                            first_seen_str = server_info.get("first_seen")
                            first_seen = datetime.datetime.fromisoformat(first_seen_str.replace("Z", "+00:00"))
                            current_time = datetime.datetime.now(datetime.timezone.utc)
                            uptime = current_time - first_seen
                            uptime = max(uptime, datetime.timedelta(seconds=0))
                            days = uptime.days
                            hours, remainder = divmod(uptime.seconds, 3600)
                            minutes, seconds = divmod(remainder, 60)
                            time_parts = []
                            if days > 0: time_parts.append(f"{days} day{'s' if days != 1 else ''}")
                            if hours > 0: time_parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
                            if minutes > 0: time_parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
                            if seconds > 0 or not time_parts: time_parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
                            uptime_str = ", ".join(time_parts)
                            printDebugMessage(f"Roblox Server Uptime: {uptime_str}")
                            if rcf.current_place_info: rcf.current_place_info["server_uptime"] = uptime_str
                        else: printDebugMessage("Failed to get server uptime: Uptime information not found in response.")
                    else: printDebugMessage("Failed to get server uptime: Request Rejected.")
                else: printDebugMessage(f"Failed to get server uptime: Job/Place ID not found")
            except Exception as e:
                printDebugMessage(f"Failed to get server uptime: An error occurred while fetching the information. Error: {e}")

        if cf.main_config.get("EFlagNotifyServerLocation") == True:
            server_uptime_text = ""
            if rcf.current_place_info and rcf.current_place_info.get("server_uptime"): server_uptime_text = ts(f"\nThe server has been up for: {rcf.current_place_info.get('server_uptime')}.")
            if rcf.set_server_type == 0:
                printSuccessMessage(f"Roblox is currently connecting to a public server in: {generated_location} [{allocated_roblox_ip}]!")
                displayNotification(ts("Joining Server"), ts(f"You have connected to a server from {generated_location}!") + server_uptime_text)
            elif rcf.set_server_type == 1:
                printSuccessMessage(f"Roblox is currently connecting to a private server in: {generated_location} [{allocated_roblox_ip}]!")
                displayNotification(ts("Joining Private Server"), ts(f"You have connected to a private server from {generated_location}!") + server_uptime_text)
            elif rcf.set_server_type == 2:
                printSuccessMessage(f"Roblox is currently connecting to a reserved server in: {generated_location} [{allocated_roblox_ip}]!")
                displayNotification(ts("Joining Reserved Server"), ts(f"You have connected to a reserved server from {generated_location}!") + server_uptime_text)
            elif rcf.set_server_type == 3:
                printSuccessMessage(f"Roblox is currently connecting to a party in: {generated_location} [{allocated_roblox_ip}]!")
                displayNotification(ts("Joining Party Server"), ts(f"You have connected to a party server from {generated_location}!") + server_uptime_text)
            else:
                printSuccessMessage(f"Roblox is currently connecting to a server in: {generated_location} [{allocated_roblox_ip}]!")
                displayNotification(ts("Joining Server"), ts(f"You have connected to a server from {generated_location}!") + server_uptime_text)
            printDebugMessage("Sent Notification to Bootstrap for Notification Center shipping!")
        app_settings = cf.handler.getRobloxAppSettings()
        logged_in_user: dict = app_settings.get("loggedInUser")
        if logged_in_user.get("name") and logged_in_user.get("id"):
            rcf.connected_user_info = {"name": logged_in_user.get("name"), "id": logged_in_user.get("id"), "display": logged_in_user.get("displayName")}
        if rcf.current_place_info:
            rcf.current_place_info["server_location"] = generated_location
            rcf.connected_to_game = True
            if cf.main_config.get("EFlagUseEfazDevAPI") == True: 
                generated_universe_id_res = cf.requests.get(f"https://api.efaz.dev/api/roblox/universeId/{rcf.current_place_info.get('placeId')}", loop_429=cf.main_config.get("EFlagEnableLoop429Requests")==True)
                if generated_universe_id_res and generated_universe_id_res.json: generated_universe_id_res.json = generated_universe_id_res.json.get("response")
            else: generated_universe_id_res = cf.requests.get(f"https://apis.roblox.com/universes/v1/places/{rcf.current_place_info.get('placeId')}/universe", loop_429=cf.main_config.get("EFlagEnableLoop429Requests")==True, cookies=createCookieHeader())
            if generated_universe_id_res.ok:
                generated_universe_id_json = generated_universe_id_res.json
                if generated_universe_id_json and generated_universe_id_json.get("universeId") != None:
                    if rcf.current_place_info: rcf.current_place_info["universeId"] = generated_universe_id_json.get("universeId")
                else: rcf.current_place_info = None
            else: rcf.current_place_info = None
            if rcf.current_place_info:
                universeId = rcf.current_place_info.get('universeId')
                if cf.main_config.get("EFlagUseEfazDevAPI") == True: 
                    generated_thumbnail_api_res = cf.requests.get(f"https://api.efaz.dev/api/roblox/game-thumbnail/{universeId}", loop_429=cf.main_config.get("EFlagEnableLoop429Requests")==True)
                    generated_place_api_res = cf.requests.get(f"https://api.efaz.dev/api/roblox/places-in-universe/{universeId}", loop_429=cf.main_config.get("EFlagEnableLoop429Requests")==True)
                    generated_universe_api_res = cf.requests.get(f"https://api.efaz.dev/api/roblox/game-info/{universeId}", loop_429=cf.main_config.get("EFlagEnableLoop429Requests")==True)
                    if generated_thumbnail_api_res and generated_thumbnail_api_res.json: generated_thumbnail_api_res.json = generated_thumbnail_api_res.json.get("response")
                    if generated_place_api_res and generated_place_api_res.json: generated_place_api_res.json = generated_place_api_res.json.get("response")
                    if generated_universe_api_res and generated_universe_api_res.json: generated_universe_api_res.json = generated_universe_api_res.json.get("response")
                else: 
                    generated_thumbnail_api_res = cf.requests.get(f"https://thumbnails.roblox.com/v1/games/icons?universeIds={universeId}&returnPolicy=PlaceHolder&size=512x512&format=Png&isCircular=false", loop_429=cf.main_config.get("EFlagEnableLoop429Requests")==True, cookies=createCookieHeader())
                    generated_place_api_res = cf.requests.get(f"https://develop.roblox.com/v1/universes/{universeId}/places?isUniverseCreation=false&limit=50&sortOrder=Asc", loop_429=cf.main_config.get("EFlagEnableLoop429Requests")==True, cookies=createCookieHeader())
                    generated_universe_api_res = cf.requests.get(f"https://games.roblox.com/v1/games?universeIds={universeId}", loop_429=cf.main_config.get("EFlagEnableLoop429Requests")==True, cookies=createCookieHeader())
                if generated_thumbnail_api_res.ok and generated_place_api_res.ok and generated_universe_api_res.ok:
                    generated_thumbnail_api_json = generated_thumbnail_api_res.json
                    generated_place_api_json = generated_place_api_res.json
                    generated_universe_api_json = generated_universe_api_res.json

                    thumbnail_url = f"{cf.main_host}/Images/AppIconPlayRoblox.png"
                    if generated_thumbnail_api_json.get("data"):
                        if len(generated_thumbnail_api_json.get("data")) > 0: thumbnail_url = generated_thumbnail_api_json.get("data")[0]["imageUrl"]
                    if rcf.current_place_info: rcf.current_place_info["thumbnail_url"] = thumbnail_url

                    if len(generated_place_api_json.get("data", [])) > 0 and len(generated_universe_api_json.get("data", [])) > 0:
                        generated_universe_api_json = generated_universe_api_json.get("data")[0]
                        place_info = {}
                        for place_under_experience in generated_place_api_json.get("data"):
                            if rcf.current_place_info and str(place_under_experience.get("id")) == str(rcf.current_place_info.get("placeId")): place_info = place_under_experience
                        if rcf.current_place_info:
                            if place_info:
                                generated_universe_api_json["rootPlaceName"] = generated_universe_api_json["name"]
                                for i in generated_universe_api_json.keys():
                                    if not place_info.get(i) and i != "id" and i != "name" and i != "description" and i != "universeId": place_info[i] = generated_universe_api_json[i]
                                if rcf.current_place_info: rcf.current_place_info["place_info"] = place_info
                        try:
                            if cf.main_os == "Windows" and rcf.connected_roblox_instance:
                                if cf.main_config.get("EFlagShowRunningAccountNameInTitle") == True:
                                    windows_opened = rcf.connected_roblox_instance.getWindowsOpened()
                                    for i in windows_opened:
                                        if rcf.connected_user_info:
                                            if cf.main_config.get("EFlagShowDisplayNameInTitle") == True: i.setWindowTitle(ts(f"Roblox - Playing @{rcf.connected_user_info.get('name', 'Unknown')} [ID: {rcf.connected_user_info.get('id', 'Unknown')}] as {rcf.connected_user_info.get('display', 'Unknown')}!"))
                                            else: i.setWindowTitle(ts(f"Roblox - Playing @{rcf.connected_user_info.get('name', 'Unknown')} [ID: {rcf.connected_user_info.get('id', 'Unknown')}]!"))
                                elif cf.main_config.get("EFlagShowRunningGameInTitle") == True:
                                    windows_opened = rcf.connected_roblox_instance.getWindowsOpened()
                                    for i in windows_opened: i.setWindowTitle(ts(f"Roblox - Playing {place_info.get('name', 'Unknown')}"))
                        except Exception: printDebugMessage(f"Something went wrong setting the Window Title: \n{trace()}")
                        try:
                            start_time = int(datetime.datetime.now(tz=datetime.UTC).timestamp())
                            if cf.main_config.get("EFlagSetDiscordRPCStart") and (type(cf.main_config.get("EFlagSetDiscordRPCStart")) is float or type(cf.main_config.get("EFlagSetDiscordRPCStart")) is int): start_time = cf.main_config.get("EFlagSetDiscordRPCStart")
                            if rcf.current_place_info: rcf.current_place_info["start_time"] = start_time
                            if cf.main_config.get("EFlagEnableDiscordRPC") == True:
                                # Handle User Thumbnail
                                if rcf.connected_user_info and cf.main_config.get("EFlagShowUserProfilePictureInsteadOfLogo") == True:
                                    thumbnail_res = cf.requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={rcf.connected_user_info.get('id')}&size=100x100&format=Png&isCircular=false", loop_429=cf.main_config.get("EFlagEnableLoop429Requests")==True, cookies=createCookieHeader())
                                    if thumbnail_res.ok:
                                        thumbnail_json = thumbnail_res.json
                                        if thumbnail_json and len(thumbnail_json.get("data", [])) > 0:
                                            user_thumbnail = thumbnail_json["data"][0].get("imageUrl")
                                            if user_thumbnail:
                                                if rcf.connected_user_info:
                                                    rcf.connected_user_info["thumbnail"] = user_thumbnail
                                                    printSuccessMessage(f"Successfully loaded user thumbnail of @{rcf.connected_user_info.get('name')} [User ID: {rcf.connected_user_info.get('id')}]!")
                                                    printDebugMessage(f"Loaded thumbnail: {user_thumbnail}")
                                            else: printDebugMessage(f"Failed to load thumbnail for @{rcf.connected_user_info.get('name')} [User ID: {rcf.connected_user_info.get('id')}]! Status Code: {thumbnail_res.status_code}")
                                        else: printDebugMessage(f"Failed to load thumbnail for @{rcf.connected_user_info.get('name')} [User ID: {rcf.connected_user_info.get('id')}]! Status Code: {thumbnail_res.status_code}")
                                    else: printDebugMessage(f"Failed to load thumbnail for @{rcf.connected_user_info.get('name')} [User ID: {rcf.connected_user_info.get('id')}]! Status Code: {thumbnail_res.status_code}")
                            
                                def embed():
                                    try:
                                        if not cf.discord_rpc: startDiscordRPC()
                                        err_count = 0
                                        loop_key = cf.discord_rpc.generate_loop_key()
                                        while True:
                                            if (not cf.discord_rpc) or (not cf.discord_rpc.connected) or cf.discord_rpc.current_loop_id != loop_key: break
                                            if cf.discord_rpc_info == None: cf.discord_rpc_info = {}
                                            playing_game_name = place_info['name']
                                            creator_name = ts(f"Made by {'@' if place_info['creator'].get('type') == 'User' else ''}{place_info['creator']['name']}")
                                            creator_name = creator_name.replace("✅", "")
                                            if place_info.get("creator").get("hasVerifiedBadge") == True: creator_name = f"{creator_name} ✅!"
                                            else: creator_name = f"{creator_name}!"
                                            if place_info.get("rootPlaceId") != place_info.get("id"): playing_game_name = f"{playing_game_name} ({place_info['rootPlaceName']})"
                                            formatted_info = {
                                                "details": cf.discord_rpc_info.get("details") if cf.discord_rpc_info.get("details") else f"Playing {playing_game_name}",
                                                "state": cf.discord_rpc_info.get("state") if cf.discord_rpc_info.get("state") else creator_name,
                                                "start": cf.discord_rpc_info.get("start") if cf.discord_rpc_info.get("start") else start_time,
                                                "stop": cf.discord_rpc_info.get("stop") if cf.discord_rpc_info.get("stop") and cf.discord_rpc_info.get("stop") > 1000 else None,
                                                "large_image_url": f"https://www.roblox.com/",
                                                "large_image": cf.discord_rpc_info.get("large_image") if cf.discord_rpc_info.get("large_image") else thumbnail_url,
                                                "large_text": cf.discord_rpc_info.get("large_text") if cf.discord_rpc_info.get("large_text") else playing_game_name,
                                                "small_image_url": f"{cf.main_host}/",
                                                "state_url": None,
                                                "buttons": [],
                                                "small_image": cf.discord_rpc_info.get("small_image") if cf.discord_rpc_info.get("small_image") else f"{cf.main_host}/Images/AppIconPlayRobloxDiscord.png",
                                                "small_text": cf.discord_rpc_info.get("small_text") if cf.discord_rpc_info.get("small_text") else obName0(),
                                                "launch_data": cf.discord_rpc_info.get("launch_data") if cf.discord_rpc_info.get("launch_data") else ""
                                            }
                                            launch_data = ""
                                            add_exam = False
                                            if formatted_info["launch_data"] != "": formatted_info["launch_data"] = f"&launchData={formatted_info['launch_data']}"; add_exam = False
                                            if formatted_info["small_image"] == f"{cf.main_host}/Images/AppIconPlayRobloxDiscord.png" and formatted_info["small_text"] == obName0() and cf.main_config.get("EFlagShowUserProfilePictureInsteadOfLogo") == True and rcf.connected_user_info and rcf.connected_user_info.get("thumbnail"): formatted_info["small_image"] = rcf.connected_user_info.get("thumbnail")
                                            if formatted_info["small_text"] == obName0() and cf.main_config.get("EFlagShowUsernameInSmallImage") == True and rcf.connected_user_info and rcf.connected_user_info.get("display") and rcf.connected_user_info.get("name"): 
                                                formatted_info["small_text"] = ts(f"Playing @{rcf.connected_user_info.get('name')} as {rcf.connected_user_info.get('display')}!")
                                                formatted_info["smart_image_url"] = f"https://www.roblox.com/users/{logged_in_user.get('id')}/profile"
                                            if rcf.current_place_info:
                                                formatted_info["buttons"] = [{
                                                    "label": ts("Open Game Page 🕹️"), 
                                                    "url": f"https://www.roblox.com/games/{rcf.current_place_info.get('placeId')}"
                                                }]
                                                formatted_info["large_image_url"] = f"https://www.roblox.com/games/{rcf.current_place_info.get('placeId')}"
                                                if formatted_info["state"] == creator_name and place_info and place_info['creator']['id'] > 0:
                                                    if place_info['creator'].get('type') == 'User': formatted_info["state_url"] = f"https://www.roblox.com/users/{place_info['creator']['id']}/profile"
                                                    else: formatted_info["state_url"] = f"https://www.roblox.com/groups/{place_info['creator']['id']}"
                                                if (rcf.set_server_type == 1 or rcf.set_server_type == 2 or rcf.set_server_type == 3) and cf.main_config.get("EFlagAllowPrivateServerJoining") == True and rcf.set_current_private_server_key:
                                                    if add_exam == True: launch_data = f'{launch_data}?gameInstanceId={rcf.current_place_info.get("jobId")}?accessCode={rcf.set_current_private_server_key}'
                                                    else: launch_data = f'{launch_data}&gameInstanceId={rcf.current_place_info.get("jobId")}&accessCode={rcf.set_current_private_server_key}'
                                                else:
                                                    if add_exam == True: launch_data = f'{launch_data}?gameInstanceId={rcf.current_place_info.get("jobId")}'
                                                    else: launch_data = f'{launch_data}&gameInstanceId={rcf.current_place_info.get("jobId")}'
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
                                                    if cf.main_config.get("EFlagEnableDiscordRPCJoining") == True:
                                                        formatted_info["buttons"].append({
                                                            "label": ts("Join Server! 🚀"),
                                                            "url": f"roblox://experiences/start?placeId={rcf.current_place_info['placeId']}{formatted_info['launch_data']}"
                                                        })
                                                    if cf.discord_rpc:
                                                        try:
                                                            req = cf.discord_rpc.update(
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
                                                                name=playing_game_name if cf.main_config.get("EFlagShowGameNameInStatusBar") else "Roblox",
                                                                buttons=formatted_info["buttons"]
                                                            )
                                                            if req.get("code") == 2: break
                                                        except Exception:
                                                            if err_count > 9:
                                                                printDebugMessage("Discord RPC Session may be broken. Loop has been broken.")
                                                                break
                                                            else: err_count += 1
                                                except Exception:
                                                    if err_count > 9:
                                                        printDebugMessage("Discord RPC Session may be broken. Loop has been broken.")
                                                        break
                                                    else:
                                                        err_count += 1
                                                        printDebugMessage(f"There was an error updating Discord RPC: \n{trace()}")
                                            else: break
                                            time.sleep(0.1)
                                    except Exception: printDebugMessage(f"There was an error updating Discord RPC: \n{trace()}")
                                cf.pip_class.startThread(func=embed, daemon=True)
                                printDebugMessage("Successfully attached Discord RPC!")
                        except Exception: printDebugMessage("Unable to insert Discord Rich Presence. Please make sure Discord is open.")
                        try:
                            if cf.main_config.get("EFlagUseDiscordWebhook") == True and cf.main_config.get("EFlagDiscordWebhookConnect") == True:
                                if cf.main_config.get("EFlagDiscordWebhookURL"):
                                    title = "Joined Server!"
                                    color = 65280
                                    if rcf.set_server_type == 0: title = ts("Joined Public Server!")
                                    elif rcf.set_server_type == 1: title = ts("Joined Private Server!")
                                    elif rcf.set_server_type == 2: title = ts("Joined Reserved Server!")
                                    elif rcf.set_server_type == 3: title = ts("Joined Party Server!"); color = 5570815
                                    else: title = ts("Joined Server!")
                                    launch_data = ""
                                    add_exam = False
                                    if launch_data != "":
                                        launch_data = f"&launchData={launch_data}"
                                        add_exam = False
                                    if (rcf.set_server_type == 1 or rcf.set_server_type == 2 or rcf.set_server_type == 3) and cf.main_config.get("EFlagAllowPrivateServerJoining") == True and rcf.set_current_private_server_key:
                                        if add_exam == True: launch_data = f'{launch_data}?gameInstanceId={rcf.current_place_info["jobId"]}&accessCode={rcf.set_current_private_server_key}'
                                        else: launch_data = f'{launch_data}&gameInstanceId={rcf.current_place_info["jobId"]}&accessCode={rcf.set_current_private_server_key}'
                                    else:
                                        if add_exam == True: launch_data = f'{launch_data}?gameInstanceId={rcf.current_place_info["jobId"]}'
                                        else: launch_data = f'{launch_data}&gameInstanceId={rcf.current_place_info["jobId"]}'
                                    user_connected_text = ts("Unknown User")
                                    if rcf.connected_user_info: user_connected_text = f'[@{rcf.connected_user_info["name"]} [{rcf.connected_user_info["id"]}]](https://www.roblox.com/users/{rcf.connected_user_info["id"]}/profile)'
                                    fields = [
                                        generateEmbedField(ts("Connected Game"), f"[{place_info['name']}](https://www.roblox.com/games/{rcf.current_place_info.get('placeId')})"),
                                        generateEmbedField(ts("Join Link"), f"[{ts('Join Now!')}](https://rbx.efaz.dev/join?placeId={rcf.current_place_info.get('placeId')}{launch_data})"),
                                        generateEmbedField(ts("Started"), f"<t:{int(start_time)}:R>"),
                                        generateEmbedField(ts("User Connected"), user_connected_text),
                                        generateEmbedField(ts("Server Location"), f"{generated_location}")
                                    ]
                                    if rcf.current_place_info and rcf.current_place_info.get("server_uptime"): fields.append(generateEmbedField(ts("Server Uptime"), f"{rcf.current_place_info.get('server_uptime')}"))
                                    generated_body = generateDiscordPayload(title, color, fields, thumbnail_url)
                                    try: sendDiscordWebhook(generated_body, "onGameJoined")
                                    except Exception: printDebugMessage(f"There was an issue sending your webhook message. Exception: \n{trace()}")
                        except Exception: printDebugMessage("Unable to send Discord Webhook. Please check if the link is valid.")
                    else: printDebugMessage("Provided place info is not found.")
                else: printDebugMessage(f"Place responses rejected by Roblox. [{generated_thumbnail_api_res.ok},{generated_thumbnail_api_res.status_code} | {generated_place_api_res.ok},{generated_place_api_res.status_code}]")
def onGameDisconnected(info):
    it_is_teleport = False
    rcf.connected_to_game = False
    synced_place_info = None
    if rcf.skip_disconnect_notification == True: rcf.skip_disconnect_notification = False; return
    if rcf.current_place_info: synced_place_info = dict(rcf.current_place_info); rcf.current_place_info = None
    if rcf.is_teleport == True:
        printYellowMessage("User has been teleported!")
        it_is_teleport = True
        rcf.is_teleport = False
    else: printErrorMessage("User has disconnected from the server!")
    try:
        if cf.main_os == "Windows" and rcf.connected_roblox_instance and cf.main_config.get("EFlagShowRunningGameInTitle") == True:
            windows_opened = rcf.connected_roblox_instance.getWindowsOpened()
            for i in windows_opened: i.setWindowTitle(ts(f"Roblox"))
    except Exception: printDebugMessage(f"Something went wrong setting the Window Title: \n{trace()}")
    if cf.main_config.get("EFlagUseDiscordWebhook") == True and cf.main_config.get("EFlagDiscordWebhookDisconnect") == True:
        if cf.main_config.get("EFlagDiscordWebhookURL"):
            thumbnail_url = cf.main_config.get("EFlagCustomBootstrapInternetURL", f"{cf.main_host}/Images/DiscordIcon.png")
            server_location = ts("Unknown Location")
            start_time = 0
            place_info = {"name": "???"}

            if synced_place_info:
                if synced_place_info.get("start_time"): start_time = synced_place_info.get("start_time")
                if synced_place_info.get("server_location"): server_location = synced_place_info.get("server_location")
                if synced_place_info.get("place_info"): place_info = synced_place_info.get("place_info")
                if synced_place_info.get("thumbnail_url"): thumbnail_url = synced_place_info.get("thumbnail_url")

                server_type = ts("Public Server")
                if rcf.set_server_type == 0: server_type = ts("Public Server")
                elif rcf.set_server_type == 1: server_type = ts("Private Server")
                elif rcf.set_server_type == 2: server_type = ts("Reserved Server")
                elif rcf.set_server_type == 3: server_type = ts("Party Server")
                else: server_type = ts("Public Server")

                title = f"{ts('Disconnected from')} {server_type}!"
                color = 16711680
                if it_is_teleport == True: title = f"{ts('Teleported to')} {server_type}!"; color = 16776960

                launch_data = ""
                add_exam = False
                if launch_data != "":
                    launch_data = f"&launchData={launch_data}"
                    add_exam = False
                if (rcf.set_server_type == 1 or rcf.set_server_type == 2 or rcf.set_server_type == 3) and cf.main_config.get("EFlagAllowPrivateServerJoining") == True and rcf.set_current_private_server_key:
                    if add_exam == True: launch_data = f'{launch_data}?gameInstanceId={synced_place_info["jobId"]}?accessCode={rcf.set_current_private_server_key}'
                    else: launch_data = f'{launch_data}&gameInstanceId={synced_place_info["jobId"]}&accessCode={rcf.set_current_private_server_key}'
                else:
                    if add_exam == True: launch_data = f'{launch_data}?gameInstanceId={synced_place_info["jobId"]}'
                    else: launch_data = f'{launch_data}&gameInstanceId={synced_place_info["jobId"]}'

                user_connected_text = ts("Unknown User")
                if rcf.connected_user_info: user_connected_text = f'[@{rcf.connected_user_info["name"]} [{rcf.connected_user_info["id"]}]](https://www.roblox.com/users/{rcf.connected_user_info["id"]}/profile)'
                generated_body = generateDiscordPayload(title, color, [
                    generateEmbedField(ts("Disconnected Game"), f"[{place_info['name']}](https://www.roblox.com/games/{synced_place_info.get('placeId')})"),
                    generateEmbedField(ts("Join Link"), f"[{ts('Join Again!')}](https://rbx.efaz.dev/join?placeId={synced_place_info.get('placeId')}{launch_data})"),
                    generateEmbedField(ts("Started"), f"<t:{int(start_time)}:R>"),
                    generateEmbedField(ts("User Connected"), user_connected_text),
                    generateEmbedField(ts("Server Location"), f"{server_location}"),
                    generateEmbedField(ts("Closing Reason"), f"{info.get('message')} (Code: {info.get('code')})")
                ], thumbnail_url)
                try: sendDiscordWebhook(generated_body, "onGameDisconnected")
                except Exception:  printDebugMessage(f"There was an issue sending your webhook message. Exception: \n{trace()}")
    if cf.main_config.get("EFlagEnableDiscordRPC") == True:
        try: 
            if cf.discord_rpc: cf.discord_rpc.clear()
        except Exception: printDebugMessage(f"There was an error clearing Discord RPC: \n{trace()}")
        cf.discord_rpc_info = None
def onGameStart(info):
    if rcf.current_place_info: onGameDisconnected({"code": "285", "message": "Client/User issued disconnect."}); rcf.skip_disconnect_notification = True
    if info.get("placeId") and info.get("jobId"): rcf.current_place_info = info
def onTeleport(consoleLine): rcf.is_teleport = True
def onRobloxAppLoginFailed(consoleLine): rcf.is_app_login_fail = True
def onPrivateServer(data):
    rcf.set_server_type = 1
    if data and data.get("data"): rcf.set_current_private_server_key = data["data"].get("accessCode")
    else: rcf.set_current_private_server_key = None
def onReservedServer(data):
    rcf.set_server_type = 2
    if data and data.get("data"): rcf.set_current_private_server_key = data["data"].get("accessCode")
    else: rcf.set_current_private_server_key = None
def onPartyServer(data):
    rcf.set_server_type = 3
    if data and data.get("data"): rcf.set_current_private_server_key = data["data"].get("accessCode")
    else: rcf.set_current_private_server_key = None
def onMainServer(consoleLine):
    rcf.set_server_type = 0
    rcf.set_current_private_server_key = None
def onLoadedFFlags(data): printSuccessMessage("Roblox client has successfully loaded FFlags from local file!")
def onRobloxVoiceChatMute(data): printDebugMessage("Voice Chat microphone has been muted!")
def onRobloxVoiceChatUnmute(data): printDebugMessage("Voice Chat microphone has been unmuted!")
def onRobloxAppStart(consoleLine):
    thumbnail_url = getRobloxThumbnailURL()
    startDiscordRPC(thumbnail_url)
    if cf.main_config.get("EFlagUseDiscordWebhook") == True and cf.main_config.get("EFlagDiscordWebhookRobloxAppStart") == True:
        if cf.main_config.get("EFlagDiscordWebhookURL"):
            embed_fields = [
                generateEmbedField(ts("Connected PID"), rcf.connected_roblox_instance.pid),
                generateEmbedField(ts("Log Location"), rcf.connected_roblox_instance.log_file)
            ]
            generated_body = generateDiscordPayload((ts("Roblox Studio Started!") if cf.run_studio == True else ts("Roblox Started!")), (65535 if cf.run_studio == True else 6225823), embed_fields, thumbnail_url)
            try: sendDiscordWebhook(generated_body, "onRobloxStart")
            except Exception: printDebugMessage(f"There was an issue sending your webhook message. Exception: \n{trace()}")
def onRobloxCrash(consoleLine):
    rcf.connected_to_game = False
    rcf.updated_count = 999
    try: 
        if cf.discord_rpc: cf.discord_rpc.close()
    except Exception: printDebugMessage(f"There was an error closing Discord RPC: \n{trace()}")
    cf.discord_rpc = None
    cf.discord_rpc_info = None
    printErrorMessage(f"There was an error inside the {'RobloxStudio' if cf.run_studio == True else 'RobloxPlayer'} that has caused it to crash! Sorry!")
    printDebugMessage(f"Crashed Data: {consoleLine}")
    if cf.main_config.get("EFlagUseDiscordWebhook") == True and cf.main_config.get("EFlagDiscordWebhookRobloxCrash") == True and cf.main_config.get("EFlagDiscordWebhookURL"):
        thumbnail_url = getRobloxThumbnailURL()
        generated_body = generateDiscordPayload((ts(f"Uh oh! Roblox Studio Crashed!") if cf.run_studio == True else ts(f"Uh oh! Roblox Crashed!")), 0, [generateEmbedField(ts("Console Log"), consoleLine)], thumbnail_url)
        try: sendDiscordWebhook(generated_body, "onRobloxCrash")
        except Exception: printDebugMessage(f"There was an issue sending your webhook message. Exception: \n{trace()}")
def onRobloxExit(consoleLine):
    if rcf.is_app_login_fail == True: printDebugMessage(f"Roblox{' Studio' if cf.run_studio == True else ''} failed to launch login!")
    else: printDebugMessage(f"User has closed the Roblox{' Studio' if cf.run_studio == True else ''} window!")
    if rcf.connected_roblox_instance and rcf.connected_roblox_instance.created_mutex == True: printYellowMessage("This process is handling multi-instance for all open Roblox windows. If you close this window, all Roblox windows may close.")
    else: printErrorMessage(f"Roblox{' Studio' if cf.run_studio == True else ''} window was closed! Closing Bootstrap App..")
    if (cf.run_studio == False and cf.main_config.get("EFlagEnableDiscordRPC") == True) or (cf.run_studio == True and cf.main_config.get("EFlagEnableDiscordRPCStudio") == True):
        try: 
            if cf.discord_rpc: cf.discord_rpc.close()
        except Exception: printDebugMessage(f"There was an error closing Discord RPC: \n{trace()}")
        cf.discord_rpc = None
        cf.discord_rpc_info = None
    if cf.run_studio == False and cf.preserve_roblox == False and cf.main_config.get("EFlagEnableMultiAutoReconnect") == True and rcf.current_place_info and rcf.current_place_info.get("place_info") and rcf.current_place_info.get("placeId"): 
        printYellowMessage("Reconnecting Roblox..")
        if type(cf.main_config.get("EFlagRobloxLinkShortcuts")) is dict and rcf.connected_user_info and rcf.connected_user_info.get("id"):
            for i, v in cf.main_config.get("EFlagRobloxLinkShortcuts").items():
                if type(v.get("cookie_paths")) is dict and v.get("cookie_id") == rcf.connected_user_info.get("id"):
                    for d, k in v.get("cookie_paths").items():
                        if cf.main_os == "Darwin" and (d.startswith(os.path.join(cf.pip_class.getLocalAppData(), "HTTPStorages", "com.roblox.")) and k.startswith(os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "RBXCookies"))): cf.custom_cookies[d] = k
                        elif cf.main_os == "Windows" and (d == os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "LocalStorage", "RobloxCookies.dat") and k.startswith(os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "RBXCookies"))): cf.custom_cookies[d] = k
        if (rcf.set_server_type == 1 or rcf.set_server_type == 2 or rcf.set_server_type == 3) and rcf.set_current_private_server_key: launch_data = f'&accessCode={rcf.set_current_private_server_key}'
        else: launch_data = ""
        cf.given_args = ["Main.py", f"roblox://experiences/start?placeId={rcf.current_place_info.get('placeId')}&universeId={rcf.current_place_info.get('universeId')}&gameInstanceId={rcf.current_place_info['jobId']}{launch_data}"]
        return cf.restartRoblox()
    rcf.current_place_info = None
    if cf.main_config.get("EFlagUseDiscordWebhook") == True and cf.main_config.get("EFlagDiscordWebhookRobloxAppClose") == True:
        if rcf.connected_roblox_instance and rcf.connected_roblox_instance.log_file != "" and cf.main_config.get("EFlagDiscordWebhookURL"):
            title = ts("Roblox Studio Closed!") if cf.run_studio == True else ts("Roblox Closed!")
            color = 12076614 if cf.run_studio == True else 16735838
            thumbnail_url = getRobloxThumbnailURL()
            embed_fields = [
                generateEmbedField(ts("Disconnected PID"), rcf.connected_roblox_instance.pid),
                generateEmbedField(ts("Log Location"), rcf.connected_roblox_instance.log_file)
            ]
            if rcf.is_app_login_fail == True: title = ts("Roblox Failed Login!"); color = 13172807
            generated_body = generateDiscordPayload(title, color, embed_fields, thumbnail_url)
            try: sendDiscordWebhook(generated_body, "onRobloxExit")
            except Exception: printDebugMessage(f"There was an issue sending your webhook message. Exception: \n{trace()}")
def onBloxstrapMessage(info, disableWebhook=False):
    if (cf.run_studio == True and cf.main_config.get("EFlagAllowBloxstrapStudioSDK") == True) or (cf.run_studio == False and cf.main_config.get("EFlagAllowBloxstrapSDK") == True):
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
            if cf.discord_rpc_info == None: cf.discord_rpc_info = {}
            for i,v in cf.discord_rpc_info.items(): before_data[i] = v
            if info["command"] == "SetRichPresence":
                if cf.discord_rpc:
                    if cf.discord_rpc_info == None: cf.discord_rpc_info = {}
                    if type(info["data"]) is dict:
                        if info["data"].get("clear") == True or info["data"].get("reset") == True: cf.discord_rpc_info = {}
                        if type(info["data"].get("details")) is str or type(info["data"].get("details")) is None: 
                            cf.discord_rpc_info["details"] = info["data"].get("details")
                            passed_data[data_names["details"]] = info["data"].get("details")
                        if type(info["data"].get("state")) is str or type(info["data"].get("state")) is None: 
                            cf.discord_rpc_info["state"] = info["data"].get("state")
                            passed_data[data_names["state"]] = info["data"].get("state")
                        if type(info["data"].get("timeStart")) is int or type(info["data"].get("timeStart")) is None or type(info["data"].get("timeStart")) is float: 
                            cf.discord_rpc_info["start"] = info["data"].get("timeStart")
                            if type(info["data"].get("timeStart")) is None: passed_data[data_names["timeStart"]] = f'None'
                            else: passed_data[data_names["timeStart"]] = f'<t:{int(info["data"].get("timeStart"))}:R>'
                        if type(info["data"].get("timeEnd")) is int or type(info["data"].get("timeEnd")) is None or type(info["data"].get("timeEnd")) is float: 
                            cf.discord_rpc_info["stop"] = info["data"].get("timeEnd")
                            if type(info["data"].get("timeEnd")) is None: passed_data[data_names["timeEnd"]] = f'None'
                            else: passed_data[data_names["timeEnd"]] = f'<t:{int(info["data"].get("timeEnd"))}:R>'
                        def getImageUrlFromAsset(assetId):
                            url = f"https://thumbnails.roblox.com/v1/assets?assetIds={assetId}&returnPolicy=PlaceHolder&size=420x420&format=Png&isCircular=false"
                            thumb_req = cf.requests.get(url, loop_429=cf.main_config.get("EFlagEnableLoop429Requests")==True, cookies=createCookieHeader())
                            if thumb_req.ok:
                                thumb_js = thumb_req.json
                                if thumb_js and thumb_js.get("data"):
                                    if len(thumb_js.get("data")) > 0: return thumb_js.get("data")[0].get("imageUrl")
                                    else: return None
                                else: return None
                            else: return None
                        if type(info["data"].get("largeImage")) is dict: 
                            if info["data"]["largeImage"].get("clear") == True or info["data"]["largeImage"].get("reset") == True:
                                cf.discord_rpc_info["large_image"] = None
                                cf.discord_rpc_info["large_text"] = None
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
                                    except Exception: link = "None"
                                else: link = "None"
                                if approved_image: cf.discord_rpc_info["small_image"] = approved_image
                                if type(info["data"]["largeImage"].get("hoverText")) is str: cf.discord_rpc_info["large_text"] = info["data"]["largeImage"]["hoverText"]
                                passed_data[data_names["largeImage"]] = f'{info["data"]["largeImage"].get("hoverText", None)} | {link}'
                        elif type(info["data"].get("largeImage")) is None:
                            cf.discord_rpc_info["large_image"] = None
                            cf.discord_rpc_info["large_text"] = None
                            passed_data[data_names["largeImage"]] = f'None'
                        if type(info["data"].get("smallImage")) is dict: 
                            if info["data"]["smallImage"].get("clear") == True or info["data"]["smallImage"].get("reset") == True:
                                cf.discord_rpc_info["small_image"] = None
                                cf.discord_rpc_info["small_text"] = None
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
                                    except Exception: link = "None"
                                else: link = "None"
                                if approved_image: cf.discord_rpc_info["small_image"] = approved_image
                                if type(info["data"]["smallImage"].get("hoverText")) is str: cf.discord_rpc_info["small_text"] = info["data"]["smallImage"]["hoverText"]
                                passed_data[data_names["smallImage"]] = f'{info["data"]["smallImage"].get("hoverText", None)} | {link}'
                        elif type(info["data"].get("smallImage")) is None:
                            cf.discord_rpc_info["small_image"] = None
                            cf.discord_rpc_info["small_text"] = None
                            passed_data[data_names["smallImage"]] = f'None'
                        went_through = True
            elif info["command"] == "SetLaunchData":
                if cf.discord_rpc:
                    if cf.discord_rpc_info == None: cf.discord_rpc_info = {}
                    if type(info["data"]) is str: 
                        cf.discord_rpc_info["launch_data"] = info["data"]
                        passed_data[data_names["launch_data"]] = info["data"]
                    went_through = True
            if went_through == True and disableWebhook == False and cf.main_config.get("EFlagUseDiscordWebhook") == True and cf.main_config.get("EFlagDiscordWebhookBloxstrapRPC") == True:
                is_different = False
                for i,v in before_data.items():
                    if before_data.get(i) != cf.discord_rpc_info.get(i): is_different = True
                for i,v in cf.discord_rpc_info.items():
                    if before_data.get(i) != cf.discord_rpc_info.get(i): is_different = True
                if is_different == False: return
                if cf.main_config.get("EFlagDiscordWebhookURL"):
                    thumbnail_url = f"{cf.main_host}/Images/Bloxstrap.png"
                    embed_fields = [generateEmbedField(ts("Requested Command"), info["command"])]
                    for i, v in passed_data.items(): embed_fields.append(generateEmbedField(i, v))
                    generated_body = generateDiscordPayload(ts("Bloxstrap RPC Changed"), 12517631, embed_fields, thumbnail_url)
                    try: sendDiscordWebhook(generated_body, "onBloxstrapMessage")
                    except Exception: printDebugMessage(f"There was an issue sending your webhook message. Exception: \n{trace()}")
def onAllRobloxEvents(data):
    if cf.main_config.get("EFlagEnableMods") == True and cf.main_config.get("EFlagSelectedModScripts") and len(rcf.selected_mod_scripts) > 0:
        for s in rcf.selected_mod_scripts:
            if os.path.exists(os.path.join(cf.mods_folder, "Mods", s, "Manifest.json")) and rcf.mods_manifest.get(s) and rcf.mod_script_modules.get(s):
                if rcf.mods_manifest[s].get("mod_script") == True:
                    try:
                        allowed_permissions = rcf.mods_manifest[s].get("permissions")
                        if "onRobloxLog" in allowed_permissions and hasattr(rcf.mod_script_modules[s], "onRobloxLog"): cf.pip_class.startThread(getattr(rcf.mod_script_modules[s], "onRobloxLog"), True, data)
                        if data.get("eventName") in allowed_permissions and hasattr(rcf.mod_script_modules[s], data.get("eventName")): cf.pip_class.startThread(getattr(rcf.mod_script_modules[s], data.get("eventName")), True, data["data"])
                    except Exception: printDebugMessage(f"Something went wrong with pinging the Mod Script script: \n{trace()}")
def onRobloxChannel(data):
    if data["channel"] == "production" or data["channel"] == "LIVE": url_channel = ""
    else: url_channel = data["channel"]
    printDebugMessage(f"Setting Channel Based on Client: {'production' if url_channel == '' else url_channel}")
    if cf.main_os == "Darwin":
        res = cf.plist_class.writePListFile(os.path.join(cf.user_folder, "Library", "Preferences", "com.roblox.RobloxStudioChannel.plist" if cf.run_studio == True else "com.roblox.RobloxPlayerChannel.plist"), {"www.roblox.com": url_channel}, binary=True, ns_mode=True)
        printDebugMessage(f"Channel Set Result: {res}")
    elif cf.main_os == "Windows":
        reg = r"Software\ROBLOX Corporation\Environments\RobloxStudio\Channel" if cf.run_studio == True else r"Software\ROBLOX Corporation\Environments\RobloxPlayer\Channel"
        try: registry_key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, reg, 0, win32con.KEY_SET_VALUE)
        except Exception: registry_key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, reg)
        win32api.RegSetValueEx(registry_key, "www.roblox.com", 0, win32con.REG_SZ, url_channel)
        win32api.RegCloseKey(registry_key)

if __name__ == "__main__":
    print("This module is not a runable instance.")
    sys.exit(1)