# 
# OrangeBlox 🍊
# Made by Efaz from efaz.dev
# v2.6.0a
# 

import Modules.config as cf
from Modules.printing import *
from Modules.utils import *
from Modules.startup import *
from Modules.options import *
from Modules.settings import continueToSettings
from Modules.modmanager import continueToModsManager
import os
import shutil
import json
import sys
import platform
    
def tutorial():
    printSystemMessage("--- Tutorial ---")
    printMainMessage(f"Welcome to {obName0()} {obName1()}!")
    printMainMessage(f"{obName0()} is a Roblox bootstrap that allows you to add modifications to your Roblox client using files, activity tracking and Python!")
    printMainMessage("Before we get started, there's some information that may be needed to know.")
    if validateInstallation(): printSuccessMessage("Installation Valid! You may continue! [✅]")
    else:
        printErrorMessage("Installation Invalid! Please use Install.py! [❌]")
        input("> ")
        sys.exit(0)
    information_num = 1
    printSystemMessage(f"--- Info #{information_num} ---")
    printMainMessage("There's lot of permissions that are needed to be set in order for this bootstrap to work.")
    printMainMessage(f"For example, it may ask you to allow access to the Roblox app files or allow access to a Terminal. Please put it in always allow in order to allow {obName0()} to function properly!")
    input("> ")
    information_num += 1
    printSystemMessage(f"--- Info #{information_num} ---")
    printMainMessage("Since this bootstrap is made using Python, anti-viruses may report this app as a virus.")
    printMainMessage(f"For example, Windows Defender may detect {obName0()} with Win32/Wacapew.C!ml. You may need to authorize the app through your anti-virus or build the app directly in order to allow use.")
    input("> ")
    information_num += 1
    printSystemMessage(f"--- Info #{information_num} ---")
    printMainMessage("Most features are based on Activity Tracking, a watching system based on watching Roblox logs in response of actions.")
    printMainMessage("This app will use your Roblox logs to track data such as Game Join Data, Discord Presences, BloxstrapRPC and a lot more!")
    printMainMessage("If you wish to change these settings, once you get to the settings menu, go to the Activity Tracking settings!")
    printYellowMessage("This will not get you banned as this is based on files, not interrupting the client.")
    input("> ")
    information_num += 1
    printSystemMessage(f"--- Info #{information_num} ---")
    displayNotification(ts("Hello!"), ts("If you see this, your notifications are set up! Great job!"))
    printMainMessage("We have just sent a notification to your computer, so that you can allow notifications")
    printYellowMessage("Depending on your OS (Windows or macOS), you may be able to select Allow for features like Server Locations to work!")
    input("> ")
    information_num += 1
    printSystemMessage(f"--- Info #{information_num} ---")
    printMainMessage("If you haven't noticed, we have also installed a Play Roblox and Run Studio app into your system!")
    printMainMessage(f"This will allow you to skip the main menu and launch Roblox instantly through {obName0()}!")
    if cf.main_os == "Darwin": printMainMessage("You may find this in your Applications folder or through Launchpad!")
    elif cf.main_os == "Windows": printMainMessage("You may find this in your Start Menu or Desktop!")
    input("> ")
    information_num += 1
    printSystemMessage(f"--- Info #{information_num} ---")
    printMainMessage(f"If you have issues with {obName0()}, you may report it on GitHub using the issues page:")
    printMainMessage("https://github.com/EfazDev/orangeblox/issues")
    printErrorMessage("However, please check if you're on the latest bootstrap version first before continuing. If you don't have the latest version, please do!")
    printYellowMessage("If you want to uninstall this bootstrap, you may run the Install.py script which you ran to be here and select Uninstall!")
    printYellowMessage("Additionally, you can use the Reinstall Roblox option in the settings menu to prevent uninstalling this.")
    printSystemMessage("--- Step 1 ---")
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
    printSystemMessage("--- Step 2 ---")
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
    printSystemMessage("--- Step 3 ---")
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
    printSystemMessage("--- Select Option ---")
    count = 1
    for i in generated_ui_options:
        printMainMessage(f"[{str(count)}] {i['message']}")
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
    printSystemMessage("--- Step 4 ---")
    if os.path.exists(os.path.join(cf.cur_path, "Translations")):
        printMainMessage("Alright! Now, select the bootstrap language you want to use! (English is default, you can just continue)")
        langs_sel = []
        co = 0
        for i, v in cf.language_names.items():
            co += 1
            langs_sel.append({
                "index": co,
                "message": v,
                "code": i
            })
        selected_language = generateMenuSelection(langs_sel, before_input=ts(f"Current Language: {cf.language_names[cf.main_config.get('EFlagSelectedBootstrapLanguage', 'en')]}\n[WARNING! All messages are translated from Google Translate and may provide incorrect or malformed information.]"))
        if selected_language:
            cf.main_config["EFlagSelectedBootstrapLanguage"] = selected_language["code"]
            cf.stdout.translation_obj.load_new_language(selected_language["code"])
            printMainMessage(f"Successfully set language to {cf.language_names[cf.main_config.get('EFlagSelectedBootstrapLanguage', 'en')]}! All future messages are now translated in this language.")
    if cf.main_config.get("EFlagDisableSettingsAccess") != True:
        printSystemMessage("--- Step 5 ---")
        printMainMessage("Nice job! Oh yea, during the tutorial, it repeated with a \"Not quite\" if you gave an incorrect input or response. However, it will close the window in future prompts like in main menu.")
        printYellowMessage("Additionally, if you do meet with an option with a *, this means that any input will result with that option.")
        printMainMessage("Anyways, welcome to step 4! Here, you can select your settings!")
        printMainMessage("In the settings menu, you can just input nothing or anything else instead of y or n to skip the option without affecting the current state of it.")
        printMainMessage("See you after a little bit!")
        input("> ")
        continueToSettings()
    if cf.main_config.get("EFlagDisableFastFlagInstallAccess") != True:
        printSystemMessage("--- Step 6 ---")
        printMainMessage("Welcome back! I hope you have enabled some things you may want!")
        printMainMessage("Now, let's get more customizable! Next, you will be able to select your fast flags.")
        printYellowMessage("But before, prepare yourself your Roblox User ID (if you're not currently logged in). It will be used for some settings depending on what you select.")
        input("> ")
        continueToFFlagInstaller()
    if cf.main_config.get("EFlagDisableModsManagerAccess") != True:
        printSystemMessage("--- Step 7 ---")
        printMainMessage("Hey! You made it through the list again!")
        printMainMessage("Now, let's explore the Mods category. Mods are files that can be used to edit your Roblox client such as a custom theme or font. Today, you will be configuring that.")
        printYellowMessage("If you want to get your own mods and install them, open the Mods Manager and use the open folder command! This will help you where to put the extracted mod.")
        input("> ")
        continueToModsManager()
    printSystemMessage("--- Final Touches ---")
    printSuccessMessage("Woo hoo! You finally reached the end of this tutorial!")
    printSuccessMessage("I hope you learned from this and how you may use Roblox using this bootstrap!")
    printSuccessMessage("For now, before you continue, I hope you have a great day!")
    input("> ")
    getSettings()
    cf.main_config["EFlagCompletedTutorial"] = True
    saveSettings()
    startMessage()
