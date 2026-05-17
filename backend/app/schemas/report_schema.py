from datetime import datetime
from decimal import Decimal
from math import ceil
from uuid import UUID

from pydantic import BaseModel


class ReportListItem(BaseModel):
    id: UUID
    task_id: UUID
    resume_title: str
    job_title: str | None = None
    total_score: Decimal | None = None
    match_score: Decimal | None = None
    summary: str | None = None
    created_at: datetime


class ReportListResponse(BaseModel):
    items: list[ReportListItem]
    total: int
    page: int
    page_size: int
    pages: int

    @classmethod
    def build(cls, items: list[ReportListItem], total: int, page: int, page_size: int) -> "ReportListResponse":
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            pages=ceil(total / page_size) if page_size else 0,
        )


class ReportDetailResponse(BaseModel):
    id: UUID
    task_id: UUID
    resume_id: UUID
    job_description_id: UUID | None = None
    total_score: Decimal | None = None
    match_score: Decimal | None = None
    summary: str | None = None
    report_data: dict
    model_provider: str
    model_name: str
    created_at: datetime
