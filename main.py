from fastapi import FastAPI, status, HTTPException, Response
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randint

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {"title": "post 1's title", "content": "post 1's content", "id":1},
    {"title": "favorite foods", "content": "I like pizza", "id":2}
]



def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i





@app.get("/")
def root():
    return {"message": "World"}




@app.get("/posts")
def get_posts():
    print(my_posts)
    return {"data":my_posts}




@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    
    print(new_post)
    post_dict = new_post.model_dump()
    post_dict['id'] = randint(1,100000)

    my_posts.append(post_dict)

    return {"data": post_dict}




@app.get("/posts/{id}")
def get_post(id: int):

    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' was not found!")
    
    return {"post_detail":post}




@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):

    index = find_index_post(id)

    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' doesn't exist!")
    
    my_posts.pop(index)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)




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


