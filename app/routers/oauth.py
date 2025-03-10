from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from .. import schemas, database
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .. import models
from ..config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict):
    data_copy = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_copy.update({"exp": expire})
    token = jwt.encode(data_copy, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_access_token(token:str, credentails_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id:str = payload.get("user_id")
        if id is None:
            raise credentails_exception
        token_data = schemas.Token_data(id=id)
    except JWTError:
        raise credentails_exception
    return token_data
    

def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentails",
                                          headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentails_exception=credentials_exception)
    user = db.query(models.User).filter(models.User.id==token.id).first()
    return user
    