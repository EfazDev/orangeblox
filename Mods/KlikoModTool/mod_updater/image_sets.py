from pathlib import Path
from mod_updater.exceptions import ImageSetsNotFoundError, ImageSetDataNotFoundError
import re
import os

IMAGESET_IMG_NAME: str = "img_set_1x_1.png"
IMAGESET_LUA_NAME: str = "GetImageSetData.lua"

def locate_imagesets(start: Path) -> Path:
    folders = []
    for dirpath, dirnames, filenames in os.walk(start):
        if IMAGESET_IMG_NAME not in filenames:
            continue
        folders.append(Path(dirpath).relative_to(start))
    if len(folders) <= 0: raise ImageSetsNotFoundError(f"Failed to find path to ImageSets")
    return folders
def locate_imagesetdata_files(start: Path) -> Path:
    files = []
    for dirpath, dirnames, filenames in os.walk(start):
        if IMAGESET_LUA_NAME not in filenames:
            continue
        files.append(Path(dirpath, IMAGESET_LUA_NAME).relative_to(start))
    if len(files) <= 0: raise ImageSetDataNotFoundError("Failed to find path to ImageSetData")
    return files
def parse_lua_content(content: str) -> dict[str, dict[str, dict[str, str | int]]]:
    # ChatGPT
    icon_map: dict[str, dict[str, dict[str, str | int]]] = {}
    image_size_pattern: str = r"function make_assets_(\dx)\(\).*?(\{.*?\}) end"
    icon_data_pattern: str = r"\['([^']+)'\] = \{ ImageRectOffset = Vector2\.new\((\d+), (\d+)\), ImageRectSize = Vector2\.new\((\d+), (\d+)\), ImageSet = '([^']+)' \}"
    image_size_matches: list = re.findall(image_size_pattern, content, re.DOTALL)
    for size, data in image_size_matches:
        if size not in icon_map: icon_map[size] = {}
        icon_data_matches: list = re.findall(icon_data_pattern, data)
        for icon in icon_data_matches:
            name, x, y, w, h, image_set = icon
            icon_map[size][name] = {
                "image_set": image_set,
                "x": int(x),
                "y": int(y),
                "w": int(w),
                "h": int(h)
            }
    return icon_map
def get_icon_map(filepath: Path) -> dict[str, dict[str, dict[str, str | int]]]:
    with open(filepath, "r", encoding="utf-8") as file: content: str = file.read()
    return parse_lua_content(content)
    w, h = image.size
    ratio = w / h
    if ratio == target_ratio:
        return image.copy()
    if ratio > target_ratio:
        new_w = int(target_ratio * h)
        new_h = h
        left = (w - new_w) // 2
        top = 0
    else:
        new_w = w
        new_h = int(w / target_ratio)
        left = 0
        top = (h - new_h) // 2
    right = left + new_w
    bottom = top + new_h
    cropped = image.crop((left, top, right, bottom))
    return cropped