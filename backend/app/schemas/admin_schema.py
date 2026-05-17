from datetime import datetime
from math import ceil
from uuid import UUID

from pydantic import BaseModel


class AdminOverviewResponse(BaseModel):
    total_users: int
    total_resumes: int
    total_jobs: int
    total_analysis_tasks: int
    total_reports: int
    total_prompt_templates: int
    total_api_calls: int
    failed_api_calls: int
    pending_tasks: int
    running_tasks: int
    failed_tasks: int
    latest_api_error_message: str | None = None


class AdminAnalysisTaskItem(BaseModel):
    id: UUID
    task_type: str
    status: str
    progress: int
    error_message: str | None = None
    user_email: str
    resume_title: str
    job_title: str | None = None
    created_at: datetime
    started_at: datetime | None = None
    finished_at: datetime | None = None


class AdminAnalysisTaskListResponse(BaseModel):
    items: list[AdminAnalysisTaskItem]
    total: int
    page: int
    page_size: int
    pages: int

    @classmethod
    def build(
        cls,
        items: list[AdminAnalysisTaskItem],
        total: int,
        page: int,
        page_size: int,
    ) -> "AdminAnalysisTaskListResponse":
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            pages=ceil(total / page_size) if page_size else 0,
        )


class AdminApiLogItem(BaseModel):
    id: UUID
    provider: str
    model_name: str
    scene: str
    status: str
    user_email: str | None = None
    task_id: UUID | None = None
    prompt_template_name: str | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    latency_ms: int | None = None
    error_type: str | None = None
    error_message: str | None = None
    created_at: datetime


class AdminApiLogListResponse(BaseModel):
    items: list[AdminApiLogItem]
    total: int
    page: int
    page_size: int
    pages: int

    @classmethod
    def build(
        cls,
        items: list[AdminApiLogItem],
        total: int,
        page: int,
        page_size: int,
    ) -> "AdminApiLogListResponse":
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            pages=ceil(total / page_size) if page_size else 0,
        )


class PromptTemplateItem(BaseModel):
    id: UUID
    name: str
    scene: str
    version: int
    status: str
    description: str | None = None
    content: str
    created_by_email: str | None = None
    updated_at: datetime
    created_at: datetime


class PromptTemplateListResponse(BaseModel):
    items: list[PromptTemplateItem]
    total: int
    page: int
    page_size: int
    pages: int

    @classmethod
    def build(
        cls,
        items: list[PromptTemplateItem],
        total: int,
        page: int,
        page_size: int,
    ) -> "PromptTemplateListResponse":
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            pages=ceil(total / page_size) if page_size else 0,
        )


class CreatePromptTemplateRequest(BaseModel):
    name: str
    scene: str
    content: str
    version: int = 1
    status: str = "active"
    description: str | None = None


class UpdatePromptTemplateRequest(BaseModel):
    name: str
    scene: str
    content: str
    version: int
    status: str
    description: str | None = None
