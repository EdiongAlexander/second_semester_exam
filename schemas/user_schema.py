from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSchema(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True

class User(UserSchema):
    id: str

class CreateUser(UserSchema):
    pass

class UpdateUser(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None