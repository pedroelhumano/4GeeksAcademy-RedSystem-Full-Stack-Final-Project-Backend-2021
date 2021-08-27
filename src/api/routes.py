"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User #Y todo lo que se necesite
from api.utils import generate_sitemap, APIException
from werkzeug.security import generate_password_hash, check_password_hash       ## Nos permite manejar tokens por authentication (usuarios)    
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity   #El 2do es para crear el token y el 3ro para pedir siempre
import datetime #Es propio de Python

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend"
    }

    return jsonify(response_body), 200

@api.route('/hash', methods=['POST', 'GET'])
def handle_hash():
    
    #Deberia ser post
    #email = request.json.get("email", None)
    #identity=email

    # Genera token
    expiracion = datetime.timedelta(days=1) #  Genera una fecha en UTC
    access_token = create_access_token(identity='mortega@4geeks.co', expires_delta=expiracion)

    # Crear password
    password = '123456'
    #password = request.json.get("password", None)
    password=generate_password_hash(password, method='sha256')

    response_token = {
        "users": "Manu", #email
        "token": access_token,
        "password": password
    }

    return jsonify(response_token), 200

@api.route('/register', methods=['POST'])
def register():
 if request.method == 'POST':
    email = request.json.get("email", None) #Lo validamos, si no existe (no lo mandan) lo definnimos "None"
    password = request.json.get("password", None) 
    rut = request.json.get("rut", None)
    name = request.json.get("name", None)
    lastname = request.json.get("lastname", None)
    contact = request.json.get("contact", None)
    register = request.json.get("register", None)
    perfil = request.json.get("perfil", None)
    fecha_nacimiento = request.json.get("fecha_nacimiento", None)
    
    if not email:
        return "Email required", 401
    if not password:
        return "Password required", 401

    email_query = User.query.filter_by(email=email).first()
    if email_query:
        return "This email has been already taken", 401
    
    user = User()
    user.email = email
    # user.is_active= True
    # Ahora se encripta la contrasena
    hashed_password=generate_password_hash(password, method='sha256')
    user.password = hashed_password
    user.rut = rut
    user.name = name
    user.lastname = lastname
    user.contact = contact
    user.register = register
    user.perfil = perfil
    user.fecha_nacimiento = fecha_nacimiento

    print(user)
    db.session.add(user)
    db.session.commit()

    response = {
        "msg": "Added successfully",
        "email": email
    }
    return jsonify(response), 201 #Devuelvo en texto plano

    #return jsonify(response_body), 200

@api.route('/users', methods=['POST', 'GET'])
@jwt_required() #Para obligar al uso del token en el header
def handle_users():
    users = User.query.all()
    users = list(map(lambda x: x.serialize(), users))
    response_body = {
        "users": users
    }

    return jsonify(response_body), 200

@api.route('/login', methods=['POST'])
def login():
    
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not email:
        return jsonify({"msg":"Email required"}), 400

    if not password:
        return jsonify({"msg":"Password required"}), 400
    
    user = User.query.filter_by(email=email).first()
    print(user)

    if not user:
        return jsonify({"msg": "The email is not correct",
        "status": 401
        
        }), 401

    # password=generate_password_hash(password, method='sha256')

    if not check_password_hash(user.password, password):
         return jsonify({"msg": "The password is not correct",
        "status": 401
        }), 400

    expiracion = datetime.timedelta(days=1)
    access_token = create_access_token(identity=user.email, expires_delta=expiracion)

    data = {
        "user": user.serialize(),
        "token": access_token, #Lo normal es que solamente se regrese el token
        "expires": expiracion.total_seconds()*1000,
        "email": email
    }


    return jsonify(data), 200
