import json

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
        "password": "Artem123"
    })
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return client

@pytest.fixture
def create_user(db):
    return User.objects.create_user('user1', password='pass123')

@pytest.mark.django_db
def test_register_user(authorized_client):
    data = {
        "username": "testtest",
        "password1": "testpassword123",
        "password2": "testpassword123",
        "first_name": "test",
        "last_name": "test",
        "email": "testuser@gmail.com"
    }

    response = authorized_client.post('/api/drf/register/', data)
    assert response.status_code == 201

@pytest.mark.django_db
def test_login_user(client, create_user):
    response = client.post('/api/drf/login/', {"username": "user1", "password": "pass123"})


