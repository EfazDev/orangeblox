import os
import platform
import shutil
import sys
import RobloxFastFlagsInstaller

def printMainMessage(mes): print(f"\033[38;5;255m{mes}\033[0m")
def printErrorMessage(mes): print(f"\033[38;5;196m{mes}\033[0m")
def printSuccessMessage(mes): print(f"\033[38;5;82m{mes}\033[0m")
def printWarnMessage(mes): print(f"\033[38;5;202m{mes}\033[0m")
def printYellowMessage(mes): print(f"\033[38;5;226m{mes}\033[0m")
def printDebugMessage(mes): print(f"\033[38;5;226m{mes}\033[0m")
def isYes(text): return text.lower() == "y" or text.lower() == "yes"
def isNo(text): return text.lower() == "n" or text.lower() == "no"
def isRequestClose(text): return text.lower() == "exit" or text.lower() == "exit()"

if __name__ == "__main__":
    main_os = platform.system()
    stored_main_app = {
        "Darwin": ["/Applications/EfazRobloxBootstrap.app", "/Applications/Play Roblox.app"],
        "Windows": [f"{os.getenv('LOCALAPPDATA')}\\EfazRobloxBootstrap", f"{os.getenv('LOCALAPPDATA')}\\EfazRobloxBootstrap\\EfazRobloxBootstrap.exe"]
    }
    current_version = {"version": "1.3.6"}
    handler = RobloxFastFlagsInstaller.Main()

    os.system("cls" if os.name == "nt" else 'echo "\033c\033[3J"; clear')
    printWarnMessage("-----------")
    printWarnMessage("Welcome to Efaz's Roblox Bootstrap Uninstaller!")
    printWarnMessage("Made by Efaz from efaz.dev!")
    printWarnMessage(f"v{current_version['version']}")
    printWarnMessage("-----------")
    if main_os == "Windows":
        printMainMessage(f"System OS: {main_os}")
        found_platform = "Windows"
    elif main_os == "Darwin":
        printMainMessage(f"System OS: {main_os} (macOS)")
        found_platform = "Darwin"
    else:
        printErrorMessage("Efaz's Roblox Bootstrap is only supported for macOS and Windows.")
        input("> ")
        sys.exit(0)
    current_python_version = platform.python_version_tuple()
    if current_python_version < ("3", "10", "0"):
        printErrorMessage("Please update your current installation of Python above 3.10.0")
        input("> ")
        sys.exit(0)
    else:
        printMainMessage(f"Python Version: {platform.python_version()}")
    if main_os == "Windows":
        installation_folder = f"{handler.getRobloxInstallFolder()}\\"
        if not os.path.exists(installation_folder):
            printMainMessage(f"Current Roblox Version: Not Installed")
        else:
            cur_vers = handler.getCurrentClientVersion()
            if cur_vers["success"] == True:
                printMainMessage(f"Current Roblox Version: {cur_vers['version']}")
            else:
                printErrorMessage("Something went wrong trying to determine your current Roblox version.")
                input("> ")
                sys.exit(0)
    elif main_os == "Darwin":
        if os.path.exists("/Applications/Roblox.app/"):
            cur_vers = handler.getCurrentClientVersion()
            if cur_vers["success"] == True:
                printMainMessage(f"Current Roblox Version: {cur_vers['version']}")
            else:
                printErrorMessage("Something went wrong trying to determine your current Roblox version.")
                input("> ")
                sys.exit(0)
        else:
            printMainMessage(f"Current Roblox Version: Not Installed")
    printWarnMessage("--- Uninstaller ---")
    if main_os == "Darwin":
        if not os.path.exists("/Applications/EfazRobloxBootstrap.app/Contents/MacOS/Efaz\'s Roblox Bootstrap.app/"):
            printMainMessage("Efaz's Roblox Bootstrap is not installed on this system.")
            input("> ")
            sys.exit(0)
    elif main_os == "Windows":
        if not os.path.exists(f"{os.getenv('LOCALAPPDATA')}\\EfazRobloxBootstrap\\"):
            printMainMessage("Efaz's Roblox Bootstrap is not installed on this system.")
            input("> ")
            sys.exit(0)
    printMainMessage("Are you sure you want to uninstall Efaz's Roblox Bootstrap from your system? (This will remove the app from your system and reinstall Roblox.) (y/n)")
    if isYes(input("> ")) == True:
        if main_os == "Darwin":
            # Remove Apps
            if os.path.exists(stored_main_app[found_platform][0]):
                printMainMessage("Removing from Applications Folder (Main Bootstrap)..")
                shutil.rmtree(stored_main_app[found_platform][0])
            if os.path.exists(stored_main_app[found_platform][1]):
                printMainMessage("Removing from Applications Folder (Play Roblox)..")
                shutil.rmtree(stored_main_app[found_platform][1])
        elif main_os == "Windows":
            # Remove URL Schemes
            printMainMessage("Resetting URL Schemes..")
            import winreg
            def set_url_scheme(protocol, exe_path):
                protocol_key = r"Software\Classes\{}".format("")
                command_key = r"Software\Classes\{}\shell\open\command".format(protocol)
                try:
                    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, protocol_key) as key:
                        winreg.SetValue(key, "", winreg.REG_SZ, "URL:{}".format(protocol))
                        winreg.SetValueEx(key, "URL Protocol", 0, winreg.REG_SZ, protocol)
                    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, command_key) as key:
                        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, '"{}" "%1"'.format(exe_path))
                    printSuccessMessage(f'URL scheme "{protocol}" has been set for "{exe_path}"')
                except Exception as e:
                    printErrorMessage(f"An error occurred: {e}")
            set_url_scheme("efaz-bootstrap", "")
            cur = handler.getCurrentClientVersion()
            if cur:
                if cur["success"] == True:
                    set_url_scheme("roblox-player", f"{os.getenv('LOCALAPPDATA')}\\Roblox\\Versions\\{cur['version']}\\RobloxPlayerBeta.exe")
                    set_url_scheme("roblox", f"{os.getenv('LOCALAPPDATA')}\\Roblox\\Versions\\{cur['version']}\\RobloxPlayerBeta.exe")
            
            # Remove Shortcuts
            printMainMessage("Removing shortcuts..")
            def remove_path(pat):
                if os.path.exists(pat): os.remove(pat)
            remove_path(os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), "Efaz's Roblox Bootstrap.lnk"))
            remove_path(os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs'), "Efaz's Roblox Bootstrap.lnk"))
            remove_path(os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), 'Play Roblox.lnk'))
            remove_path(os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs'), 'Play Roblox.lnk'))

            # Remove from Windows' Program List
            printMainMessage("Unmarking from Windows Program List..")
            app_key = r"Software\EfazRobloxBootstrap"
            uninstall_key = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\EfazRobloxBootstrap"
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, app_key, 0, winreg.KEY_WRITE) as key:
                    winreg.DeleteKey(winreg.HKEY_CURRENT_USER, app_key)
            except FileNotFoundError:
                printErrorMessage(f'Registry key "{app_key}" not found.')
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, uninstall_key, 0, winreg.KEY_WRITE) as key:
                    winreg.DeleteKey(winreg.HKEY_CURRENT_USER, uninstall_key)
            except FileNotFoundError:
                printErrorMessage(f'Registry key "{uninstall_key}" not found.')

            # Remove App
            if os.path.exists(stored_main_app[found_platform][0]):
                printMainMessage("Removing App Folder..")
                shutil.rmtree(stored_main_app[found_platform][0])
        printMainMessage("Preparing to reinstall Roblox..")
        handler.installRoblox(True, True)
        printSuccessMessage("Successfully uninstalled Efaz's Roblox Bootstrap and reinstalled Roblox!")
        input("> ")
    sys.exit(0)
else:
    class EfazRobloxBootstrapNotModule(Exception):
        def __init__(self):            
            super().__init__("Efaz's Roblox Bootstrap is only a runable instance, not a module.")
    class EfazRobloxBootstrapInstallerNotModule(Exception):
        def __init__(self):            
            super().__init__("The installer for Efaz's Roblox Bootstrap is only a runable instance, not a module.")
    class EfazRobloxBootstrapLoaderNotModule(Exception):
        def __init__(self):            
            super().__init__("The loader for Efaz's Roblox Bootstrap is only a runable instance, not a module.")
    raise EfazRobloxBootstrapInstallerNotModule()