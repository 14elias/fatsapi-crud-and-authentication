from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserOut(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserRegistration(BaseModel):
    username: str 
    email: str
    full_name: Optional[str] = None
    password : str
   
class UserResponse(BaseModel):
    id: int
    username: str 
    email: str
    full_name: str|None
    disabled: bool 
