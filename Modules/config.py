# 
# OrangeBlox 🍊
# Made by Efaz from efaz.dev
# v2.6.0f
# 

import os
import sys
import platform
import builtins
import typing

import PyKits; PyKits.BuiltinEditor(builtins)
try: import RobloxManager as rbx
except Exception: print("Restarting for module updates.."); PyKits.pip().restartScript("Main.py", sys.argv)

main_os: str = platform.system()
pip_class: PyKits.pip = PyKits.pip()
requests: PyKits.request = PyKits.request(throw_exceptions=False)
plist_class: PyKits.plist = PyKits.plist()
colors_class: PyKits.Colors = PyKits.Colors()
submit_status: PyKits.ProgressBar = PyKits.ProgressBar()
file_selector: PyKits.FileSelector = PyKits.FileSelector()
notification_socket: PyKits.Socket = PyKits.Socket(port=61239)
handler: rbx.Handler = rbx.Handler()
cur_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
content_folder_paths: typing.Dict[str, str] = {}
font_folder_paths: typing.Dict[str, str] = {}
current_global_setting_type: bool = False
modified_flags_from_mod_scripts: typing.List[str] = []
socket_authorization: str = None
skip_modification_mode: bool = False
preserve_roblox: bool = True
avoid_going_to_roblox: bool = False
installed_update: bool = False
connect_instead: bool = False
roblox_launched: bool = False
run_studio: bool = False
main_config: typing.Dict[str, typing.Union[str, int, bool, float, typing.Dict, typing.List]] = {}
custom_cookies: typing.Dict[str, str] = {}
stdout: PyKits.stdout = None
current_version: typing.Dict[str, str] = {"version": "2.6.0f"}
given_args: typing.List[str] = []
user_folder_name: str = os.path.basename(pip_class.getUserFolder())
mods_folder: str = os.path.join(cur_path, "Mods")
macos_app_path: str = (os.path.realpath(os.path.join(cur_path, "../", "../") + "/")) if main_os == "Darwin" else cur_path
user_folder: str = (os.path.expanduser("~") if main_os == "Darwin" else pip_class.getLocalAppData())
orangeblox_library: str = os.path.join(user_folder, "Library", "OrangeBlox")
versions_folder: str = os.path.join(cur_path, "Versions")
discord_rpc = None
discord_rpc_info = None
restartRoblox: typing.Callable = lambda: None
flag_types: typing.Dict[str, str] = {
    "EFlagRobloxStudioFlags": "dict",
    "EFlagRobloxPlayerFlags": "dict",
    "EFlagDisableAutosaveToInstallation": "bool",
    "EFlagOrangeBloxSyncDir": "path",
    "EFlagBootstrapRobloxInstallFolderName": "str",
    "EFlagBootstrapRobloxStudioInstallFolderName": "str",
    "EFlagRebuildClangAppFromSourceDuringUpdates": "bool",
    "EFlagRebuildPyinstallerAppFromSourceDuringUpdates": "bool",
    "EFlagRebuildNuitkaAppFromSourceDuringUpdates": "bool",
    "EFlagInstallEfazDevECCCertificates": "bool",
    "EFlagDisableDeleteOtherOSApps": "bool",
    "EFlagAvailableInstalledDirectories": "dict",
    "EFlagDisableURLSchemeInstall": "bool",
    "EFlagDisableShortcutsInstall": "bool",
    "EFlagRobloxBootstrapUpdatesAuthorizationKey": "EFlagUpdatesAuthorizationKey",
    "EFlagUpdatesAuthorizationKey": "str",
    "EFlagEnableDebugMode": "bool",
    "EFlagEnabledMods": "dict",
    "EFlagEnabledModOrder": "list",
    "EFlagMakeMainBootstrapLogFiles": "bool",
    "EFlagCompletedTutorial": "bool",
    "EFlagVerifyRobloxHashAfterInstall": "bool",
    "EFlagEnableDuplicationOfClients": "bool",
    "EFlagAllowActivityTracking": "bool",
    "EFlagDisableFastFlagInstallAccess": "bool",
    "EFlagBootstrapUpdateServer": "str",
    "EFlagLinkedComputerID": "str_local",
    "EFlagRobloxStudioEnabled": "bool",
    "EFlagRemoveRobloxAppDockShortcut": "bool",
    "EFlagFreshCopyRoblox": "bool",
    "EFlagRobloxPlayerArguments": "str",
    "EFlagRobloxStudioArguments": "str",
    "EFlagRobloxUnfriendCheckEnabled": "bool",
    "EFlagRobloxUnfriendCheckUserID": "int",
    "EFlagEnableSkipModificationMode": "bool",
    "EFlagDisableRobloxReopenAfterRestart": "bool",
    "EFlagDisableRobloxReinstallNeededChecks": "bool",
    "EFlagEnableMultiAutoReconnect": "bool",
    "EFlagEnableURLQuickLaunch": "bool",
    "EFlagEnableCPUMemoryUsageViewer": "bool",
    "EFlagNotifyServerLocation": "bool",
    "EFlagEnableDiscordRPC": "bool",
    "EFlagEnableDiscordRPCStudio": "bool",
    "EFlagEnableDiscordRPCJoining": "bool",
    "EFlagShowUserProfilePictureInsteadOfLogo": "bool",
    "EFlagShowUsernameInSmallImage": "bool",
    "EFlagAllowBloxstrapSDK": "bool",
    "EFlagAllowBloxstrapStudioSDK": "bool",
    "EFlagAllowPrivateServerJoining": "bool",
    "EFlagUseDiscordWebhook": "bool",
    "EFlagDiscordWebhookURL": "str",
    "EFlagDiscordWebhookUserId": "str",
    "EFlagDiscordWebhookConnect": "bool",
    "EFlagDiscordWebhookDisconnect": "bool",
    "EFlagDiscordWebhookRobloxAppStart": "bool",
    "EFlagDiscordWebhookRobloxAppClose": "bool",
    "EFlagDiscordWebhookRobloxCrash": "bool",
    "EFlagDiscordWebhookBloxstrapRPC": "bool",
    "EFlagDiscordWebhookGamePublished": "bool",
    "EFlagDiscordWebhookGameSaved": "bool",
    "EFlagDiscordWebhookShowPidInFooter": "bool",
    "EFlagForceReconnectOnStudioLost": "bool",
    "EFlagShowRunningAccountNameInTitle": "bool",
    "EFlagShowRunningGameInTitle": "bool",
    "EFlagShowDisplayNameInTitle": "bool",
    "EFlagSimplifiedEfazRobloxBootstrapPromptUI": "bool",
    "EFlagSkipEfazRobloxBootstrapPromptUI": "bool",
    "EFlagDisableBootstrapChecks": "bool",
    "EFlagDisablePythonUpdateChecks": "bool",
    "EFlagDisablePythonModuleUpdateChecks": "bool",
    "EFlagDisableBootstrapCooldown": "bool",
    "EFlagEnableTkinterDockMenu": "EFlagEnableGUIOptionMenus",
    "EFlagEnableGUIOptionMenus": "bool",
    "EFlagAllowFullDebugMode": "bool",
    "EFlagRobloxClientChannel": "str",
    "EFlagDisableRobloxUpdateChecks": "bool",
    "EFlagRobloxStudioClientChannel": "str",
    "EFlagDisableSecureHashSecurity": "bool",
    "EFlagDisableSettingsAccess": "bool",
    "EFlagRobloxLinkShortcuts": "dict",
    "EFlagRobloxCodesigningName": "str",
    "EFlagEnableMods": "bool",
    "EFlagSelectedModScripts": "dict",
    "EFlagRemoveBuilderFont": "bool",
    "EFlagAvatarEditorBackground": "str",
    "EFlagEnableChangeAvatarEditorBackground": "bool",
    "EFlagSelectedCursor": "str",
    "EFlagEnableChangeCursor": "bool",
    "EFlagSelectedBrandLogo": "str",
    "EFlagEnableChangeBrandIcons": "bool",
    "EFlagSelectedBrandLogo2": "str",
    "EFlagEnableChangeBrandIcons2": "bool",
    "EFlagShowGameNameInStatusBar": "bool",
    "EFlagShowStudioGameNameInStatusBar": "bool",
    "EFlagUseRobloxAppIconAsShortcutIcon": "bool",
    "EFlagReplaceRobloxRuntimeIconWithModIcon": "bool",
    "EFlagSelectedPlayerSounds": "str",
    "EFlagEnableChangePlayerSound": "bool",
    "EFlagDisableModsManagerAccess": "bool",
    "EFlagDisableModScriptsAccess": "bool",
    "EFlagDisableLinkShortcutsAccess": "bool",
    "EFlagReturnToMainMenuInstant": "bool",
    "EFlagRemoveCodeSigningMacOS": "bool",
    "EFlagModScriptRequestTooFastMessage": "bool",
    "EFlagModScriptAPIRefreshTime": "float",
    "EFlagRobloxUnfriendCheckCooldown": "int",
    "EFlagSetDiscordRPCStart": "int",
    "EFlagEndStudioPlaceWhenDisconnected": "bool",
    "EFlagDisableAutoOpenOrangeBloxFromStudio": "bool",
    "EFlagSpecifyPythonExecutable": "path",
    "EFlagEnableSecretJackpot": "bool",
    "EFlagBootstrapCooldownAmount": "int",
    "EFlagSelectedBootstrapLanguage": "str",
    "EFlagUseFollowingAppIconPath": "path",
    "EFlagEnableRoValraServerUptime": "bool",
    "EFlagUseConfigurationWebServer": "bool",
    "EFlagConfigurationWebServerURL": "str",
    "EFlagConfigurationAuthorizationKey": "str",
    "EFlagLimitAPIDocsLocalization": "str",
    "EFlagOverwriteUnneededStudioFonts": "bool",
    "EFlagEnableSeeMoreAwaiting": "bool",
    "EFlagEnableLoop429Requests": "bool",
    "EFlagEnableEndingRobloxCrashHandler": "bool",
    "EFlagEnablePythonVirtualEnvironments": "bool",
    "EFlagBuildPythonCacheOnStart": "bool",
    "EFlagEnableSlientPythonInstalls": "bool",
    "EFlagEnableDefaultDiscordRPC": "bool",
    "EFlagUseIXPFastFlagsMethod": "EFlagUseIXPFastFlagsMethod2",
    "EFlagUseIXPFastFlagsMethod2": "bool",
    "EFlagLastModVersionMacOSCaching": "str",
    "EFlagRobloxChannelUpdateToken": "str",
    "EFlagRobloxSecurityCookieUsage": "bool",
    "EFlagCustomBootstrapName": "str",
    "EFlagCustomBootstrapEmoji": "str",
    "EFlagCustomBootstrapColor": "str",
    "EFlagCustomBootstrapInternetURL": "str",
    "EFlagCustomBootstrapIconPath": "path",
    "EFlagUseEfazDevAPI": "bool"
}
_YES = {"y", "yes", "true", "t"}
_NO  = {"n", "no",  "false", "f"}
language_names: typing.Dict[str, str] = {
    "en": "English",
    "ar": "Arabic (العربية)",
    "bn": "Bengali (বাংলা)",
    "zh-cn": "Chinese (Simplified) (简体中文)",
    "zh-tw": "Chinese (Traditional) (繁體中文)",
    "da": "Danish (Dansk)",
    "de": "German (Deutsch)",
    "el": "Greek (Ελληνικά)",
    "fr": "French (Français)",
    "tl": "Filipino (Filipino)",
    "ka": "Georgian (ქართული)",
    "hi": "Hindi (हिन्दी)",
    "id": "Indonesian (Bahasa Indonesia)",
    "it": "Italian (Italiano)",
    "ja": "Japanese (日本語)",
    "ko": "Korean (한국어)",
    "pt": "Portuguese (Português)",
    "ru": "Russian (русский)",
    "es": "Spanish (Español)",
    "th": "Thai (ไทย)",
    "tr": "Turkish (Türkçe)",
    "uk": "Ukrainian (Українська)",
    "ur": "Urdu (اُردُو)",
    "vi": "Vietnamese (Tiếng Việt)"
}
updating_mods: typing.Dict[str, typing.List[str]] = {
    "PlayerSounds": ["Old", "Outdated", "Current"], 
    "AvatarEditorMaps": ["Old.rbxl", "Original.rbxl", "BobTheBuilder.rbxl", "SubwaySurfers.rbxl", "Template.rbxl", "McDonaldsWar.rbxl", "MHA.rbxl", "Backrooms.rbxl"], 
    "RobloxBrand": ["Roblox2011", "Roblox2015Red", "Roblox2021", "OrangeBlox", "Original", "Roblox2015", "Roblox2025", "Roblox2008"], 
    "RobloxStudioBrand": ["OrangeBlox", "Studio2025", "Studio2013", "Original", "Studio2015", "Studio2008", "StudioBlue2011", "StudioBlue2008", "Studio2017", "Studio2011"], 
    "Mods": ["VoiceChatRecorder", "Original", "Template", "KlikoModTool", "OldFont", "OrangeBot"], 
    "Cursors": ["2013", "macOS", "Original", "2006"]
}
special_logo_mods: typing.Dict[str, typing.List[str]] = {
    "reg": updating_mods["RobloxBrand"],
    "studio": updating_mods["RobloxStudioBrand"]
}
main_host: str = ("https://obx.efaz.dev" if current_version["version"].split(".")[2].isdigit() else "https://obxbeta.efaz.dev")

if __name__ == "__main__":
    print("This module is not a runable instance.")
    sys.exit(1)