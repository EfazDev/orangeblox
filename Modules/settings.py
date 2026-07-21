# 
# OrangeBlox 🍊
# Made by Efaz from efaz.dev
# v2.6.0i
# 

import Modules.config as cf
from Modules.printing import *
from Modules.startup import *
from Modules.utils import *
from Modules.options import *
import os
import sys
import re

def handleBasicSetting(fflag, default, ex=True):
    printMainMessage(f'Current Setting: {(cf.main_config.get(fflag, default)==ex)}')
    d = input("> ")
    if isYes(d) == True:
        cf.main_config[fflag] = True
        printDebugMessage("User selected: True")
    elif isRequestClose(d) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
    elif isNo(d) == True:
        cf.main_config[fflag] = False
        printDebugMessage("User selected: False")
def robloxSettings():
    printSystemMessage("--- Roblox Settings ---")
    printMainMessage(f"Would you like to enable using Roblox Studio with {obName0()}? (y/n)")
    d = handleBasicSetting("EFlagRobloxStudioEnabled", False)
    if d: return d

    printMainMessage("Would you like to reinstall a fresh copy of Roblox every launch? (y/n)")
    d = handleBasicSetting("EFlagFreshCopyRoblox", False)
    if d: return d

    printMainMessage(f"Would you like to set the URL Schemes for the Roblox Client and {obName0()}? [Needed for Link Shortcuts and when Roblox updates] (y/n)")
    d = handleBasicSetting("EFlagDisableURLSchemeInstall", False, False)
    if d: return d

    printMainMessage("Would you like to set start arguments for Roblox Player? (y/n)")
    printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagRobloxPlayerArguments"))}')
    d = input("> ")
    if isYes(d) == True:
        printMainMessage("Input the start arguments to use when running Roblox!")
        cf.main_config["EFlagRobloxPlayerArguments"] = input("> ")
        printDebugMessage(f'User selected: {cf.main_config.get("EFlagRobloxPlayerArguments")}')
    elif isRequestClose(d) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
    elif isNo(d) == True:
        cf.main_config["EFlagRobloxPlayerArguments"] = None
        printDebugMessage("User selected: None")

    if cf.main_config.get("EFlagRobloxStudioEnabled") == True:
        printMainMessage("Would you like to set start arguments for Roblox Studio? (y/n)")
        printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagRobloxStudioArguments"))}')
        d = input("> ")
        if isYes(d) == True:
            printMainMessage("Input the start arguments to use when running Roblox Studio!")
            cf.main_config["EFlagRobloxStudioArguments"] = input("> ")
            printDebugMessage(f'User selected: {cf.main_config.get("EFlagRobloxStudioArguments")}')
        elif isRequestClose(d) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
        elif isNo(d) == True:
            cf.main_config["EFlagRobloxStudioArguments"] = None
            printDebugMessage("User selected: None")

    printMainMessage("Would you like to enable Roblox Unfriend Checks? (y/n)")
    printYellowMessage("Warning! This may take way too long time due to Roblox ratelimits.")
    d = handleBasicSetting("EFlagRobloxUnfriendCheckEnabled", False)
    if d: return d

    printMainMessage("Would you like to enable Roblox Security Cookie Usage? (y/n)")
    printYellowMessage("This is used for authentication with Roblox APIs such as Beta Programs.")
    printYellowMessage("Warning! This option will look for cookies automatically in your Roblox Data and may bring security issues.")
    d = handleBasicSetting("EFlagRobloxSecurityCookieUsage", False)
    if d: return d

    printMainMessage("Would you like to enable URL Quick Launch? (y/n)")
    printYellowMessage("This will allow you to launch Roblox with a specific URL.")
    printYellowMessage("Using this option, OrangeBlox will automatically launch Roblox when you attempt to open Roblox from your web browser and try to be as fast as possible to open. \nIn the process, you may see the Roblox window open; just leave it open.")
    d = handleBasicSetting("EFlagEnableURLQuickLaunch", False)
    if d: return d

    if cf.main_config.get("EFlagRobloxUnfriendCheckEnabled") == True:
        def req_int():
            printMainMessage("Please enter your Roblox User ID to detect for unfriends!")
            printMainMessage("If you don't want to enter a specific User ID, enter nothing to detect the current logged in user.")
            re_in = input("> ")
            if safeConvertNumber(re_in):
                return re_in
            elif re_in == "":
                glob_settings = cf.handler.getRobloxAppSettings()
                if glob_settings.get("loggedInUser") and glob_settings.get("loggedInUser").get("id"):
                    return int(glob_settings.get("loggedInUser").get("id"))
                else:
                    return req_int()
            else:
                return req_int()
        if cf.main_config.get("EFlagRobloxUnfriendCheckUserID"):
            printMainMessage("Would you like to change your Roblox User ID for Unfriend Checks? (y/n)")
            printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagRobloxUnfriendCheckUserID"))}')
            d = input("> ")
            if isYes(d) == True:
                cf.main_config["EFlagRobloxUnfriendCheckUserID"] = req_int()
                printDebugMessage("User selected: True")
            elif isRequestClose(d) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
        else: cf.main_config["EFlagRobloxUnfriendCheckUserID"] = req_int()

    if cf.main_os == "Darwin":
        printMainMessage("Would you like to enable Quick Modification mode? (y/n)")
        printMainMessage("Quick Modification mode is an option to move the preparation process and Mod Script scripts to the background when you load from the webbrowser or when Roblox is currently active.")
        printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagEnableSkipModificationMode")==True)}')
        printYellowMessage("This may allow you to load Roblox faster but may still cause issues.")
        printYellowMessage("This will only apply to Roblox Player and not Roblox Studio.")
        d = input("> ")
        if isYes(d) == True:
            cf.main_config["EFlagEnableSkipModificationMode"] = True
            printDebugMessage("User selected: True")
        elif isRequestClose(d) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
        elif isNo(d) == True:
            cf.main_config["EFlagEnableSkipModificationMode"] = False
            printDebugMessage("User selected: False")
        
        printMainMessage("Would you like to disable allowing Roblox to reopen after macOS sleep/restart? (y/n)")
        printYellowMessage("This will only apply to Roblox Player.")
        d = handleBasicSetting("EFlagDisableRobloxReopenAfterRestart", False)
        if d: return d

    printMainMessage("Would you like to disable Roblox Reinstall checks? (y/n)")
    printMainMessage("This may ignore when a Roblox reinstall is needed due to signing.")
    d = handleBasicSetting("EFlagDisableRobloxReinstallNeededChecks", False)
    if d: return d
    
    if cf.main_config.get("EFlagRobloxStudioEnabled") == True:
        printMainMessage("Would you like to enable limiting Localized Studio Documentations to English (United States)? (Select your Roblox language to English (US) for this) (y/n)")
        printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagLimitAPIDocsLocalization")=="en-us")}')
        d = input("> ")
        if isYes(d) == True:
            cf.main_config["EFlagLimitAPIDocsLocalization"] = "en-us"
            printDebugMessage(f'User selected: {cf.main_config.get("EFlagLimitAPIDocsLocalization")}')
        elif isRequestClose(d) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
        elif isNo(d) == True:
            cf.main_config["EFlagLimitAPIDocsLocalization"] = None
            printDebugMessage("User selected: None")
        printMainMessage("Would you like to enable deleting localized Studio fonts? (y/n)")
        d = handleBasicSetting("EFlagOverwriteUnneededStudioFonts", False)
        if d: return d
