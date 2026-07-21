# 
# OrangeBlox 🍊
# Made by Efaz from efaz.dev
# v2.6.0i
# 

import Modules.config as cf
from Modules.utils import *

def firstActions():
    getSettings()
    setLoggingHandler("Main")
    if cf.main_os == "Darwin": cf.colors_class.set_console_title(f"{obName0()} {obName1()}")
def requirementCheck():
    try:
        if cf.main_config and cf.main_config.get("EFlagEnableDebugMode") == True: cf.pip_class.debug = True
        if waitForInternet() == True: printSystemMessage("-----------")
        cf.versions_folder = os.path.join(cf.cur_path, "Versions")
        if cf.main_os == "Darwin": 
            makedirs(cf.orangeblox_library)
            cf.versions_folder = os.path.join(cf.orangeblox_library, "Versions")
            if not os.path.exists(os.path.join(cf.orangeblox_library, "Mods")): shutil.copytree(os.path.join(cf.cur_path, "Mods"), os.path.join(cf.orangeblox_library, "Mods"))
            makedirs(cf.versions_folder)
            cf.mods_folder = os.path.join(cf.orangeblox_library, "Mods")
        if cf.main_os != "Windows" and cf.main_os != "Darwin":
            printErrorMessage(f"{obName0()} is only supported for macOS and Windows.")
            input("> ")
            sys.exit(0)
        if not cf.pip_class.osSupported(windows_build=17763, macos_version=(10,15,0)):
            if cf.main_os == "Windows": printErrorMessage(f"{obName0()} is only supported for Windows 10.0.17763 (October 2018) or higher. Please update your operating system in order to continue!")
            elif cf.main_os == "Darwin": printErrorMessage(f"{obName0()} is only supported for macOS 10.15 (Catalina) or higher. Please update your operating system in order to continue!")
            input("> ")
            sys.exit(0)
        if not cf.pip_class.pythonSupported(3, 11, 0):
            startMessage(first=True, ignore_support=True)
            if not cf.pip_class.pythonSupported(3, 6, 0):
                printSystemMessage("--- Python Update Required ---")
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
        if cf.pip_class.getIfRunningWindowsAdmin():
            printSystemMessage("--- Admin Permissions Not Required ---")
            printErrorMessage(f"Please run {obName0()} under user permissions instead of running administrator!")
            input("> ")
            sys.exit(0)
    except (KeyboardInterrupt, Exception) as e:
        printErrorMessage("Uh oh! A Python exception that causes the script to end has occurred!")
        printErrorMessage(f"Exception: \n{trace()}")
        printErrorMessage(f"Location Code: 4")
        input("> ")
        sys.exit(0 if cf.main_os == "Darwin" else 1)
