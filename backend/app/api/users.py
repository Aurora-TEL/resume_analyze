from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import db_session, get_current_user
from app.models.user import User
from app.schemas.user_schema import (
    CurrentUserResponse,
    UpdateCurrentUserRequest,
    UpdatePasswordRequest,
)
from app.services.user_service import update_current_user, update_current_user_password
from app.utils.response import success_response

router = APIRouter(prefix="/users", tags=["users"])


@router.put("/me")
def update_me(
    payload: UpdateCurrentUserRequest,
    db: Session = Depends(db_session),
    current_user: User = Depends(get_current_user),
):
    user = update_current_user(db, current_user, payload)
    return success_response(data=CurrentUserResponse.model_validate(user), message="更新成功")


@router.put("/me/password")
def update_me_password(
    payload: UpdatePasswordRequest,
    db: Session = Depends(db_session),
    current_user: User = Depends(get_current_user),
):
    update_current_user_password(db, current_user, payload)
    return success_response(data={"updated": True}, message="更新成功")
