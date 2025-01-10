from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import Userlogin, UserCreate
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models
from .. import utils
from . import oauth
from .. import schemas

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
def login(credentials:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.username).first()
    if not user:
        print("User not found")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify(credentials.password, user.password):
        print("Incorrect password")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    access_token = oauth.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
    