# database.py
import firebase_admin
from firebase_admin import db, credentials

# Initialize Firebase with credentials
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://test-db-4d691-default-rtdb.europe-west1.firebasedatabase.app/"
})

# Reference to the tasks collection
def get_tasks_reference():
    return db.reference("/tasks")

# Reference to the users collection
def get_users_reference():
    return db.reference("/users")

# Retrieve and increment the next numeric ID
def get_next_id(reference_path: str) -> int:
    ref = db.reference(f"/{reference_path}_last_id")
    last_id = ref.get() or 0
    new_id = last_id + 1
    ref.set(new_id)
    return new_id
