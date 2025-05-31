import json
import re
import typing

import requests

from src.nodes.node import Node, get_nodes
from src.problem import Problem
from src.utils.general import string_to_json, to_json_string

LEETCODE_URL = "https://leetcode.com"
LEETCODE_GRAPHQL_URL = f"{LEETCODE_URL}/graphql"
LEETCODE_PROBLEM_URL_FORMAT = f"{LEETCODE_URL}/problems/{{}}"
LEETCODE_PROBLEM_URL_PATTERN = re.compile(LEETCODE_URL + r"/problems/[a-z\-]+")


def parse_leetcode_problem(obj: dict) -> Problem:
    code_snippet = {x["lang"]: x["code"] for x in obj["codeSnippets"]}["Python3"]

    return Problem(
        id=int(obj["questionId"]),
        slug=obj["titleSlug"],
        url=LEETCODE_PROBLEM_URL_FORMAT.format(obj["titleSlug"]),
        title=obj["title"],
        difficulty=obj["difficulty"],
        content=obj["content"],
        tags=[x["name"] for x in obj["topicTags"]],
        code_snippet=proc_leetcode_code_snippet(code_snippet),
        test_cases=extract_leetcode_test_cases(obj["content"]),
    )


def get_leetcode_problem_slug(problem_id: int) -> str | None:
    url = LEETCODE_GRAPHQL_URL
    headers = {
        "Content-Type": "application/json",
    }
    query = """
    {
        problemsetQuestionList: questionList(
            categorySlug: ""
            limit: 10000
            skip: 0
            filters: {}
        ) {
            questions: data {
                questionId
                title
                titleSlug
                difficulty
                topicTags {
                    name
                    slug
                }
            }
        }
    }
    """

    response = requests.post(url, json={"query": query}, headers=headers)
    response.raise_for_status()

    data = response.json()
    problems = data["data"]["problemsetQuestionList"]["questions"]

    if problem_id > len(problems):
        raise ValueError(f"Problem id={problem_id} not found")

    return problems[problem_id - 1]["titleSlug"]


def get_leetcode_problem_by_slug(problem_slug: str) -> Problem:
    url = LEETCODE_GRAPHQL_URL
    headers = {"Content-Type": "application/json"}
    query = """
    query getQuestionDetail($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            questionId
            titleSlug
            title
            difficulty
            content
            topicTags {
                name
            }
            codeSnippets {
                lang
                code
            }
        }
    }
    """
    variables = {"titleSlug": problem_slug}
    payload = {
        "query": query,
        "variables": variables,
        "operationName": "getQuestionDetail",
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    obj = response.json()["data"]["question"]

    if not obj:
        raise ValueError(f'Problem slug="{problem_slug}" not found')

    return parse_leetcode_problem(obj)


def get_leetcode_problem_by_id(problem_id: int) -> Problem:
    slug = get_leetcode_problem_slug(problem_id)
    return get_leetcode_problem_by_slug(slug)


def get_leetcode_daily_problem() -> Problem:
    url = LEETCODE_GRAPHQL_URL
    headers = {"Content-Type": "application/json"}
    query = """
    query dailyQuestion {
        activeDailyCodingChallengeQuestion {
            question {
                questionId
                titleSlug
                title
                difficulty
                content
                topicTags {
                    name
                }
                codeSnippets {
                    lang
                    code
                }
            }
        }
    }
    """
    payload = {"query": query}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    obj = response.json()["data"]["activeDailyCodingChallengeQuestion"]["question"]

    if not obj:
        raise ValueError("Daily problem not found")

    return parse_leetcode_problem(obj)


def extract_leetcode_test_cases(content: str) -> list[str]:
    content = re.sub(r"<[^>]+>", "", content)
    content = content.replace("&quot;", '"')

    inputs = [x[6:] for x in tuple(re.findall("Input:.*", content))]
    inputs = [tuple(re.findall("=[^=]+,", "".join(x.split()) + ",")) for x in inputs]
    inputs = [tuple(json.loads(a[1:-1]) for a in x) for x in inputs]
    outputs = [json.loads(x[7:]) for x in tuple(re.findall("Output:.*", content))]

    return [
        "\n".join(string_to_json(to_json_string(value)) for value in (*i, o)) + "\n"
        for i, o in zip(inputs, outputs)
    ]


def proc_leetcode_code_snippet(text: str) -> str:
    typing_names = [
        name for name in dir(typing) if not name.startswith("_") and name.istitle()
    ]
    node_classes_replace = [x.ALT_NAME for x in get_nodes() if x.ALT_NAME != "Node"]
    node_classes_import = {f"'{x.ALT_NAME}'": x for x in get_nodes()}

    commented_imports: set[type[Node]] = set()
    import_types: set[str] = set()
    lines = text.splitlines()
    i = 0

    while i < len(lines):
        # Добавить отступы к комментариям.
        if lines[i][:1] == "#" or lines[i][:3] in ('"""', "'''"):
            if lines[i][:3] in ('"""', "'''"):
                i += 1
                while i < len(lines) and lines[i][:3] not in ('"""', "'''"):
                    i += 1
                i += 1
            else:
                while i < len(lines) and lines[i][:1] == "#":
                    i += 1

            for _ in range(2):
                if i == len(lines):
                    break
                if lines[i].strip():
                    lines.insert(i, "")
                i += 1

        else:
            words = lines[i].split()
            if words and words[0] == "def":
                # Заменить классы Node на имена в кавычках (чтобы не импортировать).
                start_args = lines[i].find("(") + 1
                for name in node_classes_replace:
                    lines[i] = lines[i][:start_args] + lines[i][start_args:].replace(
                        name, f"'{name}'"
                    )

                # Добавить закомментированные импорты Nodes
                # (на случай если их нужно будет импортировать).
                for name, node_class in node_classes_import.items():
                    if name in lines[i][start_args:]:
                        commented_imports.add(node_class)

                # Добавить импорты типов.
                for name in typing_names:
                    if name in re.findall(r"\w+", lines[i]):
                        import_types.add(name)

                # Добавить pass в пустые реализации.
                while i < len(lines) and lines[i].strip():
                    i += 1
                if i == len(lines):
                    lines.append(" " * 8)
                lines[i] += "pass"

        i += 1

    if import_types or commented_imports:
        lines.insert(0, "")

    if commented_imports:
        lines.insert(0, "")
        for node_class in commented_imports:
            lines.insert(
                0,
                (
                    f"# from {node_class.__module__} import "
                    f"{node_class.__name__} as {node_class.ALT_NAME}"
                ),
            )

    if import_types:
        lines.insert(0, f'from typing import {", ".join(import_types)}\n')

    if lines[-1].strip():
        lines.append("")

    return "\n".join(lines)
