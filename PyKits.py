# 
# PyKits v1.5.0
# Made by Efaz from efaz.dev
# 
# A usable set of classes with extra functions that can be used within apps.
# Import from file: import PipKits
# Import from class: 
#
# import typing
# class requests: ...
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
    def github(self, packages: typing.List[str]):
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
class Translator:
    def __init__(self, lang="en"):
        self.language = lang
        self.translation_json = {}
        self.patterns = {}
        self.extractors = {}
        self.module_imports = {}
        import os
        import json
        import re
        from collections import defaultdict
        self._os = os
        self._json = json
        self._re = re
        self._defaultdict = defaultdict
        if lang: self.load_new_language(lang)
    def load_new_language(self, lang="en", include_ansi=False):
        self.language = lang
        if lang and not (lang == "en"):
            cur_path = self._os.path.dirname(self._os.path.abspath(__file__))
            if self._os.path.exists(lang): path = lang
            else: path = self._os.path.join(cur_path, "Translations", f"{lang}.json")
            with open(path, "r", encoding="utf-8") as f: self.translation_json = self._json.load(f)
            self.translation_json.update({
                "- (*)": "- (*)",
                "[(*)] = (*)": "[(*)] = (*)",
                "[(*)] = (*) ((*))": "[(*)] = (*) ((*))",
                "[(*)] [(*)] = (*)": "[(*)] [(*)] = (*)",
                "[*] = (*)": "[*] = (*)",
                "v(*)": "v(*)",
                "(*) | (*) => (*)": "(*) | (*) => (*)",
                "> ": "> ",
                "\u001b[38;5;(*)m(*)\u001b[0m": "\u001b[38;5;(*)m(*)\u001b[0m",
                "\u001b[38;5;(*)m(*)\u001b[0m\n": "\u001b[38;5;(*)m(*)\u001b[0m\n",
                "\u001b[38;5;(*)m(*)\u001b[0m\r\n": "\u001b[38;5;(*)m(*)\u001b[0m\r\n"
            })
            self.generate_patterns(include_ansi=include_ansi)
    def generate_patterns(self, include_ansi=False):
        adding_ansi_translations = {}
        self.indexed_patterns = self._defaultdict(list)
        self.fallback_patterns = []
        for i in self.translation_json:
            regex = self.generate_regex(i)
            self.patterns[i] = regex
            parts = i.split("(*)")
            if parts[0]:
                prefix = parts[0][:(len(parts[0]) // 2)]
                self.indexed_patterns[prefix].append((i, regex))
            else: self.fallback_patterns.append((i, regex))
        if include_ansi:
            ansi_template = f"\033[38;5;(*)m(*)\033[0m\n"
            ansi_regex = self.generate_regex(ansi_template)
            self.patterns[ansi_template] = ansi_regex
            self.fallback_patterns.append((ansi_template, ansi_regex))
            adding_ansi_translations[ansi_template] = ansi_template
        self.translation_json.update(adding_ansi_translations)
        self.one_group_patterns = [regex for tpl, regex in self.patterns.items() if regex.groups == 1]
    def generate_regex(self, template: str, tolerant: bool=False):
        parts = template.split("(*)")
        escaped_parts = []
        for part in parts:
            if tolerant: part = self._re.sub(r'\.{2,}', r'\\.+', self._re.escape(part)); part = self._re.sub(r'!{2,}', r'!+', part)
            else: part = self._re.escape(part)
            escaped_parts.append(part)
        pattern = "".join(part + (r"(.+?)" if i < len(parts) - 1 else "") for i, part in enumerate(escaped_parts))
        return self._re.compile(f"^{pattern}$")
    def extract_placeholders(self, template: str, actual: str):
        if template not in self.extractors:
            parts = template.split("(*)")
            pattern = "".join(self._re.escape(part) + (r"(.+?)" if i < len(parts) - 1 else "") for i, part in enumerate(parts))
            self.extractors[template] = self._re.compile(f"^{pattern}$")
        match = self.extractors[template].match(actual)
        if match: return list(match.groups())
        return None
    def pre_translate(self, message: str, translate_id: str):
        try:
            tr_me = self.translation_json.get(translate_id)
            tr_placeholders = self.extract_placeholders(translate_id, message)
            sp = tr_me.split("(*)")
            result = []
            for i in range(len(sp)):
                result.append(sp[i])
                if i < len(tr_placeholders):
                    placeholder = tr_placeholders[i]
                    if any(regex.fullmatch(placeholder) for regex in self.one_group_patterns): result.append(self.translation_json.get(tr_placeholders[i], tr_placeholders[i]))
                    else: result.append(placeholder)
            return "".join(result)
        except Exception: return message
    def translate(self, message: str): 
        if not (self.language == "en"):
            if message in self.translation_json: return self.translation_json[message]
            possible_uses = self.indexed_patterns.get(message[:(len(message) // 2)], []) + self.fallback_patterns
            tried_templates = set()
            for i, v in possible_uses:
                tried_templates.add(i)
                if v.fullmatch(message) and self.translation_json.get(i): return self.pre_translate(message, i)
            for i, v in self.patterns.items():
                if i in tried_templates: continue
                if v.fullmatch(message) and self.translation_json.get(i): return self.pre_translate(message, i)
        return message
class Colors:
    class Color:
        def __init__(self, r: int, g: int, b: int):
            self.__colors_obj__ = Colors()
            r, g, b = self.__colors_obj__.limit_rgb_value(r), self.__colors_obj__.limit_rgb_value(g), self.__colors_obj__.limit_rgb_value(b)
            self.rgb = (r, g, b)
            self.hex = self.__colors_obj__.rgb_to_hex(r, g, b)
            self.ansi = self.__colors_obj__.hex_to_ansi2(self.hex)
        def wrap_message(self, message): return self.__colors_obj__.wrap_message(message, self.ansi)
        def grayscale(self): return self.__colors_obj__.apply_grayscale(*(self.rgb))
    class Black(Color):
        def __init__(self): super().__init__(0, 0, 0)
    class Red(Color):
        def __init__(self): super().__init__(255, 0, 0)
    class Yellow(Color):
        def __init__(self): super().__init__(255, 255, 0)
    class Green(Color):
        def __init__(self): super().__init__(0, 255, 0)
    class Teal(Color):
        def __init__(self): super().__init__(0, 255, 255)
    class Blue(Color):
        def __init__(self): super().__init__(0, 0, 255)
    class Magneta(Color):
        def __init__(self): super().__init__(255, 0, 255)
    class White(Color):
        def __init__(self): super().__init__(255, 255, 255)
    ansi_to_hex_table = {
        # 16 bit ANSI
        0: "#000000",  1: "#800000",  2: "#008000",  3: "#808000",
        4: "#000080",  5: "#800080",  6: "#008080",  7: "#c0c0c0",
        8: "#808080",  9: "#ff0000", 10: "#00ff00", 11: "#ffff00",
        12: "#0000ff", 13: "#ff00ff", 14: "#00ffff", 15: "#ffffff",

        # 256 bit ANSI
        16: "#000000", 17: "#00005f", 18: "#000087", 19: "#0000af", 20: "#0000d7", 21: "#0000ff",
        22: "#005f00", 23: "#005f5f", 24: "#005f87", 25: "#005faf", 26: "#005fd7", 27: "#005fff",
        28: "#008700", 29: "#00875f", 30: "#008787", 31: "#0087af", 32: "#0087d7", 33: "#0087ff",
        34: "#00af00", 35: "#00af5f", 36: "#00af87", 37: "#00afaf", 38: "#00afd7", 39: "#00afff",
        40: "#00d700", 41: "#00d75f", 42: "#00d787", 43: "#00d7af", 44: "#00d7d7", 45: "#00d7ff",
        46: "#00ff00", 47: "#00ff5f", 48: "#00ff87", 49: "#00ffaf", 50: "#00ffd7", 51: "#00ffff",
        52: "#5f0000", 53: "#5f005f", 54: "#5f0087", 55: "#5f00af", 56: "#5f00d7", 57: "#5f00ff",
        58: "#5f5f00", 59: "#5f5f5f", 60: "#5f5f87", 61: "#5f5faf", 62: "#5f5fd7", 63: "#5f5fff",
        64: "#5f8700", 65: "#5f875f", 66: "#5f8787", 67: "#5f87af", 68: "#5f87d7", 69: "#5f87ff",
        70: "#5faf00", 71: "#5faf5f", 72: "#5faf87", 73: "#5fafaf", 74: "#5fafd7", 75: "#5fafff",
        76: "#5fd700", 77: "#5fd75f", 78: "#5fd787", 79: "#5fd7af", 80: "#5fd7d7", 81: "#5fd7ff",
        82: "#5fff00", 83: "#5fff5f", 84: "#5fff87", 85: "#5fffaf", 86: "#5fffd7", 87: "#5fffff",
        88: "#870000", 89: "#87005f", 90: "#870087", 91: "#8700af", 92: "#8700d7", 93: "#8700ff",
        94: "#875f00", 95: "#875f5f", 96: "#875f87", 97: "#875faf", 98: "#875fd7", 99: "#875fff",
        100: "#878700", 101: "#87875f", 102: "#878787", 103: "#8787af", 104: "#8787d7", 105: "#8787ff",
        106: "#87af00", 107: "#87af5f", 108: "#87af87", 109: "#87afaf", 110: "#87afd7", 111: "#87afff",
        112: "#87d700", 113: "#87d75f", 114: "#87d787", 115: "#87d7af", 116: "#87d7d7", 117: "#87d7ff",
        118: "#87ff00", 119: "#87ff5f", 120: "#87ff87", 121: "#87ffaf", 122: "#87ffd7", 123: "#87ffff",
        124: "#af0000", 125: "#af005f", 126: "#af0087", 127: "#af00af", 128: "#af00d7", 129: "#af00ff",
        130: "#af5f00", 131: "#af5f5f", 132: "#af5f87", 133: "#af5faf", 134: "#af5fd7", 135: "#af5fff",
        136: "#af8700", 137: "#af875f", 138: "#af8787", 139: "#af87af", 140: "#af87d7", 141: "#af87ff",
        142: "#afaf00", 143: "#afaf5f", 144: "#afaf87", 145: "#afafaf", 146: "#afafd7", 147: "#afafff",
        148: "#afd700", 149: "#afd75f", 150: "#afd787", 151: "#afd7af", 152: "#afd7d7", 153: "#afd7ff",
        154: "#afff00", 155: "#afff5f", 156: "#afff87", 157: "#afffaf", 158: "#afffd7", 159: "#afffff",
        160: "#d70000", 161: "#d7005f", 162: "#d70087", 163: "#d700af", 164: "#d700d7", 165: "#d700ff",
        166: "#d75f00", 167: "#d75f5f", 168: "#d75f87", 169: "#d75faf", 170: "#d75fd7", 171: "#d75fff",
        172: "#d78700", 173: "#d7875f", 174: "#d78787", 175: "#d787af", 176: "#d787d7", 177: "#d787ff",
        178: "#d7af00", 179: "#d7af5f", 180: "#d7af87", 181: "#d7afaf", 182: "#d7afd7", 183: "#d7afff",
        184: "#d7d700", 185: "#d7d75f", 186: "#d7d787", 187: "#d7d7af", 188: "#d7d7d7", 189: "#d7d7ff",
        190: "#d7ff00", 191: "#d7ff5f", 192: "#d7ff87", 193: "#d7ffaf", 194: "#d7ffd7", 195: "#d7ffff",
        196: "#ff0000", 197: "#ff005f", 198: "#ff0087", 199: "#ff00af", 200: "#ff00d7", 201: "#ff00ff",
        202: "#ff5f00", 203: "#ff5f5f", 204: "#ff5f87", 205: "#ff5faf", 206: "#ff5fd7", 207: "#ff5fff",
        208: "#ff8700", 209: "#ff875f", 210: "#ff8787", 211: "#ff87af", 212: "#ff87d7", 213: "#ff87ff",
        214: "#ffaf00", 215: "#ffaf5f", 216: "#ffaf87", 217: "#ffafaf", 218: "#ffafd7", 219: "#ffafff",
        220: "#ffd700", 221: "#ffd75f", 222: "#ffd787", 223: "#ffd7af", 224: "#ffd7d7", 225: "#ffd7ff",
        226: "#ffff00", 227: "#ffff5f", 228: "#ffff87", 229: "#ffffaf", 230: "#ffffd7", 231: "#ffffff",

        # Grayscale
        232: "#080808", 233: "#121212", 234: "#1c1c1c", 235: "#262626",
        236: "#303030", 237: "#3a3a3a", 238: "#444444", 239: "#4e4e4e",
        240: "#585858", 241: "#626262", 242: "#6c6c6c", 243: "#767676",
        244: "#808080", 245: "#8a8a8a", 246: "#949494", 247: "#9e9e9e",
        248: "#a8a8a8", 249: "#b2b2b2", 250: "#bcbcbc", 251: "#c6c6c6",
        252: "#d0d0d0", 253: "#dadada", 254: "#e4e4e4", 255: "#eeeeee"
    }
    def __init__(self): pass
    def get_reset_color(self): return "\033[0m"
    def get_ansi_start(self, ansi_num: int): return f"\033[38;5;{ansi_num}m"
    def wrap_message(self, message: str, ansi_num: int): return f"{self.get_ansi_start(ansi_num)}{message}{self.get_reset_color()}"
    def hex_to_rgb(self, hex_code: str): hex_code = hex_code.lstrip("#"); return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
    def rgb_to_hex(self, r: int, g: int, b: int): r, g, b = self.limit_rgb_value(r), self.limit_rgb_value(g), self.limit_rgb_value(b); return f"#{r:02x}{g:02x}{b:02x}"
    def hex_to_gray(self, hex_code: str): return self.rgb_to_hex(*(self.apply_grayscale(*(self.hex_to_rgb(hex_code)))))
    def ansi_to_hex(self, ansi_num: int): return self.ansi_to_hex_table.get(ansi_num, "#000000")
    def hex_to_ansi(self, hex_code: str):
        target_rgb = self.hex_to_rgb(hex_code)
        closest_code = None
        closest_dist = float("inf")
        for c, hex in self.ansi_to_hex_table.items():
            cr, cg, cb = self.hex_to_rgb(hex)
            dist = ((cr - target_rgb[0]) ** 2 + (cg - target_rgb[1]) ** 2 + (cb - target_rgb[2]) ** 2)
            if dist < closest_dist: closest_dist = dist; closest_code = c
        return closest_code
    def hex_to_ansi2(self, hex_code: str):
        closest_code = None
        closest_dist = float("inf")
        r, g, b = self.hex_to_rgb(hex_code)
        for c, hex in self.ansi_to_hex_table.items():
            cr, cg, cb = self.hex_to_rgb(hex)
            dist = (cr - r)**2 + (cg - g)**2 + (cb - b)**2
            if dist < closest_dist: closest_code = c; closest_dist = dist
        return closest_code
    def limit_rgb_value(self, value: int): return 0 if value < 0 else (255 if value > 255 else value)
    def gamma_correct(self, value: int): return (value / 255) ** 2.2
    def inverse_gamma(self, value: int): return int((value ** (1/2.2)) * 255)
    def apply_grayscale(self, r: int, g: int, b: int): res = int(0.299*r + 0.587*g + 0.114*b); return res, res, res
    def wrap_gradient_message(self, message: str, color_stops: typing.List[str]): 
        length = len(message)
        if length == 0 or len(color_stops) < 1: return message
        if len(color_stops) < 2: return self.wrap_message(message, self.hex_to_ansi(color_stops[0]))
        stops_rgb = []
        for hex_color in color_stops:
            r, g, b = self.hex_to_rgb(hex_color)
            stops_rgb.append((
                self.gamma_correct(r),
                self.gamma_correct(g),
                self.gamma_correct(b)
            ))
        result = ""
        num_segments = len(color_stops) - 1
        for i, char in enumerate(message):
            seg_length = length / num_segments
            seg_index = min(int(i / seg_length), num_segments - 1)
            start_rgb = stops_rgb[seg_index]
            end_rgb = stops_rgb[seg_index + 1]
            t = (i - seg_index * seg_length) / seg_length
            r = self.inverse_gamma(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * t)
            g = self.inverse_gamma(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * t)
            b = self.inverse_gamma(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * t)
            ansi_code = self.hex_to_ansi2(self.rgb_to_hex(r, g, b))
            result += f"{self.get_ansi_start(ansi_code)}{char}"
        return result + self.get_reset_color()
class stdout:
    buffer: str = ""
    logger = None
    log_level: int = None
    encoding: str = "utf-8"
    line_count = 0
    locked_new = False
    lang = "en"
    awaiting_bar_logs = []
    translation_obj = None
    class CompletedProcess:
        def __init__(self, stdout, returncode): self.stdout = stdout; self.returncode = returncode

    def __init__(self, logger, log_level, lang="en"): 
        import sys
        import os
        import platform
        import subprocess
        import threading
        if not platform.system() == "Windows": import pty
        import select

        self._sys = sys
        self._os = os
        self._subprocess = subprocess
        self._threading = threading
        if not platform.system() == "Windows": self._pty = pty
        self._select = select
        self._platform = platform
        self._main_os = platform.system()
        self.logger = logger
        self.log_level = log_level
        self.lang = lang
        self.buffer = ""
        self.encoding = "utf-8"
        self.line_count = 0
        self.locked_new = False
        self.awaiting_bar_logs = []
        self.translation_obj = Translator()
        self.translate = self.translation_obj.translate
        if not (lang == "en" or lang == None): self.translation_obj.load_new_language(lang)
    def write(self, message: str): 
        if self.locked_new == True and not message.startswith("\033{progressend}"): self.awaiting_bar_logs.append(message); return
        if message.startswith("\033{progress}"):
            message = message.replace("\033{progress}", "", 1)
            self._sys.__stdout__.write("\n")
            self._sys.__stdout__.flush()
            self.locked_new = True
            return
        elif message.startswith("\033{progressend}"):
            self.locked_new = False
            for i in self.awaiting_bar_logs: self.write(i)
            self.awaiting_bar_logs = []
            return
        elif message == "\033c\033[3J": return
        
        if message == "> ":
            self._sys.__stdout__.write(message)
            self._sys.__stdout__.flush()
            return
        if self.translation_obj: message = self.translation_obj.translate(message)
        self.buffer += message
        while "\n" in self.buffer:
            line, self.buffer = self.buffer.rsplit("\n", 1)
            self.line_count += 1
            if line.rstrip(): 
                try: self.logger.log(self.log_level, line.rstrip())
                except Exception: self.logger.log(self.log_level, line.rstrip().encode(self.encoding, errors="replace").decode(self.encoding))
    def clear(self):
        self._os.system("cls" if self._os.name == "nt" else 'echo "\033c\033[3J"; clear')
        self.line_count = 0
    def fileno(self): return self._sys.__stdout__.fileno()
    def change_last_message(self, message: str):
        if self.translation_obj: message = self.translation_obj.translate(message)
        self._sys.__stdout__.write("\033[1A")
        self._sys.__stdout__.write("\033[2K")
        self._sys.__stdout__.write(message + "\n")
        self._sys.__stdout__.flush()
    def run_process(self, args=["python3"], cwd=None):
        output = []
        if not self._main_os == "Windows":
            pid, fd = self._pty.fork()
            if pid == 0: 
                if cwd: self._os.chdir(cwd)
                self._os.execvp(args[0], args)
            else:
                try:
                    buffer = ""
                    while True:
                        rlist, _, _ = self._select.select([fd, self._sys.stdin], [], [])
                        if fd in rlist:
                            try:
                                data = self._os.read(fd, 1024)
                                if not data: break
                                text = data.decode(errors="replace")
                                output.append(data)
                                buffer += text

                                while "\n" in buffer:
                                    line, buffer = buffer.split("\n", 1)
                                    line += "\n"
                                    if self.translation_obj: self._sys.__stdout__.write(self.translation_obj.translate(line))
                                    else: self._sys.__stdout__.write(line)
                                    self._sys.__stdout__.flush()
                                    if "\n" not in buffer and (buffer.strip().endswith(">\r") or buffer.strip().endswith(">")): self._sys.__stdout__.write(buffer); self._sys.__stdout__.flush(); buffer = ""; continue
                            except OSError: break
                        if self._sys.stdin in rlist:
                            user_input = self._os.read(self._sys.stdin.fileno(), 1024)
                            if not user_input: break
                            self._os.write(fd, user_input)
                finally:
                    self._os.close(fd)
                    try:  _, status = self._os.waitpid(pid, 0)
                    except ChildProcessError: status = 0
                returncode = self._os.WEXITSTATUS(status)
                return self.CompletedProcess(b''.join(output).decode().replace("\r", ""), returncode)
        else:
            proc = self._subprocess.Popen(
                args,
                stdin=self._subprocess.PIPE,
                stdout=self._subprocess.PIPE,
                stderr=self._subprocess.STDOUT,
                cwd=cwd,
                bufsize=1,
                universal_newlines=True
            )
            buffer = ""
            def reader():
                nonlocal buffer
                for line in proc.stdout:
                    output.append(line.encode())
                    buffer += line
                    while "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                        line += "\n"
                        if self.translation_obj: self._sys.__stdout__.write(self.translation_obj.translate(line))
                        else: self._sys.__stdout__.write(line)
                        self._sys.__stdout__.flush()
                        if "\n" not in buffer and buffer.strip().endswith(">"):
                            self._sys.__stdout__.write(buffer)
                            self._sys.__stdout__.flush()
                            buffer = ""
            reader_thread = self._threading.Thread(target=reader)
            reader_thread.start()
            try:
                while proc.poll() is None:
                    user_input = self._sys.stdin.readline()
                    if user_input: proc.stdin.write(user_input); proc.stdin.flush()
            except KeyboardInterrupt: proc.terminate()
            reader_thread.join()
            returncode = proc.wait()
            return self.CompletedProcess(b''.join(output).decode().replace("\r", ""), returncode)
    def flush(self):
        if self.buffer.rstrip():
            try: self.logger.log(self.log_level, self.buffer.rstrip()); 
            except Exception: self.logger.log(self.log_level, self.buffer.rstrip().encode(self.encoding, errors="replace").decode(self.encoding))
        self.buffer = ""
class ProgressBar:   
    current_percentage = 0
    status_text = ""
    def submit(self, status_text: str, percentage: int):
        import sys
        self.current_percentage = percentage
        self.status_text = status_text
        fin = round(self.current_percentage/(100/20))
        beginning = '\033[38;5;82m✅' if self.current_percentage >= 100 else '\033[38;5;255m🚀'
        if self.status_text.startswith("\033ERR"): beginning = '\033[38;5;196m❌'; self.status_text = self.status_text.replace("\033ERR", "", 1)
        message = f"{beginning} {self.status_text} [{'█'*int(fin)}{'░'*int(20-fin)}] {self.current_percentage}%\033[0m"
        if hasattr(sys.stdout, "change_last_message"): sys.stdout.change_last_message(message)
        else: 
            sys.__stdout__.write("\033[1A")
            sys.__stdout__.write("\033[2K")
            sys.__stdout__.write(message + "\n")
            sys.__stdout__.flush()
    def start(self): 
        import sys
        if hasattr(sys.stdout, "change_last_message"): print("\033{progress}")
    def end(self): 
        import sys
        if hasattr(sys.stdout, "change_last_message"): print("\033{progressend}")
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
        fin = round(((self.current_countdown/self.started)*100)/(100/self.started))
        if self.begin_in_end == True or self.current_countdown > 0: beginning = f"\033[38;5;82m✅ [{'█'*int(fin)}{'░'*int(self.started-fin)}] " if self.current_countdown == 0 else f"\033[38;5;255m⏰ [{'█'*int(fin)}{'░'*int(self.started-fin)}] "
        else: beginning = "\033[38;5;255m"
        if self.current_countdown == 0: message = f"{beginning}{self.finished_text}\033[0m"
        else: message = f"{beginning}{self.current_countdown}s\033[0m"
        if hasattr(sys.stdout, "change_last_message"): sys.stdout.change_last_message(message)
        else: 
            sys.__stdout__.write("\033[1A")
            sys.__stdout__.write("\033[2K")
            sys.__stdout__.write(message + "\n")
            sys.__stdout__.flush()
    def start(self): 
        import sys
        if hasattr(sys.stdout, "change_last_message"): print("\033{progress}")
        import time
        while self.current_countdown:
            self.submit()
            if self.current_countdown == 0: break
            self.current_countdown -= 1
            time.sleep(1)
        self.submit()
        if hasattr(sys.stdout, "change_last_message"): print("\033{progressend}")
class InstantRequestJSONResponse:
    ok = True
    json = None
    def __init__(self, data: dict=None, ok: bool=True): self.json = data; self.ok = ok
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
class PyKitsIsAModule(Exception): pass
if __name__ == "__main__": raise PyKitsIsAModule("PyKits is a module and not a runable instance!")