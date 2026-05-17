from datetime import datetime
from math import ceil
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CreateAnalysisTaskRequest(BaseModel):
    resume_id: UUID
    job_description_id: UUID | None = None
    task_type: str


class CreateAnalysisTaskResponse(BaseModel):
    task_id: UUID
    status: str
    report_id: UUID | None = None


class AnalysisTaskStatusResponse(BaseModel):
    task_id: UUID
    task_type: str
    status: str
    progress: int
    error_message: str | None = None
    report_id: UUID | None = None
    created_at: datetime
    started_at: datetime | None = None
    finished_at: datetime | None = None


class AnalysisTaskListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    task_type: str
    status: str
    progress: int
    error_message: str | None = None
    created_at: datetime
    started_at: datetime | None = None
    finished_at: datetime | None = None


class AnalysisTaskListResponse(BaseModel):
    items: list[AnalysisTaskListItem]
    total: int
    page: int
    page_size: int
    pages: int

    @classmethod
    def build(
        cls,
        items: list[AnalysisTaskListItem],
        total: int,
        page: int,
        page_size: int,
    ) -> "AnalysisTaskListResponse":
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            pages=ceil(total / page_size) if page_size else 0,
        )
