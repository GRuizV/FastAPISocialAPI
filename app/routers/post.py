
# 3RD PARTY IMPORTS
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session

# LOCAL IMPORTS
from app import schemas, models, oauth2
from app.database import get_db

# BUILT-IN IMPORTS
from typing import List, Optional




# Create a Router for the app
router = APIRouter(prefix="/posts", tags=["Post"])




# GET ALL POSTS
@router.get("/", response_model=List[schemas.PostVoteResponse])
def get_posts(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    # Posts query setting
    posts_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id)\
        .filter(models.Post.title.contains(search))\
        .limit(limit)\
        .offset(skip)
    
    # Execute the Posts query
    posts = posts_query.all()

    # Convert each SQLAlchemy model to a dictionary using Pydantic
    result = [{"Post": schemas.PostResponse.model_validate(post), "votes": votes} for post, votes in posts]
  
    # Return all posts found in the DB as a list of dicts
    return result

# CREATE ONE POST
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    
    # Create a new post with the passed info in the Endpoint according to the model defined for Posts
    new_post = models.Post(owner_id = current_user.id, **post.model_dump()) # The post unpacking (**) is doing the same as "title = post.title, content = post.content ..."

    # Add the newly created post to the DB
    db.add(new_post)

    # Commit the change to the DB
    db.commit()

    # Update the post how it was created in the DB
    db.refresh(new_post)

    # Return the newly created post back to the Client
    return new_post

# GET ONE POST BY ID
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostVoteResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    # Create the post query matching the id passed in the URL
    post_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id)\
        .filter(models.Post.id == id)

    # Get the post matched
    post = post_query.first()

    # Post look up guard (Actual query execution)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' was not found!")
    
    # Return the found post back to the Client
    return post

# DELETE ONE POST BY ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db),  current_user = Depends(oauth2.get_current_user)):

    # Create the post query matching the id passed in the URL
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    # Get the post matched
    post = post_query.first()

    # Post look up guard (Actual query execution)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' doesn't exist!")
    
    # Authentication guard (The owner of the post is the one deleting it)
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Unauthorized! Only the owner of the post can alter it!")
    
    # Execute the post query to delete it from the DB
    post_query.delete(synchronize_session = False)
    
    # Commit the change to the DB
    db.commit()

    return None # No response is necessary given the default status set in the decorator and we are not returning an entity in the response (There's not "response model" in the deco)

# UPDATE ONE POST BY ID
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),  current_user = Depends(oauth2.get_current_user)):
    
    # Create the post query matching the id passed in the URL
    post_query = db.query(models.Post).filter(models.Post.id == id)
   
    # Get the post matched
    updated_post = post_query.first()

    # Post look up guard (Actual query execution)
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' doesn't exist!")

    # Authentication guard (The owner of the post is the one deleting it)
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Unauthorized! Only the owner of the post can alter it!")
    
    # Execute the post query to update it in the DB
    post_query.update(post.model_dump(), synchronize_session = False)

    # Commit the change to the DB
    db.commit()

    # Return the updated found post back to the Client
    return updated_post
