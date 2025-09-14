# 
# Roblox Fast Flags Installer
# Made by Efaz from efaz.dev
# v2.3.9
# 
# Fulfill your Roblox needs and configuration through Python!
# 

import os
import re
import sys
import json
import time
import zlib
import shutil
import typing
import hashlib
import asyncio
import platform
import datetime
import threading
import subprocess
import urllib.parse
import xml.dom.minidom
import concurrent.futures
import xml.etree.ElementTree as ET

main_os = platform.system()
cur_path = os.path.dirname(os.path.abspath(__file__))
user_folder = (os.path.expanduser("~") if main_os == "Darwin" else os.getenv('LOCALAPPDATA'))
orangeblox_mode = False
script_version = "2.3.9"
def getLocalAppData():
    import platform
    import os
    ma_os = platform.system()
    if ma_os == "Windows": return os.path.expandvars(r'%LOCALAPPDATA%')
    elif ma_os == "Darwin": return f'{os.path.expanduser("~")}/Library/'
    else: return f'{os.path.expanduser("~")}/'
def getUserFolder():
    import platform
    import os
    ma_os = platform.system()
    if ma_os == "Windows": return os.path.basename(os.path.basename(os.path.expandvars(r'%LOCALAPPDATA%')))
    else: return os.path.expanduser("~")
def getIfLoggedInIsMacOSAdmin():
    import subprocess
    import platform
    import os
    ma_os = platform.system()
    if ma_os == "Darwin":
        logged_in_folder = getUserFolder()
        username = os.path.basename(logged_in_folder)
        groups_res = subprocess.run(["/usr/bin/groups", username], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if groups_res.returncode == 0: return "admin" in groups_res.stdout.decode("utf-8").split(" ")
        else: return False
    else: return False
def getInstallableApplicationsFolder():
    import platform
    import os
    ma_os = platform.system()
    if ma_os == "Darwin":
        if getIfLoggedInIsMacOSAdmin(): return os.path.join("/", "Applications")
        else: return os.path.join(getUserFolder(), "Applications")
    elif ma_os == "Windows": return getLocalAppData()

# Customizable Variables
macOS_dir = os.path.join(getInstallableApplicationsFolder(), "Roblox.app")  # This is Roblox macOS path
macOS_studioDir = os.path.join(getInstallableApplicationsFolder(), "RobloxStudio.app")  # This is Roblox macOS path
macOS_beforeClientServices = os.path.join("Contents", "MacOS") # This is a partial path for the executables are located for macOS Roblox, do not edit
macOS_installedPath = os.path.join(getInstallableApplicationsFolder()) # This is where Roblox is installed on macOS
windows_dir = os.path.join(os.getenv('LOCALAPPDATA') if os.getenv('LOCALAPPDATA') else "", "Roblox") # This is the Roblox folder in Windows App Data
windows_versions_dir = os.path.join(windows_dir, "Versions") # This is the Roblox versions folder path
windows_player_folder_name = "" # This is the version folder name for Roblox Player
windows_studio_folder_name = "" # This is the version folder name for Roblox Studio
submit_status = None # This is a SubmitStatus handler class used for alerting status of functions.
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
        "onSaveRobloxChannel",
        "onUserLogin",
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
        "onJoiningTeam",
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
        "onGameLoaded",
        "onLostConnection",
        "onWatchdogReconnection",
        "onTeamCreateConnect",
        "onTeamCreateDisconnect",
        "onCloudPlugins",
        "onPluginUnloading",
        "onRobloxSaved",
        "onNewStudioLaunching",
        "onStudioInstallerLaunched"
    ]
else: robloxInstanceTotalLiteralEventNames = typing.Union[str, bytes]
# Typing Literals

def ts(mes):
    mes = str(mes)
    if hasattr(sys.stdout, "translate"): mes = sys.stdout.translate(mes)
    return mes
def printMainMessage(mes):  print(f"\033[38;5;255m{ts(mes)}\033[0m")
def printErrorMessage(mes): print(f"\033[38;5;196m{ts(mes)}\033[0m")
def printSuccessMessage(mes): print(f"\033[38;5;82m{ts(mes)}\033[0m")
def printWarnMessage(mes): print(f"\033[38;5;202m{ts(mes)}\033[0m")
def printYellowMessage(mes): print(f"\033[38;5;226m{ts(mes)}\033[0m")
def printDebugMessage(mes): print(f"\033[38;5;226m[Roblox FFlag Installer] [DEBUG]: {ts(mes)}\033[0m")
def isYes(text): return text.lower() == "y" or text.lower() == "yes" or text.lower() == "true" or text.lower() == "t"
def isNo(text): return text.lower() == "n" or text.lower() == "no" or text.lower() == "false" or text.lower() == "f"
def isRequestClose(text): return text.lower() == "exit" or text.lower() == "exit()"
def printLog(mes): 
    if __name__ == "__main__": printMainMessage(mes)
    else: print(mes)
def makedirs(a): os.makedirs(a,exist_ok=True)

class request:
    class Response:
        text: str = ""
        json: typing.Union[typing.Dict, typing.List, None] = None
        ipv4: typing.List[str] = []
        ipv6: typing.List[str] = []
        redirected_urls: typing.List[str] = []
        port: int = 0
        host: str = ""
        attempted_ip: str = ""
        status_code: int = 0
        ssl_verified: bool = False
        ssl_issuer: str = ""
        ssl_subject: str = ""
        tls_version: str = ""
        headers: typing.Dict[str, str] = {}
        http_version: str = ""
        path: str = ""
        url: str = ""
        method: str = ""
        scheme: str = ""
        redirected: bool = False
        ok: bool = False
    class FileDownload(Response):
        returncode = 0
        path = ""
    class TimedOut(Exception):
        def __init__(self, url: str, time: float): super().__init__(f"Connecting to URL ({url}) took too long to respond in {time}s!")
    class ProcessError(Exception):
        def __init__(self, url: str, exception: Exception): super().__init__(f"Something went wrong connecting to URL ({url})! This was a problem created by subprocess. Exception: {str(exception)}")
    class UnknownResponse(Exception):
        def __init__(self, url: str, exception: Exception): super().__init__(f"Something went wrong processing the response from URL ({url})! Exception: {str(exception)}")
    class OpenContext:
        val = None
        def __init__(self, val): self.val = val
        def __enter__(self): return self.val
        def __exit__(self, exc_type, exc_val, exc_tb): pass
    class DownloadStatus:
        speed: str=""
        downloaded: str=""
        downloaded_bytes: int=0
        total_size: str=""
        percent: int=0
        def __init__(self, percent: int=0, speed: str="", total_size: str="", downloaded: str="", downloaded_bytes: int=0): self.speed = speed; self.downloaded = downloaded; self.percent = percent; self.downloaded_bytes = downloaded_bytes; self.total_size = total_size
    __DATA__ = typing.Union[typing.Dict, typing.List, str]
    __AUTH__ = typing.List[str]
    __HEADERS__ = typing.Dict[str, str]
    __COOKIES__ = typing.Union[typing.Dict[str, str], str]
    def __init__(self):
        import subprocess
        import json
        import os
        import re
        import shutil
        import time
        import socket
        import threading
        import urllib.request
        from urllib.parse import urlparse
        import platform
        self._subprocess = subprocess
        self._json = json
        self._os = os
        self._re = re
        self._shutil = shutil
        self._socket = socket
        self._time = time
        self._threading = threading
        self._urlreq = urllib.request
        self._urlparse = urlparse
        self._platform = platform
        self._main_os = platform.system()
    def get(self, url: str, headers: __HEADERS__={}, cookies: __COOKIES__={}, auth: __AUTH__=[], timeout: float=30.0, follow_redirects: bool=False, loop_429: bool=False, loop_count: int=-1, loop_timeout: int=1) -> Response:
        try:
            if not self.get_if_connected():
                while not self.get_if_connected(): self._time.sleep(0.5)
            curl_res = self._subprocess.run([self.get_curl(), "-v", "--compressed"] + self.format_headers(headers) + self.format_auth(auth) + self.format_cookies(cookies) + [url], stdout=self._subprocess.PIPE, stderr=self._subprocess.PIPE, timeout=timeout)
            if type(curl_res) is self._subprocess.CompletedProcess:
                new_response = self.Response()
                processed_stderr = self.process_stderr(curl_res.stderr.decode("utf-8").replace("\r", ""))
                for i, v in processed_stderr.items(): setattr(new_response, i, v)
                new_response.url = url
                new_response.text = curl_res.stdout.decode("utf-8").replace("\r", "")
                new_response.method = "GET"
                new_response.scheme = self.get_url_scheme(url)
                new_response.path = self.get_url_path(url)
                new_response.redirected_urls = [url]
                try: new_response.json = self._json.loads(new_response.text)
                except Exception as e: pass
                if self.get_if_redirect(new_response.status_code) and follow_redirects == True and new_response.headers.get("location"): 
                    req = self.get(new_response.headers.get("location"), headers=headers, cookies=cookies, auth=auth, timeout=timeout, follow_redirects=True, loop_429=loop_429, loop_count=loop_count)
                    req.redirected = True
                    req.redirected_urls = [url] + req.redirected_urls
                    return req
                elif self.get_if_cooldown(new_response.status_code) and loop_429 == True and ((1 if loop_count == -1 else loop_count) >= 1):
                    self._time.sleep(loop_timeout)
                    return self.get(url, headers=headers, cookies=cookies, auth=auth, timeout=timeout, follow_redirects=True, loop_429=loop_429, loop_count=(loop_count-1 if not (loop_count == -1) else loop_count))
                return new_response
            elif type(curl_res) is self._subprocess.TimeoutExpired: raise self.TimedOut(url, timeout)
            elif type(curl_res) is self._subprocess.SubprocessError: raise self.ProcessError(url, curl_res)
            else: raise self.UnknownResponse(url, curl_res)
        except self._subprocess.TimeoutExpired: raise self.TimedOut(url, timeout)
        except self._subprocess.SubprocessError as curl_res: raise self.ProcessError(url, curl_res)
        except Exception as e: raise self.UnknownResponse(url, e)
    def post(self, url: str, data: __DATA__, headers: __HEADERS__={}, cookies: __COOKIES__={}, auth: __AUTH__=[], timeout: float=30.0, follow_redirects: bool=False, loop_429: bool=False, loop_count: int=-1, loop_timeout: int=1) -> Response:
        try:
            if not self.get_if_connected():
                while not self.get_if_connected(): self._time.sleep(0.5)
            curl_res = self._subprocess.run([self.get_curl(), "-v", "-X", "POST", "--compressed"] + self.format_headers(headers) + self.format_auth(auth) + self.format_cookies(cookies) + self.format_data(data) + [url], stdout=self._subprocess.PIPE, stderr=self._subprocess.PIPE, timeout=timeout)
            if type(curl_res) is self._subprocess.CompletedProcess:
                new_response = self.Response()
                processed_stderr = self.process_stderr(curl_res.stderr.decode("utf-8").replace("\r", ""))
                for i, v in processed_stderr.items(): setattr(new_response, i, v)
                new_response.url = url
                new_response.text = curl_res.stdout.decode("utf-8").replace("\r", "")
                new_response.method = "POST"
                new_response.scheme = self.get_url_scheme(url)
                new_response.path = self.get_url_path(url)
                new_response.redirected_urls = [url]
                try: new_response.json = self._json.loads(new_response.text)
                except Exception as e: pass
                if self.get_if_redirect(new_response.status_code) and follow_redirects == True and new_response.headers.get("location"): 
                    req = self.post(new_response.headers.get("location"), data, headers=headers, cookies=cookies, auth=auth, timeout=timeout, follow_redirects=True, loop_429=loop_429, loop_count=loop_count)
                    req.redirected = True
                    req.redirected_urls = [url] + req.redirected_urls
                    return req
                elif self.get_if_cooldown(new_response.status_code) and loop_429 == True and ((1 if loop_count == -1 else loop_count) >= 1):
                    self._time.sleep(loop_timeout)
                    return self.post(url, data, headers=headers, cookies=cookies, auth=auth, timeout=timeout, follow_redirects=True, loop_429=loop_429, loop_count=(loop_count-1 if not (loop_count == -1) else loop_count))
                return new_response
            elif type(curl_res) is self._subprocess.TimeoutExpired: raise self.TimedOut(url, timeout)
            elif type(curl_res) is self._subprocess.SubprocessError: raise self.ProcessError(url, curl_res)
            else: raise self.UnknownResponse(url, curl_res)
        except self._subprocess.TimeoutExpired: raise self.TimedOut(url, timeout)
        except self._subprocess.SubprocessError as curl_res: raise self.ProcessError(url, curl_res)
        except Exception as e: raise self.UnknownResponse(url, e)
    def patch(self, url: str, data: __DATA__, headers: __HEADERS__={}, cookies: __COOKIES__={}, auth: __AUTH__=[], timeout: float=30.0, follow_redirects: bool=False, loop_429: bool=False, loop_count: int=-1, loop_timeout: int=1) -> Response:
        try:
            if not self.get_if_connected():
                while not self.get_if_connected(): self._time.sleep(0.5)
            curl_res = self._subprocess.run([self.get_curl(), "-v", "-X", "PATCH", "--compressed"] + self.format_headers(headers) + self.format_auth(auth) + self.format_cookies(cookies) + self.format_data(data) + [url], stdout=self._subprocess.PIPE, stderr=self._subprocess.PIPE, timeout=timeout)
            if type(curl_res) is self._subprocess.CompletedProcess:
                new_response = self.Response()
                processed_stderr = self.process_stderr(curl_res.stderr.decode("utf-8").replace("\r", ""))
                for i, v in processed_stderr.items(): setattr(new_response, i, v)
                new_response.url = url
                new_response.text = curl_res.stdout.decode("utf-8").replace("\r", "")
                new_response.method = "PATCH"
                new_response.scheme = self.get_url_scheme(url)
                new_response.path = self.get_url_path(url)
                new_response.redirected_urls = [url]
                try: new_response.json = self._json.loads(new_response.text)
                except Exception as e: pass
                if self.get_if_redirect(new_response.status_code) and follow_redirects == True and new_response.headers.get("location"): 
                    req = self.patch(new_response.headers.get("location"), data, headers=headers, cookies=cookies, auth=auth, timeout=timeout, follow_redirects=True, loop_429=loop_429, loop_count=loop_count)
                    req.redirected = True
                    req.redirected_urls = [url] + req.redirected_urls
                    return req
                elif self.get_if_cooldown(new_response.status_code) and loop_429 == True and ((1 if loop_count == -1 else loop_count) >= 1):
                    self._time.sleep(loop_timeout)
                    return self.patch(url, data, headers=headers, cookies=cookies, auth=auth, timeout=timeout, follow_redirects=True, loop_429=loop_429, loop_count=(loop_count-1 if not (loop_count == -1) else loop_count))
                return new_response
            elif type(curl_res) is self._subprocess.TimeoutExpired: raise self.TimedOut(url, timeout)
            elif type(curl_res) is self._subprocess.SubprocessError: raise self.ProcessError(url, curl_res)
            else: raise self.UnknownResponse(url, curl_res)
        except self._subprocess.TimeoutExpired: raise self.TimedOut(url, timeout)
        except self._subprocess.SubprocessError as curl_res: raise self.ProcessError(url, curl_res)
        except Exception as e: raise self.UnknownResponse(url, e)
    def put(self, url: str, data: __DATA__, headers: __HEADERS__={}, cookies: __COOKIES__={}, auth: __AUTH__=[], timeout: float=30.0, follow_redirects: bool=False, loop_429: bool=False, loop_count: int=-1, loop_timeout: int=1) -> Response:
        try:
            if not self.get_if_connected():
                while not self.get_if_connected(): self._time.sleep(0.5)
            curl_res = self._subprocess.run([self.get_curl(), "-v", "-X", "PUT", "--compressed"] + self.format_headers(headers) + self.format_auth(auth) + self.format_cookies(cookies) + self.format_data(data) + [url], stdout=self._subprocess.PIPE, stderr=self._subprocess.PIPE, timeout=timeout)
            if type(curl_res) is self._subprocess.CompletedProcess:
                new_response = self.Response()
                processed_stderr = self.process_stderr(curl_res.stderr.decode("utf-8").replace("\r", ""))
                for i, v in processed_stderr.items(): setattr(new_response, i, v)
                new_response.url = url
                new_response.text = curl_res.stdout.decode("utf-8").replace("\r", "")
                new_response.method = "PUT"
                new_response.scheme = self.get_url_scheme(url)
                new_response.path = self.get_url_path(url)
                new_response.redirected_urls = [url]
                try: new_response.json = self._json.loads(new_response.text)
                except Exception as e: pass
                if self.get_if_redirect(new_response.status_code) and follow_redirects == True and new_response.headers.get("location"):
                    req = self.put(new_response.headers.get("location"), data, headers=headers, cookies=cookies, auth=auth, timeout=timeout, follow_redirects=True, loop_429=loop_429, loop_count=loop_count)
                    req.redirected = True
                    req.redirected_urls = [url] + req.redirected_urls
                    return req
                elif self.get_if_cooldown(new_response.status_code) and loop_429 == True and ((1 if loop_count == -1 else loop_count) >= 1):
                    self._time.sleep(loop_timeout)
                    return self.put(url, data, headers=headers, cookies=cookies, auth=auth, timeout=timeout, follow_redirects=True, loop_429=loop_429, loop_count=(loop_count-1 if not (loop_count == -1) else loop_count))
                return new_response
            elif type(curl_res) is self._subprocess.TimeoutExpired: raise self.TimedOut(url, timeout)
            elif type(curl_res) is self._subprocess.SubprocessError: raise self.ProcessError(url, curl_res)
            else: raise self.UnknownResponse(url, curl_res)
        except self._subprocess.TimeoutExpired: raise self.TimedOut(url, timeout)
        except self._subprocess.SubprocessError as curl_res: raise self.ProcessError(url, curl_res)
        except Exception as e: raise self.UnknownResponse(url, e)
    def delete(self, url: str, headers: __HEADERS__={}, cookies: __COOKIES__={}, auth: __AUTH__=[], timeout: float=30.0, follow_redirects: bool=False, loop_429: bool=False, loop_count: int=-1, loop_timeout: int=1) -> Response:
        try:
            if not self.get_if_connected():
                while not self.get_if_connected(): self._time.sleep(0.5)
            curl_res = self._subprocess.run([self.get_curl(), "-v", "-X", "DELETE", "--compressed"] + self.format_headers(headers) + self.format_auth(auth) + self.format_cookies(cookies) + [url], stdout=self._subprocess.PIPE, stderr=self._subprocess.PIPE, timeout=timeout)
            if type(curl_res) is self._subprocess.CompletedProcess:
                new_response = self.Response()
                processed_stderr = self.process_stderr(curl_res.stderr.decode("utf-8").replace("\r", ""))
                for i, v in processed_stderr.items(): setattr(new_response, i, v)
                new_response.url = url
                new_response.text = curl_res.stdout.decode("utf-8").replace("\r", "")
                new_response.method = "DELETE"
                new_response.scheme = self.get_url_scheme(url)
                new_response.path = self.get_url_path(url)
                new_response.redirected_urls = [url]
                try: new_response.json = self._json.loads(new_response.text)
                except Exception as e: pass
                if self.get_if_redirect(new_response.status_code) and follow_redirects == True and new_response.headers.get("location"): 
                    req = self.delete(new_response.headers.get("location"), headers=headers, cookies=cookies, auth=auth, timeout=timeout, follow_redirects=True, loop_429=loop_429, loop_count=loop_count)
                    req.redirected = True
                    req.redirected_urls = [url] + req.redirected_urls
                    return req
                elif self.get_if_cooldown(new_response.status_code) and loop_429 == True and ((1 if loop_count == -1 else loop_count) >= 1):
                    self._time.sleep(loop_timeout)
                    return self.delete(url, headers=headers, cookies=cookies, auth=auth, timeout=timeout, follow_redirects=True, loop_429=loop_429, loop_count=(loop_count-1 if not (loop_count == -1) else loop_count))
                return new_response
            elif type(curl_res) is self._subprocess.TimeoutExpired: raise self.TimedOut(url, timeout)
            elif type(curl_res) is self._subprocess.SubprocessError: raise self.ProcessError(url, curl_res)
            else: raise self.UnknownResponse(url, curl_res)
        except self._subprocess.TimeoutExpired: raise self.TimedOut(url, timeout)
        except self._subprocess.SubprocessError as curl_res: raise self.ProcessError(url, curl_res)
        except Exception as e: raise self.UnknownResponse(url, e)
    def head(self, url: str, headers: __HEADERS__={}, cookies: __COOKIES__={}, auth: __AUTH__=[], timeout: float=30.0, follow_redirects: bool=False, loop_429: bool=False, loop_count: int=-1, loop_timeout: int=1) -> Response:
        try:
            if not self.get_if_connected():
                while not self.get_if_connected(): self._time.sleep(0.5)
            curl_res = self._subprocess.run([self.get_curl(), "-v", "-X", "HEAD", "--compressed"] + self.format_headers(headers) + self.format_auth(auth) + self.format_cookies(cookies) + [url], stdout=self._subprocess.PIPE, stderr=self._subprocess.PIPE, timeout=timeout)
            if type(curl_res) is self._subprocess.CompletedProcess:
                new_response = self.Response()
                processed_stderr = self.process_stderr(curl_res.stderr.decode("utf-8").replace("\r", ""))
                for i, v in processed_stderr.items(): setattr(new_response, i, v)
                new_response.url = url
                new_response.text = curl_res.stdout.decode("utf-8").replace("\r", "")
                new_response.method = "HEAD"
                new_response.scheme = self.get_url_scheme(url)
                new_response.path = self.get_url_path(url)
                new_response.redirected_urls = [url]
                try: new_response.json = self._json.loads(new_response.text)
                except Exception as e: pass
                if self.get_if_redirect(new_response.status_code) and follow_redirects == True and new_response.headers.get("location"): 
                    req = self.head(new_response.headers.get("location"), headers=headers, cookies=cookies, auth=auth, timeout=timeout, follow_redirects=True, loop_429=loop_429, loop_count=loop_count)
                    req.redirected = True
                    req.redirected_urls = [url] + req.redirected_urls
                    return req
                elif self.get_if_cooldown(new_response.status_code) and loop_429 == True and ((1 if loop_count == -1 else loop_count) >= 1):
                    self._time.sleep(loop_timeout)
                    return self.head(url, headers=headers, cookies=cookies, auth=auth, timeout=timeout, follow_redirects=True, loop_429=loop_429, loop_count=(loop_count-1 if not (loop_count == -1) else loop_count))
                return new_response
            elif type(curl_res) is self._subprocess.TimeoutExpired: raise self.TimedOut(url, timeout)
            elif type(curl_res) is self._subprocess.SubprocessError: raise self.ProcessError(url, curl_res)
            else: raise self.UnknownResponse(url, curl_res)
        except self._subprocess.TimeoutExpired: raise self.TimedOut(url, timeout)
        except self._subprocess.SubprocessError as curl_res: raise self.ProcessError(url, curl_res)
        except Exception as e: raise self.UnknownResponse(url, e)
    def custom(self, url: str, method: str, data: __DATA__, headers: __HEADERS__={}, cookies: __COOKIES__={}, auth: __AUTH__=[], timeout: float=30.0, follow_redirects: bool=False, loop_429: bool=False, loop_count: int=-1, loop_timeout: int=1) -> Response:
        try:
            if not self.get_if_connected():
                while not self.get_if_connected(): self._time.sleep(0.5)
            curl_res = self._subprocess.run([self.get_curl(), "-v", "-X", method, "--compressed"] + self.format_headers(headers) + self.format_auth(auth) + self.format_cookies(cookies) + self.format_data(data) + [url], stdout=self._subprocess.PIPE, stderr=self._subprocess.PIPE, timeout=timeout)
            if type(curl_res) is self._subprocess.CompletedProcess:
                new_response = self.Response()
                processed_stderr = self.process_stderr(curl_res.stderr.decode("utf-8").replace("\r", ""))
                for i, v in processed_stderr.items(): setattr(new_response, i, v)
                new_response.url = url
                new_response.text = curl_res.stdout.decode("utf-8").replace("\r", "")
                new_response.method = method.upper()
                new_response.scheme = self.get_url_scheme(url)
                new_response.path = self.get_url_path(url)
                new_response.redirected_urls = [url]
                try: new_response.json = self._json.loads(new_response.text)
                except Exception as e: pass
                if self.get_if_redirect(new_response.status_code) and follow_redirects == True and new_response.headers.get("location"): 
                    req = self.custom(new_response.headers.get("location"), method, data, headers=headers, cookies=cookies, auth=auth, timeout=timeout, follow_redirects=True, loop_429=loop_429, loop_count=loop_count)
                    req.redirected = True
                    req.redirected_urls = [url] + req.redirected_urls
                    return req
                elif self.get_if_cooldown(new_response.status_code) and loop_429 == True and ((1 if loop_count == -1 else loop_count) >= 1):
                    self._time.sleep(loop_timeout)
                    return self.custom(url, method, data, headers=headers, cookies=cookies, auth=auth, timeout=timeout, follow_redirects=True, loop_429=loop_429, loop_count=(loop_count-1 if not (loop_count == -1) else loop_count))
                return new_response
            elif type(curl_res) is self._subprocess.TimeoutExpired: raise self.TimedOut(url, timeout)
            elif type(curl_res) is self._subprocess.SubprocessError: raise self.ProcessError(url, curl_res)
            else: raise self.UnknownResponse(url, curl_res)
        except self._subprocess.TimeoutExpired: raise self.TimedOut(url, timeout)
        except self._subprocess.SubprocessError as curl_res: raise self.ProcessError(url, curl_res)
        except Exception as e: raise self.UnknownResponse(url, e)
    def open(self, *k, **s) -> OpenContext:
        mai = self.get(*k, **s)
        return self.OpenContext(mai)
    def download(self, path: str, output: str, check: bool=False, delete_existing: bool=True, submit_status=None) -> FileDownload:
        if not self.get_if_connected():
            while not self.get_if_connected(): self._time.sleep(0.5)
        if self._os.path.exists(output) and delete_existing == False: raise FileExistsError(f"This file already exists in {output}!")
        elif self._os.path.exists(output) and self._os.path.isdir(output): self._shutil.rmtree(output, ignore_errors=True)
        elif self._os.path.exists(output) and self._os.path.isfile(output): self._os.remove(output)
        download_proc = self._subprocess.Popen([self.get_curl(), "-v", "--progress-meter", "-L", "-o", output, path], shell=False, bufsize=1, universal_newlines=True, stderr=self._subprocess.PIPE, stdout=self._subprocess.PIPE)
        stderr_lines = []
        before_bytes = 0
        new_t = 0
        while True:
            line = download_proc.stderr.readline()
            if not line: break
            stderr_lines.append(line)
            if submit_status:
                stripped_line = line.lstrip()
                if stripped_line and stripped_line[0].isdigit():
                    progress = self.process_download_status(line)
                    if progress:
                        if progress.percent < 100:
                            def pro(tar_prog, before_bytes, target_t):
                                for i in range(100):
                                    byte_target = int(before_bytes+((tar_prog.downloaded_bytes-before_bytes)*((i+1)/100)))
                                    total_size_bytes = self.format_size_to_bytes(tar_prog.total_size)
                                    perc_target = int((byte_target/total_size_bytes)*100) if not (byte_target == 0 and total_size_bytes == 0) else 0
                                    if not (new_t == target_t): return
                                    submit_status.submit(self.DownloadStatus(percent=perc_target, total_size=tar_prog.total_size, speed=tar_prog.speed, downloaded_bytes=byte_target, downloaded=self.format_bytes_to_size(byte_target)))
                                    if not (new_t == target_t): return
                                    self._time.sleep(0.01)
                            new_t += 1
                            self._threading.Thread(target=pro, args=[progress, before_bytes, new_t], daemon=True).start()
                            before_bytes = progress.downloaded_bytes
                        elif before_bytes < self.format_size_to_bytes(progress.total_size):
                            new_t += 1
                            next_tar = self.format_size_to_bytes(progress.total_size)
                            for i in range(10):
                                byte_target = int(before_bytes+((next_tar-before_bytes)*((i+1)/10)))
                                total_size_bytes = self.format_size_to_bytes(progress.total_size)
                                perc_target = int((byte_target/total_size_bytes)*100) if not (byte_target == 0 and total_size_bytes == 0) else 0
                                submit_status.submit(self.DownloadStatus(percent=perc_target, total_size=progress.total_size, speed=progress.speed, downloaded_bytes=byte_target, downloaded=self.format_bytes_to_size(byte_target)))
                                self._time.sleep(0.01)
                            before_bytes = next_tar
                        else:
                            new_t += 1
                            before_bytes = progress.downloaded_bytes
                            submit_status.submit(progress)
        download_proc.wait() 
        if download_proc.returncode == 0: 
            s = self.FileDownload()
            s.returncode = 0
            s.path = output
            s.url = path
            s.method = "GET"
            s.scheme = self.get_url_scheme(path)
            s.path = self.get_url_path(path)
            processed_stderr = self.process_stderr("".join(stderr_lines))
            for i, v in processed_stderr.items(): setattr(s, i, v)
            return s
        else: 
            if check == True: raise Exception(f"Unable to download file at {path} with return code {download_proc.returncode}!")
            else: 
                s = self.FileDownload()
                s.returncode = download_proc.returncode
                s.path = None
                s.url = path
                s.method = "GET"
                s.scheme = self.get_url_scheme(path)
                s.path = self.get_url_path(path)
                processed_stderr = self.process_stderr("".join(stderr_lines))
                for i, v in processed_stderr.items(): setattr(s, i, v)
                return s
    def get_curl(self):
        pos_which = self._shutil.which("curl")
        if self._os.path.exists(pos_which): return pos_which
        elif self._main_os == "Windows" and self._os.path.exists(self._os.path.join(cur_path, "curl")): return self._os.path.join(cur_path, "curl", "curl.exe")
        elif self._os.path.exists(self._os.path.join(cur_path, "curl")): return self._os.path.join(cur_path, "curl", "curl")
        else: 
            cur_path = self._os.path.dirname(self._os.path.abspath(__file__))
            if self._main_os == "Darwin": return None
            elif self._main_os == "Windows":
                pip_class = pip()
                if self._platform.architecture()[0] == "32bit": self._urlreq.urlretrieve("https://curl.se/windows/latest.cgi?p=win32-mingw.zip", self._os.path.join(cur_path, "curl_download.zip"))
                else: self._urlreq.urlretrieve("https://curl.se/windows/latest.cgi?p=win64-mingw.zip", self._os.path.join(cur_path, "curl_download.zip"))
                if self._os.path.exists(self._os.path.join(cur_path, "curl_download.zip")):
                    unzip_res = pip_class.unzipFile(self._os.path.join(cur_path, "curl_download.zip"), self._os.path.join(cur_path, "curl"), ["curl.exe"])
                    if unzip_res.returncode == 0: return self._os.path.join(cur_path, "curl", "curl.exe")
                    else: return None 
                else: return None 
            else: return None
    def get_if_ok(self, code: int): return int(code) < 300 and int(code) >= 200
    def get_if_redirect(self, code: int): return int(code) < 400 and int(code) >= 300
    def get_if_cooldown(self, code: int): return int(code) == 429
    def get_if_connected(self):
        try: self._socket.create_connection(("8.8.8.8", 443), timeout=3).close(); return True # Connect to Google failed?
        except Exception as e: return False
    def get_url_scheme(self, url: str): 
        obj = self._urlparse(url)
        return obj.scheme
    def get_url_path(self, url: str):
        obj = self._urlparse(url)
        if obj.query == "": return obj.path
        else: return obj.path + "?" + obj.query
    def format_headers(self, headers: typing.Dict[str, str]={}):
        formatted = []
        for i, v in headers.items(): formatted.append("-H"); formatted.append(f"{i}: {v}")
        return formatted
    def format_cookies(self, cookies: typing.Union[typing.Dict[str, str], str]={}):
        if type(cookies) is str: return cookies
        else:
            formatted = []
            for i, v in cookies.items(): formatted.append("-b"); formatted.append(f"{i}={v}")
            return formatted
    def format_auth(self, auth: typing.List[str]):
        if len(auth) == 2: return ["-u", f"{auth[0]}:{auth[1]}"]
        else: return []
    def format_data(self, data: typing.Union[typing.Dict, typing.List, str]):
        is_json = False
        if type(data) is dict or type(data) is list: data = self._json.dumps(data); is_json = True
        if data: 
            if is_json == True: return ["-d", data, "-H", "Content-Type: application/json"]
            return ["-d", data]
        else: return []
    def format_params(self, data: typing.Dict[str, str]={}):
        mai_query = ""
        if len(data.keys()) > 0:
            mai_query = "?"
            for i, v in data.items(): mai_query = mai_query + f"{i}={v}"
        return mai_query
    def format_size_to_bytes(self, size_str: str):
        size_str = size_str.upper()
        try:
            if size_str.endswith("K") or size_str.endswith("k"): return int(float(size_str[:-1]) * 1024)
            if size_str.endswith("M"): return int(float(size_str[:-1]) * 1024**2)
            if size_str.endswith("G"): return int(float(size_str[:-1]) * 1024**3)
            if size_str.endswith("T"): return int(float(size_str[:-1]) * 1024**4)
            return int(size_str)
        except Exception: return 0
    def format_bytes_to_size(self, size_bytes: int):
        thresholds = [
            (1024**4, "T"),
            (1024**3, "G"),
            (1024**2, "M"),
            (1024, "k"),
        ]
        for factor, suffix in thresholds:
            if size_bytes >= factor:
                size = size_bytes / factor
                return f"{size:.1f}{suffix}"
        return str(size_bytes)
    def process_stderr(self, stderr: str):
        lines = stderr.split("\n")
        data = {
            "ipv4": [],
            "ipv6": [],
            "port": 0,
            "host": "",
            "attempted_ip": "",
            "status_code": 0,
            "ssl_verified": False,
            "ssl_issuer": "",
            "ssl_subject": "",
            "tls_version": "",
            "headers": {},
            "http_version": "",
            "ok": False
        }
        for i in lines:
            if self._main_os == "Windows": # Schannel based cUrl
                status_line_match = self._re.search(r"< HTTP/([\d.]+) (\d+)", i)
                if status_line_match:
                    data["http_version"] = status_line_match.group(1)
                    data["status_code"] = int(status_line_match.group(2))
                    data["ok"] = self.get_if_ok(data["status_code"])
                elif i.startswith("< "):
                    sl = i.replace("< ", "", 1).split(": ")
                    if len(sl) > 1: data["headers"][sl[0]] = sl[1]
                elif i == "* schannel: SSL/TLS connection renegotiated":
                    data["ssl_verified"] = True
                    data["ssl_issuer"] = "CN=Schannel Placeholder Certificate"
                    data["ssl_subject"] = f'CN={data["host"]}'
                    data["tls_version"] = "1.2"
                elif i.startswith("* IPv4: "):
                    sl = i.split("* IPv4: ")
                    if len(sl) > 1: 
                        sl.pop(0); data["ipv4"] = sl[0].split(", ")
                        if data["ipv4"][0] == "(none)": data["ipv4"] = []
                elif i.startswith("* IPv6: "):
                    sl = i.split("* IPv6: ")
                    if len(sl) > 1: 
                        sl.pop(0); data["ipv6"] = sl[0].split(", ")
                        if data["ipv6"][0] == "(none)": data["ipv6"] = []
                elif i.startswith("* Connected to ") and "port" in i:
                    sl = i.split("port ")
                    if len(sl) > 1: sl.pop(0); data["port"] = int(sl[0])
                    sl = i.split("Connected to ")
                    if len(sl) > 1: sl.pop(0); data["host"] = sl[0].split(" ")[0]
                    sl = i.split("(")
                    if len(sl) > 1: sl.pop(0); data["attempted_ip"] = sl[0].split(")")[0]
            else: # OpenSSL based cUrl
                status_line_match = self._re.search(r"< HTTP/([\d.]+) (\d+)", i)
                if status_line_match:
                    data["http_version"] = status_line_match.group(1)
                    data["status_code"] = int(status_line_match.group(2))
                    data["ok"] = self.get_if_ok(data["status_code"])
                elif i.startswith("< "):
                    sl = i.replace("< ", "", 1).split(": ")
                    if len(sl) > 1: data["headers"][sl[0]] = sl[1]
                elif i.startswith("* IPv4: "):
                    sl = i.split("* IPv4: ")
                    if len(sl) > 1: 
                        sl.pop(0); data["ipv4"] = sl[0].split(", ")
                        if data["ipv4"][0] == "(none)": data["ipv4"] = []
                elif i.startswith("* IPv6: "):
                    sl = i.split("* IPv6: ")
                    if len(sl) > 1: 
                        sl.pop(0); data["ipv6"] = sl[0].split(", ")
                        if data["ipv6"][0] == "(none)": data["ipv6"] = []
                elif i.startswith("* Connected to ") and "port" in i:
                    sl = i.split("port ")
                    if len(sl) > 1: sl.pop(0); data["port"] = int(sl[0])
                    sl = i.split("Connected to ")
                    if len(sl) > 1: sl.pop(0); data["host"] = sl[0].split(" ")[0]
                    sl = i.split("(")
                    if len(sl) > 1: sl.pop(0); data["attempted_ip"] = sl[0].split(")")[0]
                elif "SSL certificate verify ok." in i: data["ssl_verified"] = True
                elif "* SSL connection using TLSv" in i:
                    sl = i.split("* SSL connection using TLSv")
                    if len(sl) > 1: sl.pop(0); data["tls_version"] = sl[0].split(" /")[0]
                elif "*  issuer: " in i:
                    sl = i.split("*  issuer: ")
                    if len(sl) > 1: sl.pop(0); data["ssl_issuer"] = sl[0]
                elif "*  subject: " in i:
                    sl = i.split("*  subject: ")
                    if len(sl) > 1: sl.pop(0); data["ssl_subject"] = sl[0]
        return data
    def process_bytes_to_str(self, bytes: bytes): return bytes.decode("utf-8")
    def process_download_status(self, download_stat_line: str):
        pattern = self._re.compile(
            r"^\s*(\d{1,3})\s+"  # Percent
            r"(\S+)\s+"          # Total size
            r"\d{1,3}\s+"        # Percent downloaded
            r"(\S+)\s+"          # Downloaded size
            r"\S+\s+"            # Xferd percent
            r"\S+\s+"            # Xferd size
            r"\S+\s+"            # Avg Dload Speed
            r"\S+\s+"            # Avg Upload Speed
            r"\S+\s+"            # Total time
            r"\S+\s+"            # Time spent
            r"\S+\s+"            # Time left
            r"(\S+)\s*$"         # Current speed
        )
        match = pattern.search(download_stat_line)
        if match:
            percent = int(match.group(1))
            total_size = match.group(2)
            downloaded = match.group(3)
            speed = match.group(4)
            downloaded_bytes = self.format_size_to_bytes(downloaded)
            return self.DownloadStatus(speed=speed, downloaded=downloaded, downloaded_bytes=downloaded_bytes, percent=percent, total_size=total_size)
        return None
