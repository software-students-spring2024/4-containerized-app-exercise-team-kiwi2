import pytest

# class Tests:
#     def test_sanity_check(self):
#         expected = True  # the value we expect to be present
#         actual = True  # the value we see in reality
#         assert actual == expected, "Expected True to be equal to True!"

def test_ping(client):
    assert client.get('/').status_code == 200

def test_save_location(client):
    lat = 40
    long = -74

    response = client.post(
        '/save_location', json={"latitude": lat, "longitude": long}
    )
    assert response.status_code == 200

    # user_data = fake_db.find_one({"latitude": lat, "longitude": long})
    # assert user_data is not None
    # assert user_data["city"] == "New York"
    # assert user_data["region"] == "New York"
    # assert user_data["country"] == "United States of America"
    

    
