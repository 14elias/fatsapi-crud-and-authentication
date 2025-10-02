
from sqlmodel import SQLModel, Field

class Book(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title : str
    published_date : str
    author : str
    pagenumber:int

class BookCreate(SQLModel):
    title : str
    published_date : str
    author : str
