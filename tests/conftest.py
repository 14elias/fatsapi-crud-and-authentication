import pytest
import jwt
from sqlmodel import SQLModel,create_engine,Session
from fastapi.testclient import TestClient
from src import app
from src.config import setting
from src.book.data import get_session
from src.auth.utility import create_access_token,get_user_by_username
from src.config import setting



@pytest.fixture(name='session')
def session_fixture():
    DATABASE_URL = (
    f"mysql+pymysql://{setting.database_username}:"
    f"{setting.database_password}@{setting.database_host}:"
    f"{setting.database_port}/{setting.database_name}_test"
) 
    engine = create_engine(DATABASE_URL, echo=False)

    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client(session:Session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture(name="test_user")
def create_test_user(client):
    user ={
        "username": "nebyat",
        "password": "nb123",
        "email": "nb@gmail.com",
        "full_name": "nbm"
    }
    res = client.post('api/v1/users/register-user',json=user)

    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user["password"]
    return new_user


# @pytest.fixture(name="token")
# def token(client,test_user):
#     res = client.post(
#         'api/v1/users/token',
#         data={"username":test_user['username'],"password":test_user['password']}
#     )

#     assert res.status_code==200
#     print(res.json().get('access_token'))
#     return res.json().get('access_token')

@pytest.fixture(name="token")
def token(test_user):
    return create_access_token(data={"sub":test_user['username']})

# @pytest.fixture(name="current_user")
# def current_user(token,session,test_user):
#     payload = jwt.decode(token,setting.secret_key,algorithms=[setting.algorithm])
#     username=payload.get('sub')
#     user=get_user_by_username(username=username,session=session)

#     return user