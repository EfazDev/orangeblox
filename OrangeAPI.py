# 
# Orange API 🍊
# Made by Efaz from efaz.dev
# v2.0.1
# 
# Provided to Mod Scripts using variable OrangeAPI
# Developers may use the following line to see the full API in Visual Studio Code:
# import OrangeAPI as orange; OrangeAPI = orange.OrangeAPI()
# 

import time
import uuid
import threading
import platform
import typing
import json
from urllib.parse import urlparse

# Variables
current_version = {"version": "2.0.1"}
requested_functions = {}
cached_information = {}
debug_mode = False
studio_mode = False
launched_from_bootstrap = False

# Top Classes
class InvalidRequested(Exception):
    """Exception for message: You have provided an invalid requested function name!"""
    def __init__(self):            
        super().__init__("You have provided an invalid requested function name!")
class InvalidRequest(Exception):
    """Exception for message: You have provided an invalid request!"""
    def __init__(self):            
        super().__init__("You have provided an invalid request!")
class InvalidOrangeAPI(Exception):
    """Exception for message: You have provided an invalid OrangeAPI handler!"""
    def __init__(self):            
        super().__init__("You have provided an invalid OrangeAPI handler!")
class UnusedAPI(Warning):
    """Warning for message: This API variable/class is no longer usable! Please update your scripts!"""
    def __init__(self):            
        super().__init__("This API variable/class is no longer usable! Please update your scripts!")
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
        global requested_functions
        if type(bootstrap_api) is OrangeAPI:
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
                    requested_functions[generated_function_id] = None
                timeout_thread = threading.Thread(target=timeout, daemon=True)
                timeout_thread.start()
                requested_functions[generated_function_id] = self
                while (self.timed_out == False):
                    if self.fulfilled == True:
                        if self.code == 0:
                            self.success = True
                        else:
                            self.success = False
                        return
                    time.sleep(0.05)
                self.success = False
                self.code = 5
                self.value = None
            else:
                raise InvalidRequested()
        else:
            raise InvalidOrangeAPI()
    def generateResponse(self):
        return Response(self)
class Response:
    """This is a class used for returning data back in details such as success, code, response data, etc."""
    success = False
    """If the command succeeded through the bootstrap"""
    response = None
    """The response data the bootstrap returned"""
    code = 0
    """This is the response code that may indicate the error or not."""
    timed_out = False
    """If the command timed-out after 5 seconds"""
    command = ""
    """The command used [This may not match with the function name]"""
    def __init__(self, main_req):
        if type(main_req) is Request:
            self.success = main_req.success
            self.response = main_req.value
            self.code = main_req.code
            self.timed_out = main_req.timed_out
            self.command = main_req.requested
        else:
            raise InvalidRequest()
