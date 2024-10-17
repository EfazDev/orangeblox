import os
import platform
import json
import subprocess
import time
import datetime
import threading
import re

main_os = platform.system()
efaz_bootstrap_mode = False

# If your Roblox installation is inside of an another folder or on an extra hard drive, you may edit the following here.
macOS_dir = "/Applications/Roblox.app"
macOS_beforeClientServices = "/Contents/MacOS/"
windows_dir = f"{os.getenv('LOCALAPPDATA')}\\Roblox"
# If your Roblox installation is inside of an another folder or on an extra hard drive, you may edit the following here.

def printMainMessage(mes): print(f"\033[38;5;255m{mes}\033[0m")
def printErrorMessage(mes): print(f"\033[38;5;196m{mes}\033[0m")
def printSuccessMessage(mes): print(f"\033[38;5;82m{mes}\033[0m")
def printWarnMessage(mes): print(f"\033[38;5;202m{mes}\033[0m")
def printYellowMessage(mes): print(f"\033[38;5;226m{mes}\033[0m")
def printDebugMessage(mes): print(f"\033[38;5;226m{mes}\033[0m")
def isYes(text): return text.lower() == "y" or text.lower() == "yes"
def isNo(text): return text.lower() == "n" or text.lower() == "no"
def isRequestClose(text): return text.lower() == "exit" or text.lower() == "exit()"
if os.path.exists("FastFlagConfiguration.json") and os.path.exists("Main.py") and os.path.exists("PipHandler.py"):
    efaz_bootstrap_mode = True
fast_flag_installer_version = "1.4.2"

