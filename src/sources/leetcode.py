import re
from typing import Optional

from src.api.leetcode_api import (
    LEETCODE_PROBLEM_URL_FORMAT,
    LEETCODE_PROBLEM_URL_PATTERN,
    get_leetcode_daily_problem,
    get_leetcode_problem_by_id,
    get_leetcode_problem_by_slug,
)
from src.problem import Problem
from src.sources.source import Source


class Leetcode(Source):
    NAME = "leetcode"
    PROBLEM_URL_PATTERN = LEETCODE_PROBLEM_URL_PATTERN
    DAILY_SLUG = "!daily"

    @classmethod
    def _get_problem(cls, slug: str) -> Problem:
        if slug == cls.DAILY_SLUG:
            return get_leetcode_daily_problem()

        if slug.isdigit():
            return get_leetcode_problem_by_id(int(slug))

        return get_leetcode_problem_by_slug(slug)

    @classmethod
    def get_problem_url(cls, slug: str) -> str:
        if not slug.isdigit() and slug != cls.DAILY_SLUG:
            return LEETCODE_PROBLEM_URL_FORMAT.format(slug)

        problem = cls._get_problem(slug)
        return LEETCODE_PROBLEM_URL_FORMAT.format(problem.slug)

    @classmethod
    def get_problem_slug_by_url(cls, url: str) -> Optional[str]:
        results = re.findall(cls.PROBLEM_URL_PATTERN, url)
        return results[0].split("/")[-1] if results else None