def adjustRobloxInstallation():
    try:
        startMessage(first=True)
        rbx.submit_status = cf.submit_status
        rbx.orangeblox_mode = True
        if not validateInstallation():
            printSystemMessage("--- Install Required! ---")
            printMainMessage(f"Please install {obName0()} from running Install.py in order to continue!")
            input("> ")
            sys.exit(0)
        if (not os.path.exists(cf.versions_folder)) and cf.main_config.get("EFlagCompletedTutorial") == True:
            printSystemMessage("--- Hello Bootstrap User! ---")
            printMainMessage("We have updated Efaz's Roblox Bootstrap to feature a new brand (OrangeBlox) and also download Roblox into a separate folder and doesn't need vanilla Roblox to be installed!")
            printMainMessage("Your previous installation data was transferred and deleted after installation.")
            printYellowMessage(f"Once you continue, we will start reinstalling vanilla Roblox and then install a new separate Roblox into {obName0()}!")
            con = input("> ")
            if isNo(con): sys.exit(0)
            printSystemMessage("--- Reinstalling Roblox ---")
            cf.submit_status.start()
            res = cf.handler.reinstallRoblox(debug=cf.main_config.get("EFlagEnableDebugMode"), clearUserData=False, copyRobloxInstallerPath=(os.path.join(cf.orangeblox_library, "RobloxPlayerInstaller.app") if cf.main_os == "Darwin" else os.path.join(cf.cur_path, "RobloxPlayerInstaller.exe")), downloadInstaller=True, disableRobloxAutoOpen=True, downloadToken=createDownloadToken(studio=False))
            cf.submit_status.end()
            if res and res["success"] == False:
                printErrorMessage("There is an issue while trying to install Roblox. Please try again by restarting this app!")
                input("> ")
                sys.exit(0)
        if cf.main_config.get("EFlagEnableDuplicationOfClients") == True:
            printSystemMessage("--- Note about Roblox Multi-Instancing ---")
            printYellowMessage("Recently, Roblox has declared multi-instancing as exploiting. ")
            printMainMessage("As a safety measure, we have disabled multi-instancing to help prevent your accounts from being flagged and getting banned. Sorry for the inconvenience.")
            con = input("> ")
            if isNo(con): sys.exit(0)
            cf.main_config["EFlagEnableDuplicationOfClients"] = False
            saveSettings()
        rbx.windows_versions_dir = cf.versions_folder
        rbx.windows_player_folder_name = cf.main_config.get("EFlagBootstrapRobloxInstallFolderName", "com.roblox.robloxplayer")
        rbx.windows_studio_folder_name = cf.main_config.get("EFlagBootstrapRobloxStudioInstallFolderName", "com.roblox.robloxstudio")
        rbx.macOS_dir = os.path.join(cf.versions_folder, "Roblox.app")
        rbx.macOS_studioDir = os.path.join(cf.versions_folder, "Roblox Studio.app")
        rbx.macOS_installedPath = os.path.join(cf.versions_folder)
        cf.content_folder_paths["Darwin"] = os.path.join(rbx.macOS_dir, "Contents", "Resources")
        cf.font_folder_paths["Darwin"] = os.path.join(cf.content_folder_paths['Darwin'], "content", "fonts")
        if not (os.path.exists(rbx.macOS_dir) or os.path.exists(os.path.join(cf.versions_folder, rbx.windows_player_folder_name))):
            startMessage(first=True)
            printSystemMessage("--- Installing Roblox to Bootstrap ---")
            printMainMessage(f"Please wait while we install Roblox into {obName0()}!")
            makedirs(os.path.join(cf.versions_folder))
            cf.submit_status.start()
            res = cf.handler.installRoblox(debug=cf.main_config.get("EFlagEnableDebugMode"))
            cf.submit_status.end()
            if res and res["success"] == False:
                printErrorMessage("There is an issue while trying to install Roblox. Please try again by restarting this app!")
                input("> ")
                sys.exit(0)
            if cf.main_os == "Windows":
                cf.pip_class.copyTreeWithMetadata(os.path.join(cf.cur_path, "_internal"), os.path.join(cf.versions_folder, cf.main_config.get("EFlagBootstrapRobloxInstallFolderName", rbx.windows_player_folder_name), "_internal"), dirs_exist_ok=True, ignore_if_not_exist=True)
                shutil.copy(os.path.join(cf.cur_path, "OrangeBlox.exe"), os.path.join(cf.versions_folder, cf.main_config.get("EFlagBootstrapRobloxInstallFolderName", rbx.windows_player_folder_name), "RobloxPlayerInstaller.exe"))
                with open(os.path.join(cf.versions_folder, cf.main_config.get("EFlagBootstrapRobloxInstallFolderName", rbx.windows_player_folder_name), "RobloxPlayerBetaPlayRobloxRestart.txt"), "w", encoding="utf-8") as f: f.write(cf.cur_path)
            elif cf.main_os == "Darwin":
                if os.path.exists(os.path.join(cf.macos_app_path, "../", "Play Roblox.app")):
                    cf.pip_class.copyTreeWithMetadata(os.path.join(cf.macos_app_path, "../", "Play Roblox.app"), os.path.join(rbx.macOS_dir, "Contents", "MacOS", "RobloxPlayerInstaller.app"), dirs_exist_ok=True)
                    with open(os.path.join(rbx.macOS_dir, "Contents", "MacOS", "RobloxPlayerInstaller.app", "Contents", "Resources", "RobloxPlayerBetaPlayRobloxRestart"), "w", encoding="utf-8") as f: f.write(cf.cur_path)
        if cf.main_config.get("EFlagUseIXPFastFlagsMethod2") == True:
            try:
                location = os.path.join(rbx.getLocalAppData(), "Roblox", "ClientSettings", "IxpSettings.json")
                if os.path.exists(location): os.remove(location)
                cf.main_config["EFlagUseIXPFastFlagsMethod2"] = False
                cf.main_config.pop("EFlagUseIXPFastFlagsMethod2")
            except Exception: printErrorMessage(f"Unable to delete IXP Settings due to method usage: {trace()}")
    except (KeyboardInterrupt, Exception):
        printErrorMessage("Uh oh! A Python exception that causes the script to end has occurred!")
        printErrorMessage(f"Exception: \n{trace()}")
        printErrorMessage(f"Location Code: 6")
        input("> ")
        sys.exit(0 if cf.main_os == "Darwin" else 1)
