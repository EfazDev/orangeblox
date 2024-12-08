import hashlib
import json
def generateFileHash(file_path, algorithm="sha256"):
    hasher = hashlib.new(algorithm)
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()
with open("GeneratedHash.json", "w") as f:
    main_py_hash = generateFileHash("./Main.py")
    roblox_fflag_installer_hash = generateFileHash("./RobloxFastFlagsInstaller.py")
    install_hash = generateFileHash("./Install.py")
    bootstrap_api_hash = generateFileHash("./EfazRobloxBootstrapAPI.py")
    discord_presence_handler_hash = generateFileHash("./DiscordPresenceHandler.py")
    generated_hash_json = {
        "main": main_py_hash,
        "fflag_install": roblox_fflag_installer_hash,
        "install": install_hash,
        "bootstrap_api": bootstrap_api_hash,
        "discord_presence": discord_presence_handler_hash
    }
    json.dump(generated_hash_json, f, indent=4)
with open("./Apps/Scripts/GeneratedHash.json", "w") as f:
    json.dump(generated_hash_json, f, indent=4)
with open("README_Template.md", "r") as f:
    template_contents = f.read()
template_contents = template_contents.replace("!Main!", main_py_hash)
template_contents = template_contents.replace("!FFlag!", roblox_fflag_installer_hash)
template_contents = template_contents.replace("!Install!", install_hash)
template_contents = template_contents.replace("!BootstrapAPI!", bootstrap_api_hash)
template_contents = template_contents.replace("!DiscordPresence!", discord_presence_handler_hash)
with open("README.md", "w") as f:
    f.write(template_contents)