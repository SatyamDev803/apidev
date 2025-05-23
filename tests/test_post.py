from app import schemas
import pytest


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    
    # Validate response status and structure
    assert res.status_code == 200
    posts_data = res.json()
    assert len(posts_data) == len(test_posts)
    
    # Convert response data to Pydantic models for validation
    def validate(post):
        return schemas.PostOut(**post)
    posts_list = list(map(validate, posts_data))
    
    # Create a map of posts by ID for easier comparison
    test_posts_map = {post.id: post for post in test_posts}
    
    # Verify each returned post matches our test data
    for post in posts_list:
        test_post = test_posts_map[post.Post.id]
        assert post.Post.title == test_post.title
        assert post.Post.content == test_post.content
        assert post.Post.owner_id == test_post.owner_id
        assert isinstance(post.Votes, int)  # Verify votes count is present


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exists(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/5689")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content


@pytest.mark.parametrize("title, content, published", [
    ("New title", "New Content goes here", True),
    ("Favorite Meals", "Banana Smoothie and Panner", True),
    ("Favorite City", "Mumbai is my favorite city", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json={"title": "random title", "content": "random content"})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "random title"
    assert created_post.content == "random content"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']


def test_unauthorized_user_create_post(client, test_posts, test_user):
    res = client.post("/posts/", json={"title": "random title", "content": "random content"})

    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 204


def test_delete_post_not_exists(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/5689")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")

    assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
            "title": "Updates title",
            "content": "Updates post content",
            "id": test_posts[0].id
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json = data)

    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
            "title": "Updates title",
            "content": "Updates post content",
            "id": test_posts[3].id
    }

    res = authorized_client.put(f"/posts/{test_posts[3].id}", json = data)

    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401


def test_update_post_not_exists(authorized_client, test_posts, test_user):
    data = {
            "title": "Updates title",
            "content": "Updates post content",
            "id": test_posts[3].id
    }

    res = authorized_client.put(f"/posts/5689", json=data)
    assert res.status_code == 404