from fastapi import HTTPException
from second_semester_exam.schemas.user_schema import User, CreateUser, UpdateUser
from second_semester_exam.database import users
from uuid import uuid4


def find_user_by_id(user_id: str):
    for user in users:
        if user.id == user_id:
            return user
    return None


def get_users():
    return users


def get_user_by_id(user_id: str):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


def create_user(user_in: CreateUser):
    for u in users:
        if u.email == user_in.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    user = User(id=str(uuid4()), **user_in.dict())
    users.append(user)
    return user


def update_user(user_id: str, user_in: UpdateUser):
    user = find_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_in.username is not None:
        user.username = user_in.username
    if user_in.email is not None:
        user.email = user_in.email
    if user_in.is_active is not None:
        user.is_active = user_in.is_active
    return user


def deactivate_user(user_id: str):
    user = find_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    return user


def delete_user(user_id: str):
    user = find_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    users.remove(user)
