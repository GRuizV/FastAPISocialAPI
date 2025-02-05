
# 3RD PARTY IMPORTS
from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy.orm import Session

# LOCAL IMPORTS
from . import schemas
from . import models
from .database import engine, get_db

# BUILT-IN IMPORTS
import logging
from typing import List



# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Sentence to Create all tables in the database
models.Base.metadata.create_all(bind=engine)


# Initialize the server app
app = FastAPI()




# PATH OPERATIONS / ENDPOINTS DEFINITION

# ROOT DIRECTORY
@app.get("/")
def root():
    return {"message": "World"}




"""POSTS PATH OPS"""

# GET ALL POSTS
@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):

    posts_query = db.query(models.Post)
    posts = posts_query.all()

    return posts

# CREATE ONE POST
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    
    # The post unpacking (**) is doing the same as "title = post.title, content = post.content ..."
    new_post = models.Post(**post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# GET ONE POST BY ID
@app.get("/posts/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' was not found!")
    
    post = post_query.first()

    return post

# DELETE ONE POST BY ID
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' doesn't exist!")
    
    post_query.delete(synchronize_session = False)
    db.commit()

    return None # No response is necessary given the default status set in the decorator and we are not returning an entity in the response (There's not "response model" in the deco)

# UPDATE ONE POST BY ID
@app.put("/posts/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
   
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' doesn't exist!")

    post_query.update(post.model_dump(), synchronize_session = False)

    db.commit()

    updated_post = post_query.first()

    return updated_post



"""USERS PATH OPS"""

# GET ALL USERS
@app.get("/users", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):

    users_query = db.query(models.User)
    users = users_query.all()

    return users

# CREATE ONE USER
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # The post unpacking (**) is doing the same as "title = post.title, content = post.content ..."
    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# GET ONE USER BY ID
@app.get("/users/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):

    user_query = db.query(models.User).filter(models.User.id == id)

    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id '{id}' was not found!")
    
    user = user_query.first()

    return user

# DELETE ONE USER BY ID
@app.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):

    user_query = db.query(models.User).filter(models.User.id == id)
    
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id '{id}' doesn't exist!")
    
    user_query.delete(synchronize_session = False)
    db.commit()

    return None # No response is necessary given the default status set in the decorator and we are not returning an entity in the response (There's not "response model" in the deco)

# UPDATE ONE USER BY ID
@app.put("/users/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
def update_user(id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    user_query = db.query(models.User).filter(models.User.id == id)
   
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id '{id}' doesn't exist!")

    user_query.update(user.model_dump(), synchronize_session = False)

    db.commit()

    updated_user = user_query.first()

    return updated_user



















