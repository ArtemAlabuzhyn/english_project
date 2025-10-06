import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()
@pytest.fixture
def authorized_client(db):
    user = User.objects.create_user(
        username="Artem",
        password="21041992",
    )
    client = APIClient()
    response = client.post("/api/drf/login/", {
        "username": "Artem",
        "password": "21041992"
    })
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return client, user

@pytest.fixture
def create_user(db):
    return User.objects.create_user('user1', password='pass123')
