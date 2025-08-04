from pathlib import Path
from threading import Thread
from queue import Queue
import platform
import shutil
import json
import ssl
import sys
import os

from mod_updater.modules import Logger
from mod_updater.deploy_history import DeployHistory, get_deploy_history
from mod_updater.download_luapackages import download_luapackages
from mod_updater.image_sets import locate_imagesets, locate_imagesetdata_files, get_icon_map
from mod_updater.detect_modded_icons import detect_modded_icons
from mod_updater.generate_new_imagesets import generate_new_imagesets
from mod_updater.finish_mod_update import finish_mod_update

class ProgressBar():   
    current_percentage = 0
    status_text = ""
    def submit(self, status_text: str, percentage: int):
        self.current_percentage = percentage
        self.status_text = status_text
        fin = round(self.current_percentage/(100/20))
        beginning = '\033[38;5;82m✅' if self.current_percentage >= 100 else '\033[38;5;255m🚀'
        if self.status_text.startswith("\033ERR"): beginning = '\033[38;5;196m❌'; self.status_text = self.status_text.replace("\033ERR", "", 1)
        message = f"{beginning} {self.status_text} [{'█'*int(fin)}{'░'*int(20-fin)}] {self.current_percentage}%\033[0m"
        sys.__stdout__.write("\033[1A")
        sys.__stdout__.write("\033[2K")
        sys.__stdout__.write(message + "\n")
        sys.__stdout__.flush()
    def start(self): pass
    def end(self): pass
ssl._create_default_https_context = ssl._create_unverified_context
cur_path = os.path.dirname(os.path.abspath(__file__))
progress_bar = ProgressBar()
channel = None
def update_mods(check: dict[str, list[Path]], versions: str) -> None:
    latest_version = versions["version"]
    vers_channel = versions["channel"]
    global channel
    try:
        output_dir = os.path.join(cur_path, "result")
        progress_bar.start()
        progress_bar.submit("[MOD_UPDATE] Starting Mod Updater!", 0)
        output_directory = Path(output_dir)
        deploy_history: DeployHistory = get_deploy_history(latest_version)
        progress_bar.submit("[MOD_UPDATE] Making Base Directories..", 0)
        if not os.path.exists(os.path.join(cur_path, "test")): os.makedirs(os.path.join(cur_path, "test"),mode=511)
        if os.path.exists(os.path.join(cur_path, "result")): shutil.rmtree(os.path.join(cur_path, "result"), ignore_errors=True)
        os.makedirs(os.path.join(cur_path, "result"),mode=511)
        channel = vers_channel
        # Each mod will be updated simultaneously
        threads: list[Thread] = []
        exception_queue: Queue = Queue()
        for hash, mods in check.items():
            thread: Thread = Thread(
                name=f"mod_updater.hash_specific_worker_thread({hash})",
                target=hash_specific_worker_thread,
                args=(deploy_history, exception_queue, hash, mods, output_directory),
                daemon=True
            )
            thread.start()
            threads.append(thread)
        for thread in threads: thread.join()
        progress_bar.submit("[MOD_UPDATE] Cleaning up..", 95)
        if os.path.exists(os.path.join(cur_path, "test")): shutil.rmtree(os.path.join(cur_path, "test"), ignore_errors=True)
        if not exception_queue.empty():
            e: Exception = exception_queue.get()
            Logger.error(f"{type(e).__name__}: {e}", prefix="mod_updater.update_mods()")
            raise e
        else:
            progress_bar.submit("[MOD_UPDATE] Successfully updated mod!", 100)
            progress_bar.end()
    except Exception as e:
        if os.path.exists(str(e)):
            progress_bar.submit("[MOD_UPDATE] Successfully updated mod!", 100)
            progress_bar.end()
            return str(e)
        else:
            progress_bar.submit("\033ERR[MOD_UPDATE] Something went wrong with updating mod!", 100)
            progress_bar.end()
            raise e
