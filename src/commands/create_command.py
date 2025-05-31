from argparse import ArgumentParser

from src.commands.command import Command
from src.config import DEFAULT_SOLUTION_TEMPLATE_NAME, SOLUTION_DEFAULT_NAME
from src.solution import create_solution
from src.testing.utils import get_solution_template_names, get_template


class CreateCommand(Command):
    """
    Создает шаблон решения задачи в SOLUTIONS_DIRECTORY.
    """

    NAME = "create"

    def _init_args(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "solution",
            nargs="?",
            default=SOLUTION_DEFAULT_NAME,
            help="Template name",
        )
        parser.add_argument(
            "-t",
            "--template",
            nargs="?",
            default=DEFAULT_SOLUTION_TEMPLATE_NAME,
            choices=get_solution_template_names(),
            help="Solution name",
        )

    def execute(self) -> None:
        create_solution(
            name=self.args.solution,
            code_snippet=get_template(self.args.template),
        )
