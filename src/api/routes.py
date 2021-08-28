"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User 
from api.models import db, User, Contrato, OrdenTrabajo, StatusOrden, DetalleOrdenTrabajo, UserOrden, Acreditacion #Y todo lo que se necesite
from api.utils import generate_sitemap, APIException
from werkzeug.security import generate_password_hash, check_password_hash       ## Nos permite manejar tokens por authentication (usuarios)    
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity   #El 2do es para crear el token y el 3ro para pedir siempre
import datetime #Es propio de Python
from sqlalchemy.orm import sessionmaker


api = Blueprint('api', __name__)

#Para probar la conexion con la API
@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = {
        "message": "Hello! I'm a message that came from the backend"
    }
    return jsonify(response_body), 200

#Para crear un hash, no se usa en produccion
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

############################################################################################################

#Para ver datos especificos de un usuario
@api.route('/user/<int:id>', methods=['GET'])
def get_user(id = None):
    user = User.query.get(id)
    if not user:
        return "User no existe", 401
    return jsonify(user.datosusuario()), 200

#Para registrar un usuario
@api.route('/user', methods=['POST'])
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

#Para modificar un usuario
@api.route('/user/<int:id>', methods=['PUT'])
def modify_user(id = None):
    
 if request.method == 'PUT':
    rut = request.json.get("rut", None)
    name = request.json.get("name", None)
    lastname = request.json.get("lastname", None)
    contact = request.json.get("contact", None)
    register = request.json.get("register", None)
    perfil = request.json.get("perfil", None)
    fecha_nacimiento = request.json.get("fecha_nacimiento", None)
    
    user = User.query.get(id)
    if rut:
        user.rut = rut
    if name:
        user.name = name
    if lastname:
        user.lastname = lastname
    if contact:
        user.contact = contact
    if register:
        user.register = register
    if perfil:
        user.perfil = perfil
    if fecha_nacimiento:
        user.fecha_nacimiento = fecha_nacimiento
    #db.session.add(user)
    db.session.commit()

    response = {
        "msg": "Changes successfully",
        "name": name
    }
    return jsonify(response), 201 #Devuelvo en texto plano

#Para eliminar un usuario
@api.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id = None):
 if request.method == 'DELETE':
    user = User.query.get(id)
    
    db.session.delete(user)
    db.session.commit()

    response = {
        "msg": "Delete successfully",
        "name": user.name
    }
    return jsonify(response), 201 #Devuelvo en texto plano

#Para listar todos los usuarios de la Base de Datos
@api.route('/users', methods=['POST', 'GET'])
@jwt_required() #Para obligar al uso del token en el header
def handle_users():
    users = User.query.all()
    users = list(map(lambda x: x.listausuarios(), users))
    response_body = {
        "users": users
    }

    return jsonify(response_body), 200

############################################################################################################

#Para hacer login, devuelve un TOKEN
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
        "user": user.datosusuario(),
        "token": access_token, #Lo normal es que solamente se regrese el token
        "expires": expiracion.total_seconds()*1000,
        "id": user.id
    }


    return jsonify(data), 200

############################################################################################################

#Ruta para la lista de los contratos
@api.route('/lista_contratos', methods=['GET'])
def get_contratos():
    query_contratos = Contrato.query.all()
    query_contratos = list(map(lambda x: x.listacontratos(), query_contratos))
    #print(query_user)
    response_body = {
        "Lista_de_contratos": query_contratos
    }
    return jsonify(response_body), 200

#Rutas para datos especificos de un contrato
@api.route('/lista_contratos/<int:id>', methods=['GET'])
def get_contrato(id = None):
    query_contratos = Contrato.query.filter_by(id=id).first()
    return jsonify(query_contratos.datoscontrato()), 200

#Rutas para lista de ordenes de trabajo basado en un contrato
@api.route('/order_trabajo/<int:id_contrato>', methods=['GET'])
def get_order_trabajo_by_contrato(id_contrato = None):
    query_order_trabajo = OrdenTrabajo.query.filter_by(id_contrato = id_contrato)
    query_order_trabajo = list(map(lambda x: x.listaorden(), query_order_trabajo))
    return jsonify(query_order_trabajo), 200

    return jsonify(response_body), 200









#Ruta para la lista de contratos de un usuario
@api.route('/contratos_user/<int:id>', methods=['GET'])
def get_contratos_user(id = None):
    query_contratos_user = UserOrden.query.filter_by(id_user=id)
    query_contratos_user = list(map(lambda x: x.listaUserOrden(), query_contratos_user))

    Session = sessionmaker()
    session = Session()
    userOrden = UserOrden()
    ordenTrabajo = OrdenTrabajo()
    Contrato = Contrato()

    contratosUser = session.query(
         userOrden, OrdenTrabajo, Contrato,
    ).filter(
         Contrato.id == ordenTrabajo.id_contrato,
    ).filter(
         ordenTrabajo.id == userOrden.id_orden,
    ).filter(
        userOrden.id_user == id,
    ).all()
    
    response_body = {
        "Lista_de_contratos": contratosUser
    }
    return jsonify(response_body), 200

#Lista para una orden de trabajo en especifica y sus datos, hay que revisar el conflicto
#@api.route('/order/<int:id>', methods=['GET'])
#def get_order_trabajo(id = None):
    #query_order_trabajo = OrdenTrabajo.query.filter_by(id = id).first()
    #return jsonify(query_order_trabajo.datoscorden()), 200


