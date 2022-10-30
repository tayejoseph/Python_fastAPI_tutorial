
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    # we added a default value here i.e if the user did not add any boolean value
    published: bool = True

# this inherit postBase
class PostCreate(PostBase):
    pass

# response schema
# note this also inherits from postBase class




class UserCreate(BaseModel):
    email: EmailStr
    password: str

# user response schema
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    # this returns the user data based on the relationship we have created in the post model
    owner: UserOut

    # this is from fastAPI Docs
    class Config:
        orm_mode = True
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None