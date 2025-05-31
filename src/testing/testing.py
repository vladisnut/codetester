import os.path
from collections.abc import Callable, Iterable, Sequence
from importlib import import_module
from types import FunctionType, ModuleType
from typing import Any

from src.config import (
    LAUNCH_LAST_MODIFIED_SOLUTION,
    SOLUTION_DEFAULT_NAME,
    SOLUTION_SETTINGS_MODULE_NAME,
    SOLUTION_TESTS_FILE_NAME,
    SOLUTIONS_DIRECTORY,
)
from src.solution import get_last_modified_solution_name, get_solution_module
from src.testing.results.result import Result
from src.testing.testers.tester import (
    Tester,
    get_tester_by_name,
    get_tester_class_by_module,
)
from src.utils.file import read_text_file
from src.utils.style import print_message


def testing_module(
    tester_class: type[Tester],
    module: ModuleType,
    test_data: str | Iterable[tuple[Sequence, Any]],
    target: str = None,
    runner: Callable[[Any, Sequence], Any] = None,
    validator: Callable[[Sequence, Any, Any], bool] = None,
    show_time: bool = False,
    debug: bool = False,
) -> None:
    """
    :param tester_class: Класс-тестировщик модуля.
    :param module: Тестируемый модуль.
    :param test_data: Тестовые данные.
    :param target: Цель тестирования (функция, класс, метод).
    :param validator: Функция валидации результата теста.
    Принимает список аргументов теста, ожидаемое значение и результат.
    Возвращает логическое значение: был ли пройден тест.
    :param show_time: Показывать время выполнения каждого теста.
    :param debug: Выводить отладочные данные.
    """
    obj = tester_class.parse_module(module, target)
    obj.runner = runner

    if isinstance(test_data, str):
        test_data = (
            obj.split_test_set(x) for x in tester_class.parse_test_data(test_data)
        )

    for args, expected in test_data:
        obj.validate_args_and_expected(args, expected)
        result = obj.run(args, debug)

        result.validate(expected=expected, validator=validator, show_time=show_time)


def testing_solution(
    solution_name: str = None, show_time: bool = False, debug: bool = False
) -> None:
    # Получение имя решения.
    if not solution_name:
        if LAUNCH_LAST_MODIFIED_SOLUTION:
            solution_name = get_last_modified_solution_name()
        else:
            solution_name = SOLUTION_DEFAULT_NAME

    if not solution_name:
        raise Exception("No solutions found")

    # Загрузка настроек решения.
    try:
        settings_module = import_module(
            f"{SOLUTIONS_DIRECTORY}.{solution_name}.{SOLUTION_SETTINGS_MODULE_NAME}"
        )
        target = vars(settings_module).get("TARGET")
        tester = vars(settings_module).get("TESTER")
        validator = vars(settings_module).get("VALIDATOR")
        runner = vars(settings_module).get("RUNNER")

    except ModuleNotFoundError:
        settings_module = None
        tester = None
        validator = None
        target = None
        runner = None

    # Подготовка к тестированию.
    solution_module = get_solution_module(solution_name)

    if tester is not None:
        if not isinstance(tester, str):
            raise Exception("Tester must be specified by the string")
        tester_class = get_tester_by_name(tester)
        if not tester_class:
            raise Exception('Tester "{tester}" not found')
    else:
        tester_class = get_tester_class_by_module(solution_module)
        if not tester_class:
            raise Exception(
                f"There is no suitable testing class " f'for solution "{solution_name}"'
            )

    if (validator is not None) and (not isinstance(validator, FunctionType)):
        raise Exception("The validator must be a function")

    if (target is not None) and (not isinstance(target, str)):
        raise Exception("Test target must be specified by the string")

    print_message(f"Solution: {solution_name}")
    print_message(f"Type: {tester_class.NAME}")

    # Тестирование решения на тестовых данных с текстового файла.
    test_data_file_name = os.path.join(
        SOLUTIONS_DIRECTORY, solution_name, SOLUTION_TESTS_FILE_NAME
    )
    testing_module(
        tester_class=tester_class,
        module=solution_module,
        test_data=(
            read_text_file(test_data_file_name)
            if os.path.exists(test_data_file_name)
            else ""
        ),
        target=target,
        runner=runner,
        validator=validator,
        show_time=show_time,
        debug=debug,
    )

    # Тестирование решения на тестовых данных из файла с настройками решения.
    if settings_module:
        for test in vars(settings_module).get("TESTS") or []:
            if "args" in test:
                testing_module(
                    tester_class=tester_class,
                    module=solution_module,
                    test_data=[(test["args"], test.get("expected"))],
                    target=target,
                    runner=runner,
                    validator=validator,
                    show_time=show_time,
                    debug=debug,
                )

            elif "generator" in test:
                generator = test["generator"]
                if not generator:
                    continue
                count = test.get("count") or 1

                testing_module(
                    tester_class=tester_class,
                    module=solution_module,
                    test_data=(generator() for _ in range(count)),
                    target=target,
                    runner=runner,
                    validator=validator,
                    show_time=show_time,
                    debug=debug,
                )

    Result.print_status(show_time)
