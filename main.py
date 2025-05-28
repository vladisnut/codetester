import sys

from src.commands.command import proc_command


def main() -> None:
    proc_command(sys.argv[1:])


if __name__ == "__main__":
    main()
