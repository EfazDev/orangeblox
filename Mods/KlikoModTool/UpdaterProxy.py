import importlib.util
import shutil
import os
import sys
import json

current_path_location = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("update", f"{current_path_location}/mod_updater/update_mods.py")
mod_mode_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod_mode_module)
mods = json.loads(sys.argv[1])
is_studio = sys.argv[2]=="True"
studio_version = json.loads(sys.argv[3])

print("\033[38;5;226mProxied Script Outside of OrangeBlox Instance.\033[0m")
from mod_updater.check_for_mod_updates import check_for_mod_updates
from mod_updater.exceptions import DeployHistoryError
checked = check_for_mod_updates(os.path.join(current_path_location, '../'), mods, studio_version["version"])
if checked:
    try:
        mod_mode_module.update_mods(checked, studio_version)
    except DeployHistoryError as e:
        print(f"\033[38;5;196mThere was an issue trying to find the studio version! It could be not available at this time!\033[0m")
        sys.exit(1)
    except Exception as e:
        print(f"\033[38;5;196mUnable to update mods! Exception: {str(e)}\033[0m")
        sys.exit(1)
    for i in mods:
        if type(i) is str:
            i = os.path.basename(i)
            shutil.copytree(os.path.join(current_path_location, "mod_updater", "result", i), os.path.join(current_path_location, "../", i), dirs_exist_ok=True)
            with open(os.path.join(os.path.join(current_path_location, "../", i), "Manifest.json"), "w", encoding="utf-8") as f:
                json.dump({
                    "name": i,
                    "version": "1.0.0",
                    "is_studio_mod": is_studio,
                    "watermark": "Generated using Kliko Mod Generator."
                }, f, indent=4)
            shutil.rmtree(os.path.join(current_path_location, "mod_updater", "result", i), ignore_errors=True)
            print(f"\033[38;5;82mSuccessfully created {i} as OrangeBlox mod!\033[0m")