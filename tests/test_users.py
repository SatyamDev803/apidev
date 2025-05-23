from app import schemas
import jwt
from app.config import settings
import pytest


def test_create_user(client):
    res = client.post("/users/", json={
        "email": "velocity@gmail.com",
        "password": "vel123" 
    })

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "velocity@gmail.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post("/login", data={
        "username": test_user['email'],
        "password": test_user['password'] 
    })

    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert int(id) == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize(
    "email, password, expected_status", 
    [
        ('wrongemail@gmail.com', 'password123', 403),
        ('satyam@gmail.com', 'wrongpassword', 403),
        ('wrongemail@gmail.com', 'wrongpassword', 403),
        (None, 'password123', 422), 
        ('satyam@gmail.com', None, 422)
    ]
)
def test_incorrect_login(test_user, client, email, password, expected_status):
    res = client.post("/login", data={
    "username": email,
    "password": password
    })

    assert res.status_code == expected_status

