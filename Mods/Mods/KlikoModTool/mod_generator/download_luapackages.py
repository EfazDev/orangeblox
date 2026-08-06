from pathlib import Path
import concurrent.futures
import os
import shutil
import platform
import sys
from mod_generator.modules.filesystem import download, extract
from mod_generator.modules.request import Api

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
def download_luapackages(version: str, channel: str, output_directory: str | Path, macos: bool) -> None:
    progress_bar = ProgressBar()
    output_directory = Path(output_directory)
    if macos:
        download(Api.Roblox.Deployment.download(version, "RobloxStudioApp.zip", channel, macos), output_directory / "download" / f"{version}-RobloxStudioApp.zip")
        progress_bar.submit("[MOD_GEN] Extracting Roblox Studio..", 35)
        extract(os.path.join(output_directory, "download", f"{version}-RobloxStudioApp.zip"), output_directory / version / "RobloxStudio.app", False, ["RobloxStudio.app/Contents/Resources/content/*", "RobloxStudio.app/Contents/Resources/ExtraContent/*"])
        shutil.move(os.path.join(output_directory, version, "RobloxStudio.app", "RobloxStudio.app", "Contents", "Resources", "content"), output_directory / version / "content")
        shutil.move(os.path.join(output_directory, version, "RobloxStudio.app", "RobloxStudio.app", "Contents", "Resources", "ExtraContent"), output_directory / version / "ExtraContent")
        shutil.rmtree(os.path.join(output_directory, version, "RobloxStudio.app"), ignore_errors=True)
    else:
        progress_bar.submit("[MOD_GEN] Downloading Packages...", 30)
        packages = [
            ("extracontent-textures.zip", "ExtraContent/textures"),
            ("extracontent-luapackages.zip", "ExtraContent/LuaPackages"),
            ("extracontent-scripts.zip", "ExtraContent/scripts"),
            ("content-textures2.zip", "content/textures"),
            ("content-textures3.zip", "content/textures")
        ]
        def process_package(pkg_name, extract_subpath):
            download_url = Api.Roblox.Deployment.download(version, pkg_name, channel, macos)
            download_path = output_directory / "download" / f"{version}-{pkg_name}"
            extract_path = output_directory / version / extract_subpath
            download(download_url, download_path)
            extract(os.path.join(output_directory, "download", f"{version}-{pkg_name}"), extract_path)
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(process_package, pkg, dest) 
                for pkg, dest in packages
            ]
            concurrent.futures.wait(futures)
        progress_bar.submit("[MOD_GEN] Finished Downloading Packages..", 45)