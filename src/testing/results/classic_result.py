from typing import Any

from src.testing.results.result import Result
from src.utils.general import string_to_json, to_json_string
from src.utils.style import bold, underline


class ClassicResult(Result):
    def _get_result_message(self, success: bool, expected: Any) -> str:
        args_before = "\n".join(to_json_string(a) for a in self.args_before)
        message = args_before + "\n" if args_before else ""

        if self.args_before != self.args_after:
            message += underline(bold("Arguments after:")) + "\n"
            message += "\n".join(to_json_string(a) for a in self.args_after) + "\n"

        message += (
            underline(bold("Result:"))
            + " "
            + ("" if success else "  ")
            + to_json_string(self.value)
        )
        message += (
            ""
            if success
            else f'\n{underline(bold("Expected:"))} {to_json_string(expected)}'
        )

        return string_to_json(message)
