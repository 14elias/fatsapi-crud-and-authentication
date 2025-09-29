# database.py
from sqlmodel import SQLModel, create_engine, Session
from ..config import setting


DATABASE_URL = (
    f"mysql+pymysql://{setting.database_username}:"
    f"{setting.database_password}@{setting.database_host}:"
    f"{setting.database_port}/{setting.database_name}"
) 

engine = create_engine(DATABASE_URL, echo=True)

# function to create tables
def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session