from datetime import datetime
from math import ceil
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CreateJobRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    company_name: str | None = Field(default=None, max_length=200)
    industry: str | None = Field(default=None, max_length=100)
    location: str | None = Field(default=None, max_length=100)
    salary_range: str | None = Field(default=None, max_length=100)
    description_text: str = Field(min_length=1)


class UpdateJobRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    company_name: str | None = Field(default=None, max_length=200)
    industry: str | None = Field(default=None, max_length=100)
    location: str | None = Field(default=None, max_length=100)
    salary_range: str | None = Field(default=None, max_length=100)
    description_text: str = Field(min_length=1)


class JobCreateResponse(BaseModel):
    job_id: UUID
    title: str
    parse_status: str


class JobListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    company_name: str | None = None
    industry: str | None = None
    location: str | None = None
    parse_status: str
    created_at: datetime


class JobListResponse(BaseModel):
    items: list[JobListItem]
    total: int
    page: int
    page_size: int
    pages: int

    @classmethod
    def build(cls, items: list[JobListItem], total: int, page: int, page_size: int) -> "JobListResponse":
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            pages=ceil(total / page_size) if page_size else 0,
        )


class JobDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    company_name: str | None = None
    industry: str | None = None
    location: str | None = None
    salary_range: str | None = None
    description_text: str
    structured_data: dict | None = None
    parse_status: str
    parse_error: str | None = None
    created_at: datetime
    updated_at: datetime


class JobParseResponse(BaseModel):
    job_id: UUID
    parse_status: str
