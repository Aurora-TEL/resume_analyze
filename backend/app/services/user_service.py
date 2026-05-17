from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.core.security import get_password_hash, verify_password
from app.models.enums import UserStatus
from app.models.user import User
from app.schemas.user_schema import UpdateCurrentUserRequest, UpdatePasswordRequest


def ensure_active_user(user: User) -> User:
    if user.status != UserStatus.ACTIVE:
        raise AppException(message="User account is not active", code=4003, status_code=403)
    return user


def update_current_user(db: Session, user: User, payload: UpdateCurrentUserRequest) -> User:
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_current_user_password(db: Session, user: User, payload: UpdatePasswordRequest) -> None:
    if not verify_password(payload.old_password, user.password_hash):
        raise AppException(message="Old password is incorrect", code=4004, status_code=400)

    user.password_hash = get_password_hash(payload.new_password)
    db.add(user)
    db.commit()