def updateRMEvents():
    try:
        mod_script_events = {
            # OrangeBlox Permissions
            "fastFlagConfiguration": {"message": ts("Edit or view your bootstrap configuration file"), "level": 3, "detection": "FastFlagConfiguration.json"},
            "configuration": {"message": ts("Edit or view your bootstrap configuration file"), "level": 3, "detection": "Configuration.json"},
            "editMainExecutable": {"message": ts("Edit the main bootstrap executable"), "level": 4, "detection": "Main.py"},
            "editRobloxFastFlagInstallerExecutable": {"message": ts("Edit the RobloxFastFlagInstaller executable"), "level": 4, "detection": "RobloxFastFlagsInstaller.py"},
            "editOrangeAPIExecutable": {"message": ts("Edit the OrangeAPI executable"), "level": 4, "detection": "OrangeAPI.py"},
            "editModScript": {"message": ts("Edit ModScript.py executable"), "level": 4, "detection": "ModScript.py"},
            "usageOfRobloxFastFlagsInstaller": {"message": ts("Allow access to use RobloxFastFlagsInstaller directly"), "level": 3, "detection": "RobloxFastFlagsInstaller"},
            "usageOfRobloxManager": {"message": ts("Allow access to use RobloxManager directly"), "level": 3, "detection": "RobloxManager"},
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
            "generateModOrder": {"message": ts("Get information about the install arrangement of your mods"), "level": 0},
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
            "getLatestRobloxPlayerVersion": {"message": ts("Get the current version of Roblox Player"), "level": 1},
            "getLatestRobloxStudioVersion": {"message": ts("Get the current version of Roblox Studio"), "level": 1},
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
            "restartRoblox": {"message": ts("Restart the Roblox Instance"), "level": 2},
            "joinRobloxGame": {"message": ts("Join a Roblox Game"), "level": 2},
            "changeRobloxWindowSizeAndPosition": {"message": ts("Change the Roblox Window Size and Position"), "level": 2},
            "setRobloxWindowTitle": {"message": ts("Set the Roblox Window Title [Windows Only]"), "level": 1},
            "setRobloxWindowIcon": {"message": ts("Set the Roblox Window Icon [Windows Only]"), "level": 1},
            "focusRobloxWindow": {"message": ts("Focus the Roblox Window to the top window"), "level": 2},
            "getIfOSSupported": {"message": ts("Get if your operating system version is within a certain version."), "level": 0},
            "getIfPythonSupported": {"message": ts("Get if your Python executable is supported."), "level": 0},
            "getIfConnectedToInternet": {"message": ts("Get if your computer is connected to the internet."), "level": 1},
            "getIf32BitWindows": {"message": ts("Get if your computer is 32 bit of Windows."), "level": 0, "free": True},
            "getConnectedUserInfo": {"message": ts(f"Get game user information from {obName0()}"), "level": 1},
            "getIfConnectedToGame": {"message": ts("Get if you connected to a Roblox game"), "level": 0},
            "getCurrentPlaceInfo": {"message": ts(f"Get game information from internal {obName0()}"), "level": 1},
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
            "getOrangeBloxName": {"message": ts("Get the name of OrangeBlox."), "level": 0, "free": True},
            "getOrangeBloxEmoji": {"message": ts("Get the emoji set for OrangeBlox."), "level": 0, "free": True},
            "getOrangeBloxColorAnsi": {"message": ts("Get the color set for OrangeBlox. (1)"), "level": 0, "free": True},
            "getOrangeBloxColorHex": {"message": ts("Get the color set for OrangeBlox. (2)"), "level": 0, "free": True},
            "printSuccessMessage": {"message": ts("Print a console in green (indicates success)"), "level": 0, "free": True},
            "printMainMessage": {"message": ts("Print a console in the standard white color"), "level": 0, "free": True},
            "printColoredMessage": {"message": ts("Print a message on the python console using an ANSI 256 bit color number."), "level": 0, "free": True},
            "printErrorMessage": {"message": ts("Print a console in red (indicates an error)"), "level": 0, "free": True},
            "printYellowMessage": {"message": ts("Print a console in a yellow text (indicates a warning)"), "level": 0, "free": True},
            "about": {"message": ts("Get bootstrap info"), "level": 0, "free": True}
        }
        cf.handler.roblox_event_info.update(mod_script_events)
    except (KeyboardInterrupt, Exception) as e:
        printErrorMessage("Uh oh! A Python exception that causes the script to end has occurred!")
        printErrorMessage(f"Exception: \n{trace()}")
        printErrorMessage(f"Location Code: 7")
        input("> ")
        sys.exit(0 if cf.main_os == "Darwin" else 1)
