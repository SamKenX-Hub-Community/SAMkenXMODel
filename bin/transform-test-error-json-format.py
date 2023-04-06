#!/usr/bin/env python
"""
Transform test error JSON file formatter (without prettier).

It makes error json easier to review by breaking down "errorMessage"
into list of strings (delimiter: ". ").
"""
import sys
from pathlib import Path

from typing_extensions import Final

# To allow this script to be executed from other directories
sys.path.insert(0, str(Path(__file__).absolute().parent.parent))

import json
from typing import Type

from bin._file_formatter import FileFormatter


class TransformTestErrorJSONFormatter(FileFormatter):
    _ERROR_MESSAGE_KEY: Final[str] = "errorMessage"
    _BREAKDOWN_ERROR_MESSAGE_KEY: Final[str] = "_autoGeneratedBreakdownErrorMessage"
    _DELIMITER: Final[str] = ". "

    @staticmethod
    def description() -> str:
        return "Transform test error JSON file formatter"

    def format_str(self, input_str: str) -> str:
        """
        It makes error json easier to review by breaking down "errorMessage"
        into list of strings (delimiter: ". ").
        """
        obj = json.loads(input_str)
        error_message = obj.get(self._ERROR_MESSAGE_KEY)
        if isinstance(error_message, str):
            tokens = error_message.split(self._DELIMITER)
            obj[self._BREAKDOWN_ERROR_MESSAGE_KEY] = [
                token if index == len(tokens) - 1 else token + self._DELIMITER for index, token in enumerate(tokens)
            ]
        return json.dumps(obj, indent=2, sort_keys=True) + "\n"

    @staticmethod
    def decode_exception() -> Type[Exception]:
        return json.JSONDecodeError

    @staticmethod
    def file_extension() -> str:
        return ".json"


if __name__ == "__main__":
    TransformTestErrorJSONFormatter.main()
