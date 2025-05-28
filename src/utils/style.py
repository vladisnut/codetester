from enum import Enum
from typing import Any, Iterable


class Style(Enum):
    RESET = 0

    BOLD = 1
    ITALIC = 3
    UNDERLINE = 4

    NO_BOLD = 22
    NO_ITALIC = 23
    NO_UNDERLINE = 24

    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37

    def __str__(self):
        return f"\033[{self.value}m"


def bold(value: Any) -> str:
    return f"{Style.BOLD}{value}{Style.NO_BOLD}"


def italic(value: Any) -> str:
    return f"{Style.ITALIC}{value}{Style.NO_ITALIC}"


def underline(value: Any) -> str:
    return f"{Style.UNDERLINE}{value}{Style.NO_UNDERLINE}"


def print_in_style(styles: Style | Iterable[Style], *args, **kwargs) -> None:
    styles = [styles] if (type(styles) is Style) else styles
    sep = kwargs.get("sep") or " "
    message = "".join(map(str, styles)) + sep.join(map(str, args)) + str(Style.RESET)
    print(message, **kwargs)


def print_message(*args, **kwargs) -> None:
    print_in_style(Style.MAGENTA, *args, **kwargs)


def print_debug(*args, level: bool = False, **kwargs) -> None:
    args = ("[DEBUG]", *args) if level else args
    print_in_style(Style.BLUE, *args, **kwargs)


def print_warning(*args, level: bool = False, **kwargs) -> None:
    args = ("[WARNING]", *args) if level else args
    print_in_style(Style.YELLOW, *args, **kwargs)


def print_info(*args, level: bool = False, **kwargs) -> None:
    args = ("[INFO]", *args) if level else args
    print_in_style(Style.GREEN, *args, **kwargs)


def print_error(*args, level: bool = False, **kwargs) -> None:
    args = ("[ERROR]", *args) if level else args
    print_in_style(Style.RED, *args, **kwargs)
