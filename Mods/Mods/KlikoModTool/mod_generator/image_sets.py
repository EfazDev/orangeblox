from pathlib import Path
from mod_generator.exceptions import ImageSetsNotFoundError, ImageSetDataNotFoundError
from mod_generator.modules import Logger, request
from PIL import Image, PngImagePlugin
import numpy as np
import json
import sys
import re
import os

IMAGESET_IMG_NAME: str = "img_set_1x_1.png"
IMAGESET_LUA_NAME: str = "GetImageSetData.lua"
SUPPORTED_FILETYPES: list[str] = [".png"]
IMAGE_CACHE: dict[str, Image.Image] = {}

def hex_to_rgb(hex_color: str): hex_color = hex_color.lstrip("#"); return np.array([int(hex_color[i:i+2], 16) for i in (0, 2, 4)])
def clear_cache() -> None: IMAGE_CACHE.clear()
def add_watermark(mod_imagesets_directory: Path) -> None:
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text("Text", "Generated with Kliko's mod generator")
    for filepath in mod_imagesets_directory.iterdir():
        if not filepath.is_file() or not filepath.suffix == ".png": continue
        with Image.open(filepath, formats=("PNG",)) as image: image.save(filepath, format="PNG", optimize=False, pnginfo=metadata)
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
def _crop_to_fit(image: Image.Image, target_ratio: float) -> Image.Image:
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
def create_gradient_image(size: tuple[int, int], colors: list[str], angle: int) -> Image.Image:
    angle -= 90
    width, height = size
    rgb_colors = [hex_to_rgb(c) for c in colors]
    num_segments = len(rgb_colors) - 1

    x = np.linspace(0, 1, width)
    y = np.linspace(0, 1, height)
    xx, yy = np.meshgrid(x, y)
    angle_rad = np.radians(angle)
    gradient = xx * np.cos(angle_rad) + yy * np.sin(angle_rad)

    gmin = float(gradient.min())
    gmax = float(gradient.max())
    denom = gmax - gmin
    if denom == 0: norm = np.zeros_like(gradient)
    else: norm = (gradient - gmin) / denom
    if num_segments <= 0:
        result = np.zeros((height, width, 3), dtype=np.uint8)
        for ch in range(3):
            result[..., ch] = int(rgb_colors[0][ch])
        return Image.fromarray(result)
    pos = norm

    xp = np.linspace(0.0, 1.0, len(rgb_colors))
    result = np.zeros((height, width, 3), dtype=np.uint8)
    for channel in range(3):
        channel_values = np.array([c[channel] for c in rgb_colors], dtype=float)
        flat = np.interp(pos.ravel(), xp, channel_values)
        result[..., channel] = np.round(flat.reshape((height, width))).astype(np.uint8)
    return Image.fromarray(result)
def get_mask(colors: list[str], angle: int, size: tuple[int, int], icon_name: str="*") -> Image.Image:
    # Generate a unique cache key based on all colors, angle, and size
    if type(colors) is dict:
        key = f"image-mask-colors-{angle}-{size[0]}-{size[1]}-{icon_name}"
    else:
        key = f"{'-'.join(colors)}-{angle}-{size[0]}-{size[1]}-{icon_name}"
    
    if key in IMAGE_CACHE: return IMAGE_CACHE[key]
    if len(colors) == 1:
        # Solid color
        mask = Image.new("RGBA", size, colors[0])
    elif type(colors) is dict:
        if colors.get(icon_name):
            if type(colors.get(icon_name)) is list:
                if len(colors.get(icon_name)) == 1: mask = Image.new("RGBA", size, colors.get(icon_name)[0])
                else: mask = create_gradient_image(size, colors.get(icon_name), angle)
                IMAGE_CACHE[key] = mask
                return mask
            else:
                with Image.open(colors.get(icon_name)) as ma: image = ma.copy()
        elif colors.get("*"):
            if type(colors.get("*")) is list:
                if len(colors.get("*")) == 1: mask = Image.new("RGBA", size, colors.get("*")[0])
                else: mask = create_gradient_image(size, colors.get("*"), angle)
                IMAGE_CACHE[key] = mask
                return mask
            else:
                with Image.open(colors.get("*")) as ma: image = ma.copy()
        else:
            mask = Image.new("RGBA", size, "#ffffff")
            IMAGE_CACHE[key] = mask
            return mask
        cache_key: str = f"{image}-{size}"
        if image.mode != "RGBA":
            image = image.convert("RGBA")

        image.resize(size, resample=Image.Resampling.LANCZOS)
        IMAGE_CACHE[cache_key] = image
        return image
    else:
        # Gradient with multiple colors
        mask = create_gradient_image(size, colors, angle)
    IMAGE_CACHE[key] = mask
    return mask
