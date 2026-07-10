from __future__ import annotations

import re
import unicodedata
from typing import Any


class TextCleaner:
    """
    Cleans text values before normalization.

    Handles:
    - Leading/trailing whitespace
    - Multiple spaces
    - Tabs
    - Newlines
    - Unicode invisible characters
    - Non-breaking spaces
    """

    @staticmethod
    def clean(value: Any):

        if value is None:
            return None

        if not isinstance(value, str):
            return value

        # Unicode normalization
        text = unicodedata.normalize("NFKC", value)

        # Replace non-breaking spaces
        text = text.replace("\u00A0", " ")

        # Remove zero-width characters
        text = re.sub(
            r"[\u200B-\u200D\uFEFF]",
            "",
            text,
        )

        # Replace tabs/newlines
        text = (
            text.replace("\t", " ")
                .replace("\n", " ")
                .replace("\r", " ")
        )

        # Collapse multiple spaces
        text = re.sub(r"\s+", " ", text)

        text = text.strip()

        if text == "":
            return None

        return text