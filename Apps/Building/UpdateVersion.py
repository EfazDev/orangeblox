import hashlib
import subprocess
import platform
import json
import re
import os

# Generate Hash Function based on Contents
def generateFileHash(file_path: str, is_text: bool=False):
    try:
        sha_256 = hashlib.sha256()
        if is_text:
            with open(file_path, "r", encoding="utf-8", errors="ignore", newline="") as f:
                while True:
                    chunk = f.read(8192)
                    if not chunk: break
                    sha_256.update(chunk.encode("utf-8"))
        else:
            with open(file_path, "rb") as f:
                while True:
                    chunk = f.read(8192)
                    if not chunk: break
                    sha_256.update(chunk)
        return sha_256.hexdigest()
    except Exception: return None

# Load Version.json
version_json = {
    "version": "2.6.0j",
    "latest_version": "2.6.0j",
    "hashes": {},
    "download_location": "https://github.com/EfazDev/orangeblox/archive/refs/heads/main.zip"
}
display_names = {
    "Main.py": "Main Bootstrap",
    "RobloxManager.py": "Roblox Manager",
    "Install.py": "Installer",
    "OrangeAPI.py": "Bootstrap API",
    "OrangeBlox.py": "Bootstrap Loader",
    "PyKits.py": "PyKits API",
    "Modules/config.py": "Configuration Module",
    "Modules/menu.py": "Menu Module",
    "Modules/modmanager.py": "Mod Manager Module",
    "Modules/modscripts.py": "Mod Scripts Module",
    "Modules/options.py": "Menu Options Module",
    "Modules/pkg.py": "Python Package Module",
    "Modules/printing.py": "Printing/Logging Module",
    "Modules/roblox.py": "Roblox Module",
    "Modules/settings.py": "Settings Module",
    "Modules/startup.py": "Startup Module",
    "Modules/utils.py": "Utilities Module",
    "Modules/discord.py": "Discord RPC Module"
}
if os.path.exists("Version.json"):
    with open("Version.json", "r", encoding="utf-8") as f: version_json = json.load(f)

# Generate Hashes
generated_hash_json = {}
blocked_scripts = ["RobloxFastFlagsInstaller.py"]
for i in os.listdir("./"):
    if i.endswith(".py") and i not in blocked_scripts:
        generated_hash = generateFileHash(f"./{i}", is_text=True)
        generated_hash_json[i] = generated_hash
for i in os.listdir("./Modules"):
    if i.endswith(".py") and i not in blocked_scripts:
        generated_hash = generateFileHash(f"./Modules/{i}", is_text=True)
        generated_hash_json[f"Modules/{i}"] = generated_hash
generated_hash2 = generateFileHash(f"./Apps/Building/OrangeBlox.py", is_text=True)
generated_hash_json["OrangeBlox.py"] = generated_hash2
previous_hashes = version_json["hashes"]
version_json["hashes"] = generated_hash_json
if "https://github.com/EfazDev/orangeblox/" in version_json["download_location"]:
    if "beta" in (subprocess.run("git branch --show-current", shell=True, text=True, capture_output=True).stdout):
        version_json["download_location"] = "https://github.com/EfazDev/orangeblox/archive/refs/heads/beta.zip"
    else:
        version_json["download_location"] = "https://github.com/EfazDev/orangeblox/archive/refs/heads/main.zip"

# Edit Version.txt for Windows
with open("Apps/Storage/Version.txt", "r", encoding="utf-8") as f: version_txt = f.read()
split_vers = version_json["version"].split(".")
letter_version = None
if len(split_vers[2]) > 1:
    letter_version = split_vers[2][1:]
    split_vers[2] = split_vers[2][:-1]
version_txt = re.sub(r"\((\d+, \d+, \d+, \d+)\)", f"({split_vers[0]}, {split_vers[1]}, {split_vers[2]}, {ord(letter_version) if letter_version else 0})", version_txt)

# Save Files
with open("Version.json", "w", encoding="utf-8") as f: json.dump(version_json, f, indent=4)
with open("Apps/Storage/Version.txt", "w", encoding="utf-8") as f: f.write(version_txt)

# Build README.md
try:
    table_md = "| File | SHA256 Hash |\n| --- | --- |\n"
    for file_key, file_hash in generated_hash_json.items():
        display = display_names.get(file_key, file_key)
        table_md += f"| {display} ({file_key}) | `{file_hash}` |\n" 
    with open("README.md", "r", encoding="utf-8") as f:  read_me_contents = f.read()
    pattern = r"(## Hashes)\n+(.*?)\n+(## Credits)"
    replacement = rf"\1\n{table_md}\n\3"
    read_me_contents = re.sub(pattern, replacement, read_me_contents, flags=re.DOTALL)
    with open("README.md", "w", encoding="utf-8") as f: f.write(read_me_contents)
except Exception as e: print("Failed to build README.md, ignored.")