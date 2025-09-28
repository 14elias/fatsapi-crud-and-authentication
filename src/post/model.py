from sqlmodel import SQLModel,Field
from datetime import datetime,timedelta


class Post(SQLModel,table=True):
    id:int=Field(primary_key=True,default=None)
    title:str
    created_at:datetime = Field(default=datetime.now())
    description:str