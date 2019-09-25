from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, \
    get_jwt_identity, get_raw_jwt

from ..entities.entity import Session
from ..entities.usuarios import Usuarios, UsuariosSchema
import hashlib

bp_autenticacion = Blueprint('bp_autenticacion', __name__)

@bp_autenticacion.route('/login', methods=['POST'])
def login():
    posted_usuario = UsuariosSchema(only=('correo', 'contrasenna')) \
        .load(request.get_json())

    contrasennaEncriptada = hashlib.sha1(posted_usuario['contrasenna'].encode())

    session = Session()
    usuario_base = session.query(Usuarios).get(posted_usuario['correo'])
    if usuario_base is None:
        session.close()
        return 'Usuario no existe', 404
    if usuario_base.contrasenna != contrasennaEncriptada.hexdigest():
        session.close()
        return 'Contraseña incorrecta', 406

    payload = {'correo': usuario_base.correo, 'nombre': usuario_base.nombre, 'apellido1': usuario_base.apellido1,
               'apellido2': usuario_base.apellido2, 'tipo': usuario_base.tipo}

    access_token = create_access_token(identity=payload)
    refresh_token = create_refresh_token(identity=payload)

    return jsonify({'jwt': access_token, 'refreshToken': refresh_token}), 200

@bp_autenticacion.route('/login/refresh')
@jwt_refresh_token_required
def refresh_token():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return {'access_token': access_token}, 200