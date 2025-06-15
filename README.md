<h1 align="center"><img align="center" src="https://obx.efaz.dev/BootstrapImages/Banner.png" height="50%" width="50%"></h1>
<h2 align="center">Push your Roblox limitations to a new level!</h2>
<p align="center">
    <a href="https://github.com/EfazDev/orangeblox/releases/latest"><img src="https://img.shields.io/github/v/release/EfazDev/orangeblox?color=ff4b00&label=%F0%9F%94%84%20Version" alt="Version"></a>
    <a href="https://github.com/EfazDev/orangeblox/releases/latest"><img src="https://img.shields.io/github/downloads/EfazDev/orangeblox/latest/total?color=ff4b00&label=%F0%9F%92%BB%20Downloads%20(Latest)" alt="Downloads"></a>
    <a href="https://github.com/EfazDev/orangeblox/releases"><img src="https://img.shields.io/github/downloads/EfazDev/orangeblox/total?color=ff4b00&label=%F0%9F%92%BB%20Downloads%20(All%20Time)" alt="Downloads"></a>
    <a href="https://github.com/EfazDev/orangeblox"><img src="https://img.shields.io/github/stars/EfazDev/orangeblox?style=smooth&label=%E2%AD%90%20Stars&color=ff4b00" alt="Stars"></a>    
    <a href="https://twitter.efaz.dev"><img src="https://img.shields.io/twitter/follow/EfazDev?style=social&labelColor=00ffff&color=00ffff" alt="Twitter"></a>
    <a href="https://discord.efaz.dev"><img src="https://img.shields.io/discord/1099350065560166543?logo=discord&logoColor=white&label=discord&color=4d3dff" alt="Discord"></a>    
</p>
<p align="center">
    <img align="center" src="https://obx.efaz.dev/BootstrapImages/Collage.png" height="50%" width="50%" alt="Server Location Notification"><br>
</p>

