import os
import platform
import subprocess
from pathlib import Path
from mod_updater.modules import Logger
from mod_updater.exceptions import FileExtractError

def extract(source: str | Path, destination: str | Path, ignore_filetype: bool = False, specificPath: list=[]) -> None:
    source = Path(source)
    destination = Path(destination)
    Logger.info(f"Extracting file: {source.name}...", prefix="filesystem.extract()")

    if destination.is_file(): raise FileExtractError(f"Destination must be a directory! (destination: {destination.name})")
    if not source.is_file(): raise FileExtractError(f"Source does not exist! (source: {source.name})")
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not os.access(destination.parent, os.W_OK): raise FileExtractError(f"Write permissions denied for {destination.parent}")

    if ignore_filetype:
        if not os.path.exists(destination): os.makedirs(destination)
        if platform.system() == "Darwin": subprocess.run(["/usr/bin/ditto", "-xk", source, destination], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else: subprocess.run(["C:\\Windows\\System32\\tar.exe", "-xf", source, "-C", destination], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return
    match source.suffix:
        case ".zip":
            if not os.path.exists(destination): os.makedirs(destination)
            if platform.system() == "Darwin": subprocess.run(["/usr/bin/ditto", "-xk", source, destination], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else: subprocess.run(["C:\\Windows\\System32\\tar.exe", "-xf", source, "-C", destination], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        case _:
            raise FileExtractError(f"Unsupported file format: {source.name}")