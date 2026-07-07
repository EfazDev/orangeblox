from __future__ import annotations
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.colorLib.builder import buildCOLR, buildCPAL
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.recordingPen import RecordingPen
from mod_generator.exceptions import ImageSetsNotFoundError, ImageSetDataNotFoundError
from mod_generator.modules import Logger
from PIL import Image, PngImagePlugin
import pyclipper
import typing
import logging
import numpy as np
import math
import json
import re
import os

DEF_BLOCK = frozenset({".notdef", "space", "base_icon", ".null"})
IMAGESET_IMG_NAME: str = "img_set_1x_1.png"
IMAGESET_LUA_NAME: str = "GetImageSetData.lua"
BUILDERFONT_ICON_NAME: str = "BuilderIcons-Regular.ttf"
BUILDERFONT_FILLED_ICON_NAME: str = "BuilderIcons-Filled.ttf"
CONTOUR_CACHE: dict[str, list[list[tuple]]] = {}
SUB_GLYPH_CACHE: dict[str, list[list[tuple]]] = {}
CUR_PATH = os.path.dirname(os.path.abspath(__file__))
SUPPORTED_FILETYPES: list[str] = [".png"]
IMAGE_CACHE: dict[str, Image.Image] = {}
BEZIER_STEPS: int = 12

logging.getLogger("fontTools").setLevel(logging.CRITICAL + 1)

def _rotate_point(x: float, y: float, cx: float, cy: float, angle_deg: float) -> tuple[float, float]:
    if angle_deg % 360 == 0: return x, y
    rad = math.radians(angle_deg)
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    return cos_a * (x - cx) - sin_a * (y - cy) + cx, sin_a * (x - cx) + cos_a * (y - cy) + cy
def _quad_sample(p0: tuple, p1: tuple, p2: tuple) -> list[tuple]:
    out = []
    for i in range(1, BEZIER_STEPS + 1):
        t = i / BEZIER_STEPS; mt = 1.0 - t
        out.append((mt * mt * p0[0] + 2 * mt * t * p1[0] + t * t * p2[0], mt * mt * p0[1] + 2 * mt * t * p1[1] + t * t * p2[1]))
    return out
def _cubic_sample(p0: tuple, p1: tuple, p2: tuple, p3: tuple) -> list[tuple]:
    out = []
    for i in range(1, BEZIER_STEPS + 1):
        t = i / BEZIER_STEPS; mt = 1.0 - t
        out.append((mt**3 * p0[0] + 3 * mt**2 * t * p1[0] + 3 * mt * t**2 * p2[0] + t**3 * p3[0], mt**3 * p0[1] + 3 * mt**2 * t * p1[1] + 3 * mt * t**2 * p2[1] + t**3 * p3[1]))
    return out
def _append_qcurve(result: list, start: tuple, pts: list) -> None:
    off_curves, end = pts[:-1], pts[-1]
    if not off_curves: result.append(end); return
    if len(off_curves) == 1: result.extend(_quad_sample(start, off_curves[0], end)); return
    cur = start
    for i, off in enumerate(off_curves):
        nxt = ((off[0] + off_curves[i + 1][0]) / 2, (off[1] + off_curves[i + 1][1]) / 2) if i < len(off_curves) - 1 else end
        result.extend(_quad_sample(cur, off, nxt))
        cur = nxt
def _recording_to_polygons(recording: list) -> list[list[tuple]]:
    contours, current = [], []
    def _commit_contour():
        if len(current) >= 3:
            if current[0] != current[-1]: current.append(current[0])
            contours.append(list(current))
    for op, args in recording:
        if op == "moveTo": _commit_contour(); current = [args[0]]
        elif op == "lineTo": current.append(args[0]) if current else current.extend([args[0]])
        elif op == "qCurveTo" and current: _append_qcurve(current, current[-1], list(args))
        elif op == "curveTo" and current: current.extend(_cubic_sample(current[-1], args[0], args[1], args[2]))
        elif op in ("closePath", "endPath"): _commit_contour(); current = []
    _commit_contour()
    return contours
def _clip_contours_to_band(contours: list[list[tuple]], lo: float, hi: float, x_min: float, x_max: float) -> list[list[tuple]]:
    if not contours: return []
    pc = pyclipper.Pyclipper(); SCALE = 1000.0  
    for poly in contours:
        if len(poly) < 3: continue
        p_ys = [pt[1] for pt in poly]
        if max(p_ys) < lo or min(p_ys) > hi: continue
        cleaned_poly = pyclipper.CleanPolygon([(int(x * SCALE), int(y * SCALE)) for x, y in poly])
        if len(cleaned_poly) >= 3:
            try: pc.AddPath(cleaned_poly, pyclipper.PT_SUBJECT, True)
            except pyclipper.ClipperException: continue
    safe_x_min, safe_x_max = int((x_min - 1000) * SCALE), int((x_max + 1000) * SCALE)
    rect = [(safe_x_min, int(lo * SCALE)), (safe_x_max, int(lo * SCALE)), (safe_x_max, int(hi * SCALE)), (safe_x_min, int(hi * SCALE))]
    try:
        pc.AddPath(rect, pyclipper.PT_CLIP, True)
        return [[(pt[0] / SCALE, pt[1] / SCALE) for pt in poly] for poly in pc.Execute(pyclipper.CT_INTERSECTION, pyclipper.PFT_EVENODD, pyclipper.PFT_EVENODD) if len(poly) >= 3]
    except pyclipper.ClipperException: return []
