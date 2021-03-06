import os
from dotenv import load_dotenv

import json
from typing import Optional
from datetime import datetime, timedelta

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError
from passlib.context import CryptContext
from schemas import schema

load_dotenv()

USERS = json.loads(os.getenv("USERS"))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme_admin = OAuth2PasswordBearer(tokenUrl="/admin/login")
oauth2_scheme_user = OAuth2PasswordBearer(tokenUrl="/users/login")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return schema.UserSec(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_admin(token: str = Depends(oauth2_scheme_admin)):
    credentials_exception = HTTPException(
        status_code=401,
        detail='Unauthorized',
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schema.TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user(USERS, username=token_data.username)

    if user is None:
        raise credentials_exception
    return user


async def get_current_user(token: str = Depends(oauth2_scheme_user)):
    print(token)
    credentials_exception = HTTPException(
        status_code=401,
        detail='Unauthorized',
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        print(schema.TokenData(username=email))
        return schema.TokenData(username=email)
    except JWTError:
        raise credentials_exception


async def get_current_active_admin(current_user: schema.UserAuth = Depends(get_current_admin)):

    if current_user.disabled:
        raise HTTPException(status_code=403, detail='Forbidden')
    return current_user


async def get_current_active_user(current_user: schema.UserAuth = Depends(get_current_user)):

    return current_user

#  to generate new password hash
# print(get_password_hash('F@ther'))
