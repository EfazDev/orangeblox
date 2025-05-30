# 
# OrangeBlox Installer 🍊
# Made by Efaz from efaz.dev
# v2.0.3
# 

# Modules
import subprocess
import platform
import datetime
import hashlib
import shutil
import time
import stat
import json
import zlib
import sys
import os

import RobloxFastFlagsInstaller
import PipHandler

def printMainMessage(mes): print(f"\033[38;5;255m{mes}\033[0m")
def printErrorMessage(mes): print(f"\033[38;5;196m{mes}\033[0m")
def printSuccessMessage(mes): print(f"\033[38;5;82m{mes}\033[0m")
def printWarnMessage(mes): print(f"\033[38;5;202m{mes}\033[0m")
def printYellowMessage(mes): print(f"\033[38;5;226m{mes}\033[0m")
def printDebugMessage(mes): print(f"\033[38;5;226m{mes}\033[0m")

def isYes(text): return text.lower() == "y" or text.lower() == "yes" or text.lower() == "true" or text.lower() == "t"
def isNo(text): return text.lower() == "n" or text.lower() == "no" or text.lower() == "false" or text.lower() == "f"
def isRequestClose(text): return text.lower() == "exit" or text.lower() == "exit()"
def is_x86_windows(): return platform.system() == "Windows" and platform.architecture()[0] == "32bit"
def makedirs(a): os.makedirs(a,exist_ok=True)
def copy_with_symlinks(src, dest, ignore_files=[]):
    if os.path.exists(src):
        try:
            for i in ignore_files:
                if i in src:
                    return
            if os.path.lexists(dest):
                if os.path.isdir(dest) and not os.path.islink(dest):
                    pass
                else:
                    os.remove(dest)
            if os.path.islink(src):
                os.symlink(os.readlink(src), dest)
            elif os.path.isdir(src):
                makedirs(dest)
                for item in os.listdir(src):
                    if item in ignore_files:
                        continue
                    copy_with_symlinks(os.path.join(src, item), os.path.join(dest, item))
                os.chmod(dest, os.stat(src).st_mode)
                os.chmod(dest, os.stat(dest).st_mode | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)
            else:
                shutil.copy(src, dest)
                os.chmod(dest, os.stat(src).st_mode)
                os.chmod(dest, os.stat(dest).st_mode | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)
        except Exception as e:
            printDebugMessage(f"An error occurred while transferring a file, a reinstallation may be needed: {str(e)}")
def getOriginalInstalledAppPath():
    if main_os == "Darwin":
        macos_preference_expected = os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.robloxbootstrap.plist")
        if os.path.exists(macos_preference_expected):
            plist_info = PipHandler.plist().readPListFile(macos_preference_expected)
            if plist_info:
                return plist_info.get("InstalledAppPath", None), None
            else:
                return None, None
        else:
            return None, None
    elif main_os == "Windows":
        import winreg as reg
        try:
            reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"SOFTWARE\\EfazRobloxBootstrap")
            value_data, reg_type = reg.QueryValueEx(reg_key, "InstalledAppPath")
            reg.CloseKey(reg_key)
            if value_data and type(value_data) is str:
                return value_data, pip_class.getLocalAppData()
            else:
                return None, None
        except Exception as e:
            return None, None
def getSettings(directory=""):
    if main_os == "Darwin":
        if os.path.exists(os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.robloxbootstrap.plist")): os.remove(os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.robloxbootstrap.plist"))
        macos_preference_expected = os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.orangeblox.plist")
        if os.path.exists(macos_preference_expected):
            app_configuration = PipHandler.plist().readPListFile(macos_preference_expected)
            if app_configuration.get("Configuration"):
                main_config = app_configuration.get("Configuration")
            else:
                main_config = {}
        else:
            main_config = {}
        return main_config
    else:
        with open(directory, "rb") as f: obfuscated_json = f.read()
        try: obfuscated_json = json.loads(obfuscated_json)
        except Exception as e: obfuscated_json = json.loads(zlib.decompress(obfuscated_json).decode("utf-8"))
        return obfuscated_json
def saveSettings(main_config, directory=""):
    respo = {
        "saved_normally": False,
        "sync_failed": False,
        "sync_success": False
    }
    if not (main_config.get("EFlagDisableAutosaveToInstallation") == True) and (main_config.get("EFlagOrangeBloxSyncDir") and os.path.exists(main_config.get("EFlagOrangeBloxSyncDir"))):
        if os.path.exists(os.path.join(main_config.get("EFlagOrangeBloxSyncDir"), 'FastFlagConfiguration.json')):
            with open(os.path.join(main_config.get("EFlagOrangeBloxSyncDir"), 'FastFlagConfiguration.json'), "w", encoding="utf-8") as f:
                json.dump(main_config, f, indent=4)
            respo["sync_success"] = True
        elif os.path.exists(os.path.join(main_config.get("EFlagOrangeBloxSyncDir"), 'Configuration.json')):
            with open(os.path.join(main_config.get("EFlagOrangeBloxSyncDir"), 'Configuration.json'), "w", encoding="utf-8") as f:
                json.dump(main_config, f, indent=4)
            respo["sync_success"] = True
        else:
            printErrorMessage("Bootstrap Sync is not supported since the original unextracted directory is not found.")
            respo["sync_failed"] = True
    if main_os == "Darwin":
        if os.path.exists(os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.robloxbootstrap.plist")): os.remove(os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.robloxbootstrap.plist"))
        macos_preference_expected = os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.orangeblox.plist")
        if os.path.exists(macos_preference_expected):
            app_configuration = PipHandler.plist().readPListFile(macos_preference_expected)
        else:
            app_configuration = {}
        app_configuration["Configuration"] = main_config
        PipHandler.plist().writePListFile(macos_preference_expected, app_configuration, binary=True)
    else:
        data_in_string = zlib.compress(json.dumps(main_config).encode('utf-8'))
        with open(directory, "wb") as f: f.write(data_in_string)
    respo["saved_normally"] = True
    return respo
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
def getInstalledAppPath():
    if main_os == "Darwin":
        macos_preference_expected = os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.orangeblox.plist")
        if os.path.exists(macos_preference_expected):
            plist_info = PipHandler.plist().readPListFile(macos_preference_expected)
            if plist_info:
                return plist_info.get("InstalledAppPath", "/Applications/"), "/Applications/"
            else:
                return "/Applications/", "/Applications/"
        else:
            return "/Applications/", "/Applications/"
    elif main_os == "Windows":
        import winreg as reg
        try:
            reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"SOFTWARE\\OrangeBlox")
            value_data, reg_type = reg.QueryValueEx(reg_key, "InstalledAppPath")
            reg.CloseKey(reg_key)
            if value_data and type(value_data) is str:
                if os.path.exists(os.path.join(value_data, "OrangeBlox")):
                    return os.path.join(value_data, "OrangeBlox"), pip_class.getLocalAppData()
                else:
                    return value_data, pip_class.getLocalAppData()
            else:
                return pip_class.getLocalAppData(), pip_class.getLocalAppData()
        except Exception as e:
            return pip_class.getLocalAppData(), pip_class.getLocalAppData()
def setInstalledAppPath(install_app_path):
    if main_os == "Darwin":
        if os.path.exists(os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.robloxbootstrap.plist")): os.remove(os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.robloxbootstrap.plist"))
        macos_preference_expected = os.path.join(os.path.expanduser("~"), "Library", "Preferences", "dev.efaz.orangeblox.plist")
        plist_info = {}
        if os.path.exists(macos_preference_expected):
            plist_info = PipHandler.plist().readPListFile(macos_preference_expected)
        plist_info["InstalledAppPath"] = install_app_path
        PipHandler.plist().writePListFile(macos_preference_expected, plist_info, binary=True)
    elif main_os == "Windows":
        import winreg as reg
        app_key = r"Software\EfazRobloxBootstrap"
        uninstall_key = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\EfazRobloxBootstrap"
        try:
            with reg.OpenKey(reg.HKEY_CURRENT_USER, uninstall_key, 0, reg.KEY_WRITE) as key:
                reg.DeleteKey(reg.HKEY_CURRENT_USER, uninstall_key)
            with reg.OpenKey(reg.HKEY_CURRENT_USER, app_key, 0, reg.KEY_WRITE) as key:
                reg.DeleteKey(reg.HKEY_CURRENT_USER, app_key)
        except Exception:
            platform.system()
        try:
            reg_key = reg.CreateKey(reg.HKEY_CURRENT_USER, r"SOFTWARE\\OrangeBlox")
            reg.SetValueEx(reg_key, "InstalledAppPath", 0, reg.REG_SZ, install_app_path)
            reg.CloseKey(reg_key)
        except Exception as e:
            printErrorMessage("There was an error saving the assigned installed path!")
def getFolderSize(folder_path, formatWithAbbreviation=True):
    total_size = 0
    stack = [folder_path]
    while stack:
        current = stack.pop()
        try:
            with os.scandir(current) as it:
                for entry in it:
                    try:
                        if entry.is_file(follow_symlinks=False): total_size += entry.stat(follow_symlinks=False).st_size
                        elif entry.is_dir(follow_symlinks=False): stack.append(entry.path)
                    except Exception:
                        pass
        except Exception:
            pass
    def formatSize(size_bytes):
        if size_bytes == 0:
            return "0 Bytes"
        
        size_units = ["Bytes", "KB", "MB", "GB", "TB"]
        unit_index = 0
        
        while size_bytes >= 1024 and unit_index < len(size_units) - 1:
            size_bytes /= 1024
            unit_index += 1
        
        return f"{size_bytes:.2f} {size_units[unit_index]}"
    if formatWithAbbreviation == True:
        return formatSize(total_size)
    else:
        return total_size
def convertPythonExecutablesInFileToPaths(path: str, python_instance: PipHandler.pip):
    splits = os.path.basename(path).split(".")
    with open(path, "r", encoding="utf-8") as f: fi = f.read()
    if main_os == "Darwin":
        fi = fi.replace("pyinstaller ", f'\"{os.path.join(os.path.dirname(python_instance.executable), "pyinstaller")}\" ')
        fi = fi.replace("nuitka ", f'\"{os.path.join(os.path.dirname(python_instance.executable), "nuitka")}\" ')
        fi = fi.replace("python3 ", f'\"{python_instance.executable}\" ')
    else:
        pos = os.path.join(pip_class.getLocalAppData(), "../", "Roaming", "Python", os.path.basename(os.path.dirname(python_instance.executable)))
        if os.path.exists(pos):
            fi = fi.replace("pyinstaller ", f'\"{os.path.join(pos, "Scripts", "pyinstaller.exe")}\" ')
            fi = fi.replace("nuitka ", f'\"{os.path.join(pos, "Scripts", "nuitka.exe")}\" ')
        else:
            fi = fi.replace("pyinstaller ", f'\"{os.path.join(os.path.dirname(python_instance.executable), "Scripts", "pyinstaller.exe")}\" ')
            fi = fi.replace("nuitka ", f'\"{os.path.join(os.path.dirname(python_instance.executable), "Scripts", "nuitka.exe")}\" ')
        fi = fi.replace("py ", f'\"{os.path.join(os.path.dirname(python_instance.executable), "python.exe")}\" ')
    tar = os.path.join(os.path.dirname(path), f'{splits[0]}Converted.{splits[1]}')
    with open(tar, "w", encoding="utf-8") as f: f.write(fi)
    return tar
def waitForInternet():
    if pip_class.getIfConnectedToInternet() == False:
        printWarnMessage("--- Waiting for Internet ---")
        printMainMessage("Please connect to your internet in order to continue! If you're connecting to a VPN, try reconnecting.")
        while pip_class.getIfConnectedToInternet() == False:
            time.sleep(0.05)
        return True
    