def _write_sub_glyph(icon_name: str, band_idx: int, contours: list[list[tuple]], font: TTFont, glyf_table, orig_aw: int) -> str | None:
    int_contours = []
    for poly in contours:
        rounded = [(round(px), round(py)) for px, py in poly]
        dedup = []
        for pt in rounded:
            if not dedup or pt != dedup[-1]: dedup.append(pt)
        if len(dedup) > 1 and dedup[0] == dedup[-1]: dedup.pop()
        if len(dedup) < 3: continue
        simplified = [dedup[0]]
        for i in range(1, len(dedup) - 1):
            p1, p2, p3 = simplified[-1], dedup[i], dedup[i + 1]
            cross = (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])
            if abs(cross) > 25.0: simplified.append(p2)
        simplified.append(dedup[-1])
        if len(simplified) < 3: continue
        xs, ys = [p[0] for p in simplified], [p[1] for p in simplified]
        area = sum(simplified[i][0] * simplified[(i+1) % len(simplified)][1] - simplified[(i+1) % len(simplified)][0] * simplified[i][1] for i in range(len(simplified)))
        if max(xs) - min(xs) < 3 or max(ys) - min(ys) < 3 or abs(area) < 40.0: continue  
        int_contours.append(simplified)
    if not int_contours: return None
    fast_tuple = tuple(tuple(pt for pt in poly) for poly in int_contours)
    contour_hash = hash(fast_tuple)
    cache_key = f"{orig_aw}_{contour_hash}"
    if cache_key in SUB_GLYPH_CACHE: return SUB_GLYPH_CACHE[cache_key]
    pen = TTGlyphPen(None)
    for poly in int_contours:
        pen.moveTo(poly[0])
        for pt in poly[1:]: pen.lineTo(pt)
        pen.closePath()
    sub_name = f"{icon_name}.g{band_idx}"
    sub_glyph = pen.glyph()
    sub_glyph.recalcBounds(glyf_table)
    glyf_table[sub_name] = sub_glyph
    font["hmtx"].metrics[sub_name] = (orig_aw, int(getattr(sub_glyph, "xMin", 0)))
    SUB_GLYPH_CACHE[cache_key] = sub_name
    return sub_name
def _resolve_icon_colors(icon_name: str, colors_config: dict | list) -> list[str] | None:
    if type(colors_config) is list: return colors_config
    if type(colors_config) is dict:
        for key in (icon_name, "_" + icon_name, "_font", "*"):
            val = colors_config.get(key)
            if type(val) is list and all(type(v) is str for v in val): return val
    return None
def _resolve_icon_image(icon_name: str, colors_config: dict | list, old_icons: dict) -> str | None:
    if not type(colors_config) is dict: return None
    for key in (icon_name, "_" + icon_name, "_font"):
        if type(colors_config.get(key)) is str: return colors_config[key]
    if colors_config.get("_old_icons") is True and type(old_icons.get(icon_name)) is str: return old_icons[icon_name]
    return colors_config.get("*") if type(colors_config.get("*")) is str else None
def _get_outline_contours(icon_name: str, font: TTFont) -> list[list[tuple]]:
    if icon_name not in font.getGlyphSet(): return []
    rec = RecordingPen()
    try: font.getGlyphSet()[icon_name].draw(rec)
    except Exception: return []
    return _recording_to_polygons(rec.value)
