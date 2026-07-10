from __future__ import annotations

import re
from typing import Any


class NumericCleaner:
    """
    Cleans numeric values from Excel.

    Handles:
    --------
    1,250           -> 1250
    45%             -> 45
    13d             -> 13
    13 days         -> 13
    $2,500          -> 2500
    ₹1,20,000       -> 120000
    (250)           -> -250
    12.5            -> 12.5
    """

    @staticmethod
    def clean(value: Any):

        if value is None:
            return None

        if isinstance(value, (int, float)):
            return value

        text = str(value).strip()

        if text == "":
            return None

        # ----------------------------------------
        # Negative numbers in accounting format
        # Example: (250)
        # ----------------------------------------
        negative = False

        if text.startswith("(") and text.endswith(")"):
            negative = True
            text = text[1:-1]

        # ----------------------------------------
        # Remove currency symbols
        # ----------------------------------------
        text = (
            text.replace("$", "")
                .replace("₹", "")
                .replace("€", "")
                .replace("£", "")
        )

        # ----------------------------------------
        # Remove commas
        # ----------------------------------------
        text = text.replace(",", "")

        # ----------------------------------------
        # Remove percentage sign
        # ----------------------------------------
        text = text.replace("%", "")

        # ----------------------------------------
        # Remove duration suffixes
        # ----------------------------------------
        text = re.sub(
            r"\s*(day|days|d)$",
            "",
            text,
            flags=re.IGNORECASE,
        )

        text = text.strip()

        if text == "":
            return None

        # ----------------------------------------
        # Integer
        # ----------------------------------------
        try:
            number = int(text)

            if negative:
                number *= -1

            return number

        except Exception:
            pass

        # ----------------------------------------
        # Float
        # ----------------------------------------
        try:
            number = float(text)

            if negative:
                number *= -1

            return number

        except Exception:
            return value