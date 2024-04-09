import pytest
from mongomock import MongoClient
from webApp.app import create_app

@pytest.fixture
def app():
    app = create_app(MongoClient().db.collection)
    app.config['TESTING'] = True

    yield app

@pytest.fixture
def client(app):
    return app.test_client()