def globalSettings():
    printSystemMessage("--- Global Setting Modifications ---")
    printMainMessage("Welcome to the Roblox Global Settings menu! Select a setting to modify.")
    printYellowMessage("WARNING! There may be issues when setting this and values set may get reset by the client.")
    basic_settings = cf.handler.getRobloxGlobalBasicSettings(studio=cf.current_global_setting_type)
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
            "message": ts(f"Switch to {'Studio' if cf.current_global_setting_type == False else 'Player'}"),
            "data": 69420
        })
        basic_selected_data = generateMenuSelection(generated_basic_ui_options, star_option=ts("Exit Global Settings Menu"))
        if basic_selected_data:
            if basic_selected_data.get("data") == 69420:
                cf.current_global_setting_type = not cf.current_global_setting_type
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
                    cf.submit_status.start()
                    cf.handler.installGlobalBasicSettings(global_settings, debug=cf.main_config.get("EFlagEnableDebugMode")==True, studio=cf.current_global_setting_type, endRobloxInstances=False)
                    cf.submit_status.end()
                    globalSettings()
                except:
                    printDebugMessage("Unable to format to a suitable value due to an error.")
                    globalSettings()
        else:
            printMainMessage("Exiting Global Settings Menu..")
            return
    else: printErrorMessage(f"Unable to load current global settings.")
