# user_routes.py
from fastapi import APIRouter, HTTPException
from models import User
from database import get_users_reference, get_next_id
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/users/register/")
async def register_user(user: User):
    ref = get_users_reference()
    
    # Check if the email is already registered
    existing_user = ref.order_by_child("email").equal_to(user.email).get()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Generate a new numeric ID and hash the password
    user_id = get_next_id("users")
    user_data = user.dict()
    user_data["id"] = user_id
    user_data["password"] = hash_password(user.password)
    
    # Store user with the generated ID as the key
    ref.child(str(user_id)).set(user_data)
    return {"message": "User registered successfully"}

@router.post("/users/login/")
async def login_user(email: str, password: str):
    ref = get_users_reference()
    
    # Find user by email
    users = ref.order_by_child("email").equal_to(email).get()
    if not users:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    user_data = list(users.values())[0]
    if not verify_password(password, user_data["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    return {"message": "Login successful"}
