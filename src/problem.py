from dataclasses import dataclass


@dataclass
class Problem:
    id: int
    slug: str
    url: str
    title: str
    difficulty: str
    content: str
    tags: list[str]
    code_snippet: str
    test_cases: list[str]

    def __str__(self):
        return f"{self.id}. {self.title}"
