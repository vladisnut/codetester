from typing import Any

from src.testing.results.result import Result
from src.utils.style import bold, italic, underline


class StreamResult(Result):
    def _get_result_message(self, success: bool, expected: Any) -> str:
        input_string = self.args_before[0].strip()
        output_string = self.value.strip()

        message = ""
        if input_string:
            message += f'{underline(bold("Input:"))}\n{input_string}'

        if output_string:
            message += "\n" if message else ""
            message += f'{underline(bold("Output:"))}\n{output_string}'

        if not success and expected.strip():
            message += "\n" if message else ""
            message += f'{underline(bold("Expected:"))}\n{expected.strip()}'

        return message if message else italic("No input no output...")

    def _validate_answer(self, expected: Any) -> bool:
        return expected is None or self.value.split() == expected.split()