def generate_user_selected_files(
    base_directory: Path,
    colors: list[str],
    angle: int,
    user_selected_files: list[dict[str, Path | list[str]]]
) -> None:
    for filepath in user_selected_files:
        source: Path = filepath["source"]
        target: list[str] = filepath["target"]

        if not source.is_file():
            Logger.warning(f"File not found: {source.name}", prefix="mod_generator.generate_user_selected_files()")
            continue

        if source.suffix.lower() not in SUPPORTED_FILETYPES:
            Logger.warning(f"Cannot generate file: {source.name}! Only .png files are supported", prefix="mod_generator.generate_user_selected_files()")
            continue

        target_path: Path = Path(base_directory, *target)
        target_path.parent.mkdir(parents=True, exist_ok=True)

        with Image.open(source, formats=("PNG",)) as image:
            image = image.convert("RGBA")
            r, g, b, a = image.split()

        modded_icon = get_mask(colors, angle, image.size, source.name)
        modded_icon.putalpha(a)
        modded_icon.save(target_path, format="PNG", optimize=False)
def generate_additional_files(base_directory: Path, colors: list[str], angle: int, studio: bool) -> None:
    cur_path = os.path.dirname(os.path.abspath(__file__))
    mod_generator_files = Path(cur_path) / "additional_files"
    index_filepath: Path = mod_generator_files / "__index__.json"
    if not index_filepath.is_file(): Logger.warning("Cannot generate additional files! __index_.json does not exist!", prefix="mod_generator.generate_additional_files()"); return
    with open(index_filepath, "r", encoding="utf-8") as file: data: dict = json.load(file)
    for filepath in mod_generator_files.iterdir():
        if filepath.name == index_filepath.name: continue
        if studio == False and "studio-" in filepath.name: continue
        if type(colors) is dict:
            authorized = False

            # Enable basely
            if colors.get(filepath.name): authorized = True
            if colors.get("_all_optional") == True: authorized = True
            elif "voicechat-" in filepath.name and colors.get("_voice_chat") == True: authorized = True
            elif "cursor-" in filepath.name and colors.get("_cursor") == True: authorized = True
            elif "leaderboard-" in filepath.name and colors.get("_leaderboard") == True: authorized = True
            elif "emotes-" in filepath.name and colors.get("_emotes") == True: authorized = True
            elif "devconsole-" in filepath.name and colors.get("_devconsole") == True: authorized = True
            elif "menubar-" in filepath.name and colors.get("_menubar") == True: authorized = True
            elif "topbar-" in filepath.name and colors.get("_topbar") == True: authorized = True
            elif not "other-" in filepath.name: authorized = True
            # Disable in case of power
            if "voicechat-" in filepath.name and colors.get("_voice_chat") == False: authorized = False
            elif "cursor-" in filepath.name and colors.get("_cursor") == False: authorized = False
            elif "leaderboard-" in filepath.name and colors.get("_leaderboard") == False: authorized = False
            elif "emotes-" in filepath.name and colors.get("_emotes") == False: authorized = False
            elif "devconsole-" in filepath.name and colors.get("_devconsole") == False: authorized = False
            elif "menubar-" in filepath.name and colors.get("_menubar") == False: authorized = False
            elif "topbar-" in filepath.name and colors.get("_topbar") == False: authorized = False
            if authorized == False: continue
        target: list[str] | None = data.get(filepath.name)
        if not target or not isinstance(target, list): Logger.warning(f"Cannot generate additional file: {filepath.name}! Unknown target path!", prefix="mod_generator.generate_additional_files()"); continue
        target_path: Path = Path(base_directory, *target)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(filepath, formats=("PNG",)) as image:
            image = image.convert("RGBA")
            r, g, b, a = image.split()
        if type(colors) is dict:
            if type(colors.get(filepath.name)) is str:
                if "mask-" in colors.get(filepath.name) or "mask-" in filepath.name:
                    if "mask-" in colors.get(filepath.name): colors[f"{filepath.name}_temp"] = colors[filepath.name].replace("mask-", "", 1)
                    if "mask-" in filepath.name: colors[f"{filepath.name}_temp"] = colors[filepath.name]
                    modded_icon = get_mask(colors, angle, image.size, f"{filepath.name}_temp")
                    modded_icon.putalpha(a)
                    modded_icon.save(target_path, format="PNG", optimize=False)
                elif "mask2-" in colors.get(filepath.name) or "mask2-" in filepath.name:
                    if "mask2-" in colors.get(filepath.name): colors[f"{filepath.name}_temp"] = colors[filepath.name].replace("mask2-", "", 1)
                    if "mask2-" in filepath.name: colors[f"{filepath.name}_temp"] = colors[filepath.name]
                    base = image.convert("RGBA")
                    mask_overlay = get_mask(colors, angle, base.size, f"{filepath.name}_temp").convert("RGBA")
                    mask = mask_overlay.getchannel("A")
                    modded_icon = Image.composite(mask_overlay, base, mask)
                    modded_icon.save(target_path, format="PNG", optimize=False)
                elif "whiteout-" in colors.get(filepath.name) or "whiteout-" in filepath.name:
                    if "whiteout-" in colors.get(filepath.name): colors[f"{filepath.name}_temp"] = colors[filepath.name].replace("whiteout-", "", 1)
                    if "whiteout-" in filepath.name: colors[f"{filepath.name}_temp"] = colors[filepath.name]
                    base = image.convert("RGBA")
                    mask_overlay = get_mask(colors, angle, base.size, f"{filepath.name}_temp").convert("RGBA")
                    base_pixels = base.load()
                    mask_overlay_pixels = mask_overlay.load()
                    width, height = base.size
                    for y in range(height):
                        for x in range(width):
                            r, g, b, a = base_pixels[x, y]
                            if a > 0 and r > 175 and g > 175 and b > 175:
                                or_, og, ob, oa = mask_overlay_pixels[x, y]
                                base_pixels[x, y] = (or_, og, ob, a)
                    modded_icon = base
                    modded_icon.save(target_path, format="PNG", optimize=False)
                else:
                    custom_roblox_logo_path = Path(colors.get(filepath.name))
                    custom_roblox_logo = Image.open(custom_roblox_logo_path).convert("RGBA")
                    custom_roblox_logo.thumbnail(image.size, resample=Image.Resampling.LANCZOS)
                    clear_area = Image.new("RGBA", image.size, (0, 0, 0, 0))
                    image.paste(clear_area, (0,0))
                    centered_logo = Image.new("RGBA", image.size, (0, 0, 0, 0))
                    x = (image.size[0] - custom_roblox_logo.width) // 2
                    y = (image.size[1] - custom_roblox_logo.height) // 2
                    centered_logo.paste(custom_roblox_logo, (x, y), mask=custom_roblox_logo)
                    image.paste(centered_logo, (0,0), mask=centered_logo)
                    image.save(target_path, format="PNG", optimize=False)
            elif "mask2-" in filepath.name:
                if colors.get(filepath.name): colors[f"{filepath.name}_temp"] = colors[filepath.name]
                base = image.convert("RGBA")
                mask_overlay = get_mask(colors, angle, base.size, f"{filepath.name}_temp").convert("RGBA")
                mask = mask_overlay.getchannel("A")
                modded_icon = Image.composite(mask_overlay, base, mask)
                modded_icon.save(target_path, format="PNG", optimize=False)
            elif "whiteout-" in filepath.name:
                if colors.get(filepath.name): colors[f"{filepath.name}_temp"] = colors[filepath.name]
                base = image.convert("RGBA")
                mask_overlay = get_mask(colors, angle, base.size, f"{filepath.name}_temp").convert("RGBA")
                base_pixels = base.load()
                mask_overlay_pixels = mask_overlay.load()
                width, height = base.size
                for y in range(height):
                    for x in range(width):
                        r, g, b, a = base_pixels[x, y]
                        if a > 0 and r > 175 and g > 175 and b > 175:
                            or_, og, ob, oa = mask_overlay_pixels[x, y]
                            base_pixels[x, y] = (or_, og, ob, a)
                modded_icon = base
                modded_icon.save(target_path, format="PNG", optimize=False)
            else:
                modded_icon = get_mask(colors, angle, image.size, filepath.name)
                modded_icon.putalpha(a)
                modded_icon.save(target_path, format="PNG", optimize=False)
        else:
            modded_icon = get_mask(colors, angle, image.size, filepath.name)
            modded_icon.putalpha(a)
            modded_icon.save(target_path, format="PNG", optimize=False)
