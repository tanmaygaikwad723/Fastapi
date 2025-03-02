from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from ..schemas import PostCreate, PostResponse
from .. import models
from ..database import get_db
from sqlalchemy.orm import Session
from ..utils import hash
from . import oauth

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/", response_model=List[PostResponse])
def get_posts(db:Session = Depends(get_db), limit:int = 10, skip:int=0, search:Optional[str]=""):
    print(search)
    post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(data: PostCreate, db:Session = Depends(get_db), 
                current_user: int = Depends(oauth.get_current_user)):
    print(current_user.id)
    new_post = models.Post(owner_id=current_user.id, **dict(data))
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=PostResponse)
def get_post(id:int, response:Response, db:Session = Depends(get_db),
            current_user: int = Depends(oauth.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorised to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit() 
    return Response(status_code=status.HTTP_204_NO_CONTENT)
        

@router.put("/{id}", response_model=PostResponse)
def update_post(id:int, data:PostCreate, db:Session = Depends(get_db),
                current_user: int = Depends(oauth.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorised to perform requested action")
    post_query.update(dict(data), synchronize_session=False)
    db.commit()
    return post_query.first()