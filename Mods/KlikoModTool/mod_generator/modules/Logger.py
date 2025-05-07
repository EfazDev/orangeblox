import logging
from pathlib import Path
from datetime import datetime, timedelta
import sys
import inspect
import platform

from mod_generator.modules import LaunchMode


IS_FROZEN: bool = getattr(sys, "frozen", False)
if IS_FROZEN:
    ROOT: Path = Path(sys.executable).parent
else:
    ROOT = Path(__file__).parent.parent


TIMESTAMP: str = datetime.now().strftime("%Y-%m-%d@%H-%M-%S.%f")
LAUNCH_MODE: str = LaunchMode.get()
FILENAME: str = f"{TIMESTAMP}_{LAUNCH_MODE.upper()}.log"
LOG_DIRECTORY: Path = Path(ROOT, "Logs")
FILEPATH: Path = Path(LOG_DIRECTORY, FILENAME)

MAX_LOG_AGE: int = 7  # DAYS


def initialize() -> None:
    pass


def remove_old_logs() -> None:
    for log in LOG_DIRECTORY.iterdir():
        if not log.is_file():
            continue

        age: timedelta = datetime.now() - datetime.fromtimestamp(log.stat().st_mtime)
        if age > timedelta(days=MAX_LOG_AGE):
            try:
                log.unlink()
                debug(f"Removed old log: {log.name}")
            except Exception as e:
                warning(f"Failed to remove old log: {log.name}! {type(e).__name__}: {e}")


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


def info(message: object, *_, prefix: str | None = None) -> None:
    pass


def warning(message: object, *_, prefix: str | None = None) -> None:
    pass


def error(message: object, *_, prefix: str | None = None, exc_info = None) -> None:
    pass


def debug(message: object, *_, prefix: str | None = None) -> None:
    pass


def critical(message: object, *_, prefix: str | None = None, exc_info = None) -> None:
    pass


initialize()