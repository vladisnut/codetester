import webbrowser
from argparse import ArgumentParser

from src.commands.command import Command
from src.sources.source import get_source_by_problem_url, get_sources_dict


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
            choices=get_sources_dict().keys(),
            help="Problem source",
        )
        parser.add_argument(
            "-o", "--open", action="store_true", help="Open in web browser"
        )

    def execute(self) -> None:
        if self._args.source:
            source = get_sources_dict()[self._args.source]
            slug = self._args.slug
        else:
            if "https://" not in self._args.slug:
                raise Exception("If resource is not specified, slug must be a URL")
            url = self._args.slug
            source = get_source_by_problem_url(url)
            if not source:
                raise Exception(
                    f'URL "{url}" does not match the pattern of any resource'
                )
            slug = source.get_problem_slug_by_url(url)

        source.load(slug)

        if self._args.open:
            webbrowser.open(source.get_problem_url(slug))
