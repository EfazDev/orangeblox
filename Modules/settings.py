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
    def set_studio_enabled():
        printMainMessage(f"Would you like to enable using Roblox Studio with {obName0()}? (y/n)")
        return handleBasicSetting("EFlagRobloxStudioEnabled", False)
    def set_fresh_copy():
        printMainMessage("Would you like to reinstall a fresh copy of Roblox every launch? (y/n)")
        return handleBasicSetting("EFlagFreshCopyRoblox", False)
    def set_url_schemes():
        printMainMessage(f"Would you like to set the URL Schemes for the Roblox Client and {obName0()}? [Needed for Link Shortcuts and when Roblox updates] (y/n)")
        return handleBasicSetting("EFlagDisableURLSchemeInstall", False, False)
    def set_player_args():
        printMainMessage("Would you like to set start arguments for Roblox Player? (y/n)")
        printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagRobloxPlayerArguments"))}')
        d = input("> ")
        if isYes(d) == True:
            printMainMessage("Input the start arguments to use when running Roblox!")
            cf.main_config["EFlagRobloxPlayerArguments"] = input("> ")
            printDebugMessage(f'User selected: {cf.main_config.get("EFlagRobloxPlayerArguments")}')
        elif isRequestClose(d) == True: 
            printMainMessage("Closing settings..")
            return ts("Settings was closed.")
        elif isNo(d) == True:
            cf.main_config["EFlagRobloxPlayerArguments"] = None
            printDebugMessage("User selected: None")
    def set_studio_args():
        printMainMessage("Would you like to set start arguments for Roblox Studio? (y/n)")
        printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagRobloxStudioArguments"))}')
        d = input("> ")
        if isYes(d) == True:
            printMainMessage("Input the start arguments to use when running Roblox Studio!")
            cf.main_config["EFlagRobloxStudioArguments"] = input("> ")
            printDebugMessage(f'User selected: {cf.main_config.get("EFlagRobloxStudioArguments")}')
        elif isRequestClose(d) == True: 
            printMainMessage("Closing settings..")
            return ts("Settings was closed.")
        elif isNo(d) == True:
            cf.main_config["EFlagRobloxStudioArguments"] = None
            printDebugMessage("User selected: None")
    def set_unfriend_checks():
        printMainMessage("Would you like to enable Roblox Unfriend Checks? (y/n)")
        printYellowMessage("Warning! This may take way too long time due to Roblox ratelimits.")
        return handleBasicSetting("EFlagRobloxUnfriendCheckEnabled", False)
    def set_security_cookie():
        printMainMessage("Would you like to enable Roblox Security Cookie Usage? (y/n)")
        printYellowMessage("This is used for authentication with Roblox APIs such as Beta Programs.")
        printYellowMessage("Warning! This option will look for cookies automatically in your Roblox Data and may bring security issues.")
        return handleBasicSetting("EFlagRobloxSecurityCookieUsage", False)
    def set_url_quick_launch():
        printMainMessage("Would you like to enable URL Quick Launch? (y/n)")
        printYellowMessage("This will allow you to launch Roblox with a specific URL.")
        printYellowMessage("Using this option, OrangeBlox will automatically launch Roblox when you attempt to open Roblox from your web browser and try to be as fast as possible to open. \nIn the process, you may see the Roblox window open; just leave it open.")
        return handleBasicSetting("EFlagEnableURLQuickLaunch", False)
    def req_int():
        printMainMessage("Please enter your Roblox User ID to detect for unfriends!")
        printMainMessage("If you don't want to enter a specific User ID, enter nothing to detect the current logged in user.")
        re_in = input("> ")
        if safeConvertNumber(re_in): return re_in
        elif re_in == "":
            glob_settings = cf.handler.getRobloxAppSettings()
            if glob_settings.get("loggedInUser") and glob_settings.get("loggedInUser").get("id"): return int(glob_settings.get("loggedInUser").get("id"))
            else: return req_int()
        else: return req_int()
    def set_unfriend_user_id():
        if cf.main_config.get("EFlagRobloxUnfriendCheckUserID"):
            printMainMessage("Would you like to change your Roblox User ID for Unfriend Checks? (y/n)")
            printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagRobloxUnfriendCheckUserID"))}')
            d = input("> ")
            if isYes(d) == True:
                cf.main_config["EFlagRobloxUnfriendCheckUserID"] = req_int()
                printDebugMessage("User selected: True")
            elif isRequestClose(d) == True: 
                printMainMessage("Closing settings..")
                return ts("Settings was closed.")
        else: cf.main_config["EFlagRobloxUnfriendCheckUserID"] = req_int()
    def set_skip_mod_mode():
        printMainMessage("Would you like to enable Quick Modification mode? (y/n)")
        printMainMessage("Quick Modification mode is an option to move the preparation process and Mod Script scripts to the background when you load from the webbrowser or when Roblox is currently active.")
        printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagEnableSkipModificationMode")==True)}')
        printYellowMessage("This may allow you to load Roblox faster but may still cause issues.")
        printYellowMessage("This will only apply to Roblox Player and not Roblox Studio.")
        d = input("> ")
        if isYes(d) == True:
            cf.main_config["EFlagEnableSkipModificationMode"] = True
            printDebugMessage("User selected: True")
        elif isRequestClose(d) == True: 
            printMainMessage("Closing settings..")
            return ts("Settings was closed.")
        elif isNo(d) == True:
            cf.main_config["EFlagEnableSkipModificationMode"] = False
            printDebugMessage("User selected: False")
    def set_disable_reopen():
        printMainMessage("Would you like to disable allowing Roblox to reopen after macOS sleep/restart? (y/n)")
        printYellowMessage("This will only apply to Roblox Player.")
        return handleBasicSetting("EFlagDisableRobloxReopenAfterRestart", False)
    def set_disable_reinstall_checks():
        printMainMessage("Would you like to disable Roblox Reinstall checks? (y/n)")
        printMainMessage("This may ignore when a Roblox reinstall is needed due to signing.")
        return handleBasicSetting("EFlagDisableRobloxReinstallNeededChecks", False)
    def set_limit_api_docs():
        printMainMessage("Would you like to enable limiting Localized Studio Documentations to English (United States)? (Select your Roblox language to English (US) for this) (y/n)")
        printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagLimitAPIDocsLocalization")=="en-us")}')
        d = input("> ")
        if isYes(d) == True:
            cf.main_config["EFlagLimitAPIDocsLocalization"] = "en-us"
            printDebugMessage(f'User selected: {cf.main_config.get("EFlagLimitAPIDocsLocalization")}')
        elif isRequestClose(d) == True: 
            printMainMessage("Closing settings..")
            return ts("Settings was closed.")
        elif isNo(d) == True:
            cf.main_config["EFlagLimitAPIDocsLocalization"] = None
            printDebugMessage("User selected: None")
    def set_overwrite_studio_fonts():
        printMainMessage("Would you like to enable deleting localized Studio fonts? (y/n)")
        return handleBasicSetting("EFlagOverwriteUnneededStudioFonts", False)
    def go_through_all():
        if set_studio_enabled(): return ts("Settings was closed.")
        if set_fresh_copy(): return ts("Settings was closed.")
        if set_url_schemes(): return ts("Settings was closed.")
        if set_player_args(): return ts("Settings was closed.")
        if cf.main_config.get("EFlagRobloxStudioEnabled") == True:
            if set_studio_args(): return ts("Settings was closed.")
        if set_unfriend_checks(): return ts("Settings was closed.")
        if set_security_cookie(): return ts("Settings was closed.")
        if set_url_quick_launch(): return ts("Settings was closed.")
        if cf.main_config.get("EFlagRobloxUnfriendCheckEnabled") == True:
            if set_unfriend_user_id(): return ts("Settings was closed.")
        if cf.main_os == "Darwin":
            if set_skip_mod_mode(): return ts("Settings was closed.")
            if set_disable_reopen(): return ts("Settings was closed.")
        if set_disable_reinstall_checks(): return ts("Settings was closed.")
        if cf.main_config.get("EFlagRobloxStudioEnabled") == True:
            if set_limit_api_docs(): return ts("Settings was closed.")
            if set_overwrite_studio_fonts(): return ts("Settings was closed.")
        return None

    # Roblox Settings Loop
    while True:
        generated_ui_options = []
        printSystemMessage("--- Roblox Settings ---")
        generated_ui_options.append({"index": 1, "message": ts("Roblox Studio Integration"), "func": set_studio_enabled, "clear_console": True})
        generated_ui_options.append({"index": 2, "message": ts("Fresh Copy Installation"), "func": set_fresh_copy, "clear_console": True})
        generated_ui_options.append({"index": 3, "message": ts("URL Schemes"), "func": set_url_schemes, "clear_console": True})
        generated_ui_options.append({"index": 4, "message": ts("Roblox Player Arguments"), "func": set_player_args, "clear_console": True})
        ind = 5
        if cf.main_config.get("EFlagRobloxStudioEnabled") == True: generated_ui_options.append({"index": ind, "message": ts("Roblox Studio Arguments"), "func": set_studio_args, "clear_console": True}); ind += 1
        generated_ui_options.append({"index": ind, "message": ts("Unfriend Checks"), "func": set_unfriend_checks, "clear_console": True}); ind += 1
        generated_ui_options.append({"index": ind, "message": ts("Security Cookie Usage"), "func": set_security_cookie, "clear_console": True}); ind += 1
        generated_ui_options.append({"index": ind, "message": ts("URL Quick Launch"), "func": set_url_quick_launch, "clear_console": True}); ind += 1
        if cf.main_config.get("EFlagRobloxUnfriendCheckEnabled") == True: generated_ui_options.append({"index": ind, "message": ts("Unfriend Check User ID"), "func": set_unfriend_user_id, "clear_console": True}); ind += 1
        if cf.main_os == "Darwin":
            generated_ui_options.append({"index": ind, "message": ts("Quick Modification Mode"), "func": set_skip_mod_mode, "clear_console": True}); ind += 1
            generated_ui_options.append({"index": ind, "message": ts("Disable Reopen after Restart"), "func": set_disable_reopen, "clear_console": True}); ind += 1
        generated_ui_options.append({"index": ind, "message": ts("Disable Reinstall Checks"), "func": set_disable_reinstall_checks, "clear_console": True}); ind += 1
        if cf.main_config.get("EFlagRobloxStudioEnabled") == True:
            generated_ui_options.append({"index": ind, "message": ts("Limit API Docs Localization"), "func": set_limit_api_docs, "clear_console": True}); ind += 1
            generated_ui_options.append({"index": ind, "message": ts("Overwrite Unneeded Studio Fonts"), "func": set_overwrite_studio_fonts, "clear_console": True}); ind += 1
        generated_ui_options.append({"index": ind, "message": ts("Go through all settings"), "func": go_through_all, "clear_console": True})
        opt = generateMenuSelection(generated_ui_options, star_option=ts("Back to Main Settings"))
        if opt:
            if opt.get("clear_console") == True: startMessage()
            printSystemMessage(f"--- {opt.get('message')} ---")
            re = opt["func"]()
            if re == "Settings was closed." or re == ts("Settings was closed."): return ts("Settings was closed.")
        else: return
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
    def enable_tracking():
        printMainMessage("Would you like to allow Activity Tracking on the Roblox client? (y/n)")
        printMainMessage("This will allow features like:")
        printMainMessage("- Server Locations")
        printMainMessage("- Multiple Instances")
        printMainMessage("- Discord Presence (+ BloxstrapRPC support)")
        printMainMessage("- Discord Webhooks")
        printMainMessage("- Mod Scripts")
        return handleBasicSetting("EFlagAllowActivityTracking", True)
    def disable_tracking():
        printMainMessage("Are you sure you want to disable Activity Tracking? (y/n)")
        d = input("> ")
        if isYes(d) == True:
            cf.main_config["EFlagAllowActivityTracking"] = False
            printDebugMessage("User selected: False")
            printSuccessMessage("Activity Tracking disabled.")
        elif isRequestClose(d) == True: 
            printMainMessage("Closing settings..")
            return ts("Settings was closed.")
        elif isNo(d) == True: printDebugMessage("User selected: True")
    def set_server_locations():
        printMainMessage("Would you like to enable Server Locations? (y/n)")
        return handleBasicSetting("EFlagNotifyServerLocation", False)
    def set_server_uptime():
        printMainMessage("Would you like to enable Server Uptime inside Server Location Notifications? (y/n)")
        printYellowMessage("This option uses the RoValra API to get server uptime information.")
        printYellowMessage("Though this option may be inaccurate, it may still give a base.")
        return handleBasicSetting("EFlagEnableRoValraServerUptime", False)
    def set_discord_rpc():
        printMainMessage("Would you like to enable Discord RPC? (y/n)")
        return handleBasicSetting("EFlagEnableDiscordRPC", False)
    def set_discord_rpc_studio():
        printMainMessage("Would you like to enable Discord RPC for Roblox Studio? (y/n)")
        return handleBasicSetting("EFlagEnableDiscordRPCStudio", False)
    def set_rpc_joining():
        printMainMessage("Would you like to enable joining from your Discord profile? (Everyone will be allowed to join depending on type of server.)")
        return handleBasicSetting("EFlagEnableDiscordRPCJoining", False)
    def set_rpc_profile_pic():
        printMainMessage("Would you like to enable showing your account's profile picture on the small image for default?")
        return handleBasicSetting("EFlagShowUserProfilePictureInsteadOfLogo", False)
    def set_rpc_username():
        printMainMessage("Would you like to enable showing your account's username in the small image for default?")
        return handleBasicSetting("EFlagShowUsernameInSmallImage", False)
    def set_bloxstrap_sdk():
        printMainMessage("Would you like to enable games to use the Bloxstrap SDK? (y/n)")
        return handleBasicSetting("EFlagAllowBloxstrapSDK", False)
    def set_idling_rpc():
        printMainMessage("Would you like to enable Idling Roblox RPC? (y/n)")
        return handleBasicSetting("EFlagEnableDefaultDiscordRPC", True)
    def set_game_status_bar():
        printMainMessage("Would you like to enable showing playing game name in Status Bar? (y/n)")
        printYellowMessage("This option requires pypresence v4.6.0+ to be installed")
        return handleBasicSetting("EFlagShowGameNameInStatusBar", False)
    def set_studio_status_bar():
        printMainMessage("Would you like to enable showing Editing Studio Game Name in Status Bar? (y/n)")
        printYellowMessage("This option requires pypresence v4.6.0+ to be installed")
        return handleBasicSetting("EFlagShowStudioGameNameInStatusBar", False)
    def set_bloxstrap_sdk_studio():
        printMainMessage("Would you like to enable Roblox Studio to use the Bloxstrap SDK? (y/n)")
        return handleBasicSetting("EFlagAllowBloxstrapStudioSDK", False)
    def set_private_server_joining():
        printMainMessage("Would you like to enable access to private servers you connect to from Discord Presences? (users may be able to join or not) (y/n)")
        return handleBasicSetting("EFlagAllowPrivateServerJoining", False)
    def set_discord_webhook():
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
            else:
                cf.main_config["EFlagUseDiscordWebhook"] = False
                printErrorMessage("The provided webhook link is not a valid format.")
        elif isRequestClose(d) == True: 
            printMainMessage("Closing settings..")
            return ts("Settings was closed.")
        elif isNo(d) == True:
            cf.main_config["EFlagUseDiscordWebhook"] = False
            printDebugMessage("User selected: False")
    def set_webhook_preferences():
        if cf.main_config.get("EFlagUseDiscordWebhook") == True and cf.main_config.get("EFlagDiscordWebhookURL", "").startswith("https://discord.com/api/webhooks/"):
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
                if isYes(d) == True: cf.main_config["EFlagDiscordWebhookConnect"] = True; printDebugMessage("User selected: True")
                elif isNo(d) == True: cf.main_config["EFlagDiscordWebhookConnect"] = False; printDebugMessage("User selected: False")
                elif isRequestClose(d) == True: return ts("Settings was closed.")
                co += 1
                printMainMessage(f"[{co}/{max_setti}] Roblox Disconnecting Information (y/n)")
                printMainMessage("When you leave a Roblox game (or leave a Roblox Studio session), your webhook gets pinged with information such as Server Location and Joining Link.")
                printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagDiscordWebhookDisconnect")==True)}')
                d = input("> ")
                if isYes(d) == True: cf.main_config["EFlagDiscordWebhookDisconnect"] = True; printDebugMessage("User selected: True")
                elif isNo(d) == True: cf.main_config["EFlagDiscordWebhookDisconnect"] = False; printDebugMessage("User selected: False")
                elif isRequestClose(d) == True: return ts("Settings was closed.")
                co += 1
                printMainMessage(f"[{co}/{max_setti}] Roblox Opening Information (y/n)")
                printMainMessage("When you open Roblox (or Roblox Studio), your webhook gets pinged with information such as Process ID and Log File Location.")
                printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagDiscordWebhookRobloxAppStart")==True)}')
                d = input("> ")
                if isYes(d) == True: cf.main_config["EFlagDiscordWebhookRobloxAppStart"] = True; printDebugMessage("User selected: True")
                elif isNo(d) == True: cf.main_config["EFlagDiscordWebhookRobloxAppStart"] = False; printDebugMessage("User selected: False")
                elif isRequestClose(d) == True: return ts("Settings was closed.")
                co += 1
                printMainMessage(f"[{co}/{max_setti}] Roblox Closing Information (y/n)")
                printMainMessage("When you close Roblox (or Roblox Studio), your webhook gets pinged with information such as Process ID and Log File Location.")
                printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagDiscordWebhookRobloxAppClose")==True)}')
                d = input("> ")
                if isYes(d) == True: cf.main_config["EFlagDiscordWebhookRobloxAppClose"] = True; printDebugMessage("User selected: True")
                elif isNo(d) == True: cf.main_config["EFlagDiscordWebhookRobloxAppClose"] = False; printDebugMessage("User selected: False")
                elif isRequestClose(d) == True: return ts("Settings was closed.")
                co += 1
                printMainMessage(f"[{co}/{max_setti}] Roblox Crashing Information (y/n)")
                printMainMessage("When Roblox (or Roblox Studio) crashes, your webhook gets pinged with the console log that shows the cause of the crash.")
                printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagDiscordWebhookRobloxCrash")==True)}')
                d = input("> ")
                if isYes(d) == True: cf.main_config["EFlagDiscordWebhookRobloxCrash"] = True; printDebugMessage("User selected: True")
                elif isNo(d) == True: cf.main_config["EFlagDiscordWebhookRobloxCrash"] = False; printDebugMessage("User selected: False")
                elif isRequestClose(d) == True: return ts("Settings was closed.")
                co += 1
                printMainMessage(f"[{co}/{max_setti}] BloxstrapRPC Information (y/n)")
                printMainMessage("When BloxstrapRPC is triggered (if enabled), your webhook gets pinged with the changes given from the launched game.")
                printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagDiscordWebhookBloxstrapRPC")==True)}')
                d = input("> ")
                if isYes(d) == True: cf.main_config["EFlagDiscordWebhookBloxstrapRPC"] = True; printDebugMessage("User selected: True")
                elif isNo(d) == True: cf.main_config["EFlagDiscordWebhookBloxstrapRPC"] = False; printDebugMessage("User selected: False")
                elif isRequestClose(d) == True: return ts("Settings was closed.")
                if cf.main_config.get("EFlagRobloxStudioEnabled") == True:
                    co += 1
                    printMainMessage(f"[{co}/{max_setti}] Publishing Game Information (y/n)")
                    printMainMessage("When you publish a game from Roblox Studio, your webhook gets pinged with game information such as Server Location and Editing Link.")
                    printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagDiscordWebhookGamePublished")==True)}')
                    d = input("> ")
                    if isYes(d) == True: cf.main_config["EFlagDiscordWebhookGamePublished"] = True; printDebugMessage("User selected: True")
                    elif isNo(d) == True: cf.main_config["EFlagDiscordWebhookGamePublished"] = False; printDebugMessage("User selected: False")
                    elif isRequestClose(d) == True: return ts("Settings was closed.")
                    co += 1
                    printMainMessage(f"[{co}/{max_setti}] Saving Game Information (y/n)")
                    printMainMessage("When you save a game from Roblox Studio, your webhook gets pinged with game information such as Server Location and Editing Link.")
                    printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagDiscordWebhookGameSaved")==True)}')
                    d = input("> ")
                    if isYes(d) == True: cf.main_config["EFlagDiscordWebhookGameSaved"] = True; printDebugMessage("User selected: True")
                    elif isNo(d) == True: cf.main_config["EFlagDiscordWebhookGameSaved"] = False; printDebugMessage("User selected: False")
                    elif isRequestClose(d) == True: return ts("Settings was closed.")
                printMainMessage("Would you like it to show the pid number in the webhook footer? (y/n)")
                printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagDiscordWebhookShowPidInFooter")==True)}')
                d = input("> ")
                if isYes(d) == True: cf.main_config["EFlagDiscordWebhookShowPidInFooter"] = True; printDebugMessage("User selected: True")
                elif isNo(d) == True: cf.main_config["EFlagDiscordWebhookShowPidInFooter"] = False; printDebugMessage("User selected: False")
                elif isRequestClose(d) == True: return ts("Settings was closed.")
        else: printErrorMessage("Please configure a valid Discord Webhook first.")
    def set_studio_force_reconnect():
        printMainMessage("Would you like to enable force reconnection when you disconnect from a Studio server? (y/n)")
        return handleBasicSetting("EFlagForceReconnectOnStudioLost", False)
    def set_window_title_options():
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
    def go_through_all():
        if set_server_locations(): return ts("Settings was closed.")
        if set_server_uptime(): return ts("Settings was closed.")
        if set_discord_rpc(): return ts("Settings was closed.")
        if cf.main_config.get("EFlagRobloxStudioEnabled") == True:
            if set_discord_rpc_studio(): return ts("Settings was closed.")
        if cf.main_config.get("EFlagEnableDiscordRPC") == True or cf.main_config.get("EFlagEnableDiscordRPCStudio") == True:
            if set_rpc_joining(): return ts("Settings was closed.")
            if set_rpc_profile_pic(): return ts("Settings was closed.")
            if set_rpc_username(): return ts("Settings was closed.")
            if set_bloxstrap_sdk(): return ts("Settings was closed.")
            if set_idling_rpc(): return ts("Settings was closed.")
            if set_game_status_bar(): return ts("Settings was closed.")
            if set_studio_status_bar(): return ts("Settings was closed.")
            if cf.main_config.get("EFlagRobloxStudioEnabled") == True:
                if set_bloxstrap_sdk_studio(): return ts("Settings was closed.")
            if set_private_server_joining(): return ts("Settings was closed.")
        if set_discord_webhook(): return ts("Settings was closed.")
        if cf.main_config.get("EFlagUseDiscordWebhook") == True and cf.main_config.get("EFlagDiscordWebhookURL", "").startswith("https://discord.com/api/webhooks/"):
            if set_webhook_preferences(): return ts("Settings was closed.")
        if cf.main_config.get("EFlagRobloxStudioEnabled") == True:
            if set_studio_force_reconnect(): return ts("Settings was closed.")
        if cf.main_os == "Windows":
            if set_window_title_options(): return ts("Settings was closed.")
        return None

    # Main Loop
    while True:
        generated_ui_options = []
        printSystemMessage("--- Activity Tracking ---")
        if cf.main_config.get("EFlagAllowActivityTracking", True) == False:
            printYellowMessage("Activity Tracking is currently disabled.")
            printMainMessage("You must enable it to access these settings.")
            generated_ui_options.append({"index": 1, "message": ts("Enable Activity Tracking"), "func": enable_tracking, "clear_console": True})
            opt = generateMenuSelection(generated_ui_options, star_option=ts("Back to Main Settings"))
            if opt:
                if opt.get("clear_console") == True: startMessage()
                re = opt["func"]()
                if re == "Settings was closed." or re == ts("Settings was closed."): return ts("Settings was closed.")
            else: return
        else:
            ind = 1
            generated_ui_options.append({"index": ind, "message": ts("Server Locations"), "func": set_server_locations, "clear_console": True}); ind += 1
            generated_ui_options.append({"index": ind, "message": ts("Server Uptime"), "func": set_server_uptime, "clear_console": True}); ind += 1
            generated_ui_options.append({"index": ind, "message": ts("Discord RPC"), "func": set_discord_rpc, "clear_console": True}); ind += 1
            if cf.main_config.get("EFlagRobloxStudioEnabled") == True: generated_ui_options.append({"index": ind, "message": ts("Discord RPC for Roblox Studio"), "func": set_discord_rpc_studio, "clear_console": True}); ind += 1
            if cf.main_config.get("EFlagEnableDiscordRPC") == True or cf.main_config.get("EFlagEnableDiscordRPCStudio") == True:
                generated_ui_options.append({"index": ind, "message": ts("Discord RPC Joining"), "func": set_rpc_joining, "clear_console": True}); ind += 1
                generated_ui_options.append({"index": ind, "message": ts("Show Profile Picture"), "func": set_rpc_profile_pic, "clear_console": True}); ind += 1
                generated_ui_options.append({"index": ind, "message": ts("Show Username in RPC"), "func": set_rpc_username, "clear_console": True}); ind += 1
                generated_ui_options.append({"index": ind, "message": ts("Bloxstrap SDK"), "func": set_bloxstrap_sdk, "clear_console": True}); ind += 1
                generated_ui_options.append({"index": ind, "message": ts("Idling Roblox RPC"), "func": set_idling_rpc, "clear_console": True}); ind += 1
                generated_ui_options.append({"index": ind, "message": ts("Game Name in Status Bar"), "func": set_game_status_bar, "clear_console": True}); ind += 1
                generated_ui_options.append({"index": ind, "message": ts("Studio Game Name in Status Bar"), "func": set_studio_status_bar, "clear_console": True}); ind += 1
                if cf.main_config.get("EFlagRobloxStudioEnabled") == True: generated_ui_options.append({"index": ind, "message": ts("Studio Bloxstrap SDK"), "func": set_bloxstrap_sdk_studio, "clear_console": True}); ind += 1
                generated_ui_options.append({"index": ind, "message": ts("Private Server Joining via RPC"), "func": set_private_server_joining, "clear_console": True}); ind += 1
            generated_ui_options.append({"index": ind, "message": ts("Discord Webhook Setup"), "func": set_discord_webhook, "clear_console": True}); ind += 1
            if cf.main_config.get("EFlagUseDiscordWebhook") == True and cf.main_config.get("EFlagDiscordWebhookURL", "").startswith("https://discord.com/api/webhooks/"): generated_ui_options.append({"index": ind, "message": ts("Discord Webhook Ping Preferences"), "func": set_webhook_preferences, "clear_console": True}); ind += 1
            if cf.main_config.get("EFlagRobloxStudioEnabled") == True: generated_ui_options.append({"index": ind, "message": ts("Force Reconnect on Studio Disconnect"), "func": set_studio_force_reconnect, "clear_console": True}); ind += 1
            if cf.main_os == "Windows": generated_ui_options.append({"index": ind, "message": ts("Window Title Options"), "func": set_window_title_options, "clear_console": True}); ind += 1
            generated_ui_options.append({"index": ind, "message": ts("Disable Activity Tracking"), "func": disable_tracking, "clear_console": True}); ind += 1
            generated_ui_options.append({"index": ind, "message": ts("Go through all settings"), "func": go_through_all, "clear_console": True})
            opt = generateMenuSelection(generated_ui_options, star_option=ts("Back to Main Settings"))
            if opt:
                if opt.get("clear_console") == True: startMessage()
                printSystemMessage(f"--- {opt.get('message')} ---")
                re = opt["func"]()
                if re == "Settings was closed." or re == ts("Settings was closed."): return ts("Settings was closed.")
            else: return