class OrangeAPI:
    """
    The OrangeAPI is an API that Mod Scripts can use for getting or setting data, store configurations, set a Discord presence using the BloxstrapRPC and more! It is automatically added as an variable during runtime as "OrangeAPI" For Visual Studio Code users, you may use the following line of code to get a reference! [You must have it opened to the OrangeBlox folder where it contains Main.py, RobloxFastFlagInstaller.py, etc.]
   
    **OrangeAPI is only supported on OrangeBlox v2.0.0+. Any other versions like Efaz's Roblox Bootstrap v1.5.9 or below is unable to use this API.**
    **Please use the Efaz's Roblox Bootstrap API in order to support Efaz's Roblox Bootstrap v1.3.0-v1.5.9.**

    ```python
    import OrangeAPI as orange; OrangeAPI = orange.OrangeAPI()
    ```
    """
    requestedFunctions: dict = {}
    """
    ## Warning!
    This variable was moved to head in v1.4.1+ for security purposes and now returns an empty array that is not usable for communicating.
    """
    launchedFromBootstrap: bool = False
    """
    This is a boolean variable used to indicate if the module is launched from the bootstrap or not.
    """
    debugMode: bool = False
    """
    This is a boolean variable that is enabled if the user is on debug mode.
    """

    # Classes
    class Response:
        """
        ## Warning!
        This class was moved to head in v1.4.1+ for security purposes and now returns an empty class that is not usable for communicating. Additionally, most functions will not return this class and will return the response value instead. If you need to check if it's a Response or not, use the OrangeAPI.checkIfResponseClass(suspected) definition.
        """
        success = False
        """If the command succeeded through the bootstrap"""
        response = None
        """The response data the bootstrap returned"""
        code = 0
        """This is the response code that may indicate the error or not."""
        timed_out = False
        """If the command timed-out after 5 seconds"""
        command = ""
        """The command used [This may not match with the function name]"""
        def __init__(self, main_req):
            raise UnusedAPI()
    class Request:
        """
        ## Warning!
        This class was moved to head in v1.4.1+ for security purposes and now returns an empty class that is not usable for communicating.
        """
        requested = ""
        success = False
        fulfilled = False
        timed_out = False
        code = None
        value = None
        args = {}
        id = None

        def __init__(self, bootstrap_api, requested_function: str, args: dict={}):
            raise UnusedAPI()
        def generateResponse(self):
            raise UnusedAPI()
    class BloxstrapRichPresence:
        """This is a class used for generating data in a BloxstrapRPC compatible format (aka JSON string)"""
        details=None
        """The details value of the Discord Presence."""
        state=None
        """The state value of the Discord Presence."""
        timeStart=None
        """The time started value of the Discord Presence."""
        timeEnd=None
        """The time ended value of the Discord Presence."""
        largeImage=None
        """The large image link value of the Discord Presence."""
        smallImage=None
        """The small image link value of the Discord Presence."""
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
            """Generate a usable BloxstrapRPC JSON based on details, state, images and time."""
            generated_rpc_data = {}
            if self.details: generated_rpc_data["details"] = self.details
            if self.state: generated_rpc_data["state"] = self.state
            if self.largeImage: generated_rpc_data["largeImage"] = self.largeImage
            if self.smallImage: generated_rpc_data["smallImage"] = self.smallImage
            if self.timeStart: generated_rpc_data["timeStart"] = self.timeStart
            if self.timeEnd: generated_rpc_data["timeEnd"] = self.timeEnd
            return generated_rpc_data
    class DiscordWebhookField:
        """
        This is a class used to represent a Discord Webhook field!
        """
        name = ""
        """This is the field name"""
        value = ""
        """This is the field value"""
        inline = False
        """This is if the field is inline or not."""
        def __init__(self, name: str, value: str, inline: bool=False): self.name = name; self.value = value; self.inline = inline
        def convert(self): """This converts the class into a usable JSON table!"""; return {"name": str(self.name), "value": str(self.value), "inline": self.inline==True}

    # Functions
    def getMainConfiguration(self) -> dict | None: # Permission: getMainConfiguration
        """
        This gets the current user's bootstrap configuration data.

        Permission: getMainConfiguration | Level: 1 [Warning]

        **The following keys are not shown due to security: EFlagDiscordWebhookURL**
        **This function was renamed to getMainConfiguration on v2.0.1. FastFlagConfiguration functions will still function until v2.5.0.**

        ```python
        main_config = OrangeAPI.getMainConfiguration()
        print(main_config) # --> {"EFlagBlahBlah": True, "FFlagBlahBlah": "something"}
        ```
        """
        return Request(self, "getMainConfiguration").generateResponse().response
    def setMainConfiguration(self, configuration: dict, full: bool=False) -> Response | None: # Permission: setMainConfiguration
        """
        This sets the current user's bootstrap configuration data in the CURRENT running bootstrap window. This will not affect the Configuration.json file. The full argument means it will overwrite the full configuration if true, it will not manually add keys one at a time
        
        Permission: setMainConfiguration | Level: 2 [Caution]
        **This function was renamed to getMainConfiguration on v2.0.1. FastFlagConfiguration functions will still function until v2.5.0.**

        ```python
        response = OrangeAPI.setMainConfiguration({"EFlagDiscordWebhookRobloxAppStart": True}, False) # -> Response class
        ```
        """
        return Request(self, "setMainConfiguration", [configuration, full]).generateResponse()
    def saveMainConfiguration(self, configuration: dict, full: bool=False) -> Response | None: # Permission: saveMainConfiguration
        """
        This sets the current user's bootstrap configuration data through the current window AND the Configuration.json file. The full argument means it will overwrite the full configuration if true, it will not manually add keys one at a time
        
        Permission: saveMainConfiguration | Level: 2 [Caution]

        **Unless the user has recovery tools, data overwritten by this function is non-recoverable. Therefore, please check your code and make validation checks if needed! For security, EFlags keys are not able to be saved and are ignored when tried.**
        **This function was renamed to getMainConfiguration on v2.0.1. FastFlagConfiguration functions will still function until v2.5.0.**

        ```python
        response = OrangeAPI.saveMainConfiguration({"EFlagDiscordWebhookRobloxAppStart": True}, False) # -> Response class
        ```
        """
        return Request(self, "saveMainConfiguration", [configuration, full]).generateResponse()
    def getFastFlagConfiguration(self) -> dict | None: # Permission: getFastFlagConfiguration
        """
        This gets the current user's bootstrap configuration data.

        Permission: getFastFlagConfiguration | Level: 1 [Warning]

        **The following keys are not shown due to security: EFlagDiscordWebhookURL**
        **This function was renamed to getFastFlagConfiguration on v2.0.1. FastFlagConfiguration functions will still function until v2.5.0.**

        ```python
        main_config = OrangeAPI.getFastFlagConfiguration()
        print(main_config) # --> {"EFlagBlahBlah": True, "FFlagBlahBlah": "something"}
        ```
        """
        return Request(self, "getFastFlagConfiguration").generateResponse().response
    def setFastFlagConfiguration(self, configuration: dict, full: bool=False) -> Response | None: # Permission: setFastFlagConfiguration
        """
        This sets the current user's bootstrap configuration data in the CURRENT running bootstrap window. This will not affect the Configuration.json file. The full argument means it will overwrite the full configuration if true, it will not manually add keys one at a time
        
        Permission: setFastFlagConfiguration | Level: 2 [Caution]
        **This function was renamed to getMainConfiguration on v2.0.1. FastFlagConfiguration functions will still function until v2.5.0.**

        ```python
        response = OrangeAPI.setFastFlagConfiguration({"EFlagDiscordWebhookRobloxAppStart": True}, False) # -> Response class
        ```
        """
        return Request(self, "setFastFlagConfiguration", [configuration, full]).generateResponse()
    def saveFastFlagConfiguration(self, configuration: dict, full: bool=False) -> Response | None: # Permission: saveFastFlagConfiguration
        """
        This sets the current user's bootstrap configuration data through the current window AND the Configuration.json file. The full argument means it will overwrite the full configuration if true, it will not manually add keys one at a time
        
        Permission: saveFastFlagConfiguration | Level: 2 [Caution]

        **Unless the user has recovery tools, data overwritten by this function is non-recoverable. Therefore, please check your code and make validation checks if needed! For security, EFlags keys are not able to be saved and are ignored when tried.**
        **This function was renamed to getMainConfiguration on v2.0.1. FastFlagConfiguration functions will still function until v2.5.0.**

        ```python
        response = OrangeAPI.saveFastFlagConfiguration({"EFlagDiscordWebhookRobloxAppStart": True}, False) # -> Response class
        ```
        """
        return Request(self, "saveFastFlagConfiguration", [configuration, full]).generateResponse()
    def displayNotification(self, title: str="Mod Script", message: str="A mod script message!") -> Response | None: # Permission: displayNotification
        """
        This sends a notification through the bootstrap into the current user's computer depending on the OS.
        
        Permission: displayNotification | Level: 1 [Warning]

        ```python
        response = OrangeAPI.displayNotification("Hi!", "Hello Mod Mode User!") # -> Response class
        ```
        """
        return Request(self, "displayNotification", {"title": title, "message": message}).generateResponse()
    def generateModsManifest(self) -> dict[str, dict[str, typing.Any]] | None: # Permission: generateModsManifest
        """
        Get information about all the user's installed mods!
        
        Permission: generateModsManifest | Level: 0 [Normal]

        ```python
        mods = OrangeAPI.generateModsManifest() # -> 
        # {
        #     "Template": {
        #         "name": "My Very Own Mod!",
        #         "id": "Template",
        #         "version": "1.0.0",
        #         "mod_script": True,
        #         "mod_script_path": "/Applications/OrangeBlox.app/Contents/Resources/Mods/Template/ModScript.py",
        #         "manifest_path": "/Applications/OrangeBlox.app/Contents/Resources/Mods/Template/Manifest.py",
        #         "enabled": True,
        #         "permissions": ["onGameDisconnected", "sendBloxstrapRPC"],
        #         "python_modules": ["requests"],
        #         "mod_script_supports": "1.3.0",
        #         "mod_script_end_support": "1.5.0",
        #         "mod_script_end_support_reasoning": "Bugs were unable to be fixed and maintained.",
        #         "mod_script_supports_operating_system": True,
        #         "both_supported": False,
        #         "is_studio_mod": False,
        #         "list_in_normal_mods": True
        #     }
        # }
        ```
        """
        return Request(self, "generateModsManifest").generateResponse().response
    def sendBloxstrapRPC(self, command: str="SetRichPresence", data: typing.Union[BloxstrapRichPresence, dict, str]={}, disableWebhook: bool=True) -> Response | None: # Permission: sendBloxstrapRPC
        """
        This changes the current Discord Presence if found using BloxstrapRPC. If disableWebhook is enabled, the Discord webhook notification is disabled. [Original Example from Bloxstrap in Roblox Lua](https://github.com/bloxstraplabs/bloxstrap/wiki/Integrating-Bloxstrap-functionality-into-your-game#function-setrichpresence)
        
        Permission: sendBloxstrapRPC | Level: 2 [Caution]

        ```python
        response = OrangeAPI.sendBloxstrapRPC("SetRichPresence", {
            "details": "Example details value",
            "state": "Example state value",
            "largeImage": {
                "assetId": 10630555127,
                "hoverText": "Example hover text"
            },
            "smallImage": {
                "assetId": 13409122839,
                "hoverText": "Example hover text"
            }
        }) # -> Response class
        ```
        """
        if type(data) is OrangeAPI.BloxstrapRichPresence:
            generated_rpc_data = data.generate_json()
        elif type(data) is dict or type(data) is str:
            generated_rpc_data = data
        else:
            generated_rpc_data = {}
        return Request(self, "sendBloxstrapRPC", [{"command": command, "data": generated_rpc_data}, (disableWebhook == True)]).generateResponse()
    def getRobloxLogFolderSize(self, static: bool=False) -> str | int | None: # Permission: getRobloxLogFolderSize
        """
        Get the current size of the Roblox Logs folder. If static mode is enabled, it will return the size of the Logs folder in bytes. Idk why would this be useful lol.

        Permission: getRobloxLogFolderSize | Level: 0 [Normal]

        ```python
        roblox_logs_size = OrangeAPI.getRobloxLogFolderSize() # -> "1 KB"
        roblox_logs_size_static = OrangeAPI.getRobloxLogFolderSize(static=True) # -> 1000
        ```
        """
        return Request(self, "getRobloxLogFolderSize", {"static": static}).generateResponse().response   
    def getLatestRobloxVersion(self, channel: str="LIVE") -> dict[str, typing.Any] | None: # Permission: getLatestRobloxVersion
        """
        This pings the Roblox servers to get what's the latest Roblox version in a channel.

        Permission: getLatestRobloxVersion | Level: 0 [Normal]

        ```python
        latest_roblox_version = OrangeAPI.getLatestRobloxVersion() # -> 
        # {
        #     "success": True, 
        #     "client_version": "version-56269cdb46a44048", 
        #     "hash": "6470717"
        # }
        ```
        """
        return Request(self, "getLatestRobloxVersion", {"channel": channel}).generateResponse().response 
    def getInstalledRobloxVersion(self) -> dict[str, typing.Any] | None: # Permission: getInstalledRobloxVersion
        """
        This gets the current Roblox version installed including the channel the user is connected to.

        Permission: getInstalledRobloxVersion | Level: 1 [Warning]

        ```python
        current_roblox_version = OrangeAPI.getInstalledRobloxVersion() # -> 
        # {
        #     "success": True, 
        #     "client_version": "version-56269cdb46a44048",
        #     "version": "0.666.0.5566444", 
        #     "channel": "LIVE"
        # }
        ```
        """
        return Request(self, "getInstalledRobloxVersion").generateResponse().response
    def getLatestOppositeRobloxVersion(self, channel: str="LIVE") -> dict[str, typing.Any] | None: # Permission: getLatestOppositeRobloxVersion
        """
        Get the latest version of the opposite application (Roblox Player -> Studio, Studio -> Player)

        Permission: getLatestOppositeRobloxVersion | Level: 1 [Warning]

        **This function is only available in OrangeAPI v2.0.0+**

        ```python
        latest_opposite_roblox_version = OrangeAPI.getLatestOppositeRobloxVersion() # -> 
        # {
        #     "success": True, 
        #     "client_version": "version-56269cdb46a44048", 
        #     "hash": "6470717"
        # }
        ```
        """
        return Request(self, "getLatestOppositeRobloxVersion", {"channel": channel}).generateResponse().response 
    def getOppositeInstalledRobloxVersion(self) -> dict[str, typing.Any] | None: # Permission: getOppositeInstalledRobloxVersion
        """
        Get the current version of the opposite application (Roblox Player -> Studio, Studio -> Player)

        Permission: getOppositeInstalledRobloxVersion | Level: 1 [Warning]

        **This function is only available in OrangeAPI v2.0.0+**

        ```python
        current_opposite_roblox_version = OrangeAPI.getOppositeInstalledRobloxVersion() # -> 
        # {
        #     "success": True, 
        #     "client_version": "version-56269cdb46a44048",
        #     "version": "0.666.0.5566444", 
        #     "channel": "LIVE"
        # }
        ```
        """
        return Request(self, "getOppositeInstalledRobloxVersion").generateResponse().response
    def getRobloxInstallFolder(self) -> str | None: # Permission: getRobloxInstallFolder
        """
        This gets where Roblox is installed at. This may change between versions or operating systems.

        Permission: getRobloxInstallationFolder | Level: 2 [Caution]

        ```python
        current_roblox_location = OrangeAPI.getRobloxInstallFolder() # -> "/Applications/Roblox.app/"
        ```
        """
        return Request(self, "getRobloxInstallFolder").generateResponse().response   
    def getIfRobloxIsOpen(self, pid="") -> bool | None: # Permission: getIfRobloxIsOpen
        """
        This gets if Roblox is currently open using the following PID provided if got or using the latest open Roblox window.

        Permission: getIfRobloxIsOpen | Level: 1 [Warning]

        ```python
        is_roblox_opened = OrangeAPI.getIfRobloxIsOpen() # -> True
        ```
        """
        return Request(self, "getIfRobloxIsOpen", {"pid": pid}).generateResponse().response
    def getLatestRobloxPid(self) -> str | None: # Permission: getLatestRobloxPid
        """
        Get the latest Roblox window PID opened

        Permission: getLatestRobloxPid | Level: 1 [Warning]

        ```python
        roblox_pid = OrangeAPI.getLatestRobloxPid() # -> "6969"
        ```
        """
        return Request(self, "getLatestRobloxPid").generateResponse().response
    def getOpenedRobloxPids(self) -> list[str] | None: # Permission: getOpenedRobloxPids
        """
        Get all the currently opened Roblox PIDs

        Permission: getOpenedRobloxPids | Level: 1 [Warning]

        **This function is only available in OrangeAPI/Efaz's Roblox Bootstrap API v1.4.1+**

        ```python
        roblox_pids = OrangeAPI.getOpenedRobloxPids() # -> ["6969", "1234"]
        ```
        """
        return Request(self, "getOpenedRobloxPids").generateResponse().response
    def changeRobloxWindowSizeAndPosition(self, size_x: int, size_y: int, position_x: int, position_y: int) -> Response | None: # Permission: changeRobloxWindowSizeAndPosition
        """
        Change the Roblox Window Size and Position

        Permission: changeRobloxWindowSizeAndPosition | Level: 2 [Caution]

        **This function is only available in OrangeAPI/Efaz's Roblox Bootstrap API v1.4.6+**

        ```python
        response = OrangeAPI.changeRobloxWindowSizeAndPosition(400, 300, 0, 0) # -> Response
        ```
        """
        return Request(self, "changeRobloxWindowSizeAndPosition", {"size_x": size_x, "size_y": size_y, "position_x": position_x, "position_y": position_y}).generateResponse()
    def setRobloxWindowTitle(self, title: str) -> Response | None: # Permission: setRobloxWindowTitle
        """
        Set the Roblox Window Title [Windows Only]

        Permission: setRobloxWindowTitle | Level: 1 [Warning]

        **This function is only available in OrangeAPI/Efaz's Roblox Bootstrap API v1.4.6+**

        ```python
        response = OrangeAPI.setRobloxWindowTitle("Roblox - Playing GUESTY") # -> Response
        ```
        """
        return Request(self, "setRobloxWindowTitle", {"title": title}).generateResponse()
    def setRobloxWindowIcon(self, icon: str) -> Response | None: # Permission: setRobloxWindowIcon
        """
        Set the Roblox Window Icon [Windows Only]

        Permission: setRobloxWindowIcon | Level: 1 [Warning]

        **This function is only available in OrangeAPI v2.0.0+**

        ```python
        response = OrangeAPI.setRobloxWindowIcon("C:\\Users\\EfazDev\\AppData\\Local\\OrangeBlox\\Mods\\Template\\PingingRoblox.ico") # -> Response
        ```
        """
        return Request(self, "setRobloxWindowIcon", {"icon": icon}).generateResponse()
    def focusRobloxWindow(self) -> Response | None: # Permission: focusRobloxWindow
        """
        Focus the Roblox Window to the top window

        Permission: focusRobloxWindow | Level: 2 [Caution]

        **This function is only available in OrangeAPI/Efaz's Roblox Bootstrap API v1.4.6+**

        ```python
        response = OrangeAPI.focusRobloxWindow() # -> Response
        ```
        """
        return Request(self, "focusRobloxWindow").generateResponse()
    def reprepareRoblox(self) -> Response | None: # Permission: reprepareRoblox
        """
        Reprepare Roblox again if not opened. It is useful if your script has changed the user's mods.

        Permission: reprepareRoblox | Level: 2 [Caution]

        **This function is only available in OrangeAPI v2.0.0+**

        ```python
        response = OrangeAPI.reprepareRoblox() # -> Response
        ```
        """
        return Request(self, "reprepareRoblox").generateResponse()
    def sendDiscordWebhookMessage(self, title: str="Message from Mod Script", description: str=None, color: int=0, fields: list[DiscordWebhookField]=[], image: str="https://obx.efaz.dev/BootstrapImages/DiscordIcon.png") -> Response | None: # Permission: sendDiscordWebhookMessage
        """
        Send a Discord Webhook message to the user's Discord webhook!

        Permission: sendDiscordWebhookMessage | Level: 1 [Warning]

        **This function is only available in OrangeAPI v2.0.0+**

        ```python
        response = OrangeAPI.sendDiscordWebhookMessage("Hello!", "How are you today?", 65280, [OrangeAPI.DiscordWebhookField("Doing great?", "True")], "https://cdn.efaz.dev/cdn/png/logo.png") # -> Response
        ```
        """
        return Request(self, "sendDiscordWebhookMessage", {"title": title, "description": description, "color": color, "fields": fields, "image": image}).generateResponse()
    def getRobloxAppSettings(self) -> dict[str, typing.Any] | None: # Permission: getRobloxAppSettings
        """
        Get information about the Roblox client such as the logged in user, accessible polciies and settings.
        
        Permission: getRobloxAppSettings | Level: 2 [Caution]

        **This function is only available in OrangeAPI v2.0.0+**

        ```python
        app_settings = OrangeAPI.getRobloxAppSettings() # -> {
        #    "success": True, 
        #    "loggedInUser": {
        #        "id": 1078332491, 
        #        "name": "Efaazz", 
        #        "under13": False, 
        #        "displayName": "Efaz", 
        #        "countryCode": "US", 
        #        "membership": "4", 
        #        "membershipActive": True, 
        #        "theme": "dark"
        #    }, 
        #    "policyServiceResponse": {}, 
        #    "appConfiguration": {}, 
        #    "outputDeviceGUID": "", 
        #    "robloxLocaleId": "en_us"
        #}
        ```
        """
        return Request(self, "getRobloxAppSettings").generateResponse().response
    def getPlatform(self, static: bool=False) -> str: # No Permission Needed
        """
        Get the current running platform name. It may return Windows, macOS or Linux for when static is disabled. If it enabled, it will return platform.system()
        
        Permission: No Permission Needed | Level: 0 [Normal]

        ```python
        platform = OrangeAPI.getPlatform(static=False)
        if platform == "macOS":
            print("User is running macOS!")
        elif platform == "Windows":
            print("User is running Windows!")
        else:
            print("OrangeBlox is not supported by the bootstrap. How?")
        ```
        """
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
    def getDebugMode(self) -> bool: # No Permission Needed
        """
        Get if the bootstrap is in Debug Mode
        
        Permission: No Permission Needed | Level: 0 [Normal]

        ```python
        debug_mode = OrangeAPI.getDebugMode() # -> True
        ```
        """
        return debug_mode == True
    def getStudioMode(self) -> bool: # No Permission Needed
        """
        Get if the user launched Roblox Studio
        
        Permission: No Permission Needed | Level: 0 [Normal]

        ```python
        studio_mode = OrangeAPI.getStudioMode() # -> True
        ```
        """
        return studio_mode == True
    def checkIfResponseClass(self, suspected: typing.Optional[Response]) -> bool: # No Permission Needed
        """
        Check if the value you got is an Response class or just the value.

        Permission: No Permission Needed | Level: 0 [Normal]

        **This function is only available in OrangeAPI/Efaz's Roblox Bootstrap API v1.4.1+**

        ```python
        true_res = OrangeAPI.checkIfResponseClass(OrangeAPI.getLatestRobloxPid()) # -> True
        false_res = OrangeAPI.checkIfResponseClass({"a": "b"}) # -> False
        ```
        """
        if type(suspected) is Response:
            return True
        else:
            return False
    def requestInput(self, question: str, prompt: str="> ") -> str | None: # No Permission Needed
        """
        Request an input from the user with a question [Takes effect if Roblox is not launched.]
        
        Permission: No Permission Needed | Level: 0 [Normal]

        **This function is only available in OrangeAPI/Efaz's Roblox Bootstrap API v1.5.0+**

        ```python
        response = OrangeAPI.requestInput("What's your favorite ice cream?", "> ") # -> str | None
        ```
        """
        if Request(self, "getIfRobloxLaunched").generateResponse().response == False:
            print(f"\033[38;5;255m[MOD SCRIPT]: {question}\033[0m")
            return input(prompt)
        else:
            return None
    def getIfRobloxLaunched(self) -> bool | None: # No Permission Needed
        """
        Get if Roblox was launched by the bootstrap yet. [Useful for determining before interrupting the main loop]
        
        Permission: No Permission Needed | Level: 0 [Normal]

        **This function is only available in OrangeAPI/Efaz's Roblox Bootstrap API v1.5.0+**

        ```python
        is_roblox_launched = OrangeAPI.getIfRobloxLaunched() # -> False
        ```
        """
        return Request(self, "getIfRobloxLaunched").generateResponse().response
    def printMainMessage(self, mes: str) -> None: # No Permission Needed
        """
        Print a message on the python console using the bootstrap.

        Permission: No Permission Needed | Level: 0 [Normal]

        **This function is only available in OrangeAPI/Efaz's Roblox Bootstrap API v1.3.6+**

        ```python
        OrangeAPI.printMainMessage("Hello World!") # -> None
        ```
        """
        print(f"\033[38;5;255m[MOD SCRIPT]: {mes}\033[0m")
    def printColoredMessage(self, mes: str, ansi: int) -> None: # No Permission Needed
        """
        Print a message on the python console using an ANSI 256 bit color number.

        Permission: No Permission Needed | Level: 0 [Normal]

        **This function is only available in OrangeAPI v2.0.0+**

        ```python
        OrangeAPI.printColoredMessage("Hello World!", 202) # -> None
        ```
        """
        if type(ansi) is int: 
            if ansi == 202 or ansi == 208 or ansi == 166: return
            print(f"\033[38;5;{ansi}m[MOD SCRIPT]: {mes}\033[0m")
    def printErrorMessage(self, mes: str) -> None: # No Permission Needed
        """
        Print a red message on the python console using the bootstrap. [Indicates error]

        Permission: No Permission Needed | Level: 0 [Normal]

        **This function is only available in OrangeAPI/Efaz's Roblox Bootstrap API v1.3.6+**

        ```python
        OrangeAPI.printErrorMessage("Uh oh!") # -> None
        ```
        """
        print(f"\033[38;5;196m[MOD SCRIPT]: {mes}\033[0m")
    def printSuccessMessage(self, mes: str) -> None: # No Permission Needed
        """
        Print a green message on the python console using the bootstrap. [Indicates success]

        Permission: No Permission Needed | Level: 0 [Normal]

        **This function is only available in OrangeAPI/Efaz's Roblox Bootstrap API v1.3.6+**

        ```python
        OrangeAPI.printSuccessMessage("Woo!") # -> None
        ```
        """
        print(f"\033[38;5;82m[MOD SCRIPT]: {mes}\033[0m")
    def printWarnMessage(self, mes: str) -> None: # No Permission Needed
        """
        Print a yellow message on the python console using the bootstrap. [Indicates warning]
        
        Permission: No Permission Needed | Level: 0 [Normal]

        **This function is only available in OrangeAPI/Efaz's Roblox Bootstrap API v1.4.0+. For v1.3.6 Users, use OrangeAPI.printYellowMessage(mes: str)**

        ```python
        OrangeAPI.printWarnMessage("Wait!") # -> None
        ```
        """
        print(f"\033[38;5;226m[MOD SCRIPT]: {mes}\033[0m")
    def printYellowMessage(self, mes: str) -> None: # No Permission Needed
        """
        Print a yellow message on the python console using the bootstrap. [Indicates warning]
        
        Permission: No Permission Needed | Level: 0 [Normal]

        **This function is only available in OrangeAPI/Efaz's Roblox Bootstrap API v1.3.6+**

        ```python
        OrangeAPI.printWarnMessage("Wait!") # -> None
        ```
        """
        return self.printWarnMessage(mes)
    def printDebugMessage(self, mes: str) -> None: # No Permission Needed
        """
        Print a yellow message on the python console using the bootstrap IF debug mode is enabled.
        
        Permission: No Permission Needed | Level: 0 [Normal]

        **This function is only available in OrangeAPI/Efaz's Roblox Bootstrap API v1.4.0+**

        ```python
        OrangeAPI.printDebugMessage("Wait!") # -> None
        ```
        """
        if debug_mode == True: print(f"\033[38;5;226m[MOD SCRIPT]: {mes}\033[0m")
    def getConfiguration(self, name: str="*") -> dict | typing.Any | None: # No Permission Needed
        """
        Get all configurations from name "*" or one configuration from name if existing.

        Permission: No Permission Needed | Level: 0 [Normal]

        ```python
        all_configurations = OrangeAPI.getConfiguration("*") # -> {"existing": "Woah"}
        existing_configuration = OrangeAPI.getConfiguration("existing") # -> "Woah"
        non_existing_configuration = OrangeAPI.getConfiguration("non_existing") # -> None
        ```
        """
        if type(name) is str:
            return Request(self, "getConfiguration", {"name": name}).generateResponse().response
        else:
            return None
    def setConfiguration(self, name: str="*", data: typing.Union[None, str, dict, bool, int, float, list]=None) -> Response | None: # No Permission Needed
        """
        Set a configuration in a name. Values must be usable in a JSON format. If the name is a "*", the data provided must be in a dictionary like {"existing": "Woah"} for example.

        Permission: No Permission Needed | Level: 0 [Normal]

        ```python
        response = OrangeAPI.setConfiguration("existing", "Woah") # -> Response
        ```
        """
        if (data == None) or (type(data) is str) or (type(data) is dict) or (type(data) is bool) or (type(data) is int) or (type(data) is float) or (type(data) is list):
            try:
                a = json.dumps(data)
                return Request(self, "setConfiguration", {"name": name, "data": data}).generateResponse()
            except Exception as e:
                raise InvalidRequest()
        else:
            raise InvalidRequest()
    def about(self) -> dict[str, typing.Any] | None: # No Permission Needed
        """
        Get basic info about the bootstrap such as version of both API and bootstrap itself!
        
        Permission: No Permission Needed | Level: 0 [Normal]

        ```python
        response = OrangeAPI.about() # -> 
        # {
        #     "bootstrap_version": "1.3.0",
        #     "api_version": "1.3.0",
        # }
        ```
        """
        if cached_information.get("about"):
            return cached_information.get("about")
        else:
            cached_information["about"] = {"bootstrap_version": current_version["bootstrap_version"], "api_version": current_version["version"]}
            return {"bootstrap_version": current_version["bootstrap_version"], "api_version": current_version["version"]}