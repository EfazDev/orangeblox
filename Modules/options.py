# 
# OrangeBlox 🍊
# Made by Efaz from efaz.dev
# v2.6.0i
# 

import Modules.config as cf
from Modules.printing import *
from Modules.startup import *
from Modules.utils import *
import os
import shutil
import json
import sys
import platform
import subprocess
import ctypes
import time
import re

def continueToRoblox(studio=False): # Continue to Roblox
    if studio == True:
        printSystemMessage("--- Continue to Roblox Studio ---")
        printMainMessage("Continuing to next stage!")
        cf.run_studio = True
    else:
        printSystemMessage("--- Continue to Roblox ---")
        printMainMessage("Continuing to next stage!")
def connectExistingRobloxWindow(studio=False): # Connect to Existing Roblox
    printSystemMessage(ts("--- Connect to Existing Roblox ---") if studio == False else ts("--- Connect to Existing Roblox Studio ---"))
    if cf.main_config.get("EFlagAllowActivityTracking") != False:
        if cf.handler.getIfRobloxIsOpen(studio=studio):
            cf.connect_instead = True
            if studio == True: cf.run_studio = True
            printMainMessage("Continuing to next stage!")
        else:
            printErrorMessage("There's currently no open Roblox Windows to connect to.")
            input("> ")
            sys.exit(0)
    else:
        printErrorMessage("Activity Tracking is not enabled.")
        input("> ")
        sys.exit(0)
def continueToRobloxManager(): # Run Fast Flag Installer
    if cf.main_config.get("EFlagDisableFastFlagInstallAccess") == True:
        printSystemMessage("--- Fast Flags Configurations ---")
        printErrorMessage("Access to editing FFlags settings was disabled by file. Please try again later!")
        input("> ")
        return ts("FFlag Settings was not saved!")
    printSystemMessage("--------------------")
    rbx.main()
    getSettings(updating=True)
    saveSettings()
def continueToOrangeBloxInstaller(): # Run OrangeBlox Installer
    printSystemMessage(f"--- Run {obName0()} Installer ---")
    generated_ui_options = []
    if checkSyncFolder():
        printMainMessage(f"Are you sure you want to run {obName0()} installer from installation folder?")
        generated_ui_options.append({
            "index": 1, 
            "message": ts(f"Yes"), 
            "func": lambda: None,
        })
        generated_ui_options.append({
            "index": 2, 
            "message": ts(f"Download & Run"), 
            "func": lambda: None,
        })
        generated_ui_options.append({
            "index": 3, 
            "message": ts(f"Download & Create"), 
            "func": lambda: None,
        })
    else:
        printMainMessage(f"Are you sure you want to run {obName0()} installer?")
        generated_ui_options.append({
            "index": 1, 
            "message": ts(f"Yes"), 
            "func": lambda: None,
        })
        generated_ui_options.append({
            "index": 3, 
            "message": ts(f"Download & Create"), 
            "func": lambda: None,
        })
    op = generateMenuSelection(generated_ui_options, star_option=ts("No"))
    if not op: op = 0
    else: op = op["index"]
    def download_option():
        if cf.pip_class.getIfConnectedToInternet():
            printDebugMessage("Setting Installed App Path to Local User..") 
            if cf.main_os == "Darwin": setInstalledAppPath(os.path.realpath(os.path.join(cf.macos_app_path, "../") + "/"))
            elif cf.main_os == "Windows": setInstalledAppPath(cf.cur_path)
            printDebugMessage("Sending Request to Bootstrap Version Servers..") 
            version_server = cf.main_config.get("EFlagBootstrapUpdateServer", "https://obx.efaz.dev/Version.json")
            if not (type(version_server) is str and version_server.startswith("https://")): version_server = "https://obx.efaz.dev/Version.json"
            try: latest_vers_res = cf.requests.get(f"{version_server}", headers={"X-Bootstrap-Version": cf.current_version["version"], "X-Python-Version": platform.python_version(), "X-Authorization-Key": cf.main_config.get("EFlagUpdatesAuthorizationKey", "")})
            except Exception: latest_vers_res = PyKits.InstantRequestJSONResponse(ok=False)
            if latest_vers_res.ok:
                latest_vers = latest_vers_res.json
                download_location = latest_vers.get("download_location", "https://github.com/EfazDev/orangeblox/archive/refs/heads/main.zip")
                possible_download_path = os.path.join(cf.user_folder, f"OrangeBlox_v{latest_vers['latest_version']}.zip")
                if download_location == "https://github.com/EfazDev/orangeblox/archive/refs/heads/main.zip":
                    download_location = f"https://github.com/EfazDev/orangeblox/releases/download/v{latest_vers['latest_version']}/OrangeBlox-v{latest_vers['latest_version']}.zip"
                    printSuccessMessage("✅ This version is a public update available on GitHub for viewing.")
                    printSuccessMessage("✅ For information about this update, use this link: https://github.com/EfazDev/orangeblox/releases")
                    printSuccessMessage(f"✅ Download location: {download_location} => {possible_download_path}")
                elif download_location == "https://github.com/EfazDev/orangeblox/archive/refs/heads/beta.zip":
                    download_location = f"https://github.com/EfazDev/orangeblox/releases/download/v{latest_vers['latest_version']}/OrangeBlox-v{latest_vers['latest_version']}.zip"
                    printYellowMessage(f"⚠️ This version is a beta version of {obName0()} and may cause issues with your installation.")
                    printYellowMessage("⚠️ For information about this update, use this link: https://github.com/EfazDev/orangeblox/releases")
                    printYellowMessage(f"⚠️ Download location: {download_location} => {possible_download_path}")
                elif cf.main_config.get("EFlagUpdatesAuthorizationKey", "") != "":
                    printYellowMessage("🔨 This version is an update configured from an organization (this may still be a modified and an unofficial OrangeBlox version.)")
                    printYellowMessage("🔨 For information about this update, contact your administrator!")
                    printYellowMessage(f"🔨 Download location: {download_location} => {possible_download_path}")
                else:
                    printErrorMessage("❌ The download location is different from the official GitHub link!")
                    printErrorMessage(f"❌ You may be downloading an unofficial {obName0()} version! Download a copy from https://github.com/EfazDev/orangeblox!")
                    printErrorMessage(f"❌ Download location: {download_location} => {possible_download_path}")
                printMainMessage(f"Are you sure you would like to continue through downloading {obName0()} installer? (y/n)")
                a = input("> ")
                if (isYes(a) == True):
                    dow_tar = None
                    if op == "c":
                        printMainMessage(f"Please select your sync directory!")
                        custom_path = cf.file_selector.select_folder("Select the directory to create a sync directory to!", initialdir=cf.cur_path)
                        if custom_path and custom_path.ok: dow_tar = custom_path.path
                    else: dow_tar = os.path.join(cf.user_folder, f'OrangeBloxInstaller')
                    if dow_tar:
                        printDebugMessage(f"Saving Settings..")
                        saveSettings()
                        printMainMessage(f"Downloading Latest Version of {obName0()}..")
                        late_v = latest_vers.get("latest_version")
                        download_update = cf.requests.download(download_location, os.path.join(cf.user_folder, f'OrangeBlox_v{late_v}.zip'))
                        if download_update.ok:
                            printMainMessage("Download Success! Extracting ZIP now!")
                            zip_extract = cf.pip_class.unzipFile(os.path.join(cf.user_folder, f'OrangeBlox_v{late_v}.zip'), dow_tar, ["Main.py", "RobloxManager.py", "OrangeAPI.py", "Configuration.json", "Apps"])
                            if zip_extract.returncode == 0:                                                                                               
                                printMainMessage("Removing ZIP File..")
                                if os.path.exists(os.path.join(cf.user_folder, f'OrangeBlox_v{late_v}.zip')): os.remove(os.path.join(cf.user_folder, f'OrangeBlox_v{late_v}.zip'))
                                if op == "c":
                                    printMainMessage(f"Registering Sync Directory..")
                                    printDebugMessage(f'Sync Directory: {os.path.join(dow_tar)}')
                                    cf.main_config["EFlagOrangeBloxSyncDir"] = os.path.join(dow_tar)
                                    saveSettings()
                                    printSuccessMessage(f"{obName0()} Installer has been created successfully!")
                                    input("> ")
                                    return
                                else:
                                    temp_sync = False
                                    if not checkSyncFolder():
                                        printMainMessage(f"Registering Sync Directory..")
                                        printDebugMessage(f'Sync Directory: {os.path.join(dow_tar)}')
                                        cf.main_config["EFlagOrangeBloxSyncDir"] = os.path.join(dow_tar)
                                        saveSettings()
                                        temp_sync = True
                                    printMainMessage("Running Installer..")
                                    cf.stdout.clear()
                                    e = cf.stdout.run_process(args=[sys.executable, os.path.join(dow_tar, "Install.py")], cwd=dow_tar)
                                    if e.returncode == 0: printSuccessMessage(f"{obName0()} Installer has succeeded successfully! Once you continue, this script will reload.")
                                    else: printErrorMessage("The installer had a problem! Once you continue, this script will reload.")
                                    if temp_sync == False and os.path.exists(dow_tar): 
                                        if os.path.exists(os.path.join(dow_tar, "Backup.obx")): shutil.move(os.path.join(dow_tar, "Backup.obx"), os.path.join(cf.user_folder, "Documents", "OrangeBlox_Backup.obx"))
                                        shutil.rmtree(dow_tar, ignore_errors=True)
                                    input("> ")
                                    cf.pip_class.restartScript("Main.py", sys.argv)
                                    sys.exit(0)
                                    return
                            else:
                                printErrorMessage(f"There was an issue trying to unpack the {obName0()} installation folder!")
                                return ts(f"{obName0()} Installer task was canceled!")
                        else:
                            printErrorMessage(f"There was an issue trying to download {obName0()} from the download server!")
                            return ts(f"{obName0()} Installer task was canceled!")
                    else: return ts(f"{obName0()} Installer task was canceled!")
                else: return ts(f"{obName0()} Installer task was canceled!")
            else:
                printErrorMessage(f"There was an issue trying to fetch {obName0()} information!")
                return ts(f"{obName0()} Installer task was canceled!")
        else:
            printErrorMessage("Please connect to your internet in order to use this action!")
            return ts(f"{obName0()} Installer task was canceled!")
    if op == 1:
        if checkSyncFolder():
            printMainMessage("Running Installer..")
            cf.stdout.clear()
            e = cf.stdout.run_process(args=[sys.executable, os.path.join(cf.main_config.get("EFlagOrangeBloxSyncDir"), "Install.py")], cwd=cf.main_config.get("EFlagOrangeBloxSyncDir"))
            if e.returncode == 0: printSuccessMessage(f"{obName0()} Installer has succeeded successfully! Once you continue, this script will reload.")
            else: printErrorMessage("The installer had a problem! Once you continue, this script will reload.")
            input("> ")
            cf.pip_class.restartScript("Main.py", sys.argv)
            sys.exit(0)
            return
        else: return download_option()
    elif op == 2 or op == 3: return download_option()
    else: return ts(f"{obName0()} Installer task was canceled!")
