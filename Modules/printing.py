# 
# OrangeBlox 🍊
# Made by Efaz from efaz.dev
# v2.6.0i
# 

import sys
import traceback
import logging
import Modules.config as cf

def ts(mes: str):
    mes = str(mes)
    if hasattr(sys.stdout, "translate"): mes = cf.stdout.translate(mes)
    return mes
def trace():
    _, tb_v, tb_b = sys.exc_info()
    tb_lines = traceback.extract_tb(tb_b)
    lines = []
    lines.append(cf.colors_class.foreground("Traceback (most recent call last):", color="Magenta", bright=True))
    for fn, ln, f, tx in tb_lines:
        lines.append(f'  File {cf.colors_class.foreground(fn, color="Magenta", bright=True)}, line {cf.colors_class.foreground(ln, color="Magenta", bright=True)}, in {cf.colors_class.foreground(f, color="Magenta", bright=True)}')
        if tx: lines.append(f'    {tx}')
    exc_t = type(tb_v).__name__
    exc_m = str(tb_v)
    lines.append(f'{cf.colors_class.foreground(cf.colors_class.bold(f"{exc_t}:"), color="Magenta", bright=True)} {cf.colors_class.foreground(exc_m, color="Magenta", bright=False)}')
    return "\n".join(lines)
def obName0(): return str(cf.main_config.get("EFlagCustomBootstrapName", "OrangeBlox")).strip()
def obName1(): return str(cf.main_config.get("EFlagCustomBootstrapEmoji", "🍊")).strip()
def obColorA(): return cf.colors_class.hex_to_ansi2(cf.main_config.get("EFlagCustomBootstrapColor", "#ff4b00"))
def obColorH(): return str(cf.main_config.get("EFlagCustomBootstrapColor", "#ff4b00"))
def printMainMessage(mes): cf.colors_class.print(ts(mes), 255)
def printErrorMessage(mes): cf.colors_class.print(ts(mes), 196)
def printSuccessMessage(mes): cf.colors_class.print(ts(mes), 82)
def printWarnMessage(mes): cf.colors_class.print(ts(mes), 202)
def printSystemMessage(mes): cf.colors_class.print(ts(mes), obColorA())
def printYellowMessage(mes): cf.colors_class.print(ts(mes), 226)
def printDebugMessage(mes): 
    if cf.main_config.get("EFlagEnableDebugMode"): cf.colors_class.print(f"[DEBUG]: {ts(mes)}", 226); logging.debug(mes)

if __name__ == "__main__":
    print("This module is not a runable instance.")
    sys.exit(1)