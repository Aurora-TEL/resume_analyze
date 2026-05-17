from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, StringConstraints
from typing_extensions import Annotated


PhoneStr = Annotated[str, StringConstraints(max_length=50)]


class CurrentUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    nickname: str | None = None
    phone: str | None = None
    avatar_url: str | None = None
    target_position: str | None = None
    target_city: str | None = None
    work_years: Decimal | None = None
    role: str
    status: str


class UpdateCurrentUserRequest(BaseModel):
    nickname: str | None = Field(default=None, max_length=100)
    phone: PhoneStr | None = None
    target_position: str | None = Field(default=None, max_length=100)
    target_city: str | None = Field(default=None, max_length=100)
    work_years: Decimal | None = Field(default=None, ge=0, le=99.9)


class UpdatePasswordRequest(BaseModel):
    old_password: str = Field(min_length=1, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)
