from typing import Optional
import time
import platform

from mod_generator.modules import Logger

import requests
from requests import Response, ConnectionError


COOLDOWN: float = 2
TIMEOUT: tuple[int,int] = (5,15)
_cache: dict = {}

def getLatestRobloxStudioAppSettings(debug=False, bootstrapper=False, bucket=""):
    # Mac: https://clientsettingscdn.roblox.com/v2/settings/application/MacStudioApp
    # Windows: https://clientsettingscdn.roblox.com/v2/settings/application/PCStudioApp
    try:    
        if bucket == "LIVE" or bucket == "production": bucket = ""
        if platform.system() == "Darwin":
            res = requests.get(f"https://clientsettingscdn.roblox.com/v2/settings/application/{bootstrapper == True and 'MacStudioBootstrapper' or 'MacStudioApp'}{not bucket == '' and f'/bucket/{bucket}' or ''}")
            if res.ok:
                jso = res.json()
                if jso.get("applicationSettings"):
                    return {"success": True, "application_settings": jso.get("applicationSettings")}
                else:
                    return {"success": False, "message": "Something went wrong."}
            else:
                return {"success": False, "message": "Something went wrong."}
        elif platform.system() == "Windows":
            res = requests.get(f"https://clientsettingscdn.roblox.com/v2/settings/application/{bootstrapper == True and 'PCStudioBootstrapper' or 'PCStudioApp'}{not bucket == '' and f'/bucket/{bucket}' or ''}")
            if res.ok:
                jso = res.json()
                if jso.get("applicationSettings"):
                    return {"success": True, "application_settings": jso.get("applicationSettings")}
                else:
                    return {"success": False, "message": "Something went wrong."}
            else:
                return {"success": False, "message": "Something went wrong."}
        else:
            return {"success": False, "message": "OS not compatible."}
    except Exception as e:
        return {"success": False, "message": "There was an error checking. Please check your internet connection!"}

