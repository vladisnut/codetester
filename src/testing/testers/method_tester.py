import copy
import time
from collections.abc import Callable, Sequence
from types import ModuleType
from typing import Any

from src.config import MAIN_FUNCTION_NAME, SOLUTION_CLASS_NAME
from src.testing.results.classic_result import ClassicResult
from src.testing.results.result import Result
from src.testing.testers.tester import Tester
from src.testing.utils import (
    parse_test_data_as_lines,
    proc_args_by_func,
    proc_test_result,
)
from src.utils.general import (
    get_class_method_names,
    get_classes_from_module,
    get_count_required_params,
    get_funcs_from_module,
    validate_signature,
)


class MethodTester(Tester):
    """
    Тестировщик метода класса.
    Используется, когда нужно тестировать один метод класса.
    """

    NAME = "method"

    def __init__(self, class_: type, method_name: str):
        super().__init__()
        self.__class = class_
        self.__method_name = method_name

    @classmethod
    def verification_module(cls, module: ModuleType) -> bool:
        """
        В модуле должен быть класс с именем SOLUTION_CLASS_NAME с хотя бы 1 методом.
        Функции с именем MAIN_FUNCTION_NAME быть не должно.
        """
        if {x.__name__: x for x in get_funcs_from_module(module)}.get(
            MAIN_FUNCTION_NAME
        ):
            return False

        classes = get_classes_from_module(module)
        if not classes:
            return False

        solution_class = {x.__name__: x for x in classes}.get(SOLUTION_CLASS_NAME)
        if not solution_class:
            return False

        return len(get_class_method_names(solution_class)) > 0

    @classmethod
    def parse_test_data(cls, test_data: str) -> list[list]:
        return parse_test_data_as_lines(test_data)

    @classmethod
    def parse_module(cls, module: ModuleType, target: str = None) -> "MethodTester":
        classes = {x.__name__: x for x in get_classes_from_module(module)}

        if target:
            if "." not in target:
                target = f"{SOLUTION_CLASS_NAME}.target"

            if len(target.split(".")) > 2:
                raise Exception(f"Searching nested classes is not supported ({target})")
            else:
                class_name = target.split(".")[0]
                test_class = classes.get(class_name)
        else:
            test_class = classes.get(SOLUTION_CLASS_NAME)

        if not test_class:
            raise Exception(
                f"Module {module.__name__} does not have class {SOLUTION_CLASS_NAME}"
            )

        method_names = get_class_method_names(test_class)
        if not method_names:
            raise Exception(
                f"Class {SOLUTION_CLASS_NAME} does not have any matching methods"
            )

        if target:
            method_name = target.split(".")[1] if "." in target else target
            attr = getattr(test_class, method_name, None)
            if not isinstance(attr, Callable):
                raise Exception(
                    f"Target method {method_name} in module {module.__name__} not found"
                )
        else:
            method_name = method_names[0]

        return cls(test_class, method_name)

    def split_test_set(self, test_set: Sequence) -> tuple[Sequence, Any]:
        """
        Последний элемент – ожидаемый результат,
        если количество элементов N + 1,
        где N – количество параметров тестируемой функции.
        """
        obj = self.__class()
        func = getattr(obj, self.__method_name)
        count_params = get_count_required_params(func)

        if len(test_set) > count_params + 1:
            raise Exception(
                f"Function {func.__name__} has too many arguments "
                f"(more than {count_params}): {test_set}"
            )

        args = proc_args_by_func(test_set[:count_params], func)
        expected = test_set[count_params] if len(test_set) > count_params else None

        return args, expected

    def validate_args_and_expected(self, args: Sequence, expected: Any) -> None:
        if not isinstance(args, Sequence):
            raise Exception(f"List of arguments must be a sequence: {args}")

        validate_signature(getattr(self.__class(), self.__method_name), *args)

    def run(self, args: Sequence, debug: bool = False) -> Result:
        args_after = copy.deepcopy(args)
        func = None
        start_time = time.perf_counter()

        if self.runner:
            result = self.runner(self.__class, args_after)
        else:
            obj = self.__class()
            func = getattr(obj, self.__method_name)
            result = func(*args_after)

        run_time = time.perf_counter() - start_time
        if not func:
            func = getattr(self.__class(), self.__method_name)

        return ClassicResult(
            value=proc_test_result(result, func),
            time=run_time,
            args_before=args,
            args_after=args_after,
        )
