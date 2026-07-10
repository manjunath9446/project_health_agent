from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


class DataQualityReport(Base):
    __tablename__ = "data_quality_reports"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )

    completeness_score: Mapped[float] = mapped_column(
        Float,
        default=1.0,
    )

    data_confidence_score: Mapped[float] = mapped_column(
        Float,
        default=1.0,
    )

    total_issues: Mapped[int] = mapped_column(
        default=0,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    project: Mapped["Project"] = relationship(
        "Project",
        back_populates="data_quality_reports",
        lazy="selectin",
    )

    issues: Mapped[list["DataQualityIssue"]] = relationship(
        "DataQualityIssue",
        back_populates="report",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class DataQualityIssue(Base):
    __tablename__ = "data_quality_issues"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    report_id: Mapped[int] = mapped_column(
        ForeignKey("data_quality_reports.id", ondelete="CASCADE"),
        nullable=False,
    )

    issue_type: Mapped[str] = mapped_column(
        String(50),
    )

    severity: Mapped[str] = mapped_column(
        String(20),
    )

    description: Mapped[str] = mapped_column(
        Text,
    )

    entity_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    entity_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    report: Mapped["DataQualityReport"] = relationship(
        "DataQualityReport",
        back_populates="issues",
        lazy="selectin",
    )