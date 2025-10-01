import importlib.util
import shutil
import os
import sys
import json
import PyKits
import traceback
from mod_generator.exceptions import DeployHistoryError

cur_path = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("run", f"{cur_path}/mod_generator/run.py")
mod_mode_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod_mode_module)
installed = json.loads(sys.argv[1])
mod_style_json = json.loads(sys.argv[2])
is_studio = sys.argv[3]=="True"
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

fold_name = mod_style_json["name"]
if is_studio == True: fold_name = f'{mod_style_json["name"]} [STUDIO]'
print("\033[38;5;226mProxied Script Outside of OrangeBlox Instance.\033[0m")
try:
    if mod_style_json.get("advanced"): s = mod_mode_module.run(installed, fold_name, mod_style_json.get("advanced"), mod_style_json["angle"], studio=is_studio == True)
    else: s = mod_mode_module.run(installed, fold_name, mod_style_json["colors"], mod_style_json["angle"], studio=is_studio == True)
    if s: 
        shutil.copytree(s, os.path.join(cur_path, "../", fold_name), dirs_exist_ok=True)
        with open(os.path.join(os.path.join(cur_path, "../", fold_name), "Manifest.json"), "w", encoding="utf-8") as f:
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
    print(f"\033[38;5;196mUnable to update mods! Exception: \n {trace()}\033[0m")
    sys.exit(1)