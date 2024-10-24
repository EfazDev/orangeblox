# 
# Efaz's Roblox Bootstrap API
# Made by Efaz from efaz.dev
# v1.3.0
# 
# Provided to Mod Mode Scripts using variable EfazRobloxBootstrapAPI
# Developers may use the following line to see the full API in Visual Studio Code:
# from EfazRobloxBootstrapAPI import EfazRobloxBootstrapAPI; EfazRobloxBootstrapAPI = EfazRobloxBootstrapAPI()
# 

import time
import uuid
import threading
import platform
import json
from typing import Union
from urllib.parse import urlparse

current_version = {"version": "1.3.0"}

class EfazRobloxBootstrapAPI:
    # Variables [Used for contacting with the bootstrap]
    requestedFunctions = {}
    launchedFromBootstrap = False

    # Classes
    class InvalidRequested(Exception):
        def __init__(self):            
            super().__init__("You have provided an invalid requested function name!")
    class InvalidRequest(Exception):
        def __init__(self):            
            super().__init__("You have provided an invalid request!")
    class InvalidEfazBootstrapAPI(Exception):
        def __init__(self):            
            super().__init__("You have provided an invalid EfazRobloxBootstrapAPI handler!")
    class BloxstrapRichPresence:
        details=None
        state=None
        timeStart=None
        timeEnd=None
        largeImage=None
        smallImage=None
        def __init__(self, details: str=None, state: str=None, timeStart: float=None, timeEnd: float=None, largeImage: dict=None, smallImage: dict=None):
            if type(details) is str:
                self.details = details
            if type(state) is str:
                self.state = state
            if type(timeStart) is float or type(timeStart) is int:
                self.timeStart = timeStart
            if type(timeEnd) is float or type(timeEnd) is int:
                self.timeEnd = timeEnd
            if type(largeImage) is dict:
                generated_large_image = {
                    "assetId": None,
                    "hoverText": None,
                    "clear": False,
                    "reset": False
                }
                if type(largeImage.get("assetId")) is int:
                    generated_large_image["assetId"] = largeImage.get("assetId")
                elif type(largeImage.get("assetId")) is str:
                    try:
                        parsed_link = urlparse(largeImage.get("assetId"))
                        if parsed_link.netloc.endswith("roblox.com") or parsed_link.netloc.endswith("rbxcdn.com"):
                            generated_large_image["assetId"] = largeImage.get("assetId")
                        else:
                            generated_large_image["assetId"] = None
                    except Exception as e:
                        generated_large_image["assetId"] = None
                if type(largeImage.get("hoverText")) is str:
                    generated_large_image["hoverText"] = largeImage.get("hoverText")
                if type(largeImage.get("clear")) is bool:
                    generated_large_image["clear"] = largeImage.get("clear")
                if type(largeImage.get("reset")) is bool:
                    generated_large_image["reset"] = largeImage.get("reset")
                if generated_large_image["assetId"] == None and generated_large_image["hoverText"] == None:
                    generated_large_image = None
                self.largeImage = generated_large_image
            if type(smallImage) is dict:
                generated_small_image = {
                    "assetId": None,
                    "hoverText": None,
                    "clear": False,
                    "reset": False
                }
                if type(smallImage.get("assetId")) is int:
                    generated_small_image["assetId"] = smallImage.get("assetId")
                elif type(smallImage.get("assetId")) is str:
                    try:
                        parsed_link = urlparse(smallImage.get("assetId"))
                        if parsed_link.netloc.endswith("roblox.com") or parsed_link.netloc.endswith("rbxcdn.com"):
                            generated_small_image["assetId"] = smallImage.get("assetId")
                        else:
                            generated_small_image["assetId"] = None
                    except Exception as e:
                        generated_small_image["assetId"] = None
                if type(smallImage.get("hoverText")) is str:
                    generated_small_image["hoverText"] = smallImage.get("hoverText")
                if type(smallImage.get("clear")) is bool:
                    generated_small_image["clear"] = smallImage.get("clear")
                if type(smallImage.get("reset")) is bool:
                    generated_small_image["reset"] = smallImage.get("reset")
                if generated_small_image["assetId"] == None and generated_small_image["hoverText"] == None:
                    generated_small_image = None
                self.smallImage = generated_small_image
        def generate_json(self):
            generated_rpc_data = {}
            if self.details: generated_rpc_data["details"] = self.details
            if self.state: generated_rpc_data["state"] = self.state
            if self.largeImage: generated_rpc_data["largeImage"] = self.largeImage
            if self.smallImage: generated_rpc_data["smallImage"] = self.smallImage
            if self.timeStart: generated_rpc_data["timeStart"] = self.timeStart
            if self.timeEnd: generated_rpc_data["timeEnd"] = self.timeEnd
            return generated_rpc_data
    class Request:
        requested = ""
        success = False
        fulfilled = False
        timed_out = False
        code = None
        value = None
        args = {}
        id = None

        def __init__(self, bootstrap_api, requested_function: str, args: dict={}):
            if type(bootstrap_api) is EfazRobloxBootstrapAPI:
                generated_function_id = str(uuid.uuid4())
                if type(requested_function) is str:
                    self.requested = requested_function
                    if type(args) is dict:
                        self.args = args
                    elif type(args) is list:
                        self.args = args
                    else:
                        self.args = {}
                    self.id = generated_function_id
                    def timeout():
                        time.sleep(5)
                        self.timed_out = True
                        bootstrap_api.requestedFunctions[generated_function_id] = None
                    timeout_thread = threading.Thread(target=timeout, daemon=True)
                    timeout_thread.start()
                    bootstrap_api.requestedFunctions[generated_function_id] = self
                    while (self.timed_out == False):
                        if self.fulfilled == True:
                            if self.code == 0:
                                self.success = True
                            else:
                                self.success = False
                            return
                    self.success = False
                    self.code = 5
                    self.value = None
                else:
                    raise EfazRobloxBootstrapAPI.InvalidRequested()
            else:
                raise EfazRobloxBootstrapAPI.InvalidEfazBootstrapAPI()
        def generateResponse(self):
            return EfazRobloxBootstrapAPI.Response(self)
    class Response:
        success = False
        response = None
        code = 0
        timed_out = False
        command = ""
        def __init__(self, main_req):
            if type(main_req) is EfazRobloxBootstrapAPI.Request:
                self.success = main_req.success
                self.response = main_req.value
                self.code = main_req.code
                self.timed_out = main_req.timed_out
                self.command = main_req.requested
            else:
                raise EfazRobloxBootstrapAPI.InvalidRequest()
    
    # Functions
    def getPlatform(self, static=False): # No Permission Needed
        s = platform.system()
        if static == True:
            return s
        else:
            if s == "Windows":
                return "Windows"
            elif s == "Darwin":
                return "macOS"
            else:
                return "Linux"
    def getFastFlagConfiguration(self): # Permission: getFastFlagConfiguration
        return self.Request(self, "getFastFlagConfiguration").generateResponse().response
    def setFastFlagConfiguration(self, configuration: dict, full: bool=False): # Permission: setFastFlagConfiguration
        return self.Request(self, "setFastFlagConfiguration", [configuration, full]).generateResponse()
    def saveFastFlagConfiguration(self, configuration: dict, full: bool=False): # Permission: saveFastFlagConfiguration
        return self.Request(self, "saveFastFlagConfiguration", [configuration, full]).generateResponse()
    def displayNotification(self, title="Mod Script", message="A mod script message!"): # Permission: displayNotification
        return self.Request(self, "displayNotification", {"title": title, "message": message}).generateResponse()
    def generateModsManifest(self): # Permission: generateModsManifest
        return self.Request(self, "generateModsManifest").generateResponse().response
    def sendBloxstrapRPC(self, command: str="SetRichPresence", data: Union[BloxstrapRichPresence, dict, str]={}, disableWebhook=True): # Permission: sendBloxstrapRPC
        if type(data) is EfazRobloxBootstrapAPI.BloxstrapRichPresence:
            generated_rpc_data = data.generate_json()
        elif type(data) is dict or type(data) is str:
            generated_rpc_data = data
        else:
            generated_rpc_data = {}
        return self.Request(self, "sendBloxstrapRPC", [{"command": command, "data": generated_rpc_data}, (disableWebhook == True)]).generateResponse()
    def getRobloxLogFolderSize(self, static=False): # Permission: getRobloxLogFolderSize
        return self.Request(self, "getRobloxLogFolderSize", {"static": static}).generateResponse().response   
    def getLatestRobloxVersion(self, channel="LIVE"): # Permission: getLatestRobloxVersion
        return self.Request(self, "getLatestRobloxVersion", {"channel": channel}).generateResponse().response 
    def getInstalledRobloxVersion(self): # Permission: getInstalledRobloxVersion
        return self.Request(self, "getInstalledRobloxVersion").generateResponse().response
    def getRobloxInstallFolder(self): # Permission: getRobloxInstallFolder
        return self.Request(self, "getRobloxInstallFolder").generateResponse().response   
    def getIfRobloxIsOpen(self, pid=""): # Permission: getIfRobloxIsOpen
        return self.Request(self, "getIfRobloxIsOpen", {"pid": pid}).generateResponse().response
    def getLatestRobloxPid(self): # Permission: getLatestRobloxPid
        return self.Request(self, "getLatestRobloxPid").generateResponse().response
    def getDebugMode(self): # No Permission Needed
        return self.Request(self, "getDebugMode").generateResponse().response
    def getConfiguration(self, name: str="*"): # No Permission Needed
        if type(name) is str:
            return self.Request(self, "getConfiguration", {"name": name}).generateResponse().response
        else:
            return None
    def setConfiguration(self, name: str="*", data=None): # No Permission Needed
        if (type(data) is None) or (type(data) is str) or (type(data) is dict) or (type(data) is int) or (type(data) is float) or (type(data) is list):
            try:
                a = json.dumps(data)
                return self.Request(self, "setConfiguration", {"name": name, "data": data}).generateResponse().response
            except Exception as e:
                raise self.InvalidRequest()
        else:
            raise self.InvalidRequest()
    def about(self): # No Permission Needed
        bootstrap_res = self.Request(self, "about").generateResponse().response
        if bootstrap_res:
            return {"bootstrap_version": bootstrap_res["version"], "api_version": current_version}
        else:
            return None