def continueToClearTemporaryStorage(): # Clear Temporary Storage
    installer_paths = [os.path.join(cf.cur_path, 'RobloxPlayerInstaller.exe'), os.path.join(cf.cur_path, 'RobloxStudioInstaller.exe'), os.path.join(cf.orangeblox_library, 'RobloxPlayerInstaller.app'), os.path.join(cf.orangeblox_library, 'RobloxStudioInstaller.app')]
    bootstrap_image_needed_files = ["AppIcon.icns", "AppIcon.ico", "AppIcon.png", "OrangeBlox.terminal", "AppIconPlayRoblox.icns", "AppIconPlayRoblox.ico", "AppIconRunStudio.icns", "AppIconRunStudio.ico", "AppIcon64.png"]
    orangeblox_log_path = os.path.join(cf.cur_path, "Logs")
    if cf.main_os == "Darwin": orangeblox_log_path = os.path.join(cf.pip_class.getLocalAppData(), "Logs", "OrangeBlox")
    def pythonCacheAvailableToClear():
        cache_detected = []
        for dirpath, dirnames, filenames in os.walk(cf.cur_path):
            if "__pycache__" in dirnames: cache_detected.append(os.path.join(dirpath, "__pycache__"))
        if cf.main_os == "Darwin" and os.path.exists(os.path.join(cf.cur_path, "VirtualEnvironments")): cache_detected.append(os.path.join(cf.cur_path, "VirtualEnvironments"))
        return cache_detected
    def appLocksAvailableToClear():
        locks_detected = []
        for i in os.listdir(cf.cur_path):
            if i.endswith(f"_{cf.user_folder_name}"): locks_detected.append(os.path.join(cf.cur_path, i))
            elif i.startswith("Terminal_") or i == "BootstrapCooldown": locks_detected.append(os.path.join(cf.cur_path, i))
        if cf.main_os == "Darwin" and os.path.exists(cf.orangeblox_library):
            for i in os.listdir(cf.orangeblox_library):
                if not "." in i and os.path.isfile(os.path.join(cf.orangeblox_library, i)): locks_detected.append(os.path.join(cf.orangeblox_library, i))
                elif i.startswith("Terminal_") or i == "BootstrapCooldown": locks_detected.append(os.path.join(cf.orangeblox_library, i))
        return locks_detected
    def bootstrapImagesAvailableToClear():
        images_detected = []
        for i in os.listdir(os.path.join(cf.cur_path, "Images")):
            if not i in bootstrap_image_needed_files: images_detected.append(os.path.join(cf.cur_path, "Images", i))
        return images_detected
    def unneededModsAvailableToClear():
        unneeded_detected = []
        for i in os.listdir(os.path.join(cf.mods_folder, "Mods")):
            if os.path.isfile(os.path.join(cf.mods_folder, "Mods", i)): unneeded_detected.append(os.path.join(cf.mods_folder, "Mods", i))
            elif i == "GothamFont": unneeded_detected.append(os.path.join(cf.mods_folder, "Mods", i))
        return unneeded_detected
    def robloxFilesAvailableToClear():
        files = []
        for i in os.listdir(cf.versions_folder):
            if i.endswith(".zip"): files.append(os.path.join(cf.versions_folder, i))
        if cf.main_os == "Darwin" and os.path.exists(os.path.join(cf.cur_path, "Versions")): files.append(os.path.join(cf.cur_path, "Versions"))
        return files
    def getTotalClearableSize(): return getRobloxLogFolderSize(static=True) + getFolderSize(orangeblox_log_path, formatWithAbbreviation=False) + getFileSize(installer_paths, formatWithAbbreviation=False) + getFileSize(pythonCacheAvailableToClear(), formatWithAbbreviation=False) + getFileSize(bootstrapImagesAvailableToClear(), formatWithAbbreviation=False) + getFileSize(unneededModsAvailableToClear(), formatWithAbbreviation=False) + getFileSize(robloxFilesAvailableToClear(), formatWithAbbreviation=False) + getFileSize(appLocksAvailableToClear(), formatWithAbbreviation=False)
    def continueToClearLogs(clearAll=False): # Clear All Roblox Logs
        printSystemMessage("--- Clear All Roblox Logs ---")
        if cf.handler.getIfRobloxIsOpen() == True:
            printErrorMessage("We can't clear logs if Roblox is currently open! Please close it before trying again!")
            input("> ")
            return ts("Clearing Logs failed.")
        else:
            printMainMessage(f"Are you sure you want to clear all Roblox logs ({getRobloxLogFolderSize()}) (y/n)?")
            if clearAll == True or isYes(input("> ")) == True:
                if cf.handler.getIfRobloxIsOpen() == True:
                    printErrorMessage("We can't clear logs if Roblox is currently open! Please close it before trying again!")
                    input("> ")
                    return ts("Clearing Logs failed.")
                else:
                    if cf.main_os == "Darwin":
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
                    elif cf.main_os == "Windows":
                        log_path = os.path.join(rbx.windows_dir, "logs")
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
        printSystemMessage(f"--- Clear All {obName0()} Logs ---")
        printMainMessage(f"Are you sure you want to clear all {obName0()} logs ({getFolderSize(orangeblox_log_path)}) (y/n)?")
        if clearAll == True or isYes(input("> ")) == True:
            for i in os.listdir(orangeblox_log_path):
                try:
                    if os.path.isfile(os.path.join(orangeblox_log_path, i)): os.remove(os.path.join(orangeblox_log_path, i))
                except Exception: printDebugMessage(f"Unable to remove log: {i}")
            return ts(f"Successfully cleared {obName0()} logs!")
        else: return ts("Clearing Logs canceled.")
    def continueToClearPyCache(clearAll=False): # Clear Python Cache
        printSystemMessage("--- Clear Python Cache ---")
        printMainMessage(f"Are you sure you want to clear Python cache ({getFileSize(pythonCacheAvailableToClear())}) (y/n)?")
        if clearAll == True or isYes(input("> ")) == True:
            for i in pythonCacheAvailableToClear():
                if os.path.exists(i): 
                    if os.path.isdir(i): printDebugMessage(f"Removing {i}.."); shutil.rmtree(i, ignore_errors=True)
                    else: printDebugMessage(f"Removing {i}.."); os.remove(i)
            return ts("Successfully cleared Python cache!")
        else: return ts("Clearing cache canceled.")
    def continueToClearRobloxInstallers(clearAll=False): # Clear Roblox Installers
        printSystemMessage("--- Clear Roblox Installers ---")
        printMainMessage(f"Are you sure you want to clear Roblox Installers ({getFileSize(installer_paths)}) (y/n)?")
        if clearAll == True or isYes(input("> ")) == True:
            for i in installer_paths:
                if os.path.exists(i): printDebugMessage(f"Removing {i}.."); shutil.rmtree(i, ignore_errors=True)
            return ts("Successfully cleared Roblox Installers!")
        else: return ts("Clearing installers canceled.")
    def continueToClearBootstrapImages(clearAll=False): # Clear Bootstrap Images
        printSystemMessage("--- Clear Bootstrap Images ---")
        printMainMessage(f"Are you sure you want to clear Bootstrap images ({getFileSize(bootstrapImagesAvailableToClear())}) (y/n)?")
        if clearAll == True or isYes(input("> ")) == True:
            for i in bootstrapImagesAvailableToClear():
                if os.path.exists(i): 
                    if os.path.isdir(i): printDebugMessage(f"Removing {i}.."); shutil.rmtree(i, ignore_errors=True)
                    else: printDebugMessage(f"Removing {i}.."); os.remove(i)
            return ts("Successfully cleared Bootstrap Images!")
        else: return ts("Clearing bootstrap images canceled.")
    def continueToClearDownloadedRobloxFiles(clearAll=False): # Clear Downloaded Roblox Files
        printSystemMessage("--- Clear Downloaded Roblox Files ---")
        printMainMessage(f"Are you sure you want to clear downloaded Roblox files from {obName0()} ({getFileSize(robloxFilesAvailableToClear())}) (y/n)?")
        if clearAll == True or isYes(input("> ")) == True:
            for i in robloxFilesAvailableToClear():
                if os.path.exists(i): 
                    if os.path.isdir(i): printDebugMessage(f"Removing {i}.."); shutil.rmtree(i, ignore_errors=True)
                    else: printDebugMessage(f"Removing {i}.."); os.remove(i)
            return ts(f"Successfully cleared Downloaded Roblox Files from {obName0()}!")
        else: return ts("Clearing files canceled.")
    def continueToClearUnneededMods(clearAll=False): # Clear Unneeded Mods
        printSystemMessage("--- Clear Unneeded Mods ---")
        printMainMessage(f"Are you sure you want to clear unneeded mods ({getFileSize(unneededModsAvailableToClear())}) (y/n)?")
        if clearAll == True or isYes(input("> ")) == True:
            for i in unneededModsAvailableToClear():
                if os.path.exists(i): 
                    if os.path.isdir(i): printDebugMessage(f"Removing {i}.."); shutil.rmtree(i, ignore_errors=True)
                    else: printDebugMessage(f"Removing {i}.."); os.remove(i)
            return ts("Successfully cleared unneeded mods!")
        else: return ts("Clearing mods canceled.")
    def continueToClearAppLocks(clearAll=False): # Clear App Locks
        printSystemMessage("--- Clear App Locks ---")
        printMainMessage(f"Are you sure you want to clear app locks ({getFileSize(appLocksAvailableToClear())}) (y/n)?")
        if clearAll == True or isYes(input("> ")) == True:
            for i in appLocksAvailableToClear():
                if os.path.exists(i): 
                    if os.path.isdir(i): printDebugMessage(f"Removing {i}.."); shutil.rmtree(i, ignore_errors=True)
                    else: printDebugMessage(f"Removing {i}.."); os.remove(i)
            return ts("Successfully cleared app locks!")
        else: return ts("Clearing app locks canceled.")
    def continueToClearAllUnneededFiles():
        printSystemMessage("--- Clear All Unneeded Files ---")
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
    printSystemMessage("--- Clear Temporary Storage ---")
    printMainMessage(f"Select which option you would like to do! (Total Size of Clearable Files: {formatSize(getTotalClearableSize())})")
    generated_ui_options = []
    generated_ui_options.append({
        "index": 1, 
        "message": ts(f"Clear Roblox Logs ({getRobloxLogFolderSize()})"), 
        "func": continueToClearLogs,
    })
    generated_ui_options.append({
        "index": 2, 
        "message": ts(f"Clear {obName0()} Logs ({getFolderSize(orangeblox_log_path)})"), 
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
    d = generateMenuSelection(generated_ui_options, star_option=ts("Exit Storage Management"))
    if d: d["func"](); return continueToClearTemporaryStorage()
    else: return ts("Temporary storage has been cleared!")
def continueToEndRobloxInstances(studio=False): # End All Roblox Instances
    printSystemMessage(ts("--- End All Roblox Instances ---") if studio == False else ts("--- End All Roblox Studio Instances ---"))
    printMainMessage("Are you sure you want to end all currently open Roblox instances? (y/n)"if studio == False else "Are you sure you want to end all currently open Roblox Studio instances? (y/n)")
    a = input("> ")
    if isYes(a) == True:
        cf.handler.endRoblox(studio=studio)
        return ts("Successfully closed all open Roblox windows!")
    else: return ts("Roblox closing task has been canceled!")  
def continueToInstallRobloxOptions(reinstall=False): # Roblox Installer Options
    def goToReinstall(fullReset=0):
        printSystemMessage("--- Reinstall Roblox ---")
        if fullReset == 8: printMainMessage("Are you sure you want to reinstall Vanilla Roblox Studio? (y/n)")
        elif fullReset == 7: printMainMessage("Are you sure you want to reinstall Vanilla Roblox? (y/n)")
        elif fullReset == 6: printMainMessage("Are you sure you want to reinstall Roblox Studio? (y/n)")
        elif fullReset == 5: printMainMessage("...")
        elif fullReset == 4: printMainMessage("...")
        elif fullReset == 3: printMainMessage("Are you sure you want to fully reinstall Roblox and REMOVE your user data? (y/n)")
        elif fullReset == 2: printMainMessage("Are you sure you want to fully reinstall Roblox? (y/n)")
        else: printMainMessage("Are you sure you want to reinstall Roblox? (y/n)")
        if cf.main_os == "Windows": printYellowMessage("WARNING! This may force-quit any open Roblox windows!")
        a = input("> ")
        if isYes(a) == True:
            if fullReset == 8:
                cla = cf.handler.temporaryResetCustomizableVariables()
                cf.submit_status.start()
                res = cf.handler.installRoblox(studio=True, debug=cf.main_config.get("EFlagEnableDebugMode"), copyRobloxInstallerPath=(os.path.join(cf.orangeblox_library, "RobloxStudioInstaller.app") if cf.main_os == "Darwin" else os.path.join(cf.cur_path, "RobloxStudioInstaller.exe")), downloadInstaller=True, disableRobloxAutoOpen=True, downloadToken=createDownloadToken(studio=True))
                cf.submit_status.end()
                cla.set()
                return (ts("Vanilla Roblox Studio has been installed!") if res and res["success"] == True else ts("Vanilla Roblox Studio has not been installed!"))
            elif fullReset == 7:
                cla = cf.handler.temporaryResetCustomizableVariables()
                cf.submit_status.start()
                res = cf.handler.installRoblox(debug=cf.main_config.get("EFlagEnableDebugMode"), copyRobloxInstallerPath=(os.path.join(cf.orangeblox_library, "RobloxPlayerInstaller.app") if cf.main_os == "Darwin" else os.path.join(cf.cur_path, "RobloxPlayerInstaller.exe")), downloadInstaller=True, disableRobloxAutoOpen=True, downloadToken=createDownloadToken(studio=False))
                cf.submit_status.end()
                cla.set()
                return (ts("Vanilla Roblox has been installed!") if res and res["success"] == True else ts("Vanilla Roblox has not been installed!"))
            elif fullReset == 6:
                cf.submit_status.start()
                res = cf.handler.installRoblox(studio=True, debug=cf.main_config.get("EFlagEnableDebugMode"), disableRobloxAutoOpen=True, downloadToken=createDownloadToken(studio=True))
                cf.submit_status.end()
                return (ts("Roblox Studio has been reinstalled!") if res and res["success"] == True else ts("Roblox Studio has not been installed!"))
            elif fullReset == 3:
                cf.submit_status.start()
                res = cf.handler.reinstallRoblox(debug=(cf.main_config.get("EFlagEnableDebugMode") == True), clearUserData=True, disableRobloxAutoOpen=True, downloadToken=createDownloadToken(studio=False))
                cf.submit_status.end()
                return (ts("Roblox has been reinstalled fully with user data removed!") if res and res["success"] == True else ts("Roblox has not been installed!"))
            elif fullReset == 2:
                cf.submit_status.start()
                res = cf.handler.reinstallRoblox(debug=(cf.main_config.get("EFlagEnableDebugMode") == True), clearUserData=False, downloadToken=createDownloadToken(studio=False))
                cf.submit_status.end()
                return (ts("Roblox has been reinstalled fully with no user data removed!") if res and res["success"] == True else ts("Roblox has not been installed!"))
            else:
                cf.submit_status.start()
                res = cf.handler.installRoblox(debug=(cf.main_config.get("EFlagEnableDebugMode") == True), verifyInstall=cf.main_config.get("EFlagVerifyRobloxHashAfterInstall") != False, downloadToken=createDownloadToken(studio=False))
                cf.submit_status.end()
                return (ts("Roblox has been reinstalled!") if res and res["success"] == True else ts("Roblox has not been installed!"))
        else: return ts("Roblox reinstallation has been canceled!")
    def goToUninstall(fullReset=0):
        printSystemMessage("--- Uninstall Roblox ---")
        if cf.main_os == "Darwin":
            if not os.path.exists(os.path.join(cf.pip_class.getInstallableApplicationsFolder(), "Roblox.app")) and fullReset == 7:
                printErrorMessage("Vanilla Roblox is not installed right now! Please install it from the Roblox website to get it back!")
                return ts("Roblox was not uninstalled.")
            elif not os.path.exists(os.path.join(cf.pip_class.getInstallableApplicationsFolder(), "RobloxStudio.app")) and fullReset == 8:
                printErrorMessage("Vanilla Roblox Studio is not installed right now! Please install it from the Roblox website to get it back!")
                return ts("Roblox Studio was not uninstalled.")
        elif cf.main_os == "Windows":
            if not cf.handler.getRobloxInstallFolder(directory=os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "Versions")) and fullReset == 7:
                printErrorMessage("Vanilla Roblox is not installed right now! Please install it from the Roblox website to get it back!")
                return ts("Roblox was not uninstalled.")
            elif not cf.handler.getRobloxInstallFolder(directory=os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "Versions"), studio=True) and fullReset == 8:
                printErrorMessage("Vanilla Roblox Studio is not installed right now! Please install it from the Roblox website to get it back!")
                return ts("Roblox Studio was not uninstalled.")
            
        if fullReset == 4: printMainMessage("Are you sure you want to uninstall Roblox? (y/n)")
        elif fullReset == 5: printMainMessage("Are you sure you want to uninstall Roblox and REMOVE your user data? (y/n)")
        elif fullReset == 6: printMainMessage(f"Are you sure you want to uninstall Roblox Studio from {obName0()}? (y/n)")
        elif fullReset == 7: printMainMessage("Are you sure you want to uninstall Vanilla Roblox from your system? (y/n)")
        elif fullReset == 8: printMainMessage("Are you sure you want to uninstall Vanilla Roblox Studio from your system? (y/n)")
        else: printMainMessage("Are you sure you want to uninstall Roblox? (y/n)")
        printYellowMessage("WARNING! This will force-quit any open Roblox windows!")
        a = input("> ")
        if isYes(a) == True:
            if fullReset == 5:
                cf.submit_status.start()
                cf.handler.uninstallRoblox(debug=(cf.main_config.get("EFlagEnableDebugMode") == True), clearUserData=True)
                cf.submit_status.end()
                printSuccessMessage(f"Roblox has been uninstalled successfully! However, if you don't have vanilla Roblox installed, then you won't be able to play Roblox until you reopen {obName0()}. Keep a mind at that!")
                input("> ")
                sys.exit(0)
                return ts("Roblox has been uninstalled with user data removed!")
            elif fullReset == 6:
                if not (cf.handler.getRobloxInstallFolder(directory="", studio=True)):
                    printErrorMessage("Roblox Studio is not installed right now! Please enable Roblox Studio mode in Bootstrap Settings to reinstall back!")
                    return ts("Roblox Studio was not uninstalled.")
                cf.submit_status.start()
                cf.handler.uninstallRoblox(studio=True, debug=(cf.main_config.get("EFlagEnableDebugMode") == True), clearUserData=False)
                cf.submit_status.end()
                if cf.main_os == "Windows":
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
                        
                    cur_studio = cf.handler.getRobloxInstallFolder(directory=os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "Versions"), studio=True)
                    if cur_studio:
                        rbx_studio_beta = os.path.join(cur_studio, "RobloxStudioBeta.exe")
                        set_url_scheme("roblox-studio", rbx_studio_beta)
                        set_url_scheme("roblox-studio-auth", rbx_studio_beta)
                        set_file_type_reg(".rbxl", rbx_studio_beta, "Roblox Place")
                        set_file_type_reg(".rbxlx", rbx_studio_beta, "Roblox Place")
                return ts("Roblox Studio has been uninstalled!")
            elif fullReset == 7:
                if cf.main_os == "Darwin":
                    if not (os.path.exists(os.path.join(cf.pip_class.getInstallableApplicationsFolder(), "Roblox.app"))):
                        printErrorMessage("Vanilla Roblox is not installed right now! Please install it from the Roblox website to get it back!")
                        return ts("Roblox was not uninstalled.")
                    shutil.rmtree(os.path.join(cf.pip_class.getInstallableApplicationsFolder(), "Roblox.app"), ignore_errors=True)
                    printSuccessMessage("Vanilla Roblox has been uninstalled successfully!")
                    input("> ")
                    return ts("Vanilla Roblox has been uninstalled!")
                elif cf.main_os == "Windows":
                    org_dir = os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "Versions")
                    if not (cf.handler.getRobloxInstallFolder(directory=org_dir)):
                        printErrorMessage("Vanilla Roblox is not installed right now! Please install it from the Roblox website to get it back!")
                        return ts("Roblox was not uninstalled.")
                    for i in os.listdir(org_dir):
                        if os.path.exists(os.path.join(org_dir, i)) and os.path.isdir(os.path.join(org_dir, i)):
                            if os.path.exists(os.path.join(org_dir, i, "RobloxPlayerBeta.exe")):     shutil.rmtree(os.path.join(org_dir, i), ignore_errors=True)
                    printSuccessMessage("Vanilla Roblox has been uninstalled successfully!")
                    input("> ")
                    return ts("Vanilla Roblox has been uninstalled!")
            elif fullReset == 8:
                if cf.main_os == "Darwin":
                    if not (os.path.exists(os.path.join(cf.pip_class.getInstallableApplicationsFolder(), "RobloxStudio.app"))):
                        printErrorMessage("Vanilla Roblox Studio is not installed right now! Please install it from the Roblox website to get it back!")
                        return ts("Roblox Studio was not uninstalled.")
                    shutil.rmtree(os.path.join(cf.pip_class.getInstallableApplicationsFolder(), "RobloxStudio.app"), ignore_errors=True)
                    printSuccessMessage("Vanilla Roblox Studio has been uninstalled successfully!")
                    input("> ")
                    return ts("Vanilla Roblox Studio has been uninstalled!")
                elif cf.main_os == "Windows":
                    org_dir = os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "Versions")
                    if not (cf.handler.getRobloxInstallFolder(directory=org_dir, studio=True)):
                        printErrorMessage("Vanilla Roblox Studio is not installed right now! Please install it from the Roblox website to get it back!")
                        return ts("Roblox Studio was not uninstalled.")
                    for i in os.listdir(org_dir):
                        if os.path.exists(os.path.join(org_dir, i)) and os.path.isdir(os.path.join(org_dir, i)):
                            if os.path.exists(os.path.join(org_dir, i, "RobloxStudioBeta.exe")):     shutil.rmtree(os.path.join(org_dir, i), ignore_errors=True)
                    printSuccessMessage("Vanilla Roblox Studio has been uninstalled successfully!")
                    input("> ")
                    return ts("Vanilla Roblox Studio has been uninstalled!")
            else:
                cf.submit_status.start()
                cf.handler.uninstallRoblox(debug=(cf.main_config.get("EFlagEnableDebugMode") == True), clearUserData=False)
                cf.submit_status.end()
                printSuccessMessage(f"Roblox has been uninstalled successfully! However, if you don't have vanilla Roblox installed, then you won't be able to play Roblox until you reopen {obName0()}. Keep a mind at that!")
                input("> ")
                sys.exit(0)
                return ts("Roblox has been uninstalled!")
        else: return ts("Roblox reinstallation has been canceled!")
    if reinstall == True: return goToReinstall()
    else:
        printSystemMessage("--- Roblox Installer Options ---")
        li = {}
        co = 1
        printMainMessage(f"[{co}] Reinstall Roblox")
        li[str(co)] = [goToReinstall, 1]
        co += 1
        printMainMessage(f"[{co}] Full Reinstall Roblox [No Resetting]")
        li[str(co)] = [goToReinstall, 2]
        co += 1
        printMainMessage(f"[{co}] Full Reinstall Roblox [Removes User Data]")
        li[str(co)] = [goToReinstall, 3]
        co += 1
        printMainMessage(f"[{co}] Install Vanilla Roblox")
        li[str(co)] = [goToReinstall, 7]
        if cf.main_config.get("EFlagRobloxStudioEnabled"):
            co += 1
            printMainMessage(f"[{co}] Reinstall Roblox Studio")
            li[str(co)] = [goToReinstall, 6]
            if cf.main_os == "Darwin":
                co += 1
                printMainMessage(f"[{co}] Install Vanilla Roblox Studio")
                li[str(co)] = [goToReinstall, 8]
                if os.path.exists(os.path.join(cf.pip_class.getInstallableApplicationsFolder(), "RobloxStudio.app")): 
                    co += 1
                    printMainMessage(f"[{co}] Uninstall Vanilla Roblox Studio")
                    li[str(co)] = [goToUninstall, 8]
            elif cf.main_os == "Windows":
                co += 1
                printMainMessage(f"[{co}] Install Vanilla Roblox Studio")
                li[str(co)] = [goToReinstall, 8]
                if cf.handler.getRobloxInstallFolder(directory=os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "Versions"), studio=True): 
                    co += 1
                    printMainMessage(f"[{co}] Uninstall Vanilla Roblox Studio")
                    li[str(co)] = [goToUninstall, 8]
        co += 1
        printMainMessage(f"[{co}] Uninstall Roblox")
        li[str(co)] = [goToUninstall, 4]
        co += 1
        printMainMessage(f"[{co}] Uninstall Roblox [Removes User Data]")
        li[str(co)] = [goToUninstall, 5]
        current_studio_version = cf.handler.getCurrentClientVersion(studio=True)
        if current_studio_version["success"] == True:
            co += 1
            printMainMessage(f"[{co}] Uninstall Roblox Studio")
            li[str(co)] = [goToUninstall, 6]
        if cf.main_os == "Darwin":
            if os.path.exists(os.path.join(cf.pip_class.getInstallableApplicationsFolder(), "Roblox.app")): 
                co += 1
                printMainMessage(f"[{co}] Uninstall Vanilla Roblox")
                li[str(co)] = [goToUninstall, 7]
        elif cf.main_os == "Windows":
            if cf.handler.getRobloxInstallFolder(directory=os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "Versions")): 
                co += 1
                printMainMessage(f"[{co}] Uninstall Vanilla Roblox")
                li[str(co)] = [goToUninstall, 7]
        printMainMessage("[*] Exit Options Menu")
        a = input("> ")
        if li.get(a): return li.get(a)[0](li.get(a)[1])
        else: return ts("Option invalid!")
