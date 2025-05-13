from turtle import title
import pytest
from fastapi.testclient import TestClient
from app import models
from app.main import app
import pytest
from app.database import get_db, Base 
from tests.database import TestingSessionLocal, test_engine
from app.oauth2 import create_access_token


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user2(client):
    user_data = {
        "email": "testuser123@gmail.com",
        "password": "testPassword"
    }
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_user(client):
    user_data = {
        "email": "testuser@gmail.com",
        "password": "testPassword"
    }
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
        {
            "title": "First Post",
            "content": "First post content",
            "owner_id": test_user['id']
        },
        {
            "title": "Second Post",
            "content": "Second post content",
            "owner_id": test_user['id']
        },
        {
            "title": "Third Post",
            "content": "Third post content",
            "owner_id": test_user['id']
        },
        {
            "title": "Third Post",
            "content": "Third post content",
            "owner_id": test_user2['id']
        },
    ]

    # Create post models and add them to session
    posts = []
    for post_dict in posts_data:
        post = models.Post(**post_dict)
        session.add(post)
        posts.append(post)
    
    session.commit()

    return posts