def backupAssistant():
    printSystemMessage(f"--- {obName0()} Backup Assistant ---")
    printMainMessage(f"It seems that you have installed {obName0()} with a backup file included.")
    printMainMessage(f"Path: {os.path.join(cf.cur_path, 'Backup.obx')}")
    printMainMessage("Would you like to restore the data on it? (y/n)")
    printYellowMessage("This will overwrite your current configuration and mods!!")
    back = input("> ")
    if isYes(back) == True:
        backup_path = os.path.join(cf.cur_path, "Backup")
        backup_file = os.path.join(cf.cur_path, "Backup.obx")
        try:
            printMainMessage(f"Unwrapping {obName0()} file..")
            makedirs(backup_path)
            zip_extract = cf.pip_class.unzipFile(backup_file, backup_path, ["FastFlagConfiguration.json", "Cursors", "Mods", "RobloxBrand"])
            if zip_extract.returncode == 0:
                printMainMessage("Copying Configuration.json..")
                if os.path.exists(os.path.join(backup_path, "FastFlagConfiguration.json")):
                    with open(os.path.join(backup_path, "FastFlagConfiguration.json"), "r", encoding="utf-8") as f: cf.main_config = json.load(f)
                else:
                    with open(os.path.join(backup_path, "Configuration.json"), "rb") as f: obfuscated_json = f.read()
                    try: obfuscated_json = json.loads(obfuscated_json)
                    except Exception: obfuscated_json = json.loads(zlib.decompress(obfuscated_json).decode("utf-8", errors="ignore"))
                    cf.main_config = obfuscated_json
                saveSettings()
                printMainMessage("Copying AvatarEditorMaps..")
                cf.pip_class.copyTreeWithMetadata(os.path.join(backup_path, "AvatarEditorMaps"), os.path.join(cf.mods_folder, "AvatarEditorMaps"), dirs_exist_ok=True, ignore_if_not_exist=True)
                printMainMessage("Copying Cursors..")
                cf.pip_class.copyTreeWithMetadata(os.path.join(backup_path, "Cursors"), os.path.join(cf.mods_folder, "Cursors"), dirs_exist_ok=True, ignore_if_not_exist=True)
                if os.path.exists(os.path.join(backup_path, "PlayerSounds")):
                    printMainMessage("Copying PlayerSounds..")
                    cf.pip_class.copyTreeWithMetadata(os.path.join(backup_path, "PlayerSounds"), os.path.join(cf.mods_folder, "PlayerSounds"), dirs_exist_ok=True, ignore_if_not_exist=True)
                else:
                    printMainMessage("Copying DeathSounds..")
                    cf.pip_class.copyTreeWithMetadata(os.path.join(backup_path, "DeathSounds"), os.path.join(cf.mods_folder, "DeathSounds"), dirs_exist_ok=True, ignore_if_not_exist=True)
                    if os.path.exists(os.path.join(cf.mods_folder, "DeathSounds")):
                        for i in os.listdir(os.path.join(cf.mods_folder, "DeathSounds")):
                            if os.path.isfile(os.path.join(cf.mods_folder, "DeathSounds", i)):
                                possible_name = i.split(".")
                                if len(possible_name) > 1: possible_name = possible_name[0]
                                else: possible_name = i
                                makedirs(os.path.join(backup_path, "PlayerSounds", possible_name))
                                shutil.copy(os.path.join(cf.mods_folder, "DeathSounds", i), os.path.join(cf.mods_folder, "PlayerSounds", possible_name, "ouch.ogg"), follow_symlinks=False)
                        shutil.rmtree(os.path.join(cf.mods_folder, "DeathSounds"), ignore_errors=True)
                printMainMessage("Copying Mods..")
                cf.pip_class.copyTreeWithMetadata(os.path.join(backup_path, "Mods"), os.path.join(cf.mods_folder, "Mods"), dirs_exist_ok=True, ignore_if_not_exist=True)
                printMainMessage("Copying RobloxBrand..")
                cf.pip_class.copyTreeWithMetadata(os.path.join(backup_path, "RobloxBrand"), os.path.join(cf.mods_folder, "RobloxBrand"), dirs_exist_ok=True, ignore_if_not_exist=True)
                printMainMessage("Copying RobloxStudioBrand..")
                cf.pip_class.copyTreeWithMetadata(os.path.join(backup_path, "RobloxStudioBrand"), os.path.join(cf.mods_folder, "RobloxStudioBrand"), dirs_exist_ok=True, ignore_if_not_exist=True)
                printMainMessage("Finished transferring! Deleting backup data..")
                if os.path.exists(backup_path): shutil.rmtree(backup_path, ignore_errors=True)
                if os.path.exists(os.path.join(cf.cur_path, "Backup.obx")): os.remove(os.path.join(cf.cur_path, "Backup.obx"))
                printSuccessMessage(f"Successfully restored {obName0()} data! Would you to restart the app? (y/n)")
                a = input("> ")
                if isYes(a) == True: cf.pip_class.restartScript("Main.py", sys.argv)
                else: sys.exit(0)
            else: raise Exception(f"There was an issue trying to open the {obName0()} file! Make sure it's readable before trying again!")
        except Exception:
            printErrorMessage(f"There was an error trying to restore your {obName0()} files!")
            printErrorMessage(f"Python Exception: \n{trace()}")
            input("> ")
            sys.exit(0)
            return