def activityTracking():
    printSystemMessage("--- Activity Tracking ---")
    printMainMessage("Would you like to allow Activity Tracking on the Roblox client? (y/n)")
    printMainMessage("This will allow features like:")
    printMainMessage("- Server Locations")
    printMainMessage("- Multiple Instances")
    printMainMessage("- Discord Presence (+ BloxstrapRPC support)")
    printMainMessage("- Discord Webhooks")
    printMainMessage("- Mod Scripts")
    d = handleBasicSetting("EFlagAllowActivityTracking", True)
    if d: return d

    if cf.main_config.get("EFlagAllowActivityTracking") != False:
        printMainMessage("Would you like to enable Server Locations? (y/n)")
        d = handleBasicSetting("EFlagNotifyServerLocation", False)
        if d: return d

        printMainMessage("Would you like to enable Server Uptime inside Server Location Notifications? (y/n)")
        printYellowMessage("This option uses the RoValra API to get server uptime information.")
        printYellowMessage("Though this option may be inaccurate, it may still give a base.")
        d = handleBasicSetting("EFlagEnableRoValraServerUptime", False)
        if d: return d

        printMainMessage("Would you like to enable Discord RPC? (y/n)")
        d = handleBasicSetting("EFlagEnableDiscordRPC", False)
        if d: return d

        if cf.main_config.get("EFlagRobloxStudioEnabled") == True:
            printMainMessage("Would you like to enable Discord RPC for Roblox Studio? (y/n)")
            d = handleBasicSetting("EFlagEnableDiscordRPCStudio", False)
            if d: return d

        if cf.main_config.get("EFlagEnableDiscordRPC") == True or cf.main_config.get("EFlagEnableDiscordRPCStudio") == True:
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
            printYellowMessage("This option requires pypresence v4.6.0+ to be installed")
            d = handleBasicSetting("EFlagShowGameNameInStatusBar", False)
            if d: return d

            printMainMessage("Would you like to enable showing Editing Studio Game Name in Status Bar? (y/n)")
            printYellowMessage("This option requires pypresence v4.6.0+ to be installed")
            d = handleBasicSetting("EFlagShowStudioGameNameInStatusBar", False)
            if d: return d

            if cf.main_config.get("EFlagRobloxStudioEnabled") == True:
                printMainMessage("Would you like to enable Roblox Studio to use the Bloxstrap SDK? (y/n)")
                d = handleBasicSetting("EFlagAllowBloxstrapStudioSDK", False)
                if d: return d

            printMainMessage("Would you like to enable access to private servers you connect to from Discord Presences? (users may be able to join or not) (y/n)")
            d = handleBasicSetting("EFlagAllowPrivateServerJoining", False)
            if d: return d

        printMainMessage("Would you like to use a Discord Webhook? (link required) (y/n)")
        printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagUseDiscordWebhook", False)==True)}')
        d = input("> ")
        if isYes(d) == True:
            cf.main_config["EFlagUseDiscordWebhook"] = True
            printDebugMessage("User selected: True")
            printMainMessage("Please enter your Discord Webhook Link here (https://discord.com/api/webhooks/XXXXXXX/XXXXXXX): ")
            d = input("> ")
            if d.startswith("https://discord.com/api/webhooks/"):
                printDebugMessage("URL passed test.")
                cf.main_config["EFlagDiscordWebhookURL"] = d
        elif isRequestClose(d) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
        elif isNo(d) == True:
            cf.main_config["EFlagUseDiscordWebhook"] = False
            printDebugMessage("User selected: False")
        if cf.main_config.get("EFlagUseDiscordWebhook") == True:
            if cf.main_config.get("EFlagDiscordWebhookURL", "").startswith("https://discord.com/api/webhooks/"):
                printMainMessage("Enter your Discord User ID to ping you when a new notification is made (you will need Discord Developer Mode enabled in order to copy):")
                printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagDiscordWebhookUserId"))}')
                d = input("> ")
                if safeConvertNumber(d): cf.main_config["EFlagDiscordWebhookUserId"] = d
                if safeConvertNumber(cf.main_config.get("EFlagDiscordWebhookUserId", "")):
                    max_setti = 6
                    co = 1
                    if cf.main_config.get("EFlagRobloxStudioEnabled") == True: max_setti += 2
                    printMainMessage("What should this Discord Webhook send?")
                    printMainMessage(f"[{co}/{max_setti}] Roblox Connecting Information (y/n)")
                    printMainMessage("When you join a Roblox game (or edit a Roblox Studio game), your webhook gets pinged with information such as Server Location and Joining Link.")
                    printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagDiscordWebhookConnect")==True)}')
                    d = input("> ")
                    if isYes(d) == True:
                        cf.main_config["EFlagDiscordWebhookConnect"] = True
                        printDebugMessage("User selected: True")
                    elif isNo(d) == True:
                        cf.main_config["EFlagDiscordWebhookConnect"] = False
                        printDebugMessage("User selected: False")
                    co += 1
                    printMainMessage(f"[{co}/{max_setti}] Roblox Disconnecting Information (y/n)")
                    printMainMessage("When you leave a Roblox game (or leave a Roblox Studio session), your webhook gets pinged with information such as Server Location and Joining Link.")
                    printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagDiscordWebhookDisconnect")==True)}')
                    d = input("> ")
                    if isYes(d) == True:
                        cf.main_config["EFlagDiscordWebhookDisconnect"] = True
                        printDebugMessage("User selected: True")
                    elif isNo(d) == True:
                        cf.main_config["EFlagDiscordWebhookDisconnect"] = False
                        printDebugMessage("User selected: False")
                    co += 1
                    printMainMessage(f"[{co}/{max_setti}] Roblox Opening Information (y/n)")
                    printMainMessage("When you open Roblox (or Roblox Studio), your webhook gets pinged with information such as Process ID and Log File Location.")
                    printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagDiscordWebhookRobloxAppStart")==True)}')
                    d = input("> ")
                    if isYes(d) == True:
                        cf.main_config["EFlagDiscordWebhookRobloxAppStart"] = True
                        printDebugMessage("User selected: True")
                    elif isNo(d) == True:
                        cf.main_config["EFlagDiscordWebhookRobloxAppStart"] = False
                        printDebugMessage("User selected: False")
                    co += 1
                    printMainMessage(f"[{co}/{max_setti}] Roblox Closing Information (y/n)")
                    printMainMessage("When you close Roblox (or Roblox Studio), your webhook gets pinged with information such as Process ID and Log File Location.")
                    printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagDiscordWebhookRobloxAppClose")==True)}')
                    d = input("> ")
                    if isYes(d) == True:
                        cf.main_config["EFlagDiscordWebhookRobloxAppClose"] = True
                        printDebugMessage("User selected: True")
                    elif isNo(d) == True:
                        cf.main_config["EFlagDiscordWebhookRobloxAppClose"] = False
                        printDebugMessage("User selected: False")
                    co += 1
                    printMainMessage(f"[{co}/{max_setti}] Roblox Crashing Information (y/n)")
                    printMainMessage("When Roblox (or Roblox Studio) crashes, your webhook gets pinged with the console log that shows the cause of the crash.")
                    printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagDiscordWebhookRobloxCrash")==True)}')
                    d = input("> ")
                    if isYes(d) == True:
                        cf.main_config["EFlagDiscordWebhookRobloxCrash"] = True
                        printDebugMessage("User selected: True")
                    elif isNo(d) == True:
                        cf.main_config["EFlagDiscordWebhookRobloxCrash"] = False
                        printDebugMessage("User selected: False")
                    co += 1
                    printMainMessage(f"[{co}/{max_setti}] BloxstrapRPC Information (y/n)")
                    printMainMessage("When BloxstrapRPC is triggered (if enabled), your webhook gets pinged with the changes given from the launched game.")
                    printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagDiscordWebhookBloxstrapRPC")==True)}')
                    d = input("> ")
                    if isYes(d) == True:
                        cf.main_config["EFlagDiscordWebhookBloxstrapRPC"] = True
                        printDebugMessage("User selected: True")
                    elif isNo(d) == True:
                        cf.main_config["EFlagDiscordWebhookBloxstrapRPC"] = False
                        printDebugMessage("User selected: False")
                    if cf.main_config.get("EFlagRobloxStudioEnabled") == True:
                        co += 1
                        printMainMessage(f"[{co}/{max_setti}] Publishing Game Information (y/n)")
                        printMainMessage("When you publish a game from Roblox Studio, your webhook gets pinged with game information such as Server Location and Editing Link.")
                        printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagDiscordWebhookGamePublished")==True)}')
                        d = input("> ")
                        if isYes(d) == True:
                            cf.main_config["EFlagDiscordWebhookGamePublished"] = True
                            printDebugMessage("User selected: True")
                        elif isNo(d) == True:
                            cf.main_config["EFlagDiscordWebhookGamePublished"] = False
                            printDebugMessage("User selected: False")
                        co += 1
                        printMainMessage(f"[{co}/{max_setti}] Saving Game Information (y/n)")
                        printMainMessage("When you save a game from Roblox Studio, your webhook gets pinged with game information such as Server Location and Editing Link.")
                        printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagDiscordWebhookGameSaved")==True)}')
                        d = input("> ")
                        if isYes(d) == True:
                            cf.main_config["EFlagDiscordWebhookGameSaved"] = True
                            printDebugMessage("User selected: True")
                        elif isNo(d) == True:
                            cf.main_config["EFlagDiscordWebhookGameSaved"] = False
                            printDebugMessage("User selected: False")
                    printMainMessage("Would you like it to show the pid number in the webhook footer? (y/n)")
                    printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagDiscordWebhookShowPidInFooter")==True)}')
                    d = input("> ")
                    if isYes(d) == True:
                        cf.main_config["EFlagDiscordWebhookShowPidInFooter"] = True
                        printDebugMessage("User selected: True")
                    elif isNo(d) == True:
                        cf.main_config["EFlagDiscordWebhookShowPidInFooter"] = False
                        printDebugMessage("User selected: False")
            else:
                cf.main_config["EFlagUseDiscordWebhook"] = False
                printErrorMessage("The provided webhook link is not a valid format.")

        if cf.main_config.get("EFlagRobloxStudioEnabled") == True:
            printMainMessage("Would you like to enable force reconnection when you disconnect from a Studio server? (y/n)")
            d = handleBasicSetting("EFlagForceReconnectOnStudioLost", False)
            if d: return d

        if cf.main_os == "Windows":
            printMainMessage("Would you like to enable showing the Account Name in the Roblox title window? (y/n)")
            d = handleBasicSetting("EFlagShowRunningAccountNameInTitle", False)
            if d: return d
            if cf.main_config.get("EFlagShowRunningAccountNameInTitle") != True:
                printMainMessage("Would you like to enable showing the Game Name in the Roblox title window instead? (y/n)")
                d = handleBasicSetting("EFlagShowRunningGameInTitle", False)
                if d: return d
            else:
                printMainMessage("Would you like to like to include the Display Name as apart of the title? (y/n)")
                d = handleBasicSetting("EFlagShowDisplayNameInTitle", False)
                if d: return d
