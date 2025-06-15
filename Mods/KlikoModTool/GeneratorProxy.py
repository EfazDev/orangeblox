import importlib.util
import shutil
import os
import sys
import json

current_path_location = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("run", f"{current_path_location}/mod_generator/run.py")
mod_mode_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod_mode_module)
installed = json.loads(sys.argv[1])
mod_style_json = json.loads(sys.argv[2])
is_studio = sys.argv[3]=="True"
from mod_generator.exceptions import DeployHistoryError

fold_name = mod_style_json["name"]
if is_studio == True: fold_name = f'{mod_style_json["name"]} [STUDIO]'
print("\033[38;5;226mProxied Script Outside of OrangeBlox Instance.\033[0m")
try:
    if mod_style_json.get("advanced"): s = mod_mode_module.run(installed, fold_name, mod_style_json.get("advanced"), mod_style_json["angle"], studio=is_studio == True)
    else: s = mod_mode_module.run(installed, fold_name, mod_style_json["colors"], mod_style_json["angle"], studio=is_studio == True)
    if s: 
        shutil.copytree(s, os.path.join(current_path_location, "../", fold_name), dirs_exist_ok=True)
        with open(os.path.join(os.path.join(current_path_location, "../", fold_name), "Manifest.json"), "w", encoding="utf-8") as f:
            json.dump({
                "name": fold_name,
                "version": "1.0.0",
                "is_studio_mod": is_studio,
                "watermark": "Generated using Kliko Mod Generator."
            }, f, indent=4)
        shutil.rmtree(s, ignore_errors=True)
        print("\033[38;5;82mSuccessfully created as OrangeBlox mod!\033[0m")
except DeployHistoryError as e:
    print(f"\033[38;5;196mThere was an issue trying to find the studio version! It could be not available at this time!\033[0m")
    sys.exit(1)
except Exception as e:
    print(f"\033[38;5;196mUnable to update mods! Exception: {str(e)}\033[0m")
    sys.exit(1)