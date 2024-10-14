from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional


def get_region(wkt: str, data_db: Session, year: Optional[int] = None):
    """
    Get Region based on lat, lon and year data

    :params wkt: geometry info for farm data
    :params data_db: source data db
    :params year: updated year date
    :return : year region data
    """

    raw_query = text(
        f"SELECT region_name, code FROM crop_type.regions WHERE  ST_Within(ST_GeomFromText('{wkt}', 4326), geometry) AND available = true"
    )
    result = data_db.execute(raw_query).fetchone()
    if result:
        raw_query_table_check = text(
            f"SELECT CONCAT(code, '_', {year or 'max'}) AS combined_name FROM crop_type.latest_county where code = '{result[1]}'"
        )

        table_result = data_db.execute(raw_query_table_check).fetchone()

        if table_result is None:
            return {"name": result[0], "code": result[1]}
        else:
            return {
                "name": result[0],
                "code": result[1],
                "latest_data": table_result[0],
            }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Outside Coverage area"
        )
