# Usable Version in Python Scripts [Import Needed Modules During Function]
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
        
if __name__ == "__main__":
    print("PipHandler.py is a module and is not a runable instance!")