def generate_imagesets(
    base_directory: Path,
    icon_map: dict[str, dict[str, dict[str, str | int]]],
    colors: list[str],
    angle: int
) -> None:
    clear_cache()
    modded_imagesets: list[str] = []
    blacklist: list[str] = get_blacklist(get_authorized_from_blacklist(colors))
    formatted_icon_map: dict[str, dict[str, Path | list[tuple[int, int, int, int]]]] = {}

    for _, icons in icon_map.items():
        for icon_name, data in icons.items():
            if icon_name in blacklist: continue
            image_set: str = data["image_set"]
            x: int = data["x"]
            y: int = data["y"]
            w: int = data["w"]
            h: int = data["h"]
            image_set_path: Path = (base_directory / image_set).with_suffix(".png")
            if f"{image_set}.png" not in modded_imagesets: modded_imagesets.append(f"{image_set}.png")
            if image_set not in formatted_icon_map:
                formatted_icon_map[image_set] = {}
                formatted_icon_map[image_set]["path"] = image_set_path
                formatted_icon_map[image_set]["icons"] = []
            formatted_icon_map[image_set]["icons"].append({
                "name": icon_name,
                "box": (x, y, x + w, y + h)
            })
    for image_set, image_set_data in formatted_icon_map.items():
        path: Path = image_set_data["path"]
        with Image.open(path, formats=("PNG",)) as image:
            image = image.convert("RGBA")
            for icon_data in image_set_data["icons"]:
                icon_name = icon_data["name"]
                box = icon_data["box"]
                icon: Image.Image = image.crop(box)
                r, g, b, a = icon.split()
                if type(colors) is dict:
                    if type(colors.get(icon_name)) is str:
                        if colors.get(icon_name).startswith("mask-"):
                            colors[f"{icon_name}_temp"] = colors[icon_name].replace("mask-", "", 1)
                            modded_icon = get_mask(colors, angle, icon.size, f"{icon_name}_temp")
                            modded_icon.putalpha(a)
                            masked_icon = modded_icon
                        elif colors.get(icon_name).startswith("mask2-"):
                            colors[f"{icon_name}_temp"] = colors[icon_name].replace("mask2-", "", 1)
                            mask_overlay = get_mask(colors, angle, icon.size, f"{icon_name}_temp").convert("RGBA")
                            mask = mask_overlay.getchannel("A")
                            modded_icon = Image.composite(mask_overlay, icon, mask)
                            masked_icon = modded_icon
                        elif colors.get(icon_name).startswith("whiteout-") or icon_name.startswith("icons/controls/voice/"):
                            colors[f"{icon_name}_temp"] = colors[icon_name].replace("whiteout-", "", 1)
                            mask_overlay = get_mask(colors, angle, icon.size, f"{icon_name}_temp").convert("RGBA")
                            base_pixels = icon.load()
                            mask_overlay_pixels = mask_overlay.load()
                            width, height = icon.size
                            for y in range(height):
                                for x in range(width):
                                    r, g, b, a = base_pixels[x, y]
                                    if a > 0 and r > 175 and g > 175 and b > 175:
                                        or_, og, ob, oa = mask_overlay_pixels[x, y]
                                        base_pixels[x, y] = (or_, og, ob, a)
                            modded_icon = icon
                            masked_icon = modded_icon
                        else:
                            custom_roblox_logo_path = Path(colors.get(icon_name))
                            custom_roblox_logo = Image.open(custom_roblox_logo_path).convert("RGBA")
                            custom_roblox_logo.thumbnail(icon.size, resample=Image.Resampling.LANCZOS)
                            clear_area = Image.new("RGBA", icon.size, (0, 0, 0, 0))
                            image.paste(clear_area, box)
                            centered_logo = Image.new("RGBA", icon.size, (0, 0, 0, 0))
                            x = (icon.size[0] - custom_roblox_logo.width) // 2
                            y = (icon.size[1] - custom_roblox_logo.height) // 2
                            centered_logo.paste(custom_roblox_logo, (x, y), mask=custom_roblox_logo)
                            image.paste(centered_logo, box, mask=centered_logo)
                            continue
                    elif icon_name.startswith("icons/controls/voice/"):
                        mask_overlay = get_mask(colors, angle, icon.size, icon_name).convert("RGBA")
                        base_pixels = icon.load()
                        mask_overlay_pixels = mask_overlay.load()
                        width, height = icon.size
                        for y in range(height):
                            for x in range(width):
                                r, g, b, a = base_pixels[x, y]
                                if a > 0 and r > 175 and g > 175 and b > 175:
                                    or_, og, ob, oa = mask_overlay_pixels[x, y]
                                    base_pixels[x, y] = (or_, og, ob, a)
                        modded_icon = icon
                        masked_icon = modded_icon
                    else:
                        modded_icon = get_mask(colors, angle, icon.size, icon_name)
                        modded_icon.putalpha(a)
                        masked_icon = modded_icon
                else:
                    modded_icon = get_mask(colors, angle, icon.size, icon_name)
                    modded_icon.putalpha(a)
                    masked_icon = modded_icon
                image.paste(masked_icon, box)
            image.save(path, format="PNG", optimize=False)

    # Remove unmodded ImageSets
    if modded_imagesets:
        for item in base_directory.iterdir():
            if item.is_file() and item.name not in modded_imagesets: item.unlink()
