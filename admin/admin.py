from datetime import timedelta
from typing import List

from fastapi import HTTPException, FastAPI
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from starlette import status

from sqlalchemy.orm import Session
from database import crud
from schemas import schema
from variables import responses


# Dependency
from security import security
from security.security import get_current_active_admin, USERS, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from database.db_connection import get_db


app_admin = FastAPI()


@app_admin.post(
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
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):

    """TODO: change security na security_users and create new security for admin"""

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


@app_admin.get(
    "/users",
    tags=["admin"],
    description='Get information about all users',
    response_model=List[schema.UserOut],
    responses=responses.errors
)
async def read_users(
        db: Session = Depends(get_db),
        current_user: schema.UserAuth = Depends(get_current_active_admin)
):

    users = crud.get_all(db)

    return users


@app_admin.get(
    "/user",
    tags=["admin"],
    description='Get information about user with email',
    response_model=schema.UserProfileOut,
    responses=responses.errors
)
async def read_user(
        email: EmailStr,
        db: Session = Depends(get_db),
        current_user: schema.UserAuth = Depends(get_current_active_admin)
):

    user_via_email = crud.get_user_via_email(email, db)

    return user_via_email


@app_admin.get(
    "/roles",
    tags=["admin"],
    description='Get information about all roles',
    response_model=List[schema.Role],
    responses=responses.errors
)
async def read_roles(
        db: Session = Depends(get_db),
        current_user: schema.UserAuth = Depends(get_current_active_admin)
):

    roles = crud.get_roles(db)

    return roles


@app_admin.post(
    "/role",
    tags=['admin'],
    description='Create new role',
    response_model=schema.Role,
    responses=responses.errors
)
async def create_role(
        role,
        db: Session = Depends(get_db),
        current_user: schema.UserAuth = Depends(get_current_active_admin)
):

    new_role = role
    result = crud.create_role(new_role, db)

    return result


@app_admin.patch(
    "/user/privileges",
    tags=['admin'],
    description='Change user privileges',
    response_model=schema.UserProfileOut,
    responses=responses.errors
)
async def change_privileges(
        new_role: schema.NewPrivilegesIn,
        db: Session = Depends(get_db),
        current_user: schema.UserAuth = Depends(get_current_active_admin)
):

    crud.get_user_via_email(new_role.email, db)
    crud.change_privileges(new_role, db)

    user_with_new_privileges = crud.get_user_via_email(new_role.email, db)

    return user_with_new_privileges


@app_admin.delete(
    "/user",
    tags=['admin'],
    description='Delete user',
    response_model=schema.Message,
    responses=responses.errors
)
def delete_user(
        email: EmailStr,
        db: Session = Depends(get_db),
        current_user: schema.UserAuth = Depends(get_current_active_admin)
):

    crud.get_user_via_email(email, db)
    crud.delete_user(email, db)


@app_admin.post(
    '/user',
    tags=['admin'],
    description='Add new user to database',
    response_model=schema.UserOut,
    responses=responses.errors
)
def add_user(
        new_user: schema.UserIn,
        db: Session = Depends(get_db),
        current_user: schema.UserAuth = Depends(get_current_active_admin)
):

    new_user.password = security.get_password_hash(new_user.password)
    user = crud.add_user(new_user, db)

    return user