def hash_specific_worker_thread(deploy_history: DeployHistory, exception_queue: Queue, hash: str, mods: list[Path], output_directory: Path) -> None:
    global channel
    if hash == deploy_history.get_hash(deploy_history.LatestVersion.studio) or not mods: return
    try:
        temporary_directory: Path = Path(os.path.join(cur_path, "test"))
        progress_bar.submit("[MOD_UPDATE] Copying Mods to Testing!", 10)
        Logger.info("Copying mods to temporary directory...", prefix=f"mod_updater.worker_thread({hash})")
        for mod in mods: shutil.copytree(mod, temporary_directory / mod.name, dirs_exist_ok=True)
        progress_bar.submit("[MOD_UPDATE] Updating info.json!", 15)
        Logger.info("Updating info.json...", prefix=f"mod_updater.worker_thread({hash})")
        different_versions = {}
        for mod in mods:
            with open(temporary_directory / mod.name / "info.json", "r") as file: data: dict = json.load(file)
            if different_versions.get(data["clientVersionUpload"]): different_versions[data["clientVersionUpload"]][1].append(mod)
            else: different_versions[data["clientVersionUpload"]] = [data.get("channel", "LIVE"), [mod]]
            data["clientVersionUpload"] = deploy_history.LatestVersion.studio
            data["channel"] = channel
            with open(temporary_directory / mod.name / "info.json", "w") as file: json.dump(data, file, indent=4)
        progress_bar.submit("[MOD_UPDATE] Downloading Lua Packages of Latest!", 30)
        Logger.info(f"Downloading LuaPackages for {hash}", prefix=f"mod_updater.worker_thread({hash})")
        download_luapackages(deploy_history.LatestVersion.studio, channel, temporary_directory, platform.system() == "Darwin")
        co = 0
        for i, v in different_versions.items():
            i = deploy_history.get_studio_version(deploy_history.get_hash(i), deploy_history.is_macos_version(i))
            co += 1
            progress_bar.submit(f"[MOD_UPDATE] Downloading Lua Packages of Version {i} (Channel: {v[0]})!", 30+co*(15/len(different_versions.values())))
            download_luapackages(i, v[0], temporary_directory, deploy_history.is_macos_version(i))
            progress_bar.submit("[MOD_UPDATE] Locating Image Sets!", 45)
            Logger.info("Locating ImageSets...", prefix=f"mod_updater.worker_thread({hash})")
            mod_imageset_path: Path = locate_imagesets(temporary_directory / i)[0]
            latest_imageset_path: Path = locate_imagesets(temporary_directory / deploy_history.LatestVersion.studio)[0]
            progress_bar.submit("[MOD_UPDATE] Locating Image Set Data!", 50)
            Logger.info("Locating ImageSetData...", prefix=f"mod_updater.worker_thread({hash})")
            mod_imagesetdata_path: Path = locate_imagesetdata_files(temporary_directory / i)[0]
            latest_imagesetdata_path: Path = locate_imagesetdata_files(temporary_directory / deploy_history.LatestVersion.studio)[0]
            progress_bar.submit("[MOD_UPDATE] Fetching Icon Map!", 60)
            Logger.info("Getting icon map...", prefix=f"mod_updater.worker_thread({hash})")
            mod_icon_map: dict[str, dict[str, dict[str, str | int]]] = get_icon_map(temporary_directory / i / mod_imagesetdata_path)
            latest_icon_map: dict[str, dict[str, dict[str, str | int]]] = get_icon_map(temporary_directory / deploy_history.LatestVersion.studio / latest_imagesetdata_path)
            for mod in mods:
                try:
                    progress_bar.submit("[MOD_UPDATE] Locating Modded Icons!", 70)
                    Logger.info("Detecting modded icons...", prefix=f"mod_updater.worker_thread({hash})")
                    modded_icons: dict[str, list[str]] = detect_modded_icons((temporary_directory / mod.name / mod_imageset_path), (temporary_directory / i / mod_imageset_path), mod_icon_map)
                    if modded_icons:
                        progress_bar.submit("[MOD_UPDATE] Generating Image Sets!", 90)
                        Logger.info("Generating ImageSets...", prefix=f"mod_updater.worker_thread({hash})")
                        generate_new_imagesets(modded_icons, mod_icon_map, latest_icon_map, mod_imageset_path, latest_imageset_path, deploy_history.LatestVersion.studio, mod.name, temporary_directory)
                    progress_bar.submit("[MOD_UPDATE] Cleaning up..", 95)
                    Logger.info(f"Finishing mod update: {mod.name}", prefix=f"mod_updater.worker_thread({hash})")
                    finish_mod_update(mod.name, temporary_directory, output_directory)
                    if os.path.exists(temporary_directory): shutil.rmtree(temporary_directory, ignore_errors=True)
                    progress_bar.submit("[MOD_UPDATE] Successfully finished Mod Update!", 100)
                except Exception as e:
                    progress_bar.submit("\033ERR[MOD_UPDATE] Mod Updater has failed!", 100)
                    Logger.error(f"Failed to update mod: {mod.name} | {type(e).__name__}: {e}", prefix=f"mod_updater.worker_thread({hash})")
    except Exception as e:
        progress_bar.submit("\033ERR[MOD_UPDATE] Mod Updater has failed!", 100)
        Logger.error(f"{type(e).__name__}: {e}", prefix=f"mod_updater.worker_thread({hash})")
        exception_queue.put(e)