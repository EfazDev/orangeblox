from PIL import Image
import numpy as np
import sys

def hex_to_rgb(hex_color: str):
    hex_color = hex_color.lstrip("#")
    return np.array([int(hex_color[i:i+2], 16) for i in (0, 2, 4)])

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
    gradient = (gradient - gradient.min()) / (gradient.max() - gradient.min())

    scaled = gradient * num_segments
    indices = np.floor(scaled).astype(int)
    indices = np.clip(indices, 0, num_segments - 1)
    t = scaled - indices

    result = np.zeros((height, width, 3), dtype=np.uint8)
    for channel in range(3):
        c1 = np.array([color[channel] for color in rgb_colors])[indices]
        c2 = np.array([color[channel] for color in rgb_colors])[np.clip(indices + 1, 0, num_segments)]
        result[..., channel] = (c1 + (c2 - c1) * t).astype(np.uint8)

    return Image.fromarray(result)