def syncToFFlagConfiguration(): # Sync to Configuration
    printSystemMessage("--- Sync to Configuration ---")
    printMainMessage(f"Are you sure you want to save your Configuration into the Configuration.json file in your installation folder (y/n)?")
    a = input("> ")
    if isYes(a) == True:
        printMainMessage("Validating Bootstrap Install Directory..")
        if checkSyncFolder():
            if os.path.exists(os.path.join(cf.main_config.get("EFlagOrangeBloxSyncDir"), "Configuration.json")):
                printDebugMessage(f"Saving to {os.path.join(cf.main_config.get('EFlagOrangeBloxSyncDir'), 'Configuration.json')}..")
                with open(os.path.join(cf.main_config.get("EFlagOrangeBloxSyncDir"), "Configuration.json"), "w", encoding="utf-8") as f: json.dump(cf.main_config, f, indent=4)
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
    printSystemMessage("--- Sync from Configuration ---")
    printMainMessage(f"Are you sure you want to load your Configuration from the Configuration.json file in your installation folder (y/n)?")
    printErrorMessage("This will override any configuration changes inside this state to this file.")
    a = input("> ")
    if isYes(a) == True:
        printMainMessage("Validating Bootstrap Install Directory..")
        if checkSyncFolder():
            if os.path.exists(os.path.join(cf.main_config.get("EFlagOrangeBloxSyncDir"), "Configuration.json")):
                printDebugMessage(f"Loading from {os.path.join(cf.main_config.get('EFlagOrangeBloxSyncDir'), 'Configuration.json')}..")
                with open(os.path.join(cf.main_config.get("EFlagOrangeBloxSyncDir"), "Configuration.json"), "r", encoding="utf-8") as f: fromFastFlagConfig = json.load(f)
                if len(fromFastFlagConfig) < 10:
                    printYellowMessage(f"This configuration contains less than 10 items. Are you REALLY sure that you want to sync with this file? (y/n)?")
                    printErrorMessage("This can make you lose existing data on this bootstrap which could affect your experience.")
                    if isYes(input("> ")) == False: return ts("Syncing was rejected!")
                fromFastFlagConfig["EFlagOrangeBloxSyncDir"] = cf.main_config.get("EFlagOrangeBloxSyncDir")
                cf.main_config = fromFastFlagConfig
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
def urlQuickLaunch(): # URL Quick Launch
    printSystemMessage(ts("--- URL Quick Launch ---"))
    if cf.main_config.get("EFlagEnableURLQuickLaunch") != True:
        printErrorMessage("URL Quick Launch is not enabled.")
        input("> ")
        sys.exit(0)
    quick_launch_file = generateFileKey("URLQuickLaunch")
    try:
        app_lock = PyKits.Lock(quick_launch_file)
        with app_lock:
            cf.skip_modification_mode = True
            cf.avoid_going_to_roblox = True
            printMainMessage("URL Quick Launch is waiting for Roblox to be launched..")
            from Modules.roblox import runRoblox
            cf.pip_class.startThread(runRoblox)
            while cf.roblox_launched == False: time.sleep(0.1)
            printMainMessage("Welcome to URL Quick Launch! Using this option, OrangeBlox will automatically launch Roblox when you attempt to open Roblox from your web browser and try to be as fast as possible to open. In the process, you may see the Roblox window open; just leave it open.")
            while not os.path.exists(os.path.join((cf.orangeblox_library if cf.main_os == "Darwin" else cf.cur_path), "URLLaunchExchange")): time.sleep(0.1)
            urlArgumentExchange()
        if len(cf.given_args) > 1:
            cf.handler.endRoblox()
            printSuccessMessage("Received message to open URL!")
            cf.preserve_roblox = True
            cf.restartRoblox()
    except Exception:
        printErrorMessage("Uh oh! A Python exception that causes the script to end has occurred!")
        printErrorMessage(f"Exception: \n{trace()}")
        printErrorMessage(f"Location Code: 12")
        input("> ")
        sys.exit(0 if cf.main_os == "Darwin" else 1) 
