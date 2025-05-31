import webbrowser
from argparse import ArgumentParser

from src.commands.command import Command
from src.sources.source import (
    get_source_by_name,
    get_source_by_problem_url,
    get_source_names,
)


class LoadCommand(Command):
    """
    Загружает из указанного ресурса кодовую базу для решения
    задачи и тестовые данные в SOLUTIONS_DIRECTORY.
    """

    NAME = "load"

    def _init_args(self, parser: ArgumentParser) -> None:
        parser.add_argument("slug", help="Problem slug, id, or URL")
        parser.add_argument(
            "-s",
            "--source",
            default=None,
            choices=get_source_names(),
            help="Problem source",
        )
        parser.add_argument(
            "-o", "--open", action="store_true", help="Open in web browser"
        )

    def execute(self) -> None:
        if self.args.source:
            source = get_source_by_name(self.args.source)
            slug = self.args.slug
        else:
            if "https://" not in self.args.slug:
                raise Exception("If resource is not specified, slug must be a URL")
            url = self.args.slug
            source = get_source_by_problem_url(url)
            if not source:
                raise Exception(
                    f'URL "{url}" does not match the pattern of any resource'
                )
            slug = source.get_problem_slug_by_url(url)

        source.load(slug)

        if self.args.open:
            webbrowser.open(source.get_problem_url(slug))
