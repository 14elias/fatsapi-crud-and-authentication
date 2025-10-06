import pytest
from src.post.model import Post

@pytest.fixture(name="create_post")
def test_create_post(test_user,session):
    post=Post(
        title="new_post",
        description="this is new post",
        owner_id=test_user['id']
    )

    session.add(post)
    session.commit()


def test_posts(client,token,create_post):
    response = client.get("/get_posts", headers={"Authorization": f"Bearer {token}"})

    print(response.json())
    assert response.status_code==200

