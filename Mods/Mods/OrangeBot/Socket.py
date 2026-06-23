"""
PyKits v1.8.6 | Made by Efaz from efaz.dev

A usable set of classes with extra functions that can be used within apps. \n
Import from file: 
```python
import PyKits
pip_class = PyKits.pip()
colors_class = PyKits.Colors()
```
Import from class: 

```python
import typing
class request: ...
class pip: ...
class Colors: ...
pip_class = pip()
colors_class = Colors()
```

However! Classes may depend on other classes. Use this resource list:
    Socket: typing (module)
"""

# Module Information
__version__ = "1.8.6"
__license__ = "MIT"
__author__ = "EfazDev"
__maintainer__ = "EfazDev"
__email__ = "support@efaz.dev"
__all__ = [
    "Socket"
]

# Modules
import typing
class Socket:
    """
    A class that provides a simple interface for working with data between apps.
    """
    def __init__(self, host="127.0.0.1", port=60153):
        import socket
        import threading
        import errno
        import time
        import json
        self.host = host
        self.port = port
        self.debug = False
        self.topics = {}
        self._listener_thread = None
        self._buffer_size = 4096
        self._running = False
        self._json = json
        self._socket = socket
        self._time = time
        self._threading = threading
        self._errno = errno
    def subscribe(self, topic_name: str, call_func: typing.Callable): self.topics[topic_name] = call_func
    def listen(self):
        if self._running: return
        self._running = True
        self._listener_thread = self._threading.Thread(target=self._listen_loop, daemon=True)
        self._listener_thread.start()
        self._print_debug(f"System listening on port {self.port}...")
    def close(self):
        self._running = False
        if self._listener_thread and self._listener_thread.is_alive(): self._listener_thread.join()
        self._print_debug("Socket closed as per request.")
    def send(self, topic: str, data: typing.Any):
        payload_dict = {
            "topic": topic,
            "data": data
        }
        payload_bytes = self._json.dumps(payload_dict).encode('utf-8')
        try:
            with self._socket.socket(self._socket.AF_INET, self._socket.SOCK_STREAM) as s:
                s.connect((self.host, self.port))
                s.sendall(payload_bytes)
        except ConnectionRefusedError: self._print_debug(f"Could not send \"{topic}\" notification. Is the server running?")
    def request(self, topic: str, data: typing.Any, timeout: float = 5.0):
        payload_dict = {
            "topic": topic,
            "data": data
        }
        payload_bytes = self._json.dumps(payload_dict).encode('utf-8')
        try:
            with self._socket.socket(self._socket.AF_INET, self._socket.SOCK_STREAM) as s:
                if timeout: s.settimeout(timeout)
                s.connect((self.host, self.port))
                s.sendall(payload_bytes)
                s.shutdown(self._socket.SHUT_WR)
                chunks = []
                while True:
                    chunk = s.recv(self._buffer_size)
                    if not chunk: break
                    chunks.append(chunk)
                raw_bytes = b"".join(chunks)
                if raw_bytes:
                    response_payload = self._json.loads(raw_bytes.decode('utf-8'))
                    return response_payload.get("data")
        except ConnectionRefusedError: self._print_debug(f"Could not request \"{topic}\". Is the server running?")
        except Exception as e: self._print_debug(f"Request error: {e}")
        return None
    def exists(self):
        try:
            with self._socket.socket(self._socket.AF_INET, self._socket.SOCK_STREAM) as test: test.bind((self.host, self.port))
            return False
        except OSError as e:
            if e.errno in (self._errno.EADDRINUSE, 10048): return True
            raise e
    def wait_till_free(self, timeout: float=None, interval: float=1.0):
        start_time = self._time.time()
        while self.exists():
            self._print_debug(f"Port {self.port} is in use. Waiting for it to close...")
            if timeout is not None and (self._time.time() - start_time) > timeout:
                self._print_debug(f"Timeout of {timeout}s reached waiting for port {self.port}.")
                return False
            self._time.sleep(interval)
        self._print_debug(f"Port {self.port} is available.")
        return True
    def _listen_loop(self):
        with self._socket.socket(self._socket.AF_INET, self._socket.SOCK_STREAM) as s:
            s.setsockopt(self._socket.SOL_SOCKET, self._socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen()
            s.settimeout(1)
            while self._running:
                try:
                    conn, addr = s.accept()
                    req = self._threading.Thread(
                        target=self._handle_responding, 
                        args=(conn,), 
                        daemon=True
                    )
                    req.start()
                except self._socket.timeout: continue
                except Exception as e: self._print_debug(f"Listener error: {e}")
    def _handle_responding(self, conn):
        with conn:
            chunks = []
            while True:
                try:
                    chunk = conn.recv(self._buffer_size)
                    if not chunk: break
                    chunks.append(chunk)
                except Exception as e: self._print_debug(f"Error receiving data: {e}"); break
            raw_bytes = b"".join(chunks)
            if raw_bytes: 
                response_data = self._proc_message(raw_bytes)
                response_payload = {"topic": "_response", "data": response_data}
                try: conn.sendall(self._json.dumps(response_payload).encode('utf-8'))
                except Exception as e: self._print_debug(f"Could not send response back: {e}")
    def _proc_message(self, data: bytes):
        try:
            payload = self._json.loads(data.decode('utf-8'))
            topic = payload.get("topic")
            actual_data = payload.get("data")
            if topic in self.topics: return self.topics[topic](actual_data)
            else: self._print_debug(f"Warning: Received message for unknown topic \"{topic}\".")
        except self._json.JSONDecodeError: self._print_debug("Received invalid JSON data.")
    def _print_debug(self, message):
        if self.debug: print(f"Debug: {message}")