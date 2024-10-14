from db import Base

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    JSON,
    String,
    DATE,
    Float,
    DateTime,
    ARRAY,
    TIMESTAMP,
    Text,
    Boolean,
)
from sqlalchemy.sql import func


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True, default="")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    name = Column(String, nullable=False, default="")
    password = Column(String, nullable=False)
    role = Column(Integer, ForeignKey("roles.id"), default=1)
    is_active = Column(Boolean, default=False)
    unit = Column(String, nullable=False, default="metric")
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)


class AnalizeLogs(Base):
    __tablename__ = "analize_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    feature_count = Column(Integer)
    area_count = Column(Float)
    table_name = Column(String, nullable=False, default="")
    user_id = Column(Integer)
    title = Column(String, nullable=False)
    country = Column(String, nullable=False)
    time = Column(DateTime(timezone=True), default=func.now(), nullable=False)
