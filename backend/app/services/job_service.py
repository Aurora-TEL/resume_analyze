from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.models.enums import ParseStatus, PromptScene, ResourceStatus
from app.models.job_description import JobDescription
from app.models.user import User
from app.schemas.job_schema import (
    CreateJobRequest,
    JobCreateResponse,
    JobDetailResponse,
    JobListItem,
    JobListResponse,
    JobParseResponse,
    UpdateJobRequest,
)
from app.services.ai.deepseek_client import DeepSeekClient

deepseek_client = DeepSeekClient()


def _build_ai_job_structure(db: Session, current_user: User, payload: CreateJobRequest | UpdateJobRequest | JobDescription) -> dict:
    return deepseek_client.call_scene(
        db,
        PromptScene.JOB_PARSE.value,
        {
            "job_title": payload.title,
            "company_name": payload.company_name or "",
            "industry": payload.industry or "",
            "job_text": payload.description_text,
        },
        user_id=current_user.id,
    )


def get_job_or_404(db: Session, current_user: User, job_id: UUID) -> JobDescription:
    job = db.scalar(
        select(JobDescription).where(
            JobDescription.id == job_id,
            JobDescription.user_id == current_user.id,
            JobDescription.status == ResourceStatus.ACTIVE,
        )
    )
    if job is None:
        raise AppException(message="Job description not found", code=4042, status_code=404)
    return job


def create_job(db: Session, current_user: User, payload: CreateJobRequest) -> JobCreateResponse:
    parse_status = ParseStatus.PENDING
    parse_error: str | None = None
    structured_data: dict | None = None
    try:
        structured_data = _build_ai_job_structure(db, current_user, payload)
        parse_status = ParseStatus.SUCCESS
    except Exception as exc:  # noqa: BLE001
        parse_status = ParseStatus.FAILED
        parse_error = str(exc)

    job = JobDescription(
        user_id=current_user.id,
        title=payload.title,
        company_name=payload.company_name,
        industry=payload.industry,
        location=payload.location,
        salary_range=payload.salary_range,
        description_text=payload.description_text,
        structured_data=structured_data,
        parse_status=parse_status,
        parse_error=parse_error,
        status=ResourceStatus.ACTIVE,
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    return JobCreateResponse(
        job_id=job.id,
        title=job.title,
        parse_status=job.parse_status.value,
    )


def list_jobs(
    db: Session,
    current_user: User,
    page: int,
    page_size: int,
    keyword: str | None,
) -> JobListResponse:
    filters = [JobDescription.user_id == current_user.id, JobDescription.status == ResourceStatus.ACTIVE]
    if keyword:
        filters.append(
            or_(
                JobDescription.title.ilike(f"%{keyword}%"),
                JobDescription.company_name.ilike(f"%{keyword}%"),
            )
        )

    total = db.scalar(select(func.count()).select_from(JobDescription).where(*filters)) or 0
    items = db.scalars(
        select(JobDescription)
        .where(*filters)
        .order_by(JobDescription.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()

    response_items = [JobListItem.model_validate(item) for item in items]
    return JobListResponse.build(response_items, total, page, page_size)


def get_job_detail(db: Session, current_user: User, job_id: UUID) -> JobDetailResponse:
    job = get_job_or_404(db, current_user, job_id)
    return JobDetailResponse.model_validate(job)


def update_job(
    db: Session,
    current_user: User,
    job_id: UUID,
    payload: UpdateJobRequest,
) -> JobDetailResponse:
    job = get_job_or_404(db, current_user, job_id)

    job.title = payload.title
    job.company_name = payload.company_name
    job.industry = payload.industry
    job.location = payload.location
    job.salary_range = payload.salary_range
    job.description_text = payload.description_text

    try:
        job.structured_data = _build_ai_job_structure(db, current_user, payload)
        job.parse_status = ParseStatus.SUCCESS
        job.parse_error = None
    except Exception as exc:  # noqa: BLE001
        job.parse_status = ParseStatus.FAILED
        job.parse_error = str(exc)

    db.add(job)
    db.commit()
    db.refresh(job)
    return JobDetailResponse.model_validate(job)


def delete_job(db: Session, current_user: User, job_id: UUID) -> None:
    job = get_job_or_404(db, current_user, job_id)
    job.status = ResourceStatus.DELETED
    db.add(job)
    db.commit()


def parse_job(db: Session, current_user: User, job_id: UUID) -> JobParseResponse:
    job = get_job_or_404(db, current_user, job_id)

    try:
        job.structured_data = _build_ai_job_structure(db, current_user, job)
        job.parse_status = ParseStatus.SUCCESS
        job.parse_error = None
    except Exception as exc:  # noqa: BLE001
        job.parse_status = ParseStatus.FAILED
        job.parse_error = str(exc)

    db.add(job)
    db.commit()
    db.refresh(job)

    return JobParseResponse(
        job_id=job.id,
        parse_status=job.parse_status.value,
    )