def _get_image_contours(image_path: str, units: int, icon_name: str, glyf_table) -> list[list[tuple]]:
    cache_key = f"{image_path}_{units}"
    if cache_key in CONTOUR_CACHE: return CONTOUR_CACHE[cache_key]
    try:
        with Image.open(image_path, formats=("PNG",)) as img: img = img.convert("RGBA")
        orig_w, orig_h = img.size
        tar_size = 128 if max(orig_w, orig_h) < 128 else 256
        img.thumbnail((tar_size, tar_size), resample=Image.Resampling.LANCZOS)
    except Exception: return []
    arr = np.array(img); h, w = arr.shape[:2]
    og = glyf_table.get(icon_name)
    x_min, y_max, bbox_w, bbox_h = (float(og.xMin), float(og.yMax), float(og.xMax - og.xMin), float(og.yMax - og.yMin)) if og else (0.0, float(units), float(units), float(units))
    scale = min(max(1.0, bbox_w) / max(1, w), max(1.0, bbox_h) / max(1, h))
    top_x, top_y = x_min + (bbox_w - (w * scale)) / 2.0, y_max - (bbox_h - (h * scale)) / 2.0
    contours = []
    for py in range(h):
        px = 0
        while px < w:
            if arr[py, px][3] >= 80:
                start_x = px
                while px < w and arr[py, px][3] >= 80: px += 1
                fy_bot, fy_top = top_y - (py + 1) * scale, top_y - py * scale
                x0, x1 = top_x + start_x * scale, top_x + px * scale
                contours.append([(x0, fy_bot - 0.5), (x1 + 0.5, fy_bot - 0.5), (x1 + 0.5, fy_top + 0.5), (x0, fy_top + 0.5)])
            else: px += 1     
    if not contours: return []
    pc = pyclipper.Pyclipper(); SCALE = 1000.0
    for poly in contours: pc.AddPath([(int(x * SCALE), int(y * SCALE)) for x, y in poly], pyclipper.PT_SUBJECT, True)
    try: 
        result = [[(pt[0] / SCALE, pt[1] / SCALE) for pt in p] for p in pc.Execute(pyclipper.CT_UNION, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)]
        CONTOUR_CACHE[cache_key] = result
        return result
    except: return contours
