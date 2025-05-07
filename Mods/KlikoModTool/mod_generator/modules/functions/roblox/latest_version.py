from typing import Optional

from mod_generator.modules import request
from mod_generator.modules.request import Api, Response


def get(binaryType: str, channel: Optional[str] = None) -> str:
    response: Response = request.get(Api.Roblox.Deployment.latest(binaryType, channel), cached=True)
    data: dict = response.json()
    return data["clientVersionUpload"]