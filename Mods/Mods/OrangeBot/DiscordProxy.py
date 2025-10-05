#
# OrangeBot
# OrangeBlox with Discord Bot Support
# v1.0.0
# 

# Load Bootstrap API
import asyncio
import discord
import datetime
import sys
import logging
import typing
import time
import json
import os
from PIL import ImageGrab
from discord.ext import tasks
from discord import app_commands

try:
    from .... import OrangeAPI as orange
except:
    class orange():
        class OrangeAPI: pass

current_path_location = os.path.dirname(os.path.abspath(__file__))
def askForTask(func, *args, **kwargs):
    randomized = os.urandom(3).hex()
    path = os.path.join(current_path_location, f"OrangeBotTask_{randomized}.json")

    # Start tasking
    with open(path, "w", encoding="utf-8") as f:
        json.dump({
            "func": func,
            "args": args,
            "kwargs": kwargs,
            "mod_id": sys.argv[1]
        }, f, indent=None, separators=(",", ":"))

    # Awaiting loop
    while True:
        try:
            with open(path, "r", encoding="utf-8") as f:
                if f.read().endswith("🙂"): break
        except FileNotFoundError: pass
        time.sleep(0.05)

    # Data processing
    with open(path, "r", encoding="utf-8") as f: file_read = f.read().rstrip("🙂")
    os.remove(path)
    if file_read in ("True", "False", "None"): return eval(file_read)
    if file_read.isnumeric(): return int(file_read)
    try: return json.loads(file_read)
    except json.JSONDecodeError: return file_read

class OrangeAPI2:
    def __getattr__(self, name):
        def method(*args, **kwargs): return askForTask(name, *args, **kwargs)
        return method
OrangeAPI: orange.OrangeAPI = OrangeAPI2()    
debugMode = OrangeAPI.getDebugMode()
apiVersion = OrangeAPI.about()
    
# Printing Functions
def printMainMessage(mes): OrangeAPI.printMainMessage(mes) # White System Console Text
def printErrorMessage(mes): OrangeAPI.printErrorMessage(mes) # Error Colored Console Text
def printSuccessMessage(mes): OrangeAPI.printSuccessMessage(mes) # Success Colored Console Text
def printYellowMessage(mes): OrangeAPI.printYellowMessage(mes) # Yellow Colored Console Text
def printWarnMessage(mes): OrangeAPI.printWarnMessage(mes) # Yellow Colored Console Text
def printDebugMessage(mes): OrangeAPI.printDebugMessage(mes) # Debug Console Text
def ts(text): return OrangeAPI.translate(text)
def isYes(text): return text.lower() == "y" or text.lower() == "yes" or text.lower() == "true" or text.lower() == "t"

# Main Handler
intents = discord.Intents.all()
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)
task_list = {}
task = None

def generateCustomEmbed(title: str, message: str, decimal: int=16730880):
    embed = discord.Embed(color=decimal, title=title, description=message)
    embed.set_footer(
        text="OrangeBot & OrangeBlox",
        icon_url="https://cdn.efaz.dev/png/logo.png",
    )
    embed.timestamp = datetime.datetime.now()
    return embed
def getIfUserIsTrusted(user: typing.Union[discord.User, discord.Member]):
    discord_bot_users = OrangeAPI.getConfiguration("DiscordBotUsers")
    return discord_bot_users and str(user.id) in discord_bot_users

@bot.event
async def on_ready():
    # Bot Information
    printSuccessMessage(f"Logged on the bot: " + bot.user.name)
    printSuccessMessage("System is ready!")

    # Sync Command Tree for first time and mod script updates
    if OrangeAPI.getConfiguration("DiscordBotFirstTime") == True:
        await tree.sync()
        OrangeAPI.setConfiguration("DiscordBotFirstTime", False)
        OrangeAPI.setConfiguration("ModScriptVersion", OrangeAPI.getVersion())
    elif OrangeAPI.getVersion() != OrangeAPI.getConfiguration("ModScriptVersion"):
        await tree.sync()
        OrangeAPI.setConfiguration("ModScriptVersion", OrangeAPI.getVersion())

    status_task.start()
