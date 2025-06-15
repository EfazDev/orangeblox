# 
# PipHandler
# Made by Efaz from efaz.dev
# 
# A usable set of classes with extra functions that can be used within apps.
# Import from file: from PipHandler import pip
# Import from class: 
# class request: ...
# class pip: ...
# pip_class = pip()
# 

import typing
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
    __DATA__ = typing.Union[typing.Dict, typing.List, str]
    __AUTH__ = typing.List[str]
    __HEADERS__ = typing.Dict[str, str]
    __COOKIES__ = typing.Union[typing.Dict[str, str], str]
    def get(self, url: str, headers: __HEADERS__={}, cookies: __COOKIES__={}, auth: __AUTH__=[], timeout: float=30.0, follow_redirects: bool=False) -> Response:
        import subprocess
        import json
        try:
            curl_res = subprocess.run([self.get_curl(), "-v", "-X", "GET", "--compressed"] + self.format_headers(headers) + self.format_auth(auth) + self.format_cookies(cookies) + [url], text=True, capture_output=True, timeout=timeout, encoding="utf-8")
            if type(curl_res) is subprocess.CompletedProcess:
                new_response = self.Response()
                processed_stderr = self.process_stderr(curl_res.stderr)
                for i, v in processed_stderr.items(): setattr(new_response, i, v)
                try: new_response.json = json.loads(curl_res.stdout)
                except Exception: pass
                new_response.url = url
                new_response.text = curl_res.stdout
                new_response.redirected_urls = [url]
                if self.get_if_redirect(new_response.status_code) and follow_redirects == True and new_response.headers.get("location"): 
                    req = self.get(new_response.headers.get("location"), headers=headers, cookies=cookies, auth=auth, timeout=timeout, follow_redirects=True)
                    req.redirected = True
                    req.redirected_urls = [url] + req.redirected_urls
                    return req
                return new_response
            elif type(curl_res) is subprocess.TimeoutExpired: raise self.TimedOut(url, timeout)
            elif type(curl_res) is subprocess.SubprocessError: raise self.ProcessError(url, curl_res)
            else: raise self.UnknownResponse(url, curl_res)
        except subprocess.TimeoutExpired: raise self.TimedOut(url, timeout)
        except subprocess.SubprocessError as curl_res: raise self.ProcessError(url, curl_res)
        except Exception as e: raise self.UnknownResponse(url, e)
    def post(self, url: str, data: __DATA__, headers: __HEADERS__={}, cookies: __COOKIES__={}, auth: __AUTH__=[], timeout: float=30.0, follow_redirects: bool=False) -> Response:
        import subprocess
        import json
        try:
            curl_res = subprocess.run([self.get_curl(), "-v", "-X", "POST", "--compressed"] + self.format_headers(headers) + self.format_auth(auth) + self.format_cookies(cookies) + self.format_data(data) + [url], text=True, capture_output=True, timeout=timeout, encoding="utf-8")
            if type(curl_res) is subprocess.CompletedProcess:
                new_response = self.Response()
                processed_stderr = self.process_stderr(curl_res.stderr)
                for i, v in processed_stderr.items(): setattr(new_response, i, v)
                try: new_response.json = json.loads(curl_res.stdout)
                except Exception: pass
                new_response.url = url
                new_response.text = curl_res.stdout
                new_response.redirected_urls = [url]
                if self.get_if_redirect(new_response.status_code) and follow_redirects == True and new_response.headers.get("location"): 
                    req = self.post(new_response.headers.get("location"), data, headers=headers, cookies=cookies, auth=auth, timeout=timeout, follow_redirects=True)
                    req.redirected = True
                    req.redirected_urls = [url] + req.redirected_urls
                    return req
                return new_response
            elif type(curl_res) is subprocess.TimeoutExpired: raise self.TimedOut(url, timeout)
            elif type(curl_res) is subprocess.SubprocessError: raise self.ProcessError(url, curl_res)
            else: raise self.UnknownResponse(url, curl_res)
        except subprocess.TimeoutExpired: raise self.TimedOut(url, timeout)
        except subprocess.SubprocessError as curl_res: raise self.ProcessError(url, curl_res)
        except Exception as e: raise self.UnknownResponse(url, e)
    def patch(self, url: str, data: __DATA__, headers: __HEADERS__={}, cookies: __COOKIES__={}, auth: __AUTH__=[], timeout: float=30.0, follow_redirects: bool=False) -> Response:
        import subprocess
        import json
        try:
            curl_res = subprocess.run([self.get_curl(), "-v", "-X", "PATCH", "--compressed"] + self.format_headers(headers) + self.format_auth(auth) + self.format_cookies(cookies) + self.format_data(data) + [url], text=True, capture_output=True, timeout=timeout, encoding="utf-8")
            if type(curl_res) is subprocess.CompletedProcess:
                new_response = self.Response()
                processed_stderr = self.process_stderr(curl_res.stderr)
                for i, v in processed_stderr.items(): setattr(new_response, i, v)
                try: new_response.json = json.loads(curl_res.stdout)
                except Exception: pass
                new_response.url = url
                new_response.text = curl_res.stdout
                new_response.redirected_urls = [url]
                if self.get_if_redirect(new_response.status_code) and follow_redirects == True and new_response.headers.get("location"): 
                    req = self.patch(new_response.headers.get("location"), data, headers=headers, cookies=cookies, auth=auth, timeout=timeout, follow_redirects=True)
                    req.redirected = True
                    req.redirected_urls = [url] + req.redirected_urls
                    return req
                return new_response
            elif type(curl_res) is subprocess.TimeoutExpired: raise self.TimedOut(url, timeout)
            elif type(curl_res) is subprocess.SubprocessError: raise self.ProcessError(url, curl_res)
            else: raise self.UnknownResponse(url, curl_res)
        except subprocess.TimeoutExpired: raise self.TimedOut(url, timeout)
        except subprocess.SubprocessError as curl_res: raise self.ProcessError(url, curl_res)
        except Exception as e: raise self.UnknownResponse(url, e)
    def put(self, url: str, data: __DATA__, headers: __HEADERS__={}, cookies: __COOKIES__={}, auth: __AUTH__=[], timeout: float=30.0, follow_redirects: bool=False) -> Response:
        import subprocess
        import json
        try:
            curl_res = subprocess.run([self.get_curl(), "-v", "-X", "PUT", "--compressed"] + self.format_headers(headers) + self.format_auth(auth) + self.format_cookies(cookies) + self.format_data(data) + [url], text=True, capture_output=True, timeout=timeout, encoding="utf-8")
            if type(curl_res) is subprocess.CompletedProcess:
                new_response = self.Response()
                processed_stderr = self.process_stderr(curl_res.stderr)
                for i, v in processed_stderr.items(): setattr(new_response, i, v)
                try: new_response.json = json.loads(curl_res.stdout)
                except Exception: pass
                new_response.url = url
                new_response.text = curl_res.stdout
                new_response.redirected_urls = [url]
                if self.get_if_redirect(new_response.status_code) and follow_redirects == True and new_response.headers.get("location"):
                    req = self.put(new_response.headers.get("location"), data, headers=headers, cookies=cookies, auth=auth, timeout=timeout, follow_redirects=True)
                    req.redirected = True
                    req.redirected_urls = [url] + req.redirected_urls
                    return req
                return new_response
            elif type(curl_res) is subprocess.TimeoutExpired: raise self.TimedOut(url, timeout)
            elif type(curl_res) is subprocess.SubprocessError: raise self.ProcessError(url, curl_res)
            else: raise self.UnknownResponse(url, curl_res)
        except subprocess.TimeoutExpired: raise self.TimedOut(url, timeout)
        except subprocess.SubprocessError as curl_res: raise self.ProcessError(url, curl_res)
        except Exception as e: raise self.UnknownResponse(url, e)
    def delete(self, url: str, headers: __HEADERS__={}, cookies: __COOKIES__={}, auth: __AUTH__=[], timeout: float=30.0, follow_redirects: bool=False) -> Response:
        import subprocess
        import json
        try:
            curl_res = subprocess.run([self.get_curl(), "-v", "-X", "DELETE", "--compressed"] + self.format_headers(headers) + self.format_auth(auth) + self.format_cookies(cookies) + [url], text=True, capture_output=True, timeout=timeout, encoding="utf-8")
            if type(curl_res) is subprocess.CompletedProcess:
                new_response = self.Response()
                processed_stderr = self.process_stderr(curl_res.stderr)
                for i, v in processed_stderr.items(): setattr(new_response, i, v)
                try: new_response.json = json.loads(curl_res.stdout)
                except Exception: pass
                new_response.url = url
                new_response.text = curl_res.stdout
                new_response.redirected_urls = [url]
                if self.get_if_redirect(new_response.status_code) and follow_redirects == True and new_response.headers.get("location"): 
                    req = self.delete(new_response.headers.get("location"), headers=headers, cookies=cookies, auth=auth, timeout=timeout, follow_redirects=True)
                    req.redirected = True
                    req.redirected_urls = [url] + req.redirected_urls
                    return req
                return new_response
            elif type(curl_res) is subprocess.TimeoutExpired: raise self.TimedOut(url, timeout)
            elif type(curl_res) is subprocess.SubprocessError: raise self.ProcessError(url, curl_res)
            else: raise self.UnknownResponse(url, curl_res)
        except subprocess.TimeoutExpired: raise self.TimedOut(url, timeout)
        except subprocess.SubprocessError as curl_res: raise self.ProcessError(url, curl_res)
        except Exception as e: raise self.UnknownResponse(url, e)
    def head(self, url: str, headers: __HEADERS__={}, cookies: __COOKIES__={}, auth: __AUTH__=[], timeout: float=30.0, follow_redirects: bool=False) -> Response:
        import subprocess
        import json
        try:
            curl_res = subprocess.run([self.get_curl(), "-v", "-X", "HEAD", "--compressed"] + self.format_headers(headers) + self.format_auth(auth) + self.format_cookies(cookies) + [url], text=True, capture_output=True, timeout=timeout, encoding="utf-8")
            if type(curl_res) is subprocess.CompletedProcess:
                new_response = self.Response()
                processed_stderr = self.process_stderr(curl_res.stderr)
                for i, v in processed_stderr.items(): setattr(new_response, i, v)
                try: new_response.json = json.loads(curl_res.stdout)
                except Exception: pass
                new_response.url = url
                new_response.text = curl_res.stdout
                new_response.redirected_urls = [url]
                if self.get_if_redirect(new_response.status_code) and follow_redirects == True and new_response.headers.get("location"): 
                    req = self.head(new_response.headers.get("location"), headers=headers, cookies=cookies, auth=auth, timeout=timeout, follow_redirects=True)
                    req.redirected = True
                    req.redirected_urls = [url] + req.redirected_urls
                    return req
                return new_response
            elif type(curl_res) is subprocess.TimeoutExpired: raise self.TimedOut(url, timeout)
            elif type(curl_res) is subprocess.SubprocessError: raise self.ProcessError(url, curl_res)
            else: raise self.UnknownResponse(url, curl_res)
        except subprocess.TimeoutExpired: raise self.TimedOut(url, timeout)
        except subprocess.SubprocessError as curl_res: raise self.ProcessError(url, curl_res)
        except Exception as e: raise self.UnknownResponse(url, e)
    def custom(self, url: str, method: str, data: __DATA__, headers: __HEADERS__={}, cookies: __COOKIES__={}, auth: __AUTH__=[], timeout: float=30.0, follow_redirects: bool=False) -> Response:
        import subprocess
        import json
        try:
            curl_res = subprocess.run([self.get_curl(), "-v", "-X", method, "--compressed"] + self.format_headers(headers) + self.format_auth(auth) + self.format_cookies(cookies) + self.format_data(data) + [url], text=True, capture_output=True, timeout=timeout, encoding="utf-8")
            if type(curl_res) is subprocess.CompletedProcess:
                new_response = self.Response()
                processed_stderr = self.process_stderr(curl_res.stderr)
                for i, v in processed_stderr.items(): setattr(new_response, i, v)
                try: new_response.json = json.loads(curl_res.stdout)
                except Exception: pass
                new_response.url = url
                new_response.text = curl_res.stdout
                new_response.redirected_urls = [url]
                if self.get_if_redirect(new_response.status_code) and follow_redirects == True and new_response.headers.get("location"): 
                    req = self.custom(new_response.headers.get("location"), method, data, headers=headers, cookies=cookies, auth=auth, timeout=timeout, follow_redirects=True)
                    req.redirected = True
                    req.redirected_urls = [url] + req.redirected_urls
                    return req
                return new_response
            elif type(curl_res) is subprocess.TimeoutExpired: raise self.TimedOut(url, timeout)
            elif type(curl_res) is subprocess.SubprocessError: raise self.ProcessError(url, curl_res)
            else: raise self.UnknownResponse(url, curl_res)
        except subprocess.TimeoutExpired: raise self.TimedOut(url, timeout)
        except subprocess.SubprocessError as curl_res: raise self.ProcessError(url, curl_res)
        except Exception as e: raise self.UnknownResponse(url, e)
    def open(self, *k, **s) -> OpenContext:
        mai = self.get(*k, **s)
        return self.OpenContext(mai)
    def download(self, path: str, output: str, check: bool=False, delete_existing: bool=True) -> FileDownload:
        import subprocess
        import os
        import shutil
        if os.path.exists(output) and delete_existing == False: raise FileExistsError(f"This file already exists in {output}!")
        elif os.path.exists(output) and os.path.isdir(output): shutil.rmtree(output, ignore_errors=True)
        elif os.path.exists(output) and os.path.isfile(output): os.remove(output)
        download_proc = subprocess.run([self.get_curl(), "-v", "-L", "-o", output, path], shell=False, capture_output=True, text=True)
        if download_proc.returncode == 0: 
            s = self.FileDownload()
            s.returncode = 0
            s.path = output
            s.url = path
            processed_stderr = self.process_stderr(download_proc.stderr)
            for i, v in processed_stderr.items(): setattr(s, i, v)
            return s
        else: 
            if check == True: raise Exception(f"Unable to download file at {path} with return code {download_proc.returncode}!")
            else: 
                s = self.FileDownload()
                s.returncode = download_proc.returncode
                s.path = None
                processed_stderr = self.process_stderr(download_proc.stderr)
                for i, v in processed_stderr.items(): setattr(s, i, v)
                return s
    def get_curl(self):
        import urllib.request
        import platform
        import shutil
        import os
        pos_which = shutil.which("curl")
        if os.path.exists(pos_which): return pos_which
        elif platform.system() == "Windows" and os.path.exists(os.path.join(current_path_location, "curl")): return os.path.join(current_path_location, "curl", "curl.exe")
        elif os.path.exists(os.path.join(current_path_location, "curl")): return os.path.join(current_path_location, "curl", "curl")
        else: 
            current_path_location = os.path.dirname(os.path.abspath(__file__))
            if platform.system() == "Darwin": return None
            elif platform.system() == "Windows":
                pip_class = pip()
                if platform.architecture()[0] == "32bit": urllib.request.urlretrieve("https://curl.se/windows/latest.cgi?p=win32-mingw.zip", os.path.join(current_path_location, "curl_download.zip"))
                else: urllib.request.urlretrieve("https://curl.se/windows/latest.cgi?p=win64-mingw.zip", os.path.join(current_path_location, "curl_download.zip"))
                if os.path.exists(os.path.join(current_path_location, "curl_download.zip")):
                    unzip_res = pip_class.unzipFile(os.path.join(current_path_location, "curl_download.zip"), os.path.join(current_path_location, "curl"), ["curl.exe"])
                    if unzip_res.returncode == 0: return os.path.join(current_path_location, "curl", "curl.exe")
                    else: return None 
                else: return None 
            else: return None
    def get_if_ok(self, code: int): return int(code) < 300 and int(code) >= 200
    def get_if_redirect(self, code: int): return int(code) < 400 and int(code) >= 300
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
        import json
        is_json = False
        if type(data) is dict or type(data) is list: data = json.dumps(data); is_json = True
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
    def process_stderr(self, stderr: str):
        import platform
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
            "path": "",
            "method": "",
            "scheme": "",
            "ok": False
        }
        for i in lines:
            if platform.system() == "Darwin": # OpenSSL based cUrl
                if f"< HTTP/{data['http_version']} " in i:
                    sl = i.split(f"< HTTP/{data['http_version']} ")
                    if len(sl) > 1: 
                        sl.pop(0)
                        data["status_code"] = int(sl[0])
                        if self.get_if_ok(data["status_code"]): data["success"] = True; data["ok"] = True
                elif "< " in i:
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
                elif "[HTTP/" in i:
                    sl = i.split("[HTTP/")
                    if len(sl) > 1: sl.pop(0); data["http_version"] = sl[0].split("]")[0]
                    if ":scheme:" in i:
                        sl = i.split("[:scheme: ")
                        if len(sl) > 1: sl.pop(0); data["scheme"] = sl[0].split("]")[0]
                    elif ":method:" in i:
                        sl = i.split("[:method: ")
                        if len(sl) > 1: sl.pop(0); data["method"] = sl[0].split("]")[0]
                    elif ":path:" in i:
                        sl = i.split("[:path: ")
                        if len(sl) > 1: sl.pop(0); data["path"] = sl[0].split("]")[0]
            else: # Schannel based cUrl
                if f"< HTTP/{data['http_version']} " in i:
                    sl = i.split(f"< HTTP/{data['http_version']} ")
                    if len(sl) > 1: 
                        sl.pop(0)
                        data["status_code"] = int(sl[0].split(" ")[0])
                        if self.get_if_ok(data["status_code"]): data["ok"] = True
                elif "< " in i:
                    sl = i.replace("< ", "", 1).split(": ")
                    if len(sl) > 1: data["headers"][sl[0]] = sl[1]
                elif "schannel: SSL/TLS connection renegotiated" in i:
                    data["ssl_verified"] = True
                    data["ssl_issuer"] = "Schannel Placeholder Certificate"
                    data["ssl_subject"] = data["host"]
                    data["tls_version"] = "1.2"
                elif i.startswith("> ") and "HTTP/" in i:
                    sl = i.replace("> ", "").split(" ")
                    if len(sl) > 2: 
                        data["method"] = sl[0]
                        data["path"] = sl[1]
                        data["http_version"] = sl[2].split("HTTP/")[1]
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
                    if len(sl) > 1: 
                        sl.pop(0); data["port"] = int(sl[0])
                        if data["port"] == 443: data["scheme"] = "https"
                        elif data["port"] == 80 or data["port"] == 8080: data["scheme"] = "http"
                    sl = i.split("Connected to ")
                    if len(sl) > 1: sl.pop(0); data["host"] = sl[0].split(" ")[0]
                    sl = i.split("(")
                    if len(sl) > 1: sl.pop(0); data["attempted_ip"] = sl[0].split(")")[0]
        return data
