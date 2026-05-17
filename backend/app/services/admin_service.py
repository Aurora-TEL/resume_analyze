from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, joinedload

from app.core.exceptions import AppException
from app.models.analysis_report import AnalysisReport
from app.models.analysis_task import AnalysisTask
from app.models.api_call_log import ApiCallLog
from app.models.enums import ApiCallStatus, PromptScene, PromptTemplateStatus, ResourceStatus, TaskStatus
from app.models.job_description import JobDescription
from app.models.prompt_template import PromptTemplate
from app.models.resume import Resume
from app.models.user import User
from app.schemas.admin_schema import (
    AdminAnalysisTaskItem,
    AdminAnalysisTaskListResponse,
    AdminApiLogItem,
    AdminApiLogListResponse,
    AdminOverviewResponse,
    CreatePromptTemplateRequest,
    PromptTemplateItem,
    PromptTemplateListResponse,
    UpdatePromptTemplateRequest,
)


def get_admin_overview(db: Session) -> AdminOverviewResponse:
    latest_api_error = db.scalar(
        select(ApiCallLog.error_message)
        .where(
            ApiCallLog.status == ApiCallStatus.FAILED,
            ApiCallLog.error_message.is_not(None),
        )
        .order_by(ApiCallLog.created_at.desc())
        .limit(1)
    )

    return AdminOverviewResponse(
        total_users=db.scalar(select(func.count()).select_from(User)) or 0,
        total_resumes=db.scalar(
            select(func.count()).select_from(Resume).where(Resume.status == ResourceStatus.ACTIVE)
        )
        or 0,
        total_jobs=db.scalar(
            select(func.count()).select_from(JobDescription).where(JobDescription.status == ResourceStatus.ACTIVE)
        )
        or 0,
        total_analysis_tasks=db.scalar(select(func.count()).select_from(AnalysisTask)) or 0,
        total_reports=db.scalar(select(func.count()).select_from(AnalysisReport)) or 0,
        total_prompt_templates=db.scalar(select(func.count()).select_from(PromptTemplate)) or 0,
        total_api_calls=db.scalar(select(func.count()).select_from(ApiCallLog)) or 0,
        failed_api_calls=db.scalar(
            select(func.count()).select_from(ApiCallLog).where(ApiCallLog.status == ApiCallStatus.FAILED)
        )
        or 0,
        pending_tasks=db.scalar(
            select(func.count()).select_from(AnalysisTask).where(AnalysisTask.status == TaskStatus.PENDING)
        )
        or 0,
        running_tasks=db.scalar(
            select(func.count()).select_from(AnalysisTask).where(AnalysisTask.status == TaskStatus.RUNNING)
        )
        or 0,
        failed_tasks=db.scalar(
            select(func.count()).select_from(AnalysisTask).where(AnalysisTask.status == TaskStatus.FAILED)
        )
        or 0,
        latest_api_error_message=latest_api_error,
    )


