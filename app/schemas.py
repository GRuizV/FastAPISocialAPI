from pydantic import BaseModel, EmailStr
from datetime import datetime


# Post Model Schema
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




# User Model Schema
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
    email: EmailStr
    created_at: datetime

    # Pydantic setting to convert this class to a dict like response even when is not one
    class Config:
        from_attributes = True

class UserLogin(UserBase):

    """
    We are leaving this schema as placeholder in case the login of a new user requires
    something specific additional to the UserBase    
    """

    pass