class pip:
    executable = None
    debug = False
    ignore_same = False
    requests: request = None
    
    # Pip Functionalities
    def __init__(self, command: list=[], executable: str=None, debug: bool=False, find: bool=False, opposite: bool=False):
        import sys
        import os
        import subprocess
        self.debug = debug==True
        self.requests = request()
        if opposite == True: self.executable = self.findPython(opposite_arch=opposite)
        else:
            if type(executable) is str:
                if os.path.isfile(executable): self.executable = executable
                else: self.executable = self.findPython(opposite_arch=opposite) if find == True else sys.executable
            else: self.executable = self.findPython(opposite_arch=opposite) if find == True else sys.executable
        if type(command) is list and len(command) > 0: self.ensure(); subprocess.check_call([self.executable, "-m", "pip"] + command)
    def install(self, packages: typing.List[str], upgrade: bool=False):
        self.ensure()
        import subprocess
        res = {}
        generated_list = []
        for i in packages:
            if type(i) is str:  generated_list.append(i)
        if len(generated_list) > 0:
            try:
                a = subprocess.call([self.executable, "-m", "pip", "install"] + (["--upgrade"] if upgrade == True else []) + generated_list, stdout=(not self.debug) and subprocess.DEVNULL or None, stderr=(not self.debug) and subprocess.DEVNULL or None)
                if a == 0: return {"success": True, "message": "Successfully installed modules!"}
                else: return {"success": False, "message": f"Command has failed!"}
            except Exception as e: return {"success": False, "message": str(e)}
        return res
    def uninstall(self, packages: typing.List[str]):
        self.ensure()
        import subprocess
        res = {}
        generated_list = []
        for i in packages:
            if type(i) is str: generated_list.append(i)
        if len(generated_list) > 0:
            try:
                subprocess.call([self.executable, "-m", "pip", "uninstall", "-y"] + generated_list, stdout=self.debug == False and subprocess.DEVNULL or None, stderr=self.debug == False and subprocess.DEVNULL or None)
                res[i] = {"success": True}
            except Exception as e: res[i] = {"success": False}
        return res
    def installed(self, packages: typing.List[str]=[], boolonly: bool=False):
        self.ensure()
        import subprocess
        import importlib.metadata
        if self.isSameRunningPythonExecutable() and not len(packages) == 0:
            def che(a):
                try: importlib.metadata.version(a); return True
                except importlib.metadata.PackageNotFoundError: return False
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
            sub = subprocess.run([self.executable, "-m", "pip", "list"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            line_splits = sub.stdout.decode().splitlines()[2:]
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
        import subprocess
        import os
        import shutil
        import urllib.parse

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
                        self.requests.download(f"https://github.com/{url_path_2}/{url_path_1}/archive/refs/heads/main.zip", os.path.join(down_path, f"{url_path_1}.zip"))
                        downed_paths.append(os.path.join(down_path, f"{url_path_1}.zip"))
                        co += 1
                    return {"success": True, "path": down_path, "package_files": downed_paths}
                else:
                    down_path = os.path.join(current_path_location, '-'.join(generated_list) + "_download")
                    if os.path.isdir(down_path): shutil.rmtree(down_path, ignore_errors=True)
                    os.makedirs(down_path)
                    self.ensure()
                    subprocess.check_call([self.executable, "-m", "pip", "download", "--no-binary", ":all:"] + generated_list, stdout=self.debug == False and subprocess.DEVNULL, stderr=self.debug == False and subprocess.DEVNULL, cwd=down_path)
                    a = []
                    for e in os.listdir(down_path): a.append(os.path.join(down_path, e))
                    return {"success": True, "path": down_path, "package_files": a}
            except Exception as e:
                print(e)
                return {"success": False}
        return {"success": False}
    def update(self):
        self.ensure()
        import subprocess
        try:
            a = subprocess.call([self.executable, "-m", "pip", "install", "--upgrade", "pip"], stdout=(not self.debug) and subprocess.DEVNULL or None, stderr=(not self.debug) and subprocess.DEVNULL or None)
            if a == 0: return {"success": True, "message": "Successfully installed latest version of pip!"}
            else: return {"success": False, "message": f"Command has failed!"}
        except Exception as e: return {"success": False, "message": str(e)}
    def ensure(self):
        import subprocess
        import tempfile
        import ssl
        if not self.executable: return False
        ssl._create_default_https_context = ssl._create_stdlib_context
        check_for_pip_pro = subprocess.run([self.executable, "-m", "pip"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if check_for_pip_pro.returncode == 0: return True
        else:
            if self.getIfConnectedToInternet() == True:
                if self.debug == True: print(f"Downloading pip from pypi..")
                with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_file: pypi_download_path = temp_file.name
                if self.pythonSupported(3,9,0): download_res = self.requests.download("https://bootstrap.pypa.io/get-pip.py", pypi_download_path)      
                else: current_python_version = self.getCurrentPythonVersion(); download_res = self.requests.download(f"https://bootstrap.pypa.io/pip/{current_python_version.split('.')[0]}.{current_python_version.split('.')[1]}/get-pip.py", pypi_download_path)
                if download_res.returncode == 0:
                    if self.debug == True: print(f"Successfully downloaded pip! Installing to Python..")
                    install_to_py = subprocess.run([self.executable, pypi_download_path], stdout=self.debug == False and subprocess.DEVNULL, stderr=self.debug == False and subprocess.DEVNULL)
                    if install_to_py.returncode == 0:
                        if self.debug == True: print(f"Successfully installed pip to Python executable!")
                        return True
                    else: return False
                else: return False
            else:
                if self.debug == True: print(f"Unable to download pip due to no internet access.")
                return False
    
    # Pypi Packages
    def getGitHubRepository(self, packages: typing.List[str]):
        generated_list = []
        for i in packages:
            if type(i) is str: generated_list.append(i)
        if len(generated_list) > 0:
            try:
                links = {}
                for i in generated_list:
                    urll = f"https://pypi.org/pypi/{i}/json"
                    if self.getIfConnectedToInternet() == False: return {"success": False}
                    response = self.requests.get(urll)
                    if response.ok:
                        data = response.json
                        info = data["info"]
                        url = info.get("project_urls", {}).get("Source") or info.get("home_page")
                        if url: links[i] = url
                return {"success": True, "repositories": links}
            except Exception as e:
                return {"success": False}
        return {"success": False}
    
    # Python Management
    def getLatestPythonVersion(self, beta: bool=False):
        import re
        url = "https://www.python.org/downloads/"
        if beta == True: url = "https://www.python.org/download/pre-releases/"
        response = self.requests.get(url)
        if response.ok: html = response.text
        else: html = ""
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
        else: return False
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
    def osSupported(self, windows_build: int=0, macos_version: tuple=(0,0,0)):
        import platform
        if platform.system() == "Windows":
            version = platform.version()
            v = version.split(".")
            if len(v) < 3: return False
            return int(v[2]) >= windows_build
        elif platform.system() == "Darwin":
            version = platform.mac_ver()[0]
            version_tuple = tuple(map(int, version.split('.')))
            while len(version_tuple) < 3: version_tuple += (0,)
            while len(macos_version) < 3: min_version += (0,)
            return version_tuple >= macos_version
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
        if self.getIfConnectedToInternet() == False:
            if self.debug == True: print("Failed to download Python installer.")
            return
        if version == "": version = self.getLatestPythonVersion(beta=beta)
        if not version:
            if self.debug == True: print("Failed to download Python installer.")
            return
        version_url_folder = version
        if beta == True: version_url_folder = re.match(r'^\d+\.\d+\.\d+', version).group()
        if ma_os == "Darwin":
            url = f"https://www.python.org/ftp/python/{version_url_folder}/python-{version}-macos11.pkg"
            with tempfile.NamedTemporaryFile(suffix=".pkg", delete=False) as temp_file: pkg_file_path = temp_file.name
            result = self.requests.download(url, pkg_file_path)            
            if result.returncode == 0:
                subprocess.run(["open", pkg_file_path], stdout=self.debug == False and subprocess.DEVNULL, stderr=self.debug == False and subprocess.DEVNULL, check=True)
                while self.getIfProcessIsOpened("Installer.app") == True: time.sleep(0.1)
                if self.debug == True: print(f"Python installer has been executed: {pkg_file_path}")
            else:
                if self.debug == True: print("Failed to download Python installer.")
        elif ma_os == "Windows":
            if ma_arch[0] == "64bit":
                if ma_processor.lower() == "arm64": url = f"https://www.python.org/ftp/python/{version_url_folder}/python-{version}-arm64.exe"
                else: url = f"https://www.python.org/ftp/python/{version_url_folder}/python-{version}-amd64.exe"
            else: url = f"https://www.python.org/ftp/python/{version_url_folder}/python-{version}.exe"
            with tempfile.NamedTemporaryFile(suffix=".exe", delete=False) as temp_file: exe_file_path = temp_file.name
            result = self.requests.download(url, exe_file_path)
            if result.returncode == 0:
                subprocess.run([exe_file_path], stdout=self.debug == False and subprocess.DEVNULL, stderr=self.debug == False and subprocess.DEVNULL, check=True)
                if self.debug == True: print(f"Python installer has been executed: {exe_file_path}")
            else:
                if self.debug == True: print("Failed to download Python installer.")
    def installLocalPythonCertificates(self):
        import subprocess
        import platform
        import ssl
        import os
        if platform.system() == "Darwin":
            ssl._create_default_https_context = ssl._create_stdlib_context
            with open("./install_local_python_certs.py", "w") as f: f.write("""import os; import os.path; import ssl; import stat; import subprocess; import sys; STAT_0o775 = ( stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP | stat.S_IROTH |  stat.S_IXOTH ); openssl_dir, openssl_cafile = os.path.split(ssl.get_default_verify_paths().openssl_cafile); print(" -- pip install --upgrade certifi"); subprocess.check_call([sys.executable, "-E", "-s", "-m", "pip", "install", "--upgrade", "certifi"]); import certifi; os.chdir(openssl_dir); relpath_to_certifi_cafile = os.path.relpath(certifi.where()); print(" -- removing any existing file or link"); os.remove(openssl_cafile); print(" -- creating symlink to certifi certificate bundle"); os.symlink(relpath_to_certifi_cafile, openssl_cafile); print(" -- setting permissions"); os.chmod(openssl_cafile, STAT_0o775); print(" -- update complete");""")
            s = subprocess.run(f'"{self.executable}" ./install_local_python_certs.py', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            os.remove("./install_local_python_certs.py")
            if not (s.returncode == 0) and self.debug == True: print(f"Unable to install local python certificates!")
    def findPython(self, opposite_arch=False, latest=True):
        import os
        import glob
        import platform
        ma_os = platform.system()
        ma_arch = platform.machine()
        if ma_os == "Darwin":
            target_name = "python3"
            if opposite_arch == True and ma_arch == "arm64": target_name = "python3-intel64"
            if os.path.exists(f"/usr/local/bin/{target_name}") and os.path.islink(f"/usr/local/bin/{target_name}"): return f"/usr/local/bin/{target_name}"
            else:
                paths = [
                    "/usr/local/bin/python*",
                    "/opt/homebrew/bin/python*",
                    "/Library/Frameworks/Python.framework/Versions/*/bin/python*",
                    os.path.expanduser("~/Library/Python/*/bin/python*"),
                    os.path.expanduser("~/.pyenv/versions/*/bin/python*"),
                    os.path.expanduser("~/opt/anaconda*/bin/python*")
                ]
                found_paths = []
                for path_pattern in paths: found_paths.extend(glob.glob(path_pattern))
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
            for path_pattern in paths: found_paths.extend(glob.glob(path_pattern))
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
                "/opt/homebrew/bin/python*",
                "/Library/Frameworks/Python.framework/Versions/*/bin/python*",
                os.path.expanduser("~/Library/Python/*/bin/python*"),
                os.path.expanduser("~/.pyenv/versions/*/bin/python*"),
                os.path.expanduser("~/opt/anaconda*/bin/python*")
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
    def isSameRunningPythonExecutable(self):
        import os
        import sys
        if self.ignore_same == True: return False
        if os.path.exists(self.executable) and os.path.exists(sys.executable): return os.path.samefile(self.executable, sys.executable)
        else: return False
    def isOppositeArchitecture(self):
        import platform
        import os
        ma_os = platform.system()
        ma_arch = platform.machine()
        if not self.executable: return False
        if ma_os == "Windows" and os.path.dirname(self.executable).endswith("-32"): return True
        elif ma_os == "Darwin" and ma_arch.lower() == "arm64" and self.executable.endswith("-intel64"): return True
        return False
    
    # Python Functions
    def getLocalAppData(self):
        import platform
        import os
        ma_os = platform.system()
        if ma_os == "Windows": return os.path.expandvars(r'%LOCALAPPDATA%')
        elif ma_os == "Darwin": return f'{os.path.expanduser("~")}/Library/'
        else: return f'{os.path.expanduser("~")}/'
    def getUserFolder(self):
        import os
        return os.path.expanduser("~")
    def getIfLoggedInIsMacOSAdmin(self):
        import subprocess
        import platform
        import os
        ma_os = platform.system()
        if ma_os == "Darwin":
            logged_in_folder = self.getUserFolder()
            username = os.path.basename(logged_in_folder)
            groups_res = subprocess.run(["/usr/bin/groups", username], text=True, encoding="utf-8", capture_output=True)
            if groups_res.returncode == 0: return "admin" in groups_res.stdout.split(" ")
            else: return False
        else: return False
    def getInstallableApplicationsFolder(self):
        import platform
        import os
        ma_os = platform.system()
        if ma_os == "Darwin":
            if self.getIfLoggedInIsMacOSAdmin(): return os.path.join("/", "Applications")
            else: return os.path.join(self.getUserFolder(), "Applications")
        elif ma_os == "Windows":
            return self.getLocalAppData()
    def restartScript(self, scriptname: str, argv: list):
        import sys
        import subprocess
        import os
        argv.pop(0)
        res = subprocess.run([self.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), scriptname)] + argv)
        sys.exit(res.returncode)
    def endProcess(self, name="", pid=""):
        import subprocess
        import platform
        main_os = platform.system()
        if pid == "":
            if main_os == "Darwin": subprocess.run(["/usr/bin/killall", "-9", name], stdout=subprocess.DEVNULL)
            elif main_os == "Windows": subprocess.run(f"taskkill /IM {name} /F", shell=True, stdout=subprocess.DEVNULL)
            else: subprocess.run(f"killall -9 {name}", shell=True, stdout=subprocess.DEVNULL)
        else:
            if main_os == "Darwin": subprocess.run(f"kill -9 {pid}", shell=True, stdout=subprocess.DEVNULL)
            elif main_os == "Windows": subprocess.run(f"taskkill /PID {pid} /F", shell=True, stdout=subprocess.DEVNULL)
            else: subprocess.run(f"kill -9 {pid}", shell=True, stdout=subprocess.DEVNULL)
    def importModule(self, module_name: str, install_module_if_not_found: bool=False):
        import importlib
        try: return importlib.import_module(module_name)
        except ModuleNotFoundError:
            try:
                if install_module_if_not_found == True and self.isSameRunningPythonExecutable(): self.install([module_name])
                return importlib.import_module(module_name)
            except Exception as e: raise ImportError(f'Unable to find module "{module_name}" in Python {self.getCurrentPythonVersion()} environment.')
    def unzipFile(self, path: str, output: str, look_for: list=[], export_out: list=[], either: bool=False, check: bool=True):
        import subprocess
        import platform
        import os
        import shutil
        import hashlib
        class result():
            returncode = 0
            path = ""
        if not os.path.exists(output): os.makedirs(output)
        previous_output = output
        if len(look_for) > 0: output = output + f"_Full_{str(hashlib.sha256(os.urandom(6)).hexdigest()[:6])}"; os.makedirs(output)
        if platform.system() == "Windows": zip_extract = subprocess.run(["C:\\Windows\\System32\\tar.exe", "-xf", path] + export_out + ["-C", output], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check)
        else: zip_extract = subprocess.run(["/usr/bin/ditto", "-xk", path, output], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check)
        if len(look_for) > 0:
            if zip_extract.returncode == 0:
                for ro, dir, fi in os.walk(output):
                    if either == True:
                        found_all = False
                        for a in look_for:
                            if a in (fi + dir): found_all = True
                    else:
                        found_all = True
                        for a in look_for:
                            if not a in (fi + dir): found_all = False
                    if found_all == True: 
                        self.copyTreeWithMetadata(ro, previous_output, symlinks=True, dirs_exist_ok=True, ignore_if_not_exist=True)
                        shutil.rmtree(output, ignore_errors=True)
                        s = result()
                        s.path = previous_output
                        s.returncode = 0
                        return s
            if os.path.exists(output): shutil.rmtree(output, ignore_errors=True)
            if os.path.exists(previous_output): shutil.rmtree(previous_output, ignore_errors=True)
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
            process_list = subprocess.run(["tasklist"], capture_output=True, text=True).stdout
            if pid == "" or pid == None: return process_name in process_list
            else: return f"{pid} Console" in process_list or f"{pid} Service" in process_list
        else:
            if pid == "" or pid == None: return subprocess.run(f"pgrep -f '{process_name}' > /dev/null 2>&1", shell=True).returncode == 0
            else: return subprocess.run(f"ps -p {pid} > /dev/null 2>&1", shell=True).returncode == 0
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
        except Exception as e: return False
    def getIf32BitWindows(self): 
        import subprocess
        if not self.executable: return False
        if self.isSameRunningPythonExecutable():
            import platform
            return platform.system() == "Windows" and platform.architecture()[0] == "32bit"
        else:
            a = subprocess.run([self.executable, "-c", 'import platform; print(platform.system() == "Windows" and platform.architecture()[0] == "32bit")'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            final = a.stdout.decode()
            return final.replace("\n", "") == "True"
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
                        if window_pid == int(pid): system_windows.append(hwnd)
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
                    if win and win.get("kCGWindowOwnerPID"): new_set_of_system_windows.append(win)
                return new_set_of_system_windows
            else: return []
        else: return []
class plist:
    def readPListFile(self, path: str):
        import os
        if os.path.exists(path):
            import plistlib
            with open(path, "rb") as f: plist_data = plistlib.load(f)
            return plist_data
        else: return {}
    def writePListFile(self, path: str, data: typing.Union[dict, str, int, float], binary: bool=False, ns_mode: bool=False):
        try:
            import plistlib
            import subprocess
            import platform
            import os
            if ns_mode == True and platform.system() == "Darwin":
                domain = os.path.basename(path).replace(".plist", "", 1)
                for i, v in data.items(): subprocess.run(["defaults", "write", domain, i, str(v)], check=True)
            with open(path, "wb") as f:
                if binary == True: plistlib.dump(data, f, fmt=plistlib.FMT_BINARY)
                else: plistlib.dump(data, f)
            return {"success": True, "message": "Success!", "data": data}
        except Exception as e: return {"success": False, "message": "Something went wrong.", "data": e}
class stdout:
    buffer: str = ""
    logger = None
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
            with open(os.path.join(current_path_location, f"translations_{self.lang}.json")) as f: self.translation_json = json.load(f)
    def write(self, message: str): 
        import sys
        if self.locked_new == True and not message.startswith("\033{progressend}"): self.awaiting_bar_logs.append(message); return
        if message.startswith("\033{progress}"):
            message = message.replace("\033{progress}", "", 1)
            sys.__stdout__.write("\n")
            sys.__stdout__.flush()
            self.locked_new = True
            return
        elif message.startswith("\033{progressend}"):
            self.locked_new = False
            for i in self.awaiting_bar_logs: self.write(i)
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
                try: self.logger.log(self.log_level, line.rstrip())
                except Exception: self.logger.log(self.log_level, line.rstrip().encode(self.encoding, errors="replace").decode(self.encoding))
    def clear(self):
        import os
        os.system("cls" if os.name == "nt" else 'echo "\033c\033[3J"; clear')
        self.line_count = 0
    def change_last_message(self, message: str):
        import sys
        sys.__stdout__.write("\033[1A")
        sys.__stdout__.write("\033[2K")
        sys.__stdout__.write(message + "\n")
        sys.__stdout__.flush()
    def flush(self):
        if self.buffer.rstrip():
            try:  self.logger.log(self.log_level, self.buffer.rstrip()); 
            except Exception: self.logger.log(self.log_level, self.buffer.rstrip().encode(self.encoding, errors="replace").decode(self.encoding))
        self.buffer = ''
class ProgressBar:   
    current_percentage = 0
    status_text = ""
    def submit(self, status_text: str, percentage: int):
        import sys
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
class TimerBar:   
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
        import sys
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
    def __init__(self, data): self.data = data
    def json(self): return self.data
class BuiltinEditor:
    def __init__(self, builtins_mod):
        import os
        import sys
        import platform
        if platform.system() == "Windows": return
        def holding_open(path, mode="r", *args, **kwargs):
            if "r" in mode and "+" not in mode and "w" not in mode and "a" not in mode:
                try: fd = os.open(path, os.O_RDONLY | os.O_NOATIME); return os.fdopen(fd, mode, *args, **kwargs)
                except (AttributeError, PermissionError, OSError): pass
            return _original_open(path, mode, *args, **kwargs)
        def holding_input(*args, **kwargs):
            try: return _original_input(*args, **kwargs)
            except KeyboardInterrupt: return sys.exit()
            except Exception as e: raise e
        _original_open = builtins_mod.open
        _original_input = builtins_mod.input
        builtins_mod.open = holding_open
        builtins_mod.input = holding_input
if __name__ == "__main__": print("PipHandler.py is a module and is not a runable instance!")