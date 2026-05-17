from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import SoftDeleteMixin, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import ParseStatus, ResourceStatus


class JobDescription(UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "job_descriptions"

    user_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    company_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    industry: Mapped[str | None] = mapped_column(String(100), nullable=True)
    location: Mapped[str | None] = mapped_column(String(100), nullable=True)
    salary_range: Mapped[str | None] = mapped_column(String(100), nullable=True)
    description_text: Mapped[str] = mapped_column(Text, nullable=False)
    structured_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    parse_status: Mapped[ParseStatus] = mapped_column(
        Enum(ParseStatus, native_enum=False),
        nullable=False,
        default=ParseStatus.PENDING,
    )
    parse_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[ResourceStatus] = mapped_column(
        Enum(ResourceStatus, native_enum=False),
        nullable=False,
        default=ResourceStatus.ACTIVE,
    )

    user = relationship("User", back_populates="job_descriptions")
    analysis_tasks = relationship("AnalysisTask", back_populates="job_description")
    analysis_reports = relationship("AnalysisReport", back_populates="job_description")
