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
    def restartScript(self):
        import sys
        import subprocess
        subprocess.run([self.findPython()] + sys.argv, shell=True)
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
            process = subprocess.run("tasklist", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        elif ma_os == "Darwin":
            process = subprocess.run("ps aux", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        else:
            process = subprocess.run("ps aux", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        process_list = process.stdout.decode("utf-8")

        if pid == "":
            if process_list.rfind(process_name) == -1:
                return False
            else:
                return True
        else:
            if process_list.rfind(pid) == -1:
                return False
            else:
                return True
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
        
if __name__ == "__main__":
    print("PipHandler.py is a module and is not a runable instance!")