def urlSchemeHandler():
    url = cf.given_args[1]
    if ("efaz-bootstrap" in url or url.startswith("obx-launch") or ("orangeblox" in url and not url.endswith(".obx"))) and not (url.startswith("obx-launch-studio") or url.startswith("obx-launch-player")) and not os.path.isfile(url):
        try:
            if "obx-launch" in url: cf.given_args[1] = cf.given_args[1].replace("obx-launch ", "").replace("obx-launch", "")
            if "continue" in url: continueToRoblox()
            elif "run-studio" in url: continueToRoblox(studio=True)
            elif "url-quick-launch" in url: urlQuickLaunch()
            elif "new" in url: continueToRoblox()
            elif "reconnect-studio" in url: connectExistingRobloxWindow(studio=True)
            elif "reconnect" in url: connectExistingRobloxWindow()
            elif "python-updates" in url: 
                continueToUpdatePython()
                if not ("?quick-action=true" in url): optionSelection()
                else: optionSelection(isRedirectedFromApp=True)
            elif "python-module-updates" in url: 
                continueToUpdatePythonModules()
                if not ("?quick-action=true" in url): optionSelection()
                else: optionSelection(isRedirectedFromApp=True)
            elif "fflag-install" in url:
                continueToFFlagInstaller()
                if not ("?quick-action=true" in url): optionSelection()
                else: optionSelection(isRedirectedFromApp=True)
            elif "settings" in url:
                continueToSettings()
                if not ("?quick-action=true" in url): optionSelection()
                else: optionSelection(isRedirectedFromApp=True)
            elif "sync-to-install" in url:
                syncToFFlagConfiguration()
                if not ("?quick-action=true" in url): optionSelection()
                else: optionSelection(isRedirectedFromApp=True)
            elif "sync-from-install" in url:
                syncFromFFlagConfiguration()
                if not ("?quick-action=true" in url): optionSelection()
                else: optionSelection(isRedirectedFromApp=True)
            elif "end-roblox-studio" in url:
                continueToEndRobloxInstances(studio=True)
                if not ("?quick-action=true" in url): optionSelection()
                else: optionSelection(isRedirectedFromApp=True)
            elif "end-roblox" in url:
                continueToEndRobloxInstances()
                if not ("?quick-action=true" in url): optionSelection()
                else: optionSelection(isRedirectedFromApp=True)
            elif "reinstall-roblox" in url:
                continueToInstallRobloxOptions(reinstall=True)
                if not ("?quick-action=true" in url): optionSelection()
                else: optionSelection(isRedirectedFromApp=True)
            elif "roblox-installer-options" in url:
                continueToInstallRobloxOptions()
                if not ("?quick-action=true" in url): optionSelection()
                else:  optionSelection(isRedirectedFromApp=True)
            elif ("credits" in url) or ("about" in url):
                continueToCredits()
                if not ("?quick-action=true" in url): optionSelection()
                else: optionSelection(isRedirectedFromApp=True)
            elif "mods" in url:
                continueToModsManager()
                if not ("?quick-action=true" in url): optionSelection()
                else: optionSelection(isRedirectedFromApp=True)
            elif "temporary-storage" in url or "clear-logs" in url:
                continueToClearTemporaryStorage()
                if not ("?quick-action=true" in url): optionSelection()
                else: optionSelection(isRedirectedFromApp=True)
            elif ("shortcuts/" in url): continueToLinkShortcuts(url)
            else:
                printSystemMessage("--- Unknown URL ---")
                printMainMessage("There was an issue trying to parse your URL scheme. Please select an option below to continue:")
                printDebugMessage(f"URL Scheme Requested: {url}")
                printDebugMessage(f"Arguments Received: {cf.given_args}")
                printMainMessage("[1] Return to Main Menu")
                printMainMessage("[2] Continue to Roblox")
                printMainMessage("[*] End Process")
                res = input("> ")
                if res == "1":
                    cf.given_args = ["Main.py"]
                    launch()
                elif res == "2":
                    cf.given_args = ["orangeblox://continue"]
                    continueToRoblox()
                else: sys.exit(0)
        except BaseException as e:
            if type(e) is SystemExit: raise e
            printErrorMessage("Uh oh! A Python exception that causes the script to end has occurred!")
            printErrorMessage(f"Exception: \n{trace()}")
            printErrorMessage(f"Location Code: 2")
            if not ("?quick-action=true" in url): optionSelection()
            else: optionSelection(isRedirectedFromApp=True)
    elif os.path.isfile(url):
        if url.endswith(".rbxl") or url.endswith(".rbxlx"):
            printSystemMessage("--- Redirecting to Roblox Studio! ---")
            printMainMessage("Successfully loaded Roblox URL Scheme! Continuing to Roblox Studio..")
            cf.run_studio = True
        elif url.endswith(".obx"):
            if os.path.exists(url):
                try:
                    printSystemMessage(f"--- {obName0()} Backup Assistant ---")
                    printMainMessage(f"Are you sure you want to restore your {obName0()} files using the following {obName0()} file?")
                    printMainMessage(f"File: {url}")
                    printErrorMessage("This operation is dangerous to use if not used carefully and will overwrite your Mods and Configuration.")
                    printErrorMessage("If someone that you have recently met sent you this file, do not use!!")
                    printErrorMessage("Please backup your Fast Flag Configurations and Mods as this may break before continuing!")
                    PyKits.TimerBar(30, "Are you sure you want to continue with this file? (y/n)", False).start()
                    d = input("> ")
                    if isYes(d) == True:
                        backup_path = os.path.join(cf.cur_path, "Backup")
                        backup_file = url
                        try:
                            printMainMessage(f"Unwrapping {obName0()} file..")
                            makedirs(backup_path)
                            zip_extract = cf.pip_class.unzipFile(backup_file, backup_path, ["FastFlagConfiguration.json", "Cursors", "Mods", "RobloxBrand"])
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
                                    printSystemMessage("--- Attention Needed! ---")
                                    printMainMessage(f"This backup is created in a version before {obName0()} v2.0.1. Are you sure you want to continue with this backup? (y/n)")
                                    a = input("> ")
                                    if isYes(a) == False: sys.exit(0); return
                                elif back_metadata.get("bootstrap_version") > cf.current_version["version"]:
                                    printSystemMessage("--- Attention Needed! ---")
                                    printMainMessage(f"This backup is created in a version (v{back_metadata.get('bootstrap_version')}) after {obName0()} v{cf.current_version['version']}. Are you sure you want to continue with this backup? (y/n)")
                                    a = input("> ")
                                    if isYes(a) == False: sys.exit(0); return
                                elif back_metadata.get("bootstrap_version") < cf.current_version["version"]:
                                    printSystemMessage("--- Attention Needed! ---")
                                    printMainMessage(f"This backup is created in a version (v{back_metadata.get('bootstrap_version')}) before {obName0()} v{cf.current_version['version']}. Are you sure you want to continue with this backup? (y/n)")
                                    a = input("> ")
                                    if isYes(a) == False: sys.exit(0); return
                                printMainMessage("Copying Configuration.json..")
                                if os.path.exists(os.path.join(backup_path, "FastFlagConfiguration.json")):
                                    with open(os.path.join(backup_path, "FastFlagConfiguration.json"), "r", encoding="utf-8") as f: cf.main_config = json.load(f)
                                else:
                                    with open(os.path.join(backup_path, "Configuration.json"), "rb") as f: obfuscated_json = f.read()
                                    try: obfuscated_json = json.loads(obfuscated_json)
                                    except Exception: obfuscated_json = json.loads(zlib.decompress(obfuscated_json).decode("utf-8", errors="ignore"))
                                    cf.main_config = obfuscated_json
                                saveSettings()
                                printMainMessage("Copying AvatarEditorMaps..")
                                cf.pip_class.copyTreeWithMetadata(os.path.join(backup_path, "AvatarEditorMaps"), os.path.join(cf.mods_folder, "AvatarEditorMaps"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                printMainMessage("Copying Cursors..")
                                cf.pip_class.copyTreeWithMetadata(os.path.join(backup_path, "Cursors"), os.path.join(cf.mods_folder, "Cursors"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                if os.path.exists(os.path.join(backup_path, "PlayerSounds")):
                                    printMainMessage("Copying PlayerSounds..")
                                    cf.pip_class.copyTreeWithMetadata(os.path.join(backup_path, "PlayerSounds"), os.path.join(cf.mods_folder, "PlayerSounds"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                else:
                                    printMainMessage("Copying DeathSounds..")
                                    cf.pip_class.copyTreeWithMetadata(os.path.join(backup_path, "DeathSounds"), os.path.join(cf.mods_folder, "DeathSounds"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                    if os.path.exists(os.path.join(cf.cur_path, "DeathSounds")):
                                        for i in os.listdir(os.path.join(cf.cur_path, "DeathSounds")):
                                            if os.path.isfile(os.path.join(cf.cur_path, "DeathSounds", i)):
                                                possible_name = i.split(".")
                                                if len(possible_name) > 1: possible_name = possible_name[0]
                                                else: possible_name = i
                                                makedirs(os.path.join(backup_path, "PlayerSounds", possible_name))
                                                shutil.copy(os.path.join(cf.cur_path, "DeathSounds", i), os.path.join(cf.mods_folder, "PlayerSounds", possible_name, "ouch.ogg"), follow_symlinks=False)
                                        shutil.rmtree(os.path.join(cf.cur_path, "DeathSounds"), ignore_errors=True)
                                printMainMessage("Copying Mods..")
                                cf.pip_class.copyTreeWithMetadata(os.path.join(backup_path, "Mods"), os.path.join(cf.mods_folder, "Mods"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                printMainMessage("Copying RobloxBrand..")
                                cf.pip_class.copyTreeWithMetadata(os.path.join(backup_path, "RobloxBrand"), os.path.join(cf.mods_folder, "RobloxBrand"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                printMainMessage("Copying RobloxStudioBrand..")
                                cf.pip_class.copyTreeWithMetadata(os.path.join(backup_path, "RobloxStudioBrand"), os.path.join(cf.mods_folder, "RobloxStudioBrand"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                printMainMessage("Finished transferring! Deleting backup data..")
                                if os.path.exists(backup_path): shutil.rmtree(backup_path, ignore_errors=True)
                                printSuccessMessage(f"Successfully restored {obName0()} data! Would you to restart the app? (y/n)")
                                a = input("> ")
                                if isYes(a) == True: cf.pip_class.restartScript("Main.py", sys.argv)
                                else: sys.exit(0)
                            else: raise Exception(f"There was an issue trying to open the {obName0()} file! Make sure it's readable before trying again!")
                        except Exception:
                            printErrorMessage(f"There was an error trying to restore your {obName0()} files!")
                            printErrorMessage(f"Python Exception: \n{trace()}")
                            input("> ")
                            sys.exit(0)
                            return
                    else: sys.exit(0)
                except Exception:
                    printSystemMessage(f"--- {obName0()} Backup Assistant ---")
                    printErrorMessage(f"Something went wrong: \n{trace()}")
                    input("> ")
                    sys.exit(0)
            else:
                printSystemMessage(f"--- {obName0()} Backup Assistant ---")
                printErrorMessage(f"Unable to read {obName0()} file due to the file not existing or unable to be accessed.")
                input("> ")
                sys.exit(0)
        else:
            printSystemMessage(f"--- Unknown file ---")
            printErrorMessage(f"Unable to read {obName0()} file due to the file handler not added.")
            input("> ")
            sys.exit(0)
    elif "roblox-studio" in url or url.startswith("obx-launch-studio"):
        printSystemMessage("--- Redirecting to Roblox Studio! ---")
        printMainMessage("Successfully loaded Roblox Studio URL Scheme! Continuing to Roblox Studio..")
        cf.run_studio = True
        if "obx-launch-studio" in url: cf.given_args[1] = cf.given_args[1].replace("obx-launch-studio ", "").replace("obx-launch-studio", "")
    elif "roblox" in url or url.startswith("obx-launch-player"):
        printSystemMessage("--- Redirecting to Roblox! ---")
        printMainMessage("Successfully loaded Roblox URL Scheme! Continuing to Roblox..")
        if cf.main_config.get("EFlagEnableSkipModificationMode") == True: cf.skip_modification_mode = True
        if "obx-launch-player" in url: cf.given_args[1] = cf.given_args[1].replace("obx-launch-player ", "").replace("obx-launch-player", "")
    else:
        printSystemMessage("--- Unknown URL ---")
        printMainMessage("There was an issue trying to parse your URL scheme. Please select an option below to continue:")
        printDebugMessage(f"URL Scheme Requested: {url}")
        printDebugMessage(f"Arguments Received: {cf.given_args}")
        printMainMessage("[1] Return to Main Menu")
        printMainMessage("[2] Continue to Roblox")
        printMainMessage("[*] End Process")
        res = input("> ")
        if res == "1":
            cf.given_args = []
            launch()
        elif res == "2":
            cf.given_args = ["orangeblox://continue"]
            continueToRoblox()
        else: sys.exit(0)
def mainMenu():
    rbx_open = cf.handler.getIfRobloxIsOpen()
    rbx_studio_open = cf.handler.getIfRobloxIsOpen(studio=True)
    generated_ui_options = []
    generated_ui_options.append({
        "index": 1, 
        "message": ts("Continue to Roblox"), 
        "func": continueToRoblox, 
        "go_to_rbx": False
    })
    if cf.main_config.get("EFlagRobloxStudioEnabled") == True:
        generated_ui_options.append({
            "index": 2, 
            "message": ts("Continue to Roblox Studio"),
            "func": continueToRoblox, 
            "go_to_rbx": False,
            "studio": True
        })
    if cf.main_config.get("EFlagAllowActivityTracking") != False:
        if rbx_open:
            generated_ui_options.append({
                "index": 3, 
                "message": ts("Connect to Existing Roblox"), 
                "func": connectExistingRobloxWindow, 
                "go_to_rbx": False
            })
        if cf.main_config.get("EFlagRobloxStudioEnabled") == True and rbx_studio_open:
            generated_ui_options.append({
                "index": 4, 
                "message": ts("Connect to Existing Roblox Studio"), 
                "func": connectExistingRobloxWindow, 
                "go_to_rbx": False,
                "studio": True
            })
    if cf.main_config.get("EFlagEnableURLQuickLaunch") == True:
        generated_ui_options.append({
            "index": 5, 
            "message": ts("URL Quick Launch"), 
            "func": urlQuickLaunch, 
            "go_to_rbx": False
        })
    if cf.main_config.get("EFlagDisableModsManagerAccess") != True:
        generated_ui_options.append({
            "index": 6, 
            "message": ts("Open Mods Manager"), 
            "func": continueToModsManager, 
            "go_to_rbx": True, 
            "end_mes": ts("Mod Settings has been saved!"),
            "clear_console": True
        })
    if cf.main_config.get("EFlagDisableSettingsAccess") != True:
        generated_ui_options.append({
            "index": 7, 
            "message": ts("Open Settings"), 
            "func": continueToSettings, 
            "go_to_rbx": True, 
            "end_mes": ts("Settings has been saved!"),
            "clear_console": True
        })
    if cf.main_config.get("EFlagDisableLinkShortcutsAccess") != True:
        generated_ui_options.append({
            "index": 8, 
            "message": ts("Roblox Link Shortcuts"), 
            "func": continueToLinkShortcuts, 
            "go_to_rbx": False, 
            "end_mes": ts("Roblox Link Shortcut Settings are now saved!"),
            "clear_console": True
        })
    if cf.main_config.get("EFlagDisablePythonUpdateChecks") != True:
        current_python_version = cf.pip_class.getCurrentPythonVersion()
        is_python_beta = cf.pip_class.getIfPythonVersionIsBeta()
        def python_update_check():
            latest_python_version = cf.pip_class.getLatestPythonVersion(beta=is_python_beta)
            if current_python_version != latest_python_version and latest_python_version:
                if os.path.exists(generateFileKey("PythonUpdate")):
                    with open(generateFileKey("PythonUpdate"), "r") as f: ss = f.read()
                    if ss == latest_python_version: return
                with open(generateFileKey("PythonUpdate"), "w", encoding="utf-8") as f: f.write(latest_python_version)
            elif latest_python_version and os.path.exists(generateFileKey("PythonUpdate")): os.remove(generateFileKey("PythonUpdate"))
        cf.pip_class.startThread(func=python_update_check, daemon=True)
        if os.path.exists(generateFileKey("PythonUpdate")):
            with open(generateFileKey("PythonUpdate"), "r") as f: latest_python_version = f.read()
            if current_python_version != latest_python_version and latest_python_version:
                generated_ui_options.append({
                    "index": 8.5, 
                    "message": ts(f"Update Python {cf.colors_class.wrap(f'[v{current_python_version} => v{latest_python_version}]', 226 if is_python_beta else 82)}"), 
                    "func": continueToUpdatePython, 
                    "go_to_rbx": True, 
                    "end_mes": ts("Python has been updated!"),
                    "clear_console": True
                })
                displayNotification(ts("Python Update Available!"), ts(f'Python {latest_python_version} is now available for download! Install the update by opening the main menu, checking for Python updates and then install!'))
            else: os.remove(generateFileKey("PythonUpdate"))
    if cf.main_config.get("EFlagDisablePythonModuleUpdateChecks") != True:
        def python_module_update_check():
            updating_python_modules = cf.pip_class.updates()
            if updating_python_modules and updating_python_modules["success"] == True:
                if len(updating_python_modules["packages"]) > 0:
                    dumped = json.dumps(updating_python_modules["packages"], ensure_ascii=False)
                    if os.path.exists(generateFileKey("PythonModuleUpdate")):
                        with open(generateFileKey("PythonModuleUpdate"), "r") as f: ss = f.read()
                        if ss == dumped: return
                    with open(generateFileKey("PythonModuleUpdate"), "w", encoding="utf-8") as f: f.write(dumped)
                    displayNotification(ts("Python Module Updates Available!"), ts(f'{len(updating_python_modules["packages"])} Python module{"" if len(updating_python_modules["packages"]) == 1 else "s"} are now available to be updated! Install the update by opening the main menu, checking for Python Module updates and then install!'))
                elif os.path.exists(generateFileKey("PythonModuleUpdate")): os.remove(generateFileKey("PythonModuleUpdate"))
        cf.pip_class.startThread(func=python_module_update_check, daemon=True)
        if os.path.exists(generateFileKey("PythonModuleUpdate")):
            with open(generateFileKey("PythonModuleUpdate"), "r") as f: modules_updating = json.load(f)
            if len(modules_updating) > 0:
                generated_ui_options.append({
                    "index": 8.75, 
                    "message": ts(f"Update Python Modules {cf.colors_class.wrap(f'[+{len(modules_updating)}]', 82)}"), 
                    "func": continueToUpdatePythonModules, 
                    "go_to_rbx": True, 
                    "end_mes": ts("Python Modules has been updated!"),
                    "clear_console": True
                })
            else: os.remove(generateFileKey("PythonModuleUpdate"))
    if cf.main_config.get("EFlagDisableBootstrapChecks") != True:
        def bootstrap_update_check():
            get_updates_anyway = True
            emoji_to_define_update = ""
            unic = ""
            version_server = cf.main_config.get("EFlagBootstrapUpdateServer", "https://obx.efaz.dev/Version.json")
            if version_server == "https://obx.efaz.dev/Version.json": emoji_to_define_update = "✅"; get_updates_anyway = True; unic = "82"
            elif version_server == "https://obxbeta.efaz.dev/Version.json" or version_server == "https://raw.githubusercontent.com/EfazDev/orangeblox/refs/heads/beta/Version.json": emoji_to_define_update = "⚠️"; get_updates_anyway = True; unic = "226"
            elif cf.main_config.get("EFlagUpdatesAuthorizationKey", "") != "": emoji_to_define_update = "🔨"; get_updates_anyway = True; unic = "226"
            else: emoji_to_define_update = "❌"; get_updates_anyway = False; unic = "196"
            if get_updates_anyway == True:
                if not (type(version_server) is str and version_server.startswith("https://")): version_server = "https://obx.efaz.dev/Version.json"
                try: latest_vers_res = cf.requests.get(f"{version_server}", headers={"X-Bootstrap-Version": cf.current_version["version"], "X-Python-Version": platform.python_version(), "X-Authorization-Key": cf.main_config.get("EFlagUpdatesAuthorizationKey", "")})
                except Exception: latest_vers_res = PyKits.InstantRequestJSONResponse(ok=False)
                if latest_vers_res.ok:
                    latest_vers = latest_vers_res.json
                    if cf.current_version.get("version"):
                        if cf.current_version.get("version", "1.0.0") < latest_vers.get("latest_version", "1.0.0"):
                            versio_name = cf.colors_class.wrap(ts(f'New Updates Available! [v{cf.current_version.get("version", "1.0.0")} => v{latest_vers.get("latest_version", "1.0.0")}] [{emoji_to_define_update}]'), unic)
                            if os.path.exists(generateFileKey("OrangeBloxUpdate")):
                                with open(generateFileKey("OrangeBloxUpdate"), "r", encoding="utf-8") as f: ss = f.read()
                                if ss == versio_name: return
                            with open(generateFileKey("OrangeBloxUpdate"), "w", encoding="utf-8") as f: f.write(versio_name)
                            displayNotification(ts(f"{obName0()} Update Available!"), ts(f'{obName0()} v{latest_vers.get("latest_version", "1.0.0")} is now available for download! Install the update by opening the main menu, checking for updates and then install!'))
                        else:
                            if os.path.exists(generateFileKey("OrangeBloxUpdate")): os.remove(generateFileKey("OrangeBloxUpdate"))
        cf.pip_class.startThread(func=bootstrap_update_check, daemon=True)
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
        version_server = cf.main_config.get("EFlagBootstrapUpdateServer", "https://obx.efaz.dev/Version.json")
        if version_server == "https://obx.efaz.dev/Version.json": emoji_to_define_update = "✅"; unic = "82"
        elif version_server == "https://obxbeta.efaz.dev/Version.json" or version_server == "https://raw.githubusercontent.com/EfazDev/orangeblox/refs/heads/beta/Version.json": emoji_to_define_update = "⚠️"; unic = "226"
        elif cf.main_config.get("EFlagUpdatesAuthorizationKey", "") != "": emoji_to_define_update = "🔨"; unic = "226"
        else: emoji_to_define_update = "❌"; unic = "196"
        generated_ui_options.append({
            "index": 9, 
            "message": cf.colors_class.wrap(ts(f"Check for Updates [{emoji_to_define_update}]"), unic), 
            "func": continueToUpdates, 
            "go_to_rbx": True, 
            "end_mes": ts("Finished checking for updates!"),
            "clear_console": True
        })
    if rbx_open:
        generated_ui_options.append({
            "index": 10, 
            "message": ts("End All Roblox Instances"), 
            "func": continueToEndRobloxInstances, 
            "go_to_rbx": True, 
            "end_mes": ts("Roblox Instances have been ended!"),
            "clear_console": True
        })
    if cf.main_config.get("EFlagRobloxStudioEnabled") == True and rbx_studio_open:
        generated_ui_options.append({
            "index": 11, 
            "message": ts("End All Roblox Studio Instances"), 
            "func": continueToEndRobloxInstances, 
            "go_to_rbx": True, 
            "end_mes": ts("Roblox Instances have been ended!"),
            "clear_console": True,
            "studio": True
        })
    if cf.main_config.get("EFlagRobloxUnfriendCheckEnabled") == True:
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
    printSystemMessage("--- Main Menu ---")
    opt = generateMenuSelection(generated_ui_options, star_option=ts("Exit Bootstrap"))
    if opt:
        try:
            if opt.get("clear_console") == True: startMessage()
            if opt.get("studio") == True: re = opt["func"](studio=True)
            else: re = opt["func"]()
            if opt.get("go_to_rbx") == True: 
                if type(re) is str: optionSelection(re)
                else: optionSelection(opt.get("end_mes"))
        except BaseException as e:
            if type(e) is SystemExit: raise e
            printErrorMessage("Uh oh! A Python exception that causes the script to end has occurred!")
            printErrorMessage(f"Exception: \n{trace()}")
            printErrorMessage(f"Location Code: 1")
            optionSelection(ts("An error occurred!"))
    else: sys.exit(0)
    getSettings()
def launch():
    startMessage()
    if not cf.socket_authorization:
        printSystemMessage("--- Authorization Required! ---")
        printMainMessage(f"Please launch {obName0()} from the official launcher in order to continue!")
        input("> ")
        sys.exit(0)
    if os.path.exists(os.path.join(cf.cur_path, "Backup.obx")): backupAssistant()
    if cf.main_config.get("EFlagCompletedTutorial") != True: tutorial()
    if (len(cf.given_args) < 2):
        if not validateInstallation():
            printSystemMessage("--- Install Required! ---")
            printMainMessage(f"Please install {obName0()} from running Install.py in order to continue!")
            input("> ")
            sys.exit(0)
        mainMenu()
    elif len(cf.given_args) > 1: urlSchemeHandler()
def optionSelection(mes=None, isRedirectedFromApp=False): # Handle Continue to Roblox
    if mes == None: mes = ts("Option finished! Would you like to return to the main menu or would you like to continue to Roblox?")
    else:
        if mes == "": mes = ts(f"Would you like to return to the main menu or would you like to continue to Roblox?")
        else: mes = ts(f"{mes} Would you like to return to the main menu or would you like to continue to Roblox?")
    if cf.main_config.get("EFlagReturnToMainMenuInstant") != True:
        if isRedirectedFromApp == False:
            printSystemMessage(mes)
            printMainMessage("[1] Return to Main Menu")
            printMainMessage("[2] Exit Bootstrap")
            if cf.main_config.get("EFlagRobloxStudioEnabled") == True: printMainMessage("[3] Continue to Roblox Studio")
            printMainMessage("[*] Continue to Roblox")
            a = input("> ")
            if a == "1": launch()
            elif a == "2": sys.exit(0)
            elif a == "3" and cf.main_config.get("EFlagRobloxStudioEnabled") == True: continueToRoblox(studio=True)
        else:
            printSystemMessage(mes)
            printMainMessage("[1] Continue to Roblox")
            if cf.main_config.get("EFlagRobloxStudioEnabled") == True: printMainMessage("[2] Continue to Roblox Studio")
            printMainMessage("[*] Exit Bootstrap")
            a = input("> ")
            if a == "1": continueToRoblox()
            elif a == "2" and cf.main_config.get("EFlagRobloxStudioEnabled") == True: continueToRoblox(studio=True)
            else: sys.exit(0)
    elif isRedirectedFromApp == False: launch()
    else: cf.given_args = ["Main.py"]; launch()

if __name__ == "__main__":
    print("This module is not a runable instance.")
    sys.exit(1)