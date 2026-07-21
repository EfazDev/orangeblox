# 
# OrangeBlox 🍊
# Made by Efaz from efaz.dev
# v2.6.0i
# 

import builtins
import OrangeAPI
import sys
import PyKits; PyKits.BuiltinEditor(builtins)
try: import RobloxManager as rbx
except Exception: print("Restarting for module updates.."); PyKits.pip().restartScript("Main.py", sys.argv)
import Modules.config as cf
from Modules.printing import *

try:
    pypresence = cf.pip_class.importModule("pypresence")
    psutil = cf.pip_class.importModule("psutil")
    truststore = cf.pip_class.importModule("truststore")
    if cf.main_os == "Darwin":
        posix_ipc = cf.pip_class.importModule("posix_ipc")
        objc = cf.pip_class.importModule("objc")
    elif cf.main_os == "Windows": 
        win32com = cf.pip_class.importModule("win32com")
        plyer = cf.pip_class.importModule("plyer")
except Exception:
    printSystemMessage("--- Installing Python Modules ---")
    pkg_list = ["pypresence", "psutil", "truststore"]
    if cf.main_os == "Darwin": pkg_list.extend(["posix-ipc", "pyobjc-core", "pyobjc-framework-Quartz"])
    elif cf.main_os == "Windows": pkg_list.extend(["pywin32", "plyer"])
    cf.pip_class.install(pkg_list)
    # cf.pip_class.restartScript("Main.py", sys.argv)
    printSuccessMessage("Successfully installed modules!")
try:
    import psutil
    from Modules.discord import Presence
    if cf.main_os == "Darwin": import objc
    elif cf.main_os == "Windows":
        import plyer # type: ignore
        import win32api # type: ignore
        import win32con # type: ignore
except (KeyboardInterrupt, Exception) as e:
    printErrorMessage("Uh oh! A Python exception that causes the script to end has occurred!")
    printErrorMessage(f"Exception: \n{trace()}")
    printErrorMessage(f"Location Code: 5")
    input("> ")
    sys.exit(0 if cf.main_os == "Darwin" else 1) 

if __name__ == "__main__":
    print("This module is not a runable instance.")
    sys.exit(1)