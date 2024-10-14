from fastapi import APIRouter, Depends, HTTPException, status, Body, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, select
from functools import wraps
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page

# import requests
from config import setting
from db import get_db
from models import User
from utils.auth_funcs import JWTAuth
from schemas import PublicUserData
from constant import ADMIN

route = APIRouter(prefix="/admin", tags=["Admin"])


@route.get("/get-all-users")
def get_all_users(db: Session = Depends(get_db), user_token=Depends(JWTAuth())):
    if user_token["user_role"] != 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This user is not admin",
        )

    # Create the base query
    query = select(User.id, User.name, User.email, User.role, User.is_active)

    # Execute the query and fetch all results
    users = db.execute(query).fetchall()

    # Convert the result to a list of dictionaries
    users_list = [
        {
            "id": user.id,
            "name": user.name,
            "role": user.role,
            "email": user.email,
            "is_active": user.is_active,
        }
        for user in users
    ]
    response = {"ok": True, "status": 200, users_list: users_list}

    return response


@route.get("/activate-user")
def activate_user(
    user_email: str = "", db: Session = Depends(get_db), user_token=Depends(JWTAuth())
):
    """
    Activate user function

    :param user_id: user's mail
    :param db: database
    :params user_token: user data from token value
    :return : "success"
    """

    if user_token["user_role"] != 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This user is not admin",
        )

    user = (
        db.query(User)
        .filter(User.email == user_email)
        .update({"is_active": True}, synchronize_session=False)
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User doesn't exist!",
        )

    db.commit()
    response = {"ok": True, "status": 200, "details": "User activated Successfully!"}

    return response


@route.get("/deactivate-user")
def deactivate_user(
    user_email: str = "", db: Session = Depends(get_db), user_token=Depends(JWTAuth())
):
    """
    Deactivate user function

    :param user_id: user's mail
    :param db: database
    :params user_token: user data from token value
    :return : "success"
    """

    if user_token["user_role"] != 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This user is not admin",
        )

    user = (
        db.query(User)
        .filter(User.email == user_email)
        .update({"is_active": False}, synchronize_session=False)
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User doesn't exist!",
        )

    db.commit()

    response = {"ok": True, "status": 200, "details": "User deactivated Successfully!"}

    return response
