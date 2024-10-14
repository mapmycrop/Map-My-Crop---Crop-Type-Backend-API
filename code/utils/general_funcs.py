from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sib_api_v3_sdk.rest import ApiException
import sib_api_v3_sdk
import uuid
import math
import random

from models import User
from schemas import PublicUserData
from config import setting


def generate_uuid():
    """
    Generate uuid

    :return : uuid string
    """

    return str(uuid.uuid4().hex)


def get_user_by_email(db: Session, email: str):
    """
    Get User with email

    :param email: email string
    :param db: database session
    :return : existed user
    """

    existed_user = db.query(User).filter(User.email == email).first()

    if not existed_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User doesn't exist"
        )

    return existed_user


def convert_public_userdata(user):
    """
    Convert user data to public


    """
    return PublicUserData()


def send_email(sender, to, subject, html_content):
    """
    :param sender: the format should be like {"name": "Info", "email": "info@mapmycrop.com"}
    :param to: the format should be like {"name": "Customer", "email": "customer@gmail.com"}
    :param subject: string
    :param html_content: html string

    :return : will send email to owner
    """

    # Configure API key authorization: api-key
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = setting.SENDINBLUE_KEY

    # create an instance of the API class
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        sender=sender, to=[to], subject=subject, html_content=html_content
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        return api_response
    except ApiException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e)


def generate_otp():
    """
    Generate OTP code for email verification

    :return: OTP code
    """

    digits = "0123456789"
    otp = ""

    for i in range(6):
        otp += digits[math.floor(random.random() * 10)]

    return otp
