"""These imports are used create a flask server for the ml part  """

import os
from flask import Flask, jsonify
from pymongo import MongoClient
from flask_cors import CORS, cross_origin
import openai


app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

MONGO_URI = "mongodb://mongo_db:27017/mydatabase"
client = MongoClient(MONGO_URI)
db = client.mydatabase
users_collection = db.users


def predict(user_loc):

    """Function to call openAI api and get result"""
    openai.my_api_key = os.environ.get("OPENAI_API_KEY")

    location = user_loc
    messages = [
        {"role": "system", "content": "You are an intelligent assistant."},
        {"role": "user", "content": "List the 5 best things to do in " + location},
    ]
    chat = openai.chat.completions.create(messages=messages, model="gpt-3.5-turbo")
    reply = chat.choices[0].message.content
    return reply


@app.route("/ml_result", methods=["GET"])
@cross_origin()
def machine_learning_client():

    """Function to generate Ml Part"""
    user = users_collection.find_one({"name": "Test User"})

    user_loc = "" + user["city"] + user["region"] + user["country"]
    ml_response = predict(user_loc)

    if user:
        # Dump user data into JSON format
        users_collection.update_one(
            {"_id": user["_id"]}, {"$set": {"ml_response": ml_response}}
        )
        return jsonify({"message": "Ml Response Added"}), 200
    return jsonify({"message": "User not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
