
# 3RD PARTY IMPORTS
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

# LOCAL IMPORTS
from app import schemas, models, oauth2
from app.database import get_db

# BUILT-IN IMPORTS
from typing import List




# Create a Router for the app
router = APIRouter(prefix="/posts", tags=["Post"])




# GET ALL POSTS
@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # Posts query setting
    posts_query = db.query(models.Post)
    
    # Posts query execution and storing into 'posts'
    posts = posts_query.all()

    # Return all posts found in the DB
    return posts

# CREATE ONE POST
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # Create a new post with the passed info in the Endpoint according to the model defined for Posts
    new_post = models.Post(**post.model_dump()) # The post unpacking (**) is doing the same as "title = post.title, content = post.content ..."

    # Add the newly created post to the DB
    db.add(new_post)

    # Commit the change to the DB
    db.commit()

    # Update the post how it was created in the DB
    db.refresh(new_post)

    # Return the newly created post back to the Client
    return new_post

# GET ONE POST BY ID
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # Create the post query matching the id passed in the URL
    post_query = db.query(models.Post).filter(models.Post.id == id)

    # Post look up guard (Actual query execution)
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' was not found!")
    
    # Store the executed post query in a variable
    post = post_query.first()

    # Return the found post back to the Client
    return post

# DELETE ONE POST BY ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):

    # Create the post query matching the id passed in the URL
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    # Post look up guard (Actual query execution)
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' doesn't exist!")
    
    # Execute the post query to delete it from the DB
    post_query.delete(synchronize_session = False)
    
    # Commit the change to the DB
    db.commit()

    return None # No response is necessary given the default status set in the decorator and we are not returning an entity in the response (There's not "response model" in the deco)

# UPDATE ONE POST BY ID
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):
    
    # Create the post query matching the id passed in the URL
    post_query = db.query(models.Post).filter(models.Post.id == id)
   
    # Post look up guard (Actual query execution)
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' doesn't exist!")

    # Execute the post query to update it in the DB
    post_query.update(post.model_dump(), synchronize_session = False)

    # Commit the change to the DB
    db.commit()

    # Store the executed queried post in a variable
    updated_post = post_query.first()

    # Return the updated found post back to the Client
    return updated_post
