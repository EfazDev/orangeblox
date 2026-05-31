import hashlib
import subprocess
import platform
import json
import re
import os

# Generate Hash Function based on Contents
def generateFileHash(file_path):
    try:
        hasher = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                if platform.system() == "Windows": chunk = chunk.replace(b"\r\n", b"\n")
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception: return None

# Load Version.json
version_json = {
    "version": "2.5.0i",
    "latest_version": "2.5.0i",
    "hashes": {},
    "download_location": "https://github.com/EfazDev/orangeblox/archive/refs/heads/main.zip"
}
if os.path.exists("Version.json"):
    with open("Version.json", "r", encoding="utf-8") as f: version_json = json.load(f)

# Generate Hashes
generated_hash_json = {}
for i in os.listdir("./"):
    if i.endswith(".py"):
        generated_hash = generateFileHash(f"./{i}")
        generated_hash_json[i] = generated_hash
generated_hash2 = generateFileHash(f"./Apps/Building/OrangeBlox.py")
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
    with open("README.md", "r", encoding="utf-8") as f: read_me_contents = f.read()
    for i, v in previous_hashes.items(): read_me_contents = read_me_contents.replace(v, generated_hash_json[i])
    with open("README.md", "w", encoding="utf-8") as f: f.write(read_me_contents)
except Exception as e: print("Failed to build README.md, ignored.")