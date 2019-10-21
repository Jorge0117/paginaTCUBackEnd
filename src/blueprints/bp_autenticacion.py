import datetime
import uuid

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, \
    get_jwt_identity, get_raw_jwt

from src.blueprints.bp_mail import enviarCorreo
from src.entities.idCambioContrasenna import IdCambioContrasenna, IdCambioContrasennaSchema
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


@bp_autenticacion.route('/generatePassChangeId', methods=['POST'])
def generate_password_change_id():
    try:
        correo = request.data.decode(request.charset)

        session = Session()
        usuario = session.query(Usuarios).filter_by(correo=correo).first()
        if usuario is None:
            session.close()
            return "El correo insertado no pertenece a ningún usuario", 404

        id = uuid.uuid1()
        id = id.hex

        entidadId = IdCambioContrasenna(correo, id, datetime.datetime.now())

        previousId = session.query(IdCambioContrasenna).get(correo)
        if previousId is not None:
            session.delete(previousId)

        session.add(entidadId)

        urlFrontend = 'http://127.0.0.1:4200/cambioContrasenna/' + id + '/' + correo
        mail = {
            'texto': 'Si usted ha solicitado un cambio de contraseña, por favor haga click <a href="' + urlFrontend + '">aquí</a>',
            'subject': 'Solicitud de cambio de contraseña de la plataforma del CELEQ',
            'destinatario': correo
        }
        enviarCorreo(mail)

        session.commit()
        session.close()
        return '', 200
    except Exception as e:
        print(e)
        return 'Error al crear identificador de cambio de contraseña', 400


@bp_autenticacion.route('/checkPassChangeId', methods=['POST'])
def check_password_change_id():
    data = IdCambioContrasennaSchema(only=('correo', 'id')) \
        .load(request.get_json())

    session = Session()
    cachedId = session.query(IdCambioContrasenna).get(data['correo'])
    if cachedId is None:
        return "No se generó una solicitud de cambio de contraseña con ese correo", 404
    if cachedId.id != data['id']:
        return "El número identificador de cambio de contraseña no es válido", 400
    else:
        session.delete(cachedId)
        session.commit()
        return "", 200