def get_authorized_from_blacklist(colors: list):
    if type(colors) is dict:
        total = []
        if colors.get("_voice_chat") == True:
            total += [
                "icons/controls/voice/microphone_0_dark",
                "icons/controls/voice/microphone_0_light",
                "icons/controls/voice/microphone_0_small_dark",
                "icons/controls/voice/microphone_0_small_light",
                "icons/controls/voice/microphone_100_dark",
                "icons/controls/voice/microphone_100_light",
                "icons/controls/voice/microphone_100_small_dark",
                "icons/controls/voice/microphone_100_small_light",
                "icons/controls/voice/microphone_20_dark",
                "icons/controls/voice/microphone_20_light",
                "icons/controls/voice/microphone_20_small_dark",
                "icons/controls/voice/microphone_20_small_light",
                "icons/controls/voice/microphone_40_dark",
                "icons/controls/voice/microphone_40_light",
                "icons/controls/voice/microphone_40_small_dark",
                "icons/controls/voice/microphone_40_small_light",
                "icons/controls/voice/microphone_60_dark",
                "icons/controls/voice/microphone_60_light",
                "icons/controls/voice/microphone_60_small_dark",
                "icons/controls/voice/microphone_60_small_light",
                "icons/controls/voice/microphone_80_dark",
                "icons/controls/voice/microphone_80_light",
                "icons/controls/voice/microphone_80_small_dark",
                "icons/controls/voice/microphone_80_small_light",
                "icons/controls/voice/microphone_error_dark",
                "icons/controls/voice/microphone_error_light",
                "icons/controls/voice/microphone_error_small_dark",
                "icons/controls/voice/microphone_error_small_light",
                "icons/controls/voice/microphone_off_dark",
                "icons/controls/voice/microphone_off_light",
                "icons/controls/voice/microphone_off_small_dark",
                "icons/controls/voice/microphone_off_small_light",
                "icons/controls/voice/microphone_on_dark",
                "icons/controls/voice/microphone_on_light",
                "icons/controls/voice/microphone_on_small_dark",
                "icons/controls/voice/microphone_on_small_light",
                "icons/controls/voice/red_speaker_0_dark",
                "icons/controls/voice/red_speaker_0_light",
                "icons/controls/voice/red_speaker_0_small_dark",
                "icons/controls/voice/red_speaker_0_small_light",
                "icons/controls/voice/red_speaker_100_dark",
                "icons/controls/voice/red_speaker_100_light",
                "icons/controls/voice/red_speaker_100_small_dark",
                "icons/controls/voice/red_speaker_100_small_light",
                "icons/controls/voice/red_speaker_20_dark",
                "icons/controls/voice/red_speaker_20_light",
                "icons/controls/voice/red_speaker_20_small_dark",
                "icons/controls/voice/red_speaker_20_small_light",
                "icons/controls/voice/red_speaker_40_dark",
                "icons/controls/voice/red_speaker_40_light",
                "icons/controls/voice/red_speaker_40_small_dark",
                "icons/controls/voice/red_speaker_40_small_light",
                "icons/controls/voice/red_speaker_60_dark",
                "icons/controls/voice/red_speaker_60_light",
                "icons/controls/voice/red_speaker_60_small_dark",
                "icons/controls/voice/red_speaker_60_small_light",
                "icons/controls/voice/red_speaker_80_dark",
                "icons/controls/voice/red_speaker_80_light",
                "icons/controls/voice/red_speaker_80_small_dark",
                "icons/controls/voice/red_speaker_80_small_light",
                "icons/controls/voice/speaker_0_dark",
                "icons/controls/voice/speaker_0_light",
                "icons/controls/voice/speaker_0_small_dark",
                "icons/controls/voice/speaker_0_small_light",
                "icons/controls/voice/speaker_100_dark",
                "icons/controls/voice/speaker_100_light",
                "icons/controls/voice/speaker_100_small_dark",
                "icons/controls/voice/speaker_100_small_light",
                "icons/controls/voice/speaker_20_dark",
                "icons/controls/voice/speaker_20_light",
                "icons/controls/voice/speaker_20_small_dark",
                "icons/controls/voice/speaker_20_small_light",
                "icons/controls/voice/speaker_40_dark",
                "icons/controls/voice/speaker_40_light",
                "icons/controls/voice/speaker_40_small_dark",
                "icons/controls/voice/speaker_40_small_light",
                "icons/controls/voice/speaker_60_dark",
                "icons/controls/voice/speaker_60_light",
                "icons/controls/voice/speaker_60_small_dark",
                "icons/controls/voice/speaker_60_small_light",
                "icons/controls/voice/speaker_80_dark",
                "icons/controls/voice/speaker_80_light",
                "icons/controls/voice/speaker_80_small_dark",
                "icons/controls/voice/speaker_80_small_light",
                "icons/controls/voice/speaker_error_dark",
                "icons/controls/voice/speaker_error_light",
                "icons/controls/voice/speaker_error_small_dark",
                "icons/controls/voice/speaker_error_small_light",
                "icons/controls/voice/speaker_off_dark",
                "icons/controls/voice/speaker_off_light",
                "icons/controls/voice/speaker_off_small_dark",
                "icons/controls/voice/speaker_off_small_light",
                "icons/controls/voice/speaker_on_dark",
                "icons/controls/voice/speaker_on_light",
                "icons/controls/voice/speaker_on_small_dark",
                "icons/controls/voice/speaker_on_small_light",
                "icons/controls/voice/video_error_dark",
                "icons/controls/voice/video_error_light",
                "icons/controls/voice/video_error_small_dark",
                "icons/controls/voice/video_error_small_light",
                "icons/controls/voice/video_off_dark",
                "icons/controls/voice/video_off_light",
                "icons/controls/voice/video_off_small_dark",
                "icons/controls/voice/video_off_small_light",
                "icons/controls/voice/video_on_dark",
                "icons/controls/voice/video_on_light",
                "icons/controls/voice/video_on_small_dark",
                "icons/controls/voice/video_on_small_light",
                "icons/graphic/camera_on_off",
                "icons/graphic/voicechat_large"
            ]
        if colors.get("_loading") == True:
            total += [
                "icons/graphic/loadingspinner"
            ]
        return total
    return []
