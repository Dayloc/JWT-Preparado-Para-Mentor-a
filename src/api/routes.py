"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

bcrypt = Bcrypt()


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }
    return jsonify(response_body), 200


@api.route('/public', methods=['POST', 'GET'])
def ruta_publica():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }
    return jsonify(response_body), 200


@api.route('/private', methods=['POST', 'GET'])
@jwt_required()
def ruta_privada():
    user = get_jwt_identity()
    if not user:
        return jsonify({"message": "User not found"}), 404
    user = User.query.get(user)
    response_body = {
        "message": f"Hello!  I'm  a private message of {user.email}, you can only see me if you are logged in"
    }
    return jsonify(response_body), 200


@api.route('/user/login', methods=['POST'])
def login_user():
    data_request = request.get_json()

    if not 'email' in data_request or not 'password' in data_request:
        return jsonify({"message": "Email and password are required"}), 400

    user = User.query.filter_by(email=data_request['email']).first()
    access_token = create_access_token(identity=str(user.id))

    if user and bcrypt.check_password_hash(user.password, data_request['password']):
        return jsonify({
            "token": access_token,
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username
            }}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401


@api.route('/users/create', methods=['POST'])
def create_user():
    data_request = request.get_json()

    if not 'email' in data_request or not 'password' in data_request or not 'username' in data_request:
        return jsonify({"message": "Email , password and username are required"}), 400

    new_user = User(
        username=data_request['username'],
        email=data_request['email'],
        password=bcrypt.generate_password_hash(
            data_request['password']).decode('utf-8')
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while creating the user", "error": str(e)}), 500
    
    
    

@api.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200


#Verificar si el token es crorrecto 
@api.route('/verify-token', methods=['GET'])
@jwt_required()
def verify_token():
    user_id = get_jwt_identity()
    return jsonify({"message": "Token válido", "user_id": user_id}), 200