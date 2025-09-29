from sqlmodel import SQLModel,Field,Relationship
from datetime import datetime,timedelta
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..auth.model import User




class Post(SQLModel,table=True):
    id:int=Field(primary_key=True,default=None)
    title:str
    created_at:datetime = Field(default=datetime.now())
    description:str
    owner_id:int =Field(foreign_key="user.id",ondelete="CASCADE")

    owner:Optional["User"]=Relationship(back_populates='posts')