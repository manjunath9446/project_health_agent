from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

import pandas as pd


# ============================================================
# Sheet Profile
# ============================================================

@dataclass
class SheetProfile:
    sheet_name: str
    role: str
    confidence: float
    columns: List[str]


# ============================================================
# Workbook Profile
# ============================================================

@dataclass
class WorkbookProfile:
    workbook_name: Optional[str] = None

    plan_sheet: Optional[str] = None
    summary_sheet: Optional[str] = None
    comment_sheets: List[str] = field(default_factory=list)

    hierarchy_type: str = "unknown"

    field_mapping: Dict[str, str] = field(default_factory=dict)

    confidence: float = 0.0

    warnings: List[str] = field(default_factory=list)

    detected_template: str = "generic"

    sheet_profiles: List[SheetProfile] = field(default_factory=list)


# ============================================================
# Detector
# ============================================================

class WorkbookProfileDetector:

    PLAN_KEYWORDS = [
        "task",
        "task name",
        "status",
        "owner",
        "start",
        "finish",
        "end",
        "duration",
        "schedule",
        "progress",
        "percent",
        "complete",
    ]

    SUMMARY_KEYWORDS = [
        "project manager",
        "project start",
        "project end",
        "overall status",
        "category",
    ]

    COMMENT_KEYWORDS = [
        "comment",
        "meeting",
        "action",
        "note",
        "remarks",
        "discussion",
    ]

    HIERARCHY_FIELDS = {
        "parent_id": [
            "parent id",
            "parent",
        ],
        "wbs": [
            "wbs",
        ],
        "level": [
            "level",
            "outline level",
        ],
        "ancestors": [
            "ancestors",
        ],
    }

    # -------------------------------------------------------

    def detect(
        self,
        workbook: Dict[str, pd.DataFrame],
    ) -> WorkbookProfile:

        profile = WorkbookProfile()

        for sheet_name, df in workbook.items():

            cols = [
                str(c).strip().lower()
                for c in df.columns
            ]

            role = self._detect_sheet_role(
                sheet_name,
                cols,
            )

            confidence = self._sheet_confidence(
                role,
                cols,
            )

            profile.sheet_profiles.append(
                SheetProfile(
                    sheet_name=sheet_name,
                    role=role,
                    confidence=confidence,
                    columns=cols,
                )
            )

            # --------------------------

            if role == "plan":

                if (
                    profile.plan_sheet is None
                    or confidence > profile.confidence
                ):
                    profile.plan_sheet = sheet_name
                    profile.confidence = confidence

                    profile.field_mapping = self._build_mapping(cols)

                    profile.hierarchy_type = (
                        self._detect_hierarchy(cols)
                    )

            elif role == "summary":

                if profile.summary_sheet is None:
                    profile.summary_sheet = sheet_name

            elif role == "comments":

                profile.comment_sheets.append(sheet_name)

        # --------------------------
        # Validation
        # --------------------------

        if profile.plan_sheet is None:
            profile.warnings.append(
                "No project plan sheet detected."
            )

        if profile.summary_sheet is None:
            profile.warnings.append(
                "Summary sheet not detected."
            )

        if len(profile.comment_sheets) == 0:
            profile.warnings.append(
                "Comment sheet not detected."
            )

        profile.detected_template = self._detect_template(
            profile
        )

        return profile

    # =========================================================

    def _detect_sheet_role(
        self,
        sheet_name: str,
        columns: List[str],
    ) -> str:

        s = sheet_name.lower()

        if "summary" in s:
            return "summary"

        if "comment" in s:
            return "comments"

        if "meeting" in s:
            return "comments"

        plan_score = sum(
            any(k in c for c in columns)
            for k in self.PLAN_KEYWORDS
        )

        summary_score = sum(
            any(k in c for c in columns)
            for k in self.SUMMARY_KEYWORDS
        )

        comment_score = sum(
            any(k in c for c in columns)
            for k in self.COMMENT_KEYWORDS
        )

        if plan_score >= summary_score and plan_score >= comment_score:
            return "plan"

        if summary_score >= comment_score:
            return "summary"

        return "comments"

    # =========================================================

    def _sheet_confidence(
        self,
        role: str,
        cols: List[str],
    ) -> float:

        if role == "plan":

            matches = sum(
                any(
                    k in c
                    for c in cols
                )
                for k in self.PLAN_KEYWORDS
            )

            return min(matches / 8.0, 1.0)

        if role == "summary":
            return 0.90

        return 0.80

    # =========================================================

    def _detect_hierarchy(
        self,
        cols: List[str],
    ) -> str:

        for hierarchy, names in self.HIERARCHY_FIELDS.items():

            for n in names:

                if n in cols:
                    return hierarchy

        return "flat"

    # =========================================================

    def _build_mapping(
        self,
        cols: List[str],
    ) -> Dict[str, str]:

        mapping = {}

        aliases = {
            "task_name": [
                "task",
                "task name",
                "activity",
                "name",
            ],
            "owner": [
                "owner",
                "resource",
                "assignee",
            ],
            "status": [
                "status",
            ],
            "percent_complete": [
                "% complete",
                "percent complete",
                "%complete",
                "progress",
            ],
            "planned_start": [
                "start",
                "planned start",
                "start date",
            ],
            "planned_end": [
                "finish",
                "planned finish",
                "end",
                "finish date",
                "end date",
            ],
            "duration": [
                "duration",
            ],
            "schedule_health": [
                "schedule health",
                "health",
                "rag",
            ],
            "level": [
                "level",
                "outline level",
            ],
            "ancestors": [
                "ancestors",
            ],
            "wbs": [
                "wbs",
            ],
            "parent_id": [
                "parent",
                "parent id",
            ],
        }

        for std, candidates in aliases.items():

            for candidate in candidates:

                for col in cols:

                    if candidate == col:

                        mapping[std] = col
                        break

                if std in mapping:
                    break

        return mapping

    # =========================================================

    def _detect_template(
        self,
        profile: WorkbookProfile,
    ) -> str:

        if profile.hierarchy_type == "wbs":
            return "microsoft_project"

        if profile.hierarchy_type == "level":
            return "outline_level"

        if profile.hierarchy_type == "ancestors":
            return "ancestor_depth"

        if profile.hierarchy_type == "parent_id":
            return "parent_child"

        return "generic"