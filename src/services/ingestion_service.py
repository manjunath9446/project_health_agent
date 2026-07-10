from __future__ import annotations

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.project_context import ProjectContext

# Readers / Detection
from src.services.workbook_reader import WorkbookReader
from src.services.workbook_profile_detector import WorkbookProfileDetector

# Parser Infrastructure
from src.services.parser_registry import ParserRegistry
from src.services.generic_workbook_parser import GenericWorkbookParser

# Cleaning
from src.services.data_cleaning_service import DataCleaningService

# Hierarchy
from src.services.hierarchy_strategy import HierarchyStrategy
from src.services.hierarchy_builder import HierarchyBuilder

# Extractors
from src.services.summary_extractor import SummaryExtractor
from src.services.comment_extractor import CommentExtractor

# Existing Services
from src.services.normalization import Normalizer
from src.services.project_context_builder import ProjectContextBuilder
from src.services.project_persistence_service import (
    ProjectPersistenceService,
)


class IngestionService:
    """
    Enterprise Adaptive Ingestion Pipeline

    Excel Workbook
          │
          ▼
    Workbook Reader
          │
          ▼
    Workbook Profile Detector
          │
          ▼
    Parser Registry
          │
          ▼
    Generic Workbook Parser
          │
          ▼
    Data Cleaning Service
          │
          ▼
    Normalizer
          │
          ▼
    Hierarchy Strategy
          │
          ▼
    Hierarchy Builder
          │
          ▼
    Summary Extractor
          │
          ▼
    Comment Extractor
          │
          ▼
    Project Context Builder
          │
          ▼
    Persistence
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:

        self.session = session

        self.reader = WorkbookReader()

        self.detector = WorkbookProfileDetector()

        self.registry = ParserRegistry()

        # ------------------------------
        # Register supported parsers
        # ------------------------------

        self.registry.register(
            "generic",
            GenericWorkbookParser(),
        )

        self.registry.register(
            "ancestor_depth",
            GenericWorkbookParser(),
        )

        self.registry.register(
            "outline_level",
            GenericWorkbookParser(),
        )

        self.registry.register(
            "parent_child",
            GenericWorkbookParser(),
        )

        self.registry.register(
            "microsoft_project",
            GenericWorkbookParser(),
        )

        self.strategy = HierarchyStrategy()

        self.builder = HierarchyBuilder()

        self.summary_extractor = SummaryExtractor()

        self.comment_extractor = CommentExtractor()

        self.normalizer = Normalizer()

        self.persistence = ProjectPersistenceService(session)

    async def ingest(
        self,
        file_path: str,
        project_name: str,
    ) -> tuple[int, ProjectContext]:

        logger.info(
            "Starting ingestion for '{}'",
            project_name,
        )

        # =====================================================
        # STEP 1 : Read Workbook
        # =====================================================

        workbook = self.reader.read(file_path)

        logger.info(
            "Workbook contains {} sheets.",
            len(workbook),
        )

        # =====================================================
        # STEP 2 : Detect Workbook Profile
        # =====================================================

        profile = self.detector.detect(workbook)

        logger.info(
            "Detected template: {}",
            profile.detected_template,
        )

        logger.info(
            "Hierarchy type: {}",
            profile.hierarchy_type,
        )

        logger.info(
            "Plan sheet: {}",
            profile.plan_sheet,
        )

        logger.info(
            "Summary sheet: {}",
            profile.summary_sheet,
        )

        logger.info(
            "Comment sheets: {}",
            profile.comment_sheets,
        )

        for warning in profile.warnings:
            logger.warning(warning)

        # =====================================================
        # STEP 3 : Select Parser
        # =====================================================

        parser = self.registry.get_parser(profile)

        logger.info(
            "Using parser: {}",
            parser.__class__.__name__,
        )

        # =====================================================
        # STEP 4 : Parse Workbook
        # =====================================================

        rows = parser.parse(
            workbook,
            profile,
        )

        logger.info(
            "Parsed {} rows.",
            len(rows),
        )

        # =====================================================
        # STEP 5 : Clean Raw Data
        # =====================================================

        logger.info(
            "Cleaning parsed rows..."
        )

        rows = DataCleaningService.clean_rows(rows)

        logger.info(
            "Cleaning completed."
        )

        # =====================================================
        # STEP 6 : Normalize Data
        # =====================================================

        logger.info(
            "Normalizing rows..."
        )

        normalized_rows = []

        for row in rows:

            normalized = row.copy()

            normalized.update(
                self.normalizer.normalize_task_row(
                    row
                )
            )

            normalized_rows.append(normalized)

        logger.info(
            "Normalization completed."
        )

        # =====================================================
        # STEP 7 : Determine Hierarchy Depth
        # =====================================================

        normalized_rows = self.strategy.apply(
            normalized_rows,
            profile.hierarchy_type,
        )

        # =====================================================
        # STEP 8 : Build Hierarchy
        # =====================================================

        hierarchy = self.builder.build(
            normalized_rows
        )

        logger.info(
            "Hierarchy contains {} root nodes.",
            len(hierarchy),
        )

        # =====================================================
        # STEP 9 : Extract Summary
        # =====================================================

        summary = {}

        if profile.summary_sheet:

            summary = self.summary_extractor.extract(
                workbook[
                    profile.summary_sheet
                ]
            )

        # =====================================================
        # STEP 10 : Extract Comments
        # =====================================================

        comments = self.comment_extractor.extract(
            workbook,
            profile.comment_sheets,
        )

        # =====================================================
        # STEP 11 : Project Metadata
        # =====================================================

        project_manager = summary.get(
            "project_manager",
            "Unknown",
        )

        category = summary.get(
            "project_category",
            "",
        )

        # =====================================================
        # STEP 12 : Build Project Context
        # =====================================================

        context_builder = ProjectContextBuilder(
            project_name=project_name,
            project_manager=project_manager,
            category=category,
            hierarchy_roots=hierarchy,
            comments_raw=comments,
            summary_raw=summary,
        )

        project_context = context_builder.build()

        logger.info(
            "ProjectContext created with {} phases.",
            len(project_context.phases),
        )

        print("\n" + "=" * 80)
        print("PROJECT CONTEXT")
        print("=" * 80)

        print("Project :", project_context.project_name)
        print("Total Phases :", len(project_context.phases))

        for phase in project_context.phases[:5]:

            print("\nPHASE :", phase.name)
            print("Milestones :", len(phase.milestones))

            for milestone in phase.milestones[:3]:

                print(
                "   Milestone:",
                milestone.name,
                "| Tasks:",
                len(milestone.tasks),
                )
        # =====================================================
        # STEP 13 : Persist
        # =====================================================

        project_id = await self.persistence.persist(
            project_context
        )

        logger.success(
            "Project '{}' persisted successfully (ID={})",
            project_name,
            project_id,
        )

        return (
            project_id,
            project_context,
        )