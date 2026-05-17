from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import db_session, get_current_user
from app.models.user import User
from app.schemas.job_schema import CreateJobRequest, UpdateJobRequest
from app.services.job_service import (
    create_job,
    delete_job,
    get_job_detail,
    list_jobs,
    parse_job,
    update_job,
)
from app.utils.response import success_response

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("")
def create_job_description(
    payload: CreateJobRequest,
    db: Session = Depends(db_session),
    current_user: User = Depends(get_current_user),
):
    result = create_job(db, current_user, payload)
    return success_response(data=result, message="创建成功")


@router.get("")
def list_user_jobs(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    keyword: str | None = Query(default=None),
    db: Session = Depends(db_session),
    current_user: User = Depends(get_current_user),
):
    result = list_jobs(db, current_user, page, page_size, keyword)
    return success_response(data=result, message="success")


@router.get("/{job_id}")
def get_job_description(
    job_id: UUID,
    db: Session = Depends(db_session),
    current_user: User = Depends(get_current_user),
):
    result = get_job_detail(db, current_user, job_id)
    return success_response(data=result, message="success")


@router.put("/{job_id}")
def put_job_description(
    job_id: UUID,
    payload: UpdateJobRequest,
    db: Session = Depends(db_session),
    current_user: User = Depends(get_current_user),
):
    result = update_job(db, current_user, job_id, payload)
    return success_response(data=result, message="更新成功")


@router.delete("/{job_id}")
def remove_job_description(
    job_id: UUID,
    db: Session = Depends(db_session),
    current_user: User = Depends(get_current_user),
):
    delete_job(db, current_user, job_id)
    return success_response(data=None, message="删除成功")


@router.post("/{job_id}/parse")
def reparse_job_description(
    job_id: UUID,
    db: Session = Depends(db_session),
    current_user: User = Depends(get_current_user),
):
    result = parse_job(db, current_user, job_id)
    return success_response(data=result, message="解析完成")