@tasks.loop()
async def status_task():
    while True:
        try:
            current_game_info = OrangeAPI.getCurrentPlaceInfo()
            connected_game_status = OrangeAPI.getIfConnectedToGame()
            if connected_game_status == True:
                place_info = current_game_info["place_info"]
                if place_info['creator']['name'] == "Local File" and place_info['creator']['id'] == 0: creator_name = OrangeAPI.translate(f"Opened as Local File!")
                else:
                    creator_name = OrangeAPI.translate(f"Made by {'@' if place_info['creator'].get('type') == 'User' else ''}{place_info['creator']['name']}").replace("✅", "")
                    if place_info.get("creator").get("hasVerifiedBadge") == True: creator_name = f"{creator_name} ✅!"
                    else: creator_name = f"{creator_name}!"
                await bot.change_presence(status=discord.Status.idle,
                    activity=discord.Activity(
                        type=discord.ActivityType.playing,
                        name=f"Playing {place_info['name']} by {creator_name}"
                    )
                )
            else:
                await bot.change_presence(status=discord.Status.idle,
                    activity=discord.Activity(
                        type=discord.ActivityType.playing,
                        name=f"Idling on Roblox {'Studio' if OrangeAPI.getStudioMode() else 'Player'}"
                    )
                )
        except Exception as e:
            printErrorMessage(f"Error while loading status text! Error: {str(e)}")
        await asyncio.sleep(10)
@tree.command(name="sync", description="Sync command tree to all servers!")
async def sync(interaction: discord.Interaction):
    ctx = interaction
    res = ctx.response
    if getIfUserIsTrusted(ctx.user):
        await asyncio.sleep(0)
        await res.send_message(
            embed=generateCustomEmbed(
                ts("Called!"),
                ts(f"Called Discord API to sync all commands to servers!"),
                16776960
            )
        )
        try:
            await tree.sync()
            await ctx.channel.send(
                content=f"<@{ctx.user.id}>",
                embed=generateCustomEmbed(
                    ts("Success!"),
                    ts(f"Successfully saved tree to Discord API! It may take a moment to progress to all users!"),
                    65280
                ),
            )
        except Exception as e:
            printErrorMessage(str(e))
            await ctx.channel.send(
                content=f"<@{ctx.user.id}>",
                embed=generateCustomEmbed(
                    ts("Failed"),
                    ts(f"Tree failed to be saved by the Discord API. {str(e)}"),
                    16711680
                ),
            )
    else:
        await asyncio.sleep(0)
        await res.send_message(
            embed=generateCustomEmbed(
                ts("Uh oh!"), 
                ts("You do not have access to this command!"), 
                16711680
            )
        )
@tree.command(name="ping", description="Get current bot ping!")
async def ping(ctx: discord.Interaction):
    await asyncio.sleep(0)
    await ctx.response.send_message(
        embed=generateCustomEmbed("Pong!", f"{round(bot.latency * 1000)}ms", 16711680)
    )
