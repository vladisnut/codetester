import copy
import sys
import time
from typing import Sequence

from settings import DEBUG_COMMANDS, REQUIRED_EXPECTED_RESULT
from testing.abstract_test import AbstractTest
from testing.result import Result
from testing.general import TestDataError, proc_args_by_func
from utils.style import Style


class CommandTest(AbstractTest):
    """
    Класс тестирования для команд
    (когда нужно создать объект тестируемого класса и вызывать его методы).
    """

    def __init__(self, commands, args_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__commands = commands
        self.__args_list = args_list

    @classmethod
    def parse(cls, lines: Sequence) -> tuple[AbstractTest, list]:
        """
        1 строка: Список строковых команд
        (первая – название класса из файла solution.py, остальные – названия методов).
        2 строка: Списки аргументов каждой команды.
        3 строка: Список ожидаемых значений для каждой команды (необязательно).
        """
        if len(lines) not in (2, 3):
            raise TestDataError('Incorrect data format')

        commands = lines[0]
        args_list = lines[1]
        expectations = lines[2] if len(lines) >= 3 else None

        if REQUIRED_EXPECTED_RESULT and not expectations:
            raise TestDataError('Expected result not specified')

        return cls(commands, args_list), expectations

    def run(self):
        if (not isinstance(self.__commands, list) or
                tuple(x for x in self.__commands if not isinstance(x, str))):
            raise TestDataError('Incorrect command format: commands must be a list of strings')

        if not isinstance(self.__args_list, list):
            raise TestDataError('Incorrect command argument format: arguments must be in a list')

        try:
            cls = getattr(sys.modules['solution'], self.__commands[0])
        except AttributeError:
            raise NameError(self.__commands[0])

        commands = copy.deepcopy(self.__commands)
        args_list = copy.deepcopy(self.__args_list)

        start_time = time.time()
        obj = cls(*self.__args_list[0])
        results = [None]

        for command, args in zip(commands[1:], args_list[1:]):
            func = getattr(obj, command)
            args = proc_args_by_func(args, func)
            result = func(*args)

            if DEBUG_COMMANDS:
                print(Style.BLUE + f'{command}({", ".join(map(str, args))}): {result}')

            results.append(result)

        return Result(
            results,
            time.time() - start_time,
            self.__commands,
            self.__args_list
        )
