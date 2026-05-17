from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.exceptions import AppException
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.enums import UserRole, UserStatus
from app.models.user import User
from app.schemas.auth_schema import AuthUser, LoginRequest, LoginResponse, RegisterRequest, RegisterResponse

settings = get_settings()


def _get_user_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email))


def get_user_by_id(db: Session, user_id: UUID) -> User | None:
    return db.get(User, user_id)


def register_user(db: Session, payload: RegisterRequest) -> RegisterResponse:
    existing_user = _get_user_by_email(db, payload.email)
    if existing_user is not None:
        raise AppException(message="Email already registered", code=4001, status_code=400)

    user = User(
        email=payload.email,
        password_hash=get_password_hash(payload.password),
        nickname=payload.nickname,
        role=UserRole.USER,
        status=UserStatus.ACTIVE,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(str(user.id))
    return RegisterResponse(
        user_id=user.id,
        email=user.email,
        nickname=user.nickname,
        role=user.role.value,
        access_token=access_token,
    )


def login_user(db: Session, payload: LoginRequest) -> LoginResponse:
    user = _get_user_by_email(db, payload.email)
    if user is None or not verify_password(payload.password, user.password_hash):
        raise AppException(message="Invalid email or password", code=4002, status_code=401)

    if user.status != UserStatus.ACTIVE:
        raise AppException(message="User account is not active", code=4003, status_code=403)

    user.last_login_at = datetime.now(UTC)
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(str(user.id))
    return LoginResponse(
        access_token=access_token,
        expires_in=settings.jwt_expire_minutes * 60,
        user=AuthUser.model_validate(user),
    )