# region APIs
class Api:
    class GitHub:
        LATEST_VERSION: str = r"https://raw.githubusercontent.com/TheKliko/klikos-modloader/refs/heads/main/GitHub%20Files/version.json"
        RELEASE_INFO: str = r"https://api.github.com/repos/thekliko/klikos-modloader/releases/latest"
        FILEMAP: str = r"https://raw.githubusercontent.com/TheKliko/klikos-modloader/refs/heads/config/filemap.json"
        MOD_GENERATOR_BLACKLIST: str = r"https://raw.githubusercontent.com/TheKliko/klikos-modloader/refs/heads/config/mod_generator_blacklist.json"
        FASTFLAG_PRESETS: str = r"https://raw.githubusercontent.com/TheKliko/klikos-modloader/refs/heads/config/fastflag_presets.json"
        MARKETPLACE: str = r"https://raw.githubusercontent.com/TheKliko/klikos-modloader/refs/heads/remote-mod-downloads/index.json"
        @staticmethod
        def mod_thumbnail(id: str) -> str:
            return rf"https://raw.githubusercontent.com/TheKliko/klikos-modloader/refs/heads/remote-mod-downloads/thumbnails/{id}.png"
        @staticmethod
        def mod_download(id: str) -> str:
            return rf"https://raw.githubusercontent.com/TheKliko/klikos-modloader/refs/heads/remote-mod-downloads/mods/{id}.zip"
    
    class Roblox:
        FASTFLAGS: str = r"https://clientsettingscdn.roblox.com/v2/settings/application/PCDesktopClient"

        class Deployment:
            HISTORY: str = r"https://setup.rbxcdn.com/DeployHistory.txt"
            HISTORY2: str = r"https://setup.rbxcdn.com/mac/DeployHistory.txt"
            @staticmethod
            def channel(binaryType: str) -> str:
                return rf"https://clientsettings.roblox.com/v2/user-channel?binaryType={binaryType}"
            @staticmethod
            def latest(binaryType: str, channel: Optional[str] = None) -> str:
                if channel is None:
                    return rf"https://clientsettingscdn.roblox.com/v2/client-version/{binaryType}"
                return rf"https://clientsettingscdn.roblox.com/v2/client-version/{binaryType}/channel/{channel}"
            @staticmethod
            def manifest(version: str, rbx_channel: str, macos: bool) -> str:
                starter_url = "channel/common/"
                bootstrapper_settings = getLatestRobloxStudioAppSettings(bootstrapper=True, bucket=rbx_channel)
                if bootstrapper_settings["success"] == True:
                    bootstrapper_settings = bootstrapper_settings["application_settings"]
                    if bootstrapper_settings.get("FFlagReplaceChannelNameForDownload"):
                        starter_url = "channel/common/"
                    else:
                        starter_url = f"channel/{rbx_channel.lower()}/"
                link_start = f"https://setup.rbxcdn.com/{starter_url}"
                if macos == True: link_start = f"https://setup.rbxcdn.com/{starter_url}mac/"
                return rf"{link_start}{version}-rbxPkgManifest.txt"
            @staticmethod
            def download(version: str, file: str, rbx_channel: str, macos: bool) -> str:
                starter_url = "channel/common/"
                bootstrapper_settings = getLatestRobloxStudioAppSettings(bootstrapper=True, bucket=rbx_channel)
                if bootstrapper_settings["success"] == True:
                    bootstrapper_settings = bootstrapper_settings["application_settings"]
                    if bootstrapper_settings.get("FFlagReplaceChannelNameForDownload"):
                        starter_url = "channel/common/"
                    else:
                        starter_url = f"channel/{rbx_channel.lower()}/"
                link_start = f"https://setup.rbxcdn.com/{starter_url}"
                if macos == True: link_start = f"https://setup.rbxcdn.com/{starter_url}mac/"
                return rf"{link_start}{version}-{file}"

        class Activity:
            @staticmethod
            def universe_id(placeId: str) -> str:
                return rf"https://apis.roblox.com/universes/v1/places/{placeId}/universe"
            @staticmethod
            def game(universeId: str) -> str:
                return rf"https://games.roblox.com/v1/games?universeIds={universeId}"
            @staticmethod
            def thumbnail(universeId: str, size: str = "512x512", isCircular: bool = False) -> str:
                return rf"https://thumbnails.roblox.com/v1/games/icons?universeIds={universeId}&returnPolicy=PlaceHolder&size={size}&format=Png&isCircular={str(isCircular).lower()}"
            @staticmethod
            def asset(assetId: str) -> str:
                return rf"https://assetdelivery.roblox.com/v1/asset/?id={assetId}"
            @staticmethod
            def page(rootPlaceId: str) -> str:
                return rf"https://www.roblox.com/games/{rootPlaceId}"
            @staticmethod
            def deeplink(placeId: str, gameInstanceId: str) -> str:
                return rf"roblox://experiences/start?placeId={placeId}&gameInstanceId={gameInstanceId}"
            @staticmethod
            def user(userId: str) -> str:
                return rf"https://users.roblox.com/v1/users/{userId}"
            @staticmethod
            def user_thumbnail(userId: str, size: tuple[int,int] = (48,48), format: str = "png", circular: bool = False) -> str:
                return rf"https://thumbnails.roblox.com/v1/users/avatar-bust?userIds={userId}&size={size[0]}x{size[1]}&format={format}&isCircular={circular}"


# region get()
def get(url: str, attempts: int = 3, cached: bool = False, timeout: Optional[tuple[int, int]] = None, dont_log_cached_request: bool = False) -> Response:
    if cached and url in _cache:
        if not dont_log_cached_request:
            Logger.info(f"Cached GET request: {url}")
        return _cache[url]
    
    exception: Exception | None = None

    for _ in range(attempts):
        try:
            Logger.info(f"GET request: {url}")
            response: Response = requests.get(url, timeout=timeout or TIMEOUT)
            response.raise_for_status()
            _cache[url] = response
            return response

        except Exception as e:
            Logger.error(f"GET request failed! {type(e).__name__}: {e}")
            exception = e
            time.sleep(COOLDOWN)
    
    if exception is not None:
        raise exception
