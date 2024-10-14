from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db import get_db
from models import User
from schemas import (
    AuthLoginUser,
    AuthRegisterUser,
    AuthForgotUser,
    AuthResetUser,
    AuthResponse,
    PublicUserData,
)
from utils.general_funcs import get_user_by_email
from utils.auth_funcs import (
    create_access_token,
    secure_pwd,
    verify_pwd,
    send_otp_to_email,
    check_email_otp,
)


route = APIRouter(prefix="/auth", tags=["Authentication"])


@route.post("/login", response_model=AuthResponse)
def login(payload: AuthLoginUser, db: Session = Depends(get_db)):
    """
    Login function for user based on email and password

    :param payload: login user data
    :paran db: database session
    :return : login User data included token
    """

    user = get_user_by_email(db, payload.email)

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="User is not activated. Please contact sales to activate your Account.",
        )

    if not verify_pwd(plain_pwd=payload.password, hash_pwd=user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User password is incorrect.",
        )

    token_payload = {
        "user_id": user.id,
        "user_email": user.email,
        "user_role": user.role,
    }

    token = create_access_token(token_payload)

    user_dict = user.__dict__
    del user_dict["_sa_instance_state"]

    return AuthResponse(
        token=token, token_type="bearer", user=PublicUserData(**user_dict)
    )


@route.post("/register", response_model=AuthResponse)
def register(payload: AuthRegisterUser, db: Session = Depends(get_db)):
    """
    Register function for user based on email and password

    :param payload: login user data
    :paran db: database session
    :return : login User data included token
    """

    if payload.password != payload.re_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password and Re-password doesn't match",
        )

    user = User(
        name=payload.name,
        email=payload.email,
        password=secure_pwd(payload.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    token_payload = {
        "user_id": user.id,
        "user_email": user.email,
        "user_role": user.role,
    }
    token = create_access_token(token_payload)

    user_dict = user.__dict__
    del user_dict["_sa_instance_state"]

    return AuthResponse(
        token=token, token_type="bearer", user=PublicUserData(**user_dict)
    )


@route.post("/forgot_password")
def forgot_password(payload: AuthForgotUser, db: Session = Depends(get_db)):
    """
    Forgot_password function for user based on email

    :param payload: user email for reset password
    :paran db: database session
    :return : send email to reset password
    """

    user = get_user_by_email(db, payload.email)

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="User is not activated. Please contact sales to activate your Account.",
        )

    send_otp_to_email(user.email)

    return "Email was sent, please check your email box"


@route.post("/reset_password", response_model=AuthResponse)
def reset_password(payload: AuthResetUser, db: Session = Depends(get_db)):
    """
    Reset password function for user based on spec code

    :param payload: spec code and password data for reset user
    :paran db: database session
    :return : User data included token
    """

    user = db.query(User).filter(User.email == payload.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="The user doesn't exist"
        )

    if check_email_otp(payload.email, payload.spec_code):
        user.password = secure_pwd(payload.password)

        db.commit()
        db.refresh(user)

    token_payload = {
        "user_id": user.id,
        "user_email": user.email,
        "user_role": user.role,
    }
    token = create_access_token(token_payload)

    user_dict = user.__dict__
    del user_dict["_sa_instance_state"]

    return AuthResponse(
        token=token, token_type="bearer", user=PublicUserData(**user_dict)
    )


@route.post("/send_otp")
def send_otp(email: str, db: Session = Depends(get_db)):

    user = get_user_by_email(db, email)

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="User is not activated. Please contact sales to activate your Account.",
        )

    return send_otp_to_email(email)