class pip:
    executable = None
    debug = False
    ignore_same = False
    requests: request = None
    
    # Pip / PyPi Functionalities
    def __init__(self, command: list=[], executable: str=None, debug: bool=False, find: bool=False, arch: str=None):
        import sys
        import os
        import tempfile
        import re
        import json
        import platform
        import importlib
        import importlib.metadata
        import subprocess
        import glob
        import stat
        import shutil
        import urllib.parse
        import time
        import mmap

        self._sys = sys
        self._os = os
        self._tempfile = tempfile
        self._re = re
        self._platform = platform
        self._importlib = importlib
        self._importlib_metadata = importlib.metadata
        self._subprocess = subprocess
        self._glob = glob
        self._stat = stat
        self._shutil = shutil
        self._urllib_parse = urllib.parse
        self._time = time
        self._json = json
        self._mmap = mmap

        self._main_os = platform.system()
        if type(executable) is str:
            if os.path.isfile(executable): self.executable = executable
            else: self.executable = self.findPython(arch=arch, path=True) if find == True else sys.executable
        elif type(arch) is str: self.executable = self.findPython(arch=arch, path=True)
        else: self.executable = self.findPython(arch=arch, path=True) if find == True else sys.executable
        if self._main_os == "Windows":
            try:
                try:
                    import win32gui # type: ignore
                    import win32process # type: ignore
                    self._win32gui = win32gui
                    self._win32process = win32process
                except Exception:
                    self.install(["pywin32"])
                    self._win32gui = self.importModule("win32gui")
                    self._win32process = self.importModule("win32process")
            except: pass
        elif self._main_os == "Darwin":
            try:
                try:
                    from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly # type: ignore
                except Exception as e:
                    self.install(["pyobjc-framework-Quartz"])
                    Quartz = self.importModule("Quartz")
                    CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly = Quartz.CGWindowListCopyWindowInfo, Quartz.kCGWindowListOptionOnScreenOnly
                self._CGWindowListCopyWindowInfo = CGWindowListCopyWindowInfo
                self._kCGWindowListOptionOnScreenOnly = kCGWindowListOptionOnScreenOnly
            except: pass
        self.debug = debug==True
        self.requests = request()
        if type(command) is list and len(command) > 0: self.ensure(); subprocess.check_call([self.executable, "-m", "pip"] + command)
    def install(self, packages: typing.List[str], upgrade: bool=False, user: bool=True):
        self.ensure()
        res = {}
        generated_list = []
        if self.getIfVirtualEnvironment(): user = False
        for i in packages:
            if type(i) is str: generated_list.append(i)
        if len(generated_list) > 0:
            try:
                a = self._subprocess.call([self.executable, "-m", "pip", "install"] + (["--upgrade"] if upgrade == True else []) + (["--user"] if user == True else []) + generated_list, stdout=(not self.debug) and self._subprocess.DEVNULL or None, stderr=(not self.debug) and self._subprocess.DEVNULL or None)
                if a == 0: return {"success": True, "message": "Successfully installed modules!"}
                else: return {"success": False, "message": f"Command has failed! Code: {a}"}
            except Exception as e: return {"success": False, "message": str(e)}
        return res
    def uninstall(self, packages: typing.List[str]):
        self.ensure()
        res = {}
        generated_list = []
        for i in packages:
            if type(i) is str: generated_list.append(i)
        if len(generated_list) > 0:
            try:
                self._subprocess.call([self.executable, "-m", "pip", "uninstall", "-y"] + generated_list, stdout=self._subprocess.DEVNULL if self.debug == False else None, stderr=self._subprocess.DEVNULL if self.debug == False else None)
                res[i] = {"success": True}
            except Exception as e: res[i] = {"success": False}
        return res
    def installed(self, packages: typing.List[str]=[], boolonly: bool=False):
        self.ensure()
        if self.isSameRunningPythonExecutable() and not len(packages) == 0:
            def che(a):
                try: self._importlib_metadata.version(a); return True
                except self._importlib_metadata.PackageNotFoundError: return False
            if len(packages) == 1: return che(packages[0].lower())
            else:
                installed_checked = {}
                all_installed = True
                for i in packages:
                    try:
                        if che(i.lower()): installed_checked[i] = True
                        else:
                            installed_checked[i] = False
                            all_installed = False
                    except Exception as e:
                        installed_checked[i] = False
                        all_installed = False
                installed_checked["all"] = all_installed
                if boolonly == True: return installed_checked["all"]
                return installed_checked
        else:
            sub = self._subprocess.run([self.executable, "-m", "pip", "list"], stdout=self._subprocess.PIPE, stderr=self._subprocess.PIPE)
            line_splits = sub.stdout.decode().replace("\r", "").splitlines()[2:]
            installed_packages = [package.split()[0].lower() for package in line_splits if package.strip()]
            installed_checked = {}
            all_installed = True
            if len(packages) == 0: return installed_packages
            elif len(packages) == 1: return packages[0].lower() in installed_packages
            else:
                for i in packages:
                    try:
                        if i.lower() in installed_packages: installed_checked[i] = True
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
        generated_list = []
        for i in packages:
            if type(i) is str: generated_list.append(i)
        if len(generated_list) > 0:
            try:
                cur_path = self._os.path.dirname(self._os.path.abspath(__file__))
                if repository_mode == True:
                    url_paths = []
                    url_paths_2 = []
                    for i in generated_list: 
                        if i.startswith("https://github.com") or i.startswith("https://www.github.com"):
                            path_parts = self._urllib_parse.urlparse(i).path.strip('/').split('/')
                            url_paths.append(path_parts[-1])
                            url_paths_2.append(path_parts[-2])
                    down_path = self._os.path.join(cur_path, '-'.join(url_paths) + "_download")
                    if self._os.path.isdir(down_path): self._shutil.rmtree(down_path, ignore_errors=True)
                    self._os.makedirs(down_path, mode=511)
                    co = 0
                    downed_paths = []
                    for url_path_1 in url_paths:
                        url_path_2 = url_paths_2[co]
                        s = self.requests.download(f"https://github.com/{url_path_2}/{url_path_1}/archive/refs/heads/main.zip", self._os.path.join(down_path, f"{url_path_1}.zip"))
                        if s.ok: downed_paths.append(self._os.path.join(down_path, f"{url_path_1}.zip"))
                        co += 1
                    return {"success": True, "path": down_path, "package_files": downed_paths}
                else:
                    down_path = self._os.path.join(cur_path, '-'.join(generated_list) + "_download")
                    if self._os.path.isdir(down_path): self._shutil.rmtree(down_path, ignore_errors=True)
                    self._os.makedirs(down_path, mode=511)
                    self.ensure()
                    self._subprocess.check_call([self.executable, "-m", "pip", "download", "--no-binary", ":all:"] + generated_list, stdout=self.debug == False and self._subprocess.DEVNULL, stderr=self.debug == False and self._subprocess.DEVNULL, cwd=down_path)
                    a = []
                    for e in self._os.listdir(down_path): a.append(self._os.path.join(down_path, e))
                    return {"success": True, "path": down_path, "package_files": a}
            except Exception as e:
                print(e)
                return {"success": False}
        return {"success": False}
    def update(self):
        self.ensure()
        try:
            a = self._subprocess.call([self.executable, "-m", "pip", "install", "--upgrade", "pip"], stdout=self._subprocess.DEVNULL if (not self.debug) else None, stderr=self._subprocess.DEVNULL if (not self.debug) else None)
            if a == 0: return {"success": True, "message": "Successfully installed latest version of pip!"}
            else: return {"success": False, "message": f"Command has failed!"}
        except Exception as e: return {"success": False, "message": str(e)}
    def ensure(self):
        if not self.executable: return False
        check_for_pip_pro = self._subprocess.run([self.executable, "-m", "pip"], stdout=self._subprocess.DEVNULL, stderr=self._subprocess.DEVNULL)
        if check_for_pip_pro.returncode == 0: return True
        else:
            if self.getIfConnectedToInternet() == True:
                self.printDebugMessage(f"Downloading pip from pypi..")
                with self._tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_file: pypi_download_path = temp_file.name
                if self.pythonSupported(3,9,0): download_res = self.requests.download("https://bootstrap.pypa.io/get-pip.py", pypi_download_path)      
                else: current_python_version = self.getCurrentPythonVersion(); download_res = self.requests.download(f"https://bootstrap.pypa.io/pip/{current_python_version.split('.')[0]}.{current_python_version.split('.')[1]}/get-pip.py", pypi_download_path)
                if download_res.ok:
                    self.printDebugMessage(f"Successfully downloaded pip! Installing to Python..")
                    install_to_py = self._subprocess.run([self.executable, pypi_download_path], stdout=self.debug == False and self._subprocess.DEVNULL, stderr=self.debug == False and self._subprocess.DEVNULL)
                    if install_to_py.returncode == 0:
                        self.printDebugMessage(f"Successfully installed pip to Python executable!")
                        return True
                    else: return False
                else: return False
            else:
                self.printDebugMessage(f"Unable to download pip due to no internet access.")
                return False
    def updates(self, packages: typing.List[str]=[]):
        sub = self._subprocess.run([self.executable, "-m", "pip", "list", "--outdated", "--format=json"], stdout=self._subprocess.PIPE, stderr=self._subprocess.PIPE)
        json_str = sub.stdout.decode().replace("\r", "")
        try:
            tried = self._json.loads(json_str)
            if packages and len(packages) > 0: return {"success": True, "packages": [i for i in tried if i["name"] in packages]}
            return {"success": True, "packages": tried}
        except: return {"success": False, "packages": []}
    def info(self, packages: typing.List[str]):
        generated_list = []
        for i in packages:
            if type(i) is str: generated_list.append(i)
        if len(generated_list) > 0:
            try:
                information = {}
                for i in generated_list:
                    urll = f"https://pypi.org/pypi/{i}/json"
                    if self.getIfConnectedToInternet() == False: return {"success": False}
                    response = self.requests.get(urll)
                    if response.ok:
                        data = response.json
                        info = data["info"]
                        information[i] = info
                return {"success": True, "data": information}
            except Exception as e: return {"success": False}
        return {"success": False}
    def github(self, packages: typing.List[str]):
        generated_list = []
        for i in packages:
            if type(i) is str: generated_list.append(i)
        if len(generated_list) > 0:
            try:
                informed = self.info(generated_list)
                if informed["success"] == True:
                    informed = informed["data"]
                    links = {}
                    for i in generated_list:
                        if informed.get(i):
                            info = informed[i]
                            url = info.get("project_urls", {}).get("Source") or info.get("home_page")
                            if url: links[i] = url
                    return {"success": True, "repositories": links}
            except Exception as e: return {"success": False}
        return {"success": False}
    
    # Python Management
    def getLatestPythonVersion(self, beta: bool=False):
        url = "https://www.python.org/downloads/"
        if beta == True: url = "https://www.python.org/download/pre-releases/"
        response = self.requests.get(url)
        if response.ok: html = response.text
        else: html = ""
        if beta == True: match = self._re.search(r'Python (\d+\.\d+\.\d+)([a-zA-Z0-9]+)?', html)
        else: match = self._re.search(r"Download Python (\d+\.\d+\.\d+)", html)
        if match:
            if beta == True: version = f'{match.group(1)}{match.group(2)}'
            else: version = match.group(1)
            return version
        else:
            self.printDebugMessage("Failed to find latest Python version.")
            return None
    def getCurrentPythonVersion(self):
        if not self.executable: return None
        if self.isSameRunningPythonExecutable(): return self._platform.python_version()
        else:
            a = self._subprocess.run([self.executable, "-V"], stdout=self._subprocess.PIPE, stderr=self._subprocess.PIPE)
            final = a.stdout.decode()
            if a.returncode == 0: return final.replace("Python ", "").replace("\n", "").replace("\r", "")
            else: return None
    def getIfPythonVersionIsBeta(self, version=""):
        if version == "": cur_vers = self.getCurrentPythonVersion()
        else: cur_vers = version
        match = self._re.search(r'(\d+\.\d+\.\d+)([a-z]+(\d+)?)?', cur_vers)
        if match:
            _, suf, _ = match.groups()
            if suf: return True
            return False
        else: return False
    def getIfPythonIsLatest(self):
        cur_vers = self.getCurrentPythonVersion()
        if self.getIfPythonVersionIsBeta(): latest_vers = self.getLatestPythonVersion(beta=True)
        else: latest_vers = self.getLatestPythonVersion(beta=False)
        return cur_vers == latest_vers
    def pythonInstalled(self, computer=False):
        if computer == True:
            if self.findPython(): return True
            else: return False
        else:
            if not self.executable: return False
            if self._os.path.exists(self.executable): return True
            else: return False
    def extractPythonVersion(self, path):
        name = self._os.path.basename(path)
        match = self._re.search(r'python(?:w)?(?:-?|\s*)(\d+)(?:\.(\d+))?(?:\.(\d+))?', name)
        if match: return tuple(int(g) if g is not None else 0 for g in match.groups())
        version_part = self._os.path.basename(self._os.path.dirname(path))
        match2 = self._re.match(r'(\d+)(?:\.(\d+))?(?:\.(\d+))?', version_part)
        if match2: return tuple(int(g) if g is not None else 0 for g in match2.groups())
        return (0, 0, 0)
    def pythonSupported(self, major: int=3, minor: int=13, patch: int=2):
        cur_version = self.getCurrentPythonVersion()
        if not cur_version: return False
        return self.pythonSupportedStatic(cur_version, major, minor, patch)
    def pythonSupportedStatic(self, version: str, major: int=3, minor: int=13, patch: int=2):
        if not version: return False
        match = self._re.match(r"(\d+)\.(\d+)\.(\w+)", version)
        if match:
            version = match.groups() 
            def to_int(val): return int(self._re.sub(r'\D', '', val))
            return tuple(map(to_int, version)) >= (major, minor, patch)
        else: return False
    def osSupported(self, windows_build: int=0, macos_version: tuple=(0,0,0)):
        if self._main_os == "Windows":
            version = self._platform.version()
            v = version.split(".")
            if len(v) < 3: return False
            return int(v[2]) >= windows_build
        elif self._main_os == "Darwin":
            version = self._platform.mac_ver()[0]
            version_tuple = tuple(map(int, version.split('.')))
            while len(version_tuple) < 3: version_tuple += (0,)
            while len(macos_version) < 3: min_version += (0,)
            return version_tuple >= macos_version
        else: return False
    def pythonInstall(self, version: str="", beta: bool=False, silent: bool=False):
        ma_os = self._main_os
        ma_arch = self._platform.architecture()
        ma_processor = self._platform.machine()
        macos_version_numbers = {
            "3.10.0a3": "11.0",
            "3.9.1rc1": "11.0"
        }
        if not self.pythonSupportedStatic(version, 3, 9, 2):
            if not self.pythonSupportedStatic(version, 3, 9, 2) and self.pythonSupportedStatic(version, 3, 7, 0): macos_version_numbers[version] = "x10.9"
            elif self.pythonSupportedStatic(version, 3, 7, 0): macos_version_numbers[version] = "x10.6"
        if self.getIfConnectedToInternet() == False:
            self.printDebugMessage("Failed to download Python installer.")
            return
        if version == "": version = self.getLatestPythonVersion(beta=beta)
        if not version:
            self.printDebugMessage("Failed to download Python installer.")
            return
        version_url_folder = version
        if beta == True: version_url_folder = self._re.match(r'^\d+\.\d+\.\d+', version).group()
        if ma_os == "Darwin":
            url = f"https://www.python.org/ftp/python/{version_url_folder}/python-{version}-macos{macos_version_numbers.get(version, '11')}.pkg"
            with self._tempfile.NamedTemporaryFile(suffix=".pkg", delete=False) as temp_file: pkg_file_path = temp_file.name
            result = self.requests.download(url, pkg_file_path)            
            if result.ok:
                if silent == True: 
                    self.printDebugMessage(f"Silently installing Python packages.. Admin permissions may be requested.")
                    self._subprocess.run(["osascript", "-e", f"do shell script \"installer -pkg '{pkg_file_path}' -target /\" with administrator privileges"], stdout=self.debug == False and self._subprocess.DEVNULL, stderr=self.debug == False and self._subprocess.DEVNULL, check=True)
                    self.printDebugMessage(f"Successfully installed Python package: {pkg_file_path}")
                else:
                    self._subprocess.run(["open", pkg_file_path], stdout=self.debug == False and self._subprocess.DEVNULL, stderr=self.debug == False and self._subprocess.DEVNULL, check=True)
                    while self.getIfProcessIsOpened("/System/Library/CoreServices/Installer.app") == True: self._time.sleep(0.1)
                    self.printDebugMessage(f"Python installer has been executed: {pkg_file_path}")
            else:
                self.printDebugMessage("Failed to download Python installer.")
        elif ma_os == "Windows":
            if version < "3.11.0": self.printDebugMessage("PyKits is not normally made for versions less than 3.11.0.")
            if ma_arch[0] == "64bit":
                if ma_processor.lower() == "arm64": url = f"https://www.python.org/ftp/python/{version_url_folder}/python-{version}-arm64.exe"
                else: url = f"https://www.python.org/ftp/python/{version_url_folder}/python-{version}-amd64.exe"
            else: url = f"https://www.python.org/ftp/python/{version_url_folder}/python-{version}.exe"
            with self._tempfile.NamedTemporaryFile(suffix=".exe", delete=False) as temp_file: exe_file_path = temp_file.name
            result = self.requests.download(url, exe_file_path)
            if result.ok:
                if silent == True:
                    self.printDebugMessage(f"Silently installing Python packages..")
                    self._subprocess.run([exe_file_path, "/quiet"], stdout=self.debug == False and self._subprocess.DEVNULL, stderr=self.debug == False and self._subprocess.DEVNULL, check=True)
                    self.printDebugMessage(f"Successfully installed Python package: {exe_file_path}")
                else:
                    self._subprocess.run([exe_file_path], stdout=self.debug == False and self._subprocess.DEVNULL, stderr=self.debug == False and self._subprocess.DEVNULL, check=True)
                    self.printDebugMessage(f"Python installer has been executed: {exe_file_path}")
            else:
                self.printDebugMessage("Failed to download Python installer.")
    def installLocalPythonCertificates(self):
        if self._main_os == "Darwin":
            with open("./install_local_python_certs.py", "w") as f: f.write("""import os; import os.path; import ssl; import stat; import subprocess; import sys; STAT_0o775 = ( stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP | stat.S_IROTH |  stat.S_IXOTH ); openssl_dir, openssl_cafile = os.path.split(ssl.get_default_verify_paths().openssl_cafile); print(" -- pip install --upgrade certifi"); subprocess.check_call([sys.executable, "-E", "-s", "-m", "pip", "install", "--upgrade", "certifi"]); import certifi; os.chdir(openssl_dir); relpath_to_certifi_cafile = os.path.relpath(certifi.where()); print(" -- removing any existing file or link"); os.remove(openssl_cafile); print(" -- creating symlink to certifi certificate bundle"); os.symlink(relpath_to_certifi_cafile, openssl_cafile); print(" -- setting permissions"); os.chmod(openssl_cafile, STAT_0o775); print(" -- update complete");""")
            s = self._subprocess.run(f'"{self.executable}" ./install_local_python_certs.py', shell=True, stdout=self._subprocess.DEVNULL, stderr=self._subprocess.DEVNULL)
            self._os.remove("./install_local_python_certs.py")
            if not (s.returncode == 0) and self.debug == True: print(f"Unable to install local python certificates!")
    def getIf32BitWindows(self): return self._main_os == "Windows" and self.getArchitecture() == "x86"
    def getIfArmWindows(self): return self._main_os == "Windows" and self.getArchitecture() == "arm"
    def getIfRunningWindowsAdmin(self):
        if self._main_os == "Windows":
            try: import ctypes; return ctypes.windll.shell32.IsUserAnAdmin()
            except: return False
        else: return False
    def getArchitecture(self):
        if self.isSameRunningPythonExecutable():
            machine_var = self._platform.machine()
            if self._main_os == "Windows":
                with open(self.executable if self.executable else self._sys.executable, "rb") as f:
                    mm = self._mmap.mmap(f.fileno(), 0, access=self._mmap.ACCESS_READ)
                    pe_offset = int.from_bytes(mm[0x3C:0x40], "little")
                    machine = int.from_bytes(mm[pe_offset + 4:pe_offset + 6], "little")
                    mm.close()
                arch_map = { 0x014c: "x86", 0x8664: "x64", 0xAA64: "arm", 0x01c0: "arm" }
                return arch_map.get(machine, "")
            elif self._main_os == "Darwin":
                if machine_var.lower() == "arm64": return "arm"
                elif machine_var.lower() == "x86_64": return "intel"
                else: return "x86"
            else: return machine_var
        else:
            exe = self.executable if self.executable else self._sys.executable
            if self._main_os == "Darwin":
                try:
                    s = self._subprocess.run([exe, "-c", "import platform; machine_var = platform.machine(); print('arm' if machine_var.lower() == 'arm64' else ('intel' if machine_var.lower() == 'x86_64' else 'x86'))"], stdout=self._subprocess.PIPE, stderr=self._subprocess.PIPE)
                    final = s.stdout.decode()
                    return final.replace("\n", "").replace("\r", "")
                except: return ""
            elif self._main_os == "Windows":
                with open(exe, "rb") as f:
                    mm = self._mmap.mmap(f.fileno(), 0, access=self._mmap.ACCESS_READ)
                    pe_offset = int.from_bytes(mm[0x3C:0x40], "little")
                    machine = int.from_bytes(mm[pe_offset + 4:pe_offset + 6], "little")
                    mm.close()
                arch_map = { 0x014c: "x86", 0x8664: "x64", 0xAA64: "arm", 0x01c0: "arm" }
                return arch_map.get(machine, "")
            else: return machine_var
    def getIfVirtualEnvironment(self):
        alleged_path = self._os.path.dirname(self.executable)
        return self._os.path.exists(self._os.path.join(alleged_path, "activate")) or self._os.path.exists(self._os.path.join(alleged_path, "activate.bat"))
    def findPython(self, arch=None, latest=True, optimize=True, path=False):
        ma_os = self._main_os
        if ma_os == "Darwin":
            target_name = "python3-intel64" if arch == "intel" else "python3"
            if optimize == True and self._os.path.exists(f"/usr/local/bin/{target_name}") and self._os.path.islink(f"/usr/local/bin/{target_name}"): return f"/usr/local/bin/{target_name}" if path == True else pip(executable=f"/usr/local/bin/{target_name}")
            else:
                paths = [
                    "/usr/local/bin/python*",
                    "/opt/homebrew/bin/python*",
                    "/Library/Frameworks/Python.framework/Versions/*/bin/python*",
                    self._os.path.expanduser("~/Library/Python/*/bin/python*"),
                    self._os.path.expanduser("~/.pyenv/versions/*/bin/python*"),
                    self._os.path.expanduser("~/opt/anaconda*/bin/python*")
                ]
                found_paths = []
                for path_pattern in paths: found_paths.extend(self._glob.glob(path_pattern))
                if latest == True: found_paths.sort(reverse=True, key=self.extractPythonVersion)
                for pat in found_paths:
                    if self._os.path.isfile(pat):
                        if pat.endswith("t") or pat.endswith("config") or pat.endswith("m") or self._os.path.basename(pat).startswith("pythonw"): continue
                        pip_class = pip(executable=pat)
                        if arch:
                            py_arch = pip_class.getArchitecture()
                            if py_arch == "": continue
                            if py_arch == arch: return pat if path == True else pip_class
                        else: return pat if path == True else pip_class
                return None
        elif ma_os == "Windows":
            paths = [
                self._os.path.expandvars(r'%LOCALAPPDATA%\\Programs\\Python\\Python*'),
                self._os.path.expandvars(r'%LOCALAPPDATA%\\Programs\\Python\\Python*\\python.exe'),
                self._os.path.expandvars(r'%PROGRAMFILES%\\Python*\\python.exe'),
                self._os.path.expandvars(r'%PROGRAMFILES(x86)%\\Python*\\python.exe')
            ]
            found_paths = []
            for path_pattern in paths: found_paths.extend(self._glob.glob(path_pattern))
            if latest == True: found_paths.sort(reverse=True, key=self.extractPythonVersion)
            for pat in found_paths:
                if self._os.path.isfile(pat):
                    pip_class = pip(executable=pat)
                    if arch:
                        py_arch = pip_class.getArchitecture()
                        if py_arch == "": continue
                        if py_arch == arch: return pat if path == True else pip_class
                    else: return pat if path == True else pip_class
            return None
    def findPythons(self, arch=None, latest=True, paths=False):
        ma_os = self._main_os
        founded_pythons = []
        if ma_os == "Darwin":
            path_table = [
                "/usr/local/bin/python*",
                "/opt/homebrew/bin/python*",
                "/Library/Frameworks/Python.framework/Versions/*/bin/python*",
                self._os.path.expanduser("~/Library/Python/*/bin/python*"),
                self._os.path.expanduser("~/.pyenv/versions/*/bin/python*"),
                self._os.path.expanduser("~/opt/anaconda*/bin/python*")
            ]
            found_paths = []
            for path_pattern in path_table: found_paths.extend(self._glob.glob(path_pattern))
            if latest == True: found_paths.sort(reverse=True, key=self.extractPythonVersion)
            for path in found_paths:
                if self._os.path.isfile(path):
                    if path.endswith("t") or path.endswith("config") or path.endswith("m") or self._os.path.basename(path).startswith("pythonw"): continue
                    pip_class = pip(executable=path)
                    if arch:
                        py_arch = pip_class.getArchitecture()
                        if py_arch == "": continue
                        if py_arch == arch: founded_pythons.append(path if paths == True else pip_class)
                    else: founded_pythons.append(path if paths == True else pip_class)
        elif ma_os == "Windows":
            path_table = [
                self._os.path.expandvars(r'%LOCALAPPDATA%\\Programs\\Python\\Python*'),
                self._os.path.expandvars(r'%LOCALAPPDATA%\\Programs\\Python\\Python*\\python.exe'),
                self._os.path.expandvars(r'%PROGRAMFILES%\\Python*\\python.exe'),
                self._os.path.expandvars(r'%PROGRAMFILES(x86)%\\Python*\\python.exe')
            ]
            found_paths = []
            for path_pattern in path_table: found_paths.extend(self._glob.glob(path_pattern))
            if latest == True: found_paths.sort(reverse=True, key=self.extractPythonVersion)
            for path in found_paths:
                if self._os.path.isfile(path):
                    pip_class = pip(executable=path)
                    if arch:
                        py_arch = pip_class.getArchitecture()
                        if py_arch == "": continue
                        if py_arch == arch: founded_pythons.append(path if paths == True else pip_class)
                    else: founded_pythons.append(path if paths == True else pip_class)
        return founded_pythons
    def isSameRunningPythonExecutable(self):
        if self.ignore_same == True: return False
        if not self.executable: return False
        if self._os.path.exists(self.executable) and self._os.path.exists(self._sys.executable): return self._os.path.samefile(self.executable, self._sys.executable)
        else: return False

    # Python Functions
    def getLocalAppData(self):
        ma_os = self._main_os
        if ma_os == "Windows": return self._os.path.expandvars(r'%LOCALAPPDATA%')
        elif ma_os == "Darwin": return f'{self._os.path.expanduser("~")}/Library/'
        else: return f'{self._os.path.expanduser("~")}/'
    def getUserFolder(self): return self._os.path.expanduser("~")
    def getIfLoggedInIsMacOSAdmin(self):
        ma_os = self._main_os
        if ma_os == "Darwin":
            logged_in_folder = self.getUserFolder()
            username = self._os.path.basename(logged_in_folder)
            groups_res = self._subprocess.run(["/usr/bin/groups", username], stdout=self._subprocess.PIPE, stderr=self._subprocess.PIPE)
            if groups_res.returncode == 0: return "admin" in groups_res.stdout.decode("utf-8").split(" ")
            else: return False
        else: return False
    def getInstallableApplicationsFolder(self):
        ma_os = self._main_os
        if ma_os == "Darwin":
            if self.getIfLoggedInIsMacOSAdmin(): return self._os.path.join("/", "Applications")
            else: return self._os.path.join(self.getUserFolder(), "Applications")
        elif ma_os == "Windows":
            return self.getLocalAppData()
    def restartScript(self, scriptname: str, argv: list):
        argv.pop(0)
        res = self._subprocess.run([self.executable, self._os.path.join(self._os.path.dirname(self._os.path.abspath(__file__)), scriptname)] + argv)
        self._sys.exit(res.returncode)
    def endProcess(self, name="", pid=""):
        main_os = self._main_os
        if pid == "":
            if main_os == "Darwin": self._subprocess.run(["/usr/bin/killall", "-9", name], stdout=self._subprocess.DEVNULL)
            elif main_os == "Windows": self._subprocess.run(f"taskkill /IM {name} /F", shell=True, stdout=self._subprocess.DEVNULL)
            else: self._subprocess.run(f"killall -9 {name}", shell=True, stdout=self._subprocess.DEVNULL)
        else:
            if main_os == "Darwin": self._subprocess.run(f"kill -9 {pid}", shell=True, stdout=self._subprocess.DEVNULL)
            elif main_os == "Windows": self._subprocess.run(f"taskkill /PID {pid} /F", shell=True, stdout=self._subprocess.DEVNULL)
            else: self._subprocess.run(f"kill -9 {pid}", shell=True, stdout=self._subprocess.DEVNULL)
    def importModule(self, module_name: str, install_module_if_not_found: bool=False, loop_until_import: bool=False):
        self.uncacheLoadedModules()
        try: 
            s = self._importlib.import_module(module_name)
            if type(s) is None: raise ModuleNotFoundError("")
            else: return s
        except ModuleNotFoundError:
            try:
                if install_module_if_not_found == True and self.isSameRunningPythonExecutable(): self.install([module_name])
                self.uncacheLoadedModules()
                s = self._importlib.import_module(module_name)
                if type(s) is None: raise ModuleNotFoundError("")
                else: return s
            except Exception: 
                if loop_until_import == False: raise ImportError(f'Unable to find module "{module_name}" in Python {self.getCurrentPythonVersion()} environment.')
                self._time.sleep(1)
                return self.importModule(module_name=module_name, install_module_if_not_found=install_module_if_not_found, loop_until_import=loop_until_import)
        except Exception as e: raise ImportError(f'Unable to import module "{module_name}" in Python {self.getCurrentPythonVersion()} environment. Exception: {str(e)}')
    def uncacheLoadedModules(self):
        if getattr(self._sys, "frozen", False): pass
        else:
            import site
            self._site = site
            site_packages_paths = self._site.getsitepackages() + [self._site.getusersitepackages()]
            for path in site_packages_paths:
                if path not in self._sys.path and self._os.path.exists(path): self._sys.path.append(path)
        self._importlib.invalidate_caches()
    def unzipFile(self, path: str, output: str, look_for: list=[], export_out: list=[], either: bool=False, check: bool=True, moving_file_func: typing.Callable=None):
        class result():
            returncode = 0
            path = ""
        if not self._os.path.exists(output): self._os.makedirs(output, mode=511)
        previous_output = output
        if output.endswith("/"): output = output[:-1]
        if len(look_for) > 0: output = output + f"_Full_{self._os.urandom(3).hex()}"; self._os.makedirs(output, mode=511)
        if self._main_os == "Windows": zip_extract = self._subprocess.run(["C:\\Windows\\System32\\tar.exe", "-xf", path] + export_out + ["-C", output], stdout=self._subprocess.PIPE, stderr=self._subprocess.PIPE, check=check)
        else: zip_extract = self._subprocess.run(["/usr/bin/ditto", "-xk", path, output], stdout=self._subprocess.PIPE, stderr=self._subprocess.PIPE, check=check)
        if len(look_for) > 0:
            if zip_extract.returncode == 0:
                for ro, dir, fi in self._os.walk(output):
                    if either == True:
                        found_all = False
                        for a in look_for:
                            if a in (fi + dir): found_all = True
                    else:
                        found_all = True
                        for a in look_for:
                            if not a in (fi + dir): found_all = False
                    if found_all == True: 
                        if moving_file_func: moving_file_func()
                        if self._os.path.exists(previous_output): self._shutil.rmtree(previous_output, ignore_errors=True)
                        self._shutil.move(ro, previous_output)
                        self._shutil.rmtree(output, ignore_errors=True)
                        s = result()
                        s.path = previous_output
                        s.returncode = 0
                        return s
            if self._os.path.exists(output): self._shutil.rmtree(output, ignore_errors=True)
            if self._os.path.exists(previous_output): self._shutil.rmtree(previous_output, ignore_errors=True)
            s = result()
            s.path = None
            s.returncode = 1
            return s
        else:
            s = result()
            s.path = previous_output
            s.returncode = 0
            return s
    def copyTreeWithMetadata(self, src: str, dst: str, symlinks=False, ignore=None, dirs_exist_ok=False, ignore_if_not_exist=False):
        if not self._os.path.exists(src) and ignore_if_not_exist == False: return
        if not dirs_exist_ok and self._os.path.exists(dst): raise FileExistsError(f"Destination '{dst}' already exists.")
        self._os.makedirs(dst, exist_ok=True, mode=511)
        for root, dirs, files in self._os.walk(src):
            rel_path = self._os.path.relpath(root, src)
            dst_root = self._os.path.join(dst, rel_path)
            ignored_names = ignore(root, self._os.listdir(root)) if ignore else set()
            dirs[:] = [d for d in dirs if d not in ignored_names]
            files = [f for f in files if f not in ignored_names]
            self._os.makedirs(dst_root, exist_ok=True, mode=511)
            for dir_name in dirs:
                src_dir = self._os.path.join(root, dir_name)
                dst_dir = self._os.path.join(dst_root, dir_name)

                if self._os.path.islink(src_dir) and symlinks:
                    link_target = self._os.readlink(src_dir)
                    self._os.symlink(link_target, dst_dir)
                else:
                    self._os.makedirs(dst_dir, exist_ok=True, mode=511)
                    self._shutil.copystat(src_dir, dst_dir, follow_symlinks=False)
                    self._os.chmod(dst_dir, self._os.stat(dst_dir).st_mode | self._stat.S_IWGRP | self._stat.S_IROTH | self._stat.S_IWOTH)
            for file_name in files:
                src_file = self._os.path.join(root, file_name)
                dst_file = self._os.path.join(dst_root, file_name)
                if self._os.path.islink(src_file) and symlinks:
                    link_target = self._os.readlink(src_file)
                    self._os.symlink(link_target, dst_file)
                else:
                    self._shutil.copy2(src_file, dst_file)
                    self._os.chmod(dst_file, self._os.stat(dst_file).st_mode | self._stat.S_IWGRP | self._stat.S_IROTH | self._stat.S_IWOTH)
            self._shutil.copystat(root, dst_root, follow_symlinks=False)
            self._os.chmod(dst_root, self._os.stat(dst_root).st_mode | self._stat.S_IWGRP | self._stat.S_IROTH | self._stat.S_IWOTH)
        return dst
    def getIfProcessIsOpened(self, process_name="", pid=""):
        ma_os = self._main_os
        if ma_os == "Windows":
            process_list = self._subprocess.run(["tasklist"], stdout=self._subprocess.PIPE, stderr=self._subprocess.PIPE).stdout.decode("utf-8")
            if pid == "" or pid == None: return process_name in process_list
            else: return f"{pid} Console" in process_list or f"{pid} Service" in process_list
        else:
            if pid == "" or pid == None: return self._subprocess.run(f"pgrep -f '{process_name}' > /dev/null 2>&1", shell=True).returncode == 0
            else: return self._subprocess.run(f"ps -p {pid} > /dev/null 2>&1", shell=True).returncode == 0
    def getAmountOfProcesses(self, process_name=""):
        ma_os = self._main_os
        if ma_os == "Windows":
            process = self._subprocess.Popen(["tasklist"], stdout=self._subprocess.PIPE, stderr=self._subprocess.PIPE)
            output, _ = process.communicate()
            process_list = output.decode("utf-8")
            return process_list.lower().count(process_name.lower())
        else:
            result = self._subprocess.run(f"pgrep -f '{process_name}'", stdout=self._subprocess.PIPE, stderr=self._subprocess.PIPE, shell=True)
            process_ids = result.stdout.decode("utf-8").strip().split("\n")
            return len([pid for pid in process_ids if pid.isdigit()])
    def getIfConnectedToInternet(self): return self.requests.get_if_connected()
    def getProcessWindows(self, pid: int):
        if (type(pid) is str and pid.isnumeric()) or type(pid) is int:
            if self._main_os == "Windows":
                system_windows = []
                def callback(hwnd, _):
                    if self._win32gui.IsWindowVisible(hwnd):
                        _, window_pid = self._win32process.GetWindowThreadProcessId(hwnd)
                        if window_pid == int(pid): system_windows.append(hwnd)
                self._win32gui.EnumWindows(callback, None)
                return system_windows
            elif self._main_os == "Darwin":
                system_windows = self._CGWindowListCopyWindowInfo(self._kCGWindowListOptionOnScreenOnly, 0)
                app_windows = [win for win in system_windows if win.get("kCGWindowOwnerPID") == int(pid)]
                new_set_of_system_windows = []
                for win in app_windows:
                    if win and win.get("kCGWindowOwnerPID"): new_set_of_system_windows.append(win)
                return new_set_of_system_windows
            else: return []
        else: return []
    def printDebugMessage(self, message: str):
        if self.debug == True: print(f"\033[38;5;226m[PyKits] [DEBUG]: {message}\033[0m")
