import pytest
from src.post.model import Post
from src.post.schema import PostOut

@pytest.fixture(name="create_post")
def create_post(test_user,session):
    post=Post(
        title="new_post",
        description="this is new post",
        owner_id=test_user['id']
    )

    session.add(post)
    session.commit()

    return post



def test_posts(client,token,create_post):
    response = client.get("/get_posts", headers={"Authorization": f"Bearer {token}"})

    print(response.json())
    assert response.status_code==200



def test_create_post(client,token):
    post = {"title":"vikings history", "description":"the most underarted movie"}
    response = client.post("/create_post", json=post, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json().get("title") == "vikings history"



@pytest.mark.parametrize("title,description,status_code", [
    (None,"the most underarted movie",422),
    (None,None,422),
    ("viking history",None,422)
])
def test_incorrect_create_post(client,token,title,description,status_code):
    post = {"title":title, "description":description}
    response = client.post("/create_post", json=post, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status_code




def test_unauthorized_create_post(client):
    post = {"title":"this is false", "description":"yhea it is false"}
    response = client.post("/create_post", json=post, headers={"Authorization": f"Bearer token"})

    assert response.status_code == 401




def test_get_a_post(client,token,create_post):
    response = client.get('/get_a_post/1', headers={"Authorization":f"Bearer {token}"})

    post = PostOut(**response.json())
    print(post)

    assert response.status_code == 200
    assert post.Post.title == create_post.title

