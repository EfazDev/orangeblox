#
# Hello there! Welcome to Mod Scripts!
# Mod Scripts are Python scripts that you can make to run code like configuring your Roblox experience and sending a notification for when you got something in a game!
# If you're a python developer, you may be able to get started here!
# If you're a person who would like to run multiple mods, you'll only be able to run 1 script at a time due to security, so choose wisely!
# 

# Load Bootstrap API
import OrangeAPI as orange; OrangeAPI = orange.OrangeAPI()
debugMode = OrangeAPI.getDebugMode()
apiVersion = OrangeAPI.about()
    
# Printing Functions
def printMainMessage(mes): OrangeAPI.printMainMessage(mes) # White System Console Text
def printErrorMessage(mes): OrangeAPI.printErrorMessage(mes) # Error Colored Console Text
def printSuccessMessage(mes): OrangeAPI.printSuccessMessage(mes) # Success Colored Console Text
def printYellowMessage(mes): OrangeAPI.printWarnMessage(mes) # Yellow Colored Console Text
def printWarnMessage(mes): OrangeAPI.printWarnMessage(mes) # Yellow Colored Console Text
def printDebugMessage(mes): OrangeAPI.printDebugMessage(mes) # Debug Console Text
def isYes(text): return text.lower() == "y" or text.lower() == "yes" or text.lower() == "true" or text.lower() == "t"

# Main Handler
def onRobloxAppStart(data):
    template_count = OrangeAPI.getConfiguration("template_count")
    if not template_count: template_count = 0
    template_count += 1
    OrangeAPI.setConfiguration("template_count", template_count)
    printWarnMessage("--- Template ---")
    printMainMessage("Hello there!")
    printMainMessage("This is a template mod script here!")
    printMainMessage("This is ran when Roblox opened earlier.")
    printMainMessage("If you know python, try editing this script from the Template Mod folder and installing through Install.py!")
    printDebugMessage(f"You can only see this if you're in debug mode! Template Mod Script has ran {template_count} times!")
    printYellowMessage("However, please do rename the Template folder to a new name to prevent updating from new OrangeBlox updates!")
    printWarnMessage("--- Template ---")
def onRobloxCrash(data):
    printMainMessage("Oof! Roblox crashed!")
def onBloxstrapSDK(data):
    printMainMessage("Bloxstrap SDK requested!")
def onRobloxPassedUpdate(data):
    printSuccessMessage("Woo hoo! Roblox passed the update check!")
def onGameDisconnected(data):
    printErrorMessage("The template script detected the game disconnect. :(")
def onGameJoined(data):
    printSuccessMessage("Woo hoo! The template script detected you joined a game!")