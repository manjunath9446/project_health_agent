from sqlalchemy import Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from src.core.database import Base

class Summary(Base):
    __tablename__ = "summaries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), unique=True)
    project_start: Mapped[datetime | None] = mapped_column(DateTime)
    project_end: Mapped[datetime | None] = mapped_column(DateTime)
    total_tasks: Mapped[int] = mapped_column(default=0)
    completed_tasks: Mapped[int] = mapped_column(default=0)
    in_progress_tasks: Mapped[int] = mapped_column(default=0)
    not_started_tasks: Mapped[int] = mapped_column(default=0)

    project: Mapped["Project"] = relationship(back_populates="summary")