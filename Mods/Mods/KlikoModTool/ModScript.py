#
# Kliko Mod Generator
# Originally Made by TheKliko, Reedited by EfazDev
# v1.3.1
# 

# Python Modules
import subprocess
import shutil
import json
import sys
import re
import os

# Load Bootstrap API
import OrangeAPI as orange; OrangeAPI = orange.OrangeAPI()
debugMode = OrangeAPI.getDebugMode()
apiVersion = OrangeAPI.about()
current_version = OrangeAPI.getVersion()
cur_path = os.path.dirname(os.path.abspath(__file__))

def getFilePrompt():
    return subprocess.run([sys.executable, "-c", "import promptlib; prompter = promptlib.Files(); print(prompter.file())"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode().strip()
    
# Printing Functions
def printMainMessage(mes): OrangeAPI.printMainMessage(mes) # White System Console Text
def printErrorMessage(mes): OrangeAPI.printErrorMessage(mes) # Error Colored Console Text
def printSuccessMessage(mes): OrangeAPI.printSuccessMessage(mes) # Success Colored Console Text
def printYellowMessage(mes): OrangeAPI.printWarnMessage(mes) # Yellow Colored Console Text
def printDebugMessage(mes): OrangeAPI.printDebugMessage(mes) # Debug Console Text
def isYes(text: str): text = text.strip(); return text.lower() == "y" or text.lower() == "yes" or text.lower() == "true" or text.lower() == "t"
def isNo(text: str): text = text.strip(); return text.lower() == "n" or text.lower() == "no" or text.lower() == "false" or text.lower() == "f"
    
OrangeAPI.printColoredMessage("Kliko Mod Tool 🍎 for OrangeBlox 🍊", 197)
OrangeAPI.printColoredMessage("Edited for OrangeBlox by EfazDev 🍊 / Originally Made By TheKliko 🍎", 197)
OrangeAPI.printColoredMessage("THIS MOD IS NOT MADE BY THEKLIKO NOR WARRANTED BY HIM!", 197)
studio = OrangeAPI.getStudioMode()
installed = OrangeAPI.getInstalledRobloxVersion()
installed = {"success": installed["success"], "channel": installed.get("channel"), "version": installed.get("client_version"), "hash": installed.get("hash")}
if installed["success"] == False:
    installed = OrangeAPI.getLatestRobloxVersion()
    installed = {"success": installed["success"], "channel": installed.get("attempted_channel"), "version": installed.get("client_version"), "hash": installed.get("hash")}
if installed["success"] == True:
    OrangeAPI.printColoredMessage(f"Roblox Version Used: {installed['version']} (Channel: {installed['channel']} 🍎)", 197)
    if not (type(OrangeAPI.getConfiguration("KlikoHandlingModType")) is int):
        printMainMessage("[1] = Generate New Mods")
        printMainMessage("[2] = Update Old Mods")
        a = OrangeAPI.requestInput("What type of mod action would you like to use? (To reset, delete your Configuration file)", "> ")
        if a:
            if a == "1": OrangeAPI.setConfiguration("KlikoHandlingModType", 1)
            elif a == "2": OrangeAPI.setConfiguration("KlikoHandlingModType", 2)
            else: printDebugMessage("Invalid mod type option.")
    mod_type = OrangeAPI.getConfiguration("KlikoHandlingModType")
    if (type(mod_type) is int):
        if mod_type == 1:
            mod_style_config = OrangeAPI.getConfiguration("ModConfiguration")
            mod_style_file = None
            if mod_style_config and os.path.isfile(mod_style_config): mod_style_file = mod_style_config
            else:
                if OrangeAPI.getIfRobloxLaunched() == False:
                    printMainMessage("Would you like to use an existing Generative Mod Configuration or would you like to make a new configuration?")
                    printMainMessage("[1] = New Configuration")
                    printMainMessage("[2] = Use Existing Configuration")
                    printMainMessage("[3] = Use Provided Configuration")
                    a = OrangeAPI.requestInput("Enter here:", "> ")
                    if a and a == "1":
                        mod_name = OrangeAPI.requestInput("Alright then! Enter the name of the configuration below to get started!", "> ")
                        def getAngle():
                            angl = OrangeAPI.requestInput("Now, enter the angle number of the gradient image!", "> ")
                            if angl.isdigit() and int(angl) >= 0:
                                printDebugMessage(f"Angle Number: {int(angl)}*")
                                return int(angl)
                            else:
                                printErrorMessage("Please try again!")
                                return getAngle()
                        angle = getAngle()
                        printMainMessage("Time for the fun part! Let's select the color for the gradient!")
                        printMainMessage("For selecting your color, use this Google link and use the Hex value.")
                        printMainMessage("https://www.google.com/search?q=color+picker")
                        printMainMessage("Then, when you're done, type \"exit\"!")
                        colors = []
                        def addColor():
                            r = OrangeAPI.requestInput("Enter the Color HEX Value here:", "> ")
                            if bool(re.fullmatch(r'#(?:[0-9a-fA-F]{3}){1,2}$', r.strip())):
                                printDebugMessage(f"Validated Color!: {r}")
                                colors.append(r)
                                return addColor()
                            elif r.lower() == "exit": return
                            else:
                                printErrorMessage("Please try again!")
                                return addColor()
                        addColor()
                        printMainMessage("Now for some configurations!")
                        printMainMessage("Select the types of ui to color! (y/n)")
                        all_optional_enabled = isYes(OrangeAPI.requestInput("All Optional Images (if enabled, every setting below will be enabled unless you say 'n' to one of them)", "> "))
                        emote_wheel_input = OrangeAPI.requestInput("Emote Wheel", "> ")
                        voice_chat_icon_input = OrangeAPI.requestInput("Voice Chat Icons", "> ")
                        menubar_input = OrangeAPI.requestInput("In Game Menu", "> ")
                        topbar_input = OrangeAPI.requestInput("In Game Topbar", "> ")
                        leaderboard_input = OrangeAPI.requestInput("Leaderboard Hover", "> ")
                        dev_console_input = OrangeAPI.requestInput("Developer Console (F9)", "> ")
                        loading_wheel_input = OrangeAPI.requestInput("Loading Wheel", "> ")
                        cursor_input = OrangeAPI.requestInput("Cursors", "> ")
                        selected_file = os.path.join(cur_path, f"{mod_name}_GenerativeConfig.json")
                        def broke_down(s: str=None):
                            if not s: return all_optional_enabled
                            return (True if isYes(s) else (False if isNo(s) else all_optional_enabled))
                        with open(selected_file, "w") as f:
                            json.dump({
                                "name": mod_name,
                                "colors": colors,
                                "angle": angle,
                                "advanced": {
                                    "*": colors,
                                    "_all_optional": all_optional_enabled,
                                    "_voice_chat": broke_down(voice_chat_icon_input),
                                    "_cursor": broke_down(cursor_input),
                                    "_leaderboard": broke_down(leaderboard_input),
                                    "_emotes": broke_down(emote_wheel_input),
                                    "_devconsole": broke_down(dev_console_input),
                                    "_menubar": broke_down(menubar_input),
                                    "_topbar": broke_down(topbar_input),
                                    "_loading": broke_down(loading_wheel_input)
                                }
                            }, f, indent=4)
                        mod_style_file = selected_file
                        OrangeAPI.setConfiguration("ModConfiguration", mod_style_file)
                        printSuccessMessage("Successfully saved Configuration!")
                        printSuccessMessage(f"File Path: {selected_file}")
                    elif a and a == "2":
                        printMainMessage("Please select your Generative Mod Configuration file!")
                        selected_file = getFilePrompt()
                        if os.path.exists(selected_file) and os.path.isfile(selected_file):
                            mod_style_file = selected_file
                            OrangeAPI.setConfiguration("ModConfiguration", mod_style_file)
                            printSuccessMessage(f"Saved selected mod configuration to settings! Path: {mod_style_file}")
                        else: printErrorMessage("No file was given. Disabled Generative Mods.")
                    else:
                        printMainMessage("Please select the Provided Mod Configuration to use.")
                        mod_packs_dir = os.path.join(cur_path, "resources", "mod_packs")
                        provided_mods = os.listdir(mod_packs_dir)
                        configurations = {}
                        for mod in provided_mods:
                            if os.path.isdir(os.path.join(mod_packs_dir, mod)) and os.path.exists(os.path.join(mod_packs_dir, mod, "GenerativeMod.json")):
                                try:
                                    with open(os.path.join(mod_packs_dir, mod, "GenerativeMod.json"), "r", encoding="utf-8") as f:
                                        configurations[mod] = json.load(f)
                                    if not type(configurations[mod]) is dict: configurations.pop(mod)
                                except: pass
                        indexed = {}
                        for i, v in configurations.items():
                            indexed[str(len(indexed) + 1)] = (i, v)
                            de = v.get('description')
                            au = v.get('author')
                            printMainMessage(f"[{len(indexed)}] - {v.get('name') if v.get('name') else i}{f' - {de}' if de else ''}{f' - By {au}' if au else ''}")
                        b = OrangeAPI.requestInput("Enter here:", "> ")
                        if b and indexed.get(b):
                            i, v = indexed.get(b)
                            selected_file = os.path.join(mod_packs_dir, i, "GenerativeMod.json")
                            if os.path.exists(selected_file) and os.path.isfile(selected_file):
                                mod_style_file = selected_file
                                OrangeAPI.setConfiguration("ModConfiguration", mod_style_file)
                                printSuccessMessage(f"Saved selected mod configuration to settings! Path: {mod_style_file}")
                            else: printErrorMessage("No file was given. Disabled Generative Mods.")
                else: printErrorMessage("File was unable to be asked for. Disabled Generative Mods.")
            if not (type(OrangeAPI.getConfiguration("EnabledRobloxStudio")) is bool):
                a = OrangeAPI.requestInput("Would you like to enable mod generation for Roblox Studio too? (y/n)", "> ")
                if a:
                    if isYes(a) == True: OrangeAPI.setConfiguration("EnabledRobloxStudio", True)
                    else: OrangeAPI.setConfiguration("EnabledRobloxStudio", False)
            if OrangeAPI.getConfiguration("EnabledRobloxStudio") == False and studio == True:
                printDebugMessage("Skipped Generating Mods for Roblox Studio due to generation disabled..")
                mod_style_file = None
            if mod_style_file:
                if type(mod_style_file) is str and os.path.isfile(mod_style_file):
                    try:
                        with open(mod_style_file, "r", encoding="utf-8") as f: mod_style_json = json.load(f)
                        if mod_style_json.get("name") and (mod_style_json.get("colors") or mod_style_json.get("advanced")) and mod_style_json.get("angle"):
                            if not (OrangeAPI.getConfiguration(f"LastUpdatedRoblox{'Studio' if studio else ''}") == installed["version"] and OrangeAPI.getConfiguration(f"KlikoModVersion{'Studio' if studio else ''}") == current_version):
                                printMainMessage("Running Proxy using Python Executable..")
                                fold_name = mod_style_json["name"]
                                if studio == True: fold_name = f'{mod_style_json["name"]} [STUDIO]'
                                if mod_style_json.get("advanced"):
                                    resources_folder = os.path.join(cur_path, "resources", mod_style_json["name"])
                                    if not os.path.exists(resources_folder): os.makedirs(resources_folder,mode=511)
                                    def file_extension(s: str): return "." + s.split(".")[-1]
                                    def generate_f(s: str): return os.path.join(resources_folder, f"{s}{file_extension(mod_style_json['advanced'][s])}")
                                    def convert_relative(s: str): return s.replace("./", os.path.dirname(mod_style_file)).replace("{main}", os.path.dirname(mod_style_file))
                                    for i, v in mod_style_json["advanced"].items():
                                        if type(v) is str and os.path.exists(convert_relative(v)): 
                                            if not os.path.exists(os.path.dirname(generate_f(i))): os.makedirs(os.path.dirname(generate_f(i)),mode=511)
                                            shutil.copy(convert_relative(v), generate_f(i)); mod_style_json["advanced"][i] = generate_f(i)
                                res = subprocess.run([sys.executable, os.path.join(cur_path, "GeneratorProxy.py"), json.dumps(installed), json.dumps(mod_style_json), str(studio)])
                                if res.returncode == 0: 
                                    OrangeAPI.setConfiguration(f"LastUpdatedRoblox{'Studio' if studio else ''}", installed["version"])
                                    OrangeAPI.setConfiguration(f"KlikoModVersion{'Studio' if studio else ''}", current_version)
                                    if not OrangeAPI.getIfModIsEnabled(fold_name): OrangeAPI.enableMod(fold_name)
                                    printMainMessage("Repreparing Roblox..")
                                    OrangeAPI.reprepareRoblox()
                                    printSuccessMessage("Proxy has ended with a success!")
                                    OrangeAPI.sendDiscordWebhookMessage("Mod Successfully Built!", f"Your gradient mod \"{mod_style_json.get('name')}\" was successfully built using the Kliko's Mod Tool OrangeBlox extension!", 11468544, [OrangeAPI.DiscordWebhookField("Mod Location", os.path.realpath(os.path.join(cur_path, "..", fold_name)), True), OrangeAPI.DiscordWebhookField("Client Version", installed["version"], True), OrangeAPI.DiscordWebhookField("Client Channel", installed["channel"], True)], "https://cdn.efaz.dev/cdn/png/orange_hammer.png")
                                else:
                                    printErrorMessage("Proxy has ended with an error!")
                                    OrangeAPI.sendDiscordWebhookMessage("Mod Building Failed!", f"Your gradient mod \"{mod_style_json.get('name')}\" was unable to be built using the Kliko's Mod Tool OrangeBlox extension!", 16711680, [OrangeAPI.DiscordWebhookField("Target Mod Location", os.path.realpath(os.path.join(cur_path, "..", fold_name)), True), OrangeAPI.DiscordWebhookField("Client Version", installed["version"], True), OrangeAPI.DiscordWebhookField("Client Channel", installed["channel"], True)], "https://cdn.efaz.dev/cdn/png/orange_error.png")
                            else: printSuccessMessage("No changes are needed as the latest mod generated is installed!")
                        else:
                            printDebugMessage("Mod configuration is invalid!")
                            OrangeAPI.setConfiguration("ModConfiguration", None)
                    except Exception as e:
                        printErrorMessage("Something went wrong!")
                        printDebugMessage(str(e))
                else:
                    printDebugMessage("Mod file is not found.")
                    OrangeAPI.setConfiguration("ModConfiguration", None)
        elif mod_type == 2:
            if not (type(OrangeAPI.getConfiguration("EnabledRobloxStudio")) is bool):
                a = OrangeAPI.requestInput("Would you like to enable mod generation for Roblox Studio too? (y/n)", "> ")
                if a:
                    if isYes(a) == True: OrangeAPI.setConfiguration("EnabledRobloxStudio", True)
                    else: OrangeAPI.setConfiguration("EnabledRobloxStudio", False)
            mod_manifest = OrangeAPI.generateModsManifest()
            if not OrangeAPI.getConfiguration("EnabledMods"):
                if OrangeAPI.getIfRobloxLaunched() == False:
                    def b():
                        enabled_mods = OrangeAPI.getConfiguration("EnabledMods") or []
                        printMainMessage("Please select the Mods to update automatically")
                        co = 0
                        q = {}
                        for _, i in mod_manifest.items():
                            if i.get("name") == "Original": continue
                            if i.get("list_in_normal_mods") == False and i.get("enabled") == False: continue
                            co += 1
                            if type(i.get("name")) is str: final_name = f"{i.get('name')} [{i.get('id')}]"
                            else: final_name = f"{i.get('name')}"
                            printMainMessage(f"[{'✅' if i['id'] in enabled_mods else '❌'}] [{co}] = {final_name}")
                            q[str(co)] = i
                        printMainMessage(f"[exit] = Exit Mod Selector")
                        c = OrangeAPI.requestInput("Enter the response below:", "> ")
                        if q.get(c):
                            mod = q.get(c)
                            if mod['id'] in enabled_mods: enabled_mods.pop(mod['id']); printDebugMessage(f"Removed mod: {mod['id']}")
                            else: enabled_mods.append(mod['id']); printDebugMessage(f"Added mod: {mod['id']}")
                            OrangeAPI.setConfiguration("EnabledMods", enabled_mods)
                            b()
                        elif c == "exit":
                            OrangeAPI.setConfiguration("EnabledMods", enabled_mods)
                            return
                        else:
                            printDebugMessage(f"Invalid response.")
                            b()
                    b()
                else: printErrorMessage("Mod was unable to be asked for. Disabled Generative Mods.")
            enabled_mods = OrangeAPI.getConfiguration("EnabledMods") or []
            verified_mods = []
            for i in enabled_mods:
                if os.path.exists(os.path.join(cur_path, "../", i)):
                    if os.path.exists(os.path.join(cur_path, "../", i, "info.json")): verified_mods.append(os.path.join(cur_path, "../", i))
                    else: printDebugMessage(f"The mod '{i}' is not supported for updating due to a lack of version.")
                else: printDebugMessage(f"Mod doesn't exist! Mod: {i}")
            if OrangeAPI.getConfiguration("EnabledRobloxStudio") == False and studio == True:
                printDebugMessage("Skipped Generating Mods for Roblox Studio due to generation disabled..")
                mod_style_file = None
            if len(verified_mods) > 0:
                try:
                    printMainMessage("Running Proxy using Python Executable..")
                    res = subprocess.run([sys.executable, os.path.join(cur_path, "UpdaterProxy.py"), json.dumps(verified_mods), str(studio), json.dumps(installed)])
                    if res.returncode == 0: 
                        OrangeAPI.setConfiguration(f"LastUpdatedRoblox{'Studio' if studio else ''}", installed["version"])
                        for i in enabled_mods:
                            if not OrangeAPI.getIfModIsEnabled(i): OrangeAPI.enableMod(i)
                        printMainMessage("Repreparing Roblox..")
                        OrangeAPI.reprepareRoblox()
                        printSuccessMessage("Proxy has ended with a success!")
                        OrangeAPI.sendDiscordWebhookMessage("Mods Successfully Updated!", f"Your mods \"{', '.join(verified_mods)}\" was successfully updated using the Kliko's Mod Tool OrangeBlox extension!", 11468544, [OrangeAPI.DiscordWebhookField("Mods Location", os.path.realpath(os.path.join(cur_path, "../")), True), OrangeAPI.DiscordWebhookField("Client Version", installed["version"], True), OrangeAPI.DiscordWebhookField("Client Channel", installed["channel"], True)], "https://cdn.efaz.dev/cdn/png/orange_updating.png")
                    else:
                        printErrorMessage("Proxy has ended with an error!")
                        OrangeAPI.sendDiscordWebhookMessage("Mod Updating Failed!", f"Your mods \"{', '.join(verified_mods)}\" was unable to be updated using the Kliko's Mod Tool OrangeBlox extension!", 16711680, [OrangeAPI.DiscordWebhookField("Target Mods Location", os.path.realpath(os.path.join(cur_path, "../")), True), OrangeAPI.DiscordWebhookField("Client Version", installed["version"], True), OrangeAPI.DiscordWebhookField("Client Channel", installed["channel"], True)], "https://cdn.efaz.dev/cdn/png/orange_error.png")
                except Exception as e:
                    printErrorMessage("Proxy has ended with an error!")
                    printDebugMessage(str(e))
            else:
                printSuccessMessage("No mods are available to update! Resetting configuration..")
                OrangeAPI.setConfiguration("EnabledMods", [])
    else: printDebugMessage("Unable to respond for type of mod action.")