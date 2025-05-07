import os
import json
import shutil
import ssl
import sys
import platform
from pathlib import Path
from tempfile import TemporaryDirectory

from mod_generator.deploy_history import DeployHistory, DeployHistoryError, get_deploy_history
from mod_generator.download_luapackages import download_luapackages
from mod_generator.locate_imagesets import locate_imagesets
from mod_generator.locate_imagesetdata_file import locate_imagesetdata_file
from mod_generator.get_icon_map import get_icon_map
from mod_generator.generate_imagesets import generate_imagesets
from mod_generator.generate_additional_files import generate_additional_files
from mod_generator.generate_user_selected_files import generate_user_selected_files
from mod_generator.add_watermark import add_watermark
from mod_generator.deploy_history import DeployHistory, get_deploy_history

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
current_path_location = os.path.dirname(os.path.abspath(__file__))
progress_bar = ProgressBar()

def run(versions: str, name: str, colors: list[str], angle: int, studio: bool=False, user_selected_files: list[dict[str, Path | list[str]]] | None = None) -> None:
    try:
        channel = versions["channel"]
        try:
            deploy_history: DeployHistory = get_deploy_history(versions['version'])
            hash = deploy_history.get_hash(versions['version'])
        except Exception as e:
            hash = versions['hash']
        progress_bar.start()
        progress_bar.submit("[MOD_GEN] Fetching Studio Version!", 5)
        version: str = deploy_history.get_studio_version(hash, macos=platform.system()=="Darwin")
        output_dir = os.path.join(current_path_location, "test")
        output_dir = Path(output_dir)

        progress_bar.submit("[MOD_GEN] Making Base Directories..", 0)
        if not os.path.exists(os.path.join(current_path_location, "test")):
            os.makedirs(os.path.join(current_path_location, "test"))
        if os.path.exists(os.path.join(current_path_location, "result")):
            shutil.rmtree(os.path.join(current_path_location, "result"), ignore_errors=True)
        os.makedirs(os.path.join(current_path_location, "result"))

        """
        if os.path.exists(os.path.join(current_path_location, "test", name)):
            shutil.copytree(os.path.join(current_path_location, "test", name), os.path.join(current_path_location, "result", name), dirs_exist_ok=True)
            shutil.rmtree(os.path.join(current_path_location, "test"), ignore_errors=True)
            raise Exception(os.path.join(current_path_location, "result", name))
        """

        # Generate mods for latest Player version, instead of the latest Studio version
        deployment = ""
        studio_version = version

        progress_bar.submit("[MOD_GEN] Creating Temporary Directories..", 10)
        temporary_directory: Path = Path(os.path.join(current_path_location, "test"))
        temp_target: Path = temporary_directory / name
        temp_target.mkdir(parents=True, exist_ok=True)

        progress_bar.submit("[MOD_GEN] Generating Mod Folder..", 15)
        data: dict = {"clientVersionUpload": studio_version, "channel": channel, "watermark": "Generated with Kliko's mod generator"}
        with open(temp_target / "info.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        progress_bar.submit("[MOD_GEN] Downloading Roblox Studio Packages..", 20)
        download_luapackages(studio_version, channel, temporary_directory, studio)

        progress_bar.submit("[MOD_GEN] Locating Image Sets..", 50)
        imageset_path: Path = locate_imagesets(temporary_directory / studio_version)
        shutil.copytree((temporary_directory / studio_version / imageset_path), (temp_target / imageset_path), dirs_exist_ok=True)

        progress_bar.submit("[MOD_GEN] Locating Image Set Data..", 60)
        imagesetdata_path: Path = locate_imagesetdata_file(temporary_directory / studio_version)

        progress_bar.submit("[MOD_GEN] Fetching Icon Map..", 70)
        icon_map: dict[str, dict[str, dict[str, str | int]]] = get_icon_map(temporary_directory / studio_version / imagesetdata_path)

        progress_bar.submit("[MOD_GEN] Generating Image Sets..", 80)
        generate_imagesets((temp_target / imageset_path), icon_map, colors, angle)

        progress_bar.submit("[MOD_GEN] Generating Additional Files..", 90)
        generate_additional_files(temp_target, colors, angle)
        if user_selected_files: 
            progress_bar.submit("[MOD_GEN] Generating User Selected Files..", 90)
            generate_user_selected_files(temp_target, colors, angle, user_selected_files)

        # add_watermark((temp_target / imageset_path))
        progress_bar.submit("[MOD_GEN] Cleaning up..", 95)
        if os.path.exists(os.path.join(current_path_location, "test", name)):
            shutil.copytree(os.path.join(current_path_location, "test", name), os.path.join(current_path_location, "result", name), dirs_exist_ok=True)
            shutil.rmtree(os.path.join(current_path_location, "test"), ignore_errors=True)
            raise Exception(os.path.join(current_path_location, "result", name))
        else:
            raise Exception("Mod doesn't exist.")
    except Exception as e:
        if os.path.exists(str(e)):
            progress_bar.submit("[MOD_GEN] Successfully created mod!", 100)
            progress_bar.end()
            return str(e)
        else:
            progress_bar.submit("\033ERR[MOD_GEN] Something went wrong with making mod!", 100)
            progress_bar.end()
            raise e