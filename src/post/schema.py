from pydantic import BaseModel
from datetime import datetime
from ..auth.schema import UserOut

class CreatePost(BaseModel):
    title:str
    description:str


class PostOut(CreatePost):
    id:int
    title:str
    created_at:datetime 
    description:str
    owner:UserOut

    class config:
        from_orm=True

class PostOutVote(BaseModel):
    Post:PostOut
    likes:int



class Vote(BaseModel):
    post_id:int
    dir:int