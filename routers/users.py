from fastapi import APIRouter, HTTPException, status
from second_semester_exam.schemas.user_schema import User, CreateUser, UpdateUser
from second_semester_exam.database import users
from uuid import uuid4

router = APIRouter()

def find_user_by_id(user_id: str):
    for user in users:
        if user.id == user_id:
            return user
        return None

@router.get("/", status_code=status.HTTP_200_OK)
def get_users():
    return users

@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: str):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user_in: CreateUser):
    for u in users:
        if u.email == user_in.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    user = User(id=str(uuid4()), **user_in.dict())
    users.append(user)
    return {"message": "User created successfully", "user": user}

@router.put("/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id: str, user_in: UpdateUser):
    user = find_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
     # Only update the fields that were provided
    if user_in.username is not None:
        user.username = user_in.username
    if user_in.email is not None:
        user.email = user_in.email
    if user_in.is_active is not None:
        user.is_active = user_in.is_active
    return {"message": "User updated successfully", "user": user}

@router.put("/{user_id}/deactivate", status_code=status.HTTP_200_OK)
def deactivate_user(user_id: str):
    user = find_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    return {"message": "User deactivated successfully", "user": user}

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: str):
    user = find_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    users.remove(user)
    return {"message": "User deleted successfully"}