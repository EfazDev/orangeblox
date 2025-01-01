import os
import platform
import json
import subprocess
import time
import datetime
import threading
import re
import sys

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
def printDebugMessage(mes): print(f"\033[38;5;226m[Roblox FFlag Installer] [DEBUG]: {mes}\033[0m")
def isYes(text): return text.lower() == "y" or text.lower() == "yes"
def isNo(text): return text.lower() == "n" or text.lower() == "no"
def isRequestClose(text): return text.lower() == "exit" or text.lower() == "exit()"
if os.path.exists("FastFlagConfiguration.json") and os.path.exists("Main.py") and os.path.exists("PipHandler.py"):
    efaz_bootstrap_mode = True
fast_flag_installer_version = "1.7.5"

class pip:
    executable = None
    def __init__(self, command: list=[], executable: str=None):
        import sys
        import os
        import subprocess
        if type(executable) is str:
            if os.path.isfile(executable):
                self.executable = executable
            else:
                if getattr(sys, "frozen", False):
                    self.executable = self.findPython()
                else:
                    self.executable = sys.executable
        else:
            if getattr(sys, "frozen", False):
                self.executable = self.findPython()
            else:
                self.executable = sys.executable
        if type(command) is list and len(command) > 0:
            subprocess.check_call([self.executable, "-m", "pip"] + command)
    def install(self, packages: list[str]):
        import subprocess
        res = {}
        generated_list = []
        for i in packages:
            if type(i) is str:
                generated_list.append(i)
        if len(generated_list) > 0:
            try:
                subprocess.check_call([self.executable, "-m", "pip", "install"] + generated_list)
                res[i] = {"success": True}
            except Exception as e:
                res[i] = {"success": False}
        return res
    def uninstall(self, packages: list[str]):
        import subprocess
        res = {}
        generated_list = []
        for i in packages:
            if type(i) is str:
                generated_list.append(i)
        if len(generated_list) > 0:
            try:
                subprocess.check_call([self.executable, "-m", "pip", "uninstall"] + generated_list)
                res[i] = {"success": True}
            except Exception as e:
                res[i] = {"success": False}
        return res
    def installed(self, packages: list[str]):
        import importlib
        installed = {}
        all_installed = True
        for i in packages:
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
        if self.findPython():
            return True
        else:
            return False
    def pythonInstall(self):
        import subprocess
        import platform
        import tempfile
        ma_os = platform.system()
        ma_arch = platform.architecture()
        ma_processor = platform.machine()
        if ma_os == "Darwin":
            url = "https://www.python.org/ftp/python/3.13.0/python-3.13.0-macos11.pkg"
            pkg_file_path = tempfile.mktemp(suffix=".pkg")
            result = subprocess.run(["curl", "-o", pkg_file_path, url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)            
            if result.returncode == 0:
                subprocess.run(["open", pkg_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                print(f"Python installer has been executed: {pkg_file_path}")
            else:
                print("Failed to download Python installer.")
        elif ma_os == "Windows":
            if ma_arch[0] == "64bit":
                if ma_processor.lower() == "arm64":
                    url = "https://www.python.org/ftp/python/3.13.0/python-3.13.0-arm64.exe"
                else:
                    url = "https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe"
            else:
                url = "https://www.python.org/ftp/python/3.13.0/python-3.13.0.exe"
            exe_file_path = tempfile.mktemp(suffix=".exe")
            result = subprocess.run(["curl", "-o", exe_file_path, url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)            
            if result.returncode == 0:
                subprocess.run([exe_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                print(f"Python installer has been executed: {exe_file_path}")
            else:
                print("Failed to download Python installer.")
    def getLocalAppData(self):
        import platform
        import os
        ma_os = platform.system()
        if ma_os == "Windows":
            return os.path.expandvars(r'%LOCALAPPDATA%')
        elif ma_os == "Darwin":
            return f'{os.path.expanduser("~")}/Library/'
        else:
            return f'{os.path.expanduser("~")}/'
    def restartScript(self, argv: list):
        import sys
        import subprocess
        subprocess.run([self.findPython()] + argv, shell=True)
        sys.exit(0)
    def importModule(self, module_name: str, install_module_if_not_found: bool=False):
        import importlib
        import subprocess
        try:
            return importlib.import_module(module_name)
        except ModuleNotFoundError:
            try:
                if install_module_if_not_found == True: self.install([module_name])
                return importlib.import_module(module_name)
            except subprocess.CalledProcessError as e:
                raise ImportError(f'Unable to find module "{module_name}" in Python environment.')
    def getIfProcessIsOpened(self, process_name="", pid=""):
        import platform
        import subprocess
        ma_os = platform.system()
        if ma_os == "Windows":
            process = subprocess.Popen(["tasklist"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, _ = process.communicate()
            process_list = output.decode("utf-8")

            if pid == "" or pid == None:
                if process_list.rfind(process_name) == -1:
                    return False
                else:
                    return True
            else:
                if process_list.rfind(pid) == -1:
                    return False
                else:
                    return True
        else:
            if pid == "" or pid == None:
                if subprocess.run(f"pgrep -f '{process_name}' > /dev/null 2>&1", shell=True).returncode == 0:
                    return True
                else:
                    return False
            else:
                if subprocess.run(f"ps -p {pid} > /dev/null 2>&1", shell=True).returncode == 0:
                    return True
                else:
                    return False
    def getProcessWindows(self, pid: int):
        import platform
        if (type(pid) is str and pid.isnumeric()) or type(pid) is int:
            if platform.system() == "Windows":
                try:
                    import win32gui # type: ignore
                    import win32process # type: ignore
                except Exception as e:
                    self.install(["pywin32"])
                    import win32gui # type: ignore
                    import win32process # type: ignore
                system_windows = []
                def callback(hwnd, _):
                    if win32gui.IsWindowVisible(hwnd):
                        _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
                        if window_pid == int(pid):
                            system_windows.append(hwnd)
                win32gui.EnumWindows(callback, None)
                return system_windows
            elif platform.system() == "Darwin":
                try:
                    from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly
                except Exception as e:
                    self.install(["pyobjc"])
                    from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly
                system_windows = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, 0)
                app_windows = [win for win in system_windows if win.get("kCGWindowOwnerPID") == int(pid)]
                new_set_of_system_windows = []
                for win in app_windows:
                    if win and win.get("kCGWindowOwnerPID"):
                        new_set_of_system_windows.append(win)
                return new_set_of_system_windows
            else:
                return []
        else:
            return []
    def findPython(self):
        import os
        import glob
        import platform
        ma_os = platform.system()
        ma_arch = platform.architecture()
        if ma_os == "Darwin":
            if os.path.exists("/usr/local/bin/python3") and os.path.islink("/usr/local/bin/python3"):
                return "/usr/local/bin/python3"
            else:
                paths = [
                    "/usr/local/bin/python*",
                    "/Library/Frameworks/Python.framework/Versions/*/bin/python*",
                    "~/Library/Python/*/bin/python*"
                ]
                for path_pattern in paths:
                    for path in glob.glob(path_pattern):
                        if os.path.isfile(path):
                            if not (ma_arch[1].lower() == "arm64" and "intel64" in path):
                                return path
                return None
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
                        return path
            return None
class Main:
    # System Functions
    def __init__(self):
        self.__main_os__ = main_os
    robloxInstanceEventNames = [
        "onRobloxExit", 
        "onRobloxLog",
        "onRobloxSharedLogLaunch",
        "onRobloxAppStart", 
        "onRobloxAppLoginFailed", 
        "onRobloxPassedUpdate", 
        "onBloxstrapSDK", 
        "onLoadedFFlags", 
        "onHttpResponse", 
        "onOtherRobloxLog",
        "onRobloxCrash",
        "onRobloxChannel",
        "onRobloxTerminateInstance",
        "onGameStart", 
        "onGameLoading", 
        "onGameLoadingNormal", 
        "onGameLoadingPrivate", 
        "onGameLoadingReserved", 
        "onGameLoadingParty", 
        "onGameUDMUXLoaded", 
        "onGameAudioDeviceAvailable",
        "onGameTeleport", 
        "onGameTeleportFailed", 
        "onGameJoinInfo", 
        "onGameJoined", 
        "onGameLeaving", 
        "onGameDisconnected",
        "onRobloxVoiceChatMute",
        "onRobloxVoiceChatUnmute",
        "onRobloxVoiceChatStart",
        "onRobloxVoiceChatLeft",
        "onRobloxAudioDeviceStopRecording",
        "onRobloxAudioDeviceStartRecording",
    ]
    robloxInstanceEventInfo = {
        # 0 = Safe, 1 = Caution, 2 = Warning, 3 = Dangerous
        "onRobloxExit": {"message": "Allow detecting when Roblox closes", "level": 0, "robloxEvent": True}, 
        "onRobloxLog": {"message": "Allow detecting every Roblox event", "level": 3, "robloxEvent": True},
        "onRobloxSharedLogLaunch": {"message": "Allow detecting when Roblox was closed by the module due to a shared launch", "level": 2, "robloxEvent": True},
        "onRobloxLauncherDestroyed": {"message": "Allow detecting when the Roblox Launcher is destroyed", "level": 0, "robloxEvent": True},
        "onRobloxAppStart": {"message": "Allow detecting when Roblox starts", "level": 0, "robloxEvent": True}, 
        "onRobloxAppLoginFailed": {"message": "Allow detecting when Roblox logging in fails", "level": 0, "robloxEvent": True},
        "onRobloxPassedUpdate": {"message": "Allow detecting when Roblox passes update checks", "level": 0, "robloxEvent": True}, 
        "onBloxstrapSDK": {"message": "Allow detecting when BloxstrapRPC is triggered", "level": 1, "robloxEvent": True}, 
        "onLoadedFFlags": {"message": "Allow detecting when FFlags are loaded", "level": 0, "robloxEvent": True}, 
        "onHttpResponse": {"message": "Allow detecting when Roblox HttpResponses are ran", "level": 2, "robloxEvent": True}, 
        "onOtherRobloxLog": {"message": "Allow detecting when Unknown Roblox Handlers are detected", "level": 3, "robloxEvent": True},
        "onRobloxCrash": {"message": "Allow detecting when Roblox crashes", "level": 1, "robloxEvent": True},
        "onRobloxChannel": {"message": "Allow detecting the current Roblox channel", "level": 0, "robloxEvent": True},
        "onRobloxTerminateInstance": {"message": "Allow detecting when Roblox closes an extra window.", "level": 1, "robloxEvent": True},
        "onGameStart": {"message": "Allow getting Job ID, Place ID and Roblox IP", "level": 2, "robloxEvent": True}, 
        "onGameLoading": {"message": "Allow detecting when loading any server", "level": 1, "robloxEvent": True}, 
        "onGameLoadingNormal": {"message": "Allow detecting when loading public server", "level": 1, "robloxEvent": True}, 
        "onGameLoadingPrivate": {"message": "Allow detecting when loading private server", "level": 2, "robloxEvent": True}, 
        "onGameLoadingReserved": {"message": "Allow detecting when loading reserved server", "level": 2, "robloxEvent": True},
        "onGameLoadingParty": {"message": "Allow detecting when loading party", "level": 1, "robloxEvent": True}, 
        "onRobloxVoiceChatMute": {"message": "Detect when you mute your microphone during your Roblox Voice Chat", "level": 1, "robloxEvent": True}, 
        "onRobloxVoiceChatUnmute": {"message": "Detect when you unmute your microphone during your Roblox Voice Chat", "level": 1, "robloxEvent": True}, 
        "onRobloxVoiceChatStart": {"message": "Detect when Voice Chats on the client start", "level": 1, "robloxEvent": True}, 
        "onRobloxVoiceChatLeft": {"message": "Detect when Voice Chats on the client end", "level": 1, "robloxEvent": True},
        "onRobloxAudioDeviceStartRecording": {"message": "Allow detecting when a game audio device starts recording.", "level": 1, "robloxEvent": True},
        "onRobloxAudioDeviceStopRecording": {"message": "Allow detecting when a game audio device stops recording.", "level": 1, "robloxEvent": True},
        "onGameAudioDeviceAvailable": {"message": "Allow detecting when a new game audio device is available.", "level": 1, "robloxEvent": True},
        "onGameUDMUXLoaded": {"message": "Allow detecting when Roblox Server IPs are loaded", "level": 2, "robloxEvent": True}, 
        "onGameTeleport": {"message": "Allow detecting when you teleport places", "level": 1, "robloxEvent": True}, 
        "onGameTeleportFailed": {"message": "Allow detecting when teleporting fails", "level": 1, "robloxEvent": True}, 
        "onGameJoinInfo": {"message": "Allow getting join info for a game", "level": 2, "robloxEvent": True}, 
        "onGameJoined": {"message": "Allow detecting when Roblox loads a game fully", "level": 0, "robloxEvent": True}, 
        "onGameLeaving": {"message": "Allow detecting when you leave a game", "level": 0, "robloxEvent": True}, 
        "onGameDisconnected": {"message": "Allow detecting when you disconnect from a game", "level": 0, "robloxEvent": True},

        # Efaz's Roblox Bootstrap Permissions
        "fastFlagConfiguration": {"message": "Edit or view your bootstrap configuration file", "level": 3, "detection": "FastFlagConfiguration.json"},
        "editMainExecutable": {"message": "Edit the main bootstrap executable", "level": 4, "detection": "Main.py"},
        "editRobloxFastFlagInstallerExecutable": {"message": "Edit the RobloxFastFlagInstaller executable", "level": 4, "detection": "RobloxFastFlagInstaller.py"},
        "editEfazRobloxBootstrapAPIExecutable": {"message": "Edit the EfazRobloxBootstrapAPI executable", "level": 4, "detection": "EfazRobloxBootstrapAPI.py"},
        "editModScript": {"message": "Edit ModScript.py executable", "level": 4, "detection": "ModScript.py"},
        "notifications": {"message": "Configure or send notifications through Bootstrap", "level": 1, "detection": "AppNotification"},
        "configureModModes": {"message": "Configure your mod modes", "level": 2, "detection": "Mods"},
        "configureRobloxBranding": {"message": "Configure your Roblox client's branding", "level": 1, "detection": "RobloxBrand"},
        "importOtherModules": {"message": "Import outside modules from source", "level": 2, "detection": "importlib"},
        "runOtherScripts": {"message": "Run other scripts or commands", "level": 2, "detection": "subprocess"},
        "configureDeathSounds": {"message": "Configure your death sounds", "level": 1, "detection": "DeathSounds"},
        "configureCursors": {"message": "Configure your cursors", "level": 1, "detection": "Cursors"},
        "configureAvatarMaps": {"message": "Configure your avatar maps", "level": 1, "detection": "AvatarEditorMaps"},
        "generateModsManifest": {"message": "Get information about all your installed mods", "level": 0},
        "displayNotification": {"message": "Send notifications through the bootstrap", "level": 1},
        "getRobloxLogFolderSize": {"message": "Get current size of the Roblox Logs folder", "level": 0},
        "grantFileEditing": {"message": "Grant permissions to read/edit other files", "level": 3},
        "allowAccessingPythonFiles": {"message": "Allow access to other Python files", "level": 2},
        "sendBloxstrapRPC": {"message": "Send requests through Bloxstrap RPC", "level": 2},
        "getLatestRobloxVersion": {"message": "Get the latest Roblox version", "level": 0},
        "getInstalledRobloxVersion": {"message": "Get the currently installed Roblox version", "level": 1},
        "getRobloxInstallationFolder": {"message": "Get the Roblox installation folder", "level": 2},
        "getIfRobloxIsOpen": {"message": "Get if the Roblox client is open", "level": 1},
        "getFastFlagConfiguration": {"message": "View your bootstrap configuration file", "level": 1},
        "setFastFlagConfiguration": {"message": "Set your bootstrap configuration within executable", "level": 2},
        "saveFastFlagConfiguration": {"message": "Edit and save your bootstrap configuration file", "level": 2},
        "getIfRobloxLaunched": {"message": "Get if Roblox has launched from the bootstrap", "level": 0, "free": True},
        "getLatestRobloxPid": {"message": "Get the current latest Roblox window's PID", "level": 1},
        "getOpenedRobloxPids": {"message": "Get all the currently opened Roblox PIDs", "level": 1},
        "changeRobloxWindowSizeAndPosition": {"message": "Change the Roblox Window Size and Position", "level": 2},
        "setRobloxWindowTitle": {"message": "Set the Roblox Window Title [Windows Only]", "level": 1},
        "focusRobloxWindow": {"message": "Focus the Roblox Window to the top window", "level": 2},
        "getConfiguration": {"message": "Get data in a separate configuration", "level": 0, "free": True},
        "setConfiguration": {"message": "Store data in a separate configuration", "level": 0, "free": True},
        "getDebugMode": {"message": "Get if the bootstrap is in Debug Mode", "level": 0, "free": True},
        "printSuccessMessage": {"message": "Print a console in green (indicates success)", "level": 0, "free": True},
        "printMainMessage": {"message": "Print a console in the standard white color", "level": 0, "free": True},
        "printErrorMessage": {"message": "Print a console in red (indicates an error)", "level": 0, "free": True},
        "printYellowMessage": {"message": "Print a console in a yellow text (indicates a warning)", "level": 0, "free": True},
        "about": {"message": "Get bootstrap info", "level": 0, "free": True},
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
        await_20_second_log_creation = False
        await_log_creation_attempts = 0
        windows_roblox_starter_launched_roblox = False
        class __ReadingLineResponse__():
            class EndRoblox(): code=0
            class EndWatchdog(): code=1
        class InvalidRobloxHandlerException(Exception):
            def __init__(self):            
                super().__init__("Please make sure you're providing the RobloxFastFlagsInstaller.Main class!")
        def __init__(self, main_handler, pid: str, log_file: str="", debug_mode: bool=False, allow_other_logs: bool=False, await_20_second_log_creation=False, created_mutex=None):
            if type(main_handler) is Main:
                self.main_handler = main_handler
                self.event_names = main_handler.robloxInstanceEventNames
                self.pid = pid
                self.debug_mode = debug_mode
                self.allow_other_logs = allow_other_logs
                self.created_mutex = created_mutex
                self.await_20_second_log_creation = await_20_second_log_creation
                if log_file == "" or os.path.exists(log_file):
                    self.main_log_file = log_file
                self.startActivityTracking()
            else:
                raise self.InvalidRobloxHandlerException()
        def awaitRobloxClosing(self):
            while True:
                time.sleep(1)
                if not self.pid:
                    self.ended_process = True
                    break
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
        def getWindowsOpened(self) -> "list[Main.RobloxWindow]":
            if self.pid and not (self.pid == "") and self.pid.isnumeric():
                try:
                    if main_os == "Windows":
                        try:
                            import win32gui # type: ignore
                            import win32process # type: ignore
                        except Exception as e:
                            pip().install(["pywin32"])
                            import win32gui # type: ignore
                            import win32process # type: ignore
                        system_windows = []
                        def callback(hwnd, _):
                            if win32gui.IsWindowVisible(hwnd):
                                _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
                                if window_pid == int(self.pid):
                                    system_windows.append(hwnd)
                        win32gui.EnumWindows(callback, None)
                        roblox_windows_classes = []
                        for i in system_windows:
                            roblox_windows_classes.append(self.main_handler.RobloxWindow(self.pid, i))
                        return roblox_windows_classes
                    elif main_os == "Darwin":
                        try:
                            from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly
                        except Exception as e:
                            pip().install(["pyobjc"])
                            from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly
                        system_windows = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, 0)
                        app_windows = [win for win in system_windows if win.get("kCGWindowOwnerPID") == int(self.pid)]
                        new_set_of_system_windows = []
                        for win in app_windows:
                            if win and win.get("kCGWindowOwnerPID"):
                                new_set_of_system_windows.append(win)
                        roblox_windows_classes = []
                        for i in new_set_of_system_windows:
                            roblox_windows_classes.append(self.main_handler.RobloxWindow(self.pid, i))
                        return roblox_windows_classes
                    else:
                        return []
                except Exception as e:
                    return []
            else:
                return []
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
                        passed_lines = []
                        def newest(path):
                            files = os.listdir(path)
                            paths = []
                            for basename in files:
                                if "Player" in basename:
                                    paths.append(os.path.join(path, basename))
                            return max(paths, key=os.path.getctime)
                        def fileCreatedRecently(file_path):
                            try:
                                creation_time = os.path.getctime(file_path)
                                current_time = time.time()
                                if (current_time - creation_time) <= 20:
                                    return True
                                else:
                                    return False
                            except:
                                return False
                        def submitToThread(eventName="onUnknownEvent", data=None, isLine=True):
                            if not (eventName == "onRobloxLog"): 
                                submitToThread(eventName="onRobloxLog", data={"eventName": eventName, "data": data, "isLine": isLine}, isLine=False)
                                if isLine == True:
                                    if self.debug_mode == True and not (eventName == "onOtherRobloxLog" and self.allow_other_logs == False): printDebugMessage(f'Event triggered: {eventName}, Line: {data}')
                                else:
                                    if self.debug_mode == True: printDebugMessage(f'Event triggered: {eventName}, Data: {data}')
                            for i in self.events:
                                if i and callable(i.get("callback")) and i.get("name") == eventName: threading.Thread(target=i.get("callback"), args=[data]).start()
                        def handleLine(line=""):
                            if "[FLog::RobloxStarter] RobloxStarter destroyed" in line:
                                if self.windows_roblox_starter_launched_roblox == False:
                                    submitToThread(eventName="onRobloxExit", data=line)
                                    submitToThread(eventName="onRobloxSharedLogLaunch", data=line)
                                    return self.__ReadingLineResponse__.EndWatchdog()
                                else:
                                    submitToThread(eventName="onRobloxLauncherDestroyed", data=line)
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
                            elif "[FLog::GameJoinUtil] GameJoinUtil::initiateTeleportToPlace" in line:
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
                            elif '"partyId":' in line:
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
                            elif "[FLog::Audio] InputDevice" in line:
                                def generate_arg():
                                    pattern = re.compile(
                                        r'(?P<timestamp>[^\s]+),(?P<unknown_value>[^\s]+),(?P<unknown_hex>[^\s]+),(?P<unknown_number>[^\s]+) \[FLog::Audio\] InputDevice (?P<device_index>\d+): (?P<device_name>[^()]+)\(\{(?P<device_id>[0-9a-fA-F-]+)\}\) (?P<connections>\d+/\d+/\d+)'
                                    )
                                    match = pattern.search(line)
                                    if not match:
                                        return None
                                    data = match.groupdict()
                                    result = {
                                        "device_name": data.get("device_name"),
                                        "device_uuid": data.get("device_id"),
                                        "device_index": int(data.get("device_index")),
                                        "connection_divisons": data.get("connections")
                                    }
                                    return result
                                generated_data = generate_arg()
                                if generated_data:
                                    submitToThread(eventName="onGameAudioDeviceAvailable", data=generated_data, isLine=False)
                            elif "[FLog::ClientRunInfo] The channel is " in line:
                                def generate_arg():
                                    pattern = re.compile(
                                        r'(?P<timestamp>[^\s]+),(?P<unknown_value>[^\s]+),(?P<unknown_hex>[^\s]+),(?P<unknown_number>[^\s]+) \[FLog::ClientRunInfo\] The channel is (?P<channel>\w+)'
                                    )
                                    match = pattern.search(line)
                                    if not match:
                                        return None
                                    data = match.groupdict()
                                    result = {
                                        "channel": data.get("channel")
                                    }
                                    if result["channel"] == "production": result["channel"] = "LIVE"
                                    return result
                                generated_data = generate_arg()
                                if generated_data:
                                    submitToThread(eventName="onRobloxChannel", data=generated_data, isLine=False)
                                    self.windows_roblox_starter_launched_roblox = True
                            elif "[FLog::Warning] WebLogin authentication is failed and App is quitting" in line:
                                submitToThread(eventName="onRobloxAppLoginFailed", data=line, isLine=True)
                            elif "[FLog::UgcExperienceController] UgcExperienceController: doTeleport: joinScriptUrl" in line:
                                submitToThread(eventName="onGameTeleport", data=line, isLine=True)
                            elif "raiseTeleportInitFailedEvent" in line:
                                submitToThread(eventName="onGameTeleportFailed", data=line, isLine=True)
                            elif "RobloxAudioDevice::SetMicrophoneMute true" in line:
                                submitToThread(eventName="onRobloxVoiceChatMute", data=line, isLine=True)
                            elif "RobloxAudioDevice::SetMicrophoneMute false" in line:
                                submitToThread(eventName="onRobloxVoiceChatUnmute", data=line, isLine=True)
                            elif "VoiceChatSession::leave" in line and "leaveRequested:1" in line:
                                submitToThread(eventName="onRobloxVoiceChatLeft", data=line, isLine=True)
                            elif "VoiceChatSession::publishStart - JoinProfiling" in line:
                                submitToThread(eventName="onRobloxVoiceChatStart", data=line, isLine=True)
                            elif "RobloxAudioDevice::StopRecording" in line:
                                submitToThread(eventName="onRobloxAudioDeviceStopRecording", data=line, isLine=True)
                            elif "RobloxAudioDevice::StartRecording" in line:
                                submitToThread(eventName="onRobloxAudioDeviceStartRecording", data=line, isLine=True)
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
                                                "isTeleport": None,
                                                "followUserId": None
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
                            elif "RBXCRASH:" in line or "[FLog::CrashReportLog] Terminated" in line:
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
                                        threading.Thread(target=b, daemon=True).start()
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
                            self.await_log_creation_attempts = 0
                            def getLogFile():
                                logs_path = None
                                if main_os == "Darwin":
                                    logs_path = f'{os.path.expanduser("~")}/Library/Logs/Roblox/'
                                elif main_os == "Windows":
                                    logs_path = f'{windows_dir}\\logs\\'
                                else:
                                    logs_path = f'{os.path.expanduser("~")}/Library/Logs/Roblox/'
                                main_log = newest(logs_path)
                                if not main_log.endswith(".log"):
                                    time.sleep(0.5)
                                    return getLogFile()
                                if self.await_20_second_log_creation == True:
                                    logs_attached = []
                                    if os.path.exists("RobloxFastFlagLogFilesAttached.json"):
                                        with open("RobloxFastFlagLogFilesAttached.json", "r") as f:
                                            logs_attached = json.load(f)
                                    if self.await_log_creation_attempts < 40:
                                        if fileCreatedRecently(main_log):
                                            if main_log in logs_attached:
                                                time.sleep(0.5)
                                                self.await_log_creation_attempts += 1
                                                return getLogFile()
                                            else:
                                                logs_attached.append(main_log)
                                                with open("RobloxFastFlagLogFilesAttached.json", "w") as f:
                                                    json.dump(logs_attached, f, indent=4)
                                                return main_log
                                        else:
                                            time.sleep(0.5)
                                            self.await_log_creation_attempts += 1
                                            return getLogFile()
                                    else:
                                        return main_log
                                else:
                                    return main_log
                            main_log = getLogFile()
                            self.main_log_file = main_log
                        else:
                            main_log = self.main_log_file

                        with open(main_log, "r", encoding="utf-8", errors="ignore") as file:
                            def cleanLogs():
                                if self.debug_mode == True: printDebugMessage(f"Cleaning logs from session..")
                                with open(main_log, "r", encoding="utf-8", errors="ignore") as file:
                                    lines = file.readlines()
                                with open(main_log, "w", encoding="utf-8", errors="ignore") as write_file:
                                    end_lines = []
                                    current_log = ""
                                    for line in lines:
                                        should_remove = False
                                        f_index = line.find("[F")
                                        if f_index != -1:
                                            filtered_line = line[f_index:]
                                            if filtered_line == current_log:
                                                should_remove = True
                                            elif "[FLog::WndProcessCheck]" in line:
                                                should_remove = True
                                            elif "[FLog::FMOD] FMOD API error" in line:
                                                should_remove = True
                                            else:
                                                current_log = filtered_line
                                        if should_remove == False: end_lines.append(line)
                                    write_file.writelines(end_lines)
                            while True:
                                line = file.readline()
                                if not line:
                                    threading.Thread(target=cleanLogs).start()
                                    break
                                if self.ended_process == True:
                                    submitToThread(eventName="onRobloxExit", data=line)
                                    return
                                if not (line in passed_lines):
                                    timestamp_str = line.split(",")
                                    if len(timestamp_str) > 0:
                                        timestamp_str = timestamp_str[0]
                                        if re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z", timestamp_str):
                                            timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                                            current_time = datetime.datetime.now(datetime.timezone.utc)
                                            if timestamp:
                                                age_in_seconds = int(current_time.timestamp() - timestamp.timestamp())
                                                if age_in_seconds < 60:
                                                    res = handleLine(line)
                                                    if res:
                                                        if res.code == 0:
                                                            threading.Thread(target=cleanLogs).start()
                                                            break
                                                        elif res.code == 1:
                                                            self.ended_process = True
                                                            return
                                    else:
                                        res = handleLine(line)
                                        if res:
                                            if res.code == 0:
                                                self.ended_process = True
                                                threading.Thread(target=cleanLogs).start()
                                                break     
                                            elif res.code == 1:
                                                self.ended_process = True
                                                return
                            file.seek(0, os.SEEK_END)
                            while True:
                                line = file.readline()
                                if self.ended_process == True:
                                    submitToThread(eventName="onRobloxExit", data=line)
                                    threading.Thread(target=cleanLogs).start()
                                    break
                                if not line:
                                    time.sleep(0.01)
                                    continue
                                if not (line in passed_lines):
                                    timestamp_str = line.split(",")
                                    if len(timestamp_str) > 0:
                                        timestamp_str = timestamp_str[0]
                                        if re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z", timestamp_str):
                                            timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                                            current_time = datetime.datetime.now(datetime.timezone.utc)
                                            if timestamp:
                                                age_in_seconds = int(current_time.timestamp() - timestamp.timestamp())
                                                if age_in_seconds < 60:
                                                    res = handleLine(line)
                                                    if res:
                                                        if res.code == 0:
                                                            self.ended_process = True
                                                            threading.Thread(target=cleanLogs).start()
                                                            break     
                                                        elif res.code == 1:
                                                            self.ended_process = True
                                                            return  
                                        else:
                                            res = handleLine(line)
                                            if res:
                                                if res.code == 0:
                                                    self.ended_process = True
                                                    threading.Thread(target=cleanLogs).start()
                                                    break     
                                                elif res.code == 1:
                                                    self.ended_process = True
                                                    return
                                    else:
                                        res = handleLine(line)
                                        if res:
                                            if res.code == 0:
                                                self.ended_process = True
                                                threading.Thread(target=cleanLogs).start()
                                                break     
                                            elif res.code == 1:
                                                self.ended_process = True
                                                return                           
                threading.Thread(target=watchDog).start()
                threading.Thread(target=self.awaitRobloxClosing).start()
    class RobloxWindow():
        pid = None
        system_handler = None
        def __init__(self, pid, system_handler):
            self.pid = pid
            self.system_handler = system_handler
        def focusWindow(self):
            if main_os == "Windows":
                try:
                    import win32gui # type: ignore
                    import win32process # type: ignore
                except Exception as e:
                    pip().install(["pywin32"])
                    import win32gui # type: ignore
                    import win32process # type: ignore
                win32gui.SetFocus(self.system_handler)
            elif main_os == "Darwin":
                import subprocess
                subprocess.run(["osascript", "-e", f'tell application "System Events" to set frontmost of (every process whose unix id is {self.pid}) to true'])
        def setWindowTitle(self, title):
            if main_os == "Windows":
                try:
                    import win32gui # type: ignore
                except Exception as e:
                    pip().install(["pywin32"])
                    import win32gui # type: ignore
                win32gui.SetWindowText(self.system_handler, title)
        def setWindowPositionAndSize(self, size_x, size_y, position_x, position_y):
            if main_os == "Windows":
                try:
                    import win32gui # type: ignore
                except Exception as e:
                    pip().install(["pywin32"])
                    import win32gui # type: ignore
                win32gui.SetWindowPos(self.system_handler, win32gui.HWND_TOP, size_x, size_y, position_x, position_y, win32gui.SWP_SHOWWINDOW)
            elif main_os == "Darwin":
                try:
                    process = subprocess.run(["osascript", "-e", f'''
                    tell application "System Events"
                        set theProcess to (first process whose unix id is {self.pid})
                        if (count of windows of theProcess) > 0 then
                            set theWindow to window 1 of theProcess
                            set position of theWindow to {{{position_x}, {position_y}}}
                            set size of theWindow to {{{size_x}, {size_y}}}
                        end if
                    end tell'''], capture_output=True, text=True)
                    if process.stderr:
                        print("Error:", process.stderr)
                    print(process.stdout)
                except Exception as e:
                    print(f"Failed to execute AppleScript: {e}")
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
    def endRoblox(self, pid=""):
        if self.getIfRobloxIsOpen():
            if pid == "":
                if self.__main_os__ == "Darwin":
                    subprocess.run("killall -9 RobloxPlayer", shell=True, stdout=subprocess.DEVNULL)
                elif self.__main_os__ == "Windows":
                    subprocess.run("taskkill /IM RobloxPlayerBeta.exe /F", shell=True, stdout=subprocess.DEVNULL)
                else:
                    self.printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
            else:
                if self.__main_os__ == "Darwin":
                    subprocess.run(f"kill -9 {pid}", shell=True, stdout=subprocess.DEVNULL)
                elif self.__main_os__ == "Windows":
                    subprocess.run(f"taskkill /PID {pid} /F", shell=True, stdout=subprocess.DEVNULL)
                else:
                    self.printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
    def getIfRobloxIsOpen(self, installer=False, pid=""):
        if self.__main_os__ == "Windows":
            process = subprocess.Popen(["tasklist"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, _ = process.communicate()
            process_list = output.decode("utf-8")

            if pid == "" or pid == None:
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
        elif self.__main_os__ == "Darwin":
            if pid == "" or pid == None:
                if installer == False:
                    if subprocess.run(f"pgrep -f {macOS_dir}{macOS_beforeClientServices}RobloxPlayer > /dev/null 2>&1", shell=True).returncode == 0:
                        return True
                    else:
                        return False
                else:
                    if subprocess.run(f"pgrep -f {macOS_dir}{macOS_beforeClientServices}RobloxPlayerInstaller > /dev/null 2>&1", shell=True).returncode == 0:
                        return True
                    else:
                        return False
            else:
                if subprocess.run(f"ps -p {pid} > /dev/null 2>&1", shell=True).returncode == 0:
                    return True
                else:
                    return False
        else:
            self.printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
            return
    def getLatestClientVersion(self, debug=False, channel="LIVE"):
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

        try:    
            if self.__main_os__ == "Darwin":
                if debug == True: printDebugMessage("Sending Request to Roblox Servers..") 
                if channel:
                    res = requests.get(f"https://clientsettingscdn.roblox.com/v2/client-version/MacPlayer/channel/{channel}")
                else:
                    res = requests.get(f"https://clientsettingscdn.roblox.com/v2/client-version/MacPlayer")
                if res.ok:
                    jso = res.json()
                    if jso.get("clientVersionUpload") and jso.get("version"):
                        if debug == True: printDebugMessage(f"Called ({res.url}): {res.text}")
                        return {"success": True, "client_version": jso.get("clientVersionUpload"), "short_version": jso.get("version")}
                    else:
                        if debug == True: printDebugMessage(f"Something went wrong: {res.text}")
                        return {"success": False, "message": "Something went wrong."}
                else:
                    if not (channel == "LIVE"):
                        if debug == True: printDebugMessage(f"Roblox rejected update check with channel {channel}, retrying as channel LIVE: {res.text}")
                        return self.getLatestClientVersion(debug=debug, channel="LIVE")
                    else:
                        if debug == True: printDebugMessage(f"Something went wrong: {res.text}")
                        return {"success": False, "message": "Something went wrong."}
            elif self.__main_os__ == "Windows":
                if debug == True: printDebugMessage("Sending Request to Roblox Servers..") 
                if channel:
                    res = requests.get(f"https://clientsettingscdn.roblox.com/v2/client-version/WindowsPlayer/channel/{channel}")
                else:
                    res = requests.get(f"https://clientsettingscdn.roblox.com/v2/client-version/WindowsPlayer")
                if res.ok:
                    jso = res.json()
                    if jso.get("clientVersionUpload") and jso.get("version"):
                        if debug == True: printDebugMessage(f"Called ({res.url}): {res.text}")
                        return {"success": True, "client_version": jso.get("clientVersionUpload"), "short_version": jso.get("version")}
                    else:
                        if debug == True: printDebugMessage(f"Something went wrong: {res.text}")
                        return {"success": False, "message": "Something went wrong."}
                else:
                    if not (channel == "LIVE"):
                        if debug == True: printDebugMessage(f"Roblox rejected update check with channel {channel}, retrying as channel LIVE: {res.text}")
                        return self.getLatestClientVersion(debug=debug, channel="LIVE")
                    else:
                        if debug == True: printDebugMessage(f"Something went wrong: {res.text}")
                        return {"success": False, "message": "Something went wrong."}
            else:
                self.printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
                return {"success": False, "message": "OS not compatible."}
        except Exception as e:
            return {"success": False, "message": "There was an error checking. Please check your internet connection!"}
    def getCurrentClientVersion(self):
        if self.__main_os__ == "Darwin":
            if os.path.exists(f"{macOS_dir}/Contents/Info.plist"):
                read_plist = self.readPListFile(f"{macOS_dir}/Contents/Info.plist")
                if read_plist.get("CFBundleShortVersionString"):
                    version_channel = "LIVE"
                    try:
                        if os.path.exists(f'{os.path.expanduser("~")}/Library/Preferences/com.roblox.RobloxPlayerChannel.plist'):
                            read_install_plist = self.readPListFile(f'{os.path.expanduser("~")}/Library/Preferences/com.roblox.RobloxPlayerChannel.plist')
                            if read_install_plist.get("www.roblox.com") and not read_install_plist.get("www.roblox.com") == "":
                                version_channel = read_install_plist.get("www.roblox.com", "LIVE")
                    except Exception:
                        version_channel = "LIVE"
                    return {"success": True, "isClientVersion": False, "version": read_plist["CFBundleShortVersionString"], "channel": version_channel}
                else:
                    return {"success": False, "message": "Something went wrong."}
            else:
                return {"success": False, "message": "Roblox not installed."}
        elif self.__main_os__ == "Windows":
            res = self.getRobloxInstallFolder()
            if res:
                import winreg
                version_channel = ""
                try:
                    registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\ROBLOX Corporation\Environments\RobloxPlayer\Channel", 0, winreg.KEY_READ)
                    value, regtype = winreg.QueryValueEx(registry_key, "www.roblox.com")
                    winreg.CloseKey(registry_key)
                    if value.replace(" ", "") == "": 
                        version_channel = "LIVE"
                    else:
                        if value == "production":
                            version_channel = "LIVE"
                        else:
                            version_channel = value
                except Exception:
                    version_channel = "LIVE"
                return {"success": True, "isClientVersion": True, "version": os.path.basename(os.path.dirname(res)), "channel": version_channel}
            else:
                return {"success": False, "message": "Roblox not installed."}
        else:
            self.printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
            return {"success": False, "message": "OS not compatible."}
    def installFastFlagsJSON(self, fastflagJSON: object, askForPerms=False, merge=True, flat=False, endRobloxInstances=True, isBootstrapper=False, debug=False):
        if __name__ == "__main__":
            if self.__main_os__ == "Darwin":
                if endRobloxInstances == True:
                    printMainMessage(f"Closing any open Roblox windows..")
                    self.endRoblox()
                if isBootstrapper == False:
                    printMainMessage(f"Generating Client Settings Folder..")
                    if not os.path.exists(f"{macOS_dir}{macOS_beforeClientServices}ClientSettings"):
                        os.mkdir(f"{macOS_dir}{macOS_beforeClientServices}ClientSettings")
                        printSuccessMessage(f"Created {macOS_dir}{macOS_beforeClientServices}ClientSettings..")
                    else:
                        printWarnMessage(f"Client Settings is already created. Skipping Folder Creation..")
                printMainMessage(f"Writing ClientAppSettings.json")
                if merge == True:
                    if isBootstrapper == True and os.path.exists("FastFlagConfiguration.json"):
                        try:
                            printMainMessage("Reading Previous Configurations..")
                            with open(f"FastFlagConfiguration.json", "r") as f:
                                merge_json = json.load(f)
                            merge_json.update(fastflagJSON)
                            fastflagJSON = merge_json
                        except Exception as e:
                            printErrorMessage(f"Something went wrong while trying to generate a merged JSON: {str(e)}")
                    elif os.path.exists(f"{macOS_dir}{macOS_beforeClientServices}ClientSettings/ClientAppSettings.json"):
                        try:
                            printMainMessage("Reading Previous Client App Settings..")
                            with open(f"{macOS_dir}{macOS_beforeClientServices}ClientSettings/ClientAppSettings.json", "r") as f:
                                merge_json = json.load(f)
                            merge_json.update(fastflagJSON)
                            fastflagJSON = merge_json
                        except Exception as e:
                            printErrorMessage(f"Something went wrong while trying to generate a merged JSON: {str(e)}")
                set_location = f"{macOS_dir}{macOS_beforeClientServices}ClientSettings/ClientAppSettings.json"
                if isBootstrapper == True and os.path.exists("FastFlagConfiguration.json"):
                    set_location = "FastFlagConfiguration.json"
                with open(set_location, "w") as f:
                    if flat == True:
                        json.dump(fastflagJSON, f)
                    else:
                        json.dump(fastflagJSON, f, indent=4)
                printSuccessMessage("DONE!")
                if isBootstrapper == True:
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
                    if isBootstrapper == False:
                        printMainMessage(f"Generating Client Settings Folder..")
                        if not os.path.exists(f"{most_recent_roblox_version_dir}ClientSettings"):
                            os.mkdir(f"{most_recent_roblox_version_dir}ClientSettings")
                            printSuccessMessage(f"Created {most_recent_roblox_version_dir}ClientSettings..")
                        else:
                            printWarnMessage(f"Client Settings is already created. Skipping Folder Creation..")
                    printMainMessage(f"Writing ClientAppSettings.json")
                    if merge == True:
                        if os.path.exists("FastFlagConfiguration.json"):
                            try:
                                printMainMessage("Reading Previous Configurations..")
                                with open(f"FastFlagConfiguration.json", "r") as f:
                                    merge_json = json.load(f)
                                merge_json.update(fastflagJSON)
                                fastflagJSON = merge_json
                            except Exception as e:
                                printErrorMessage(f"Something went wrong while trying to generate a merged JSON: {str(e)}")
                        elif os.path.exists(f"{most_recent_roblox_version_dir}ClientSettings\\ClientAppSettings.json"):
                            try:
                                printMainMessage("Reading Previous Client App Settings..")
                                with open(f"{most_recent_roblox_version_dir}ClientSettings\\ClientAppSettings.json", "r") as f:
                                    merge_json = json.load(f)
                                merge_json.update(fastflagJSON)
                                fastflagJSON = merge_json
                            except Exception as e:
                                printErrorMessage(f"Something went wrong while trying to generate a merged JSON: {str(e)}")
                    
                    set_location = f"{most_recent_roblox_version_dir}ClientSettings\\ClientAppSettings.json"
                    if isBootstrapper == True and os.path.exists("FastFlagConfiguration.json"):
                        set_location = "FastFlagConfiguration.json"
                    with open(set_location, "w") as f:
                        if flat == True:
                            json.dump(fastflagJSON, f)
                        else:
                            json.dump(fastflagJSON, f, indent=4)
                    printSuccessMessage("DONE!")
                    if isBootstrapper == True:
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
                    if os.path.exists(f"{macOS_dir}{macOS_beforeClientServices}ClientSettings/ClientAppSettings.json"):
                        try:
                            with open(f"{macOS_dir}{macOS_beforeClientServices}ClientSettings/ClientAppSettings.json", "r") as f:
                                merge_json = json.load(f)
                            merge_json.update(fastflagJSON)
                            fastflagJSON = merge_json
                            if debug == True: printDebugMessage("Successfully merged the JSON in the ClientSettings folder with the provided json!")
                        except Exception as e:
                            self.printLog(f"Something went wrong while trying to generate a merged JSON: {str(e)}")
                with open(f"{macOS_dir}{macOS_beforeClientServices}ClientSettings/ClientAppSettings.json", "w") as f:
                    if flat == True:
                        json.dump(fastflagJSON, f)
                    else:
                        json.dump(fastflagJSON, f, indent=4)
                if debug == True: printDebugMessage(f"Saved to ClientAppSettings.json successfully!")
            elif self.__main_os__ == "Windows":
                self.endRoblox()
                if debug == True: printDebugMessage("Ending Roblox Instances..")
                most_recent_roblox_version_dir = self.getRobloxInstallFolder(f"{windows_dir}\\Versions")
                if most_recent_roblox_version_dir:
                    if not os.path.exists(f"{most_recent_roblox_version_dir}ClientSettings"):
                        os.mkdir(f"{most_recent_roblox_version_dir}ClientSettings")
                        if debug == True: printDebugMessage("Created ClientSettings folder..")
                    if merge == True:
                        if os.path.exists(f"{most_recent_roblox_version_dir}ClientSettings\\ClientAppSettings.json"):
                            try:
                                with open(f"{most_recent_roblox_version_dir}ClientSettings\\ClientAppSettings.json", "r") as f:
                                    merge_json = json.load(f)
                                merge_json.update(fastflagJSON)
                                fastflagJSON = merge_json
                                if debug == True: printDebugMessage("Successfully merged the JSON in the ClientSettings folder with the provided json!")
                            except Exception as e:
                                self.printLog(f"Something went wrong while trying to generate a merged JSON: {str(e)}")
                    with open(f"{most_recent_roblox_version_dir}ClientSettings\\ClientAppSettings.json", "w") as f:
                        if flat == True:
                            json.dump(fastflagJSON, f)
                        else:
                            json.dump(fastflagJSON, f, indent=4)
                    if debug == True: printDebugMessage(f"Saved to ClientAppSettings.json successfully!")
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
                    if os.path.exists(f"{fold}\\RobloxPlayerBeta.exe"):
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
    def getOpenedRobloxPids(self):
        if self.__main_os__ == "Darwin":
            try:
                result = subprocess.run(["ps", "axo", "pid,etime,command"], stdout=subprocess.PIPE, text=True)
                processes = result.stdout
                roblox_lines = [line for line in processes.splitlines() if "RobloxPlayer" in line]
                if not roblox_lines:
                    return None
                pid_list = []
                for i in roblox_lines:
                    pid_list.append(i.split()[0])
                return pid_list
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
                pid_list = []
                for i in program_lines:
                    pid_list.append(i.split()[1])
                return pid_list
            except Exception as e:
                printErrorMessage(f"Error occurred while getting Roblox Instance: {e}")
                return None
    def getAllOpenedRobloxWindows(self) -> "list[RobloxWindow]":
        pids = self.getOpenedRobloxPids()
        generated_window_instances = []
        for i in pids:
            process_windows = pip().getProcessWindows(i)
            for e in process_windows:
                generated_window_instances.append(self.RobloxWindow(int(i), e))
        return generated_window_instances
    def getOpenedRobloxWindows(self, pid):
        generated_window_instance = None
        process_windows = pip().getProcessWindows(pid)
        for e in process_windows:
            generated_window_instance =  self.RobloxWindow(int(pid), e)
        return generated_window_instance
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
                            kernel32.ReleaseMutex(mutex)
                        except Exception as e:
                            kernel32.ReleaseMutex(mutex)
                def hold_mutex2():
                    mutex = kernel32.CreateMutexA(None, wintypes.BOOL(True), "ROBLOX_singletonMutex")
                    if mutex:
                        try:
                            if awaitRobloxClosure == True:
                                while self.getIfRobloxIsOpen():
                                    time.sleep(1)
                            else:
                                while True:
                                    time.sleep(1)
                            kernel32.ReleaseMutex(mutex)
                        except Exception as e:
                            kernel32.ReleaseMutex(mutex)
                threading.Thread(target=hold_mutex).start()
                threading.Thread(target=hold_mutex2).start()
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
                            test_instance = self.RobloxInstance(self, pid=cur_open_pid, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=False)
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
                            test_instance = self.RobloxInstance(self, pid=cur_open_pid, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=False)
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
                                        return self.RobloxInstance(self, pid=pid, log_file=mainLogFile, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=True)
                                    else:
                                        return self.RobloxInstance(self, pid=pid, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=True)
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
                                        return self.RobloxInstance(self, pid=pid, log_file=mainLogFile, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=True)
                                    else:
                                        return self.RobloxInstance(self, pid=pid, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=True)
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
                                    return self.RobloxInstance(self, pid=pid, log_file=mainLogFile, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=True)
                                else:
                                    return self.RobloxInstance(self, pid=pid, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=True)
        elif self.__main_os__ == "Windows":
            created_mutex = False
            if not self.getIfRobloxIsOpen():
                if makeDupe == True:
                   created_mutex = self.prepareMultiInstance(debug=debug)
                   if created_mutex == True:
                       if debug == True: printDebugMessage("Successfully attached the mutex! Once this window closes, all the other Roblox windows will close.")
                   else:
                       if debug == True: printDebugMessage("There's an issue trying to create a mutex!")
            else:
                if len(self.getAllOpenedRobloxWindows()) > 0:
                    if debug == True and makeDupe == False: printDebugMessage("Roblox is currently open right now and multiple instance is disabled!")
                elif makeDupe == True:
                    self.endRoblox()
                    created_mutex = self.prepareMultiInstance(debug=debug)
                    if created_mutex == True:
                        if debug == True: printDebugMessage("Successfully attached the mutex! Once this window closes, all the other Roblox windows will close.")
                    else:
                        if debug == True: printDebugMessage("There's an issue trying to create a mutex!")

            most_recent_roblox_version_dir = self.getRobloxInstallFolder(f"{windows_dir}\\Versions")
            if most_recent_roblox_version_dir:
                if debug == True: printDebugMessage("Running RobloxPlayerBeta.exe..")
                if startData == "":
                    a = subprocess.run(f"start {most_recent_roblox_version_dir}RobloxPlayerBeta.exe", shell=True, stdout=subprocess.DEVNULL)
                else:
                    a = subprocess.run(f'start {most_recent_roblox_version_dir}RobloxPlayerBeta.exe "{startData}"', shell=True, stdout=subprocess.DEVNULL)
                if a.returncode == 0:
                    if attachInstance == True:
                        if makeDupe == True:
                            if self.getIfRobloxIsOpen() == True:
                                cur_open_pid = self.getLatestOpenedRobloxPid()
                                start_time = datetime.datetime.now(tz=datetime.UTC).timestamp()
                                test_instance = self.RobloxInstance(self, pid=cur_open_pid, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=False)
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
                                test_instance = self.RobloxInstance(self, pid=cur_open_pid, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=False)
                                while True:
                                    if test_instance.ended_process == True:
                                        break
                                    elif start_time+3 < datetime.datetime.now(tz=datetime.UTC).timestamp():
                                        test_instance.requestThreadClosing()
                                        break
                                    else:
                                        time.sleep(1)
                                if self.getIfRobloxIsOpen() == True:
                                    pid = self.getLatestOpenedRobloxPid()
                                    if pid:
                                        if not (mainLogFile == ""):
                                            return self.RobloxInstance(self, pid=pid, log_file=mainLogFile, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=True, created_mutex=created_mutex)
                                        else:
                                            return self.RobloxInstance(self, pid=pid, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=True, created_mutex=created_mutex)
                        else:
                            time.sleep(2)
                            if self.getIfRobloxIsOpen() == True:
                                cur_open_pid = self.getLatestOpenedRobloxPid()
                                start_time = datetime.datetime.now(tz=datetime.UTC).timestamp()
                                test_instance = self.RobloxInstance(self, pid=cur_open_pid, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=False)
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
                                test_instance = self.RobloxInstance(self, pid=cur_open_pid, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=False)
                                while True:
                                    if test_instance.ended_process == True:
                                        break
                                    elif start_time+3 < datetime.datetime.now(tz=datetime.UTC).timestamp():
                                        test_instance.requestThreadClosing()
                                        break
                                    else:
                                        time.sleep(1)
                                if self.getIfRobloxIsOpen() == True:
                                    pid = self.getLatestOpenedRobloxPid()
                                    if pid:
                                        if not (mainLogFile == ""):
                                            return self.RobloxInstance(self, pid=pid, log_file=mainLogFile, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=True, created_mutex=created_mutex)
                                        else:
                                            return self.RobloxInstance(self, pid=pid, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=True, created_mutex=created_mutex)
            else:
                self.printLog("Roblox couldn't be found.")
        else:
            self.printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
    def installRoblox(self, forceQuit=True, debug=False, disableRobloxAutoOpen=True, copyRobloxInstallationPath=""):
        if self.getIfRobloxIsOpen():
            if forceQuit == True:
                self.endRoblox()
                if debug == True: printDebugMessage("Ending Roblox Instances..")
        def waitForRobloxEnd():
            if disableRobloxAutoOpen == True:
                for i in range(150):
                    if debug == True and (i % 10) == 0: printDebugMessage(f"Waited: {int(i/10)}/15 seconds")
                    if self.getIfRobloxIsOpen():
                        self.endRoblox()
                        break
                    time.sleep(0.1)
                
        if self.__main_os__ == "Darwin":
            if self.getIfRobloxIsOpen(installer=True):
                if debug == True: printDebugMessage("Installer is already opened. Waiting for installation to end..")
                while True:
                    if not self.getIfRobloxIsOpen(installer=True):
                        break
                    else:
                        time.sleep(1)
                waitForRobloxEnd()
            else:
                try:
                    if not copyRobloxInstallationPath == "":
                        try:
                            if debug == True: printDebugMessage(f"Replicating Roblox Player installer to path: {copyRobloxInstallationPath}")
                            import shutil
                            shutil.copytree(f"{macOS_dir}{macOS_beforeClientServices}RobloxPlayerInstaller.app", copyRobloxInstallationPath, dirs_exist_ok=True)
                        except Exception as e:
                            if debug == True: printDebugMessage("Unable to replicate installer to the designated file path.")
                        if debug == True: printDebugMessage("Running RobloxPlayerInstaller executable..")
                        insta = subprocess.run(f"{copyRobloxInstallationPath}/Contents/MacOS/RobloxPlayerInstaller", shell=True, check=True, stdout=subprocess.DEVNULL)
                    else:
                        if debug == True: printDebugMessage("Running RobloxPlayerInstaller executable..")
                        insta = subprocess.run(f"{macOS_dir}{macOS_beforeClientServices}RobloxPlayerInstaller.app/Contents/MacOS/RobloxPlayerInstaller", shell=True, check=True, stdout=subprocess.DEVNULL)
                    if insta.returncode == 0:
                        if debug == True: printDebugMessage("Installer has succeeded! Awaiting Roblox closing..")
                    else:
                        if debug == True: printDebugMessage(f"Installer has failed. Code: {insta.returncode}")
                    waitForRobloxEnd()
                except Exception as e:
                    printErrorMessage(f"Something went wrong starting Roblox Installer: {str(e)}")
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
                    waitForRobloxEnd()
                else:
                    if debug == True: printDebugMessage("Running RobloxPlayerInstaller executable..")
                    try:
                        insta = subprocess.Popen(f"{most_recent_roblox_version_dir}RobloxPlayerInstaller.exe", shell=True, stdout=subprocess.DEVNULL)
                        while True:
                            if not self.getIfRobloxIsOpen(installer=True):
                                break
                            else:
                                time.sleep(1)
                        if debug == True: printDebugMessage("Installer has succeeded! Awaiting Roblox closing..")
                        waitForRobloxEnd()
                    except Exception as e:
                        printErrorMessage(f"Something went wrong starting Roblox Installer: {str(e)}")
            else:
                self.printLog("Roblox Installer couldn't be found.")
        else:
            self.printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")

if __name__ == "__main__":
    handler = Main()
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
        if main_os == "Windows":
            printMainMessage(f"System OS: {main_os}")
            found_platform = "Windows"
        elif main_os == "Darwin":
            printMainMessage(f"System OS: {main_os} (macOS)")
            found_platform = "Darwin"
        else:
            input("> ")
            sys.exit(0)
        current_python_version = platform.python_version_tuple()
        if current_python_version < ("3", "10", "0"):
            printErrorMessage("Please update your current installation of Python above 3.10.0")
            input("> ")
            sys.exit(0)
        else:
            printMainMessage(f"Python Version: {platform.python_version()}")
        if main_os == "Windows":
            if not os.path.exists(windows_dir):
                printErrorMessage("The Roblox Website App Path doesn't exist. Please install Roblox from your web browser in order to use!")
                exit()
        elif main_os == "Darwin":
            if not os.path.exists(macOS_dir):
                printErrorMessage("The Roblox Website App Path doesn't exist. Please install Roblox from your web browser in order to use!")
                exit()
            else:
                installed_roblox_version = handler.getCurrentClientVersion()
                if installed_roblox_version["success"] == True:
                    printMainMessage(f"Current Roblox Version: {installed_roblox_version['version']}")
                else:
                    printErrorMessage("Something went wrong trying to determine your current Roblox version.")
                    input("> ")
                    sys.exit(0)
        printWarnMessage("-----------")
    else:
        if main_os == "Windows":
            printWarnMessage(f"Starting Roblox Fast Flags Installer v{fast_flag_installer_version}!")
        elif main_os == "Darwin":
            printWarnMessage(f"Starting Roblox Fast Flags Installer v{fast_flag_installer_version}!")
        else:
            printErrorMessage("Please run this script on macOS/Windows.")
            exit()
        printWarnMessage("--------------------")

    def getUserId():
        printMainMessage("Please input your User ID! This can be found on your profile in the URL: https://www.roblox.com/users/XXXXXXXX/profile")
        id = input("> ")
        if id.isnumeric():
            return id
        elif isRequestClose(id):
            printMainMessage("Ending installation..")
            exit()
        else:
            printWarnMessage("Let's try again!")
            return getUserId()
    
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
        elif isRequestClose(cap):
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
            generated_json["FFlagGameBasicSettingsFramerateCap1"] = "true" # If roblox decides to change, I won't need to :)
            generated_json["FFlagGameBasicSettingsFramerateCap2"] = "true"
            generated_json["FFlagGameBasicSettingsFramerateCap3"] = "true"
            generated_json["FFlagGameBasicSettingsFramerateCap4"] = "true"
            generated_json["FFlagGameBasicSettingsFramerateCap5"] = "true"
            generated_json["FFlagGameBasicSettingsFramerateCap6"] = "true"
            generated_json["FFlagGameBasicSettingsFramerateCap7"] = "true"
            generated_json["FFlagGameBasicSettingsFramerateCap8"] = "true"
            generated_json["FFlagGameBasicSettingsFramerateCap9"] = "true"
            generated_json["FFlagGameBasicSettingsFramerateCap10"] = "true" # If roblox decides to change, I won't need to :)
            generated_json["DFIntTaskSchedulerTargetFps"] = 0
        elif isRequestClose(robloxFPSUnlocker) == True:
            printMainMessage("Ending installation..")
            exit()
        elif isNo(robloxFPSUnlocker) == True:
            generated_json["FFlagGameBasicSettingsFramerateCap1"] = "false" # If roblox decides to change, I won't need to :)
            generated_json["FFlagGameBasicSettingsFramerateCap2"] = "false"
            generated_json["FFlagGameBasicSettingsFramerateCap3"] = "false"
            generated_json["FFlagGameBasicSettingsFramerateCap4"] = "false"
            generated_json["FFlagGameBasicSettingsFramerateCap5"] = "false"
            generated_json["FFlagGameBasicSettingsFramerateCap6"] = "false"
            generated_json["FFlagGameBasicSettingsFramerateCap7"] = "false"
            generated_json["FFlagGameBasicSettingsFramerateCap8"] = "false"
            generated_json["FFlagGameBasicSettingsFramerateCap9"] = "false"
            generated_json["FFlagGameBasicSettingsFramerateCap10"] = "false" # If roblox decides to change, I won't need to :)
            generated_json["DFIntTaskSchedulerTargetFps"] = None

    # Verified Badge
    printWarnMessage("--- Verified Badge ---")
    printMainMessage("Would you like to use a verified badge during Roblox Games? (y/n)")
    installVerifiedBadge = input("> ")
    if isYes(installVerifiedBadge) == True:
        id = getUserId()
        if id: generated_json["FStringWhitelistVerifiedUserId"] = str(id)
    elif isRequestClose(installVerifiedBadge) == True:
        printMainMessage("Ending installation..")
        exit()
    elif isNo(installVerifiedBadge) == True:
        generated_json["FStringWhitelistVerifiedUserId"] = ""

    # Rename Charts to Discover
    printWarnMessage("--- Replace Charts ---")
    printMainMessage("Would you like to rename Charts back to Discover (may work)? (y/n)")
    installRenameCharts = input("> ")
    if isYes(installRenameCharts) == True:
        generated_json["FFlagLuaAppChartsPageRenameIXP"] = "false"
    elif isRequestClose(installRenameCharts) == True:
        printMainMessage("Ending installation..")
        exit()
    elif isNo(installRenameCharts) == True:
        generated_json["FFlagLuaAppChartsPageRenameIXP"] = "true"

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
    printMainMessage("Would you like to increase the limit on Max Assets loading from 100 to 999,999? (this will make loading into games faster depending on your computer) (y/n)")
    printYellowMessage("WARNING! This can crash your Roblox session!")
    installRemoveMaxAssets = input("> ")
    if isYes(installRemoveMaxAssets) == True:
        generated_json["DFIntNumAssetsMaxToPreload"] = "999999"
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
        generated_json["FFlagLuaAppGenreUnderConstructionDesktopFix"] = "false"
    elif isRequestClose(installGenreSystem) == True:
        printMainMessage("Ending installation..")
        exit()
    elif isNo(installGenreSystem) == True:
        generated_json["FFlagLuaAppGenreUnderConstruction"] = "true"
        generated_json["FFlagLuaAppGenreUnderConstructionDesktopFix"] = "true"

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

    # Enable New Camera Controls
    printWarnMessage("--- Enable New Camera Controls ---")
    printMainMessage("Would you like to enable new camera controls? (y/n)")
    installNewCamera = input("> ")
    if isYes(installNewCamera) == True:
        generated_json["FFlagNewCameraControls"] = "true"
    elif isRequestClose(installNewCamera) == True:
        printMainMessage("Ending installation..")
        exit()
    elif isNo(installNewCamera) == True:
        generated_json["FFlagNewCameraControls"] = "false"

    # Hide Internet Disconnect Message
    printWarnMessage("--- Hide Internet Disconnect Message ---")
    printMainMessage("Would you like to hide the Internet Disconnect message when you're kicked? (You will still be kicked, jsut the message will not show.) (y/n)")
    installHideDisconnect = input("> ")
    if isYes(installHideDisconnect) == True:
        generated_json["DFFlagDebugDisableTimeoutDisconnect"] = "true"
    elif isRequestClose(installHideDisconnect) == True:
        printMainMessage("Ending installation..")
        exit()
    elif isNo(installHideDisconnect) == True:
        generated_json["DFFlagDebugDisableTimeoutDisconnect"] = "false"

    # Disable In-Game Purchases
    printWarnMessage("--- Disable In-Game Purchases ---")
    printMainMessage("Would you like to disable in-game purchases (game-passes, developer products, etc.)? (You will still be kicked, jsut the message will not show.) (y/n)")
    installDisablePurchases = input("> ")
    if isYes(installDisablePurchases) == True:
        generated_json["DFFlagOrder66"] = "true"
    elif isRequestClose(installDisablePurchases) == True:
        printMainMessage("Ending installation..")
        exit()
    elif isNo(installDisablePurchases) == True:
        generated_json["DFFlagOrder66"] = "false"

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
    printMainMessage("Would you like to enable Darker mode on your client? (Recently, this may not work.) (y/n)")
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
        generated_json["FFlagLuaAppEnableFoundationColors4"] = "true"
        generated_json["FFlagLuaAppEnableFoundationColors5"] = "true"
        generated_json["FFlagLuaAppEnableFoundationColors6"] = "true"
        generated_json["FFlagLuaAppEnableFoundationColors7"] = "true"
        generated_json["FFlagLuaAppEnableFoundationColors8"] = "true"
        generated_json["FFlagLuaAppEnableFoundationColors9"] = "true"
        generated_json["FFlagLuaAppEnableFoundationColors10"] = "true"
    elif isRequestClose(installBlueColors) == True:
        printMainMessage("Ending installation..")
        exit()
    elif isNo(installBlueColors) == True:
        generated_json["FFlagLuaAppEnableFoundationColors3"] = "false"
        generated_json["FFlagLuaAppEnableFoundationColors4"] = "false"
        generated_json["FFlagLuaAppEnableFoundationColors5"] = "false"
        generated_json["FFlagLuaAppEnableFoundationColors6"] = "false"
        generated_json["FFlagLuaAppEnableFoundationColors7"] = "false"
        generated_json["FFlagLuaAppEnableFoundationColors8"] = "false"
        generated_json["FFlagLuaAppEnableFoundationColors9"] = "false"
        generated_json["FFlagLuaAppEnableFoundationColors10"] = "false"

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
            printMainMessage("Enter Key Name: ")
            key = input("> ")
            if isRequestClose(key) or key == "":
                return {"success": False, "key": "", "value": ""}
            if efaz_bootstrap_mode == True and key.startswith("EFlag"):
                printMainMessage("Are you sure you want to set this Efaz's Roblox Bootstrap setting?")
                con = input("> ")
                if isYes(con) == False:
                    return loop()
            printMainMessage("Enter Key Value: ")
            value = input("> ")
            if isRequestClose(value):
                return {"success": False, "key": "", "value": ""}
            if value.isnumeric():
                printMainMessage("Would you like this value to be a number value or do you want to keep it as a string? (y/n)")
                isNum = input("> ")
                if isNum == True:
                    value = int(value)
            elif value == "true" or value == "false":
                printMainMessage("Would you like this value to be a boolean value or do you want to keep it as a string? (y/n)")
                isBool = input("> ")
                if isBool == True:
                    value = value=="true"
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
                handler.installFastFlagsJSON(generated_json, endRobloxInstances=False, isBootstrapper=True)
            else:
                printMainMessage("Ending installation..")
                exit()