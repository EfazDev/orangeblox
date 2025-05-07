from mod_generator.modules import request
from mod_generator.modules.request import Api, Response


def get(binaryType: str) -> str:
    response: Response = request.get(Api.Roblox.Deployment.channel(binaryType), cached=True)
    data: dict = response.json()
    return data["channelName"]