<h1 align="center"><img align="center" src="https://obx.efaz.dev/BootstrapImages/Banner.png" height="50%" width="50%"></h1>
<h2 align="center">Push your Roblox limitations to a new level!</h2>
<p align="center">
    <a href="https://github.com/EfazDev/orangeblox/releases/latest"><img src="https://img.shields.io/github/v/release/EfazDev/orangeblox?color=ff4b00&label=%F0%9F%94%84%20Version" alt="Version"></a>
    <a href="https://github.com/EfazDev/orangeblox/releases/latest"><img src="https://img.shields.io/github/downloads/EfazDev/orangeblox/total?color=ff4b00&label=%F0%9F%92%BB%20Downloads" alt="Downloads"></a>
    <a href="https://github.com/EfazDev/orangeblox"><img src="https://img.shields.io/github/stars/EfazDev/orangeblox?style=smooth&label=%E2%AD%90%20Stars&color=ff4b00" alt="Stars"></a>    
    <a href="https://twitter.efaz.dev"><img src="https://img.shields.io/twitter/follow/EfazDev?style=social&labelColor=00ffff&color=00ffff" alt="Twitter"></a>
    <a href="https://discord.efaz.dev"><img src="https://img.shields.io/discord/1099350065560166543?logo=discord&logoColor=white&label=discord&color=4d3dff" alt="Discord"></a>    
</p>
<p align="center">
    <img align="center" src="https://obx.efaz.dev/BootstrapImages/ServerLocations.png" height="50%" width="50%" alt="Server Location Notification"><br>
    <p align="center">
        <img src="https://obx.efaz.dev/BootstrapImages/WebhookPlayer.png" alt="Server Location Notification">
        <img src="https://obx.efaz.dev/BootstrapImages/WebhookStudio.png" alt="Server Location Notification">
    </p>
    <p align="center">
        <img src="https://obx.efaz.dev/BootstrapImages/PlayerRPC.png" alt="Player Discord Rich Presence">
        <img src="https://obx.efaz.dev/BootstrapImages/StudioRPC.png" alt="Studio Discord Rich Presence">
    </p>
    <p align="center">
        <img align="center" src="https://obx.efaz.dev/BootstrapImages/AvatarEditor.png" height="500" width="800" alt="Subway Surfers Avatar Map"><br><br><img align="center" src="https://obx.efaz.dev/BootstrapImages/MultipleInstance.png" alt="Multiple Roblox Instances with Pet Simulator 99 Opened">
    </p>
</p>

