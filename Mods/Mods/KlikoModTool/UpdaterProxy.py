import importlib.util
import shutil
import os
import sys
import json
import PyKits
import traceback
from mod_updater.check_for_mod_updates import check_for_mod_updates
from mod_updater.exceptions import DeployHistoryError

cur_path = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("update", f"{cur_path}/mod_updater/update_mods.py")
mod_mode_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod_mode_module)
mods = json.loads(sys.argv[1])
is_studio = sys.argv[2]=="True"
studio_version = json.loads(sys.argv[3])
colors_class = PyKits.Colors()

def trace():
    _, tb_v, tb_b = sys.exc_info()
    tb_lines = traceback.extract_tb(tb_b)
    lines = []
    lines.append(colors_class.foreground("Traceback (most recent call last):", color="Magenta", bright=True))
    for fn, ln, f, tx in tb_lines:
        lines.append(f'  File {colors_class.foreground(fn, color="Magenta", bright=True)}, line {colors_class.foreground(ln, color="Magenta", bright=True)}, in {colors_class.foreground(f, color="Magenta", bright=True)}')
        if tx: lines.append(f'    {tx}')
    exc_t = type(tb_v).__name__
    exc_m = str(tb_v)
    lines.append(f'{colors_class.foreground(colors_class.bold(f"{exc_t}:"), color="Magenta", bright=True)} {colors_class.foreground(exc_m, color="Magenta", bright=False)}')
    return "\n".join(lines)

print("\033[38;5;226mProxied Script Outside of OrangeBlox Instance.\033[0m")
checked = check_for_mod_updates(os.path.join(cur_path, '../'), mods, studio_version["version"])
if checked:
    try: mod_mode_module.update_mods(checked, studio_version)
    except DeployHistoryError as e:
        print(f"\033[38;5;196mThere was an issue trying to find the studio version! It could be not available at this time!\033[0m")
        sys.exit(1)
    except Exception as e:
        print(f"\033[38;5;196mUnable to update mods! Exception: \n {trace()}\033[0m")
        sys.exit(1)
    for i in mods:
        if type(i) is str:
            i = os.path.basename(i)
            shutil.copytree(os.path.join(cur_path, "mod_updater", "result", i), os.path.join(cur_path, "../", i), dirs_exist_ok=True)
            with open(os.path.join(os.path.join(cur_path, "../", i), "Manifest.json"), "w", encoding="utf-8") as f:
                json.dump({
                    "name": i,
                    "version": "1.0.0",
                    "is_studio_mod": is_studio,
                    "watermark": "Generated using Kliko Mod Generator."
                }, f, indent=4)
            shutil.rmtree(os.path.join(cur_path, "mod_updater", "result", i), ignore_errors=True)
            print(f"\033[38;5;82mSuccessfully created {i} as OrangeBlox mod!\033[0m")