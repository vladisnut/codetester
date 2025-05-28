import random
from typing import Any, Sequence


def validator(
    args_before: Sequence, args_after: Sequence, expected: Any, result: Any
) -> bool:
    """
    Возвращает True, если сумма индексов даёт число,
    которое есть в списке чисел, иначе False.
    """
    nums, target = args_before[0], args_before[1]
    i, j = result[0], result[1]
    return nums[i] + nums[j] == target


def generator(
    min_value: int, max_value: int, nums_max_len: int
) -> tuple[Sequence, Any]:
    """
    Базовый генератор.
    """
    nums = [
        random.randint(min_value, max_value)
        for _ in range(random.randint(2, nums_max_len))
    ]
    i, j = random.randint(0, len(nums) - 1), random.randint(1, len(nums) - 1)
    while i == j:
        j = random.randint(0, len(nums) - 1)

    return [nums, nums[i] + nums[j]], [i, j]


def normal_generator() -> tuple[Sequence, Any]:
    """
    Многократное тестирование алгоритма на средних объемах данных.
    """
    return generator(-1000, 1000, 100)


def stress_generator() -> tuple[Sequence, Any]:
    """
    Тестирование алгоритма на больших объемах данных
    для проверки на максимальное время выполнения алгоритма.
    """
    return generator(-(10**9), 10**9, 10**4)


# По умолчанию будет выбран method.
TESTER = None

# По умолчанию будет выбран Solution.twoSum.
TARGET = None

VALIDATOR = validator

TESTS = [
    {
        # Обычный тест, имеющий аргументы и ожидаемое значение.
        "args": [[2, 7, 11, 15], 18],
        "expected": [1, 2],
    },
    {
        # Генерация тестового случая, запускающаяся 100 раз.
        "generator": normal_generator,
        "count": 100,
    },
    {
        # Генерация тестового случая, запускающаяся 1 раз.
        "generator": stress_generator,
    },
]