def bootstrapSettings():
    def set_language():
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
    def set_rebuilder():
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
        elif isRequestClose(a) == True: 
            printMainMessage("Closing settings..")
            return ts("Settings was closed.")
        elif isNo(a) == True:
            cf.main_config["EFlagRebuildPyinstallerAppFromSourceDuringUpdates"] = False
            cf.main_config["EFlagRebuildNuitkaAppFromSourceDuringUpdates"] = False
            printDebugMessage("User selected: False")
    def set_ecc_ca():
        printMainMessage("Would you like to enable installing the latest version of EfazDev ECC Security CA? (y/n)")
        printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagInstallEfazDevECCCertificates")==True)}')
        printYellowMessage("This is apart of code-signing and may affect security.")
        a = input("> ")
        if isYes(a) == True:
            cf.main_config["EFlagInstallEfazDevECCCertificates"] = True
            printDebugMessage("User selected: True")
        elif isRequestClose(a) == True: 
            printMainMessage("Closing settings..")
            return ts("Settings was closed.")
        elif isNo(a) == True:
            cf.main_config["EFlagInstallEfazDevECCCertificates"] = False
            printDebugMessage("User selected: False")
    def set_sync_folder():
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
        elif isRequestClose(a) == True: 
            printMainMessage("Closing settings..")
            return ts("Settings was closed.")
        elif isNo(a) == True:
            cf.main_config["EFlagOrangeBloxSyncDir"] = None
            printDebugMessage("User selected: None")
    def set_clang_rebuild():
        printMainMessage("Would you like to rebuild OrangeLoader, Play Roblox, and Run Studio app based on source code? (y/n)")
        printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagRebuildClangAppFromSourceDuringUpdates")==True)}')
        printYellowMessage("Clang++ is required to be installed on your Mac in order to use.")
        a = input("> ")
        if isYes(a) == True:
            cf.main_config["EFlagRebuildClangAppFromSourceDuringUpdates"] = True
            printDebugMessage("User selected: True")
        elif isRequestClose(a) == True: 
            printMainMessage("Closing settings..")
            return ts("Settings was closed.")
        elif isNo(a) == True:
            cf.main_config["EFlagRebuildClangAppFromSourceDuringUpdates"] = False
            printDebugMessage("User selected: False")
    def set_see_more():
        printMainMessage("Would you like to enable See More Awaiting on List Selections? (y/n)")
        return handleBasicSetting("EFlagEnableSeeMoreAwaiting", False)
    def set_429_loops():
        printMainMessage("Would you like to enable 429 Loops when the Roblox server gives a 429 (Too much request) response? (y/n)")
        return handleBasicSetting("EFlagEnableLoop429Requests", False)
    def set_cpu_memory():
        printMainMessage("Would you like to enable showing CPU Percentage and Memory Usage? (y/n)")
        return handleBasicSetting("EFlagEnableCPUMemoryUsageViewer", True)
    def set_disable_bootstrap_checks():
        printMainMessage("Would you like to disable Bootstrap Update Checks? (y/n)")
        return handleBasicSetting("EFlagDisableBootstrapChecks", False)
    def set_disable_python_checks():
        printMainMessage("Would you like to disable Python Update Checks? (y/n)")
        return handleBasicSetting("EFlagDisablePythonUpdateChecks", False)
    def set_disable_python_module_checks():
        printMainMessage("Would you like to disable Python Module Update Checks? (y/n)")
        return handleBasicSetting("EFlagDisablePythonModuleUpdateChecks", False)
    def set_cursor_start():
        printMainMessage("Would you like to begin the selection menu cursor at the start of the list instead of at the end? (y/n)")
        return handleBasicSetting("EFlagBeginMenuCursorAtStart", False)
    def set_silent_python_installs():
        printMainMessage("Would you like to enable slient Python installs instead of a prompt for python updates? (y/n)")
        if cf.main_os == "Darwin": printYellowMessage("For macOS users, admin permission is needed in order to install.")
        return handleBasicSetting("EFlagEnableSlientPythonInstalls", False)
    def set_custom_theme():
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
        elif isRequestClose(d) == True: 
            printMainMessage("Closing settings..")
            return ts("Settings was closed.")
        elif isNo(d) == True:
            cf.main_config["EFlagCustomBootstrapName"] = "OrangeBlox"
            cf.main_config["EFlagCustomBootstrapEmoji"] = "🍊"
            cf.main_config["EFlagCustomBootstrapColor"] = "#ff4b00"
            cf.main_config["EFlagCustomBootstrapInternetURL"] = f"{cf.main_host}/Images/AppIcon.png"
            cf.main_config["EFlagCustomBootstrapIconPath"] = os.path.join(cf.cur_path, "Images", "AppIcon.png")
            printDebugMessage("User selected: Default")
    def set_beta():
        printMainMessage(f"Would you like to enable {obName0()} Beta? (y/n)")
        printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagBootstrapUpdateServer")=="https://raw.githubusercontent.com/EfazDev/orangeblox/refs/heads/beta/Version.json" or cf.main_config.get("EFlagBootstrapUpdateServer")=="https://obxbeta.efaz.dev/Version.json")}')
        printYellowMessage("Betas could contain bugs that could break your Roblox installation!")
        d = input("> ")
        if isYes(d) == True:
            cf.main_config["EFlagBootstrapUpdateServer"] = "https://obxbeta.efaz.dev/Version.json"
            printDebugMessage("User selected: True")
        elif isRequestClose(d) == True: 
            printMainMessage("Closing settings..")
            return ts("Settings was closed.")
        elif isNo(d) == True:
            cf.main_config["EFlagBootstrapUpdateServer"] = "https://obx.efaz.dev/Version.json"
            printDebugMessage("User selected: False")
    def set_disable_autosave():
        printMainMessage(f"Would you like to disable automatically saving your {obName0()} Configuration to your installation folder? (y/n)")
        return handleBasicSetting("EFlagDisableAutosaveToInstallation", False)
    def set_disable_cooldown():
        printMainMessage("Would you like to disable Bootstrap Cooldowns? (y/n)")
        printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagDisableBootstrapCooldown")==True)}')
        printYellowMessage("If your computer is laggy, this may prevent multiple windows opening.")
        d = input("> ")
        if isYes(d) == True:
            cf.main_config["EFlagDisableBootstrapCooldown"] = True
            printDebugMessage("User selected: True")
        elif isRequestClose(d) == True: 
            printMainMessage("Closing settings..")
            return ts("Settings was closed.")
        elif isNo(d) == True:
            cf.main_config["EFlagDisableBootstrapCooldown"] = False
            printDebugMessage("User selected: False")
    def set_virtual_envs():
        printMainMessage(f"Would you like to use Python Virtual Environments for {obName0()}? (y/n)")
        return handleBasicSetting("EFlagEnablePythonVirtualEnvironments", False)
    def set_python_cache():
        printMainMessage("Would you like to build Python cache on app start? (y/n)")
        return handleBasicSetting("EFlagBuildPythonCacheOnStart", False)
    def set_os_specific_options():
        if cf.main_os == "Windows":
            printMainMessage(f"Would you like to make shortcuts for {obName0()}? [Needed for launching through the Windows Start Menu and Desktop] (y/n)")
            return handleBasicSetting("EFlagDisableShortcutsInstall", False, False)
        elif cf.main_os == "Darwin":
            printMainMessage("Would you like to enable Dock Bar and System Tray options when right clicking the app icon? (y/n)")
            return handleBasicSetting("EFlagEnableGUIOptionMenus", True)
    def go_through_all():
        if set_language(): return ts("Settings was closed.")
        if set_rebuilder(): return ts("Settings was closed.")
        if set_ecc_ca(): return ts("Settings was closed.")
        if set_sync_folder(): return ts("Settings was closed.")
        if cf.main_os == "Darwin":
            if set_clang_rebuild(): return ts("Settings was closed.")
        if set_see_more(): return ts("Settings was closed.")
        if set_429_loops(): return ts("Settings was closed.")
        if set_cpu_memory(): return ts("Settings was closed.")
        if set_disable_bootstrap_checks(): return ts("Settings was closed.")
        if set_disable_python_checks(): return ts("Settings was closed.")
        if set_disable_python_module_checks(): return ts("Settings was closed.")
        if set_cursor_start(): return ts("Settings was closed.")
        if cf.main_config.get("EFlagDisablePythonUpdateChecks", False) == False:
            if set_silent_python_installs(): return ts("Settings was closed.")
        if set_custom_theme(): return ts("Settings was closed.")
        if set_beta(): return ts("Settings was closed.")
        if set_disable_autosave(): return ts("Settings was closed.")
        if cf.main_os == "Windows":
            if set_disable_cooldown(): return ts("Settings was closed.")
        if set_virtual_envs(): return ts("Settings was closed.")
        if set_python_cache(): return ts("Settings was closed.")
        if set_os_specific_options(): return ts("Settings was closed.")
        return None
    while True:
        generated_ui_options = []
        printSystemMessage("--- Bootstrap Settings ---")
        ind = 1
        generated_ui_options.append({"index": ind, "message": ts("Bootstrap Language"), "func": set_language, "clear_console": True}); ind += 1
        generated_ui_options.append({"index": ind, "message": ts("Main Loader Rebuilder"), "func": set_rebuilder, "clear_console": True}); ind += 1
        generated_ui_options.append({"index": ind, "message": ts("Install ECC Security CA"), "func": set_ecc_ca, "clear_console": True}); ind += 1
        generated_ui_options.append({"index": ind, "message": ts("Sync Folder"), "func": set_sync_folder, "clear_console": True}); ind += 1
        if cf.main_os == "Darwin":
            generated_ui_options.append({"index": ind, "message": ts("Rebuild Clang App"), "func": set_clang_rebuild, "clear_console": True}); ind += 1
        generated_ui_options.append({"index": ind, "message": ts("See More Awaiting"), "func": set_see_more, "clear_console": True}); ind += 1
        generated_ui_options.append({"index": ind, "message": ts("429 Loops"), "func": set_429_loops, "clear_console": True}); ind += 1
        generated_ui_options.append({"index": ind, "message": ts("CPU/Memory Usage Viewer"), "func": set_cpu_memory, "clear_console": True}); ind += 1
        generated_ui_options.append({"index": ind, "message": ts("Disable Bootstrap Update Checks"), "func": set_disable_bootstrap_checks, "clear_console": True}); ind += 1
        generated_ui_options.append({"index": ind, "message": ts("Disable Python Update Checks"), "func": set_disable_python_checks, "clear_console": True}); ind += 1
        generated_ui_options.append({"index": ind, "message": ts("Disable Python Module Update Checks"), "func": set_disable_python_module_checks, "clear_console": True}); ind += 1
        generated_ui_options.append({"index": ind, "message": ts("Menu Cursor Start Location"), "func": set_cursor_start, "clear_console": True}); ind += 1
        if cf.main_config.get("EFlagDisablePythonUpdateChecks", False) == False: generated_ui_options.append({"index": ind, "message": ts("Silent Python Installs"), "func": set_silent_python_installs, "clear_console": True}); ind += 1
        generated_ui_options.append({"index": ind, "message": ts("Custom Bootstrap Theme"), "func": set_custom_theme, "clear_console": True}); ind += 1
        generated_ui_options.append({"index": ind, "message": ts(f"{obName0()} Beta Options"), "func": set_beta, "clear_console": True}); ind += 1
        generated_ui_options.append({"index": ind, "message": ts("Disable Autosave to Installation"), "func": set_disable_autosave, "clear_console": True}); ind += 1
        if cf.main_os == "Windows": generated_ui_options.append({"index": ind, "message": ts("Disable Bootstrap Cooldowns"), "func": set_disable_cooldown, "clear_console": True}); ind += 1
        generated_ui_options.append({"index": ind, "message": ts("Python Virtual Environments"), "func": set_virtual_envs, "clear_console": True}); ind += 1
        generated_ui_options.append({"index": ind, "message": ts("Build Python Cache on Start"), "func": set_python_cache, "clear_console": True}); ind += 1
        if cf.main_os == "Windows": generated_ui_options.append({"index": ind, "message": ts("App Shortcuts"), "func": set_os_specific_options, "clear_console": True}); ind += 1
        elif cf.main_os == "Darwin": generated_ui_options.append({"index": ind, "message": ts("Dock Bar and System Tray Options"), "func": set_os_specific_options, "clear_console": True}); ind += 1
        generated_ui_options.append({"index": ind, "message": ts("Go through all settings"), "func": go_through_all, "clear_console": True})
        opt = generateMenuSelection(generated_ui_options, star_option=ts("Back to Main Settings"))
        if opt:
            if opt.get("clear_console") == True: startMessage()
            printSystemMessage(f"--- {opt.get('message')} ---")
            re = opt["func"]()
            if re == "Settings was closed." or re == ts("Settings was closed."): return ts("Settings was closed.")
        else: return
