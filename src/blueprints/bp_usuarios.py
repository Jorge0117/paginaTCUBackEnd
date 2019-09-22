from flask import Blueprint, jsonify, request
from ..entities.entity import Session
from ..entities.usuarios import Usuarios, UsuariosSchema

bp_usuarios = Blueprint('bp_usuarios', __name__)

@bp_usuarios.route('/usuarios')
def consultar_usuarios():
    session = Session()
    objeto_usuarios = session.query(Usuarios).all()

    schema = UsuariosSchema(many=True)
    usuario = schema.dump(objeto_usuarios)

    session.close()
    return jsonify(usuario)

@bp_usuarios.route('/usuarios/id', methods=['GET'])
def consultar_usuario_id():
    correo = request.args.get('correo')
    session = Session()
    objeto_usuario = session.query(Usuarios).get(correo)

    schema = UsuariosSchema()
    usuario = schema.dump(objeto_usuario)
    session.close()
    return jsonify(usuario)

@bp_usuarios.route('/usuarios', methods=['POST'])
def agregar_usuario():
    # mount exam object
    posted_usuario = UsuariosSchema(only=('correo', 'nombre', 'apellido1', 'apellido2', 'contrasenna', 'tipo'))\
        .load(request.get_json())

    usuario = Usuarios(**posted_usuario)

    # persist exam
    session = Session()
    session.add(usuario)
    session.commit()

    # return created exam
    nuevo_usuario = UsuariosSchema().dump(usuario)
    session.close()
    return jsonify(nuevo_usuario), 201

@bp_usuarios.route('/usuarios/editar', methods=['POST'])
def editar_usuario():
    posted_usuario = UsuariosSchema(only=('correo', 'nombre', 'apellido1', 'apellido2', 'contrasenna', 'tipo')) \
        .load(request.get_json())

    usuario_actualizado = Usuarios(**posted_usuario)

    session = Session()
    objeto_usuario = session.query(Usuarios).get(usuario_actualizado.correo)
    if objeto_usuario is None:
        return "Usuario no encontrado", 404

    schema = UsuariosSchema()

    objeto_usuario.nombre = usuario_actualizado.nombre
    objeto_usuario.apellido1 = usuario_actualizado.apellido1
    objeto_usuario.apellido2 = usuario_actualizado.apellido2
    objeto_usuario.contrasenna = usuario_actualizado.contrasenna
    objeto_usuario.tipo = usuario_actualizado.tipo

    session.add(objeto_usuario)
    session.commit()
    usuario = schema.dump(objeto_usuario)
    session.close()

    return jsonify(usuario)

@bp_usuarios.route('/usuarios', methods=['DELETE'])
def eliminar_usuario():
    correo = request.args.get('correo')
    session = Session()
    objeto_usuario = session.query(Usuarios).get(correo)
    if objeto_usuario is None:
        return "Usuario no encontrado", 404

    session.delete(objeto_usuario)
    session.commit()

    session.close()
    return '', 200