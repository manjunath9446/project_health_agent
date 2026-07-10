import pandas as pd
from loguru import logger
from src.core.exceptions import MissingSheetError, IngestionError

def read_excel_workbook(file_path: str) -> dict[str, pd.DataFrame]:
    try:
        xls = pd.ExcelFile(file_path)
    except Exception as e:
        raise IngestionError(f"Cannot open Excel file: {str(e)}")
    required = ["Project Plan", "Comments", "Summary"]
    for sheet in required:
        if sheet not in xls.sheet_names:
            raise MissingSheetError(f"Required sheet '{sheet}' missing.")
    df_plan = pd.read_excel(xls, "Project Plan")
    df_comments = pd.read_excel(xls, "Comments")
    df_summary = pd.read_excel(xls, "Summary")
    logger.info(f"Read {len(df_plan)} plan rows, {len(df_comments)} comments.")
    return {"project_plan": df_plan, "comments": df_comments, "summary": df_summary}