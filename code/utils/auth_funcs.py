import time
from jose import jwt
from fastapi import HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from typing import Optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import setting
from cache import get_redis
from utils.general_funcs import send_email, generate_uuid, generate_otp, send_email
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pydantic import ValidationError


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


class JWTAuth(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTAuth, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        credentials: HTTPAuthorizationCredentials = await super(JWTAuth, self).__call__(
            request
        )

        if credentials is None:
            raise HTTPException(status_code=401, detail="Missing authorization token")

        if not credentials.scheme == "Bearer":
            raise HTTPException(
                status_code=403, detail="Invalid authentication scheme."
            )

        try:
            payload = jwt.decode(
                credentials.credentials,
                setting.JWT_SECRET_KEY,
                algorithms=[setting.JWT_ALGORITHM],
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except (jwt.PyJWTError, ValidationError):
            raise HTTPException(status_code=403, detail="Invalid token")

        # Check if the token is still valid
        exp = payload.get("exp")
        if exp is None or exp < time.time():
            raise HTTPException(status_code=401, detail="Token has expired")

        return payload


def create_access_token(data: dict):
    """
    generate access token

    :param data: loged user data
    :return : encrypted string with user data and expire time
    """

    to_encode = data.copy()
    expire = time.time() + setting.JWT_EXPIRE_HOUR * 60 * 60
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, setting.JWT_SECRET_KEY, algorithm=setting.JWT_ALGORITHM
    )
    return encoded_jwt


def secure_pwd(password: str):
    """
    generate secure password

    :param password: password string user send
    :return : hashed password
    """

    return pwd_context.hash(password)


def verify_pwd(plain_pwd: str, hash_pwd: str):
    """
    confirm password

    :param plain_pwd: unhashed password
    :param hash_pwd: hashed password
    :return : true or false
    """

    return pwd_context.verify(plain_pwd, hash_pwd)


def send_reset_password_email(client_email: str):
    spec_code = generate_uuid()

    cache = get_redis()
    if cache.get(f"{spec_code}_spec_code"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The link already sent to your email, if didn't get yet, please try again after 10 minutes",
        )
    cache.set(f"{spec_code}_spec_code", client_email, 10 * 60)

    sender = {"name": "MMC-Crop-Type", "email": "alerts@mapmycrop.com"}
    to = {"email": client_email, "name": "Customer"}
    subject = "Map My Crop - Crop Type"
    html_content = f"<html><body><h3>Your Map My Crop - Crop Type reset password link is {setting.FRONTEND_LINK}/{spec_code}</h3></body></html>"

    send_email(sender=sender, to=to, subject=subject, html_content=html_content)


def get_email_from_spec_code(spec_code: str):
    """
    Get email data that saved in cache using spec_code

    :param spec_code: spec code
    :return : email data from cache
    """

    cache = get_redis()
    email = cache.get(f"{spec_code}_spec_code")

    if not email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This request is timeout request",
        )

    return email


def send_otp_to_email(email):
    """
    Sending OTP code to specific email.

    :param email: email for OTP
    :return: True if it's successful, raise Exception if it's failed
    """

    otp_code = generate_otp()

    cache = get_redis()
    cache.set(f"{email}_otp", otp_code, 10 * 60)

    sender = {"name": "MMC-Crop-Type", "email": "alerts@mapmycrop.com"}
    to = {"email": email, "name": "Customer"}
    subject = "Map My Crop OTP"
    html_content = f"<html><body><h3>Your MMC-Crop Type OTP verification code is {otp_code}</h3></body></html>"

    send_email(sender=sender, to=to, subject=subject, html_content=html_content)

    return True


def check_email_otp(email, code):
    """
    Check email verification with OTP code

    :param email: email number for OTP verification
    :param code: OTP code
    :return: True if it's successful, raise Exception if not
    """

    cache = get_redis()

    if code == cache.get(f"{email}_otp"):
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="OTP is not valid"
        )
