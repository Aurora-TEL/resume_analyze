from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.core.exceptions import AppException
from app.core.config import get_settings
from app.models.analysis_report import AnalysisReport
from app.models.analysis_task import AnalysisTask
from app.models.enums import ParseStatus, PromptScene, TaskStatus, TaskType
from app.models.job_description import JobDescription
from app.models.resume import Resume
from app.models.user import User
from app.schemas.analysis_schema import (
    AnalysisTaskListItem,
    AnalysisTaskListResponse,
    AnalysisTaskStatusResponse,
    CreateAnalysisTaskRequest,
    CreateAnalysisTaskResponse,
)
from app.schemas.report_schema import ReportDetailResponse, ReportListItem, ReportListResponse
from app.services.ai.deepseek_client import DeepSeekClient
from app.services.job_service import get_job_or_404, parse_job
from app.services.resume_service import get_resume_or_404, parse_resume

deepseek_client = DeepSeekClient()
settings = get_settings()


def _ensure_resume_ready(db: Session, current_user: User, resume: Resume) -> Resume:
    if resume.parse_status != ParseStatus.SUCCESS or not resume.structured_data:
        parse_resume(db, current_user, resume.id)
        resume = get_resume_or_404(db, current_user, resume.id)
    return resume


def _ensure_job_ready(db: Session, current_user: User, job: JobDescription) -> JobDescription:
    if job.parse_status != ParseStatus.SUCCESS or not job.structured_data:
        parse_job(db, current_user, job.id)
        job = get_job_or_404(db, current_user, job.id)
    return job


def _build_report_data(db: Session, current_user: User, task_type: TaskType, task_id: UUID, resume: Resume, job: JobDescription | None) -> dict:
    if task_type != TaskType.FULL_ANALYSIS:
        raise AppException(message="Only full_analysis is supported in the current AI flow", code=4008, status_code=400)

    if job is None:
        raise AppException(message="Job description is required for full analysis", code=4007, status_code=400)

    ai_result = deepseek_client.call_scene(
        db,
        PromptScene.FULL_ANALYSIS.value,
        {
            "resume_text": resume.raw_text or "",
            "resume_structured_data": resume.structured_data or {},
            "job_text": job.description_text,
            "job_structured_data": job.structured_data or {},
        },
        user_id=current_user.id,
        task_id=task_id,
    )

    return {
        "total_score": ai_result["total_score"],
        "match_score": ai_result["match_score"],
        "summary": ai_result["summary"],
        "report_data": ai_result,
    }


def _get_report_id_for_task(db: Session, task_id: UUID) -> UUID | None:
    report = db.scalar(select(AnalysisReport.id).where(AnalysisReport.task_id == task_id))
    return report


def _build_task_status(task: AnalysisTask, report_id: UUID | None = None) -> AnalysisTaskStatusResponse:
    return AnalysisTaskStatusResponse(
        task_id=task.id,
        task_type=task.task_type.value,
        status=task.status.value,
        progress=task.progress,
        error_message=task.error_message,
        report_id=report_id,
        created_at=task.created_at,
        started_at=task.started_at,
        finished_at=task.finished_at,
    )