def continueToCredits(): # Credits
    quote = "'"
    printSystemMessage("--- Credits ---")
    printMainMessage(f"1. Made by {cf.colors_class.wrap('@EfazDev 🍊', 202)}")
    printMainMessage(f"2. Old Player Sounds and Cursors were sourced from {cf.colors_class.wrap('Bloxstrap 🎮 (https://github.com/pizzaboxer/bloxstrap)', 165)}")
    printMainMessage(f"3. Avatar Editor Maps were from {cf.colors_class.wrap(f'Mielesgames{quote}s Map Files 🗺️ (https://github.com/Mielesgames/RobloxAvatarEditorMaps)', 197)} slightly edited to be usable for the current version of Roblox (as of the time of writing this)")
    printMainMessage(f"4. The Kliko's Mod Tool Mod Script was edited and made from {cf.colors_class.wrap(f'Kliko{quote}s Mod Tool and Kliko{quote}s modloader 🎮 (https://github.com/klikos-modloader/klikos-modloader)', 196)}")
    printMainMessage("5. Python Module Creators:")
    printMainMessage(f" • {cf.colors_class.wrap('qwertyquerty (pypresence) 🦖 (https://github.com/qwertyquerty/pypresence)', 34)}")
    printMainMessage(f" • {cf.colors_class.wrap('Ronald Oussoren (pyobjc) 🔁 (https://github.com/ronaldoussoren/pyobjc)', 40)}")
    printMainMessage(f" • {cf.colors_class.wrap('Philip Semanchuk (posix-ipc) 🙂 (https://github.com/osvenskan/posix_ipc)', 226)}")
    printMainMessage(f" • {cf.colors_class.wrap('Mark Hammond (pywin32) 🪟 (https://github.com/mhammond/pywin32)', 129)}")
    printMainMessage(f" • {cf.colors_class.wrap('Kivy (plyer) 🧰 (https://github.com/kivy/plyer)', 214)}")
    printMainMessage(f" • {cf.colors_class.wrap('Giampaolo Rodola (psutil) 🔌 (https://github.com/giampaolo/psutil)', 97)}")
    printMainMessage(f" • {cf.colors_class.wrap('sethmlarson (truststore) 🔌 (https://github.com/sethmlarson/truststore)', 226)}")
    printMainMessage(f"Licenses are listed in {'https://github.com/EfazDev/orangeblox/tree/main/Licenses'} or included with your installation in: {os.path.join(cf.cur_path, 'Licenses')}")
    printMainMessage(f"6. The logo of OrangeBlox was made thanks of {cf.colors_class.wrap('@CabledRblx 🦆', 226)}. Thanks :)")
    printMainMessage(f"7. Server Locations are sourced from {cf.colors_class.wrap('freeipapi.com 🌐', 201)}")
    printMainMessage(f"8. Server Uptimes are sourced from {cf.colors_class.wrap('RoValra 🌐', 88)}")
    if cf.main_os == "Darwin": 
        printMainMessage(f'9. macOS App was built using {cf.colors_class.wrap("pyinstaller 📦", 39)} and {cf.colors_class.wrap("clang 📦", 226)}. You can recreate and deploy using the following command! Use the README.md for more information.')
        printMainMessage(f"Command: \"{sys.executable}\" Install.py -r -rp -rc")
        printYellowMessage(f"Nuitka requires a C compiler in order to use. For more information, use this manual: https://nuitka.net/user-documentation/user-manual.html")
    elif cf.main_os == "Windows": 
        printMainMessage(f'9. Windows App was built using {cf.colors_class.wrap("pyinstaller 📦", 39)}. You can recreate and deploy using the following command! Use the README.md for more information.')
        printMainMessage(f"Command: \"{sys.executable}\" Install.py -r -rp")
    printDebugMessage(f"Operating System: {cf.main_os}")
