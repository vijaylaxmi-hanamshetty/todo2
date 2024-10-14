from pydantic import BaseModel
from typing import Optional

# Base class for user-related models
class UserBase(BaseModel):
    username: str

    class Config:
        from_attributes = True 


# Create user schema, extending from UserBase
class UserCreate(UserBase):
    email: str
    password: str

    class Config:
        from_attributes = True


# Schema for creating a new task
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


# Schema for reading task, extending from TaskCreate
class Task(TaskCreate):
    id: str
    owner_id: str 
    class Config:
        from_attributes = True


# Token response model
class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True