def list_admin_analysis_tasks(
    db: Session,
    *,
    page: int,
    page_size: int,
    status: str | None,
    task_type: str | None,
    keyword: str | None,
) -> AdminAnalysisTaskListResponse:
    filters = []
    if status:
        filters.append(AnalysisTask.status == status)
    if task_type:
        filters.append(AnalysisTask.task_type == task_type)
    if keyword:
        keyword_like = f"%{keyword}%"
        filters.append(
            or_(
                User.email.ilike(keyword_like),
                Resume.title.ilike(keyword_like),
                JobDescription.title.ilike(keyword_like),
            )
        )

    total_query = (
        select(func.count())
        .select_from(AnalysisTask)
        .join(User, AnalysisTask.user_id == User.id)
        .join(Resume, AnalysisTask.resume_id == Resume.id)
        .join(JobDescription, AnalysisTask.job_description_id == JobDescription.id, isouter=True)
        .where(*filters)
    )
    total = db.scalar(total_query) or 0

    items = db.scalars(
        select(AnalysisTask)
        .options(
            joinedload(AnalysisTask.user),
            joinedload(AnalysisTask.resume),
            joinedload(AnalysisTask.job_description),
        )
        .join(User, AnalysisTask.user_id == User.id)
        .join(Resume, AnalysisTask.resume_id == Resume.id)
        .join(JobDescription, AnalysisTask.job_description_id == JobDescription.id, isouter=True)
        .where(*filters)
        .order_by(AnalysisTask.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()

    response_items = [
        AdminAnalysisTaskItem(
            id=item.id,
            task_type=item.task_type.value,
            status=item.status.value,
            progress=item.progress,
            error_message=item.error_message,
            user_email=item.user.email,
            resume_title=item.resume.title,
            job_title=item.job_description.title if item.job_description else None,
            created_at=item.created_at,
            started_at=item.started_at,
            finished_at=item.finished_at,
        )
        for item in items
    ]
    return AdminAnalysisTaskListResponse.build(response_items, total, page, page_size)


def list_admin_api_logs(
    db: Session,
    *,
    page: int,
    page_size: int,
    status: str | None,
    scene: str | None,
    keyword: str | None,
) -> AdminApiLogListResponse:
    filters = []
    if status:
        filters.append(ApiCallLog.status == status)
    if scene:
        filters.append(ApiCallLog.scene == scene)
    if keyword:
        keyword_like = f"%{keyword}%"
        filters.append(
            or_(
                User.email.ilike(keyword_like),
                ApiCallLog.error_message.ilike(keyword_like),
                ApiCallLog.model_name.ilike(keyword_like),
                PromptTemplate.name.ilike(keyword_like),
            )
        )

    total = db.scalar(
        select(func.count())
        .select_from(ApiCallLog)
        .join(User, ApiCallLog.user_id == User.id, isouter=True)
        .join(PromptTemplate, ApiCallLog.prompt_template_id == PromptTemplate.id, isouter=True)
        .where(*filters)
    ) or 0

    logs = db.scalars(
        select(ApiCallLog)
        .options(
            joinedload(ApiCallLog.user),
            joinedload(ApiCallLog.prompt_template),
        )
        .join(User, ApiCallLog.user_id == User.id, isouter=True)
        .join(PromptTemplate, ApiCallLog.prompt_template_id == PromptTemplate.id, isouter=True)
        .where(*filters)
        .order_by(ApiCallLog.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()

    items = [
        AdminApiLogItem(
            id=log.id,
            provider=log.provider,
            model_name=log.model_name,
            scene=log.scene,
            status=log.status.value,
            user_email=log.user.email if log.user else None,
            task_id=log.task_id,
            prompt_template_name=log.prompt_template.name if log.prompt_template else None,
            prompt_tokens=log.prompt_tokens,
            completion_tokens=log.completion_tokens,
            total_tokens=log.total_tokens,
            latency_ms=log.latency_ms,
            error_type=log.error_type,
            error_message=log.error_message,
            created_at=log.created_at,
        )
        for log in logs
    ]
    return AdminApiLogListResponse.build(items, total, page, page_size)


def list_prompt_templates(
    db: Session,
    *,
    page: int,
    page_size: int,
    scene: str | None,
    status: str | None,
    keyword: str | None,
) -> PromptTemplateListResponse:
    filters = []
    if scene:
        filters.append(PromptTemplate.scene == scene)
    if status:
        filters.append(PromptTemplate.status == status)
    if keyword:
        keyword_like = f"%{keyword}%"
        filters.append(
            or_(
                PromptTemplate.name.ilike(keyword_like),
                PromptTemplate.description.ilike(keyword_like),
                PromptTemplate.content.ilike(keyword_like),
            )
        )

    total = db.scalar(select(func.count()).select_from(PromptTemplate).where(*filters)) or 0
    templates = db.scalars(
        select(PromptTemplate)
        .options(joinedload(PromptTemplate.creator))
        .where(*filters)
        .order_by(PromptTemplate.updated_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()

    items = [
        PromptTemplateItem(
            id=item.id,
            name=item.name,
            scene=item.scene.value,
            version=item.version,
            status=item.status.value,
            description=item.description,
            content=item.content,
            created_by_email=item.creator.email if item.creator else None,
            created_at=item.created_at,
            updated_at=item.updated_at,
        )
        for item in templates
    ]
    return PromptTemplateListResponse.build(items, total, page, page_size)


def create_prompt_template(db: Session, current_user: User, payload: CreatePromptTemplateRequest) -> PromptTemplateItem:
    try:
        scene = PromptScene(payload.scene)
        status = PromptTemplateStatus(payload.status)
    except ValueError as exc:
        raise AppException(message="Invalid prompt template scene or status", code=4009, status_code=400) from exc

    template = PromptTemplate(
        name=payload.name,
        scene=scene,
        content=payload.content,
        version=payload.version,
        status=status,
        description=payload.description,
        created_by=current_user.id,
    )
    db.add(template)
    db.commit()
    db.refresh(template)

    return PromptTemplateItem(
        id=template.id,
        name=template.name,
        scene=template.scene.value,
        version=template.version,
        status=template.status.value,
        description=template.description,
        content=template.content,
        created_by_email=current_user.email,
        created_at=template.created_at,
        updated_at=template.updated_at,
    )


def update_prompt_template(
    db: Session,
    current_user: User,
    template_id: str,
    payload: UpdatePromptTemplateRequest,
) -> PromptTemplateItem:
    try:
        template_uuid = UUID(template_id)
    except ValueError as exc:
        raise AppException(message="Invalid prompt template id", code=4008, status_code=400) from exc

    template = db.get(PromptTemplate, template_uuid)
    if template is None:
        raise AppException(message="Prompt template not found", code=4045, status_code=404)

    try:
        template.scene = PromptScene(payload.scene)
        template.status = PromptTemplateStatus(payload.status)
    except ValueError as exc:
        raise AppException(message="Invalid prompt template scene or status", code=4009, status_code=400) from exc

    template.name = payload.name
    template.content = payload.content
    template.version = payload.version
    template.description = payload.description
    template.created_by = current_user.id
    db.add(template)
    db.commit()
    db.refresh(template)

    creator_email = template.creator.email if template.creator else current_user.email
    return PromptTemplateItem(
        id=template.id,
        name=template.name,
        scene=template.scene.value,
        version=template.version,
        status=template.status.value,
        description=template.description,
        content=template.content,
        created_by_email=creator_email,
        created_at=template.created_at,
        updated_at=template.updated_at,
    )


def delete_prompt_template(db: Session, template_id: str) -> None:
    try:
        template_uuid = UUID(template_id)
    except ValueError as exc:
        raise AppException(message="Invalid prompt template id", code=4008, status_code=400) from exc

    template = db.get(PromptTemplate, template_uuid)
    if template is None:
        raise AppException(message="Prompt template not found", code=4045, status_code=404)

    template.status = PromptTemplateStatus.DELETED
    db.add(template)
    db.commit()
