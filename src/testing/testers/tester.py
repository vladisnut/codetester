from abc import abstractmethod
from collections.abc import Callable, Sequence
from types import ModuleType
from typing import Any

from src.testing.results.result import Result


class Tester:
    NAME: str = None

    def __init__(self):
        self.runner: Callable[[Any, Sequence], Any] | None = None

    @classmethod
    @abstractmethod
    def verification_module(cls, module: ModuleType) -> bool:
        """
        Проверка на то, что модуль подходит под данный класс тестирования.
        """

    @classmethod
    @abstractmethod
    def parse_test_data(cls, test_data: str) -> list[list]:
        """
        Парсинг тестовых данных. Возвращает список, где каждый элемент –
        список аргументов для каждого теста.
        """

    @classmethod
    @abstractmethod
    def parse_module(cls, module: ModuleType, target: str = None) -> "Tester":
        """
        Парсинг тестируемого модуля. Возвращает тестирующий класс.
        """

    @abstractmethod
    def split_test_set(self, test_set: Sequence) -> tuple[Sequence, Any]:
        """
        Разбивает последовательность тестовых данных кортеж
        из аргументов теста и его ожидаемый результат и возвращает его.

        :param test_set: Последовательность тестовых данных.
        """

    @abstractmethod
    def validate_args_and_expected(self, args: Sequence, expected: Any) -> None:
        """
        Проверка аргументов на правильный формат.
        """

    @abstractmethod
    def run(self, args: Sequence, debug: bool = False) -> Result:
        """
        Запускает тест.
        """


def get_tester_by_name(name: str) -> type[Tester]:
    return {x.NAME: x for x in Tester.__subclasses__()}.get(name)


def get_tester_class_by_module(module: ModuleType) -> type[Tester] | None:
    tester_classes = [
        cls for cls in Tester.__subclasses__() if cls.verification_module(module)
    ]
    return tester_classes[0] if tester_classes else None
