try:
    import pypresence
    import logging
    import warnings
    import time
    import uuid
    import sys
    import sys
    import threading
except Exception as e:
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
            import subprocess
            import tempfile

            ma_os = platform.system()
            if ma_os == "Darwin":
                url = "https://www.python.org/ftp/python/3.12.5/python-3.12.5-macos11.pkg"
                pkg_file_path = tempfile.mktemp(suffix=".pkg")
                result = subprocess.run(["curl", "-o", pkg_file_path, url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)            
                if result.returncode == 0:
                    subprocess.run(["open", pkg_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                    print(f"Python installer has been executed: {pkg_file_path}")
                else:
                    print("Failed to download Python installer.")
            elif ma_os == "Windows":
                url = "https://www.python.org/ftp/python/3.12.5/python-3.12.5.exe"
                exe_file_path = tempfile.mktemp(suffix=".exe")
                result = subprocess.run(["curl", "-o", exe_file_path, url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)            
                if result.returncode == 0:
                    subprocess.run(["open", exe_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                    print(f"Python installer has been executed: {exe_file_path}")
                else:
                    print("Failed to download Python installer.")
    pip().install(["pypresence"])
    import pypresence
    import logging
    import warnings
    import time
    import uuid
    import sys
    import sys
    import threading

def suppress_hook():
    logging.getLogger("asyncio").setLevel(logging.ERROR)
    def a():
        return
    sys.__excepthook__ = a
    warnings.simplefilter("ignore", ResourceWarning)

class Presence(pypresence.Presence):
    connected = False
    discord_session_connected = False
    current_presence = None
    main_thread = None
    stop_event = None
    current_loop_id = None

    def __init__(self, *args, **kwargs):
        self.presence_class = super()
        self.presence_class.__init__(*args, **kwargs)
    def connect(self):
        if self.connected == False:
            def create_connection():
                try:
                    self.presence_class.connect()
                    self.stop_event = threading.Event()
                    suppress_hook()

                    def loop():
                        err_count = 0
                        while not self.stop_event.is_set():
                            if not self:
                                break
                            if self.connected == False:
                                break
                            try:
                                if self.connected == True:
                                    if self.current_presence:
                                        self.presence_class.update(**(self.current_presence))
                                    else:
                                        self.presence_class.clear()
                                else:
                                    break
                            except Exception as e:
                                err_count += 1
                            time.sleep(4.5)
                    self.main_thread = threading.Thread(target=loop, daemon=True)
                    self.main_thread.start()
                    self.discord_session_connected = True
                except Exception as e:
                    # Discord may not be open, await opening loop.
                    if self.connected == True:
                        time.sleep(0.5)
                        create_connection()
            threading.Thread(target=create_connection, daemon=True).start()
            self.connected = True
            return {"success": True, "code": 0}
        else:
            return {"success": True, "code": 1}
    def generate_loop_key(self):
        self.current_loop_id = str(uuid.uuid4())
        return self.current_loop_id
    def update(self, *args, **kwargs):
        if self.connected == True:
            if self.current_loop_id:
                if not (self.current_loop_id == kwargs.get("loop_key", "")):
                    return {"success": False, "code": 2}
                else:
                    if kwargs.get("loop_key"): kwargs.pop("loop_key")
            self.current_presence = kwargs
            return {"success": True, "code": 0}
        else:
            return {"success": False, "code": 1}
    def close(self):
        if self.connected == True:
            self.connected = False
            if self.discord_session_connected == True: 
                if self.stop_event: self.stop_event.set()
                if self.main_thread: self.main_thread.join()
                self.presence_class.close()
            self.current_presence = None
            self.current_loop_id = None
            return {"success": True, "code": 0}
        else:
            return {"success": False, "code": 1}
    def clear(self, *args, **kwargs):
        if self.connected == True:
            if self.discord_session_connected == True: self.presence_class.clear(*args, **kwargs)
            self.current_presence = None
            self.current_loop_id = None
            return {"success": True, "code": 0}
        else:
            return {"success": False, "code": 1}