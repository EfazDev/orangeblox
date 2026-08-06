#
# OrangeBot
# OrangeBlox with Discord Bot Support
# v1.1.0
# 

# Load Bootstrap API
import OrangeAPI as orange; OrangeAPI = orange.OrangeAPI()
import subprocess
import threading
import discord
import uuid
import time
import sys
import os
current_path_location = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_path_location)
from Socket import Socket
debugMode = OrangeAPI.getDebugMode()
apiVersion = OrangeAPI.about()
    
# Printing Functions
def printMainMessage(mes): OrangeAPI.printMainMessage(mes) # White System Console Text
def printErrorMessage(mes): OrangeAPI.printErrorMessage(mes) # Error Colored Console Text
def printSuccessMessage(mes): OrangeAPI.printSuccessMessage(mes) # Success Colored Console Text
def printYellowMessage(mes): OrangeAPI.printYellowMessage(mes) # Yellow Colored Console Text
def printWarnMessage(mes): OrangeAPI.printWarnMessage(mes) # Yellow Colored Console Text
def printDebugMessage(mes): OrangeAPI.printDebugMessage(mes) # Debug Console Text
def isYes(text): return text.lower() in {"y", "yes", "true", "t"}
def ts(text): return OrangeAPI.translate(text)

# Main Handler
mod_id = str(uuid.uuid4())
discord_thread = None
ms_socket = Socket(port=61243)

# Setup
printWarnMessage("--- OrangeBot Setup ---")
printWarnMessage(f"Debug Mode: {debugMode}")
printWarnMessage(f"Discord API Version: {discord.__version__}")
printWarnMessage(f"OrangeAPI Version: {apiVersion.get('api_version')}")
printWarnMessage("-----------------------")
if OrangeAPI.getConfiguration("DiscordBotEnabled") == None and not OrangeAPI.getIfRobloxLaunched():
    printMainMessage(f"Hello! It seems like it's your first time with setting up OrangeBot!")
    printMainMessage("Please select the tutorial mode you would like to use!")
    printMainMessage("[1] = Starters")
    printMainMessage("[2] = Advanced (Skip)")
    tutorial_mode = OrangeAPI.requestInput(ts("Input tutorial mode:"))
    if tutorial_mode:
        tutorial_mode = tutorial_mode.lower()
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

def handling_task(data):
    task_key = data.get("task_key")
    func_name = data.get("func")
    args = data.get("args", [])
    kwargs = data.get("kwargs", {})
    if task_key != mod_id: return None
    if func_name == "check_api_status": res = True
    else:
        res = None
        try: res = getattr(OrangeAPI, func_name)(*args, **kwargs)
        except Exception:  res = False
    if OrangeAPI.checkIfResponseClass(res):  formatted_res = res.success
    elif isinstance(res, dict):  formatted_res = res
    else: formatted_res = str(res)
    return formatted_res
def run_handling():
    ms_socket.subscribe("task", handling_task)
    ms_socket.listen()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt: ms_socket.close()
def clean_up_tasks():
    for file in os.listdir(current_path_location):
        if file.startswith("OrangeBotTask_"):
            try:
                os.remove(os.path.join(current_path_location, file))
            except Exception:
                pass
def run_discord_proxy():
    global discord_thread
    printMainMessage("Starting discord.py proxy!")
    discord_thread = subprocess.Popen([sys.executable, os.path.join(current_path_location, "DiscordProxy.py"), mod_id], creationflags=subprocess.CREATE_NO_WINDOW if OrangeAPI.getPlatform() == "Windows" else 0)
    returncode = discord_thread.wait()
    if returncode == 0 or returncode == -15:
        printSuccessMessage("Discord Proxy ended with success!")
    else:
        printErrorMessage(f"Discord Proxy ended with fail! Return code: {returncode}")
def full_start():
    clean_up_tasks()
    threading.Thread(target=run_handling, daemon=True).start()
    time.sleep(1)
    threading.Thread(target=run_discord_proxy, daemon=True).start()

# Start Discord Bot
if OrangeAPI.getConfiguration("DiscordBotEnabled") == True:
    def start():
        taken = OrangeAPI.createAppLock("BotLock")
        if taken: full_start()
        else:
            while True:
                taken = OrangeAPI.createAppLock("BotLock")
                if taken:
                    full_start()
                    break
                time.sleep(10)
    threading.Thread(target=start, daemon=True).start()