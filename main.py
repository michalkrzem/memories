from fastapi import FastAPI
from users import users
from schemas import schema
from admin import admin
from variables import responses


app = FastAPI()


app.mount('/users', users.app_users)
app.mount('/admin', admin.app_admin)


@app.get(
    "/",
    tags=['Welcome'],
    description='This is app with sdministration panel',
    response_model=schema.Message,
    responses=responses.errors
)
async def root():
    return {"detail": "Hello Admin!"}
