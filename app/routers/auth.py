
# 3RD PARTY IMPORTS
from fastapi import APIRouter, status, HTTPException, Depends, Response
from sqlalchemy.orm import Session

# LOCAL IMPORTS
from app import schemas, utils, models
from app.database import get_db


# BUILT-IN IMPORTS
from typing import List




# Create a Router for the app
router = APIRouter(tags=["Authentication"])




# LOGIN PATH OP
@router.post('/login', status_code=status.HTTP_202_ACCEPTED)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    
    # # Hash the user attempted password
    # hashed_password = utils.hash(user_credentials.password)
    # user_credentials.password = hashed_password # Update the user credentials provided

    # Build the DB query
    user_query = db.query(models.User).filter(models.User.email == user_credentials.email)

    # User existence validation query execution guard
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The user with email '{user_credentials.email}' was not found!") 

    # Get the actual authorized user
    user = user_query.first()

    # Password validation guard
    if not utils.compare_pwds(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials!") 
    
    # Created token
    # Return the token

    return {"message": f"Welcome, {user_credentials.email}. You have successfully logged in!"}

















