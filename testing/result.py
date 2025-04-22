from types import FunctionType

from settings import SHOW_EXECUTION_TIME
from utils.style import Style


class Result:
    """
    Класс, хранящий результаты работы тестируемой функции.
    """
    __count_runs = 0
    __count_passed = 0

    def __init__(self, value, time, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.value = value
        self.time = time

    @classmethod
    def count_runs(cls):
        return cls.__count_runs

    @classmethod
    def count_passed(cls):
        return cls.__count_passed

    def validate(self, expected=None) -> bool:
        """
        Проверка результата теста.

        :param expected: Ожидаемое значение или функция валидации результата.
        """

        def proc_value(v):
            return f'"{v}"' if type(v) == str else str(v)

        Result.__count_runs += 1

        if isinstance(expected, FunctionType):
            success = expected(self.value)
        else:
            success = expected is None or self.value == expected

        message = Style.GREEN if success else Style.RED
        message += f'{"=" * 20} TEST {Result.__count_runs} {"=" * 20}\n'
        message += '\n'.join(proc_value(a) for a in self.args)
        message += '\n' if self.kwargs else ''
        message += '\n'.join(f'{k}={proc_value(v)}' for k, v in self.kwargs.items())
        message += f'\n{Style.BOLD}Result: {"" if success else "  "}{self.value}'

        if SHOW_EXECUTION_TIME:
            message += f'\n{Style.ITALIC}Time: {self.time}'

        if success:
            Result.__count_passed += 1
        else:
            message += f'\nExpected: {expected}'

        print(message + Style.RESET + '\n')
        return success
