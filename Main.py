# 
# OrangeBlox 🍊
# Made by Efaz from efaz.dev
# v2.6.0e
# 

# Python Modules
import sys
import Modules.config as cf
from Modules.printing import *
from Modules.utils import *
from Modules.startup import startUp
from Modules.menu import launch
from Modules.roblox import runRoblox

# Main Runtime
if __name__ == "__main__":
    try: 
        startUp() # Handle Configurations
        launch() # Main Menu
        if cf.avoid_going_to_roblox == False: runRoblox() # Run Roblox If Continued!
    except (KeyboardInterrupt, Exception) as e:
        printErrorMessage("Uh oh! A Python exception that causes the script to end has occurred!")
        printErrorMessage(f"Exception: \n{trace()}")
        printErrorMessage(f"Location Code: 0")
        input("> ")
        sys.exit(0 if cf.main_os == "Darwin" else 1)
else:
    # Detected as Module, Return with Exception
    class OrangeBloxNotModule(Exception): pass
    raise OrangeBloxNotModule("OrangeBlox is only a runable instance, not a module.")