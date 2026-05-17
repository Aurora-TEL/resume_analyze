from decimal import Decimal

from sqlalchemy import Enum, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class AnalysisReport(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "analysis_reports"
    __table_args__ = (UniqueConstraint("task_id", name="uq_analysis_reports_task_id"),)

    task_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("analysis_tasks.id"), nullable=False)
    user_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    resume_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("resumes.id"), nullable=False, index=True)
    job_description_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("job_descriptions.id"),
        nullable=True,
    )
    total_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    match_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    report_data: Mapped[dict] = mapped_column(JSONB, nullable=False)
    model_provider: Mapped[str] = mapped_column(String(50), nullable=False)
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    report_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    task = relationship("AnalysisTask", back_populates="report")
    user = relationship("User", back_populates="analysis_reports")
    resume = relationship("Resume", back_populates="analysis_reports")
    job_description = relationship("JobDescription", back_populates="analysis_reports")
