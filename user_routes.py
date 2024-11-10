# user_routes.py
from fastapi import APIRouter, HTTPException
from models import User
from database import get_users_reference, get_next_id
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

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
    return user_data

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    ref = get_users_reference().child(str(user_id))
    user = ref.get()
    if user:
        return {"id": user_id, **user}
    raise HTTPException(status_code=404, detail="User not found")
