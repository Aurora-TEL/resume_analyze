from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import db_session, get_current_user
from app.models.user import User
from app.services.analysis_service import get_report_detail, list_reports
from app.utils.response import success_response

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("")
def report_list(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    resume_id: UUID | None = Query(default=None),
    job_description_id: UUID | None = Query(default=None),
    db: Session = Depends(db_session),
    current_user: User = Depends(get_current_user),
):
    result = list_reports(db, current_user, page, page_size, resume_id, job_description_id)
    return success_response(data=result, message="success")


@router.get("/{report_id}")
def report_detail(
    report_id: UUID,
    db: Session = Depends(db_session),
    current_user: User = Depends(get_current_user),
):
    result = get_report_detail(db, current_user, report_id)
    return success_response(data=result, message="success")
