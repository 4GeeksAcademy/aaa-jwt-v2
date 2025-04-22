from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

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

@api.route('/signup', methods=['POST'])
def signup():

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

    user_id = new_user.id
    access_token = create_access_token(identity=str(user_id))

    return jsonify({ **new_user.serialize(), "access_token": access_token }), 201

@api.route('/login', methods=['POST'])
def login():
    
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({'msg': 'error en email o password'}), 400

    current_user = User.query.filter_by(email = email).first()
    if not current_user:
        return jsonify({'msg': 'usuario no existe'}), 404
    
    pass_db = current_user.password
    true_or_false = bcrypt.check_password_hash(pass_db, password)

    if true_or_false:

            user_id = current_user.id
            access_token = create_access_token(
            identity=str(user_id))

            return jsonify({
                "msg": "Sesion iniciada",
                "access_token": access_token,
                "email": email
            }), 200
            

    else:
            return jsonify({"msg": "Usuario o contraseña invalido."}), 401
    
@api.route('/private', methods=["GET"])
@jwt_required()
def home():

    current_user_id = get_jwt_identity()

    if current_user_id:
        users = User.query.all()
        user_list = []
        for user in users:
            user_act = {
            "id": user.id,
            "email": user.email,
            "is_active": user.is_active
            }
            user_list.append(user_act)

        return jsonify({"users": user_list}), 200

    else:
        return jsonify({"Error": "Inicia sesion"}), 401