import copy
import time
from types import ModuleType
from typing import Any, Sequence

from config import MAIN_FUNCTION_NAME, SOLUTION_CLASS_NAME
from src.testing.results.classic_result import ClassicResult
from src.testing.results.result import Result
from src.testing.testers.tester import Tester
from src.testing.utils import (
    parse_test_data_as_lines,
    proc_args_by_func,
    proc_test_result,
)
from src.utils.general import (
    get_class_method_names,
    get_classes_from_module,
    get_funcs_from_module,
    validate_signature,
)
from src.utils.style import print_debug


class ClassTester(Tester):
    """
    Тестировщик класса.
    Используется, когда нужно создавать объект тестируемого класса
    и вызывать его методы.
    """

    NAME = "class"

    def __init__(self, class_: type):
        super().__init__()
        self.__class = class_

    @classmethod
    def verification_module(cls, module: ModuleType) -> bool:
        """
        В модуле должен быть хотя бы 1 класс с минимум 2 методами.
        Класса с именем SOLUTION_CLASS_NAME быть не должно.
        Функции с именем MAIN_FUNCTION_NAME быть не должно.
        """
        if {x.__name__: x for x in get_funcs_from_module(module)}.get(
            MAIN_FUNCTION_NAME
        ):
            return False

        classes = get_classes_from_module(module)
        if not classes or {x.__name__: x for x in classes}.get(SOLUTION_CLASS_NAME):
            return False

        return len(get_class_method_names(classes[0])) > 1

    @classmethod
    def parse_test_data(cls, test_data: str) -> list[list]:
        return parse_test_data_as_lines(test_data)

    @classmethod
    def parse_module(cls, module: ModuleType, target: str = None) -> "ClassTester":
        classes = get_classes_from_module(module)
        if not classes:
            raise Exception(f"Module {module.__name__} has no classes")

        if target:
            test_class = {x.__name__: x for x in classes}.get(target)
            if not test_class:
                raise Exception(
                    f"Target class {target} in module {module.__name__} not found"
                )
        else:
            test_class = classes[0]

        return cls(test_class)

    def split_test_set(self, test_set: Sequence) -> tuple[Sequence, Any]:
        """
        1 элемент: Список строковых команд
        (первая – название класса, остальные – названия вызываемых методов).
        2 элемент: Списки аргументов каждой команды.
        3 элемент: Список ожидаемых результатов для каждой команды (необязательно).
        """
        if len(test_set) < 2:
            raise Exception(
                "A test suite must have at least 2 elements: a list of string commands "
                f"and a list of arguments for each command: {test_set}"
            )

        if len(test_set) > 3:
            raise Exception(
                f"Tester set has too many parameters (more than 3): {test_set}"
            )

        commands = test_set[0]
        args_list = test_set[1]
        expected = test_set[2] if len(test_set) >= 3 else None

        return (commands, args_list), expected

    def validate_args_and_expected(self, args: Sequence, expected: Any) -> None:
        if not isinstance(args, Sequence):
            raise Exception(f"List of arguments must be a sequence: {args}")

        commands = args[0]
        args_list = args[1]
        test_set = (commands, args_list, expected)

        if not all(isinstance(x, Sequence) for x in test_set):
            raise Exception(f"All elements of a test set must be lists: {test_set}")

        if len(set(map(len, test_set))) != 1:
            raise Exception(
                f"All elements of the test set must have the same length: {test_set}"
            )

        if not isinstance(commands, Sequence) or tuple(
            x for x in commands if not isinstance(x, str)
        ):
            raise Exception(
                "The first element of a test set (commands) "
                f"must be a list of strings: {commands}"
            )

        if not isinstance(args_list, Sequence):
            raise Exception(
                "The second element of the test suite (command arguments) "
                f"must be lists: {args_list}"
            )

        obj = self.__class(*args_list[0])
        for method_name, method_args in zip(commands[1:], args_list[1:]):
            validate_signature(getattr(obj, method_name), *method_args)

    def run(self, args: Sequence, debug: bool = False) -> Result:
        args_after = copy.deepcopy(args)
        commands = args[0]
        args_list_after = args_after[1]
        results = [None]

        start_time = time.perf_counter()

        if self.runner:
            results = self.runner(self.__class, args_after)
        else:
            obj = self.__class(*args_list_after[0])
            for method_name, method_args in zip(commands[1:], args_list_after[1:]):
                func = getattr(obj, method_name)
                method_args = proc_args_by_func(method_args, func)
                result = func(*method_args)
                if debug:
                    print_debug(
                        f'{method_name}({", ".join(map(str, method_args))}): {result}'
                    )
                results.append(proc_test_result(result, func))

        run_time = time.perf_counter() - start_time

        return ClassicResult(
            value=results,
            time=run_time,
            args_before=args,
            args_after=args_after,
        )
