from pydantic import BaseModel
from datetime import datetime


# Model Schema
class PostBase(BaseModel):

    title: str
    content: str
    published: bool = True




class PostCreate(PostBase):
    pass




class PostResponse(PostBase):

    id: int
    created_at: datetime

    # Pydantic setting to convert this class to a dict like response even when is not one
    class Config:
        orm_mode = True