def get_blacklist(authorized: list=[]) -> list[str]:
    blacklist = [
        "chat_bubble/chat-bubble",
        "chat_bubble/chat-bubble-bottom",
        "chat_bubble/chat-bubble-middle",
        "chat_bubble/chat-bubble-self",
        "chat_bubble/chat-bubble-self-bottom",
        "chat_bubble/chat-bubble-self-middle",
        "chat_bubble/chat-bubble-self-tip",
        "chat_bubble/chat-bubble-self-top",
        "chat_bubble/chat-bubble-self2",
        "chat_bubble/chat-bubble-single",
        "chat_bubble/chat-bubble-tip",
        "chat_bubble/chat-bubble-top",
        "chat_bubble/chat-bubble2",
        "component_assets/avatarBG_dark",
        "component_assets/avatarBG_light",
        "component_assets/bulletDown_17_stroke_3",
        "component_assets/bulletLeft_17",
        "component_assets/bulletLeft_17_stroke_3",
        "component_assets/bulletRight_17",
        "component_assets/bulletRight_17_stroke_3",
        "component_assets/bulletUp_17_stroke_3",
        "component_assets/bullet_17",
        "component_assets/circle_15_stroke_3",
        "component_assets/circle_16",
        "component_assets/circle_17",
        "component_assets/circle_17_mask",
        "component_assets/circle_17_stroke_1",
        "component_assets/circle_17_stroke_3",
        "component_assets/circle_21",
        "component_assets/circle_21_stroke_1",
        "component_assets/circle_22_stroke_3",
        "component_assets/circle_24_stroke_1",
        "component_assets/circle_25",
        "component_assets/circle_26_stroke_3",
        "component_assets/circle_28_padding_10",
        "component_assets/circle_29",
        "component_assets/circle_29_mask",
        "component_assets/circle_29_stroke_1",
        "component_assets/circle_30_stroke_3",
        "component_assets/circle_36",
        "component_assets/circle_36_stroke_1",
        "component_assets/circle_42_stroke_3",
        "component_assets/circle_49",
        "component_assets/circle_49_mask",
        "component_assets/circle_49_stroke_1",
        "component_assets/circle_52_stroke_3",
        "component_assets/circle_60_stroke_2",
        "component_assets/circle_68_stroke_2",
        "component_assets/circle_69_stroke_3",
        "component_assets/circle_72_stroke_3",
        "component_assets/circle_9",
        "component_assets/circle_9_stroke_1",
        "component_assets/contactFullAvatar_large",
        "component_assets/contactFullAvatar_small",
        "component_assets/contactHeadshot",
        "component_assets/dropshadow_16_20",
        "component_assets/dropshadow_17_16",
        "component_assets/dropshadow_17_4",
        "component_assets/dropshadow_17_8",
        "component_assets/dropshadow_24_6",
        "component_assets/dropshadow_25",
        "component_assets/dropshadow_28",
        "component_assets/dropshadow_56_8",
        "component_assets/dropshadow_chatOff",
        "component_assets/dropshadow_chatOn",
        "component_assets/dropshadow_more",
        "component_assets/dropshadow_square_4",
        "component_assets/dropshadow_thumbnail_28",
        "component_assets/genreBG",
        "component_assets/halfcircleLeft_17",
        "component_assets/halfcircleRight_17",
        "component_assets/itemBG_dark",
        "component_assets/itemBG_light",
        "component_assets/profileHeaderBG",
        "component_assets/square_7_stroke_3",
        "component_assets/triangleDown_16",
        "component_assets/triangleLeft_16",
        "component_assets/triangleRight_16",
        "component_assets/triangleUp_16",
        "component_assets/userBG_dark",
        "component_assets/user_60_mask",
        "component_assets/user_glow",
        "component_assets/vignette_246",
        "gradient/gradient_0_100",
        "icons/controls/voice/microphone_0_dark",
        "icons/controls/voice/microphone_0_light",
        "icons/controls/voice/microphone_0_small_dark",
        "icons/controls/voice/microphone_0_small_light",
        "icons/controls/voice/microphone_100_dark",
        "icons/controls/voice/microphone_100_light",
        "icons/controls/voice/microphone_100_small_dark",
        "icons/controls/voice/microphone_100_small_light",
        "icons/controls/voice/microphone_20_dark",
        "icons/controls/voice/microphone_20_light",
        "icons/controls/voice/microphone_20_small_dark",
        "icons/controls/voice/microphone_20_small_light",
        "icons/controls/voice/microphone_40_dark",
        "icons/controls/voice/microphone_40_light",
        "icons/controls/voice/microphone_40_small_dark",
        "icons/controls/voice/microphone_40_small_light",
        "icons/controls/voice/microphone_60_dark",
        "icons/controls/voice/microphone_60_light",
        "icons/controls/voice/microphone_60_small_dark",
        "icons/controls/voice/microphone_60_small_light",
        "icons/controls/voice/microphone_80_dark",
        "icons/controls/voice/microphone_80_light",
        "icons/controls/voice/microphone_80_small_dark",
        "icons/controls/voice/microphone_80_small_light",
        "icons/controls/voice/microphone_error_dark",
        "icons/controls/voice/microphone_error_light",
        "icons/controls/voice/microphone_error_small_dark",
        "icons/controls/voice/microphone_error_small_light",
        "icons/controls/voice/microphone_off_dark",
        "icons/controls/voice/microphone_off_light",
        "icons/controls/voice/microphone_off_small_dark",
        "icons/controls/voice/microphone_off_small_light",
        "icons/controls/voice/microphone_on_dark",
        "icons/controls/voice/microphone_on_light",
        "icons/controls/voice/microphone_on_small_dark",
        "icons/controls/voice/microphone_on_small_light",
        "icons/controls/voice/red_speaker_0_dark",
        "icons/controls/voice/red_speaker_0_light",
        "icons/controls/voice/red_speaker_0_small_dark",
        "icons/controls/voice/red_speaker_0_small_light",
        "icons/controls/voice/red_speaker_100_dark",
        "icons/controls/voice/red_speaker_100_light",
        "icons/controls/voice/red_speaker_100_small_dark",
        "icons/controls/voice/red_speaker_100_small_light",
        "icons/controls/voice/red_speaker_20_dark",
        "icons/controls/voice/red_speaker_20_light",
        "icons/controls/voice/red_speaker_20_small_dark",
        "icons/controls/voice/red_speaker_20_small_light",
        "icons/controls/voice/red_speaker_40_dark",
        "icons/controls/voice/red_speaker_40_light",
        "icons/controls/voice/red_speaker_40_small_dark",
        "icons/controls/voice/red_speaker_40_small_light",
        "icons/controls/voice/red_speaker_60_dark",
        "icons/controls/voice/red_speaker_60_light",
        "icons/controls/voice/red_speaker_60_small_dark",
        "icons/controls/voice/red_speaker_60_small_light",
        "icons/controls/voice/red_speaker_80_dark",
        "icons/controls/voice/red_speaker_80_light",
        "icons/controls/voice/red_speaker_80_small_dark",
        "icons/controls/voice/red_speaker_80_small_light",
        "icons/controls/voice/speaker_0_dark",
        "icons/controls/voice/speaker_0_light",
        "icons/controls/voice/speaker_0_small_dark",
        "icons/controls/voice/speaker_0_small_light",
        "icons/controls/voice/speaker_100_dark",
        "icons/controls/voice/speaker_100_light",
        "icons/controls/voice/speaker_100_small_dark",
        "icons/controls/voice/speaker_100_small_light",
        "icons/controls/voice/speaker_20_dark",
        "icons/controls/voice/speaker_20_light",
        "icons/controls/voice/speaker_20_small_dark",
        "icons/controls/voice/speaker_20_small_light",
        "icons/controls/voice/speaker_40_dark",
        "icons/controls/voice/speaker_40_light",
        "icons/controls/voice/speaker_40_small_dark",
        "icons/controls/voice/speaker_40_small_light",
        "icons/controls/voice/speaker_60_dark",
        "icons/controls/voice/speaker_60_light",
        "icons/controls/voice/speaker_60_small_dark",
        "icons/controls/voice/speaker_60_small_light",
        "icons/controls/voice/speaker_80_dark",
        "icons/controls/voice/speaker_80_light",
        "icons/controls/voice/speaker_80_small_dark",
        "icons/controls/voice/speaker_80_small_light",
        "icons/controls/voice/speaker_error_dark",
        "icons/controls/voice/speaker_error_light",
        "icons/controls/voice/speaker_error_small_dark",
        "icons/controls/voice/speaker_error_small_light",
        "icons/controls/voice/speaker_off_dark",
        "icons/controls/voice/speaker_off_light",
        "icons/controls/voice/speaker_off_small_dark",
        "icons/controls/voice/speaker_off_small_light",
        "icons/controls/voice/speaker_on_dark",
        "icons/controls/voice/speaker_on_light",
        "icons/controls/voice/speaker_on_small_dark",
        "icons/controls/voice/speaker_on_small_light",
        "icons/controls/voice/video_error_dark",
        "icons/controls/voice/video_error_light",
        "icons/controls/voice/video_error_small_dark",
        "icons/controls/voice/video_error_small_light",
        "icons/controls/voice/video_off_dark",
        "icons/controls/voice/video_off_light",
        "icons/controls/voice/video_off_small_dark",
        "icons/controls/voice/video_off_small_light",
        "icons/controls/voice/video_on_dark",
        "icons/controls/voice/video_on_light",
        "icons/controls/voice/video_on_small_dark",
        "icons/controls/voice/video_on_small_light",
        "icons/graphic/camera_on_off",
        "icons/graphic/gamesanditems_2xl",
        "icons/graphic/hearts_large",
        "icons/graphic/loadingspinner",
        "icons/graphic/logomark",
        "icons/graphic/newclothing_3xl",
        "icons/graphic/newclothing_xlarge",
        "icons/graphic/voicechat_large",
        "squircles/fill",
        "squircles/hollow",
        "squircles/hollowBold"
    ]
    for i in authorized:
        if i in blacklist: blacklist.remove(i)
    return blacklist