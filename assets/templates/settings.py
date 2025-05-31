from collections.abc import Callable, Sequence
from typing import Any


def runner(target: type | Callable, args: Sequence) -> Any:
    """
    Пользовательская настройка запуска тестируемой цели.

    :param target: Тестируемая цель (функция или класс).
    :param args: Аргументы теста.
    :returns: Результат выполнения кода.
    """
    pass


def validator(
    args_before: Sequence, args_after: Sequence, expected: Any, result: Any
) -> bool:
    """
    Валидация результата теста.

    :param args_before: Аргументы до выполнения кода.
    :param args_after: Аргументы после выполнения кода.
    :param expected: Ожидаемый результат.
    :param result: Результат выполнения кода.
    :returns: True, если тест пройден, иначе False.
    """
    pass


def generator() -> tuple[Sequence, Any]:
    """
    Генерация тестового случая.

    :returns: Кортеж из двух элементов:
    последовательность аргументов теста, ожидаемое значение.
    """
    pass


# Допустимые значения:
# имя функции, класса или метода класса (в формате ClassName.methodName)
TARGET = None

# Допустимые значения:
# "function", "method", "class", "stream"
TESTER = None

# RUNNER = runner

# VALIDATOR = validator

TESTS = [
    # {
    #     'args': [],
    #     'expected': None
    # },
    # {
    #     'generator': generator,
    #     'count': 100
    # },
]
