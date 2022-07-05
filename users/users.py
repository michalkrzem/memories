from datetime import timedelta
from typing import List

from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from schemas.schema import UserTokenAuth
from users import crud
from schemas import schema
from security.security import get_current_active_user, USERS, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

# Dependency
from security import security
from security.security import create_access_token
from database.db_connection import get_db


app_users = FastAPI()
templates = Jinja2Templates(directory="templates")

origins = [
    "http://localhost",
    "http://localhost:8000"
    "http://localhost:8080",
]

app_users.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app_users.get(
    "/",
    tags=['USERS'],
    description='This is app for my family',
    response_model=schema.Message,
    response_class=HTMLResponse
)
async def login(
        request: Request,
        db: Session = Depends(get_db),
        current_user: schema.UserAuth = Depends(get_current_active_user)
):

    return templates.TemplateResponse("users.html", {"request": request})


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
async def login_for_access_token(
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
):

    user = crud.get_user_via_email(form_data.username, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not security.verify_password(form_data.password, user.password):
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
    tags=["USERS"],
    response_model=schema.UserProfileOut
)
async def read_user_me(
        db: Session = Depends(get_db),
        current_user: schema.UserAuth = Depends(get_current_active_user)
):
    user_via_email = crud.get_user_via_email(current_user.username, db)

    return user_via_email


@app_users.patch(
    "/me/password",
    tags=['USERS'],
    response_model=schema.UserProfileOut,
)
async def change_password(
        passwords: schema.NewPasswordIn,
        db: Session = Depends(get_db),
        current_user: schema.UserAuth = Depends(get_current_active_user)
):
    db_password_hash = crud.get_user_via_email(current_user.username, db).password
    correct_old_password = security.verify_password(passwords.old_password, db_password_hash)
    correct_new_password = (passwords.new_password == passwords.new_password_repeat)
    new_password_hash = security.get_password_hash(passwords.new_password)

    if correct_new_password and correct_old_password:
        crud.change_password(new_password_hash, current_user.username, db)

    user_with_new_password = crud.get_user_via_email(current_user.username, db)

    return user_with_new_password


@app_users.get(
    '/me/tags',
    tags=['USERS'],
    response_model=List[schema.TagOut]
)
async def get_tags_for_me(
    db: Session = Depends(get_db),
    current_user: schema.UserAuth = Depends(get_current_active_user)
):
    tags = crud.get_tags_for_me(current_user.username, db)

    return tags


@app_users.post(
    '/me/tag',
    tags=['USERS'],
    response_model=schema.Tag
)
async def create_new_tag(
        new_tag: str,
        db: Session = Depends(get_db),
        current_user: schema.UserAuth = Depends(get_current_active_user)
):

    tag = crud.create_new_tag(new_tag, current_user.username, db)

    return tag


@app_users.post(
    '/me/post',
    tags=['USERS'],
    response_model=schema.PostInOut
)
def create_post(
        new_post: schema.PostIn,
        db: Session = Depends(get_db),
        current_user: schema.UserAuth = Depends(get_current_active_user)
):

    post = crud.create_new_post(new_post, db, current_user.username)

    return post


@app_users.get(
    '/me/posts',
    tags=["USERS"],
    response_model=List[schema.PostOut]
)
def get_all_my_posts(
        db: Session = Depends(get_db),
        current_user: schema.UserAuth = Depends(get_current_active_user)
):

    posts = crud.get_posts(current_user.username, db)

    return posts


@app_users.get(
    '/me/tag/posts',
    tags=["USERS"],
    response_model=List[schema.PostOut]
)
def get_my_posts_by_tag(
        tag_id: int,
        db: Session = Depends(get_db),
        current_user: schema.UserAuth = Depends(get_current_active_user)
):

    posts_by_tag = crud.get_posts_by_tag(current_user.username, tag_id, db)

    return posts_by_tag
