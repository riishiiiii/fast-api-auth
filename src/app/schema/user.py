from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum


class UserCreate(BaseModel):
    user_name: str
    name: str
    email: EmailStr
    phone_number: str
    password: str


class User(BaseModel):
    user_id: int
    user_name: str
    name: str
    email: EmailStr
    password: str
    sign_up_date: Optional[datetime] = None


class UserLogin(BaseModel):
    user_name: str
    password: str


class UserFields(Enum):
    USER_ID = "user_id"
    USER_NAME = "user_name"
    NAME = "name"
    PASSWORD = "password"
    EMAIL = "email"
    SIGN_UP_DATE = "sign_up_date"

