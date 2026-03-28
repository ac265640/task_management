from fastapi import APIRouter
from src.tasks import controller

task_routes=APIRouter(prefix="/tasks")

@task_routes.post("/create")
def create_tasks():
    return controller.create_task()