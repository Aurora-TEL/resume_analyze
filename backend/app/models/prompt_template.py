from sqlalchemy import Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import SoftDeleteMixin, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import PromptScene, PromptTemplateStatus


class PromptTemplate(UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "prompt_templates"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    scene: Mapped[PromptScene] = mapped_column(
        Enum(PromptScene, native_enum=False),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[PromptTemplateStatus] = mapped_column(
        Enum(PromptTemplateStatus, native_enum=False),
        nullable=False,
        default=PromptTemplateStatus.ACTIVE,
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    creator = relationship("User", back_populates="prompt_templates")
    api_call_logs = relationship("ApiCallLog", back_populates="prompt_template")
