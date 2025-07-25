# 
# EfazRobloxBootstrapAPI
# Made by Efaz from efaz.dev
# Documentation Edition for v2.2.1
# 
# Provided to Mod Scripts using variable EfazRobloxBootstrapAPI for versions 1.5.9 or lower
# Later versions must use the OrangeAPI for documentation of features made after v1.5.9 but are allowed to use the variable in runtime.
# This version of EfazRobloxBootstrapAPI is a mapped version of OrangeAPI and redirects to OrangeAPI when used.
#
# EfazRobloxBootstrapAPI: import EfazRobloxBootstrapAPI as ERBAPI; EfazRobloxBootstrapAPI = ERBAPI.EfazRobloxBootstrapAPI()
# OrangeAPI: import OrangeAPI as orange; OrangeAPI = orange.OrangeAPI()
# 
"""
EfazRobloxBootstrapAPI | Made by Efaz from efaz.dev | Documentation Edition for v2.2.1

Provided to Mod Scripts using variable EfazRobloxBootstrapAPI for versions 1.5.9 or lower.
Later versions must use the OrangeAPI for documentation of features made after v1.5.9 but are allowed to use the variable in runtime.
This version of EfazRobloxBootstrapAPI is a mapped version of OrangeAPI and redirects to OrangeAPI when used.
```python
EfazRobloxBootstrapAPI: import EfazRobloxBootstrapAPI as ERBAPI; EfazRobloxBootstrapAPI = ERBAPI.EfazRobloxBootstrapAPI()
OrangeAPI: import OrangeAPI as orange; OrangeAPI = orange.OrangeAPI()
```
"""

from typing import Union

# Variables
current_version = {"version": "2.2.1"}
requested_functions = {}
cached_information = {}
debug_mode = False
launched_from_bootstrap = False

# Top Classes
class UnusedAPI(Warning):
    """Warning for message: This API module is a map for OrangeBlox v2.0.0+. Using this in OrangeBlox/Efaz's Roblox Bootstrap will prevent connections."""
    def __init__(self):            
        super().__init__("This API module is a map for OrangeBlox v2.0.0+. Using this in OrangeBlox/Efaz's Roblox Bootstrap will prevent connections.")
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
        raise UnusedAPI()
    def generateResponse(self):
        raise UnusedAPI()
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
        raise UnusedAPI()
