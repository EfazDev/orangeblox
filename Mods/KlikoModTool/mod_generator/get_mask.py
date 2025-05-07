from PIL import Image
from mod_generator.create_gradient_image import create_gradient_image

cache: dict[str, Image.Image] = {}

def get_mask(colors: list[str], angle: int, size: tuple[int, int]) -> Image.Image:
    # Generate a unique cache key based on all colors, angle, and size
    key = f"{'-'.join(colors)}-{angle}-{size[0]}-{size[1]}"
    
    if key in cache:
        return cache[key]
    
    if len(colors) == 1:
        # Solid color
        mask = Image.new("RGBA", size, colors[0])
    else:
        # Gradient with multiple colors
        mask = create_gradient_image(size, colors, angle)

    cache[key] = mask
    return mask

def clear_cache() -> None:
    cache.clear()
