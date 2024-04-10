"""These imports are used create a flask server for the ml part  """

import os
from flask import Flask, jsonify
from pymongo import MongoClient
from flask_cors import cross_origin
import openai


def predict(user_loc, openai_key):
    """Function to call openAI api and get result"""
    openai.my_api_key = openai_key
    location = user_loc
    messages = [
        {"role": "system", "content": "You are an intelligent assistant."},
        {"role": "user", "content": "List the 5 best things to do in " + location},
    ]
    chat = openai.chat.completions.create(messages=messages, model="gpt-3.5-turbo")
    reply = chat.choices[0].message.content
    return reply


def create_app(collection, api_key):
    """Create the app and related functions"""
    app = Flask(__name__)
    app.config["CORS_HEADERS"] = "Content-Type"

    @app.route("/ml_result", methods=["GET"])
    @cross_origin()
    def machine_learning_client():
        """Function to generate Ml Part"""
        user = collection.find_one({"name": "Test User"})
        if user:
            user_loc = "" + user["city"] + user["region"] + user["country"]
            ml_response = predict(user_loc, api_key)
            # Dump user data into JSON format
            collection.update_one(
                {"_id": user["_id"]}, {"$set": {"ml_response": ml_response}}
            )
            return jsonify({"message": "Ml Response Added"}), 200
        return jsonify({"message": "User not found"}), 404

    return app


if __name__ == "__main__":
    MONGO_URI = "mongodb://mongo_db:27017/mydatabase"
    client = MongoClient(MONGO_URI)
    db = client.mydatabase
    users_collection = db.users
    key = os.environ.get("OPENAI_API_KEY")
    main_app = create_app(users_collection, key)
    main_app.run(host="0.0.0.0", port=5001)