def _get_native_color_contours(image_path: str, units: int, icon_name: str, glyf_table, max_colors: int = 64) -> dict[str, list[list[tuple]]]:
    try:
        with Image.open(image_path, formats=("PNG",)) as img: 
            img = img.convert("RGBA")
            orig_w, orig_h = img.size
            tar_size = 128 if max(orig_w, orig_h) < 128 else 256
            img.thumbnail((tar_size, tar_size), resample=Image.Resampling.LANCZOS)
            alpha = img.getchannel("A").point(lambda p: 255 if p >= 128 else 0)
            img.putalpha(alpha)
            rgb = img.convert("RGB")
            rgb = rgb.quantize(
                colors=max_colors, 
                method=Image.Quantize.FASTOCTREE, 
                dither=Image.Dither.NONE
            )
            img = rgb.convert("RGBA")
            img.putalpha(alpha)
    except Exception: return {}
    arr = np.array(img)
    h, w = arr.shape[:2]
    og = glyf_table.get(icon_name)
    x_min, y_max, bbox_w, bbox_h = (float(og.xMin), float(og.yMax), float(og.xMax - og.xMin), float(og.yMax - og.yMin)) if og else (0.0, float(units), float(units), float(units))
    scale = min(max(1.0, bbox_w) / max(1, w), max(1.0, bbox_h) / max(1, h))
    top_x, top_y = x_min + (bbox_w - (w * scale)) / 2.0, y_max - (bbox_h - (h * scale)) / 2.0
    color_rects: dict[str, list[list[tuple]]] = {}
    for py in range(h):
        px = 0
        while px < w:
            r, g, b, a = arr[py, px]
            if a >= 80:
                start_x = px
                hex_col = f"#{r:02x}{g:02x}{b:02x}"
                while px < w and arr[py, px][3] >= 80 and f"#{arr[py, px][0]:02x}{arr[py, px][1]:02x}{arr[py, px][2]:02x}" == hex_col: px += 1
                if hex_col not in color_rects: color_rects[hex_col] = []
                fy_bot, fy_top = top_y - (py + 1) * scale, top_y - py * scale
                x0, x1 = top_x + start_x * scale, top_x + px * scale
                color_rects[hex_col].append([(x0, fy_bot), (x1, fy_bot), (x1, fy_top), (x0, fy_top)])
            else: px += 1
    final_color_contours = {}
    SCALE = 1000.0
    pc_master = pyclipper.Pyclipper()
    for rects in color_rects.values():
        for poly in rects: pc_master.AddPath([(int(x * SCALE), int(y * SCALE)) for x, y in poly], pyclipper.PT_SUBJECT, True)     
    try: 
        sil = pc_master.Execute(pyclipper.CT_UNION, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
        if sil:
            smooth_radius = int(scale * 0.5 * SCALE)
            if smooth_radius > 0:
                pco_smooth = pyclipper.PyclipperOffset()
                pco_smooth.AddPaths(sil, pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)
                sil = pco_smooth.Execute(smooth_radius)
                pco_smooth.Clear()
                pco_smooth.AddPaths(sil, pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)
                sil = pco_smooth.Execute(-smooth_radius)
    except Exception: sil = []
    if not sil: return {}
    safe_expansion = scale * 1.5
    offset_delta = safe_expansion * SCALE
    for hex_col, rects in color_rects.items():
        pc = pyclipper.Pyclipper()
        for poly in rects: pc.AddPath([(int(x * SCALE), int(y * SCALE)) for x, y in poly], pyclipper.PT_SUBJECT, True)
        try: 
            unioned = pc.Execute(pyclipper.CT_UNION, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
            if not unioned: continue
            pco = pyclipper.PyclipperOffset()
            pco.AddPaths(unioned, pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)
            dilated = pco.Execute(offset_delta)
            pc_clip = pyclipper.Pyclipper()
            pc_clip.AddPaths(dilated, pyclipper.PT_SUBJECT, True)
            pc_clip.AddPaths(sil, pyclipper.PT_CLIP, True)
            final_clipped = pc_clip.Execute(pyclipper.CT_INTERSECTION, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
            result = [[(pt[0] / SCALE, pt[1] / SCALE) for pt in p] for p in final_clipped]
            if result: final_color_contours[hex_col] = result
        except: pass
    return final_color_contours
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
def locate_builderfont(start: Path) -> Path:
    files = []
    for dirpath, dirnames, filenames in os.walk(start):
        if BUILDERFONT_ICON_NAME in filenames:
            files.append(Path(dirpath).relative_to(start) / BUILDERFONT_ICON_NAME)
        if BUILDERFONT_FILLED_ICON_NAME in filenames:
            files.append(Path(dirpath).relative_to(start) / BUILDERFONT_FILLED_ICON_NAME)
    if len(files) <= 0: raise ImageSetsNotFoundError(f"Failed to find path to BuilderFonts")
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
def create_gradient_image(size: tuple[int, int], colors: list[str], angle: int, icon_image: Image.Image = None) -> Image.Image:
    angle -= 90
    width, height = size
    rgb_colors = [hex_to_rgb(c) for c in colors]
    num_segments = len(rgb_colors) - 1
    x = np.linspace(0, 1, width)
    y = np.linspace(0, 1, height)
    xx, yy = np.meshgrid(x, y)
    angle_rad = np.radians(angle)
    gradient = xx * np.cos(angle_rad) + yy * np.sin(angle_rad)
    if icon_image is not None:
        icon_arr = np.array(icon_image)
        if icon_arr.shape[-1] == 4:
            alpha = icon_arr[..., 3]
            valid_pixels = gradient[alpha > 0]
            if len(valid_pixels) > 0:
                gmin = float(valid_pixels.min())
                gmax = float(valid_pixels.max())
            else:
                gmin = float(gradient.min())
                gmax = float(gradient.max())
        else:
            gmin = float(gradient.min())
            gmax = float(gradient.max())
    else:
        gmin = float(gradient.min())
        gmax = float(gradient.max())
    denom = gmax - gmin
    if denom == 0: norm = np.zeros_like(gradient)
    else: norm = (gradient - gmin) / denom
    norm = np.clip(norm, 0, 1)
    if num_segments <= 0:
        result = np.zeros((height, width, 3), dtype=np.uint8)
        for ch in range(3):
            result[..., ch] = int(rgb_colors[0][ch])
        return Image.fromarray(result)
    xp = np.linspace(0.0, 1.0, len(rgb_colors))
    result = np.zeros((height, width, 3), dtype=np.uint8)
    for channel in range(3):
        channel_values = np.array([c[channel] for c in rgb_colors], dtype=float)
        flat = np.interp(norm.ravel(), xp, channel_values)
        result[..., channel] = np.round(flat.reshape((height, width))).astype(np.uint8)
    return Image.fromarray(result)
def get_mask(colors: list[str], angle: int, size: tuple[int, int], icon_name: str="*", icon_image: Image.Image = None) -> Image.Image:
    if type(colors) is dict: key = f"image-mask-colors-{angle}-{size[0]}-{size[1]}-{icon_name}"
    else: key = f"{'-'.join(colors)}-{angle}-{size[0]}-{size[1]}-{icon_name}"
    if key in IMAGE_CACHE:  return IMAGE_CACHE[key]
    if type(colors) is list and len(colors) == 1: mask = Image.new("RGBA", size, colors[0])
    elif type(colors) is dict:
        if colors.get(icon_name):
            if type(colors.get(icon_name)) is list:
                if len(colors.get(icon_name)) == 1:  mask = Image.new("RGBA", size, colors.get(icon_name)[0])
                else: mask = create_gradient_image(size, colors.get(icon_name), angle, icon_image)
                IMAGE_CACHE[key] = mask
                return mask
            else:
                with Image.open(colors.get(icon_name)) as ma: image = ma.copy()
        elif colors.get("*"):
            if type(colors.get("*")) is list:
                if len(colors.get("*")) == 1:  mask = Image.new("RGBA", size, colors.get("*")[0])
                else: mask = create_gradient_image(size, colors.get("*"), angle, icon_image)
                IMAGE_CACHE[key] = mask
                return mask
            else:
                with Image.open(colors.get("*")) as ma: image = ma.copy()
        else:
            mask = Image.new("RGBA", size, "#ffffff")
            IMAGE_CACHE[key] = mask
            return mask
        cache_key: str = f"{image}-{size}"
        if image.mode != "RGBA": image = image.convert("RGBA")
        image.resize(size, resample=Image.Resampling.LANCZOS)
        IMAGE_CACHE[cache_key] = image
        return image
    else:
        mask = create_gradient_image(size, colors, angle, icon_image)
        IMAGE_CACHE[key] = mask
        return mask
def interpolate_gradient(hex_stops: list[str], t: float) -> tuple[float, float, float, float]:
    t = max(0.0, min(1.0, t))
    if len(hex_stops) == 1:
        r, g, b = hex_to_rgb(hex_stops[0])
        return r / 255.0, g / 255.0, b / 255.0, 1.0
    n = len(hex_stops) - 1
    scaled = t * n
    idx = min(int(scaled), n - 1)
    lt = scaled - idx
    c1, c2 = hex_to_rgb(hex_stops[idx]), hex_to_rgb(hex_stops[idx + 1])
    r = (c1[0] + (c2[0] - c1[0]) * lt) / 255.0
    g = (c1[1] + (c2[1] - c1[1]) * lt) / 255.0
    b = (c1[2] + (c2[2] - c1[2]) * lt) / 255.0
    return min(r, 1.0), min(g, 1.0), min(b, 1.0), 1.0
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

        modded_icon = get_mask(colors, angle, image.size, source.name, image)
        modded_icon.putalpha(a)
        modded_icon.save(target_path, format="PNG", optimize=False)
def generate_additional_files(base_directory: Path, colors: list[str], angle: int, studio: bool) -> None:
    mod_generator_files = Path(CUR_PATH) / "additional_files"
    index_filepath: Path = mod_generator_files / "__index__.json"
    if not index_filepath.is_file(): Logger.warning("Cannot generate additional files! __index_.json does not exist!", prefix="mod_generator.generate_additional_files()"); return
    with open(index_filepath, "r", encoding="utf-8") as file: data: dict = json.load(file)
    for filepath in mod_generator_files.iterdir():
        if filepath.name == index_filepath.name or filepath.name == ".DS_Store": continue
        if studio == False and "studio-" in filepath.name: continue
        if filepath.name == "buildericon.json":
            with open(filepath, "r", encoding="utf-8") as file: builder_icons_data: dict = json.load(file)
            with open(Path(base_directory, "ExtraContent", "LuaPackages", "Packages", "_Index", "BuilderIcons", "BuilderIcons", "BuilderIcons.json"), "w", encoding="utf-8") as file: json.dump(builder_icons_data, file, indent=4)
            continue
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
        if not target or not type(target) is list: Logger.warning(f"Cannot generate additional file: {filepath.name}! Unknown target path!", prefix="mod_generator.generate_additional_files()"); continue
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
                    modded_icon = get_mask(colors, angle, image.size, f"{filepath.name}_temp", image)
                    modded_icon.putalpha(a)
                    modded_icon.save(target_path, format="PNG", optimize=False)
                elif "mask2-" in colors.get(filepath.name) or "mask2-" in filepath.name:
                    if "mask2-" in colors.get(filepath.name): colors[f"{filepath.name}_temp"] = colors[filepath.name].replace("mask2-", "", 1)
                    if "mask2-" in filepath.name: colors[f"{filepath.name}_temp"] = colors[filepath.name]
                    base = image.convert("RGBA")
                    mask_overlay = get_mask(colors, angle, base.size, f"{filepath.name}_temp", base).convert("RGBA")
                    mask = mask_overlay.getchannel("A")
                    modded_icon = Image.composite(mask_overlay, base, mask)
                    modded_icon.save(target_path, format="PNG", optimize=False)
                elif "whiteout-" in colors.get(filepath.name) or "whiteout-" in filepath.name:
                    if "whiteout-" in colors.get(filepath.name): colors[f"{filepath.name}_temp"] = colors[filepath.name].replace("whiteout-", "", 1)
                    if "whiteout-" in filepath.name: colors[f"{filepath.name}_temp"] = colors[filepath.name]
                    base = image.convert("RGBA")
                    mask_overlay = get_mask(colors, angle, base.size, f"{filepath.name}_temp", base).convert("RGBA")
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
                mask_overlay = get_mask(colors, angle, base.size, f"{filepath.name}_temp", base).convert("RGBA")
                mask = mask_overlay.getchannel("A")
                modded_icon = Image.composite(mask_overlay, base, mask)
                modded_icon.save(target_path, format="PNG", optimize=False)
            elif "whiteout-" in filepath.name:
                if colors.get(filepath.name): colors[f"{filepath.name}_temp"] = colors[filepath.name]
                base = image.convert("RGBA")
                mask_overlay = get_mask(colors, angle, base.size, f"{filepath.name}_temp", base).convert("RGBA")
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
                modded_icon = get_mask(colors, angle, image.size, filepath.name, image)
                modded_icon.putalpha(a)
                modded_icon.save(target_path, format="PNG", optimize=False)
        else:
            modded_icon = get_mask(colors, angle, image.size, filepath.name, image)
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
                            modded_icon = get_mask(colors, angle, icon.size, f"{icon_name}_temp", icon)
                            modded_icon.putalpha(a)
                            masked_icon = modded_icon
                        elif colors.get(icon_name).startswith("mask2-"):
                            colors[f"{icon_name}_temp"] = colors[icon_name].replace("mask2-", "", 1)
                            mask_overlay = get_mask(colors, angle, icon.size, f"{icon_name}_temp", icon).convert("RGBA")
                            mask = mask_overlay.getchannel("A")
                            modded_icon = Image.composite(mask_overlay, icon, mask)
                            masked_icon = modded_icon
                        elif colors.get(icon_name).startswith("whiteout-") or icon_name.startswith("icons/controls/voice/"):
                            colors[f"{icon_name}_temp"] = colors[icon_name].replace("whiteout-", "", 1)
                            mask_overlay = get_mask(colors, angle, icon.size, f"{icon_name}_temp", icon).convert("RGBA")
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
                        mask_overlay = get_mask(colors, angle, icon.size, icon_name, icon).convert("RGBA")
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
                        modded_icon = get_mask(colors, angle, icon.size, icon_name, icon)
                        modded_icon.putalpha(a)
                        masked_icon = modded_icon
                else:
                    modded_icon = get_mask(colors, angle, icon.size, icon_name, icon)
                    modded_icon.putalpha(a)
                    masked_icon = modded_icon
                image.paste(masked_icon, box)
            image.save(path, format="PNG", optimize=False)

    # Remove unmodded ImageSets
    if modded_imagesets:
        for item in base_directory.iterdir():
            if item.is_file() and item.name not in modded_imagesets: item.unlink()
def generate_fonts_with_color(
    base_directory: Path, 
    builder_fonts: typing.List[Path], 
    colors: dict | list, 
    angle: int = 0
) -> None:
    max_stops = 2
    if type(colors) is list: max_stops = max(2, len(colors))
    elif type(colors) is dict:
        lists = [v for v in colors.values() if type(v) is list and all(type(i) is str for i in v)]
        if lists: max_stops = max([len(l) for l in lists] + [2])
    n_bands = max(2, max_stops * 8)
    angle = angle % 360
    use_native_colors = type(colors) is dict and colors.get("_imagecolors_font") == True
    try: old_icons = get_old_icons()
    except Exception: old_icons = {}
    for font_path in builder_fonts:
        SUB_GLYPH_CACHE.clear()
        font = TTFont(Path(base_directory, font_path))
        units, glyf_table = font["head"].unitsPerEm, font["glyf"]
        original_order, extra_names, color_glyphs = list(font.getGlyphOrder()), [], {}
        master_palette: list[tuple[float, float, float, float]] = []
        palette_cache: dict[typing.Any, int] = {}
        def get_palette_start_idx(stops: list[str]) -> int:
            key = tuple(stops)
            if key not in palette_cache:
                palette_cache[key] = len(master_palette)
                master_palette.extend(interpolate_gradient(stops, i / (n_bands - 1)) for i in range(n_bands))
            return palette_cache[key]
        def get_solid_color_idx(hex_col: str) -> int:
            cache_key = f"solid_{hex_col}"
            if cache_key not in palette_cache:
                r, g, b = hex_to_rgb(hex_col)
                palette_cache[cache_key] = len(master_palette)
                master_palette.append((r / 255.0, g / 255.0, b / 255.0, 1.0))
            return palette_cache[cache_key]
        for icon_name in original_order:
            if icon_name in DEF_BLOCK: continue
            icon_img = _resolve_icon_image(icon_name, colors, old_icons)
            icon_stops = _resolve_icon_colors(icon_name, colors)
            if icon_img and use_native_colors and colors.get(icon_name):
                native_dict = _get_native_color_contours(icon_img, units, icon_name, glyf_table)
                if not native_dict: continue
                orig_aw = font["hmtx"].metrics[icon_name][0]
                layers = []
                band_idx = 0
                for hex_col, color_contours in native_dict.items():
                    color_idx = get_solid_color_idx(hex_col)
                    if sub := _write_sub_glyph(icon_name, f"n{band_idx}", color_contours, font, glyf_table, orig_aw): layers.append((sub, color_idx))
                    band_idx += 1
                if not layers: continue
                extra_names.extend(s for s, _ in layers if s not in extra_names)
                color_glyphs[icon_name] = layers
                continue 
            if not icon_stops: continue
            start_idx = get_palette_start_idx(icon_stops)
            contours = _get_image_contours(icon_img, units, icon_name, glyf_table) if icon_img else _get_outline_contours(icon_name, font)
            if not contours: continue
            xs, ys = [pt[0] for p in contours for pt in p], [pt[1] for p in contours for pt in p]
            if not xs or not ys: continue
            if icon_img:
                og = glyf_table.get(icon_name)
                if og and hasattr(og, "xMin"):
                    cx = (float(og.xMax) + float(og.xMin)) / 2.0
                    cy = (float(og.yMax) + float(og.yMin)) / 2.0
                else: cx, cy = float(units) / 2.0, float(units) / 2.0
            else: cx, cy = sum([min(xs), max(xs)]) / 2.0, sum([min(ys), max(ys)]) / 2.0
            alignment_offset = 0 
            slice_angle = angle + alignment_offset
            rot_contours = [[_rotate_point(x, y, cx, cy, slice_angle) for x, y in poly] for poly in contours]
            r_xs, r_ys = [pt[0] for p in rot_contours for pt in p], [pt[1] for p in rot_contours for pt in p]
            r_y_min, r_y_max = min(r_ys), max(r_ys)
            r_x_min, r_x_max = min(r_xs), max(r_xs)
            band_size = (r_y_max - r_y_min) / n_bands
            orig_aw = font["hmtx"].metrics[icon_name][0]
            layers = []
            for band in range(n_bands):
                lo = r_y_min + band * band_size
                hi = r_y_min + (band + 1) * band_size
                if band < n_bands - 1: hi += 50.0 
                clipped_rot = _clip_contours_to_band(rot_contours, lo, hi, r_x_min, r_x_max)
                clipped = [[_rotate_point(x, y, cx, cy, -slice_angle) for x, y in poly] for poly in clipped_rot]
                if sub := _write_sub_glyph(icon_name, band, clipped, font, glyf_table, orig_aw): layers.append((sub, start_idx + band))
            if not layers: continue
            extra_names.extend(s for s, _ in layers if s not in extra_names)
            color_glyphs[icon_name] = layers
        font.setGlyphOrder(original_order + extra_names)
        font["CPAL"] = buildCPAL([master_palette])
        if color_glyphs: font["COLR"] = buildCOLR(color_glyphs)
        save_path = Path(base_directory, font_path).with_name(Path(font_path).stem + "Custom" + Path(font_path).suffix)
        font.save(save_path)
def generate_fonts_with_color_og(
    base_directory: Path,
    builder_fonts: typing.List[Path],
    colors: list[str],
    angle: int, 
    studio: bool
):
    target = ["ExtraContent", "LuaPackages", "Packages", "_Index", "BuilderIcons", "BuilderIcons", "Font"]
    Path(base_directory, *target).mkdir(parents=True, exist_ok=True)
    for font_path in builder_fonts:
        font = TTFont(Path(base_directory, font_path))
        units = font["head"].unitsPerEm
        colors_needed = {}
        handled_alignment = []
        index = 0

        if type(colors) is dict:
            old_icons = get_old_icons()
            for icon_name in font.getGlyphOrder():
                selected_color = False
                selected_icon = False

                def handle_table(table):
                    nonlocal index
                    nonlocal colors_needed
                    nonlocal selected_color
                    nonlocal selected_icon
                    nonlocal handled_alignment
                    nonlocal icon_name
                    if table:
                        if not selected_color and type(table) is list:
                            if len(table) == 1: 
                                r, g, b = 0, 0, 0
                                rgb = hex_to_rgb(table[0])
                                r += float(rgb[0])/255.0
                                g += float(rgb[1])/255.0
                                b += float(rgb[2])/255.0
                                colors_needed[icon_name] = [index, (min(float(r), 1.0), min(float(g), 1.0), min(float(b), 1.0), 1.0)]
                                index += 1
                            else: 
                                r, g, b, t = 0, 0, 0, 0
                                for i in table:
                                    rgb = hex_to_rgb(i)
                                    r += float(rgb[0])/255.0
                                    g += float(rgb[1])/255.0
                                    b += float(rgb[2])/255.0
                                    t += 1
                                colors_needed[icon_name] = [index, (min(float(r / t), 1.0), min(float(g / t), 1.0), min(float(b / t), 1.0), 1.0)]
                                index += 1
                            selected_color = True
                        if not selected_icon and type(table) is str:
                            blocked_icons = (".notdef", "space", "base_icon")
                            if icon_name in blocked_icons: return
                            with Image.open(table, formats=("PNG",)) as image: image = image.convert("RGBA")
                            image.thumbnail((64, 64), resample=Image.Resampling.NEAREST)
                            arr = np.array(image)
                            h, w = arr.shape[:2]
                            glyphset = font.getGlyphSet()
                            units = font["head"].unitsPerEm
                            orig_aw, orig_lsb = font["hmtx"][icon_name]
                            orig_glyph = font["glyf"][icon_name]
                            try:
                                xMin = orig_glyph.xMin
                                yMax = orig_glyph.yMax
                                xMax = orig_glyph.xMax
                                yMin = orig_glyph.yMin
                                bbox_width = xMax - xMin
                                bbox_height = yMax - yMin
                            except Exception:
                                xMin = 0
                                yMax = units
                                bbox_width = 0
                                bbox_height = 0
                            if bbox_width <= 0:
                                bbox_width = max(1.0, orig_aw - orig_lsb)
                                xMin = orig_lsb
                            if bbox_height <= 0:
                                bbox_height = units
                                yMax = units
                            scale = min(bbox_width / (float(w)), bbox_height / (float(h)))*1.2
                            if scale <= 0: scale = 1.0
                            top_left_x = xMin
                            top_left_y = yMax*1.1
                            pen = TTGlyphPen(glyphset)
                            for py in range(h):
                                for px in range(w):
                                    r, g, b, a = arr[py, px]
                                    if a < 128: continue
                                    fy_top = top_left_y - (py * scale)
                                    fy_bottom = top_left_y - ((py + 1) * scale)
                                    x0 = top_left_x + (px * scale)
                                    x1 = top_left_x + ((px + 1) * scale)
                                    y0 = fy_bottom
                                    y1 = fy_top
                                    pen.moveTo((x0, y0))
                                    pen.lineTo((x1, y0))
                                    pen.lineTo((x1, y1))
                                    pen.lineTo((x0, y1))
                                    pen.closePath()
                            new_glyph = pen.glyph()
                            new_glyph.recalcBounds(glyphset)
                            font["glyf"][icon_name] = new_glyph
                            font["hmtx"][icon_name] = (orig_aw, orig_lsb)
                            if icon_name in font["glyf"] and hasattr(font["glyf"][icon_name], 'xMin'):
                                glyph = font["glyf"][icon_name]
                                glyph_width = glyph.xMax - glyph.xMin
                                new_aw = units
                                new_lsb = (units - glyph_width) / 2
                                font['hmtx'].metrics[icon_name] = (int(round(new_aw) * 1.05), round(new_lsb))
                                handled_alignment.append(icon_name)
                            selected_icon = True
                handle_table(colors.get(icon_name))
                handle_table(colors.get("_" + icon_name))
                handle_table(colors.get("_font"))
                if colors.get("_old_icons") == True and old_icons.get(icon_name): handle_table(old_icons.get(icon_name))
                handle_table(colors.get("*"))
                if not selected_color:
                    colors_needed[icon_name] = [index, (1.0, 1.0, 1.0, 1.0)]
                    index += 1
        else:
            for icon_name in font.getGlyphOrder():
                if len(colors) == 1: 
                    r, g, b = 0, 0, 0
                    rgb = hex_to_rgb(colors[0])
                    r += float(rgb[0])/255.0
                    g += float(rgb[1])/255.0
                    b += float(rgb[2])/255.0
                    colors_needed[icon_name] = [index, (min(float(r), 1.0), min(float(g), 1.0), min(float(b)), 1.0)]
                    index += 1
                else:
                    r, g, b, t = 0, 0, 0, 0
                    for i in colors:
                        rgb = hex_to_rgb(i)
                        r += float(rgb[0])/255.0
                        g += float(rgb[1])/255.0
                        b += float(rgb[2])/255.0
                        t += 1
                    colors_needed[icon_name] = [index, (min(float(r / t), 1.0), min(float(g / t), 1.0), min(float(b / t), 1.0), 1.0)]
                    index += 1
        
        palettes_data = [
            [
                rgba for _, rgba in sorted(colors_needed.values(), key=lambda item: item[0])
            ]
        ]
        font['CPAL'] = buildCPAL(palettes_data)

        for glyph_name in font.getGlyphOrder():
            if glyph_name not in ['.notdef', '.null', 'space']:
                if glyph_name in font["glyf"] and hasattr(font["glyf"][glyph_name], 'xMin') and glyph_name not in handled_alignment:
                    glyph = font["glyf"][glyph_name]
                    glyph_width = glyph.xMax - glyph.xMin
                    new_aw = units
                    new_lsb = (units - glyph_width) / 2
                    font['hmtx'].metrics[glyph_name] = (int(round(new_aw) / 1.1), round(new_lsb))

        color_glyphs = {}
        for glyph_name in font.getGlyphOrder():
            if glyph_name not in ['.notdef', '.null', 'space']:
                color_glyphs[glyph_name] = [
                    (glyph_name, colors_needed[glyph_name][0])
                ]
        font['COLR'] = buildCOLR(color_glyphs)
        font_path.name = f"{font_path.stem}Custom{font_path.suffix}"
        font.save(Path(base_directory, font_path))
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
    return [i for i in blacklist if i not in authorized]
def get_old_icons(blocked: list=[]) -> dict[str]:
    icons = {}
    for i in os.listdir(os.path.join(CUR_PATH, "..", "resources", "old_icons")):
        j = i.split(".")[0]
        if j not in blocked: icons[j] = os.path.join(CUR_PATH, "..", "resources", "old_icons", i)
    return icons