from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import data_get_db, get_db
from typing import Optional
from sqlalchemy import text
from utils.auth_funcs import JWTAuth
from utils.farmcrop_funcs import get_region
from utils.analize_funcs import save_analize_log
from urllib.parse import unquote_plus

route = APIRouter(prefix="/farmcrop", tags=["FarmCrop"])


@route.get("/polygon")
def get_farm_polygon(
    wkt: str,
    data_db: Session = Depends(data_get_db),
    db: Session = Depends(get_db),
    year: Optional[int] = None,
    user_token=Depends(JWTAuth()),
):
    """
    Get farm based on polygon

    :params wkt: polygons data
    :params data_db: datasource db
    :params year: updated year
    :params user_token: user data from token value
    """

    converted_wkt = unquote_plus(wkt)
    region = get_region(wkt=converted_wkt, year=year, data_db=data_db)
    if "latest_data" in region:
        raw_text = text(
            f"""
            SELECT json_build_object(
                'type', 'FeatureCollection',
                'features', json_agg(ST_AsGeoJSON(t.*)::json)
            )
            FROM crop_type.{region['latest_data']}  AS t WHERE ST_Contains(ST_GeomFromText('{converted_wkt}', 4326), geom)
            """
        )
        result = data_db.execute(raw_text).scalar()

        if result["features"]:
            table_name = region["latest_data"]

            feature = result["features"]
            area_list = []
            for i in feature:
                country = i["properties"].get("country")
                area_ha = i["properties"].get("area_ha")
                area_list.append(area_ha if area_ha is not None else 0.0)

            area_ha = sum(area_list)

            feature_count = len(result["features"])

            save_analize_log(
                user_id=user_token["user_id"],
                feature_count=feature_count,
                area=area_ha,
                db=db,
                table_name=table_name,
                title="Buffer request",
                country=country,
            )

        return result

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location is not farm land",
        )


@route.get("/buffer")
def get_farm_buffer(
    lat: float,
    lon: float,
    buffer: float,
    data_db: Session = Depends(data_get_db),
    db: Session = Depends(get_db),
    year: Optional[int] = None,
    user_token=Depends(JWTAuth()),
):
    """
    Get farm based on polygon

    :params lat: burffer's lat position
    :params lon: burffer's lon position
    :params buffer: buffer's radius
    :params data_db: datasource db
    :params year: updated year
    :params user_token: user data from token value
    """

    wkt = f"POINT({lon} {lat})"
    region = get_region(wkt=wkt, year=year, data_db=data_db)

    if "latest_data" in region:
        raw_text = text(
            f"""SELECT json_build_object(
                'type', 'FeatureCollection',
                'features', json_agg(ST_AsGeoJSON(t.*)::json)
            )
            FROM crop_type.{region['latest_data']}  AS t WHERE ST_Intersects(
                geom,
                ST_Buffer(
                    ST_SetSRID(ST_MakePoint({lon}, {lat}),4326)::geography,
                    {buffer}
                )::geometry
            )
            """
        )

        result = data_db.execute(raw_text).scalar()

        if result["features"]:
            table_name = region["latest_data"]

            feature = result["features"]
            area_list = []
            for i in feature:
                country = i["properties"].get("country")
                area_ha = i["properties"].get("area_ha")
                area_list.append(area_ha if area_ha is not None else 0.0)

            area_ha = sum(area_list)

            feature_count = len(result["features"])

            save_analize_log(
                user_id=user_token["user_id"],
                feature_count=feature_count,
                area=area_ha,
                db=db,
                table_name=table_name,
                title="Buffer request",
                country=country,
            )

        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location is not farm land",
        )
