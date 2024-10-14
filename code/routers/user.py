from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas import PublicUserData, PostUserProfile, UpdatePassword
from db import get_db
from utils.auth_funcs import JWTAuth, secure_pwd, verify_pwd
from models import User

route = APIRouter(prefix="/user", tags=["User"])


@route.post("/profile", response_model=PublicUserData)
def update_profile_data(
    payload: PostUserProfile,
    db: Session = Depends(get_db),
    user_token=Depends(JWTAuth()),
):
    """
    user profile update function

    :param payload: user update profile data
    :param db: db session data
    :param user_token: user token data
    :return : updated user data
    """

    user = db.query(User).filter(User.id == user_token["user_id"]).first()
    if payload.name:
        user.name = payload.name

    if payload.unit:
        if payload.unit != "metric" and payload.unit != "imperial":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unit value should be `metric` or `imperial`",
            )
        else:
            user.unit = payload.unit

    db.commit()
    db.refresh(user)

    db.add(user)
    db.commit()
    db.refresh(user)

    user_dict = user.__dict__
    del user_dict["_sa_instance_state"]

    return PublicUserData(**user_dict)


@route.get("/profile", response_model=PublicUserData)
def get_user_profile(db: Session = Depends(get_db), user_token=Depends(JWTAuth())):
    """
    get user token by token

    :param user_token: user token data from request header
    :return : authenticated user data
    """
    user = db.query(User).filter(User.id == user_token["user_id"]).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User doesn't exist"
        )

    user_dict = user.__dict__
    del user_dict["_sa_instance_state"]

    return PublicUserData(**user_dict)


@route.put("/update-password", response_model=PublicUserData)
def update_user_password(
    payload: UpdatePassword,
    db: Session = Depends(get_db),
    user_token=Depends(JWTAuth()),
):
    user = db.query(User).filter(User.id == user_token["user_id"]).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User doesn't exist"
        )

    if not verify_pwd(payload.current_password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Password doesn't match"
        )

    user.password = secure_pwd(payload.new_password)

    db.commit()
    db.refresh(user)

    user_dict = user.__dict__
    del user_dict["_sa_instance_state"]

    return PublicUserData(**user_dict)
