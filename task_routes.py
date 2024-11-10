# task_routes.py
from fastapi import APIRouter, HTTPException
from models import Task
from database import get_tasks_reference, get_next_id

router = APIRouter()

@router.post("/tasks/")
async def create_task(task: Task):
    task_id = get_next_id("tasks")
    ref = get_tasks_reference().child(str(task_id))
    task_data = task.dict()
    task_data["id"] = task_id
    ref.set(task_data)
    return task_data

@router.get("/tasks/")
async def get_tasks():
    ref = get_tasks_reference()
    tasks = ref.get()
    return [{"id": int(key), **value} for key, value in tasks.items()] if tasks else []

@router.get("/tasks/{task_id}")
async def get_task(task_id: int):
    ref = get_tasks_reference().child(str(task_id))
    task = ref.get()
    if task:
        return {"id": task_id, **task}
    raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    ref = get_tasks_reference().child(str(task_id))
    if ref.get():
        ref.delete()
        return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")