class EfazRobloxBootstrapAPI:
    """
    The EfazRobloxBootstrapAPI is the API that Mod Scripts used to have before OrangeAPI v2.0.0. Please update to OrangeAPI v2.0.0 in order to stay supported.
   
    **EfazRobloxBootstrapAPI is only supported on Efaz's Roblox Bootstrap v1.3.0-v1.5.9. Any other versions like v1.2.5 or below is unable to use this API. For OrangeBlox v2.0.0+, this API replicates the OrangeAPI class.**

    ```python
    import OrangeAPI as orange; OrangeAPI = orange.OrangeAPI()
    ```
    """
    requestedFunctions = {}
    """
    ## Warning!
    This variable was moved to head in v1.4.1+ for security purposes and now returns an empty array that is not usable for communicating.
    """
    launchedFromBootstrap = False
    """
    This is a boolean variable used to indicate if the module is launched from the bootstrap or not.
    """
    debugMode = False
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
            raise UnusedAPI()
        def generate_json(self):
            """Generate a usable BloxstrapRPC JSON based on details, state, images and time."""
            raise UnusedAPI()
    
    # Functions
    def getPlatform(self, static=False): # No Permission Needed
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
        raise UnusedAPI()
    def getFastFlagConfiguration(self): # Permission: getFastFlagConfiguration
        """
        This gets the current user's FastFlagConfiguration data.

        Permission: getFastFlagConfiguration | Level: 1 [Warning]

        **The following keys are not shown due to security: EFlagDiscordWebhookURL**

        ```python
        main_config = OrangeAPI.getFastFlagConfiguration()
        print(main_config) # --> {"EFlagBlahBlah": True, "FFlagBlahBlah": "something"}
        ```
        """
        raise UnusedAPI()
    def setFastFlagConfiguration(self, configuration: dict, full: bool=False): # Permission: setFastFlagConfiguration
        """
        This sets the current user's FastFlagConfiguration data in the CURRENT running bootstrap window. This will not affect the FastFlagConfiguration.json file. The full argument means it will overwrite the full configuration if true, it will not manually add keys one at a time
        
        Permission: setFastFlagConfiguration | Level: 2 [Caution]

        ```python
        response = OrangeAPI.setFastFlagConfiguration({"EFlagDiscordWebhookRobloxAppStart": True}, False) # -> Response class
        ```
        """
        raise UnusedAPI()
    def saveFastFlagConfiguration(self, configuration: dict, full: bool=False): # Permission: saveFastFlagConfiguration
        """
        This sets the current user's FastFlagConfiguration data through the current window AND the FastFlagConfiguration.json file. The full argument means it will overwrite the full configuration if true, it will not manually add keys one at a time
        
        Permission: saveFastFlagConfiguration | Level: 2 [Caution]

        **Unless the user has recovery tools, data overwritten by this function is non-recoverable. Therefore, please check your code and make validation checks if needed! For security, EFlags keys are not able to be saved and are ignored when tried.**

        ```python
        response = OrangeAPI.saveFastFlagConfiguration({"EFlagDiscordWebhookRobloxAppStart": True}, False) # -> Response class
        ```
        """
        raise UnusedAPI()
    def displayNotification(self, title="Mod Script", message="A mod script message!"): # Permission: displayNotification
        """
        This sends a notification through the bootstrap into the current user's computer depending on the OS.
        
        Permission: displayNotification | Level: 1 [Warning]

        ```python
        response = OrangeAPI.displayNotification("Hi!", "Hello Mod Mode User!") # -> Response class
        ```
        """
        raise UnusedAPI()
    def generateModsManifest(self): # Permission: generateModsManifest
        """
        Get information about all the user's installed mods!
        
        Permission: generateModsManifest | Level: 0 [Normal]

        ```python
        mods = OrangeAPI.generateModsManifest() # -> 
        # [
        #     {
        #         "name": "My Very Own Mod!",
        #         "id": "Template",
        #         "version": "1.0.0",
        #         "mod_script": True,
        #         "mod_script_path": "/Applications/OrangeBlox.app/Contents/Resources/Mods/Template/ModScript.py",
        #         "manifest_path": "/Applications/OrangeBlox.app/Contents/Resources/Mods/Template/Manifest.py",
        #         "enabled": True,
        #         "permissions": ["onGameDisconnected", "sendBloxstrapRPC"],
        #         "python_modules": ["requests"]
        #     }
        # ]
        ```
        """
        raise UnusedAPI()
    def sendBloxstrapRPC(self, command: str="SetRichPresence", data: Union[BloxstrapRichPresence, dict, str]={}, disableWebhook=True): # Permission: sendBloxstrapRPC
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
        raise UnusedAPI()
    def getRobloxLogFolderSize(self, static=False): # Permission: getRobloxLogFolderSize
        """
        Get the current size of the Roblox Logs folder. If static mode is enabled, it will return the size of the Logs folder in bytes. Idk why would this be useful lol.

        Permission: getRobloxLogFolderSize | Level: 0 [Normal]

        ```python
        roblox_logs_size = OrangeAPI.getRobloxLogFolderSize() # -> "1 KB"
        roblox_logs_size_static = OrangeAPI.getRobloxLogFolderSize(static=True) # -> 1000
        ```
        """
        raise UnusedAPI()
    def getLatestRobloxVersion(self, channel="LIVE"): # Permission: getLatestRobloxVersion
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
        raise UnusedAPI()
    def getInstalledRobloxVersion(self): # Permission: getInstalledRobloxVersion
        """
        This gets the current Roblox version installed including the channel the user is connected to.

        Permission: getInstalledRobloxVersion | Level: 1 [Warning]

        ```python
        current_roblox_version = OrangeAPI.getInstalledRobloxVersion() # -> 
        # {
        #     "success": True, 
        #     "version": "0.666.0.566444", 
        #     "client_version": "version-56269cdb46a44048", 
        #     "channel": "LIVE"
        # }
        ```
        """
        raise UnusedAPI()
    def getRobloxInstallFolder(self): # Permission: getRobloxInstallFolder
        """
        This gets where Roblox is installed at. This may change between versions or operating systems.

        Permission: getRobloxInstallationFolder | Level: 2 [Caution]

        ```python
        current_roblox_location = OrangeAPI.getRobloxInstallFolder() # -> "/Applications/Roblox.app/"
        ```
        """
        raise UnusedAPI()
    def getIfRobloxIsOpen(self, pid=""): # Permission: getIfRobloxIsOpen
        """
        This gets if Roblox is currently open using the following PID provided if got or using the latest open Roblox window.

        Permission: getIfRobloxIsOpen | Level: 1 [Warning]

        ```python
        is_roblox_opened = OrangeAPI.getIfRobloxIsOpen() # -> True
        ```
        """
        raise UnusedAPI()
    def getLatestRobloxPid(self): # Permission: getLatestRobloxPid
        """
        Get the latest Roblox window PID opened

        Permission: getLatestRobloxPid | Level: 1 [Warning]

        ```python
        roblox_pid = OrangeAPI.getLatestRobloxPid() # -> "6969"
        ```
        """
        raise UnusedAPI()
    def getOpenedRobloxPids(self): # Permission: getOpenedRobloxPids
        """
        Get all the currently opened Roblox PIDs

        Permission: getOpenedRobloxPids | Level: 1 [Warning]

        **This function is only available in OrangeAPI v1.4.1+**

        ```python
        roblox_pids = OrangeAPI.getOpenedRobloxPids() # -> ["6969", "1234"]
        ```
        """
        raise UnusedAPI()
    def changeRobloxWindowSizeAndPosition(self, size_x: int, size_y: int, position_x: int, position_y: int): # Permission: changeRobloxWindowSizeAndPosition
        """
        Change the Roblox Window Size and Position

        Permission: changeRobloxWindowSizeAndPosition | Level: 2 [Warning]

        **This function is only available in OrangeAPI v1.4.6+**

        ```python
        response = OrangeAPI.changeRobloxWindowSizeAndPosition(400, 300, 0, 0) # -> Response
        ```
        """
        raise UnusedAPI()
    def setRobloxWindowTitle(self, title): # Permission: setRobloxWindowTitle
        """
        Set the Roblox Window Title [Windows Only]

        Permission: setRobloxWindowTitle | Level: 1 [Warning]

        **This function is only available in OrangeAPI v1.4.6+**

        ```python
        response = OrangeAPI.setRobloxWindowTitle("Roblox - Playing GUESTY") # -> Response
        ```
        """
        raise UnusedAPI()
    def focusRobloxWindow(self): # Permission: getOpenedRobloxPids
        """
        Focus the Roblox Window to the top window

        Permission: focusRobloxWindow | Level: 2 [Warning]

        **This function is only available in OrangeAPI v1.4.6+**

        ```python
        response = OrangeAPI.focusRobloxWindow() # -> Response
        ```
        """
        raise UnusedAPI()
    def getDebugMode(self): # No Permission Needed
        """
        Get if the bootstrap is in Debug Mode
        
        Permission: No Permission Needed | Level: 0 [Normal]

        ```python
        debug_mode = OrangeAPI.getDebugMode() # -> True
        ```
        """
        raise UnusedAPI()
    def checkIfResponseClass(self, suspected): # No Permission Needed
        """
        Check if the value you got is an Response class or just the value.

        Permission: No Permission Needed | Level: 0 [Normal]

        **This function is only available in OrangeAPI v1.4.1+**

        ```python
        true_res = OrangeAPI.checkIfResponseClass(OrangeAPI.getLatestRobloxPid()) # -> True
        false_res = OrangeAPI.checkIfResponseClass({"a": "b"}) # -> False
        ```
        """
        raise UnusedAPI()
    def requestInput(self, question, prompt: str="> "): # No Permission Needed
        """
        Request an input from the user with a question [Takes effect if Roblox is not launched.]
        
        Permission: No Permission Needed | Level: 0 [Normal]

        **This function is only available in OrangeAPI v1.5.0+**

        ```python
        response = OrangeAPI.requestInput("What's your favorite ice cream?", "> ") # -> str | None
        ```
        """
        raise UnusedAPI()
    def getIfRobloxLaunched(self): # No Permission Needed
        """
        Get if Roblox was launched by the bootstrap yet. [Useful for determining before interrupting the main loop]
        
        Permission: No Permission Needed | Level: 0 [Normal]

        **This function is only available in OrangeAPI v1.5.0+**

        ```python
        is_roblox_launched = OrangeAPI.getIfRobloxLaunched() # -> False
        ```
        """
        raise UnusedAPI()
    def getRobloxAppSettings(self): # Permission: getRobloxAppSettings
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
        raise UnusedAPI()
    def printMainMessage(self, mes): # No Permission Needed
        """
        Print a message on the python console using the bootstrap.

        Permission: No Permission Needed | Level: 0 [Normal]

        **This function is only available in OrangeAPI v1.3.6+**

        ```python
        OrangeAPI.printMainMessage("Hello World!") # -> None
        ```
        """
        raise UnusedAPI()
    def printErrorMessage(self, mes): # No Permission Needed
        """
        Print a red message on the python console using the bootstrap. [Indicates error]

        Permission: No Permission Needed | Level: 0 [Normal]

        **This function is only available in OrangeAPI v1.3.6+**

        ```python
        OrangeAPI.printErrorMessage("Uh oh!") # -> None
        ```
        """
        raise UnusedAPI()
    def printSuccessMessage(self, mes): # No Permission Needed
        """
        Print a green message on the python console using the bootstrap. [Indicates success]

        Permission: No Permission Needed | Level: 0 [Normal]

        **This function is only available in OrangeAPI v1.3.6+**

        ```python
        OrangeAPI.printSuccessMessage("Woo!") # -> None
        ```
        """
        raise UnusedAPI()
    def printWarnMessage(self, mes): # No Permission Needed
        """
        Print a yellow message on the python console using the bootstrap. [Indicates warning]
        
        Permission: No Permission Needed | Level: 0 [Normal]

        **This function is only available in OrangeAPI v1.4.0+. For v1.3.6 Users, use OrangeAPI.printYellowMessage(mes: str)**

        ```python
        OrangeAPI.printWarnMessage("Wait!") # -> None
        ```
        """
        raise UnusedAPI()
    def printYellowMessage(self, mes): # No Permission Needed
        """
        Print a yellow message on the python console using the bootstrap. [Indicates warning]
        
        Permission: No Permission Needed | Level: 0 [Normal]

        **This function is only available in OrangeAPI v1.3.6+**

        ```python
        OrangeAPI.printWarnMessage("Wait!") # -> None
        ```
        """
        raise UnusedAPI()
    def printDebugMessage(self, mes): # No Permission Needed
        """
        Print a yellow message on the python console using the bootstrap IF debug mode is enabled.
        
        Permission: No Permission Needed | Level: 0 [Normal]

        **This function is only available in OrangeAPI v1.4.0+**

        ```python
        OrangeAPI.printDebugMessage("Wait!") # -> None
        ```
        """
        raise UnusedAPI()
    def getConfiguration(self, name: str="*"): # No Permission Needed
        """
        Get all configurations from name "*" or one configuration from name if existing.

        Permission: No Permission Needed | Level: 0 [Normal]

        ```python
        all_configurations = OrangeAPI.getConfiguration("*") # -> {"existing": "Woah"}
        existing_configuration = OrangeAPI.getConfiguration("existing") # -> "Woah"
        non_existing_configuration = OrangeAPI.getConfiguration("non_existing") # -> None
        ```
        """
        raise UnusedAPI()
    def setConfiguration(self, name: str="*", data=None): # No Permission Needed
        """
        Set a configuration in a name. Values must be usable in a JSON format. If the name is a "*", the data provided must be in a dictionary like {"existing": "Woah"} for example.

        Permission: No Permission Needed | Level: 0 [Normal]

        ```python
        response = OrangeAPI.setConfiguration("existing", "Woah") # -> Response
        ```
        """
        raise UnusedAPI()
    def about(self): # No Permission Needed
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
        raise UnusedAPI()
import OrangeAPI as orange
OrangeAPI = orange.OrangeAPI