"""
PyKits v1.6.1 (MINI) | Made by Efaz from efaz.dev

A usable set of classes with extra functions that can be used within apps. \n
Import from file: 
```python
import PyKits
colors_class = PyKits.Colors()
```
Import from class: 

```python
import typing
class Colors: ...
colors_class = Colors()
```

However! Classes may depend on other classes. Use this resource list:
    Colors: typing (module)
    PyKitsIsAModule: None
"""

import typing
class Colors:
    class Color:
        def __init__(self, r: int, g: int, b: int):
            self.__colors_obj__ = Colors()
            r, g, b = self.__colors_obj__.limit_rgb_value(r), self.__colors_obj__.limit_rgb_value(g), self.__colors_obj__.limit_rgb_value(b)
            self.rgb = (r, g, b)
            self.hex = self.__colors_obj__.rgb_to_hex(r, g, b)
            self.ansi = self.__colors_obj__.hex_to_ansi2(self.hex)
            self.decimal = self.__colors_obj__.hex_to_decimal(self.hex)
        def __int__(self): return self.ansi
        def __str__(self): return f"Color[{', '.join([str(i) for i in self.rgb])}]"
        def wrap(self, message): return self.__colors_obj__.wrap(message, self.ansi)
        def grayscale(self): return self.__colors_obj__.apply_grayscale(*(self.rgb))
    class Black(Color):
        def __init__(self): 
            super().__init__(0, 0, 0)
            self.sgi = self.__colors_obj__.sgi_color_table["Black"]
        def __str__(self): return "Black"
    class Red(Color):
        def __init__(self): 
            super().__init__(255, 0, 0)
            self.sgi = self.__colors_obj__.sgi_color_table["Red"]
        def __str__(self): return "Red"
    class Yellow(Color):
        def __init__(self): 
            super().__init__(255, 255, 0)
            self.sgi = self.__colors_obj__.sgi_color_table["Yellow"]
        def __str__(self): return "Yellow"
    class Green(Color):
        def __init__(self): 
            super().__init__(0, 255, 0)
            self.sgi = self.__colors_obj__.sgi_color_table["Green"]
        def __str__(self): return "Green"
    class Teal(Color):
        def __init__(self): 
            super().__init__(0, 255, 255)
            self.sgi = self.__colors_obj__.sgi_color_table["Teal"]
        def __str__(self): return "Teal"
    class Blue(Color):
        def __init__(self): 
            super().__init__(0, 0, 255)
            self.sgi = self.__colors_obj__.sgi_color_table["Blue"]
        def __str__(self): return "Blue"
    class Magneta(Color):
        def __init__(self): 
            super().__init__(255, 0, 255)
            self.sgi = self.__colors_obj__.sgi_color_table["Magneta"]
        def __str__(self): return "Magneta"
    class White(Color):
        def __init__(self): 
            super().__init__(255, 255, 255)
            self.sgi = self.__colors_obj__.sgi_color_table["White"]
        def __str__(self): return "White"
    ansi_to_hex_table = {
        # 16 bit ANSI
        0: "#000000",  1: "#800000",  2: "#008000",  3: "#808000",
        4: "#000080",  5: "#800080",  6: "#008080",  7: "#c0c0c0",
        8: "#808080",  9: "#ff0000", 10: "#00ff00", 11: "#ffff00",
        12: "#0000ff", 13: "#ff00ff", 14: "#00ffff", 15: "#ffffff",

        # 256 bit ANSI
        16: "#000000", 17: "#00005f", 18: "#000087", 19: "#0000af", 20: "#0000d7", 21: "#0000ff",
        22: "#005f00", 23: "#005f5f", 24: "#005f87", 25: "#005faf", 26: "#005fd7", 27: "#005fff",
        28: "#008700", 29: "#00875f", 30: "#008787", 31: "#0087af", 32: "#0087d7", 33: "#0087ff",
        34: "#00af00", 35: "#00af5f", 36: "#00af87", 37: "#00afaf", 38: "#00afd7", 39: "#00afff",
        40: "#00d700", 41: "#00d75f", 42: "#00d787", 43: "#00d7af", 44: "#00d7d7", 45: "#00d7ff",
        46: "#00ff00", 47: "#00ff5f", 48: "#00ff87", 49: "#00ffaf", 50: "#00ffd7", 51: "#00ffff",
        52: "#5f0000", 53: "#5f005f", 54: "#5f0087", 55: "#5f00af", 56: "#5f00d7", 57: "#5f00ff",
        58: "#5f5f00", 59: "#5f5f5f", 60: "#5f5f87", 61: "#5f5faf", 62: "#5f5fd7", 63: "#5f5fff",
        64: "#5f8700", 65: "#5f875f", 66: "#5f8787", 67: "#5f87af", 68: "#5f87d7", 69: "#5f87ff",
        70: "#5faf00", 71: "#5faf5f", 72: "#5faf87", 73: "#5fafaf", 74: "#5fafd7", 75: "#5fafff",
        76: "#5fd700", 77: "#5fd75f", 78: "#5fd787", 79: "#5fd7af", 80: "#5fd7d7", 81: "#5fd7ff",
        82: "#5fff00", 83: "#5fff5f", 84: "#5fff87", 85: "#5fffaf", 86: "#5fffd7", 87: "#5fffff",
        88: "#870000", 89: "#87005f", 90: "#870087", 91: "#8700af", 92: "#8700d7", 93: "#8700ff",
        94: "#875f00", 95: "#875f5f", 96: "#875f87", 97: "#875faf", 98: "#875fd7", 99: "#875fff",
        100: "#878700", 101: "#87875f", 102: "#878787", 103: "#8787af", 104: "#8787d7", 105: "#8787ff",
        106: "#87af00", 107: "#87af5f", 108: "#87af87", 109: "#87afaf", 110: "#87afd7", 111: "#87afff",
        112: "#87d700", 113: "#87d75f", 114: "#87d787", 115: "#87d7af", 116: "#87d7d7", 117: "#87d7ff",
        118: "#87ff00", 119: "#87ff5f", 120: "#87ff87", 121: "#87ffaf", 122: "#87ffd7", 123: "#87ffff",
        124: "#af0000", 125: "#af005f", 126: "#af0087", 127: "#af00af", 128: "#af00d7", 129: "#af00ff",
        130: "#af5f00", 131: "#af5f5f", 132: "#af5f87", 133: "#af5faf", 134: "#af5fd7", 135: "#af5fff",
        136: "#af8700", 137: "#af875f", 138: "#af8787", 139: "#af87af", 140: "#af87d7", 141: "#af87ff",
        142: "#afaf00", 143: "#afaf5f", 144: "#afaf87", 145: "#afafaf", 146: "#afafd7", 147: "#afafff",
        148: "#afd700", 149: "#afd75f", 150: "#afd787", 151: "#afd7af", 152: "#afd7d7", 153: "#afd7ff",
        154: "#afff00", 155: "#afff5f", 156: "#afff87", 157: "#afffaf", 158: "#afffd7", 159: "#afffff",
        160: "#d70000", 161: "#d7005f", 162: "#d70087", 163: "#d700af", 164: "#d700d7", 165: "#d700ff",
        166: "#d75f00", 167: "#d75f5f", 168: "#d75f87", 169: "#d75faf", 170: "#d75fd7", 171: "#d75fff",
        172: "#d78700", 173: "#d7875f", 174: "#d78787", 175: "#d787af", 176: "#d787d7", 177: "#d787ff",
        178: "#d7af00", 179: "#d7af5f", 180: "#d7af87", 181: "#d7afaf", 182: "#d7afd7", 183: "#d7afff",
        184: "#d7d700", 185: "#d7d75f", 186: "#d7d787", 187: "#d7d7af", 188: "#d7d7d7", 189: "#d7d7ff",
        190: "#d7ff00", 191: "#d7ff5f", 192: "#d7ff87", 193: "#d7ffaf", 194: "#d7ffd7", 195: "#d7ffff",
        196: "#ff0000", 197: "#ff005f", 198: "#ff0087", 199: "#ff00af", 200: "#ff00d7", 201: "#ff00ff",
        202: "#ff5f00", 203: "#ff5f5f", 204: "#ff5f87", 205: "#ff5faf", 206: "#ff5fd7", 207: "#ff5fff",
        208: "#ff8700", 209: "#ff875f", 210: "#ff8787", 211: "#ff87af", 212: "#ff87d7", 213: "#ff87ff",
        214: "#ffaf00", 215: "#ffaf5f", 216: "#ffaf87", 217: "#ffafaf", 218: "#ffafd7", 219: "#ffafff",
        220: "#ffd700", 221: "#ffd75f", 222: "#ffd787", 223: "#ffd7af", 224: "#ffd7d7", 225: "#ffd7ff",
        226: "#ffff00", 227: "#ffff5f", 228: "#ffff87", 229: "#ffffaf", 230: "#ffffd7", 231: "#ffffff",

        # Grayscale
        232: "#080808", 233: "#121212", 234: "#1c1c1c", 235: "#262626",
        236: "#303030", 237: "#3a3a3a", 238: "#444444", 239: "#4e4e4e",
        240: "#585858", 241: "#626262", 242: "#6c6c6c", 243: "#767676",
        244: "#808080", 245: "#8a8a8a", 246: "#949494", 247: "#9e9e9e",
        248: "#a8a8a8", 249: "#b2b2b2", 250: "#bcbcbc", 251: "#c6c6c6",
        252: "#d0d0d0", 253: "#dadada", 254: "#e4e4e4", 255: "#eeeeee"
    }
    sgi_color_table = {
        "Black": [30, 90, 40, 100], 
        "Red": [31, 91, 41, 101], 
        "Green": [32, 92, 42, 102], 
        "Yellow": [33, 93, 43, 103], 
        "Blue": [34, 94, 44, 104], 
        "Magenta": [35, 95, 45, 105], 
        "Teal": [36, 96, 46, 106], 
        "White": [37, 97, 47, 107]
    }
    def __init__(self): import os, platform; self._os = os; self._platform = platform; self._main_os = platform.system()
    def fix_windows_ansi(self):
        def getIfRunningWindowsAdmin():
            if self._main_os == "Windows":
                try: import ctypes; return ctypes.windll.shell32.IsUserAnAdmin()
                except: return False
            else: return False
        if getIfRunningWindowsAdmin():
            if not hasattr(self, "_ctypes"): import ctypes; self._ctypes = ctypes
            kernel32 = self._ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)
            mode = self._ctypes.c_uint()
            kernel32.GetConsoleMode(handle, self._ctypes.byref(mode))
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)
    def get_reset_color(self): return "\033[0m"
    def get_ansi_start(self, ansi_num: int): 
        if isinstance(ansi_num, self.Color): ansi_num = ansi_num.ansi
        return f"\033[38;5;{ansi_num}m"
    def get_sgr_start(self, sgr_num: int): return f"\033[{sgr_num}m"
    def bold(self, message: str): return f"\033[1m{message}\033[0m"
    def italic(self, message: str): return f"\033[3m{message}\033[0m"
    def underline(self, message: str): return f"\033[4m{message}\033[0m"
    def strikethrough(self, message: str): return f"\033[9m{message}\033[0m"
    def clear_console(self): self._os.system("cls" if self._os.name == "nt" else 'echo "\033c\033[3J"; clear')
    def set_console_title(self, title: str):
        if self._platform.system() == "Windows": self._os.system(f"title {title}")
        else: self._os.system(f'echo "\\033]0;{title}\\007"')
    def foreground(self, message: str, color: str="White", bright: bool=False): 
        if isinstance(color, self.Color): color = color.__str__()
        return f"{self.get_sgr_start(self.sgi_color_table[color][1 if bright == True else 0])}{message}{self.get_reset_color()}"
    def background(self, message: str, color: str="White", bright: bool=False): 
        if isinstance(color, self.Color): color = color.__str__()
        return f"{self.get_sgr_start(self.sgi_color_table[color][3 if bright == True else 2])}{message}{self.get_reset_color()}"
    def wrap(self, message: str, ansi_num: int): return f"{self.get_ansi_start(ansi_num)}{message}{self.get_reset_color()}"
    def print(self, message: str, ansi_num: int): print(self.wrap(message=message, ansi_num=ansi_num))
    def print_gradient(self, message: str, color_stops: typing.List[str]): print(self.wrap_gradient(message=message, color_stops=color_stops))
    def hex_to_rgb(self, hex_code: str): hex_code = hex_code.lstrip("#"); return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
    def rgb_to_hex(self, r: int, g: int, b: int): r, g, b = self.limit_rgb_value(r), self.limit_rgb_value(g), self.limit_rgb_value(b); return f"#{r:02x}{g:02x}{b:02x}"
    def hex_to_gray(self, hex_code: str): return self.rgb_to_hex(*(self.apply_grayscale(*(self.hex_to_rgb(hex_code)))))
    def ansi_to_hex(self, ansi_num: int): return self.ansi_to_hex_table.get(ansi_num, "#000000")
    def decimal_to_rgb(self, value: int): return ((value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF)
    def rgb_to_decimal(self, r: int, g: int, b: int): return (self.limit_rgb_value(r) << 16) + (self.limit_rgb_value(g) << 8) + self.limit_rgb_value(b)
    def decimal_to_hex(self, value: int): return self.rgb_to_hex(*self.decimal_to_rgb(value))
    def hex_to_decimal(self, hex_code: str): return self.rgb_to_decimal(*self.hex_to_rgb(hex_code))
    def hex_to_ansi(self, hex_code: str):
        target_rgb = self.hex_to_rgb(hex_code)
        closest_code = None
        closest_dist = float("inf")
        for c, hex in self.ansi_to_hex_table.items():
            cr, cg, cb = self.hex_to_rgb(hex)
            dist = ((cr - target_rgb[0]) ** 2 + (cg - target_rgb[1]) ** 2 + (cb - target_rgb[2]) ** 2)
            if dist < closest_dist: closest_dist = dist; closest_code = c
        return closest_code
    def hex_to_ansi2(self, hex_code: str):
        closest_code = None
        closest_dist = float("inf")
        r, g, b = self.hex_to_rgb(hex_code)
        for c, hex in self.ansi_to_hex_table.items():
            cr, cg, cb = self.hex_to_rgb(hex)
            dist = (cr - r)**2 + (cg - g)**2 + (cb - b)**2
            if dist < closest_dist: closest_code = c; closest_dist = dist
        return closest_code
    def limit_rgb_value(self, value: int): return 0 if value < 0 else (255 if value > 255 else value)
    def gamma_correct(self, value: int): return (value / 255) ** 2.2
    def inverse_gamma(self, value: int): return int((value ** (1/2.2)) * 255)
    def apply_grayscale(self, r: int, g: int, b: int): res = int(0.299*r + 0.587*g + 0.114*b); return res, res, res
    def wrap_gradient(self, message: str, color_stops: typing.List[str]): 
        length = len(message)
        if length == 0 or len(color_stops) < 1: return message
        if len(color_stops) < 2: return self.wrap(message, self.hex_to_ansi(color_stops[0]))
        stops_rgb = []
        for hex_color in color_stops:
            if isinstance(hex_color, self.Color): hex_color = hex_color.hex
            r, g, b = self.hex_to_rgb(hex_color)
            stops_rgb.append((
                self.gamma_correct(r),
                self.gamma_correct(g),
                self.gamma_correct(b)
            ))
        result = ""
        num_segments = len(color_stops) - 1
        for i, char in enumerate(message):
            seg_length = length / num_segments
            seg_index = min(int(i / seg_length), num_segments - 1)
            start_rgb = stops_rgb[seg_index]
            end_rgb = stops_rgb[seg_index + 1]
            t = (i - seg_index * seg_length) / seg_length
            r = self.inverse_gamma(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * t)
            g = self.inverse_gamma(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * t)
            b = self.inverse_gamma(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * t)
            ansi_code = self.hex_to_ansi2(self.rgb_to_hex(r, g, b))
            result += f"{self.get_ansi_start(ansi_code)}{char}"
        return result + self.get_reset_color()
class PyKitsIsAModule(Exception): pass
if __name__ == "__main__": raise PyKitsIsAModule("PyKits is a module and not a runable instance!")