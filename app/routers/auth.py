
# 3RD PARTY IMPORTS
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# LOCAL IMPORTS
from app import schemas, utils, models, oauth2
from app.database import get_db


# BUILT-IN IMPORTS
...




# Create a Router for the app
router = APIRouter(tags=["Authentication"])




# LOGIN PATH OP
@router.post('/login', status_code=status.HTTP_202_ACCEPTED)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    # Build the DB query
    user_query = db.query(models.User).filter(models.User.email == user_credentials.username)

    # User existence validation query execution guard
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials!") 

    # Get the actual authorized user
    user = user_query.first()

    # Password validation guard
    if not utils.compare_pwds(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials!") 
    
    # Create the token
    access_token = oauth2.create_access_token(data= {"user_id": user.id})

    return {"token": access_token, "token_type": "bearer"}

