def continueToUnfriendedFriends(): # View Unfriended Friends
    printSystemMessage(f"--- Unfriended Friends ---")
    unfriended_friends = []
    blank_user_ids = 0
    friend_check_id = cf.main_config.get('EFlagRobloxUnfriendCheckUserID', 1)
    try:
        printMainMessage("Fetching Friends! This may take a moment.")
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
                printDebugMessage(f"Called ({friend_list_req.url}): {friend_list_req.json}")
                if friend_list_req.ok and friend_req_json.get("PageItems"):
                    friend_list_json["data"] += friend_req_json.get("PageItems")
                    if friend_req_json.get("NextCursor"):  query["cursor"] = friend_req_json.get("NextCursor")
                    else: reached_end = True
            except Exception: pass
            time.sleep(1)
        
        last_pinged_friend_list = {}
        if os.path.exists(os.path.join(generateFileKey("CachedFriendsList", ext=".json"))):
            with open(os.path.join(generateFileKey("CachedFriendsList", ext=".json")), "r", encoding="utf-8") as f: last_pinged_friend_list = json.load(f)
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
                        if i.get("id") != -1: user_ids.append(i.get("id"))
                    if len(user_ids) > 150:
                        chunked = []
                        for e in range(0, len(user_ids), 150): chunked.append(user_ids[e:e + 150])
                        unfriended_friends = []
                        for e in chunked:
                            reached_end3 = False
                            while reached_end3 == False:
                                user_info_req = cf.requests.post(f"https://users.roblox.com/v1/users", {"userIds": e, "excludeBannedUsers": False}, timeout=5, cookies=createCookieHeader())
                                if user_info_req.ok: unfriended_friends += user_info_req.json.get("data"); reached_end3 = True
                                printDebugMessage(f"Called ({user_info_req.url}): {user_info_req.json}")
                                time.sleep(1)
                        reached_end2 = True
                    else:
                        user_info_req = cf.requests.post(f"https://users.roblox.com/v1/users", {"userIds": user_ids, "excludeBannedUsers": False}, timeout=5, cookies=createCookieHeader())
                        if user_info_req.ok: unfriended_friends = user_info_req.json.get("data"); reached_end2 = True
                        printDebugMessage(f"Called ({user_info_req.url}): {user_info_req.json}")
                        time.sleep(1)
                except Exception: pass
            last_pinged_friend_list[str(friend_check_id)] = friend_list_json.get("data")
        else: last_pinged_friend_list[str(friend_check_id)] = friend_list_json.get("data")
        with open(os.path.join(generateFileKey("CachedFriendsList", ext=".json")), "w", encoding="utf-8") as f: json.dump(last_pinged_friend_list, f, indent=4)
    except Exception:
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
    is_python_beta = cf.pip_class.getIfPythonVersionIsBeta()
    current_python_version = cf.pip_class.getCurrentPythonVersion()
    latest_python_version = cf.pip_class.getLatestPythonVersion(beta=is_python_beta)
    printSystemMessage(f"--- Update to Python {latest_python_version} ---")
    if current_python_version == latest_python_version: printSuccessMessage(f"You're already in the latest version of Python!")
    else:
        printMainMessage(f"Would you like to update Python to {latest_python_version} using the official Python Installer? (y/n)")
        printMainMessage(f"{cf.colors_class.wrap(f'[v{current_python_version} => v{latest_python_version}]', 226 if is_python_beta else 82)}")
        co = input("> ")
        if isYes(co) == True:
            if cf.main_config.get("EFlagEnableSlientPythonInstalls") == True:
                printMainMessage("Python may take a moment to install! Please wait!")
                if cf.main_os == "Darwin": printYellowMessage("For macOS users, admin permission is needed in order to install.")
                cf.pip_class.pythonInstall(latest_python_version, is_python_beta, silent=True)
            else:
                printMainMessage("Python Installer should launch after a moment. Follow the prompts to install!")
                cf.pip_class.pythonInstall(latest_python_version, is_python_beta)
            printMainMessage("Validating Python Installation..")
            if cf.pip_class.getMajorMinorVersion(current_python_version) < cf.pip_class.getMajorMinorVersion(latest_python_version):
                current_latest_python = latest_python_version
            else:
                latest_pip_class = PyKits.pip()
                latest_pip_class.ignore_same = True
                current_latest_python = latest_pip_class.getCurrentPythonVersion()
            if current_latest_python == latest_python_version:
                printSuccessMessage(f"Python {latest_python_version} has been successfully installed! Would you like to restart Python? (y/n)")
                co = input("> ")
                if isYes(co) == True: cf.pip_class.restartScript("Main.py", sys.argv)
                sys.exit(0)
            else: printErrorMessage("Python Installation was may be canceled or Python was not installed!")
