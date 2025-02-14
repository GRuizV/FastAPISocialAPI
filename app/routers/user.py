
# 3RD PARTY IMPORTS
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

# LOCAL IMPORTS
from app import schemas, models, utils
from app.database import get_db

# BUILT-IN IMPORTS
from typing import List




# Create a Router for the app
router = APIRouter(prefix="/users", tags=["Users"])




# GET ALL USERS
@router.get("/", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):

    # Users query setting
    users_query = db.query(models.User)

    # Users query executing
    users = users_query.all()

    # Return all users found in the DB
    return users

# CREATE ONE USER
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # Hash the password passed by the Client
    hashed_password = utils.hash(user.password)

    # Update the password hashed
    user.password = hashed_password

    # Create a new user with the passed info in the Endpoint according to the model defined for Users
    new_user = models.User(**user.model_dump()) # The post unpacking (**) is doing the same as "title = post.title, content = post.content ...

    # Add the newly created user to the DB
    db.add(new_user)

    # Commit the change to the DB
    db.commit()

    # Update the user how it was created in the DB
    db.refresh(new_user)

    # Return the newly created user back to the Client
    return new_user

# GET ONE USER BY ID
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):

    # Create the user query matching the id passed in the URL
    user_query = db.query(models.User).filter(models.User.id == id)

    # User look up guard (Actual query execution)
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id '{id}' was not found!")
    
    # Store the executed user query in a variable
    user = user_query.first()

    # Return the found user back to the Client
    return user

# DELETE ONE USER BY ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):

    # Create the user query matching the id passed in the URL
    user_query = db.query(models.User).filter(models.User.id == id)
    
    # User look up guard (Actual query execution)
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id '{id}' doesn't exist!")
    
    # Execute the user query to delete it from the DB
    user_query.delete(synchronize_session = False)

    # Commit the change to the DB
    db.commit()

    return None # No response is necessary given the default status set in the decorator and we are not returning an entity in the response (There's not "response model" in the deco)

# UPDATE ONE USER BY ID
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
def update_user(id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # Hash the password passed by the Client
    hashed_password = utils.hash(user.password)

    # Update the password hashed
    user.password = hashed_password

    # Create the user query matching the id passed in the URL
    user_query = db.query(models.User).filter(models.User.id == id)
   
    # User look up guard (Actual query execution)
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id '{id}' doesn't exist!")

    # Execute the user query to update it in the DB
    user_query.update(user.model_dump(), synchronize_session = False)

    # Commit the change to the DB
    db.commit()

    # Store the executed queried user in a variable
    updated_user = user_query.first()

    # Return the updated found user back to the Client
    return updated_user
