class pip:
    def install(self, packages: list[str]):
        for i in packages:
            import subprocess
            import sys
            subprocess.check_call([sys.executable, "-m", "pip", "install", i])
    def uninstall(self, packages: list[str]):
        for i in packages:
            import subprocess
            import sys
            subprocess.check_call([sys.executable, "-m", "pip", "uninstall", i])
    def installed(self, packages: list[str]):
        installed = {}
        all_installed = True
        for i in packages:
            import importlib
            try:
                a = importlib.import_module(i)
                if a:
                    installed[i] = True
                else:
                    installed[i] = False
                    all_installed = False
            except Exception as e:
                installed[i] = False
                all_installed = False
        installed["all"] = all_installed
        return installed
    def pythonInstalled(self):
        import platform
        import os
        import subprocess
        import glob
        ma_os = platform.system()
        if ma_os == "Darwin":
            paths = [
                "/usr/local/bin/python*",
                "/Library/Frameworks/Python.framework/Versions/*/bin/python*",
                "~/Library/Python/*/bin/python*"
            ]
            for path_pattern in paths:
                for path in glob.glob(path_pattern):
                    if os.path.isfile(path):
                        return True
            return False
        elif ma_os == "Windows":
            paths = [
                os.path.expandvars(r'%LOCALAPPDATA%\\Programs\\Python\\Python*'),
                os.path.expandvars(r'%LOCALAPPDATA%\\Programs\\Python\\Python*\\python.exe'),
                os.path.expandvars(r'%PROGRAMFILES%\\Python*\\python.exe'),
                os.path.expandvars(r'%PROGRAMFILES(x86)%\\Python*\\python.exe')
            ]
            for path_pattern in paths:
                for path in glob.glob(path_pattern):
                    if os.path.isfile(path):
                        return True
            return False
    def pythonInstall(self):
        import platform
        import requests
        import subprocess
        import tempfile

        ma_os = platform.system()
        if ma_os == "Darwin":
            url = "https://www.python.org/ftp/python/3.12.5/python-3.12.5-macos11.pkg"
            response = requests.get(url)
            
            if response.status_code == 200:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pkg") as pkg_file:
                    pkg_file.write(response.content)
                    pkg_file_path = pkg_file.name
                subprocess.run(["open", pkg_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                print(f"Python installer has been executed: {pkg_file_path}")
            else:
                print("Failed to download Python installer.")
        elif ma_os == "Windows":
            url = "https://www.python.org/ftp/python/3.12.5/python-3.12.5-amd64.exe"
            response = requests.get(url)
            
            if response.status_code == 200:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".exe") as exe_file:
                    exe_file.write(response.content)
                    exe_file_path = exe_file.name
                subprocess.run([exe_file_path], check=True)
                print(f"Python installer has been executed: {exe_file_path}")
            else:
                print("Failed to download Python installer.")
class Main():
    # System Functions
    def __init__(self):
        self.__main_os__ = main_os
    robloxInstanceEventNames = [
        "onRobloxExit", 
        "onRobloxLog",
        "onRobloxAppStart", 
        "onRobloxPassedUpdate", 
        "onBloxstrapSDK", 
        "onLoadedFFlags", 
        "onGameUDMUXLoaded", 
        "onHttpResponse", 
        "onOtherRobloxLog",
        "onRobloxCrash",
        "onRobloxTerminateInstance",
        "onGameStart", 
        "onGameLoading", 
        "onGameLoadingNormal", 
        "onGameLoadingPrivate", 
        "onGameLoadingReserved", 
        "onGameLoadingParty", 
        "onGameTeleport", 
        "onGameTeleportFailed", 
        "onGameJoinInfo", 
        "onGameJoined", 
        "onGameLeaving", 
        "onGameDisconnected"
    ]
    robloxInstanceInfoNames = {
        "onRobloxExit": "Allow detecting when Roblox closes", 
        "onRobloxLog": "Allow detecting every Roblox event",
        "onRobloxAppStart": "Allow detecting when Roblox starts", 
        "onRobloxPassedUpdate": "Allow detecting when Roblox passes update checks", 
        "onBloxstrapSDK": "Allow detecting when BloxstrapRPC is triggered", 
        "onLoadedFFlags": "Allow detecting when FFlags are loaded", 
        "onGameUDMUXLoaded": "Allow detecting when Roblox Server IPs are loaded", 
        "onHttpResponse": "Allow detecting when Roblox HttpResponses are ran", 
        "onOtherRobloxLog": "Allow detecting when Unknown Roblox Handlers are detected",
        "onRobloxCrash": "Allow detecting when Roblox crashes",
        "onRobloxTerminateInstance": "Allow detecting when Roblox closes an extra window.",
        "onGameStart": "Allow getting Job ID, Place ID and Roblox IP", 
        "onGameLoading": "Allow detecting when loading any server", 
        "onGameLoadingNormal": "Allow detecting when loading public server", 
        "onGameLoadingPrivate": "Allow detecting when loading private server", 
        "onGameLoadingReserved": "Allow detecting when loading reserved server", 
        "onGameLoadingParty": "Allow detecting when loading party", 
        "onGameTeleport": "Allow detecting when you teleport places", 
        "onGameTeleportFailed": "Allow detecting when teleporting fails", 
        "onGameJoinInfo": "Allow getting join info for a game", 
        "onGameJoined": "Allow detecting when Roblox loads a game fully", 
        "onGameLeaving": "Allow detecting when you leave a game", 
        "onGameDisconnected": "Allow detecting when you disconnect from a game",

        # Efaz's Roblox Bootstrap Permissions
        "fastFlagConfiguration": "Edit or view your bootstrap configuration file",
        "editMainExecutable": "Edit the main bootstrap executable",
        "editModScript": "Edit ModScript.py executable",
        "notifications": "Configure or send macOS Notifications through Bootstrap",
        "configureModModes": "Configure your mod modes",
        "configureRobloxBranding": "Configure your Roblox client's branding",
        "configureDeathSounds": "Configure your death sounds",
        "configureCursors": "Configure your cursors",
        "configureAvatarMaps": "Configure your avatar maps"
    }
    # System Functions 
    class RobloxInstance():
        events = []
        pid = ""
        watchdog_started = False
        ended_process = False
        main_handler = None
        main_log_file = ""
        debug_mode = False
        disconnect_cooldown = False
        requested_end_tracking = False
        disconnect_code_list = {
            "103": "The Roblox experience you are trying to join is currently not available.",
            "256": "Developer has shut down all game servers or game server has shut down for other reasons, please reconnect.",
            "260": "There was a problem receiving data, please reconnect.",
            "261": "Error while receiving data, please reconnect.",
            "262": "There was a problem sending data, please reconnect.",
            "264": "Same account launched experience from different device. Leave the experience from the other device and try again.",
            "266": "Your connection timed out. Check your internet connection and try again.",
            "267": "You were kicked from this experience.",
            "268": "You have been kicked due to unexpected client behavior.",
            "271": "You have been kicked by server, please reconnect.",
            "272": "Lost connection due to an error.",
            "273": "Same account launched experience from different device. Reconnect if you prefer to use this device.",
            "274": "The experience's developer has temporarily shut down the experience server. Please try again.",
            "275": "Roblox has shut down the server for maintenance. Please try again.",
            "277": "Please check your internet connection and try again.",
            "278": "You were disconnected for being idle 20 minutes.",
            "279": "Failed to connect to the Game. (ID = 17: Connection attempt failed.)",
            "280": "Your version of Roblox may be out of date. Please update Roblox and try again.",
            "282": "Disconnected from game, please reconnect.",
            "284": "A fatal error occurred while running this game.",
            "285": "Client/User issued disconnect.",
            "286": "Your device does not have enough memory to run this experience. Exit back to the app.",
            "291": "Player has been removed from the DataModel.",
            "292": "Your device's memory is low. Leaving now will preserve your state and prevent Roblox from crashing.",
            "517": "This game is currently unavailable. Please try again later.",
            "522": "The user you attempted to join has left the game.",
            "523": "The status of the experience has changed and you no longer have access. Please try again later.",
            "524": "You do not have permission to join this experience.",
            "525": "The server is currently busy. Please try again.",
            "528": "Your party is too large to join this experience. Try joining a different experience.",
            "529": "A Http error has occurred. Please close the client and try again.",
            "533": "Your privacy settings prevent you from joining this server.",
            "600": "You were banned from this experience by the creator.",
            "610": "Unable to join game instance.",
            "770": "Game's root place is not active."
        }
        event_names = None
        created_mutex = False

        class __ReadingLineResponse__():
            class EndRoblox(): code=0

        class InvalidRobloxHandlerException(Exception):
            def __init__(self):            
                super().__init__("Please make sure you're providing the RobloxFastFlagsInstaller.Main class!")

        def __init__(self, main_handler, pid: str, log_file: str="", debug_mode: bool=False, allow_other_logs: bool=False, created_mutex=None):
            if type(main_handler) is Main:
                self.main_handler = main_handler
                self.event_names = main_handler.robloxInstanceEventNames
                self.pid = pid
                self.debug_mode = debug_mode
                self.allow_other_logs = allow_other_logs
                self.created_mutex = created_mutex
                if log_file == "" or os.path.exists(log_file):
                    self.main_log_file = log_file
                self.startActivityTracking()
            else:
                raise self.InvalidRobloxHandlerException()
        def awaitRobloxClosing(self):
            while True:
                time.sleep(1)
                if (self.main_handler.getIfRobloxIsOpen(pid=self.pid) == False) or self.requested_end_tracking == True or (self.ended_process == True):
                    self.ended_process = True
                    break
        def setRobloxEventCallback(self, eventName: str, eventCallback):
            if callable(eventCallback):
                if eventName in self.event_names:
                    for i in self.events:
                        if i and i["name"] == eventName: self.events.remove(i)
                    self.events.append({"name": eventName, "callback": eventCallback})
                    if self.watchdog_started == False:
                        self.startActivityTracking()
        def addRobloxEventCallback(self, eventName: str, eventCallback):
            if callable(eventCallback):
                if eventName in self.event_names:
                    self.events.append({"name": eventName, "callback": eventCallback})
                    if self.watchdog_started == False:
                        self.startActivityTracking()
        def clearRobloxEventCallbacks(self, eventName: str=""):
            if eventName == "":
                self.events = []
            else:
                for i in self.events:
                    if i and i["name"] == eventName: self.events.remove(i)
        def requestThreadClosing(self):
            self.requested_end_tracking = True
        def startActivityTracking(self):
            if self.watchdog_started == False:
                self.watchdog_started = True
                def watchDog():
                    time.sleep(0.5)
                    if main_os == "Darwin" or main_os == "Windows":
                        main_log = ""
                        def newest(path):
                            files = os.listdir(path)
                            paths = []
                            for basename in files:
                                if "Player" in basename:
                                    paths.append(os.path.join(path, basename))
                            return max(paths, key=os.path.getctime)

                        def submitToThread(eventName="onUnknownEvent", data=None, isLine=True):
                            if not (eventName == "onRobloxLog"): 
                                submitToThread(eventName="onRobloxLog", data={"eventName": eventName, "data": data, "isLine": isLine}, isLine=False)
                                if isLine == True:
                                    if self.debug_mode == True and not (eventName == "onOtherRobloxLog" and self.allow_other_logs == False): printDebugMessage(f"Event triggered: {eventName}, Line: {data}")
                                else:
                                    if self.debug_mode == True: printDebugMessage(f"Event triggered: {eventName}, Data: {data}")
                            for i in self.events:
                                if i and callable(i.get("callback")) and i.get("name") == eventName: threading.Thread(target=i.get("callback"), args=[data]).start()

                        def handleLine(line=""):
                            if "The crash manager ends the monitor thread at exit." in line or "[FLog::SingleSurfaceApp] destroy controllers" in line:
                                submitToThread(eventName="onRobloxExit", data=line)
                                return self.__ReadingLineResponse__.EndRoblox()
                            elif "[FLog::UpdateController] Update check thread: updateRequired FALSE" in line:
                                submitToThread(eventName="onRobloxPassedUpdate", data=line)
                            elif "[FLog::SingleSurfaceApp] initializeWithAppStarter" in line:
                                submitToThread(eventName="onRobloxAppStart", data=line)
                            elif "[FLog::Output] ! Joining game" in line:
                                def generate_arg():
                                    pattern = r"'([a-f0-9-]+)' place (\d+) at (\d+\.\d+\.\d+\.\d+)"
                                    match = re.search(pattern, line)
                                    if match:
                                        jobId = match.group(1)
                                        placeId = match.group(2)
                                        ip_address = match.group(3)
                                        return {
                                            "jobId": jobId,
                                            "placeId": placeId,
                                            "ip": ip_address
                                        }   
                                    return None
                                
                                generated_data = generate_arg()
                                if generated_data:
                                    submitToThread(eventName="onGameStart", data=generated_data, isLine=False)
                            elif "[FLog::SingleSurfaceApp] launchUGCGameInternal" in line:
                                submitToThread(eventName="onGameLoading", data=line, isLine=True)
                            elif "[FLog::GameJoinUtil] GameJoinUtil::joinGamePostStandard" in line:
                                url_start = line.find("URL: ") + len("URL: ")
                                body_start = line.find("BODY: ")
                                url = line[url_start:body_start].strip()
                                body_json_str = line[body_start + len("BODY: "):].strip()
                                try:
                                    body = json.loads(body_json_str)
                                except json.JSONDecodeError as e:
                                    body = None
                                generated_data = {"url": url, "data": body}
                                if generated_data:
                                    submitToThread(eventName="onGameLoadingNormal", data=generated_data, isLine=False)
                            elif "[FLog::GameJoinUtil] GameJoinUtil::joinGamePostPrivateServer" in line:
                                url_start = line.find("URL: ") + len("URL: ")
                                body_start = line.find("BODY: ")
                                url = line[url_start:body_start].strip()
                                body_json_str = line[body_start + len("BODY: "):].strip()
                                try:
                                    body = json.loads(body_json_str)
                                except json.JSONDecodeError as e:
                                    body = None
                                generated_data = {"url": url, "data": body}
                                if generated_data:
                                    submitToThread(eventName="onGameLoadingPrivate", data=generated_data, isLine=False)
                            elif "[FLog::GameJoinUtil] GameJoinUtil::initiateTeleportToReservedServer" in line:
                                url_start = line.find("URL: ") + len("URL: ")
                                body_start = line.find("Body: ")
                                url = line[url_start:body_start].strip()
                                body_json_str = line[body_start + len("Body: "):].strip()
                                try:
                                    body = json.loads(body_json_str)
                                except json.JSONDecodeError as e:
                                    body = None
                                generated_data = {"url": url, "data": body}
                                if generated_data:
                                    submitToThread(eventName="onGameLoadingReserved", data=generated_data, isLine=False)
                            elif "[FLog::GameJoinUtil] GameJoinUtil::initiateTeleportToParty" in line:
                                url_start = line.find("URL: ") + len("URL: ")
                                body_start = line.find("Body: ")
                                url = line[url_start:body_start].strip()
                                body_json_str = line[body_start + len("Body: "):].strip()
                                try:
                                    body = json.loads(body_json_str)
                                except json.JSONDecodeError as e:
                                    body = None
                                generated_data = {"url": url, "data": body}
                                if generated_data:
                                    submitToThread(eventName="onGameLoadingParty", data=generated_data, isLine=False)
                            elif "[FLog::Output] [BloxstrapRPC]" in line:
                                def generate_arg():
                                    json_start_index = line.find('[BloxstrapRPC]') + len('[BloxstrapRPC] ')
                                    if json_start_index == -1:
                                        return None
                                    json_str = line[json_start_index:].strip()
                                    try:
                                        return json.loads(json_str)
                                    except json.JSONDecodeError as e:
                                        if self.debug_mode == True: printDebugMessage(str(e))
                                        return None
                                generated_data = generate_arg()
                                if generated_data:
                                    submitToThread(eventName="onBloxstrapSDK", data=generated_data, isLine=False)
                            elif "[FLog::Output] LoadClientSettingsFromLocal" in line:
                                submitToThread(eventName="onLoadedFFlags", data=line, isLine=True)
                            elif "[FLog::Network] UDMUX Address = " in line:
                                def generate_arg():
                                    pattern = re.compile(
                                        r'(?P<timestamp>[^\s]+),(?P<unknown_value>[^\s]+),(?P<unknown_hex>[^\s]+),(?P<unknown_number>[^\s]+) \[FLog::Network\] UDMUX Address = (?P<udmux_address>[^\s]+), Port = (?P<udmux_port>[^\s]+) \| RCC Server Address = (?P<rcc_address>[^\s]+), Port = (?P<rcc_port>[^\s]+)'
                                    )
                                    match = pattern.search(line)
                                    if not match:
                                        return None
                                    data = match.groupdict()
                                    result = {
                                        "connected_address": data.get("udmux_address"),
                                        "connected_port": int(data.get("udmux_port")),
                                        "connected_rcc_address": data.get("rcc_address"),
                                        "connected_rcc_port": int(data.get("rcc_port"))
                                    }
                                    return result
                                
                                generated_data = generate_arg()
                                if generated_data:
                                    submitToThread(eventName="onGameUDMUXLoaded", data=generated_data, isLine=False)
                            elif "[FLog::UgcExperienceController] UgcExperienceController: doTeleport: joinScriptUrl" in line:
                                submitToThread(eventName="onGameTeleport", data=line, isLine=True)
                            elif "raiseTeleportInitFailedEvent" in line:
                                submitToThread(eventName="onGameTeleportFailed", data=line, isLine=True)
                            elif "HttpResponse(" in line:
                                def generate_arg():
                                    try:
                                        pattern = re.compile(
                                            r'(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z),'
                                            r'(?P<elapsed_time>\d+\.\d+),'
                                            r'(?P<unknown>\w+),'
                                            r'(?P<unknown2>\d+)\s*\[(?P<log_level>[^\]]+)\]\s*'
                                            r'(?P<http_response>HttpResponse\(#\d+ 0x[\da-fA-F]+\))\s*'
                                            r'time:(?P<response_time>\d+\.\d+)ms\s*\(net:(?P<net_time>\d+\.\d+)ms\s*'
                                            r'callback:(?P<callback_time>\d+\.\d+)ms\s*timeInRetryQueue:(?P<retry_queue_time>\d+\.\d+)ms\)\s*'
                                            r'error:(?P<error_code>\d+)\s*message:(?P<error_message>[^\s]+):\s*(?P<error_details>.+)\s*'
                                            r'ip:\s*external:(?P<external_ip>\d+)\s*'
                                            r'numberOfTimesRetried:(?P<retries>\d+)'
                                        )

                                        match = pattern.match(line)
                                        data = match.groupdict()
                                        if match:
                                            return {
                                                "numberOfTimesRetried": data.get("numberOfTimesRetried"),
                                                "url": re.compile(r'DnsResolve\s+url:\s*\{\s*"(https://[^"]+)"\s*\}').search(data.get("error_details")).group(1),
                                                "error_code": data.get("error_code"),
                                                "callback_time": data.get("callback_time"),
                                                "response_time": data.get("response_time"),
                                                "http_response": data.get("http_response")
                                            }
                                        else:
                                            return None
                                    except Exception as e:
                                        return None
                                    
                                generated_data = generate_arg()
                                if generated_data:
                                    submitToThread(eventName="onHttpResponse", data=generated_data, isLine=False)
                                else:
                                    submitToThread(eventName="onHttpResponse", data=line, isLine=True)
                            elif '"jobId":' in line:
                                import urllib.parse
                                def generate_arg(json_str):
                                    def fix_json_string(json_str):
                                        try:
                                            a = (json_str).replace(" ", "").replace("\n", "")
                                            return json.loads(a)
                                        except Exception as e:
                                            return None
                                        
                                    def extract_ticket_info(ticket):
                                        decoded_ticket = (urllib.parse.unquote(ticket)) + '}'
                                        try:
                                            ticket_json = fix_json_string(decoded_ticket)
                                            if not ticket_json:
                                                raise Exception()
                                            return {
                                                "placeId": ticket_json.get("PlaceId"),
                                                "jobId": ticket_json.get("GameId"),
                                                "username": ticket_json.get("UserName"),
                                                "userId": ticket_json.get("UserId"),
                                                "displayName": ticket_json.get("DisplayName"),
                                                "universeId": ticket_json.get("UniverseId"),
                                                "isTeleport": ticket_json.get("IsTeleport"),
                                                "followUserId": ticket_json.get("FollowUserId")
                                            }
                                        except Exception as e:
                                            decoded_ticket = (urllib.parse.unquote(ticket)) + '"}'
                                            try:
                                                ticket_json = fix_json_string(decoded_ticket)
                                                if not ticket_json:
                                                    raise Exception()
                                                return {
                                                    "placeId": ticket_json.get("PlaceId"),
                                                    "jobId": ticket_json.get("GameId"),
                                                    "username": ticket_json.get("UserName"),
                                                    "userId": ticket_json.get("UserId"),
                                                    "displayName": ticket_json.get("DisplayName"),
                                                    "universeId": ticket_json.get("UniverseId"),
                                                    "isTeleport": ticket_json.get("IsTeleport"),
                                                    "followUserId": ticket_json.get("FollowUserId")
                                                }
                                            except Exception as e:
                                                try:
                                                    decoded_ticket = (urllib.parse.unquote(ticket)) + '""}'
                                                    ticket_json = fix_json_string(decoded_ticket)
                                                    if not ticket_json:
                                                        raise Exception()
                                                    return {
                                                        "placeId": ticket_json.get("PlaceId"),
                                                        "jobId": ticket_json.get("GameId"),
                                                        "username": ticket_json.get("UserName"),
                                                        "userId": ticket_json.get("UserId"),
                                                        "displayName": ticket_json.get("DisplayName"),
                                                        "universeId": ticket_json.get("UniverseId"),
                                                        "isTeleport": ticket_json.get("IsTeleport"),
                                                        "followUserId": ticket_json.get("FollowUserId")
                                                    }
                                                except Exception as e:
                                                    try:
                                                        decoded_ticket = (urllib.parse.unquote(ticket)) + ':""}'
                                                        ticket_json = fix_json_string(decoded_ticket)
                                                        if not ticket_json:
                                                            raise Exception()
                                                        return {
                                                            "placeId": ticket_json.get("PlaceId"),
                                                            "jobId": ticket_json.get("GameId"),
                                                            "username": ticket_json.get("UserName"),
                                                            "userId": ticket_json.get("UserId"),
                                                            "displayName": ticket_json.get("DisplayName"),
                                                            "universeId": ticket_json.get("UniverseId"),
                                                            "isTeleport": ticket_json.get("IsTeleport"),
                                                            "followUserId": ticket_json.get("FollowUserId")
                                                        }
                                                    except Exception as e:
                                                        return None
                                                
                                    json_str = json_str + '"'
                                    json_obj = fix_json_string(json_str + "}")
                                    if json_obj:
                                        ticket_url = json_obj.get("joinScriptUrl")
                                        if ticket_url:
                                            parsed_url = urllib.parse.urlparse(ticket_url)
                                            query_params = urllib.parse.parse_qs(parsed_url.query)
                                            ticket = query_params.get("ticket", [None])[0]
                                            ticket = ticket.split(',"MatchmakingDecisionId"')[0]
                                            if ticket:
                                                b = extract_ticket_info(ticket)
                                                return b
                                            else:
                                                return json_obj
                                        else:
                                            return {
                                                "placeId": None,
                                                "jobId": json_obj.get("jobId"),
                                                "username": None,
                                                "userId": None,
                                                "displayName": None,
                                                "universeId": None,
                                                "isTeleport": None
                                            }
                                
                                first_try = False
                                try:
                                    json.loads(line)
                                    first_try = True
                                except Exception as e:
                                    first_try = False
                                
                                if first_try == False:
                                    generated_data = generate_arg(line)
                                    if generated_data:
                                        submitToThread(eventName="onGameJoinInfo", data=generated_data, isLine=False)
                            elif "[FLog::Network] serverId:" in line:
                                def generate_arg():
                                    match = re.search(r'serverId:\s*(\d{1,3}(?:\.\d{1,3}){3})\|(\d+)', line)
                                    if match:
                                        ip = match.group(1)
                                        port = int(match.group(2))
                                        return {
                                            "ip": ip,
                                            "port": port
                                        }
                                    else:
                                        return {
                                            "ip": "127.0.0.1",
                                            "port": 443
                                        }
                                    
                                generated_data = generate_arg()
                                if generated_data:
                                    submitToThread(eventName="onGameJoined", data=generated_data, isLine=False)
                            elif "[FLog::SingleSurfaceApp] leaveUGCGameInternal" in line:
                                submitToThread(eventName="onGameLeaving", data=line, isLine=True)
                            elif "RBXCRASH: UnhandledException" in line:
                                submitToThread(eventName="onRobloxCrash", data=line, isLine=True)
                            elif "Roblox::terminateWaiter" in line:
                                submitToThread(eventName="onRobloxTerminateInstance", data=line, isLine=True)
                            elif "[FLog::Network] Sending disconnect with reason" in line:
                                code = line.split(':')[-1].strip()
                                if code and code.isnumeric():
                                    main_code = int(code)
                                    if self.disconnect_cooldown == False:
                                        self.disconnect_cooldown = True
                                        def b():
                                            time.sleep(3)
                                            self.disconnect_cooldown = False
                                        threading.Thread(target=b).start()
                                        code_message = "Unknown"
                                        if self.disconnect_code_list.get(str(main_code)):
                                            code_message = self.disconnect_code_list.get(str(main_code))
                                        submitToThread(eventName="onGameDisconnected", data={"code": main_code, "message": code_message}, isLine=False)
                            elif "[FLog::Output]" in line:
                                def generate_arg():
                                    output = line.find('[FLog::Output]') + len('[FLog::Output] ')
                                    if output == -1:
                                        return None
                                    return line[output:].strip()
                                generated_data = generate_arg()
                                if generated_data:
                                    submitToThread(eventName="onGameLog", data=generated_data, isLine=False)
                            else:
                                submitToThread(eventName="onOtherRobloxLog", data=line, isLine=True)
                        if self.main_log_file == "":
                            if main_os == "Darwin":
                                main_log = newest(f'{os.path.expanduser("~")}/Library/Logs/Roblox/')
                            elif main_os == "Windows":
                                main_log = newest(f'{windows_dir}\\logs\\')
                            else:
                                main_log = newest(f'{os.path.expanduser("~")}/Library/Logs/Roblox/')
                            self.main_log_file = main_log
                        else:
                            main_log = self.main_log_file

                        with open(main_log, "r", encoding="utf-8", errors="ignore") as file:
                            while True:
                                line = file.readline()
                                if self.ended_process == True:
                                    submitToThread(eventName="onRobloxExit", data=line)
                                    return
                                if not line:
                                    break
                                res = handleLine(line)
                                if res and res.code == 0:
                                    break
                            file.seek(0, os.SEEK_END)
                            while True:
                                line = file.readline()
                                if self.ended_process == True:
                                    submitToThread(eventName="onRobloxExit", data=line)
                                    break
                                if not line:
                                    time.sleep(0.01)
                                    continue
                                res = handleLine(line)
                                if res and res.code == 0:
                                    self.ended_process = True
                                    break                                
                threading.Thread(target=watchDog).start()
                threading.Thread(target=self.awaitRobloxClosing).start()
    def printLog(self, m):
        if __name__ == "__main__":
            printMainMessage(m)
        else:
            print(m)
    def readPListFile(self, path):
        if os.path.exists(path) and path.endswith(".plist"):
            import plistlib
            with open(path, "rb") as f:
                plist_data = plistlib.load(f)
            return plist_data
        else:
            return {}
    def writePListFile(self, path, data):
        if path.endswith(".plist"):
            try:
                import plistlib
                with open(path, "wb") as f:
                    plistlib.dump(data, f)
                return {"success": True, "message": "Success!", "data": data}
            except Exception as e:
                return {"success": False, "message": "Something went wrong.", "data": ""}
        else:
            return {"success": False, "message": "Path doesn't end with .plist", "data": path}
    def endRoblox(self):
        if self.getIfRobloxIsOpen():
            if self.__main_os__ == "Darwin":
                os.system("killall -9 RobloxPlayer")
            elif self.__main_os__ == "Windows":
                os.system("taskkill /IM RobloxPlayerBeta.exe /F")
            else:
                self.printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
    def getIfRobloxIsOpen(self, installer=False, pid=""):
        if self.__main_os__ == "Windows":
            process = subprocess.Popen(["tasklist"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif self.__main_os__ == "Darwin":
            process = subprocess.Popen(["ps", "aux"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            self.printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
            return

        output, _ = process.communicate()
        process_list = output.decode("utf-8")

        if pid == "":
            if main_os == "Darwin":
                if installer == False:
                    if process_list.rfind("/RobloxPlayer") == -1:
                        return False
                    else:
                        return True
                else:
                    if process_list.rfind("/RobloxPlayerInstaller") == -1:
                        return False
                    else:
                        return True
            else:
                if installer == False:
                    if process_list.rfind("RobloxPlayerBeta.exe") == -1:
                        return False
                    else:
                        return True
                else:
                    if process_list.rfind("RobloxPlayerInstaller.exe") == -1:
                        return False
                    else:
                        return True
        else:
            if process_list.rfind(pid) == -1:
                return False
            else:
                return True
    def getLatestClientVersion(self, debug=False):
        # Mac: https://clientsettingscdn.roblox.com/v2/client-version/MacPlayer
        # Windows: https://clientsettingscdn.roblox.com/v2/client-version/WindowsPlayer

        try:
            import requests
        except Exception as e:
            printMainMessage("This application is requesting for the latest Roblox version but needs a module. Would you like to install it? (y/n)")
            if isYes(input("> ")) == True:
                pip().install(["requests"])
                import requests
                printSuccessMessage("Successfully installed modules!")
            else:
                printErrorMessage("Returning back to application.")
                return {"success": False, "message": "User rejected need of module."}
            
        if self.__main_os__ == "Darwin":
            if debug == True: printDebugMessage("Sending Request to Roblox Servers..") 
            res = requests.get("https://clientsettingscdn.roblox.com/v2/client-version/MacPlayer")
            if res.ok:
                jso = res.json()
                if jso.get("clientVersionUpload") and jso.get("version"):
                    if debug == True: printDebugMessage(f"{res.text}")
                    return {"success": True, "client_version": jso.get("clientVersionUpload"), "short_version": jso.get("version")}
                else:
                    if debug == True: printDebugMessage(f"Something went wrong: {res.text}")
                    return {"success": False, "message": "Something went wrong."}
            else:
                if debug == True: printDebugMessage(f"Something went wrong: {res.text}")
                return {"success": False, "message": "Something went wrong."}
        elif self.__main_os__ == "Windows":
            if debug == True: printDebugMessage("Sending Request to Roblox Servers..") 
            res = requests.get("https://clientsettingscdn.roblox.com/v2/client-version/WindowsPlayer")
            if res.ok:
                jso = res.json()
                if jso.get("clientVersionUpload") and jso.get("version"):
                    if debug == True: printDebugMessage(f"{res.text}")
                    return {"success": True, "client_version": jso.get("clientVersionUpload"), "short_version": jso.get("version")}
                else:
                    if debug == True: printDebugMessage(f"Something went wrong: {res.text}")
                    return {"success": False, "message": "Something went wrong."}
            else:
                if debug == True: printDebugMessage(f"Something went wrong: {res.text}")
                return {"success": False, "message": "Something went wrong."}
        else:
            self.printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
            return {"success": False, "message": "OS not compatible."}
    def getCurrentClientVersion(self):
        if self.__main_os__ == "Darwin":
            if os.path.exists(f"{macOS_dir}/Contents/Info.plist"):
                read_plist = self.readPListFile(f"{macOS_dir}/Contents/Info.plist")
                if read_plist.get("CFBundleShortVersionString"):
                    return {"success": True, "isClientVersion": False, "version": read_plist["CFBundleShortVersionString"]}
                else:
                    return {"success": False, "message": "Something went wrong."}
            else:
                return {"success": False, "message": "Roblox not installed."}
        elif self.__main_os__ == "Windows":
            res = self.getRobloxInstallFolder()
            if res:
                return {"success": True, "isClientVersion": True, "version": os.path.basename(os.path.dirname(res))}
            else:
                return {"success": False, "message": "Roblox not installed."}
        else:
            self.printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
            return {"success": False, "message": "OS not compatible."}
    def installFastFlagsJSON(self, fastflagJSON: object, askForPerms=False, merge=True, flat=False, endRobloxInstances=True, isBootstrapper=False, debug=False):
        fastFlagFileName = "ClientAppSettings.json"
        if __name__ == "__main__":
            if self.__main_os__ == "Darwin":
                if endRobloxInstances == True:
                    printMainMessage(f"Closing any open Roblox windows..")
                    self.endRoblox()
                if efaz_bootstrap_mode == False:
                    printMainMessage(f"Generating Client Settings Folder..")
                    if not os.path.exists(f"{macOS_dir}{macOS_beforeClientServices}ClientSettings"):
                        os.mkdir(f"{macOS_dir}{macOS_beforeClientServices}ClientSettings")
                        printSuccessMessage(f"Created {macOS_dir}{macOS_beforeClientServices}ClientSettings..")
                    else:
                        printWarnMessage(f"Client Settings is already created. Skipping Folder Creation..")
                printMainMessage(f"Writing {fastFlagFileName}")
                if merge == True:
                    if os.path.exists("FastFlagConfiguration.json"):
                        try:
                            printMainMessage("Reading Previous Configurations..")
                            with open(f"FastFlagConfiguration.json", "r") as f:
                                merge_json = json.loads(f.read())
                            merge_json.update(fastflagJSON)
                            fastflagJSON = merge_json
                        except Exception as e:
                            printErrorMessage(f"Something went wrong while trying to generate a merged JSON: {str(e)}")
                    elif os.path.exists(f"{macOS_dir}{macOS_beforeClientServices}ClientSettings/{fastFlagFileName}"):
                        try:
                            printMainMessage("Reading Previous Client App Settings..")
                            with open(f"{macOS_dir}{macOS_beforeClientServices}ClientSettings/{fastFlagFileName}", "r") as f:
                                merge_json = json.loads(f.read())
                            merge_json.update(fastflagJSON)
                            fastflagJSON = merge_json
                        except Exception as e:
                            printErrorMessage(f"Something went wrong while trying to generate a merged JSON: {str(e)}")
                set_location = f"{macOS_dir}{macOS_beforeClientServices}ClientSettings/{fastFlagFileName}"
                if os.path.exists("FastFlagConfiguration.json"):
                    set_location = "FastFlagConfiguration.json"
                with open(set_location, "w") as f:
                    if flat == True:
                        json.dump(fastflagJSON, f)
                    else:
                        json.dump(fastflagJSON, f, indent=4)
                printSuccessMessage("DONE!")
                if efaz_bootstrap_mode == True:
                    printSuccessMessage("Your fast flags was successfully saved into your Fast Flag Settings!")
                    printSuccessMessage(f"If you like to update your fast flags, go to: {set_location}")
                else:
                    printSuccessMessage("Your fast flags should be installed!")
                    printSuccessMessage("Please know that you'll have to use this script again after every Roblox update/reinstall!")
                    printSuccessMessage(f"If you like to update your fast flags, go to: {set_location}")
                    printSuccessMessage(f"Additionally, if you would like to, you may install Efaz's Roblox Bootstrap on your computer to automatically do this (it's similar to Bloxstrap)")
                    printMainMessage("Would you like to open Roblox? (y/n)")
                    if input("> ").lower() == "y":
                        self.openRoblox()
            elif self.__main_os__ == "Windows":
                printMainMessage(f"Closing any open Roblox windows..")
                self.endRoblox()
                printMainMessage(f"Finding latest Roblox Version..")
                most_recent_roblox_version_dir = self.getRobloxInstallFolder(f"{windows_dir}\\Versions")
                if most_recent_roblox_version_dir:
                    printMainMessage(f"Found version: {most_recent_roblox_version_dir}")
                    if efaz_bootstrap_mode == False:
                        printMainMessage(f"Generating Client Settings Folder..")
                        if not os.path.exists(f"{most_recent_roblox_version_dir}ClientSettings"):
                            os.mkdir(f"{most_recent_roblox_version_dir}ClientSettings")
                            printSuccessMessage(f"Created {most_recent_roblox_version_dir}ClientSettings..")
                        else:
                            printWarnMessage(f"Client Settings is already created. Skipping Folder Creation..")
                    printMainMessage(f"Writing {fastFlagFileName}")
                    if merge == True:
                        if os.path.exists("FastFlagConfiguration.json"):
                            try:
                                printMainMessage("Reading Previous Configurations..")
                                with open(f"FastFlagConfiguration.json", "r") as f:
                                    merge_json = json.loads(f.read())
                                merge_json.update(fastflagJSON)
                                fastflagJSON = merge_json
                            except Exception as e:
                                printErrorMessage(f"Something went wrong while trying to generate a merged JSON: {str(e)}")
                        elif os.path.exists(f"{most_recent_roblox_version_dir}ClientSettings\\{fastFlagFileName}"):
                            try:
                                printMainMessage("Reading Previous Client App Settings..")
                                with open(f"{most_recent_roblox_version_dir}ClientSettings\\{fastFlagFileName}", "r") as f:
                                    merge_json = json.loads(f.read())
                                merge_json.update(fastflagJSON)
                                fastflagJSON = merge_json
                            except Exception as e:
                                printErrorMessage(f"Something went wrong while trying to generate a merged JSON: {str(e)}")
                    
                    set_location = f"{most_recent_roblox_version_dir}ClientSettings\\{fastFlagFileName}"
                    if os.path.exists("FastFlagConfiguration.json"):
                        set_location = "FastFlagConfiguration.json"
                    with open(set_location, "w") as f:
                        if flat == True:
                            json.dump(fastflagJSON, f)
                        else:
                            json.dump(fastflagJSON, f, indent=4)
                    printSuccessMessage("DONE!")
                    if efaz_bootstrap_mode == True:
                        printSuccessMessage("Your fast flags was successfully saved into your Fast Flag Settings!")
                        printSuccessMessage(f"If you like to update your fast flags, go to: {set_location}")
                    else:
                        printSuccessMessage("Your fast flags should be installed!")
                        printSuccessMessage("Please know that you'll have to use this script again after every Roblox update/reinstall! Also, it only shows if you play a game, not in the home menu!")
                        printSuccessMessage(f"If you like to update your fast flags, go to: {set_location}")
                        printMainMessage("Would you like to open Roblox? (y/n)")
                        if input("> ").lower() == "y":
                            self.openRoblox()
                else:
                    printErrorMessage("Roblox couldn't be found.")
            else:
                printErrorMessage("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
        else:
            if askForPerms == True:
                self.printLog("Would you like to continue with the Roblox Fast Flag installation? (y/n)")
                self.printLog("WARNING! This will force-quit any open Roblox windows! Please close them in order to prevent data loss!")
                if not (input("> ").lower() == "y"):
                    self.printLog("Stopped installation..")
                    return
            if self.__main_os__ == "Darwin":
                if endRobloxInstances == True:
                    self.endRoblox()
                    if debug == True: printDebugMessage("Ending Roblox Instances..")
                if not os.path.exists(f"{macOS_dir}{macOS_beforeClientServices}ClientSettings"):
                    os.mkdir(f"{macOS_dir}{macOS_beforeClientServices}ClientSettings")
                    if debug == True: printDebugMessage("Created ClientSettings folder..")
                if merge == True:
                    if os.path.exists(f"{macOS_dir}{macOS_beforeClientServices}ClientSettings/{fastFlagFileName}"):
                        try:
                            with open(f"{macOS_dir}{macOS_beforeClientServices}ClientSettings/{fastFlagFileName}", "r") as f:
                                merge_json = json.loads(f.read())
                            merge_json.update(fastflagJSON)
                            fastflagJSON = merge_json
                            if debug == True: printDebugMessage("Merged JSON.")
                        except Exception as e:
                            self.printLog(f"Something went wrong while trying to generate a merged JSON: {str(e)}")
                with open(f"{macOS_dir}{macOS_beforeClientServices}ClientSettings/{fastFlagFileName}", "w") as f:
                    if flat == True:
                        json.dump(fastflagJSON, f)
                    else:
                        json.dump(fastflagJSON, f, indent=4)
                if debug == True: printDebugMessage(f"Saved {fastFlagFileName}")
            elif self.__main_os__ == "Windows":
                self.endRoblox()
                if debug == True: printDebugMessage("Ending Roblox Instances..")
                most_recent_roblox_version_dir = self.getRobloxInstallFolder(f"{windows_dir}\\Versions")
                if most_recent_roblox_version_dir:
                    if not os.path.exists(f"{most_recent_roblox_version_dir}ClientSettings"):
                        os.mkdir(f"{most_recent_roblox_version_dir}ClientSettings")
                        if debug == True: printDebugMessage("Created ClientSettings folder..")
                    if merge == True:
                        if os.path.exists(f"{most_recent_roblox_version_dir}ClientSettings\\{fastFlagFileName}"):
                            try:
                                with open(f"{most_recent_roblox_version_dir}ClientSettings\\{fastFlagFileName}", "r") as f:
                                    merge_json = json.loads(f.read())
                                merge_json.update(fastflagJSON)
                                fastflagJSON = merge_json
                                if debug == True: printDebugMessage("Merged JSON.")
                            except Exception as e:
                                self.printLog(f"Something went wrong while trying to generate a merged JSON: {str(e)}")
                    with open(f"{most_recent_roblox_version_dir}ClientSettings\\{fastFlagFileName}", "w") as f:
                        if flat == True:
                            json.dump(fastflagJSON, f)
                        else:
                            json.dump(fastflagJSON, f, indent=4)
                    if debug == True: printDebugMessage(f"Saved {fastFlagFileName}")
                else:
                    self.printLog("Roblox couldn't be found.")
            else:
                self.printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
    def getRobloxInstallFolder(self, versions_dir=f"{windows_dir}\\Versions"): # Thanks ChatGPT :)
        if self.__main_os__ == "Windows":
            versions = [os.path.join(versions_dir, folder) for folder in os.listdir(versions_dir) if os.path.isdir(os.path.join(versions_dir, folder))]
            formatted = []
            if not versions:
                return None
            for fold in versions:
                if os.path.isdir(fold):
                    if os.path.exists(f"{fold}\\RobloxPlayerLauncher.exe"):
                        formatted.append(f"{fold}\\")
            if len(formatted) > 0:
                latest_folder = max(formatted, key=os.path.getmtime)
                return latest_folder
            else:
                return None
        elif self.__main_os__ == "Darwin":
            return f"{macOS_dir}/"
        else:
            self.printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
    def getLatestOpenedRobloxPid(self):
        if self.__main_os__ == "Darwin":
            try:
                result = subprocess.run(["ps", "axo", "pid,etime,command"], stdout=subprocess.PIPE, text=True)
                processes = result.stdout
                roblox_lines = [line for line in processes.splitlines() if "RobloxPlayer" in line]
                if not roblox_lines:
                    return None
                def sort_by_etime(line):
                    etime = line.split()[1]
                    parts = etime.split('-') if '-' in etime else [etime]
                    time_parts = parts[-1].split(':')
                    total_seconds = 0
                    if len(parts) > 1:
                        total_seconds += int(parts[0]) * 86400
                    if len(time_parts) == 3:
                        total_seconds += int(time_parts[0]) * 3600
                        total_seconds += int(time_parts[1]) * 60
                        total_seconds += int(time_parts[2])
                    elif len(time_parts) == 2:
                        total_seconds += int(time_parts[0]) * 60
                        total_seconds += int(time_parts[1])
                    return total_seconds
                roblox_lines.sort(key=sort_by_etime)
                latest_process = roblox_lines[0]
                pid = latest_process.split()[0]
                return pid
            except Exception as e:
                printErrorMessage(f"Error occurred while getting Roblox Instance: {e}")
                return None
        elif self.__main_os__ == "Windows":
            try:
                result = subprocess.Popen(["tasklist"], stdout=subprocess.PIPE, text=True)
                processes = result.stdout.read()
                program_lines = [line for line in processes.splitlines() if "RobloxPlayerBeta.exe" in line]
                if not program_lines:
                    return None
                latest_process = program_lines[-1]
                pid = latest_process.split()[1]
                return pid
            except Exception as e:
                printErrorMessage(f"Error occurred while getting Roblox Instance: {e}")
                return None
    def prepareMultiInstance(self, required=False, debug=False, awaitRobloxClosure=True):
        if self.__main_os__ == "Darwin":
            try:
                import posix_ipc
            except Exception as e:
                if required == True:
                    pip().install(["posix-ipc"])
                    import posix_ipc
                else:
                    printMainMessage("This application is requesting for semaphore access but needs a module. Would you like to install it? (y/n)")
                    if isYes(input("> ")) == True:
                        pip().install(["posix-ipc"])
                        import posix_ipc
                        printSuccessMessage("Successfully installed modules!")
                    else:
                        printErrorMessage("Returning back to application.")
                        return {"success": False, "message": "User rejected need of module."}
            try:
                posix_ipc.unlink_semaphore("/RobloxPlayerUniq")
                if debug == True: printDebugMessage(f"Successfully unlinked semaphore to allow Roblox multi instance!")
                return True
            except posix_ipc.ExistentialError:
                if debug == True: printDebugMessage(f"Roblox Single Instance Semaphore does not exist. You may launch Roblox without any problems!")
                return True
        elif self.__main_os__ == "Windows":
            import ctypes
            from ctypes import wintypes
            kernel32 = ctypes.windll.kernel32
            mutex = kernel32.OpenMutexA(0x1F0001, wintypes.BOOL(True), "ROBLOX_singletonMutex")
            if not (mutex == 0): 
                if debug == True: printDebugMessage("Unable to attach to mutex because it's already created by Roblox or by an another script.")
                return False
            else:
                def hold_mutex():
                    mutex = kernel32.CreateMutexW(None, wintypes.BOOL(True), "ROBLOX_singletonMutex")
                    if mutex:
                        try:
                            if awaitRobloxClosure == True:
                                while self.getIfRobloxIsOpen():
                                    time.sleep(1)
                            else:
                                while True:
                                    time.sleep(1)
                        except KeyboardInterrupt:
                            if debug == True: printDebugMessage("Mutex holding was disrupted by an unexpected request.")
                        finally:
                            kernel32.ReleaseMutex(mutex)
                threading.Thread(target=hold_mutex).start()
                return True
        else:
            self.printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
            return False
    def openRoblox(self, forceQuit=False, makeDupe=False, startData="", debug=False, attachInstance=False, allowRobloxOtherLogDebug=False, mainLogFile="") -> "RobloxInstance | None":
        if self.getIfRobloxIsOpen():
            if forceQuit == True:
                self.endRoblox()
                if debug == True: printDebugMessage("Ending Roblox Instances..")
        if self.__main_os__ == "Darwin":
            if makeDupe == True:
                if self.getIfRobloxIsOpen() == True:
                    self.prepareMultiInstance(debug=debug, required=True)
                    com = f"open --new -a '{macOS_dir}{macOS_beforeClientServices}RobloxPlayer' '{startData}'"
                    if debug == True: printDebugMessage("Running Roblox Player Unix Executable..")
                    a = subprocess.run(com, shell=True, check=True)
                    if a.returncode == 0:
                        if attachInstance == True:
                            cur_open_pid = self.getLatestOpenedRobloxPid()
                            start_time = datetime.datetime.now(tz=datetime.UTC).timestamp()
                            test_instance = self.RobloxInstance(self, pid=cur_open_pid, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug)
                            while True:
                                if test_instance.ended_process == True:
                                    break
                                elif start_time+3 < datetime.datetime.now(tz=datetime.UTC).timestamp():
                                    test_instance.requestThreadClosing()
                                    break
                                else:
                                    time.sleep(1)
                            cur_open_pid = self.getLatestOpenedRobloxPid()
                            start_time = datetime.datetime.now(tz=datetime.UTC).timestamp()
                            test_instance = self.RobloxInstance(self, pid=cur_open_pid, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug)
                            while True:
                                if test_instance.ended_process == True:
                                    break
                                elif start_time+3 < datetime.datetime.now(tz=datetime.UTC).timestamp():
                                    test_instance.requestThreadClosing()
                                    break
                                else:
                                    time.sleep(1)
                            if self.getIfRobloxIsOpen() == True:
                                self.prepareMultiInstance(debug=debug, required=True)
                                pid = self.getLatestOpenedRobloxPid()
                                if pid:
                                    if not (mainLogFile == ""):
                                        return self.RobloxInstance(self, pid=pid, log_file=mainLogFile, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug)
                                    else:
                                        return self.RobloxInstance(self, pid=pid, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug)
                else:
                    com = f"open --new -a '{macOS_dir}{macOS_beforeClientServices}RobloxPlayer' '{startData}'"
                    if debug == True: printDebugMessage("Running Roblox Player Unix Executable..")
                    a = subprocess.run(com, shell=True)
                    if a.returncode == 0:
                        if attachInstance == True:
                            time.sleep(2)
                            if self.getIfRobloxIsOpen() == True:
                                pid = self.getLatestOpenedRobloxPid()
                                if pid:
                                    if not (mainLogFile == ""):
                                        return self.RobloxInstance(self, pid=pid, log_file=mainLogFile, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug)
                                    else:
                                        return self.RobloxInstance(self, pid=pid, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug)
            else:
                if debug == True: printDebugMessage("Running Roblox.app..")
                a = subprocess.run(f"open -a {macOS_dir} '{startData}'", shell=True)
                if a.returncode == 0:
                    if attachInstance == True:
                        time.sleep(2)
                        if self.getIfRobloxIsOpen() == True:
                            pid = self.getLatestOpenedRobloxPid()
                            if pid:
                                if not (mainLogFile == ""):
                                    return self.RobloxInstance(self, pid=pid, log_file=mainLogFile, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug)
                                else:
                                    return self.RobloxInstance(self, pid=pid, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug)
        elif self.__main_os__ == "Windows":
            created_mutex = False
            if not self.getIfRobloxIsOpen():
                if makeDupe == True:
                   created_mutex = self.prepareMultiInstance(debug=debug)
            most_recent_roblox_version_dir = self.getRobloxInstallFolder(f"{windows_dir}\\Versions")
            if most_recent_roblox_version_dir:
                if debug == True: printDebugMessage("Running RobloxPlayerBeta.exe..")
                if startData == "":
                    subprocess.Popen(f"{most_recent_roblox_version_dir}RobloxPlayerBeta.exe", shell=True)
                else:
                    subprocess.Popen(f"{most_recent_roblox_version_dir}RobloxPlayerBeta.exe {startData}", shell=True)
                if attachInstance == True:
                    time.sleep(2)
                    if self.getIfRobloxIsOpen() == True:
                        pid = self.getLatestOpenedRobloxPid()
                        if pid:
                            if not (mainLogFile == ""):
                                return self.RobloxInstance(self, pid=pid, log_file=mainLogFile, debug_mode=debug, created_mutex=created_mutex)
                            else:
                                return self.RobloxInstance(self, pid=pid, debug_mode=debug, created_mutex=created_mutex)
            else:
                self.printLog("Roblox couldn't be found.")
        else:
            self.printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
    def installRoblox(self, forceQuit=True, debug=False, disableRobloxAutoOpen=True):
        if self.getIfRobloxIsOpen():
            if forceQuit == True:
                self.endRoblox()
                if debug == True: printDebugMessage("Ending Roblox Instances..")
        def waitForRobloxEnd():
            if disableRobloxAutoOpen == True:
                if self.getIfRobloxIsOpen():
                    self.endRoblox()
                    return
                time.sleep(1)
                if self.getIfRobloxIsOpen():
                    self.endRoblox()
                    return
                time.sleep(1)
                if self.getIfRobloxIsOpen():
                    self.endRoblox()
                    return
                time.sleep(1)
                if self.getIfRobloxIsOpen():
                    self.endRoblox()
                    return
        if self.__main_os__ == "Darwin":
            if self.getIfRobloxIsOpen(installer=True):
                if debug == True: printDebugMessage("Installer is already opened. Waiting for installation to end..")
                while True:
                    if not self.getIfRobloxIsOpen(installer=True):
                        break
                    else:
                        time.sleep(1)
                
                threading.Thread(target=waitForRobloxEnd).start()
            else:
                if debug == True: printDebugMessage("Running RobloxPlayerInstaller.app..")
                subprocess.run([f"{macOS_dir}{macOS_beforeClientServices}RobloxPlayerInstaller.app/Contents/MacOS/RobloxPlayerInstaller"], shell=True)
                threading.Thread(target=waitForRobloxEnd).start()
                
        elif self.__main_os__ == "Windows":
            most_recent_roblox_version_dir = self.getRobloxInstallFolder(f"{windows_dir}\\Versions")
            if most_recent_roblox_version_dir:
                if self.getIfRobloxIsOpen(installer=True):
                    if debug == True: printDebugMessage("Installer is already opened. Waiting for installation to end..")
                    while True:
                        if not self.getIfRobloxIsOpen(installer=True):
                            break
                        else:
                            time.sleep(1)
                    threading.Thread(target=waitForRobloxEnd).start()
                else:
                    if debug == True: printDebugMessage("Running RobloxPlayerInstaller.exe..")
                    os.system(f"start {most_recent_roblox_version_dir}RobloxPlayerInstaller.exe")
                    while True:
                        if not self.getIfRobloxIsOpen(installer=True):
                            break
                        else:
                            time.sleep(1)
                    threading.Thread(target=waitForRobloxEnd).start()
            else:
                self.printLog("Roblox Installer couldn't be found.")
        else:
            self.printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")

if __name__ == "__main__":
    if efaz_bootstrap_mode == False:
        os.system("cls" if os.name == "nt" else 'echo "\033c\033[3J"; clear')
        if main_os == "Windows":
            printWarnMessage("-----------")
            printWarnMessage("Welcome to Roblox Fast Flags Installer!")
        elif main_os == "Darwin":
            printWarnMessage("-----------")
            printWarnMessage("Welcome to Roblox Fast Flags Installer!")
        else:
            printErrorMessage("Please run this script on macOS/Windows.")
            exit()
        printWarnMessage("Made by Efaz from efaz.dev!")
        printWarnMessage(f"v{fast_flag_installer_version}")
        printWarnMessage("-----------")
    else:
        if main_os == "Windows":
            printWarnMessage(f"Starting Roblox Fast Flags Installer v{fast_flag_installer_version}!")
        elif main_os == "Darwin":
            printWarnMessage(f"Starting Roblox Fast Flags Installer v{fast_flag_installer_version}!")
        else:
            printErrorMessage("Please run this script on macOS/Windows.")
            exit()
    if main_os == "Windows":
        if not os.path.exists(windows_dir):
            printErrorMessage("The Roblox Website App Path doesn't exist. Please install Roblox from your web browser in order to use!")
            exit()
    elif main_os == "Darwin":
        if not os.path.exists(macOS_dir):
            printErrorMessage("The Roblox Website App Path doesn't exist. Please install Roblox from your web browser in order to use!")
            exit()
    handler = Main()

    def getUserId():
        printMainMessage("Please input your User ID! This can be found on your profile in the URL: https://www.roblox.com/users/XXXXXXXX/profile")
        printMainMessage("This will be used for items that require a User ID.")
        id = input("> ")
        if id.isnumeric():
            return id
        elif id == "exit":
            printMainMessage("Ending installation..")
            exit()
        else:
            printWarnMessage("Let's try again!")
            return getUserId()
        
    def isYes(text):
        return text.lower() == "y" or text.lower() == "yes"
    
    def isNo(text):
        return text.lower() == "n" or text.lower() == "no"
    
    def isRequestClose(text):
        return text.lower() == "exit" or text.lower() == "exit()"
    
    id = getUserId()
    if id:
        # Based JSON
        generated_json = {}

        # FPS Unlocker
        printWarnMessage("--- FPS Unlocker ---")
        printMainMessage("Would you like to use an FPS Unlocker? (y/n)")
        installFPSUnlocker = input("> ")
        def getFPSCap():
            printWarnMessage("- FPS Cap -")
            printMainMessage("Enter the FPS cap to install on your client. (Leave blank for no cap)")
            cap = input("> ")
            if cap.isnumeric():
                return cap
            elif cap == "exit":
                printMainMessage("Ending installation..")
                exit()
            else:
                return None
        if isYes(installFPSUnlocker) == True:
            # FPS Cap
            fpsCap = getFPSCap()

            # Roblox Vulkan Rendering
            printWarnMessage("- Roblox Vulkan Rendering -")
            printMainMessage("Would you like to use Vulkan Rendering? (It will remove the cap fully but may cause issues) (y/n)")
            useVulkan = input("> ")
            generated_json["FFlagTaskSchedulerLimitTargetFpsTo2402"] = "false"

            if main_os == "Darwin":
                generated_json["FFlagDebugGraphicsDisableMetal"] =  "true"

            if fpsCap == None:
                generated_json["DFIntTaskSchedulerTargetFps"] = 99999
            else:
                generated_json["DFIntTaskSchedulerTargetFps"] = int(fpsCap)

            if isYes(useVulkan) == True:
                generated_json["FFlagDebugGraphicsPreferVulkan"] = "true"
            elif isNo(useVulkan) == True:
                generated_json["FFlagDebugGraphicsPreferVulkan"] = "false"
            elif isRequestClose(useVulkan) == True:
                printMainMessage("Ending installation..")
                exit()
        elif isRequestClose(installFPSUnlocker) == True:
            printMainMessage("Ending installation..")
            exit()
        elif isNo(installFPSUnlocker) == True:
            generated_json["FFlagDebugGraphicsPreferVulkan"] = "false"
            generated_json["DFIntTaskSchedulerTargetFps"] = 60
            generated_json["FFlagDebugGraphicsDisableMetal"] = "false"

            # Roblox FPS Unlocker
            printWarnMessage("- Roblox FPS Unlocker -")
            printMainMessage("Would you like the Roblox FPS Unlocker in your settings? (This may not work depending on your Roblox client version.) (y/n)")
            robloxFPSUnlocker = input("> ")
            if isYes(robloxFPSUnlocker) == True:
                generated_json["FFlagGameBasicSettingsFramerateCap5"] = "true" # If roblox decides to change, I won't need to :)
                generated_json["FFlagGameBasicSettingsFramerateCap6"] = "true"
                generated_json["FFlagGameBasicSettingsFramerateCap7"] = "true"
                generated_json["FFlagGameBasicSettingsFramerateCap8"] = "true"
                generated_json["FFlagGameBasicSettingsFramerateCap9"] = "true"
                generated_json["FFlagGameBasicSettingsFramerateCap10"] = "true" # If roblox decides to change, I won't need to :)
                generated_json["DFIntTaskSchedulerTargetFps"] = 0
            elif isRequestClose(robloxFPSUnlocker) == True:
                printMainMessage("Ending installation..")
                exit()

        # Verified Badge
        printWarnMessage("--- Verified Badge ---")
        printMainMessage("Would you like to use a verified badge during Roblox Games? (y/n)")
        installVerifiedBadge = input("> ")
        if isYes(installVerifiedBadge) == True:
            generated_json["FStringWhitelistVerifiedUserId"] = str(id)
        elif isRequestClose(installVerifiedBadge) == True:
            printMainMessage("Ending installation..")
            exit()
        elif isNo(installVerifiedBadge) == True:
            generated_json["FStringWhitelistVerifiedUserId"] = ""

        # Accessory Adjustments
        printWarnMessage("--- Accessory Adjustments ---")
        printMainMessage("Would you like to install an accessory adjustments fast flag? (It may depend on your current version of Roblox.) (y/n)")
        installAccessoryAdjust = input("> ")
        if isYes(installAccessoryAdjust) == True:
            generated_json["FFlagAccessoryAdjustmentEnabled2"] = "true"
            generated_json["FFlagHumanoidDescriptionUseInstances5"] = "true"
            generated_json["FFlagEnableNonUAPAccessoryAdjustment"] = "true"
            generated_json["FFlagAXAvatarFetchResultCamelCase"] = "true"
            generated_json["FFlagAccessoryAdjustmentEnabled3"] = "true"
            generated_json["FFlagAXAccessoryAdjustment"] = "true"
            generated_json["FFlagAXAccessoryAdjustmentIXPEnabled"] = "true"
            generated_json["FFlagAXAccessoryAdjustmentIXPEnabledForAll"] = "true"
        elif isRequestClose(installAccessoryAdjust) == True:
            printMainMessage("Ending installation..")
            exit()

        # Rename Charts to Discover
        printWarnMessage("--- Replace Charts ---")
        printMainMessage("Would you like to rename Charts back to Discover (may work)? (y/n)")
        installRenameCharts = input("> ")
        if isYes(installRenameCharts) == True:
            generated_json["FFlagLuaAppChartsPageRenameIXP"] = "true"
        elif isRequestClose(installRenameCharts) == True:
            printMainMessage("Ending installation..")
            exit()

        if main_os == "Windows":
            # Enable Developer Tools
            printWarnMessage("--- Enable Developer Tools ---")
            printMainMessage("Would you like to enable Developer Tools inside of the Roblox App (when website frame is opened) (Ctrl+Shift+I)? (y/n)")
            installEnableDeveloper = input("> ")
            if isYes(installEnableDeveloper) == True:
                generated_json["FFlagDebugEnableNewWebView2DevTool"] = "true"
            elif isRequestClose(installEnableDeveloper) == True:
                printMainMessage("Ending installation..")
                exit()

        # Display FPS
        printWarnMessage("--- Display FPS ---")
        printMainMessage("Would you like your client to display the FPS? (y/n)")
        installFPSViewer = input("> ")
        if isYes(installFPSViewer) == True:
            generated_json["FFlagDebugDisplayFPS"] = "true"
        elif isRequestClose(installFPSViewer) == True:
            printMainMessage("Ending installation..")
            exit()
        elif isNo(installFPSViewer) == True:
            generated_json["FFlagDebugDisplayFPS"] = "false"

        # Disable Ads
        printWarnMessage("--- Disable Ads ---")
        printMainMessage("Would you like your client to disable ads? (y/n)")
        installRemoveAds = input("> ")
        if isYes(installRemoveAds) == True:
            generated_json["FFlagAdServiceEnabled"] = "false"
        elif isRequestClose(installRemoveAds) == True:
            printMainMessage("Ending installation..")
            exit()
        elif isNo(installRemoveAds) == True:
            generated_json["FFlagAdServiceEnabled"] = "true"

        # Increase Max Assets Loading
        printWarnMessage("--- Increase Max Assets Loading ---")
        printMainMessage("Would you like to increase the limit on Max Assets loading from 100 to 1,000? (this will make loading into games faster depending on your computer) (y/n)")
        printYellowMessage("WARNING! This can crash your Roblox session!")
        installRemoveMaxAssets = input("> ")
        if isYes(installRemoveMaxAssets) == True:
            generated_json["DFIntNumAssetsMaxToPreload"] = "1000"
        elif isRequestClose(installRemoveMaxAssets) == True:
            printMainMessage("Ending installation..")
            exit()
        elif isNo(installRemoveMaxAssets) == True:
            generated_json["DFIntNumAssetsMaxToPreload"] = "100"

        # Enable Genre System
        printWarnMessage("--- Enable New Genre System Under Making ---")
        printMainMessage("Would you like to enable the new genre system in beta? (y/n)")
        installGenreSystem = input("> ")
        if isYes(installGenreSystem) == True:
            generated_json["FFlagLuaAppGenreUnderConstruction"] = "false"
        elif isRequestClose(installGenreSystem) == True:
            printMainMessage("Ending installation..")
            exit()
        elif isNo(installGenreSystem) == True:
            generated_json["FFlagLuaAppGenreUnderConstruction"] = "true"

        # Enable Freecam
        printWarnMessage("--- Enable Freecam ---")
        printMainMessage("Would you like to enable freecam on the Roblox client (only works if you're a Roblox Developer of a game or a Star Creator)? (y/n)")
        installFreecam = input("> ")
        if isYes(installFreecam) == True:
            generated_json["FFlagLoadFreecamModule"] = "true"
        elif isRequestClose(installFreecam) == True:
            printMainMessage("Ending installation..")
            exit()
        elif isNo(installFreecam) == True:
            generated_json["FFlagLoadFreecamModule"] = "false"

        # Enable Text Size Scaling
        printWarnMessage("--- Enable Text Size Scaling ---")
        printMainMessage("Would you like to enable the text size scaling in beta? (y/n)")
        installTextSizeScale = input("> ")
        if isYes(installTextSizeScale) == True:
            generated_json["FFlagEnablePreferredTextSizeScale"] = "true"
            generated_json["FFlagEnablePreferredTextSizeSettingInMenus2"] = "true"
        elif isRequestClose(installTextSizeScale) == True:
            printMainMessage("Ending installation..")
            exit()
        elif isNo(installTextSizeScale) == True:
            generated_json["FFlagEnablePreferredTextSizeScale"] = "false"
            generated_json["FFlagEnablePreferredTextSizeSettingInMenus2"] = "false"

        # Remove Automatically Translated
        printWarnMessage("--- Remove Automatically Translated ---")
        printMainMessage("Would you like to remove the chat automatically translated message in the chat? (y/n)")
        installRemoveAutoTranslate = input("> ")
        if isYes(installRemoveAutoTranslate) == True:
            generated_json["FFlagChatTranslationEnableSystemMessage"] = "false"
        elif isRequestClose(installRemoveAutoTranslate) == True:
            printMainMessage("Ending installation..")
            exit()
        elif isNo(installRemoveAutoTranslate) == True:
            generated_json["FFlagChatTranslationEnableSystemMessage"] = "true"

        # Darker Mode
        printWarnMessage("--- Darker Mode ---")
        printMainMessage("Would you like to enable Darker mode on your client? (y/n)")
        installDarkerMode = input("> ")
        if isYes(installDarkerMode) == True:
            generated_json["FFlagLuaAppUseUIBloxColorPalettes1"] = "true"
            generated_json["FFlagUIBloxUseNewThemeColorPalettes"] = "true"
        elif isRequestClose(installDarkerMode) == True:
            printMainMessage("Ending installation..")
            exit()
        elif isNo(installDarkerMode) == True:
            generated_json["FFlagLuaAppUseUIBloxColorPalettes1"] = "false"
            generated_json["FFlagUIBloxUseNewThemeColorPalettes"] = "false"

        # Blue Foundation Colors
        printWarnMessage("--- Blue Foundation Colors ---")
        printMainMessage("Would you like to enable new blue foundation colors on the Roblox client? (y/n)")
        installBlueColors = input("> ")
        if isYes(installBlueColors) == True:
            generated_json["FFlagLuaAppEnableFoundationColors3"] = "true"
        elif isRequestClose(installBlueColors) == True:
            printMainMessage("Ending installation..")
            exit()
        elif isNo(installBlueColors) == True:
            generated_json["FFlagLuaAppEnableFoundationColors3"] = "false"

        # Custom Disconnect Message
        printWarnMessage("--- Custom Disconnect Message ---")
        printMainMessage("Would you like to use your own disconnect message? (disconnect button will disappear) (y/n)")
        installCustomDisconnect = input("> ")
        if isYes(installCustomDisconnect) == True:
            generated_json["FFlagReconnectDisabled"] = "true"
            printMainMessage("Enter the Disconnect Message below:")
            generated_json["FStringReconnectDisabledReason"] = input("> ")
        elif isRequestClose(installCustomDisconnect) == True:
            printMainMessage("Ending installation..")
            exit()
        elif isNo(installCustomDisconnect) == True:
            generated_json["FFlagReconnectDisabled"] = "false"
            generated_json["FStringReconnectDisabledReason"] = ""

        # Ability to Hide UI
        printWarnMessage("--- Hide UI ---")
        printMainMessage("Would you like to enable the ability to hide GUIs? (y/n)")
        installHideUI = input("> ")
        if isYes(installHideUI) == True:
            printMainMessage("Enter a Group ID that you're currently in so this flag can work:")
            generated_json["DFIntCanHideGuiGroupId"] = input("> ")
            if main_os == "Windows":
                printMainMessage("Combinations for hiding:")
                printMainMessage("Ctrl+Shift+B = Toggles BillboardGuis and SurfaceGuis")
                printMainMessage("Ctrl+Shift+C = Toggles PlayerGui")
                printMainMessage("Ctrl+Shift+G = Toggles CoreGui")
                printMainMessage("Ctrl+Shift+N = Toggles GUIs that appear above players")
            elif main_os == "Darwin":
                printMainMessage("Combinations for hiding:")
                printMainMessage("Command+Shift+B = Toggles BillboardGuis and SurfaceGuis")
                printMainMessage("Command+Shift+C = Toggles PlayerGui")
                printMainMessage("Command+Shift+G = Toggles CoreGui")
                printMainMessage("Command+Shift+N = Toggles GUIs that appear above players")
            else:
                printMainMessage("Ending installation..")
                exit()
        elif isRequestClose(installHideUI) == True:
            printMainMessage("Ending installation..")
            exit()
        elif isNo(installHideUI) == True:
            generated_json["DFIntCanHideGuiGroupId"] = ""

        # Quick Connect
        printWarnMessage("--- Quick Connect ---")
        printMainMessage("Would you like to install Quick Connect on your client? (y/n)")
        printErrorMessage("WARNING! This can be buggy and may cause issues on your Roblox experience!!!")
        installQuickConnect = input("> ")
        if isYes(installQuickConnect) == True:
            generated_json["FFlagEnableQuickGameLaunch"] = "true"
        elif isRequestClose(installQuickConnect) == True:
            printMainMessage("Ending installation..")
            exit()
        elif isNo(installQuickConnect) == True:
            generated_json["FFlagEnableQuickGameLaunch"] = "false"

        # Custom Fast Flags
        printWarnMessage("--- Custom Fast Flags ---")
        def custom():
            def loop():
                printMainMessage("Enter Key Value: ")
                key = input("> ")
                if key == "exit" or key == "":
                    return {"success": False, "key": "", "value": ""}
                if efaz_bootstrap_mode == True and key.startswith("EFlag"):
                    printMainMessage("Are you sure you want to set this Efaz's Roblox Bootstrap setting?")
                    con = input("> ")
                    if isYes(con) == False:
                        return loop()
                printMainMessage("Enter Value Value: ")
                value = input("> ")
                if value == "exit":
                    return {"success": False, "key": "", "value": ""}
                if value.isnumeric():
                    printMainMessage("Would you like this value to be a number value or do you want to keep it as a string? (y/n)")
                    isNum = input("> ")
                    if isNum == True:
                        value = int(value)
                return {"success": True, "key": key, "value": value}
            completeLoop = loop()
            if completeLoop["success"] == True:
                generated_json[completeLoop["key"]] = completeLoop["value"]
                printMainMessage("Would you like to add more fast flags? (y/n)")
                more = input("> ")
                if isYes(more) == True:
                    custom()
        printMainMessage("Would you like to use custom fast flags? (y/n)")
        installCustom = input("> ")
        if isYes(installCustom) == True:
            custom()
        elif isRequestClose(installCustom) == True:
            printMainMessage("Ending installation..")
            exit()

        # Installation Mode
        if efaz_bootstrap_mode == False:
            printWarnMessage("--- Installation Mode ---")
            printMainMessage("[y/yes] = Install/Reinstall Flags")
            printMainMessage("[n/no/(*)] = Cancel Install")
            printMainMessage("[j/json] = Get JSON Settings")
            printMainMessage("[nm/no-merge] = Don't Merge Settings with Previous Settings")
            printMainMessage("[f/flat] = Flat JSON Install")
            printMainMessage("[fnm/flat-no-merge] = Flat-No-Merge Install")
            printMainMessage("[r/reset] = Reset Settings")
            select_mode = input("> ")
            if isYes(select_mode) == True:
                printMainMessage("Selected Mode: Install/Reinstall Flags")
            elif select_mode.lower() == "j" or select_mode.lower() == "json":
                printMainMessage("Selected Mode: Get JSON Settings")
            elif select_mode.lower() == "nm" or select_mode.lower() == "no-merge":
                printMainMessage("Selected Mode: Don't Merge Settings with Previous Settings")
            elif select_mode.lower() == "f" or select_mode.lower() == "flat":
                printMainMessage("Selected Mode: Flat JSON Install")
            elif select_mode.lower() == "fnm" or select_mode.lower() == "flat-no-merge":
                printMainMessage("Selected Mode: Flat-No-Merge Install")
            elif select_mode.lower() == "r" or select_mode.lower() == "reset":
                printMainMessage("Selected Mode: Reset Settings")
            else:
                printMainMessage("Ending installation..")
                exit()
        else:
            select_mode = "y"

        # Installation
        if not (select_mode.lower() == "j" or select_mode.lower() == "json"):
            if efaz_bootstrap_mode == False:
                printWarnMessage("--- Installation Ready! ---")
                printMainMessage("Settings are now finished and now ready for setup!")
                printMainMessage("Would you like to continue with the fast flag installation? (y/n)")
                printErrorMessage("WARNING! This will force-quit any open Roblox windows! Please close them now before continuing in order to prevent data loss!")
                install_now = input("> ")
                if isYes(install_now) == True:
                    if isYes(select_mode) == True:
                        handler.installFastFlagsJSON(generated_json)
                    elif select_mode.lower() == "j" or select_mode.lower() == "json":
                        printMainMessage("Generated JSON:")
                        printMainMessage(json.dumps(generated_json))
                        exit()
                    elif select_mode.lower() == "nm" or select_mode.lower() == "no-merge":
                        handler.installFastFlagsJSON(generated_json, merge=False)
                    elif select_mode.lower() == "f" or select_mode.lower() == "flat":
                        handler.installFastFlagsJSON(generated_json, flat=True)
                    elif select_mode.lower() == "fnm" or select_mode.lower() == "flat-no-merge":
                        handler.installFastFlagsJSON(generated_json, merge=False, flat=True)
                    elif select_mode.lower() == "r" or select_mode.lower() == "reset":
                        handler.installFastFlagsJSON({})
                    else:
                        printMainMessage("Ending installation..")
                        exit()
                else:
                    printMainMessage("Ending installation..")
                    exit()
            else:
                printWarnMessage("--- Saving Ready! ---")
                printMainMessage("Are you sure you would like to save these FFlags in the bootstrap system?")
                install_now = input("> ")
                if isYes(install_now) == True:
                    handler.installFastFlagsJSON(generated_json, endRobloxInstances=False)
                else:
                    printMainMessage("Ending installation..")
                    exit()