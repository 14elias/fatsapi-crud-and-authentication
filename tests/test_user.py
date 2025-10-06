import pytest
import jwt
from src.auth.schema import UserOut,Token
from src.config import setting

def test_root(client):
    res=client.get('/')
    assert res.json() =={"message": "Hello from FastAPI on Render!"}
    assert res.status_code == 200


def test_user_register(client):
    res = client.post('api/v1/users/register-user',json={
        "username": "nebyat",
        "password": "nb123",
        "email": "nb@gmail.com",
        "full_name": "nbm"
    })

    new_user = UserOut(**res.json())
    assert new_user.username=="nebyat"
    assert new_user.email == "nb@gmail.com"
    assert res.status_code == 201


def test_user_register_duplicate(client,test_user):
    res = client.post('/api/v1/users/register-user', json=test_user)
    assert res.status_code == 409


def test_user_login(client,test_user):
    res = client.post(
        'api/v1/users/token',
        data={"username":test_user['username'],"password":test_user['password']}
    )
    res_login = Token(**res.json())
    payload = jwt.decode(res_login.access_token,setting.secret_key,algorithms=[setting.algorithm])
    assert payload.get('sub')==test_user['username']
    assert res_login.token_type == 'bearer'
    assert res.status_code == 200

@pytest.mark.parametrize("username,password,status_code",[
    ('nebyat','wrong',401),
    ('wrong','nb123',401),
    ('wrong','wrong',401),
    ('nebyat',None,401),
    (None,'nb123',401),
])
def test_incorrect_login(client,test_user,username,password,status_code):
    res = client.post(
        'api/v1/users/token',
        data={"username":username,"password":password}
    )

    assert res.status_code==status_code
    # assert res.json().get('detail')=="Incorrect username or password"


def test_user_login_dontexist(client):
    res = client.post('api/v1/users/token',data={"username":"ella","password":"el123"})
    assert res.status_code == 401