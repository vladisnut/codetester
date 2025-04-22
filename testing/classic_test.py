import copy
import time
from typing import Sequence

from settings import REQUIRED_EXPECTED_RESULT
from testing.abstract_test import AbstractTest
from testing.result import Result
from testing.general import proc_args_by_func, Solution, proc_result, solution_method_names, get_params_signature, \
    TestDataError


class ClassicTest(AbstractTest):
    """
    Классический класс тестирования.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__args = args
        self.__kwargs = kwargs

    @classmethod
    def parse(cls, lines: Sequence) -> tuple[AbstractTest, list]:
        """
        1..N строки: Аргументы (в каждой строке свой аргумент).
        N+1 строка: Ожидаемое значение (необязательно).
        N – количество параметров тестируемой функции.
        """
        func = getattr(Solution(), solution_method_names[0])
        count_params = len(get_params_signature(func))
        if len(lines) < count_params:
            raise TestDataError('Incorrect number of arguments')

        args = lines[:count_params]
        expected = lines[count_params] if len(lines) > count_params else None

        if REQUIRED_EXPECTED_RESULT and not expected:
            raise TestDataError('Expected result not specified')

        args = proc_args_by_func(args, func)

        return cls(*args), expected

    def run(self):
        args = copy.deepcopy(self.__args)
        kwargs = copy.deepcopy(self.__kwargs)

        start_time = time.time()
        solution = Solution()
        func = getattr(solution, solution_method_names[0])
        result = func(*args, **kwargs)

        return Result(
            proc_result(result),
            time.time() - start_time,
            *self.__args,
            **self.__kwargs
        )
