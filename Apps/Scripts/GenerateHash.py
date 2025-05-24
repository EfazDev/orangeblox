import hashlib
import json
import os

# Generate Hash Function based on Contents
def generateFileHash(file_path):
    try:
        with open(file_path, "rb") as f:
            hasher = hashlib.md5()
            chunk = f.read(8192)
            while chunk: 
                hasher.update(chunk)
                chunk = f.read(8192)
        return hasher.hexdigest()
    except Exception as e:
        return None

# Load Version.json
version_json = {
    "version": "2.0.2",
    "latest_version": "2.0.2",
    "versions_required_install": {"2.0.2": True},
    "hashes": {},
    "download_location": "https://github.com/EfazDev/orangeblox/archive/refs/heads/main.zip"
}
if os.path.exists("Version.json"):
    with open("Version.json", "r", encoding="utf-8") as f:
        version_json = json.load(f)

# Generate Hashes
main_py_hash = generateFileHash("./Main.py")
roblox_fflag_installer_hash = generateFileHash("./RobloxFastFlagsInstaller.py")
install_hash = generateFileHash("./Install.py")
bootstrap_api_hash = generateFileHash("./OrangeAPI.py")
discord_presence_handler_hash = generateFileHash("./DiscordPresenceHandler.py")
pip_handler_hash = generateFileHash("./PipHandler.py")
generated_hash_json = {
    "main": main_py_hash,
    "fflag_install": roblox_fflag_installer_hash,
    "install": install_hash,
    "bootstrap_api": bootstrap_api_hash,
    "discord_presence": discord_presence_handler_hash,
    "pip_handler": pip_handler_hash
}
previous_hashes = version_json["hashes"]
version_json["hashes"] = generated_hash_json

# Save Files
with open("Version.json", "w", encoding="utf-8") as f:
    json.dump(version_json, f, indent=4)
with open("./Apps/Scripts/Version.json", "w", encoding="utf-8") as f:
    json.dump(version_json, f, indent=4)

# Build README.md
try:
    with open("README.md", "r", encoding="utf-8") as f:
        read_me_contents = f.read()
    read_me_contents = read_me_contents.replace(previous_hashes["main"], main_py_hash)
    read_me_contents = read_me_contents.replace(previous_hashes["fflag_install"], roblox_fflag_installer_hash)
    read_me_contents = read_me_contents.replace(previous_hashes["install"], install_hash)
    read_me_contents = read_me_contents.replace(previous_hashes["bootstrap_api"], bootstrap_api_hash)
    read_me_contents = read_me_contents.replace(previous_hashes["discord_presence"], discord_presence_handler_hash)
    read_me_contents = read_me_contents.replace(previous_hashes["pip_handler"], pip_handler_hash)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(read_me_contents)
except Exception as e:
    print("Failed to build README.md, ignored.")