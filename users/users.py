from typing import List

from fastapi import APIRouter
from fastapi import FastAPI, Depends
from database.db_connection import SessionLocal
from sqlalchemy.orm import Session
from database import crud
from schemas import schema


# Dependency
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


router = APIRouter()


@router.get(
    "/users/me",
    tags=["users"]
)
async def read_user_me(db: Session = Depends(get_db)):

    return {'result': 'res'}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}