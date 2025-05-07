import logging
from pathlib import Path
from datetime import datetime, timedelta
import os
import sys
import inspect
import platform


IS_FROZEN: bool = getattr(sys, "frozen", False)
if IS_FROZEN:
    ROOT: Path = Path(sys.executable).parent
else:
    ROOT = Path(__file__).parent.parent


TIMESTAMP: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")
FILENAME: str = f"{TIMESTAMP}_MODDING-TOOL.log"
LOG_DIRECTORY: Path = Path(ROOT, "Logs")
FILEPATH: Path = Path(LOG_DIRECTORY, FILENAME)

MAX_LOG_AGE: int = 7  # DAYS


def initialize() -> None:
    pass


def remove_old_logs() -> None:
    logs: list[Path] = [Path(LOG_DIRECTORY, file) for file in os.listdir(LOG_DIRECTORY)]

    for log in logs:
        age: timedelta = datetime.now() - datetime.fromtimestamp(os.path.getmtime(log))
        if age > timedelta(days=MAX_LOG_AGE):
            try:
                os.remove(log)
                debug(f"Removed old log: {log.name}")
            except Exception as e:
                warning(f"Failed to remove old log: {log.name} | Reason: {type(e).__name__}: {e}")


def get_prefix() -> str:
        UNKNOWN: str = "unknown()"
        frame = inspect.currentframe()
        if frame is None:
            return UNKNOWN
        frame = frame.f_back
        if frame is None:
            return UNKNOWN
        frame = frame.f_back
        if frame is None:
            return UNKNOWN

        filepath: Path = Path(frame.f_code.co_filename)
        module: str = filepath.parent.stem if filepath.stem == "__init__" else filepath.stem
        function: str = frame.f_code.co_name
        return f"{module}.{function}()"


def info(message: object, prefix=None) -> None:
    pass


def warning(message: object, prefix=None) -> None:
    pass


def error(message: object, exc_info = None, prefix=None) -> None:
    pass


def debug(message: object, prefix=None) -> None:
    pass


def critical(message: object, exc_info = None, prefix=None) -> None:
    pass


initialize()