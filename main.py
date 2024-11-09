from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class Task(BaseModel):
    name: str
    description: str

tasks: List[Task] = []

# Create a task
@app.post("/tasks/")
async def create_task(task: Task):
    task_id = len(tasks) + 1  # Simple auto-increment ID (in production, use a database)
    task_with_id = task.dict()
    task_with_id['id'] = task_id
    tasks.append(task_with_id)
    return task_with_id

# Get all tasks
@app.get("/tasks/")
async def get_tasks():
    return tasks

# Get a specific task by index
@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task:
        return task
    return {"error": "Task not found"}

# Delete a task by id
@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task:
        tasks.remove(task)
        return {"message": "Task deleted successfully"}
    return {"error": "Task not found"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)