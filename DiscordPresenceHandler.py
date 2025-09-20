# Modules
import sys

try:
    import pypresence
    import logging
    import warnings
    import time
    import platform
    import uuid
    import sys
    import threading
    import PyKits
except Exception as e:
    import PyKits
    pypresence = PyKits.pip().importModule("pypresence", install_module_if_not_found=True)
    import logging
    import warnings
    import time
    import platform
    import uuid
    import sys
    import threading

main_os = platform.system()
pip_class = PyKits.pip()
colors_class = PyKits.Colors()

def suppress_hook():
    logging.getLogger("asyncio").setLevel(logging.CRITICAL)
    def a(): return
    sys.__excepthook__ = a
    warnings.simplefilter("ignore", ResourceWarning)

def ts(mes):
    mes = str(mes)
    if hasattr(sys.stdout, "translate"): mes = sys.stdout.translate(mes)
    return mes
def printMainMessage(mes): print(colors_class.wrap(ts(mes), 255))
def printErrorMessage(mes): print(colors_class.wrap(ts(mes), 196))
def printSuccessMessage(mes): print(colors_class.wrap(ts(mes), 82))
def printWarnMessage(mes): print(colors_class.wrap(ts(mes), 202))
def printYellowMessage(mes): print(colors_class.wrap(ts(mes), 226))

class Presence(pypresence.Presence):
    connected = False
    discord_session_connected = False
    current_presence = None
    main_thread = None
    stop_event = None
    debug_mode = False
    current_loop_id = None
    default_presence = None

    def __init__(self, *args, **kwargs): super(Presence, self).__init__(*args, **kwargs)
    def get_if_discord_opened(self):
        if main_os == "Darwin":
            if pip_class.getIfProcessIsOpened("Discord Helper") or pip_class.getIfProcessIsOpened("Discord PTB Helper") or pip_class.getIfProcessIsOpened("Discord Canary Helper"): return True
        elif main_os == "Windows":
            if pip_class.getIfProcessIsOpened("Discord.exe") or pip_class.getIfProcessIsOpened("DiscordPTB.exe") or pip_class.getIfProcessIsOpened("DiscordCanary.exe"): return True
        else:
            if pip_class.getIfProcessIsOpened("Discord"): return True
        return False
    def connect(self):
        if self.connected == False:
            def create_connection():
                try:
                    super(Presence, self).connect()
                    self.stop_event = threading.Event()
                    suppress_hook()
                    self.printDebugMessage(f"Started Discord Presence!")

                    def loop():
                        try:
                            while not self.stop_event.is_set():
                                if not (self.connected == True): break
                                if self.get_if_discord_opened():
                                    if self.discord_session_connected == False:
                                        def connect_attempt():
                                            try:
                                                while True:
                                                    if self.get_if_discord_opened() == True:
                                                        super(Presence, self).connect()
                                                        self.printDebugMessage(f"Reactivated Discord Presence!")
                                                        break
                                                    else: time.sleep(2)
                                            except Exception as e:
                                                self.printDebugMessage(f"Connection may be broken. Error: {str(e)}")
                                                time.sleep(2)
                                                connect_attempt()
                                        connect_attempt()
                                    self.discord_session_connected = True
                                    try:
                                        if self.connected == True:
                                            if self.current_presence: super(Presence, self).update(**(self.current_presence))
                                            else: super(Presence, self).clear()
                                    except Exception as e: pass
                                else:
                                    if self.discord_session_connected == True: self.printDebugMessage(f"Deactivated Discord Presence!")
                                    self.discord_session_connected = False
                                time.sleep(4.5)
                        except Exception as e:
                            self.printDebugMessage(f"Unable to connect to Discord (2)! Error: {str(e)}")
                            self.discord_session_connected = False
                            try: self.close()
                            except Exception as e: pass
                    self.main_thread = threading.Thread(target=loop, daemon=True)
                    self.main_thread.start()
                except Exception as e:
                    # Discord may not be open, await opening loop.
                    if not type(e) is pypresence.DiscordNotFound and not type(e) is ConnectionRefusedError: self.printDebugMessage(f"Unable to connect to Discord (1)! Error: {str(e)}")
                    if self.connected == True:
                        while (self.get_if_discord_opened() == False and self.connected == True): time.sleep(0.5)
                        if self.connected == True: create_connection()
            self.connected = True
            threading.Thread(target=create_connection, daemon=True).start()
            return {"success": True, "code": 0}
        else: return {"success": True, "code": 1}
    def generate_loop_key(self):
        self.current_loop_id = str(uuid.uuid4())
        self.printDebugMessage(f"[generate_loop_key()]: Loop key is generated! Key: {self.current_loop_id}")
        return self.current_loop_id
    def set_debug_mode(self, enabled: bool):
        self.debug_mode = enabled==True
        self.printDebugMessage(f"[set_debug_mode()]: Debug Mode is enabled!")
    def update(self, *args, **kwargs):
        if self.connected == True:
            if self.current_loop_id:
                if not (self.current_loop_id == kwargs.get("loop_key", "")): return {"success": False, "code": 2}
                else:
                    if kwargs.get("loop_key"): kwargs.pop("loop_key")
            self.current_presence = kwargs
            return {"success": True, "code": 0}
        else: return {"success": False, "code": 1}
    def close(self):
        if self.connected == True:
            self.connected = False
            if self.stop_event: self.stop_event.set()
            if self.main_thread: self.main_thread.join()
            if self.discord_session_connected == True: 
                try:
                    super(Presence, self).close()
                    self.discord_session_connected = False
                    self.printDebugMessage(f"[close()]: Closed Discord Presence!")
                except Exception as e: self.printDebugMessage(f"[close()]: Unable to close to Discord! Error: {str(e)}")
                
            self.current_presence = None
            self.current_loop_id = None
            return {"success": True, "code": 0}
        else: return {"success": False, "code": 1}
    def clear(self, *args, **kwargs):
        if self.connected == True:
            if self.discord_session_connected == True: super(Presence, self).clear(*args, **kwargs)
            self.current_presence = self.default_presence
            self.current_loop_id = None
            return {"success": True, "code": 0}
        else: return {"success": False, "code": 1}
    def presence_class(self): return super(Presence, self)
    def printDebugMessage(self, mes):
        if self.debug_mode == True: print(colors_class.wrap(f"[Discord Presence] [DEBUG]: {ts(mes)}", 226))