import copy
import time
from types import ModuleType
from typing import Any, Callable, Sequence

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
    get_classes_from_module,
    get_count_required_params,
    get_funcs_from_module,
    validate_signature,
)


class FunctionTester(Tester):
    """
    Тестировщик функции.
    Используется, когда нужно тестировать одну функцию.
    """

    NAME = "function"

    def __init__(self, func: Callable):
        super().__init__()
        self.__func = func

    @classmethod
    def verification_module(cls, module: ModuleType) -> bool:
        """
        В модуле должна быть хотя бы 1 функция.
        Функции с именем MAIN_FUNCTION_NAME быть не должно.
        Класса с именем SOLUTION_CLASS_NAME быть не должно.
        """
        funcs = get_funcs_from_module(module)
        if not funcs or {x.__name__: x for x in funcs}.get(MAIN_FUNCTION_NAME):
            return False

        classes = get_classes_from_module(module)
        if {x.__name__: x for x in classes}.get(SOLUTION_CLASS_NAME):
            return False

        return True

    @classmethod
    def parse_test_data(cls, test_data: str) -> list[list]:
        return parse_test_data_as_lines(test_data)

    @classmethod
    def parse_module(cls, module: ModuleType, target: str = None) -> "FunctionTester":
        funcs = get_funcs_from_module(module)
        if not funcs:
            raise Exception(f"Module {module.__name__} has no functions")

        if target:
            func = {x.__name__: x for x in funcs}.get(target)
            if not func:
                raise Exception(
                    f"Module {module.__name__} does not have function {target}"
                )
        else:
            func = funcs[0]

        return cls(func)

    def split_test_set(self, test_set: Sequence) -> tuple[Sequence, Any]:
        """
        Последний элемент – ожидаемый результат,
        если количество элементов N + 1,
        где N – количество параметров тестируемой функции.
        """
        count_params = get_count_required_params(self.__func)

        if len(test_set) > count_params + 1:
            raise Exception(
                f"Function {self.__func.__name__} has too many arguments "
                f"(more than {count_params}): {test_set}"
            )

        args = proc_args_by_func(test_set[:count_params], self.__func)
        expected = test_set[count_params] if len(test_set) > count_params else None

        return args, expected

    def validate_args_and_expected(self, args: Sequence, expected: Any) -> None:
        if not isinstance(args, Sequence):
            raise Exception(f"List of arguments must be a sequence: {args}")

        validate_signature(self.__func, *args)

    def run(self, args: Sequence, debug: bool = False) -> Result:
        args_after = copy.deepcopy(args)
        start_time = time.perf_counter()

        if self.runner:
            result = self.runner(self.__func, args_after)
        else:
            result = self.__func(*args_after)

        run_time = time.perf_counter() - start_time

        return ClassicResult(
            value=proc_test_result(result, self.__func),
            time=run_time,
            args_before=args,
            args_after=args_after,
        )
