from argparse import ArgumentParser

from src.commands.command import Command
from src.testing.testing import testing_solution


class TestCommand(Command):
    """
    Тестирует код заданного решения из SOLUTIONS_DIRECTORY.
    Тесты в test.txt должны быть разделены хотя бы одной пустой строкой.
    Первые N строк теста – входные параметры тестируемого кода.
    (N + 1)-я строка содержит ожидаемый результат (необязательно).
    """

    NAME = "test"

    def _init_args(self, parser: ArgumentParser) -> None:
        parser.add_argument("solution", nargs="?", help="Solution name")
        parser.add_argument(
            "-t",
            "--time",
            action="store_true",
            help="Print execution time of each test",
        )
        parser.add_argument("-d", "--debug", action="store_true", help="Debug mode")

    def execute(self) -> None:
        testing_solution(self._args.solution, self._args.time, self._args.debug)
