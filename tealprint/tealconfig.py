from colored import fg

from .teallevel import TealLevel


class Colors:
    error = fg("red")
    warning = fg("dark_orange")


class TealConfig:
    level: TealLevel = TealLevel.info
    indent_char = " "
    indent_by: int = 4
    colors_default = Colors()
