"""Module for testing the main flask app"""

import pytest
from mongomock import MongoClient
from webApp.app import create_app


def test_sanity_check():
    """Placeholder test"""
    expected = True  # the value we expect to be present
    actual = True  # the value we see in reality
    assert actual == expected, "Expected True to be equal to True!"


@pytest.fixture
def app():
    """Created app instance with mock database for testing"""
    app = create_app(MongoClient().db.collection)
    app.config["TESTING"] = True

    yield app


@pytest.fixture
def client(app):
    """Returned client for test usage"""
    return app.test_client()


def test_ping(client):
    """Ensure Home page is running"""
    res =  client.get("/")
    assert res.status_code == 200


def test_save_location(client):
    """Ensure location is saved to database"""
    lat = 40
    long = -74

    response = client.post(
        "/save_location", json={"latitude": lat, "longitude": long}
    )
    assert response.status_code == 200


def test_get_user(client):
    """Ensure data can be retrieved from database"""
    lat = 40
    long = -74

    client.post("/save_location", json={"latitude": lat, "longitude": long})
    response = client.get("/get_user")
    assert response.status_code == 200


def test_get_user_fail(client):
    """Ensure error occurs when data is not found"""
    response = client.get("/get_user")
    assert response.status_code == 404