@tree.command(name="connectedgame", description="Get connected game info!")
async def connectedgame(interaction: discord.Interaction):
    ctx = interaction
    res = ctx.response
    if getIfUserIsTrusted(ctx.user):
        try:
            await asyncio.sleep(0)
            await res.send_message(
                embed=generateCustomEmbed(
                    ts("Called!"),
                    ts(f"Successfully called task for getting game information! Please wait a moment!"),
                    16776960
                )
            )
            connected_to_game = OrangeAPI.getIfConnectedToGame()
            current_game_info = OrangeAPI.getCurrentPlaceInfo()
            connected_user_info = OrangeAPI.getConnectedUserInfo()
            current_roblox_pid = OrangeAPI.getCurrentRobloxPid()
            current_roblox_vers = OrangeAPI.getInstalledRobloxVersion()
            main_embed = generateCustomEmbed(
                ts("Current Game Information!"),
                ts(f"You are currently inside of a game!") if connected_to_game else ts("You are currently disconnected!"),
                65280 if connected_to_game else 16711680
            )
            main_embed.add_field(name=ts("Connected"), value=str(connected_to_game))
            main_embed.add_field(name=ts("Studio"), value=str(OrangeAPI.getStudioMode()))
            main_embed.add_field(name=ts("Instance PID"), value=current_roblox_pid)
            if current_roblox_vers.get("success") == True:
                main_embed.add_field(name=ts("Roblox Version"), value=f"{current_roblox_vers.get('version')} ({current_roblox_vers.get('channel')}: {current_roblox_vers.get('client_version')})")
            if connected_to_game == True:
                place_info = current_game_info["place_info"]
                server_location = current_game_info.get("server_location", "Unknown Location")
                place_name = place_info.get("name")
                start_time = current_game_info.get("start_time", 1)
                place_id = current_game_info.get("placeId")
                universe_id = current_game_info.get("universeId")
                thumbnail_url = current_game_info.get("thumbnail_url", "https://obx.efaz.dev/Images/AppIcon512.png")
                username = connected_user_info.get("name", "Unknown")
                display_name = connected_user_info.get("display", "Unknown")
                user_id = connected_user_info.get("id", -1)
                user_thumbnail_url = connected_user_info.get("thumbnail", "https://obx.efaz.dev/Images/AppIcon512.png")
                user_connected_text = ts("Unknown User")
                if connected_user_info: user_connected_text = f'[@{username} [{user_id}]](https://www.roblox.com/users/{user_id}/profile)'
                if place_info['creator']['name'] == "Local File" and place_info['creator']['id'] == 0: creator_name = ts(f"Opened as Local File!")
                else:
                    creator_name = ts(f"Made by {'@' if place_info['creator'].get('type') == 'User' else ''}{place_info['creator']['name']}").replace("✅", "")
                    if place_info.get("creator").get("hasVerifiedBadge") == True: creator_name = f"{creator_name} ✅!"
                    else: creator_name = f"{creator_name}!"
                if place_info['creator'].get('type') == 'User':
                    creator_link = f"https://www.roblox.com/users/{place_info['creator'].get('id')}"
                else:
                    creator_link = f"https://www.roblox.com/groups/{place_info['creator'].get('id')}"
                main_embed.set_thumbnail(url=thumbnail_url if thumbnail_url else user_thumbnail_url)
                main_embed.add_field(name=ts("Joined Game"), value=f"[{place_name}](https://www.roblox.com/games/{place_id}) (By [{creator_name}]({creator_link}))")
                main_embed.add_field(name=ts("Started"), value=f"<t:{int(start_time)}:R>")
                main_embed.add_field(name=ts("User Connected"), value=user_connected_text)
                main_embed.add_field(name=ts("Server Location"), value=server_location)
            else:
                roblox_tilt_logo = OrangeAPI.getRobloxThumbnailURL()
                app_settings = OrangeAPI.getRobloxAppSettings()
                main_embed.set_thumbnail(url=roblox_tilt_logo)
                if app_settings.get("success") == True:
                    user_connected_text = ts("Unknown User")
                    user_info = app_settings.get("loggedInUser")
                    if user_info: user_connected_text = f'[@{user_info.get("name")} [{user_info.get("id")}]](https://www.roblox.com/users/{user_info.get("id")}/profile)'
                    main_embed.add_field(name=ts("Logged In User"), value=user_connected_text)
            await ctx.channel.send(
                embed=main_embed
            )
        except Exception as e:
            printErrorMessage(str(e))
            await ctx.channel.send(
                embed=generateCustomEmbed(
                    ts("Uh oh!"),
                    ts(f"Something went wrong! Exception: {str(e)}"),
                    16711680
                ),
            )
    else:
        await asyncio.sleep(0)
        await res.send_message(
            embed=generateCustomEmbed(
                ts("Uh oh!"),
                ts("You do not have access to this command!"), 
                16711680
            )
        )
@tree.command(name="screenshot", description="Get screenshot of computer screen!")
async def screenshot(interaction: discord.Interaction):
    ctx = interaction
    res = ctx.response
    if getIfUserIsTrusted(ctx.user):
        try:
            await asyncio.sleep(0)
            await res.send_message(
                embed=generateCustomEmbed(
                    ts("Called!"),
                    ts(f"Successfully called task for screenshotting your screen! Please wait a moment!"),
                    16776960
                )
            )
            main_embed = generateCustomEmbed(
                ts("Success!"),
                ts(f"Successfully screenshotted screen!"),
                65280
            )
            screenshot = ImageGrab.grab()
            screenshot_path = os.path.join(current_path_location, "screenshot_screen.png")
            screenshot.save(screenshot_path)
            await ctx.channel.send(
                embed=main_embed,
                files=[discord.File(screenshot_path)]
            )
            os.remove(screenshot_path)
        except Exception as e:
            printErrorMessage(str(e))
            await ctx.channel.send(
                embed=generateCustomEmbed(
                    ts("Uh oh!"),
                    ts(f"Something went wrong! Exception: {str(e)}"),
                    16711680
                ),
            )
    else:
        await asyncio.sleep(0)
        await res.send_message(
            embed=generateCustomEmbed(
                ts("Uh oh!"), 
                ts("You do not have access to this command!"), 
                16711680
            )
        )
