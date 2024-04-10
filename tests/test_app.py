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
def new_app():
    """Created app instance with mock database for testing"""
    temp_app = create_app(MongoClient().db.collection)
    temp_app.config["TESTING"] = True

    yield temp_app


@pytest.fixture
def temp_client(new_app):
    """Returned client for test usage"""
    return new_app.test_client()


def test_ping(temp_client):
    """Ensure Home page is running"""
    assert temp_client.get("/").status_code == 200


def test_save_location(temp_client):
    """Ensure location is saved to database"""
    lat = 40
    long = -74

    response = temp_client.post(
        "/save_location", json={"latitude": lat, "longitude": long}
    )
    assert response.status_code == 200


def test_get_user(temp_client):
    """Ensure data can be retrieved from database"""
    lat = 40
    long = -74

    temp_client.post("/save_location", json={"latitude": lat, "longitude": long})
    response = temp_client.get("/get_user")
    assert response.status_code == 200


def test_get_user_fail(temp_client):
    """Ensure error occurs when data is not found"""
    response = temp_client.get("/get_user")
    assert response.status_code == 404