def bootstrapSettings():
    printSystemMessage("--- Bootstrap Settings ---")
    if os.path.exists(os.path.join(cf.cur_path, "Translations")):
        printMainMessage("Select your bootstrap language:")
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
    current_rebuilder = None
    if cf.main_config.get("EFlagRebuildPyinstallerAppFromSourceDuringUpdates")==True: current_rebuilder = "Pyinstaller"
    elif cf.main_config.get("EFlagRebuildNuitkaAppFromSourceDuringUpdates")==True: current_rebuilder = "Nuitka"
    printMainMessage(f"Would you like to enable rebuilding the {obName0()} main loader? If so, what builder should it use? (y/n)")
    printMainMessage("[1] = Pyinstaller")
    printMainMessage("[2] = Nuitka [CAN TAKE A WHILE]")
    printMainMessage("[n] = None")
    printMainMessage(f'Current Setting: {current_rebuilder}')
    printYellowMessage("In order to use Pyinstaller, the module is needed to be installed.")
    printYellowMessage("In order to use Nuitka, the module and a C compiler is needed to be installed.")
    if cf.main_os == "Darwin": printYellowMessage("For macOS users, it is suggested to install Xcode Command Line Tools from the official Apple website."); printYellowMessage("https://developer.apple.com/xcode/resources/")
    elif cf.main_os == "Windows": printYellowMessage("For Windows, it is required to use Microsoft Visual Code 2022 compilation for using Nuitka."); printYellowMessage("https://nuitka.net/user-documentation/user-manual.html")
    a = input("> ")
    if a == "1":
        cf.main_config["EFlagRebuildPyinstallerAppFromSourceDuringUpdates"] = True
        cf.main_config["EFlagRebuildNuitkaAppFromSourceDuringUpdates"] = False
    elif a == "2":
        cf.main_config["EFlagRebuildPyinstallerAppFromSourceDuringUpdates"] = False
        cf.main_config["EFlagRebuildNuitkaAppFromSourceDuringUpdates"] = True
    elif isRequestClose(a) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
    elif isNo(a) == True:
        cf.main_config["EFlagRebuildPyinstallerAppFromSourceDuringUpdates"] = False
        cf.main_config["EFlagRebuildNuitkaAppFromSourceDuringUpdates"] = False
        printDebugMessage("User selected: False")

    printMainMessage("Would you like to enable installing the latest version of EfazDev ECC Security CA? (y/n)")
    printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagInstallEfazDevECCCertificates")==True)}')
    printYellowMessage("This is apart of code-signing and may affect security.")
    a = input("> ")
    if isYes(a) == True:
        cf.main_config["EFlagInstallEfazDevECCCertificates"] = True
        printDebugMessage("User selected: True")
    elif isRequestClose(a) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
    elif isNo(a) == True:
        cf.main_config["EFlagInstallEfazDevECCCertificates"] = False
        printDebugMessage("User selected: False")

    printMainMessage("Would you like to change your Sync Folder? (y/n)")
    printMainMessage(f'Current Setting: {cf.main_config.get("EFlagOrangeBloxSyncDir") if checkSyncFolder() else None}')
    printYellowMessage("If you want to create a new sync folder, please use the OrangeBlox Installer option and choose to create installer.")
    printYellowMessage("If you want to use an existing sync folder, use this.")
    a = input("> ")
    if isYes(a) == True:
        custom_path = cf.file_selector.select_folder("Select the sync directory!", initialdir=cf.cur_path)
        if custom_path and custom_path.ok and checkSyncFolder(custom_path.path): 
            cf.main_config["EFlagOrangeBloxSyncDir"] = custom_path.path
            printDebugMessage(f"User selected: {custom_path.path}")
        else: printErrorMessage("The selected folder is not a valid sync folder. Please make sure the folder contains the necessary files and try again.")
    elif isRequestClose(a) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
    elif isNo(a) == True:
        cf.main_config["EFlagOrangeBloxSyncDir"] = None
        printDebugMessage("User selected: None")

    if cf.main_os == "Darwin":
        printMainMessage("Would you like to rebuild OrangeLoader, Play Roblox, and Run Studio app based on source code? (y/n)")
        printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagRebuildClangAppFromSourceDuringUpdates")==True)}')
        printYellowMessage("Clang++ is required to be installed on your Mac in order to use.")
        a = input("> ")
        if isYes(a) == True:
            cf.main_config["EFlagRebuildClangAppFromSourceDuringUpdates"] = True
            printDebugMessage("User selected: True")
        elif isRequestClose(a) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
        elif isNo(a) == True:
            cf.main_config["EFlagRebuildClangAppFromSourceDuringUpdates"] = False
            printDebugMessage("User selected: False")

    printMainMessage("Would you like to enable See More Awaiting on List Selections? (y/n)")
    d = handleBasicSetting("EFlagEnableSeeMoreAwaiting", False)
    if d: return d

    printMainMessage("Would you like to enable 429 Loops when the Roblox server gives a 429 (Too much request) response? (y/n)")
    d = handleBasicSetting("EFlagEnableLoop429Requests", False)
    if d: return d

    printMainMessage("Would you like to enable showing CPU Percentage and Memory Usage? (y/n)")
    d = handleBasicSetting("EFlagEnableCPUMemoryUsageViewer", True)
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

    if cf.main_config.get("EFlagDisablePythonUpdateChecks", False) == False:
        printMainMessage("Would you like to enable slient Python installs instead of a prompt for python updates? (y/n)")
        if cf.main_os == "Darwin": printYellowMessage("For macOS users, admin permission is needed in order to install.")
        d = handleBasicSetting("EFlagEnableSlientPythonInstalls", False)
        if d: return d

    printMainMessage(f"Would you like to customize OrangeBlox bootstrap theme? (y/n)")
    printMainMessage(f'Current Setting: {cf.main_config.get("EFlagCustomBootstrapName", "OrangeBlox")}')
    d = input("> ")
    if isYes(d) == True:
        try:
            printMainMessage("Please enter the custom name for OrangeBlox (OrangeBlox will reset to default):")
            printMainMessage(f'Current Name: {cf.main_config.get("EFlagCustomBootstrapName", "OrangeBlox")}')
            k = input("> ")
            if k == "OrangeBlox": raise Exception("reset_theme")
            if k: cf.main_config["EFlagCustomBootstrapName"] = k
            if len(cf.main_config["EFlagCustomBootstrapName"].strip()) < 2: raise Exception(ts("Name is too short."))
            printMainMessage(f"Please enter the emoji for {cf.main_config['EFlagCustomBootstrapName']}:")
            printMainMessage(f'Current Emoji: {cf.main_config.get("EFlagCustomBootstrapEmoji", "🍊")}')
            k = input("> ")
            if k: cf.main_config["EFlagCustomBootstrapEmoji"] = k
            if len(cf.main_config["EFlagCustomBootstrapEmoji"].strip()) != 1: raise Exception(ts("Invalid Emoji format."))
            printMainMessage(f"Please enter the HEX color for {cf.main_config['EFlagCustomBootstrapName']}:")
            printMainMessage("For selecting your color, use this Google link and use the Hex value.")
            printMainMessage("https://www.google.com/search?q=color+picker")
            printMainMessage(f'Current Color: {cf.main_config.get("EFlagCustomBootstrapColor", "#ff4b00")}')
            k = input("> ")
            if k: cf.main_config["EFlagCustomBootstrapColor"] = k
            import re as regex
            if not bool(regex.fullmatch(r'#(?:[0-9a-fA-F]{3}){1,2}$', cf.main_config["EFlagCustomBootstrapColor"].strip())): raise Exception(ts("Invalid HEX color format."))
            cf.colors_class.hex_to_rgb(cf.main_config["EFlagCustomBootstrapColor"])
            printMainMessage(f"Please enter the internet url of the image file:")
            printYellowMessage("This will be used for places on the internet such as Discord Webhooks. However, the file must be a direct downloadable image link, not a webpage.")
            printMainMessage(f'Current URL: {cf.main_config.get("EFlagCustomBootstrapInternetURL", f"{cf.main_host}/Images/AppIcon.png")}')
            k = input("> ")
            if k: cf.main_config["EFlagCustomBootstrapInternetURL"] = k
            if not cf.main_config["EFlagCustomBootstrapInternetURL"].startswith("https") and not cf.main_config["EFlagCustomBootstrapInternetURL"].startswith("ftp"): raise Exception(ts("The internet URL should be https or ftp."))
            printMainMessage("Would you like to use a local image file or would you like to download this file?")
            printMainMessage(f'Current Image: {cf.main_config.get("EFlagCustomBootstrapIconPath", os.path.join(cf.cur_path, "Images", "AppIcon.png"))}')
            printMainMessage("[1] = Local File")
            printMainMessage("[*] = Download File")
            d = input("> ")
            if d == "1":
                printMainMessage(f"Please enter the path (or the image file you want to use):")
                printYellowMessage("Please note that it will have to be a working file in order to be used!")
                k = input("> ")
                if k: cf.main_config["EFlagCustomBootstrapIconPath"] = k
                if not os.path.exists(cf.main_config["EFlagCustomBootstrapIconPath"]): raise Exception(ts("Unable to find local image file."))
            else:
                printMainMessage("Downloading image file..")
                path_to_download = generateFileKey("AppIcon", ext=".png")
                img_download_res = cf.requests.download(cf.main_config["EFlagCustomBootstrapInternetURL"], path_to_download)
                if img_download_res.ok:
                    cf.main_config["EFlagCustomBootstrapIconPath"] = path_to_download
                    printMainMessage("Successfully downloaded image file!")
                else:
                    printErrorMessage("Unable to download image file from the internet URL provided.")
                    printMainMessage(f"Please enter the path (or the image file you want to use):")
                    printYellowMessage("Please note that it will have to be a working file in order to be used!")
                    k = input("> ")
                    if k: cf.main_config["EFlagCustomBootstrapIconPath"] = k
                    if not os.path.exists(cf.main_config["EFlagCustomBootstrapIconPath"]): raise Exception(ts("Unable to find local image file."))
            printDebugMessage("User selected: Custom")
            printSuccessMessage(f"Successfully set the theme of OrangeBlox to {cf.main_config['EFlagCustomBootstrapName']}!")
            if cf.main_os == "Darwin":
                printYellowMessage("Colors that are outside OrangeBlox such as the terminal may be needed to changed manually.")
                printYellowMessage("This can be done by modifying the OrangeBlox terminal profile.")
                printYellowMessage("Also, for local files, there may be popups to allow access to the folder those files are in. Allow those popups for the Terminal and OrangeBlox app.")
        except Exception as e:
            if str(e) != "reset_theme": printErrorMessage(f"An error occurred while setting customizations: {str(e)}")
            cf.main_config["EFlagCustomBootstrapName"] = "OrangeBlox"
            cf.main_config["EFlagCustomBootstrapEmoji"] = "🍊"
            cf.main_config["EFlagCustomBootstrapColor"] = "#ff4b00"
            cf.main_config["EFlagCustomBootstrapInternetURL"] = f"{cf.main_host}/Images/AppIcon.png"
            cf.main_config["EFlagCustomBootstrapIconPath"] = os.path.join(cf.cur_path, "Images", "AppIcon.png")
            printDebugMessage("User selected: Default")
    elif isRequestClose(d) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
    elif isNo(d) == True:
        cf.main_config["EFlagCustomBootstrapName"] = "OrangeBlox"
        cf.main_config["EFlagCustomBootstrapEmoji"] = "🍊"
        cf.main_config["EFlagCustomBootstrapColor"] = "#ff4b00"
        cf.main_config["EFlagCustomBootstrapInternetURL"] = f"{cf.main_host}/Images/AppIcon.png"
        cf.main_config["EFlagCustomBootstrapIconPath"] = os.path.join(cf.cur_path, "Images", "AppIcon.png")
        printDebugMessage("User selected: Default")

    printMainMessage(f"Would you like to enable {obName0()} Beta? (y/n)")
    printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagBootstrapUpdateServer")=="https://raw.githubusercontent.com/EfazDev/orangeblox/refs/heads/beta/Version.json" or cf.main_config.get("EFlagBootstrapUpdateServer")=="https://obxbeta.efaz.dev/Version.json")}')
    printYellowMessage("Betas could contain bugs that could break your Roblox installation!")
    d = input("> ")
    if isYes(d) == True:
        cf.main_config["EFlagBootstrapUpdateServer"] = "https://obxbeta.efaz.dev/Version.json"
        printDebugMessage("User selected: True")
    elif isRequestClose(d) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
    elif isNo(d) == True:
        cf.main_config["EFlagBootstrapUpdateServer"] = "https://obx.efaz.dev/Version.json"
        printDebugMessage("User selected: False")

    printMainMessage(f"Would you like to disable automatically saving your {obName0()} Configuration to your installation folder? (y/n)")
    d = handleBasicSetting("EFlagDisableAutosaveToInstallation", False)
    if d: return d

    if cf.main_os == "Windows":
        printMainMessage("Would you like to disable Bootstrap Cooldowns? (y/n)")
        printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagDisableBootstrapCooldown")==True)}')
        printYellowMessage("If your computer is laggy, this may prevent multiple windows opening.")
        d = input("> ")
        if isYes(d) == True:
            cf.main_config["EFlagDisableBootstrapCooldown"] = True
            printDebugMessage("User selected: True")
        elif isRequestClose(d) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
        elif isNo(d) == True:
            cf.main_config["EFlagDisableBootstrapCooldown"] = False
            printDebugMessage("User selected: False")

    printMainMessage(f"Would you like to use Python Virtual Environments for {obName0()}? (y/n)")
    d = handleBasicSetting("EFlagEnablePythonVirtualEnvironments", False)
    if d: return d

    printMainMessage("Would you like to build Python cache on app start? (y/n)")
    d = handleBasicSetting("EFlagBuildPythonCacheOnStart", False)
    if d: return d
        
    if cf.main_os == "Windows":
        printMainMessage(f"Would you like to make shortcuts for {obName0()}? [Needed for launching through the Windows Start Menu and Desktop] (y/n)")
        d = handleBasicSetting("EFlagDisableShortcutsInstall", False, False)
        if d: return d
    elif cf.main_os == "Darwin":
        printMainMessage("Would you like to enable Dock Bar and System Tray options when right clicking the app icon? (y/n)")
        d = handleBasicSetting("EFlagEnableGUIOptionMenus", True)
        if d: return d
