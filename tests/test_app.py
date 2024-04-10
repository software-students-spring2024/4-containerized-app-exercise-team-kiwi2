import pytest
from mongomock import MongoClient
from webApp.app import create_app

def test_sanity_check():
    expected = True  # the value we expect to be present
    actual = True  # the value we see in reality
    assert actual == expected, "Expected True to be equal to True!"

@pytest.fixture
def app():
    app = create_app(MongoClient().db.collection)
    app.config['TESTING'] = True

    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_ping(client):
    assert client.get('/').status_code == 200

def test_save_location(client):
    lat = 40
    long = -74

    response = client.post(
        '/save_location', json={"latitude": lat, "longitude": long}
    )
    assert response.status_code == 200

def test_get_user(client):
    lat = 40
    long = -74
    
    client.post(
        '/save_location', json={"latitude": lat, "longitude": long}
    )
    response = client.get('/get_user')
    assert response.status_code == 200

def test_get_user_fail(client):
    response = client.get('/get_user')
    assert response.status_code == 404

    
