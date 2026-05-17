from pathlib import Path
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy import func, select, update
from sqlalchemy.orm import Session

from app.core.config import ROOT_DIR
from app.core.exceptions import AppException
from app.models.enums import ParseStatus, ResourceStatus
from app.models.resume import Resume
from app.models.user import User
from app.schemas.resume_schema import (
    ResumeDetailResponse,
    ResumeListItem,
    ResumeListResponse,
    ResumeParseResponse,
    ResumeUploadResponse,
    UpdateResumeRequest,
)
from app.models.enums import PromptScene
from app.services.ai.deepseek_client import DeepSeekClient
from app.services.file_service import (
    build_resume_storage_path,
    validate_resume_file,
    write_file,
)
from app.services.parser_service import extract_text

deepseek_client = DeepSeekClient()


def _resume_absolute_path(file_path: str) -> Path:
    return ROOT_DIR / file_path


def get_resume_or_404(db: Session, current_user: User, resume_id: UUID) -> Resume:
    resume = db.scalar(
        select(Resume).where(
            Resume.id == resume_id,
            Resume.user_id == current_user.id,
            Resume.status == ResourceStatus.ACTIVE,
        )
    )
    if resume is None:
        raise AppException(message="Resume not found", code=4041, status_code=404)
    return resume


def upload_resume(db: Session, current_user: User, file: UploadFile, title: str | None) -> ResumeUploadResponse:
    content = file.file.read()
    file_size = len(content)

    try:
        file_type = validate_resume_file(file.filename or "", file.content_type, file_size)
    except ValueError as exc:
        raise AppException(message=str(exc), code=4005, status_code=400) from exc

    absolute_path, relative_path = build_resume_storage_path(current_user.id, file_type)
    write_file(absolute_path, content)

    parse_status = ParseStatus.PENDING
    parse_error: str | None = None
    raw_text: str | None = None
    try:
        raw_text = extract_text(absolute_path, file_type)
        parse_status = ParseStatus.SUCCESS
    except Exception as exc:  # noqa: BLE001
        parse_status = ParseStatus.FAILED
        parse_error = str(exc)

    existing_resume_count = db.scalar(
        select(func.count()).select_from(Resume).where(
            Resume.user_id == current_user.id,
            Resume.status == ResourceStatus.ACTIVE,
        )
    ) or 0

    resume = Resume(
        user_id=current_user.id,
        title=title or Path(file.filename or "resume").stem,
        file_name=file.filename or f"resume.{file_type}",
        file_type=file_type,
        file_size=file_size,
        file_path=relative_path,
        raw_text=raw_text,
        parse_status=parse_status,
        parse_error=parse_error,
        version=1,
        is_default=existing_resume_count == 0,
        status=ResourceStatus.ACTIVE,
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)

    return ResumeUploadResponse(
        resume_id=resume.id,
        title=resume.title,
        file_name=resume.file_name,
        file_type=resume.file_type,
        file_size=resume.file_size,
        parse_status=resume.parse_status.value,
    )


def list_resumes(
    db: Session,
    current_user: User,
    page: int,
    page_size: int,
    keyword: str | None,
    status: str | None,
) -> ResumeListResponse:
    filters = [Resume.user_id == current_user.id, Resume.status == ResourceStatus.ACTIVE]
    if keyword:
        filters.append(Resume.title.ilike(f"%{keyword}%"))
    if status:
        filters.append(Resume.parse_status == status)

    total = db.scalar(select(func.count()).select_from(Resume).where(*filters)) or 0
    items = db.scalars(
        select(Resume)
        .where(*filters)
        .order_by(Resume.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()

    response_items = [ResumeListItem.model_validate(item) for item in items]
    return ResumeListResponse.build(response_items, total, page, page_size)


def get_resume_detail(db: Session, current_user: User, resume_id: UUID) -> ResumeDetailResponse:
    resume = get_resume_or_404(db, current_user, resume_id)
    return ResumeDetailResponse.model_validate(resume)


def update_resume(
    db: Session,
    current_user: User,
    resume_id: UUID,
    payload: UpdateResumeRequest,
) -> ResumeDetailResponse:
    resume = get_resume_or_404(db, current_user, resume_id)
    update_data = payload.model_dump(exclude_unset=True)

    if update_data.get("is_default") is True:
        db.execute(
            update(Resume)
            .where(
                Resume.user_id == current_user.id,
                Resume.id != resume.id,
                Resume.status == ResourceStatus.ACTIVE,
            )
            .values(is_default=False)
        )

    for field, value in update_data.items():
        setattr(resume, field, value)

    db.add(resume)
    db.commit()
    db.refresh(resume)
    return ResumeDetailResponse.model_validate(resume)


def delete_resume(db: Session, current_user: User, resume_id: UUID) -> None:
    resume = get_resume_or_404(db, current_user, resume_id)
    resume.status = ResourceStatus.DELETED
    db.add(resume)
    db.commit()


def parse_resume(db: Session, current_user: User, resume_id: UUID) -> ResumeParseResponse:
    resume = get_resume_or_404(db, current_user, resume_id)

    try:
        raw_text = extract_text(_resume_absolute_path(resume.file_path), resume.file_type)
        resume.raw_text = raw_text
        resume.structured_data = deepseek_client.call_scene(
            db,
            PromptScene.RESUME_PARSE.value,
            {
                "resume_text": raw_text,
                "target_position": current_user.target_position or "",
            },
            user_id=current_user.id,
        )
        resume.parse_status = ParseStatus.SUCCESS
        resume.parse_error = None
    except Exception as exc:  # noqa: BLE001
        resume.parse_status = ParseStatus.FAILED
        resume.parse_error = str(exc)

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return ResumeParseResponse(
        resume_id=resume.id,
        parse_status=resume.parse_status.value,
    )