def create_analysis_task(db: Session, current_user: User, payload: CreateAnalysisTaskRequest) -> CreateAnalysisTaskResponse:
    try:
        task_type = TaskType(payload.task_type)
    except ValueError as exc:
        raise AppException(message="Invalid task type", code=4006, status_code=400) from exc

    resume = get_resume_or_404(db, current_user, payload.resume_id)
    job = None
    if payload.job_description_id:
        job = get_job_or_404(db, current_user, payload.job_description_id)

    if task_type in {TaskType.JOB_MATCH, TaskType.FULL_ANALYSIS} and job is None:
        raise AppException(message="job_description_id is required for this task type", code=4007, status_code=400)

    task = AnalysisTask(
        user_id=current_user.id,
        resume_id=resume.id,
        job_description_id=job.id if job else None,
        task_type=task_type,
        status=TaskStatus.PENDING,
        progress=0,
        retry_count=0,
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    try:
        task.status = TaskStatus.RUNNING
        task.progress = 10
        task.started_at = datetime.now(UTC)
        db.add(task)
        db.commit()
        db.refresh(task)

        resume = _ensure_resume_ready(db, current_user, resume)
        task.progress = 35
        db.add(task)
        db.commit()

        if job is not None:
            job = _ensure_job_ready(db, current_user, job)
        task.progress = 60
        db.add(task)
        db.commit()

        report_payload = _build_report_data(db, current_user, task_type, task.id, resume, job)
        report = AnalysisReport(
            task_id=task.id,
            user_id=current_user.id,
            resume_id=resume.id,
            job_description_id=job.id if job else None,
            total_score=report_payload["total_score"],
            match_score=report_payload["match_score"],
            summary=report_payload["summary"],
            report_data=report_payload["report_data"],
            model_provider="deepseek",
            model_name=settings.deepseek_model,
            report_version=1,
        )
        db.add(report)

        task.status = TaskStatus.SUCCESS
        task.progress = 100
        task.finished_at = datetime.now(UTC)
        task.error_message = None
        db.add(task)
        db.commit()
        db.refresh(task)
        db.refresh(report)

        return CreateAnalysisTaskResponse(task_id=task.id, status=task.status.value, report_id=report.id)
    except AppException as exc:
        task.status = TaskStatus.FAILED
        task.progress = 100
        task.finished_at = datetime.now(UTC)
        task.error_message = exc.message
        db.add(task)
        db.commit()
        raise
    except Exception as exc:  # noqa: BLE001
        task.status = TaskStatus.FAILED
        task.progress = 100
        task.finished_at = datetime.now(UTC)
        task.error_message = str(exc)
        db.add(task)
        db.commit()
        raise AppException(message="Analysis failed", code=5001, status_code=500, errors=str(exc)) from exc


def get_analysis_task_status(db: Session, current_user: User, task_id: UUID) -> AnalysisTaskStatusResponse:
    task = db.scalar(
        select(AnalysisTask).where(
            AnalysisTask.id == task_id,
            AnalysisTask.user_id == current_user.id,
        )
    )
    if task is None:
        raise AppException(message="Analysis task not found", code=4043, status_code=404)

    report_id = _get_report_id_for_task(db, task.id)
    return _build_task_status(task, report_id)


def list_analysis_tasks(
    db: Session,
    current_user: User,
    page: int,
    page_size: int,
    status: str | None,
    task_type: str | None,
) -> AnalysisTaskListResponse:
    filters = [AnalysisTask.user_id == current_user.id]
    if status:
        filters.append(AnalysisTask.status == status)
    if task_type:
        filters.append(AnalysisTask.task_type == task_type)

    total = db.scalar(select(func.count()).select_from(AnalysisTask).where(*filters)) or 0
    items = db.scalars(
        select(AnalysisTask)
        .where(*filters)
        .order_by(AnalysisTask.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()

    response_items = [
        AnalysisTaskListItem(
            id=item.id,
            task_type=item.task_type.value,
            status=item.status.value,
            progress=item.progress,
            error_message=item.error_message,
            created_at=item.created_at,
            started_at=item.started_at,
            finished_at=item.finished_at,
        )
        for item in items
    ]
    return AnalysisTaskListResponse.build(response_items, total, page, page_size)


def list_reports(
    db: Session,
    current_user: User,
    page: int,
    page_size: int,
    resume_id: UUID | None,
    job_description_id: UUID | None,
) -> ReportListResponse:
    filters = [AnalysisReport.user_id == current_user.id]
    if resume_id:
        filters.append(AnalysisReport.resume_id == resume_id)
    if job_description_id:
        filters.append(AnalysisReport.job_description_id == job_description_id)

    total = db.scalar(select(func.count()).select_from(AnalysisReport).where(*filters)) or 0
    items = db.scalars(
        select(AnalysisReport)
        .options(
            joinedload(AnalysisReport.resume),
            joinedload(AnalysisReport.job_description),
        )
        .where(*filters)
        .order_by(AnalysisReport.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()

    response_items = [
        ReportListItem(
            id=item.id,
            task_id=item.task_id,
            resume_title=item.resume.title,
            job_title=item.job_description.title if item.job_description else None,
            total_score=item.total_score,
            match_score=item.match_score,
            summary=item.summary,
            created_at=item.created_at,
        )
        for item in items
    ]
    return ReportListResponse.build(response_items, total, page, page_size)


def get_report_detail(db: Session, current_user: User, report_id: UUID) -> ReportDetailResponse:
    report = db.scalar(
        select(AnalysisReport).where(
            AnalysisReport.id == report_id,
            AnalysisReport.user_id == current_user.id,
        )
    )
    if report is None:
        raise AppException(message="Report not found", code=4044, status_code=404)

    return ReportDetailResponse(
        id=report.id,
        task_id=report.task_id,
        resume_id=report.resume_id,
        job_description_id=report.job_description_id,
        total_score=report.total_score,
        match_score=report.match_score,
        summary=report.summary,
        report_data=report.report_data,
        model_provider=report.model_provider,
        model_name=report.model_name,
        created_at=report.created_at,
    )
