  
"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Contrato
from api.utils import generate_sitemap, APIException


api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend"
    }

    return jsonify(response_body), 200

@api.route('/lista_users', methods=['GET'])
def get_users():
    query_user = User.query.all()
    query_user = list(map(lambda x: x.listausuarios(), query_user))
    print(query_user)
    response_body = {
        #"msg": "Hello, this is your GET /user response ",
        "Lista_de_usuarios": query_user
    }
    return jsonify(response_body), 200

@api.route('/lista_users/<int:id>', methods=['GET'])
def get_user(id = None):
    query_user = User.query.filter_by(id=id).first()
    return jsonify(query_user.datosusuario()), 200

@api.route('/lista_contratos', methods=['GET'])
def get_contratos():
    query_contratos = Contrato.query.all()
    query_contratos = list(map(lambda x: x.listacontratos(), query_contratos))
    #print(query_user)
    response_body = {
        "Lista_de_contratos": query_contratos
    }
    return jsonify(response_body), 200

@api.route('/lista_contratos/<int:id>', methods=['GET'])
def get_contrato(id = None):
    query_contratos = Contrato.query.filter_by(id=id).first()
    return jsonify(query_contratos.datoscontrato()), 200