> [!IMPORTANT]
> Hello! If you were an user of Efaz's Roblox Bootstrap on v1.5.9 or lower, you might have noticed we have rebranded to OrangeBlox! Any mods and data are transferred as of this change and your mod scripts are able to still work under the EfazRobloxBootstrapAPI. However, you'll have to install manually rather than automatically downloading from the bootstrap. For more information, [click here.](https://github.com/efazdev/orangeblox/wiki/Rebranding-to-OrangeBlox)

## What is OrangeBlox?
OrangeBlox is a Python program heavily inspired by Bloxstrap made for macOS and Windows! It also uses [Activity Tracking](https://github.com/pizzaboxer/bloxstrap/wiki/What-is-activity-tracking%3F), supports [BloxstrapRPC](https://github.com/pizzaboxer/bloxstrap/wiki/Integrating-Bloxstrap-functionality-into-your-game) and a lot more!

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
10. Run Python Scripts based on events ran on the Roblox client using Mod Scripts! *[One script limit]
11. Play Roblox/Run Studio app so you can run Roblox directly!
12. Read Logs from Roblox using RobloxFastFlagsInstaller* (requires Debug Mode)!
13. + Way more features that can be explored!

## Requirements
1. [Latest ZIP of OrangeBlox](https://github.com/EfazDev/orangeblox/releases/latest)
2. [Python 3.11+](https://www.python.org/downloads/) (You may install Python 3.13.3 from InstallPython.bat (Windows) or from InstallPython.sh (macOS))
3. Python Modules: <br>
   macOS: pip install pypresence pyobjc-core pyobjc-framework-Quartz pyobjc-framework-Cocoa posix-ipc requests plyer <br>
   Windows: pip install pypresence requests pywin32 plyer

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
> OrangeBlox is a safe Windows/macOS program and won't harm your Roblox account. However, pyinstaller has some issues where apps created contain false positives detecting from anti-virus software. For example, Windows Defender may detect the bootstrap with Win32/Wacapew.C!ml. You may need to authorize the app through your anti-virus or build the app directly in order to allow use.

## Hashes
| File | MD5 Hash |
| --- | --- |
| Main Bootstrap (Main.py) | `4157adee276734e322ba9a4c85e4ac5b` |
| Roblox FFlag Installer (RobloxFastFlagsInstaller.py) | `63c702f983aa462bab4af9ad54f34436` |
| Installer (Install.py) | `d616a3262d4252876139f361740451f0` |
| Bootstrap API (OrangeAPI.py) | `04caac38eed270bbe8e3f9e2e35f9d44` |
| Discord Presence Handler (DiscordPresenceHandler.py) | `4750ac894f5154d8be739f5f662f6165` |
| Pip Handler (PipHandler.py) | `9020b79a78e958a5622d68358b6d5ba7` |

## Credits
1. Made by <a href="https://www.efaz.dev"><img src="https://img.shields.io/static/v1?label=&color=ff4b00&message=@EfazDev%20%F0%9F%8D%8A" style="margin-bottom: -4px;" alt="@EfazDev 🍊"></a>
2. Old Death Sound and Cursors were sourced from <a href="https://github.com/pizzaboxer/bloxstrap"><img src="https://img.shields.io/static/v1?label=&color=bb00ff&message=Bloxstrap%20%F0%9F%8E%AE" style="margin-bottom: -4px;" alt="Bloxstrap 🎮"></a>
3. Avatar Editor Maps were from <a href="https://github.com/Mielesgames/RobloxAvatarEditorMaps"><img src="https://img.shields.io/static/v1?label=&color=ff0062&message=Mielesgames%27s%20Map%20Files%20%F0%9F%97%BA%EF%B8%8F" style="margin-bottom: -4px;" alt="Mielesgames's Map Files 🗺️"></a> slightly edited to be usable for the current version of Roblox (as of the time of writing this)
4. Server Locations was made thanks to <a href="https://ipinfo.io/"><img src="https://img.shields.io/static/v1?label=&color=00AFFF&message=ipinfo.io%20%F0%9F%8C%90" style="margin-bottom: -4px;" alt="ipinfo.io 🌐"></a> as it wouldn't be possible to convert ip addresses without them!
5. The logo of OrangeBlox was made thanks of <a href="https://twitter.com/_Cabled_"><img src="https://img.shields.io/static/v1?label=&color=ffff00&message=@CabledRblx%20%F0%9F%A6%86" style="margin-bottom: -4px;" alt="@CabledRblx 🦆"></a>. Thanks :)
6. macOS and Windows App was built using <a href="https://pyinstaller.org/en/stable/"><img src="https://img.shields.io/static/v1?label=&color=00AFFF&message=pyinstaller%20%F0%9F%93%A6" style="margin-bottom: -4px;" alt="pyinstaller 📦"></a>. You can recreate and deploy using this command: `python3 Install.py --rebuild-mode --rebuild-pyinstaller --rebuild-clang --full-rebuild`
> [!IMPORTANT]
> This command can be used using the native operating system your computer has. You will also need to run the rebuilding process in the OrangeBlox folder as current path. For Windows, in order to build a x86 exe file in x64, use Python in x86 and include the `--full-rebuild` argument. Arguments `--rebuild-clang` is only available in macOS and requires Xcode Command Tools to be installed