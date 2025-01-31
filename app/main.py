from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
from typing import Optional
from random import randint
import psycopg2
from psycopg2.extras import RealDictCursor
from decouple import config
import time



# Main app setting
app = FastAPI()




# Models Setting
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None




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
            cursor_factory=RealDictCursor
            )
        
        cursor = conn.cursor()

        print('Database connection was successful!')
        break

    except Exception as e:
        print("Connecting to database failed")
        print(f"Error: {e}")
        time.sleep(2)







# ENDPOINTS DEFINITION

# ROOT DIRECTORY
@app.get("/")
def root():
    return {"message": "World"}


# GET ALL POSTS
@app.get("/posts")
def get_posts():

    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()

    return {"data":posts}


# CREATE ONE POST
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    
    cursor.execute("""INSERT INTO posts (title, content, published) 
	    VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    
    new_post = cursor.fetchone()
    conn.commit()

    return {"data":new_post}


# GET ONE POST BY ID
@app.get("/posts/{id}")
def get_post(id: int):

    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    
    post = cursor.fetchone()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' was not found!")
    
    return {"post_detail":post}


# DELETE ONE POST BY ID
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):

    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    
    post = cursor.fetchone()
    conn.commit()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' doesn't exist!")
    
    return None # No response is necessary given the default status set in the decorator


# UPDATE ONE POST BY ID
@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, id))
    
    post = cursor.fetchone()
    conn.commit()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' doesn't exist!")

    return {"data":post}


