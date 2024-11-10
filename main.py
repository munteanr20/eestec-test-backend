# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from task_routes import router as task_router
from user_routes import router as user_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(task_router)
app.include_router(user_router)
