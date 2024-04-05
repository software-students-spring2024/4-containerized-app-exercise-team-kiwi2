"""Module to import Flask and pymongo"""
from flask import Flask, jsonify, render_template
from pymongo import MongoClient

app = Flask(__name__)


MONGO_URI = "mongodb://mongo_db:27017/mydatabase"
client = MongoClient(MONGO_URI)
db = client.mydatabase
users_collection = db.users

@app.route('/')
def ping_server():
    """Function for home page"""
    return render_template('index.html')


@app.route('/save_user', methods=['GET'])
def save_user():
    """Test function to save user"""
    user_data = {
        'name': 'Test User',
        'email': 'test@example.com'
    }
    result = users_collection.insert_one(user_data)
    return jsonify({'message': 'User saved successfully', 'user_id': str(result.inserted_id)}), 201

# Route to get one user
@app.route('/get_user', methods=['GET'])
def get_user():
    """Test function to get user"""
    user = users_collection.find_one({'name': 'Test User'})
    if user:
        # Dump user data into JSON format
        dumped_user = {
            'name': user['name'],
            'email': user['email']
        }
        return jsonify({'user': dumped_user}), 200
    return jsonify({'message': 'User not found'}), 404



if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)
