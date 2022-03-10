import datetime
from datetime import timedelta
from typing import List

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from starlette import status

from database.db_connection import SessionLocal
from sqlalchemy.orm import Session
from database import crud
from schemas import schema
from variables import responses


# Dependency
from security import security
from security.security import get_current_active_user, USERS, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


router = APIRouter()


@router.post(
    "/token",
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
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = security.authenticate_user(USERS, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized - Błąd logowania",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"user": user.username, "access_token": access_token, "token_type": "bearer"}


@router.get(
    "/admin/users",
    tags=["admin"],
    description='Get informations about all users',
    response_model=List[schema.UserOut],
    responses=responses.errors
)
async def read_users(
        db: Session = Depends(get_db),
        current_user: schema.UserAuth = Depends(get_current_active_user)
):

    users = crud.get_all(db)

    return users


@router.get(
    "/admin/user",
    tags=["admin"],
    description='Get information about user with email',
    response_model=schema.UserOut,
    responses=responses.errors
)
async def read_user(
        email: EmailStr,
        db: Session = Depends(get_db),
        current_user: schema.UserAuth = Depends(get_current_active_user)
):

    user_via_email = crud.get_usrer_via_email(email, db)

    return user_via_email


@router.get(
    "/admin/roles",
    tags=["admin"],
    description='Get information about all roles',
    response_model=List[schema.Role],
    responses=responses.errors
)
async def read_user(
        db: Session = Depends(get_db),
        current_user: schema.UserAuth = Depends(get_current_active_user)
):

    roles = crud.get_roles(db)

    return roles


@router.post(
    "/admin/role",
    tags=['admin'],
    description='Create new role',
    response_model=schema.Role,
    responses=responses.errors
)
async def create_role(
        role,
        db: Session = Depends(get_db),
        current_user: schema.UserAuth = Depends(get_current_active_user)
):

    new_role = role
    result = crud.create_role(new_role, db)

    return result


@router.patch(
    "/admin/user/privileges",
    tags=['admin'],
    description='Change user privileges',
    response_model=schema.UserEmailOut,
    responses=responses.errors
)
async def change_privileges(
        new_role: schema.NewPrivilegesIn,
        db: Session = Depends(get_db),
        current_user: schema.UserAuth = Depends(get_current_active_user)
):

    crud.get_usrer_via_email(new_role.email, db)
    crud.change_privileges(new_role, db)

    user_with_new_privileges = crud.get_usrer_via_email(new_role.email, db)

    return user_with_new_privileges


@router.delete(
    "/admin/user",
    tags=['admin'],
    description='Delete user',
    response_model=schema.Message,
    responses=responses.errors
)
def delete_user(
        email: EmailStr,
        db: Session = Depends(get_db),
        current_user: schema.UserAuth = Depends(get_current_active_user)
):

    crud.get_usrer_via_email(email, db)
    crud.delete_user(email, db)


@router.post(
    '/admin/user',
    tags=['admin'],
    description='Add new user to database',
    response_model=schema.UserOut,
    responses=responses.errors
)
def add_user(
        new_user: schema.User,
        db: Session = Depends(get_db),
        current_user: schema.UserAuth = Depends(get_current_active_user)
):
    new_user.created_on = datetime.datetime.now()
    user = crud.add_user(new_user, db)

    return user
