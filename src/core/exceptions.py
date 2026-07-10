class ProjectHealthError(Exception):
    """Base exception for the system."""

class IngestionError(ProjectHealthError):
    """Raised when Excel parsing or normalization fails."""

class ValidationError(ProjectHealthError):
    """Raised when data quality rules are violated."""

class MissingSheetError(IngestionError):
    """Required sheet missing from workbook."""

class InvalidHierarchyError(IngestionError):
    """Project hierarchy is malformed."""