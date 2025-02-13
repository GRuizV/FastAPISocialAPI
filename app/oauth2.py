
# 3RD PARTY IMPORTS
from jose import JWTError, jwt

# LOCAL IMPORTS
from datetime import datetime, timedelta
from decouple import config

# BUILT-IN IMPORTS
...



# Constants definition
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKE_EXPIRE_MINUTES = 30




# Token creation function
def create_access_token(data: dict):

    # Create a copy of the actual passed data
    to_encode = data.copy()

    # Set an expiration date (in minutes) when authenticated
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKE_EXPIRE_MINUTES)

    # Update the 'exp' field in the data to be encoded
    to_encode["exp"] = expire

    # Encode the data into the JWT
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    # Return the encoded JWT
    return encoded_jwt