@tree.command(name="endroblox", description="End the current Roblox instance!")
async def endcurrentroblox(interaction: discord.Interaction):
    ctx = interaction
    res = ctx.response
    if getIfUserIsTrusted(ctx.user):
        try:
            await asyncio.sleep(0)
            if OrangeAPI.getCurrentRobloxPid():
                ores = OrangeAPI.endRoblox(pid=OrangeAPI.getCurrentRobloxPid())
                if ores:
                    main_embed = generateCustomEmbed(
                        ts("Success!"),
                        ts(f"Successfully ended Roblox!"),
                        65280
                    )
                    await res.send_message(
                        embed=main_embed
                    )
                else:
                    await ctx.channel.send(
                        embed=generateCustomEmbed(
                            ts("Uh oh!"),
                            ts(f"Something went wrong!"),
                            16711680
                        ),
                    )
            else:
                await asyncio.sleep(0)
                await res.send_message(
                    embed=generateCustomEmbed(
                        ts("Uh oh!"),
                        ts("Unable to find current Roblox instance!"), 
                        16711680
                    )
                )
        except Exception as e:
            printErrorMessage(str(e))
            await ctx.channel.send(
                embed=generateCustomEmbed(
                    ts("Uh oh!"),
                    ts(f"Something went wrong! Exception: {str(e)}"),
                    16711680
                ),
            )
    else:
        await asyncio.sleep(0)
        await res.send_message(
            embed=generateCustomEmbed(
                ts("Uh oh!"),
                ts("You do not have access to this command!"), 
                16711680
            )
        )
@tree.command(name="focusrbx", description="Force current set Roblox Window!")
async def focusroblox(interaction: discord.Interaction):
    ctx = interaction
    res = ctx.response
    if getIfUserIsTrusted(ctx.user):
        try:
            await asyncio.sleep(0)
            if OrangeAPI.getCurrentRobloxPid():
                ores = OrangeAPI.focusRobloxWindow()
                if ores:
                    main_embed = generateCustomEmbed(
                        ts("Success!"),
                        ts(f"Successfully focused Roblox!"),
                        65280
                    )
                    await res.send_message(
                        embed=main_embed
                    )
                else:
                    await ctx.channel.send(
                        embed=generateCustomEmbed(
                            ts("Uh oh!"),
                            ts(f"Something went wrong!"),
                            16711680
                        ),
                    )
            else:
                await asyncio.sleep(0)
                await res.send_message(
                    embed=generateCustomEmbed(
                        ts("Uh oh!"),
                        ts("Unable to find current Roblox instance!"), 
                        16711680
                    )
                )
        except Exception as e:
            printErrorMessage(str(e))
            await ctx.channel.send(
                embed=generateCustomEmbed(
                    ts("Uh oh!"),
                    ts(f"Something went wrong! Exception: {str(e)}"),
                    16711680
                ),
            )
    else:
        await asyncio.sleep(0)
        await res.send_message(
            embed=generateCustomEmbed(
                ts("Uh oh!"),
                ts("You do not have access to this command!"), 
                16711680
            )
        )
@tree.command(name="moverbx", description="Move and resize Roblox Window")
async def moveroblox(interaction: discord.Interaction, sizex: int, sizey: int, posx: int, posy: int):
    ctx = interaction
    res = ctx.response
    if getIfUserIsTrusted(ctx.user):
        try:
            await asyncio.sleep(0)
            if OrangeAPI.getCurrentRobloxPid():
                ores = OrangeAPI.changeRobloxWindowSizeAndPosition(sizex, sizey, posx, posy)
                if ores:
                    main_embed = generateCustomEmbed(
                        ts("Success!"),
                        ts(f"Successfully moved and resized Roblox Window!"),
                        65280
                    )
                    await res.send_message(
                        embed=main_embed
                    )
                else:
                    await ctx.channel.send(
                        embed=generateCustomEmbed(
                            ts("Uh oh!"),
                            ts(f"Something went wrong!"),
                            16711680
                        ),
                    )
            else:
                await asyncio.sleep(0)
                await res.send_message(
                    embed=generateCustomEmbed(
                        ts("Uh oh!"),
                        ts("Unable to find current Roblox instance!"), 
                        16711680
                    )
                )
        except Exception as e:
            printErrorMessage(str(e))
            await ctx.channel.send(
                embed=generateCustomEmbed(
                    ts("Uh oh!"),
                    ts(f"Something went wrong! Exception: {str(e)}"),
                    16711680
                ),
            )
    else:
        await asyncio.sleep(0)
        await res.send_message(
            embed=generateCustomEmbed(
                ts("Uh oh!"),
                ts("You do not have access to this command!"), 
                16711680
            )
        )
def startDiscordBot():
    try:
        if OrangeAPI.getConfiguration("DiscordBotEnabled") == True:
            bot.run(
                OrangeAPI.getConfiguration("DiscordBotToken"),
                reconnect=True,
                log_level=logging.CRITICAL
            )
    except Exception as e:
        printMainMessage(f"Error launching discord bot. Error: {str(e)}")

# Start Discord Bot
startDiscordBot()