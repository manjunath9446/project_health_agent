from __future__ import annotations

from typing import Dict, List

import pandas as pd


class CommentExtractor:
    """
    Extract comments from any worksheet.

    Supports:

    1. Structured comments
    2. Meeting notes
    3. Free text sheets
    """

    COMMENT_HEADERS = [
        "comment",
        "comments",
        "remark",
        "remarks",
        "note",
        "notes",
        "discussion",
        "action",
        "action item",
    ]

    AUTHOR_HEADERS = [
        "author",
        "owner",
        "resource",
        "created by",
    ]

    DATE_HEADERS = [
        "date",
        "created",
        "updated",
    ]

    def extract(
        self,
        workbook: Dict[str, pd.DataFrame],
        sheets: List[str],
    ) -> List[dict]:

        comments = []

        for sheet in sheets:

            df = workbook[sheet]

            comments.extend(self._extract_sheet(df))

        return comments

    def _extract_sheet(
        self,
        df: pd.DataFrame,
    ) -> List[dict]:

        if df.empty:
            return []

        cols = {
            str(c).strip().lower(): c
            for c in df.columns
        }

        comment_col = None
        author_col = None
        date_col = None

        for h in self.COMMENT_HEADERS:
            if h in cols:
                comment_col = cols[h]

        for h in self.AUTHOR_HEADERS:
            if h in cols:
                author_col = cols[h]

        for h in self.DATE_HEADERS:
            if h in cols:
                date_col = cols[h]

        comments = []

        # ------------------------------------
        # Structured table
        # ------------------------------------

        if comment_col:

            for _, row in df.iterrows():

                text = row.get(comment_col)

                if pd.isna(text):
                    continue

                comments.append(
                    {
                        "text": str(text),
                        "author": row.get(author_col)
                        if author_col
                        else None,
                        "date": row.get(date_col)
                        if date_col
                        else None,
                    }
                )

            return comments

        # ------------------------------------
        # Free-form sheet
        # ------------------------------------

        for _, row in df.iterrows():

            values = []

            for value in row:

                if pd.isna(value):
                    continue

                value = str(value).strip()

                if len(value) < 5:
                    continue

                values.append(value)

            if values:

                comments.append(
                    {
                        "text": " | ".join(values),
                        "author": None,
                        "date": None,
                    }
                )

        return comments