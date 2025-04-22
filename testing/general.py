import importlib
import json
from inspect import signature
from types import FunctionType
from typing import Type, Iterable

from testing.abstract_test import AbstractTest
from testing.result import Result
from utils.list_node import ListNode, list_to_linked_list, linked_list_to_list
from utils.style import Style
from utils.tree_node import TreeNode, list_to_binary_tree, binary_tree_to_list


SOLUTION_MODULE_NAME = 'solution'
solution_module = importlib.import_module(SOLUTION_MODULE_NAME)

Solution = tuple(v for v in vars(solution_module).values() if type(v) is type and v.__module__ == SOLUTION_MODULE_NAME)
if not Solution:
    raise NotImplementedError(f'Module {SOLUTION_MODULE_NAME} has no class')

Solution = Solution[0]
solution_method_names = tuple(
    v.__name__ for v in Solution.__dict__.values()
    if type(v) == FunctionType and v.__name__[0] != '_'
)
if not solution_method_names:
    raise NotImplementedError(f'Class {Solution.__name__} from module {SOLUTION_MODULE_NAME} has no methods')


class TestDataError(Exception):
    def __init__(self, msg: str):
        self.msg = msg
        super().__init__()

    def __str__(self):
        return self.msg


def get_params_signature(func):
    return tuple(signature(func).parameters.items())


def proc_args_by_func(args: Iterable, func) -> list:
    proc_args = []
    signatures = get_params_signature(func)

    for arg, (_, param_type) in zip(args, signatures):
        if ListNode.__name__ in str(param_type):
            if isinstance(arg, list):
                if len(arg) and isinstance(arg[0], list):
                    arg = [list_to_linked_list(el) or [] for el in arg]
                else:
                    arg = list_to_linked_list(arg) or []

        if TreeNode.__name__ in str(param_type):
            if isinstance(arg, list):
                if len(arg) and isinstance(arg[0], list):
                    arg = [list_to_binary_tree(el) or [] for el in arg]
                else:
                    arg = list_to_binary_tree(arg) or []

        proc_args.append(arg)

    return proc_args


def proc_result(result):
    if isinstance(result, ListNode):
        return linked_list_to_list(result) or []

    if isinstance(result, TreeNode):
        return binary_tree_to_list(result) or []

    return result


def print_test_results():
    style = Style.BOLD + Style.UNDERLINE
    if Result.count_passed() == Result.count_runs():
        style += Style.GREEN
    else:
        style += Style.YELLOW

    print(f'{style}Tests passed: {Result.count_passed()}/{Result.count_runs()}')


def testing(
        cls: Type[AbstractTest],
        tests_data: str
):
    """
    Тестирование класса, находящегося в solution.py.

    :param cls: Тестирующий класс.
    :param tests_data: Текст с тестовыми данными.
    Его парсинг определяется тестирующим классом.
    """
    lines = [line.strip() for line in tests_data.strip().splitlines()]
    lines = [lines[i] for i in range(len(lines))
             if i == 0 or not(lines[i] == '' and lines[i-1] == '')]

    tests_data = '\n'.join(lines).split('\n\n')
    for data in tests_data:
        lines = [json.loads(line) for line in data.splitlines()]
        obj, expected = cls.parse(lines)
        obj.run().validate(expected)

    print_test_results()


def generate_and_testing(
        cls: Type[AbstractTest],
        generate_args_func,
        validation_func,
        count: int
):
    """
    Генерация тестовых данных и тестирование ими класса,
    находящегося в solution.py.

    :param cls: Тестирующий класс.
    :param generate_args_func: Функция генерации аргументов.
    Ничего не принимает, возвращает итерируемый объект с аргументами.
    :param validation_func: Функция валидации возвращенного результата.
    Принимает результат работы функции, возвращает логическое значение.
    :param count: Количество тестов.
    """
    for _ in range(count):
        args = generate_args_func()
        cls(*args).run().validate(validation_func)

    print_test_results()
