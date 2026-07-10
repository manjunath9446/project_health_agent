from src.services.normalization import Normalizer
import pandas as pd

def test_status_normalization():
    row = {"status": "In Progress", "percent_complete": 30, "planned_start": "2025-01-01", "planned_end": "2025-01-10"}
    norm = Normalizer.normalize_task_row(row)
    assert norm["normalized_status"] == "In Progress"
    assert norm["normalized_percent_complete"] == 30.0
    assert norm["normalized_planned_start"].year == 2025