import json
import os
from importlib import import_module
from types import ModuleType
from typing import Optional

from config import (
    SOLUTION_DATA_FILE_NAME,
    SOLUTION_DESCRIPTION_FILE_NAME,
    SOLUTION_MODULE_NAME,
    SOLUTION_SETTINGS_MODULE_NAME,
    SOLUTION_SETTINGS_TEMPLATE_NAME,
    SOLUTION_TESTS_FILE_NAME,
    SOLUTIONS_DIRECTORY,
)
from src.testing.utils import get_template
from src.utils.file import create_text_file, read_text_file


def get_solution_names() -> list[str]:
    if not os.path.exists(SOLUTIONS_DIRECTORY):
        return []

    return [d for d in os.listdir(SOLUTIONS_DIRECTORY) if d[0] != "_"]


def get_solution_name_by_problem_id(problem_id: int) -> Optional[str]:
    for solution in get_solution_names():
        file_name = os.path.join(SOLUTIONS_DIRECTORY, solution, SOLUTION_DATA_FILE_NAME)
        if not os.path.exists(file_name):
            continue

        data = json.loads(read_text_file(file_name))
        if data.get("id") == problem_id:
            return solution

    return None


def get_solution_module(solution_name: str) -> ModuleType:
    try:
        return import_module(
            f"{SOLUTIONS_DIRECTORY}.{solution_name}.{SOLUTION_MODULE_NAME}"
        )

    except ModuleNotFoundError:
        if solution_name.isdigit():
            problem_id = int(solution_name)
            solution_name = get_solution_name_by_problem_id(problem_id)
            if not solution_name:
                raise Exception(f"There is no solution id={problem_id}")
            return import_module(
                f"{SOLUTIONS_DIRECTORY}.{solution_name}.{SOLUTION_MODULE_NAME}"
            )
        else:
            raise Exception(f'There is no solution named "{solution_name}"')


def get_last_modified_solution_name() -> Optional[str]:
    if not os.path.exists(SOLUTIONS_DIRECTORY):
        return None

    times = sorted(
        [
            (os.path.getmtime(os.path.join(SOLUTIONS_DIRECTORY, solution)), solution)
            for solution in get_solution_names()
        ],
        reverse=True,
    )

    return times[0][1] if len(times) else None


def create_solution(
    name: str,
    code_snippet: str = "",
    tests: str = "",
    data: dict = None,
    description: str = None,
) -> None:
    path = os.path.join(SOLUTIONS_DIRECTORY, name)
    os.makedirs(path, exist_ok=True)

    create_text_file(os.path.join(path, f"{SOLUTION_MODULE_NAME}.py"), code_snippet)
    create_text_file(
        os.path.join(path, f"{SOLUTION_SETTINGS_MODULE_NAME}.py"),
        get_template(SOLUTION_SETTINGS_TEMPLATE_NAME),
    )
    create_text_file(os.path.join(path, SOLUTION_TESTS_FILE_NAME), tests)

    data_file_name = os.path.join(path, SOLUTION_DATA_FILE_NAME)
    if data:
        create_text_file(data_file_name, json.dumps(data, ensure_ascii=False, indent=4))
    elif os.path.exists(data_file_name):
        os.remove(data_file_name)

    description_file_name = os.path.join(path, SOLUTION_DESCRIPTION_FILE_NAME)
    if description:
        create_text_file(description_file_name, description)
    elif os.path.exists(description_file_name):
        os.remove(description_file_name)
