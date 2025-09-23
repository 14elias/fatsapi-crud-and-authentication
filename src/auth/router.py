from fastapi import Session, Fastapi, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .utility import get_user_by_username, get_password_hash
from sqlmodel import create_engine,SQLModel
from .model import User
from typing import Annotated
from src.book.data import get_session

data_router = APIRouter()

@data_router.on_event("startup")
def on_startup():
    engine = create_engine("sqlite:///./test.db", echo=True)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        if not get_user_by_username("johndoe", session):
            new_user = User(
                username="johndoe",
                email="johndoe@example.com",
                full_name="John Doe",
                hashed_password=get_password_hash("secret"),  # password = "secret"
                disabled=False,
            )
            session.add(new_user)
            session.commit()



    