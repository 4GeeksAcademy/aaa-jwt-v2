"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_bcrypt import Bcrypt

api = Blueprint('api', __name__)

bcrypt = Bcrypt()

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/user', methods=['POST'])
def create_user():

    name = request.json.get('name')
    password = request.json.get('password')
    email = request.json.get('email')
    
    if not name or not password or not email: 
        
        return jsonify({ 'msg': 'necesitamos todos los datos para poder registrar un usuario' }), 400
    
    user = User.query.filter_by(email = email).first()

    if user: 
        return jsonify({ 'msg': 'este email ya esta registrado' }), 400
    
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(name = name, password = password_hash, email = email)
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.serialize()), 201

@api.route('/login', methods=['POST'])
def login():
    
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({'msg': 'error en email o password'}), 400

    current_user = User.query.filter_by(email = email).first()
    if not current_user:
        return jsonify({'msg': 'usuario no existe'}), 404
    
    #