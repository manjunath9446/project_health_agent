from datetime import datetime, timedelta
import pandas as pd

def parse_date(val) -> datetime | None:
    if pd.isna(val) or val is None:
        return None
    try:
        if isinstance(val, pd.Timestamp):
            return val.to_pydatetime()
        if isinstance(val, str):
            for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d %H:%M:%S", "%d-%b-%Y", "%b %d, %Y"):
                try:
                    return datetime.strptime(val.strip(), fmt)
                except ValueError:
                    continue
        if isinstance(val, (int, float)):
            base = datetime(1899, 12, 30)
            return base + timedelta(days=float(val))
        return datetime.fromisoformat(str(val))
    except:
        return None