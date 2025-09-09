from pydantic import BaseModel, ConfigDict, constr, field_validator
from ..enum import OperationUserStatus
from typing import Annotated
from ..models import validate_email_address
from fastapi import Query

PasswordStr = Annotated[
    str,
    constr(min_length=8, max_length=64, pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).*$")
]

# for create users
class UserBase(BaseModel):
    email: str
    username: str

    @field_validator('email')
    @classmethod
    def valid_email(cls, value: str) -> str:
        return validate_email_address(value)

class UserCreate(UserBase):
    password: PasswordStr
    
class UserInDB(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status_operation: OperationUserStatus = OperationUserStatus.CREATED

#for delete user
class UserDelete(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int

class CheckUser(BaseModel):
    username: str | None = Query(None, description="Логин пользователя")
    email: str | None = Query(None, description="Email пользователя")

    @field_validator('email')
    @classmethod
    def validate_email(cls, value: str | None) -> str | None:
        """Валидация email если он передан"""
        if value is None:
            return value
        return validate_email_address(value)  # Ваш кастомный валидатор