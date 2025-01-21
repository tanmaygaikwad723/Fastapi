from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass 


class PostResponse(PostBase):
    id: int
    created_at : datetime
    owner_id : int

    class Config:
        orm_mode = True
    

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: str
    id: int
    created_at : datetime

    class Config:
        orm_mode = True


class Userlogin(BaseModel):
    email = EmailStr
    password = str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class Token_data(BaseModel):
    id: Optional[str] = None