# models.py
from pydantic import BaseModel, EmailStr

class Task(BaseModel):
    id: int
    name: str
    description: str

class User(BaseModel):
    id: int
    email: EmailStr
    password: str
    isTeacher: bool
