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
import random
import string

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
@jwt_required()
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
        return jsonify({"msg":"Email requerido"}), 401
    if not password:
        return jsonify({"msg":"Contraseña requerida"}), 401

    email_query = User.query.filter_by(email=email).first()
    if email_query:
        return jsonify({"msg":"Este email pertenece a otro usuario"}), 401
    
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
        "msg": "Usuario creado exitosamente",
        "email": email
    }
    return jsonify(response), 201 #Devuelvo en texto plano

#Para modificar un usuario
@api.route('/user/<int:id>', methods=['PUT'])
@jwt_required()
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
@jwt_required()
def delete_user(id = None):
 if request.method == 'DELETE':
    user = User.query.get(id)
    
    db.session.delete(user)
    db.session.commit()

    response = {
        "msg": "Usuario eliminado satisfactoriamente",
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
        return jsonify({"msg":"Email requerido"}), 400

    if not password:
        return jsonify({"msg":"Contraseña requerida"}), 400
    
    user = User.query.filter_by(email=email).first()
    print(user)

    if not user:
        return jsonify({"msg": "El email no existe",
        "status": 401
        
        }), 401

    # password=generate_password_hash(password, method='sha256')

    if not check_password_hash(user.password, password):
         return jsonify({"msg": "La contraseña no es correcta",
        "status": 401
        }), 400

    expiracion = datetime.timedelta(days=1)
    access_token = create_access_token(identity=user.email, expires_delta=expiracion)

    data = {
        "id": user.id,
        "email": user.email,
        "perfil": user.perfil,
        "token": access_token, #Lo normal es que solamente se regrese el token
        "expires": expiracion.total_seconds()*1000,
    }


    return jsonify(data), 200

#Para cambiar la contrasena
@api.route('/cambiarc/<int:id>', methods=['PUT'])
@jwt_required()
def cambiarc(id = None):
    
    actual = request.json.get("actual", None)
    nueva = request.json.get("nueva", None)
    
    user = User.query.get(id)

    if not check_password_hash(user.password, actual):
         return jsonify({"msg": "La contraseña actual no es correcta",
        "status": 401
        }), 400
    hashed_password=generate_password_hash(nueva, method='sha256')
    user.password = hashed_password
    db.session.commit()

    response = {
        "msg": "Contraseña cambiada exitosamente"
    }
    return jsonify(response), 201 #Devuelvo en texto plano

#Para recuperar la contrasena
@api.route('/recuperarc', methods=['PUT'])
def recuperarc():
    
    email = request.json.get("email", None)

    if not email:
        return jsonify({"msg":"Email requerido"}), 400
    
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"msg": "El email no existe",
        "status": 401
        }), 401

    nuevaC = (''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(8)))

    hashed_password=generate_password_hash(nuevaC, method='sha256')
    user.password = hashed_password
    db.session.commit()

    response = {
        "msg": "Contraseña restablecida. Revisa tu correo electrónico",
        "contrasena": nuevaC
    }
    return jsonify(response), 201 #Devuelvo en texto plano

############################################################################################################

#Para ver todos los contratos
@api.route('/contratos', methods=['GET'])
@jwt_required()
def get_contratos():
    query_contratos = Contrato.query.all()
    query_contratos = list(map(lambda x: x.listacontratos(), query_contratos))
    #print(query_user)
    response_body = {
        "Lista_de_contratos": query_contratos
    }
    return jsonify(response_body), 200

#Para ver datos de un contrato
@api.route('/contrato/<int:id>', methods=['GET'])
@jwt_required()
def get_contrato(id = None):
    query_contratos = Contrato.query.filter_by(id=id).first()
    return jsonify(query_contratos.datoscontrato()), 200

#Para crear un contrato
@api.route('/contrato', methods=['POST'])
@jwt_required()
def post_contrato():
 if request.method == 'POST':
    id_project = request.json.get("id_project", None)
    region = request.json.get("region", None)
    comuna = request.json.get("comuna", None)
    sector = request.json.get("sector", None)
    plano = request.json.get("plano", None)
    obra_descripcion = request.json.get("obra_descripcion", None)
    planta_matriz = request.json.get("planta_matriz", None)
    comentario = request.json.get("comentario", None)
    tecnicos = request.json.get("tecnicos", None)
    
    if not id_project:
        return "Nombre de contrato required", 401

    contrato = Contrato()
    contrato.id_project = id_project
    contrato.region = region
    contrato.comuna = comuna
    contrato.sector = sector
    contrato.plano = plano
    contrato.obra_descripcion = obra_descripcion
    contrato.planta_matriz = planta_matriz
    contrato.comentario = comentario
    contrato.tecnicos = tecnicos

    db.session.add(contrato)
    db.session.commit()

    response = {
        "msg": "Added successfully",
        "name": id_project
    }
    return jsonify(response), 201 #Devuelvo en texto plano