def debugging():
    printSystemMessage("--- Debugging ---")
    printMainMessage("Would you like to enable Debug Mode? (y/n)")
    printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagEnableDebugMode")==True)}')
    printYellowMessage("[WARNING! This will expose information like login to Roblox.]")
    printYellowMessage("[DO NOT EVER ENABLE IF SOMEONE TOLD YOU SO OR YOU USUALLY RECORD!!]")
    d = input("> ")
    if isYes(d) == True:
        cf.main_config["EFlagEnableDebugMode"] = True
        printDebugMessage("User selected: True")
    elif isRequestClose(d) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
    elif isNo(d) == True:
        cf.main_config["EFlagEnableDebugMode"] = False
        printDebugMessage("User selected: False")
    cf.pip_class.debug = cf.main_config.get("EFlagEnableDebugMode") == True

    if cf.main_config.get("EFlagEnableDebugMode") == True:
        printMainMessage("Would you like to print unhandled Roblox client events? (y/n)")
        d = handleBasicSetting("EFlagAllowFullDebugMode", False)
        if d: return d

    printMainMessage("Would you like to enable saving Bootstrap logs? (y/n)")
    d = handleBasicSetting("EFlagMakeMainBootstrapLogFiles", False)
    if d: return d

    printMainMessage("Would you like to set a Roblox client channel? (y/n)")
    printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagRobloxClientChannel", "LIVE"))}')
    printYellowMessage("This will be used to determine the latest Roblox version.")
    d = input("> ")
    if isYes(d) == True:
        def t():
            printMainMessage("Please enter the channel in the input selection below! You may also use the link below to determine the channel for your account!")
            printMainMessage(f"https://clientsettings.roblox.com/v2/user-channel?binaryType={'MacPlayer' if cf.main_os == 'Darwin' else 'WindowsPlayer'}")
            printMainMessage('Additionally, you may enter "A" to automatically determine or "D" to disable Roblox update checks.')
            channel_inp = input("> ")
            if channel_inp == "A":
                cf.main_config["EFlagRobloxClientChannel"] = None
                cf.main_config["EFlagDisableRobloxUpdateChecks"] = False
                printSuccessMessage("Successfully set Roblox client channel to automatically determine!")
            elif channel_inp == "D":
                cf.main_config["EFlagRobloxClientChannel"] = "LIVE"
                cf.main_config["EFlagDisableRobloxUpdateChecks"] = True
                printSuccessMessage(f"Successfully disabled Roblox Update Checks for launching from {obName0()}. Roblox may still check for updates though.")
            else:
                try:
                    a = cf.handler.getLatestClientVersion(studio=False, debug=cf.main_config.get("EFlagEnableDebugMode"), channel=channel_inp, token=createDownloadToken(False))
                    if a.get("success") == True and a.get("attempted_channel") == channel_inp:
                        cf.main_config["EFlagRobloxClientChannel"] = channel_inp
                        cf.main_config["EFlagDisableRobloxUpdateChecks"] = False
                        printSuccessMessage("Successfully set Roblox client channel!")
                    else:
                        printErrorMessage("Channel may not exist. Please try again or use LIVE!")
                        t()
                except Exception:
                    printErrorMessage("Something went wrong. Please try again or use LIVE!")
                    t()
        t()
    elif isRequestClose(d) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
    elif isNo(d) == True:
        cf.main_config["EFlagRobloxClientChannel"] = "LIVE"
        cf.main_config["EFlagDisableRobloxUpdateChecks"] = False
        printDebugMessage("User selected: False")

    if cf.main_config.get("EFlagRobloxStudioEnabled") == True:
        printMainMessage("Would you like to set a Roblox Studio client channel? (y/n)")
        printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagRobloxStudioClientChannel", "LIVE"))}')
        printYellowMessage("This will be used to determine the latest Roblox Studio version.")
        d = input("> ")
        if isYes(d) == True:
            def t():
                printMainMessage("Please enter the channel in the input selection below! You may also use the link below to determine the channel for your account!")
                printMainMessage(f"https://clientsettings.roblox.com/v2/user-channel?binaryType={'MacStudio' if cf.main_os == 'Darwin' else 'WindowsStudio'}")
                printMainMessage('Additionally, you may enter "A" to automatically determine or "D" to disable Roblox Studio update checks.')
                channel_inp = input("> ")
                if channel_inp == "A":
                    cf.main_config["EFlagRobloxStudioClientChannel"] = None
                    cf.main_config["EFlagDisableRobloxUpdateChecks"] = False
                    printSuccessMessage("Successfully set Roblox Studio client channel to automatically determine!")
                elif channel_inp == "D":
                    cf.main_config["EFlagRobloxStudioClientChannel"] = "LIVE"
                    cf.main_config["EFlagDisableRobloxUpdateChecks"] = True
                    printSuccessMessage(f"Successfully disabled Roblox Studio Update Checks for launching from {obName0()}. Roblox may still check for updates though.")
                else:
                    try:
                        a = cf.handler.getLatestClientVersion(studio=True, debug=cf.main_config.get("EFlagEnableDebugMode"), channel=channel_inp, token=createDownloadToken(True))
                        if a.get("success") == True and a.get("attempted_channel") == channel_inp:
                            cf.main_config["EFlagRobloxStudioClientChannel"] = channel_inp
                            cf.main_config["EFlagDisableRobloxUpdateChecks"] = False
                            printSuccessMessage("Successfully set Roblox Studio client channel!")
                        else:
                            printErrorMessage("Channel may not exist. Please try again or use LIVE!")
                            t()
                    except Exception:
                        printErrorMessage("Something went wrong. Please try again or use LIVE!")
                        t()
            t()
        elif isRequestClose(d) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
        elif isNo(d) == True:
            cf.main_config["EFlagRobloxStudioClientChannel"] = "LIVE"
            cf.main_config["EFlagDisableRobloxUpdateChecks"] = False
            printDebugMessage("User selected: False")

    printMainMessage("Would you like to enable Hash Verification on Roblox Player and Studio after updates? (y/n)")
    printMainMessage(f'Current Setting: {cf.main_config.get("EFlagVerifyRobloxHashAfterInstall")!=False}')
    printYellowMessage("This is a security measure that be used to validate Roblox in case of insecure downloads.")
    d = input("> ")
    if isYes(d) == True:
        cf.main_config["EFlagVerifyRobloxHashAfterInstall"] = True
        printDebugMessage("User selected: True")
    elif isRequestClose(d) == True: printMainMessage("Closing settings.."); return ts("Settings was closed.")
    elif isNo(d) == True:
        cf.main_config["EFlagVerifyRobloxHashAfterInstall"] = False
        printDebugMessage("User selected: False")
