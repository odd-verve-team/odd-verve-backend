import pytest

def test_anonymous_cart_add_item(api_client):
    payload = {
        "artworkId": "some-uuid-1234",
        "quantity": 1
    }
    response = api_client.post('/api/v1/cart/', payload, format='json')
    
    assert response.status_code == 201
    assert len(response.data['items']) > 0
    assert response.data['items'][0]['artworkId'] == "some-uuid-1234"