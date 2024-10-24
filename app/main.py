from fastapi import FastAPI
from fastapi.routing import APIRouter

from models.user import User
from models.task import Task

app = FastAPI()
api_router = APIRouter()


@app.get("/")
async def root():
    return {"message": "Welcome to Taskmanager"}


api_router.include_router(User.router)
api_router.include_router(Task.router)

app.include_router(api_router)
