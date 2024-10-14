from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from typing import List

from schemas import (
    AnalizeResponse,
    CountryAnalizeResponse,
    DailyAnalizeResponse,
    SummaryAnalizeResponse,
)
from db import get_db
from utils.auth_funcs import JWTAuth
from utils.analize_funcs import get_analize, get_analize_with_period
from models import AnalizeLogs

route = APIRouter(prefix="/analize", tags=["Analize"])


@route.get("/", response_model=List[AnalizeResponse])
def analize(db: Session = Depends(get_db), user_token=Depends(JWTAuth())):
    user_id = user_token["user_id"]

    result = get_analize(user_id, db)

    return result


@route.get("/period", response_model=List[AnalizeResponse])
def analize_with_period(
    from_date: date, to_date: date, db=Depends(get_db), user_token=Depends(JWTAuth())
):
    user_id = user_token["user_id"]

    analize_data = get_analize_with_period(user_id, from_date, to_date, db)

    return analize_data


@route.get("/summary", response_model=SummaryAnalizeResponse)
def analize_with_period(db: Session = Depends(get_db), user_token=Depends(JWTAuth())):
    user_id = user_token["user_id"]

    # analize_data = get_analize_with_period(user_id, db)
    analize_logs = (
        db.query(
            func.sum(AnalizeLogs.feature_count).label("feature_count"),
            func.sum(AnalizeLogs.area_count).label("area"),
            func.count().label("request_count"),
        )
        .filter(AnalizeLogs.user_id == user_id)
        .one()
    )

    return analize_logs


@route.get("/requests_by_country", response_model=List[CountryAnalizeResponse])
def analize_with_period(
    from_date: date,
    to_date: date,
    db: Session = Depends(get_db),
    user_token=Depends(JWTAuth()),
):
    user_id = user_token["user_id"]

    # analize_data = get_analize_with_period(user_id, db)
    country_logs = (
        db.query(
            AnalizeLogs.country.label("country"), func.count().label("request_count")
        )
        .filter(func.date(AnalizeLogs.time) >= from_date)
        .filter(func.date(AnalizeLogs.time) <= to_date)
        .filter(AnalizeLogs.user_id == user_id)
        .group_by(AnalizeLogs.country)
        .all()
    )

    return country_logs


@route.get("/requests_by_daily", response_model=List[DailyAnalizeResponse])
def analize_with_period(
    from_date: date,
    to_date: date,
    db: Session = Depends(get_db),
    user_token=Depends(JWTAuth()),
):
    user_id = user_token["user_id"]

    # analize_data = get_analize_with_period(user_id, db)
    daily_logs = (
        db.query(
            func.date(AnalizeLogs.time).label("date"),
            func.sum(AnalizeLogs.feature_count).label("feature_count"),
            func.count().label("request_count"),
        )
        .filter(func.date(AnalizeLogs.time) >= from_date)
        .filter(func.date(AnalizeLogs.time) <= to_date)
        .filter(AnalizeLogs.user_id == user_id)
        .group_by(func.date(AnalizeLogs.time))
        .all()
    )

    return daily_logs
