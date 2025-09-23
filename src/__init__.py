from fastapi import FastAPI, Depends, APIRouter
from src.book.route import book_router
from src.book.data import init_db
from src.book.schema import Book
from src.auth.utility import user_router


from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.auth.utility import get_user_by_username, get_password_hash
from sqlmodel import create_engine,SQLModel,Session
from src.auth.model import User
from typing import Annotated
from src.book.data import get_session

version = 'v1'

app = FastAPI(
    version = version
)



@app.on_event("startup")
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




app.include_router(book_router, prefix=f'/api/{version}/books')
app.include_router(user_router, prefix=f'/api/{version}/users')


init_db()