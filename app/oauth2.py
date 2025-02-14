
# 3RD PARTY IMPORTS
from jose import JWTError, jwt
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session


# LOCAL IMPORTS
from app import schemas, models
from app.database import get_db

# BUILT-IN IMPORTS
from datetime import datetime, timedelta, timezone
from decouple import config



# Constants & Variables Definition
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKE_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')




# Token creation function
def create_access_token(data: dict):

    # Create a copy of the actual passed data
    to_encode = data.copy()

    # Set an expiration date (in minutes) when authenticated
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKE_EXPIRE_MINUTES)

    # Update the 'exp' field in the data to be encoded
    to_encode["exp"] = expire

    # Encode the data into the JWT
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    # Return the encoded JWT
    return encoded_jwt


# Token validation function
def verify_access_token(token: str, credentials_exception):

    try: 

        # Decode the passed token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract the id value in the payload
        id = payload.get("user_id")

        # Payload validation guard
        if not id:
            raise credentials_exception
        
        # Token data validated
        token_data = schemas.TokenData(id=id)

    except JWTError as e:
        print(e)
        raise credentials_exception
    
    # Return the token data
    return token_data


# Actually User Authentication Function
def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    # Set the type of exception to be passed if the token validation fails
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail=f"Could not validate credentials",
                                            headers={'WWW-Authenticate': "Bearer"} )
    
    # Store the response of the token verification
    validated_token = verify_access_token(token=token, credentials_exception=credentials_exception)

    # Call the actual user from the DB
    user = db.query(models.User).where(models.User.id == validated_token.id).first()

    # Return the actual authenticated User
    return user








































