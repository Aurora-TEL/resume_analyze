from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from sqlalchemy.orm import Session

from app.core.deps import db_session, get_current_user
from app.models.user import User
from app.schemas.resume_schema import UpdateResumeRequest
from app.services.resume_service import (
    delete_resume,
    get_resume_detail,
    list_resumes,
    parse_resume,
    update_resume,
    upload_resume,
)
from app.utils.response import success_response

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.post("/upload")
def upload(
    file: UploadFile = File(...),
    title: str | None = Form(default=None),
    db: Session = Depends(db_session),
    current_user: User = Depends(get_current_user),
):
    result = upload_resume(db, current_user, file, title)
    return success_response(data=result, message="上传成功")


@router.get("")
def list_user_resumes(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    keyword: str | None = Query(default=None),
    status: str | None = Query(default=None),
    db: Session = Depends(db_session),
    current_user: User = Depends(get_current_user),
):
    result = list_resumes(db, current_user, page, page_size, keyword, status)
    return success_response(data=result, message="success")


@router.get("/{resume_id}")
def detail(
    resume_id: UUID,
    db: Session = Depends(db_session),
    current_user: User = Depends(get_current_user),
):
    result = get_resume_detail(db, current_user, resume_id)
    return success_response(data=result, message="success")


@router.patch("/{resume_id}")
def patch_resume(
    resume_id: UUID,
    payload: UpdateResumeRequest,
    db: Session = Depends(db_session),
    current_user: User = Depends(get_current_user),
):
    result = update_resume(db, current_user, resume_id, payload)
    return success_response(data=result, message="更新成功")


@router.delete("/{resume_id}")
def remove_resume(
    resume_id: UUID,
    db: Session = Depends(db_session),
    current_user: User = Depends(get_current_user),
):
    delete_resume(db, current_user, resume_id)
    return success_response(data=None, message="删除成功")


@router.post("/{resume_id}/parse")
def reparse_resume(
    resume_id: UUID,
    db: Session = Depends(db_session),
    current_user: User = Depends(get_current_user),
):
    result = parse_resume(db, current_user, resume_id)
    return success_response(data=result, message="解析完成")
