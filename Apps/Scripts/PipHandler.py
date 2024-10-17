import subprocess
import importlib
import platform
import os
import glob
import tempfile

class pip:
    executable = None
    def __init__(self, command: list=[], executable: str=None):
        if type(executable) is str:
            if os.path.isfile(executable):
                self.executable = executable
            else:
                self.executable = self.findPython()
        else:
            self.executable = self.findPython()
        if type(command) is list and len(command) > 0:
            subprocess.check_call([self.executable, "-m", "pip"] + command)
    def install(self, packages: list[str]):
        for i in packages:
            subprocess.check_call([self.executable, "-m", "pip", "install", i])
    def uninstall(self, packages: list[str]):
        for i in packages:
            subprocess.check_call([self.executable, "-m", "pip", "uninstall", i])
    def installed(self, packages: list[str]):
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
            if ma_arch[0] == "32bit":
                url = "https://www.python.org/ftp/python/3.13.0/python-3.13.0.exe"
            elif ma_arch[0] == "64bit" and ma_processor.lower() == "arm64":
                url = "https://www.python.org/ftp/python/3.13.0/python-3.13.0-arm64.exe"
            elif ma_arch[0] == "64bit" and ma_processor.lower() == "amd64":
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
    def findPython(self):
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