
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

    users_query = db.query(models.User)
    users = users_query.all()

    return users

# CREATE ONE USER
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # Password Hashing - user.password
    hashed_password = utils.hash(user.password)

    # Input hashed password updated
    user.password = hashed_password

    # The post unpacking (**) is doing the same as "title = post.title, content = post.content ..."
    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# GET ONE USER BY ID
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):

    user_query = db.query(models.User).filter(models.User.id == id)

    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id '{id}' was not found!")
    
    user = user_query.first()

    return user

# DELETE ONE USER BY ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):

    user_query = db.query(models.User).filter(models.User.id == id)
    
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id '{id}' doesn't exist!")
    
    user_query.delete(synchronize_session = False)
    db.commit()

    return None # No response is necessary given the default status set in the decorator and we are not returning an entity in the response (There's not "response model" in the deco)

# UPDATE ONE USER BY ID
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
def update_user(id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # Password Hashing - user.password
    hashed_password = utils.hash(user.password)   
    user.password = hashed_password # Input hashed password updated


    user_query = db.query(models.User).filter(models.User.id == id)
   
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id '{id}' doesn't exist!")

    user_query.update(user.model_dump(), synchronize_session = False)

    db.commit()

    updated_user = user_query.first()

    return updated_user
































