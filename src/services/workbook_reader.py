from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd
from loguru import logger


class WorkbookReader:
    """
    Reads all worksheets from an Excel workbook.

    Returns:
    {
        sheet_name: DataFrame
    }
    """

    def read(
        self,
        file_path: str,
    ) -> Dict[str, pd.DataFrame]:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(file_path)

        workbook = pd.read_excel(
            path,
            sheet_name=None,
            engine="openpyxl",
        )

        cleaned: Dict[str, pd.DataFrame] = {}

        for sheet_name, df in workbook.items():

            df = df.copy()

            # Clean column names
            df.columns = [
                str(col).strip()
                for col in df.columns
            ]

            # Remove completely empty columns
            df = df.dropna(
                axis=1,
                how="all",
            )

            cleaned[sheet_name.strip()] = df

        # =====================================================
        # DEBUG (Temporary)
        # =====================================================
        for sheet_name, df in cleaned.items():

            print("\n" + "=" * 100)
            print(f"SHEET : {sheet_name}")
            print("=" * 100)

            print("\nColumns:")
            print(df.columns.tolist())

            print("\nFirst 10 Rows:")
            print(df.head(10))

            print("\nShape:", df.shape)

            logger.info(
                f"{sheet_name} -> {df.shape[0]} rows x {df.shape[1]} columns"
            )

        return cleaned