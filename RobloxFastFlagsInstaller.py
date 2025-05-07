# 
# Roblox Fast Flags Installer
# Made by Efaz from efaz.dev
# v2.1.0
# 
# Fulfill your Roblox needs and configuration through Python!
# 

import os
import platform
import json
import subprocess
import time
import datetime
import threading
import shutil
import typing
import hashlib
import urllib.request
import re
import sys

main_os = platform.system()
orangeblox_mode = False
current_path_location = os.path.dirname(os.path.abspath(__file__))
user_folder = (main_os == "Darwin" and os.path.expanduser("~") or os.getenv('LOCALAPPDATA'))

# Customizable Variables
macOS_dir = os.path.join("/", "Applications", "Roblox.app")  # This is Roblox macOS path
macOS_studioDir = os.path.join("/", "Applications", "RobloxStudio.app")  # This is Roblox macOS path
macOS_beforeClientServices = os.path.join("Contents", "MacOS") # This is a partial path for the executables are located for macOS Roblox, do not edit
macOS_installedPath = os.path.join("/", "Applications") # This is where Roblox is installed on macOS
windows_dir = os.path.join(os.getenv('LOCALAPPDATA') or "", "Roblox") # This is the Roblox folder in Windows App Data
windows_versions_dir = os.path.join(windows_dir, "Versions") # This is the Roblox versions folder path
windows_player_folder_name = "" # This is the version folder name for Roblox Player
windows_studio_folder_name = "" # This is the version folder name for Roblox Studio
submitStatus = None # This is a SubmitStatus handler class used for alerting status of functions.
# Customizable Variables

# Typing Literals
if sys.version_info >= (3, 8, 0):
    robloxInstanceTotalLiteralEventNames = typing.Literal[
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
        "onGameLog",
        "onGameError",
        "onGameWarning",
        "onRobloxVoiceChatMute",
        "onRobloxVoiceChatUnmute",
        "onRobloxVoiceChatStart",
        "onRobloxVoiceChatLeft",
        "onRobloxAudioDeviceStopRecording",
        "onRobloxAudioDeviceStartRecording",
        "onPlayTestStart",
        "onOpeningGame",
        "onExpiredFlag",
        "onApplyingFeature",
        "onPluginLoading",
        "onRobloxPublishing",
        "onRobloxLauncherDestroyed",
        "onPlayTestDisconnected",
        "onTelemetryLog",
        "onClosingGame",
        "onTeamCreateConnect",
        "onTeamCreateDisconnect",
        "onCloudPlugins",
        "onPluginUnloading",
        "onRobloxSaved",
        "onNewStudioLaunching",
        "onStudioInstallerLaunched"
    ]
else:
    robloxInstanceTotalLiteralEventNames = typing.AnyStr
# Typing Literals

def printMainMessage(mes): print(f"\033[38;5;255m{mes}\033[0m")
def printErrorMessage(mes): print(f"\033[38;5;196m{mes}\033[0m")
def printSuccessMessage(mes): print(f"\033[38;5;82m{mes}\033[0m")
def printWarnMessage(mes): print(f"\033[38;5;202m{mes}\033[0m")
def printYellowMessage(mes): print(f"\033[38;5;226m{mes}\033[0m")
def printDebugMessage(mes): print(f"\033[38;5;226m[Roblox FFlag Installer] [DEBUG]: {mes}\033[0m")
def isYes(text): return text.lower() == "y" or text.lower() == "yes" or text.lower() == "true" or text.lower() == "t"
def isNo(text): return text.lower() == "n" or text.lower() == "no" or text.lower() == "false" or text.lower() == "f"
def isRequestClose(text): return text.lower() == "exit" or text.lower() == "exit()"
def printLog(mes): 
    if __name__ == "__main__": printMainMessage(mes)
    else: print(mes)
def makedirs(a): os.makedirs(a,exist_ok=True)

if os.path.exists("Main.py") and os.path.exists("PipHandler.py") and os.path.exists("OrangeAPI.py"): orangeblox_mode = True
fast_flag_installer_version = "2.1.0"
sys.dont_write_bytecode = True

