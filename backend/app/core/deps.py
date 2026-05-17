from typing import Any
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import AppException
from app.models.enums import UserRole
from app.models.user import User
from app.core.security import decode_access_token
from app.services.auth_service import get_user_by_id
from app.services.user_service import ensure_active_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def db_session(db: Session = Depends(get_db)) -> Session:
    return db


def get_token_payload(token: str = Depends(oauth2_scheme)) -> dict[str, Any]:
    try:
        return decode_access_token(token)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from exc


def get_current_user(
    payload: dict[str, Any] = Depends(get_token_payload),
    db: Session = Depends(db_session),
) -> User:
    subject = payload.get("sub")
    if not subject:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    try:
        user_id = UUID(subject)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject") from exc

    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return ensure_active_user(user)


def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ADMIN:
        raise AppException(message="Admin permission required", code=4031, status_code=403)
    return current_user
