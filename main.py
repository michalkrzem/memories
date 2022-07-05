from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from users import users
from schemas import schema
from admin import admin
from variables import responses


app = FastAPI()


app.mount('/users', users.app_users)
app.mount('/admin', admin.app_admin)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get(
    "/",
    tags=['Welcome'],
    description='This is app for my family',
    response_model=schema.Message,
    response_class=HTMLResponse
)
async def login(request: Request):

    return templates.TemplateResponse("login.html", {"request": request})
