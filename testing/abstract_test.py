from abc import abstractmethod
from typing import Sequence

from testing.result import Result


class AbstractTest:
    """
    Абстрактный класс типа тестирования.
    """

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def parse(cls, lines: Sequence) -> tuple['AbstractTest', list]:
        """
        :param lines: Строки данных одного теста.
        Каждый элемент перечисляется через запятую.
        """
        pass

    @abstractmethod
    def run(self) -> Result:
        """
        Выполнить тест.

        :return: Объект результата теста.
        """
        pass
