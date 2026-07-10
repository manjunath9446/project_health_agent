from __future__ import annotations

from datetime import datetime, date
from typing import Any

import pandas as pd


class DateCleaner:
    """
    Cleans date values from Excel.

    Supports:
    ----------
    Excel Timestamp
    datetime
    date
    Excel serial dates
    11-Feb-2026
    11-Feb-26
    11/02/2026
    2026-02-11
    2026/02/11
    """

    DATE_FORMATS = [

        "%d-%b-%Y",
        "%d-%b-%y",

        "%d/%m/%Y",
        "%d/%m/%y",

        "%Y-%m-%d",
        "%Y/%m/%d",

        "%m/%d/%Y",
        "%m/%d/%y",

        "%d.%m.%Y",

    ]

    @classmethod
    def clean(
        cls,
        value: Any,
    ):

        if value is None:
            return None

        # ------------------------------
        # Pandas Timestamp
        # ------------------------------
        if isinstance(value, pd.Timestamp):
            return value.to_pydatetime()

        # ------------------------------
        # datetime
        # ------------------------------
        if isinstance(value, datetime):
            return value

        # ------------------------------
        # date
        # ------------------------------
        if isinstance(value, date):
            return datetime.combine(
                value,
                datetime.min.time(),
            )

        # ------------------------------
        # Excel serial number
        # ------------------------------
        if isinstance(value, (int, float)):

            try:
                return pd.to_datetime(
                    value,
                    unit="D",
                    origin="1899-12-30",
                ).to_pydatetime()

            except Exception:
                pass

        text = str(value).strip()

        if text == "":
            return None

        # ------------------------------
        # Try pandas parser
        # ------------------------------
        try:

            dt = pd.to_datetime(
                text,
                errors="raise",
            )

            return dt.to_pydatetime()

        except Exception:
            pass

        # ------------------------------
        # Try explicit formats
        # ------------------------------
        for fmt in cls.DATE_FORMATS:

            try:

                return datetime.strptime(
                    text,
                    fmt,
                )

            except Exception:
                continue

        return None