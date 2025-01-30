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




# Dummy DB for Testing
my_posts = [
    {"title": "post 1's title", "content": "post 1's content", "id":1},
    {"title": "favorite foods", "content": "I like pizza", "id":2}
]




# Utils Definition
def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i




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
def create_posts(new_post: Post):
    
    print(new_post)
    post_dict = new_post.model_dump()
    post_dict['id'] = randint(1,100000)

    my_posts.append(post_dict)

    return {"data": post_dict}


# GET ONE POST BY ID
@app.get("/posts/{id}")
def get_post(id: int):

    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' was not found!")
    
    return {"post_detail":post}


# DELETE ONE POST BY ID
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):

    index = find_index_post(id)

    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' doesn't exist!")
    
    my_posts.pop(index)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# UPDATE ONE POST BY ID
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    
    print(post)

    index = find_index_post(id)

    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' doesn't exist!")
    
    updated_post = post.model_dump()
    updated_post['id'] = id
    my_posts[index] = updated_post

    return {"data":updated_post}


