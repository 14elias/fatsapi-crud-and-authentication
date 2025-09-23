# database.py
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL =os.getenv("DATABASE_URL")  # change later to PostgreSQL if needed
engine = create_engine(DATABASE_URL, echo=True)

# function to create tables
def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session