def continueToUpdatePythonModules(): # Update Python Modules
    printSystemMessage(f"--- Update Python Modules ---")
    updating_python_modules = cf.pip_class.updates()
    if updating_python_modules and updating_python_modules["success"] == True:
        if len(updating_python_modules["packages"]) > 0:
            strs = []
            only_package_names = []
            for i in updating_python_modules["packages"]: vers1 = i['version']; vers2 = i['latest_version']; strs.append(f"{i['name']} {cf.colors_class.wrap(f'(v{vers1} => v{vers2})', 82)}"); only_package_names.append(i["name"])
            printMainMessage("The following modules are available to be updated!")
            printMainMessage(", ".join(strs))
            printMainMessage("Would you like to install the updates to them now?")
            co = input("> ")
            if isYes(co) == True:
                printMainMessage("Please wait while the modules are being updated!")
                update_modules = cf.pip_class.install(only_package_names, upgrade=True)
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
def continueToLinkShortcuts(url_scheme=None): # Link Shortcuts
    from Modules.menu import optionSelection
    printSystemMessage("--- Link Shortcuts ---")
    if cf.main_config.get("EFlagDisableSettingsAccess") == True:
        printErrorMessage("Access to using Link Shortcuts was disabled by file. Please try again later!")
        input("> ")
        optionSelection(mes="Link Shortcuts was not used!")
        return
    if type(url_scheme) is str and url_scheme != "efaz-bootstrap://shortcuts/?quick-action=true" and url_scheme != "orangeblox://shortcuts/?quick-action=true":
        if '://' in url_scheme: path = url_scheme.split('://', 1)[1]
        else: path = url_scheme.split(':', 1)[1]
        generated_shortcut_id = path.replace("shortcuts/", "").replace("?quick-action=true", "")
        if type(cf.main_config.get("EFlagRobloxLinkShortcuts")) is dict:
            if cf.main_config.get("EFlagRobloxLinkShortcuts").get(generated_shortcut_id):
                shortcut_info = cf.main_config.get("EFlagRobloxLinkShortcuts").get(generated_shortcut_id)
                running = False
                if type(shortcut_info.get("url")) is str and (shortcut_info.get("url").startswith("roblox:") or shortcut_info.get("url").startswith("roblox-player:") or shortcut_info.get("url").startswith("roblox-studio:") or shortcut_info.get("url").startswith("roblox-studio-auth:")):
                    if len(cf.given_args) > 1: cf.given_args[1] = shortcut_info["url"]
                    else: cf.given_args.append(shortcut_info["url"])
                    if shortcut_info["url"].startswith("roblox-studio"): cf.run_studio = True
                    running = True
                if type(shortcut_info.get("cookie_paths")) is dict:
                    for i, v in shortcut_info.get("cookie_paths").items():
                        if cf.main_os == "Darwin" and (i.startswith(os.path.join(cf.pip_class.getLocalAppData(), "HTTPStorages", "com.roblox.")) and v.startswith(os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "RBXCookies"))): cf.custom_cookies[i] = v
                        elif cf.main_os == "Windows" and (i == os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "LocalStorage", "RobloxCookies.dat") and v.startswith(os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "RBXCookies"))): cf.custom_cookies[i] = v
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
            generated_ui_options = []
            has_cookies = False
            if type(cf.main_config.get("EFlagRobloxLinkShortcuts")) is dict:
                for i, v in cf.main_config.get("EFlagRobloxLinkShortcuts").items():
                    if v and v.get("name") and v.get("id"): 
                        approved = False
                        cookie_added_str = ""
                        if v.get("cookie_paths"):
                            for c, k in v.get("cookie_paths").items():
                                if os.path.exists(k): approved = True; cookie_added_str = f" [User: @{v.get('cookie_user')}]"; has_cookies = True
                        if v.get("linked_computer") and v.get("linked_computer") != cf.main_config.get("EFlagLinkedComputerID"): cookie_added_str += " [Linked]"
                        if v.get("url") or approved == True: generated_ui_options.append({"index": 1, "message": f"{v.get('name')} [{i}]{cookie_added_str}", "shortcut_info": v})
            generated_ui_options.append({"index": 1000000, "message": ts("Create a new shortcut")})
            generated_ui_options.append({"index": 1000001, "message": ts("Create a new user shortcut")})
            generated_ui_options.append({"index": 1000002, "message": ts("Generate a new shortcut app")})
            generated_ui_options.append({"index": 1000003, "message": ts("Run a shortcut in a new instance")})
            if has_cookies == True and cf.main_config.get("EFlagRobloxSecurityCookieUsage") == True: generated_ui_options.append({"index": 1000004, "message": ts("Validate cookie shortcuts")})
            generated_ui_options.append({"index": 1000005, "message": ts("Delete a shortcut")})
            generated_ui_options = sorted(generated_ui_options, key=lambda x: x["index"])
            opt = generateMenuSelection(generated_ui_options)
            if opt:
                if opt["index"] == 1000000:
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
                        key = re.sub(r'[^A-Za-z0-9_\-]', '', key)
                        printMainMessage("Confirm the shortcut below? (y/n)")
                        printMainMessage(f"Name: {name}")
                        printMainMessage(f"URL: {ur}")
                        printMainMessage(f"Key: {key}")
                        if isYes(input("> ")) == True:
                            if cf.main_config.get("EFlagRobloxLinkShortcuts"): cf.main_config.get("EFlagRobloxLinkShortcuts")[key] = {"url": ur, "name": name, "id": key}
                            else:
                                cf.main_config["EFlagRobloxLinkShortcuts"] = {}
                                cf.main_config["EFlagRobloxLinkShortcuts"][key] = {"url": ur, "name": name, "id": key, "linked_computer": cf.main_config.get("EFlagLinkedComputerID")}
                            printSuccessMessage(f'Successfully created shortcut "{name}"! You may use this link using your browser or go through the main menu to use this shortcut: orangeblox://shortcuts/{key}')
                        saveSettings()
                        printMainMessage("Would you like to create an another shortcut? (y/n)")
                        if isYes(input("> ")) == True: loo()
                    loo()
                    linkLoop()
                elif opt["index"] == 1000001:
                    printYellowMessage("Important Notes:")
                    printYellowMessage("This option will automatically fetch your cookies and save them into the Roblox folder so you can login quicker.")
                    printYellowMessage(f"This option cannot be backed up to an another computer using {obName0()} installer due to cookie locations are saved.")
                    printYellowMessage("Launching Roblox from the web will automatically log out the user. Please know that.")
                    printYellowMessage("Log into the account you want to save as a shortcut before you continue.")
                    if not cf.handler.getIfRobloxIsOpen():
                        printMainMessage("Would you like to open Roblox without user data in order to login and create a cookie? (y/n)")
                        printYellowMessage("Warning! The cookies before this may be brought back after setup.")
                        printYellowMessage("But, it may be best to prevent the log out issue.")
                        if isYes(input("> ")) == True:
                            if cf.main_os == "Darwin":
                                httpStorages = os.path.join(cf.pip_class.getLocalAppData(), "HTTPStorages")
                                if os.path.exists(os.path.join(httpStorages, "com.roblox.RobloxPlayer.binarycookies")): 
                                    shutil.copy(os.path.join(httpStorages, "com.roblox.RobloxPlayer.binarycookies"), os.path.join(httpStorages, "dev.efaz.temp.RobloxPlayer.binarycookies"))
                                    os.remove(os.path.join(httpStorages, "com.roblox.RobloxPlayer.binarycookies"))
                            elif cf.main_os == "Windows":
                                if os.path.exists(os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "LocalStorage", "RobloxCookies.dat")): 
                                    shutil.copy(os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "LocalStorage", "RobloxCookies.dat"), os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "LocalStorage", "TempRobloxCookies.dat")); 
                                    os.remove(os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "LocalStorage", "RobloxCookies.dat"))
                            s = cf.handler.openRoblox(forceQuit=True, attachInstance=True)
                            def endRbx(log): 
                                while True: 
                                    if cf.main_os == "Darwin":
                                        if os.path.exists(os.path.join(httpStorages, "com.roblox.RobloxPlayer.binarycookies")): 
                                            with open(os.path.join(httpStorages, "com.roblox.RobloxPlayer.binarycookies"), "rb") as f: cookie_data = f.read()
                                            if "Sharing-this-will-allow-someone-to-log-in".encode("utf-8") in cookie_data: break
                                    else:
                                        if os.path.exists(os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "LocalStorage", "RobloxCookies.dat")):
                                            with open(os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "LocalStorage", "RobloxCookies.dat"), "r", encoding="utf-8") as f: cookie_data = f.read()
                                            if "CookiesData" in cookie_data: break
                                    time.sleep(1)
                                s.endInstance()
                            s.addRobloxEventCallback("onUserLogin", endRbx)
                            printMainMessage("Login to the Roblox account you would like to use!")
                            printMainMessage("(The windows may automatically close once the login is successful.)")
                            s.awaitRobloxClosing()
                    user_info = cf.handler.getRobloxAppSettings().get("loggedInUser", {})
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
                        key = re.sub(r'[^A-Za-z0-9_\-]', '', key)
                        printMainMessage("Confirm the shortcut below? (y/n)")
                        printMainMessage(f"Name: {name}")
                        if ur != "": printMainMessage(f"URL: {ur}")
                        printMainMessage(f"User: @{user_info.get('name')} [{user_info.get('id')}]")
                        printMainMessage(f"Key: {key}")
                        if isYes(input("> ")) == True:
                            paths_generated = {}
                            if cf.main_os == "Darwin":
                                makedirs(os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "RBXCookies", key))
                                httpStorages = os.path.join(cf.pip_class.getLocalAppData(), "HTTPStorages")
                                if os.path.exists(os.path.join(httpStorages, "com.roblox.RobloxPlayer.binarycookies")):
                                    t = os.path.join(httpStorages, "com.roblox.RobloxPlayer.binarycookies")
                                    paths_generated[t] = os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "RBXCookies", key, "com.roblox.RobloxPlayer.binarycookies")
                                    shutil.copy(t, paths_generated[t], follow_symlinks=False)
                                if os.path.exists(os.path.join(httpStorages, "com.roblox.RobloxStudio.binarycookies")):
                                    t = os.path.join(httpStorages, "com.roblox.RobloxStudio.binarycookies")
                                    paths_generated[t] = os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "RBXCookies", key, "com.roblox.RobloxStudio.binarycookies")
                                    shutil.copy(t, paths_generated[t], follow_symlinks=False)
                            elif cf.main_os == "Windows":
                                makedirs(os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "RBXCookies", key))
                                if os.path.exists(os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "LocalStorage", "RobloxCookies.dat")):
                                    t = os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "LocalStorage", "RobloxCookies.dat")
                                    paths_generated[t] = os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "RBXCookies", key, "RobloxCookies.dat")
                                    shutil.copy(t, paths_generated[t], follow_symlinks=False)
                            if cf.main_config.get("EFlagRobloxLinkShortcuts"): cf.main_config.get("EFlagRobloxLinkShortcuts")[key] = {"cookie_paths": paths_generated, "cookie_id": user_info.get("id"), "cookie_user": user_info.get("name"), "url": ur if ur != "" else None, "name": name, "id": key}
                            else:
                                cf.main_config["EFlagRobloxLinkShortcuts"] = {}
                                cf.main_config["EFlagRobloxLinkShortcuts"][key] = {"cookie_paths": paths_generated, "cookie_id": user_info.get("id"), "cookie_user": user_info.get("name"), "url": ur if ur != "" else None, "name": name, "id": key, "linked_computer": cf.main_config.get("EFlagLinkedComputerID")}
                            printSuccessMessage(f'Successfully created shortcut "{name}"! You may use this link using your browser or go through the main menu to use this shortcut: orangeblox://shortcuts/{key}')
                            saveSettings()
                        if cf.main_os == "Darwin":
                            httpStorages = os.path.join(cf.pip_class.getLocalAppData(), "HTTPStorages")
                            if os.path.exists(os.path.join(httpStorages, "dev.efaz.temp.RobloxPlayer.binarycookies")): 
                                shutil.copy(os.path.join(httpStorages, "dev.efaz.temp.RobloxPlayer.binarycookies"), os.path.join(httpStorages, "com.roblox.RobloxPlayer.binarycookies"))
                                os.remove(os.path.join(httpStorages, "dev.efaz.temp.RobloxPlayer.binarycookies"))
                        elif cf.main_os == "Windows":
                            if os.path.exists(os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "LocalStorage", "TempRobloxCookies.dat")): 
                                shutil.copy(os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "LocalStorage", "TempRobloxCookies.dat"), os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "LocalStorage", "RobloxCookies.dat")); 
                                os.remove(os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "LocalStorage", "TempRobloxCookies.dat"))
                    else: printErrorMessage("Log in was not detected in the client!")
                    linkLoop()
                elif opt["index"] == 1000002:
                    if type(cf.main_config.get("EFlagRobloxLinkShortcuts")) is dict:
                        def loo():
                            if type(cf.main_config.get("EFlagRobloxLinkShortcuts")) is dict:
                                generated_ui_options = []
                                printSystemMessage("--- Select Link Shortcut ---")
                                for i, v in cf.main_config.get("EFlagRobloxLinkShortcuts").items():
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
                                    info = cf.main_config.get("EFlagRobloxLinkShortcuts")[key]
                                    printMainMessage("Confirm the shortcut below? (y/n)")
                                    printMainMessage(f"Name: {info['name']}")
                                    printMainMessage(f"URL: {info['url']}")
                                    if info.get("cookie_id"): printMainMessage(f"User: @{info.get('cookie_user')} [{info.get('cookie_id')}]")
                                    printMainMessage(f"Key: {key}")
                                    if isYes(input("> ")) == True: 
                                        info['name'] = info['name'].replace("../", "").replace("./", "")
                                        printMainMessage("Generating Shortcut App..")
                                        if cf.main_os == "Windows":
                                            try:
                                                import win32com.client as win32client # type: ignore
                                                import pythoncom # type: ignore
                                                pythoncom.CoInitialize()
                                                try:
                                                    shell = win32client.Dispatch('WScript.Shell')
                                                    def create_shortcut(target_path, shortcut_path, working_directory=None, icon_path=None, arguments=None):
                                                        if not os.path.exists(os.path.dirname(shortcut_path)): os.makedirs(os.path.dirname(shortcut_path),mode=511)
                                                        shortcut = shell.CreateShortcut(shortcut_path)
                                                        shortcut.TargetPath = target_path
                                                        if arguments: shortcut.Arguments = arguments
                                                        if working_directory: shortcut.WorkingDirectory = working_directory
                                                        if icon_path: shortcut.IconLocation = icon_path
                                                        shortcut.Save()
                                                        del shortcut
                                                    create_shortcut(os.path.join(cf.cur_path, "OrangeBlox.exe"), os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), f"{info['name']}.lnk"), arguments=f"orangeblox://shortcuts/{key}")
                                                    create_shortcut(os.path.join(cf.cur_path, "OrangeBlox.exe"), os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs'), f"{info['name']}.lnk"), arguments=f"orangeblox://shortcuts/{key}", icon_path=os.path.join(cf.cur_path, "Images", "AppIconRunStudio.ico"))
                                                    create_shortcut(os.path.join(cf.cur_path, "OrangeBlox.exe"), os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Roblox'), f"{info['name']}.lnk"), arguments=f"orangeblox://shortcuts/{key}", icon_path=os.path.join(cf.cur_path, "Images", "AppIconRunStudio.ico"))     
                                                    printSuccessMessage("Generated Shortcut App!")
                                                    del shell
                                                finally: pythoncom.CoUninitialize()
                                            except Exception as e: printErrorMessage(f"Unable to create shortcuts: {str(e)}")
                                        elif cf.main_os == "Darwin":
                                            if os.path.exists(os.path.join(cf.macos_app_path, "../", "Play Roblox.app")):
                                                if not (os.path.exists(os.path.join(cf.pip_class.getInstallableApplicationsFolder(), f"{info['name']}.app")) and not os.path.exists(os.path.join(cf.pip_class.getInstallableApplicationsFolder(), f"{info['name']}.app", "Contents", "Resources", "AlternativeLink"))):
                                                    cf.pip_class.copyTreeWithMetadata(os.path.join(cf.macos_app_path, "../", "Play Roblox.app"), os.path.join(cf.pip_class.getInstallableApplicationsFolder(), f"{info['name']}.app"), dirs_exist_ok=True)
                                                    with open(os.path.join(cf.pip_class.getInstallableApplicationsFolder(), f"{info['name']}.app", "Contents", "Resources", "AlternativeLink"), "w", encoding="utf-8") as f: f.write(f"orangeblox://shortcuts/{key}")
                                                    for i in generateCodesignCommand(os.path.join(cf.pip_class.getInstallableApplicationsFolder(), f"{info['name']}.app"), cf.main_config.get("EFlagRobloxCodesigningName", "-")): 
                                                        if i[0] == "/usr/bin/xattr": subprocess.run(i, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                                                        else: subprocess.Popen(i, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                                                    printSuccessMessage("Generated Shortcut App!")
                                                else: printErrorMessage(f"Unable to generate a shortcut app because this path for the shortcut is non-{obName0()} and exists!")
                                            else: printErrorMessage("Unable to generate a shortcut app because Play Roblox app is not available!")
                                    saveSettings()
                                    printMainMessage("Would you like to generate an another shortcut app? (y/n)")
                                    if isYes(input("> ")) == True: loo()
                        loo()
                    else: printErrorMessage("You have no shortcuts created!")
                    linkLoop()
                elif opt["index"] == 1000003:
                    if type(cf.main_config.get("EFlagRobloxLinkShortcuts")) is dict:
                        generated_ui_options = []
                        printSystemMessage("--- Select Link Shortcut ---")
                        for i, v in cf.main_config.get("EFlagRobloxLinkShortcuts").items():
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
                            if cf.main_os == "Darwin": subprocess.run([cf.pip_class.getPathFile("/usr/bin/open"), f"orangeblox://shortcuts/{key}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cf.cur_path)
                            else: subprocess.run(["start", f"orangeblox://shortcuts/{key}"], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cf.cur_path)
                            printSuccessMessage("Successfully called to open a new instance! Please wait for Roblox to open and run a game before continuing the next account!")
                        else: printErrorMessage("Shortcut not found!")
                    else: printErrorMessage("You have no shortcuts created!")
                    linkLoop()
                elif opt["index"] == 1000004:
                    printMainMessage("Validating cookies of cookie user shortcuts..")
                    failed = []
                    try:
                        if type(cf.main_config.get("EFlagRobloxLinkShortcuts")) is dict:
                            for i, v in cf.main_config.get("EFlagRobloxLinkShortcuts").items():
                                if v and v.get("name") and v.get("id"): 
                                    approved = False
                                    if v.get("cookie_paths"):
                                        parsed_cookie = None
                                        parsed_studio_cookie = None
                                        for path, k in v.get("cookie_paths").items():
                                            if cf.main_os == "Windows" and "RobloxCookies.dat" in k:
                                                parsed_cookie = cf.handler.parseRobloxCookieFile(k)
                                                parsed_studio_cookie = cf.handler.parseRobloxCookieFile(k)
                                            elif cf.main_os == "Darwin" and "RobloxStudio.binarycookies" in path:
                                                parsed_studio_cookie = cf.handler.parseRobloxCookieFile(k)
                                            elif cf.main_os == "Darwin" and "RobloxPlayer.binarycookies" in path:
                                                parsed_cookie = cf.handler.parseRobloxCookieFile(k)
                                        try:
                                            if parsed_cookie:
                                                cookie_req = cf.requests.get("https://users.roblox.com/v1/users/authenticated", cookies={".ROBLOSECURITY": parsed_cookie})
                                                if cookie_req.status_code in (403, 401): failed.append((1, v.get("id"), v.get("name"), v.get('cookie_user')))
                                            if parsed_studio_cookie:
                                                cookie_req = cf.requests.get("https://users.roblox.com/v1/users/authenticated", cookies={".ROBLOSECURITY": parsed_studio_cookie})
                                                if cookie_req.status_code in (403, 401): failed.append((2, v.get("id"), v.get("name"), v.get('cookie_user')))
                                        except Exception: printErrorMessage(f"Unable to validate shortcut {v.get('name')} due to an Python exception: \n{trace()}")
                        printSystemMessage("--- Final Results! ---")
                        if len(failed) > 0:
                            printYellowMessage("The following shortcuts no longer have valid cookies:")
                            printMainMessage(", ".join([f"{shortcut_name} [{shortcut_id}] [@{cookie_user}]{'' if client == 1 else ' [STUDIO]'}" for client, shortcut_id, shortcut_name, cookie_user in failed]))
                        else: printMainMessage("Your shortcuts are valid and don't contain invalid cookies. :D")
                    except Exception: printErrorMessage(f"Unable to validate due to an Python exception: \n{trace()}")
                    printSystemMessage("--- Link Shortcuts ---")
                    linkLoop()
                elif opt["index"] == 1000005:
                    if type(cf.main_config.get("EFlagRobloxLinkShortcuts")) is dict:
                        def loo():
                            if type(cf.main_config.get("EFlagRobloxLinkShortcuts")) is dict:
                                generated_ui_options = []
                                printSystemMessage("--- Select Link Shortcut ---")
                                for i, v in cf.main_config.get("EFlagRobloxLinkShortcuts").items():
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
                                    info = cf.main_config.get("EFlagRobloxLinkShortcuts")[key]
                                    printMainMessage("Confirm the shortcut below? (y/n)")
                                    printMainMessage(f"Name: {info['name']}")
                                    printMainMessage(f"URL: {info['url']}")
                                    if info.get("cookie_id"): printMainMessage(f"User: @{info.get('cookie_user')} [{info.get('cookie_id')}]")
                                    printMainMessage(f"Key: {key}")
                                    if isYes(input("> ")) == True: cf.main_config["EFlagRobloxLinkShortcuts"].pop(key)
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
                            if cf.main_os == "Darwin" and (i.startswith(os.path.join(cf.pip_class.getLocalAppData(), "HTTPStorages", "com.roblox.")) and v.startswith(os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "RBXCookies"))): cf.custom_cookies[i] = v
                            elif cf.main_os == "Windows" and (i == os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "LocalStorage", "RobloxCookies.dat") and v.startswith(os.path.join(cf.pip_class.getLocalAppData(), "Roblox", "RBXCookies"))): cf.custom_cookies[i] = v
                        running = True
                    if type(opt["shortcut_info"].get("url")) is str and (opt["shortcut_info"].get("url").startswith("roblox:") or opt["shortcut_info"].get("url").startswith("roblox-player:") or opt["shortcut_info"].get("url").startswith("roblox-studio:") or opt["shortcut_info"].get("url").startswith("roblox-studio-auth:")):
                        if len(cf.given_args) > 1: cf.given_args[1] = opt["shortcut_info"]["url"]
                        else: cf.given_args.append(opt["shortcut_info"]["url"])
                        if opt["shortcut_info"]["url"].startswith("roblox-studio"): cf.run_studio = True
                        running = True
                    if running == True: printSuccessMessage(f"Starting shortcut \"{opt['shortcut_info']['name']}\"!"); continueToRoblox()
                    else: sys.exit(0)
            else:
                if not url_scheme or not ("?quick-action=true" in url_scheme): optionSelection(mes="Link Shortcuts has closed!")
                else: sys.exit(0)
        linkLoop()
def continueToUpdates(): # Check for Updates
    printSystemMessage("--- Checking for Bootstrap Updates ---")
    printDebugMessage("Setting Installed App Path to Local User..") 
    if cf.main_os == "Darwin": setInstalledAppPath(os.path.realpath(os.path.join(cf.macos_app_path, "../") + "/"))
    elif cf.main_os == "Windows": setInstalledAppPath(os.path.realpath(cf.cur_path))
    printDebugMessage("Sending Request to Bootstrap Version Servers..") 
    version_server = cf.main_config.get("EFlagBootstrapUpdateServer", "https://obx.efaz.dev/Version.json")
    if not (type(version_server) is str and version_server.startswith("https://")): version_server = "https://obx.efaz.dev/Version.json"
    try: latest_vers_res = cf.requests.get(f"{version_server}", headers={"X-Bootstrap-Version": cf.current_version["version"], "X-Python-Version": platform.python_version(), "X-Authorization-Key": cf.main_config.get("EFlagUpdatesAuthorizationKey", "")})
    except Exception: latest_vers_res = PyKits.InstantRequestJSONResponse(ok=False)
    if latest_vers_res.ok:
        latest_vers = latest_vers_res.json
        if cf.current_version.get("version"):
            printDebugMessage(f'Called ({version_server}): {latest_vers}') 
            if cf.current_version.get("version", "1.0.0") < latest_vers.get("latest_version", "1.0.0"):
                download_location = latest_vers.get("download_location", "https://github.com/EfazDev/orangeblox/archive/refs/heads/main.zip")
                printDebugMessage(f"Update v{latest_vers['latest_version']} detected!")
                printSystemMessage("--- New Bootstrap Update ---")
                printMainMessage(f"We have detected a new version of {obName0()}! Would you like to install it? (y/n)")
                if download_location == "https://github.com/EfazDev/orangeblox/archive/refs/heads/main.zip":
                    download_location = f"https://github.com/EfazDev/orangeblox/releases/download/v{latest_vers['latest_version']}/OrangeBlox-v{latest_vers['latest_version']}.zip"
                    printSuccessMessage("✅ This version is a public update available on GitHub for viewing.")
                    printSuccessMessage("✅ For information about this update, use this link: https://github.com/EfazDev/orangeblox/releases")
                    printSuccessMessage(f"✅ Download Location: {download_location}")
                elif download_location == "https://github.com/EfazDev/orangeblox/archive/refs/heads/beta.zip":
                    download_location = f"https://github.com/EfazDev/orangeblox/releases/download/v{latest_vers['latest_version']}/OrangeBlox-v{latest_vers['latest_version']}.zip"
                    printYellowMessage(f"⚠️ This version is a beta version of {obName0()} and may cause issues with your installation.")
                    printYellowMessage("⚠️ For information about this update, use this link: https://github.com/EfazDev/orangeblox/releases")
                    printSuccessMessage(f"⚠️ Download Location: {download_location}")
                elif cf.main_config.get("EFlagUpdatesAuthorizationKey", "") != "":
                    printYellowMessage("🔨 This version is an update configured from an organization (this may still be a modified and an unofficial OrangeBlox version.)")
                    printYellowMessage("🔨 For information about this update, contact your administrator!")
                    printSuccessMessage(f"🔨 Download Location: {download_location}")
                else:
                    printErrorMessage("❌ The download location is different from the official GitHub link!")
                    printErrorMessage(f"❌ You may be downloading an unofficial {obName0()} version! Download a copy from https://github.com/EfazDev/orangeblox!")
                    printSuccessMessage(f"❌ Download Location: {download_location}")
                printSuccessMessage(f"v{cf.current_version.get('version', '1.0.0')} [Current] => v{latest_vers['latest_version']} [Latest]")
                if isYes(input("> ")) == True:
                    printDebugMessage(f"Saving Settings..")
                    saveSettings()
                    printMainMessage("Downloading latest version..")
                    printDebugMessage(f"Download location: {download_location} => {os.path.join(cf.cur_path, 'Update.zip')}")
                    try:
                        download_update = cf.requests.download(download_location, os.path.join(cf.cur_path, 'Update.zip'))
                        if download_update.ok:
                            printMainMessage("Download Success! Extracting ZIP now!")
                            zip_extract = cf.pip_class.unzipFile(os.path.join(cf.cur_path, "Update.zip"), os.path.join(cf.cur_path, 'Update'), ["Main.py", "RobloxManager.py", "OrangeAPI.py", "Configuration.json", "Apps"])
                            if zip_extract.returncode == 0:
                                printMainMessage("Extracted successfully! Installing Files!")
                                try:
                                    for file in os.listdir(os.path.join(cf.cur_path, 'Update')):
                                        src_path = os.path.join(os.path.join(cf.cur_path, 'Update'), file)
                                        dest_path = os.path.join(cf.cur_path, file)
                                        if os.path.isdir(src_path):
                                            try: cf.pip_class.copyTreeWithMetadata(src_path, dest_path, dirs_exist_ok=True)
                                            except Exception: printDebugMessage(f"Update Error for directory ({src_path}): \n{trace()}")
                                        else:
                                            if (not file.endswith(".json")) or file == "Version.json":
                                                try: shutil.copy2(src_path, dest_path)
                                                except Exception: printDebugMessage(f"Update Error for file ({src_path}): \n{trace()}")
                                    if checkSyncFolder():
                                        printMainMessage("Extending Changes to Installation Folder..")
                                        for file in os.listdir(os.path.join(cf.cur_path, 'Update')):
                                            src_path = os.path.join(os.path.join(cf.cur_path, 'Update'), file)
                                            dest_path = os.path.join(cf.main_config.get("EFlagOrangeBloxSyncDir"), file)
                                            if os.path.isdir(src_path):
                                                try: cf.pip_class.copyTreeWithMetadata(src_path, dest_path, dirs_exist_ok=True)
                                                except Exception: printDebugMessage(f"Update Error for directory ({src_path}): \n{trace()}")
                                            else:
                                                if (not file.endswith(".json")) or file == "Version.json":
                                                    try: shutil.copy2(src_path, dest_path)
                                                    except Exception: printDebugMessage(f"Update Error for file ({src_path}): \n{trace()}")
                                    if os.path.exists(generateFileKey("OrangeBloxUpdate")): os.remove(generateFileKey("OrangeBloxUpdate"))
                                    printMainMessage("Running Installer..")
                                    if cf.main_os == "Windows":
                                        if len(cf.given_args) > 1:
                                            filtered_args = cf.given_args[1]
                                            if (("roblox-player:" in filtered_args) or ("roblox-studio:" in filtered_args) or ("roblox-studio-auth:" in filtered_args) or ("roblox:" in filtered_args) or ("efaz-bootstrap:" in filtered_args) or ("orangeblox:" in filtered_args)):
                                                printMainMessage(f"Creating URL Exchange file..")
                                                with open(os.path.join(cf.cur_path, "URLLaunchExchange"), "w", encoding="utf-8") as f: f.write(filtered_args)
                                        silent_install = subprocess.run(f'start cmd.exe /c ""{sys.executable}" "{os.path.join(cf.cur_path, "Install.py")}" --update-mode"', shell=True, cwd=cf.cur_path)
                                        if silent_install.returncode != 0: printErrorMessage("Bootstrap Installer failed.")
                                        try:
                                            printMainMessage("Cleaning up files..")
                                            os.remove(os.path.join(cf.cur_path, 'Update.zip'))
                                            shutil.rmtree(os.path.join(cf.cur_path, 'Update'), ignore_errors=True)
                                        except Exception:
                                            printErrorMessage(f"Something went wrong while cleaning the files for {obName0()} update!")
                                            printDebugMessage(f"Cleaning Error: \n{trace()}")
                                        sys.exit(0)
                                    else:
                                        silent_install = cf.stdout.run_process(args=[sys.executable, "Install.py", "--update-mode"], cwd=cf.cur_path)
                                        if silent_install.returncode != 0: printErrorMessage("Bootstrap Installer failed.")
                                        try:
                                            printMainMessage("Cleaning up files..")
                                            os.remove(os.path.join(cf.cur_path, 'Update.zip'))
                                            shutil.rmtree(os.path.join(cf.cur_path, 'Update'), ignore_errors=True)
                                        except Exception:
                                            printErrorMessage(f"Something went wrong while cleaning the files for {obName0()} update!")
                                            printDebugMessage(f"Cleaning Error: \n{trace()}")
                                        sys.exit(0)
                                except Exception:
                                    printErrorMessage(f"Something went wrong while updating the files for {obName0()}!")
                                    printDebugMessage(f"Updating Error: \n{trace()}")
                                try:
                                    printMainMessage("Cleaning up files..")
                                    os.remove(os.path.join(cf.cur_path, 'Update.zip'))
                                    shutil.rmtree(os.path.join(cf.cur_path, 'Update'), ignore_errors=True)
                                except Exception:
                                    printErrorMessage(f"Something went wrong while cleaning the files for {obName0()} update!")
                                    printDebugMessage(f"Cleaning Error: \n{trace()}")
                                printSuccessMessage(f"Update to v{latest_vers['version']} was finished successfully! Restarting bootstrap..")
                                cf.pip_class.restartScript("Main.py", cf.given_args)
                                sys.exit(0)
                            else:
                                try:
                                    printMainMessage("Cleaning up files..")
                                    os.remove(os.path.join(cf.cur_path, 'Update.zip'))
                                    shutil.rmtree(os.path.join(cf.cur_path, 'Update'), ignore_errors=True)
                                except Exception:
                                    printErrorMessage(f"Something went wrong while cleaning the files for {obName0()} update!")
                                    printDebugMessage(f"Update Error: \n{trace()}")
                                printErrorMessage("There was an issue extracting the update due to an error!")
                                return ts("Update was unable to be installed!")
                        else:
                            printErrorMessage("There was an issue downloading the update due to an curl error!")
                            return ts("Update was unable to be installed!")
                    except Exception:
                        printErrorMessage("There was an issue downloading the update due to an curl error!")
                        return ts("Update was unable to be installed!")
                else:
                    printDebugMessage("User rejected update.")
                    return ts("Update was cancelled!")
            elif cf.current_version.get("version", "1.0.0") > latest_vers.get("latest_version", "1.0.0"):
                printSuccessMessage(f"{obName0()} is in a beta version! No updates are needed!")
                return ts("No updates are needed!")
            else:
                printMainMessage(f"{obName0()} is currently on the latest version! No updates are needed!")
                return ts("No updates are needed!")
        else:
            printDebugMessage("There was an error reading the latest version.")
            return ts("There was an issue while checking for updates.")
    else:
        printDebugMessage("Update Check Response failed.")
        return ts("There was an issue while checking for updates.")

if __name__ == "__main__":
    print("This module is not a runable instance.")
    sys.exit(1)