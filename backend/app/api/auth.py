from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import db_session, get_current_user
from app.models.user import User
from app.schemas.auth_schema import LoginRequest, RegisterRequest
from app.schemas.user_schema import CurrentUserResponse
from app.services.auth_service import login_user, register_user
from app.utils.response import success_response

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(db_session)):
    result = register_user(db, payload)
    return success_response(data=result, message="success")


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(db_session)):
    result = login_user(db, payload)
    return success_response(data=result, message="success")


@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    result = CurrentUserResponse.model_validate(current_user)
    return success_response(data=result, message="success")


@router.post("/logout")
def logout(_: User = Depends(get_current_user)):
    return success_response(data={"logged_out": True}, message="success")
