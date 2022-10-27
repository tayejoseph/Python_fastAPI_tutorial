
from datetime import datetime
from pydantic import BaseModel


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
class Post(PostBase):
    id: int
    created_at: datetime

    # this is from fastAPI Docs
    class Config:
        orm_mode = True