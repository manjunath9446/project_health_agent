from __future__ import annotations

from typing import Dict, List, Any

from src.utils.text_cleaner import TextCleaner
from src.utils.excel_error_handler import ExcelErrorHandler
from src.utils.numeric_cleaner import NumericCleaner
from src.utils.date_cleaner import DateCleaner
from src.utils.boolean_cleaner import BooleanCleaner


class DataCleaningService:
    """
    Enterprise ETL Cleaning Layer.

    This service cleans every parsed row before
    the Normalizer is executed.

    Pipeline
    --------
    Raw Row
        ↓
    Text Cleaner
        ↓
    Excel Error Cleaner
        ↓
    Numeric Cleaner
        ↓
    Date Cleaner
        ↓
    Boolean Cleaner
        ↓
    Clean Row
    """

    NUMERIC_FIELDS = {
        "duration",
        "percent_complete",
        "total_float",
        "variance",
        "variance2",
        "baseline_variance",
    }

    DATE_FIELDS = {
        "planned_start",
        "planned_end",
        "baseline_start",
        "baseline_finish",
        "baseline_start2",
        "baseline_finish2",
        "project_start",
        "project_end",
    }

    BOOLEAN_FIELDS = {
        "critical",
        "critical_task",
        "at_risk",
        "on_hold",
        "not_applicable",
    }

    @classmethod
    def clean_row(
        cls,
        row: Dict[str, Any],
    ) -> Dict[str, Any]:

        cleaned = {}

        for key, value in row.items():

            # ----------------------------------
            # Step 1
            # Excel Errors
            # ----------------------------------

            value = ExcelErrorHandler.clean(value)

            # ----------------------------------
            # Step 2
            # Text cleanup
            # ----------------------------------

            value = TextCleaner.clean(value)

            # ----------------------------------
            # Step 3
            # Numeric cleanup
            # ----------------------------------

            if key in cls.NUMERIC_FIELDS:
                value = NumericCleaner.clean(value)

            # ----------------------------------
            # Step 4
            # Date cleanup
            # ----------------------------------

            elif key in cls.DATE_FIELDS:
                value = DateCleaner.clean(value)

            # ----------------------------------
            # Step 5
            # Boolean cleanup
            # ----------------------------------

            elif key in cls.BOOLEAN_FIELDS:
                value = BooleanCleaner.clean(value)

            cleaned[key] = value

        return cleaned

    # --------------------------------------------------------

    @classmethod
    def clean_rows(
        cls,
        rows: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:

        return [
            cls.clean_row(row)
            for row in rows
        ]