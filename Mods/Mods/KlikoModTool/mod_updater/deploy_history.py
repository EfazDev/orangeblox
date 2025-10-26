from mod_updater.modules import request
from mod_updater.modules.request import Response, Api
from mod_updater.exceptions import DeployHistoryError
import re

class Deployment:
    version: str
    hash: str
    binaryType: str
    is_macos: bool
    def __init__(self, binaryType: str, version: str, hash: str, is_macos: bool):
        self.binaryType = binaryType
        self.version = version
        self.hash = hash
        self.is_macos = is_macos
class DeployHistory:
    class LatestVersion: player: str; studio: str
    player: list[Deployment]
    studio: list[Deployment]
    mixed: list[Deployment]
    def __init__(self, latest_version: str) -> None:
        self.player, self.studio, self.mixed = self._get_history()
        self.LatestVersion.studio = latest_version
    def _get_history(self) -> tuple[list[Deployment], list[Deployment], list[Deployment]]:
        response: Response = request.get(Api.Roblox.Deployment.HISTORY)
        response2: Response = request.get(Api.Roblox.Deployment.HISTORY2)
        text: str = response.text
        text2: str = response2.text
        lines: list[str] = text.splitlines()
        lines2: list[str] = text2.splitlines()

        player: list[Deployment] = []
        studio: list[Deployment] = []
        mixed: list[Deployment] = []

        for entry in lines:
            try:
                items: list[str] = entry.removeprefix("New ").removesuffix(" ...").split()
                binary_type: str = items[0]
                is_macos = False
                if binary_type == "Studio64": binary_type = "WindowsStudio64"
                version: str = items[1]
                hash: str = items[-1]
                deployment: Deployment = Deployment(binary_type, version, hash, is_macos)
                if binary_type == "WindowsPlayer": player.insert(0, deployment)
                elif binary_type == "WindowsStudio64": studio.insert(0, deployment)
                mixed.insert(0, deployment)
            except Exception:
                continue
        for entry in lines2:
            try:
                items: list[str] = entry.removeprefix("New ").removesuffix(" ...").split()
                binary_type: str = items[0]
                is_macos = True
                if binary_type == "Studio": binary_type = "MacStudio"
                elif binary_type == "Client": binary_type = "MacPlayer"
                version: str = items[1]
                hash: str = items[-2]
                deployment: Deployment = Deployment(binary_type, version, hash, is_macos)
                if binary_type == "MacPlayer": player.insert(0, deployment)
                elif binary_type == "MacStudio": studio.insert(0, deployment)
                mixed.insert(0, deployment)
            except Exception:
                continue
        return (player, studio, mixed)
    def get_hash(self, version: str) -> str:
        for deployment in self.mixed:
            if deployment.version == version: return deployment.hash
        raise DeployHistoryError(f"Could not get hash of {version}")
    def get_studio_version(self, hash: str, macos: bool=False) -> str:
        for deployment in self.studio:
            if deployment.hash == hash and deployment.is_macos == macos: return deployment.version
        raise DeployHistoryError(f"Could not get version of {hash}")
    def get_latest_studio_version(self, macos: bool=False, hash_majors: tuple=None) -> str:
        hash_pattern = re.compile(r'^\d+(?:\.\d+)*$')
        def _is_hash(ver): return bool(hash_pattern.fullmatch(ver))
        if hash_majors:
            candidates = [d for d in self.studio if d.is_macos == macos and _is_hash(d.hash) and d.hash.split()[0] == hash_majors[0] and d.hash.split()[1] == hash_majors[1]]
        else:
            candidates = [d for d in self.studio if d.is_macos == macos and _is_hash(d.hash)]
        s = max(candidates, key=lambda d: tuple(int(part) for part in d.hash.split('.')))
        return s.version
    def is_macos_version(self, version: str) -> str:
        for deployment in self.mixed:
            if deployment.version == version: return deployment.is_macos
        raise DeployHistoryError(f"Could not get is macos of {version}")
    def player_equivalent(self, version: str) -> str:
        for deployment in self.studio:
            if deployment.version == version:
                studio_hash = deployment.hash
                break
        else:
            raise DeployHistoryError(f"Could not find Player equivalent of {version}! Given version is not Studio")
        for deployment in self.player:
            if deployment.hash == studio_hash:
                return deployment.version
        raise DeployHistoryError(f"Could not find Player equivalent of {version}! Player version with the same hash does not exist!")
    def studio_equivalent(self, version: str) -> str:
        for deployment in self.player:
            if deployment.version == version:
                player_hash = deployment.hash
                break
        else:
            raise DeployHistoryError(f"Could not find Studio equivalent of {version}! Given version is not Player")
        for deployment in self.studio:
            if deployment.hash == player_hash: return deployment.version
        raise DeployHistoryError(f"Could not find Studio equivalent of {version}! Studio version with the same hash does not exist!")
    def is_player_version(self, version: str) -> bool:
        for deployment in self.player:
            if deployment.version == version: return True
        return False
    def is_studio_version(self, version: str) -> bool:
        for deployment in self.studio:
            if deployment.version == version: return True
        return False
cache: dict = {}
def get_deploy_history(version: str) -> DeployHistory:
    if version in cache: return cache[version]
    deploy_history = DeployHistory(version)
    cache[version] = deploy_history
    return deploy_history