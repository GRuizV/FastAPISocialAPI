
# 3RD PARTY IMPORTS
from pydantic import BaseModel, EmailStr


# LOCAL IMPORTS
...

# BUILT-IN IMPORTS
from datetime import datetime
from typing import Optional





# POST MODEL SCHEMAS
class PostBase(BaseModel):

    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):

    """
    We are leaving this schema as placeholder in case the creation of a new post requires
    something specific additional to the PostBase    
    """

    pass


class PostResponse(PostBase):

    id: int
    created_at: datetime

    # Pydantic setting to convert this class to a dict like response even when is not one
    class Config:
        from_attributes = True




# USER MODEL SCHEMAS
class UserBase(BaseModel):

    email: EmailStr
    password: str


class UserCreate(UserBase):
    
    """
    We are leaving this schema as placeholder in case the creation of a new user requires
    something specific additional to the UserBase    
    """

    pass

class UserResponse(BaseModel):

    id: int
    created_at: datetime

    # Pydantic setting to convert this class to a dict like response even when is not one
    class Config:
        from_attributes = True

#Schema to Validate Users when logging in
class UserLogin(UserBase):

    """
    We are leaving this schema as placeholder in case the login of a new user requires
    something specific additional to the UserBase    
    """

    pass




# TOKEN MODEL SCHEMA
class Token(BaseModel):

    access_token: str
    token_type: str

class TokenData(BaseModel):

    id: Optional[int] = None



