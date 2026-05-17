from datetime import datetime
from math import ceil
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ResumeUploadResponse(BaseModel):
    resume_id: UUID
    title: str
    file_name: str
    file_type: str
    file_size: int
    parse_status: str


class ResumeListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    file_name: str
    file_type: str
    file_size: int
    parse_status: str
    version: int
    is_default: bool
    created_at: datetime


class ResumeListResponse(BaseModel):
    items: list[ResumeListItem]
    total: int
    page: int
    page_size: int
    pages: int

    @classmethod
    def build(cls, items: list[ResumeListItem], total: int, page: int, page_size: int) -> "ResumeListResponse":
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            pages=ceil(total / page_size) if page_size else 0,
        )


class ResumeDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    file_name: str
    file_type: str
    file_size: int
    raw_text: str | None = None
    structured_data: dict | None = None
    parse_status: str
    parse_error: str | None = None
    version: int
    is_default: bool
    created_at: datetime
    updated_at: datetime


class UpdateResumeRequest(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    is_default: bool | None = None


class ResumeParseResponse(BaseModel):
    resume_id: UUID
    parse_status: str
