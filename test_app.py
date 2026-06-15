import pytest
from app import app, calculate_distance, parse_point

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_calculate_distance():
    assert calculate_distance((2, 5), (1, 6)) == pytest.approx(1.414, 0.01)

def test_parse_point():
    assert parse_point("2,5") == (2, 5)

def test_html_get(client):
    response = client.get('/')
    assert response.status_code == 200

def test_html_post_valid(client):
    response = client.post('/', data={'apoint': '2,5', 'bpoint': '1,6'})
    assert response.status_code == 200

def test_html_post_invalid(client):
    response = client.post('/', data={'apoint': 'a,b', 'bpoint': '1,6'})
    assert response.status_code == 200
    assert b"error" in response.data

def test_api_get_distances(client):
    response = client.get('/api/distances')
    assert response.status_code == 200

def test_api_post_valid(client):
    response = client.post('/api/distance', json={'start_point': '2,5', 'end_point': '1,6'})
    assert response.status_code == 200

def test_api_post_invalid(client):
    response = client.post('/api/distance', json={'start_point': 'a,b', 'end_point': '1,6'})
    assert response.status_code == 400

def test_api_post_missing(client):
    response = client.post('/api/distance', json={'start_point': '2,5'})
    assert response.status_code == 400