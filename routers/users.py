from fastapi import APIRouter, status
from schemas.user_schema import CreateUser, UpdateUser
from services import user_service

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def get_users():
    return user_service.get_users()


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: str):
    user = user_service.get_user_by_id(user_id)
    return user


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user_in: CreateUser):
    user = user_service.create_user(user_in)
    return {"message": "User created successfully", "user": user}


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id: str, user_in: UpdateUser):
    user = user_service.update_user(user_id, user_in)
    return {"message": "User updated successfully", "user": user}


@router.put("/{user_id}/deactivate", status_code=status.HTTP_200_OK)
def deactivate_user(user_id: str):
    user = user_service.deactivate_user(user_id)
    return {"message": "User deactivated successfully", "user": user}


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
    user_service.delete_user(user_id)