> [!IMPORTANT]
> Hello! If you were an user of Efaz's Roblox Bootstrap on v1.5.9 or lower, you might have noticed we have rebranded to OrangeBlox! Any mods and data are transferred as of this change and your mod scripts are able to still work under the EfazRobloxBootstrapAPI. However, you'll have to install manually rather than automatically downloading from the bootstrap. For more information, [click here.](https://github.com/efazdev/orangeblox/wiki/Rebranding-to-OrangeBlox)

## What is OrangeBlox?
OrangeBlox is a Python [Console](https://www.google.com/search?q=developer+console+terminal&udm=2) program heavily inspired by Bloxstrap made for macOS and Windows! It also uses [Activity Tracking](https://github.com/pizzaboxer/bloxstrap/wiki/What-is-activity-tracking%3F), supports [BloxstrapRPC](https://github.com/pizzaboxer/bloxstrap/wiki/Integrating-Bloxstrap-functionality-into-your-game) and a lot more!

## Features
1. Set FFlag and Global Setting Customizations on your Roblox installation!
2. Install Mods including a custom Avatar Map, App Icon, Cursor, and Death Sound!
3. Customize with unlimited mods that you can download and insert an extracted folder copy into the Mods folder! *[Requires to go through bootstrap in Mods Manager]
4. Use multiple instances directly by launching from your default web browser or the OrangeBlox app!
5. Get server locations when joining (courtesy of ipinfo.io)
6. Apply the same experience to Roblox Studio with mods!
7. Discord Rich Presences [Includes Support for BloxstrapRPC]
8. Roblox Studio Support with Mods and FFlags! *[FFlags may not work due to future Roblox updates]
9. Discord Webhooks [Join, Disconnect, Teleport, Crash, BloxstrapRPC and More Notifications!]
10. Run Python Scripts based on events ran on the Roblox client using Mod Scripts!
11. Play Roblox/Run Studio app so you can run Roblox directly!
12. Read Logs from Roblox using RobloxFastFlagsInstaller* (requires Debug Mode)!
13. + Way more features that can be explored!

## Requirements
1. [Latest ZIP of OrangeBlox](https://github.com/EfazDev/orangeblox/releases/latest)
2. [Windows 10.0.17134+ (April 2018)](https://www.microsoft.com/en-us/software-download/) or [macOS 10.13+ (High Sierra)](https://apps.apple.com/us/app/macos-high-sierra/id1246284741)
3. [Python 3.11+](https://www.python.org/downloads/) (You may install Python 3.13.5 from InstallPython.bat (Windows) or from InstallPython.sh (macOS))
4. Python Modules: <br>
   macOS: pip install pypresence pyobjc-core pyobjc-framework-Quartz pyobjc-framework-Cocoa posix-ipc requests plyer psutil <br>
   Windows: pip install pypresence requests pywin32 plyer psutil

## Install
1. Once you have installed Python 3.11 or higher and downloaded the ZIP file, extract the full ZIP into a new folder.
2. After you have EXTRACTED the folder, open it and make sure you see Install.py. Once you do, run it.
2. Complete the installation process and once it says success, run the bootstrap by using the Launchpad for macOS or by using the Search Menu for Windows.
3. Complete the tutorial about how to use the bootstrap.
4. Done! You have installed OrangeBlox!
> [!NOTE]
> If there's an error during the installation process, try checking if your computer is supported or if something was edited that may cause this error. macOS may also edit permissions of the files if run under an admin account, keep an insight of that.

## Anti-Virus Information
> [!IMPORTANT]
> OrangeBlox is a safe Windows/macOS program and won't harm your Roblox account. However, compilers like Nuitka and pyinstaller may have some issues where apps created contain false positives from anti-virus software. For example, Windows Defender may detect the bootstrap with Win32/Wacapew.C!ml. In order to prevent this, you may need to authorize the app through your anti-virus or build the app directly.

## Python 3.14 Beta Support
> [!IMPORTANT]
> OrangeBlox is somewhat compatible with beta versions of Python such as Python 3.14. However, Pypi packages such as pyobjc, Nuitka/pyinstaller, psutil and plyer will all need to support the Python beta in order to work with OrangeBlox. Using beta versions of Python is only recommended for developers that know what they're doing and is not recommended for public use.

## Hashes
| File | MD5 Hash |
| --- | --- |
| Main Bootstrap (Main.py) | `b67f858d3b5831891d27ac4afdaa6ebf` |
| Roblox FFlag Installer (RobloxFastFlagsInstaller.py) | `1f69e7392d6b4f1e0f334cf0ea7b23e3` |
| Installer (Install.py) | `0a199ba4d11d8fd125fd35eba2f76293` |
| Bootstrap API (OrangeAPI.py) | `3fc02a417f21dc96e6683f43bd117381` |
| Bootstrap API (Efaz's Roblox Bootstrap) (EfazRobloxBootstrapAPI.py) | `b7978c8b7faf890eb2aacf21440d43c6` |
| Bootstrap Loader (OrangeBlox.py) | `5b12ad8570fde8f27897a75a37acbe7b` |
| Discord Presence Handler (DiscordPresenceHandler.py) | `a417cda5ca6e07b78540b49a871b253a` |
| Pip Handler (PipHandler.py) | `a25f43b23109725094cde3c95c34f3ad` |

## Credits
1. Made by <a href="https://www.efaz.dev"><img src="https://img.shields.io/static/v1?label=&color=ff4b00&message=@EfazDev%20%F0%9F%8D%8A" style="margin-bottom: -4px;" alt="@EfazDev 🍊"></a>
2. Old Death Sound and Cursors were sourced from <a href="https://github.com/pizzaboxer/bloxstrap"><img src="https://img.shields.io/static/v1?label=&color=bb00ff&message=Bloxstrap%20%F0%9F%8E%AE" style="margin-bottom: -4px;" alt="Bloxstrap 🎮"></a>
3. Avatar Editor Maps were from <a href="https://github.com/Mielesgames/RobloxAvatarEditorMaps"><img src="https://img.shields.io/static/v1?label=&color=ff0062&message=Mielesgames%27s%20Map%20Files%20%F0%9F%97%BA%EF%B8%8F" style="margin-bottom: -4px;" alt="Mielesgames's Map Files 🗺️"></a> slightly edited to be usable for the current version of Roblox (as of the time of writing this)
4. Server Locations was made thanks to <a href="https://ipinfo.io/"><img src="https://img.shields.io/static/v1?label=&color=00AFFF&message=ipinfo.io%20%F0%9F%8C%90" style="margin-bottom: -4px;" alt="ipinfo.io 🌐"></a> as it wouldn't be possible to get IP address locations without them!
5. The logo of OrangeBlox was made thanks of <a href="https://twitter.com/_Cabled_"><img src="https://img.shields.io/static/v1?label=&color=ffff00&message=@CabledRblx%20%F0%9F%A6%86" style="margin-bottom: -4px;" alt="@CabledRblx 🦆"></a>. Thanks :)
6. macOS App was built using <a href="https://nuitka.net/"><img src="https://img.shields.io/static/v1?label=&color=FFFF00&message=Nuitka%20%F0%9F%93%A6" style="margin-bottom: -4px;" alt="Nuitka 📦"></a>. You can recreate and deploy using this command: `python3 Install.py --rebuild-mode --rebuild-nuitka --rebuild-clang`
7. Windows App was built using <a href="https://pyinstaller.org/en/stable/"><img src="https://img.shields.io/static/v1?label=&color=00AFFF&message=pyinstaller%20%F0%9F%93%A6" style="margin-bottom: -4px;" alt="pyinstaller 📦"></a>. You can recreate and deploy using this command: `python3 Install.py --rebuild-mode --rebuild-pyinstaller --full-rebuild`
> [!IMPORTANT]
> This command can be used using the native operating system your computer has. You will also need to run the rebuilding process in the OrangeBlox folder as current path. For Windows, in order to build a x86 exe file in x64, install Python in x86 and include the `--full-rebuild` argument. The argument `--rebuild-clang` is only available in macOS and requires Xcode Command Tools to be installed. Nuitka requires a C compiler to be installed on your computer in order to build. For Windows, use Microsoft Visual Studio 2022 compilation. For more information about Nuitka compiling, use this manual: https://nuitka.net/user-documentation/user-manual.html