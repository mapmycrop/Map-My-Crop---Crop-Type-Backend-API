from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from config import setting


SQLALCHEMY_DATABASE_URL = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
    setting.DB_USER,
    setting.DB_PASSWORD,
    setting.DB_HOST,
    setting.DB_PORT,
    setting.DB_NAME,
)

DATA_SQLALCHEMY_DATABASE_URL = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
    setting.DATA_DB_USER,
    setting.DATA_DB_PASSWORD,
    setting.DATA_DB_HOST,
    setting.DATA_DB_PORT,
    setting.DATA_DB_NAME,
)


pool_size = 75
max_overflow = 25

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_size=pool_size, max_overflow=max_overflow
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

data_engine = create_engine(
    DATA_SQLALCHEMY_DATABASE_URL, pool_size=pool_size, max_overflow=max_overflow
)

data_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=data_engine)

data_Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()

    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        print("Database error", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database Error! Please try again later",
        )

    try:
        yield db
    finally:
        db.close()


# Dependency
def data_get_db():
    db = data_SessionLocal()

    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        print("Database error", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database Error! Please try again later",
        )

    try:
        yield db
    finally:
        db.close()
