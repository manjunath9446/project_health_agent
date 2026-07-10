from __future__ import annotations

from typing import Dict

import pandas as pd


class SummaryExtractor:
    """
    Extracts project summary.

    Supports

    1. Key-value sheets

    Project Manager | John

    2. Traditional tables

    project_manager
    project_start
    project_end
    """

    FIELD_ALIASES = {
        "project_manager": [
            "project manager",
            "pm",
        ],
        "project_start": [
            "project start",
            "start date",
        ],
        "project_end": [
            "project end",
            "end date",
        ],
        "project_category": [
            "category",
        ],
        "overall_status": [
            "overall status",
            "status",
        ],
    }

    def extract(
        self,
        df: pd.DataFrame,
    ) -> Dict:

        if df.empty:
            return {}

        if len(df.columns) == 2:
            return self._extract_key_value(df)

        return self._extract_table(df)

    def _extract_key_value(
        self,
        df: pd.DataFrame,
    ) -> Dict:

        summary = {}

        for _, row in df.iterrows():

            key = str(row.iloc[0]).strip().lower()

            value = row.iloc[1]

            for std, aliases in self.FIELD_ALIASES.items():

                if key in aliases:
                    summary[std] = value

        return summary

    def _extract_table(
        self,
        df: pd.DataFrame,
    ) -> Dict:

        summary = {}

        cols = {
            str(c).strip().lower(): c
            for c in df.columns
        }

        if len(df) == 0:
            return summary

        first = df.iloc[0]

        for std, aliases in self.FIELD_ALIASES.items():

            for alias in aliases:

                if alias in cols:
                    summary[std] = first[cols[alias]]
                    break

        return summary