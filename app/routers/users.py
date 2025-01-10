from typing import Optional, List
from fastapi import  status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from ..schemas import UserCreate, UserResponse
from .. import models
from ..database import engine, get_db
from sqlalchemy.orm import Session
from ..utils import hash

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/",  status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user:UserCreate, db:Session=Depends(get_db)):
    user.password = hash(user.password)
    new_user = models.User(**dict(user))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=UserResponse)
def get_user(id:int, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} does not exist")
    return user