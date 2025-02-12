
# 3RD PARTY IMPORTS
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

# LOCAL IMPORTS
from app import schemas, models
from app.database import get_db

# BUILT-IN IMPORTS
from typing import List




# Create a Router for the app
router = APIRouter(prefix="/posts", tags=["Post"])




# GET ALL POSTS
@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):

    posts_query = db.query(models.Post)
    posts = posts_query.all()

    return posts

# CREATE ONE POST
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    
    # The post unpacking (**) is doing the same as "title = post.title, content = post.content ..."
    new_post = models.Post(**post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# GET ONE POST BY ID
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' was not found!")
    
    post = post_query.first()

    return post

# DELETE ONE POST BY ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' doesn't exist!")
    
    post_query.delete(synchronize_session = False)
    db.commit()

    return None # No response is necessary given the default status set in the decorator and we are not returning an entity in the response (There's not "response model" in the deco)

# UPDATE ONE POST BY ID
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
   
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' doesn't exist!")

    post_query.update(post.model_dump(), synchronize_session = False)

    db.commit()

    updated_post = post_query.first()

    return updated_post
