import re

from src.api.codeforces_api import (
    CODEFORCES_PROBLEM_URL_FORMAT,
    CODEFORCES_PROBLEM_URL_PATTERN,
    get_codeforces_problem,
)
from src.problem import Problem
from src.sources.source import Source


class Codeforces(Source):
    NAME = "codeforces"
    PROBLEM_URL_PATTERN = CODEFORCES_PROBLEM_URL_PATTERN

    @classmethod
    def _get_problem(cls, slug: str) -> Problem:
        return get_codeforces_problem(int(slug[:-1]), slug[-1])

    @classmethod
    def get_problem_url(cls, slug: str) -> str:
        return CODEFORCES_PROBLEM_URL_FORMAT.format(slug[:-1], slug[-1])

    @classmethod
    def get_problem_slug_by_url(cls, url: str) -> str | None:
        results = re.findall(cls.PROBLEM_URL_PATTERN, url)
        return "".join(results[0].split("/")[-2:]) if results else None
