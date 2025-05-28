import copy
import inspect
import json
import os
from typing import Any, Callable, Sequence

from config import SOLUTION_TEMPLATES_DIRECTORY, TEMPLATES_DIRECTORY
from src.nodes.node import get_node_classes
from src.utils.file import read_text_file
from src.utils.general import get_params_signature


def parse_test_data(test_data: str) -> list[str]:
    lines = [line.strip() for line in test_data.strip().splitlines()]
    if not lines:
        return []

    lines = [
        lines[i].strip()
        for i in range(len(lines))
        if i == 0 or lines[i].strip() or lines[i - 1].strip()
    ]
    return "\n".join(lines).split("\n\n")


def parse_test_data_as_lines(test_data: str) -> list[list]:
    """
    Парсинг тестовых данных как списка аргументов.
    Каждый аргумент находится в отдельной строке.
    Наборы тестовых данных разделяются хотя бы одной пустой строкой.
    """
    test_data_list = parse_test_data(test_data)
    if not test_data_list:
        return []

    return [
        [json.loads(line) for line in test_data.splitlines()]
        for test_data in test_data_list
    ]


def parse_test_data_as_stream(test_data: str) -> list[tuple[str, str]]:
    """
    Парсинг тестовых данных как поток аргументов.
    Аргументы можно писать как в одной строке, так и разделив
    их на несколько строк.
    Входные и выходные данные разделяются минимум одной пустой строкой.
    Наборы тестовых данных разделяются каждой второй последовательностью,
    состоящей минимум из одной пустой строки.
    """
    test_data_list = parse_test_data(test_data)
    if not test_data_list:
        return []

    if len(test_data_list) % 2 != 0:
        test_data_list.append("")

    return [
        (test_data_list[i - 1], test_data_list[i])
        for i in range(1, len(test_data_list), 2)
    ]


def proc_args_by_func(args: Sequence, func: Callable) -> list:
    """
    Конвертирует списки в классы Node (и списки списков),
    если соответствующие параметры функции имеют сигнатуру
    соответствующий Node.
    """
    result_args = list(copy.copy(args))
    signatures = get_params_signature(func)

    for i, (arg, (_, param_type)) in enumerate(zip(args, signatures)):
        for node_class in get_node_classes():
            annotation = str(param_type.annotation)
            if node_class.__name__ in annotation or node_class.ALT_NAME in annotation:
                if len(arg) and isinstance(arg[0], Sequence):
                    result_args[i] = [node_class.from_list(x) or [] for x in arg]
                else:
                    result_args[i] = node_class.from_list(arg) or []
                break

    return result_args


def proc_test_result(value: Any, func: Callable) -> Any:
    """
    Конвертирует значение в список, если оно является классом node.
    """
    sig = inspect.signature(func)
    return_annotation = str(sig.return_annotation)

    for node_class in get_node_classes():
        if isinstance(value, node_class):
            return value.to_list()
        if value is None and node_class.__name__ in return_annotation:
            return []

    return value


def get_header(name: str, width: int, line_char: str = "=") -> str:
    name = name.strip()

    lines_width, d = divmod(width - len(name) - 6, 2)
    left_line = line_char * max(0, lines_width)
    right_line = left_line + (line_char if (lines_width and d) else "")

    return f"{left_line} [ {name} ] {right_line}"


def get_template(name: str, group: str = None) -> str:
    paths = [TEMPLATES_DIRECTORY] + ([group] if group else [])
    return read_text_file(os.path.join(*paths, name) + ".py")


def get_solution_template_names() -> list[str]:
    return [os.path.splitext(x)[0] for x in os.listdir(SOLUTION_TEMPLATES_DIRECTORY)]