def fetchModsFromMacApp():
    try:
        if cf.main_os == "Darwin" and cf.main_config.get("EFlagLastModVersionMacOSCaching") != cf.current_version["version"]:
            printMainMessage("Syncing mods..")
            sync_folder_names = ["AvatarEditorMaps", "Cursors", "PlayerSounds", "RobloxBrand", "RobloxStudioBrand", "Mods"]
            for sync_folder_name in sync_folder_names:
                targeted_sync_location = os.path.join(cf.cur_path, "Mods", sync_folder_name)
                if os.path.exists(targeted_sync_location) and os.path.isdir(targeted_sync_location):
                    for i in os.listdir(targeted_sync_location):
                        syncing_mod_path = os.path.join(targeted_sync_location, i)
                        if os.path.isdir(syncing_mod_path) and i in cf.updating_mods[sync_folder_name]:
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
            cf.main_config["EFlagLastModVersionMacOSCaching"] = cf.current_version["version"]
            saveSettings()
    except Exception:
        printErrorMessage("Uh oh! A Python exception that causes the script to end has occurred!")
        printErrorMessage(f"Exception: \n{trace()}")
        printErrorMessage(f"Location Code: 10")
        input("> ")
        sys.exit(0 if cf.main_os == "Darwin" else 1)
def robloxInstallationCheck():
    try:
        if cf.main_os == "Windows":
            cf.content_folder_paths["Windows"] = cf.handler.getRobloxInstallFolder()
            if cf.content_folder_paths.get("Windows"):
                cf.font_folder_paths["Windows"] = os.path.join(cf.content_folder_paths['Windows'], "content", "fonts")
                if not os.path.exists(cf.font_folder_paths["Windows"]):
                    startMessage(first=True)
                    printSystemMessage("--- Installing Roblox ---")
                    printMainMessage(f"Please wait while we install Roblox into {obName0()}!")
                    cf.submit_status.start()
                    res = cf.handler.installRoblox(debug=cf.main_config.get("EFlagEnableDebugMode"), verifyInstall=cf.main_config.get("EFlagVerifyRobloxHashAfterInstall")!=False)
                    cf.submit_status.end()
                    if res and res["success"] == False:
                        printErrorMessage("There is an issue while trying to install Roblox. Please try again by restarting this app!")
                        input("> ")
                        sys.exit(0)
            else:
                startMessage(first=True)
                printSystemMessage("--- Installing Roblox ---")
                printMainMessage(f"Please wait while we install Roblox into {obName0()}!")
                cf.submit_status.start()
                res = cf.handler.installRoblox(debug=cf.main_config.get("EFlagEnableDebugMode"), verifyInstall=cf.main_config.get("EFlagVerifyRobloxHashAfterInstall")!=False)
                cf.submit_status.end()
                if res and res["success"] == False:
                    printErrorMessage("There is an issue while trying to install Roblox. Please try again by restarting this app!")
                    input("> ")
                    sys.exit(0)
        elif cf.main_os == "Darwin":
            if not os.path.exists(rbx.macOS_dir):
                startMessage(first=True)
                printSystemMessage("--- Installing Roblox ---")
                printMainMessage(f"Please wait while we install Roblox into {obName0()}!")
                cf.submit_status.start()
                res = cf.handler.installRoblox(debug=cf.main_config.get("EFlagEnableDebugMode"), verifyInstall=cf.main_config.get("EFlagVerifyRobloxHashAfterInstall")!=False)
                cf.submit_status.end()
                if res and res["success"] == False:
                    printErrorMessage("There is an issue while trying to install Roblox. Please try again by restarting this app!")
                    input("> ")
                    sys.exit(0)
        installed_roblox_version = cf.handler.getCurrentClientVersion()
        if installed_roblox_version["success"] != True:
            startMessage(first=True)
            printErrorMessage("Something went wrong trying to determine your current Roblox version.")
            input("> ")
            sys.exit(0)
    except (KeyboardInterrupt, Exception) as e:
        printErrorMessage("Uh oh! A Python exception that causes the script to end has occurred!")
        printErrorMessage(f"Exception: \n{trace()}")
        printErrorMessage(f"Location Code: 8")
        input("> ")
        sys.exit(0 if cf.main_os == "Darwin" else 1)
