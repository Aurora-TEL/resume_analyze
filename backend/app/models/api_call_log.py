from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import UUIDPrimaryKeyMixin
from app.models.enums import ApiCallStatus


class ApiCallLog(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "api_call_logs"

    user_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    task_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("analysis_tasks.id"),
        nullable=True,
        index=True,
    )
    prompt_template_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("prompt_templates.id"),
        nullable=True,
    )
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    scene: Mapped[str] = mapped_column(String(100), nullable=False)
    request_length: Mapped[int | None] = mapped_column(Integer, nullable=True)
    response_length: Mapped[int | None] = mapped_column(Integer, nullable=True)
    prompt_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    completion_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[ApiCallStatus] = mapped_column(
        Enum(ApiCallStatus, native_enum=False),
        nullable=False,
    )
    error_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    request_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    user = relationship("User", back_populates="api_call_logs")
    task = relationship("AnalysisTask", back_populates="api_call_logs")
    prompt_template = relationship("PromptTemplate", back_populates="api_call_logs")
