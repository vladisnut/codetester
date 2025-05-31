import argparse
import sys
import traceback
from abc import abstractmethod
from argparse import ArgumentParser, Namespace
from collections.abc import Sequence

from src.config import SOLUTION_MODULE_NAME
from src.utils.general import print_exc_from_level
from src.utils.style import print_error


class Command:
    NAME: str = None

    def __init__(self, args: Sequence[str]):
        parser = ArgumentParser()
        self._init_args(parser)
        self.__args = parser.parse_args(args)

    def _init_args(self, parser: ArgumentParser) -> None:
        pass

    @property
    def args(self) -> Namespace:
        return self.__args

    @abstractmethod
    def execute(self) -> None:
        pass


def get_command_by_name(name: str) -> type[Command]:
    return {x.NAME: x for x in Command.__subclasses__()}.get(name)


def get_command_names() -> list[str]:
    return [x.NAME for x in Command.__subclasses__()]


def proc_command(args: Sequence[str]) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=get_command_names(), help="Command")

    if not len(args):
        parser.print_help()
        return

    command_args = parser.parse_args([args[0]])
    command_class = get_command_by_name(command_args.command)

    try:
        command = command_class(args[1:])
        command.execute()

    except Exception as e:
        _, _, exc_traceback = sys.exc_info()
        stack_summary = traceback.extract_tb(exc_traceback)

        if any(
            (f"{SOLUTION_MODULE_NAME}.py" in frame.filename) for frame in stack_summary
        ):
            print_exc_from_level(5)
        else:
            traceback.print_exc()
            print_error(str(e), level=True)
