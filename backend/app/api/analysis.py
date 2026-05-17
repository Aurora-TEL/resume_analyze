from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import db_session, get_current_user
from app.models.user import User
from app.schemas.analysis_schema import CreateAnalysisTaskRequest
from app.services.analysis_service import (
    create_analysis_task,
    get_analysis_task_status,
    list_analysis_tasks,
)
from app.utils.response import success_response

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("/tasks")
def create_task(
    payload: CreateAnalysisTaskRequest,
    db: Session = Depends(db_session),
    current_user: User = Depends(get_current_user),
):
    result = create_analysis_task(db, current_user, payload)
    return success_response(data=result, message="分析完成")


@router.get("/tasks/{task_id}")
def get_task(
    task_id: UUID,
    db: Session = Depends(db_session),
    current_user: User = Depends(get_current_user),
):
    result = get_analysis_task_status(db, current_user, task_id)
    return success_response(data=result, message="success")


@router.get("/tasks")
def list_tasks(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    status: str | None = Query(default=None),
    task_type: str | None = Query(default=None),
    db: Session = Depends(db_session),
    current_user: User = Depends(get_current_user),
):
    result = list_analysis_tasks(db, current_user, page, page_size, status, task_type)
    return success_response(data=result, message="success")