class pip:
    executable = None
    debug = False
    def __init__(self, command: list=[], executable: str=None, debug: bool=False):
        import sys
        import os
        import subprocess
        self.debug = debug==True
        if type(executable) is str:
            if os.path.isfile(executable):
                self.executable = executable
            else:
                self.executable = sys.executable
        else:
            self.executable = sys.executable
        if type(command) is list and len(command) > 0: subprocess.check_call([self.executable, "-m", "pip"] + command)
    def install(self, packages: typing.List[str]):
        import subprocess
        res = {}
        generated_list = []
        for i in packages:
            if type(i) is str: 
                generated_list.append(i)
        if len(generated_list) > 0:
            try:
                a = subprocess.call([self.executable, "-m", "pip", "install"] + generated_list, stdout=(not self.debug) and subprocess.DEVNULL or None, stderr=(not self.debug) and subprocess.DEVNULL or None)
                if a == 0: return {"success": True, "message": "Successfully installed modules!"}
                else: return {"success": False, "message": f"Command has failed!"}
            except Exception as e:
                return {"success": False, "message": str(e)}
        return res
    def uninstall(self, packages: typing.List[str]):
        import subprocess
        res = {}
        generated_list = []
        for i in packages:
            if type(i) is str:
                generated_list.append(i)
        if len(generated_list) > 0:
            try:
                subprocess.call([self.executable, "-m", "pip", "uninstall", "-y"] + generated_list, stdout=self.debug == False and subprocess.DEVNULL or None, stderr=self.debug == False and subprocess.DEVNULL or None)
                res[i] = {"success": True}
            except Exception as e:
                res[i] = {"success": False}
        return res
    def installed(self, packages: typing.List[str]=[], boolonly: bool=False):
        import subprocess
        sub = subprocess.run([self.executable, "-m", "pip", "list"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        line_splits = sub.stdout.decode().splitlines()[2:]
        installed_packages = [package.split()[0].lower() for package in line_splits if package.strip()]
        installed_checked = {}
        all_installed = True
        if len(packages) == 0:
            return installed_packages
        elif len(packages) == 1:
            return packages[0].lower() in installed_packages
        else:
            for i in packages:
                try:
                    if i.lower() in installed_packages:
                        installed_checked[i] = True
                    else:
                        installed_checked[i] = False
                        all_installed = False
                except Exception as e:
                    installed_checked[i] = False
                    all_installed = False
            installed_checked["all"] = all_installed
            if boolonly == True: return installed_checked["all"]
            return installed_checked
    def download(self, packages: typing.List[str], repository_mode: bool=False):
        import subprocess
        import os
        import shutil
        import urllib.parse
        import urllib.request
        res = {}
        generated_list = []
        for i in packages:
            if type(i) is str: generated_list.append(i)
        if len(generated_list) > 0:
            try:
                current_path_location = os.path.dirname(os.path.abspath(__file__))
                if repository_mode == True:
                    url_paths = []
                    url_paths_2 = []
                    for i in generated_list: 
                        if i.startswith("https://github.com") or i.startswith("https://www.github.com"):
                            path_parts = urllib.parse.urlparse(i).path.strip('/').split('/')
                            url_paths.append(path_parts[-1])
                            url_paths_2.append(path_parts[-2])
                    down_path = os.path.join(current_path_location, '-'.join(url_paths) + "_download")
                    if os.path.isdir(down_path): shutil.rmtree(down_path, ignore_errors=True)
                    os.makedirs(down_path)
                    co = 0
                    downed_paths = []
                    for url_path_1 in url_paths:
                        url_path_2 = url_paths_2[co]
                        urllib.request.urlretrieve(f"https://github.com/{url_path_2}/{url_path_1}/archive/refs/heads/main.zip", os.path.join(down_path, f"{url_path_1}.zip"))
                        downed_paths.append(os.path.join(down_path, f"{url_path_1}.zip"))
                        co += 1
                    return {"success": True, "path": down_path, "package_files": downed_paths}
                else:
                    down_path = os.path.join(current_path_location, '-'.join(generated_list) + "_download")
                    if os.path.isdir(down_path): shutil.rmtree(down_path, ignore_errors=True)
                    os.makedirs(down_path)
                    subprocess.check_call([self.executable, "-m", "pip", "download", "--no-binary", ":all:"] + generated_list, stdout=self.debug == False and subprocess.DEVNULL, stderr=self.debug == False and subprocess.DEVNULL, cwd=down_path)
                    a = []
                    for e in os.listdir(down_path): a.append(os.path.join(down_path, e))
                    return {"success": True, "path": down_path, "package_files": a}
            except Exception as e:
                print(e)
                return {"success": False}
        return {"success": False}
    def getGitHubRepository(self, packages: typing.List[str]):
        import json
        import urllib.request
        res = {}
        generated_list = []
        for i in packages:
            if type(i) is str: generated_list.append(i)
        if len(generated_list) > 0:
            try:
                links = {}
                for i in generated_list:
                    urll = f"https://pypi.org/pypi/{i}/json"
                    with urllib.request.urlopen(urll) as response:
                        data = json.load(response)
                        info = data["info"]
                        url = info.get("project_urls", {}).get("Source") or info.get("home_page")
                    if url: links[i] = url
                return {"success": True, "repositories": links}
            except Exception as e:
                return {"success": False}
        return {"success": False}
    def getLatestPythonVersion(self, beta: bool=False):
        import urllib.request
        import re
        import gzip
        import io
        import ssl
        url = "https://www.python.org/downloads/"
        if beta == True: url = "https://www.python.org/download/pre-releases/"
        unsecure_context = None
        if not self.pythonSupported(3, 9, 0): unsecure_context = ssl._create_unverified_context()
        with urllib.request.urlopen(url, context=unsecure_context) as response:
            if response.headers.get('Content-Encoding') == 'gzip':
                buf = io.BytesIO(response.read())
                f = gzip.GzipFile(fileobj=buf)
                html = f.read().decode('utf-8')
            else:
                html = response.read().decode('utf-8')
        if beta == True: match = re.search(r'Python (\d+\.\d+\.\d+)([a-zA-Z0-9]+)?', html)
        else: match = re.search(r"Download Python (\d+\.\d+\.\d+)", html)
        if match:
            if beta == True: version = f'{match.group(1)}{match.group(2)}'
            else: version = match.group(1)
            return version
        else:
            if self.debug == True: print("Failed to find latest Python version.")
            return None
    def getCurrentPythonVersion(self):
        import subprocess
        if not self.executable: return None
        if self.isSameRunningPythonExecutable():
            import platform
            return platform.python_version()
        else:
            a = subprocess.run([self.executable, "-V"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            final = a.stdout.decode()
            if a.returncode == 0: return final.replace("Python ", "").replace("\n", "")
            else: return None
    def getIfPythonVersionIsBeta(self, version=""):
        import re
        if version == "": cur_vers = self.getCurrentPythonVersion()
        else: cur_vers = version
        match = re.search(r'(\d+\.\d+\.\d+)([a-z]+(\d+)?)?', cur_vers)
        if match:
            _, suf, _ = match.groups()
            if suf: return True
            return False
        else:
            return False
    def getIfPythonIsLatest(self):
        cur_vers = self.getCurrentPythonVersion()
        if self.getIfPythonVersionIsBeta(): latest_vers = self.getLatestPythonVersion(beta=True)
        else: latest_vers = self.getLatestPythonVersion(beta=False)
        return cur_vers == latest_vers
    def pythonInstalled(self, computer=False):
        import os
        if computer == True:
            if self.findPython(): return True
            else: return False
        else:
            if not self.executable: return False
            if os.path.exists(self.executable): return True
            else: return False
    def pythonSupported(self, major: int=3, minor: int=13, patch: int=2):
        import re
        cur_version = self.getCurrentPythonVersion()
        if not cur_version: return False
        match = re.match(r"(\d+)\.(\d+)\.(\w+)", cur_version)
        if match:
            cur_version = match.groups() 
            def to_int(val): return int(re.sub(r'\D', '', val))
            return tuple(map(to_int, cur_version)) >= (major, minor, patch)
        else: return False
    def pythonInstall(self, version: str="", beta: bool=False):
        import subprocess
        import platform
        import tempfile
        import time
        import re
        ma_os = platform.system()
        ma_arch = platform.architecture()
        ma_processor = platform.machine()
        if version == "": version = self.getLatestPythonVersion(beta=beta)
        if not version:
            if self.debug == True: print("Failed to download Python installer.")
            return
        version_url_folder = version
        if beta == True: version_url_folder = re.match(r'^\d+\.\d+\.\d+', version).group()
        if ma_os == "Darwin":
            url = f"https://www.python.org/ftp/python/{version_url_folder}/python-{version}-macos11.pkg"
            with tempfile.NamedTemporaryFile(suffix=".pkg", delete=False) as temp_file: pkg_file_path = temp_file.name
            result = subprocess.run(["curl", "-o", pkg_file_path, url], stdout=self.debug == False and subprocess.DEVNULL, stderr=self.debug == False and subprocess.DEVNULL)            
            if result.returncode == 0:
                subprocess.run(["open", pkg_file_path], stdout=self.debug == False and subprocess.DEVNULL, stderr=self.debug == False and subprocess.DEVNULL, check=True)
                while self.getIfProcessIsOpened("Installer") == True:
                    time.sleep(0.1)
                if self.debug == True: print(f"Python installer has been executed: {pkg_file_path}")
            else:
                if self.debug == True: print("Failed to download Python installer.")
        elif ma_os == "Windows":
            if ma_arch[0] == "64bit":
                if ma_processor.lower() == "arm64": url = f"https://www.python.org/ftp/python/{version_url_folder}/python-{version}-arm64.exe"
                else: url = f"https://www.python.org/ftp/python/{version_url_folder}/python-{version}-amd64.exe"
            else:
                url = f"https://www.python.org/ftp/python/{version_url_folder}/python-{version}.exe"
            with tempfile.NamedTemporaryFile(suffix=".exe", delete=False) as temp_file: exe_file_path = temp_file.name
            result = subprocess.run(["curl", "-o", exe_file_path, url], stdout=self.debug == False and subprocess.DEVNULL, stderr=self.debug == False and subprocess.DEVNULL)            
            if result.returncode == 0:
                subprocess.run([exe_file_path], stdout=self.debug == False and subprocess.DEVNULL, stderr=self.debug == False and subprocess.DEVNULL, check=True)
                if self.debug == True: print(f"Python installer has been executed: {exe_file_path}")
            else:
                if self.debug == True: print("Failed to download Python installer.")
    def getLocalAppData(self):
        import platform
        import os
        ma_os = platform.system()
        if ma_os == "Windows": return os.path.expandvars(r'%LOCALAPPDATA%')
        elif ma_os == "Darwin": return f'{os.path.expanduser("~")}/Library/'
        else: return f'{os.path.expanduser("~")}/'
    def restartScript(self, scriptname: str, argv: list):
        import sys
        import subprocess
        import os
        argv.pop(0)
        subprocess.run(f'"{self.executable}" {os.path.join(os.path.dirname(os.path.abspath(__file__)), scriptname)}{" ".join(argv)}', shell=True)
        sys.exit(0)
    def importModule(self, module_name: str, install_module_if_not_found: bool=False):
        import importlib
        try:
            return importlib.import_module(module_name)
        except ModuleNotFoundError:
            try:
                if install_module_if_not_found == True and self.isSameRunningPythonExecutable(): self.install([module_name])
                return importlib.import_module(module_name)
            except Exception as e:
                raise ImportError(f'Unable to find module "{module_name}" in Python {self.getCurrentPythonVersion()} environment.')
    def copyTreeWithMetadata(self, src: str, dst: str, symlinks=False, ignore=None, dirs_exist_ok=False, ignore_if_not_exist=False):
        import shutil
        import os
        import stat
        if not os.path.exists(src) and ignore_if_not_exist == False: return
        if not dirs_exist_ok and os.path.exists(dst): raise FileExistsError(f"Destination '{dst}' already exists.")
        os.makedirs(dst, exist_ok=True)
        for root, dirs, files in os.walk(src):
            rel_path = os.path.relpath(root, src)
            dst_root = os.path.join(dst, rel_path)
            ignored_names = ignore(root, os.listdir(root)) if ignore else set()
            dirs[:] = [d for d in dirs if d not in ignored_names]
            files = [f for f in files if f not in ignored_names]
            os.makedirs(dst_root, exist_ok=True)
            for dir_name in dirs:
                src_dir = os.path.join(root, dir_name)
                dst_dir = os.path.join(dst_root, dir_name)

                if os.path.islink(src_dir) and symlinks:
                    link_target = os.readlink(src_dir)
                    os.symlink(link_target, dst_dir)
                else:
                    os.makedirs(dst_dir, exist_ok=True)
                    shutil.copystat(src_dir, dst_dir, follow_symlinks=False)
                    os.chmod(dst_dir, os.stat(dst_dir).st_mode | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)
            for file_name in files:
                src_file = os.path.join(root, file_name)
                dst_file = os.path.join(dst_root, file_name)
                if os.path.islink(src_file) and symlinks:
                    link_target = os.readlink(src_file)
                    os.symlink(link_target, dst_file)
                else:
                    shutil.copy2(src_file, dst_file)
                    os.chmod(dst_file, os.stat(dst_file).st_mode | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)
            shutil.copystat(root, dst_root, follow_symlinks=False)
            os.chmod(dst_root, os.stat(dst_root).st_mode | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)
        return dst
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
    def getAmountOfProcesses(self, process_name=""):
        import platform
        import subprocess
        ma_os = platform.system()
        if ma_os == "Windows":
            process = subprocess.Popen(["tasklist"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, _ = process.communicate()
            process_list = output.decode("utf-8")
            return process_list.lower().count(process_name.lower())
        else:
            result = subprocess.run(f"pgrep -f '{process_name}'", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            process_ids = result.stdout.decode("utf-8").strip().split("\n")
            return len([pid for pid in process_ids if pid.isdigit()])
    def getIfConnectedToInternet(self):
        import socket
        try:
            socket.create_connection(("8.8.8.8", 443), timeout=3)
            return True
        except Exception as e:
            return False
    def is32BitWindows(self): 
        import subprocess
        if not self.executable: return False
        if self.isSameRunningPythonExecutable():
            import platform
            return platform.system() == "Windows" and platform.architecture()[0] == "32bit"
        else:
            a = subprocess.run([self.executable, "-c", 'import platform; print(platform.system() == "Windows" and platform.architecture()[0] == "32bit")'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            final = a.stdout.decode()
            return final.replace("\n", "") == "True"
    def isOppositeArchitecture(self):
        import platform
        import os
        ma_os = platform.system()
        ma_arch = platform.machine()
        if not self.executable: return False
        if ma_os == "Windows" and os.path.dirname(self.executable).endswith("-32"): return True
        elif ma_os == "Darwin" and ma_arch.lower() == "arm64" and self.executable.endswith("-intel64"): return True
        return False
    def isSameRunningPythonExecutable(self):
        import os
        import sys
        return os.path.samefile(self.executable, sys.executable)
    def getProcessWindows(self, pid: int):
        import platform
        if (type(pid) is str and pid.isnumeric()) or type(pid) is int:
            if platform.system() == "Windows":
                try:
                    import win32gui # type: ignore
                    import win32process # type: ignore
                except Exception as e:
                    self.install(["pywin32"])
                    win32gui = self.importModule("win32gui")
                    win32process = self.importModule("win32process")
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
                    self.install(["pyobjc-framework-Quartz"])
                    Quartz = self.importModule("Quartz")
                    CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly = Quartz.CGWindowListCopyWindowInfo, Quartz.kCGWindowListOptionOnScreenOnly
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
    def findPython(self, opposite_arch=False, latest=True):
        import os
        import glob
        import platform
        ma_os = platform.system()
        ma_arch = platform.machine()
        if ma_os == "Darwin":
            target_name = "python3"
            if opposite_arch == True and ma_arch == "arm64": target_name = "python3-intel64"
            if os.path.exists(f"/usr/local/bin/{target_name}") and os.path.islink(f"/usr/local/bin/{target_name}"):
                return f"/usr/local/bin/{target_name}"
            else:
                paths = [
                    "/usr/local/bin/python*",
                    "/Library/Frameworks/Python.framework/Versions/*/bin/python*",
                    os.path.expanduser("~/Library/Python/*/bin/python*")
                ]
                found_paths = []
                for path_pattern in paths:
                    found_paths.extend(glob.glob(path_pattern))
                if latest == True: found_paths = sorted(found_paths, reverse=True, key=lambda x: x.split("/")[-2] if "Versions" in x else x)
                for path in found_paths:
                    if os.path.isfile(path):
                        if not (opposite_arch == True) and not (ma_arch.lower() == "arm64" and "intel64" in path): return path
                        elif opposite_arch == True and ma_arch.lower() == "arm64" and "intel64" in path: return path
                return None
        elif ma_os == "Windows":
            paths = [
                os.path.expandvars(r'%LOCALAPPDATA%\\Programs\\Python\\Python*'),
                os.path.expandvars(r'%LOCALAPPDATA%\\Programs\\Python\\Python*\\python.exe'),
                os.path.expandvars(r'%PROGRAMFILES%\\Python*\\python.exe'),
                os.path.expandvars(r'%PROGRAMFILES(x86)%\\Python*\\python.exe')
            ]

            found_paths = []
            for path_pattern in paths:
                found_paths.extend(glob.glob(path_pattern))
            if latest == True: found_paths = sorted(found_paths, reverse=True, key=lambda x: x if x.endswith("python.exe") else x + "\\python.exe")
            for path in found_paths:
                if os.path.isfile(path):
                    if opposite_arch == True and "-32" not in os.path.dirname(path): continue
                    return path
            return None
    def findPythons(self, opposite_arch=False):
        import os
        import glob
        import platform
        ma_os = platform.system()
        ma_arch = platform.machine()
        founded_pythons = []
        if ma_os == "Darwin":
            paths = [
                "/usr/local/bin/python*",
                "/Library/Frameworks/Python.framework/Versions/*/bin/python*",
                "~/Library/Python/*/bin/python*"
            ]
            for path_pattern in paths:
                for path in glob.glob(path_pattern):
                    if os.path.isfile(path):
                        if not (opposite_arch == True) and not (ma_arch.lower() == "arm64" and "intel64" in path): 
                            if path.endswith("t") or path.endswith("config") or path.endswith("m") or os.path.basename(path).startswith("pythonw"): continue
                            pip_class_for_py = pip(executable=path)
                            founded_pythons.append(pip_class_for_py)
                        elif ma_arch.lower() == "arm64" and "intel64" in path and opposite_arch == True:
                            if path.endswith("t") or path.endswith("config") or path.endswith("m") or os.path.basename(path).startswith("pythonw"): continue
                            pip_class_for_py = pip(executable=path)
                            founded_pythons.append(pip_class_for_py)
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
                        if opposite_arch == True and not (os.path.dirname(path).endswith("-32")): continue
                        pip_class_for_py = pip(executable=path)
                        founded_pythons.append(pip_class_for_py)
        return founded_pythons
class plist:
    def readPListFile(self, path: str):
        import os
        if os.path.exists(path) and path.endswith(".plist"):
            import plistlib
            with open(path, "rb") as f:
                plist_data = plistlib.load(f)
            return plist_data
        else:
            return {}
    def writePListFile(self, path: str, data):
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
class Main:
    # System Definitions
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
        "onGameLog",
        "onGameError",
        "onGameWarning",
        "onRobloxVoiceChatMute",
        "onRobloxVoiceChatUnmute",
        "onRobloxVoiceChatStart",
        "onRobloxVoiceChatLeft",
        "onRobloxAudioDeviceStopRecording",
        "onRobloxAudioDeviceStartRecording",
    ]
    robloxStudioInstanceEventNames = [
        "onRobloxExit", 
        "onRobloxLog",
        "onLoadedFFlags",
        "onPlayTestStart",
        "onOpeningGame",
        "onGameUDMUXLoaded",
        "onGameJoined",
        "onHttpResponse",
        "onExpiredFlag",
        "onApplyingFeature",
        "onRobloxChannel",
        "onGameAudioDeviceAvailable",
        "onPluginLoading",
        "onRobloxPublishing",
        "onRobloxCrash",
        "onBloxstrapSDK",
        "onRobloxAudioDeviceStopRecording",
        "onRobloxAudioDeviceStartRecording",
        "onRobloxLauncherDestroyed",
        "onPlayTestDisconnected",
        "onGameLog",
        "onGameError",
        "onGameWarning",
        "onTelemetryLog",
        "onRobloxAppStart",
        "onOtherRobloxLog",
        "onClosingGame",
        "onTeamCreateConnect",
        "onTeamCreateDisconnect",
        "onCloudPlugins",
        "onPluginUnloading",
        "onRobloxSaved",
        "onNewStudioLaunching",
        "onStudioInstallerLaunched"
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
        "onGameLog": {"message": "Allow getting Roblox log messages", "level": 2, "robloxEvent": True}, 
        "onGameWarning": {"message": "Allow getting Roblox warning log messages", "level": 2, "robloxEvent": True}, 
        "onGameError": {"message": "Allow getting Roblox error log messages", "level": 2, "robloxEvent": True}, 
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
        "onRobloxAudioDeviceStartRecording": {"message": "Allow detecting when a game audio device starts recording", "level": 1, "robloxEvent": True},
        "onRobloxAudioDeviceStopRecording": {"message": "Allow detecting when a game audio device stops recording", "level": 1, "robloxEvent": True},
        "onGameAudioDeviceAvailable": {"message": "Allow detecting when a new game audio device is available", "level": 1, "robloxEvent": True},
        "onGameUDMUXLoaded": {"message": "Allow detecting when Roblox Server IPs are loaded", "level": 2, "robloxEvent": True}, 
        "onGameTeleport": {"message": "Allow detecting when you teleport places", "level": 1, "robloxEvent": True}, 
        "onGameTeleportFailed": {"message": "Allow detecting when teleporting fails", "level": 1, "robloxEvent": True}, 
        "onGameJoinInfo": {"message": "Allow getting join info for a game", "level": 2, "robloxEvent": True}, 
        "onGameJoined": {"message": "Allow detecting when Roblox loads a game fully", "level": 0, "robloxEvent": True}, 
        "onGameLeaving": {"message": "Allow detecting when you leave a game", "level": 0, "robloxEvent": True}, 
        "onGameDisconnected": {"message": "Allow detecting when you disconnect from a game", "level": 0, "robloxEvent": True},
        
        "onPlayTestStart": {"message": "Allow detecting when you started a playtest", "level": 0, "robloxEvent": True},
        "onStudioLoginSuccess": {"message": "Allow detecting when you have logged into studio successfully", "level": 1, "robloxEvent": True},
        "onOpeningGame": {"message": "Allow detecting when you loaded a place/document", "level": 1, "robloxEvent": True},
        "onExpiredFlag": {"message": "Allow detecting when a flag in your studio data has expired", "level": 1, "robloxEvent": True},
        "onApplyingFeature": {"message": "Allow detecting when a feature in your studio data is loading", "level": 1, "robloxEvent": True},
        "onPluginLoading": {"message": "Allow detecting when a plugin is loading", "level": 1, "robloxEvent": True},
        "onRobloxPublishing": {"message": "Allow detecting when you are publishing the game", "level": 1, "robloxEvent": True},
        "onPlayTestDisconnected": {"message": "Allow detecting when you disconnect from playtesting.", "level": 1, "robloxEvent": True},
        "onTelemetryLog": {"message": "Allow detecting studio log information.", "level": 2, "robloxEvent": True},
        "onClosingGame": {"message": "Allow detecting when you close a place/document", "level": 1, "robloxEvent": True},
        "onCloudPlugins": {"message": "Allow detecting loading plugins from the web.", "level": 1, "robloxEvent": True},
        "onTeamCreateConnect": {"message": "Allow detecting when you connect to a team connect server.", "level": 1, "robloxEvent": True},
        "onTeamCreateDisconnect": {"message": "Allow detecting when you disconnect to a team connect server.", "level": 1, "robloxEvent": True},
        "onPluginUnloading": {"message": "Allow detecting when a plugin is unloading", "level": 1, "robloxEvent": True},
        "onRobloxSaved": {"message": "Allow detecting when Roblox has saved to Roblox", "level": 1, "robloxEvent": True},
        "onNewStudioLaunching": {"message": "Allow detecting when a new Roblox Studio window is created", "level": 1, "robloxEvent": True},

        # OrangeBlox Permissions
        "fastFlagConfiguration": {"message": "Edit or view your bootstrap configuration file", "level": 3, "detection": "FastFlagConfiguration"},
        "editMainExecutable": {"message": "Edit the main bootstrap executable", "level": 4, "detection": "Main.py"},
        "editRobloxFastFlagInstallerExecutable": {"message": "Edit the RobloxFastFlagInstaller executable", "level": 4, "detection": "RobloxFastFlagInstaller.py"},
        "editOrangeAPIExecutable": {"message": "Edit the OrangeAPI executable", "level": 4, "detection": "OrangeAPI.py"},
        "editModScript": {"message": "Edit ModScript.py executable", "level": 4, "detection": "ModScript.py"},
        "usageOfRobloxFastFlagsInstaller": {"message": "Allow access to use RobloxFastFlagsInstaller directly", "level": 3, "detection": "RobloxFastFlagsInstaller"},
        "notifications": {"message": "Configure or send notifications through Bootstrap", "level": 1, "detection": "AppNotification"},
        "configureModModes": {"message": "Configure your mods", "level": 2, "detection": "Mods"},
        "configureRobloxBranding": {"message": "Configure your Roblox Player's branding", "level": 1, "detection": "RobloxBrand"},
        "configureRobloxStudioBranding": {"message": "Configure your Roblox Studio's branding", "level": 1, "detection": "RobloxStudioBrand"},
        "importOtherModules": {"message": "Import outside modules from source", "level": 2, "detection": "importlib"},
        "runOtherScripts": {"message": "Run other scripts or commands", "level": 2, "detection": "subprocess"},
        "configureDeathSounds": {"message": "Configure your death sounds", "level": 1, "detection": "DeathSounds"},
        "configureCursors": {"message": "Configure your cursors", "level": 1, "detection": "Cursors"},
        "configureAvatarMaps": {"message": "Configure your avatar maps", "level": 1, "detection": "AvatarEditorMaps"},
        "generateModsManifest": {"message": "Get information about all your installed mods", "level": 0},
        "displayNotification": {"message": "Send notifications through the bootstrap", "level": 1},
        "getRobloxAppSettings": {"message": "Get information about the Roblox client such as the logged in user, accessible policies and settings.", "level": 2},
        "getRobloxLogFolderSize": {"message": "Get current size of the Roblox Logs folder", "level": 0},
        "grantFileEditing": {"message": "Grant permissions to read/edit other files", "level": 3},
        "allowAccessingPythonFiles": {"message": "Allow access to other Python files", "level": 2},
        "sendDiscordWebhookMessage": {"message": "Send messages through your Discord Webhooks", "level": 1},
        "sendBloxstrapRPC": {"message": "Send requests through Bloxstrap RPC", "level": 2},
        "getLatestRobloxVersion": {"message": "Get the latest Roblox version", "level": 0},
        "getInstalledRobloxVersion": {"message": "Get the currently installed Roblox version", "level": 1},
        "getLatestOppositeRobloxVersion": {"message": "Get the latest version of the opposite application (Roblox Player -> Studio, Studio -> Player)", "level": 1},
        "getOppositeInstalledRobloxVersion": {"message": "Get the current version of the opposite application (Roblox Player -> Studio, Studio -> Player)", "level": 1},
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
        "setRobloxWindowIcon": {"message": "Set the Roblox Window Icon [Windows Only]", "level": 1},
        "focusRobloxWindow": {"message": "Focus the Roblox Window to the top window", "level": 2},
        "reprepareRoblox": {"message": "Receive the ability to restart preparation when Roblox is not opened.", "level": 2},
        "getConfiguration": {"message": "Get data in a separate configuration", "level": 0, "free": True},
        "setConfiguration": {"message": "Store data in a separate configuration", "level": 0, "free": True},
        "getDebugMode": {"message": "Get if the bootstrap is in Debug Mode", "level": 0, "free": True},
        "printSuccessMessage": {"message": "Print a console in green (indicates success)", "level": 0, "free": True},
        "printMainMessage": {"message": "Print a console in the standard white color", "level": 0, "free": True},
        "printColoredMessage": {"message": "Print a message on the python console using an ANSI 256 bit color number.", "level": 0, "free": True},
        "printErrorMessage": {"message": "Print a console in red (indicates an error)", "level": 0, "free": True},
        "printYellowMessage": {"message": "Print a console in a yellow text (indicates a warning)", "level": 0, "free": True},
        "about": {"message": "Get bootstrap info", "level": 0, "free": True},
    }
    robloxBundleExportFiles = {
        # This list is from Bloxstrap converted to Python
        "RobloxApp.zip": "/",
        "Libraries.zip": "/",
        "redist.zip": "/",
        "shaders.zip": "/shaders",
        "ssl.zip": "/ssl",
        "WebView2.zip": "/",
        "WebView2RuntimeInstaller.zip": "/WebView2RuntimeInstaller",
        "content-avatar.zip": "/content/avatar",
        "content-configs.zip": "/content/configs",
        "content-fonts.zip": "/content/fonts",
        "content-sky.zip": "/content/sky",
        "content-sounds.zip": "/content/sounds",
        "content-textures2.zip": "/content/textures",
        "content-models.zip": "/content/models",
        "content-textures3.zip": "/PlatformContent/pc/textures",
        "content-terrain.zip": "/PlatformContent/pc/terrain",
        "content-platform-fonts.zip": "/PlatformContent/pc/fonts",
        "content-platform-dictionaries.zip": "/PlatformContent/pc/shared_compression_dictionaries",
        "extracontent-luapackages.zip": "/ExtraContent/LuaPackages",
        "extracontent-translations.zip": "/ExtraContent/translations",
        "extracontent-models.zip": "/ExtraContent/models",
        "extracontent-textures.zip": "/ExtraContent/textures",
        "extracontent-places.zip": "/ExtraContent/places"
    }
    robloxStudioBundleExportFiles = {
        # This list is from Bloxstrap converted to Python
        "redist.zip": "/",
        "ApplicationConfig.zip": "/ApplicationConfig",
        "BuiltInPlugins.zip": "/BuiltInPlugins",
        "BuiltInStandalonePlugins.zip": "/BuiltInStandalonePlugins",
        "Plugins.zip": "/Plugins",
        "Qml.zip": "/Qml",
        "StudioFonts.zip": "/StudioFonts",
        "WebView2.zip": "/",
        "WebView2RuntimeInstaller.zip": "/WebView2RuntimeInstaller",
        "RobloxStudio.zip": "/",
        "Libraries.zip": "/",
        "LibrariesQt5.zip": "/",
        "RibbonConfig.zip": "/RibbonConfig",
        "content-avatar.zip": "/content/avatar",
        "content-configs.zip": "/content/configs",
        "content-fonts.zip": "/content/fonts",
        "content-models.zip": "/content/models",
        "content-qt_translations.zip": "/content/qt_translations",
        "content-sky.zip": "/content/sky",
        "content-sounds.zip": "/content/sounds",
        "shaders.zip": "/shaders",
        "ssl.zip": "/ssl",
        "content-textures2.zip": "/content/textures",
        "content-textures3.zip": "/content/textures",
        "content-studio_svg_textures.zip": "/content/studio_svg_textures",
        "content-terrain.zip": "/PlatformContent/pc/terrain",
        "content-platform-fonts.zip": "/PlatformContent/pc/fonts",
        "content-api-docs.zip": "/content/api_docs",
        "extracontent-scripts.zip": "/ExtraContent/scripts",
        "extracontent-luapackages.zip": "/ExtraContent/LuaPackages",
        "extracontent-translations.zip": "/ExtraContent/translations",
        "extracontent-models.zip": "/ExtraContent/models",
        "extracontent-textures.zip": "/ExtraContent/textures"
    }
    
    # System Functions 
    class WatchdogLineResponse():
        code: int=None
        def __init__(self, code: int): self.code = code
        class EndRoblox(): code=0
        class EndWatchdog(): code=1
    class InvalidRobloxHandlerException(Exception):
        def __init__(self): super().__init__("Please make sure you're providing the RobloxFastFlagsInstaller.Main class!")
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
        is_studio = False
        await_20_second_log_creation = False
        await_log_creation_attempts = 0
        windows_roblox_starter_launched_roblox = False
        def __init__(self, main_handler, pid: str, log_file: str="", debug_mode: bool=False, allow_other_logs: bool=False, await_20_second_log_creation: bool=False, created_mutex: bool=None, studio: bool=False):
            if type(main_handler) is Main:
                self.main_handler = main_handler
                self.pid = pid
                self.debug_mode = debug_mode
                self.allow_other_logs = allow_other_logs
                self.created_mutex = created_mutex
                self.is_studio = studio
                self.await_20_second_log_creation = await_20_second_log_creation
                if studio == True:
                    self.event_names = main_handler.robloxStudioInstanceEventNames
                else:
                    self.event_names = main_handler.robloxInstanceEventNames
                if log_file == "" or os.path.exists(log_file):
                    self.main_log_file = log_file
                self.startActivityTracking()
            else:
                raise Main.InvalidRobloxHandlerException()
        def awaitRobloxClosing(self):
            while True:
                time.sleep(1)
                if not self.pid:
                    self.ended_process = True
                    break
                if (self.main_handler.getIfRobloxIsOpen(pid=self.pid) == False) or self.requested_end_tracking == True or (self.ended_process == True):
                    self.ended_process = True
                    break
        def setRobloxEventCallback(self, eventName: robloxInstanceTotalLiteralEventNames, eventCallback: typing.Callable[[typing.Any], None]):
            if callable(eventCallback):
                if eventName in self.event_names:
                    for i in self.events:
                        if i and i["name"] == eventName: self.events.remove(i)
                    self.events.append({"name": eventName, "callback": eventCallback})
                    if self.watchdog_started == False: self.startActivityTracking()
        def addRobloxEventCallback(self, eventName: robloxInstanceTotalLiteralEventNames, eventCallback: typing.Callable[[typing.Any], None]):
            if callable(eventCallback):
                if eventName in self.event_names:
                    self.events.append({"name": eventName, "callback": eventCallback})
                    if self.watchdog_started == False: self.startActivityTracking()
        def getWindowsOpened(self) -> "list[Main.RobloxWindow]":
            if self.pid and not (self.pid == "") and self.pid.isnumeric():
                try:
                    if main_os == "Windows":
                        try:
                            import win32gui # type: ignore
                            import win32process # type: ignore
                        except Exception as e:
                            pip().install(["pywin32"])
                            win32gui = pip().importModule("win32gui")
                            win32process = pip().importModule("win32process")
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
                            pip().install(["pyobjc-framework-Quartz"])
                            Quartz = pip().importModule("Quartz")
                            CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly = Quartz.CGWindowListCopyWindowInfo, Quartz.kCGWindowListOptionOnScreenOnly
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
        def clearRobloxEventCallbacks(self, eventName: robloxInstanceTotalLiteralEventNames=""):
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
                                if self.is_studio == False and "Player" in basename:
                                    paths.append(os.path.join(path, basename))
                                elif self.is_studio == True and "Studio" in basename:
                                    paths.append(os.path.join(path, basename))
                            if len(paths) > 0: return max(paths, key=os.path.getctime)
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
                                    if self.debug_mode == True: 
                                        if type(data) is str and (data.startswith("Settings Date timestamp is") or data.startswith("Settings Date header was")):
                                            if self.allow_other_logs == True: printDebugMessage(f'Event triggered: {eventName}, Data: {data}')
                                        else:
                                            printDebugMessage(f'Event triggered: {eventName}, Data: {data}')
                            for i in self.events:
                                if i and callable(i.get("callback")) and i.get("name") == eventName: threading.Thread(target=i.get("callback"), args=[data]).start()
                        def handleLine(line=""):
                            if self.is_studio == True:
                                if "[FLog::Output] LoadClientSettingsFromLocal" in line:
                                    submitToThread(eventName="onLoadedFFlags", data=line, isLine=True)
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
                                        submitToThread(eventName="onPlayTestStart", data=generated_data, isLine=False)
                                elif "[FLog::StudioKeyEvents] open place" in line:
                                    def generate_arg():
                                        pattern = r"identifier\s*=\s*(\/[^\)\s]+|\d+)"
                                        match = re.search(pattern, line)
                                        if not match:
                                            pattern = r"(?:[a-zA-Z]:\\|\/)(?:[^\/\\\n]+[\/\\])*[^\/\\\n]+"
                                            match = re.findall(pattern, line)
                                            if len(match) < 1:
                                                return None
                                            else:
                                                result = {
                                                    "place_identifier": match[0]
                                                }
                                                return result
                                        else:
                                            result = {
                                                "place_identifier": match.group(1)
                                            }
                                            return result
                                    
                                    generated_data = generate_arg()
                                    if generated_data:
                                        submitToThread(eventName="onOpeningGame", data=generated_data, isLine=False)
                                elif "[FLog::RobloxIDEDoc] RobloxIDEDoc::doClose" in line:
                                    submitToThread(eventName="onClosingGame", data=line, isLine=True)
                                elif "[FLog::StudioKeyEvents] starting Qt main event loop" in line:
                                    submitToThread(eventName="onRobloxAppStart", data=line, isLine=True)
                                elif "[FLog::StudioKeyEvents] login [end][success]" in line:
                                    submitToThread(eventName="onStudioLoginSuccess", data=line, isLine=True)
                                elif "[FLog::StudioKeyEvents] launching new studio instance" in line:
                                    submitToThread(eventName="onNewStudioLaunching", data=line, isLine=True)
                                elif "[FLog::StudioKeyEvents] team create connect (connection accepted)" in line:
                                    submitToThread(eventName="onTeamCreateConnect", data=line, isLine=True)
                                elif "[FLog::StudioKeyEvents] team create disconnect" in line:
                                    submitToThread(eventName="onTeamCreateDisconnect", data=line, isLine=True)
                                elif "[FLog::Output] Web returned cloud plugins:" in line:
                                    def generate_arg():
                                        match = re.search(r'\[([\d,\s]+)\]', line)
                                        if not match:
                                            return None
                                        else:
                                            return list(map(int, match.group(1).split(',')))
                                    generated_data = generate_arg()
                                    if generated_data:
                                        submitToThread(eventName="onCloudPlugins", data=generated_data, isLine=False)
                                elif "[FLog::Output] UpdateUtils::requestInstallerUpdate - Launching Installer for update:" in line:
                                    submitToThread(eventName="onStudioInstallerLaunched", data=line, isLine=True)
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
                                elif "[FLog::Network] serverId:" in line:
                                    def generate_arg():
                                        match = re.search(r'serverId:\s*(\d{1,3}(?:\.\d{1,3}){3})\|(\d+)', line)
                                        if match:
                                            ip = match.group(1)
                                            port = int(match.group(2))
                                            if ip == "127.0.0.1": return
                                            return {
                                                "ip": ip,
                                                "port": port
                                            }
                                        
                                    generated_data = generate_arg()
                                    if generated_data:
                                        submitToThread(eventName="onGameJoined", data=generated_data, isLine=False)
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
                                elif "[FLog::Error] Redundant Flag ID:" in line:
                                    def generate_arg():
                                        pattern = r"Redundant Flag ID:\s+([\w\d_]+)"
                                        match = re.search(pattern, line)
                                        if not match:
                                            return None
                                        else:
                                            result = {
                                                "flag_id": match.group(1)
                                            }
                                            return result
                                    generated_data = generate_arg()
                                    if generated_data:
                                        submitToThread(eventName="onExpiredFlag", data=generated_data, isLine=False)
                                elif "[FLog::BetaFeatures] Applying settings for beta feature id" in line:
                                    def generate_arg():
                                        pattern = r"beta feature id (\w+)"
                                        match = re.search(pattern, line)
                                        if not match:
                                            return None
                                        else:
                                            result = {
                                                "feature_id": match.group(1)
                                            }
                                            return result
                                    generated_data = generate_arg()
                                    if generated_data:
                                        submitToThread(eventName="onApplyingFeature", data=generated_data, isLine=False)
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
                                elif "[FLog::PluginLoadingEnhanced] Running plugin" in line:
                                    def generate_arg():
                                        pattern = r"plugin '([\w\d_]+)'\s+in datamodel (\w+)"
                                        match = re.search(pattern, line)
                                        if not match:
                                            return None
                                        else:
                                            result = {
                                                "plugin_id": match.group(1),
                                                "datamodel": match.group(2),
                                            }
                                            return result
                                    generated_data = generate_arg()
                                    if generated_data:
                                        submitToThread(eventName="onPluginLoading", data=generated_data, isLine=False)
                                elif "[FLog::PluginLoadingEnhanced] Unloading plugin" in line:
                                    def generate_arg():
                                        pattern = r"plugin '([\w\d_]+)'\s+in datamodel (\w+)"
                                        match = re.search(pattern, line)
                                        if not match:
                                            return None
                                        else:
                                            result = {
                                                "plugin_id": match.group(1),
                                                "datamodel": match.group(2),
                                            }
                                            return result
                                    generated_data = generate_arg()
                                    if generated_data:
                                        submitToThread(eventName="onPluginUnloading", data=generated_data, isLine=False)
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
                                elif "[FLog::StudioTimingLog] ======== Studio Publish Place Times =======" in line:
                                    submitToThread(eventName="onRobloxPublishing", data=line, isLine=True)
                                elif "[FLog::StudioTimingLog] ======== Studio Save To Cloud Times =======" in line:
                                    submitToThread(eventName="onRobloxSaved", data=line, isLine=True)
                                elif "RBXCRASH:" in line or "[FLog::CrashReportLog] Terminated" in line:
                                    submitToThread(eventName="onRobloxCrash", data=line, isLine=True)
                                elif "RobloxAudioDevice::StopRecording" in line:
                                    submitToThread(eventName="onRobloxAudioDeviceStopRecording", data=line, isLine=True)
                                elif "RobloxAudioDevice::StartRecording" in line:
                                    submitToThread(eventName="onRobloxAudioDeviceStartRecording", data=line, isLine=True)
                                elif "[FLog::Output] About to exit the application, doing cleanup." in line:
                                    if self.windows_roblox_starter_launched_roblox == False:
                                        submitToThread(eventName="onRobloxExit", data=line)
                                        submitToThread(eventName="onRobloxSharedLogLaunch", data=line)
                                        return self.main_handler.WatchdogLineResponse.EndWatchdog()
                                    else:
                                        submitToThread(eventName="onRobloxLauncherDestroyed", data=line)
                                elif "[FLog::Network] Client:Disconnect" in line:
                                    if self.disconnect_cooldown == False:
                                        self.disconnect_cooldown = True
                                        def b():
                                            time.sleep(3)
                                            self.disconnect_cooldown = False
                                        threading.Thread(target=b, daemon=True).start()
                                        submitToThread(eventName="onPlayTestDisconnected", data=None, isLine=False)
                                elif "[FLog::Output]" in line:
                                    def generate_arg():
                                        output = line.find('[FLog::Output]') + len('[FLog::Output] ')
                                        if output == -1:
                                            return None
                                        return line[output:].strip()
                                    generated_data = generate_arg()
                                    if generated_data:
                                        submitToThread(eventName="onGameLog", data=generated_data, isLine=False)
                                elif "[FLog::Error]" in line:
                                    def generate_arg():
                                        output = line.find('[FLog::Error]') + len('[FLog::Error] ')
                                        if output == -1:
                                            return None
                                        return line[output:].strip()
                                    generated_data = generate_arg()
                                    if generated_data:
                                        submitToThread(eventName="onGameError", data=generated_data, isLine=False)
                                elif "[FLog::Warning]" in line:
                                    def generate_arg():
                                        output = line.find('[FLog::Warning]') + len('[FLog::Warning] ')
                                        if output == -1:
                                            return None
                                        return line[output:].strip()
                                    generated_data = generate_arg()
                                    if generated_data:
                                        submitToThread(eventName="onGameWarning", data=generated_data, isLine=False)
                                elif "[telemetryLog]" in line:
                                    def generate_arg():
                                        output = line.find('[telemetryLog]') + len('[telemetryLog] ')
                                        if output == -1:
                                            return None
                                        return line[output:].strip()
                                    generated_data = generate_arg()
                                    if generated_data:
                                        submitToThread(eventName="onTelemetryLog", data=generated_data, isLine=False)
                                else:
                                    submitToThread(eventName="onOtherRobloxLog", data=line, isLine=True)
                            else:
                                if "[FLog::RobloxStarter] RobloxStarter destroyed" in line:
                                    if self.windows_roblox_starter_launched_roblox == False:
                                        submitToThread(eventName="onRobloxExit", data=line)
                                        submitToThread(eventName="onRobloxSharedLogLaunch", data=line)
                                        return self.main_handler.WatchdogLineResponse.EndWatchdog()
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
                                elif "[FLog::Warning] WebLogin authentication is failed and App is quitting" in line or "[FLog::Warning] (RobloxPlayerAppDelegate) WebLogin authentication failure" in line:
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
                                elif "[FLog::Error]" in line:
                                    def generate_arg():
                                        output = line.find('[FLog::Error]') + len('[FLog::Error] ')
                                        if output == -1:
                                            return None
                                        return line[output:].strip()
                                    generated_data = generate_arg()
                                    if generated_data:
                                        submitToThread(eventName="onGameError", data=generated_data, isLine=False)
                                elif "[FLog::Warning]" in line:
                                    def generate_arg():
                                        output = line.find('[FLog::Warning]') + len('[FLog::Warning] ')
                                        if output == -1:
                                            return None
                                        return line[output:].strip()
                                    generated_data = generate_arg()
                                    if generated_data:
                                        submitToThread(eventName="onGameWarning", data=generated_data, isLine=False)
                                else:
                                    submitToThread(eventName="onOtherRobloxLog", data=line, isLine=True)
                        if self.main_log_file == "":
                            self.await_log_creation_attempts = 0
                            def getLogFile():
                                logs_path = None
                                if main_os == "Darwin":
                                    logs_path = os.path.join(user_folder, "Library", "Logs", "Roblox")
                                elif main_os == "Windows":
                                    logs_path = os.path.join(windows_dir, "logs")
                                else:
                                    logs_path = os.path.join(user_folder, "Library", "Logs", "Roblox")
                                makedirs(logs_path)
                                main_log = newest(logs_path)
                                if not main_log:
                                    time.sleep(0.5)
                                    return getLogFile()
                                if not main_log.endswith(".log"):
                                    time.sleep(0.5)
                                    return getLogFile()
                                logs_attached = []
                                if os.path.exists(os.path.join(logs_path, "RFFILogFiles.json")):
                                    with open(os.path.join(logs_path, "RFFILogFiles.json"), "r", encoding="utf-8") as f:
                                        logs_attached = json.load(f)
                                if self.await_20_second_log_creation == True:
                                    if self.await_log_creation_attempts < 40:
                                        if fileCreatedRecently(main_log):
                                            if main_log in logs_attached:
                                                time.sleep(0.5)
                                                self.await_log_creation_attempts += 1
                                                return getLogFile()
                                            else:
                                                logs_attached.append(main_log)
                                                with open(os.path.join(logs_path, "RFFILogFiles.json"), "w", encoding="utf-8") as f:
                                                    json.dump(logs_attached, f, indent=4)
                                                return main_log
                                        else:
                                            time.sleep(0.5)
                                            self.await_log_creation_attempts += 1
                                            return getLogFile()
                                    else:
                                        logs_attached.append(main_log)
                                        with open(os.path.join(logs_path, "RFFILogFiles.json"), "w", encoding="utf-8") as f:
                                            json.dump(logs_attached, f, indent=4)
                                        return main_log
                                else:
                                    logs_attached.append(main_log)
                                    with open(os.path.join(logs_path, "RFFILogFiles.json"), "w", encoding="utf-8") as f:
                                        json.dump(logs_attached, f, indent=4)
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
                                            if filtered_line == current_log or "[FLog::WndProcessCheck]" in line or "[FLog::FMOD] FMOD API error" in line or "HttpResponse(" in line:
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
                                            try:
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
                                            except Exception as e:
                                                if self.debug_mode == True: printDebugMessage(f"Unable to read log: {str(e)}")
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
                    win32gui = pip().importModule("win32gui")
                    win32process = pip().importModule("win32process")
                win32gui.SetFocus(self.system_handler)
            elif main_os == "Darwin":
                subprocess.run(["osascript", "-e", f'tell application "System Events" to set frontmost of (every process whose unix id is {self.pid}) to true'])
        def destroyWindow(self):
            if main_os == "Windows":
                try:
                    import win32gui # type: ignore
                    import win32process # type: ignore
                except Exception as e:
                    pip().install(["pywin32"])
                    win32gui = pip().importModule("win32gui")
                    win32process = pip().importModule("win32process")
                win32gui.DestroyWindow(self.system_handler)
            elif main_os == "Darwin":
                Main().endRoblox(str(self.pid))
        def setWindowTitle(self, title: str):
            if main_os == "Windows":
                try:
                    import win32gui # type: ignore
                except Exception as e:
                    pip().install(["pywin32"])
                    win32gui = pip().importModule("win32gui")
                win32gui.SetWindowText(self.system_handler, title)
            elif main_os == "Darwin":
                printLog("Setting Window Title is unavailable for macOS.")
        def setWindowIcon(self, icon: str):
            if main_os == "Windows":
                try:
                    import win32gui # type: ignore
                    import win32con # type: ignore
                except Exception as e:
                    pip().install(["pywin32"])
                    win32gui = pip().importModule("win32gui")
                    win32con = pip().importModule("win32con")
                if not type(icon) is str or not icon.endswith(".ico"): raise Exception("This icon is not an ico file!")
                Icon = win32gui.LoadImage(
                    None,
                    icon,
                    win32con.IMAGE_ICON,
                    128, 128,
                    win32con.LR_LOADFROMFILE
                )
                win32gui.SendMessage(self.system_handler, win32con.WM_SETICON, win32con.ICON_SMALL, Icon)
                win32gui.SendMessage(self.system_handler, win32con.WM_SETICON, win32con.ICON_BIG, Icon)
            elif main_os == "Darwin":
                printLog("Setting Window Icons is unavailable for macOS.")
        def setWindowPositionAndSize(self, size_x: int, size_y: int, position_x: int, position_y: int):
            if main_os == "Windows":
                try:
                    import win32gui # type: ignore
                except Exception as e:
                    pip().install(["pywin32"])
                    win32gui = pip().importModule("win32gui")
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
                    end tell'''])
                except Exception as e:
                    printLog(f"Failed to execute AppleScript: {e}")
        def setWindowPosition(self, position_x: int, position_y: int):
            if main_os == "Windows":
                try:
                    import win32gui # type: ignore
                except Exception as e:
                    pip().install(["pywin32"])
                    win32gui = pip().importModule("win32gui")
                win32gui.SetWindowPos(self.system_handler, win32gui.HWND_TOP, None, None, position_x, position_y, win32gui.SWP_SHOWWINDOW)
            elif main_os == "Darwin":
                try:
                    process = subprocess.run(["osascript", "-e", f'''
                    tell application "System Events"
                        set theProcess to (first process whose unix id is {self.pid})
                        if (count of windows of theProcess) > 0 then
                            set theWindow to window 1 of theProcess
                            set position of theWindow to {{{position_x}, {position_y}}}
                        end if
                    end tell'''])
                except Exception as e:
                    printLog(f"Failed to execute AppleScript: {e}")
        def setWindowSize(self, size_x: int, size_y: int):
            if main_os == "Windows":
                try:
                    import win32gui # type: ignore
                except Exception as e:
                    pip().install(["pywin32"])
                    win32gui = pip().importModule("win32gui")
                win32gui.SetWindowPos(self.system_handler, win32gui.HWND_TOP, size_x, size_y, win32gui.SWP_SHOWWINDOW)
            elif main_os == "Darwin":
                try:
                    process = subprocess.run(["osascript", "-e", f'''
                    tell application "System Events"
                        set theProcess to (first process whose unix id is {self.pid})
                        if (count of windows of theProcess) > 0 then
                            set theWindow to window 1 of theProcess
                            set size of theWindow to {{{size_x}, {size_y}}}
                        end if
                    end tell'''])
                except Exception as e:
                    printLog(f"Failed to execute AppleScript: {e}")
        def getWindowPositionAndSize(self):
            if main_os == "Windows":
                try:
                    import win32gui # type: ignore
                except Exception as e:
                    pip().install(["pywin32"])
                    win32gui = pip().importModule("win32gui")
                x, y, x1, y1 = win32gui.GetWindowRect(self.system_handler)
                return (x, y), (x1 - x, y1 - y)
            elif main_os == "Darwin":
                try:
                    from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly
                except Exception as e:
                    pip().install(["pyobjc-framework-Quartz"])
                    Quartz = pip().importModule("Quartz")
                    CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly = Quartz.CGWindowListCopyWindowInfo, Quartz.kCGWindowListOptionOnScreenOnly
                window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, 0)
                for window in window_list:
                    if str(window.get("kCGWindowOwnerPID")) == str(self.pid):
                        bounds = window.get("kCGWindowBounds", {})
                        if bounds:
                            x, y, width, height = bounds['X'], bounds['Y'], bounds['Width'], bounds['Height']
                            return (x, y), (width, height)
            return None, None
    class CustomizableVariables():
        def __init__(self, org_macOS_dir, org_macOS_studioDir, org_macOS_beforeClientServices, org_macOS_installedPath, org_windows_dir, org_windows_versions_dir, org_windows_player_folder_name, org_windows_studio_folder_name):
            self.org_macOS_dir = org_macOS_dir
            self.org_macOS_studioDir = org_macOS_studioDir
            self.org_macOS_beforeClientServices = org_macOS_beforeClientServices
            self.org_macOS_installedPath = org_macOS_installedPath
            self.org_windows_dir = org_windows_dir
            self.org_windows_versions_dir = org_windows_versions_dir
            self.org_windows_player_folder_name = org_windows_player_folder_name
            self.org_windows_studio_folder_name = org_windows_studio_folder_name
        def set(self):
            global macOS_dir
            global macOS_studioDir
            global macOS_beforeClientServices
            global macOS_installedPath
            global windows_dir
            global windows_versions_dir
            global windows_player_folder_name
            global windows_studio_folder_name

            macOS_dir = self.org_macOS_dir
            macOS_studioDir = self.org_macOS_studioDir
            macOS_beforeClientServices = self.org_macOS_beforeClientServices
            macOS_installedPath = self.org_macOS_installedPath
            windows_dir = self.org_windows_dir
            windows_versions_dir = self.org_windows_versions_dir
            windows_player_folder_name = self.org_windows_player_folder_name
            windows_studio_folder_name = self.org_windows_studio_folder_name
    class SubmitStatus():
        current_percentage = 0
        status_text = ""
        callable: typing.Callable[[int, str], None] = None
        def submit(self, status_text: str, percentage: int):
            self.current_percentage = percentage
            self.status_text = status_text
            self.callable(percentage, status_text)
    def endRoblox(self, pid=""):
        if self.getIfRobloxIsOpen():
            if pid == "":
                if self.__main_os__ == "Darwin":
                    subprocess.run("killall -9 RobloxPlayer", shell=True, stdout=subprocess.DEVNULL)
                elif self.__main_os__ == "Windows":
                    subprocess.run("taskkill /IM RobloxPlayerBeta.exe /F", shell=True, stdout=subprocess.DEVNULL)
                else:
                    printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
            else:
                if self.__main_os__ == "Darwin":
                    subprocess.run(f"kill -9 {pid}", shell=True, stdout=subprocess.DEVNULL)
                elif self.__main_os__ == "Windows":
                    subprocess.run(f"taskkill /PID {pid} /F", shell=True, stdout=subprocess.DEVNULL)
                else:
                    printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
    def endRobloxStudio(self, pid=""):
        if self.getIfRobloxStudioIsOpen():
            if pid == "":
                if self.__main_os__ == "Darwin":
                    subprocess.run("killall -9 RobloxStudio", shell=True, stdout=subprocess.DEVNULL)
                elif self.__main_os__ == "Windows":
                    subprocess.run("taskkill /IM RobloxStudioBeta.exe /F", shell=True, stdout=subprocess.DEVNULL)
                else:
                    printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
            else:
                if self.__main_os__ == "Darwin":
                    subprocess.run(f"kill -9 {pid}", shell=True, stdout=subprocess.DEVNULL)
                elif self.__main_os__ == "Windows":
                    subprocess.run(f"taskkill /PID {pid} /F", shell=True, stdout=subprocess.DEVNULL)
                else:
                    printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
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
                    if subprocess.run(["pgrep", "-f", f"{os.path.join(macOS_dir, macOS_beforeClientServices, 'RobloxPlayer')}"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).returncode == 0:
                        return True
                    else:
                        return False
                else:
                    if subprocess.run(["pgrep", "-f", f"{os.path.join(macOS_dir, macOS_beforeClientServices, 'RobloxPlayerInstaller')}"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).returncode == 0:
                        return True
                    else:
                        return False
            else:
                if subprocess.run(["ps", "-p", f"{pid}"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).returncode == 0:
                    return True
                else:
                    return False
        else:
            printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
            return
    def getIfRobloxStudioIsOpen(self, installer=False, pid=""):
        if self.__main_os__ == "Windows":
            process = subprocess.Popen(["tasklist"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, _ = process.communicate()
            process_list = output.decode("utf-8")

            if pid == "" or pid == None:
                if installer == False:
                    if process_list.rfind("RobloxStudioBeta.exe") == -1:
                        return False
                    else:
                        return True
                else:
                    if process_list.rfind("RobloxStudioInstaller.exe") == -1:
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
                    if subprocess.run(["pgrep", "-f", f"{os.path.join(macOS_studioDir, macOS_beforeClientServices, 'RobloxStudio')}"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).returncode == 0:
                        return True
                    else:
                        return False
                else:
                    if subprocess.run(["pgrep", "-f", f"{os.path.join(macOS_studioDir, macOS_beforeClientServices, 'RobloxStudioInstaller')}"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).returncode == 0:
                        return True
                    else:
                        return False
            else:
                if subprocess.run(["ps", "-p", f"{pid}"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).returncode == 0:
                    return True
                else:
                    return False
        else:
            printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
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
                requests = pip().importModule("requests")
                printSuccessMessage("Successfully installed modules!")
            else:
                printErrorMessage("Returning back to application.")
                return {"success": False, "message": "User rejected need of module."}

        try:    
            if channel == "production": channel = "LIVE"
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
                        return {"success": True, "client_version": jso.get("clientVersionUpload"), "hash": jso.get("version"), "attempted_channel": channel or "LIVE"}
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
                        return {"success": True, "client_version": jso.get("clientVersionUpload"), "hash": jso.get("version"), "attempted_channel": channel or "LIVE"}
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
                printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
                return {"success": False, "message": "OS not compatible."}
        except Exception as e:
            return {"success": False, "message": "There was an error checking. Please check your internet connection!"}
    def getCurrentClientVersion(self):
        if self.__main_os__ == "Darwin":
            if os.path.exists(os.path.join(macOS_dir, "Contents", "Info.plist")):
                read_plist = plist().readPListFile(os.path.join(macOS_dir, "Contents", "Info.plist"))
                if read_plist.get("CFBundleShortVersionString"):
                    version_channel = "LIVE"
                    try:
                        if os.path.exists(os.path.join(user_folder, "Library", "Preferences", "com.roblox.RobloxPlayerChannel.plist")):
                            read_install_plist = plist().readPListFile(os.path.join(user_folder, "Library", "Preferences", "com.roblox.RobloxPlayerChannel.plist"))
                            if read_install_plist.get("www.roblox.com") and not read_install_plist.get("www.roblox.com") == "":
                                version_channel = read_install_plist.get("www.roblox.com", "LIVE")
                    except Exception:
                        version_channel = "LIVE"
                    client_vers = None
                    if os.path.exists(os.path.join(macOS_dir, "Contents", "MacOS", "RobloxVersion.json")):
                        with open(os.path.join(macOS_dir, "Contents", "MacOS", "RobloxVersion.json"), "r", encoding="utf-8") as f:
                            vers_js = json.load(f)
                        client_vers = vers_js.get("ClientVersion")
                    return {"success": True, "client_version": client_vers, "version": read_plist["CFBundleShortVersionString"], "channel": version_channel}
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
                client_vers = os.path.basename(os.path.dirname(res))
                app_vers = None
                if os.path.exists(os.path.join(res, "RobloxVersion.json")):
                    with open(os.path.join(res, "RobloxVersion.json"), "r", encoding="utf-8") as f:
                        vers_js = json.load(f)
                    client_vers = vers_js.get("ClientVersion")
                    app_vers = vers_js.get("AppVersion")
                return {"success": True, "client_version": client_vers, "version": app_vers, "channel": version_channel}
            else:
                return {"success": False, "message": "Roblox not installed."}
        else:
            printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
            return {"success": False, "message": "OS not compatible."}
    def getLatestStudioClientVersion(self, debug=False, channel="LIVE"):
        # Mac: https://clientsettingscdn.roblox.com/v2/client-version/MacStudio
        # Windows: https://clientsettingscdn.roblox.com/v2/client-version/WindowsStudio64 | https://clientsettingscdn.roblox.com/v2/client-version/WindowsStudio

        try:
            import requests
        except Exception as e:
            printMainMessage("This application is requesting for the latest Roblox version but needs a module. Would you like to install it? (y/n)")
            if isYes(input("> ")) == True:
                pip().install(["requests"])
                requests = pip().importModule("requests")
                printSuccessMessage("Successfully installed modules!")
            else:
                printErrorMessage("Returning back to application.")
                return {"success": False, "message": "User rejected need of module."}

        try:    
            if channel == "production": channel = "LIVE"
            if self.__main_os__ == "Darwin":
                if debug == True: printDebugMessage("Sending Request to Roblox Servers..") 
                if channel:
                    res = requests.get(f"https://clientsettingscdn.roblox.com/v2/client-version/MacStudio/channel/{channel}")
                else:
                    res = requests.get(f"https://clientsettingscdn.roblox.com/v2/client-version/MacStudio")
                if res.ok:
                    jso = res.json()
                    if jso.get("clientVersionUpload") and jso.get("version"):
                        if debug == True: printDebugMessage(f"Called ({res.url}): {res.text}")
                        return {"success": True, "client_version": jso.get("clientVersionUpload"), "hash": jso.get("version"), "attempted_channel": channel or "LIVE"}
                    else:
                        if debug == True: printDebugMessage(f"Something went wrong: {res.text}")
                        return {"success": False, "message": "Something went wrong."}
                else:
                    if not (channel == "LIVE"):
                        if debug == True: printDebugMessage(f"Roblox rejected update check with channel {channel}, retrying as channel LIVE: {res.text}")
                        return self.getLatestStudioClientVersion(debug=debug, channel="LIVE")
                    else:
                        if debug == True: printDebugMessage(f"Something went wrong: {res.text}")
                        return {"success": False, "message": "Something went wrong."}
            elif self.__main_os__ == "Windows":
                if debug == True: printDebugMessage("Sending Request to Roblox Servers..") 
                is32Bit = pip().is32BitWindows()
                if channel:
                    res = requests.get(f"https://clientsettingscdn.roblox.com/v2/client-version/WindowsStudio{is32Bit == True and '' or '64'}/channel/{channel}")
                else:
                    res = requests.get(f"https://clientsettingscdn.roblox.com/v2/client-version/WindowsStudio{is32Bit == True and '' or '64'}")
                if res.ok:
                    jso = res.json()
                    if jso.get("clientVersionUpload") and jso.get("version"):
                        if debug == True: printDebugMessage(f"Called ({res.url}): {res.text}")
                        return {"success": True, "client_version": jso.get("clientVersionUpload"), "hash": jso.get("version"), "attempted_channel": channel or "LIVE"}
                    else:
                        if debug == True: printDebugMessage(f"Something went wrong: {res.text}")
                        return {"success": False, "message": "Something went wrong."}
                else:
                    if not (channel == "LIVE"):
                        if debug == True: printDebugMessage(f"Roblox rejected update check with channel {channel}, retrying as channel LIVE: {res.text}")
                        return self.getLatestStudioClientVersion(debug=debug, channel="LIVE")
                    else:
                        if debug == True: printDebugMessage(f"Something went wrong: {res.text}")
                        return {"success": False, "message": "Something went wrong."}
            else:
                printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
                return {"success": False, "message": "OS not compatible."}
        except Exception as e:
            return {"success": False, "message": "There was an error checking. Please check your internet connection!"}
    def getCurrentStudioClientVersion(self):
        if self.__main_os__ == "Darwin":
            if os.path.exists(os.path.join(macOS_studioDir, "Contents", "Info.plist")):
                read_plist = plist().readPListFile(os.path.join(macOS_studioDir, "Contents", "Info.plist"))
                if read_plist.get("CFBundleShortVersionString"):
                    version_channel = "LIVE"
                    try:
                        if os.path.exists(os.path.join(user_folder, "Library", "Preferences", "com.roblox.RobloxStudioChannel.plist")):
                            read_install_plist = plist().readPListFile(os.path.join(user_folder, "Library", "Preferences", "com.roblox.RobloxStudioChannel.plist"))
                            if read_install_plist.get("www.roblox.com") and not read_install_plist.get("www.roblox.com") == "":
                                version_channel = read_install_plist.get("www.roblox.com", "LIVE")
                    except Exception:
                        version_channel = "LIVE"
                    vers = None
                    if os.path.exists(os.path.join(macOS_studioDir, "Contents", "MacOS", "RobloxVersion.json")):
                        with open(os.path.join(macOS_studioDir, "Contents", "MacOS", "RobloxVersion.json"), "r", encoding="utf-8") as f:
                            vers_js = json.load(f)
                        vers = vers_js.get("ClientVersion")
                    return {"success": True, "client_version": vers, "version": read_plist["CFBundleShortVersionString"], "channel": version_channel}
                else:
                    return {"success": False, "message": "Something went wrong."}
            else:
                return {"success": False, "message": "Roblox not installed."}
        elif self.__main_os__ == "Windows":
            res = self.getRobloxInstallFolder(studio=True)
            if res:
                import winreg
                version_channel = ""
                try:
                    registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\ROBLOX Corporation\Environments\RobloxStudio\Channel", 0, winreg.KEY_READ)
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
                client_vers = os.path.basename(os.path.dirname(res))
                app_vers = None
                if os.path.exists(os.path.join(res, "RobloxVersion.json")):
                    with open(os.path.join(res, "RobloxVersion.json"), "r", encoding="utf-8") as f:
                        vers_js = json.load(f)
                    client_vers = vers_js.get("ClientVersion")
                    app_vers = vers_js.get("AppVersion")
                return {"success": True, "client_version": client_vers, "version": app_vers, "channel": version_channel}
            else:
                return {"success": False, "message": "Roblox not installed."}
        else:
            printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
            return {"success": False, "message": "OS not compatible."}
    def getRobloxInstallFolder(self, directory="", studio=False):
        if self.__main_os__ == "Windows":
            versions = None
            if directory == "":
                if os.path.exists(windows_versions_dir) and os.path.isdir(windows_versions_dir): versions = [os.path.join(windows_versions_dir, folder) for folder in os.listdir(windows_versions_dir) if os.path.isdir(os.path.join(windows_versions_dir, folder))]
            else:
                if os.path.exists(directory) and os.path.isdir(directory): versions = [os.path.join(directory, folder) for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))]
            formatted = []
            if not versions:
                return None
            for fold in versions:
                if os.path.isdir(fold):
                    if studio == True:
                        if os.path.exists(os.path.join(fold, "RobloxStudioBeta.exe")): formatted.append(fold)
                    else:
                        if os.path.exists(os.path.join(fold, "RobloxPlayerBeta.exe")) and os.path.exists(os.path.join(fold, "RobloxPlayerBeta.dll")) and os.path.exists(os.path.join(fold, "RobloxCrashHandler.exe")): formatted.append(fold)
            if len(formatted) > 0:
                latest_folder = max(formatted, key=os.path.getmtime)
                return latest_folder
            else:
                return None
        elif self.__main_os__ == "Darwin":
            return studio == True and f"{macOS_studioDir}/" or f"{macOS_dir}/"
        else:
            printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
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
    def getLatestOpenedRobloxStudioPid(self):
        if self.__main_os__ == "Darwin":
            try:
                result = subprocess.run(["ps", "axo", "pid,etime,command"], stdout=subprocess.PIPE, text=True)
                processes = result.stdout
                roblox_lines = [line for line in processes.splitlines() if "RobloxStudio" in line]
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
                program_lines = [line for line in processes.splitlines() if "RobloxStudioBeta.exe" in line]
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
    def getOpenedRobloxStudioPids(self):
        if self.__main_os__ == "Darwin":
            try:
                result = subprocess.run(["ps", "axo", "pid,etime,command"], stdout=subprocess.PIPE, text=True)
                processes = result.stdout
                roblox_lines = [line for line in processes.splitlines() if "RobloxStudio" in line]
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
                program_lines = [line for line in processes.splitlines() if "RobloxStudioBeta.exe" in line]
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
    def getAllOpenedRobloxStudioWindows(self) -> "list[RobloxWindow]":
        pids = self.getOpenedRobloxStudioPids()
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
    def getRobloxAppSettings(self):
        appStorage = {}
        if self.__main_os__ == "Darwin":
            try:
                if os.path.exists(os.path.join(user_folder, "Library", "Roblox", "LocalStorage", "appStorage.json")):
                    appStorage = json.load(open(os.path.join(user_folder, "Library", "Roblox", "LocalStorage", "appStorage.json"), "r", encoding="utf-8"))
            except Exception:
                appStorage = {}
        elif self.__main_os__ == "Windows":
            try:
                if os.path.exists(os.path.join(windows_dir, "LocalStorage", "appStorage.json")):
                    appStorage = json.load(open(os.path.join(windows_dir, "LocalStorage", "appStorage.json"), "r", encoding="utf-8"))
            except Exception:
                appStorage = {}
        else:
            printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
            return {"success": False, "message": "OS not compatible."}
        return {
            "success": True, 
            "loggedInUser": {
                "id": (type(appStorage.get("UserId")) is str and appStorage.get("UserId").isnumeric()) and int(appStorage.get("UserId")) or None,
                "name": appStorage.get("Username"),
                "under13": appStorage.get("IsUnder13")=="true",
                "displayName": appStorage.get("DisplayName"),
                "countryCode": appStorage.get("CountryCode"),
                "membership": appStorage.get("Membership"),
                "membershipActive": not (appStorage.get("Membership")=="0"),
                "theme": appStorage.get("AuthenticatedTheme")
            },
            "outputDeviceGUID": appStorage.get("SelectedOutputDeviceGuid"),
            "robloxLocaleId": appStorage.get("RobloxLocaleId"),
            "browerTrackerId": appStorage.get("BrowserTrackerId"),
            "appConfiguration": appStorage.get("AppConfiguration") and json.loads(appStorage.get("AppConfiguration")) or {},
            "experimentCache": appStorage.get("ExperimentCache") and json.loads(appStorage.get("ExperimentCache")) or {},
            "policyServiceResponse": appStorage.get("PolicyServiceHttpResponse") and json.loads(appStorage.get("PolicyServiceHttpResponse")) or {}
        }
    def getRobloxGlobalBasicSettings(self, studio=False):
        import xml.etree.ElementTree as ET
        roblox_app_location = ""
        if self.__main_os__ == "Darwin":
            roblox_app_location = os.path.join(user_folder, "Library", "Roblox")
        elif self.__main_os__ == "Windows":
            roblox_app_location = windows_dir
        else:
            printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
            return {"success": False, "message": "OS not compatible."}   
        def convertToBestValue(value: str):
            if value == None: return None
            if value.lower() == "true":
                return True
            elif value.lower() == "false":
                return False
            try:
                if "." in value: return float(value)
                return int(value)
            except ValueError:
                return value 
        file_name = None
        for i in os.listdir(roblox_app_location):
            if not (i.find("GlobalBasicSettings") == -1):
                if studio == True and i.find("_Studio") == -1: continue
                file_name = i
        if file_name:
            with open(os.path.join(roblox_app_location, file_name), "r", encoding="utf-8") as f:
                xml_contents = f.read()
            xml_root = ET.fromstring(xml_contents)
            final_settings = {}
            for prop in xml_root.findall(".//Properties/*"):
                prop_key = prop.get("name")
                if prop.tag == "Vector2":
                    final_settings[prop_key] = {"type": prop.tag, "data": (convertToBestValue(prop.find("X").text), convertToBestValue(prop.find("Y").text))}
                else:
                    final_settings[prop_key] = {"type": prop.tag, "data": convertToBestValue(prop.text)}
            return {"success": True, "data": final_settings}
        else:
            return {"success": False, "message": "Unable to find settings file."} 
    def temporaryResetCustomizableVariables(self):
        global macOS_dir
        global macOS_studioDir
        global macOS_beforeClientServices
        global macOS_installedPath
        global windows_dir
        global windows_versions_dir
        global windows_player_folder_name
        global windows_studio_folder_name

        org_macOS_dir = macOS_dir
        org_macOS_studioDir = macOS_studioDir
        org_macOS_beforeClientServices = macOS_beforeClientServices
        org_macOS_installedPath = macOS_installedPath
        org_windows_dir = windows_dir
        org_windows_versions_dir = windows_versions_dir
        org_windows_player_folder_name = windows_player_folder_name
        org_windows_studio_folder_name = windows_studio_folder_name

        macOS_dir = "/Applications/Roblox.app"
        macOS_studioDir = "/Applications/RobloxStudio.app"
        macOS_beforeClientServices = "/Contents/MacOS/"
        macOS_installedPath = "/Applications/"
        windows_dir = f"{os.getenv('LOCALAPPDATA')}\\Roblox"
        windows_versions_dir = f"{windows_dir}\\Versions"
        windows_player_folder_name = ""
        windows_studio_folder_name = ""
        return self.CustomizableVariables(org_macOS_dir, org_macOS_studioDir, org_macOS_beforeClientServices, org_macOS_installedPath, org_windows_dir, org_windows_versions_dir, org_windows_player_folder_name, org_windows_studio_folder_name)
    def getLatestRobloxAppSettings(self, debug=False, bootstrapper=False, bucket=""):
        # Mac: https://clientsettingscdn.roblox.com/v2/settings/application/MacDesktopPlayer
        # Windows: https://clientsettingscdn.roblox.com/v2/settings/application/PCDesktopClient

        try:
            import requests
        except Exception as e:
            printMainMessage("This application is requesting for the latest Roblox app settings but needs a module. Would you like to install it? (y/n)")
            if isYes(input("> ")) == True:
                pip().install(["requests"])
                requests = pip().importModule("requests")
                printSuccessMessage("Successfully installed modules!")
            else:
                printErrorMessage("Returning back to application.")
                return {"success": False, "message": "User rejected need of module."}

        try:    
            if bucket == "LIVE" or bucket == "production": bucket = ""
            if self.__main_os__ == "Darwin":
                if debug == True: printDebugMessage("Sending Request to Roblox Servers..") 
                res = requests.get(f"https://clientsettingscdn.roblox.com/v2/settings/application/{bootstrapper == True and 'MacClientBootstrapper' or 'MacDesktopPlayer'}{not bucket == '' and f'/bucket/{bucket}' or ''}")
                if res.ok:
                    jso = res.json()
                    if jso.get("applicationSettings"):
                        if debug == True: printDebugMessage(f"Successfully got application settings! URL: ({res.url})")
                        return {"success": True, "application_settings": jso.get("applicationSettings")}
                    else:
                        if debug == True: printDebugMessage(f"Something went wrong: {res.text}")
                        return {"success": False, "message": "Something went wrong."}
                else:
                    if debug == True: printDebugMessage(f"Something went wrong: {res.text}")
                    return {"success": False, "message": "Something went wrong."}
            elif self.__main_os__ == "Windows":
                if debug == True: printDebugMessage("Sending Request to Roblox Servers..") 
                res = requests.get(f"https://clientsettingscdn.roblox.com/v2/settings/application/{bootstrapper == True and 'PCClientBootstrapper' or 'PCDesktopClient'}{not bucket == '' and f'/bucket/{bucket}' or ''}")
                if res.ok:
                    jso = res.json()
                    if jso.get("applicationSettings"):
                        if debug == True: printDebugMessage(f"Successfully got application settings! URL: ({res.url})")
                        return {"success": True, "application_settings": jso.get("applicationSettings")}
                    else:
                        if debug == True: printDebugMessage(f"Something went wrong: {res.text}")
                        return {"success": False, "message": "Something went wrong."}
                else:
                    if debug == True: printDebugMessage(f"Something went wrong: {res.text}")
                    return {"success": False, "message": "Something went wrong."}
            else:
                printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
                return {"success": False, "message": "OS not compatible."}
        except Exception as e:
            return {"success": False, "message": "There was an error checking. Please check your internet connection!"}
    def getLatestRobloxStudioAppSettings(self, debug=False, bootstrapper=False, bucket=""):
        # Mac: https://clientsettingscdn.roblox.com/v2/settings/application/MacStudioApp
        # Windows: https://clientsettingscdn.roblox.com/v2/settings/application/PCStudioApp

        try:
            import requests
        except Exception as e:
            printMainMessage("This application is requesting for the latest Roblox app settings but needs a module. Would you like to install it? (y/n)")
            if isYes(input("> ")) == True:
                pip().install(["requests"])
                requests = pip().importModule("requests")
                printSuccessMessage("Successfully installed modules!")
            else:
                printErrorMessage("Returning back to application.")
                return {"success": False, "message": "User rejected need of module."}

        try:    
            if bucket == "LIVE" or bucket == "production": bucket = ""
            if self.__main_os__ == "Darwin":
                if debug == True: printDebugMessage("Sending Request to Roblox Servers..") 
                res = requests.get(f"https://clientsettingscdn.roblox.com/v2/settings/application/{bootstrapper == True and 'MacStudioBootstrapper' or 'MacStudioApp'}{not bucket == '' and f'/bucket/{bucket}' or ''}")
                if res.ok:
                    jso = res.json()
                    if jso.get("applicationSettings"):
                        if debug == True: printDebugMessage(f"Successfully got application settings! URL: ({res.url})")
                        return {"success": True, "application_settings": jso.get("applicationSettings")}
                    else:
                        if debug == True: printDebugMessage(f"Something went wrong: {res.text}")
                        return {"success": False, "message": "Something went wrong."}
                else:
                    if debug == True: printDebugMessage(f"Something went wrong: {res.text}")
                    return {"success": False, "message": "Something went wrong."}
            elif self.__main_os__ == "Windows":
                if debug == True: printDebugMessage("Sending Request to Roblox Servers..") 
                res = requests.get(f"https://clientsettingscdn.roblox.com/v2/settings/application/{bootstrapper == True and 'PCStudioBootstrapper' or 'PCStudioApp'}{not bucket == '' and f'/bucket/{bucket}' or ''}")
                if res.ok:
                    jso = res.json()
                    if jso.get("applicationSettings"):
                        if debug == True: printDebugMessage(f"Successfully got application settings! URL: ({res.url})")
                        return {"success": True, "application_settings": jso.get("applicationSettings")}
                    else:
                        if debug == True: printDebugMessage(f"Something went wrong: {res.text}")
                        return {"success": False, "message": "Something went wrong."}
                else:
                    if debug == True: printDebugMessage(f"Something went wrong: {res.text}")
                    return {"success": False, "message": "Something went wrong."}
            else:
                printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
                return {"success": False, "message": "OS not compatible."}
        except Exception as e:
            return {"success": False, "message": "There was an error checking. Please check your internet connection!"}
    def prepareMultiInstance(self, required=False, debug=False, awaitRobloxClosure=True):
        if self.__main_os__ == "Darwin":
            try:
                import posix_ipc
            except Exception as e:
                if required == True:
                    pip().install(["posix-ipc"])
                    posix_ipc = pip().importModule("posix_ipc")
                else:
                    printMainMessage("This application is requesting for semaphore access but needs a module. Would you like to install it? (y/n)")
                    if isYes(input("> ")) == True:
                        pip().install(["posix-ipc"])
                        posix_ipc = pip().importModule("posix_ipc")
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
            printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
            return False
    def parseRobloxURL(self, url: str=""):
        p = url.split('+')[1:]
        data = {}
        for s in p:
            if ':' in s: key, value = s.split(':', 1); data[key] = value
        return data
    def openRoblox(self, forceQuit=False, makeDupe=False, startData="", debug=False, attachInstance=False, allowRobloxOtherLogDebug=False, mainLogFile="") -> "RobloxInstance | None":
        if self.getIfRobloxIsOpen():
            if forceQuit == True:
                self.endRoblox()
                if debug == True: printDebugMessage("Ending Roblox Instances..")
        if self.__main_os__ == "Darwin":
            if makeDupe == True:
                if self.getIfRobloxIsOpen() == True:
                    self.prepareMultiInstance(debug=debug, required=True)
                    com = f"open -n -a \'{os.path.join(macOS_dir, macOS_beforeClientServices, 'RobloxPlayer')}\' {startData}"
                    if debug == True: printDebugMessage("Running Roblox Player Unix Executable..")
                    a = subprocess.run(com, shell=True, check=True)
                    if a.returncode == 0:
                        if attachInstance == True:
                            cur_open_pid = self.getLatestOpenedRobloxPid()
                            start_time = datetime.datetime.now(tz=datetime.UTC).timestamp()
                            test_instance = self.RobloxInstance(self, pid=cur_open_pid, debug_mode=False, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=False)
                            while True:
                                if test_instance.ended_process == True:
                                    break
                                elif len(test_instance.getWindowsOpened()) > 0:
                                    time.sleep(1)
                                    if len(test_instance.getWindowsOpened()) > 0: break
                                elif start_time+3 < datetime.datetime.now(tz=datetime.UTC).timestamp():
                                    break
                                else:
                                    time.sleep(0.5)
                            test_instance.requestThreadClosing()
                            if self.getIfRobloxIsOpen() == True:
                                self.prepareMultiInstance(debug=debug, required=True)
                                pid = self.getLatestOpenedRobloxPid()
                                if pid:
                                    if not (mainLogFile == ""):
                                        return self.RobloxInstance(self, pid=pid, log_file=mainLogFile, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=True)
                                    else:
                                        return self.RobloxInstance(self, pid=pid, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=True)
                else:
                    com = f"open -n -a \'{os.path.join(macOS_dir, macOS_beforeClientServices, 'RobloxPlayer')}\' {startData}"
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
                a = subprocess.run(f"open -a \'{macOS_dir}\' {startData}", shell=True)
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

            most_recent_roblox_version_dir = self.getRobloxInstallFolder()
            if most_recent_roblox_version_dir:
                if debug == True: printDebugMessage("Running RobloxPlayerBeta.exe..")
                if startData == "":
                    a = subprocess.run(f"start {os.path.join(most_recent_roblox_version_dir, 'RobloxPlayerBeta.exe')}", shell=True, stdout=subprocess.DEVNULL)
                else:
                    a = subprocess.run(f'start {os.path.join(most_recent_roblox_version_dir, "RobloxPlayerBeta.exe")} {startData}', shell=True, stdout=subprocess.DEVNULL)
                if a.returncode == 0:
                    if attachInstance == True:
                        if makeDupe == True:
                            if self.getIfRobloxIsOpen() == True:
                                cur_open_pid = self.getLatestOpenedRobloxPid()
                                start_time = datetime.datetime.now(tz=datetime.UTC).timestamp()
                                test_instance = self.RobloxInstance(self, pid=cur_open_pid, debug_mode=False, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=False)
                                while True:
                                    if test_instance.ended_process == True:
                                        break
                                    elif len(test_instance.getWindowsOpened()) > 0:
                                        time.sleep(1)
                                        if len(test_instance.getWindowsOpened()) > 0: break
                                    elif start_time+3 < datetime.datetime.now(tz=datetime.UTC).timestamp():
                                        break
                                    else:
                                        time.sleep(0.5)
                                test_instance.requestThreadClosing()
                                if self.getIfRobloxIsOpen() == True:
                                    pid = self.getLatestOpenedRobloxPid()
                                    if pid:
                                        if not (mainLogFile == ""):
                                            return self.RobloxInstance(self, pid=pid, log_file=mainLogFile, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=True, created_mutex=created_mutex)
                                        else:
                                            return self.RobloxInstance(self, pid=pid, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=True, created_mutex=created_mutex)
                        else:
                            time.sleep(1)
                            if self.getIfRobloxIsOpen() == True:
                                cur_open_pid = self.getLatestOpenedRobloxPid()
                                start_time = datetime.datetime.now(tz=datetime.UTC).timestamp()
                                test_instance = self.RobloxInstance(self, pid=cur_open_pid, debug_mode=False, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=False)
                                while True:
                                    if test_instance.ended_process == True:
                                        break
                                    elif len(test_instance.getWindowsOpened()) > 0:
                                        time.sleep(1)
                                        if len(test_instance.getWindowsOpened()) > 0: break
                                    elif start_time+3 < datetime.datetime.now(tz=datetime.UTC).timestamp():
                                        break
                                    else:
                                        time.sleep(0.5)
                                test_instance.requestThreadClosing()
                                if self.getIfRobloxIsOpen() == True:
                                    pid = self.getLatestOpenedRobloxPid()
                                    if pid:
                                        if not (mainLogFile == ""):
                                            return self.RobloxInstance(self, pid=pid, log_file=mainLogFile, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=True, created_mutex=created_mutex)
                                        else:
                                            return self.RobloxInstance(self, pid=pid, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=True, created_mutex=created_mutex)
            else:
                printLog("Roblox couldn't be found.")
        else:
            printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
    def openRobloxStudio(self, forceQuit=False, startData="", makeDupe=True, debug=False, attachInstance=False, allowRobloxOtherLogDebug=False, mainLogFile="") -> "RobloxInstance | None":
        if self.getIfRobloxStudioIsOpen():
            if forceQuit == True:
                self.endRobloxStudio()
                if debug == True: printDebugMessage("Ending Roblox Studio Instances..")
        if self.__main_os__ == "Darwin":
            if makeDupe == True:
                com = f"open -n -a \'{os.path.join(macOS_studioDir, macOS_beforeClientServices, 'RobloxStudio')}\' --args {startData}"
                if debug == True: printDebugMessage("Running Roblox Studio Unix Executable..")
                a = subprocess.run(com, shell=True)
                if a.returncode == 0:
                    if attachInstance == True:
                        time.sleep(2)
                        if self.getIfRobloxStudioIsOpen() == True:
                            pid = self.getLatestOpenedRobloxStudioPid()
                            if pid:
                                if not (mainLogFile == ""):
                                    return self.RobloxInstance(self, pid=pid, log_file=mainLogFile, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=True, studio=True)
                                else:
                                    return self.RobloxInstance(self, pid=pid, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=True, studio=True)
            else:
                if debug == True: printDebugMessage("Running RobloxStudio.app..")
                a = subprocess.run(f"open -a \'{macOS_studioDir}\' --args {startData}", shell=True)
                if a.returncode == 0:
                    if attachInstance == True:
                        time.sleep(2)
                        if self.getIfRobloxStudioIsOpen() == True:
                            pid = self.getLatestOpenedRobloxStudioPid()
                            if pid:
                                if not (mainLogFile == ""):
                                    return self.RobloxInstance(self, pid=pid, log_file=mainLogFile, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=True, studio=True)
                                else:
                                    return self.RobloxInstance(self, pid=pid, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=True, studio=True)
        elif self.__main_os__ == "Windows":
            created_mutex = False
            most_recent_roblox_version_dir = self.getRobloxInstallFolder(studio=True)
            if most_recent_roblox_version_dir:
                if debug == True: printDebugMessage("Running RobloxStudioBeta.exe..")
                if startData == "":
                    a = subprocess.run(f"start {os.path.join(most_recent_roblox_version_dir, 'RobloxStudioBeta.exe')}", shell=True, stdout=subprocess.DEVNULL)
                else:
                    a = subprocess.run(f'start {os.path.join(most_recent_roblox_version_dir, "RobloxStudioBeta.exe")} {startData}', shell=True, stdout=subprocess.DEVNULL)
                if a.returncode == 0:
                    if attachInstance == True:
                        if makeDupe == True:
                            if self.getIfRobloxStudioIsOpen() == True:
                                cur_open_pid = self.getLatestOpenedRobloxStudioPid()
                                start_time = datetime.datetime.now(tz=datetime.UTC).timestamp()
                                test_instance = self.RobloxInstance(self, pid=cur_open_pid, debug_mode=False, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=False, studio=True)
                                while True:
                                    if test_instance.ended_process == True:
                                        break
                                    elif len(test_instance.getWindowsOpened()) > 0:
                                        time.sleep(1)
                                        if len(test_instance.getWindowsOpened()) > 0: break
                                    elif start_time+3 < datetime.datetime.now(tz=datetime.UTC).timestamp():
                                        break
                                    else:
                                        time.sleep(0.5)
                                test_instance.requestThreadClosing()
                                if self.getIfRobloxStudioIsOpen() == True:
                                    pid = self.getLatestOpenedRobloxStudioPid()
                                    if pid:
                                        if not (mainLogFile == ""):
                                            return self.RobloxInstance(self, pid=pid, log_file=mainLogFile, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=True, created_mutex=created_mutex, studio=True)
                                        else:
                                            return self.RobloxInstance(self, pid=pid, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=True, created_mutex=created_mutex, studio=True)
                        else:
                            time.sleep(1)
                            if self.getIfRobloxStudioIsOpen() == True:
                                cur_open_pid = self.getLatestOpenedRobloxStudioPid()
                                start_time = datetime.datetime.now(tz=datetime.UTC).timestamp()
                                test_instance = self.RobloxInstance(self, pid=cur_open_pid, debug_mode=False, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=False, studio=True)
                                while True:
                                    if test_instance.ended_process == True:
                                        break
                                    elif len(test_instance.getWindowsOpened()) > 0:
                                        time.sleep(1)
                                        if len(test_instance.getWindowsOpened()) > 0: break
                                    elif start_time+3 < datetime.datetime.now(tz=datetime.UTC).timestamp():
                                        break
                                    else:
                                        time.sleep(0.5)
                                test_instance.requestThreadClosing()
                                if self.getIfRobloxStudioIsOpen() == True:
                                    pid = self.getLatestOpenedRobloxStudioPid()
                                    if pid:
                                        if not (mainLogFile == ""):
                                            return self.RobloxInstance(self, pid=pid, log_file=mainLogFile, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=True, created_mutex=created_mutex, studio=True)
                                        else:
                                            return self.RobloxInstance(self, pid=pid, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_20_second_log_creation=True, created_mutex=created_mutex, studio=True)
            else:
                printLog("Roblox Studio couldn't be found.")
        else:
            printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
    def downloadRobloxInstaller(self, filePath="", channel="LIVE", debug=False):
        if self.__main_os__ == "Darwin" or self.__main_os__ == "Windows":
            bootstrapper_settings = self.getLatestRobloxStudioAppSettings(debug=debug, bootstrapper=True, bucket=channel)
            if bootstrapper_settings["success"] == True:
                starter_url = ""
                bootstrapper_settings = bootstrapper_settings["application_settings"]
                if bootstrapper_settings.get("FFlagReplaceChannelNameForDownload"):
                    starter_url = "channel/common/"
                else:
                    starter_url = f"channel/{channel.lower()}/"
                if self.__main_os__ == "Darwin":
                    cur_vers = self.getLatestClientVersion(debug, channel)
                    if cur_vers and cur_vers.get("success") == True:
                        if debug == True: printDebugMessage(f"Downloading Roblox DMG from Roblox's servers..")
                        cur_vers_down_link = f'https://setup.rbxcdn.com/{starter_url}mac/{cur_vers.get("client_version")}-Roblox.zip'
                        urllib.request.urlretrieve(cur_vers_down_link, os.path.join(current_path_location, "RobloxPlayerInstall.zip"))
                        zip_extract = subprocess.run(["unzip", "-o", os.path.join(current_path_location, "RobloxPlayerInstall.zip"), "-d", os.path.join(current_path_location, "RobloxPlayerInstall")], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                        if zip_extract.returncode == 0:
                            pip().copyTreeWithMetadata(os.path.join(current_path_location, "RobloxPlayerInstall", "RobloxPlayerInstaller.app"), filePath, dirs_exist_ok=True, symlinks=True)
                            shutil.rmtree(os.path.join(current_path_location, "RobloxPlayerInstall"), ignore_errors=True)
                            os.remove(os.path.join(current_path_location, "RobloxPlayerInstall.zip"))
                        else:
                            if debug == True: printDebugMessage(f"Unable to unzip Roblox Player installer due to an error.")
                    else:
                        if debug == True: printDebugMessage(f"Unable to download Roblox Player installer due to an http error.")
                elif self.__main_os__ == "Windows":
                    cur_vers = self.getLatestClientVersion(debug, channel)
                    if cur_vers and cur_vers.get("success") == True:
                        if debug == True: printDebugMessage(f"Downloading Roblox EXE from Roblox's servers..")
                        cur_vers_down_link = f'https://setup.rbxcdn.com/{starter_url}{cur_vers.get("client_version")}-RobloxPlayerInstaller.exe'
                        urllib.request.urlretrieve(cur_vers_down_link, filePath)
                        if debug == True: printDebugMessage(f"Successfully downloaded installer!")
                        return filePath
                    else:
                        if debug == True: printDebugMessage(f"Unable to download Roblox Player installer due to an http error.")
                else: 
                    printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
            else:
                if debug == True: printDebugMessage(f"Unable to fetch install bootstrapper settings from Roblox.")
        else:
            printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
    def downloadRobloxStudioInstaller(self, filePath="", channel="LIVE", debug=False):
        if self.__main_os__ == "Darwin" or self.__main_os__ == "Windows":
            bootstrapper_settings = self.getLatestRobloxStudioAppSettings(debug=debug, bootstrapper=True, bucket=channel)
            if bootstrapper_settings["success"] == True:
                starter_url = ""
                bootstrapper_settings = bootstrapper_settings["application_settings"]
                if bootstrapper_settings.get("FFlagReplaceChannelNameForDownload"):
                    starter_url = "channel/common/"
                else:
                    starter_url = f"channel/{channel.lower()}/"
                if self.__main_os__ == "Darwin":
                    cur_vers = self.getLatestStudioClientVersion(debug, channel)
                    if cur_vers and cur_vers.get("success") == True:
                        if debug == True: printDebugMessage(f"Downloading Roblox Studio DMG from Roblox's servers..")
                        cur_vers_down_link = f'https://setup.rbxcdn.com/{starter_url}mac/{cur_vers.get("client_version")}-RobloxStudio.zip'
                        urllib.request.urlretrieve(cur_vers_down_link, os.path.join(current_path_location, "RobloxStudioInstall.zip"))
                        zip_extract = subprocess.run(["unzip", "-o", os.path.join(current_path_location, "RobloxStudioInstall.zip"), "-d", os.path.join(current_path_location, "RobloxStudioInstall")], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                        if zip_extract.returncode == 0:
                            pip().copyTreeWithMetadata(os.path.join(current_path_location, "RobloxStudioInstall", "RobloxStudioInstaller.app"), filePath, dirs_exist_ok=True, symlinks=True)
                            shutil.rmtree(os.path.join(current_path_location, "RobloxStudioInstall"), ignore_errors=True)
                            os.remove(os.path.join(current_path_location, "RobloxStudioInstall.zip"))
                        else:
                            if debug == True: printDebugMessage(f"Unable to unzip Roblox Studio installer due to an error.")
                    else:
                        if debug == True: printDebugMessage(f"Unable to download Roblox Studio installer due to an http error.")
                elif self.__main_os__ == "Windows":
                    cur_vers = self.getLatestStudioClientVersion(debug, channel)
                    if cur_vers and cur_vers.get("success") == True:
                        if debug == True: printDebugMessage(f"Downloading Roblox Studio EXE from Roblox's servers..")
                        cur_vers_down_link = f'https://setup.rbxcdn.com/{starter_url}{cur_vers.get("client_version")}-RobloxStudioInstaller.exe'
                        urllib.request.urlretrieve(cur_vers_down_link, filePath)
                        if debug == True: printDebugMessage(f"Successfully downloaded installer!")
                        return filePath
                    else:
                        if debug == True: printDebugMessage(f"Unable to download Roblox Studio installer due to an http error.")
                else: 
                    printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
            else:
                if debug == True: printDebugMessage(f"Unable to fetch install bootstrapper settings from Roblox.")
        else:
            printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
    def installFastFlags(self, fflags: dict, askForPerms=False, merge=True, flat=False, endRobloxInstances=True, debug=False, studio=False):
        if __name__ == "__main__":
            if self.__main_os__ == "Darwin":
                if endRobloxInstances == True:
                    if studio == True:
                        printMainMessage(f"Closing any open Roblox Studio windows..")
                        self.endRobloxStudio()
                    else:
                        printMainMessage(f"Closing any open Roblox windows..")
                        self.endRoblox()
                if orangeblox_mode == False:
                    printMainMessage(f"Generating ClientSettings Folder..")
                    if not os.path.exists(os.path.join(studio == True and macOS_studioDir or macOS_dir, macOS_beforeClientServices, "ClientSettings")):
                        os.mkdir(os.path.join(studio == True and macOS_studioDir or macOS_dir, macOS_beforeClientServices, "ClientSettings"))
                        printSuccessMessage(f"Created {os.path.join(studio == True and macOS_studioDir or macOS_dir, macOS_beforeClientServices, 'ClientSettings')}..")
                    else:
                        printWarnMessage(f"Client Settings is already created. Skipping Folder Creation..")
                printMainMessage(f"Writing ClientAppSettings.json")
                if merge == True:
                    if orangeblox_mode == True:
                        try:
                            printMainMessage("Reading Previous Configurations..")
                            macos_preference_expected = os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.orangeblox.plist")
                            if os.path.exists(macos_preference_expected):
                                app_configuration = plist().readPListFile(macos_preference_expected)
                                if app_configuration.get("Configuration"):
                                    merge_json = app_configuration.get("Configuration")
                                else:
                                    merge_json = {}
                            else:
                                merge_json = {}
                            if studio == True:
                                if merge_json.get("EFlagRobloxStudioFlags"):
                                    merge_json["EFlagRobloxStudioFlags"].update(fflags)
                                else:
                                    merge_json.update(fflags)
                            else:
                                if merge_json.get("EFlagRobloxPlayerFlags"):
                                    merge_json["EFlagRobloxPlayerFlags"].update(fflags)
                                else:
                                    merge_json.update(fflags)
                            fflags = merge_json
                        except Exception as e:
                            printErrorMessage(f"Something went wrong while trying to generate a merged JSON: {str(e)}")
                    elif os.path.exists(os.path.join(studio == True and macOS_studioDir or macOS_dir, macOS_beforeClientServices, "ClientSettings", 'ClientAppSettings.json')):
                        try:
                            printMainMessage("Reading Previous Client App Settings..")
                            with open(os.path.join(studio == True and macOS_studioDir or macOS_dir, macOS_beforeClientServices, "ClientSettings", f'ClientAppSettings.json'), "r", encoding="utf-8") as f:
                                merge_json = json.load(f)
                            merge_json.update(fflags)
                            fflags = merge_json
                        except Exception as e:
                            printErrorMessage(f"Something went wrong while trying to generate a merged JSON: {str(e)}")
                set_location = os.path.join(studio == True and macOS_studioDir or macOS_dir, macOS_beforeClientServices, "ClientSettings", f'ClientAppSettings.json')
                if orangeblox_mode == True:
                    set_location = os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.orangeblox.plist")
                    app_configuration = plist().readPListFile(set_location)
                    app_configuration["Configuration"] = fflags
                    plist().writePListFile(set_location, app_configuration)
                else:
                    with open(set_location, "w", encoding="utf-8") as f:
                        if flat == True:
                            json.dump(fflags, f)
                        else:
                            json.dump(fflags, f, indent=4)
                printSuccessMessage("DONE!")
                if orangeblox_mode == True:
                    printSuccessMessage("Your fast flags was successfully saved into your Fast Flag Settings!")
                    printSuccessMessage(f"If you like to update your fast flags, go to: {set_location}")
                else:
                    printSuccessMessage(f"Your FFlags have been installed to Roblox {studio == True and 'Studio' or 'Client'}!")
                    printSuccessMessage("Please know that you'll have to use this script again after every update/reinstall!")
                    printSuccessMessage(f"If you like to update your fast flags, go to: {set_location}")
                    printSuccessMessage(f"Additionally, if you would like to, you may install a Roblox bootstrap on your computer to automatically do this.")
                    if studio == True:
                        printMainMessage("Would you like to open Roblox Studio? (y/n)")
                        if input("> ").lower() == "y": self.openRobloxStudio()
                    else:
                        printMainMessage("Would you like to open Roblox? (y/n)")
                        if input("> ").lower() == "y": self.openRoblox()
            elif self.__main_os__ == "Windows":
                if endRobloxInstances == True:
                    if studio == True:
                        printMainMessage(f"Closing any open Roblox Studio windows..")
                        self.endRobloxStudio()
                    else:
                        printMainMessage(f"Closing any open Roblox windows..")
                        self.endRoblox()
                printMainMessage(f"Finding latest Roblox Version..")
                most_recent_roblox_version_dir = self.getRobloxInstallFolder(studio=studio)
                if most_recent_roblox_version_dir:
                    printMainMessage(f"Found version: {most_recent_roblox_version_dir}")
                    if orangeblox_mode == False:
                        printMainMessage(f"Generating ClientSettings Folder..")
                        if not os.path.exists(os.path.join(most_recent_roblox_version_dir, "ClientSettings")):
                            os.mkdir(os.path.join(most_recent_roblox_version_dir, "ClientSettings"))
                            printSuccessMessage(f"Created {most_recent_roblox_version_dir}ClientSettings..")
                        else:
                            printWarnMessage(f"Client Settings is already created. Skipping Folder Creation..")
                    printMainMessage(f"Writing ClientAppSettings.json")
                    if merge == True:
                        if os.path.exists("FastFlagConfiguration.json"):
                            try:
                                printMainMessage("Reading Previous Configurations..")
                                with open(f"FastFlagConfiguration.json", "r", encoding="utf-8") as f:
                                    merge_json = json.load(f)
                                if studio == True:
                                    if merge_json.get("EFlagRobloxStudioFlags"):
                                        merge_json["EFlagRobloxStudioFlags"].update(fflags)
                                    else:
                                        merge_json.update(fflags)
                                else:
                                    if merge_json.get("EFlagRobloxPlayerFlags"):
                                        merge_json["EFlagRobloxPlayerFlags"].update(fflags)
                                    else:
                                        merge_json.update(fflags)
                                fflags = merge_json
                            except Exception as e:
                                printErrorMessage(f"Something went wrong while trying to generate a merged JSON: {str(e)}")
                        elif os.path.exists(os.path.join(most_recent_roblox_version_dir, "ClientSettings", f"ClientAppSettings.json")):
                            try:
                                printMainMessage("Reading Previous Client App Settings..")
                                with open(os.path.join(most_recent_roblox_version_dir, "ClientSettings", f"ClientAppSettings.json"), "r", encoding="utf-8") as f:
                                    merge_json = json.load(f)
                                merge_json.update(fflags)
                                fflags = merge_json
                            except Exception as e:
                                printErrorMessage(f"Something went wrong while trying to generate a merged JSON: {str(e)}")
                    
                    set_location = os.path.join(most_recent_roblox_version_dir, "ClientSettings", f"ClientAppSettings.json")
                    if orangeblox_mode == True and os.path.exists("FastFlagConfiguration.json"):
                        set_location = "FastFlagConfiguration.json"
                    with open(set_location, "w", encoding="utf-8") as f:
                        if flat == True:
                            json.dump(fflags, f)
                        else:
                            json.dump(fflags, f, indent=4)
                    printSuccessMessage("DONE!")
                    if orangeblox_mode == True:
                        printSuccessMessage("Your fast flags was successfully saved into your Fast Flag Settings!")
                        printSuccessMessage(f"If you like to update your fast flags, go to: {set_location}")
                    else:
                        printSuccessMessage(f"Your FFlags have been installed to Roblox {studio == True and 'Studio' or 'Client'}!")
                        printSuccessMessage("Please know that you'll have to use this script again after every update/reinstall!")
                        printSuccessMessage(f"If you like to update your fast flags, go to: {set_location}")
                        printSuccessMessage(f"Additionally, if you would like to, you may install a Roblox bootstrap on your computer to automatically do this.")
                        if studio == True:
                            printMainMessage("Would you like to open Roblox Studio? (y/n)")
                            if input("> ").lower() == "y": self.openRobloxStudio()
                        else:
                            printMainMessage("Would you like to open Roblox? (y/n)")
                            if input("> ").lower() == "y": self.openRoblox()
                else:
                    printErrorMessage("Roblox couldn't be found.")
            else:
                printErrorMessage("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
        else:
            if askForPerms == True:
                if submitStatus: submitStatus.submit("[FFLAGS] Asking for permissions..", 0)
                printLog("Would you like to continue with the Roblox Fast Flag installation? (y/n)")
                printLog("WARNING! This will force-quit any open Roblox windows! Please close them in order to prevent data loss!")
                if not (input("> ").lower() == "y"):
                    printLog("Stopped installation..")
                    if submitStatus: submitStatus.submit("\033ERR[FFLAGS] Asking for permissions..", 0)
                    return
            if self.__main_os__ == "Darwin":
                if endRobloxInstances == True:
                    if submitStatus: submitStatus.submit("[FFLAGS] Ending Roblox Windows..", 10)
                    if studio == True:
                        if debug == True: printDebugMessage(f"Closing any open Roblox Studio windows..")
                        self.endRobloxStudio()
                    else:
                        if debug == True: printDebugMessage(f"Closing any open Roblox windows..")
                        self.endRoblox()
                if submitStatus: submitStatus.submit("[FFLAGS] Creating ClientSettings Folder..", 25)
                if not os.path.exists(os.path.join(studio == True and macOS_studioDir or macOS_dir, macOS_beforeClientServices, "ClientSettings")):
                    if debug == True: printDebugMessage("Creating ClientSettings folder..")
                    os.mkdir(os.path.join(studio == True and macOS_studioDir or macOS_dir, macOS_beforeClientServices, "ClientSettings"))
                if merge == True:
                    if submitStatus: submitStatus.submit("[FFLAGS] Merging Possible Configurations..", 45)
                    if os.path.exists(os.path.join(studio == True and macOS_studioDir or macOS_dir, macOS_beforeClientServices, "ClientSettings", f'ClientAppSettings.json')):
                        try:
                            with open(os.path.join(studio == True and macOS_studioDir or macOS_dir, macOS_beforeClientServices, "ClientSettings", f'ClientAppSettings.json'), "r", encoding="utf-8") as f:
                                merge_json = json.load(f)
                            merge_json.update(fflags)
                            fflags = merge_json
                            if debug == True: printDebugMessage("Successfully merged the JSON in the ClientSettings folder with the provided json!")
                        except Exception as e:
                            printLog(f"Something went wrong while trying to generate a merged JSON: {str(e)}")
                if submitStatus: submitStatus.submit("[FFLAGS] Saving Configuration..", 50)
                with open(os.path.join(studio == True and macOS_studioDir or macOS_dir, macOS_beforeClientServices, "ClientSettings", f'ClientAppSettings.json'), "w", encoding="utf-8") as f:
                    if flat == True:
                        json.dump(fflags, f)
                    else:
                        json.dump(fflags, f, indent=4)
                if submitStatus: submitStatus.submit("[FFLAGS] Saved FFlags!", 100)
                if debug == True: printDebugMessage(f"Saved to ClientAppSettings.json successfully!")
            elif self.__main_os__ == "Windows":
                if endRobloxInstances == True:
                    if submitStatus: submitStatus.submit("[FFLAGS] Ending Roblox Windows..", 10)
                    if studio == True:
                        if debug == True: printDebugMessage(f"Closing any open Roblox Studio windows..")
                        self.endRobloxStudio()
                    else:
                        if debug == True: printDebugMessage(f"Closing any open Roblox windows..")
                        self.endRoblox()
                most_recent_roblox_version_dir = self.getRobloxInstallFolder(studio=studio)
                if most_recent_roblox_version_dir:
                    if submitStatus: submitStatus.submit("[FFLAGS] Creating ClientSettings Folder..", 25)
                    if not os.path.exists(os.path.join(most_recent_roblox_version_dir, "ClientSettings")):
                        if debug == True: printDebugMessage("Creating ClientSettings folder..")
                        os.mkdir(os.path.join(most_recent_roblox_version_dir, "ClientSettings"))
                    if merge == True:
                        if submitStatus: submitStatus.submit("[FFLAGS] Merging Possible Configurations..", 45)
                        if os.path.exists(os.path.join(most_recent_roblox_version_dir, "ClientSettings", f"ClientAppSettings.json")):
                            try:
                                with open(os.path.join(most_recent_roblox_version_dir, "ClientSettings", f"ClientAppSettings.json"), "r", encoding="utf-8") as f:
                                    merge_json = json.load(f)
                                merge_json.update(fflags)
                                fflags = merge_json
                                if debug == True: printDebugMessage("Successfully merged the JSON in the ClientSettings folder with the provided json!")
                            except Exception as e:
                                printLog(f"Something went wrong while trying to generate a merged JSON: {str(e)}")
                    if submitStatus: submitStatus.submit("[FFLAGS] Saving Configuration..", 50)
                    with open(os.path.join(most_recent_roblox_version_dir, "ClientSettings", f"ClientAppSettings.json"), "w", encoding="utf-8") as f:
                        if flat == True:
                            json.dump(fflags, f)
                        else:
                            json.dump(fflags, f, indent=4)
                    if submitStatus: submitStatus.submit("[FFLAGS] Saved FFlags!", 100)
                    if debug == True: printDebugMessage(f"Saved to ClientAppSettings.json successfully!")
                else:
                    printLog("Roblox couldn't be found.")
                    if submitStatus: submitStatus.submit("\033ERR[FFLAGS] Roblox couldn't be found!", 100)
            else:
                printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
                if submitStatus: submitStatus.submit("\033ERR[FFLAGS] RobloxFastFlagsInstaller is only supported for macOS and Windows.", 100)
    def installGlobalBasicSettings(self, globalsettings: dict, askForPerms=False, endRobloxInstances=True, flat=False, debug=False, studio=False):
        if askForPerms == True:
            if submitStatus: submitStatus.submit("[GLOBALSETTINGS] Asking for permissions..", 0)
            printLog("Would you like to continue with the Roblox Fast Flag installation? (y/n)")
            printLog("WARNING! This will force-quit any open Roblox windows! Please close them in order to prevent data loss!")
            if not (input("> ").lower() == "y"):
                printLog("Stopped installation..")
                return
        import xml.etree.ElementTree as ET
        import xml.dom.minidom
        roblox_app_location = ""
        if self.__main_os__ == "Darwin":
            roblox_app_location = os.path.join(user_folder, "Library", "Roblox")
        elif self.__main_os__ == "Windows":
            roblox_app_location = windows_dir
        else:
            printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
            if submitStatus: submitStatus.submit("\033ERR[GLOBALSETTINGS] RobloxFastFlagsInstaller is only supported for macOS and Windows.", 0)
            return  
        if endRobloxInstances == True:
            if submitStatus: submitStatus.submit("[GLOBALSETTINGS] Ending Roblox Windows..", 10)
            if studio == True:
                if debug == True: printDebugMessage(f"Closing any open Roblox Studio windows..")
                self.endRobloxStudio()
            else:
                if debug == True: printDebugMessage(f"Closing any open Roblox windows..")
                self.endRoblox()
        if submitStatus: submitStatus.submit("[GLOBALSETTINGS] Finding Global Basic Settings..", 25)
        file_name = None
        for i in os.listdir(roblox_app_location):
            if not (i.find("GlobalBasicSettings") == -1):
                if studio == True and i.find("_Studio") == -1: continue
                file_name = i
        if file_name:
            if submitStatus: submitStatus.submit("[GLOBALSETTINGS] Found Global Basic Settings File!", 25)
            if debug == True: printDebugMessage(f"Founded File Name: {file_name}")
            if debug == True: printDebugMessage("Reading Settings XML..")
            if submitStatus: submitStatus.submit("[GLOBALSETTINGS] Reading XML File!", 25)
            with open(os.path.join(roblox_app_location, file_name), "r", encoding="utf-8") as f:
                xml_contents = f.read()
            if submitStatus: submitStatus.submit("[GLOBALSETTINGS] Finding root of file!", 30)
            xml_original_root = ET.fromstring(xml_contents)
            item_class = xml_original_root.find(".//Item")
            referent = item_class.get("referent") if item_class is not None else None
            if submitStatus: submitStatus.submit("[GLOBALSETTINGS] Recreating XML Base!", 45)
            if debug == True: printDebugMessage("Recreating XML Tree..")
            xml_root = ET.Element("roblox", {
                "xmlns:xmime": "http://www.w3.org/2005/05/xmlmime",
                "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                "xsi:noNamespaceSchemaLocation": "http://www.roblox.com/roblox.xsd",
                "version": "4"
            })
            xml_item = ET.SubElement(xml_root, "Item", {"class": "UserGameSettings", "referent": referent})
            xml_properties = ET.SubElement(xml_item, "Properties")
            if submitStatus: submitStatus.submit("[GLOBALSETTINGS] Recreating XML Tree!", 70)
            for key, value in globalsettings.items():
                prop_type = value["type"]
                prop_value = value["data"]
                if prop_type == "Vector2":
                    vector2_element = ET.SubElement(xml_properties, "Vector2", {"name": key})
                    ET.SubElement(vector2_element, "X").text = str(prop_value[0])
                    ET.SubElement(vector2_element, "Y").text = str(prop_value[1])
                else:
                    ET.SubElement(xml_properties, prop_type, {"name": key}).text = str(prop_value)
            if submitStatus: submitStatus.submit("[GLOBALSETTINGS] Finalizing Tree!", 90)
            if debug == True: printDebugMessage("Finalizing XML Tree..")
            if flat == True:
                final_xml_contents = ET.tostring(xml_root, encoding="utf-8").decode()
            else:
                final_xml_contents = xml.dom.minidom.parseString(ET.tostring(xml_root, encoding="utf-8").decode()).toprettyxml(indent="    ")
            if debug == True: printDebugMessage("Saving to File..")
            with open(os.path.join(roblox_app_location, file_name), "w", encoding="utf-8") as f:
                f.write(final_xml_contents)
            if submitStatus: submitStatus.submit("[GLOBALSETTINGS] Successfully saved Global Basic Settings!", 100)
            if debug == True: printDebugMessage("Successfully saved Global Basic Settings!")
        else:
            if submitStatus: submitStatus.submit("\033ERR[GLOBALSETTINGS] Unable to find file.", 100)
            printLog("Unable to find settings file.")
    def installRoblox(self, forceQuit=True, debug=False, disableRobloxAutoOpen=True, downloadInstaller=False, downloadChannel=None, copyRobloxInstallerPath="", verifyInstall=False):
        if self.getIfRobloxIsOpen():
            if forceQuit == True:
                if submitStatus: submitStatus.submit("[INSTALL] Ending Roblox Instances..", 0)
                self.endRoblox()
                if debug == True: printDebugMessage("Ending Roblox Instances..")
        def waitForRobloxEnd():
            if disableRobloxAutoOpen == True:
                for i in range(15):
                    if debug == True: printDebugMessage(f"Waited: {i}/15 seconds")
                    if submitStatus: submitStatus.submit("[INSTALL] Awaiting Roblox to Close..", 90)
                    if self.getIfRobloxIsOpen():
                        self.endRoblox()
                        break
                    time.sleep(1)
                
        if self.__main_os__ == "Darwin":
            if self.getIfRobloxIsOpen(installer=True):
                if submitStatus: submitStatus.submit("[INSTALL] Waiting for existing installer..", 10)
                if debug == True: printDebugMessage("Installer is already opened. Waiting for installation to end..")
                while True:
                    if not self.getIfRobloxIsOpen(installer=True):
                        break
                    else:
                        time.sleep(1)
                waitForRobloxEnd()
                if submitStatus: submitStatus.submit("[INSTALL] Roblox is installed!", 100)
            else:
                if macOS_installedPath == os.path.join("/", "Applications"):   
                    try:
                        if not copyRobloxInstallerPath == "":
                            if downloadInstaller == True:
                                if os.path.exists(copyRobloxInstallerPath) and os.path.isfile(copyRobloxInstallerPath): os.remove(copyRobloxInstallerPath)
                                if os.path.exists(copyRobloxInstallerPath) and os.path.isdir(copyRobloxInstallerPath): shutil.rmtree(copyRobloxInstallerPath, ignore_errors=True)
                                if submitStatus: submitStatus.submit("[INSTALL] Fetching Current Version and Channel..", 15)
                                if downloadChannel == None:
                                    channel_res = self.getCurrentClientVersion()
                                    if channel_res.get("success") == True:
                                        downloadChannel = channel_res.get("channel", "LIVE")
                                    else:
                                        downloadChannel = "LIVE"
                                if submitStatus: submitStatus.submit("[INSTALL] Downloading Roblox Installer..", 20)
                                self.downloadRobloxInstaller(copyRobloxInstallerPath, downloadChannel, debug)
                            else:
                                if os.path.exists(os.path.join(macOS_dir, macOS_beforeClientServices, "RobloxPlayerInstaller.app")):
                                    try:
                                        if submitStatus: submitStatus.submit("[INSTALL] Downloading Roblox Installer..", 30)
                                        if debug == True: printDebugMessage(f"Replicating Roblox Player installer to path: {copyRobloxInstallerPath}")
                                        pip().copyTreeWithMetadata(os.path.join(macOS_dir, macOS_beforeClientServices, "RobloxPlayerInstaller.app"), copyRobloxInstallerPath, dirs_exist_ok=True)
                                    except Exception as e:
                                        if debug == True: printDebugMessage("Unable to replicate installer to the designated file path.")
                                else:
                                    if debug == True: printDebugMessage("There's no version of Roblox installed. Installing from downloaded installer app.")
                            if submitStatus: submitStatus.submit("[INSTALL] Running Roblox Installer..", 50)
                            if debug == True: printDebugMessage("Running RobloxPlayerInstaller executable..")
                            insta = subprocess.run(os.path.join(copyRobloxInstallerPath, "Contents", "MacOS", "RobloxPlayerInstaller"), shell=True, check=True, stdout=subprocess.DEVNULL)
                        else:
                            if submitStatus: submitStatus.submit("[INSTALL] Running Roblox Installer..", 50)
                            if debug == True: printDebugMessage("Running RobloxPlayerInstaller executable..")
                            insta = subprocess.run(os.path.join(macOS_dir, macOS_beforeClientServices, "RobloxPlayerInstaller.app", "Contents", "MacOS", "RobloxPlayerInstaller"), shell=True, check=True, stdout=subprocess.DEVNULL)
                        if insta.returncode == 0:
                            if submitStatus: submitStatus.submit("[INSTALL] Installer has been run successfully!", 80)
                            if debug == True: printDebugMessage("Installer has succeeded! Awaiting Roblox closing..")
                        else:
                            if submitStatus: submitStatus.submit("[INSTALL] Installer has failed..", 80)
                            if debug == True: printDebugMessage(f"Installer has failed. Code: {insta.returncode}")
                        waitForRobloxEnd()
                        if submitStatus: submitStatus.submit("[INSTALL] Roblox is installed!", 100)
                    except Exception as e:
                        printErrorMessage(f"Something went wrong starting Roblox Installer: {str(e)}")
                        if submitStatus: submitStatus.submit("\033ERR[INSTALL] Installer couldn't be started!", 15)
                else:
                    if submitStatus: submitStatus.submit("[INSTALL] Fetching current version and channel!", 30)
                    if downloadChannel == None:
                        channel_res = self.getCurrentClientVersion()
                        if channel_res.get("success") == True:
                            downloadChannel = channel_res.get("channel", "LIVE")
                        else:
                            downloadChannel = "LIVE"
                    if submitStatus: submitStatus.submit("[INSTALL] Getting latest version!", 50)
                    latest_vers = self.getLatestClientVersion(debug, downloadChannel)
                    if latest_vers["success"] == True:
                        if submitStatus: submitStatus.submit("[INSTALL] Installing Roblox Bundle!", 80)
                        self.endRoblox()
                        self.installRobloxBundle(macOS_installedPath, macOS_dir, downloadChannel, debug, verifyInstall)
                        if submitStatus: submitStatus.submit("[INSTALL] Installed Roblox Bundle!", 100)
                    else:
                        if submitStatus: submitStatus.submit("\033ERR[INSTALL] Latest Version couldn't be fetched!", 50)
        elif self.__main_os__ == "Windows":
            if self.getIfRobloxIsOpen(installer=True):
                if submitStatus: submitStatus.submit("[INSTALL] Waiting for existing installer..", 10)
                if debug == True: printDebugMessage("Installer is already opened. Waiting for installation to end..")
                while True:
                    if not self.getIfRobloxIsOpen(installer=True):
                        break
                    else:
                        time.sleep(1)
                waitForRobloxEnd()
                if submitStatus: submitStatus.submit("[INSTALL] Roblox is installed!", 100)
                return
            
            if windows_versions_dir == os.path.join(os.getenv('LOCALAPPDATA'), "Roblox", "Versions"):    
                most_recent_roblox_version_dir = self.getRobloxInstallFolder()
                if most_recent_roblox_version_dir:
                    if submitStatus: submitStatus.submit("[INSTALL] Running Roblox Installer..", 50)
                    if debug == True: printDebugMessage("Running RobloxPlayerInstaller executable..")
                    try:
                        insta = subprocess.run(os.path.join(most_recent_roblox_version_dir, "RobloxPlayerInstaller.exe"), shell=True, stdout=subprocess.DEVNULL)
                        while True:
                            if not self.getIfRobloxIsOpen(installer=True):
                                break
                            else:
                                time.sleep(1)
                        if submitStatus: submitStatus.submit("[INSTALL] Installer has been run successfully!", 80)
                        if debug == True: printDebugMessage("Installer has succeeded! Awaiting Roblox closing..")
                        waitForRobloxEnd()
                    except Exception as e:
                        printErrorMessage(f"Something went wrong starting Roblox Installer: {str(e)}")
                        if submitStatus: submitStatus.submit("\033ERR[INSTALL] Installer has been failed!", 80)
                else:
                    if not (copyRobloxInstallerPath == "") and downloadInstaller == True:
                        if os.path.exists(copyRobloxInstallerPath) and os.path.isfile(copyRobloxInstallerPath): os.remove(copyRobloxInstallerPath)
                        if os.path.exists(copyRobloxInstallerPath) and os.path.isdir(copyRobloxInstallerPath): shutil.rmtree(copyRobloxInstallerPath, ignore_errors=True)
                        if submitStatus: submitStatus.submit("[INSTALL] Fetching Current Version and Channel..", 15)
                        if downloadChannel == None:
                            channel_res = self.getCurrentClientVersion()
                            if channel_res.get("success") == True:
                                downloadChannel = channel_res.get("channel", "LIVE")
                            else:
                                downloadChannel = "LIVE"
                        if submitStatus: submitStatus.submit("[INSTALL] Downloading Roblox Installer..", 20)
                        self.downloadRobloxInstaller(copyRobloxInstallerPath, downloadChannel, debug)
                        if not os.path.exists(copyRobloxInstallerPath):
                            printLog("Roblox Installer couldn't be found.")
                            if submitStatus: submitStatus.submit("\033ERR[INSTALL] Installer couldn't be found!", 50)
                        else:
                            if submitStatus: submitStatus.submit("[INSTALL] Running Roblox Installer..", 50)
                            if debug == True: printDebugMessage("Running RobloxPlayerInstaller executable..")
                            try:
                                insta = subprocess.run(f"{copyRobloxInstallerPath}", shell=True, stdout=subprocess.DEVNULL)
                                while True:
                                    if not self.getIfRobloxIsOpen(installer=True):
                                        break
                                    else:
                                        time.sleep(1)
                                if submitStatus: submitStatus.submit("[INSTALL] Installer has been run successfully!", 80)
                                if debug == True: printDebugMessage("Installer has succeeded! Awaiting Roblox closing..")
                                waitForRobloxEnd()
                            except Exception as e:
                                printErrorMessage(f"Something went wrong starting Roblox Installer: {str(e)}")
                                if submitStatus: submitStatus.submit("\033ERR[INSTALL] Installer couldn't be started!", 80)
                    else:
                        printLog("Roblox Installer couldn't be found.")
                        if submitStatus: submitStatus.submit("\033ERR[INSTALL] Installer couldn't be found!", 15)
            else:
                if submitStatus: submitStatus.submit("[INSTALL] Fetching Current Version and Channel!", 15)
                if downloadChannel == None:
                    channel_res = self.getCurrentClientVersion()
                    if channel_res.get("success") == True:
                        downloadChannel = channel_res.get("channel", "LIVE")
                    else:
                        downloadChannel = "LIVE"
                if submitStatus: submitStatus.submit("[INSTALL] Fetching latest version..", 30)
                latest_vers = self.getLatestClientVersion(debug, downloadChannel)
                if latest_vers["success"] == True:
                    self.endRoblox()
                    if submitStatus: submitStatus.submit("[INSTALL] Removing Old Roblox Bundles..", 50)
                    for i in os.listdir(windows_versions_dir):
                        if os.path.isdir(os.path.join(windows_versions_dir, i)) and os.path.exists(os.path.join(windows_versions_dir, i, "RobloxPlayerBeta.exe")):
                            shutil.rmtree(os.path.join(windows_versions_dir, i), ignore_errors=True)
                    if submitStatus: submitStatus.submit("[INSTALL] Installing Roblox Bundle..", 80)
                    if not (windows_player_folder_name == ""): 
                        makedirs(os.path.join(windows_versions_dir, windows_player_folder_name))
                        self.installRobloxBundle(os.path.join(windows_versions_dir, windows_player_folder_name), "", downloadChannel, debug, verifyInstall)
                    else:
                        makedirs(os.path.join(windows_versions_dir))
                        self.installRobloxBundle(os.path.join(windows_versions_dir), "", downloadChannel, debug, verifyInstall)
                    if submitStatus: submitStatus.submit("[INSTALL] Installed Roblox Bundle!", 100)
                else:
                    printLog("Unable to fetch latest version.")
                    if submitStatus: submitStatus.submit("\033ERR[INSTALL] Unable to fetch latest version.", 100)
        else:
            printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
            if submitStatus: submitStatus.submit("\033ERR[INSTALL] RobloxFastFlagsInstaller is only supported for macOS and Windows.", 100)
    def installRobloxStudio(self, forceQuit=True, debug=False, disableRobloxAutoOpen=True, downloadInstaller=False, downloadChannel=None, copyRobloxInstallerPath="", verifyInstall=False):
        if self.getIfRobloxStudioIsOpen():
            if forceQuit == True:
                if submitStatus: submitStatus.submit("[INSTALL] Ending Roblox Instances..", 0)
                self.endRobloxStudio()
                if debug == True: printDebugMessage("Ending Roblox Studio Instances..")
        def waitForRobloxEnd():
            if disableRobloxAutoOpen == True:
                for i in range(15):
                    if debug == True: printDebugMessage(f"Waited: {i}/15 seconds")
                    if self.getIfRobloxStudioIsOpen():
                        self.endRobloxStudio()
                        break
                    time.sleep(1)
                
        if self.__main_os__ == "Darwin":
            if self.getIfRobloxStudioIsOpen(installer=True):
                if debug == True: printDebugMessage("Installer is already opened. Waiting for installation to end..")
                while True:
                    if not self.getIfRobloxStudioIsOpen(installer=True):
                        break
                    else:
                        time.sleep(1)
                waitForRobloxEnd()
            else:
                if macOS_installedPath == os.path.join("/", "Applications"):   
                    try:
                        if not copyRobloxInstallerPath == "":
                            if downloadInstaller == True:
                                if os.path.exists(copyRobloxInstallerPath) and os.path.isfile(copyRobloxInstallerPath): os.remove(copyRobloxInstallerPath)
                                if os.path.exists(copyRobloxInstallerPath) and os.path.isdir(copyRobloxInstallerPath): shutil.rmtree(copyRobloxInstallerPath, ignore_errors=True)
                                if submitStatus: submitStatus.submit("[INSTALL] Fetching Current Version and Channel..", 15)
                                if downloadChannel == None:
                                    channel_res = self.getCurrentStudioClientVersion()
                                    if channel_res.get("success") == True:
                                        downloadChannel = channel_res.get("channel", "LIVE")
                                    else:
                                        downloadChannel = "LIVE"
                                if submitStatus: submitStatus.submit("[INSTALL] Downloading Roblox Studio Installer..", 20)
                                self.downloadRobloxStudioInstaller(copyRobloxInstallerPath, downloadChannel, debug)
                            else:
                                if os.path.exists(os.path.join(macOS_studioDir, macOS_beforeClientServices, "RobloxStudioInstaller.app")):
                                    try:
                                        if submitStatus: submitStatus.submit("[INSTALL] Downloading Roblox Installer..", 30)
                                        if debug == True: printDebugMessage(f"Replicating Roblox Player installer to path: {copyRobloxInstallerPath}")
                                        pip().copyTreeWithMetadata(os.path.join(macOS_studioDir, macOS_beforeClientServices, "RobloxStudioInstaller.app"), copyRobloxInstallerPath, dirs_exist_ok=True)
                                    except Exception as e:
                                        if debug == True: printDebugMessage("Unable to replicate installer to the designated file path.")
                                else:
                                    if debug == True: printDebugMessage("There's no version of Roblox installed. Installing from downloaded installer app.")
                            if submitStatus: submitStatus.submit("[INSTALL] Running Roblox Studio Installer..", 50)
                            if debug == True: printDebugMessage("Running RobloxStudioInstaller executable..")
                            insta = subprocess.run(os.path.join(copyRobloxInstallerPath, "Contents", "MacOS", "RobloxStudioInstaller"), shell=True, check=True, stdout=subprocess.DEVNULL)
                        else:
                            if submitStatus: submitStatus.submit("[INSTALL] Running Roblox Studio Installer..", 50)
                            if debug == True: printDebugMessage("Running RobloxStudioInstaller executable..")
                            insta = subprocess.run(os.path.join(macOS_studioDir, macOS_beforeClientServices, "RobloxStudioInstaller.app", "Contents", "MacOS", "RobloxPlayerInstaller"), shell=True, check=True, stdout=subprocess.DEVNULL)
                        if submitStatus: submitStatus.submit("[INSTALL] Installer has been run successfully!", 80)
                        if insta.returncode == 0:
                            if debug == True: printDebugMessage("Installer has succeeded! Awaiting Roblox closing..")
                        else:
                            if debug == True: printDebugMessage(f"Installer has failed. Code: {insta.returncode}")
                        waitForRobloxEnd()
                    except Exception as e:
                        printErrorMessage(f"Something went wrong starting Roblox Installer: {str(e)}")
                else:
                    if submitStatus: submitStatus.submit("[INSTALL] Fetching Current Version and Channel!", 15)
                    if downloadChannel == None:
                        channel_res = self.getCurrentStudioClientVersion()
                        if channel_res.get("success") == True:
                            downloadChannel = channel_res.get("channel", "LIVE")
                        else:
                            downloadChannel = "LIVE"
                    if submitStatus: submitStatus.submit("[INSTALL] Fetching latest version..", 30)
                    latest_vers = self.getLatestStudioClientVersion(debug, downloadChannel)
                    if latest_vers["success"] == True:
                        if submitStatus: submitStatus.submit("[INSTALL] Installing Roblox Studio Bundle..", 80)
                        self.endRobloxStudio()
                        self.installRobloxStudioBundle(macOS_installedPath, macOS_studioDir, downloadChannel, debug, verifyInstall)
                        if submitStatus: submitStatus.submit("[INSTALL] Installed Roblox Studio Bundle!", 100)
        elif self.__main_os__ == "Windows":
            if self.getIfRobloxStudioIsOpen(installer=True):
                if debug == True: printDebugMessage("Installer is already opened. Waiting for installation to end..")
                while True:
                    if not self.getIfRobloxStudioIsOpen(installer=True):
                        break
                    else:
                        time.sleep(1)
                waitForRobloxEnd()
                return
            
            if windows_versions_dir == os.path.join(os.getenv('LOCALAPPDATA'), "Roblox", "Versions"):    
                most_recent_roblox_version_dir = self.getRobloxInstallFolder(studio=True)
                if most_recent_roblox_version_dir:
                    if submitStatus: submitStatus.submit("[INSTALL] Running Roblox Studio Installer..", 50)
                    if debug == True: printDebugMessage("Running RobloxPlayerInstaller executable..")
                    try:
                        insta = subprocess.run(os.path.join(most_recent_roblox_version_dir, "RobloxStudioInstaller.exe"), shell=True, stdout=subprocess.DEVNULL)
                        while True:
                            if not self.getIfRobloxStudioIsOpen(installer=True):
                                break
                            else:
                                time.sleep(1)
                        if submitStatus: submitStatus.submit("[INSTALL] Installer has been run successfully!", 80)
                        if debug == True: printDebugMessage("Installer has succeeded! Awaiting Roblox closing..")
                        waitForRobloxEnd()
                    except Exception as e:
                        printErrorMessage(f"Something went wrong starting Roblox Installer: {str(e)}")
                        if submitStatus: submitStatus.submit("\033ERR[INSTALL] Installer has been failed!", 80)
                else:
                    if not (copyRobloxInstallerPath == "") and downloadInstaller == True:
                        if os.path.exists(copyRobloxInstallerPath) and os.path.isfile(copyRobloxInstallerPath): os.remove(copyRobloxInstallerPath)
                        if os.path.exists(copyRobloxInstallerPath) and os.path.isdir(copyRobloxInstallerPath): shutil.rmtree(copyRobloxInstallerPath, ignore_errors=True)
                        if downloadChannel == None:
                            channel_res = self.getCurrentStudioClientVersion()
                            if channel_res.get("success") == True:
                                downloadChannel = channel_res.get("channel", "LIVE")
                            else:
                                downloadChannel = "LIVE"
                        if submitStatus: submitStatus.submit("[INSTALL] Downloading Roblox Studio Installer..", 20)
                        self.downloadRobloxStudioInstaller(copyRobloxInstallerPath, downloadChannel, debug)
                        if not os.path.exists(copyRobloxInstallerPath):
                            printLog("Roblox Installer couldn't be found.")
                            if submitStatus: submitStatus.submit("\033ERR[INSTALL] Installer couldn't be found!", 50)
                        else:
                            if submitStatus: submitStatus.submit("[INSTALL] Running Roblox Studio Installer..", 50)
                            if debug == True: printDebugMessage("Running RobloxPlayerInstaller executable..")
                            try:
                                insta = subprocess.run(f"{copyRobloxInstallerPath}", shell=True, stdout=subprocess.DEVNULL)
                                while True:
                                    if not self.getIfRobloxStudioIsOpen(installer=True):
                                        break
                                    else:
                                        time.sleep(1)
                                if submitStatus: submitStatus.submit("[INSTALL] Installer has been run successfully!", 80)
                                if debug == True: printDebugMessage("Installer has succeeded! Awaiting Roblox closing..")
                                waitForRobloxEnd()
                            except Exception as e:
                                printErrorMessage(f"Something went wrong starting Roblox Installer: {str(e)}")
                                if submitStatus: submitStatus.submit("\033ERR[INSTALL] Installer couldn't be started!", 80)
                    else:
                        printLog("Roblox Installer couldn't be found.")
                        if submitStatus: submitStatus.submit("\033ERR[INSTALL] Installer couldn't be found!", 15)
            else:
                if submitStatus: submitStatus.submit("[INSTALL] Fetching Current Version and Channel!", 15)
                if downloadChannel == None:
                    channel_res = self.getCurrentStudioClientVersion()
                    if channel_res.get("success") == True:
                        downloadChannel = channel_res.get("channel", "LIVE")
                    else:
                        downloadChannel = "LIVE"
                if submitStatus: submitStatus.submit("[INSTALL] Fetching latest version..", 30)
                latest_vers = self.getLatestStudioClientVersion(debug, downloadChannel)
                if latest_vers["success"] == True:
                    self.endRobloxStudio()
                    if submitStatus: submitStatus.submit("[INSTALL] Removing Old Roblox Studio Bundles..", 50)
                    for i in os.listdir(windows_versions_dir):
                        if os.path.isdir(os.path.join(windows_versions_dir, i)) and os.path.exists(os.path.join(windows_versions_dir, i, "RobloxStudioBeta.exe")):
                            shutil.rmtree(os.path.join(windows_versions_dir, i), ignore_errors=True)
                    if submitStatus: submitStatus.submit("[INSTALL] Installing Roblox Studio Bundle..", 80)
                    if not (windows_studio_folder_name == ""): 
                        makedirs(os.path.join(windows_versions_dir, windows_studio_folder_name))
                        self.installRobloxStudioBundle(os.path.join(windows_versions_dir, windows_studio_folder_name), "", downloadChannel, debug, verifyInstall)
                    else:
                        makedirs(os.path.join(windows_versions_dir))
                        self.installRobloxStudioBundle(os.path.join(windows_versions_dir), "", downloadChannel, debug, verifyInstall)
                    if submitStatus: submitStatus.submit("[INSTALL] Installed Roblox Studio Bundle!", 100)
                else:
                    if submitStatus: submitStatus.submit("\033ERR[INSTALL] Unable to fetch latest version.", 100)
        else:
            printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
            if submitStatus: submitStatus.submit("\033ERR[INSTALL] RobloxFastFlagsInstaller is only supported for macOS and Windows.", 100)
    def installRobloxBundle(self, installPath="", appPath="", channel="LIVE", debug=False, verify=False):
        if self.__main_os__ == "Darwin" or self.__main_os__ == "Windows":
            try:
                if submitStatus: submitStatus.submit("[BUNDLE] Fetching Latest Player Version..", 0)
                cur_vers = self.getLatestClientVersion(debug, channel)
                if cur_vers and cur_vers.get("success") == True:
                    try:
                        import requests
                    except Exception as e:
                        pip().install(["requests"])
                        requests = pip().importModule("requests")
                        printSuccessMessage("Successfully installed modules!")
                    if self.getIfRobloxIsOpen():
                        if submitStatus: submitStatus.submit("[BUNDLE] Closing Roblox..", 5)
                        if debug == True: printDebugMessage(f"Closing Roblox to prevent issues during download..")
                        self.endRoblox()
                    if submitStatus: submitStatus.submit("[BUNDLE] Fetching Bootstrap Settings..", 15)
                    bootstrapper_settings = self.getLatestRobloxStudioAppSettings(debug=debug, bootstrapper=True, bucket=channel)
                    if bootstrapper_settings["success"] == True:
                        starter_url = ""
                        bootstrapper_settings = bootstrapper_settings["application_settings"]
                        if bootstrapper_settings.get("FFlagReplaceChannelNameForDownload"):
                            starter_url = "channel/common/"
                        else:
                            starter_url = f"channel/{channel.lower()}/"
                        if self.__main_os__ == "Windows":
                            if submitStatus: submitStatus.submit("[BUNDLE] Fetching Package Manifest..", 30)
                            if debug == True: printDebugMessage(f"Fetching Latest Package Manifest from Roblox's servers..")
                            rbx_manifest_link = f'https://setup.rbxcdn.com/{starter_url}{cur_vers.get("client_version")}-rbxPkgManifest.txt'
                            rbx_hashes_link = f'https://setup.rbxcdn.com/{starter_url}{cur_vers.get("client_version")}-rbxManifest.txt'
                            rbx_man_req = requests.get(rbx_manifest_link)
                            rbx_hashes_link = requests.get(rbx_hashes_link)
                            if rbx_man_req.ok:
                                rbx_man_res = rbx_man_req.text
                                rbx_lines = rbx_man_res.splitlines()
                                def is_filename(rbx_line):
                                    return not rbx_line.isdigit() and not re.fullmatch(r'[a-fA-F0-9]{32}', rbx_line) and rbx_line != "v0"
                                marked_install_files = [rbx_line for rbx_line in rbx_lines if is_filename(rbx_line)]
                                rbx_hashes_res = rbx_hashes_link.text.strip().split("\n")
                                rbx_hash_dict = {}
                                for i in range(0, len(rbx_hashes_res), 2):
                                    file_path = rbx_hashes_res[i].strip()
                                    file_hash = rbx_hashes_res[i + 1].strip()
                                    rbx_hash_dict[file_path] = file_hash
                                per_step = 0
                                if submitStatus: submitStatus.submit("[BUNDLE] Downloading Packages..", 40)
                                try:
                                    for i in marked_install_files:
                                        per_step += 1
                                        if not i == "":
                                            if debug == True: printDebugMessage(f"Downloading from Roblox's server: {i} [{round((per_step/(len(marked_install_files)*2))*100, 2)}/100]")
                                            urllib.request.urlretrieve(f'https://setup.rbxcdn.com/{starter_url}{cur_vers.get("client_version")}-{i}', os.path.join(installPath, i))
                                            if self.robloxBundleExportFiles.get(i):
                                                export_destination = self.robloxBundleExportFiles.get(i)
                                                makedirs(f'{installPath}{export_destination}')
                                                zip_extract = subprocess.run(["tar", "-xf", f"{os.path.join(installPath, i)}", "-C", f'{installPath}{export_destination}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                                                per_step += 1
                                                if submitStatus: submitStatus.submit(f"[BUNDLE] Downloading Packages [{i}]..", round((per_step/(len(marked_install_files)*2))*100, 2))
                                                if zip_extract.returncode == 0:
                                                    os.remove(os.path.join(installPath, i))
                                                    if debug == True: printDebugMessage(f"Successfully exported {i}! [{round((per_step/(len(marked_install_files)*2))*100, 2)}/100]")
                                                else:
                                                    if debug == True: printDebugMessage(f"Unable to export: {i} [{round((per_step/(len(marked_install_files)*2))*100, 2)}/100]")
                                            elif i.endswith(".zip"):
                                                export_destination = "/"
                                                makedirs(f'{installPath}{export_destination}')
                                                zip_extract = subprocess.run(["tar", "-xf", f"{os.path.join(installPath, i)}", "-C", f'{installPath}{export_destination}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                                                if zip_extract.returncode == 0:
                                                    os.remove(os.path.join(installPath, i))
                                                    if debug == True: printDebugMessage(f"Successfully exported {i}!")
                                                else:
                                                    if debug == True: printDebugMessage(f"Unable to export: {i}")
                                    if verify == True:
                                        if submitStatus: submitStatus.submit(f"[BUNDLE] Verifying Roblox Install..", 80)
                                        if debug == True: printDebugMessage(f"Verifying Roblox Install..")
                                        def calculate_rbx_hash(file_path):
                                            try:
                                                with open(file_path, "rb") as f:
                                                    hasher = hashlib.md5()
                                                    chunk = f.read(8192)
                                                    while chunk: 
                                                        hasher.update(chunk)
                                                        chunk = f.read(8192)
                                                return hasher.hexdigest()
                                            except Exception:
                                                return None
                                        verified = True
                                        for rbx_file, hash_value in rbx_hash_dict.items():
                                            if os.path.exists(os.path.join(installPath, rbx_file)):
                                                calculated_hash = calculate_rbx_hash(os.path.join(installPath, rbx_file))
                                                if calculated_hash == None:
                                                    if debug == True: printDebugMessage(f"Unable to verify file: {rbx_file}")
                                                    continue
                                                elif not (calculated_hash == hash_value):
                                                    if debug == True: printDebugMessage(f"Unable to verify file: {hash_value} => {calculated_hash}")
                                                    verified = False
                                                    break
                                        if verified == False:
                                            printErrorMessage(f"Unable to install Roblox due to a verification error.")
                                            return
                                    with open(os.path.join(installPath, "RobloxVersion.json"), "w", encoding="utf-8") as f:
                                        json.dump({"ClientVersion": cur_vers.get("client_version", "version-000000000000"), "AppVersion": cur_vers.get("hash", "0.000.0.0000000")}, f, indent=4)
                                    with open(os.path.join(installPath, "AppSettings.xml"), "w", encoding="utf-8") as f:
                                        f.write('<?xml version="1.0" encoding="UTF-8"?><Settings><ContentFolder>content</ContentFolder><BaseUrl>http://www.roblox.com</BaseUrl></Settings>')
                                    if submitStatus: submitStatus.submit(f"[BUNDLE] Successfully installed Roblox Bundle!", 100)
                                    if debug == True: printDebugMessage(f"Successfully installed Roblox to: {installPath} [Client: {cur_vers.get('client_version')}]")
                                except Exception as e:
                                    if submitStatus: submitStatus.submit(f"\033ERR[BUNDLE] Unable to download and install Roblox Bundle!", 100)
                                    if debug == True: printDebugMessage(f"Unable to install Roblox Bundle: {str(e)}")
                            else:
                                if debug == True: printDebugMessage(f"Unable to download Roblox manifest due to an http error. Code: {rbx_man_req.status_code}")
                                if submitStatus: submitStatus.submit("\033ERR[BUNDLE] Unable to fetch Roblox manifest file!", 100)
                        elif self.__main_os__ == "Darwin":
                            if platform.machine() == "arm64":
                                roblox_player_down = f'https://setup.rbxcdn.com/{starter_url}mac/arm64/{cur_vers.get("client_version")}-RobloxPlayer.zip'
                            else:
                                roblox_player_down = f'https://setup.rbxcdn.com/{starter_url}mac/{cur_vers.get("client_version")}-RobloxPlayer.zip'
                            if submitStatus: submitStatus.submit(f"[BUNDLE] Downloading Roblox App!", 0)
                            if debug == True: printDebugMessage(f"Downloading Player from Roblox's server: {roblox_player_down}")
                            try:
                                urllib.request.urlretrieve(roblox_player_down, os.path.join(installPath, "RobloxPlayer.zip"))
                                if os.path.exists(os.path.join(installPath, "RobloxPlayer.zip")):
                                    if os.path.exists(os.path.join(installPath, "RobloxPlayer")) or os.path.exists(appPath):
                                        if debug == True: printDebugMessage(f"Cleaning before install..")
                                        if os.path.exists(os.path.join(installPath, "RobloxPlayer")): shutil.rmtree(os.path.join(installPath, "RobloxPlayer"), ignore_errors=True)
                                        if os.path.exists(os.path.join(appPath)): shutil.rmtree(os.path.join(appPath), ignore_errors=True)
                                    if submitStatus: submitStatus.submit(f"[BUNDLE] Extracting Roblox App!", 30)
                                    if debug == True: printDebugMessage(f"Extracting Player from Downloaded ZIP: {os.path.join(installPath, 'RobloxPlayer.zip')}")
                                    zip_extract = subprocess.run(["unzip", "-o", os.path.join(installPath, "RobloxPlayer.zip"), "-d", os.path.join(installPath, "RobloxPlayer")], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                                    if zip_extract.returncode == 0:
                                        if submitStatus: submitStatus.submit(f"[BUNDLE] Moving Player!", 60)
                                        if debug == True: printDebugMessage(f"Moving Player..")
                                        pip().copyTreeWithMetadata(os.path.join(installPath, "RobloxPlayer", "RobloxPlayer.app"), appPath, dirs_exist_ok=True, symlinks=True)
                                        if submitStatus: submitStatus.submit(f"[BUNDLE] Cleaning up Player!", 80)
                                        if debug == True: printDebugMessage(f"Cleaning up..")
                                        shutil.rmtree(os.path.join(installPath, "RobloxPlayer"), ignore_errors=True)
                                        os.remove(os.path.join(installPath, "RobloxPlayer.zip"))
                                        with open(os.path.join(appPath, "Contents", "MacOS", "RobloxVersion.json"), "w", encoding="utf-8") as f:
                                            json.dump({"ClientVersion": cur_vers.get("client_version", "version-000000000000"), "AppVersion": cur_vers.get("hash", "0.000.0.0000000")}, f, indent=4)
                                        if submitStatus: submitStatus.submit(f"[BUNDLE] Successfully installed Roblox Bundle!", 100)
                                        if debug == True: printDebugMessage(f"Successfully installed Roblox to: {installPath} [Client: {cur_vers.get('client_version')}]")
                                    else:
                                        if debug == True: printDebugMessage(f"Unable to extract Player: {zip_extract.returncode}")
                                        if submitStatus: submitStatus.submit("\033ERR[BUNDLE] Failed to extract Roblox Player.", 100)
                                else:
                                    if debug == True: printDebugMessage(f"Unable to download the Roblox Player.")
                                    if submitStatus: submitStatus.submit("\033ERR[BUNDLE] Failed to download Roblox Player.", 100)
                            except Exception as e:
                                if debug == True: printDebugMessage(f"Unable to download and install the Roblox Player.")
                                if submitStatus: submitStatus.submit("\033ERR[BUNDLE] Failed to download and install Roblox Player.", 100)
                    else:
                        if debug == True: printDebugMessage(f"Unable to fetch install bootstrapper settings from Roblox.")
                        if submitStatus: submitStatus.submit("\033ERR[BUNDLE] Unable to fetch bootstrapper settings.", 100)
                else:
                    if debug == True: printDebugMessage(f"Unable to fetch Roblox manifest file due to an http error.")
                    if submitStatus: submitStatus.submit("\033ERR[BUNDLE] Unable to fetch Roblox manifest file!", 100)
            except Exception as e:
                if debug == True: printDebugMessage(f"Unable to download and install Roblox Bundle. Error: {str(e)}")
                if submitStatus: submitStatus.submit("\033ERR[INSTALL] Unable to download and install Roblox Bundle!", 100)
        else:
            printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
            if submitStatus: submitStatus.submit("\033ERR[BUNDLE] RobloxFastFlagsInstaller is only supported for macOS and Windows.", 100)
    def installRobloxStudioBundle(self, installPath="", appPath="", channel="LIVE", debug=False, verify=False):
        if self.__main_os__ == "Darwin" or self.__main_os__ == "Windows":
            try:
                if submitStatus: submitStatus.submit("[BUNDLE] Fetching Latest Studio Version..", 0)
                cur_vers = self.getLatestStudioClientVersion(debug, channel)
                if cur_vers and cur_vers.get("success") == True:
                    try:
                        import requests
                    except Exception as e:
                        pip().install(["requests"])
                        requests = pip().importModule("requests")
                        printSuccessMessage("Successfully installed modules!")
                    if self.getIfRobloxIsOpen():
                        if submitStatus: submitStatus.submit("[BUNDLE] Closing Roblox Studio..", 5)
                        if debug == True: printDebugMessage(f"Closing Roblox to prevent issues during download..")
                        self.endRobloxStudio()
                    if submitStatus: submitStatus.submit("[BUNDLE] Fetching Bootstrap Settings..", 15)
                    bootstrapper_settings = self.getLatestRobloxStudioAppSettings(debug=debug, bootstrapper=True, bucket=channel)
                    if bootstrapper_settings["success"] == True:
                        starter_url = ""
                        bootstrapper_settings = bootstrapper_settings["application_settings"]
                        if bootstrapper_settings.get("FFlagReplaceChannelNameForDownload"):
                            starter_url = "channel/common/"
                        else:
                            starter_url = f"channel/{channel.lower()}/"
                        if self.__main_os__ == "Windows":
                            if submitStatus: submitStatus.submit("[BUNDLE] Fetching Package Manifest..", 30)
                            if debug == True: printDebugMessage(f"Fetching Latest Package Manifest from Roblox's servers..")
                            rbx_manifest_link = f'https://setup.rbxcdn.com/{starter_url}{cur_vers.get("client_version")}-rbxPkgManifest.txt'
                            rbx_hashes_link = f'https://setup.rbxcdn.com/{starter_url}{cur_vers.get("client_version")}-rbxManifest.txt'
                            rbx_man_req = requests.get(rbx_manifest_link)
                            rbx_hashes_link = requests.get(rbx_hashes_link)
                            if rbx_man_req.ok:
                                rbx_man_res = rbx_man_req.text
                                rbx_lines = rbx_man_res.splitlines()
                                def is_filename(rbx_line):
                                    return not rbx_line.isdigit() and not re.fullmatch(r'[a-fA-F0-9]{32}', rbx_line) and rbx_line != "v0"
                                marked_install_files = [rbx_line for rbx_line in rbx_lines if is_filename(rbx_line)]
                                rbx_hashes_res = rbx_hashes_link.text.strip().split("\n")
                                rbx_hash_dict = {}
                                for i in range(0, len(rbx_hashes_res), 2):
                                    file_path = rbx_hashes_res[i].strip()
                                    file_hash = rbx_hashes_res[i + 1].strip()
                                    rbx_hash_dict[file_path] = file_hash
                                per_step = 0
                                if submitStatus: submitStatus.submit("[BUNDLE] Downloading Packages..", 40)
                                try:
                                    for i in marked_install_files:
                                        per_step += 1
                                        if not i == "":
                                            if debug == True: printDebugMessage(f"Downloading from Roblox's server: {i} [{round((per_step/(len(marked_install_files)*2))*100, 2)}/100]")
                                            urllib.request.urlretrieve(f'https://setup.rbxcdn.com/{starter_url}{cur_vers.get("client_version")}-{i}', os.path.join(installPath, i))
                                            if self.robloxStudioBundleExportFiles.get(i):
                                                export_destination = self.robloxStudioBundleExportFiles.get(i)
                                                makedirs(f'{installPath}{export_destination}')
                                                zip_extract = subprocess.run(["tar", "-xf", f"{os.path.join(installPath, i)}", "-C", f'{installPath}{export_destination}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                                                per_step += 1
                                                if submitStatus: submitStatus.submit(f"[BUNDLE] Downloading Packages [{i}]..", round((per_step/(len(marked_install_files)*2))*100, 2))
                                                if zip_extract.returncode == 0:
                                                    os.remove(os.path.join(installPath, i))
                                                    if debug == True: printDebugMessage(f"Successfully exported {i}! [{round((per_step/(len(marked_install_files)*2))*100, 2)}/100]")
                                                else:
                                                    if debug == True: printDebugMessage(f"Unable to export: {i} [{round((per_step/(len(marked_install_files)*2))*100, 2)}/100]")
                                            elif i.endswith(".zip"):
                                                export_destination = "/"
                                                makedirs(f'{installPath}{export_destination}')
                                                zip_extract = subprocess.run(["tar", "-xf", f"{os.path.join(installPath, i)}", "-C", f'{installPath}{export_destination}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                                                if zip_extract.returncode == 0:
                                                    os.remove(os.path.join(installPath, i))
                                                    if debug == True: printDebugMessage(f"Successfully exported {i}!")
                                                else:
                                                    if debug == True: printDebugMessage(f"Unable to export: {i}")
                                    if verify == True:
                                        if submitStatus: submitStatus.submit(f"[BUNDLE] Verifying Roblox Studio Install..", 80)
                                        if debug == True: printDebugMessage(f"Verifying Roblox Studio Install..")
                                        def calculate_md5_hash(file_path):
                                            try:
                                                with open(file_path, "rb") as f:
                                                    hasher = hashlib.md5()
                                                    chunk = f.read(8192)
                                                    while chunk: 
                                                        hasher.update(chunk)
                                                        chunk = f.read(8192)
                                                return hasher.hexdigest()
                                            except Exception as e:
                                                if debug == True: printDebugMessage(f"There was an issue trying to get hash: {str(e)}")
                                                return None
                                        verified = True
                                        for rbx_file, hash_value in rbx_hash_dict.items():
                                            if os.path.exists(os.path.join(installPath, rbx_file)):
                                                calculated_hash = calculate_md5_hash(os.path.join(installPath, rbx_file))
                                                if calculated_hash == None:
                                                    if debug == True: printDebugMessage(f"Unable to verify file: {rbx_file}")
                                                    continue
                                                elif not (calculated_hash == hash_value):
                                                    if debug == True: printDebugMessage(f"Unable to verify file: {hash_value} => {calculated_hash}")
                                                    verified = False
                                                    break
                                        if verified == False:
                                            printErrorMessage(f"Unable to install Roblox Studio due to a verification error.")
                                            return
                                    with open(os.path.join(installPath, "RobloxVersion.json"), "w", encoding="utf-8") as f:
                                        json.dump({"ClientVersion": cur_vers.get("client_version", "version-000000000000"), "AppVersion": cur_vers.get("hash", "0.000.0.0000000")}, f, indent=4)
                                    with open(os.path.join(installPath, "AppSettings.xml"), "w", encoding="utf-8") as f:
                                        f.write('<?xml version="1.0" encoding="UTF-8"?><Settings><ContentFolder>content</ContentFolder><BaseUrl>http://www.roblox.com</BaseUrl></Settings>')
                                    if submitStatus: submitStatus.submit(f"[BUNDLE] Successfully installed Roblox Studio Bundle!", 100)
                                    if debug == True: printDebugMessage(f"Successfully installed Roblox Studio to: {installPath} [Client: {cur_vers.get('client_version')}]")
                                except Exception as e:
                                    if submitStatus: submitStatus.submit(f"\033ERR[BUNDLE] Unable to download and install Roblox Studio Bundle!", 100)
                                    if debug == True: printDebugMessage(f"Unable to install Roblox Studio Bundle: {str(e)}")
                            else:
                                if debug == True: printDebugMessage(f"Unable to download Roblox manifest due to an http error. Code: {rbx_man_req.status_code}")
                                if submitStatus: submitStatus.submit("\033ERR[INSTALL] Unable to fetch Roblox manifest file!", 100)
                        elif self.__main_os__ == "Darwin":
                            if platform.machine() == "arm64":
                                roblox_studio_down = f'https://setup.rbxcdn.com/{starter_url}mac/arm64/{cur_vers.get("client_version")}-RobloxStudioApp.zip'
                            else:
                                roblox_studio_down = f'https://setup.rbxcdn.com/{starter_url}mac/{cur_vers.get("client_version")}-RobloxStudioApp.zip'
                            if submitStatus: submitStatus.submit(f"[BUNDLE] Downloading Roblox Studio App!", 0)
                            if debug == True: printDebugMessage(f"Downloading Studio from Roblox's server: {roblox_studio_down}")
                            try:
                                urllib.request.urlretrieve(roblox_studio_down, os.path.join(installPath, "RobloxStudioApp.zip"))
                                if os.path.exists(os.path.join(installPath, "RobloxStudioApp.zip")):
                                    if os.path.exists(os.path.join(installPath, "RobloxStudioApp")) or os.path.exists(appPath):
                                        if debug == True: printDebugMessage(f"Cleaning before install..")
                                        if os.path.exists(os.path.join(installPath, "RobloxStudioApp")): shutil.rmtree(os.path.join(installPath, "RobloxStudioApp"), ignore_errors=True)
                                        if os.path.exists(os.path.join(appPath)): shutil.rmtree(os.path.join(appPath), ignore_errors=True)
                                    if submitStatus: submitStatus.submit(f"[BUNDLE] Extracting Roblox Studio App!", 30)
                                    if debug == True: printDebugMessage(f"Extracting Studio from Downloaded ZIP: {os.path.join(installPath, 'RobloxStudioApp.zip')}")
                                    zip_extract = subprocess.run(["unzip", "-o", os.path.join(installPath, "RobloxStudioApp.zip"), "-d", os.path.join(installPath, "RobloxStudioApp")], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                                    if zip_extract.returncode == 0:
                                        if submitStatus: submitStatus.submit(f"[BUNDLE] Moving Studio!", 60)
                                        if debug == True: printDebugMessage(f"Moving Studio..")
                                        pip().copyTreeWithMetadata(os.path.join(installPath, "RobloxStudioApp", "RobloxStudio.app"), appPath, dirs_exist_ok=True, symlinks=True)
                                        if submitStatus: submitStatus.submit(f"[BUNDLE] Cleaning up Studio!", 80)
                                        if debug == True: printDebugMessage(f"Cleaning up..")
                                        shutil.rmtree(os.path.join(installPath, "RobloxStudioApp"), ignore_errors=True)
                                        os.remove(os.path.join(installPath, "RobloxStudioApp.zip"))
                                        with open(os.path.join(appPath, "Contents", "MacOS", "RobloxVersion.json"), "w", encoding="utf-8") as f:
                                            json.dump({"ClientVersion": cur_vers.get("client_version", "version-000000000000"), "AppVersion": cur_vers.get("hash", "0.000.0.0000000")}, f, indent=4)
                                        if submitStatus: submitStatus.submit(f"[BUNDLE] Successfully installed Roblox Studio Bundle!", 100)
                                        if debug == True: printDebugMessage(f"Successfully installed Roblox Studio to: {installPath} [Client: {cur_vers.get('client_version')}]")
                                    else:
                                        if debug == True: printDebugMessage(f"Unable to extract Studio: {zip_extract.returncode}")
                                        if submitStatus: submitStatus.submit("\033ERR[INSTALL] Failed to extract Roblox Studio.", 100)
                                else:
                                    if debug == True: printDebugMessage(f"Unable to download the Roblox Studio.")
                                    if submitStatus: submitStatus.submit("\033ERR[INSTALL] Failed to download Roblox Studio.", 100)
                            except:
                                if debug == True: printDebugMessage(f"Unable to download and install the Roblox Studio.")
                                if submitStatus: submitStatus.submit("\033ERR[INSTALL] Failed to download and install Roblox Studio.", 100)
                    else:
                        if debug == True: printDebugMessage(f"Unable to fetch install bootstrapper settings from Roblox.")
                        if submitStatus: submitStatus.submit("\033ERR[INSTALL] Unable to fetch bootstrapper settings.", 100)
                else:
                    if debug == True: printDebugMessage(f"Unable to fetch Roblox manifest file due to an http error.")
                    if submitStatus: submitStatus.submit("\033ERR[INSTALL] Unable to fetch Roblox manifest file!", 100)
            except Exception as e:
                if debug == True: printDebugMessage(f"Unable to download and install Roblox Studio Bundle. Error: {str(e)}")
                if submitStatus: submitStatus.submit("\033ERR[INSTALL] Unable to download and install Roblox Studio Bundle!", 100)
        else:
            printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
            if submitStatus: submitStatus.submit("\033ERR[INSTALL] RobloxFastFlagsInstaller is only supported for macOS and Windows.", 100)
    def uninstallRoblox(self, clearUserData=True, debug=False):
        if self.getIfRobloxIsOpen():
            self.endRoblox()
            if debug == True: printDebugMessage("Ending Roblox Instances..")
                
        if self.__main_os__ == "Darwin":
            try:
                if os.path.exists(macOS_dir):
                    if submitStatus: submitStatus.submit("[UNINSTALL] Removing app..", 0)
                    if debug == True: printDebugMessage("Removing Roblox App from Applications..")
                    shutil.rmtree(macOS_dir, ignore_errors=True)
                if os.path.exists(os.path.join(user_folder, "Library", "Roblox", "OTAPatchBackups")):
                    if submitStatus: submitStatus.submit("[UNINSTALL] Removing OTA Patch Backups..", 20)
                    if debug == True: printDebugMessage("Removing OTA Patch Backups..")
                    shutil.rmtree(os.path.join(user_folder, "Library", "Roblox", "OTAPatchBackups"), ignore_errors=True)
                if os.path.exists(os.path.join(user_folder, "Library", "Roblox", "placeIDEState")):
                    if submitStatus: submitStatus.submit("[UNINSTALL] Place IDE States..", 40)
                    if debug == True: printDebugMessage("Removing Place IDE States..")
                    shutil.rmtree(os.path.join(user_folder, "Library", "Roblox", "placeIDEState"), ignore_errors=True)
                if os.path.exists(os.path.join(user_folder, "Library", "Logs", "Roblox")):
                    if submitStatus: submitStatus.submit("[UNINSTALL] Removing Logs..", 60)
                    if debug == True: printDebugMessage("Removing Roblox Logs..")
                    shutil.rmtree(os.path.join(user_folder, "Library", "Logs", "Roblox"), ignore_errors=True)
                if clearUserData == True and os.path.exists(os.path.join(user_folder, "Library", "Roblox")):
                    if submitStatus: submitStatus.submit("[UNINSTALL] Removing Roblox User Data..", 80)
                    if debug == True: printDebugMessage("Removing Roblox User Data..")
                    shutil.rmtree(os.path.join(user_folder, "Library", "Roblox"), ignore_errors=True)
                if submitStatus: submitStatus.submit("[UNINSTALL] Successfully uninstalled Roblox!", 100)
            except Exception as e:
                printErrorMessage(f"Something went wrong deleting Roblox: {str(e)}")
        elif self.__main_os__ == "Windows":
            try:
                for i in os.listdir(f"{windows_versions_dir}"):
                    if os.path.isdir(os.path.join(windows_versions_dir, i)) and os.path.exists(os.path.join(windows_versions_dir, i, "RobloxPlayerBeta.exe")):
                        if submitStatus: submitStatus.submit("[UNINSTALL] Removing app..", 0)
                        if debug == True: printDebugMessage("Removing Roblox App from System..")
                        shutil.rmtree(os.path.join(windows_versions_dir, i), ignore_errors=True)
                if os.path.exists(os.path.join(windows_dir, "OTAPatchBackups")):
                    if submitStatus: submitStatus.submit("[UNINSTALL] Removing OTA Patch Backups..", 45)
                    if debug == True: printDebugMessage("Removing OTA Patch Backups..")
                    shutil.rmtree(os.path.join(windows_dir, "OTAPatchBackups"), ignore_errors=True)
                if os.path.exists(os.path.join(windows_dir, "placeIDEState")):
                    if submitStatus: submitStatus.submit("[UNINSTALL] Removing Place IDE States..", 60)
                    if debug == True: printDebugMessage("Removing Place IDE States..")
                    shutil.rmtree(os.path.join(windows_dir, "placeIDEState"), ignore_errors=True)
                if os.path.exists(os.path.join(windows_dir, "Downloads", "roblox-player")):
                    if submitStatus: submitStatus.submit("[UNINSTALL] Removing Roblox Downloads..", 75)
                    if debug == True: printDebugMessage("Removing Downloads..")
                    shutil.rmtree(os.path.join(windows_dir, "Downloads", "roblox-player"), ignore_errors=True)
                if os.path.exists(os.path.join(windows_dir, "UniversalApp")):
                    if submitStatus: submitStatus.submit("[UNINSTALL] Removing Universe App..", 85)
                    if debug == True: printDebugMessage("Removing Universal App..")
                    shutil.rmtree(os.path.join(windows_dir, "UniversalApp"), ignore_errors=True)
                if os.path.exists(os.path.join(windows_dir, "logs")):
                    if submitStatus: submitStatus.submit("[UNINSTALL] Removing Logs..", 90)
                    if debug == True: printDebugMessage("Removing Roblox Logs..")
                    shutil.rmtree(os.path.join(windows_dir, "logs"), ignore_errors=True)
                if clearUserData == True and os.path.exists(windows_dir):
                    if submitStatus: submitStatus.submit("[UNINSTALL] Removing Roblox User Data..", 95)
                    if debug == True: printDebugMessage("Removing Roblox User Data..")
                    shutil.rmtree(windows_dir, ignore_errors=True)
                if submitStatus: submitStatus.submit("[UNINSTALL] Successfully uninstalled Roblox!", 100)
            except Exception as e:
                printErrorMessage(f"Something went wrong starting Roblox Installer: {str(e)}")
        else:
            printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
            if submitStatus: submitStatus.submit("\033ERR[INSTALL] RobloxFastFlagsInstaller is only supported for macOS and Windows.", 100)
    def reinstallRoblox(self, debug=False, clearUserData=True, disableRobloxAutoOpen=False, copyRobloxInstallerPath="", downloadInstaller=False):
        if self.__main_os__ == "Darwin" or self.__main_os__ == "Windows":
            if self.getIfRobloxIsOpen():
                self.endRoblox()
                if debug == True: printDebugMessage("Ending Roblox Instances..")

            channel = "LIVE"
            if downloadInstaller == True:
                channel_res = self.getCurrentClientVersion()
                if channel_res.get("success") == True:
                    channel = channel_res.get("channel", "LIVE")
                    
            if submitStatus: submitStatus.submit("Uninstalling Roblox", 0)
            self.uninstallRoblox(debug=debug, clearUserData=clearUserData)
            if submitStatus: submitStatus.submit("Installing Roblox", 50)
            self.installRoblox(debug=debug, disableRobloxAutoOpen=disableRobloxAutoOpen, copyRobloxInstallerPath=copyRobloxInstallerPath, downloadInstaller=downloadInstaller, downloadChannel=channel)
            if submitStatus: submitStatus.submit("Successfully reinstalled Roblox Player!", 100)
        else:
            printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
            if submitStatus: submitStatus.submit("\033ERR[INSTALL] RobloxFastFlagsInstaller is only supported for macOS and Windows.", 100)
    def uninstallRobloxStudio(self, clearUserData=True, debug=False):
        if self.getIfRobloxStudioIsOpen():
            self.endRobloxStudio()
            if debug == True: printDebugMessage("Ending Roblox Instances..")
                
        if self.__main_os__ == "Darwin":
            try:
                if os.path.exists(macOS_studioDir):
                    if submitStatus: submitStatus.submit("[UNINSTALL] Removing app..", 0)
                    if debug == True: printDebugMessage("Removing Roblox Studio App from Applications..")
                    shutil.rmtree(macOS_studioDir, ignore_errors=True)
                if os.path.exists(os.path.join(user_folder, "Library", "Roblox", "OTAPatchBackups")):
                    if submitStatus: submitStatus.submit("[UNINSTALL] Removing OTA Patch Backups..", 20)
                    if debug == True: printDebugMessage("Removing OTA Patch Backups..")
                    shutil.rmtree(os.path.join(user_folder, "Library", "Roblox", "OTAPatchBackups"), ignore_errors=True)
                if os.path.exists(os.path.join(user_folder, "Library", "Roblox", "placeIDEState")):
                    if submitStatus: submitStatus.submit("[UNINSTALL] Removing Place IDE States..", 40)
                    if debug == True: printDebugMessage("Removing Place IDE States..")
                    shutil.rmtree(os.path.join(user_folder, "Library", "Roblox", "placeIDEState"), ignore_errors=True)
                if os.path.exists(os.path.join(user_folder, "Library", "Logs", "Roblox")):
                    if submitStatus: submitStatus.submit("[UNINSTALL] Removing Logs..", 60)
                    if debug == True: printDebugMessage("Removing Roblox Logs..")
                    shutil.rmtree(os.path.join(user_folder, "Library", "Logs", "Roblox"), ignore_errors=True)
                if clearUserData == True and os.path.exists(os.path.join(user_folder, "Library", "Roblox")):
                    if submitStatus: submitStatus.submit("[UNINSTALL] Removing Roblox User Data..", 80)
                    if debug == True: printDebugMessage("Removing Roblox User Data..")
                    shutil.rmtree(os.path.join(user_folder, "Library", "Roblox"), ignore_errors=True)
                if submitStatus: submitStatus.submit("[UNINSTALL] Successfully uninstalled Roblox Studio!", 100)
            except Exception as e:
                printErrorMessage(f"Something went wrong removing Roblox: {str(e)}")
        elif self.__main_os__ == "Windows":
            try:
                for i in os.listdir(windows_versions_dir):
                    if os.path.isdir(os.path.join(windows_versions_dir, i)) and os.path.exists(os.path.join(windows_versions_dir, i, "RobloxStudioBeta.exe")):
                        if submitStatus: submitStatus.submit("[UNINSTALL] Removing Roblox Studio App..", 0)
                        if debug == True: printDebugMessage("Removing Roblox Studio App from System..")
                        shutil.rmtree(os.path.join(windows_versions_dir, i), ignore_errors=True)
                if os.path.exists(os.path.join(windows_dir, "OTAPatchBackups")):
                    if submitStatus: submitStatus.submit("[UNINSTALL] Removing OTA Patch Backups..", 45)
                    if debug == True: printDebugMessage("Removing OTA Patch Backups..")
                    shutil.rmtree(os.path.join(windows_dir, "OTAPatchBackups"), ignore_errors=True)
                if os.path.exists(os.path.join(windows_dir, "placeIDEState")):
                    if submitStatus: submitStatus.submit("[UNINSTALL] Removing Place IDE States..", 60)
                    if debug == True: printDebugMessage("Removing Place IDE States..")
                    shutil.rmtree(os.path.join(windows_dir, "placeIDEState"), ignore_errors=True)
                if os.path.exists(os.path.join(windows_dir, "Downloads", "roblox-studio")):
                    if submitStatus: submitStatus.submit("[UNINSTALL] Removing Downloads..", 75)
                    if debug == True: printDebugMessage("Removing Downloads..")
                    shutil.rmtree(os.path.join(windows_dir, "Downloads", "roblox-studio"), ignore_errors=True)
                if os.path.exists(os.path.join(windows_dir, "UniversalApp")):
                    if submitStatus: submitStatus.submit("[UNINSTALL] Removing Universal App..", 80)
                    if debug == True: printDebugMessage("Removing Universal App..")
                    shutil.rmtree(os.path.join(windows_dir, "UniversalApp"), ignore_errors=True)
                if os.path.exists(os.path.join(windows_dir, "logs")):
                    if submitStatus: submitStatus.submit("[UNINSTALL] Removing Logs..", 85)
                    if debug == True: printDebugMessage("Removing Roblox Logs..")
                    shutil.rmtree(os.path.join(windows_dir, "logs"), ignore_errors=True)
                if clearUserData == True and os.path.exists(windows_dir):
                    if submitStatus: submitStatus.submit("[UNINSTALL] Removing Roblox User Data..", 90)
                    if debug == True: printDebugMessage("Removing Roblox User Data..")
                    shutil.rmtree(windows_dir, ignore_errors=True)
                if submitStatus: submitStatus.submit("[UNINSTALL] Successfully uninstalled Roblox Studio!", 100)
            except Exception as e:
                printErrorMessage(f"Something went wrong starting Roblox Installer: {str(e)}")
        else:
            printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
            if submitStatus: submitStatus.submit("\033ERR[INSTALL] RobloxFastFlagsInstaller is only supported for macOS and Windows.", 100)
    def reinstallRobloxStudio(self, debug=False, clearUserData=True, disableRobloxAutoOpen=False, copyRobloxInstallerPath="", downloadInstaller=False):
        if self.__main_os__ == "Darwin" or self.__main_os__ == "Windows":
            if self.getIfRobloxStudioIsOpen():
                self.endRobloxStudio()
                if debug == True: printDebugMessage("Ending Roblox Studio Instances..")

            channel = "LIVE"
            if downloadInstaller == True:
                channel_res = self.getCurrentStudioClientVersion()
                if channel_res.get("success") == True:
                    channel = channel_res.get("channel", "LIVE")
                    
            if submitStatus: submitStatus.submit("Uninstalling Roblox Studio", 0)
            self.uninstallRobloxStudio(debug=debug, clearUserData=clearUserData)
            if submitStatus: submitStatus.submit("Installing Roblox Studio", 50)
            self.installRobloxStudio(debug=debug, disableRobloxAutoOpen=disableRobloxAutoOpen, copyRobloxInstallerPath=copyRobloxInstallerPath, downloadInstaller=downloadInstaller, downloadChannel=channel)
            if submitStatus: submitStatus.submit("Successfully reinstalled Roblox Studio!", 100)
        else:
            printLog("RobloxFastFlagsInstaller is only supported for macOS and Windows.")
            if submitStatus: submitStatus.submit("\033ERR[INSTALL] RobloxFastFlagsInstaller is only supported for macOS and Windows.", 100)

if __name__ == "__main__":
    handler = Main()
    pip_class = pip()
    if orangeblox_mode == False:
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
        def waitForInternet():
            if pip_class.getIfConnectedToInternet() == False:
                printWarnMessage("--- Waiting for Internet ---")
                printMainMessage("Please connect to your internet in order to continue! If you're connecting to a VPN, try reconnecting.")
                while pip_class.getIfConnectedToInternet() == False:
                    time.sleep(0.05)
                return True
        if waitForInternet() == True: printWarnMessage("-----------")
        if main_os == "Windows":
            printMainMessage(f"System OS: {main_os}")
            found_platform = "Windows"
        elif main_os == "Darwin":
            printMainMessage(f"System OS: {main_os} (macOS {platform.mac_ver()[0]})")
            found_platform = "Darwin"
        else:
            input("> ")
            sys.exit(0)
        printMainMessage(f"Python Version: {pip_class.getCurrentPythonVersion()}{pip_class.getIfPythonVersionIsBeta() and ' (BETA)' or ''}")
        if not pip_class.pythonSupported(3, 11, 0):
            if not pip_class.pythonSupported(3, 6, 0):
                printErrorMessage("Please update your current installation of Python above 3.11.0")
                input("> ")
                sys.exit(0)
            else:
                latest_python = pip_class.getLatestPythonVersion()
                printWarnMessage("--- Python Update Required ---")
                printMainMessage("Hello! In order to use OrangeBlox, you'll need to install Python 3.11 or higher in order to continue. ")
                printMainMessage(f"If you wish, you may install Python {latest_python} by typing \"y\" and continue.")
                printMainMessage("Otherwise, you may close the app by just continuing without typing.")
                if isYes(input("> ")) == True:
                    pip_class.pythonInstall(latest_python)
                    printSuccessMessage(f"If installed correctly, Python {latest_python} should be available to be used!")
                    printSuccessMessage("Please restart the script to install!")
                    input("> ")
                sys.exit(0)
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
        app_settings = handler.getRobloxAppSettings()
        if app_settings.get("loggedInUser") and app_settings.get("loggedInUser").get("id"):
            return app_settings.get("loggedInUser").get("id")
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
    def getIfStudio():
        printMainMessage("Please select the type of Roblox would you like to install to!")
        printMainMessage("[1] = Roblox Player")
        printMainMessage("[2] = Roblox Studio")
        id = input("> ")
        if id == "1":
            return False
        elif id == "2":
            return True
        else:
            return getIfStudio()

    # Information
    user_id = getUserId()
    generated_json = {}
    is_studio = getIfStudio()

    # Important Information
    printWarnMessage("--- Important Information ---")
    printMainMessage("May 2nd, 2025 - v2.1.0")
    printMainMessage("As of some updates from Roblox, some FFlags may not work in the future. Other functions such as Roblox Opening and Activity Tracking is still available from this module.")

    # Setup Information
    printWarnMessage("--- Setup Information ---")
    printMainMessage(f"Roblox User ID: {user_id}")
    printMainMessage(f"Install to Studio: {is_studio==True}")
    if is_studio == True: printMainMessage("Alright! So, we will start with flags that are available for the Roblox player to be run in the playtest window!")

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
        if user_id: generated_json["FStringWhitelistVerifiedUserId"] = str(user_id)
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
    printMainMessage("Would you like to increase the limit on Max Assets loading from 100? (this will make loading into games faster depending on your computer) (y/n)")
    printYellowMessage("WARNING! This can crash your Roblox session!")
    installRemoveMaxAssets = input("> ")
    if isYes(installRemoveMaxAssets) == True:
        printMainMessage("Enter the amount of assets you would like to load at the same time:")
        installRemoveMaxAssetsNum = input("> ")
        if installRemoveMaxAssetsNum.isnumeric():
            generated_json["DFIntNumAssetsMaxToPreload"] = str(int(installRemoveMaxAssetsNum))
            generated_json["DFIntAssetPreloading"] = str(int(installRemoveMaxAssetsNum))
        else:
            printYellowMessage("Disabled limit due to invalid prompt.")
            generated_json["DFIntNumAssetsMaxToPreload"] = "100"
            generated_json["DFIntAssetPreloading"] = "100"
    elif isRequestClose(installRemoveMaxAssets) == True:
        printMainMessage("Ending installation..")
        exit()
    elif isNo(installRemoveMaxAssets) == True:
        generated_json["DFIntNumAssetsMaxToPreload"] = "100"
        generated_json["DFIntAssetPreloading"] = "100"

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

    # Disable Voice Chat
    printWarnMessage("--- Disable Voice Chat ---")
    printMainMessage("Would you like to disable Voice Chat? (y/n)")
    installDisableVoiceChat = input("> ")
    if isYes(installDisableVoiceChat) == True:
        generated_json["DFFlagVoiceChat4"] = "false"
    elif isRequestClose(installDisableVoiceChat) == True:
        printMainMessage("Ending installation..")
        exit()
    elif isNo(installDisableVoiceChat) == True:
        generated_json["DFFlagVoiceChat4"] = "true"

    # Disable In-Game Chat
    printWarnMessage("--- Disable In-Game Chat ---")
    printMainMessage("Would you like to disable In-Game Chat? (y/n)")
    installDisableGameChat = input("> ")
    if isYes(installDisableGameChat) == True:
        generated_json["FFlagDebugForceChatDisabled"] = "true"
    elif isRequestClose(installDisableGameChat) == True:
        printMainMessage("Ending installation..")
        exit()
    elif isNo(installDisableGameChat) == True:
        generated_json["FFlagDebugForceChatDisabled"] = "false"

    # Disable Full Screen Title Bar
    printWarnMessage("--- Disable Full Screen Title Bar ---")
    printMainMessage("Would you like to disable the Title Bar when you go into full screen on the Roblox client? (y/n)")
    installDisableFullScreenTitle = input("> ")
    if isYes(installDisableFullScreenTitle) == True:
        generated_json["FIntFullscreenTitleBarTriggerDelayMillis"] = "3600000"
    elif isRequestClose(installDisableFullScreenTitle) == True:
        printMainMessage("Ending installation..")
        exit()
    elif isNo(installDisableFullScreenTitle) == True:
        generated_json["FIntFullscreenTitleBarTriggerDelayMillis"] = ""

    # Enable Red Text Font
    printWarnMessage("--- Enable Red Text Font ---")
    printMainMessage("Would you like to enable Red text instead of White text color in the lua app? (y/n)")
    installRedText = input("> ")
    if isYes(installRedText) == True:
        generated_json["FStringDebugHighlightSpecificFont"] = "rbxasset://fonts/families/BuilderSans.json"
    elif isRequestClose(installRedText) == True:
        printMainMessage("Ending installation..")
        exit()
    elif isNo(installRedText) == True:
        generated_json["FStringDebugHighlightSpecificFont"] = ""

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

    # Rendering Mode
    got_modes = []
    ui_options = {}
    if main_os == "Darwin":
        got_modes.append("Metal (for MacOS)")
    got_modes.append("Vulkan (may cause issues)")
    got_modes.append("OpenGL")
    got_modes.append("DirectX 10")
    got_modes.append("DirectX 11")
    got_modes = sorted(got_modes)
    count = 1

    generated_json["FFlagDebugGraphicsPreferMetal"] = ""
    generated_json["FFlagDebugGraphicsDisableDirect3D11"] = ""
    generated_json["FFlagDebugGraphicsPreferVulkan"] = ""
    generated_json["FFlagDebugGraphicsPreferOpenGL"] = ""
    generated_json["FFlagDebugGraphicsPreferD3D11FL10"] = ""
    generated_json["FFlagDebugGraphicsPreferD3D11"] = ""
        
    printWarnMessage("--- Rendering Mode ---")
    printMainMessage("Select a rendering mode to force on the client:")
    print("\033[38;5;215mThis FFlag was from the LatteFlags GitHub! (https://github.com/espresso-soft/latteflags)\033[0m")
    for i in got_modes:
        printMainMessage(f"[{str(count)}] = {i}")
        ui_options[str(count)] = i
        count += 1
    print("[*] = None")
    installRenderingMode = input("> ")
    if ui_options.get(installRenderingMode):
        opt = ui_options[installRenderingMode]
        if opt == "Metal (for MacOS)":
            generated_json["FFlagDebugGraphicsPreferMetal"] = "true"
        elif opt == "Vulkan (may cause issues)":
            generated_json["FFlagDebugGraphicsDisableDirect3D11"] = "true"
            generated_json["FFlagDebugGraphicsPreferVulkan"] = "true"
        elif opt == "OpenGL":
            generated_json["FFlagDebugGraphicsDisableDirect3D11"] = "true"
            generated_json["FFlagDebugGraphicsPreferOpenGL"] = "true"
        elif opt == "DirectX 10":
            generated_json["FFlagDebugGraphicsPreferD3D11FL10"] = "true"
        elif opt == "DirectX 11":
            generated_json["FFlagDebugGraphicsPreferD3D11"] = "true"

    # Lighting Mode
    got_modes = []
    ui_options = {}
    got_modes.append("Voxel Lighting (Phase 1)")
    got_modes.append("Shadowmap Lighting (Phase 2)")
    got_modes.append("Future Lighting (Phase 3)")
    got_modes.append("Unified Lighting")
    got_modes = sorted(got_modes)
    count = 1

    generated_json["DFFlagDebugRenderForceTechnologyVoxel"] = ""
    generated_json["FFlagDebugForceFutureIsBrightPhase2"] = ""
    generated_json["FFlagDebugForceFutureIsBrightPhase3"] = ""
    generated_json["FFlagRenderUnifiedLighting10"] = ""
    generated_json["FFlagUnifiedLightingBetaFeature"] = ""
        
    printWarnMessage("--- Lighting Mode ---")
    printMainMessage("Select a lighting mode to force on the client:")
    print("\033[38;5;215mThis FFlag was from the LatteFlags GitHub! (https://github.com/espresso-soft/latteflags)\033[0m")
    for i in got_modes:
        printMainMessage(f"[{str(count)}] = {i}")
        ui_options[str(count)] = i
        count += 1
    print("[*] = None")
    installLightingMode = input("> ")
    if ui_options.get(installLightingMode):
        opt = ui_options[installLightingMode]
        if opt == "Voxel Lighting (Phase 1)":
            generated_json["DFFlagDebugRenderForceTechnologyVoxel"] = "true"
        elif opt == "Shadowmap Lighting (Phase 2)":
            generated_json["FFlagDebugForceFutureIsBrightPhase2"] = "true"
        elif opt == "Future Lighting (Phase 3)":
            generated_json["FFlagDebugForceFutureIsBrightPhase3"] = "true"
        elif opt == "Unified Lighting":
            generated_json["FFlagRenderUnifiedLighting10"] = "true"
            generated_json["FFlagUnifiedLightingBetaFeature"] = "true"

    # Texture Quality
    got_modes = []
    ui_options = {}
    got_modes.append("Level 1 (Low Quality)")
    got_modes.append("Level 2 (Medium Quality)")
    got_modes.append("Level 3 (Highest Quality)")
    got_modes = sorted(got_modes)
    count = 1

    generated_json["DFFlagTextureQualityOverrideEnabled"] = ""
    generated_json["DFIntTextureQualityOverride"] = ""
        
    printWarnMessage("--- Texture Quality ---")
    printMainMessage("Select a texture quality number to put on the client:")
    for i in got_modes:
        printMainMessage(f"[{str(count)}] = {i}")
        ui_options[str(count)] = i
        count += 1
    print("[*] = None")
    installTextureQuality = input("> ")
    if ui_options.get(installTextureQuality):
        opt = ui_options[installTextureQuality]
        if opt == "Level 1 (Low Quality)":
            generated_json["DFFlagTextureQualityOverrideEnabled"] = "true"
            generated_json["DFIntTextureQualityOverride"] = "1"
        elif opt == "Level 2 (Medium Quality)":
            generated_json["DFFlagTextureQualityOverrideEnabled"] = "true"
            generated_json["DFIntTextureQualityOverride"] = "2"
        elif opt == "Level 3 (Highest Quality)":
            generated_json["DFFlagTextureQualityOverrideEnabled"] = "true"
            generated_json["DFIntTextureQualityOverride"] = "3"

    # Disable Highlights
    printWarnMessage("--- Disable Highlights ---")
    printMainMessage("Would you like to disable Highlight rendering on the client? (y/n)")
    print("\033[38;5;215mThis FFlag was from the LatteFlags GitHub! (https://github.com/espresso-soft/latteflags)\033[0m")
    installDisableHighLight = input("> ")
    if isYes(installDisableHighLight) == True:
        generated_json["DFFlagRenderHighlightManagerPrepare"] = "true"
    elif isRequestClose(installDisableHighLight) == True:
        printMainMessage("Ending installation..")
        exit()
    elif isNo(installDisableHighLight) == True:
        generated_json["DFFlagRenderHighlightManagerPrepare"] = "false"

    # Limit Videos Playing
    printWarnMessage("--- Limit Videos Playing ---")
    printMainMessage("Would you like to set a number of Videos that can be played in-game on the client? (y/n)")
    print("\033[38;5;215mThis FFlag was from the LatteFlags GitHub! (https://github.com/espresso-soft/latteflags)\033[0m")
    installLimitVideos = input("> ")
    if isYes(installLimitVideos) == True:
        printMainMessage("Input the number of videos you would like to limit:")
        installLimitVideosNum = input("> ")
        if installLimitVideosNum.isnumeric():
            generated_json["DFIntVideoMaxNumberOfVideosPlaying"] = str(int(installLimitVideosNum))
        else:
            printYellowMessage("Disabled limit due to invalid prompt.")
            generated_json["DFIntVideoMaxNumberOfVideosPlaying"] = ""
    elif isRequestClose(installLimitVideos) == True:
        printMainMessage("Ending installation..")
        exit()
    elif isNo(installLimitVideos) == True:
        generated_json["DFIntVideoMaxNumberOfVideosPlaying"] = ""

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
    printMainMessage("Would you like to use your own disconnect message? (reconnect button will disappear) (y/n)")
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

    # Pre-Rendering
    printWarnMessage("--- Pre-Rendering ---")
    printMainMessage("Would you like to enable Pre-Rendering on the client? (y/n)")
    printYellowMessage("This may conclude a 25% Performance Boost but may cause compatibility issues in games.")
    print("\033[38;5;215mThis FFlag was from the LatteFlags GitHub! (https://github.com/espresso-soft/latteflags)\033[0m")
    installPreRendering = input("> ")
    if isYes(installPreRendering) == True:
        generated_json["FFlagMovePrerender"] = "true"
    elif isRequestClose(installPreRendering) == True:
        printMainMessage("Ending installation..")
        exit()
    elif isNo(installPreRendering) == True:
        generated_json["FFlagMovePrerender"] = "false"

    # Studio Flags
    if is_studio == True: 
        printMainMessage("Alright! After that, we can now start with studio specific flags!")
        # Default to Select Tool
        printWarnMessage("--- Default to Select Tool ---")
        printMainMessage("Would you like to enable defaulting to the Select tool when in a place? (y/n)")
        installSelectTool = input("> ")
        if isYes(installSelectTool) == True:
            generated_json["FFlagDefaultToSelectTool"] = True
        elif isRequestClose(installSelectTool) == True:
            printMainMessage("Ending installation..")
            exit()
        elif isNo(installSelectTool) == True:
            generated_json["FFlagDefaultToSelectTool"] = False
        
        # Enable Materials Generator
        printWarnMessage("--- Enable Materials Generator ---")
        printMainMessage("Would you like to enable materials generator? (y/n)")
        installMaterialsGen = input("> ")
        if isYes(installMaterialsGen) == True:
            generated_json["FFlagEnableMaterialGenerator"] = True
        elif isRequestClose(installMaterialsGen) == True:
            printMainMessage("Ending installation..")
            exit()
        elif isNo(installMaterialsGen) == True:
            generated_json["FFlagEnableMaterialGenerator"] = False

        # Enable Ragdoll Death Animation
        printWarnMessage("--- Enable Ragdoll Death Animation ---")
        printMainMessage("Would you like to enable the ragdoll death animation? (y/n)")
        installRagdoll = input("> ")
        if isYes(installRagdoll) == True:
            generated_json["DFStringDefaultAvatarDeathType"] = "Ragdoll"
        elif isRequestClose(installRagdoll) == True:
            printMainMessage("Ending installation..")
            exit()
        elif isNo(installRagdoll) == True:
            generated_json["DFStringDefaultAvatarDeathType"] = None

        # Enable Assistant Code Generation
        printWarnMessage("--- Enable Assistant Code Generation ---")
        printMainMessage("Would you like to allow the assistant to generate code? (y/n)")
        installAssistantCode = input("> ")
        if isYes(installAssistantCode) == True:
            generated_json["FFlagLuauCodegen"] = True
        elif isRequestClose(installAssistantCode) == True:
            printMainMessage("Ending installation..")
            exit()
        elif isNo(installAssistantCode) == True:
            generated_json["FFlagLuauCodegen"] = False
        
        # Enable Multi Select
        printWarnMessage("--- Enable Multi Select ---")
        printMainMessage("Would you like to enable multi selecting? (y/n)")
        installMultiSelect = input("> ")
        if isYes(installMultiSelect) == True:
            generated_json["FFlagMultiSelect"] = True
        elif isRequestClose(installMultiSelect) == True:
            printMainMessage("Ending installation..")
            exit()
        elif isNo(installMultiSelect) == True:
            generated_json["FFlagMultiSelect"] = False

    # Custom Fast Flags
    printWarnMessage("--- Custom Fast Flags ---")
    def custom():
        def loop():
            printMainMessage("Enter Key Name: ")
            key = input("> ")
            if isRequestClose(key) or key == "":
                return {"success": False, "key": "", "value": ""}
            if orangeblox_mode == True and key.startswith("EFlag"):
                printMainMessage("Are you sure you want to set this OrangeBlox setting?")
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
    if orangeblox_mode == False:
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
        if orangeblox_mode == False:
            printWarnMessage("--- Installation Ready! ---")
            printMainMessage("Settings are now finished and now ready for setup!")
            printMainMessage("Would you like to continue with the fast flag installation? (y/n)")
            printErrorMessage("WARNING! This will force-quit any open Roblox windows! Please close them now before continuing in order to prevent data loss!")
            install_now = input("> ")
            if isYes(install_now) == True:
                if isYes(select_mode) == True:
                    handler.installFastFlags(generated_json, studio=is_studio)
                elif select_mode.lower() == "j" or select_mode.lower() == "json":
                    printMainMessage("Generated JSON:")
                    printMainMessage(json.dumps(generated_json))
                    exit()
                elif select_mode.lower() == "nm" or select_mode.lower() == "no-merge":
                    handler.installFastFlags(generated_json, merge=False, studio=is_studio)
                elif select_mode.lower() == "f" or select_mode.lower() == "flat":
                    handler.installFastFlags(generated_json, flat=True, studio=is_studio)
                elif select_mode.lower() == "fnm" or select_mode.lower() == "flat-no-merge":
                    handler.installFastFlags(generated_json, merge=False, flat=True, studio=is_studio)
                elif select_mode.lower() == "r" or select_mode.lower() == "reset":
                    handler.installFastFlags({}, studio=is_studio)
                else:
                    printMainMessage("Ending installation..")
                    exit()
            else:
                printMainMessage("Ending installation..")
                exit()
        else:
            printWarnMessage("--- Saving Ready! ---")
            printMainMessage("Are you sure you would like to save these FFlags in the bootstrap system? (y/n)")
            install_now = input("> ")
            if isNo(install_now) == True:
                printMainMessage("Ending installation..")
                exit()
            else:
                handler.installFastFlags(generated_json, endRobloxInstances=False, studio=is_studio)