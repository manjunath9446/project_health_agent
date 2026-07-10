from __future__ import annotations

from typing import Any


class ExcelErrorHandler:
    """
    Converts Excel error values into None.

    Handles:
    - #N/A
    - #VALUE!
    - #REF!
    - #DIV/0!
    - #NAME?
    - #NUM!
    - #NULL!
    - #UNPARSEABLE
    - NULL
    - N/A
    - NA
    - -
    - --
    - Empty strings
    """

    ERROR_VALUES = {
        "#N/A",
        "#VALUE!",
        "#REF!",
        "#DIV/0!",
        "#NAME?",
        "#NUM!",
        "#NULL!",
        "#UNPARSEABLE",
        "NULL",
        "N/A",
        "NA",
        "-",
        "--",
        "",
    }

    @classmethod
    def clean(cls, value: Any):

        if value is None:
            return None

        if isinstance(value, str):

            text = value.strip().upper()

            if text in cls.ERROR_VALUES:
                return None

        return value