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
    "version": "2.1.1",
    "latest_version": "2.1.1",
    "versions_required_install": {"2.1.1": True},
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
generated_hash2 = generateFileHash(f"./Apps/Scripts/OrangeBlox.py")
generated_hash_json["OrangeBlox.py"] = generated_hash2
previous_hashes = version_json["hashes"]
version_json["hashes"] = generated_hash_json

# Save Files
with open("Version.json", "w", encoding="utf-8") as f: json.dump(version_json, f, indent=4)

# Build README.md
try:
    with open("README.md", "r", encoding="utf-8") as f: read_me_contents = f.read()
    for i, v in previous_hashes.items(): read_me_contents = read_me_contents.replace(v, generated_hash_json[i])
    with open("README.md", "w", encoding="utf-8") as f: f.write(read_me_contents)
except Exception as e: print("Failed to build README.md, ignored.")