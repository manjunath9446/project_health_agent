from __future__ import annotations

from typing import Any


class BooleanCleaner:
    """
    Cleans boolean values from Excel.

    TRUE VALUES
    -----------
    True
    true
    TRUE
    Yes
    YES
    Y
    1
    X
    ✔
    Complete

    FALSE VALUES
    ------------
    False
    false
    FALSE
    No
    NO
    N
    0
    ✘
    ""
    None
    """

    TRUE_VALUES = {
        "TRUE",
        "YES",
        "Y",
        "1",
        "X",
        "✔",
        "✓",
        "COMPLETE",
        "COMPLETED",
        "DONE",
        "ACTIVE",
    }

    FALSE_VALUES = {
        "FALSE",
        "NO",
        "N",
        "0",
        "",
        "NONE",
        "NULL",
        "NA",
        "N/A",
        "-",
    }

    @classmethod
    def clean(
        cls,
        value: Any,
    ) -> bool | None:

        if value is None:
            return None

        # Already boolean
        if isinstance(value, bool):
            return value

        # Integer / Float
        if isinstance(value, (int, float)):
            return bool(value)

        text = str(value).strip().upper()

        if text in cls.TRUE_VALUES:
            return True

        if text in cls.FALSE_VALUES:
            return False

        # Unknown value
        return None