
# 3RD PARTY IMPORTS
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

# LOCAL IMPORTS
from . import models
from .database import engine, get_db

# BUILT-IN IMPORTS
import time
import logging
from decouple import config



# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



# Sentence to Create all tables in the database
models.Base.metadata.create_all(bind=engine)


# Initialize the server app
app = FastAPI()




# Model Schema
class Post(BaseModel):
    title: str
    content: str
    published: bool = True




# Constants Settings
DB_USER = config('DB_USER')
DB_NAME = config('DB_NAME')
DB_PASS = config('DB_PASS')



# Establishing the DBs Connection
while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database=f"{DB_NAME}",
            user=f"{DB_USER}",
            password=f"{DB_PASS}",
            cursor_factory=RealDictCursor,
            )
        
        cursor = conn.cursor()

        print('Database connection was successful!')
        break

    except Exception as e:
        print("Connecting to database failed")
        print(f"Error: {e}")
        time.sleep(2)







# PATH OPERATIONS / ENDPOINTS DEFINITION

# ROOT DIRECTORY
@app.get("/")
def root():
    return {"message": "World"}


# GET ALL POSTS
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()

    return {"data":posts}


# CREATE ONE POST
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    
    # The post unpacking (**) is doing the same as "title = post.title, content = post.content ..."
    new_post = models.Post(**post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data":new_post}


# GET ONE POST BY ID
@app.get("/posts/{id}", status_code=status.HTTP_201_CREATED)
def get_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' was not found!")
    
    return {"post_detail":post}


# DELETE ONE POST BY ID
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)
    
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' doesn't exist!")
    
    post.delete(synchronize_session = False)
    db.commit()

    return None # No response is necessary given the default status set in the decorator


# UPDATE ONE POST BY ID
@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    old_post = post_query.first()

    if not old_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' doesn't exist!")

    post_query.update(post.model_dump(), synchronize_session = False)

    db.commit()

    return {"data":post_query.first()}


