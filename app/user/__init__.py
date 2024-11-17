from flask import Blueprint, request, jsonify
from app.db.models import db
from app.user.add_user import add_user  # Import the function for adding a user

# Create a Blueprint for user-related routes
user_blueprint = Blueprint('user', __name__)

# Route for adding a new user
@user_blueprint.route('/add_user', methods=['POST'])
def add_user_route():
    data = request.get_json()  # Get data from the request

    # Call the add_user function with the data
    try:
        add_user(data)
        return jsonify({"message": "User added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
