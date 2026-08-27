import pytest

from unittest.mock import patch

@pytest.mark.django_db
def test_user_registration(api_client, db_session):
    payload = {
        "email": "artist@example.com",
        "password": "strongpassword123",
        "fullName": "Тарас Шевченко",
        "role": "artist",
    }

    response = api_client.post(
        "/api/v1/auth/register",
        payload,
        format="json",
    )

    assert response.status_code == 201
    assert response.data["detail"] == "Успішно зареєстровано"


@pytest.mark.django_db
def test_user_login_sets_cookies(api_client):
    # Спочатку реєструємо
    register_payload = {
        "email": "user@example.com",
        "password": "password123",
        "fullName": "Іван Франко"
    }
    api_client.post('/api/v1/auth/register', register_payload, format='json')

    # Виконуємо вхід
    login_payload = {
        "email": "user@example.com",
        "password": "password123"
    }
    response = api_client.post('/api/v1/auth/login', login_payload, format='json')
    
    # Тепер повернеться 200 OK
    assert response.status_code == 200
    assert 'access_token' in response.cookies
    assert 'refresh_token' in response.cookies
    assert response.cookies['access_token']['httponly'] is True