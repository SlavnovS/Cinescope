from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
import datetime
from constants import Roles

class TestUser(BaseModel):
    email: str
    fullName: str
    password: str = Field(min_length=8, max_length=20)
    passwordRepeat: str = Field(min_length=8, max_length=20)
    roles: list[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @classmethod
    @field_validator("passwordRepeat")
    def password_repeat_validator(cls, value: str, info) -> str:
        if "password" in info.data and value != info.data['password']:
            raise ValueError("Пароли не совпадают")
        return value

class RegisterUserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    fullName: str
    verified: bool
    banned: bool
    roles: List[Roles]
    createdAt: str

    @classmethod
    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени")
        return value