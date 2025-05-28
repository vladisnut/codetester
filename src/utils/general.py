import inspect
import sys
import traceback
from itertools import chain
from types import FunctionType, ModuleType
from typing import Any, Callable, Union, get_origin


def get_funcs_from_module(module: ModuleType) -> list[FunctionType]:
    return [
        v
        for v in vars(module).values()
        if type(v) is FunctionType and v.__module__ == module.__name__
    ]


def get_classes_from_module(module: ModuleType) -> list[type]:
    return [
        v
        for v in vars(module).values()
        if type(v) is type and v.__module__ == module.__name__
    ]


def get_class_method_names(cls: type) -> list[str]:
    return [
        v.__name__
        for v in cls.__dict__.values()
        if isinstance(v, FunctionType) and v.__name__[0] != "_"
    ]


def get_params_signature(func: Callable) -> list:
    return list(inspect.signature(func).parameters.items())


def get_count_required_params(func: Callable) -> int:
    return sum(
        1
        for _, v in inspect.signature(func).parameters.items()
        if v.default is inspect.Parameter.empty
    )


def validate_signature(func: Callable, *args, **kwargs) -> None:
    try:
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)

        for name, value in bound_args.arguments.items():
            param = sig.parameters[name]
            if param.annotation != inspect.Parameter.empty:
                annotation = get_origin(param.annotation) or param.annotation
                if (
                    not isinstance(annotation, str)
                    and annotation != Union
                    and not isinstance(value, annotation)
                ):
                    raise TypeError()

    except TypeError:
        raise TypeError(
            f"Arguments ({args_to_string(*args, **kwargs)}) "
            f"are not suitable for the signature of function "
            f"{func.__qualname__}({parameters_to_string(func)})"
        )


def time_to_string(t: float) -> str:
    data = [
        (1e-6, 1e9, "ns"),
        (1e-3, 1e6, "us"),
        (1.0, 1e3, "ms"),
    ]

    for t_max, d, unit in data:
        if t < t_max:
            return f"{round(t * d):,} {unit}"

    return f"{round(t, 3):,} s"


def to_json_string(value: Any) -> str:
    return f'"{value}"' if isinstance(value, str) else str(value)


def string_to_json(s: str) -> str:
    REPLACE_LIST = {
        "'": '"',
        "None": "null",
        "True": "true",
        "False": "false",
    }
    for key, value in REPLACE_LIST.items():
        s = s.replace(key, value)

    return s


def args_to_string(*args, **kwargs) -> str:
    return ", ".join(
        chain(
            map(to_json_string, args),
            (f"{k}={to_json_string(v)}" for k, v in kwargs.items()),
        )
    )


def parameters_to_string(func: Callable) -> str:
    parameters = inspect.signature(func).parameters.values()
    return ", ".join(map(str, parameters))


def print_exc_from_level(level: int = 0) -> None:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    if not exc_traceback:
        return

    for _ in range(level):
        if exc_traceback.tb_next:
            exc_traceback = exc_traceback.tb_next
        else:
            break

    truncated_tb = traceback.format_exception(exc_type, exc_value, exc_traceback)
    print("".join(truncated_tb), end="", file=sys.stderr)
