import re
from abc import abstractmethod
from re import Pattern
from typing import AnyStr

from src.config import CREATE_NEW_SOLUTIONS, SOLUTION_DEFAULT_NAME
from src.problem import Problem
from src.solution import create_solution
from src.utils.style import print_message


class Source:
    NAME: str = None
    PROBLEM_URL_PATTERN: Pattern[AnyStr] = None

    @classmethod
    @abstractmethod
    def _get_problem(cls, slug: str) -> Problem:
        pass

    @classmethod
    def validate_problem_url(cls, url: str) -> None:
        if not re.match(cls.PROBLEM_URL_PATTERN, url):
            raise ValueError(f'URL "{url}" is not a link to a {cls.NAME} problem')

    @classmethod
    @abstractmethod
    def get_problem_url(cls, slug: str) -> str:
        pass

    @classmethod
    @abstractmethod
    def get_problem_slug_by_url(cls, url: str) -> str | None:
        pass

    @classmethod
    def _save(cls, problem: Problem) -> None:
        keys = ["id", "slug", "url", "title", "difficulty", "tags"]
        create_solution(
            name=problem.slug if CREATE_NEW_SOLUTIONS else SOLUTION_DEFAULT_NAME,
            code_snippet=problem.code_snippet,
            tests="\n".join(x for x in problem.test_cases),
            data={k: problem.__dict__[k] for k in keys},
            description=problem.content,
        )

    @classmethod
    def load(cls, slug: str) -> None:
        if "https://" in slug:
            cls.validate_problem_url(slug)
            slug = cls.get_problem_slug_by_url(slug)

        problem = cls._get_problem(slug)
        cls._save(problem)
        print_message(f'{cls.NAME.capitalize()} problem "{problem}" loaded')


def get_sources() -> list[type[Source]]:
    return Source.__subclasses__()


def get_source_by_name(name: str) -> type[Source]:
    return {x.NAME: x for x in Source.__subclasses__()}.get(name)


def get_source_names() -> list[str]:
    return [x.NAME for x in Source.__subclasses__()]


def get_source_by_problem_url(url: str) -> type[Source] | None:
    for source in get_sources():
        try:
            source.validate_problem_url(url)
            return source
        except ValueError:
            pass

    return None
