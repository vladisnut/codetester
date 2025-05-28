import copy
import io
import sys
import time
from types import ModuleType
from typing import Any, Sequence

from config import MAIN_FUNCTION_NAME
from src.testing.results.result import Result
from src.testing.results.stream_result import StreamResult
from src.testing.testers.tester import Tester
from src.testing.utils import parse_test_data_as_stream
from src.utils.general import get_funcs_from_module


class StreamTester(Tester):
    """
    Потоковый тестировщик.
    Используется, когда нужно тестировать код используя операции ввода-вывода.
    """

    NAME = "stream"

    def __init__(self, main_func: type):
        super().__init__()
        self.__main_func = main_func

    @classmethod
    def verification_module(cls, module: ModuleType) -> bool:
        """
        В модуле должна быть функция MAIN_FUNCTION_NAME.
        """
        funcs = get_funcs_from_module(module)
        if not funcs:
            return False

        return bool({x.__name__: x for x in funcs}.get(MAIN_FUNCTION_NAME))

    @classmethod
    def parse_test_data(cls, test_data: str) -> list[list]:
        return [
            [[i], o if o else None] for i, o in parse_test_data_as_stream(test_data)
        ]

    @classmethod
    def parse_module(cls, module: ModuleType, target: str = None) -> "StreamTester":
        funcs = {x.__name__: x for x in get_funcs_from_module(module)}
        if not funcs:
            raise Exception(f"Module {module.__name__} has no functions")

        func_name = target or MAIN_FUNCTION_NAME
        func = funcs.get(func_name)
        if not func:
            raise Exception(
                f"Module {module.__name__} does not have function {func_name}"
            )

        return cls(func)

    def split_test_set(self, test_set: Sequence) -> tuple[Sequence, Any]:
        """
        1 элемент – строка входных данных.
        2 элемент – строка выходных данных.
        """
        if len(test_set) < 1:
            raise Exception(
                f"Tester set must have at least one element: input string: {test_set}"
            )

        if len(test_set) > 2:
            raise Exception(
                f"Tester set has too many parameters (more than 2): {test_set}"
            )

        return test_set[0], test_set[1]

    def validate_args_and_expected(self, args: Sequence, expected: Any) -> None:
        if not isinstance(args, Sequence):
            raise Exception(f"List of arguments must be a sequence: {args}")

        if not all(isinstance(x, str) for x in args):
            raise Exception(f"All elements of a test set must be strings: {args}")

        if expected is not None and not isinstance(expected, str):
            raise Exception(f"The expected value must be a string: {expected}")

    def run(self, args: Sequence, debug: bool = False) -> Result:
        if self.runner:
            args_after = copy.deepcopy(args)

            start_time = time.perf_counter()
            result = self.runner(self.__main_func, args_after)
            run_time = time.perf_counter() - start_time

        else:
            args_after = args
            try:
                input_stream = io.StringIO(args[0].strip())
                output_stream = io.StringIO()

                sys.stdin = input_stream
                sys.stdout = output_stream

                start_time = time.perf_counter()
                self.__main_func()
                run_time = time.perf_counter() - start_time
                result = output_stream.getvalue()

            finally:
                sys.stdin = sys.__stdin__
                sys.stdout = sys.__stdout__

        return StreamResult(
            value=result,
            time=run_time,
            args_before=args,
            args_after=args_after,
        )
