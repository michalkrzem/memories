from datetime import timedelta

from fastapi import HTTPException
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from sqlalchemy.orm import Session
from database import crud
from schemas import schema
from security.security_adm import get_current_active_user, USERS, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

# Dependency
from security import security_adm
from security.security_adm import create_access_token
from database.db_connection import get_db


app_users = FastAPI()


@app_users.post(
    "/login",
    tags=["TOKEN"],
    description="Generate token",
    deprecated=False,
    response_model=schema.Token,
    responses={
        405: {
            "model": schema.Message,
            "description": "Method Not Allowed"
        }
    }
)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.get_user_via_email(form_data.username, db)
    print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not security_adm.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"user": user.email, "access_token": access_token, "token_type": "bearer"}


@app_users.get(
    "/me",
    tags=["users"],
    response_model=schema.UserEmailOut
)
async def read_user_me(
        db: Session = Depends(get_db),
        current_user: schema.UserAuth = Depends(get_current_active_user)

):
    user_via_email = crud.get_user_via_email(current_user.username, db)

    return user_via_email

