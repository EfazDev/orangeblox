<h1 align="center"><img align="center" src="https://github.com/EfazDev/roblox-bootstrap/blob/main/BootstrapImages/AppIcon.png?raw=true" width="40" height="40"> Efaz's Roblox Bootstrap</h1>
<h2 align="center">Push your Roblox limitations to a new level!</h2>
<p align="center">
    <a href="https://github.com/EfazDev/roblox-bootstrap/releases/latest"><img src="https://img.shields.io/github/v/release/EfazDev/roblox-bootstrap?color=7a39fb" alt="Version"></a>
    <a href="https://github.com/EfazDev/roblox-bootstrap"><img src="https://img.shields.io/github/stars/EfazDev/roblox-bootstrap?style=plastic&label=%E2%AD%90%20Stars&color=ffff00" alt="Stars"></a>    
    <a href="https://twitter.efaz.dev"><img src="https://img.shields.io/twitter/follow/EfazDev?style=social&labelColor=00ffff&color=00ffff" alt="Twitter"></a>
    <a href="https://discord.efaz.dev"><img src="https://img.shields.io/discord/1099350065560166543?logo=discord&logoColor=white&label=discord&color=4d3dff" alt="Discord"></a>    
</p>
<p align="center">
    <img align="center" src="https://github.com/EfazDev/roblox-bootstrap/blob/main/BootstrapImages/MultipleInstances.png?raw=true" alt="Multiple Roblox Instances with Pet Simulator 99 Opened">
    <br>
    <img align="center" src="https://github.com/EfazDev/roblox-bootstrap/blob/main/BootstrapImages/AvatarEditor.png?raw=true" alt="Subway Surfers Avatar Map">
    <br>
    <img align="center" src="https://github.com/EfazDev/roblox-bootstrap/blob/main/BootstrapImages/ServerLocations.png?raw=true" alt="Server Location Notification">
    <br>
    <img align="center" src="https://github.com/EfazDev/roblox-bootstrap/blob/main/BootstrapImages/DiscordPresences.png?raw=true" alt="Discord Rich Presences">
</p>

## What is this?
Efaz's Roblox Bootstrap is a Python program heavily inspired by Bloxstrap made for macOS and Windows! It also uses [Activity Tracking](https://github.com/pizzaboxer/bloxstrap/wiki/What-is-activity-tracking%3F), supports [BloxstrapRPC](https://github.com/pizzaboxer/bloxstrap/wiki/Integrating-Bloxstrap-functionality-into-your-game) and lot more!

## Features
1. Set FFlag Customizations on your Roblox installation!
2. Set a custom Avatar Map, App Icon, Cursor, and Death Sound!
3. Customize with unlimited mods that you can download and insert an extracted folder copy into the Mods folder! *[Requires to go through bootstrap in Mods Manager]
4. Use multiple instances directly by launching from your default web browser or the EfazRobloxBootstrap app!
5. Get server locations when joining (also uses ipinfo.io like Bloxstrap)
6. Discord Rich Presences [Includes Support for BloxstrapRPC]
7. Discord Webhooks [Join, Disconnect, Teleport, Crash, App Start, App Close, Bloxstrap RPC Notifications]
8. Run Python Scripts based on events ran on the Roblox client using Mod Mode Scripts! *[One script limit]
9. Play Roblox app so you can run Roblox directly!
10. Read Logs from Roblox using RobloxFastFlagsInstaller and Debug Mode!

## Requirements
1. [Full ZIP file](https://github.com/EfazDev/roblox-bootstrap/archive/refs/heads/main.zip)
2. [Python 3.10+](https://www.python.org/downloads/) (You may install Python 3.13.0 from InstallPython.bat (Windows) or from InstallPython.sh (macOS))
3. Python Modules: pip install pypresence pyobjc posix-ipc requests plyer (For Windows: pip install pypresence requests pywin32 plyer)
> [!NOTE]
> Python 3.10 is not tested with the bootstrap, it may work though.

## Install
1. Once you have installed Python 3.10 or higher and downloaded the ZIP file, extract the full ZIP into a new folder.
2. After you have EXTRACTED the folder, open it and make sure you see Install.py. Once you do, run it.
2. Complete the installation process and once it says success, run the bootstrap by using the Launchpad for macOS or by using the Search Menu for Windows.
3. Complete the tutorial about how to use the bootstrap.
4. Done! You have installed Efaz's Roblox Bootstrap!
> [!NOTE]
> If there's an error during the installation process, try checking if your computer is supported or if something was edited that may cause this error.

## Anti-Virus Information
> [!IMPORTANT]
> Efaz's Roblox Bootstrap is a safe Windows/macOS program and won't harm your Roblox client or your account (unless you have installed shady scripts/software and the app was modified). However, pyinstaller has some issues where apps created contain false positives from anti-virus software. For example, Windows Defender would result with Win32/Wacapew.C!ml. You may need to authorize the app or use the x86 app instead (Windows only, python Install.py --use-x86-windows) in order to allow use.

## Hashes
Main Bootstrap (Main.py): `643019857e86beb00de91888fb27a886d898526bbff5d5e5a7ad0c0069388ae9`<br>
Roblox FFlag Installer (RobloxFastFlagsInstaller.py): `15e27fc47d934aa39085751dc23e5f041257d9b921a919011f771ffba6e99391`<br>
Installer (Install.py): `d01417e48f1fdc0d804a2782c81e97646be648a48393047491297070d1728d14`<br>
Bootstrap API (EfazRobloxBootstrapAPI.py): `819b22a2a642f05f405d009f5765e903de1fb77aa1071d96736bd814217453d8`<br>
Discord Presence Handler (DiscordPresenceHandler.py): `013c2a690f87e40b11370acbec4cb6c41e446522505ff827948362bd1188dec8`<br>

## Credits
1. Made by <span style="color:#FF8700">@EfazDev</span>
2. Old Death Sound and Cursors were sourced from <span style="color:#FF5FFF">[Bloxstrap files](https://github.com/pizzaboxer/bloxstrap)</span>
3. AvatarEditorMaps were from <span style="color:#FF00FF">[Mielesgames's Map Files](https://github.com/Mielesgames/RobloxAvatarEditorMaps)</span> slightly edited to be usable for the current version of Roblox (as of the time of writing this)
4. Some files were exported from the main macOS Roblox.app or Bloxstrap files. <span style="color:#FF8700">(Logo was from the Apple Pages icon, recolored and then added the Roblox Logo)</span>
5. macOS and Windows App was built using <span style="color:#00AFFF">pyinstaller</span>. You can recreate and deploy using this command: `python3 Install.py --rebuild-mode --rebuild-pyinstaller --rebuild-clang --full-rebuild-macOS-intel-arm64`
> [!IMPORTANT]
> This command can be used using the native operating system your computer has. You will also need to run the rebuilding process in the EfazRobloxBootstrap folder as current path. In order to create a x86 exe file from x64 for Windows, use Python 3.13.0 in x86 (32-bit). Additionally, change `python3` to the Python Executable if python3 is not available as a command tool and --rebuild-clang is only available in macOS and requires Xcode Command Tools to be installed while --full-rebuild-macOS-intel-arm64 is only available just in macOS.