if __name__ == "__main__":
    main_os = platform.system()
    pip_class = PipHandler.pip()
    stored_main_app = {
        "OverallInstall": main_os == "Darwin" and "/Applications/" or f"{pip_class.getLocalAppData()}",
        "Darwin": [
            "/Applications/OrangeBlox.app/Contents/MacOS/OrangeBlox.app", 
            "/Applications/OrangeBlox.app", 
            "/Applications/Play Roblox.app", 
            "/Applications/Run Studio.app"
        ],
        "Windows": [
            os.path.join(f"{pip_class.getLocalAppData()}", "OrangeBlox"), 
            os.path.join(f"{pip_class.getLocalAppData()}", "OrangeBlox", "OrangeBlox.exe"), 
            os.path.join(f"{pip_class.getLocalAppData()}", "OrangeBlox"), 
            os.path.join(f"{pip_class.getLocalAppData()}", "OrangeBlox")
        ]
    }
    ignore_files = [
        "dist", 
        ".git",
        "build",
        "CNAME", 
        ".github",
        "LICENSE", 
        "README.md",
        "RepairData", 
        "__pycache__", 
        "InstallPython.sh", 
        "InstallPython.bat",
        "Configuration.json", 
        "RobloxFastFlagLogFilesAttached.json"
    ]
    current_version = {"version": "2.0.3"}
    current_path_location = os.path.dirname(os.path.abspath(__file__))
    rebuild_target = []
    repair_mode = False
    silent_mode = False
    update_mode = False
    backup_mode = False
    rebuild_mode = False
    uninstall_mode = False
    instant_install = False
    use_x86_windows = False
    repair_argv_mode = False
    full_rebuild_mode = False
    rebuild_from_source = None
    use_sudo_for_codesign = False
    use_installation_syncing = True
    disable_download_for_app = True
    remove_unneeded_messages = True
    rebuild_from_source_clang = False
    disabled_shortcuts_installation = None
    disabled_url_scheme_installation = None
    disable_remove_other_operating_systems = False

    handler = RobloxFastFlagsInstaller.Main()
    def ignore_files_func(dir, files): return set(ignore_files) & set(files)

    if "--rebuild-mode" in sys.argv:
        rebuild_mode = True
        disable_remove_other_operating_systems = True
        instant_install = True
    elif "--update-mode" in sys.argv:
        silent_mode = True
        instant_install = True
        disable_remove_other_operating_systems = True
        update_mode = True
    else:
        if "--install" in sys.argv: instant_install = True
        if "--silent" in sys.argv:
            silent_mode = True
            def printMainMessage(mes): silent_mode = True
            def printErrorMessage(mes): print(f"\033[38;5;196m{mes}\033[0m")
            def printSuccessMessage(mes): silent_mode = True
            def printWarnMessage(mes): silent_mode = True
            def printDebugMessage(mes): silent_mode = True
        else:
            if not ("--no-clear" in sys.argv): os.system("cls" if os.name == "nt" else 'echo "\033c\033[3J"; clear')
        if "--disable-remove" in sys.argv: disable_remove_other_operating_systems = True
    if "--disable-installation-sync" in sys.argv: use_installation_syncing = False
    if "--enable-unneeded-messages" in sys.argv: remove_unneeded_messages = False
    if "--disable-url-schemes" in sys.argv: disabled_url_scheme_installation = True
    if "--disable-shortcuts" in sys.argv: disabled_shortcuts_installation = True
    if "--rebuild-pyinstaller" in sys.argv: rebuild_from_source = 1
    if "--rebuild-nuitka" in sys.argv: rebuild_from_source = 2
    if "--full-rebuild" in sys.argv: full_rebuild_mode = True
    if "--uninstall-mode" in sys.argv: uninstall_mode = True
    if "--repair-mode" in sys.argv: repair_argv_mode = True
    if "--backup-mode" in sys.argv: backup_mode = True
    if "--use-sudo-for-codesign" in sys.argv: use_sudo_for_codesign = True
    if "--rebuild-clang" in sys.argv: rebuild_from_source_clang = True
    if "--use-x86-windows" in sys.argv: use_x86_windows = True

    expected_app_path, default_app_path = getInstalledAppPath()
    expected_app_paths = {}
    org_expected_app_path, org_default_app_path = getOriginalInstalledAppPath()
    if org_expected_app_path:
        expected_app_paths["OverallInstall"] = org_expected_app_path
        if main_os == "Darwin":
            expected_app_paths["Darwin"] = [
                os.path.join(org_expected_app_path, "OrangeBlox.app/Contents/MacOS/OrangeBlox.app"), 
                os.path.join(org_expected_app_path, "OrangeBlox.app"), 
                os.path.join(org_expected_app_path, "Play Roblox.app"), 
                os.path.join(org_expected_app_path, "Run Studio.app")
            ]
        elif main_os == "Windows":
            expected_app_paths["Windows"] = [
                os.path.join(org_expected_app_path), 
                os.path.join(org_expected_app_path, "OrangeBlox.exe"), 
                os.path.join(org_expected_app_path), 
                os.path.join(org_expected_app_path)
            ]
    else:
        if expected_app_path:
            expected_app_paths["OverallInstall"] = expected_app_path
            if main_os == "Darwin":
                expected_app_paths["Darwin"] = [
                    os.path.join(expected_app_path, "OrangeBlox.app/Contents/MacOS/OrangeBlox.app"), 
                    os.path.join(expected_app_path, "OrangeBlox.app"), 
                    os.path.join(expected_app_path, "Play Roblox.app"), 
                    os.path.join(expected_app_path, "Run Studio.app")
                ]
            elif main_os == "Windows":
                expected_app_paths["Windows"] = [
                    os.path.join(expected_app_path), 
                    os.path.join(expected_app_path, "OrangeBlox.exe"), 
                    os.path.join(expected_app_path), 
                    os.path.join(expected_app_path)
                ]
        else:
            expected_app_paths = stored_main_app

    printWarnMessage("-----------")
    printWarnMessage("Welcome to OrangeBlox Installer 🍊!")
    printWarnMessage("Made by Efaz from efaz.dev!")
    printWarnMessage(f"v{current_version['version']}")
    printWarnMessage("-----------")
    # Requirement Checks
    if waitForInternet() == True: printWarnMessage("-----------")
    if main_os == "Windows":
        printMainMessage(f"System OS: {main_os} ({platform.version()})")
        found_platform = "Windows"
    elif main_os == "Darwin":
        printMainMessage(f"System OS: {main_os} (macOS {platform.mac_ver()[0]})")
        found_platform = "Darwin"
    else:
        printErrorMessage("OrangeBlox is only supported for macOS and Windows.")
        input("> ")
        sys.exit(0)
    if not pip_class.osSupported(windows_build=17134, macos_version=(10,13,0)):
        if main_os == "Windows": printErrorMessage("OrangeBlox is only supported for Windows 10.0.17134 (April 2018) or higher. Please update your operating system in order to continue!")
        elif main_os == "Darwin": printErrorMessage("OrangeBlox is only supported for macOS 10.13 (High Sierra) or higher. Please update your operating system in order to continue!")
        input("> ")
        sys.exit(0)
    printMainMessage(f"Python Version: {pip_class.getCurrentPythonVersion()}{pip_class.getIfPythonVersionIsBeta() and ' (BETA)' or ''}")
    if not pip_class.pythonSupported(3, 11, 0):
        if not pip_class.pythonSupported(3, 6, 0):
            printErrorMessage("Please update your current installation of Python above 3.11.0")
            input("> ")
            sys.exit(0)
        else:
            latest_python = pip_class.getLatestPythonVersion()
            printWarnMessage("--- Python Update Required ---")
            printMainMessage("Hello! In order to use OrangeBlox, you'll need to install Python 3.11 or higher in order to continue. ")
            printMainMessage(f"If you wish, you may install Python {latest_python} by typing \"y\" and continue.")
            printMainMessage("Otherwise, you may close the app by just continuing without typing.")
            if isYes(input("> ")) == True:
                pip_class.pythonInstall(latest_python)
                printSuccessMessage(f"If installed correctly, Python {latest_python} should be available to be used!")
                printSuccessMessage("Please restart the script to install!")
                input("> ")
            sys.exit(0)
    if expected_app_path and (main_os == "Darwin" and os.path.exists(os.path.join(expected_app_paths[found_platform][1], "Contents", "Resources", "Versions")) or os.path.exists(os.path.join(expected_app_paths[found_platform][1], "Versions"))):
        versions_folder = os.path.join(expected_app_paths[found_platform][1], "Versions")
        if main_os == "Darwin": versions_folder = os.path.join(expected_app_paths[found_platform][1], "Contents", "Resources", "Versions")
        main_config = getSettings(directory=os.path.join(expected_app_paths[found_platform][1], "FastFlagConfiguration.json"))
        RobloxFastFlagsInstaller.windows_versions_dir = versions_folder
        RobloxFastFlagsInstaller.windows_player_folder_name = main_config.get("EFlagBootstrapRobloxInstallFolderName", "com.roblox.robloxplayer")
        RobloxFastFlagsInstaller.windows_studio_folder_name = main_config.get("EFlagBootstrapRobloxStudioInstallFolderName", "com.roblox.robloxstudio")
        if main_config.get("EFlagPreventRobloxMacOSAppOverlapping", False) == True:
            user_folder_name = os.path.basename(os.path.expanduser("~"))
            versions_folder = os.path.join(versions_folder, user_folder_name)
            RobloxFastFlagsInstaller.macOS_dir = os.path.join(versions_folder, "Roblox.app")
            RobloxFastFlagsInstaller.macOS_studioDir = os.path.join(versions_folder, "Roblox Studio.app")
            RobloxFastFlagsInstaller.macOS_installedPath = os.path.join(versions_folder)
        else:
            RobloxFastFlagsInstaller.macOS_dir = os.path.join(versions_folder, "Roblox.app")
            RobloxFastFlagsInstaller.macOS_studioDir = os.path.join(versions_folder, "Roblox Studio.app")
            RobloxFastFlagsInstaller.macOS_installedPath = os.path.join(versions_folder)
        installed_roblox_version = handler.getCurrentClientVersion()
        if installed_roblox_version["success"] == True:
            installed_roblox_studio_version = handler.getCurrentStudioClientVersion()
            if installed_roblox_studio_version["success"] == True:
                if installed_roblox_studio_version['version'] == installed_roblox_version['version']:
                    printMainMessage(f"Current Roblox & Roblox Studio Version: {installed_roblox_version['version']}")
                else:
                    printMainMessage(f"Current Roblox Version: {installed_roblox_version['version']}")
                    printMainMessage(f"Current Roblox Studio Version: {installed_roblox_studio_version['version']}")
            else:
                printMainMessage(f"Current Roblox Version: {installed_roblox_version['version']}")
        else:
            printErrorMessage("Something went wrong trying to determine your current Roblox version.")
            input("> ")
            sys.exit(0)
    printMainMessage(f"Installation Folder: {current_path_location}")
    overwrited = False

    if os.path.exists(expected_app_paths[found_platform][0]) and os.path.exists(expected_app_paths[found_platform][1]):
        overwrited = True
        stored_main_app = expected_app_paths
    elif os.path.exists(os.path.join(expected_app_paths["OverallInstall"], "EfazRobloxBootstrap")) or os.path.exists(os.path.join(expected_app_paths["OverallInstall"], "EfazRobloxBootstrap.app")):
        overwrited = True
        stored_main_app = expected_app_paths
    def install():
        global disabled_url_scheme_installation
        global use_x86_windows
        global rebuild_from_source
        global rebuild_from_source_clang
        global disable_remove_other_operating_systems
        global disabled_shortcuts_installation
        global disable_download_for_app
        global use_installation_syncing
        global rebuild_target
        started_build_time = datetime.datetime.now().timestamp()

        try:
            requests = pip_class.importModule("requests")
            plyer = pip_class.importModule("plyer")
            pypresence = pip_class.importModule("pypresence")
            tkinter = pip_class.importModule("tkinter")
            if main_os == "Darwin":
                posix_ipc = pip_class.importModule("posix_ipc")
                objc = pip_class.importModule("objc")
            elif main_os == "Windows":
                win32com = pip_class.importModule("win32com")
            if rebuild_from_source == 1: rebuild_target = ["pyinstaller"]
            if rebuild_from_source == 2: rebuild_target = ["Nuitka"]
            if len(rebuild_target) > 0 and not pip_class.installed(rebuild_target, boolonly=True): raise Exception(f"Please install {rebuild_target[0]} for this mode!")
        except Exception as e:
            if not instant_install == True: printMainMessage("Modules from the internet are needed to be installed in order to use OrangeBlox. Do you want to install them now? (y/n)")
            if instant_install == True or isYes(input("> ")) == True:
                if rebuild_from_source == 1: rebuild_target = ["pyinstaller"]
                if rebuild_from_source == 2: rebuild_target = ["Nuitka"]
                pip_class.install(["requests", "plyer", "pypresence", "tk"] + rebuild_target)
                if main_os == "Darwin": pip_class.install(["posix-ipc", "pyobjc-core", "pyobjc-framework-Quartz", "pyobjc-framework-Cocoa"])
                elif main_os == "Windows": pip_class.install(["pywin32"])
                pip_class.restartScript("Install.py", sys.argv)
                printSuccessMessage("Successfully installed modules!")
            else:
                printErrorMessage("Ending installation..")
                sys.exit(0)

        if os.path.exists(os.path.join(current_path_location, "Apps")):
            if main_os == "Darwin":
                # Get FastFlagConfiguration.json Data
                if overwrited == True:
                    printMainMessage("Getting Configuration File Data..")
                    fast_config_path = os.path.join(stored_main_app[found_platform][1], "Contents", "Resources", "FastFlagConfiguration.json")
                    if os.path.exists(os.path.join(stored_main_app["OverallInstall"], "EfazRobloxBootstrap.app")):
                        fast_config_path = os.path.join(stored_main_app["OverallInstall"], "EfazRobloxBootstrap.app", "Contents", "Resources", "FastFlagConfiguration.json")
                    if os.path.exists(fast_config_path):
                        with open(fast_config_path, "r", encoding="utf-8") as f:
                            main_config = json.load(f)
                    else:
                        main_config = getSettings(directory=fast_config_path)
                else:
                    main_config = {}
                    if os.path.exists(os.path.join(current_path_location, "FastFlagConfiguration.json")):
                        with open(os.path.join(current_path_location, "FastFlagConfiguration.json"), "r", encoding="utf-8") as f:
                            main_config = json.load(f)

                # Adapt Fast Flags from Efaz's Roblox Bootstrap
                if not main_config.get("EFlagRobloxPlayerFlags"):
                    printMainMessage("Converting Fast Flags..")
                    player_flags = {}
                    for i, v in main_config.items():
                        if not i.startswith("EFlag"):
                            player_flags[i] = v
                    for i, v in player_flags.items():
                        main_config.pop(i)
                    main_config["EFlagRobloxPlayerFlags"] = player_flags
                    main_config["EFlagRobloxStudioFlags"] = {}

                # Rebuild Clang Apps from Source
                if rebuild_from_source_clang == True or (main_config.get("EFlagRebuildClangAppFromSourceDuringUpdates") == True and update_mode == True):
                    printMainMessage("Running Clang++ Rebuild..")
                    extra_detail = " nosudo"
                    if use_sudo_for_codesign == True: extra_detail = ""
                    if os.path.exists(os.path.join(current_path_location, "SigningCertificateName")): 
                        with open(os.path.join(current_path_location, "SigningCertificateName")) as f: extra_detail = extra_detail + " '" + f.read() + "'"
                    pa = convertPythonExecutablesInFileToPaths(os.path.join(current_path_location, 'Apps', 'Scripts', 'Clang', 'MakeLoadersMac.sh') if platform.machine() == "arm64" else os.path.join(current_path_location, 'Apps', 'Scripts', 'Clang', 'MakeLoadersMacIntel.sh'), pip_class)
                    rebuild_status = subprocess.run(f"sh {pa} installer" + extra_detail, shell=True, cwd=current_path_location)
                    if rebuild_status.returncode == 0:
                        printSuccessMessage(f"Rebuilding Clang App succeeded! Continuing to installation..")
                        os.remove(pa)
                    else:
                        printErrorMessage(f"Rebuild failed! Status code: {rebuild_status.returncode}")
                        os.remove(pa)
                        return

                # Rebuild Pyinstaller & Nuitka Apps
                if rebuild_from_source == 1 or (main_config.get("EFlagRebuildPyinstallerAppFromSourceDuringUpdates") == True and update_mode == True):
                    extra_detail = " nosudo"
                    if use_sudo_for_codesign == True: extra_detail = ""
                    if os.path.exists(os.path.join(current_path_location, "SigningCertificateName")): 
                        with open(os.path.join(current_path_location, "SigningCertificateName")) as f: extra_detail = extra_detail + " '" + f.read() + "'"
                    printMainMessage("Running Pyinstaller Rebuild..")
                    pa = convertPythonExecutablesInFileToPaths(os.path.join(current_path_location, 'Apps', 'Scripts', 'Pyinstaller', 'RecreateMacOS.sh') if platform.machine() == "arm64" else os.path.join(current_path_location, 'Apps', 'Scripts', 'Pyinstaller', 'RecreateMacOSIntel.sh'), pip_class)
                    rebuild_status = subprocess.run(f"sh {pa} installer" + extra_detail, shell=True, cwd=current_path_location)
                    if rebuild_status.returncode == 0:
                        printSuccessMessage(f"Rebuilding Pyinstaller App succeeded! Continuing to installation..")
                        os.remove(pa)
                    else:
                        printErrorMessage(f"Rebuild failed! Status code: {rebuild_status.returncode}")
                        os.remove(pa)
                        return
                    if full_rebuild_mode == True and platform.machine() == "arm64":
                        printMainMessage("Running Intel Pyinstaller Rebuild..")
                        pa = convertPythonExecutablesInFileToPaths(os.path.join(current_path_location, 'Apps', 'Scripts', 'Pyinstaller', 'RecreateMacOSIntel.sh'), pip_class)
                        rebuild_status = subprocess.run(f"sh {pa} installer" + extra_detail, shell=True, cwd=current_path_location)
                        if rebuild_status.returncode == 0:
                            printSuccessMessage(f"Rebuilding Intel Pyinstaller App succeeded! Continuing to installation..")
                        else:
                            printErrorMessage(f"Rebuild failed! Status code: {rebuild_status.returncode}")
                        os.remove(pa)
                elif rebuild_from_source == 2 or (main_config.get("EFlagRebuildNuitkaAppFromSourceDuringUpdates") == True and update_mode == True):
                    extra_detail = " nosudo"
                    if use_sudo_for_codesign == True: extra_detail = ""
                    if os.path.exists(os.path.join(current_path_location, "SigningCertificateName")): 
                        with open(os.path.join(current_path_location, "SigningCertificateName")) as f: extra_detail = extra_detail + " '" + f.read() + "'"
                    printMainMessage("Running Nuitka Rebuild..")
                    pa = convertPythonExecutablesInFileToPaths(os.path.join(current_path_location, 'Apps', 'Scripts', 'Nuitka', 'RecreateMacOS.sh') if platform.machine() == "arm64" else os.path.join(current_path_location, 'Apps', 'Scripts', 'Pyinstaller', 'RecreateMacOSIntel.sh'), pip_class)
                    rebuild_status = subprocess.run(f"sh {pa} installer" + extra_detail, shell=True, cwd=current_path_location)
                    if rebuild_status.returncode == 0:
                        printSuccessMessage(f"Rebuilding Nuitka App succeeded! Continuing to installation..")
                        os.remove(pa)
                    else:
                        printErrorMessage(f"Rebuild failed! Status code: {rebuild_status.returncode}")
                        os.remove(pa)
                        return
                    if full_rebuild_mode == True and platform.machine() == "arm64":
                        printMainMessage("Running Intel Nuitka Rebuild..")
                        pa = convertPythonExecutablesInFileToPaths(os.path.join(current_path_location, 'Apps', 'Scripts', 'Nuitka', 'RecreateMacOSIntel.sh'), pip_class)
                        rebuild_status = subprocess.run(f"sh {pa} installer" + extra_detail, shell=True, cwd=current_path_location)
                        if rebuild_status.returncode == 0:
                            printSuccessMessage(f"Rebuilding Intel Nuitka App succeeded! Continuing to installation..")
                        else:
                            printErrorMessage(f"Rebuild failed! Status code: {rebuild_status.returncode}")
                        os.remove(pa)

                if platform.machine() == "arm64":
                    if os.path.exists(os.path.join(current_path_location, "Apps", "OrangeBloxMac.zip")):
                        # Unzip Installation ZIP
                        printMainMessage("Unzipping Installation ZIP File..")
                        try:
                            makedirs(os.path.join(current_path_location, "Apps", "OrangeBloxMac"))
                            subprocess.run(["unzip", "-o", os.path.join(current_path_location, "Apps", "OrangeBloxMac.zip"), "-d", os.path.join(current_path_location, "Apps", "OrangeBloxMac")], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                        except Exception as e:
                            printErrorMessage(f"Something went wrong while trying to unzip macOS apps file: {str(e)}")
                        time.sleep(1)
                    else:
                        printYellowMessage("Something went wrong finding OrangeBloxMac.zip. It will require a OrangeBloxMac folder in order for installation to finish.")
                else:
                    if os.path.exists(os.path.join(current_path_location, "Apps", "OrangeBloxMacIntel.zip")):
                        # Unzip Installation ZIP
                        printMainMessage("Unzipping Installation ZIP File..")
                        try:
                            makedirs(os.path.join(current_path_location, "Apps", "OrangeBloxMac"))
                            subprocess.run(["unzip", "-o", os.path.join(current_path_location, "Apps", "OrangeBloxMacIntel.zip"), "-d", os.path.join(current_path_location, "Apps", "OrangeBloxMac")], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                        except Exception as e:
                            printErrorMessage(f"Something went wrong while trying to unzip macOS apps file: {str(e)}")
                        time.sleep(1)
                    else:
                        printYellowMessage("Something went wrong finding OrangeBloxMacIntel.zip. It will require a OrangeBloxMac folder in order for installation to finish.")
                if os.path.exists(os.path.join(current_path_location, "Apps", "OrangeBloxMac")):
                    # Delete Other Operating System Files
                    if not (disable_remove_other_operating_systems == True or main_config.get("EFlagDisableDeleteOtherOSApps") == True):
                        deleted_other_os = False
                        if os.path.exists(os.path.join(current_path_location, "Apps", "OrangeBloxWindows.zip")):
                            os.remove(os.path.join(current_path_location, "Apps", "OrangeBloxWindows.zip"))
                            deleted_other_os = True
                        if deleted_other_os == True: printMainMessage("To help save space, the script has automatically deleted files made for other operating systems!")

                    # Remove Old Versions of Loader
                    if os.path.exists(f"/Applications/EfazRobloxBootstrapLoader.app/"):
                        printMainMessage("Removing Older Versions of Bootstrap Loader..")
                        shutil.rmtree(f"/Applications/EfazRobloxBootstrapLoader.app/", ignore_errors=True)
                    elif os.path.exists(os.path.join(stored_main_app[found_platform][1], "Contents", "MacOS", "OrangeBlox.app")):
                        printMainMessage("Clearing Bootstrap App..")
                        shutil.rmtree(os.path.join(stored_main_app[found_platform][1], "Contents", "MacOS", "OrangeBlox.app"), ignore_errors=True)
                    
                    # Remove Installed Bootstrap
                    if os.path.exists(stored_main_app[found_platform][0]):
                        try:
                            printMainMessage("Removing Installed Bootstrap..")
                            shutil.rmtree(stored_main_app[found_platform][0])
                        except Exception as e:
                            printErrorMessage("Something went wrong removing installed bootstrap!")

                    # Delete frameworks if there's extra
                    del_fram = False
                    if os.path.exists(f"{stored_main_app[found_platform][1]}/Contents/MacOS/OrangeBlox.app/Contents/Frameworks/"):
                        if del_fram == False: printMainMessage("Clearing App Frameworks.."); del_fram = True
                        shutil.rmtree(f"{stored_main_app[found_platform][1]}/Contents/MacOS/OrangeBlox.app/Contents/Frameworks/", ignore_errors=True)
                    if os.path.exists(f"{stored_main_app[found_platform][1]}/Contents/Frameworks/"):
                        if del_fram == False: printMainMessage("Clearing App Frameworks.."); del_fram = True
                        shutil.rmtree(f"{stored_main_app[found_platform][1]}/Contents/Frameworks/", ignore_errors=True)
                    if os.path.exists(f"{stored_main_app[found_platform][2]}/Contents/Frameworks/"):
                        if del_fram == False: printMainMessage("Clearing App Frameworks.."); del_fram = True
                        shutil.rmtree(f"{stored_main_app[found_platform][2]}/Contents/Frameworks/", ignore_errors=True)
                    if os.path.exists(f"{stored_main_app[found_platform][3]}/Contents/Frameworks/"):
                        if del_fram == False: printMainMessage("Clearing App Frameworks.."); del_fram = True
                        shutil.rmtree(f"{stored_main_app[found_platform][3]}/Contents/Frameworks/", ignore_errors=True)

                    # Convert All Mod Modes to Mods
                    if os.path.exists(f"{current_path_location}/ModModes/"):
                        printMainMessage("Converting Mod Modes to Mods..")
                        for i in os.listdir(f"{current_path_location}/ModModes/"):
                            mod_mode_path = os.path.join(f"{current_path_location}/ModModes/", i)
                            if os.path.isdir(mod_mode_path):
                                if not os.path.exists(f"{current_path_location}/Mods/{i}/"):
                                    makedirs(f"{current_path_location}/Mods/{i}/")
                                pip_class.copyTreeWithMetadata(mod_mode_path, f"{current_path_location}/Mods/{i}/", dirs_exist_ok=True)
                        shutil.rmtree(f"{current_path_location}/ModModes/")
                    if os.path.exists(f"{stored_main_app[found_platform][1]}/Contents/Resources/ModModes/"):
                        printMainMessage("Converting Mod Modes to Mods..")
                        for i in os.listdir(f"{stored_main_app[found_platform][1]}/Contents/Resources/ModModes/"):
                            mod_mode_path = os.path.join(f"{stored_main_app[found_platform][1]}/Contents/Resources/ModModes/", i)
                            if os.path.isdir(mod_mode_path):
                                if not os.path.exists(f"{stored_main_app[found_platform][1]}/Contents/Resources/Mods/{i}/"):
                                    makedirs(f"{stored_main_app[found_platform][1]}/Contents/Resources/Mods/{i}/")
                                pip_class.copyTreeWithMetadata(mod_mode_path, f"{stored_main_app[found_platform][1]}/Contents/Resources/Mods/{i}/", dirs_exist_ok=True)
                        shutil.rmtree(f"{stored_main_app[found_platform][1]}/Contents/Resources/ModModes/")
                    
                    # Install to /Applications/
                    printMainMessage("Installing to Applications Folder..")
                    copy_with_symlinks(f"{current_path_location}/Apps/OrangeBloxMac/Apps/OrangeLoader.app", stored_main_app[found_platform][1])
                    if os.path.exists(stored_main_app[found_platform][0]):
                        copy_with_symlinks(f"{current_path_location}/Apps/OrangeBloxMac/Apps/OrangeBlox.app", stored_main_app[found_platform][0], ignore_files=ignore_files)
                    else:
                        copy_with_symlinks(f"{current_path_location}/Apps/OrangeBloxMac/Apps/OrangeBlox.app", stored_main_app[found_platform][0])
                    copy_with_symlinks(f"{current_path_location}/Apps/OrangeBloxMac/Apps/OrangePlayRoblox.app", stored_main_app[found_platform][2])
                    copy_with_symlinks(f"{current_path_location}/Apps/OrangeBloxMac/Apps/OrangeRunStudio.app", stored_main_app[found_platform][3])

                    # Prepare Contents of .app files
                    printMainMessage("Fetching App Folder..")
                    if os.path.exists(stored_main_app[found_platform][0]):
                        # Export ./ to /Contents/Resources/
                        printMainMessage("Copying Main Resources..")
                        if os.path.exists(os.path.join(stored_main_app["OverallInstall"], "EfazRobloxBootstrap.app", "Contents", "Resources")):
                            pip_class.copyTreeWithMetadata(os.path.join(stored_main_app["OverallInstall"], "EfazRobloxBootstrap.app", "Contents", "Resources"), f"{stored_main_app[found_platform][1]}/Contents/Resources/", dirs_exist_ok=True, ignore=ignore_files_func)
                        pip_class.copyTreeWithMetadata(f"{current_path_location}/", f"{stored_main_app[found_platform][1]}/Contents/Resources/", dirs_exist_ok=True, ignore=ignore_files_func)
                        
                        # Reduce Download Safety Measures
                        # This can prevent messages like: Apple could not verify “OrangeBlox.app” is free of malware that may harm your Mac or compromise your privacy.
                        if disable_download_for_app == True:
                            printMainMessage("Reducing Download Safety Measures..")
                            subprocess.run(f"xattr -rd com.apple.quarantine \"{stored_main_app[found_platform][1]}/Contents/MacOS/OrangeBlox.app/\"", shell=True, stdout=subprocess.DEVNULL)
                            subprocess.run(f"xattr -rd com.apple.quarantine \"{stored_main_app[found_platform][1]}/Contents/MacOS/OrangeBlox.app/\"", shell=True, stdout=subprocess.DEVNULL)

                        # Remove Apps Folder in /Contents/Resources/
                        printMainMessage("Cleaning App..")
                        if os.path.exists(os.path.join(stored_main_app[found_platform][0], "Contents", "Resources", "Apps")):
                            shutil.rmtree(os.path.join(stored_main_app[found_platform][0], "Contents", "Resources", "Apps"))
                        if os.path.exists(os.path.join(stored_main_app[found_platform][1], "Contents", "Resources", "Apps")):
                            shutil.rmtree(os.path.join(stored_main_app[found_platform][1], "Contents", "Resources", "Apps"))
                        if os.path.exists(os.path.join(stored_main_app[found_platform][2], "Contents", "Resources", "Apps")):
                            shutil.rmtree(os.path.join(stored_main_app[found_platform][2], "Contents", "Resources", "Apps"))
                        if os.path.exists(os.path.join(stored_main_app[found_platform][3], "Contents", "Resources", "Apps")):
                            shutil.rmtree(os.path.join(stored_main_app[found_platform][3], "Contents", "Resources", "Apps"))

                        # Sync Configuration Files
                        printMainMessage("Configurating App Data..")
                        if not ("OrangeBlox.app" in current_path_location): main_config["EFlagOrangeBloxSyncDir"] = current_path_location
                        main_config["EFlagAvailableInstalledDirectories"] = stored_main_app
                        saveSettings(main_config, directory=os.path.join(stored_main_app[found_platform][1], "Contents", "Resources", "FastFlagConfiguration.json"))
                        with open(os.path.join(stored_main_app[found_platform][2], "Contents", "Resources", "LocatedAppDirectory"), "w", encoding="utf-8") as f:
                            f.write(os.path.join(stored_main_app[found_platform][1], "Contents"))
                        with open(os.path.join(stored_main_app[found_platform][3], "Contents", "Resources", "LocatedAppDirectory"), "w", encoding="utf-8") as f:
                            f.write(os.path.join(stored_main_app[found_platform][1], "Contents"))
                        if stored_main_app.get("OverallInstall"): setInstalledAppPath(stored_main_app.get("OverallInstall"))
                        if os.path.exists(os.path.join(stored_main_app[found_platform][1], "Contents", "Resources", "FastFlagConfiguration.json")): os.remove(os.path.join(stored_main_app[found_platform][1], "Contents", "Resources", "FastFlagConfiguration.json"))

                        # Handle Avatar Maps
                        map_folder_contained = []
                        avatar_editor_path = os.path.join(stored_main_app[found_platform][1], "Contents", "Resources", "AvatarEditorMaps")
                        for ava_map in os.listdir(avatar_editor_path):
                            if os.path.isdir(os.path.join(avatar_editor_path, ava_map)):
                                map_folder_contained.append(ava_map)
                        if len(map_folder_contained) > 0:
                            printMainMessage("Converting Old Avatar Maps..")
                            for ava_map_fold in map_folder_contained:
                                if os.path.exists(os.path.join(avatar_editor_path, ava_map_fold, "AvatarBackground.rbxl")): shutil.copy(os.path.join(avatar_editor_path, ava_map_fold, "AvatarBackground.rbxl"), os.path.join(avatar_editor_path, f"{ava_map_fold}.rbxl"))
                                shutil.rmtree(os.path.join(avatar_editor_path, ava_map_fold), ignore_errors=True)

                        # Finalize Branding
                        if os.path.exists(os.path.join(stored_main_app["OverallInstall"], "EfazRobloxBootstrap.app", "Contents", "Resources")):
                            printMainMessage("Finalizing App Branding..")
                            shutil.rmtree(os.path.join(stored_main_app["OverallInstall"], "EfazRobloxBootstrap.app"), ignore_errors=True)

                        # Success!
                        end_build_time = datetime.datetime.now().timestamp()
                        if overwrited == True:
                            printSuccessMessage(f"Successfully updated OrangeBlox in {round(end_build_time-started_build_time, 3)}s!")
                        else:
                            printSuccessMessage(f"Successfully installed OrangeBlox in {round(end_build_time-started_build_time, 3)}s!")
                    else:
                        printErrorMessage("Something went wrong trying to find the application folder.")
                    shutil.rmtree(f"{current_path_location}/Apps/OrangeBloxMac/")
                else:
                    printErrorMessage("Something went wrong trying to find the installation folder.")
            elif main_os == "Windows":
                # Get FastFlagConfiguration.json Data
                if overwrited == True:
                    printMainMessage("Getting Configuration File Data..")
                    fast_config_path = os.path.join(f"{stored_main_app[found_platform][0]}", "Configuration.json")
                    if os.path.exists(os.path.join(stored_main_app["OverallInstall"], "EfazRobloxBootstrap", "FastFlagConfiguration.json")): fast_config_path = os.path.join(stored_main_app["OverallInstall"], "EfazRobloxBootstrap", "FastFlagConfiguration.json")
                    elif os.path.exists(os.path.join(stored_main_app[found_platform][0], "FastFlagConfiguration.json")): fast_config_path = os.path.join(stored_main_app[found_platform][0], "FastFlagConfiguration.json")
                    main_config = getSettings(directory=fast_config_path if os.path.exists(fast_config_path) else os.path.join(current_path_location, "Configuration.json"))
                else:
                    main_config = {}
                    if os.path.exists(os.path.join(current_path_location, "Configuration.json")):
                        with open(os.path.join(current_path_location, "Configuration.json"), "r", encoding="utf-8") as f: main_config = json.load(f)

                # Adapt Fast Flags from Efaz's Roblox Bootstrap
                if not main_config.get("EFlagRobloxPlayerFlags"):
                    printMainMessage("Converting Fast Flags..")
                    player_flags = {}
                    for i, v in main_config.items():
                        if not i.startswith("EFlag"):
                            player_flags[i] = v
                    for i, v in player_flags.items():
                        main_config.pop(i)
                    main_config["EFlagRobloxPlayerFlags"] = player_flags
                    main_config["EFlagRobloxStudioFlags"] = {}

                # Rebuild Pyinstaller & Nuitka Apps
                if rebuild_from_source == 1 or (main_config.get("EFlagRebuildPyinstallerAppFromSourceDuringUpdates") == True and update_mode == True):
                    printMainMessage("Running Pyinstaller Rebuild..")
                    pa = convertPythonExecutablesInFileToPaths(os.path.join(current_path_location, "Apps", "Scripts", "Pyinstaller", f"RecreateWindows{'32' if is_x86_windows() else ''}.bat"), pip_class)
                    rebuild_status = subprocess.run(f"{pa} installer signexe", shell=True, cwd=current_path_location)
                    if rebuild_status.returncode == 0:
                        printSuccessMessage("Pyinstaller Rebuild Success!")
                        os.remove(pa)
                        if full_rebuild_mode == True and not is_x86_windows():
                            printMainMessage("Running Pyinstaller Rebuild in x86..")
                            x86_python = PipHandler.pip(opposite=True)
                            if x86_python.pythonInstalled():
                                if x86_python.installed(["pyinstaller"]):
                                    pa = convertPythonExecutablesInFileToPaths(os.path.join(current_path_location, "Apps", "Scripts", "Pyinstaller", f"RecreateWindows32.bat"), x86_python)
                                    rebuild_x86_status = subprocess.run(f"{pa} installer signexe", shell=True, cwd=current_path_location)
                                    os.remove(pa)
                                    if rebuild_x86_status.returncode == 0:
                                        printSuccessMessage("Pyinstaller x86 Rebuild Success!")
                                    else:
                                        printErrorMessage(f"Pyinstaller Rebuild failed! Status code: {rebuild_status.returncode}")
                                        return
                                else:
                                    printYellowMessage(f"Skipped full build because x86 version of pyinstaller is not installed")
                            else:
                                printYellowMessage(f"Skipped full build because x86 version of Python is not installed")
                    else:
                        printErrorMessage(f"Pyinstaller Rebuild failed! Status code: {rebuild_status.returncode}")
                        return
                elif rebuild_from_source == 2 or (main_config.get("EFlagRebuildNuitkaAppFromSourceDuringUpdates") == True and update_mode == True):
                    printMainMessage("Running Nuitka Rebuild..")
                    pa = convertPythonExecutablesInFileToPaths(os.path.join(current_path_location, "Apps", "Scripts", "Nuitka", f"RecreateWindows{'32' if is_x86_windows() else ''}.bat"), pip_class)
                    rebuild_status = subprocess.run(f"{pa} installer signexe", shell=True, cwd=current_path_location)
                    os.remove(pa)
                    if rebuild_status.returncode == 0:
                        printSuccessMessage("Nuitka Rebuild success!")
                        if full_rebuild_mode == True and not is_x86_windows():
                            printMainMessage("Running Nuitka Rebuild in x86..")
                            x86_python = PipHandler.pip(opposite=True)
                            if x86_python.pythonInstalled():
                                if x86_python.installed(["Nuitka"]):
                                    pa = convertPythonExecutablesInFileToPaths(os.path.join(current_path_location, "Apps", "Scripts", "Nuitka", f"RecreateWindows32.bat"), x86_python)
                                    rebuild_x86_status = subprocess.run(f"{pa} installer signexe", shell=True, cwd=current_path_location)
                                    os.remove(pa)
                                    if rebuild_x86_status.returncode == 0:
                                        printSuccessMessage("Nuitka x86 Rebuild Success!")
                                    else:
                                        printErrorMessage(f"Nuitka Rebuild failed! Status code: {rebuild_status.returncode}")
                                        return
                                else:
                                    printYellowMessage(f"Skipped full build because x86 version of Nuitka is not installed")
                            else:
                                printYellowMessage(f"Skipped full build because x86 version of Python is not installed")
                    else:
                        printErrorMessage(f"Nuitka Rebuild failed! Status code: {rebuild_status.returncode}")
                        return
                    
                if os.path.exists(f"{current_path_location}/Apps/OrangeBloxWindows.zip"):
                    # Unzip Installation ZIP
                    printMainMessage("Unzipping Installation ZIP File..")
                    try:
                        makedirs(f'{current_path_location}/Apps/OrangeBloxWindows/')
                        subprocess.run(["tar", "-xf", f'{current_path_location}/Apps/OrangeBloxWindows.zip', "-C", f'{current_path_location}/Apps/OrangeBloxWindows/'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                    except Exception as e:
                        printErrorMessage(f"Something went wrong while trying to unzip macOS apps file: {str(e)}")
                    time.sleep(1)
                else:
                    printYellowMessage("Something went wrong finding OrangeBloxWindows.zip. It will require a OrangeBloxWindows folder in order for installation to finish.")
                if os.path.exists(f"{current_path_location}/Apps/OrangeBloxWindows/"):
                    # Delete Other Operating System Files
                    deleted_other_os = False
                    if not (disable_remove_other_operating_systems == True or main_config.get("EFlagDisableDeleteOtherOSApps") == True):
                        if os.path.exists(os.path.join(current_path_location, "/Apps/OrangeBloxMac.zip")):
                            os.remove(os.path.join(current_path_location, "/Apps/OrangeBloxMac.zip"))
                            deleted_other_os = True
                        if os.path.exists(os.path.join(current_path_location, "/Apps/OrangeBloxMacIntel.zip")):
                            os.remove(os.path.join(current_path_location, "/Apps/OrangeBloxMacIntel.zip"))
                            deleted_other_os = True
                        if deleted_other_os == True: printMainMessage("To help save space, the script has automatically deleted files made for other operating systems!")

                    # Convert All Mod Modes to Mods
                    if os.path.exists(os.path.join(current_path_location, "/ModModes/")):
                        printMainMessage("Converting Mod Modes to Mods..")
                        for i in os.listdir(os.path.join(current_path_location, "/ModModes/")):
                            mod_mode_path = os.path.join(os.path.join(current_path_location, "/ModModes/"), i)
                            if os.path.isdir(mod_mode_path):
                                if not os.path.exists(os.path.join(current_path_location, f"/Mods/{i}/")):
                                    makedirs(os.path.join(current_path_location, f"/Mods/{i}/"))
                                pip_class.copyTreeWithMetadata(mod_mode_path, f"{current_path_location}/Mods/{i}/")
                        shutil.rmtree(os.path.join(current_path_location, "/ModModes/"))
                    if os.path.exists(os.path.join(stored_main_app[found_platform][0], "ModModes")):
                        printMainMessage("Converting Mod Modes to Mods..")
                        for i in os.listdir(os.path.join(stored_main_app[found_platform][0], "ModModes")):
                            mod_mode_path = os.path.join(os.path.join(stored_main_app[found_platform][0], "ModModes"), i)
                            if os.path.isdir(mod_mode_path):
                                if not os.path.exists(os.path.join(stored_main_app[found_platform][0], "Mods", i)):
                                    makedirs(os.path.join(stored_main_app[found_platform][0], "Mods", i))
                                pip_class.copyTreeWithMetadata(mod_mode_path, os.path.join(stored_main_app[found_platform][0], "Mods", i), dirs_exist_ok=True)
                        shutil.rmtree(os.path.join(stored_main_app[found_platform][0], "ModModes"))

                    # Copy Apps
                    printMainMessage("Creating paths..")
                    makedirs(stored_main_app[found_platform][0])

                    # Copy EfazRobloxBootstrap
                    if os.path.exists(os.path.join(stored_main_app["OverallInstall"], "EfazRobloxBootstrap")): 
                        printMainMessage("Copying EfazRobloxBootstrap App..")
                        pip_class.copyTreeWithMetadata(os.path.join(stored_main_app["OverallInstall"], "EfazRobloxBootstrap"), stored_main_app[found_platform][0], dirs_exist_ok=True, ignore=ignore_files_func)

                    # Install EXE File
                    if pip_class.getIfProcessIsOpened("OrangeBlox.exe"):
                        printMainMessage("Closing OrangeBlox executable in order to install EXE file..")
                        pip_class.endProcess("OrangeBlox.exe")
                    printMainMessage("Installing EXE File..")
                    try:
                        if is_x86_windows() or use_x86_windows == True:
                            shutil.copy(os.path.join(current_path_location, "Apps", "OrangeBloxWindows", "OrangeBlox32.exe"), stored_main_app[found_platform][1])
                            shutil.copy(os.path.join(current_path_location, "Apps", "OrangeBloxWindows", "PlayRoblox32.exe"), os.path.join(stored_main_app[found_platform][2], "PlayRoblox.exe"))
                            shutil.copy(os.path.join(current_path_location, "Apps", "OrangeBloxWindows", "RunStudio32.exe"), os.path.join(stored_main_app[found_platform][2], "RunStudio.exe"))
                            pip_class.copyTreeWithMetadata(os.path.join(current_path_location, "Apps", "OrangeBloxWindows", "_internal32"), os.path.join(stored_main_app[found_platform][0], "_internal"), dirs_exist_ok=True, symlinks=True, ignore_if_not_exist=True)
                        else:
                            if os.path.exists(os.path.join(current_path_location, "Apps", "OrangeBloxWindows", "OrangeBlox.exe")):
                                shutil.copy(os.path.join(current_path_location, "Apps", "OrangeBloxWindows", "OrangeBlox.exe"), stored_main_app[found_platform][1])
                                shutil.copy(os.path.join(current_path_location, "Apps", "OrangeBloxWindows",  "PlayRoblox.exe"), os.path.join(stored_main_app[found_platform][2], "PlayRoblox.exe"))
                                shutil.copy(os.path.join(current_path_location, "Apps", "OrangeBloxWindows",  "RunStudio.exe"), os.path.join(stored_main_app[found_platform][2], "RunStudio.exe"))
                                pip_class.copyTreeWithMetadata(os.path.join(current_path_location, "Apps", "OrangeBloxWindows", "_internal"), os.path.join(stored_main_app[found_platform][0], "_internal"), dirs_exist_ok=True, symlinks=True, ignore_if_not_exist=True)
                            else:
                                printErrorMessage("There was an issue trying to find the x64 version of the Windows app. Would you like to install the 32-bit version? [32-bit Python is not needed.]")
                                a = input("> ")
                                if not (a.lower() == "n"):
                                    shutil.copy(os.path.join(current_path_location, "Apps", "OrangeBloxWindows", "OrangeBlox32.exe"), stored_main_app[found_platform][1])
                                    shutil.copy(os.path.join(current_path_location, "Apps", "OrangeBloxWindows",  "PlayRoblox32.exe"), os.path.join(stored_main_app[found_platform][2], "PlayRoblox.exe"))
                                    shutil.copy(os.path.join(current_path_location, "Apps", "OrangeBloxWindows",  "RunStudio32.exe"), os.path.join(stored_main_app[found_platform][2], "RunStudio.exe"))
                                    pip_class.copyTreeWithMetadata(os.path.join(current_path_location, "Apps", "OrangeBloxWindows", "_internal32"), os.path.join(stored_main_app[found_platform][0], "_internal"), dirs_exist_ok=True, symlinks=True, ignore_if_not_exist=True)
                                else:
                                    sys.exit(0)
                    except Exception as e:
                        printErrorMessage(f"There was an issue installing the EXE file: {str(e)}")

                    # Reduce Download Safety Measures
                    # This can prevent messages from Microsoft Smartscreen
                    if disable_download_for_app == True:
                        printMainMessage("Reducing Download Safety Measures..")
                        unblock_1 = subprocess.run(["powershell", "-Command", f'Unblock-File -Path "{stored_main_app[found_platform][1]}"'], shell=True, stdout=subprocess.DEVNULL)
                        if not (unblock_1.returncode == 0): printErrorMessage(f"Unable to unblock main bootstrap app: {unblock_1.returncode}")
                        unblock_2 = subprocess.run(["powershell", "-Command", f'Unblock-File -Path "{os.path.join(stored_main_app[found_platform][2], "PlayRoblox.exe")}"'], shell=True, stdout=subprocess.DEVNULL)
                        if not (unblock_2.returncode == 0): printErrorMessage(f"Unable to unblock Play Roblox app: {unblock_2.returncode}")
                        unblock_3 = subprocess.run(["powershell", "-Command", f'Unblock-File -Path "{os.path.join(stored_main_app[found_platform][2], "RunStudio.exe")}"'], shell=True, stdout=subprocess.DEVNULL)
                        if not (unblock_3.returncode == 0): printErrorMessage(f"Unable to unblock Run Studio app: {unblock_3.returncode}")

                    # Setup URL Schemes
                    import winreg
                    if instant_install == False:
                        if not (disabled_url_scheme_installation == True):
                            printMainMessage("Setting up URL Schemes..")
                            def set_url_scheme(protocol, exe_path):
                                try:
                                    protocol_key = r"Software\Classes\{}".format(protocol)
                                    command_key = r"Software\Classes\{}\shell\open\command".format(protocol)
                                    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, protocol_key) as key:
                                        winreg.SetValue(key, "", winreg.REG_SZ, "URL:{}".format(protocol))
                                        winreg.SetValueEx(key, "URL Protocol", 0, winreg.REG_SZ, protocol)
                                    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, command_key) as key:
                                        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, '"{}" "%1"'.format(exe_path))
                                    printSuccessMessage(f'URL scheme "{protocol}" has been set for "{exe_path}"')
                                except Exception as e:
                                    printErrorMessage(f"An error occurred: {e}")
                            def get_file_type_reg(extension):
                                try:
                                    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, extension) as key:
                                        file_type, _ = winreg.QueryValueEx(key, "")
                                        return file_type
                                except FileNotFoundError:
                                    return None
                            def set_file_type_reg(extension, exe_path, file_type):
                                try:
                                    import ctypes
                                    extension = extension if extension.startswith('.') else f'.{extension}'
                                    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{extension}") as key: winreg.SetValue(key, "", winreg.REG_SZ, file_type)
                                    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{file_type}\\shell\\open\\command") as key: winreg.SetValue(key, "", winreg.REG_SZ, f'"{exe_path}" "%1"')
                                    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{file_type}\\DefaultIcon") as key: winreg.SetValue(key, "", winreg.REG_SZ, f"{exe_path},0")
                                    ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x0000, None, None)
                                    printSuccessMessage(f'File Handling "{extension}" has been set for "{exe_path}"')
                                except Exception as e:
                                    printErrorMessage(f"An error occurred: {e}")
                            set_url_scheme("efaz-bootstrap", stored_main_app[found_platform][1])
                            set_url_scheme("orangeblox", stored_main_app[found_platform][1])
                            set_url_scheme("roblox-player", stored_main_app[found_platform][1])
                            set_url_scheme("roblox", stored_main_app[found_platform][1])
                            set_file_type_reg(".obx", stored_main_app[found_platform][1], "OrangeBlox Backup")
                            # set_file_type_reg(".rbxl", stored_main_app[found_platform][1], "Roblox Place")
                            # set_file_type_reg(".rbxlx", stored_main_app[found_platform][1], "Roblox Place")
                            # set_url_scheme("roblox-studio", stored_main_app[found_platform][1])
                            # set_url_scheme("roblox-studio-auth", stored_main_app[found_platform][1])
                    else:
                        if not (main_config.get("EFlagDisableURLSchemeInstall") == True):
                            printMainMessage("Setting up URL Schemes..")
                            def set_url_scheme(protocol, exe_path):
                                try:
                                    protocol_key = r"Software\Classes\{}".format(protocol)
                                    command_key = r"Software\Classes\{}\shell\open\command".format(protocol)
                                    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, protocol_key) as key:
                                        winreg.SetValue(key, "", winreg.REG_SZ, "URL:{}".format(protocol))
                                        winreg.SetValueEx(key, "URL Protocol", 0, winreg.REG_SZ, protocol)
                                    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, command_key) as key:
                                        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, '"{}" "%1"'.format(exe_path))
                                    printSuccessMessage(f'URL scheme "{protocol}" has been set for "{exe_path}"')
                                except Exception as e:
                                    printErrorMessage(f"An error occurred: {e}")
                            def get_file_type_reg(extension):
                                try:
                                    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, extension) as key:
                                        file_type, _ = winreg.QueryValueEx(key, "")
                                        return file_type
                                except FileNotFoundError:
                                    return None
                            def set_file_type_reg(extension, exe_path, file_type):
                                try:
                                    import ctypes
                                    extension = extension if extension.startswith('.') else f'.{extension}'
                                    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{extension}") as key: winreg.SetValue(key, "", winreg.REG_SZ, file_type)
                                    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{file_type}\\shell\\open\\command") as key: winreg.SetValue(key, "", winreg.REG_SZ, f'"{exe_path}" "%1"')
                                    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{file_type}\\DefaultIcon") as key: winreg.SetValue(key, "", winreg.REG_SZ, f"{exe_path},0")
                                    ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x0000, None, None)
                                    printSuccessMessage(f'File Handling "{extension}" has been set for "{exe_path}"')
                                except Exception as e:
                                    printErrorMessage(f"An error occurred: {e}")
                            set_url_scheme("efaz-bootstrap", stored_main_app[found_platform][1])
                            set_url_scheme("orangeblox", stored_main_app[found_platform][1])
                            set_url_scheme("roblox-player", stored_main_app[found_platform][1])
                            set_url_scheme("roblox", stored_main_app[found_platform][1])
                            set_file_type_reg(".obx", stored_main_app[found_platform][1], "OrangeBlox Backup")
                            # set_file_type_reg(".rbxl", stored_main_app[found_platform][1], "Roblox Place")
                            # set_file_type_reg(".rbxlx", stored_main_app[found_platform][1], "Roblox Place")
                            # set_url_scheme("roblox-studio", stored_main_app[found_platform][1])
                            # set_url_scheme("roblox-studio-auth", stored_main_app[found_platform][1])

                    # Setup Shortcuts
                    if not (disabled_shortcuts_installation == True or main_config.get("EFlagDisableShortcutsInstall") == True):
                        printMainMessage("Setting up shortcuts..")
                        try:
                            import win32com.client # type: ignore
                            def create_shortcut(target_path, shortcut_path, working_directory=None, icon_path=None):
                                shell = win32com.client.Dispatch('WScript.Shell')
                                if not os.path.exists(os.path.dirname(shortcut_path)): os.makedirs(os.path.dirname(shortcut_path))
                                shortcut = shell.CreateShortcut(shortcut_path)
                                shortcut.TargetPath = target_path
                                if working_directory:
                                    shortcut.WorkingDirectory = working_directory
                                if icon_path:
                                    shortcut.IconLocation = icon_path
                                shortcut.save()
                            create_shortcut(stored_main_app[found_platform][1], os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs'), "OrangeBlox.lnk"))
                            create_shortcut(stored_main_app[found_platform][1], os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), "OrangeBlox.lnk"))
                            create_shortcut(os.path.join(stored_main_app[found_platform][2], "PlayRoblox.exe"), os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), "Roblox Player.lnk"))
                            create_shortcut(os.path.join(stored_main_app[found_platform][2], "PlayRoblox.exe"), os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs'), 'Play Roblox.lnk'))
                            create_shortcut(os.path.join(stored_main_app[found_platform][2], "PlayRoblox.exe"), os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Roblox'), 'Roblox Player.lnk'))
                            create_shortcut(os.path.join(stored_main_app[found_platform][2], "RunStudio.exe"), os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), "Roblox Studio.lnk"))
                            create_shortcut(os.path.join(stored_main_app[found_platform][2], "RunStudio.exe"), os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs'), 'Run Studio.lnk'))
                            create_shortcut(os.path.join(stored_main_app[found_platform][2], "RunStudio.exe"), os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Roblox'), 'Roblox Studio.lnk'))
                        except Exception as e:
                            printYellowMessage(f"There was an issue setting shortcuts and may be caused due to OneDrive. Error: {str(e)}")

                    # Copy App Resources
                    printMainMessage("Fetching App Folder..")
                    if os.path.exists(stored_main_app[found_platform][1]):
                        # Export ./ to {app_path}/
                        printMainMessage("Copying Main Resources..")
                        pip_class.copyTreeWithMetadata(current_path_location, stored_main_app[found_platform][0], dirs_exist_ok=True, ignore=ignore_files_func)

                        # Handle Existing Configuration Files
                        printMainMessage("Configurating App Data..")
                        if disabled_url_scheme_installation == True:
                            main_config["EFlagDisableURLSchemeInstall"] = True
                        elif disabled_url_scheme_installation == False:
                            main_config["EFlagDisableURLSchemeInstall"] = False
                        if disabled_shortcuts_installation == True:
                            main_config["EFlagDisableShortcutsInstall"] = True
                        elif disabled_shortcuts_installation == False:
                            main_config["EFlagDisableShortcutsInstall"] = False

                        if use_installation_syncing == True and not ("/Local/OrangeBlox/" in current_path_location): main_config["EFlagOrangeBloxSyncDir"] = current_path_location
                        main_config["EFlagAvailableInstalledDirectories"] = stored_main_app
                        data_in_string = zlib.compress(json.dumps(main_config).encode('utf-8'))
                        with open(os.path.join(f"{stored_main_app[found_platform][0]}", "Configuration.json"), "wb") as f: f.write(data_in_string)
                        if os.path.exists(os.path.join(f"{stored_main_app[found_platform][0]}", "FastFlagConfiguration.json")): os.remove(os.path.join(f"{stored_main_app[found_platform][0]}", "FastFlagConfiguration.json"))

                        # Handle Avatar Maps
                        map_folder_contained = []
                        avatar_editor_path = os.path.join(stored_main_app[found_platform][0], "AvatarEditorMaps")
                        for ava_map in os.listdir(avatar_editor_path):
                            if os.path.isdir(os.path.join(avatar_editor_path, ava_map)):
                                map_folder_contained.append(ava_map)
                        if len(map_folder_contained) > 0:
                            printMainMessage("Converting Old Avatar Maps..")
                            for ava_map_fold in map_folder_contained:
                                if os.path.exists(os.path.join(avatar_editor_path, ava_map_fold, "AvatarBackground.rbxl")): shutil.copy(os.path.join(avatar_editor_path, ava_map_fold, "AvatarBackground.rbxl"), os.path.join(avatar_editor_path, f"{ava_map_fold}.rbxl"))
                                shutil.rmtree(os.path.join(avatar_editor_path, ava_map_fold), ignore_errors=True)

                        # Remove Apps Folder in Installed Folder
                        if os.path.exists(os.path.join(stored_main_app[found_platform][0], "Apps")):
                            printMainMessage("Cleaning App..")
                            shutil.rmtree(os.path.join(stored_main_app[found_platform][0], "Apps"))

                        # Mark Installation in Windows
                        printMainMessage("Marking Program Installation into Windows..")
                        app_key = "Software\\OrangeBlox"
                        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, app_key) as key:
                            winreg.SetValueEx(key, "InstallPath", 0, winreg.REG_SZ, stored_main_app[found_platform][0])
                            winreg.SetValueEx(key, "Installed", 0, winreg.REG_DWORD, 1)

                        registry_path = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\OrangeBlox"
                        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, registry_path) as key:
                            winreg.SetValueEx(key, "UninstallString", 0, winreg.REG_SZ, f"{sys.executable} {os.path.join(stored_main_app[found_platform][0], 'Install.py')} --uninstall-mode")
                            winreg.SetValueEx(key, "ModifyPath", 0, winreg.REG_SZ, f"{sys.executable} {os.path.join(stored_main_app[found_platform][0], 'Install.py')}")
                            winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, "OrangeBlox")
                            winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, current_version["version"])
                            winreg.SetValueEx(key, "DisplayIcon", 0, winreg.REG_SZ, os.path.join(stored_main_app[found_platform][0], "BootstrapImages", "AppIcon.ico"))
                            winreg.SetValueEx(key, "HelpLink", 0, winreg.REG_SZ, "https://github.com/efazdev/orangeblox")
                            winreg.SetValueEx(key, "URLUpdateInfo", 0, winreg.REG_SZ, "https://github.com/efazdev/orangeblox")
                            winreg.SetValueEx(key, "URLInfoAbout", 0, winreg.REG_SZ, "https://github.com/efazdev/orangeblox")
                            winreg.SetValueEx(key, "InstallLocation", 0, winreg.REG_SZ, stored_main_app[found_platform][0])
                            winreg.SetValueEx(key, "Publisher", 0, winreg.REG_SZ, "EfazDev")
                            winreg.SetValueEx(key, "EstimatedSize", 0, winreg.REG_DWORD, min(getFolderSize(stored_main_app[found_platform][0], formatWithAbbreviation=False) // 1024, 0xFFFFFFFF))
                    
                        # Finalize Branding
                        if os.path.exists(os.path.join(stored_main_app["OverallInstall"], "EfazRobloxBootstrap")):
                            printMainMessage("Finalizing App Branding..")
                            shutil.rmtree(os.path.join(stored_main_app["OverallInstall"], "EfazRobloxBootstrap"), ignore_errors=True)
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
                            try:
                                def remove_path(pat):
                                    if os.path.exists(pat): 
                                        os.remove(pat)
                                remove_path(os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), "Efaz\'s Roblox Bootstrap.lnk"))
                                remove_path(os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs'), "Efaz\'s Roblox Bootstrap.lnk"))
                            except Exception as e:
                                printErrorMessage(f"Unable to remove shortcuts: {str(e)}")

                        # Finalize App Location
                        if stored_main_app.get("OverallInstall"): setInstalledAppPath(stored_main_app.get("OverallInstall"))

                        # Success!
                        end_build_time = datetime.datetime.now().timestamp()
                        if overwrited == True:
                            printSuccessMessage(f"Successfully updated OrangeBlox in {round(end_build_time-started_build_time, 3)}s!")
                        else:
                            printSuccessMessage(f"Successfully installed OrangeBlox in {round(end_build_time-started_build_time, 3)}s!")
                        shutil.rmtree(f"{current_path_location}/Apps/OrangeBloxWindows/")
                    else:
                        printErrorMessage("Something went wrong trying to find the installation folder.")
                else:
                    printErrorMessage("Something went wrong trying to find the installation folder.")
            else:
                printErrorMessage("OrangeBlox is only supported for macOS and Windows.")
        else:
            printErrorMessage("There was an issue while finding the Apps folder for installation.")
    if silent_mode == True:
        instant_install = True
        try:
            install()
        except Exception as e:
            printErrorMessage(f"Something went wrong during installation: {str(e)}")
    else:
        if overwrited == True:
            printWarnMessage("--- Updater ---")
        else:
            printWarnMessage("--- Installer ---")
        if instant_install == True:
            try:
                install()
            except Exception as e:
                printErrorMessage(f"Something went wrong during installation: {str(e)}")
            if rebuild_mode == False: input("> ")
        else:
            printMainMessage("Welcome to OrangeBlox Installer 🍊!")
            printMainMessage("OrangeBlox is a Roblox bootstrap that allows you to add modifications to your Roblox client using files, activity tracking and Python!")
            printMainMessage("Before we continue to installing, you must complete these questions before you can install!")
            printMainMessage("If you want to say yes, type \"y\". Otherwise, type \"n\". Anyway, here ya go!")

            try:
                requests = pip_class.importModule("requests")
                plyer = pip_class.importModule("plyer")
                pypresence = pip_class.importModule("pypresence")
                tkinter = pip_class.importModule("tkinter")
                if main_os == "Darwin":
                    posix_ipc = pip_class.importModule("posix_ipc")
                    objc = pip_class.importModule("objc")
                elif main_os == "Windows":
                    win32com = pip_class.importModule("win32com")
                if rebuild_from_source == 1: rebuild_target = ["pyinstaller"]
                if rebuild_from_source == 2: rebuild_target = ["Nuitka"]
                if len(rebuild_target) > 0 and not pip_class.installed(rebuild_target, boolonly=True): raise Exception(f"Please install {rebuild_target[0]} for this mode!")
            except Exception as e:
                if not instant_install == True: printMainMessage("Modules from the internet are needed to be installed in order to use OrangeBlox. Do you want to install them now? (y/n)")
                if instant_install == True or isYes(input("> ")) == True:
                    if rebuild_from_source == 1: rebuild_target = ["pyinstaller"]
                    if rebuild_from_source == 2: rebuild_target = ["Nuitka"]
                    pip_class.install(["requests", "plyer", "pypresence", "tk"] + rebuild_target)
                    if main_os == "Darwin": pip_class.install(["posix-ipc", "pyobjc-core", "pyobjc-framework-Quartz", "pyobjc-framework-Cocoa"])
                    elif main_os == "Windows": pip_class.install(["pywin32"])
                    pip_class.restartScript("Install.py", sys.argv)
                    printSuccessMessage("Successfully installed modules!")
                else:
                    printErrorMessage("Ending installation..")
                    sys.exit(0)
            
            if overwrited == False:
                printMainMessage("Would you like to check for any new bootstrap updates right now? (y/n)")
                a = input("> ")
                if isYes(a) == True:
                    import requests
                    version_server = "https://obx.efaz.dev/Version.json"
                    if not (type(version_server) is str and version_server.startswith("https://")): version_server = "https://obx.efaz.dev/Version.json"
                    latest_vers_res = requests.get(f"{version_server}")
                    if latest_vers_res.ok:
                        latest_vers = latest_vers_res.json()
                        if current_version.get("version"):
                            if current_version.get("version", "1.0.0") < latest_vers.get("latest_version", "1.0.0"):
                                download_location = latest_vers.get("download_location", "https://github.com/EfazDev/orangeblox/archive/refs/heads/main.zip")
                                printWarnMessage("--- New Bootstrap Update ---")
                                printMainMessage(f"We have detected a new version of OrangeBlox! Would you like to install it? (y/n)")
                                if download_location == "https://github.com/EfazDev/orangeblox/archive/refs/heads/main.zip":
                                    printSuccessMessage("✅ This version is a public update available on GitHub for viewing.")
                                elif download_location == "https://cdn.efaz.dev/cdn/py/orangeblox-beta.zip":
                                    printYellowMessage("⚠️ This version is a beta and may cause issues with your installation.")
                                else:
                                    printErrorMessage("❌ The download location for this version is different from the official GitHub download link!! You may be downloading an unofficial OrangeBlox version!")
                                printSuccessMessage(f"v{current_version.get('version', '1.0.0')} [Current] => v{latest_vers['latest_version']} [Latest]")
                                if isYes(input("> ")) == True:
                                    printMainMessage("Downloading latest version..")
                                    download_update = subprocess.run(["curl", "-L", download_location, "-o", f"{current_path_location}/Update.zip"])
                                    if download_update.returncode == 0:
                                        printMainMessage("Download Success! Extracting ZIP now!")
                                        makedirs(f"{current_path_location}/Update/")
                                        if main_os == "Darwin": zip_extract = subprocess.run(["unzip", "-o", "Update.zip", "-d", f"{current_path_location}/Update/"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                        elif main_os == "Windows": zip_extract = subprocess.run(["tar", "-xf", 'Update.zip', "-C", f'{current_path_location}/Update/'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                        if zip_extract.returncode == 0:
                                            printMainMessage("Extracted successfully! Installing Files!")
                                            for file in os.listdir(f"{current_path_location}/Update/orangeblox-main/"):
                                                src_path = os.path.join(f"{current_path_location}/Update/orangeblox-main/", file)
                                                dest_path = os.path.join(current_path_location, file)
                                                
                                                if os.path.isdir(src_path):
                                                    pip_class.copyTreeWithMetadata(src_path, dest_path, dirs_exist_ok=True)
                                                else:
                                                    if not file.endswith(".json"):
                                                        shutil.copy2(src_path, dest_path)
                                            printMainMessage("Cleaning up files..")
                                            os.remove("Update.zip")
                                            shutil.rmtree(f"{current_path_location}/Update/")
                                            printSuccessMessage(f"Update to v{latest_vers['version']} was finished successfully! Restarting installer..")
                                            subprocess.run(args=[sys.executable] + sys.argv)
                                            sys.exit(0)
                                        else:
                                            printMainMessage("Cleaning up files..")
                                            os.remove("Update.zip")
                                            shutil.rmtree(f"{current_path_location}/Update/")
                                            printErrorMessage("Extracting ZIP File failed. Would you like to continue to Roblox without updating? (y/n)")
                                            if isYes(input("> ")) == False: sys.exit(0)
                                    else:
                                        printErrorMessage("Downloading ZIP File failed. Would you like to continue to Roblox without updating? (y/n)")
                                        if isYes(input("> ")) == False: sys.exit(0)
                            elif current_version.get("version", "1.0.0") > latest_vers.get("latest_version", "1.0.0"):
                                printSuccessMessage("The bootstrap is a beta version! No updates are needed!")
                            else:
                                printMainMessage("The bootstrap is currently on the latest version! No updates are needed!")
                    else:
                        printErrorMessage("There was an issue while checking for updates.")
                if main_os == "Windows":
                    printMainMessage("Would you like to set the URL Schemes for the Roblox Client and the bootstrap? [Needed for Roblox Link Shortcuts and when Roblox updates] (y/n)")
                    a = input("> ")
                    if isYes(a) == False:
                        disabled_url_scheme_installation = True
                    printMainMessage("Would you like to make shortcuts for the bootstrap? [Needed for launching through the Windows Start Menu and Desktop] (y/n)")
                    a = input("> ")
                    if isYes(a) == False:
                        disabled_shortcuts_installation = True
                printMainMessage("In order to allow running for the first time, we're gonna reduce download securities for the app bundle. [This won't affect other apps or downloaded files]")
                printMainMessage("This will not bypass scans by your anti-virus software. It will only allow running by the operating system. (y/n)")
                a = input("> ")
                if isYes(a) == False:
                    disable_download_for_app = False
                printMainMessage("Would you like to allow syncing configurations and mods from this folder to the app? (Only 1 installation folder can be used) (y/n)")
                a = input("> ")
                if isYes(a) == False:
                    use_installation_syncing = False
                printMainMessage("Would you like to rebuild the main app based on source code? (y/n)")
                printYellowMessage("Pyinstaller is required to be installed for this to work.")
                a = input("> ")
                if isYes(a) == True:
                    if not pip_class.installed(["pyinstaller"], boolonly=True): pip_class.install(["pyinstaller"])
                    rebuild_from_source = True
                if main_os == "Darwin":
                    printMainMessage("Would you like to rebuild the Bootstrap Loader, Play Roblox app and Run Studio app based on source code? (y/n)")
                    printYellowMessage("Clang++ is required to be installed on your Mac in order to use.")
                    a = input("> ")
                    if isYes(a) == True:
                        rebuild_from_source_clang = True
                if main_os == "Windows":
                    printMainMessage("Would you like to set an install location for the bootstrap? (y/n)")
                    a = input("> ")
                    if isYes(a) == True:
                        try:
                            import tkinter as tk
                            from tkinter import filedialog
                            root = tk.Tk()
                            root.withdraw()
                            folder_path = filedialog.askdirectory(title="Select an installation path to install the Bootstrap!", initialdir=default_app_path)
                            if folder_path and os.path.isdir(folder_path):
                                printMainMessage(f"You have selected the following folder to install the bootstrap into: {folder_path}")
                                printMainMessage(f"Example Resemblance: {os.path.join(folder_path, 'OrangeBlox', 'OrangeBlox.exe') if main_os == 'Windows' else os.path.join(folder_path, "OrangeBlox.app")}")
                                printMainMessage("Would you like to install into this folder? (y/n)")
                                if isYes(input("> ")):
                                    if folder_path and os.path.isdir(folder_path):
                                        if os.path.exists(os.path.join(folder_path, "OrangeBlox")):
                                            printErrorMessage("An OrangeBlox instance already exists in this folder!")
                                        else:
                                            if main_os == "Darwin":
                                                stored_main_app["OverallInstall"] = folder_path
                                                stored_main_app["Darwin"] = [
                                                    os.path.join(folder_path, "OrangeBlox.app/Contents/MacOS/OrangeBlox.app"), 
                                                    os.path.join(folder_path, "OrangeBlox.app"), 
                                                    os.path.join(folder_path, "Play Roblox.app"), 
                                                    os.path.join(folder_path, "Run Studio.app")
                                                ]
                                            elif main_os == "Windows":
                                                stored_main_app["OverallInstall"] = folder_path
                                                stored_main_app["Windows"] = [
                                                    os.path.join(folder_path, "OrangeBlox"), 
                                                    os.path.join(folder_path, "OrangeBlox", "OrangeBlox.exe"), 
                                                    os.path.join(folder_path, "OrangeBlox"), 
                                                    os.path.join(folder_path, "OrangeBlox")
                                                ]
                                    else:
                                        printMainMessage("Alright, it's your choice! In order to reselect, please restart setup!")
                                else:
                                    printMainMessage("Alright, it's your choice! In order to reselect, please restart setup!")
                            else:
                                printMainMessage("No folder was selected.")
                        except Exception as e:
                            printErrorMessage("There was an error selecting a folder!")
                    
                printMainMessage("Would you like to delete other operating system versions? (This may save 30MB+ of space) (y/n)")
                a = input("> ")
                if isYes(a) == False:
                    disable_remove_other_operating_systems = True
                if remove_unneeded_messages == False: printMainMessage("Alright now, last question, select carefully!")
                if overwrited == True:
                    printMainMessage("Do you want to update OrangeBlox? (This will reupdate all files based on this Installation folder.) (y/n)")
                else:
                    printMainMessage("Do you want to install OrangeBlox into your system? (y/n)")
                res = input("> ")
                if isYes(res) == True:
                    if remove_unneeded_messages == False: printMainMessage("Yippieee!!!")
                    try:
                        install()
                    except Exception as e:
                        printErrorMessage(f"Something went wrong during installation: {str(e)}")
                    input("> ")
                else:
                    if remove_unneeded_messages == False: printMainMessage("Aw, well, better next time! (..maybe)")
            else:
                def requestUpdate():
                    global disable_remove_other_operating_systems
                    printMainMessage("Would you like to delete other operating system versions? (This may save 30MB+ of space) (y/n)")
                    a = input("> ")
                    if isYes(a) == False:
                        disable_remove_other_operating_systems = True
                    printMainMessage("Do you want to update OrangeBlox? (This will reupdate all files based on this Installation folder.) (y/n)")
                    res = input("> ")
                    if isYes(res) == True:
                        if remove_unneeded_messages == False: printMainMessage("Yippieee!!!")
                        try:
                            install()
                        except Exception as e:
                            printErrorMessage(f"Something went wrong during installation: {str(e)}")
                        input("> ")
                    else:
                        if remove_unneeded_messages == False: printMainMessage("Aw, well, better next time! (..maybe)")
                def requestUninstall():
                    if main_os == "Darwin":
                        if not os.path.exists(f"{stored_main_app[found_platform][1]}/Contents/MacOS/OrangeBlox.app/"):
                            printMainMessage("OrangeBlox is not installed on this system.")
                            input("> ")
                            sys.exit(0)
                    elif main_os == "Windows":
                        if not os.path.exists(f"{stored_main_app[found_platform][0]}"):
                            printMainMessage("OrangeBlox is not installed on this system.")
                            input("> ")
                            sys.exit(0)
                    printMainMessage("Are you sure you want to uninstall OrangeBlox from your system? (This will remove the app from your system and reinstall Roblox.) (y/n)")
                    if repair_mode == False: 
                        res = input("> ")
                    else:
                        res = "y"
                    if isYes(res) == True:
                        if main_os == "Darwin":
                            if pip_class.getIfProcessIsOpened("OrangeBlox.app"):
                                printErrorMessage("Please close OrangeBlox.app first before continuing to uninstall!")
                                input("> ")
                                sys.exit(0)
                            else:
                                # Remove Apps
                                if os.path.exists(stored_main_app[found_platform][1]):
                                    printMainMessage("Removing from Applications Folder (Main Bootstrap)..")
                                    shutil.rmtree(stored_main_app[found_platform][1])
                                if os.path.exists(stored_main_app[found_platform][2]):
                                    printMainMessage("Removing from Applications Folder (Play Roblox)..")
                                    shutil.rmtree(stored_main_app[found_platform][2])
                                if os.path.exists(stored_main_app[found_platform][3]):
                                    printMainMessage("Removing from Applications Folder (Run Studio)..")
                                    shutil.rmtree(stored_main_app[found_platform][3])
                        elif main_os == "Windows":
                            if pip_class.getIfProcessIsOpened("OrangeBlox.exe"):
                                printErrorMessage("Please close OrangeBlox.exe first before continuing to uninstall!")
                                input("> ")
                                sys.exit(0)
                            else:
                                # Remove URL Schemes
                                printMainMessage("Resetting URL Schemes..")
                                try:
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
                                    def get_file_type_reg(extension):
                                        try:
                                            with winreg.OpenKey(winreg.HKEY_CLASSHKEY_CURRENT_USERES_ROOT, extension) as key:
                                                file_type, _ = winreg.QueryValueEx(key, "")
                                                return file_type
                                        except FileNotFoundError:
                                            return None
                                    def set_file_type_reg(extension, exe_path, file_type):
                                        try:
                                            import ctypes
                                            extension = extension if extension.startswith('.') else f'.{extension}'
                                            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{extension}") as key: winreg.SetValue(key, "", winreg.REG_SZ, file_type)
                                            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{file_type}\\shell\\open\\command") as key: winreg.SetValue(key, "", winreg.REG_SZ, f'"{exe_path}" "%1"')
                                            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{file_type}\\DefaultIcon") as key: winreg.SetValue(key, "", winreg.REG_SZ, f"{exe_path},0")
                                            ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x0000, None, None)
                                            printSuccessMessage(f'File Handling "{extension}" has been set for "{exe_path}"')
                                        except Exception as e:
                                            printErrorMessage(f"An error occurred: {e}")
                                    set_url_scheme("efaz-bootstrap", "")
                                    set_url_scheme("orangeblox", "")
                                    set_file_type_reg(".obx", "", "Uninstalled OrangeBlox")
                                    cur = handler.getCurrentClientVersion()
                                    cur_studio = handler.getRobloxInstallFolder(studio=True, directory=f"{pip_class.getLocalAppData()}\\Roblox\\Versions")
                                    if cur:
                                        if cur["success"] == True:
                                            set_url_scheme("roblox-player", f"{pip_class.getLocalAppData()}\\Roblox\\Versions\\{cur['version']}\\RobloxPlayerBeta.exe")
                                            set_url_scheme("roblox", f"{pip_class.getLocalAppData()}\\Roblox\\Versions\\{cur['version']}\\RobloxPlayerBeta.exe")
                                    if cur_studio:
                                        rbx_studio_beta = f"{cur_studio}\\RobloxStudioBeta.exe"
                                        set_url_scheme("roblox-studio", rbx_studio_beta)
                                        set_url_scheme("roblox-studio-auth", rbx_studio_beta)
                                        set_file_type_reg(".rbxl", rbx_studio_beta, "Roblox Place")
                                        set_file_type_reg(".rbxlx", rbx_studio_beta, "Roblox Place")
                                except Exception as e:
                                    printErrorMessage(f"Unable to reset URL schemes: {str(e)}")

                                # Remove Shortcuts
                                printMainMessage("Removing shortcuts..")
                                try:
                                    def remove_path(pat):
                                        if os.path.exists(pat): 
                                            os.remove(pat)
                                    import win32com.client # type: ignore
                                    def create_shortcut(target_path, shortcut_path, working_directory=None, icon_path=None):
                                        shell = win32com.client.Dispatch('WScript.Shell')
                                        if not os.path.exists(os.path.dirname(shortcut_path)): os.makedirs(os.path.dirname(shortcut_path))
                                        shortcut = shell.CreateShortcut(shortcut_path)
                                        shortcut.TargetPath = target_path
                                        if working_directory:
                                            shortcut.WorkingDirectory = working_directory
                                        if icon_path:
                                            shortcut.IconLocation = icon_path
                                        shortcut.save()
                                    remove_path(os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), 'Play Roblox.lnk'))
                                    remove_path(os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), 'Run Studio.lnk'))
                                    remove_path(os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), "OrangeBlox.lnk"))
                                    remove_path(os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs'), 'Play Roblox.lnk'))
                                    remove_path(os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs'), 'Run Studio.lnk'))
                                    remove_path(os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs'), "OrangeBlox.lnk"))
                                    if cur:
                                        if cur["success"] == True:
                                            create_shortcut(f"{pip_class.getLocalAppData()}\\Roblox\\Versions\\{cur['version']}\\RobloxPlayerBeta.exe", os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), 'Roblox Player.lnk'))
                                            create_shortcut(f"{pip_class.getLocalAppData()}\\Roblox\\Versions\\{cur['version']}\\RobloxPlayerBeta.exe", os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Roblox'), 'Roblox Player.lnk'))
                                    if cur_studio:
                                        if cur_studio["success"] == True:
                                            create_shortcut(f"{pip_class.getLocalAppData()}\\Roblox\\Versions\\{cur_studio['version']}\\RobloxStudioBeta.exe", os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), 'Roblox Studio.lnk'))
                                            create_shortcut(f"{pip_class.getLocalAppData()}\\Roblox\\Versions\\{cur_studio['version']}\\RobloxStudioBeta.exe", os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Roblox'), 'Roblox Studio.lnk'))
                                except Exception as e:
                                    printErrorMessage(f"Unable to remove shortcuts: {str(e)}")

                                # Remove from Windows' Program List
                                printMainMessage("Unmarking from Windows Program List..")
                                app_key = r"Software\OrangeBlox"
                                uninstall_key = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\OrangeBlox"
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
                        if repair_mode == False:
                            printMainMessage("Preparing to reinstall Roblox..")
                            RobloxFastFlagsInstaller.macOS_dir = "/Applications/Roblox.app"
                            RobloxFastFlagsInstaller.macOS_studioDir = "/Applications/RobloxStudio.app"
                            RobloxFastFlagsInstaller.macOS_beforeClientServices = "/Contents/MacOS/"
                            RobloxFastFlagsInstaller.macOS_installedPath = "/Applications/"
                            RobloxFastFlagsInstaller.windows_dir = f"{pip_class.getLocalAppData()}\\Roblox"
                            RobloxFastFlagsInstaller.windows_versions_dir = f"{RobloxFastFlagsInstaller.windows_dir}\\Versions"
                            RobloxFastFlagsInstaller.windows_player_folder_name = ""
                            RobloxFastFlagsInstaller.windows_studio_folder_name = ""
                            handler.installRoblox(debug=True, downloadInstaller=True, downloadChannel=None, copyRobloxInstallerPath=(main_os == "Windows" and f"{RobloxFastFlagsInstaller.windows_dir}\\RobloxPlayerInstaller.exe" or f"{RobloxFastFlagsInstaller.macOS_dir}{RobloxFastFlagsInstaller.macOS_beforeClientServices}RobloxPlayerInstaller.app"))
                            printSuccessMessage("Successfully uninstalled OrangeBlox and reinstalled Roblox!")
                            input("> ")
                    else:
                        if remove_unneeded_messages == False: printMainMessage("Aw, well, better next time! (..maybe)")
                def requestRepair():
                    global instant_install
                    global repair_mode
                    global overwrited
                    printMainMessage("Are you sure you want to repair/reinstall the bootstrap? (y/n)")
                    res = input("> ")
                    if isYes(res) == True:
                        repair_mode = True
                        if not os.path.exists(f"{current_path_location}/Apps/"):
                            printErrorMessage("Please use an installation folder to install a new version from before continuing to repair!")
                            input("> ")
                            sys.exit(0)
                        if main_os == "Darwin":
                            if pip_class.getIfProcessIsOpened("OrangeBlox.app"):
                                printErrorMessage("Please close OrangeBlox.app first before continuing to repair!")
                                input("> ")
                                sys.exit(0)
                        elif main_os == "Windows":
                            if pip_class.getIfProcessIsOpened("OrangeBlox.exe"):
                                printErrorMessage("Please close OrangeBlox.exe first before continuing to repair!")
                                input("> ")
                                sys.exit(0)
                        app_location = f"{current_path_location}/"
                        repair_path = f"{current_path_location}/RepairData/"
                        if os.path.exists(repair_path):
                            printYellowMessage("Repair Data already exists!")
                            shutil.rmtree(repair_path, ignore_errors=True)
                        else:
                            printMainMessage("Making Repair Data Folder..")
                            os.mkdir(repair_path)
                        printMainMessage("Finding app..")
                        if main_os == "Darwin":
                            app_location = f"{stored_main_app[found_platform][1]}/Contents/Resources/"
                        elif main_os == "Windows":
                            app_location = f"{stored_main_app[found_platform][0]}"
                        if not os.path.exists(app_location):
                            printErrorMessage("OrangeBlox is not installed!")
                            input("> ")
                            sys.exit(0)
                        printMainMessage("Copying Configuration.json..")
                        main_config = getSettings(os.path.join(app_location, "Configuration.json"))
                        with open(os.path.join(repair_path, "Configuration.json"), "w", encoding="utf-8") as f:
                            json.dump(main_config, f, indent=4)
                        printMainMessage("Copying AvatarEditorMaps..")
                        pip_class.copyTreeWithMetadata(os.path.join(app_location, "AvatarEditorMaps"), os.path.join(repair_path, "AvatarEditorMaps"), dirs_exist_ok=True, ignore_if_not_exist=True)
                        printMainMessage("Copying Cursors..")
                        pip_class.copyTreeWithMetadata(os.path.join(app_location, "Cursors"), os.path.join(repair_path, "Cursors"), dirs_exist_ok=True, ignore_if_not_exist=True)
                        printMainMessage("Copying DeathSounds..")
                        pip_class.copyTreeWithMetadata(os.path.join(app_location, "DeathSounds"), os.path.join(repair_path, "DeathSounds"), dirs_exist_ok=True, ignore_if_not_exist=True)
                        printMainMessage("Copying Mods..")
                        pip_class.copyTreeWithMetadata(os.path.join(app_location, "Mods"), os.path.join(repair_path, "Mods"), dirs_exist_ok=True, ignore_if_not_exist=True)
                        printMainMessage("Copying RobloxBrand..")
                        pip_class.copyTreeWithMetadata(os.path.join(app_location, "RobloxBrand"), os.path.join(repair_path, "RobloxBrand"), dirs_exist_ok=True, ignore_if_not_exist=True)
                        printMainMessage("Copying RobloxStudioBrand..")
                        pip_class.copyTreeWithMetadata(os.path.join(app_location, "RobloxStudioBrand"), os.path.join(repair_path, "RobloxStudioBrand"), dirs_exist_ok=True, ignore_if_not_exist=True)
                        printMainMessage("Creating Metadata..")
                        ver = current_version["version"]
                        if os.path.exists(os.path.join(app_location, "Version.json")):
                            ver_js = None
                            with open(os.path.join(app_location, "Version.json"), "r", encoding="utf-8") as f: ver_js = json.load(f)
                            if ver_js: ver = ver_js["version"]
                        with open(os.path.join(repair_path, "Metadata.json"), "w", encoding="utf-8") as f:
                            json.dump({
                                "installer_version": current_version["version"],
                                "bootstrap_version": ver,
                                "script_hash": generateFileHash(os.path.join(app_location, "Main.py")),
                            }, f, indent=4)
                        printMainMessage("Uninstalling Bootstrap..")
                        try:
                            requestUninstall()
                            printMainMessage("Redirecting to install mode.")
                            instant_install = True
                            overwrited = False
                            try:
                                install()
                                printMainMessage("Installation was a success! Preparing data..")
                                printMainMessage("Copying Configuration.json..")
                                if os.path.exists(os.path.join(repair_path, "FastFlagConfiguration.json")):
                                    with open(os.path.join(repair_path, "FastFlagConfiguration.json"), "r", encoding="utf-8") as f: main_config = json.load(f)
                                else:
                                    with open(os.path.join(repair_path, "Configuration.json"), "r", encoding="utf-8") as f: main_config = json.load(f)
                                saveSettings(main_config, directory=os.path.join(app_location, "Configuration.json"))
                                shutil.copy(os.path.join(repair_path, "Configuration.json"), os.path.join(app_location, "Configuration.json"))
                                printMainMessage("Copying AvatarEditorMaps..")
                                pip_class.copyTreeWithMetadata(os.path.join(repair_path, "AvatarEditorMaps"), os.path.join(app_location, "AvatarEditorMaps"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                printMainMessage("Copying Cursors..")
                                pip_class.copyTreeWithMetadata(os.path.join(repair_path, "Cursors"), os.path.join(app_location, "Cursors"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                printMainMessage("Copying DeathSounds..")
                                pip_class.copyTreeWithMetadata(os.path.join(repair_path, "DeathSounds"), os.path.join(app_location, "DeathSounds"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                printMainMessage("Copying Mods..")
                                pip_class.copyTreeWithMetadata(os.path.join(repair_path, "Mods"), os.path.join(app_location, "Mods"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                printMainMessage("Copying RobloxBrand..")
                                pip_class.copyTreeWithMetadata(os.path.join(repair_path, "RobloxBrand"), os.path.join(app_location, "RobloxBrand"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                printMainMessage("Copying RobloxStudioBrand..")
                                pip_class.copyTreeWithMetadata(os.path.join(repair_path, "RobloxStudioBrand"), os.path.join(app_location, "RobloxStudioBrand"), dirs_exist_ok=True, ignore_if_not_exist=True)
                                printMainMessage("Finished transferring! Deleting repair data..")
                                if os.path.exists(repair_path):
                                    shutil.rmtree(repair_path, ignore_errors=True)
                                printSuccessMessage("Successfully repaired OrangeBlox!")
                                input("> ")
                            except Exception as e:
                                printErrorMessage(f"Something went wrong during installation: {str(e)}")
                                printErrorMessage("Your data is saved inside the RepairData folder.")
                                input("> ")
                        except Exception as e:
                            printErrorMessage(f"Something went wrong during uninstallation: {str(e)}")
                            printErrorMessage("Your data is saved inside the RepairData folder.")
                            input("> ")
                def requestBackup():
                    global instant_install
                    global repair_mode
                    global overwrited
                    printMainMessage("Are you sure you want to backup bootstrap data? This will save to a new file called Backup.obx (y/n)")
                    res = input("> ")
                    if isYes(res) == True:
                        if main_os == "Darwin":
                            if pip_class.getIfProcessIsOpened("OrangeBlox.app"):
                                printErrorMessage("Please close OrangeBlox.app first before continuing to repair!")
                                input("> ")
                                sys.exit(0)
                        elif main_os == "Windows":
                            if pip_class.getIfProcessIsOpened("OrangeBlox.exe"):
                                printErrorMessage("Please close OrangeBlox.exe first before continuing to repair!")
                                input("> ")
                                sys.exit(0)
                        app_location = f"{current_path_location}/"
                        backup_path = f"{current_path_location}/Backup/"
                        if os.path.exists(backup_path):
                            printYellowMessage("Backup Folder already exists!")
                            shutil.rmtree(backup_path, ignore_errors=True)
                        else:
                            printMainMessage("Making Backup Folder..")
                            os.mkdir(backup_path)
                        printMainMessage("Finding app..")
                        if main_os == "Darwin":
                            app_location = f"{stored_main_app[found_platform][1]}/Contents/Resources/"
                        elif main_os == "Windows":
                            app_location = f"{stored_main_app[found_platform][0]}"
                        if not os.path.exists(app_location):
                            printErrorMessage("OrangeBlox is not installed!")
                            input("> ")
                            sys.exit(0)
                        printMainMessage("Copying Configuration.json..")
                        main_config = getSettings(os.path.join(app_location, "Configuration.json"))
                        with open(os.path.join(backup_path, "Configuration.json"), "w", encoding="utf-8") as f:
                            json.dump(main_config, f, indent=4)
                        printMainMessage("Copying AvatarEditorMaps..")
                        pip_class.copyTreeWithMetadata(os.path.join(app_location, "AvatarEditorMaps"), os.path.join(backup_path, "AvatarEditorMaps"), dirs_exist_ok=True, ignore_if_not_exist=True)
                        printMainMessage("Copying Cursors..")
                        pip_class.copyTreeWithMetadata(os.path.join(app_location, "Cursors"), os.path.join(backup_path, "Cursors"), dirs_exist_ok=True, ignore_if_not_exist=True)
                        printMainMessage("Copying DeathSounds..")
                        pip_class.copyTreeWithMetadata(os.path.join(app_location, "DeathSounds"), os.path.join(backup_path, "DeathSounds"), dirs_exist_ok=True, ignore_if_not_exist=True)
                        printMainMessage("Copying Mods..")
                        pip_class.copyTreeWithMetadata(os.path.join(app_location, "Mods"), os.path.join(backup_path, "Mods"), dirs_exist_ok=True, ignore_if_not_exist=True)
                        printMainMessage("Copying RobloxBrand..")
                        pip_class.copyTreeWithMetadata(os.path.join(app_location, "RobloxBrand"), os.path.join(backup_path, "RobloxBrand"), dirs_exist_ok=True, ignore_if_not_exist=True)
                        printMainMessage("Copying RobloxStudioBrand..")
                        pip_class.copyTreeWithMetadata(os.path.join(app_location, "RobloxStudioBrand"), os.path.join(backup_path, "RobloxStudioBrand"), dirs_exist_ok=True, ignore_if_not_exist=True)
                        printMainMessage("Creating Metadata..")
                        ver = current_version["version"]
                        if os.path.exists(os.path.join(app_location, "Version.json")):
                            ver_js = None
                            with open(os.path.join(app_location, "Version.json"), "r", encoding="utf-8") as f: ver_js = json.load(f)
                            if ver_js: ver = ver_js["version"]
                        with open(os.path.join(backup_path, "Metadata.json"), "w", encoding="utf-8") as f:
                            json.dump({
                                "installer_version": current_version["version"],
                                "bootstrap_version": ver,
                                "script_hash": generateFileHash(os.path.join(app_location, "Main.py")),
                            }, f, indent=4)
                        printMainMessage("Archiving Backup..")
                        file_dir = ""
                        for i in os.listdir(backup_path): 
                            file_dir = file_dir + f' "{i}"'
                        if main_os == "Darwin": subprocess.run(f'zip -r -y "../Backup.obx"{file_dir}', cwd=backup_path, shell=True)
                        elif main_os == "Windows": 
                            s = subprocess.run(f'powershell Compress-Archive -Path * -Update -DestinationPath ../Backup.zip', cwd=backup_path, shell=True)
                            if s.returncode == 0: os.rename(os.path.join(current_path_location, "Backup.zip"), os.path.join(current_path_location, 'Backup.obx'))
                        printMainMessage("Cleaning up..")
                        shutil.rmtree(backup_path, ignore_errors=True)
                        printSuccessMessage(f"Successfully backed up OrangeBlox data!")
                        printSuccessMessage(f"Application Path: {app_location}")
                        printSuccessMessage(f"File Path: {os.path.join(current_path_location, 'Backup.obx')}")
                        input("> ")
                if uninstall_mode == True:
                    requestUninstall()
                elif repair_argv_mode == True:
                    requestRepair()
                elif backup_mode == True:
                    requestBackup()
                else:
                    printMainMessage("Please select an installer option you want to do!")
                    printMainMessage("[1] = Update Bootstrap")
                    printMainMessage("[2] = Uninstall Bootstrap")
                    printMainMessage("[3] = Repair Bootstrap")
                    printMainMessage("[4] = Backup Bootstrap")
                    printMainMessage("[*] = Exit Installer")
                    res = input("> ")
                    if res == "1":
                        requestUpdate()
                    elif res == "2":
                        requestUninstall()
                    elif res == "3":
                        requestRepair()
                    elif res == "4":
                        requestBackup()
    if update_mode == True:
        if main_os == "Darwin":
            if os.path.exists(f"{stored_main_app[found_platform][1]}/Contents/MacOS/OrangeBlox.app/"):
                if not pip_class.getIfProcessIsOpened("/Terminal.app/Contents/MacOS/Terminal"):
                    printMainMessage("Opening Terminal.app in order for console to show..")
                    subprocess.Popen(f'open -j -F -a /System/Applications/Utilities/Terminal.app', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                printMainMessage("Loading OrangeBlox executable!")
                subprocess.Popen(f'open -n -a "{stored_main_app[found_platform][1]}/Contents/MacOS/OrangeBlox.app/Contents/MacOS/OrangeBlox"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            else:
                printErrorMessage("Bootstrap Launch Failed: App is not installed.")
        elif main_os == "Windows":
            generated_app_path = stored_main_app[found_platform][0]
            if os.path.exists(os.path.join(generated_app_path, "OrangeBlox.exe")):
                printMainMessage("Loading OrangeBlox.exe!")
                subprocess.Popen(f'{os.path.join(generated_app_path, "OrangeBlox.exe")}')
            else:
                printErrorMessage("Bootstrap Launch Failed: App is not installed.")
    sys.exit(0)
else:
    class OrangeBloxNotModule(Exception):
        def __init__(self): super().__init__("OrangeBlox is only a runable instance, not a module.")
    class OrangeBloxInstallerNotModule(Exception):
        def __init__(self): super().__init__("The installer for OrangeBlox is only a runable instance, not a module.")
    class OrangeBloxLoaderNotModule(Exception):
        def __init__(self): super().__init__("The loader for OrangeBlox is only a runable instance, not a module.")
    raise OrangeBloxInstallerNotModule()