class plist:
    def __init__(self):
        import os
        import plistlib
        import subprocess
        import platform
        self._os = os
        self._plistlib = plistlib
        self._subprocess = subprocess
        self._platform = platform
        self._main_os = platform.system()
    def readPListFile(self, path: str):
        if self._os.path.exists(path):
            with open(path, "rb") as f: plist_data = self._plistlib.load(f)
            return plist_data
        else: return {}
    def writePListFile(self, path: str, data: typing.Union[dict, str, int, float], binary: bool=False, ns_mode: bool=False):
        try:
            if ns_mode == True and self._main_os == "Darwin":
                domain = self._os.path.basename(path).replace(".plist", "", 1)
                for i, v in data.items(): self._subprocess.run(["defaults", "write", domain, i, str(v)], check=True)
            with open(path, "wb") as f:
                if binary == True: self._plistlib.dump(data, f, fmt=self._plistlib.FMT_BINARY)
                else: self._plistlib.dump(data, f)
            return {"success": True, "message": "Success!", "data": data}
        except Exception as e: return {"success": False, "message": "Something went wrong.", "data": e}
pip_class = pip()
requests = request()
plist_class = plist()

# Install Python Packages
try:
    import psutil
    if main_os == "Darwin":
        from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly
        import posix_ipc
    elif main_os == "Windows":
        import win32gui # type: ignore
        import win32process # type: ignore
        import win32con # type: ignore
        import win32api # type: ignore
except Exception as e:
    pip_class.install(["psutil"])
    if main_os == "Darwin": pip_class.install(["posix-ipc", "pyobjc-core", "pyobjc-framework-Quartz"])
    elif main_os == "Windows": pip_class.install(["pywin32"])
    psutil = pip_class.importModule("psutil")
    if main_os == "Darwin":
        Quartz = pip_class.importModule("Quartz")
        CGWindowListCopyWindowInfo = Quartz.CGWindowListCopyWindowInfo
        kCGWindowListOptionOnScreenOnly = Quartz.kCGWindowListOptionOnScreenOnly
        posix_ipc = pip_class.importModule("posix_ipc")
    elif main_os == "Windows":
        win32gui = pip_class.importModule("win32gui")
        win32process = pip_class.importModule("win32process")
        win32con = pip_class.importModule("win32con")
        win32api = pip_class.importModule("win32api")
# Install Python Packages

