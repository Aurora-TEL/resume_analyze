from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import TaskStatus, TaskType


class AnalysisTask(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "analysis_tasks"
    __table_args__ = (
        CheckConstraint("progress >= 0 AND progress <= 100", name="ck_analysis_tasks_progress_range"),
    )

    user_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    resume_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("resumes.id"), nullable=False, index=True)
    job_description_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("job_descriptions.id"),
        nullable=True,
    )
    task_type: Mapped[TaskType] = mapped_column(
        Enum(TaskType, native_enum=False),
        nullable=False,
    )
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, native_enum=False),
        nullable=False,
        default=TaskStatus.PENDING,
    )
    progress: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="analysis_tasks")
    resume = relationship("Resume", back_populates="analysis_tasks")
    job_description = relationship("JobDescription", back_populates="analysis_tasks")
    report = relationship("AnalysisReport", back_populates="task", uselist=False)
    api_call_logs = relationship("ApiCallLog", back_populates="task")
