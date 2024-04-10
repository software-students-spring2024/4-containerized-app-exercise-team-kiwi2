import os
import pytest
from mongomock import MongoClient
from machineLearningClient.app import create_app

def test_sanity_check():
    expected = True  # the value we expect to be present
    actual = True  # the value we see in reality
    assert actual == expected, "Expected True to be equal to True!"

@pytest.fixture
def db():
    client = MongoClient()
    db = client.db.collection
    yield db
    client.drop_database(db)


def test_ML_client(db):
    user_data = {
        "name": "Test User",
        "latitude": 40,
        "longitude": -74,
        "city": "New York",
        "region": "New York",
        "country": "United States of America",
        "ml_response": ""
    }
    db.insert_one(user_data)
    app = create_app(db, os.environ.get("OPENAI_API_KEY"))
    app.config['TESTING'] = True
    client = app.test_client()
    response = client.get('/ml_result')
    assert response.status_code == 200

def test_ML_client_fail(db):
    user_data = {
        "name": "Test",
        "latitude": 40,
        "longitude": -74,
        "city": "New York",
        "region": "New York",
        "country": "United States of America",
        "ml_response": ""
    }
    db.insert_one(user_data)
    app = create_app(db, os.environ.get("OPENAI_API_KEY"))
    app.config['TESTING'] = True
    client = app.test_client()
    response = client.get('/ml_result')
    assert response.status_code == 404


    