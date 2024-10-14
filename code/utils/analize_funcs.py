from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import date, datetime
from sqlalchemy import text

from models import AnalizeLogs


def save_analize_log(
    user_id: int,
    feature_count: int,
    area: float,
    table_name: str,
    title: str,
    country: str,
    db: Session,
):
    """
    Save log function

    :params user_id: current login user id
    :params feature_count: requested feature total count
    :params area: requested area total count
    :params table_name: used table name
    :params db: croptype db
    :return : None & save log
    """
    try:
        analize_log = AnalizeLogs(
            user_id=user_id,
            feature_count=feature_count,
            area_count=area,
            table_name=table_name,
            title=title,
            country=country,
        )

        db.add(analize_log)
        db.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_analize(user_id: int, db: Session):
    try:
        analize_log = db.query(AnalizeLogs).filter(AnalizeLogs.user_id == user_id).all()

        if not analize_log:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Log not found"
            )

        result = []

        for entry in analize_log:
            table_name = entry.table_name
            feature_count = entry.feature_count
            area = entry.area_count
            date = entry.time.date()
            time = datetime.strptime(
                entry.time.time().strftime("%H:%M:%S"), "%H:%M:%S"
            ).time()
            title = entry.title
            country = entry.country

            result.append(
                {
                    "table_name": table_name,
                    "feature_count": feature_count,
                    "date": date,
                    "area": area,
                    "time": time,
                    "title": title,
                    "country": country,
                }
            )

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_analize_with_period(user_id: int, start: date, end: date, db: Session):
    try:
        analize_log = (
            db.query(AnalizeLogs)
            .filter(AnalizeLogs.time >= start)
            .filter(AnalizeLogs.time <= end)
            .filter(AnalizeLogs.user_id == user_id)
            .all()
        )

        if not analize_log:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Log not found"
            )

        result = []
        for entry in analize_log:
            table_name = entry.table_name
            feature_count = entry.feature_count
            area = entry.area_count
            date = entry.time.date()
            time = datetime.strptime(
                entry.time.time().strftime("%H:%M:%S"), "%H:%M:%S"
            ).time()
            title = entry.title
            country = entry.country

            result.append(
                {
                    "table_name": table_name,
                    "feature_count": feature_count,
                    "date": date,
                    "area": area,
                    "time": time,
                    "title": title,
                    "country": country,
                }
            )

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
