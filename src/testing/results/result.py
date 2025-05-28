from abc import abstractmethod
from typing import Any, Callable, Sequence

from config import HEADER_WIDTH
from src.testing.utils import get_header
from src.utils.general import time_to_string
from src.utils.style import Style, bold, italic, print_error, print_info, print_warning


class Result:
    """
    Класс, хранящий результаты работы тестируемой функции.
    """

    __count_runs = 0
    __count_passed = 0
    __tests_without_expected = []
    __total_time = 0

    def __init__(
        self, value: Any, time: float, args_before: Sequence, args_after: Sequence
    ):
        self.value = value
        self.time = time
        self.args_before = args_before
        self.args_after = args_after

    @classmethod
    def print_status(cls, show_time: bool = False) -> None:
        message = str(Style.BOLD) + get_header("RESULT", width=HEADER_WIDTH) + "\n"
        message += f"Tests passed: {cls.__count_passed}/{cls.__count_runs}"

        if show_time:
            message += f"\nTime: {time_to_string(cls.__total_time)}"

        if cls.__count_passed == cls.__count_runs:
            print_info(message)
        else:
            print_warning(message)

        if cls.__tests_without_expected:
            count = len(cls.__tests_without_expected)
            print_warning(
                f"{count} tests do not have expected results: "
                f"{cls.__tests_without_expected}",
                level=True,
            )

    @abstractmethod
    def _get_result_message(self, success: bool, expected: Any) -> str:
        raise NotImplementedError()

    def _validate_answer(self, expected: Any) -> bool:
        return expected is None or self.value == expected

    def validate(
        self,
        expected: Any = None,
        validator: Callable[[Sequence, Sequence, Any, Any], bool] = None,
        show_time: bool = False,
    ) -> bool:
        """
        Проверка результата теста.

        :param expected: Ожидаемый результат.
        :param validator: Функция валидации результата теста.
        Принимает список аргументов теста, ожидаемое значение и результат.
        Возвращает логическое значение: был ли пройден тест.
        :param show_time: Выводить время выполнения теста.
        """
        Result.__count_runs += 1
        Result.__total_time += self.time

        if expected is None and self.value is not None:
            Result.__tests_without_expected.append(Result.__count_runs)

        if validator:
            success = validator(self.args_before, self.args_after, expected, self.value)
        else:
            success = self._validate_answer(expected)

        if success:
            Result.__count_passed += 1

        print_func = print_info if success else print_error
        message = get_header(f"TEST {Result.__count_runs}", HEADER_WIDTH) + "\n"
        message += self._get_result_message(success, expected)

        if show_time:
            message += italic(bold(f"\n(Time: {time_to_string(self.time)})"))

        print_func(message + "\n")
        return success
