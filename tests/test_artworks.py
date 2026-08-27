import pytest
from unittest.mock import patch

@pytest.mark.django_db
@patch('django.core.cache.cache.get')
def test_get_artworks_list(mock_cache_get, api_client):
    # Симулюємо порожній кеш Redis
    mock_cache_get.return_value = None

    response = api_client.get('/api/v1/artworks/')
    
    assert response.status_code == 200
    assert isinstance(response.data, list)