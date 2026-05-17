from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import db_session, get_admin_user
from app.models.user import User
from app.schemas.admin_schema import CreatePromptTemplateRequest, UpdatePromptTemplateRequest
from app.services.admin_service import (
    create_prompt_template,
    delete_prompt_template,
    get_admin_overview,
    list_admin_analysis_tasks,
    list_admin_api_logs,
    list_prompt_templates,
    update_prompt_template,
)
from app.utils.response import success_response

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/overview")
def overview(
    db: Session = Depends(db_session),
    _: User = Depends(get_admin_user),
):
    return success_response(data=get_admin_overview(db), message="success")


@router.get("/analysis-tasks")
def analysis_tasks(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    status: str | None = Query(default=None),
    task_type: str | None = Query(default=None),
    keyword: str | None = Query(default=None),
    db: Session = Depends(db_session),
    _: User = Depends(get_admin_user),
):
    result = list_admin_analysis_tasks(
        db,
        page=page,
        page_size=page_size,
        status=status,
        task_type=task_type,
        keyword=keyword,
    )
    return success_response(data=result, message="success")


@router.get("/api-logs")
def api_logs(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    status: str | None = Query(default=None),
    scene: str | None = Query(default=None),
    keyword: str | None = Query(default=None),
    db: Session = Depends(db_session),
    _: User = Depends(get_admin_user),
):
    result = list_admin_api_logs(
        db,
        page=page,
        page_size=page_size,
        status=status,
        scene=scene,
        keyword=keyword,
    )
    return success_response(data=result, message="success")


@router.get("/prompt-templates")
def prompt_templates(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    scene: str | None = Query(default=None),
    status: str | None = Query(default=None),
    keyword: str | None = Query(default=None),
    db: Session = Depends(db_session),
    _: User = Depends(get_admin_user),
):
    result = list_prompt_templates(
        db,
        page=page,
        page_size=page_size,
        scene=scene,
        status=status,
        keyword=keyword,
    )
    return success_response(data=result, message="success")


@router.post("/prompt-templates")
def create_template(
    payload: CreatePromptTemplateRequest,
    db: Session = Depends(db_session),
    current_user: User = Depends(get_admin_user),
):
    result = create_prompt_template(db, current_user, payload)
    return success_response(data=result, message="created")


@router.put("/prompt-templates/{template_id}")
def update_template(
    template_id: str,
    payload: UpdatePromptTemplateRequest,
    db: Session = Depends(db_session),
    current_user: User = Depends(get_admin_user),
):
    result = update_prompt_template(db, current_user, template_id, payload)
    return success_response(data=result, message="updated")


@router.delete("/prompt-templates/{template_id}")
def delete_template(
    template_id: str,
    db: Session = Depends(db_session),
    _: User = Depends(get_admin_user),
):
    delete_prompt_template(db, template_id)
    return success_response(data={"deleted": True}, message="deleted")
