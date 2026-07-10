import re

import pandas as pd

from src.utils.date_utils import parse_date
from src.utils.dependency_parser import parse_dependencies
from src.core.normalization_constants import (
    STATUS_MAP,
    SCHEDULE_HEALTH_MAP,
    BOOLEAN_TRUE_VALUES,
)


class Normalizer:
    @staticmethod
    def normalize_duration(value):
        """
        Convert duration values into integer days.

        Examples:
            170d -> 170
            18d -> 18
            1d -> 1
            0 -> 0
            5 days -> 5
            None -> None
        """

        if value is None or pd.isna(value):
            return None

        if isinstance(value, int):
            return value

        if isinstance(value, float):
            return int(value)

        text = str(value).strip()

        if text == "":
            return None

        match = re.search(r"\d+", text)

        if match:
            return int(match.group())

        return None

    @staticmethod
    def normalize_task_row(row: dict) -> dict:
        norm = dict(row)

        # -------------------------------------------------
        # Status
        # -------------------------------------------------
        raw_status = str(row.get("status", "")).strip().lower()
        norm["normalized_status"] = STATUS_MAP.get(
            raw_status,
            "Not Started",
        )

        # -------------------------------------------------
        # Schedule Health
        # -------------------------------------------------
        raw_health = str(
            row.get("schedule_health", "")
        ).strip().lower()

        norm["normalized_schedule_health"] = (
            SCHEDULE_HEALTH_MAP.get(raw_health)
        )

        # -------------------------------------------------
        # Percent Complete
        # -------------------------------------------------
        try:
            norm["normalized_percent_complete"] = float(
                row.get("percent_complete", 0)
            )
        except (ValueError, TypeError):
            norm["normalized_percent_complete"] = 0.0

        # -------------------------------------------------
        # Dates
        # -------------------------------------------------
        norm["normalized_planned_start"] = parse_date(
            row.get("planned_start")
        )

        norm["normalized_planned_end"] = parse_date(
            row.get("planned_end")
        )

        # -------------------------------------------------
        # Duration
        # -------------------------------------------------
        norm["normalized_duration"] = (
            Normalizer.normalize_duration(
                row.get("duration")
            )
        )

        # -------------------------------------------------
        # Boolean Flags
        # -------------------------------------------------
        def to_bool(value):
            if value is None or pd.isna(value):
                return False

            if isinstance(value, bool):
                return value

            if isinstance(value, (int, float)):
                return bool(value)

            return (
                str(value).strip().lower()
                in BOOLEAN_TRUE_VALUES
            )

        norm["normalized_at_risk"] = to_bool(
            row.get("at_risk")
        )

        norm["normalized_on_hold"] = to_bool(
            row.get("on_hold")
        )

        norm["normalized_not_applicable"] = to_bool(
            row.get("not_applicable")
        )

        # -------------------------------------------------
        # Dependencies
        # -------------------------------------------------
        norm["normalized_dependencies"] = (
            parse_dependencies(
                row.get("predecessor_dependencies")
            )
        )

        # -------------------------------------------------
        # Owner
        # -------------------------------------------------
        owner = row.get("owner")

        norm["normalized_owner"] = (
            None
            if owner is None or pd.isna(owner)
            else str(owner).strip()
        )

        # -------------------------------------------------
        # Description
        # -------------------------------------------------
        description = row.get("description")

        norm["normalized_description"] = (
            None
            if description is None or pd.isna(description)
            else str(description).strip()
        )

        return norm

    @staticmethod
    def normalize_summary(summary: dict) -> dict:
        norm = dict(summary)

        # -----------------------------------------
        # Dates
        # -----------------------------------------
        for field in (
            "project_start",
            "project_end",
        ):
            norm[f"normalized_{field}"] = parse_date(
                summary.get(field)
            )

        # -----------------------------------------
        # Integer Fields
        # -----------------------------------------
        integer_fields = [
            "total_tasks",
            "completed_tasks",
            "in_progress_tasks",
            "not_started_tasks",
        ]

        for field in integer_fields:
            try:
                norm[f"normalized_{field}"] = int(
                    float(summary.get(field, 0))
                )
            except Exception:
                norm[f"normalized_{field}"] = 0

        return norm