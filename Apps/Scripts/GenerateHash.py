import hashlib
import json
import os

# Generate Hash Function based on Contents
def generateFileHash(file_path, algorithm="sha256"):
    hasher = hashlib.new(algorithm)
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()

# Load Version.json
version_json = {
    "version": "1.5.7",
    "latest_version": "1.5.7",
    "versions_required_install": {"1.5.7": True},
    "hashes": {},
    "download_location": "https://github.com/EfazDev/roblox-bootstrap/archive/refs/heads/main.zip"
}
if os.path.exists("Version.json"):
    with open("Version.json", "r") as f:
        version_json = json.load(f)

# Generate Hashes
main_py_hash = generateFileHash("./Main.py")
roblox_fflag_installer_hash = generateFileHash("./RobloxFastFlagsInstaller.py")
install_hash = generateFileHash("./Install.py")
bootstrap_api_hash = generateFileHash("./EfazRobloxBootstrapAPI.py")
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
with open("Version.json", "w") as f:
    json.dump(version_json, f, indent=4)
with open("./Apps/Scripts/Version.json", "w") as f:
    json.dump(version_json, f, indent=4)
with open("README.md", "r") as f:
    read_me_contents = f.read()

# Build README.md
read_me_contents = read_me_contents.replace(previous_hashes["main"], main_py_hash)
read_me_contents = read_me_contents.replace(previous_hashes["fflag_install"], roblox_fflag_installer_hash)
read_me_contents = read_me_contents.replace(previous_hashes["install"], install_hash)
read_me_contents = read_me_contents.replace(previous_hashes["bootstrap_api"], bootstrap_api_hash)
read_me_contents = read_me_contents.replace(previous_hashes["discord_presence"], discord_presence_handler_hash)
read_me_contents = read_me_contents.replace(previous_hashes["pip_handler"], pip_handler_hash)
with open("README.md", "w") as f:
    f.write(read_me_contents)