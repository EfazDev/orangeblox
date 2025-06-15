from pathlib import Path
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
def download_luapackages(version: str, channel: str, output_directory: str | Path, studio: bool) -> None:
    progress_bar = ProgressBar()
    output_directory = Path(output_directory)
    if platform.system() == "Darwin":
        download(Api.Roblox.Deployment.download(version, "RobloxStudioApp.zip", channel, True), output_directory / "download" / f"{version}-RobloxStudioApp.zip")
        progress_bar.submit("[MOD_GEN] Extracting Roblox Studio..", 35)
        extract(os.path.join(output_directory, "download", f"{version}-RobloxStudioApp.zip"), output_directory / version / "RobloxStudio.app", False, ["RobloxStudio.app/Contents/Resources/content/*", "RobloxStudio.app/Contents/Resources/ExtraContent/*"])
        shutil.copytree(os.path.join(output_directory, version, "RobloxStudio.app", "RobloxStudio.app", "Contents", "Resources", "content"), output_directory / version / "content", dirs_exist_ok=True)
        shutil.copytree(os.path.join(output_directory, version, "RobloxStudio.app", "RobloxStudio.app", "Contents", "Resources", "ExtraContent"), output_directory / version / "ExtraContent", dirs_exist_ok=True)
        shutil.rmtree(os.path.join(output_directory, version, "RobloxStudio.app"), ignore_errors=True)
    else:
        progress_bar.submit("[MOD_GEN] Downloading Extra Content Textures..", 30)
        download(Api.Roblox.Deployment.download(version, "extracontent-textures.zip", channel, True), output_directory / "download" / f"{version}-extracontent-textures.zip")
        extract(os.path.join(output_directory, "download", f"{version}-extracontent-textures.zip"), output_directory / version / "ExtraContent" / "textures")
        progress_bar.submit("[MOD_GEN] Downloading Lua Packages..", 40)
        download(Api.Roblox.Deployment.download(version, "extracontent-luapackages.zip", channel, True), output_directory / "download" / f"{version}-extracontent-luapackages.zip")
        extract(os.path.join(output_directory, "download", f"{version}-extracontent-luapackages.zip"), output_directory / version / "ExtraContent" / "LuaPackages")
        progress_bar.submit("[MOD_GEN] Downloading Extra Lua Scripts..", 40)
        download(Api.Roblox.Deployment.download(version, "extracontent-scripts.zip", channel, True), output_directory / "download" / f"{version}-extracontent-scripts.zip")
        extract(os.path.join(output_directory, "download", f"{version}-extracontent-scripts.zip"), output_directory / version / "ExtraContent" / "scripts")
        progress_bar.submit("[MOD_GEN] Downloading Textures..", 45)
        download(Api.Roblox.Deployment.download(version, "content-textures2.zip", channel, True), output_directory / "download" / f"{version}-content-textures2.zip")
        extract(os.path.join(output_directory, "download", f"{version}-content-textures2.zip"), output_directory / version / "content" / "textures")
        download(Api.Roblox.Deployment.download(version, "content-textures3.zip", channel, True), output_directory / "download" / f"{version}-content-textures3.zip")
        extract(os.path.join(output_directory, "download", f"{version}-content-textures3.zip"), output_directory / version / "content" / "textures")