def urlArgumentExchange():
    try:
        argv = list(filter(None, sys.argv))
        if len(argv) > 1: cf.socket_authorization = argv[1]
        exchange_path = os.path.join(cf.cur_path, "URLLaunchExchange")
        if cf.main_os == "Darwin": exchange_path = os.path.join(cf.orangeblox_library, "URLLaunchExchange")
        if os.path.exists(exchange_path):
            with open(exchange_path, "r", encoding="utf-8") as f: filtered_args = f.read()
            cf.given_args = ["Main.py", filtered_args]
            os.remove(exchange_path)
    except (KeyboardInterrupt, Exception) as e:
        printErrorMessage("Uh oh! A Python exception that causes the script to end has occurred!")
        printErrorMessage(f"Exception: \n{trace()}")
        printErrorMessage(f"Location Code: 9")
        input("> ")
        sys.exit(0 if cf.main_os == "Darwin" else 1)
def startUp():
    firstActions() # First Actions
    requirementCheck() # Requirement Checks
    adjustRobloxInstallation() # Roblox Installation Usage Check
    updateRMEvents() # Update Mod Script Event Information
    fetchModsFromMacApp() # For macOS, Fetch Mods Folder
    robloxInstallationCheck() # Fetch or Install Roblox
    urlArgumentExchange() # URL Argument Exchange Between Loader and Main Script

if __name__ == "__main__":
    print("This module is not a runable instance.")
    sys.exit(1)