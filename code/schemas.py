# from pydantic_settings import BaseModel
from pydantic import BaseModel
from pydantic import EmailStr
from typing import Optional, List, Dict
from datetime import datetime, date, time


class PublicUserData(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: int
    is_active: bool
    unit: str

    class Config:
        from_attributes = True


class AuthLoginUser(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    token: str
    token_type: str
    user: PublicUserData


class AuthRegisterUser(BaseModel):
    name: str
    email: EmailStr
    password: str
    re_password: str


class AuthForgotUser(BaseModel):
    email: EmailStr


class PostUserProfile(BaseModel):
    name: Optional[str]
    unit: Optional[str]


class AuthResetUser(BaseModel):
    spec_code: str
    email: EmailStr
    password: str


class UpdatePassword(BaseModel):
    current_password: str
    new_password: str


class AnalizeResponse(BaseModel):
    table_name: str
    feature_count: int
    date: date
    time: time
    area: float
    title: str
    country: str


class SummaryAnalizeResponse(BaseModel):
    feature_count: int
    area: float
    request_count: int


class CountryAnalizeResponse(BaseModel):
    country: str
    request_count: int


class DailyAnalizeResponse(BaseModel):
    feature_count: int
    request_count: int
    date: date
