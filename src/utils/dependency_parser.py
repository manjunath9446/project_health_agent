import re
from typing import List

def parse_dependencies(raw: str | None) -> List[str]:
    if not raw:
        return []
    parts = re.split(r'[;,|\n]+', str(raw))
    return [p.strip() for p in parts if p.strip()]