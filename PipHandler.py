# 
# PipHandler
# Made by Efaz from efaz.dev
# 
# A usable class with extra functions that can be used within apps.
# Import from file: from PipHandler import pip
# Import from class: 
# class pip: ...
# pip_class = pip()
# 

import typing
import logging
import sys
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
class stdout:
    buffer: str = ""
    logger: logging.Logger = None
    log_level: int = None
    encoding: str = "utf-8"
    line_count = 0
    locked_new = False
    lang = "norm"
    awaiting_bar_logs = []
    translation_json = {}

    def __init__(self, logger, log_level, lang="norm"): 
        self.logger = logger; self.log_level = log_level; self.lang = lang
        if not (self.lang == "norm"):
            import json
            import os
            current_path_location = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(current_path_location, f"translations_{self.lang}.json")) as f:
                self.translation_json = json.load(f)
    def write(self, message: str): 
        if self.locked_new == True and not message.startswith("\033{progressend}"): self.awaiting_bar_logs.append(message); return
        if message.startswith("\033{progress}"):
            message = message.replace("\033{progress}", "", 1)
            sys.__stdout__.write("\n")
            sys.__stdout__.flush()
            self.locked_new = True
            return
        elif message.startswith("\033{progressend}"):
            self.locked_new = False
            for i in self.awaiting_bar_logs:
                self.write(i)
            self.awaiting_bar_logs = []
            return
        
        if message == "> ":
            sys.__stdout__.write(message)
            sys.__stdout__.flush()
            return
        if not (self.lang == "norm"):
            def translate(a): 
                s = a
                for i, v in self.translation_json.items(): s = s.replace(i, v)
                return s
            message = translate(message)
        self.buffer += message; 
        while "\n" in self.buffer:
            line, self.buffer = self.buffer.rsplit("\n", 1)
            self.line_count += 1
            if line.rstrip(): 
                try:
                    self.logger.log(self.log_level, line.rstrip())
                except Exception:
                    self.logger.log(self.log_level, line.rstrip().encode(self.encoding, errors="replace").decode(self.encoding))
    def clear(self):
        import os
        os.system("cls" if os.name == "nt" else 'echo "\033c\033[3J"; clear')
        self.line_count = 0
    def change_last_message(self, message: str):
        sys.__stdout__.write("\033[1A")
        sys.__stdout__.write("\033[2K")
        sys.__stdout__.write(message + "\n")
        sys.__stdout__.flush()
    def flush(self):
        if self.buffer.rstrip():
            try: 
                self.logger.log(self.log_level, self.buffer.rstrip()); 
            except Exception:
                self.logger.log(self.log_level, self.buffer.rstrip().encode(self.encoding, errors="replace").decode(self.encoding))
        self.buffer = ''
class ProgressBar():   
    current_percentage = 0
    status_text = ""
    def submit(self, status_text: str, percentage: int):
        self.current_percentage = percentage
        self.status_text = status_text
        if getattr(sys.stdout, "line_count"):
            fin = round(self.current_percentage/(100/20))
            beginning = '\033[38;5;82m✅' if self.current_percentage >= 100 else '\033[38;5;255m🚀'
            if self.status_text.startswith("\033ERR"): beginning = '\033[38;5;196m❌'; self.status_text = self.status_text.replace("\033ERR", "", 1)
            message = f"{beginning} {self.status_text} [{'█'*int(fin)}{'░'*int(20-fin)}] {self.current_percentage}%\033[0m"
            sys.stdout.change_last_message(message)
    def start(self): print("\033{progress}")
    def end(self): print("\033{progressend}")
class TimerBar():   
    current_countdown = 5
    started = 5
    finished_text = "Continue with your action!"
    begin_in_end = True
    def __init__(self, countdown: int=5, finished_text: str="Continue with your action!", begin_in_end: bool=True):
        self.current_countdown = int(countdown); 
        self.started = int(countdown); 
        self.finished_text = finished_text; 
        self.begin_in_end = begin_in_end
    def submit(self):
        if getattr(sys.stdout, "line_count"):
            fin = round(((self.current_countdown/self.started)*100)/(100/self.started))
            if self.begin_in_end == True or self.current_countdown > 0: beginning = f"\033[38;5;82m✅ [{'█'*int(fin)}{'░'*int(self.started-fin)}] " if self.current_countdown == 0 else f"\033[38;5;255m⏰ [{'█'*int(fin)}{'░'*int(self.started-fin)}] "
            else: beginning = "\033[38;5;255m"
            if self.current_countdown == 0: message = f"{beginning}{self.finished_text}\033[0m"
            else: message = f"{beginning}{self.current_countdown}s\033[0m"
            sys.stdout.change_last_message(message)
    def start(self): 
        print("\033{progress}")
        import time
        while self.current_countdown:
            self.submit()
            if self.current_countdown == 0: break
            self.current_countdown -= 1
            time.sleep(1)
        self.submit()
        print("\033{progressend}")
class InstantRequestJSONResponse:
    ok = True
    data = None
    def __init__(self, data):
        self.data = data
    def json(self):
        return self.data
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
if __name__ == "__main__": print("PipHandler.py is a module and is not a runable instance!")