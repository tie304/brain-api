import os
import jwt
from fastapi import APIRouter, HTTPException, Depends
from jwt import PyJWTError
from models.user import TokenData
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta

AUTH_SECRET_KEY = os.environ.get("AUTH_SECRET_KEY")
AUTH_ALGORITHM = os.environ.get("AUTH_ALGORITHM")
AUTH_ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("AUTH_ACCESS_TOKEN_EXPIRE_MINUTES")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, AUTH_SECRET_KEY, algorithm=AUTH_ALGORITHM)
    return encoded_jwt


async def validate_current_user(token: str):

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, AUTH_SECRET_KEY, algorithms=[AUTH_ALGORITHM])
        username: str = payload.get("sub")
        token_data = TokenData(username=username)
        if username is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    return token_data.username