class Handler:
    # System Definitions
    roblox_player_event_names = [
        "onRobloxExit", 
        "onRobloxLog",
        "onRobloxSharedLogLaunch",
        "onRobloxAppStart", 
        "onRobloxAppLoginFailed", 
        "onRobloxPassedUpdate", 
        "onBloxstrapSDK", 
        "onLoadedFFlags", 
        "onSaveRobloxChannel",
        "onUserLogin",
        "onWebSocketFailing",
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
        "onWatchdogReconnection"
    ]
    roblox_studio_event_names = [
        "onRobloxExit", 
        "onRobloxLog",
        "onLoadedFFlags",
        "onSaveRobloxChannel",
        "onUserLogin",
        "onWebSocketFailing",
        "onPlayTestStart",
        "onOpeningGame",
        "onGameUDMUXLoaded",
        "onGameJoined",
        "onJoiningTeam",
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
        "onGameLoaded",
        "onLostConnection",
        "onTeamCreateConnect",
        "onTeamCreateDisconnect",
        "onCloudPlugins",
        "onPluginUnloading",
        "onRobloxSaved",
        "onNewStudioLaunching",
        "onStudioInstallerLaunched",
        "onWatchdogReconnection"
    ]
    roblox_event_info = {
        # 0 = Safe, 1 = Caution, 2 = Warning, 3 = Dangerous
        "onRobloxExit": {"message": ts("Allow detecting when Roblox closes"), "level": 0, "robloxEvent": True}, 
        "onRobloxLog": {"message": ts("Allow detecting every Roblox event"), "level": 3, "robloxEvent": True},
        "onRobloxSharedLogLaunch": {"message": ts("Allow detecting when Roblox was closed by the module due to a shared launch"), "level": 2, "robloxEvent": True},
        "onRobloxLauncherDestroyed": {"message": ts("Allow detecting when the Roblox Launcher is destroyed"), "level": 0, "robloxEvent": True},
        "onRobloxAppStart": {"message": ts("Allow detecting when Roblox starts"), "level": 0, "robloxEvent": True}, 
        "onRobloxAppLoginFailed": {"message": ts("Allow detecting when Roblox logging in fails"), "level": 0, "robloxEvent": True},
        "onRobloxPassedUpdate": {"message": ts("Allow detecting when Roblox passes update checks"), "level": 0, "robloxEvent": True}, 
        "onBloxstrapSDK": {"message": ts("Allow detecting when BloxstrapRPC is triggered"), "level": 1, "robloxEvent": True}, 
        "onLoadedFFlags": {"message": ts("Allow detecting when FFlags are loaded"), "level": 0, "robloxEvent": True}, 
        "onSaveRobloxChannel": {"message": ts("Allow detecting when Roblox Channel is saved"), "level": 1, "robloxEvent": True},
        "onUserLogin": {"message": ts("Allow detecting when the user is logged on"), "level": 1, "robloxEvent": True},
        "onWebSocketFailing": {"message": ts("Allow detecting when the Roblox websocket is loose and about to disconnect"), "level": 1, "robloxEvent": True},
        "onHttpResponse": {"message": ts("Allow detecting when Roblox HttpResponses are ran"), "level": 2, "robloxEvent": True}, 
        "onOtherRobloxLog": {"message": ts("Allow detecting when Unknown Roblox Handlers are detected"), "level": 3, "robloxEvent": True},
        "onRobloxCrash": {"message": ts("Allow detecting when Roblox crashes"), "level": 1, "robloxEvent": True},
        "onRobloxChannel": {"message": ts("Allow detecting the current Roblox channel"), "level": 0, "robloxEvent": True},
        "onRobloxTerminateInstance": {"message": ts("Allow detecting when Roblox closes an extra window."), "level": 1, "robloxEvent": True},
        "onGameLog": {"message": ts("Allow getting Roblox log messages"), "level": 2, "robloxEvent": True}, 
        "onGameWarning": {"message": ts("Allow getting Roblox warning log messages"), "level": 2, "robloxEvent": True}, 
        "onGameError": {"message": ts("Allow getting Roblox error log messages"), "level": 2, "robloxEvent": True}, 
        "onGameStart": {"message": ts("Allow getting Job ID, Place ID and Roblox IP"), "level": 2, "robloxEvent": True}, 
        "onGameLoading": {"message": ts("Allow detecting when loading any server"), "level": 1, "robloxEvent": True}, 
        "onGameLoadingNormal": {"message": ts("Allow detecting when loading public server"), "level": 1, "robloxEvent": True}, 
        "onGameLoadingPrivate": {"message": ts("Allow detecting when loading private server"), "level": 2, "robloxEvent": True}, 
        "onGameLoadingReserved": {"message": ts("Allow detecting when loading reserved server"), "level": 2, "robloxEvent": True},
        "onGameLoadingParty": {"message": ts("Allow detecting when loading party"), "level": 1, "robloxEvent": True}, 
        "onRobloxVoiceChatMute": {"message": ts("Detect when you mute your microphone during your Roblox Voice Chat"), "level": 1, "robloxEvent": True}, 
        "onRobloxVoiceChatUnmute": {"message": ts("Detect when you unmute your microphone during your Roblox Voice Chat"), "level": 1, "robloxEvent": True}, 
        "onRobloxVoiceChatStart": {"message": ts("Detect when Voice Chats on the client start"), "level": 1, "robloxEvent": True}, 
        "onRobloxVoiceChatLeft": {"message": ts("Detect when Voice Chats on the client end"), "level": 1, "robloxEvent": True},
        "onRobloxAudioDeviceStartRecording": {"message": ts("Allow detecting when a game audio device starts recording"), "level": 1, "robloxEvent": True},
        "onRobloxAudioDeviceStopRecording": {"message": ts("Allow detecting when a game audio device stops recording"), "level": 1, "robloxEvent": True},
        "onGameAudioDeviceAvailable": {"message": ts("Allow detecting when a new game audio device is available"), "level": 1, "robloxEvent": True},
        "onGameUDMUXLoaded": {"message": ts("Allow detecting when Roblox Server IPs are loaded"), "level": 2, "robloxEvent": True}, 
        "onGameTeleport": {"message": ts("Allow detecting when you teleport places"), "level": 1, "robloxEvent": True}, 
        "onGameTeleportFailed": {"message": ts("Allow detecting when teleporting fails"), "level": 1, "robloxEvent": True}, 
        "onGameJoinInfo": {"message": ts("Allow getting join info for a game"), "level": 2, "robloxEvent": True}, 
        "onGameJoined": {"message": ts("Allow detecting when Roblox loads a game fully"), "level": 0, "robloxEvent": True}, 
        "onGameLeaving": {"message": ts("Allow detecting when you leave a game"), "level": 0, "robloxEvent": True}, 
        "onGameDisconnected": {"message": ts("Allow detecting when you disconnect from a game"), "level": 0, "robloxEvent": True},
        "onWatchdogReconnection": {"message": ts("Allow detecting when watchdog was reconnected"), "level": 0, "robloxEvent": True},
        
        # Roblox Studio Permissions
        "onJoiningTeam": {"message": ts("Allow detecting when you join a team create server"), "level": 1, "robloxEvent": True},
        "onPlayTestStart": {"message": ts("Allow detecting when you started a playtest"), "level": 0, "robloxEvent": True},
        "onStudioLoginSuccess": {"message": ts("Allow detecting when you have logged into studio successfully"), "level": 1, "robloxEvent": True},
        "onOpeningGame": {"message": ts("Allow detecting when you loaded a place/document"), "level": 1, "robloxEvent": True},
        "onExpiredFlag": {"message": ts("Allow detecting when a flag in your studio data has expired"), "level": 1, "robloxEvent": True},
        "onApplyingFeature": {"message": ts("Allow detecting when a feature in your studio data is loading"), "level": 1, "robloxEvent": True},
        "onPluginLoading": {"message": ts("Allow detecting when a plugin is loading"), "level": 1, "robloxEvent": True},
        "onRobloxPublishing": {"message": ts("Allow detecting when you are publishing the game"), "level": 1, "robloxEvent": True},
        "onPlayTestDisconnected": {"message": ts("Allow detecting when you disconnect from playtesting."), "level": 1, "robloxEvent": True},
        "onTelemetryLog": {"message": ts("Allow detecting studio log information."), "level": 2, "robloxEvent": True},
        "onClosingGame": {"message": ts("Allow detecting when you close a place/document"), "level": 1, "robloxEvent": True},
        "onGameLoaded": {"message": ts("Allow detecting when you fully load a game"), "level": 1, "robloxEvent": True},
        "onLostConnection": {"message": ts("Allow detecting when you disconnect due to lost connection in a Studio server"), "level": 1, "robloxEvent": True},
        "onCloudPlugins": {"message": ts("Allow detecting loading plugins from the web."), "level": 1, "robloxEvent": True},
        "onTeamCreateConnect": {"message": ts("Allow detecting when you connect to a team connect server."), "level": 1, "robloxEvent": True},
        "onTeamCreateDisconnect": {"message": ts("Allow detecting when you disconnect to a team connect server."), "level": 1, "robloxEvent": True},
        "onPluginUnloading": {"message": ts("Allow detecting when a plugin is unloading"), "level": 1, "robloxEvent": True},
        "onRobloxSaved": {"message": ts("Allow detecting when Roblox has saved to Roblox"), "level": 1, "robloxEvent": True},
        "onNewStudioLaunching": {"message": ts("Allow detecting when a new Roblox Studio window is created"), "level": 1, "robloxEvent": True}
    }
    roblox_bundle_files = {
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
    roblox_studio_bundle_files = {
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
        "studiocontent-models.zip": "/StudioContent/models",
        "studiocontent-textures.zip": "/StudioContent/textures",
        "extracontent-models.zip": "/ExtraContent/models",
        "extracontent-textures.zip": "/ExtraContent/textures"
    }
    roblox_download_locations = {
        "setup.rbxcdn.com": 0,
        "setup-aws.rbxcdn.com": 2,
        "setup-ak.rbxcdn.com": 2,
        "roblox-setup.cachefly.net": 2,
        "s3.amazonaws.com/setup.roblox.com": 4
    }
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
    optimal_download_location = "setup.rbxcdn.com"
    last_mfc_studio_version = "version-012732894899482c"
    image_cache = {}

    # System Functions 
    class WatchdogLineResponse():
        code: int=None
        data: typing.Any=None
        def __init__(self, code: int, data: typing.Any): self.code = code; self.data = data
        class EndRoblox(): code=0; data=None
        class EndWatchdog(): code=1; data=None
        class ReconnectWatchdog(): code=2; data=None
        class NormalResponse(): code=3; data=None
    class InvalidRobloxHandlerException(Exception):
        def __init__(self): super().__init__("Please make sure you're providing the RobloxFastFlagsInstaller.Handler class!")
    class RobloxInstance():
        __events__ = []
        pid = ""
        watchdog_started = False
        ended_process = False
        main_handler = None
        log_file = ""
        debug_mode = False
        disconnect_cooldown = False
        end_tracking = False
        connected_to_game = False
        validating_disconnect = False
        created_mutex = False
        is_studio = False
        loading_existing_logs = False
        await_log_creation = False
        await_log_creation_attempts = 0
        one_threaded = True
        roblox_starter_launched = False
        audio_focused = False
        daemon = False

        def __init__(self, main_handler, pid: str="", log_file: str="", debug_mode: bool=False, allow_other_logs: bool=False, await_log_creation: bool=False, created_mutex: bool=False, studio: bool=False, one_threaded: bool=True, daemon: bool=False, start_watchdog: bool=True):
            if type(main_handler) is Handler:
                self.main_handler = main_handler
                if pid == "": self.pid = self.main_handler.getLatestOpenedRobloxPid(studio=studio)
                else: self.pid = pid
                self.debug_mode = debug_mode==True
                self.allow_other_logs = allow_other_logs==True
                self.created_mutex = created_mutex==True
                self.is_studio = studio==True
                self.await_log_creation = await_log_creation==True
                self.one_threaded = one_threaded==True
                self.daemon = daemon==True
                if log_file != "" and os.path.exists(log_file): self.log_file = log_file
                if start_watchdog == True: self.startActivityTracking()
            else: raise Handler.InvalidRobloxHandlerException()
        def awaitRobloxClosing(self):
            while True:
                time.sleep(1)
                if not self.pid: self.ended_process = True; break
                if (self.main_handler.getIfRobloxIsOpen(studio=self.is_studio, pid=self.pid) == False) or self.end_tracking == True or (self.ended_process == True): self.ended_process = True; break
        def setRobloxEventCallback(self, eventName: robloxInstanceTotalLiteralEventNames, eventCallback: typing.Callable[[typing.Any], None]):
            if callable(eventCallback):
                if eventName in self.getAvailableEventNames():
                    for i in self.__events__:
                        if i and i["name"] == eventName: self.__events__.remove(i)
                    self.__events__.append({"name": eventName, "callback": eventCallback})
                    if self.watchdog_started == False: self.startActivityTracking()
        def addRobloxEventCallback(self, eventName: robloxInstanceTotalLiteralEventNames, eventCallback: typing.Callable[[typing.Any], None]):
            if callable(eventCallback):
                if eventName in self.getAvailableEventNames():
                    self.__events__.append({"name": eventName, "callback": eventCallback})
                    if self.watchdog_started == False: self.startActivityTracking()
        def getWindowsOpened(self) -> "list[Handler.RobloxWindow]":
            if self.pid and not (self.pid == "") and self.pid.isnumeric():
                try:
                    if main_os == "Windows":
                        system_windows = []
                        def callback(hwnd, _):
                            if win32gui.IsWindowVisible(hwnd):
                                _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
                                if window_pid == int(self.pid): system_windows.append(hwnd)
                        win32gui.EnumWindows(callback, None)
                        roblox_windows_classes = []
                        for i in system_windows: roblox_windows_classes.append(self.main_handler.RobloxWindow(self.pid, i, self.main_handler))
                        return roblox_windows_classes
                    elif main_os == "Darwin":
                        system_windows = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, 0)
                        app_windows = [win for win in system_windows if win.get("kCGWindowOwnerPID") == int(self.pid)]
                        new_set_of_system_windows = []
                        for win in app_windows:
                            if win and win.get("kCGWindowOwnerPID"): new_set_of_system_windows.append(win)
                        roblox_windows_classes = []
                        for i in new_set_of_system_windows: roblox_windows_classes.append(self.main_handler.RobloxWindow(self.pid, i, self.main_handler))
                        return roblox_windows_classes
                    else: return []
                except Exception as e: return []
            else: return []
        def clearRobloxEventCallbacks(self, eventName: robloxInstanceTotalLiteralEventNames=""):
            if eventName == "": self.__events__ = []
            else:
                for i in self.__events__:
                    if i and i["name"] == eventName: self.__events__.remove(i)
        def endInstance(self): 
            if self.is_studio == True: self.main_handler.endRobloxStudio(pid=self.pid)
            else: self.main_handler.endRoblox(pid=self.pid)
        def newestFile(self, path: str):
            files = os.listdir(path)
            paths = []
            for basename in files:
                if self.is_studio == False and "Player" in basename: paths.append(os.path.join(path, basename))
                elif self.is_studio == True and "Studio" in basename: paths.append(os.path.join(path, basename))
            if len(paths) > 0: return max(paths, key=os.path.getctime)
        def getAvailableEventNames(self):
            if self.is_studio == True: return self.main_handler.roblox_studio_event_names
            else: return self.main_handler.roblox_player_event_names
        def fileCreatedRecently(self, file_path: str):
            try:
                creation_time = os.path.getctime(file_path)
                current_time = time.time()
                if (current_time - creation_time) <= 10: return True
                else: return False
            except: return False
        def getLatestLogFile(self):
            logs_path = None
            if main_os == "Darwin": logs_path = os.path.join(user_folder, "Library", "Logs", "Roblox")
            elif main_os == "Windows": logs_path = os.path.join(windows_dir, "logs")
            else: logs_path = os.path.join(windows_dir, "logs")
            makedirs(logs_path)
            main_log = self.newestFile(logs_path)
            if not main_log: time.sleep(0.5); return self.getLatestLogFile()
            if not main_log.endswith(".log"): time.sleep(0.5); return self.getLatestLogFile()
            logs_attached = []
            if os.path.exists(os.path.join(logs_path, "RFFILogFiles.json")):
                with open(os.path.join(logs_path, "RFFILogFiles.json"), "r", encoding="utf-8") as f: logs_attached = json.load(f)
            if self.await_log_creation == True:
                if self.await_log_creation_attempts < 40:
                    if self.fileCreatedRecently(main_log):
                        if main_log in logs_attached:
                            time.sleep(0.5)
                            self.await_log_creation_attempts += 1
                            if self.debug_mode == True: printDebugMessage(f"Log file is already used in an another Roblox Instance ({self.await_log_creation_attempts}/40)")
                            return self.getLatestLogFile()
                        else:
                            logs_attached.append(main_log)
                            with open(os.path.join(logs_path, "RFFILogFiles.json"), "w", encoding="utf-8") as f: json.dump(logs_attached, f, indent=4)
                            if self.debug_mode == True: printDebugMessage(f"Successfully found log file ({self.await_log_creation_attempts}/40). Returning with: {main_log}")
                            return main_log
                    else:
                        time.sleep(0.5)
                        self.await_log_creation_attempts += 1
                        if self.debug_mode == True: printDebugMessage(f"Awaiting Log Creation ({self.await_log_creation_attempts}/40)")
                        return self.getLatestLogFile()
                else:
                    logs_attached.append(main_log)
                    with open(os.path.join(logs_path, "RFFILogFiles.json"), "w", encoding="utf-8") as f: json.dump(logs_attached, f, indent=4)
                    if self.debug_mode == True: printDebugMessage(f"Unable to find a new file within 20 seconds ({self.await_log_creation_attempts}/40). Returning with: {main_log}")
                    return main_log
            else:
                if self.debug_mode == True: printDebugMessage(f"Successfully found log file. Returning with: {main_log}")
                return main_log
        def cleanLogs(self):
            if self.debug_mode == True: printDebugMessage(f"Cleaning logs from session..")
            with open(self.log_file, "r", encoding="utf-8", errors="ignore") as file: lines = file.readlines()
            with open(self.log_file, "w", encoding="utf-8", errors="ignore") as write_file:
                end_lines = []
                current_log = ""
                for line in lines:
                    should_remove = False
                    f_index = line.find("[F")
                    if f_index != -1:
                        filtered_line = line[f_index:]
                        if filtered_line == current_log or "[FLog::WndProcessCheck]" in line or "[FLog::FMOD] FMOD API error" in line: should_remove = True
                        else: current_log = filtered_line
                    if should_remove == False: end_lines.append(line)
                write_file.writelines(end_lines)
        def handleLogLine(self, line: str=""):
            if self.is_studio == True:
                if "[FLog::Output] LoadClientSettingsFromLocal" in line: self.submitEvent(eventName="onLoadedFFlags", data=line, isLine=True)
                elif "[FLog::Output] ! Joining game" in line:
                    def generate_arg():
                        pattern = r"'([a-f0-9-]+)' place (\d+) at (\d+)"
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
                    if generated_data: self.submitEvent(eventName="onPlayTestStart", data=generated_data, isLine=False)
                elif "[FLog::TeamCreateJoinPayload] Joining game" in line:
                    def generate_arg():
                        pattern = r"([a-f0-9-]+) place (\d+) at [(\d+\.\d+\.\d+\.\d+)]:(\d+)"
                        match = re.search(pattern, line)
                        if match:
                            jobId = match.group(1)
                            placeId = match.group(2)
                            ip_address = match.group(3)
                            port = match.group(4)
                            return {
                                "jobId": jobId,
                                "placeId": placeId,
                                "ip": ip_address,
                                "port": port
                            }   
                        return None
                    
                    generated_data = generate_arg()
                    if generated_data: self.submitEvent(eventName="onJoiningTeam", data=generated_data, isLine=False)
                elif "[FLog::Output] Saved channel" in line:
                    def generate_arg():
                        pattern = re.compile(r"(?P<timestamp>[^\s]+),(?P<unknown_value>[^\s]+),(?P<unknown_hex>[^\s]+),(?P<unknown_number>[^\s]+) \[FLog::Output\] Saved channel '(?P<channel>[^']*)' to '(?P<name>[^']*)' for baseUrl '(?P<baseUrl>[^']*)'")
                        match = pattern.search(line)
                        if not match: return None
                        data = match.groupdict()
                        result = {
                            "channel": data.get("channel"),
                            "name": data.get("name"),
                            "baseUrl": data.get("baseUrl")
                        }
                        if result["channel"] == "production" or result["channel"] == "": result["channel"] = "LIVE"
                        return result
                    generated_data = generate_arg()
                    if generated_data: self.submitEvent(eventName="onSaveRobloxChannel", data=generated_data, isLine=False); self.submitEvent(eventName="onUserLogin", data=None, isLine=False)
                elif "[FLog::Output] Web returned cloud plugins:" in line:
                    def generate_arg():
                        match = re.search(r'\[([\d,\s]+)\]', line)
                        if not match: return None
                        else: return list(map(int, match.group(1).split(',')))
                    generated_data = generate_arg()
                    if generated_data: self.submitEvent(eventName="onCloudPlugins", data=generated_data, isLine=False)
                elif "[FLog::Output] UpdateUtils::requestInstallerUpdate - Launching Installer for update:" in line: self.submitEvent(eventName="onStudioInstallerLaunched", data=line, isLine=True)
                elif "[FLog::Output] Connecting to UDMUX server" in line:
                    def generate_arg():
                        pattern = re.compile(
                            r'(?P<timestamp>[^\s]+),(?P<unknown_value>[^\s]+),(?P<unknown_hex>[^\s]+),(?P<unknown_number>[^\s]+) \[FLog::Output\] Connecting to UDMUX server (?P<udmux_address>[^\s]+):(?P<udmux_port>[^\s]+), and RCC Server (?P<rcc_address>[^\s]+):(?P<rcc_port>[^\s]+)'
                        )
                        match = pattern.search(line)
                        if not match: return None
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
                        self.submitEvent(eventName="onGameUDMUXLoaded", data=generated_data, isLine=False)
                        self.submitEvent(eventName="onGameJoined", data={
                            "ip": generated_data["connected_address"],
                            "port": generated_data["connected_port"]
                        }, isLine=False)
                elif "[FLog::Output] Connecting to " in line:
                    def generate_arg():
                        pattern = re.compile(
                            r'(?P<timestamp>[^\s]+),(?P<unknown_value>[^\s]+),(?P<unknown_hex>[^\s]+),(?P<unknown_number>[^\s]+) \[FLog::Output\] Connecting to (?P<udmux_address>[^\s]+):(?P<udmux_port>[^\s]+)'
                        )
                        match = pattern.search(line)
                        if not match: return None
                        data = match.groupdict()
                        result = {
                            "connected_address": data.get("udmux_address"),
                            "connected_port": int(data.get("udmux_port"))
                        }
                        return result
                    
                    generated_data = generate_arg()
                    if generated_data:
                        if not (generated_data["connected_address"] == "127.0.0.1"):
                            self.submitEvent(eventName="onGameUDMUXLoaded", data=generated_data, isLine=False)
                            self.submitEvent(eventName="onGameJoined", data={
                                "ip": generated_data["connected_address"],
                                "port": generated_data["connected_port"]
                            }, isLine=False)
                elif "[FLog::Output] About to exit the application, doing cleanup." in line:
                    if self.roblox_starter_launched == False:
                        self.submitEvent(eventName="onRobloxExit", data=line)
                        self.submitEvent(eventName="onRobloxSharedLogLaunch", data=line)
                        return self.main_handler.WatchdogLineResponse.EndWatchdog()
                    else: self.submitEvent(eventName="onRobloxLauncherDestroyed", data=line)
                elif "[FLog::Output] [BloxstrapRPC]" in line:
                    def generate_arg():
                        json_start_index = line.find('[BloxstrapRPC]') + len('[BloxstrapRPC] ')
                        if json_start_index == -1: return None
                        json_str = line[json_start_index:].strip()
                        try: return json.loads(json_str)
                        except json.JSONDecodeError as e:
                            if self.debug_mode == True: printDebugMessage(str(e))
                            return None
                    generated_data = generate_arg()
                    if generated_data: self.submitEvent(eventName="onBloxstrapSDK", data=generated_data, isLine=False)
                elif "RobloxAudioDevice::StopRecording" in line: self.submitEvent(eventName="onRobloxAudioDeviceStopRecording", data=line, isLine=True)
                elif "RobloxAudioDevice::StartRecording" in line: self.submitEvent(eventName="onRobloxAudioDeviceStartRecording", data=line, isLine=True)
                elif "[FLog::Output]" in line:
                    def generate_arg():
                        output = line.find('[FLog::Output]') + len('[FLog::Output] ')
                        if output == -1: return None
                        return line[output:].strip()
                    generated_data = generate_arg()
                    if generated_data: self.submitEvent(eventName="onGameLog", data=generated_data, isLine=False)
                elif "[FLog::Error] Redundant Flag ID:" in line:
                    def generate_arg():
                        pattern = r"Redundant Flag ID:\s+([\w\d_]+)"
                        match = re.search(pattern, line)
                        if not match: return None
                        else:
                            result = {
                                "flag_id": match.group(1)
                            }
                            return result
                    generated_data = generate_arg()
                    if generated_data: self.submitEvent(eventName="onExpiredFlag", data=generated_data, isLine=False)
                elif "[FLog::Error]" in line:
                    def generate_arg():
                        output = line.find('[FLog::Error]') + len('[FLog::Error] ')
                        if output == -1: return None
                        return line[output:].strip()
                    generated_data = generate_arg()
                    if generated_data: self.submitEvent(eventName="onGameError", data=generated_data, isLine=False)
                elif "[FLog::Warning]" in line:
                    def generate_arg():
                        output = line.find('[FLog::Warning]') + len('[FLog::Warning] ')
                        if output == -1: return None
                        return line[output:].strip()
                    generated_data = generate_arg()
                    if generated_data: self.submitEvent(eventName="onGameWarning", data=generated_data, isLine=False)
                elif "[FLog::StudioKeyEvents] open place" in line:
                    def generate_arg():
                        pattern = r"identifier\s*=\s*(\/[^\)\s]+|\d+)"
                        match = re.search(pattern, line)
                        if not match:
                            pattern = r"(?:[a-zA-Z]:\\|\/)(?:[^\/\\\n]+[\/\\])*[^\/\\\n]+"
                            match = re.findall(pattern, line)
                            if len(match) < 1: return None
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
                    if generated_data: self.submitEvent(eventName="onOpeningGame", data=generated_data, isLine=False)
                elif "[FLog::RobloxIDEDoc] RobloxIDEDoc::doClose" in line: self.submitEvent(eventName="onClosingGame", data=line, isLine=True); self.connected_to_game = False
                elif "[telemetryLog] TaskNames: " in line and "OpenPlaceSuccess" in line: self.submitEvent(eventName="onGameLoaded", data=line, isLine=True); self.connected_to_game = True
                elif "[FLog::TeamCreateManager] Disconnected due to Lost connection to the game server, please reconnect" in line: self.submitEvent(eventName="onLostConnection", data=line, isLine=True); self.connected_to_game = False
                elif "[FLog::StudioKeyEvents] starting Qt main event loop" in line: self.submitEvent(eventName="onRobloxAppStart", data=line, isLine=True)
                elif "[FLog::StudioKeyEvents] login [end][success]" in line: self.submitEvent(eventName="onStudioLoginSuccess", data=line, isLine=True)
                elif "[FLog::StudioKeyEvents] launching new studio instance" in line: self.submitEvent(eventName="onNewStudioLaunching", data=line, isLine=True)
                elif "[FLog::StudioKeyEvents] team create connect (connection accepted)" in line: self.submitEvent(eventName="onTeamCreateConnect", data=line, isLine=True)
                elif "[FLog::StudioKeyEvents] team create disconnect" in line: self.submitEvent(eventName="onTeamCreateDisconnect", data=line, isLine=True)
                elif "[DFLog::HttpTraceError] HttpResponse(" in line:
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
                            else: return None
                        except Exception as e: return None                 
                    generated_data = generate_arg()
                    if generated_data: self.submitEvent(eventName="onHttpResponse", data=generated_data, isLine=False)
                    else: self.submitEvent(eventName="onHttpResponse", data=line, isLine=True)
                elif "[FLog::BetaFeatures] Applying settings for beta feature id" in line:
                    def generate_arg():
                        pattern = r"beta feature id (\w+)"
                        match = re.search(pattern, line)
                        if not match: return None
                        else:
                            result = {
                                "feature_id": match.group(1)
                            }
                            return result
                    generated_data = generate_arg()
                    if generated_data: self.submitEvent(eventName="onApplyingFeature", data=generated_data, isLine=False)
                elif "[FLog::ClientRunInfo] The channel is " in line:
                    def generate_arg():
                        pattern = re.compile(r'(?P<timestamp>[^\s]+),(?P<unknown_value>[^\s]+),(?P<unknown_hex>[^\s]+),(?P<unknown_number>[^\s]+) \[FLog::ClientRunInfo\] The channel is (?P<channel>[^\s]+)')
                        match = pattern.search(line)
                        if not match: return None
                        data = match.groupdict()
                        result = {
                            "channel": data.get("channel")
                        }
                        if result["channel"] == "production": result["channel"] = "LIVE"
                        return result
                    generated_data = generate_arg()
                    if generated_data:
                        self.submitEvent(eventName="onRobloxChannel", data=generated_data, isLine=False)
                        self.roblox_starter_launched = True
                elif "[FLog::Audio] InputDevice" in line:
                    def generate_arg():
                        pattern = re.compile(r'(?P<timestamp>[^\s]+),(?P<unknown_value>[^\s]+),(?P<unknown_hex>[^\s]+),(?P<unknown_number>[^\s]+) \[FLog::Audio\] InputDevice (?P<device_index>\d+): (?P<device_name>[^()]+)\(\{(?P<device_id>[0-9a-fA-F-]+)\}\) (?P<connections>\d+/\d+/\d+)')
                        match = pattern.search(line)
                        if not match: return None
                        data = match.groupdict()
                        result = {
                            "device_name": data.get("device_name"),
                            "device_uuid": data.get("device_id"),
                            "device_index": int(data.get("device_index")),
                            "connection_divisons": data.get("connections")
                        }
                        return result
                    generated_data = generate_arg()
                    if generated_data: self.submitEvent(eventName="onGameAudioDeviceAvailable", data=generated_data, isLine=False)
                elif "[FLog::PluginLoadingEnhanced] Running plugin" in line:
                    def generate_arg():
                        pattern = r"plugin '([\w\d_]+)'\s+in datamodel (\w+)"
                        match = re.search(pattern, line)
                        if not match: return None
                        else:
                            result = {
                                "plugin_id": match.group(1),
                                "datamodel": match.group(2),
                            }
                            return result
                    generated_data = generate_arg()
                    if generated_data: self.submitEvent(eventName="onPluginLoading", data=generated_data, isLine=False)
                elif "[FLog::PluginLoadingEnhanced] Unloading plugin" in line:
                    def generate_arg():
                        pattern = r"plugin '([\w\d_]+)'\s+in datamodel (\w+)"
                        match = re.search(pattern, line)
                        if not match: return None
                        else:
                            result = {
                                "plugin_id": match.group(1),
                                "datamodel": match.group(2),
                            }
                            return result
                    generated_data = generate_arg()
                    if generated_data: self.submitEvent(eventName="onPluginUnloading", data=generated_data, isLine=False)
                elif "[FLog::StudioTimingLog] ======== Studio Publish Place Times =======" in line: self.submitEvent(eventName="onRobloxPublishing", data=line, isLine=True)
                elif "[FLog::StudioTimingLog] ======== Studio Save To Cloud Times =======" in line: self.submitEvent(eventName="onRobloxSaved", data=line, isLine=True)
                elif "RBXCRASH:" in line or "[FLog::CrashReportLog] Terminated" in line: self.submitEvent(eventName="onRobloxCrash", data=line, isLine=True)
                elif "[FLog::WindowsLuaApp] Application did receive notification, type(DID_LOG_IN" in line: self.submitEvent(eventName="onUserLogin", data=None, isLine=False)
                elif "[FLog::Network] Client:Disconnect" in line:
                    if self.disconnect_cooldown == False:
                        self.disconnect_cooldown = True
                        def b():
                            time.sleep(3)
                            self.disconnect_cooldown = False
                        threading.Thread(target=b, daemon=True).start()
                        self.submitEvent(eventName="onPlayTestDisconnected", data=None, isLine=False)
                elif "[telemetryLog]" in line:
                    def generate_arg():
                        output = line.find('[telemetryLog]') + len('[telemetryLog] ')
                        if output == -1: return None
                        return line[output:].strip()
                    generated_data = generate_arg()
                    if generated_data: self.submitEvent(eventName="onTelemetryLog", data=generated_data, isLine=False)
                else: self.submitEvent(eventName="onOtherRobloxLog", data=line, isLine=True)
            else:
                if "[FLog::Output] ! Joining game" in line:
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
                    if generated_data: self.submitEvent(eventName="onGameStart", data=generated_data, isLine=False); self.connected_to_game = True
                elif "[FLog::Output] [BloxstrapRPC]" in line:
                    def generate_arg():
                        json_start_index = line.find('[BloxstrapRPC]') + len('[BloxstrapRPC] ')
                        if json_start_index == -1: return None
                        json_str = line[json_start_index:].strip()
                        try: return json.loads(json_str)
                        except json.JSONDecodeError as e:
                            if self.debug_mode == True: printDebugMessage(str(e))
                            return None
                    generated_data = generate_arg()
                    if generated_data: self.submitEvent(eventName="onBloxstrapSDK", data=generated_data, isLine=False)
                elif "[FLog::Output] Saved channel" in line:
                    def generate_arg():
                        pattern = re.compile(r"(?P<timestamp>[^\s]+),(?P<unknown_value>[^\s]+),(?P<unknown_hex>[^\s]+),(?P<unknown_number>[^\s]+) \[FLog::Output\] Saved channel '(?P<channel>[^']*)' to '(?P<name>[^']*)' for baseUrl '(?P<baseUrl>[^']*)'")
                        match = pattern.search(line)
                        if not match: return None
                        data = match.groupdict()
                        result = {
                            "channel": data.get("channel"),
                            "name": data.get("name"),
                            "baseUrl": data.get("baseUrl")
                        }
                        if result["channel"] == "production" or result["channel"] == "": result["channel"] = "LIVE"
                        return result
                    generated_data = generate_arg()
                    if generated_data: self.submitEvent(eventName="onSaveRobloxChannel", data=generated_data, isLine=False); self.submitEvent(eventName="onUserLogin", data=None, isLine=False)
                elif "[FLog::Output] LoadClientSettingsFromLocal" in line: self.submitEvent(eventName="onLoadedFFlags", data=line, isLine=True)
                elif "RobloxAudioDevice::SetMicrophoneMute true" in line: self.submitEvent(eventName="onRobloxVoiceChatMute", data=line, isLine=True)
                elif "RobloxAudioDevice::SetMicrophoneMute false" in line: self.submitEvent(eventName="onRobloxVoiceChatUnmute", data=line, isLine=True)
                elif "VoiceChatSession::leave" in line and "leaveRequested:1" in line: self.submitEvent(eventName="onRobloxVoiceChatLeft", data=line, isLine=True)
                elif "VoiceChatSession::publishStart - JoinProfiling" in line: self.submitEvent(eventName="onRobloxVoiceChatStart", data=line, isLine=True)
                elif "RobloxAudioDevice::StopRecording" in line: self.submitEvent(eventName="onRobloxAudioDeviceStopRecording", data=line, isLine=True)
                elif "RobloxAudioDevice::StartRecording" in line: self.submitEvent(eventName="onRobloxAudioDeviceStartRecording", data=line, isLine=True)
                elif "raiseTeleportInitFailedEvent" in line: self.submitEvent(eventName="onGameTeleportFailed", data=line, isLine=True)
                elif "[FLog::Output]" in line:
                    def generate_arg():
                        output = line.find('[FLog::Output]') + len('[FLog::Output] ')
                        if output == -1: return None
                        return line[output:].strip()
                    generated_data = generate_arg()
                    if generated_data: self.submitEvent(eventName="onGameLog", data=generated_data, isLine=False)
                elif "[FLog::Error]" in line:
                    def generate_arg():
                        output = line.find('[FLog::Error]') + len('[FLog::Error] ')
                        if output == -1: return None
                        return line[output:].strip()
                    generated_data = generate_arg()
                    if generated_data: self.submitEvent(eventName="onGameError", data=generated_data, isLine=False)
                elif "[FLog::Warning]" in line:
                    def generate_arg():
                        output = line.find('[FLog::Warning]') + len('[FLog::Warning] ')
                        if output == -1: return None
                        return line[output:].strip()
                    generated_data = generate_arg()
                    if generated_data: self.submitEvent(eventName="onGameWarning", data=generated_data, isLine=False)
                if "[FLog::RobloxStarter] RobloxStarter destroyed" in line:
                    if self.roblox_starter_launched == False:
                        self.submitEvent(eventName="onRobloxExit", data=line)
                        self.submitEvent(eventName="onRobloxSharedLogLaunch", data=line)
                        return self.main_handler.WatchdogLineResponse.EndWatchdog()
                    else: self.submitEvent(eventName="onRobloxLauncherDestroyed", data=line)
                elif "[FLog::UpdateController] Update check thread: updateRequired FALSE" in line: self.submitEvent(eventName="onRobloxPassedUpdate", data=line)
                elif "[FLog::SingleSurfaceApp] initializeWithAppStarter" in line: self.submitEvent(eventName="onRobloxAppStart", data=line)
                elif "[FLog::SingleSurfaceApp] launchUGCGameInternal" in line: self.submitEvent(eventName="onGameLoading", data=line, isLine=True)
                elif "[FLog::GameJoinUtil] GameJoinUtil::initiateTeleportToPlace" in line:
                    url_start = line.find("URL: ") + len("URL: ")
                    body_start = line.find("BODY: ")
                    url = line[url_start:body_start].strip()
                    body_json_str = line[body_start + len("BODY: "):].strip()
                    try: body = json.loads(body_json_str)
                    except json.JSONDecodeError as e: body = None
                    generated_data = {"url": url, "data": body}
                    if generated_data: self.submitEvent(eventName="onGameLoadingNormal", data=generated_data, isLine=False)
                elif "[DFLog::SignalRCoreError] ID: " in line and "Disconnected - Websocket error: Failed ws recv" in line: 
                    def generate_arg():
                        pattern = re.compile(r"(?P<timestamp>[^\s]+),(?P<unknown_value>[^\s]+),(?P<unknown_hex>[^\s]+),(?P<unknown_number>[^\s]+) \[DFLog::SignalRCoreError\] ID: (?P<id_number>[^']*) Disconnected - Websocket error: (?P<error_message_1>[^']*) - err: (?P<error_message_2>[^']*)")
                        match = pattern.search(line)
                        if not match: return None
                        data = match.groupdict()
                        if not data.get("id_number").isnumeric(): return None
                        result = {
                            "id": int(data.get("id_number")),
                            "err_message_1": data.get("error_message_1"),
                            "err_message_2": data.get("error_message_2")
                        }
                        return result
                    generated_data = generate_arg()
                    if generated_data: self.submitEvent(eventName="onWebSocketFailing", data=generated_data, isLine=False)
                elif "[FLog::GameJoinUtil] GameJoinUtil::joinGamePostPrivateServer" in line:
                    url_start = line.find("URL: ") + len("URL: ")
                    body_start = line.find("BODY: ")
                    url = line[url_start:body_start].strip()
                    body_json_str = line[body_start + len("BODY: "):].strip()
                    try: body = json.loads(body_json_str)
                    except json.JSONDecodeError as e: body = None
                    generated_data = {"url": url, "data": body}
                    if generated_data: self.submitEvent(eventName="onGameLoadingPrivate", data=generated_data, isLine=False)
                elif "[FLog::GameJoinUtil] GameJoinUtil::initiateTeleportToReservedServer" in line:
                    url_start = line.find("URL: ") + len("URL: ")
                    body_start = line.find("Body: ")
                    url = line[url_start:body_start].strip()
                    body_json_str = line[body_start + len("Body: "):].strip()
                    try: body = json.loads(body_json_str)
                    except json.JSONDecodeError as e: body = None
                    generated_data = {"url": url, "data": body}
                    if generated_data: self.submitEvent(eventName="onGameLoadingReserved", data=generated_data, isLine=False)
                elif "[FLog::WindowsLuaApp] Application did receive notification, type(DID_LOG_IN" in line: self.submitEvent(eventName="onUserLogin", data=None, isLine=False)
                elif "[FLog::Network] UDMUX Address = " in line:
                    def generate_arg():
                        pattern = re.compile(r'(?P<timestamp>[^\s]+),(?P<unknown_value>[^\s]+),(?P<unknown_hex>[^\s]+),(?P<unknown_number>[^\s]+) \[FLog::Network\] UDMUX Address = (?P<udmux_address>[^\s]+), Port = (?P<udmux_port>[^\s]+) \| RCC Server Address = (?P<rcc_address>[^\s]+), Port = (?P<rcc_port>[^\s]+)')
                        match = pattern.search(line)
                        if not match: return None
                        data = match.groupdict()
                        result = {
                            "connected_address": data.get("udmux_address"),
                            "connected_port": int(data.get("udmux_port")),
                            "connected_rcc_address": data.get("rcc_address"),
                            "connected_rcc_port": int(data.get("rcc_port"))
                        }
                        return result
                    generated_data = generate_arg()
                    if generated_data: self.submitEvent(eventName="onGameUDMUXLoaded", data=generated_data, isLine=False)
                elif "[FLog::Audio] InputDevice" in line:
                    def generate_arg():
                        pattern = re.compile(r'(?P<timestamp>[^\s]+),(?P<unknown_value>[^\s]+),(?P<unknown_hex>[^\s]+),(?P<unknown_number>[^\s]+) \[FLog::Audio\] InputDevice (?P<device_index>\d+): (?P<device_name>[^()]+)\(\{(?P<device_id>[0-9a-fA-F-]+)\}\) (?P<connections>\d+/\d+/\d+)')
                        match = pattern.search(line)
                        if not match: return None
                        data = match.groupdict()
                        result = {
                            "device_name": data.get("device_name"),
                            "device_uuid": data.get("device_id"),
                            "device_index": int(data.get("device_index")),
                            "connection_divisons": data.get("connections")
                        }
                        return result
                    generated_data = generate_arg()
                    if generated_data: self.submitEvent(eventName="onGameAudioDeviceAvailable", data=generated_data, isLine=False)
                elif "[FLog::ClientRunInfo] The channel is " in line:
                    def generate_arg():
                        pattern = re.compile(r'(?P<timestamp>[^\s]+),(?P<unknown_value>[^\s]+),(?P<unknown_hex>[^\s]+),(?P<unknown_number>[^\s]+) \[FLog::ClientRunInfo\] The channel is (?P<channel>[^\s]+)')
                        match = pattern.search(line)
                        if not match: return None
                        data = match.groupdict()
                        result = {"channel": data.get("channel")}
                        if result["channel"] == "production": result["channel"] = "LIVE"
                        return result
                    generated_data = generate_arg()
                    if generated_data:
                        self.submitEvent(eventName="onRobloxChannel", data=generated_data, isLine=False)
                        self.roblox_starter_launched = True
                elif "[FLog::Warning] WebLogin authentication is failed and App is quitting" in line or "[FLog::Warning] (RobloxPlayerAppDelegate) WebLogin authentication failure" in line or "[FLog::Error] fetch flag exception:" in line: self.submitEvent(eventName="onRobloxAppLoginFailed", data=line, isLine=True)
                elif "[FLog::UgcExperienceController] UgcExperienceController: doTeleport: joinScriptUrl" in line:
                    def generate_arg(json_str):
                        def fix_json_string(json_str):
                            try:
                                a = (json_str).replace(" ", "").replace("\n", "")
                                return json.loads(a)
                            except Exception as e: return None
                        def extract_ticket_info(ticket):
                            decoded_ticket = (urllib.parse.unquote(ticket)) + '}'
                            try:
                                ticket_json = fix_json_string(decoded_ticket)
                                if not ticket_json: raise Exception()
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
                                    if not ticket_json: raise Exception()
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
                                        if not ticket_json: raise Exception()
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
                                            if not ticket_json: raise Exception()
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
                                        except Exception as e: return None         
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
                                else: return json_obj
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
                        else:
                            return {
                                "placeId": None,
                                "jobId": None,
                                "username": None,
                                "userId": None,
                                "displayName": None,
                                "universeId": None,
                                "isTeleport": None,
                                "followUserId": None
                            }
                    generated_data = generate_arg(line)
                    if generated_data: self.submitEvent(eventName="onGameTeleport", data=generated_data, isLine=False)
                elif "[DFLog::HttpTraceError] HttpResponse(" in line:
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
                            else: return None
                        except Exception as e: return None
                        
                    generated_data = generate_arg()
                    if generated_data: self.submitEvent(eventName="onHttpResponse", data=generated_data, isLine=False)
                    else: self.submitEvent(eventName="onHttpResponse", data=line, isLine=True)
                elif '"partyId":' in line:
                    url_start = line.find("URL: ") + len("URL: ")
                    body_start = line.find("Body: ")
                    url = line[url_start:body_start].strip()
                    body_json_str = line[body_start + len("Body: "):].strip()
                    try: body = json.loads(body_json_str)
                    except json.JSONDecodeError as e: body = None
                    generated_data = {"url": url, "data": body}
                    if generated_data: self.submitEvent(eventName="onGameLoadingParty", data=generated_data, isLine=False)
                elif '"jobId":' in line:
                    def generate_arg(json_str):
                        def fix_json_string(json_str):
                            try:
                                a = (json_str).replace(" ", "").replace("\n", "")
                                return json.loads(a)
                            except Exception as e: return None
                        def extract_ticket_info(ticket):
                            decoded_ticket = (urllib.parse.unquote(ticket)) + '}'
                            try:
                                ticket_json = fix_json_string(decoded_ticket)
                                if not ticket_json: raise Exception()
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
                                    if not ticket_json: raise Exception()
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
                                        if not ticket_json: raise Exception()
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
                                            if not ticket_json: raise Exception()
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
                                        except Exception as e: return None              
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
                                else: return json_obj
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
                    except Exception as e: first_try = False
                    
                    if first_try == False:
                        generated_data = generate_arg(line)
                        if generated_data: self.submitEvent(eventName="onGameJoinInfo", data=generated_data, isLine=False)
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
                    if generated_data: self.submitEvent(eventName="onGameJoined", data=generated_data, isLine=False)
                elif "[FLog::SingleSurfaceApp] leaveUGCGameInternal" in line: self.submitEvent(eventName="onGameLeaving", data=line, isLine=True)
                elif "RBXCRASH:" in line or "[FLog::CrashReportLog] Terminated" in line: self.submitEvent(eventName="onRobloxCrash", data=line, isLine=True); self.connected_to_game = False
                elif "Roblox::terminateWaiter" in line: self.submitEvent(eventName="onRobloxTerminateInstance", data=line, isLine=True)
                elif "[FLog::AudioFocusManager] AudioFocusManager::AudioFocusManager() constructor" in line: self.audio_focused = True
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
                            if self.main_handler.disconnect_code_list.get(str(main_code)): code_message = self.main_handler.disconnect_code_list.get(str(main_code))
                            self.submitEvent(eventName="onGameDisconnected", data={"code": main_code, "message": code_message}, isLine=False); self.connected_to_game = False; self.validating_disconnect = True
                elif "[FLog::SingleSurfaceApp] destroyLuaApp: (stage:LuaApp) blocking:true." in line:
                    if self.validating_disconnect == False and self.audio_focused == False: return self.main_handler.WatchdogLineResponse.ReconnectWatchdog()
                    else: self.validating_disconnect = False
                else: self.submitEvent(eventName="onOtherRobloxLog", data=line, isLine=True)
            return self.main_handler.WatchdogLineResponse.NormalResponse()
        def submitEvent(self, eventName: str="onUnknownEvent", data: typing.Any=None, isLine: bool=True):
            if not (eventName == "onRobloxLog"): 
                self.submitEvent(eventName="onRobloxLog", data={"eventName": eventName, "data": data, "isLine": isLine}, isLine=False)
                if isLine == True:
                    if self.debug_mode == True and not (eventName == "onOtherRobloxLog" and self.allow_other_logs == False): printDebugMessage(f'Event triggered: {eventName}, Line: {data}')
                else:
                    if self.debug_mode == True: 
                        if type(data) is str and (data.startswith("Settings Date timestamp is") or data.startswith("Settings Date header was")):
                            if self.allow_other_logs == True: printDebugMessage(f'Event triggered: {eventName}, Data: {data}')
                        else: printDebugMessage(f'Event triggered: {eventName}, Data: {data}')
            for i in self.__events__:
                if i and callable(i.get("callback")) and i.get("name") == eventName: 
                    if self.one_threaded == True:
                        try: i.get("callback")(data)
                        except Exception as e: printErrorMessage(e)
                    else: threading.Thread(target=i.get("callback"), args=[data], daemon=self.daemon).start()
        def startActivityTracking(self):
            if self.watchdog_started == False:
                self.watchdog_started = True
                def watchDog():
                    time.sleep(0.5)
                    if main_os == "Darwin" or main_os == "Windows":
                        main_log = ""
                        passed_lines = []
                        if self.log_file == "":
                            self.await_log_creation_attempts = 0
                            main_log = self.getLatestLogFile()
                            self.log_file = main_log
                        else: main_log = self.log_file

                        with open(main_log, "r", encoding="utf-8", errors="ignore") as file:
                            self.loading_existing_logs = True
                            while True:
                                line = file.readline()
                                if not line:
                                    threading.Thread(target=self.cleanLogs).start()
                                    break
                                if self.ended_process == True:
                                    self.submitEvent(eventName="onRobloxExit", data=line)
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
                                                        res = self.handleLogLine(line)
                                                        if res:
                                                            if res.code == 0:
                                                                threading.Thread(target=self.cleanLogs).start()
                                                                break
                                                            elif res.code == 1:
                                                                self.ended_process = True
                                                                return
                                                            elif res.code == 2:
                                                                self.watchdog_started = False
                                                                self.log_file = ""
                                                                self.submitEvent("onWatchdogReconnection", None, isLine=False)
                                                                self.startActivityTracking()
                                                                return
                                            except Exception as e:
                                                if self.debug_mode == True: printDebugMessage(f"Unable to read log: {str(e)}")
                                    else:
                                        res = self.handleLogLine(line)
                                        if res:
                                            if res.code == 0:
                                                self.ended_process = True
                                                threading.Thread(target=self.cleanLogs).start()
                                                break     
                                            elif res.code == 1:
                                                self.ended_process = True
                                                return
                                            elif res.code == 2:
                                                self.watchdog_started = False
                                                self.log_file = ""
                                                self.submitEvent("onWatchdogReconnection", None, isLine=False)
                                                self.startActivityTracking()
                                                return 
                            self.loading_existing_logs = False
                            file.seek(0, os.SEEK_END)
                            while True:
                                line = file.readline()
                                if self.ended_process == True:
                                    self.submitEvent(eventName="onRobloxExit", data=line)
                                    threading.Thread(target=self.cleanLogs).start()
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
                                                    res = self.handleLogLine(line)
                                                    if res:
                                                        if res.code == 0:
                                                            self.ended_process = True
                                                            threading.Thread(target=self.cleanLogs).start()
                                                            break     
                                                        elif res.code == 1:
                                                            self.ended_process = True
                                                            return 
                                                        elif res.code == 2:
                                                            self.watchdog_started = False
                                                            self.log_file = ""
                                                            self.submitEvent("onWatchdogReconnection", None, isLine=False)
                                                            self.startActivityTracking()
                                                            return 
                                        else:
                                            res = self.handleLogLine(line)
                                            if res:
                                                if res.code == 0:
                                                    self.ended_process = True
                                                    threading.Thread(target=self.cleanLogs).start()
                                                    break     
                                                elif res.code == 1:
                                                    self.ended_process = True
                                                    return
                                                elif res.code == 2:
                                                    self.watchdog_started = False
                                                    self.log_file = ""
                                                    self.submitEvent("onWatchdogReconnection", None, isLine=False)
                                                    self.startActivityTracking()
                                                    return
                                    else:
                                        res = self.handleLogLine(line)
                                        if res:
                                            if res.code == 0:
                                                self.ended_process = True
                                                threading.Thread(target=self.cleanLogs).start()
                                                break     
                                            elif res.code == 1:
                                                self.ended_process = True
                                                return  
                                            elif res.code == 2:
                                                self.watchdog_started = False
                                                self.log_file = ""
                                                self.submitEvent("onWatchdogReconnection", None, isLine=False)
                                                self.startActivityTracking()
                                                return                         
                threading.Thread(target=watchDog, daemon=self.daemon).start()
                threading.Thread(target=self.awaitRobloxClosing, daemon=self.daemon).start()
        def requestThreadClosing(self): self.end_tracking = True
    class RobloxWindow():
        pid = None
        system_handler = None
        main_handler = None
        def __init__(self, pid: str, system_handler: str, main_handler):
            self.pid = pid
            self.system_handler = system_handler
            self.main_handler: Handler = main_handler
        def focusWindow(self):
            if main_os == "Windows": win32gui.SetFocus(self.system_handler)
            elif main_os == "Darwin": subprocess.run(["osascript", "-e", f'tell application "System Events" to set frontmost of (every process whose unix id is {self.pid}) to true'])
        def destroyWindow(self):
            if main_os == "Windows": win32gui.DestroyWindow(self.system_handler)
            elif main_os == "Darwin": self.main_handler.endRoblox(pid=str(self.pid))
        def setWindowTitle(self, title: str):
            if main_os == "Windows": win32gui.SetWindowText(self.system_handler, title)
            elif main_os == "Darwin": printLog("Setting Window Title is unavailable for macOS.")
        def setWindowIcon(self, icon: str, cache: bool=True):
            if main_os == "Windows":
                if not type(icon) is str or not icon.endswith(".ico"): raise Exception("This icon is not an ico file!")
                if not os.path.exists(icon): raise Exception("This icon doesn't exist!")
                if cache == True and self.main_handler.image_cache.get(f"setWindowIcon_{icon}"): Icon = self.main_handler.image_cache.get(f"setWindowIcon_{icon}")
                else:
                    Icon = win32gui.LoadImage(
                        None,
                        icon,
                        win32con.IMAGE_ICON,
                        128, 128,
                        win32con.LR_LOADFROMFILE
                    )
                if cache == True: self.main_handler.image_cache[f"setWindowIcon_{icon}"] = Icon
                win32gui.SendMessage(self.system_handler, win32con.WM_SETICON, win32con.ICON_SMALL, Icon)
                win32gui.SendMessage(self.system_handler, win32con.WM_SETICON, win32con.ICON_BIG, Icon)
            elif main_os == "Darwin": printLog("Setting Window Icons is unavailable for macOS.")
        def setWindowPositionAndSize(self, size_x: int, size_y: int, position_x: int, position_y: int):
            if main_os == "Windows": win32gui.SetWindowPos(self.system_handler, win32gui.HWND_TOP, size_x, size_y, position_x, position_y, win32gui.SWP_SHOWWINDOW)
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
                except Exception as e: printLog(f"Failed to execute AppleScript: {e}")
        def setWindowPosition(self, position_x: int, position_y: int):
            if main_os == "Windows": win32gui.SetWindowPos(self.system_handler, win32gui.HWND_TOP, None, None, position_x, position_y, win32gui.SWP_SHOWWINDOW)
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
                except Exception as e: printLog(f"Failed to execute AppleScript: {e}")
        def setWindowSize(self, size_x: int, size_y: int):
            if main_os == "Windows": win32gui.SetWindowPos(self.system_handler, win32gui.HWND_TOP, size_x, size_y, win32gui.SWP_SHOWWINDOW)
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
                except Exception as e: printLog(f"Failed to execute AppleScript: {e}")
        def getWindowPositionAndSize(self):
            if main_os == "Windows":
                x, y, x1, y1 = win32gui.GetWindowRect(self.system_handler)
                return (x, y), (x1 - x, y1 - y)
            elif main_os == "Darwin":
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
    def __init__(self): 
        self.__main_os__ = main_os
        if pip_class.getIfConnectedToInternet() == True:
            async def testResult(host: str, priority: int, executor: concurrent.futures.ThreadPoolExecutor):
                await asyncio.sleep(priority)
                def block_test(): return requests.get(f"https://{host}/versionStudio", timeout=5).text
                version_studio = await asyncio.get_event_loop().run_in_executor(executor, block_test)
                if version_studio == self.last_mfc_studio_version: return host
                else: raise ValueError(f"Hash mismatch from {host}: got {version_studio}")
            async def overall():
                exceptions = []
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    tasks = [asyncio.create_task(testResult(host, priority, executor)) for host, priority in self.roblox_download_locations.items()]
                    while tasks:
                        done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                        for i in done:
                            tasks.remove(i)
                            if i.cancelled(): continue
                            elif i.exception(): exceptions.append(i.exception())
                            else:
                                for t in tasks: t.cancel()
                                return i.result()
            def start_asyncio_loop(): self.optimal_download_location = asyncio.run(overall())
            if pip_class.pythonSupported(3, 11, 0): threading.Thread(target=start_asyncio_loop, daemon=True).start()
        else: self.optimal_download_location = "setup.rbxcdn.com"
    def endRoblox(self, studio: bool=False, pid: str=""):
        if self.getIfRobloxIsOpen(studio=studio, pid=pid):
            if pid == "":
                if studio == True:
                    if self.__main_os__ == "Darwin": subprocess.run(["/usr/bin/killall", "-9", "RobloxStudio"], stdout=subprocess.DEVNULL)
                    elif self.__main_os__ == "Windows": subprocess.run("taskkill /IM RobloxStudioBeta.exe /F", shell=True, stdout=subprocess.DEVNULL)
                    else: self.unsupportedFunction()
                else:
                    if self.__main_os__ == "Darwin": subprocess.run(["/usr/bin/killall", "-9", "RobloxPlayer"], stdout=subprocess.DEVNULL)
                    elif self.__main_os__ == "Windows": subprocess.run("taskkill /IM RobloxPlayerBeta.exe /F", shell=True, stdout=subprocess.DEVNULL)
                    else: self.unsupportedFunction()
            else:
                if self.__main_os__ == "Darwin": subprocess.run(f"kill -9 {pid}", shell=True, stdout=subprocess.DEVNULL)
                elif self.__main_os__ == "Windows": subprocess.run(f"taskkill /PID {pid} /F", shell=True, stdout=subprocess.DEVNULL)
                else: self.unsupportedFunction()
    def endRobloxCrashHandler(self, pid: str=""):
        if pid == "":
            if self.__main_os__ == "Darwin": subprocess.run(["/usr/bin/killall", "-9", "RobloxCrashHandler"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            elif self.__main_os__ == "Windows": subprocess.run("taskkill /IM RobloxCrashHandler.exe /F", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else: self.unsupportedFunction()
        else:
            if self.__main_os__ == "Darwin": subprocess.run(f"kill -9 {pid}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            elif self.__main_os__ == "Windows": subprocess.run(f"taskkill /PID {pid} /F", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else: self.unsupportedFunction()
    def getIfRobloxIsOpen(self, studio: bool=False, installer: bool=False, pid: str=""):
        if self.__main_os__ == "Windows":
            exe_file_name = ("RobloxStudioInstaller.exe" if installer else "RobloxStudioBeta.exe") if studio == True else ("RobloxPlayerInstaller.exe" if installer else "RobloxPlayerBeta.exe")
            if pid == "" or pid == None:
                for proc in psutil.process_iter(attrs=["name"]):
                    if proc.info["name"] == exe_file_name: return True
                return False
            else: 
                try: proc = psutil.Process(int(pid)); return proc.is_running() and proc.name() == exe_file_name
                except (psutil.NoSuchProcess, psutil.AccessDenied, ValueError): return False
        elif self.__main_os__ == "Darwin":
            if pid == "" or pid == None:
                if installer == False: return subprocess.run(["pgrep", "-f", f"{os.path.join(macOS_beforeClientServices, ('RobloxStudio' if studio == True else 'RobloxPlayer'))}"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).returncode == 0
                else: return subprocess.run(["pgrep", "-f", f"{os.path.join(macOS_beforeClientServices, ('RobloxStudioInstaller' if studio == True else 'RobloxPlayerInstaller'))}"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).returncode == 0
            else: return subprocess.run(["ps", "-p", f"{pid}"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).returncode == 0
        else:
            self.unsupportedFunction()
            return
    def getLatestClientVersion(self, studio: bool=False, debug: bool=False, channel: str="LIVE"):
        # Mac: https://clientsettingscdn.roblox.com/v2/client-version/MacPlayer | MacStudio
        # Windows: https://clientsettingscdn.roblox.com/v2/client-version/WindowsPlayer | WindowsStudio64 | WindowsStudio
        try:    
            if channel == "production": channel = "LIVE"
            if self.__main_os__ == "Darwin":
                if debug == True: printDebugMessage("Sending Request to Roblox Servers..") 
                if channel: res = requests.get(f"https://clientsettingscdn.roblox.com/v2/client-version/{'MacStudio' if studio == True else 'MacPlayer'}/channel/{channel}")
                else: res = requests.get(f"https://clientsettingscdn.roblox.com/v2/client-version/{'MacStudio' if studio == True else 'MacPlayer'}")
                if res.ok:
                    jso = res.json
                    if jso.get("clientVersionUpload") and jso.get("version"):
                        if debug == True: printDebugMessage(f"Called ({res.url}): {res.text}")
                        return {"success": True, "client_version": jso.get("clientVersionUpload"), "hash": jso.get("version"), "attempted_channel": channel or "LIVE"}
                    else:
                        if debug == True: printDebugMessage(f"Something went wrong: {res.text} | {res.status_code}")
                        return {"success": False, "message": "Something went wrong."}
                else:
                    if not (channel == "LIVE"):
                        if debug == True: printDebugMessage(f"Roblox rejected update check with channel {channel}, retrying as channel LIVE: {res.text}")
                        return self.getLatestClientVersion(studio=studio, debug=debug, channel="LIVE")
                    else:
                        if debug == True: printDebugMessage(f"Something went wrong: {res.text} | {res.status_code}")
                        return {"success": False, "message": "Something went wrong."}
            elif self.__main_os__ == "Windows":
                if debug == True: printDebugMessage("Sending Request to Roblox Servers..") 
                is32Bit = pip_class.getIf32BitWindows()
                if channel: res = requests.get(f"https://clientsettingscdn.roblox.com/v2/client-version/{('WindowsStudio' if is32Bit == True else 'WindowsStudio64') if studio == True else 'WindowsPlayer'}/channel/{channel}")
                else: res = requests.get(f"https://clientsettingscdn.roblox.com/v2/client-version/{('WindowsStudio' if is32Bit == True else 'WindowsStudio64') if studio == True else 'WindowsPlayer'}")
                if res.ok:
                    jso = res.json
                    if jso.get("clientVersionUpload") and jso.get("version"):
                        if debug == True: printDebugMessage(f"Called ({res.url}): {res.text}")
                        return {"success": True, "client_version": jso.get("clientVersionUpload"), "hash": jso.get("version"), "attempted_channel": channel or "LIVE"}
                    else:
                        if debug == True: printDebugMessage(f"Something went wrong: {res.text} | {res.status_code}")
                        return {"success": False, "message": "Something went wrong."}
                else:
                    if not (channel == "LIVE"):
                        if debug == True: printDebugMessage(f"Roblox rejected update check with channel {channel}, retrying as channel LIVE: {res.text}")
                        return self.getLatestClientVersion(studio=studio, debug=debug, channel="LIVE")
                    else:
                        if debug == True: printDebugMessage(f"Something went wrong: {res.text} | {res.status_code}")
                        return {"success": False, "message": "Something went wrong."}
            else:
                self.unsupportedFunction()
                return {"success": False, "message": "OS not compatible."}
        except Exception as e:
            if debug == True: printDebugMessage(str(e))
            return {"success": False, "message": "There was an error checking. Please check your internet connection!"}
    def getCurrentClientVersion(self, studio: bool=False):
        if self.__main_os__ == "Darwin":
            tar_dir = macOS_studioDir if studio == True else macOS_dir
            if os.path.exists(os.path.join(tar_dir, "Contents", "Info.plist")):
                read_plist = plist_class.readPListFile(os.path.join(tar_dir, "Contents", "Info.plist"))
                if read_plist.get("CFBundleShortVersionString"):
                    version_channel = "LIVE"
                    try:
                        if studio == True and os.path.exists(os.path.join(user_folder, "Library", "Preferences", "com.roblox.RobloxStudioChannel.plist")):
                            read_install_plist = plist_class.readPListFile(os.path.join(user_folder, "Library", "Preferences", "com.roblox.RobloxStudioChannel.plist"))
                            if read_install_plist.get("www.roblox.com") and not read_install_plist.get("www.roblox.com") == "": version_channel = read_install_plist.get("www.roblox.com", "LIVE")
                        elif os.path.exists(os.path.join(user_folder, "Library", "Preferences", "com.roblox.RobloxPlayerChannel.plist")):
                            read_install_plist = plist_class.readPListFile(os.path.join(user_folder, "Library", "Preferences", "com.roblox.RobloxPlayerChannel.plist"))
                            if read_install_plist.get("www.roblox.com") and not read_install_plist.get("www.roblox.com") == "": version_channel = read_install_plist.get("www.roblox.com", "LIVE")
                    except Exception: version_channel = "LIVE"
                    client_vers = None
                    if os.path.exists(os.path.join(tar_dir, "Contents", "MacOS", "RobloxVersion.json")):
                        with open(os.path.join(tar_dir, "Contents", "MacOS", "RobloxVersion.json"), "r", encoding="utf-8") as f: vers_js = json.load(f)
                        client_vers = vers_js.get("ClientVersion")
                    return {"success": True, "client_version": client_vers, "version": read_plist["CFBundleShortVersionString"], "channel": version_channel}
                else: return {"success": False, "message": "Something went wrong."}
            else: return {"success": False, "message": "Roblox not installed."}
        elif self.__main_os__ == "Windows":
            res = self.getRobloxInstallFolder(studio=studio)
            if res:
                version_channel = ""
                try:
                    registry_key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, r"Software\ROBLOX Corporation\Environments\RobloxStudio\Channel" if studio == True else r"Software\ROBLOX Corporation\Environments\RobloxPlayer\Channel", 0, win32con.KEY_READ)
                    value, regtype = win32api.RegQueryValueEx(registry_key, "www.roblox.com")
                    win32api.RegCloseKey(registry_key)
                    if value.replace(" ", "") == "":  version_channel = "LIVE"
                    else:
                        if value == "production": version_channel = "LIVE"
                        else: version_channel = value
                except Exception: version_channel = "LIVE"
                client_vers = os.path.basename(os.path.dirname(res))
                app_vers = None
                if os.path.exists(os.path.join(res, "RobloxVersion.json")):
                    with open(os.path.join(res, "RobloxVersion.json"), "r", encoding="utf-8") as f: vers_js = json.load(f)
                    client_vers = vers_js.get("ClientVersion")
                    app_vers = vers_js.get("AppVersion")
                return {"success": True, "client_version": client_vers, "version": app_vers, "channel": version_channel}
            else: return {"success": False, "message": "Roblox not installed."}
        else:
            self.unsupportedFunction()
            return {"success": False, "message": "OS not compatible."}
    def getRobloxInstallFolder(self, studio: bool=False, directory: str=""):
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
            else: return None
        elif self.__main_os__ == "Darwin": return f"{macOS_studioDir}/" if studio == True else f"{macOS_dir}/"
        else: self.unsupportedFunction()
    def getLatestOpenedRobloxPid(self, studio: bool=False):
        if self.__main_os__ == "Darwin":
            try:
                result = subprocess.run(["ps", "axo", "pid,etime,command"], stdout=subprocess.PIPE, text=True)
                processes = result.stdout
                roblox_lines = [line for line in processes.splitlines() if ("/MacOS/RobloxStudio" if studio == True else "/MacOS/RobloxPlayer") in line]
                if not roblox_lines: return None
                def sort_by_etime(line):
                    etime = line.split()[1]
                    parts = etime.split('-') if '-' in etime else [etime]
                    time_parts = parts[-1].split(':')
                    total_seconds = 0
                    if len(parts) > 1: total_seconds += int(parts[0]) * 86400
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
                program_lines = [line for line in processes.splitlines() if ("RobloxStudioBeta.exe" if studio == True else "RobloxPlayerBeta.exe") in line]
                if not program_lines:
                    return None
                latest_process = program_lines[-1]
                pid = latest_process.split()[1]
                return pid
            except Exception as e:
                printErrorMessage(f"Error occurred while getting Roblox Instance: {e}")
                return None
    def getOpenedRobloxPids(self, studio: bool=False):
        if self.__main_os__ == "Darwin":
            try:
                result = subprocess.run(["ps", "axo", "pid,etime,command"], stdout=subprocess.PIPE, text=True)
                processes = result.stdout
                roblox_lines = [line for line in processes.splitlines() if ("/MacOS/RobloxStudio" if studio == True else "/MacOS/RobloxPlayer") in line]
                if not roblox_lines: return None
                pid_list = []
                for i in roblox_lines: pid_list.append(i.split()[0])
                return pid_list
            except Exception as e:
                printErrorMessage(f"Error occurred while getting Roblox Instance: {e}")
                return None
        elif self.__main_os__ == "Windows":
            try:
                result = subprocess.Popen(["tasklist"], stdout=subprocess.PIPE, text=True)
                processes = result.stdout.read()
                program_lines = [line for line in processes.splitlines() if ("RobloxStudioBeta.exe" if studio == True else "RobloxPlayerBeta.exe") in line]
                if not program_lines: return None
                pid_list = []
                for i in program_lines: pid_list.append(i.split()[1])
                return pid_list
            except Exception as e:
                printErrorMessage(f"Error occurred while getting Roblox Instance: {e}")
                return None
    def getAllOpenedRobloxWindows(self, studio: bool=False) -> "list[RobloxWindow]":
        pids = self.getOpenedRobloxPids(studio=studio)
        generated_window_instances = []
        for i in pids:
            process_windows = pip_class.getProcessWindows(i)
            for e in process_windows: generated_window_instances.append(self.RobloxWindow(int(i), e, self))
        return generated_window_instances
    def getOpenedRobloxWindows(self, pid: str):
        generated_window_instance = None
        process_windows = pip_class.getProcessWindows(pid)
        for e in process_windows: generated_window_instance = self.RobloxWindow(int(pid), e, self)
        return generated_window_instance
    def getRobloxAppSettings(self):
        appStorage = {}
        if self.__main_os__ == "Darwin":
            try:
                if os.path.exists(os.path.join(user_folder, "Library", "Roblox", "LocalStorage", "appStorage.json")): appStorage = json.load(open(os.path.join(user_folder, "Library", "Roblox", "LocalStorage", "appStorage.json"), "r", encoding="utf-8"))
            except Exception: appStorage = {}
        elif self.__main_os__ == "Windows":
            try:
                if os.path.exists(os.path.join(windows_dir, "LocalStorage", "appStorage.json")): appStorage = json.load(open(os.path.join(windows_dir, "LocalStorage", "appStorage.json"), "r", encoding="utf-8"))
            except Exception: appStorage = {}
        else:
            self.unsupportedFunction()
            return {"success": False, "message": "OS not compatible."}
        return {
            "success": True, 
            "loggedInUser": {
                "id": int(appStorage.get("UserId")) if (type(appStorage.get("UserId")) is str and appStorage.get("UserId").isnumeric()) else None,
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
            "appConfiguration": json.loads(appStorage.get("AppConfiguration")) if appStorage.get("AppConfiguration") else {},
            "experimentCache": json.loads(appStorage.get("ExperimentCache")) if appStorage.get("ExperimentCache") else {},
            "policyServiceResponse": json.loads(appStorage.get("PolicyServiceHttpResponse")) if appStorage.get("PolicyServiceHttpResponse") else {}
        }
    def getRobloxGlobalBasicSettings(self, studio: bool=False):
        roblox_app_location = ""
        if self.__main_os__ == "Darwin": roblox_app_location = os.path.join(user_folder, "Library", "Roblox")
        elif self.__main_os__ == "Windows": roblox_app_location = windows_dir
        else:
            self.unsupportedFunction()
            return {"success": False, "message": "OS not compatible."}   
        def convertToBestValue(value: str):
            if value == None: return None
            if value.lower() == "true": return True
            elif value.lower() == "false": return False
            try:
                if "." in value: return float(value)
                return int(value)
            except ValueError: return value 
        file_name = None
        for i in os.listdir(roblox_app_location):
            if not (i.find("GlobalBasicSettings") == -1):
                if studio == True and i.find("_Studio") == -1: continue
                file_name = i
        if file_name:
            with open(os.path.join(roblox_app_location, file_name), "r", encoding="utf-8") as f: xml_contents = f.read()
            xml_root = ET.fromstring(xml_contents)
            final_settings = {}
            for prop in xml_root.findall(".//Properties/*"):
                prop_key = prop.get("name")
                if prop.tag == "Vector2": final_settings[prop_key] = {"type": prop.tag, "data": (convertToBestValue(prop.find("X").text), convertToBestValue(prop.find("Y").text))}
                else: final_settings[prop_key] = {"type": prop.tag, "data": convertToBestValue(prop.text)}
            return {"success": True, "data": final_settings}
        else: return {"success": False, "message": "Unable to find settings file."} 
    def getBestRobloxDownloadServer(self): return self.optimal_download_location
    def getLatestRobloxAppSettings(self, studio: bool=False, debug: bool=False, bootstrapper: bool=False, bucket: str=""):
        # Mac: https://clientsettingscdn.roblox.com/v2/settings/application/MacDesktopPlayer | MacClientBootstrapper | MacStudioBootstrapper | MacStudioApp
        # Windows: https://clientsettingscdn.roblox.com/v2/settings/application/PCDesktopClient | PCClientBootstrapper | PCStudioBootstrapper | PCStudioApp
        try:    
            if bucket == "LIVE" or bucket == "production": bucket = ""
            if self.__main_os__ == "Darwin":
                if debug == True: printDebugMessage("Sending Request to Roblox Servers..") 
                res = requests.get(f"https://clientsettingscdn.roblox.com/v2/settings/application/{('MacStudioBootstrapper' if bootstrapper == True else 'MacStudioApp') if studio == True else ('MacClientBootstrapper' if bootstrapper == True else 'MacDesktopPlayer')}{f'/bucket/{bucket}' if not bucket == '' else ''}")
                if res.ok:
                    jso = res.json
                    if jso.get("applicationSettings"):
                        if debug == True: printDebugMessage(f"Successfully got application settings! URL: ({res.url})")
                        return {"success": True, "application_settings": jso.get("applicationSettings")}
                    else:
                        if debug == True: printDebugMessage(f"Something went wrong: {res.text} | {res.status_code}")
                        return {"success": False, "message": "Something went wrong."}
                else:
                    if debug == True: printDebugMessage(f"Something went wrong: {res.text} | {res.status_code}")
                    return {"success": False, "message": "Something went wrong."}
            elif self.__main_os__ == "Windows":
                if debug == True: printDebugMessage("Sending Request to Roblox Servers..") 
                res = requests.get(f"https://clientsettingscdn.roblox.com/v2/settings/application/{('PCStudioBootstrapper' if bootstrapper == True else 'PCStudioApp') if studio == True else ('PCClientBootstrapper' if bootstrapper == True else 'PCDesktopClient')}{f'/bucket/{bucket}' if not bucket == '' else ''}")
                if res.ok:
                    jso = res.json
                    if jso.get("applicationSettings"):
                        if debug == True: printDebugMessage(f"Successfully got application settings! URL: ({res.url})")
                        return {"success": True, "application_settings": jso.get("applicationSettings")}
                    else:
                        if debug == True: printDebugMessage(f"Something went wrong: {res.text} | {res.status_code}")
                        return {"success": False, "message": "Something went wrong."}
                else:
                    if debug == True: printDebugMessage(f"Something went wrong: {res.text} | {res.status_code}")
                    return {"success": False, "message": "Something went wrong."}
            else:
                self.unsupportedFunction()
                return {"success": False, "message": "OS not compatible."}
        except Exception as e:
            if debug == True: printDebugMessage(str(e))
            return {"success": False, "message": "There was an error checking. Please check your internet connection!"}
    def prepareMultiInstance(self, debug: bool=False, awaitRobloxClosure: bool=True, allowReattachment: bool=True):
        if self.__main_os__ == "Darwin":
            try:
                posix_ipc.unlink_semaphore("/RobloxPlayerUniq")
                if debug == True: printDebugMessage(f"Successfully unlinked semaphore to allow Roblox multi instance!")
                return True
            except posix_ipc.ExistentialError:
                if debug == True: printDebugMessage(f"Roblox Single Instance Semaphore does not exist. You may launch Roblox without any problems!")
                return True
        elif self.__main_os__ == "Windows":
            import ctypes.wintypes
            kernel32 = ctypes.windll.kernel32
            mutexes_events = [["ROBLOX_singletonEvent", b"ROBLOX_singletonEvent"], ["ROBLOX_SingletonEvent", b"ROBLOX_SingletonEvent"], ["ROBLOX_singletonMutex", b"ROBLOX_singletonMutex"]]
            is_created = False
            for mutex_names in mutexes_events:
                mutex_name = mutex_names[0]
                mutex_bytename = mutex_names[1]
                mutex = kernel32.OpenMutexA(0x1F0001, ctypes.wintypes.BOOL(True), mutex_bytename)
                mutex2 = kernel32.OpenMutexW(0x1F0001, ctypes.wintypes.BOOL(True), mutex_name)
                if not (mutex and mutex2): 
                    if allowReattachment == True:
                        if self.getIfRobloxIsOpen():
                            if debug == True: printDebugMessage(f"Reattaching mutexes under name: {mutex_name}.")
                            self.endRoblox()
                    else:
                        if mutex: kernel32.CloseHandle(mutex)
                        if mutex2: kernel32.CloseHandle(mutex2)
                        if debug == True: printDebugMessage("Unable to attach to mutex because it's already created by Roblox or by an another script.")
                        return False
                    def hold_mutex(mu_name):
                        mutexW = kernel32.CreateMutexW(None, ctypes.wintypes.BOOL(True), mu_name)
                        if mutexW:
                            try:
                                if awaitRobloxClosure == True:
                                    while self.getIfRobloxIsOpen(): time.sleep(1)
                                else:
                                    while True: time.sleep(1)
                            except Exception as e: 
                                if debug == True: printDebugMessage(f"There was an error holding mutex W: {str(e)}")
                            finally: kernel32.ReleaseMutex(mutexW)
                        else:
                            if debug == True: printDebugMessage(f"There was an error holding mutex W due to response: {mutexW}")
                    def hold_mutex2(mu_name):
                        mutexA = kernel32.CreateMutexA(None, ctypes.wintypes.BOOL(True), mu_name)
                        if mutexA:
                            try:
                                if awaitRobloxClosure == True:
                                    while self.getIfRobloxIsOpen(): time.sleep(1)
                                else:
                                    while True: time.sleep(1)
                                kernel32.ReleaseMutex(mutexA)
                            except Exception as e: 
                                if debug == True: printDebugMessage(f"There was an error holding mutex A: {str(e)}")
                            finally: kernel32.ReleaseMutex(mutexA)
                        else:
                            if debug == True: printDebugMessage(f"There was an error holding mutex A due to response: {mutexA}")
                    threading.Thread(target=hold_mutex, args=[mutex_name]).start()
                    threading.Thread(target=hold_mutex2, args=[mutex_bytename]).start()
                    is_created = True
            return is_created
        else:
            self.unsupportedFunction()
            return False
    def parseRobloxLauncherURL(self, url: str=""):
        p = url.split('+')[1:]
        data = {}
        for s in p:
            if ':' in s: key, value = s.split(':', 1); data[key] = value
        return data
    def createRobloxLauncherURL(self, url_scheme: str="roblox", data: typing.Dict[str, str]={}): 
        s = []
        for i, v in data.items(): s.append(f"{i}:{v}")
        return f"{url_scheme}:1+{'+'.join(s)}"
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

        macOS_dir = os.path.join(getInstallableApplicationsFolder(), "Roblox.app")
        macOS_studioDir = os.path.join(getInstallableApplicationsFolder(), "RobloxStudio.app")
        macOS_beforeClientServices = os.path.join("Contents", "MacOS")
        macOS_installedPath = os.path.join(getInstallableApplicationsFolder())
        windows_dir = os.path.join(os.getenv('LOCALAPPDATA') if os.getenv('LOCALAPPDATA') else "", "Roblox")
        windows_versions_dir = os.path.join(windows_dir, "Versions")
        windows_player_folder_name = ""
        windows_studio_folder_name = ""
        return self.CustomizableVariables(org_macOS_dir, org_macOS_studioDir, org_macOS_beforeClientServices, org_macOS_installedPath, org_windows_dir, org_windows_versions_dir, org_windows_player_folder_name, org_windows_studio_folder_name)
    def openRoblox(self, studio: bool=False, forceQuit: bool=False, makeDupe: bool=False, startData: typing.Union[list, str]="", debug: bool=False, attachInstance: bool=False, allowRobloxOtherLogDebug: bool=False, mainLogFile: str="", oneThreadedInstance: bool=True) -> "RobloxInstance | None":
        client_label = "Studio" if studio == True else "Player"
        if self.getIfRobloxIsOpen(studio=studio):
            if forceQuit == True:
                self.endRoblox(studio=studio)
                if debug == True: printDebugMessage("Ending Roblox Instances..")
        if self.__main_os__ == "Darwin":
            tar_dir = macOS_studioDir if studio == True else macOS_dir
            if startData == "": startData = []
            elif type(startData) is list:
                s = []
                for i in startData:
                    if i == "": s.append(i)
                for e in s: startData.remove(e)
            if makeDupe == True and not (studio == True):
                if self.getIfRobloxIsOpen(studio=studio) == True:
                    self.prepareMultiInstance(debug=debug)
                    # com = f"open -n -a \'{os.path.join(macOS_dir, macOS_beforeClientServices, 'RobloxPlayer')}\' {startData}"
                    com = ["/usr/bin/open", "-n", "-a", os.path.join(tar_dir, macOS_beforeClientServices, "RobloxPlayer")] + (startData if type(startData) is list else startData.split(" "))
                    if debug == True: printDebugMessage(f"Running Roblox Executable using Command: {com}")
                    a = subprocess.run(com, check=True)
                    if a.returncode == 0:
                        if attachInstance == True:
                            cur_open_pid = self.getLatestOpenedRobloxPid(studio=studio)
                            start_time = datetime.datetime.now(tz=datetime.UTC).timestamp()
                            test_instance = self.RobloxInstance(self, pid=cur_open_pid, studio=studio, debug_mode=False, allow_other_logs=allowRobloxOtherLogDebug, await_log_creation=False, one_threaded=oneThreadedInstance)
                            while True:
                                if test_instance.ended_process == True: break
                                elif len(test_instance.getWindowsOpened()) > 0:
                                    time.sleep(5)
                                    if len(test_instance.getWindowsOpened()) > 0: break
                                elif start_time+20 < datetime.datetime.now(tz=datetime.UTC).timestamp(): break
                                else: time.sleep(0.5)
                            test_instance.requestThreadClosing()
                            if self.getIfRobloxIsOpen(studio=studio) == True:
                                self.prepareMultiInstance(debug=debug)
                                pid = self.getLatestOpenedRobloxPid(studio=studio)
                                if pid: return self.RobloxInstance(self, pid=pid, studio=studio, log_file=mainLogFile, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_log_creation=True, one_threaded=oneThreadedInstance)
                else:
                    # com = f"open -n -a \'{os.path.join(macOS_dir, macOS_beforeClientServices, 'RobloxPlayer')}\' {startData}"
                    com = ["/usr/bin/open", "-n", "-a", os.path.join(tar_dir, macOS_beforeClientServices, 'RobloxPlayer')] + (startData if type(startData) is list else startData.split(" "))
                    if debug == True: printDebugMessage(f"Running Roblox Executable using Command: {com}")
                    a = subprocess.run(com, check=True)
                    if a.returncode == 0:
                        if attachInstance == True:
                            time.sleep(2)
                            if self.getIfRobloxIsOpen(studio=studio) == True:
                                pid = self.getLatestOpenedRobloxPid(studio=studio)
                                if pid: return self.RobloxInstance(self, pid=pid, studio=studio, log_file=mainLogFile, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_log_creation=True, one_threaded=oneThreadedInstance)
            else:
                # f"open -a \'{macOS_dir}\' {startData}"
                com = ["/usr/bin/open"] + (["-n"] if makeDupe == True else []) + ["-a", tar_dir] + (startData if type(startData) is list else startData.split(" "))
                if debug == True: printDebugMessage(f"Running Roblox using Command: {com}")
                a = subprocess.run(com, check=True)
                if a.returncode == 0:
                    if attachInstance == True:
                        time.sleep(2)
                        if self.getIfRobloxIsOpen(studio=studio) == True:
                            pid = self.getLatestOpenedRobloxPid(studio=studio)
                            if pid: return self.RobloxInstance(self, pid=pid, studio=studio, log_file=mainLogFile, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_log_creation=True, one_threaded=oneThreadedInstance)
        elif self.__main_os__ == "Windows":
            created_mutex = False
            if makeDupe == True and not (studio == True):
                try:
                    created_mutex = self.prepareMultiInstance(debug=debug)
                    if debug == True:
                        if created_mutex == True: printDebugMessage("Successfully attached the mutex! Once this window closes, all the other Roblox windows will close.")
                        else: printDebugMessage("There's an issue trying to create a mutex! This may be because the mutex was already taken!")
                except Exception:
                    if debug == True: printDebugMessage("There's an issue trying to create a mutex!")
            most_recent_roblox_version_dir = self.getRobloxInstallFolder(studio=studio)
            if most_recent_roblox_version_dir:
                startData = startData.replace("&", "^&")
                if startData == "": com = ["start", os.path.join(most_recent_roblox_version_dir, f'Roblox{client_label}Beta.exe')]
                else: com = ["start", os.path.join(most_recent_roblox_version_dir, f"Roblox{client_label}Beta.exe"), startData]
                if debug == True: printDebugMessage(f"Running Roblox{client_label}Beta.exe using Command: {com}")
                a = subprocess.run(com, shell=True, check=True, stdout=subprocess.DEVNULL)
                if a.returncode == 0:
                    if attachInstance == True:
                        if makeDupe == True:
                            if self.getIfRobloxIsOpen(studio=studio) == True:
                                cur_open_pid = self.getLatestOpenedRobloxPid(studio=studio)
                                start_time = datetime.datetime.now(tz=datetime.UTC).timestamp()
                                test_instance = self.RobloxInstance(self, pid=cur_open_pid, studio=studio, debug_mode=False, allow_other_logs=allowRobloxOtherLogDebug, await_log_creation=False, one_threaded=oneThreadedInstance)
                                while True:
                                    if test_instance.ended_process == True: break
                                    elif len(test_instance.getWindowsOpened()) > 0:
                                        time.sleep(5)
                                        if len(test_instance.getWindowsOpened()) > 0: break
                                    elif start_time+20 < datetime.datetime.now(tz=datetime.UTC).timestamp(): break
                                    else: time.sleep(0.5)
                                test_instance.requestThreadClosing()
                                if self.getIfRobloxIsOpen(studio=studio) == True:
                                    pid = self.getLatestOpenedRobloxPid(studio=studio)
                                    if pid: return self.RobloxInstance(self, pid=pid, studio=studio, log_file=mainLogFile, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_log_creation=True, created_mutex=created_mutex, one_threaded=oneThreadedInstance)
                        else:
                            time.sleep(1)
                            if self.getIfRobloxIsOpen(studio=studio) == True:
                                cur_open_pid = self.getLatestOpenedRobloxPid(studio=studio)
                                start_time = datetime.datetime.now(tz=datetime.UTC).timestamp()
                                test_instance = self.RobloxInstance(self, pid=cur_open_pid, studio=studio, debug_mode=False, allow_other_logs=allowRobloxOtherLogDebug, await_log_creation=False, one_threaded=oneThreadedInstance)
                                while True:
                                    if test_instance.ended_process == True: break
                                    elif len(test_instance.getWindowsOpened()) > 0:
                                        time.sleep(5)
                                        if len(test_instance.getWindowsOpened()) > 0: break
                                    elif start_time+20 < datetime.datetime.now(tz=datetime.UTC).timestamp(): break
                                    else: time.sleep(0.5)
                                test_instance.requestThreadClosing()
                                if self.getIfRobloxIsOpen(studio=studio) == True:
                                    pid = self.getLatestOpenedRobloxPid(studio=studio)
                                    if pid: return self.RobloxInstance(self, pid=pid, studio=studio, log_file=mainLogFile, debug_mode=debug, allow_other_logs=allowRobloxOtherLogDebug, await_log_creation=True, created_mutex=created_mutex, one_threaded=oneThreadedInstance)
            else: printLog("Roblox couldn't be found.")
        else: self.unsupportedFunction()
    def downloadRobloxInstaller(self, studio: bool=False, filePath: str="", channel: str="LIVE", debug: bool=False):
        if self.__main_os__ == "Darwin" or self.__main_os__ == "Windows":
            client_label = "Studio" if studio == True else "Player"
            bootstrapper_settings = self.getLatestRobloxAppSettings(studio=studio, debug=debug, bootstrapper=True, bucket=channel)
            if bootstrapper_settings["success"] == True:
                starter_url = ""
                bootstrapper_settings = bootstrapper_settings["application_settings"]
                if bootstrapper_settings.get("FFlagReplaceChannelNameForDownload", True): starter_url = "channel/common/"
                else: starter_url = f"channel/{channel.lower()}/"
                if self.__main_os__ == "Darwin":
                    cur_vers = self.getLatestClientVersion(studio=studio, debug=debug, channel=channel)
                    if cur_vers and cur_vers.get("success") == True:
                        if debug == True: printDebugMessage(f"Downloading Roblox {client_label} DMG from Roblox's servers..")
                        cur_vers_down_link = f'https://{self.getBestRobloxDownloadServer()}/{starter_url}mac/{"arm64/" if platform.machine() == "arm64" else ""}{cur_vers.get("client_version")}-Roblox{"Studio" if studio == True else ""}.zip'
                        if debug == True: printDebugMessage(f"Downloading from: {cur_vers_down_link}")
                        down_req = requests.download(cur_vers_down_link, os.path.join(cur_path, f"Roblox{client_label}Install.zip"))
                        if down_req.ok:
                            zip_extract = pip_class.unzipFile(os.path.join(cur_path, f"Roblox{client_label}Install.zip"), filePath, ["Contents"])
                            if zip_extract.returncode == 0: os.remove(os.path.join(cur_path, f"Roblox{client_label}Install.zip"))
                            else:
                                if debug == True: printDebugMessage(f"Unable to unzip Roblox {client_label} installer due to an error.")
                        else:
                            if debug == True: printDebugMessage(f"Unable to download Roblox {client_label} installer due to an error. Code: {down_req.status_code}")
                    else:
                        if debug == True: printDebugMessage(f"Unable to download Roblox {client_label} installer due to an http error.")
                elif self.__main_os__ == "Windows":
                    cur_vers = self.getLatestClientVersion(studio=studio, debug=debug, channel=channel)
                    if cur_vers and cur_vers.get("success") == True:
                        if debug == True: printDebugMessage(f"Downloading Roblox EXE from Roblox's servers..")
                        cur_vers_down_link = f'https://{self.getBestRobloxDownloadServer()}/{starter_url}{cur_vers.get("client_version")}-Roblox{client_label}Installer.exe'
                        if debug == True: printDebugMessage(f"Downloading from: {cur_vers_down_link}")
                        down_req = requests.download(cur_vers_down_link, filePath)
                        if down_req.ok:
                            if debug == True: printDebugMessage(f"Successfully downloaded installer!")
                            return filePath
                        else:
                            if debug == True: printDebugMessage(f"Unable to download Roblox {client_label} installer due to an http error. Code: {down_req.status_code}")
                    else:
                        if debug == True: printDebugMessage(f"Unable to download Roblox {client_label} installer due to an http error.")
                else: self.unsupportedFunction()
            else:
                if debug == True: printDebugMessage(f"Unable to fetch install bootstrapper settings from Roblox.")
        else: self.unsupportedFunction()
    def installFastFlags(self, fflags: dict, studio: bool=False, askForPerms: bool=False, merge: bool=True, flat: bool=False, endRobloxInstances: bool=True, debug: bool=False, main: bool=False):
        if __name__ == "__main__" or main == True:
            if self.__main_os__ == "Darwin":
                if endRobloxInstances == True:
                    if studio == True:
                        printMainMessage(f"Closing any open Roblox Studio windows..")
                        self.endRoblox(studio=True)
                    else:
                        printMainMessage(f"Closing any open Roblox windows..")
                        self.endRoblox()
                if orangeblox_mode == False:
                    printMainMessage(f"Generating ClientSettings Folder..")
                    if not os.path.exists(os.path.join(macOS_studioDir if studio == True else macOS_dir, macOS_beforeClientServices, "ClientSettings")):
                        os.mkdir(os.path.join(macOS_studioDir if studio == True else macOS_dir, macOS_beforeClientServices, "ClientSettings"))
                        printSuccessMessage(f"Created {os.path.join(macOS_studioDir if studio == True else macOS_dir, macOS_beforeClientServices, 'ClientSettings')}..")
                    else: printWarnMessage(f"Client Settings is already created. Skipping Folder Creation..")
                printMainMessage(f"Writing ClientAppSettings.json")
                if merge == True:
                    if orangeblox_mode == True:
                        try:
                            printMainMessage("Reading Previous Configurations..")
                            macos_preference_expected = os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.orangeblox.plist")
                            if os.path.exists(macos_preference_expected):
                                app_configuration = plist_class.readPListFile(macos_preference_expected)
                                if app_configuration.get("Configuration"): merge_json = app_configuration.get("Configuration")
                                else: merge_json = {}
                            else: merge_json = {}
                            if studio == True:
                                if not merge_json.get("EFlagRobloxStudioFlags"): merge_json["EFlagRobloxStudioFlags"] = {}
                                merge_json["EFlagRobloxStudioFlags"].update(fflags)
                            else:
                                if not merge_json.get("EFlagRobloxPlayerFlags"): merge_json["EFlagRobloxPlayerFlags"] = {}
                                merge_json["EFlagRobloxPlayerFlags"].update(fflags)
                            fflags = merge_json
                        except Exception as e: printErrorMessage(f"Something went wrong while trying to generate a merged JSON: {str(e)}")
                    elif os.path.exists(os.path.join(macOS_studioDir if studio == True else macOS_dir, macOS_beforeClientServices, "ClientSettings", 'ClientAppSettings.json')):
                        try:
                            printMainMessage("Reading Previous Client App Settings..")
                            with open(os.path.join(macOS_studioDir if studio == True else macOS_dir, macOS_beforeClientServices, "ClientSettings", f'ClientAppSettings.json'), "r", encoding="utf-8") as f: merge_json = json.load(f)
                            merge_json.update(fflags)
                            fflags = merge_json
                        except Exception as e: printErrorMessage(f"Something went wrong while trying to generate a merged JSON: {str(e)}")
                set_location = os.path.join(macOS_studioDir if studio == True else macOS_dir, macOS_beforeClientServices, "ClientSettings", f'ClientAppSettings.json')
                if orangeblox_mode == True:
                    set_location = os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.orangeblox.plist")
                    app_configuration = plist_class.readPListFile(set_location)
                    app_configuration["Configuration"] = fflags
                    plist_class.writePListFile(set_location, app_configuration, binary=True)
                else:
                    with open(set_location, "w", encoding="utf-8") as f:
                        if flat == True: json.dump(fflags, f)
                        else: json.dump(fflags, f, indent=4)
                printSuccessMessage("DONE!")
                if orangeblox_mode == True:
                    printSuccessMessage("Your fast flags was successfully saved into your Fast Flag Settings!")
                    printSuccessMessage(f"If you like to update your fast flags, go to: {set_location}")
                else:
                    printSuccessMessage(f"Your FFlags have been installed to Roblox {'Studio' if studio == True else 'Client'}!")
                    printSuccessMessage("Please know that you'll have to use this script again after every update/reinstall!")
                    printSuccessMessage(f"If you like to update your fast flags, go to: {set_location}")
                    printSuccessMessage(f"Additionally, if you would like to, you may install a Roblox bootstrap on your computer to automatically do this.")
                    if studio == True:
                        printMainMessage("Would you like to open Roblox Studio? (y/n)")
                        if input("> ").lower() == "y": self.openRoblox(studio=studio)
                    else:
                        printMainMessage("Would you like to open Roblox? (y/n)")
                        if input("> ").lower() == "y": self.openRoblox()
            elif self.__main_os__ == "Windows":
                if endRobloxInstances == True:
                    if studio == True:
                        printMainMessage(f"Closing any open Roblox Studio windows..")
                        self.endRoblox(studio=True)
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
                        else: printWarnMessage(f"Client Settings is already created. Skipping Folder Creation..")
                    printMainMessage(f"Writing ClientAppSettings.json")
                    if merge == True:
                        if os.path.exists("Configuration.json"):
                            try:
                                printMainMessage("Reading Previous Configurations..")
                                with open(f"Configuration.json", "rb") as f: merge_json = f.read()
                                try: merge_json = json.loads(merge_json)
                                except Exception as e: merge_json = json.loads(zlib.decompress(merge_json).decode("utf-8"))
                                if studio == True:
                                    if not merge_json.get("EFlagRobloxStudioFlags"): merge_json["EFlagRobloxStudioFlags"] = {}
                                    merge_json["EFlagRobloxStudioFlags"].update(fflags)
                                else:
                                    if not merge_json.get("EFlagRobloxPlayerFlags"): merge_json["EFlagRobloxPlayerFlags"] = {}
                                    merge_json["EFlagRobloxPlayerFlags"].update(fflags)
                                fflags = merge_json
                            except Exception as e: printErrorMessage(f"Something went wrong while trying to generate a merged JSON: {str(e)}")
                        elif os.path.exists(os.path.join(most_recent_roblox_version_dir, "ClientSettings", f"ClientAppSettings.json")):
                            try:
                                printMainMessage("Reading Previous Client App Settings..")
                                with open(os.path.join(most_recent_roblox_version_dir, "ClientSettings", f"ClientAppSettings.json"), "r", encoding="utf-8") as f: merge_json = json.load(f)
                                merge_json.update(fflags)
                                fflags = merge_json
                            except Exception as e: printErrorMessage(f"Something went wrong while trying to generate a merged JSON: {str(e)}")
                    set_location = os.path.join(most_recent_roblox_version_dir, "ClientSettings", f"ClientAppSettings.json")
                    if orangeblox_mode == True and os.path.exists("Configuration.json"):
                        data_in_string = zlib.compress(json.dumps(fflags).encode('utf-8'))
                        with open(os.path.join(cur_path, "Configuration.json"), "wb") as f: f.write(data_in_string)
                    else:
                        with open(set_location, "w", encoding="utf-8") as f:
                            if flat == True: json.dump(fflags, f)
                            else: json.dump(fflags, f, indent=4)
                    printSuccessMessage("DONE!")
                    if orangeblox_mode == True:
                        printSuccessMessage("Your fast flags was successfully saved into your Fast Flag Settings!")
                        printSuccessMessage(f"If you like to update your fast flags, go to: {set_location}")
                    else:
                        printSuccessMessage(f"Your FFlags have been installed to Roblox {'Studio' if studio == True else 'Client'}!")
                        printSuccessMessage("Please know that you'll have to use this script again after every update/reinstall!")
                        printSuccessMessage(f"If you like to update your fast flags, go to: {set_location}")
                        printSuccessMessage(f"Additionally, if you would like to, you may install a Roblox bootstrap on your computer to automatically do this.")
                        if studio == True:
                            printMainMessage("Would you like to open Roblox Studio? (y/n)")
                            if input("> ").lower() == "y": self.openRoblox(studio=studio)
                        else:
                            printMainMessage("Would you like to open Roblox? (y/n)")
                            if input("> ").lower() == "y": self.openRoblox()
                else: printErrorMessage("Roblox couldn't be found.")
            else: printErrorMessage("Roblox Fast Flags Installer is only supported for macOS and Windows.")
        else:
            if askForPerms == True:
                if submit_status: submit_status.submit("[FFLAGS] Asking for permissions..", 0)
                printLog("Would you like to continue with the Roblox Fast Flag installation? (y/n)")
                printLog("WARNING! This will force-quit any open Roblox windows! Please close them in order to prevent data loss!")
                if not (input("> ").lower() == "y"):
                    printLog("Stopped installation..")
                    if submit_status: submit_status.submit("\033ERR[FFLAGS] Asking for permissions..", 0)
                    return
            if self.__main_os__ == "Darwin":
                if endRobloxInstances == True:
                    if submit_status: submit_status.submit("[FFLAGS] Ending Roblox Windows..", 10)
                    if studio == True:
                        if debug == True: printDebugMessage(f"Closing any open Roblox Studio windows..")
                        self.endRoblox(studio=True)
                    else:
                        if debug == True: printDebugMessage(f"Closing any open Roblox windows..")
                        self.endRoblox()
                if submit_status: submit_status.submit("[FFLAGS] Creating ClientSettings Folder..", 25)
                if not os.path.exists(os.path.join(macOS_studioDir if studio == True else macOS_dir, macOS_beforeClientServices, "ClientSettings")):
                    if debug == True: printDebugMessage("Creating ClientSettings folder..")
                    os.mkdir(os.path.join(macOS_studioDir if studio == True else macOS_dir, macOS_beforeClientServices, "ClientSettings"))
                if merge == True:
                    if submit_status: submit_status.submit("[FFLAGS] Merging Possible Configurations..", 45)
                    if os.path.exists(os.path.join(macOS_studioDir if studio == True else macOS_dir, macOS_beforeClientServices, "ClientSettings", f'ClientAppSettings.json')):
                        try:
                            with open(os.path.join(macOS_studioDir if studio == True else macOS_dir, macOS_beforeClientServices, "ClientSettings", f'ClientAppSettings.json'), "r", encoding="utf-8") as f: merge_json = json.load(f)
                            merge_json.update(fflags)
                            fflags = merge_json
                            if debug == True: printDebugMessage("Successfully merged the JSON in the ClientSettings folder with the provided json!")
                        except Exception as e: printLog(f"Something went wrong while trying to generate a merged JSON: {str(e)}")
                if submit_status: submit_status.submit("[FFLAGS] Saving Configuration..", 50)
                with open(os.path.join(macOS_studioDir if studio == True else macOS_dir, macOS_beforeClientServices, "ClientSettings", f'ClientAppSettings.json'), "w", encoding="utf-8") as f:
                    if flat == True: json.dump(fflags, f)
                    else: json.dump(fflags, f, indent=4)
                if submit_status: submit_status.submit("[FFLAGS] Saved FFlags!", 100)
                if debug == True: printDebugMessage(f"Saved to ClientAppSettings.json successfully!")
            elif self.__main_os__ == "Windows":
                if endRobloxInstances == True:
                    if submit_status: submit_status.submit("[FFLAGS] Ending Roblox Windows..", 10)
                    if studio == True:
                        if debug == True: printDebugMessage(f"Closing any open Roblox Studio windows..")
                        self.endRoblox(studio=True)
                    else:
                        if debug == True: printDebugMessage(f"Closing any open Roblox windows..")
                        self.endRoblox()
                most_recent_roblox_version_dir = self.getRobloxInstallFolder(studio=studio)
                if most_recent_roblox_version_dir or orangeblox_mode == True:
                    if submit_status: submit_status.submit("[FFLAGS] Creating ClientSettings Folder..", 25)
                    if not os.path.exists(os.path.join(most_recent_roblox_version_dir, "ClientSettings")):
                        if debug == True: printDebugMessage("Creating ClientSettings folder..")
                        os.mkdir(os.path.join(most_recent_roblox_version_dir, "ClientSettings"))
                    if merge == True:
                        if submit_status: submit_status.submit("[FFLAGS] Merging Possible Configurations..", 45)
                        if os.path.exists(os.path.join(most_recent_roblox_version_dir, "ClientSettings", f"ClientAppSettings.json")):
                            try:
                                with open(os.path.join(most_recent_roblox_version_dir, "ClientSettings", f"ClientAppSettings.json"), "r", encoding="utf-8") as f: merge_json = json.load(f)
                                merge_json.update(fflags)
                                fflags = merge_json
                                if debug == True: printDebugMessage("Successfully merged the JSON in the ClientSettings folder with the provided json!")
                            except Exception as e: printLog(f"Something went wrong while trying to generate a merged JSON: {str(e)}")
                    if submit_status: submit_status.submit("[FFLAGS] Saving Configuration..", 50)
                    with open(os.path.join(most_recent_roblox_version_dir, "ClientSettings", f"ClientAppSettings.json"), "w", encoding="utf-8") as f:
                        if flat == True: json.dump(fflags, f)
                        else: json.dump(fflags, f, indent=4)
                    if submit_status: submit_status.submit("[FFLAGS] Saved FFlags!", 100)
                    if debug == True: printDebugMessage(f"Saved to ClientAppSettings.json successfully!")
                else:
                    printLog("Roblox couldn't be found.")
                    if submit_status: submit_status.submit("\033ERR[FFLAGS] Roblox couldn't be found!", 100)
            else:
                self.unsupportedFunction()
                if submit_status: submit_status.submit("\033ERR[FFLAGS] Roblox Fast Flags Installer is only supported for macOS and Windows.", 100)
    def installGlobalBasicSettings(self, globalsettings: dict, studio: bool=False, askForPerms: bool=False, endRobloxInstances: bool=True, flat: bool=False, debug: bool=False):
        if askForPerms == True:
            if submit_status: submit_status.submit("[GLOBALSETTINGS] Asking for permissions..", 0)
            printLog("Would you like to continue with the Roblox Fast Flag installation? (y/n)")
            printLog("WARNING! This will force-quit any open Roblox windows! Please close them in order to prevent data loss!")
            if not (input("> ").lower() == "y"):
                printLog("Stopped installation..")
                return
        roblox_app_location = ""
        if self.__main_os__ == "Darwin": roblox_app_location = os.path.join(user_folder, "Library", "Roblox")
        elif self.__main_os__ == "Windows": roblox_app_location = windows_dir
        else:
            self.unsupportedFunction()
            if submit_status: submit_status.submit("\033ERR[GLOBALSETTINGS] Roblox Fast Flags Installer is only supported for macOS and Windows.", 0)
            return  
        if endRobloxInstances == True:
            if submit_status: submit_status.submit("[GLOBALSETTINGS] Ending Roblox Windows..", 10)
            if studio == True:
                if debug == True: printDebugMessage(f"Closing any open Roblox Studio windows..")
                self.endRoblox(studio=True)
            else:
                if debug == True: printDebugMessage(f"Closing any open Roblox windows..")
                self.endRoblox()
        if submit_status: submit_status.submit("[GLOBALSETTINGS] Finding Global Basic Settings..", 25)
        file_name = None
        for i in os.listdir(roblox_app_location):
            if not (i.find("GlobalBasicSettings") == -1):
                if studio == True and i.find("_Studio") == -1: continue
                file_name = i
        if file_name:
            if submit_status: submit_status.submit("[GLOBALSETTINGS] Found Global Basic Settings File!", 25)
            if debug == True: printDebugMessage(f"Founded File Name: {file_name}")
            if debug == True: printDebugMessage("Reading Settings XML..")
            if submit_status: submit_status.submit("[GLOBALSETTINGS] Reading XML File!", 25)
            with open(os.path.join(roblox_app_location, file_name), "r", encoding="utf-8") as f: xml_contents = f.read()
            if submit_status: submit_status.submit("[GLOBALSETTINGS] Finding root of file!", 30)
            xml_original_root = ET.fromstring(xml_contents)
            item_class = xml_original_root.find(".//Item")
            referent = item_class.get("referent") if item_class is not None else None
            if submit_status: submit_status.submit("[GLOBALSETTINGS] Recreating XML Base!", 45)
            if debug == True: printDebugMessage("Recreating XML Tree..")
            xml_root = ET.Element("roblox", {
                "xmlns:xmime": "http://www.w3.org/2005/05/xmlmime",
                "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                "xsi:noNamespaceSchemaLocation": "https://www.roblox.com/roblox.xsd",
                "version": "4"
            })
            xml_item = ET.SubElement(xml_root, "Item", {"class": "UserGameSettings", "referent": referent})
            xml_properties = ET.SubElement(xml_item, "Properties")
            if submit_status: submit_status.submit("[GLOBALSETTINGS] Recreating XML Tree!", 70)
            for key, value in globalsettings.items():
                prop_type = value["type"]
                prop_value = value["data"]
                if prop_type == "Vector2":
                    vector2_element = ET.SubElement(xml_properties, "Vector2", {"name": key})
                    ET.SubElement(vector2_element, "X").text = str(prop_value[0])
                    ET.SubElement(vector2_element, "Y").text = str(prop_value[1])
                else: ET.SubElement(xml_properties, prop_type, {"name": key}).text = str(prop_value)
            if submit_status: submit_status.submit("[GLOBALSETTINGS] Finalizing Tree!", 90)
            if debug == True: printDebugMessage("Finalizing XML Tree..")
            if flat == True: final_xml_contents = ET.tostring(xml_root, encoding="utf-8").decode()
            else: final_xml_contents = xml.dom.minidom.parseString(ET.tostring(xml_root, encoding="utf-8").decode()).toprettyxml(indent="    ")
            if debug == True: printDebugMessage("Saving to File..")
            with open(os.path.join(roblox_app_location, file_name), "w", encoding="utf-8") as f: f.write(final_xml_contents)
            if submit_status: submit_status.submit("[GLOBALSETTINGS] Successfully saved Global Basic Settings!", 100)
            if debug == True: printDebugMessage("Successfully saved Global Basic Settings!")
        else:
            if submit_status: submit_status.submit("\033ERR[GLOBALSETTINGS] Unable to find file.", 100)
            printLog("Unable to find settings file.")
    def installRoblox(self, studio: bool=False, forceQuit: bool=True, debug: bool=False, disableRobloxAutoOpen: bool=True, downloadInstaller: bool=False, downloadChannel: str=None, copyRobloxInstallerPath: str="", verifyInstall: bool=True):
        client_label = "Studio" if studio == True else "Player"
        if self.getIfRobloxIsOpen(studio=studio):
            if forceQuit == True:
                if submit_status: submit_status.submit(f"[INSTALL] Ending Roblox {client_label} Instances..", 0)
                self.endRoblox(studio=studio)
                if debug == True: printDebugMessage(f"Ending Roblox {client_label} Instances..")
        def waitForRobloxEnd():
            if disableRobloxAutoOpen == True:
                for i in range(15):
                    if debug == True: printDebugMessage(f"Waited: {i}/15 seconds")
                    if submit_status: submit_status.submit("[INSTALL] Awaiting Roblox to Close..", 90)
                    if self.getIfRobloxIsOpen(studio=studio):
                        self.endRoblox(studio=studio)
                        break
                    time.sleep(1)
                
        if self.__main_os__ == "Darwin":
            if self.getIfRobloxIsOpen(studio=studio, installer=True):
                if submit_status: submit_status.submit("[INSTALL] Waiting for existing installer..", 10)
                if debug == True: printDebugMessage("Installer is already opened. Waiting for installation to end..")
                while True:
                    if not self.getIfRobloxIsOpen(studio=studio, installer=True): break
                    else: time.sleep(1)
                waitForRobloxEnd()
                if submit_status: submit_status.submit("[INSTALL] Roblox is installed!", 100)
                return {"success": True}
            else:
                if macOS_installedPath == os.path.join(getInstallableApplicationsFolder()):   
                    try:
                        if not copyRobloxInstallerPath == "":
                            if downloadInstaller == True:
                                if os.path.exists(copyRobloxInstallerPath) and os.path.isfile(copyRobloxInstallerPath): os.remove(copyRobloxInstallerPath)
                                if os.path.exists(copyRobloxInstallerPath) and os.path.isdir(copyRobloxInstallerPath): shutil.rmtree(copyRobloxInstallerPath, ignore_errors=True)
                                if submit_status: submit_status.submit("[INSTALL] Fetching Current Version and Channel..", 15)
                                if downloadChannel == None:
                                    channel_res = self.getCurrentClientVersion(studio=studio)
                                    if channel_res.get("success") == True: downloadChannel = channel_res.get("channel", "LIVE")
                                    else: downloadChannel = "LIVE"
                                if submit_status: submit_status.submit("[INSTALL] Downloading Roblox Installer..", 20)
                                self.downloadRobloxInstaller(studio=studio, filePath=copyRobloxInstallerPath, channel=downloadChannel, debug=debug)
                            else:
                                if os.path.exists(os.path.join((macOS_studioDir if studio == True else macOS_dir), macOS_beforeClientServices, f"Roblox{client_label}Installer.app")):
                                    try:
                                        if submit_status: submit_status.submit("[INSTALL] Downloading Roblox Installer..", 30)
                                        if debug == True: printDebugMessage(f"Replicating Roblox {client_label} installer to path: {copyRobloxInstallerPath}")
                                        pip_class.copyTreeWithMetadata(os.path.join((macOS_studioDir if studio == True else macOS_dir), macOS_beforeClientServices, f"Roblox{client_label}Installer.app"), copyRobloxInstallerPath, dirs_exist_ok=True)
                                    except Exception as e:
                                        if debug == True: printDebugMessage("Unable to replicate installer to the designated file path.")
                                else:
                                    if debug == True: printDebugMessage("There's no version of Roblox installed. Installing from downloaded installer app.")
                            if submit_status: submit_status.submit("[INSTALL] Running Roblox Installer..", 50)
                            if debug == True: printDebugMessage(f"Running Roblox{client_label}Installer executable..")
                            insta = subprocess.run(os.path.join(copyRobloxInstallerPath, "Contents", "MacOS", f"Roblox{client_label}Installer"), shell=True, check=True, stdout=subprocess.DEVNULL)
                        else:
                            if submit_status: submit_status.submit("[INSTALL] Running Roblox Installer..", 50)
                            if debug == True: printDebugMessage(f"Running Roblox{client_label}Installer executable..")
                            insta = subprocess.run(os.path.join((macOS_studioDir if studio == True else macOS_dir), macOS_beforeClientServices, f"Roblox{client_label}Installer.app", "Contents", "MacOS", f"Roblox{client_label}Installer"), shell=True, check=True, stdout=subprocess.DEVNULL)
                        if insta.returncode == 0:
                            if submit_status: submit_status.submit("[INSTALL] Installer has been run successfully!", 80)
                            if debug == True: printDebugMessage("Installer has succeeded! Awaiting Roblox closing..")
                            waitForRobloxEnd()
                            if submit_status: submit_status.submit("[INSTALL] Roblox is installed!", 100)
                            return {"success": True}
                        else:
                            if submit_status: submit_status.submit("[INSTALL] Installer has failed..", 80)
                            if debug == True: printDebugMessage(f"Installer has failed. Code: {insta.returncode}")
                            return {"success": False}
                    except Exception as e:
                        printErrorMessage(f"Something went wrong starting Roblox Installer: {str(e)}")
                        if submit_status: submit_status.submit("\033ERR[INSTALL] Installer couldn't be started!", 15)
                        return {"success": False}
                else:
                    if submit_status: submit_status.submit("[INSTALL] Fetching current version and channel!", 30)
                    if downloadChannel == None:
                        channel_res = self.getCurrentClientVersion(studio=studio)
                        if channel_res.get("success") == True: downloadChannel = channel_res.get("channel", "LIVE")
                        else: downloadChannel = "LIVE"
                    if submit_status: submit_status.submit("[INSTALL] Getting latest version!", 50)
                    latest_vers = self.getLatestClientVersion(studio=studio, debug=debug, channel=downloadChannel)
                    if latest_vers["success"] == True:
                        if submit_status: submit_status.submit("[INSTALL] Installing Roblox Bundle!", 80)
                        self.endRoblox(studio=studio)
                        s = self.installRobloxBundle(studio=studio, installPath=macOS_installedPath, appPath=(macOS_studioDir if studio == True else macOS_dir), channel=downloadChannel, debug=debug, verify=verifyInstall)
                        if submit_status: submit_status.submit("[INSTALL] Installed Roblox Bundle!", 100)
                        return s
                    else:
                        if submit_status: submit_status.submit("\033ERR[INSTALL] Latest Version couldn't be fetched!", 50)
                        return {"success": False}
        elif self.__main_os__ == "Windows":
            if self.getIfRobloxIsOpen(studio=studio, installer=True):
                if submit_status: submit_status.submit("[INSTALL] Waiting for existing installer..", 10)
                if debug == True: printDebugMessage("Installer is already opened. Waiting for installation to end..")
                while True:
                    if not self.getIfRobloxIsOpen(studio=studio, installer=True): break
                    else: time.sleep(1)
                waitForRobloxEnd()
                if submit_status: submit_status.submit("[INSTALL] Roblox is installed!", 100)
                return {"success": True}
                return
            
            if windows_versions_dir == os.path.join(pip_class.getLocalAppData(), "Roblox", "Versions"):    
                most_recent_roblox_version_dir = self.getRobloxInstallFolder(studio=studio)
                if most_recent_roblox_version_dir:
                    if submit_status: submit_status.submit("[INSTALL] Running Roblox Installer..", 50)
                    if debug == True: printDebugMessage(f"Running Roblox{client_label}Installer executable..")
                    try:
                        insta = subprocess.run(os.path.join(most_recent_roblox_version_dir, f"Roblox{client_label}Installer.exe"), shell=True, stdout=subprocess.DEVNULL)
                        while True:
                            if not self.getIfRobloxIsOpen(studio=studio, installer=True): break
                            else: time.sleep(1)
                        if submit_status: submit_status.submit("[INSTALL] Installer has been run successfully!", 80)
                        if debug == True: printDebugMessage("Installer has succeeded! Awaiting Roblox closing..")
                        waitForRobloxEnd()
                        return {"success": True}
                    except Exception as e:
                        printErrorMessage(f"Something went wrong starting Roblox Installer: {str(e)}")
                        if submit_status: submit_status.submit("\033ERR[INSTALL] Installer has been failed!", 80)
                        return {"success": False}
                else:
                    if not (copyRobloxInstallerPath == "") and downloadInstaller == True:
                        if os.path.exists(copyRobloxInstallerPath) and os.path.isfile(copyRobloxInstallerPath): os.remove(copyRobloxInstallerPath)
                        if os.path.exists(copyRobloxInstallerPath) and os.path.isdir(copyRobloxInstallerPath): shutil.rmtree(copyRobloxInstallerPath, ignore_errors=True)
                        if submit_status: submit_status.submit("[INSTALL] Fetching Current Version and Channel..", 15)
                        if downloadChannel == None:
                            channel_res = self.getCurrentClientVersion(studio=studio)
                            if channel_res.get("success") == True: downloadChannel = channel_res.get("channel", "LIVE")
                            else: downloadChannel = "LIVE"
                        if submit_status: submit_status.submit(f"[INSTALL] Downloading Roblox {client_label} Installer..", 20)
                        self.downloadRobloxInstaller(studio=studio, filePath=copyRobloxInstallerPath, channel=downloadChannel, debug=debug)
                        if not os.path.exists(copyRobloxInstallerPath):
                            printLog("Roblox Installer couldn't be found.")
                            if submit_status: submit_status.submit("\033ERR[INSTALL] Installer couldn't be found!", 50)
                            return {"success": False}
                        else:
                            if submit_status: submit_status.submit(f"[INSTALL] Running Roblox {client_label} Installer..", 50)
                            if debug == True: printDebugMessage(f"Running Roblox{client_label}Installer executable..")
                            try:
                                insta = subprocess.run(f"{copyRobloxInstallerPath}", shell=True, stdout=subprocess.DEVNULL)
                                while True:
                                    if not self.getIfRobloxIsOpen(studio=studio, installer=True): break
                                    else: time.sleep(1)
                                if submit_status: submit_status.submit("[INSTALL] Installer has been run successfully!", 80)
                                if debug == True: printDebugMessage("Installer has succeeded! Awaiting Roblox closing..")
                                waitForRobloxEnd()
                                return {"success": True}
                            except Exception as e:
                                printErrorMessage(f"Something went wrong starting Roblox Installer: {str(e)}")
                                if submit_status: submit_status.submit("\033ERR[INSTALL] Installer couldn't be started!", 80)
                                return {"success": False}
                    else:
                        printLog("Roblox Installer couldn't be found.")
                        if submit_status: submit_status.submit("\033ERR[INSTALL] Installer couldn't be found!", 15)
                        return {"success": False}
            else:
                if submit_status: submit_status.submit("[INSTALL] Fetching Current Version and Channel!", 15)
                if downloadChannel == None:
                    channel_res = self.getCurrentClientVersion(studio=studio)
                    if channel_res.get("success") == True: downloadChannel = channel_res.get("channel", "LIVE")
                    else: downloadChannel = "LIVE"
                if submit_status: submit_status.submit("[INSTALL] Fetching latest version..", 30)
                latest_vers = self.getLatestClientVersion(studio=studio, debug=debug, channel=downloadChannel)
                if latest_vers["success"] == True:
                    self.endRoblox(studio=studio)
                    if submit_status: submit_status.submit("[INSTALL] Removing Old Roblox Bundles..", 50)
                    for i in os.listdir(windows_versions_dir):
                        if os.path.isdir(os.path.join(windows_versions_dir, i)) and os.path.exists(os.path.join(windows_versions_dir, i, f"Roblox{client_label}Beta.exe")): shutil.rmtree(os.path.join(windows_versions_dir, i), ignore_errors=True)
                    if submit_status: submit_status.submit(f"[INSTALL] Installing Roblox {client_label} Bundle..", 80)
                    if studio == True and not (windows_studio_folder_name == ""): 
                        makedirs(os.path.join(windows_versions_dir, windows_studio_folder_name))
                        s = self.installRobloxBundle(studio=studio, installPath=os.path.join(windows_versions_dir, windows_studio_folder_name), appPath="", channel=downloadChannel, debug=debug, verify=verifyInstall)
                    elif studio == False and not (windows_player_folder_name == ""): 
                        makedirs(os.path.join(windows_versions_dir, windows_player_folder_name))
                        s = self.installRobloxBundle(studio=studio, installPath=os.path.join(windows_versions_dir, windows_player_folder_name), appPath="", channel=downloadChannel, debug=debug, verify=verifyInstall)
                    else:
                        makedirs(os.path.join(windows_versions_dir))
                        s = self.installRobloxBundle(studio=studio, installPath=os.path.join(windows_versions_dir), appPath="", channel=downloadChannel, debug=debug, verify=verifyInstall)
                    if submit_status: submit_status.submit(f"[INSTALL] Installed Roblox {client_label} Bundle!", 100)
                    return s
                else:
                    printLog("Unable to fetch latest version.")
                    if submit_status: submit_status.submit("\033ERR[INSTALL] Unable to fetch latest version.", 100)
                    return {"success": False}
        else:
            self.unsupportedFunction()
            if submit_status: submit_status.submit("\033ERR[INSTALL] Roblox Fast Flags Installer is only supported for macOS and Windows.", 100)
            return {"success": False}
    def installRobloxBundle(self, studio: bool=False, installPath: str="", appPath: str="", channel: str="LIVE", debug: bool=False, verify: bool=True, lock: bool=True):
        if self.__main_os__ == "Darwin" or self.__main_os__ == "Windows":
            try:
                client_label = "Studio" if studio == True else "Player"
                if submit_status: submit_status.submit(f"[BUNDLE] Fetching Latest {client_label} Version..", 0)
                cur_vers = self.getLatestClientVersion(studio=studio, debug=debug, channel=channel)
                if cur_vers and cur_vers.get("success") == True:
                    if self.getIfRobloxIsOpen(studio=studio):
                        if submit_status: submit_status.submit("[BUNDLE] Closing Roblox..", 5)
                        if debug == True: printDebugMessage(f"Closing Roblox to prevent issues during download..")
                        self.endRoblox(studio=studio)
                    if submit_status: submit_status.submit("[BUNDLE] Fetching Bootstrap Settings..", 15)
                    bootstrapper_settings = self.getLatestRobloxAppSettings(studio=studio, debug=debug, bootstrapper=True, bucket=channel)
                    if bootstrapper_settings["success"] == True:
                        starter_url = ""
                        bootstrapper_settings = bootstrapper_settings["application_settings"]
                        if bootstrapper_settings.get("FFlagReplaceChannelNameForDownload", True): starter_url = "channel/common/"
                        else: starter_url = f"channel/{channel.lower()}/"
                        if self.__main_os__ == "Windows":
                            if submit_status: submit_status.submit("[BUNDLE] Fetching Package Manifest..", 30)
                            alleged_path = None
                            if lock == True:
                                if installPath.endswith("/"): installPathA = installPath[:-1]
                                elif installPath.endswith("\\"): installPathA = installPath[:-1]
                                else: installPathA = installPath
                                alleged_path = os.path.join(installPathA, f"RFFIInstall{client_label}BundleLock_{os.path.basename(pip_class.getUserFolder())}")
                                if os.path.exists(alleged_path):
                                    with open(alleged_path, "r", encoding="utf-8") as f: pid_str = f.read()
                                    if pid_str.isnumeric() and pip_class.getIfProcessIsOpened(pid=pid_str):
                                        if submit_status: submit_status.submit("[BUNDLE] There's already an install in progress! Awaiting finish..", 45)
                                        while os.path.exists(alleged_path) and pip_class.getIfProcessIsOpened(pid=pid_str): time.sleep(0.5)
                                        if os.path.exists(installPath):
                                            if debug == True: printDebugMessage(f"Install was finished and installed!")
                                            if submit_status: submit_status.submit("[BUNDLE] Installed succeeded!", 100)
                                            return {"success": True}
                                        else:
                                            if debug == True: printDebugMessage(f"Install was not finished and an error might have occurred!")
                                            if submit_status: submit_status.submit("\033ERR[BUNDLE] Install was not finished!", 100)
                                            return {"success": False}
                                    else:
                                        with open(alleged_path, "w", encoding="utf-8") as f: f.write(str(os.getpid()))
                                else:
                                    with open(alleged_path, "w", encoding="utf-8") as f: f.write(str(os.getpid()))
                            try:
                                if debug == True: printDebugMessage(f"Fetching Latest Package Manifest from Roblox's servers..")
                                rbx_manifest_link = f'https://{self.getBestRobloxDownloadServer()}/{starter_url}{cur_vers.get("client_version")}-rbxPkgManifest.txt'
                                rbx_hashes_link = f'https://{self.getBestRobloxDownloadServer()}/{starter_url}{cur_vers.get("client_version")}-rbxManifest.txt'
                                rbx_man_req = requests.get(rbx_manifest_link)
                                rbx_hashes_link = requests.get(rbx_hashes_link)
                                if rbx_man_req.ok:
                                    rbx_man_res = rbx_man_req.text
                                    rbx_lines = rbx_man_res.splitlines()
                                    def is_filename(rbx_line): return not rbx_line.isdigit() and not re.fullmatch(r'[a-fA-F0-9]{32}', rbx_line) and rbx_line != "v0"
                                    marked_install_files = [rbx_line for rbx_line in rbx_lines if is_filename(rbx_line)]
                                    rbx_hashes_res = rbx_hashes_link.text.strip().split("\n")
                                    rbx_hash_dict = {}
                                    for i in range(0, len(rbx_hashes_res), 2):
                                        file_path = rbx_hashes_res[i].strip()
                                        file_hash = rbx_hashes_res[i + 1].strip()
                                        rbx_hash_dict[file_path] = file_hash
                                    if submit_status: submit_status.submit("[BUNDLE] Downloading Packages..", 40)
                                    try:
                                        def calculate_rbx_hash(file_path):
                                            try:
                                                with open(file_path, "rb") as f:
                                                    hasher = hashlib.md5()
                                                    chunk = f.read(8192)
                                                    while chunk: 
                                                        hasher.update(chunk)
                                                        chunk = f.read(8192)
                                                return hasher.hexdigest()
                                            except Exception: return None
                                        downloaded_zip_files = []
                                        per_step = 0
                                        for i in marked_install_files:
                                            per_step += 1
                                            if not i == "":
                                                if submit_status: submit_status.submit(f"[BUNDLE] Downloading Package [{i}]..", round((per_step/(len(marked_install_files)))*100, 2))
                                                if debug == True: printDebugMessage(f"Downloading from Roblox's server: {i} [{round((per_step/(len(marked_install_files)))*100, 2)}/100]")
                                                down_req = requests.download(f'https://{self.getBestRobloxDownloadServer()}/{starter_url}{cur_vers.get("client_version")}-{i}', os.path.join(installPath, i))
                                                if down_req.ok: downloaded_zip_files.append(i)
                                                else:
                                                    printErrorMessage(f"Unable to install Roblox due to a download error.")
                                                    if alleged_path and os.path.exists(alleged_path): os.remove(alleged_path)
                                                    if submit_status: submit_status.submit(f"\033ERR[BUNDLE] Unable to install Roblox due to a download error.", 80)
                                                    if os.path.exists(installPath): shutil.rmtree(installPath, ignore_errors=True)
                                                    return {"success": False}
                                        if verify == True:
                                            per_step = 0
                                            verified = True
                                            if submit_status: submit_status.submit(f"[BUNDLE] Verifying Packages..", 0)
                                            for i in downloaded_zip_files:
                                                per_step += 1
                                                if submit_status: submit_status.submit(f"[BUNDLE] Verifying Package [{i}]..", round((per_step/(len(downloaded_zip_files)))*100, 2))
                                                if debug == True: printDebugMessage(f"Verifying from Roblox's server: {i} [{round((per_step/(len(downloaded_zip_files)))*100, 2)}/100]")
                                                if rbx_hash_dict.get(i):
                                                    hash_value = rbx_hash_dict.get(i)
                                                    calculated_hash = calculate_rbx_hash(os.path.join(installPath, i))
                                                    if calculated_hash == None:
                                                        if debug == True: printDebugMessage(f"Unable to verify file: {i}")
                                                        continue
                                                    elif not (calculated_hash == hash_value):
                                                        if debug == True: printDebugMessage(f"Unable to verify file: {hash_value} => {calculated_hash}")
                                                        verified = False
                                                        break
                                            if verified == False:
                                                printErrorMessage(f"Unable to install Roblox due to a verification error.")
                                                if alleged_path and os.path.exists(alleged_path): os.remove(alleged_path)
                                                if submit_status: submit_status.submit(f"\033ERR[BUNDLE] Unable to install Roblox due to a verification error.", 80)
                                                if os.path.exists(installPath): shutil.rmtree(installPath, ignore_errors=True)
                                                return {"success": False}
                                        per_step = 0
                                        if submit_status: submit_status.submit(f"[BUNDLE] Installing Packages..", 0)
                                        for i in downloaded_zip_files:
                                            per_step += 1
                                            if submit_status: submit_status.submit(f"[BUNDLE] Installing Package [{i}]..", round((per_step/(len(downloaded_zip_files)))*100, 2))
                                            if debug == True: printDebugMessage(f"Installing package: {i} [{round((per_step/(len(downloaded_zip_files)))*100, 2)}/100]")
                                            if studio == True and self.roblox_studio_bundle_files.get(i): export_destination = self.roblox_studio_bundle_files.get(i)
                                            elif not (studio == True) and self.roblox_bundle_files.get(i): export_destination = self.roblox_bundle_files.get(i)
                                            elif i.endswith(".zip"): export_destination = "/"
                                            makedirs(f'{installPath}{export_destination}')
                                            if i.endswith(".zip"):
                                                zip_extract = pip_class.unzipFile(os.path.join(installPath, i), f'{installPath}{export_destination}')
                                                if zip_extract.returncode == 0:
                                                    os.remove(os.path.join(installPath, i))
                                                    if debug == True: printDebugMessage(f"Successfully exported {i}!")
                                                elif debug == True: printDebugMessage(f"Unable to export: {i}")
                                            if i == "WebView2RuntimeInstaller.zip":
                                                try:
                                                    reg_sets = [
                                                        (win32con.HKEY_LOCAL_MACHINE, "SOFTWAREWOW6432Node\\Microsoft\\EdgeUpdate\\Clients\\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}", 0),
                                                        (win32con.HKEY_CURRENT_USER, "Software\\Microsoft\\EdgeUpdate\\Clients\\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}", 0)
                                                    ]
                                                    if pip_class.getIf32BitWindows():
                                                        reg_sets = [
                                                            (win32con.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\EdgeUpdate\\Clients\\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}", win32con.KEY_WOW64_64KEY),
                                                            (win32con.HKEY_CURRENT_USER, "Software\\Microsoft\\EdgeUpdate\\Clients\\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}", 0)
                                                        ]
                                                    vers = None
                                                    for hive, path, view in reg_sets:
                                                        try:
                                                            reg_key = win32api.RegOpenKeyEx(hive, path, 0, win32con.KEY_READ | view)
                                                            version, _ = win32api.RegQueryValueEx(reg_key, "pv")
                                                            win32api.RegCloseKey(reg_key)
                                                            vers = version
                                                        except Exception: pass
                                                    if vers:
                                                        if debug == True: printDebugMessage(f"WebView2 (vers: {version}) is currently installed!")
                                                    else: raise Exception("oranges!!")
                                                except Exception:
                                                    try:
                                                        web2_res = subprocess.run([os.path.join(installPath, "WebView2RuntimeInstaller", "MicrosoftEdgeWebview2Setup.exe"), "/silent", "/install"])
                                                        if web2_res.returncode == 0: printDebugMessage(f"WebView2 has been installed successfully!")
                                                        elif web2_res.returncode == 2147747880: printDebugMessage(f"WebView2 is currently installed!")
                                                        else: printErrorMessage(f"WebView2 has failed to be installed! Code: {web2_res.returncode}")
                                                    except Exception as e: printErrorMessage(f"WebView2 has failed to be installed! Exception: {str(e)}")
                                        with open(os.path.join(installPath, "RobloxVersion.json"), "w", encoding="utf-8") as f: json.dump({"ClientVersion": cur_vers.get("client_version", "version-000000000000"), "AppVersion": cur_vers.get("hash", "0.000.0.0000000")}, f, indent=4)
                                        with open(os.path.join(installPath, "AppSettings.xml"), "w", encoding="utf-8") as f: f.write('<?xml version="1.0" encoding="UTF-8"?><Settings><ContentFolder>content</ContentFolder><BaseUrl>https://www.roblox.com</BaseUrl></Settings>')
                                        if alleged_path and os.path.exists(alleged_path): os.remove(alleged_path)
                                        if submit_status: submit_status.submit(f"[BUNDLE] Successfully installed Roblox {client_label} Bundle!", 100)
                                        if debug == True: printDebugMessage(f"Successfully installed Roblox {client_label} to: {installPath} [Client: {cur_vers.get('client_version')}]")
                                        return {"success": True}
                                    except Exception as e:
                                        if alleged_path and os.path.exists(alleged_path): os.remove(alleged_path)
                                        if submit_status: submit_status.submit(f"\033ERR[BUNDLE] Unable to download and install Roblox {client_label} Bundle!", 100)
                                        if debug == True: printDebugMessage(f"Unable to install Roblox Bundle: {str(e)}")
                                        if os.path.exists(installPath): shutil.rmtree(installPath, ignore_errors=True)
                                        return {"success": False}
                                else:
                                    if alleged_path and os.path.exists(alleged_path): os.remove(alleged_path)
                                    if debug == True: printDebugMessage(f"Unable to download Roblox manifest due to an http error. Code: {rbx_man_req.status_code}")
                                    if submit_status: submit_status.submit("\033ERR[BUNDLE] Unable to fetch Roblox manifest file!", 100)
                                    if os.path.exists(installPath): shutil.rmtree(installPath, ignore_errors=True)
                                    return {"success": False}
                            except Exception as e:
                                if alleged_path and os.path.exists(alleged_path): os.remove(alleged_path)
                                if submit_status: submit_status.submit(f"\033ERR[BUNDLE] Unable to download and install Roblox {client_label} Bundle!", 100)
                                if debug == True: printDebugMessage(f"Unable to install Roblox Bundle: {str(e)}")
                                if os.path.exists(installPath): shutil.rmtree(installPath, ignore_errors=True)
                                return {"success": False}
                        elif self.__main_os__ == "Darwin":
                            zip_name = f'Roblox{"StudioApp" if studio == True else "Player"}.zip'
                            alleged_path = None
                            if lock == True:
                                if installPath.endswith("/"): installPathA = installPath[:-1]
                                elif installPath.endswith("\\"): installPathA = installPath[:-1]
                                else: installPathA = installPath
                                alleged_path = os.path.join(installPathA, f"RFFIInstall{'Studio' if studio == True else 'Player'}BundleLock_{os.path.basename(pip_class.getUserFolder())}")
                                if os.path.exists(alleged_path):
                                    with open(alleged_path, "r", encoding="utf-8") as f: pid_str = f.read()
                                    if pid_str.isnumeric() and pip_class.getIfProcessIsOpened(pid=pid_str):
                                        if submit_status: submit_status.submit("[BUNDLE] There's already an install in progress! Awaiting finish..", 0)
                                        while os.path.exists(alleged_path) and pip_class.getIfProcessIsOpened(pid=pid_str): time.sleep(0.5)
                                        if os.path.exists(installPath):
                                            if debug == True: printDebugMessage(f"Install was finished and installed!")
                                            if submit_status: submit_status.submit("[BUNDLE] Installed succeeded!", 100)
                                            return {"success": True}
                                        else:
                                            if debug == True: printDebugMessage(f"Install was not finished and an error might have occurred!")
                                            if submit_status: submit_status.submit("\033ERR[BUNDLE] Install was not finished!", 100)
                                            return {"success": False}
                                    else:
                                        with open(alleged_path, "w", encoding="utf-8") as f: f.write(str(os.getpid()))
                                else:
                                    with open(alleged_path, "w", encoding="utf-8") as f: f.write(str(os.getpid()))
                            roblox_player_down = f'https://{self.getBestRobloxDownloadServer()}/{starter_url}mac/{"arm64/" if platform.machine() == "arm64" else ""}{cur_vers.get("client_version")}-{zip_name}'
                            if submit_status: submit_status.submit(f"[BUNDLE] Downloading Roblox App!", 0)
                            if debug == True: printDebugMessage(f"Downloading {client_label} from Roblox's server: {roblox_player_down}")
                            try:
                                class download_stat:
                                    def submit(self, info):
                                        if submit_status: submit_status.submit(f"[BUNDLE] Downloading Roblox App!", int((info.percent/10)*3))
                                down_req = requests.download(roblox_player_down, os.path.join(installPath, zip_name), submit_status=download_stat())
                                if down_req.ok and os.path.exists(os.path.join(installPath, zip_name)):
                                    if os.path.exists(os.path.join(installPath, f"Roblox{client_label}")) or os.path.exists(appPath):
                                        if debug == True: printDebugMessage(f"Cleaning before install..")
                                        if os.path.exists(os.path.join(installPath, f"Roblox{client_label}")): shutil.rmtree(os.path.join(installPath, f"Roblox{client_label}"), ignore_errors=True)
                                        if os.path.exists(os.path.join(appPath)): shutil.rmtree(os.path.join(appPath), ignore_errors=True)
                                    if submit_status: submit_status.submit(f"[BUNDLE] Extracting Roblox App!", 30)
                                    if debug == True: printDebugMessage(f"Extracting Player from Downloaded ZIP: {os.path.join(installPath, zip_name)}")
                                    def zip_moving(): 
                                        if submit_status: submit_status.submit(f"[BUNDLE] Moving Roblox Files!", 55)
                                    zip_extract = pip_class.unzipFile(os.path.join(installPath, zip_name), appPath, ["Contents"], [f"Roblox{client_label}.app/Contents/*"], moving_file_func=zip_moving)
                                    if zip_extract.returncode == 0:
                                        if submit_status: submit_status.submit(f"[BUNDLE] Cleaning up {client_label}!", 80)
                                        if debug == True: printDebugMessage(f"Cleaning up..")
                                        os.remove(os.path.join(installPath, zip_name))
                                        with open(os.path.join(appPath, "Contents", "MacOS", "RobloxVersion.json"), "w", encoding="utf-8") as f: json.dump({"ClientVersion": cur_vers.get("client_version", "version-000000000000"), "AppVersion": cur_vers.get("hash", "0.000.0.0000000")}, f, indent=4)
                                        if submit_status: submit_status.submit(f"[BUNDLE] Successfully installed Roblox {client_label} Bundle!", 100)
                                        if debug == True: printDebugMessage(f"Successfully installed Roblox to: {installPath} [Client: {cur_vers.get('client_version')}]")
                                        if alleged_path and os.path.exists(alleged_path): os.remove(alleged_path)
                                        return {"success": True}
                                    else:
                                        if debug == True: printDebugMessage(f"Unable to extract {client_label} due to an error!")
                                        if submit_status: submit_status.submit(f"\033ERR[BUNDLE] Failed to extract Roblox {client_label}.", 100)
                                        if os.path.exists(appPath): shutil.rmtree(appPath, ignore_errors=True)
                                        if alleged_path and os.path.exists(alleged_path): os.remove(alleged_path)
                                        return {"success": False}
                                else:
                                    if debug == True: printDebugMessage(f"Unable to download the Roblox {client_label}.")
                                    if submit_status: submit_status.submit(f"\033ERR[BUNDLE] Failed to download Roblox {client_label}.", 100)
                                    if os.path.exists(appPath): shutil.rmtree(appPath, ignore_errors=True)
                                    if os.path.exists(os.path.join(installPath, zip_name)): os.remove(os.path.join(installPath, zip_name))
                                    if alleged_path and os.path.exists(alleged_path): os.remove(alleged_path)
                                    return {"success": False}
                            except Exception as e:
                                if debug == True: printDebugMessage(f"Unable to download and install the Roblox {client_label}."); printDebugMessage(f"Exception: {str(e)}")
                                if submit_status: submit_status.submit(f"\033ERR[BUNDLE] Failed to download and install Roblox {client_label}.", 100)
                                if os.path.exists(appPath): shutil.rmtree(appPath, ignore_errors=True)
                                if alleged_path and os.path.exists(alleged_path): os.remove(alleged_path)
                                return {"success": False}
                    else:
                        if debug == True: printDebugMessage(f"Unable to fetch install bootstrapper settings from Roblox.")
                        if submit_status: submit_status.submit("\033ERR[BUNDLE] Unable to fetch bootstrapper settings.", 100)
                        return {"success": False}
                else:
                    if debug == True: printDebugMessage(f"Unable to fetch Roblox manifest file due to an http error.")
                    if submit_status: submit_status.submit("\033ERR[BUNDLE] Unable to fetch Roblox manifest file!", 100)
                    return {"success": False}
            except Exception as e:
                if debug == True: printDebugMessage(f"Unable to download and install Roblox Bundle. Error: {str(e)}")
                if submit_status: submit_status.submit("\033ERR[INSTALL] Unable to download and install Roblox Bundle!", 100)
                return {"success": False}
        else:
            self.unsupportedFunction()
            if submit_status: submit_status.submit("\033ERR[BUNDLE] Roblox Fast Flags Installer is only supported for macOS and Windows.", 100)
            return {"success": False}
    def uninstallRoblox(self, studio: bool=False, clearUserData: bool=True, debug: bool=False):
        if self.getIfRobloxIsOpen(studio=studio):
            self.endRoblox(studio=studio)
            if debug == True: printDebugMessage("Ending Roblox Instances..")
                
        if self.__main_os__ == "Darwin":
            try:
                if studio == True and os.path.exists(macOS_studioDir):
                    if submit_status: submit_status.submit("[UNINSTALL] Removing app..", 0)
                    if debug == True: printDebugMessage("Removing Roblox Studio App from Applications..")
                    shutil.rmtree(macOS_studioDir, ignore_errors=True)
                elif os.path.exists(macOS_dir):
                    if submit_status: submit_status.submit("[UNINSTALL] Removing app..", 0)
                    if debug == True: printDebugMessage("Removing Roblox App from Applications..")
                    shutil.rmtree(macOS_dir, ignore_errors=True)
                if os.path.exists(os.path.join(user_folder, "Library", "Roblox", "OTAPatchBackups")):
                    if submit_status: submit_status.submit("[UNINSTALL] Removing OTA Patch Backups..", 20)
                    if debug == True: printDebugMessage("Removing OTA Patch Backups..")
                    shutil.rmtree(os.path.join(user_folder, "Library", "Roblox", "OTAPatchBackups"), ignore_errors=True)
                if os.path.exists(os.path.join(user_folder, "Library", "Roblox", "placeIDEState")):
                    if submit_status: submit_status.submit("[UNINSTALL] Place IDE States..", 40)
                    if debug == True: printDebugMessage("Removing Place IDE States..")
                    shutil.rmtree(os.path.join(user_folder, "Library", "Roblox", "placeIDEState"), ignore_errors=True)
                if os.path.exists(os.path.join(user_folder, "Library", "Logs", "Roblox")):
                    if submit_status: submit_status.submit("[UNINSTALL] Removing Logs..", 60)
                    if debug == True: printDebugMessage("Removing Roblox Logs..")
                    shutil.rmtree(os.path.join(user_folder, "Library", "Logs", "Roblox"), ignore_errors=True)
                if clearUserData == True and os.path.exists(os.path.join(user_folder, "Library", "Roblox")):
                    if submit_status: submit_status.submit("[UNINSTALL] Removing Roblox User Data..", 80)
                    if debug == True: printDebugMessage("Removing Roblox User Data..")
                    shutil.rmtree(os.path.join(user_folder, "Library", "Roblox"), ignore_errors=True)
                if submit_status: submit_status.submit("[UNINSTALL] Successfully uninstalled Roblox!", 100)
            except Exception as e: printErrorMessage(f"Something went wrong deleting Roblox: {str(e)}")
        elif self.__main_os__ == "Windows":
            try:
                for i in os.listdir(f"{windows_versions_dir}"):
                    if os.path.isdir(os.path.join(windows_versions_dir, i)) and os.path.exists(os.path.join(windows_versions_dir, i, "RobloxPlayerBeta.exe")):
                        if submit_status: submit_status.submit("[UNINSTALL] Removing app..", 0)
                        if debug == True: printDebugMessage("Removing Roblox App from System..")
                        shutil.rmtree(os.path.join(windows_versions_dir, i), ignore_errors=True)
                if os.path.exists(os.path.join(windows_dir, "OTAPatchBackups")):
                    if submit_status: submit_status.submit("[UNINSTALL] Removing OTA Patch Backups..", 45)
                    if debug == True: printDebugMessage("Removing OTA Patch Backups..")
                    shutil.rmtree(os.path.join(windows_dir, "OTAPatchBackups"), ignore_errors=True)
                if os.path.exists(os.path.join(windows_dir, "placeIDEState")):
                    if submit_status: submit_status.submit("[UNINSTALL] Removing Place IDE States..", 60)
                    if debug == True: printDebugMessage("Removing Place IDE States..")
                    shutil.rmtree(os.path.join(windows_dir, "placeIDEState"), ignore_errors=True)
                if os.path.exists(os.path.join(windows_dir, "Downloads", "roblox-player")):
                    if submit_status: submit_status.submit("[UNINSTALL] Removing Roblox Downloads..", 75)
                    if debug == True: printDebugMessage("Removing Downloads..")
                    shutil.rmtree(os.path.join(windows_dir, "Downloads", "roblox-player"), ignore_errors=True)
                if os.path.exists(os.path.join(windows_dir, "UniversalApp")):
                    if submit_status: submit_status.submit("[UNINSTALL] Removing Universe App..", 85)
                    if debug == True: printDebugMessage("Removing Universal App..")
                    shutil.rmtree(os.path.join(windows_dir, "UniversalApp"), ignore_errors=True)
                if os.path.exists(os.path.join(windows_dir, "logs")):
                    if submit_status: submit_status.submit("[UNINSTALL] Removing Logs..", 90)
                    if debug == True: printDebugMessage("Removing Roblox Logs..")
                    shutil.rmtree(os.path.join(windows_dir, "logs"), ignore_errors=True)
                if clearUserData == True and os.path.exists(windows_dir):
                    if submit_status: submit_status.submit("[UNINSTALL] Removing Roblox User Data..", 95)
                    if debug == True: printDebugMessage("Removing Roblox User Data..")
                    shutil.rmtree(windows_dir, ignore_errors=True)
                if submit_status: submit_status.submit("[UNINSTALL] Successfully uninstalled Roblox!", 100)
            except Exception as e: printErrorMessage(f"Something went wrong starting Roblox Installer: {str(e)}")
        else:
            self.unsupportedFunction()
            if submit_status: submit_status.submit("\033ERR[INSTALL] Roblox Fast Flags Installer is only supported for macOS and Windows.", 100)
    def reinstallRoblox(self, studio: bool=False, debug: bool=False, clearUserData: bool=True, disableRobloxAutoOpen: bool=False, copyRobloxInstallerPath: str="", downloadInstaller: bool=False):
        if self.__main_os__ == "Darwin" or self.__main_os__ == "Windows":
            client_label = "Studio" if studio == True else "Player"
            if self.getIfRobloxIsOpen(studio=studio):
                self.endRoblox(studio=studio)
                if debug == True: printDebugMessage(f"Ending Roblox {client_label} Instances..")
            channel = "LIVE"
            if downloadInstaller == True:
                channel_res = self.getCurrentClientVersion(studio=studio)
                if channel_res.get("success") == True: channel = channel_res.get("channel", "LIVE")           
            if submit_status: submit_status.submit(f"Uninstalling Roblox {client_label}", 0)
            self.uninstallRoblox(studio=studio, debug=debug, clearUserData=clearUserData)
            if submit_status: submit_status.submit(f"Installing Roblox {client_label}", 50)
            s = self.installRoblox(studio=studio, debug=debug, disableRobloxAutoOpen=disableRobloxAutoOpen, copyRobloxInstallerPath=copyRobloxInstallerPath, downloadInstaller=downloadInstaller, downloadChannel=channel)
            if submit_status: submit_status.submit(f"Successfully reinstalled Roblox {client_label}!", 100)
            return s
        else:
            self.unsupportedFunction()
            if submit_status: submit_status.submit("\033ERR[INSTALL] Roblox Fast Flags Installer is only supported for macOS and Windows.", 100)
            return {"success": False}
    def endRobloxStudio(self, *args, **kwargs): """This function has been deprecated for ```Handler.endRoblox(studio=True)```"""; return self.endRoblox(studio=True, *args, **kwargs)
    def getIfRobloxStudioIsOpen(self, *args, **kwargs): """This function has been deprecated for ```Handler.getIfRobloxIsOpen(studio=True)```"""; return self.getIfRobloxIsOpen(studio=True, *args, **kwargs)
    def getLatestStudioClientVersion(self, *args, **kwargs): """This function has been deprecated for ```Handler.getLatestClientVersion(studio=True)```"""; return self.getLatestClientVersion(studio=True, *args, **kwargs)
    def getCurrentStudioClientVersion(self, *args, **kwargs): """This function has been deprecated for ```Handler.getCurrentClientVersion(studio=True)```"""; return self.getCurrentClientVersion(studio=True, *args, **kwargs)
    def getLatestOpenedRobloxStudioPid(self, *args, **kwargs): """This function has been deprecated for ```Handler.getLatestOpenedRobloxPid(studio=True)```"""; return self.getLatestOpenedRobloxPid(studio=True, *args, **kwargs)
    def getOpenedRobloxStudioPids(self, *args, **kwargs): """This function has been deprecated for ```Handler.getOpenedRobloxPids(studio=True)```"""; return self.getOpenedRobloxPids(studio=True, *args, **kwargs)
    def getAllOpenedRobloxStudioWindows(self, *args, **kwargs): """This function has been deprecated for ```Handler.getAllOpenedRobloxWindows(studio=True)```"""; return self.getAllOpenedRobloxWindows(studio=True, *args, **kwargs)
    def getLatestRobloxStudioAppSettings(self, *args, **kwargs): """This function has been deprecated for ```Handler.getLatestRobloxAppSettings(studio=True)```"""; return self.getLatestRobloxAppSettings(studio=True, *args, **kwargs)
    def openRobloxStudio(self, *args, **kwargs): """This function has been deprecated for ```Handler.openRoblox(studio=True)```"""; return self.openRoblox(studio=True, *args, **kwargs)
    def downloadRobloxStudioInstaller(self, *args, **kwargs): """This function has been deprecated for ```Handler.downloadRobloxInstaller(studio=True)```"""; return self.downloadRobloxInstaller(studio=True, *args, **kwargs)
    def installRobloxStudio(self, *args, **kwargs): """This function has been deprecated for ```Handler.installRoblox(studio=True)```"""; return self.installRoblox(studio=True, *args, **kwargs)
    def installRobloxStudioBundle(self, *args, **kwargs): """This function has been deprecated for ```Handler.installRobloxBundle(studio=True)```"""; return self.installRobloxBundle(studio=True, *args, **kwargs)
    def uninstallRobloxStudio(self, *args, **kwargs): """This function has been deprecated for ```Handler.uninstallRoblox(studio=True)```"""; return self.uninstallRoblox(studio=True, *args, **kwargs)
    def reinstallRobloxStudio(self, *args, **kwargs): """This function has been deprecated for ```Handler.reinstallRoblox(studio=True)```"""; return self.reinstallRoblox(studio=True, *args, **kwargs)
    def unsupportedFunction(self): printLog("Roblox Fast Flags Installer is only supported for macOS and Windows.")
Main = Handler
def main():
    handler = Handler()
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
            return
        printWarnMessage("Made by Efaz from efaz.dev!")
        printWarnMessage(f"v{script_version}")
        printWarnMessage("-----------")
        def waitForInternet():
            if pip_class.getIfConnectedToInternet() == False:
                printWarnMessage("--- Waiting for Internet ---")
                printMainMessage("Please connect to your internet in order to continue! If you're connecting to a VPN, try reconnecting.")
                while pip_class.getIfConnectedToInternet() == False: time.sleep(0.05)
                return True
        if waitForInternet() == True: printWarnMessage("-----------")
        if main_os == "Windows": printMainMessage(f"System OS: {main_os} ({platform.version()})")
        elif main_os == "Darwin": printMainMessage(f"System OS: {main_os} (macOS {platform.mac_ver()[0]})")
        else:
            input("> ")
            return
        if not pip_class.osSupported(windows_build=17763, macos_version=(10,13,0)):
            if main_os == "Windows": printErrorMessage("Roblox Fast Flags Installer is only supported for Windows 10.0.17763 (October 2018) or higher. Please update your operating system in order to continue!")
            elif main_os == "Darwin": printErrorMessage("Roblox Fast Flags Installer is only supported for macOS 10.13 (High Sierra) or higher. Please update your operating system in order to continue!")
            input("> ")
            return
        printMainMessage(f"Python Version: {pip_class.getCurrentPythonVersion()}{pip_class.getIfPythonVersionIsBeta() and ' (BETA)' or ''}")
        if not pip_class.pythonSupported(3, 11, 0):
            if not pip_class.pythonSupported(3, 6, 0):
                printErrorMessage("Please update your current installation of Python above 3.11.0")
                input("> ")
                return
            else:
                latest_python = pip_class.getLatestPythonVersion()
                printWarnMessage("--- Python Update Required ---")
                printMainMessage("Hello! In order to use Roblox Fast Flags Installer, you'll need to install Python 3.11 or higher in order to continue. ")
                printMainMessage(f"If you wish, you may install Python {latest_python} by typing \"y\" and continue.")
                printMainMessage("Otherwise, you may close the app by just continuing without typing.")
                if isYes(input("> ")) == True:
                    pip_class.pythonInstall(latest_python)
                    printSuccessMessage(f"If installed correctly, Python {latest_python} should be available to be used!")
                    printSuccessMessage("Please restart the script to install!")
                    input("> ")
                return
        if main_os == "Windows":
            if not os.path.exists(windows_dir):
                printErrorMessage("The Roblox Website App Path doesn't exist. Please install Roblox from your web browser in order to use!")
                return
        elif main_os == "Darwin":
            if not os.path.exists(macOS_dir):
                printErrorMessage("The Roblox Website App Path doesn't exist. Please install Roblox from your web browser in order to use!")
                return
            else:
                installed_roblox_version = handler.getCurrentClientVersion()
                if installed_roblox_version["success"] == True: printMainMessage(f"Current Roblox Version: {installed_roblox_version['version']}")
                else:
                    printErrorMessage("Something went wrong trying to determine your current Roblox version.")
                    input("> ")
                    return
        printWarnMessage("-----------")
    else:
        if main_os == "Windows": printWarnMessage(f"Starting Roblox Fast Flags Installer v{script_version}!")
        elif main_os == "Darwin": printWarnMessage(f"Starting Roblox Fast Flags Installer v{script_version}!")
        else:
            printErrorMessage("Please run this script on macOS/Windows.")
            return
        printWarnMessage("--------------------")

    def getUserId():
        app_settings = handler.getRobloxAppSettings()
        if app_settings.get("loggedInUser") and app_settings.get("loggedInUser").get("id"): return app_settings.get("loggedInUser").get("id")
        printMainMessage("Please input your User ID! This can be found on your profile in the URL: https://www.roblox.com/users/XXXXXXXX/profile")
        id = input("> ")
        if id.isnumeric(): return id
        elif isRequestClose(id):
            printMainMessage("Ending installation..")
            return
        else:
            printWarnMessage("Let's try again!")
            return getUserId()
    def getIfStudio():
        printMainMessage("Please select the type of Roblox would you like to install to!")
        printMainMessage("[1] = Roblox Player")
        printMainMessage("[2] = Roblox Studio")
        id = input("> ")
        if id == "1": return False
        elif id == "2": return True
        else: return getIfStudio()

    # Information
    user_id = getUserId()
    generated_json = {}
    is_studio = getIfStudio()

    if not user_id: return

    # Important Information
    printWarnMessage("--- Important Information ---")
    printMainMessage("May 2nd, 2025 - v2.0.3")
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
        if cap.isnumeric(): return cap
        else: return None
    if isYes(installFPSUnlocker) == True:
        # FPS Cap
        fpsCap = getFPSCap()

        # Roblox Vulkan Rendering
        printWarnMessage("- Roblox Vulkan Rendering -")
        printMainMessage("Would you like to use Vulkan Rendering? (It will remove the cap fully but may cause issues) (y/n)")
        useVulkan = input("> ")
        generated_json["FFlagTaskSchedulerLimitTargetFpsTo2402"] = "false"

        if fpsCap == None: generated_json["DFIntTaskSchedulerTargetFps"] = "9999"
        else: generated_json["DFIntTaskSchedulerTargetFps"] = fpsCap

        if isYes(useVulkan) == True: 
            generated_json["FFlagDebugGraphicsPreferVulkan"] = "true"
            if main_os == "Darwin": generated_json["FFlagDebugGraphicsDisableMetal"] =  "true"
        elif isNo(useVulkan) == True: 
            generated_json["FFlagDebugGraphicsPreferVulkan"] = "false"
            if main_os == "Darwin": generated_json["FFlagDebugGraphicsDisableMetal"] =  "false"
        elif isRequestClose(useVulkan) == True:
            printMainMessage("Ending installation..")
            return
    elif isRequestClose(installFPSUnlocker) == True:
        printMainMessage("Ending installation..")
        return
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
            return
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
        return
    elif isNo(installVerifiedBadge) == True: generated_json["FStringWhitelistVerifiedUserId"] = None

    # Rename Charts to Discover
    printWarnMessage("--- Replace Charts ---")
    printMainMessage("Would you like to rename Charts back to Discover (may work)? (y/n)")
    installRenameCharts = input("> ")
    if isYes(installRenameCharts) == True: generated_json["FFlagLuaAppChartsPageRenameIXP"] = "false"
    elif isRequestClose(installRenameCharts) == True:
        printMainMessage("Ending installation..")
        return
    elif isNo(installRenameCharts) == True: generated_json["FFlagLuaAppChartsPageRenameIXP"] = "true"

    # Enable Developer Tools
    printWarnMessage("--- Enable Developer Tools ---")
    printMainMessage("Would you like to enable Developer Tools inside of the Roblox App (when website frame is opened) (Ctrl+Shift+I)? (y/n)")
    installEnableDeveloper = input("> ")
    if isYes(installEnableDeveloper) == True: generated_json["FFlagDebugEnableNewWebView2DevTool"] = "true"
    elif isRequestClose(installEnableDeveloper) == True:
        printMainMessage("Ending installation..")
        return
    elif isNo(installEnableDeveloper) == True: generated_json["FFlagDebugEnableNewWebView2DevTool"] = "false"

    # Display FPS
    printWarnMessage("--- Display FPS ---")
    printMainMessage("Would you like your client to display the FPS? (y/n)")
    installFPSViewer = input("> ")
    if isYes(installFPSViewer) == True: generated_json["FFlagDebugDisplayFPS"] = "true"
    elif isRequestClose(installFPSViewer) == True:
        printMainMessage("Ending installation..")
        return
    elif isNo(installFPSViewer) == True: generated_json["FFlagDebugDisplayFPS"] = "false"

    # Disable Ads
    printWarnMessage("--- Disable Ads ---")
    printMainMessage("Would you like your client to disable ads? (y/n)")
    installRemoveAds = input("> ")
    if isYes(installRemoveAds) == True: generated_json["FFlagAdServiceEnabled"] = "false"
    elif isRequestClose(installRemoveAds) == True:
        printMainMessage("Ending installation..")
        return
    elif isNo(installRemoveAds) == True: generated_json["FFlagAdServiceEnabled"] = "true"

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
        return
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
        return
    elif isNo(installGenreSystem) == True:
        generated_json["FFlagLuaAppGenreUnderConstruction"] = "true"
        generated_json["FFlagLuaAppGenreUnderConstructionDesktopFix"] = "true"

    # Enable Freecam
    printWarnMessage("--- Enable Freecam ---")
    printMainMessage("Would you like to enable freecam on the Roblox client (only works if you're a Roblox Developer of a game or a Star Creator)? (y/n)")
    installFreecam = input("> ")
    if isYes(installFreecam) == True: generated_json["FFlagLoadFreecamModule"] = "true"
    elif isRequestClose(installFreecam) == True:
        printMainMessage("Ending installation..")
        return
    elif isNo(installFreecam) == True: generated_json["FFlagLoadFreecamModule"] = "false"

    # Enable New Camera Controls
    printWarnMessage("--- Enable New Camera Controls ---")
    printMainMessage("Would you like to enable new camera controls? (y/n)")
    installNewCamera = input("> ")
    if isYes(installNewCamera) == True: generated_json["FFlagNewCameraControls"] = "true"
    elif isRequestClose(installNewCamera) == True:
        printMainMessage("Ending installation..")
        return
    elif isNo(installNewCamera) == True: generated_json["FFlagNewCameraControls"] = "false"

    # Hide Internet Disconnect Message
    printWarnMessage("--- Hide Internet Disconnect Message ---")
    printMainMessage("Would you like to hide the Internet Disconnect message when you're kicked? (You will still be kicked, jsut the message will not show.) (y/n)")
    installHideDisconnect = input("> ")
    if isYes(installHideDisconnect) == True: generated_json["DFFlagDebugDisableTimeoutDisconnect"] = "true"
    elif isRequestClose(installHideDisconnect) == True:
        printMainMessage("Ending installation..")
        return
    elif isNo(installHideDisconnect) == True: generated_json["DFFlagDebugDisableTimeoutDisconnect"] = "false"

    # Disable In-Game Purchases
    printWarnMessage("--- Disable In-Game Purchases ---")
    printMainMessage("Would you like to disable in-game purchases (game-passes, developer products, etc.)? (You will still be kicked, jsut the message will not show.) (y/n)")
    installDisablePurchases = input("> ")
    if isYes(installDisablePurchases) == True: generated_json["DFFlagOrder66"] = "true"
    elif isRequestClose(installDisablePurchases) == True:
        printMainMessage("Ending installation..")
        return
    elif isNo(installDisablePurchases) == True: generated_json["DFFlagOrder66"] = "false"

    # Disable Voice Chat
    printWarnMessage("--- Disable Voice Chat ---")
    printMainMessage("Would you like to disable Voice Chat? (y/n)")
    installDisableVoiceChat = input("> ")
    if isYes(installDisableVoiceChat) == True: generated_json["DFFlagVoiceChat4"] = "false"
    elif isRequestClose(installDisableVoiceChat) == True:
        printMainMessage("Ending installation..")
        return
    elif isNo(installDisableVoiceChat) == True: generated_json["DFFlagVoiceChat4"] = "true"

    # Disable In-Game Chat
    printWarnMessage("--- Disable In-Game Chat ---")
    printMainMessage("Would you like to disable In-Game Chat? (y/n)")
    installDisableGameChat = input("> ")
    if isYes(installDisableGameChat) == True: generated_json["FFlagDebugForceChatDisabled"] = "true"
    elif isRequestClose(installDisableGameChat) == True:
        printMainMessage("Ending installation..")
        return
    elif isNo(installDisableGameChat) == True: generated_json["FFlagDebugForceChatDisabled"] = "false"

    # Disable Full Screen Title Bar
    printWarnMessage("--- Disable Full Screen Title Bar ---")
    printMainMessage("Would you like to disable the Title Bar when you go into full screen on the Roblox client? (y/n)")
    installDisableFullScreenTitle = input("> ")
    if isYes(installDisableFullScreenTitle) == True: generated_json["FIntFullscreenTitleBarTriggerDelayMillis"] = "3600000"
    elif isRequestClose(installDisableFullScreenTitle) == True:
        printMainMessage("Ending installation..")
        return
    elif isNo(installDisableFullScreenTitle) == True: generated_json["FIntFullscreenTitleBarTriggerDelayMillis"] = None

    # Enable Red Text Font
    printWarnMessage("--- Enable Red Text Font ---")
    printMainMessage("Would you like to enable Red text instead of White text color in the lua app? (y/n)")
    installRedText = input("> ")
    if isYes(installRedText) == True: generated_json["FStringDebugHighlightSpecificFont"] = "rbxasset://fonts/families/BuilderSans.json"
    elif isRequestClose(installRedText) == True:
        printMainMessage("Ending installation..")
        return
    elif isNo(installRedText) == True: generated_json["FStringDebugHighlightSpecificFont"] = None

    # Remove Automatically Translated
    printWarnMessage("--- Remove Automatically Translated ---")
    printMainMessage("Would you like to remove the chat automatically translated message in the chat? (y/n)")
    installRemoveAutoTranslate = input("> ")
    if isYes(installRemoveAutoTranslate) == True: generated_json["FFlagChatTranslationEnableSystemMessage"] = "false"
    elif isRequestClose(installRemoveAutoTranslate) == True:
        printMainMessage("Ending installation..")
        return
    elif isNo(installRemoveAutoTranslate) == True: generated_json["FFlagChatTranslationEnableSystemMessage"] = "true"

    # Rendering Mode
    got_modes = []
    ui_options = {}
    if main_os == "Darwin": got_modes.append("Metal (for MacOS)")
    got_modes.append("Vulkan (may cause issues)")
    got_modes.append("OpenGL")
    got_modes.append("DirectX 10")
    got_modes.append("DirectX 11")
    got_modes = sorted(got_modes)
    count = 1

    generated_json["FFlagDebugGraphicsPreferMetal"] = None
    generated_json["FFlagDebugGraphicsDisableDirect3D11"] = None
    generated_json["FFlagDebugGraphicsPreferVulkan"] = None
    generated_json["FFlagDebugGraphicsPreferOpenGL"] = None
    generated_json["FFlagDebugGraphicsPreferD3D11FL10"] = None
    generated_json["FFlagDebugGraphicsPreferD3D11"] = None
        
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
        if opt == "Metal (for MacOS)": generated_json["FFlagDebugGraphicsPreferMetal"] = "true"
        elif opt == "Vulkan (may cause issues)":
            generated_json["FFlagDebugGraphicsDisableDirect3D11"] = "true"
            generated_json["FFlagDebugGraphicsPreferVulkan"] = "true"
        elif opt == "OpenGL":
            generated_json["FFlagDebugGraphicsDisableDirect3D11"] = "true"
            generated_json["FFlagDebugGraphicsPreferOpenGL"] = "true"
        elif opt == "DirectX 10": generated_json["FFlagDebugGraphicsPreferD3D11FL10"] = "true"
        elif opt == "DirectX 11": generated_json["FFlagDebugGraphicsPreferD3D11"] = "true"

    # Lighting Mode
    got_modes = []
    ui_options = {}
    got_modes.append("Voxel Lighting (Phase 1)")
    got_modes.append("Shadowmap Lighting (Phase 2)")
    got_modes.append("Future Lighting (Phase 3)")
    got_modes.append("Unified Lighting")
    got_modes = sorted(got_modes)
    count = 1

    generated_json["DFFlagDebugRenderForceTechnologyVoxel"] = None
    generated_json["FFlagDebugForceFutureIsBrightPhase2"] = None
    generated_json["FFlagDebugForceFutureIsBrightPhase3"] = None
    generated_json["FFlagRenderUnifiedLighting10"] = None
    generated_json["FFlagUnifiedLightingBetaFeature"] = None
        
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
        if opt == "Voxel Lighting (Phase 1)": generated_json["DFFlagDebugRenderForceTechnologyVoxel"] = "true"
        elif opt == "Shadowmap Lighting (Phase 2)": generated_json["FFlagDebugForceFutureIsBrightPhase2"] = "true"
        elif opt == "Future Lighting (Phase 3)": generated_json["FFlagDebugForceFutureIsBrightPhase3"] = "true"
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

    generated_json["DFFlagTextureQualityOverrideEnabled"] = None
    generated_json["DFIntTextureQualityOverride"] = None
        
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
    if isYes(installDisableHighLight) == True: generated_json["DFFlagRenderHighlightManagerPrepare"] = "true"
    elif isRequestClose(installDisableHighLight) == True:
        printMainMessage("Ending installation..")
        return
    elif isNo(installDisableHighLight) == True: generated_json["DFFlagRenderHighlightManagerPrepare"] = "false"

    # Disable VC Beta Badge
    printWarnMessage("--- Disable VC Beta Badge ---")
    printMainMessage("Would you like to disable the VC beta badge on the client? (y/n)")
    print("\033[38;5;34mThis FFlag was from the Dantez GitHub! (https://github.com/Dantezz025/Roblox-Fast-Flags)\033[0m")
    installVCBadge = input("> ")
    if isYes(installVCBadge) == True: 
        generated_json["FFlagVoiceBetaBadge"] = "false"
        generated_json["FFlagTopBarUseNewBadge"] = "false"
        generated_json["FFlagEnableBetaBadgeLearnMore"] = "false"
        generated_json["FFlagBetaBadgeLearnMoreLinkFormview"] = "false"
        generated_json["FFlagControlBetaBadgeWithGuac"] = "false"
    elif isRequestClose(installVCBadge) == True:
        printMainMessage("Ending installation..")
        return
    elif isNo(installVCBadge) == True: 
        generated_json["FFlagVoiceBetaBadge"] = "true"
        generated_json["FFlagTopBarUseNewBadge"] = "true"
        generated_json["FFlagEnableBetaBadgeLearnMore"] = "true"
        generated_json["FFlagBetaBadgeLearnMoreLinkFormview"] = "true"
        generated_json["FFlagControlBetaBadgeWithGuac"] = "true"

    # Fix Stutter Animations
    printWarnMessage("--- Stutter Animations Fix ---")
    printMainMessage("Would you like to disable the VC beta badge on the client? (y/n)")
    print("\033[38;5;34mThis FFlag was from the Dantez GitHub! (https://github.com/Dantezz025/Roblox-Fast-Flags)\033[0m")
    installStutterAnimation = input("> ")
    if isYes(installStutterAnimation) == True:  generated_json["DFIntTimestepArbiterThresholdCFLThou"] = "300"
    elif isRequestClose(installStutterAnimation) == True:
        printMainMessage("Ending installation..")
        return
    elif isNo(installStutterAnimation) == True: generated_json["DFIntTimestepArbiterThresholdCFLThou"] = None

    # Fix Stutter Animations
    printWarnMessage("--- Disable Wi-Fi Disconnect ---")
    printMainMessage("Would you like to disable disconnecting from servers when wifi is changed on the client? (y/n)")
    print("\033[38;5;34mThis FFlag was from the Dantez GitHub! (https://github.com/Dantezz025/Roblox-Fast-Flags)\033[0m")
    installWifiConnect = input("> ")
    if isYes(installWifiConnect) == True:  generated_json["DFFlagDebugDisableTimeoutDisconnect"] = "true"
    elif isRequestClose(installWifiConnect) == True:
        printMainMessage("Ending installation..")
        return
    elif isNo(installWifiConnect) == True: generated_json["DFFlagDebugDisableTimeoutDisconnect"] = "false"

    # Rename Connections to Friends
    printWarnMessage("--- Rename Connections to Friends ---")
    printMainMessage("Would you like to enable renaming Connections back to Friends on the client? (y/n)")
    installConnectionsRename = input("> ")
    if isYes(installConnectionsRename) == True: 
        generated_json.update({
            "FFlagLuaAppRenameFriendsToConnectionsEdp": "false",
            "FFlagRenameFriendsToConnections": "false",
            "FFlagRenameFriendsToConnectionsAppChat2": "false",
            "FFlagRenameFriendsToConnectionsCoreUI": "false",
            "FFlagRenameFriendsToConnectionsFriendsMenu": "false",
            "FFlagRenameFriendsToConnectionsFriendsPage": "false",
            "FFlagRenameFriendsToConnectionsPartyLobby": "false",
            "FFlagRenameFriendsToConnectionsProfile": "false",
            "FFlagRenameFriendsToConnectionsWebviewHeading": "false"
        })
    elif isRequestClose(installConnectionsRename) == True:
        printMainMessage("Ending installation..")
        return
    elif isNo(installConnectionsRename) == True: 
        generated_json.update({
            "FFlagLuaAppRenameFriendsToConnectionsEdp": "true",
            "FFlagRenameFriendsToConnections": "true",
            "FFlagRenameFriendsToConnectionsAppChat2": "true",
            "FFlagRenameFriendsToConnectionsCoreUI": "true",
            "FFlagRenameFriendsToConnectionsFriendsMenu": "true",
            "FFlagRenameFriendsToConnectionsFriendsPage": "true",
            "FFlagRenameFriendsToConnectionsPartyLobby": "true",
            "FFlagRenameFriendsToConnectionsProfile": "true",
            "FFlagRenameFriendsToConnectionsWebviewHeading": "true"
        })

    # Reduce FPS #1
    printWarnMessage("--- Reduce FPS #1 ---")
    printMainMessage("Would you like to enable reducing FPS using pack 1? (y/n)")
    print("\033[38;5;34mThis FFlag was from the Dantez GitHub! (https://github.com/Dantezz025/Roblox-Fast-Flags)\033[0m")
    installReduceFPS1 = input("> ")
    if isYes(installReduceFPS1) == True:  
        generated_json["FFlagDebugDisableTelemetryEphemeralCounter"] = "true"
        generated_json["FFlagDebugDisableTelemetryEphemeralStat"] = "true"
        generated_json["FFlagDebugDisableTelemetryEventIngest"] = "true"
        generated_json["FFlagDebugDisableTelemetryPoint"] = "true"
        generated_json["FFlagDebugDisableTelemetryV2Counter"] = "true"
        generated_json["FFlagDebugDisableTelemetryV2Event"] = "true"
        generated_json["FFlagDebugDisableTelemetryV2Stat"] = "true"
    elif isRequestClose(installReduceFPS1) == True:
        printMainMessage("Ending installation..")
        return
    elif isNo(installReduceFPS1) == True:
        generated_json["FFlagDebugDisableTelemetryEphemeralCounter"] = "false"
        generated_json["FFlagDebugDisableTelemetryEphemeralStat"] = "false"
        generated_json["FFlagDebugDisableTelemetryEventIngest"] = "false"
        generated_json["FFlagDebugDisableTelemetryPoint"] = "false"
        generated_json["FFlagDebugDisableTelemetryV2Counter"] = "false"
        generated_json["FFlagDebugDisableTelemetryV2Event"] = "false"
        generated_json["FFlagDebugDisableTelemetryV2Stat"] = "false"

    # Reduce FPS #2
    printWarnMessage("--- Reduce FPS #2 ---")
    printMainMessage("Would you like to enable reducing FPS using pack 2 (comfort mode)? (y/n)")
    print("\033[38;5;34mThis FFlag was from the Dantez GitHub! (https://github.com/Dantezz025/Roblox-Fast-Flags)\033[0m")
    installReduceFPS2 = input("> ")
    if isYes(installReduceFPS2) == True:  
        generated_json["DFIntCSGLevelOfDetailSwitchingDistance"] = 250
        generated_json["DFIntCSGLevelOfDetailSwitchingDistanceL12"] = 500
        generated_json["DFIntCSGLevelOfDetailSwitchingDistanceL23"] = 750
        generated_json["DFIntCSGLevelOfDetailSwitchingDistanceL34"] = 1000
        generated_json["DFIntTextureQualityOverride"] = 1
        generated_json["FFlagDisablePostFx"] = "true"
    elif isRequestClose(installReduceFPS2) == True:
        printMainMessage("Ending installation..")
        return
    elif isNo(installReduceFPS2) == True:
        generated_json["DFIntCSGLevelOfDetailSwitchingDistance"] = None
        generated_json["DFIntCSGLevelOfDetailSwitchingDistanceL12"] = None
        generated_json["DFIntCSGLevelOfDetailSwitchingDistanceL23"] = None
        generated_json["DFIntCSGLevelOfDetailSwitchingDistanceL34"] = None
        generated_json["DFIntTextureQualityOverride"] = None
        generated_json["FFlagDisablePostFx"] = None

    # Reduce Ping
    printWarnMessage("--- Reduce Ping ---")
    printMainMessage("Would you like to enable reducing ping flags? (y/n)")
    print("\033[38;5;34mThis FFlag was from the Dantez GitHub! (https://github.com/Dantezz025/Roblox-Fast-Flags)\033[0m")
    installReducePing = input("> ")
    if isYes(installReducePing) == True:  
        generated_json.update({
            "DFIntConnectionMTUSize": 900,
            "FIntRakNetResendBufferArrayLength": "128",
            "FFlagOptimizeNetwork": "True",
            "FFlagOptimizeNetworkRouting": "True",
            "FFlagOptimizeNetworkTransport": "True",
            "FFlagOptimizeServerTickRate": "True",
            "DFIntServerPhysicsUpdateRate": "60",
            "DFIntServerTickRate": "60",
            "DFIntRakNetResendRttMultiple": "1",
            "DFIntRaknetBandwidthPingSendEveryXSeconds": "1",
            "DFIntOptimizePingThreshold": "50",
            "DFIntPlayerNetworkUpdateQueueSize": "20",
            "DFIntPlayerNetworkUpdateRate": "60",
            "DFIntNetworkPrediction": "120",
            "DFIntNetworkLatencyTolerance": "1",
            "DFIntMinimalNetworkPrediction": "0.1"
        })
    elif isRequestClose(installReducePing) == True:
        printMainMessage("Ending installation..")
        return
    elif isNo(installReducePing) == True:
        generated_json.update({
            "DFIntConnectionMTUSize": None,
            "FIntRakNetResendBufferArrayLength": None,
            "FFlagOptimizeNetwork": None,
            "FFlagOptimizeNetworkRouting": None,
            "FFlagOptimizeNetworkTransport": None,
            "FFlagOptimizeServerTickRate": None,
            "DFIntServerPhysicsUpdateRate": None,
            "DFIntServerTickRate": None,
            "DFIntRakNetResendRttMultiple": None,
            "DFIntRaknetBandwidthPingSendEveryXSeconds": None,
            "DFIntOptimizePingThreshold": None,
            "DFIntPlayerNetworkUpdateQueueSize": None,
            "DFIntPlayerNetworkUpdateRate": None,
            "DFIntNetworkPrediction": None,
            "DFIntNetworkLatencyTolerance": None,
            "DFIntMinimalNetworkPrediction": None
        })

    # Limit Videos Playing
    printWarnMessage("--- Limit Videos Playing ---")
    printMainMessage("Would you like to set a number of Videos that can be played in-game on the client? (y/n)")
    print("\033[38;5;215mThis FFlag was from the LatteFlags GitHub! (https://github.com/espresso-soft/latteflags)\033[0m")
    installLimitVideos = input("> ")
    if isYes(installLimitVideos) == True:
        printMainMessage("Input the number of videos you would like to limit:")
        installLimitVideosNum = input("> ")
        if installLimitVideosNum.isnumeric(): generated_json["DFIntVideoMaxNumberOfVideosPlaying"] = str(int(installLimitVideosNum))
        else:
            printYellowMessage("Disabled limit due to invalid prompt.")
            generated_json["DFIntVideoMaxNumberOfVideosPlaying"] = None
    elif isRequestClose(installLimitVideos) == True:
        printMainMessage("Ending installation..")
        return
    elif isNo(installLimitVideos) == True: generated_json["DFIntVideoMaxNumberOfVideosPlaying"] = None

    # Limit Animations Playing
    printWarnMessage("--- Limit Animations Playing ---")
    printMainMessage("Would you like to set a number of Animations that can be played in-game on the client? (y/n)")
    installLimitAnimations = input("> ")
    if isYes(installLimitAnimations) == True:
        printMainMessage("Input the number of animations you would like to limit:")
        installLimitAnimationsNum = input("> ")
        if installLimitAnimationsNum.isnumeric(): generated_json["DFIntMaxActiveAnimationTracks"] = str(int(installLimitAnimationsNum))
        else:
            printYellowMessage("Disabled limit due to invalid prompt.")
            generated_json["DFIntMaxActiveAnimationTracks"] = None
    elif isRequestClose(installLimitAnimations) == True:
        printMainMessage("Ending installation..")
        return
    elif isNo(installLimitAnimations) == True: generated_json["DFIntMaxActiveAnimationTracks"] = None

    # Disable Foundation Mode
    printWarnMessage("--- Disable Foundation Mode ---")
    printMainMessage("Would you like to disable Foundation mode on your client? (This is the new layout Roblox added) (y/n)")
    installDisableFoundationMode = input("> ")
    if isYes(installDisableFoundationMode) == True:
        generated_json["FFlagLuaAppUseUIBloxColorPalettes1"] = "true"
        generated_json["FFlagUIBloxUseNewThemeColorPalettes"] = "true"
        generated_json["FFlagLuaAppEnableFoundationColors7"] = "false"
    elif isRequestClose(installDisableFoundationMode) == True:
        printMainMessage("Ending installation..")
        return
    elif isNo(installDisableFoundationMode) == True:
        generated_json["FFlagLuaAppUseUIBloxColorPalettes1"] = "false"
        generated_json["FFlagUIBloxUseNewThemeColorPalettes"] = "false"
        generated_json["FFlagLuaAppEnableFoundationColors7"] = "true"

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
        return
    elif isNo(installCustomDisconnect) == True:
        generated_json["FFlagReconnectDisabled"] = "false"
        generated_json["FStringReconnectDisabledReason"] = None

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
            return
    elif isRequestClose(installHideUI) == True:
        printMainMessage("Ending installation..")
        return
    elif isNo(installHideUI) == True: generated_json["DFIntCanHideGuiGroupId"] = None

    # Quick Connect
    printWarnMessage("--- Quick Connect ---")
    printMainMessage("Would you like to install Quick Connect on your client? (y/n)")
    printErrorMessage("WARNING! This can be buggy and may cause issues on your Roblox experience!!!")
    installQuickConnect = input("> ")
    if isYes(installQuickConnect) == True: generated_json["FFlagEnableQuickGameLaunch"] = "true"
    elif isRequestClose(installQuickConnect) == True:
        printMainMessage("Ending installation..")
        return
    elif isNo(installQuickConnect) == True: generated_json["FFlagEnableQuickGameLaunch"] = "false"

    # Pre-Rendering
    printWarnMessage("--- Pre-Rendering ---")
    printMainMessage("Would you like to enable Pre-Rendering on the client? (y/n)")
    printYellowMessage("This may conclude a 25% Performance Boost but may cause compatibility issues in games.")
    print("\033[38;5;215mThis FFlag was from the LatteFlags GitHub! (https://github.com/espresso-soft/latteflags)\033[0m")
    installPreRendering = input("> ")
    if isYes(installPreRendering) == True: generated_json["FFlagMovePrerender"] = "true"
    elif isRequestClose(installPreRendering) == True:
        printMainMessage("Ending installation..")
        return
    elif isNo(installPreRendering) == True: generated_json["FFlagMovePrerender"] = "false"

    # Studio Flags
    if is_studio == True: 
        printMainMessage("Alright! After that, we can now start with studio specific flags!")
        # Default to Select Tool
        printWarnMessage("--- Default to Select Tool ---")
        printMainMessage("Would you like to enable defaulting to the Select tool when in a place? (y/n)")
        installSelectTool = input("> ")
        if isYes(installSelectTool) == True: generated_json["FFlagDefaultToSelectTool"] = True
        elif isRequestClose(installSelectTool) == True:
            printMainMessage("Ending installation..")
            return
        elif isNo(installSelectTool) == True: generated_json["FFlagDefaultToSelectTool"] = False
        
        # Enable Materials Generator
        printWarnMessage("--- Enable Materials Generator ---")
        printMainMessage("Would you like to enable materials generator? (y/n)")
        installMaterialsGen = input("> ")
        if isYes(installMaterialsGen) == True: generated_json["FFlagEnableMaterialGenerator"] = True
        elif isRequestClose(installMaterialsGen) == True:
            printMainMessage("Ending installation..")
            return
        elif isNo(installMaterialsGen) == True: generated_json["FFlagEnableMaterialGenerator"] = False

        # Enable Ragdoll Death Animation
        printWarnMessage("--- Enable Ragdoll Death Animation ---")
        printMainMessage("Would you like to enable the ragdoll death animation? (y/n)")
        installRagdoll = input("> ")
        if isYes(installRagdoll) == True: generated_json["DFStringDefaultAvatarDeathType"] = "Ragdoll"
        elif isRequestClose(installRagdoll) == True:
            printMainMessage("Ending installation..")
            return
        elif isNo(installRagdoll) == True: generated_json["DFStringDefaultAvatarDeathType"] = None

        # Enable Assistant Code Generation
        printWarnMessage("--- Enable Assistant Code Generation ---")
        printMainMessage("Would you like to allow the assistant to generate code? (y/n)")
        installAssistantCode = input("> ")
        if isYes(installAssistantCode) == True: generated_json["FFlagLuauCodegen"] = True
        elif isRequestClose(installAssistantCode) == True:
            printMainMessage("Ending installation..")
            return
        elif isNo(installAssistantCode) == True: generated_json["FFlagLuauCodegen"] = False
        
        # Enable Multi Select
        printWarnMessage("--- Enable Multi Select ---")
        printMainMessage("Would you like to enable multi selecting? (y/n)")
        installMultiSelect = input("> ")
        if isYes(installMultiSelect) == True: generated_json["FFlagMultiSelect"] = True
        elif isRequestClose(installMultiSelect) == True:
            printMainMessage("Ending installation..")
            return
        elif isNo(installMultiSelect) == True: generated_json["FFlagMultiSelect"] = False

        # Enable Old Explorer
        printWarnMessage("--- Enable Old Explorer ---")
        printMainMessage("Would you like to enable the Old Explorer and disable the new explorer? (y/n)")
        installOldExplorer = input("> ")
        if isYes(installOldExplorer) == True: 
            generated_json["FFlagKillOldExplorer1"] = False
            generated_json["FFlagKillOldExplorer2"] = False
            generated_json["FFlagKillOldExplorer3"] = False
            generated_json["FFlagKillOldExplorer4"] = False
            generated_json["FFlagKillOldExplorer5"] = False
            generated_json["FFlagKillOldExplorer6"] = False
            generated_json["FFlagKillOldExplorer7"] = False
            generated_json["FFlagKillOldExplorer8"] = False
            generated_json["FFlagKillOldExplorer9"] = False
            generated_json["FFlagKillOldExplorer10"] = False
            generated_json["FFlagKillOldExplorer11"] = False
        elif isRequestClose(installOldExplorer) == True:
            printMainMessage("Ending installation..")
            return
        elif isNo(installOldExplorer) == True: 
            generated_json["FFlagKillOldExplorer1"] = True
            generated_json["FFlagKillOldExplorer2"] = True
            generated_json["FFlagKillOldExplorer3"] = True
            generated_json["FFlagKillOldExplorer4"] = True
            generated_json["FFlagKillOldExplorer5"] = True
            generated_json["FFlagKillOldExplorer6"] = True
            generated_json["FFlagKillOldExplorer7"] = True
            generated_json["FFlagKillOldExplorer8"] = True
            generated_json["FFlagKillOldExplorer9"] = True
            generated_json["FFlagKillOldExplorer10"] = True
            generated_json["FFlagKillOldExplorer11"] = True

    # Custom Fast Flags
    printWarnMessage("--- Custom Fast Flags ---")
    def custom():
        def loop():
            printMainMessage("Select FFlag Mode:")
            printMainMessage("[1] = Import JSON")
            printMainMessage("[2] = Create Value Manually")
            printMainMessage("[*] = Exit FFlag Maker")
            d = input("> ")
            if d == "1":
                printMainMessage("Please input the JSON text below:")
                printErrorMessage("FLAGS MAY BREAK YOUR ROBLOX INSTALLATION. PLEASE MAKE SURE TO BE CAREFUL OF WHAT YOU PUT HERE!")
                js = input("> ")
                try:
                    js = json.loads(js)
                    if not type(js) is dict: raise Exception("Not dictionary")
                    printMainMessage("Are you sure you would like to use this FFlag JSON?")
                    for i, v in js.items(): printMainMessage(f"[{i}] = {v} ({type(v).__name__})")
                    if not (isYes(input("> ")) == True): raise Exception("Canceled save")
                    for i, v in js.items(): generated_json[i] = v
                except Exception as e: return loop()
            elif d == "2":
                printMainMessage("Enter Key Name: ")
                key = input("> ")
                if isRequestClose(key) or key == "": return {"success": False, "key": "", "value": ""}
                if orangeblox_mode == True and key.startswith("EFlag"):
                    printMainMessage("This setting cannot be changed through Roblox Fast Flags Installer. Please configure this through OrangeBlox settings instead.")
                    input("> ")
                    return loop()
                printMainMessage("Enter Key Value: ")
                value = input("> ")
                if isRequestClose(value): return {"success": False, "key": "", "value": ""}
                if value.isnumeric():
                    printMainMessage("Would you like this value to be a number value or do you want to keep it as a string? (y/n)")
                    isNum = input("> ")
                    if isYes(isNum) == True: value = int(value)
                elif value == "true" or value == "false":
                    printMainMessage("Would you like this value to be a boolean value or do you want to keep it as a string? (y/n)")
                    isBool = input("> ")
                    if isYes(isBool) == True: value = value=="true"
                return {"success": True, "key": key, "value": value}
            else: return {"success": False, "key": "", "value": ""}
        completeLoop = loop()
        if completeLoop["success"] == True:
            generated_json[completeLoop["key"]] = completeLoop["value"]
            printMainMessage("Would you like to add more fast flags? (y/n)")
            more = input("> ")
            if isYes(more) == True: custom()
    printMainMessage("Would you like to use custom fast flags? (y/n)")
    installCustom = input("> ")
    if isYes(installCustom) == True: custom()
    elif isRequestClose(installCustom) == True:
        printMainMessage("Ending installation..")
        return

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
        if isYes(select_mode) == True: printMainMessage("Selected Mode: Install/Reinstall Flags")
        elif select_mode.lower() == "j" or select_mode.lower() == "json": printMainMessage("Selected Mode: Get JSON Settings")
        elif select_mode.lower() == "nm" or select_mode.lower() == "no-merge": printMainMessage("Selected Mode: Don't Merge Settings with Previous Settings")
        elif select_mode.lower() == "f" or select_mode.lower() == "flat": printMainMessage("Selected Mode: Flat JSON Install")
        elif select_mode.lower() == "fnm" or select_mode.lower() == "flat-no-merge": printMainMessage("Selected Mode: Flat-No-Merge Install")
        elif select_mode.lower() == "r" or select_mode.lower() == "reset": printMainMessage("Selected Mode: Reset Settings")
        else:
            printMainMessage("Ending installation..")
            return
    else: select_mode = "y"

    # Installation
    if orangeblox_mode == False:
        printWarnMessage("--- Installation Ready! ---")
        printMainMessage("Settings are now finished and now ready for setup!")
        printMainMessage("Would you like to continue with the fast flag installation? (y/n)")
        printErrorMessage("WARNING! This will force-quit any open Roblox windows! Please close them now before continuing in order to prevent data loss!")
        install_now = input("> ")
        if isYes(install_now) == True:
            if isYes(select_mode) == True: handler.installFastFlags(generated_json, studio=is_studio, main=True)
            elif select_mode.lower() == "j" or select_mode.lower() == "json":
                printMainMessage("Generated JSON:")
                printMainMessage(json.dumps(generated_json))
                return
            elif select_mode.lower() == "nm" or select_mode.lower() == "no-merge": handler.installFastFlags(generated_json, merge=False, studio=is_studio, main=True)
            elif select_mode.lower() == "f" or select_mode.lower() == "flat": handler.installFastFlags(generated_json, flat=True, studio=is_studio, main=True)
            elif select_mode.lower() == "fnm" or select_mode.lower() == "flat-no-merge": handler.installFastFlags(generated_json, merge=False, flat=True, studio=is_studio, main=True)
            elif select_mode.lower() == "r" or select_mode.lower() == "reset": handler.installFastFlags({}, studio=is_studio, main=True)
            else:
                printMainMessage("Ending installation..")
                return
        else:
            printMainMessage("Ending installation..")
            return
    else:
        printWarnMessage("--- Saving Ready! ---")
        printMainMessage("Are you sure you would like to save these FFlags in the bootstrap system? (y/n)")
        install_now = input("> ")
        if isNo(install_now) == True:
            printMainMessage("Ending installation..")
            return
        else: handler.installFastFlags(generated_json, endRobloxInstances=False, studio=is_studio, main=True)
if __name__ == "__main__": main()