from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class ProjectAnalysis(Base):

    __tablename__ = "project_analysis"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False,
    )

    rag_status: Mapped[str] = mapped_column(
        String(20),
    )

    health_score: Mapped[float] = mapped_column(
        Float,
    )

    forecast_delay: Mapped[int] = mapped_column(
        Integer,
    )

    delay_probability: Mapped[float] = mapped_column(
        Float,
    )

    executive_summary: Mapped[str] = mapped_column(
        Text,
    )

    recommendations: Mapped[str] = mapped_column(
        Text,
    )

    risks: Mapped[str] = mapped_column(
        Text,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )