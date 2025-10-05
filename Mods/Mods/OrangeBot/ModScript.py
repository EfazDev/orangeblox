#
# OrangeBot
# OrangeBlox with Discord Bot Support
# v1.0.0
# 

# Load Bootstrap API
import OrangeAPI as orange; OrangeAPI = orange.OrangeAPI()
import traceback
import tempfile
import subprocess
import threading
import discord
import json
import uuid
import time
import sys
import os
debugMode = OrangeAPI.getDebugMode()
apiVersion = OrangeAPI.about()
    
# Printing Functions
def printMainMessage(mes): OrangeAPI.printMainMessage(mes) # White System Console Text
def printErrorMessage(mes): OrangeAPI.printErrorMessage(mes) # Error Colored Console Text
def printSuccessMessage(mes): OrangeAPI.printSuccessMessage(mes) # Success Colored Console Text
def printYellowMessage(mes): OrangeAPI.printYellowMessage(mes) # Yellow Colored Console Text
def printWarnMessage(mes): OrangeAPI.printWarnMessage(mes) # Yellow Colored Console Text
def printDebugMessage(mes): OrangeAPI.printDebugMessage(mes) # Debug Console Text
def isYes(text): return text.lower() == "y" or text.lower() == "yes" or text.lower() == "true" or text.lower() == "t"
def ts(text): return OrangeAPI.translate(text)

# Main Handler
current_path_location = os.path.dirname(os.path.abspath(__file__))
mod_id = str(uuid.uuid4())

# Setup
printWarnMessage("--- OrangeBot Setup ---")
printWarnMessage(f"Debug Mode: {debugMode}")
printWarnMessage(f"Discord API Version: {discord.__version__}")
printWarnMessage(f"OrangeAPI Version: {apiVersion.get("api_version")}")
printWarnMessage("-----------------------")
if OrangeAPI.getConfiguration("DiscordBotEnabled") == None and not OrangeAPI.getIfRobloxLaunched():
    printMainMessage(f"Hello! It seems like it's your first time with setting up OrangeBot!")
    printMainMessage("Please select the tutorial mode you would like to use!")
    printMainMessage("[1] = Starters")
    printMainMessage("[2] = Advanced (Skip)")
    tutorial_mode = OrangeAPI.requestInput(ts("Input tutorial mode:")).lower()
    if tutorial_mode == "1":
        printMainMessage("1. Alright, so, start with going to your browser!")
        OrangeAPI.requestInput("This can be any browser such as Google Chrome, Firefox or Microsoft Edge.")
        OrangeAPI.requestInput("2. Next, type this link in the URL tab and login to your discord account. (THIS IS THE REAL DISCORD) \nhttps://discord.com/developers/applications")
        OrangeAPI.requestInput("3. Next up, once the page is loaded and you've logged in, press the New Application button in the top right.\nThis will put up a prompt for a name, feel free to put any name you like!")
        OrangeAPI.requestInput("4. This will pull up the Application page. Go to the Bot tab and set the username of your choice and enable ALL intents!\nAlso, please press Reset Token to get the bot token. This is going to be important later!")
        OrangeAPI.requestInput("5. We are now gonna add your bot to your Discord Server. Go to the OAuth2 tab and select \"bot\" and \"Administrator\" as the scopes and permissions. \nThen, take the generated link at the bottom of the page and put it in the URL tab of your webbrowser.")
        OrangeAPI.requestInput("6. Finally, add the bot to your Discord Server and you may continue on to this installation!\nHave a great day!")
    discord_token = OrangeAPI.requestInput(ts("Please input your Discord Bot Token below (https://discord.com/developers/applications):"))
    if discord_token and len(discord_token) > 50:
        printSuccessMessage("Successfully set Discord Bot Token in settings!")
        OrangeAPI.setConfiguration("DiscordBotEnabled", True)
        OrangeAPI.setConfiguration("DiscordBotToken", discord_token)
    if OrangeAPI.getConfiguration("DiscordBotEnabled") == True and not OrangeAPI.getIfRobloxLaunched():
        printMainMessage("Let's now add what users to trust!")
        printMainMessage("Please enable developer mode in your Discord Client and right click on the user to get a user id!")
        printMainMessage("And, for multiple users, separate by ONLY one comma between each id. (No spaces!!)")
        discord_users = OrangeAPI.requestInput(ts("Please input the Discord User IDs to trust:"))
        if discord_users:
            discord_users = discord_users.split(",")
            OrangeAPI.setConfiguration("DiscordBotUsers", discord_users)
    printMainMessage(f"If you want to reset this setup, please reset the configuration in Mod Script Settings.")
    OrangeAPI.setConfiguration("DiscordBotFirstTime", True)

def run_handling():
    handled = []
    while True:
        try:
            for file in os.listdir(current_path_location):
                full_path = os.path.join(current_path_location, file)
                if not file.startswith("OrangeBotTask_") or file in handled: continue

                # Read Task
                try:
                    with open(full_path, "r", encoding="utf-8") as f: content = f.read()
                except Exception: continue

                # Already Handled
                if content.endswith("🙂"):
                    handled.append(file)
                    continue

                # Content Validation
                try: task = json.loads(content)
                except json.JSONDecodeError: continue
                if not (type(task) is dict) or task.get("mod_id") != mod_id: continue

                # Arguments
                func_name = task.get("func")
                args = task.get("args", [])
                kwargs = task.get("kwargs", {})

                # Execute Function
                res = None
                try:
                    res = getattr(OrangeAPI, func_name)(*args, **kwargs)
                except Exception:
                    traceback.print_exc()
                    res = False

                # Write Result
                try:
                    with open(full_path, "w", encoding="utf-8") as f:
                        if OrangeAPI.checkIfResponseClass(res): f.write(f"{res.success}🙂")
                        elif type(res) is dict:
                            json.dump(res, f, separators=(",", ":"))
                            f.write("🙂")
                        else: f.write(f"{res}🙂")
                except Exception: traceback.print_exc()
                handled.append(file)
        except Exception: traceback.print_exc()
        time.sleep(0.05)
def run_discord_proxy():
    printMainMessage("Starting discord.py proxy!")
    s = subprocess.run([sys.executable, os.path.join(current_path_location, "DiscordProxy.py"), mod_id])
    if s.returncode == 0:
        printSuccessMessage("Discord Proxy ended with success!")
    else:
        printErrorMessage(f"Discord Proxy ended with fail! Return code: {s.returncode}")

# Start Discord Bot
if OrangeAPI.getConfiguration("DiscordBotEnabled") == True:
    def start():
        taken = OrangeAPI.createAppLock("BotLock")
        if taken:
            threading.Thread(target=run_discord_proxy, daemon=True).start()
            run_handling()
        else:
            while True:
                taken = OrangeAPI.createAppLock("BotLock")
                if taken:
                    threading.Thread(target=run_discord_proxy, daemon=True).start()
                    run_handling()
                    break
                time.sleep(10)
    threading.Thread(target=start, daemon=True).start()