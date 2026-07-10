import yaml
import pandas as pd
from typing import Dict, List, Any
from src.core.config import settings

class ColumnMapping:
    def __init__(self, template_name: str = "default"):
        with open(settings.excel_column_mapping_path, "r") as f:
            config = yaml.safe_load(f)
        self.mapping = config[template_name]

    def get_excel_col(self, domain_field: str, sheet: str = "project_plan") -> str | None:
        return self.mapping.get(sheet, {}).get(domain_field)

class WorkbookParser:
    def __init__(self, mapping: ColumnMapping):
        self.mapping = mapping

    def parse_project_plan(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        rows = []
        prefix = self.mapping.get_excel_col("ancestor_level_prefix", "project_plan")
        ancestor_cols = sorted([c for c in df.columns if c.startswith(prefix)])
        for _, row in df.iterrows():
            record = {}
            for col in ancestor_cols:
                record[col] = row.get(col)
            for domain, excel_col in self.mapping.mapping["project_plan"].items():
                if domain == "ancestor_level_prefix":
                    continue
                if excel_col in df.columns:
                    record[domain] = row.get(excel_col)
            record["_source_row"] = _
            rows.append(record)
        return rows

    def parse_comments(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        comments = []
        comment_col = self.mapping.get_excel_col("comment", "comments")
        author_col = self.mapping.get_excel_col("author", "comments")
        for _, row in df.iterrows():
            text = row.get(comment_col) if comment_col else None
            if pd.isna(text) or str(text).strip() == "":
                continue
            comments.append({
                "text": str(text).strip(),
                "author": str(row.get(author_col)) if author_col and not pd.isna(row.get(author_col)) else None,
                "_source_row": _
            })
        return comments

    def parse_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        if df.empty:
            return {}
        row = df.iloc[0]
        summary = {}
        for domain, excel_col in self.mapping.mapping["summary"].items():
            if excel_col in df.columns:
                summary[domain] = row.get(excel_col)
        return summary