#Para modificar un contrato
@api.route('/contrato/<int:id>', methods=['PUT'])
@jwt_required()
def put_contrato(id = None):
 if request.method == 'PUT':
    id_project = request.json.get("id_project", None)
    region = request.json.get("region", None)
    comuna = request.json.get("comuna", None)
    sector = request.json.get("sector", None)
    plano = request.json.get("plano", None)
    obra_descripcion = request.json.get("obra_descripcion", None)
    planta_matriz = request.json.get("planta_matriz", None)
    status = request.json.get("status", None)
    comentario = request.json.get("comentario", None)
    tecnicos = request.json.get("tecnicos", None)

    contrato = Contrato.query.get(id)

    if status == "Finalizado":
        if not tecnicos:
            return jsonify({"msg":"No se puede finalizar un contrato si no tiene técnicos asignados"}), 400

    if id_project:
        contrato.id_project = id_project
    if region:
        contrato.region = region
    if comuna:
        contrato.comuna = comuna
    if sector:
        contrato.sector = sector
    if plano:
        contrato.plano = plano
    if obra_descripcion:
        contrato.obra_descripcion = obra_descripcion
    if planta_matriz:
        contrato.planta_matriz = planta_matriz
    if status:
        contrato.status = status
    if comentario:
        contrato.comentario = comentario
    if tecnicos:
        contrato.tecnicos = tecnicos
    #db.session.add(user)
    db.session.commit()

    response = {
        "msg": "Changes successfully",
        "name": id_project
    }
    return jsonify(response), 201 #Devuelvo en texto plano

#Para eliminar un contrato
@api.route('/contrato/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_contrato(id = None):
 if request.method == 'DELETE':
    contrato = Contrato.query.get(id)

    """ orden = OrdenTrabajo.query.filter_by(id_contrato = id)
    
    while orden:
        db.session.delete(orden)
        orden = OrdenTrabajo.query.filter_by(id_contrato = id) """

    db.session.delete(contrato)
    db.session.commit()

    response = {
        "msg": "Delete successfully",
        "name": contrato.id_project
    }
    return jsonify(response), 201 #Devuelvo en texto plano

############################################################################################################

#Para ver todas las ordenes de trabajo de un contrato
@api.route('/orders/<int:id_contrato>', methods=['GET'])
@jwt_required()
def get_order_trabajo_by_contrato(id_contrato = None):
    query_order_trabajo = OrdenTrabajo.query.filter_by(id_contrato = id_contrato)
    query_order_trabajo = list(map(lambda x: x.listaorden(), query_order_trabajo))
    return jsonify(query_order_trabajo), 200

    return jsonify(response_body), 200

#Para ver una orden de trabajo en especifico
@api.route('/order/<int:id>', methods=['GET'])
@jwt_required()
def get_order_trabajo(id = None):
    query_order_trabajo = OrdenTrabajo.query.filter_by(id = id).first()
    return jsonify(query_order_trabajo.datoscorden()), 200

#Para crear una orden de trabajo de un contrato
@api.route('/order', methods=['POST'])
@jwt_required()
def post_order_trabajo():
 if request.method == 'POST':
    id_contrato = request.json.get("id_contrato", None)
    id_nombre = request.json.get("id_nombre", None)
    tipo = request.json.get("tipo", None)
    direccion = request.json.get("direccion", None)
    descripcion = request.json.get("descripcion", None)
    tecnicos = request.json.get("tecnicos", None)
    
    if not id_contrato:
        return "Contrato required", 401
    contrato_query = Contrato.query.get(id_contrato)
    if not contrato_query:
        return "No existe ese contrato", 401

    orden = OrdenTrabajo()
    orden.id_contrato = id_contrato
    orden.id_nombre = id_nombre
    orden.tipo = tipo
    orden.direccion = direccion
    orden.descripcion = descripcion
    orden.tecnicos = tecnicos

    db.session.add(orden)
    db.session.commit()

    response = {
        "msg": "Added successfully",
        "name": id_nombre
    }
    return jsonify(response), 201 #Devuelvo en texto plano

#Para modificar una orden de trabajo
@api.route('/order/<int:id>', methods=['PUT'])
@jwt_required()
def put_order_trabajo(id = None):
 if request.method == 'PUT':
    id_nombre = request.json.get("id_nombre", None)
    tipo = request.json.get("tipo", None)
    direccion = request.json.get("direccion", None)
    descripcion = request.json.get("descripcion", None)
    status = request.json.get("status", None)
    tecnicos = request.json.get("tecnicos", None)
    
    ordentrabajo = OrdenTrabajo.query.get(id)

    if status == "Finalizado":
        if not tecnicos:
            return jsonify({"msg":"No se puede finalizar una orden de trabajo si no tiene técnicos asignados"}), 400

    if id_nombre:
        ordentrabajo.id_nombre = id_nombre
    if tipo:
        ordentrabajo.tipo = tipo
    if direccion:
        ordentrabajo.direccion = direccion
    if descripcion:
        ordentrabajo.descripcion = descripcion
    if status:
        ordentrabajo.status = status
    if tecnicos:
        ordentrabajo.tecnicos = tecnicos
    #db.session.add(user)
    db.session.commit()

    response = {
        "msg": "Changes successfully",
        "name": id_nombre
    }
    return jsonify(response), 201 #Devuelvo en texto plano

#Para eliminar una orden de trabajo
@api.route('/order/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_orden(id = None):
 if request.method == 'DELETE':
    order = OrdenTrabajo.query.get(id)
    
    db.session.delete(order)
    db.session.commit()

    response = {
        "msg": "Delete successfully",
        "name": order.id_nombre
    }
    return jsonify(response), 201 #Devuelvo en texto plano

############################################################################################################






