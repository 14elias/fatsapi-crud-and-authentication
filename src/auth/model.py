from sqlmodel import SQLModel, Field,Relationship
from typing import Optional
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..post.model import Post


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str
    full_name: Optional[str] = None
    hashed_password: str
    disabled: bool = False
    role:str = Field(default='user')

    posts:list["Post"] = Relationship(back_populates='owner')