def mainSettings():
    generated_ui_options = []
    printSystemMessage("--- Settings ---")
    generated_ui_options.append({
        "index": 1, 
        "message": ts("Roblox Modifications & Settings"), 
        "func": robloxSettings,
        "clear_console": True
    })
    generated_ui_options.append({
        "index": 1.5, 
        "message": ts("Roblox Fast Flag Configurations"), 
        "func": continueToRobloxManager,
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
        "message": ts(f"{obName0()} Installer Options"), 
        "func": continueToOrangeBloxInstaller, 
        "go_to_rbx": True,  
        "end_mes": ts(f"{obName0()} has been modified!"),
        "clear_console": True
    })
    generated_ui_options.append({
        "index": 10, 
        "message": ts("Debugging"), 
        "func": debugging,
        "clear_console": True
    })
    if checkSyncFolder():
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
            printSystemMessage(f"{re} Would you like to return to settings or exit it?")
            printMainMessage("[1] Return to Settings")
            printMainMessage("[*] Exit Settings")
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
def continueToSettings(): # Open Settings
    if cf.main_config.get("EFlagDisableSettingsAccess") == True:
        printSystemMessage("--- Settings ---")
        printErrorMessage("Access to editing Settings was disabled by file. Please try again later!")
        input("> ")
        return ts("Settings was not saved!")
    return mainSettings()

if __name__ == "__main__":
    print("This module is not a runable instance.")
    sys.exit(1)