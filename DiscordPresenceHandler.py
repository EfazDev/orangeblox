try:
    import pypresence
    import logging
    import warnings
    import time
    import platform
    import uuid
    import sys
    import threading
    from PipHandler import pip
except Exception as e:
    from PipHandler import pip
    pip().install(["pypresence"])
    import pypresence
    import logging
    import warnings
    import time
    import platform
    import uuid
    import sys
    import threading

main_os = platform.system()
pip_class = pip()

def suppress_hook():
    logging.getLogger("asyncio").setLevel(logging.CRITICAL)
    def a():
        return
    sys.__excepthook__ = a
    warnings.simplefilter("ignore", ResourceWarning)

def printMainMessage(mes): print(f"\033[38;5;255m{mes}\033[0m")
def printErrorMessage(mes): print(f"\033[38;5;196m{mes}\033[0m")
def printSuccessMessage(mes): print(f"\033[38;5;82m{mes}\033[0m")
def printWarnMessage(mes): print(f"\033[38;5;202m{mes}\033[0m")
def printYellowMessage(mes): print(f"\033[38;5;226m{mes}\033[0m")

class Presence(pypresence.Presence):
    connected = False
    discord_session_connected = False
    current_presence = None
    main_thread = None
    stop_event = None
    debug_mode = False
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
                    self.printDebugMode(f"[Connection Handler]: Started Discord Presence!")

                    def loop():
                        try:
                            while not self.stop_event.is_set():
                                if not self:
                                    break
                                if not (self.connected == True):
                                    break

                                is_closed = True
                                if main_os == "Darwin":
                                    if pip_class.getIfProcessIsOpened("Discord Helper (Plugin).app"): is_closed = False
                                elif main_os == "Windows":
                                    if pip_class.getIfProcessIsOpened("Discord.exe"): is_closed = False
                                else:
                                    if pip_class.getIfProcessIsOpened("Discord"): is_closed = False
                                if is_closed == False:
                                    if self.discord_session_connected == False:
                                        try:
                                            self.presence_class.connect()
                                            self.printDebugMode(f"[Connection Handler]: Reactivated Discord Presence!")
                                        except Exception as e:
                                            def connect_attempt():
                                                try:
                                                    self.presence_class.connect()
                                                    self.printDebugMode(f"[Connection Handler]: Reactivated Discord Presence!")
                                                except Exception as e:
                                                    self.printDebugMode(f"[Connection Handler]: Connection may be broken. Error: {str(e)}")
                                                    time.sleep(2)
                                                    connect_attempt()
                                            connect_attempt()
                                    self.discord_session_connected = True
                                    try:
                                        if self.connected == True:
                                            if self.current_presence:
                                                self.presence_class.update(**(self.current_presence))
                                            else:
                                                self.presence_class.clear()
                                    except:
                                        random_variable = 0
                                else:
                                    if self.discord_session_connected == True:
                                        self.printDebugMode(f"[Connection Handler]: Deactivated Discord Presence!")
                                    self.discord_session_connected = False
                                time.sleep(4.5)
                        except Exception as e:
                            self.printDebugMode(f"[Connection Handler]: Unable to connect to Discord! Error: {str(e)}")
                            self.discord_session_connected = False
                            try:
                                self.close()
                            except:
                                random_variable = 1
                    self.main_thread = threading.Thread(target=loop, daemon=True)
                    self.main_thread.start()
                except Exception as e:
                    # Discord may not be open, await opening loop.
                    if self.connected == True:
                        if main_os == "Darwin":
                            while (pip_class.getIfProcessIsOpened("Discord Helper (Plugin).app") == False and self.connected == True):
                                time.sleep(0.5)
                        elif main_os == "Windows":
                            while (pip_class.getIfProcessIsOpened("Discord.exe") == False and self.connected == True):
                                time.sleep(0.5)
                        else:
                            while (pip_class.getIfProcessIsOpened("Discord") == False and self.connected == True):
                                time.sleep(0.5)
                        if self.connected == True:
                            try:
                                create_connection()
                            except Exception as e:
                                self.printDebugMode(f"[Connection Handler]: Unable to connect to Discord! Error: {str(e)}")
            threading.Thread(target=create_connection, daemon=True).start()
            self.connected = True
            return {"success": True, "code": 0}
        else:
            return {"success": True, "code": 1}
    def generate_loop_key(self):
        self.current_loop_id = str(uuid.uuid4())
        self.printDebugMode(f"[generate_loop_key()]: Loop key is generated! Key: {self.current_loop_id}")
        return self.current_loop_id
    def set_debug_mode(self, enabled: bool):
        self.debug_mode = enabled==True
        self.printDebugMode(f"[set_debug_mode()]: Debug Mode is enabled!")
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
            if self.stop_event: self.stop_event.set()
            if self.main_thread: self.main_thread.join()
            if self.discord_session_connected == True: 
                try:
                    self.presence_class.close()
                    self.discord_session_connected = False
                    self.printDebugMode(f"[close()]: Closed Discord Presence!")
                except Exception as e:
                    self.printDebugMode(f"[close()]: Unable to close to Discord! Error: {str(e)}")
                
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
    def printDebugMode(self, mes):
        if self.debug_mode == True: print(f"\033[38;5;226m[Discord Presence] [DEBUG]: {mes}\033[0m")