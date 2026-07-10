from sqlalchemy import String, Integer, Float, DateTime, Boolean, ForeignKey, Enum, Text
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import enum
from src.core.database import Base

class ProjectStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"

class TaskStatus(str, enum.Enum):
    COMPLETED = "Completed"
    IN_PROGRESS = "In Progress"
    NOT_STARTED = "Not Started"

class ScheduleHealth(str, enum.Enum):
    GREEN = "Green"
    YELLOW = "Yellow"
    RED = "Red"

class Project(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    project_manager: Mapped[str] = mapped_column(String(255))
    category: Mapped[str] = mapped_column(String(100))
    status: Mapped[ProjectStatus] = mapped_column(default=ProjectStatus.ACTIVE)
    start_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    phases: Mapped[list["Phase"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    comments: Mapped[list["Comment"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    summary: Mapped["Summary"] = relationship(back_populates="project", uselist=False, cascade="all, delete-orphan")
    data_quality_reports: Mapped[list["DataQualityReport"]] = relationship(back_populates="project", cascade="all, delete-orphan")

class Phase(Base):
    __tablename__ = "phases"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    name: Mapped[str] = mapped_column(String(255))
    order_index: Mapped[int] = mapped_column(default=0)
    start_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    audit_raw_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    project: Mapped["Project"] = relationship(back_populates="phases")
    milestones: Mapped[list["Milestone"]] = relationship(back_populates="phase", cascade="all, delete-orphan")

class Milestone(Base):
    __tablename__ = "milestones"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    phase_id: Mapped[int] = mapped_column(ForeignKey("phases.id"))
    name: Mapped[str] = mapped_column(String(255))
    order_index: Mapped[int] = mapped_column(default=0)
    planned_start: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    planned_end: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.NOT_STARTED)
    schedule_health: Mapped[ScheduleHealth | None] = mapped_column(nullable=True)
    audit_raw_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    phase: Mapped["Phase"] = relationship(back_populates="milestones")
    tasks: Mapped[list["Task"]] = relationship(back_populates="milestone", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    milestone_id: Mapped[int] = mapped_column(ForeignKey("milestones.id"))
    name: Mapped[str] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
    owner: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.NOT_STARTED)
    percent_complete: Mapped[float] = mapped_column(Float, default=0.0)
    planned_start: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    planned_end: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    duration: Mapped[int | None] = mapped_column(Integer)
    schedule_health: Mapped[ScheduleHealth | None] = mapped_column(nullable=True)
    at_risk: Mapped[bool] = mapped_column(default=False)
    on_hold: Mapped[bool] = mapped_column(default=False)
    not_applicable: Mapped[bool] = mapped_column(default=False)
    predecessors: Mapped[str | None] = mapped_column(Text)
    audit_raw_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    milestone: Mapped["Milestone"] = relationship(back_populates="tasks")