def debugging():
    def set_debug_mode():
        printMainMessage("Would you like to enable Debug Mode? (y/n)")
        printMainMessage(f'Current Setting: {(cf.main_config.get("EFlagEnableDebugMode")==True)}')
        printYellowMessage("[WARNING! This will expose information like login to Roblox.]")
        printYellowMessage("[DO NOT EVER ENABLE IF SOMEONE TOLD YOU SO OR YOU USUALLY RECORD!!]")
        d = input("> ")
        if isYes(d) == True:
            cf.main_config["EFlagEnableDebugMode"] = True
            printDebugMessage("User selected: True")
        elif isRequestClose(d) == True: 
            printMainMessage("Closing settings..")
            return ts("Settings was closed.")
        elif isNo(d) == True:
            cf.main_config["EFlagEnableDebugMode"] = False
            printDebugMessage("User selected: False")
        cf.pip_class.debug = cf.main_config.get("EFlagEnableDebugMode") == True
    def set_full_debug_mode():
        printMainMessage("Would you like to print unhandled Roblox client events? (y/n)")
        return handleBasicSetting("EFlagAllowFullDebugMode", False)
    def set_bootstrap_logs():
        printMainMessage("Would you like to enable saving Bootstrap logs? (y/n)")
        return handleBasicSetting("EFlagMakeMainBootstrapLogFiles", False)
    def set_roblox_channel():
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
                elif isRequestClose(channel_inp) == True:
                    printMainMessage("Closing settings..")
                    return ts("Settings was closed.")
                else:
                    try:
                        a = cf.handler.getLatestClientVersion(studio=False, debug=cf.main_config.get("EFlagEnableDebugMode"), channel=channel_inp, token=createDownloadToken(False))
                        if a.get("success") == True and a.get("attempted_channel") == channel_inp:
                            cf.main_config["EFlagRobloxClientChannel"] = channel_inp
                            cf.main_config["EFlagDisableRobloxUpdateChecks"] = False
                            printSuccessMessage("Successfully set Roblox client channel!")
                        else:
                            printErrorMessage("Channel may not exist. Please try again or use LIVE!")
                            return t()
                    except Exception:
                        printErrorMessage("Something went wrong. Please try again or use LIVE!")
                        return t()
            return t()
        elif isRequestClose(d) == True: 
            printMainMessage("Closing settings..")
            return ts("Settings was closed.")
        elif isNo(d) == True:
            cf.main_config["EFlagRobloxClientChannel"] = "LIVE"
            cf.main_config["EFlagDisableRobloxUpdateChecks"] = False
            printDebugMessage("User selected: False")
    def set_studio_channel():
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
                elif isRequestClose(channel_inp) == True:
                    printMainMessage("Closing settings..")
                    return ts("Settings was closed.")
                else:
                    try:
                        a = cf.handler.getLatestClientVersion(studio=True, debug=cf.main_config.get("EFlagEnableDebugMode"), channel=channel_inp, token=createDownloadToken(True))
                        if a.get("success") == True and a.get("attempted_channel") == channel_inp:
                            cf.main_config["EFlagRobloxStudioClientChannel"] = channel_inp
                            cf.main_config["EFlagDisableRobloxUpdateChecks"] = False
                            printSuccessMessage("Successfully set Roblox Studio client channel!")
                        else:
                            printErrorMessage("Channel may not exist. Please try again or use LIVE!")
                            return t()
                    except Exception:
                        printErrorMessage("Something went wrong. Please try again or use LIVE!")
                        return t()
            return t()
        elif isRequestClose(d) == True: 
            printMainMessage("Closing settings..")
            return ts("Settings was closed.")
        elif isNo(d) == True:
            cf.main_config["EFlagRobloxStudioClientChannel"] = "LIVE"
            cf.main_config["EFlagDisableRobloxUpdateChecks"] = False
            printDebugMessage("User selected: False")
    def set_hash_verification():
        printMainMessage("Would you like to enable Hash Verification on Roblox Player and Studio after updates? (y/n)")
        printMainMessage(f'Current Setting: {cf.main_config.get("EFlagVerifyRobloxHashAfterInstall")!=False}')
        printYellowMessage("This is a security measure that be used to validate Roblox in case of insecure downloads.")
        d = input("> ")
        if isYes(d) == True:
            cf.main_config["EFlagVerifyRobloxHashAfterInstall"] = True
            printDebugMessage("User selected: True")
        elif isRequestClose(d) == True: 
            printMainMessage("Closing settings..")
            return ts("Settings was closed.")
        elif isNo(d) == True:
            cf.main_config["EFlagVerifyRobloxHashAfterInstall"] = False
            printDebugMessage("User selected: False")
    def go_through_all():
        if set_debug_mode(): return ts("Settings was closed.")
        if cf.main_config.get("EFlagEnableDebugMode") == True:
            if set_full_debug_mode(): return ts("Settings was closed.")
        if set_bootstrap_logs(): return ts("Settings was closed.")
        if set_roblox_channel(): return ts("Settings was closed.")
        if cf.main_config.get("EFlagRobloxStudioEnabled") == True:
            if set_studio_channel(): return ts("Settings was closed.")
        if set_hash_verification(): return ts("Settings was closed.")
        return None
    while True:
        generated_ui_options = []
        printSystemMessage("--- Debugging ---")
        ind = 1
        generated_ui_options.append({"index": ind, "message": ts("Debug Mode"), "func": set_debug_mode, "clear_console": True}); ind += 1
        if cf.main_config.get("EFlagEnableDebugMode") == True: generated_ui_options.append({"index": ind, "message": ts("Print Unhandled Client Events"), "func": set_full_debug_mode, "clear_console": True}); ind += 1
        generated_ui_options.append({"index": ind, "message": ts("Save Bootstrap Logs"), "func": set_bootstrap_logs, "clear_console": True}); ind += 1
        generated_ui_options.append({"index": ind, "message": ts("Roblox Client Channel"), "func": set_roblox_channel, "clear_console": True}); ind += 1
        if cf.main_config.get("EFlagRobloxStudioEnabled") == True: generated_ui_options.append({"index": ind, "message": ts("Roblox Studio Client Channel"), "func": set_studio_channel, "clear_console": True}); ind += 1
        generated_ui_options.append({"index": ind, "message": ts("Hash Verification"), "func": set_hash_verification, "clear_console": True}); ind += 1
        generated_ui_options.append({"index": ind, "message": ts("Go through all settings"), "func": go_through_all, "clear_console": True})
        opt = generateMenuSelection(generated_ui_options, star_option=ts("Back to Main Settings"))
        if opt:
            if opt.get("clear_console") == True: startMessage()
            printSystemMessage(f"--- {opt.get('message')} ---")
            re = opt["func"]()
            if re == "Settings was closed." or re == ts("Settings was closed."): return ts("Settings was closed.")
        else: return
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
            generated_ui_options = []
            generated_ui_options.append({
                "index": 1,
                "message": ts("Return to Settings"),
                "func": mainSettings,
                "clear_console": True
            })
            opt2 = generateMenuSelection(generated_ui_options, star_option=ts("Exit Settings"))
            if opt2:
                if opt2.get("clear_console") == True: startMessage()
                re = opt2["func"]()
                if re == "Settings was closed." or re == ts("Settings was closed."): return ts("Settings was closed.")
            else:
                saveSettings()
                printSuccessMessage("Successfully saved settings!")
                return ts("Successfully saved settings!")
        else:
            if re == "Settings was closed." or re == ts("Settings was closed."):
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