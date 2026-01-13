from pydantic import BaseModel, Field, field_validator, RootModel
from typing import Optional, List
from datetime import datetime, timedelta
from constants import Roles
from enum import Enum

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
    banned: Optional[bool] = None
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

class PaymentStatus(str, Enum):
    SUCCESS = "SUCCESS"
    INVALID_CARD = "INVALID_CARD"
    ERROR = "ERROR"

class PaymentGetResponse(BaseModel):
    id: int
    user_id: str = Field(pattern=r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$',
                        alias='userId')
    movie_id: int = Field(..., gt=0, alias='movieId')
    status: PaymentStatus
    amount: int
    total: int
    created_at: datetime = Field(alias='createdAt')

class PaymentsList(RootModel[List[PaymentGetResponse]]):
    pass