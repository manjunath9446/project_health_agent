from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List, Any

import pandas as pd

from src.services.workbook_profile_detector import WorkbookProfile


# ============================================================
# Parser Interface
# ============================================================

class BaseWorkbookParser(ABC):
    """
    Every parser converts a workbook into a normalized
    flat list of rows.

    It DOES NOT build hierarchy.
    It DOES NOT normalize values.

    Output:
        [
            {
                "_depth": ...,
                "task_name": ...,
                "status": ...,
                ...
            }
        ]
    """

    @abstractmethod
    def parse(
        self,
        workbook: Dict[str, pd.DataFrame],
        profile: WorkbookProfile,
    ) -> List[Dict[str, Any]]:
        raise NotImplementedError


# ============================================================
# Parser Registry
# ============================================================

class ParserRegistry:

    def __init__(self):

        self._parsers: Dict[str, BaseWorkbookParser] = {}

    # --------------------------------------------------------

    def register(
        self,
        template_name: str,
        parser: BaseWorkbookParser,
    ) -> None:

        self._parsers[template_name] = parser

    # --------------------------------------------------------

    def get_parser(
        self,
        profile: WorkbookProfile,
    ) -> BaseWorkbookParser:

        template = profile.detected_template

        if template in self._parsers:
            return self._parsers[template]

        if "generic" in self._parsers:
            return self._parsers["generic"]

        raise RuntimeError(
            f"No parser registered for template '{template}'"
        )

    # --------------------------------------------------------

    def available_parsers(self) -> list[str]:
        return list(self._parsers.keys())