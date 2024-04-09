"""Module to import Flask and pymongo"""

from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
import requests


def create_app(users_collection):
    app = Flask(__name__)

    @app.route("/")
    def ping_server():
        """Function for home page"""
        return render_template("index.html")


    @app.route("/save_location", methods=["POST"])
    def save_location():
        """Save city of current user."""
        data = request.json
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        url_base = "http://api.weatherapi.com/v1/search.json?key=4c826779d36e41a6bb8231845240704&q="

        api_url = url_base + str(latitude) + "," + str(longitude)

        response = requests.get(api_url, timeout=15)

        data = response.json()

        city = data[0]["name"]
        region = data[0]["region"]
        country = data[0]["country"]

    user_data = {
        "name": "Test User",
        "latitude": latitude,
        "longitude": longitude,
        "city": city,
        "region": region,
        "country": country,
        "ml_response": "",
    }

    result = users_collection.insert_one(user_data)

    user_id = str(result.inserted_id)

    response = {"message": "User data saved successfully", "user_id": user_id}
    return jsonify(response), 200


# Route to get one user
@app.route("/get_user", methods=["GET"])
def get_user():
    """Function to get user info"""

    user = users_collection.find_one({"name": "Test User"})
    if user:
        # Dump user data into JSON format
        dumped_user = {
            "name": user["name"],
            "latitude": user["latitude"],
            "longitude": user["longitude"],
            "city": user["city"],
            "region": user["region"],
            "country": user["country"],
            "ml_response": user["ml_response"],
        }
        return jsonify({"user": dumped_user}), 200
    return jsonify({"message": "User not found"}), 404


if __name__ == "__main__":
    MONGO_URI = "mongodb://mongo_db:27017/mydatabase"
    client = MongoClient(MONGO_URI)
    db = client.mydatabase
    users_collection = db.users
    app = create_app(users_collection)
    app.run(host="0.0.0.0", port=5000)
