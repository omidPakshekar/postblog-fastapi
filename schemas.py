import pydantic
from datetime import datetime


class UserBase(pydantic.BaseModel):
    email: str 
    name: str




# reciveing data from api
class UserRequest(UserBase):
    password_hash: str

    # stop lazy load data
    class Config:
        orm_mode = True 

class UserResponse(UserBase):
    id: int 
    created_at: datetime

    # stop lazy load data
    class Config:
        orm_mode = True 



class PostBase(pydantic.BaseModel):
    post_title: str 
    post_description: str 
    post_image: str

class PostRequest(PostBase):
    pass 

class PostResponse(PostBase):
    id: int  
    user_id: int 
    created_at: datetime

    # stop lazy load data
    class Config:
        orm_mode = True 






