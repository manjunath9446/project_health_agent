from __future__ import annotations

from typing import Dict, List, Any

import pandas as pd

from src.services.parser_registry import BaseWorkbookParser
from src.services.workbook_profile_detector import WorkbookProfile


class GenericWorkbookParser(BaseWorkbookParser):
    """
    Converts any supported workbook into a flat normalized
    representation.

    Output contains NO hierarchy.

    Hierarchy will be built later.
    """

    def parse(
        self,
        workbook: Dict[str, pd.DataFrame],
        profile: WorkbookProfile,
    ) -> List[Dict[str, Any]]:

        if profile.plan_sheet is None:
            raise ValueError("No project plan sheet detected.")

        df = workbook[profile.plan_sheet]
        df = df.copy()

        df.columns = [
        str(c).strip().lower()
        for c in df.columns
            ]

        mapping = profile.field_mapping

        rows: List[Dict[str, Any]] = []

        for excel_index, (_, row) in enumerate(df.iterrows(), start=2):

            record = {
                "_source_sheet": profile.plan_sheet,
                "_source_row": excel_index,
            }

            for standard_field, excel_column in mapping.items():

                value = None

                if excel_column in df.columns:
                    value = row.get(excel_column)

                if pd.isna(value):
                    value = None

                record[standard_field] = value

            record["_depth"] = None

            rows.append(record)
            if excel_index < 10:
                print(record)

        return rows