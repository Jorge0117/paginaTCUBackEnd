from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from ..entities.entity import Session
from ..entities.personas import Personas, PersonasSchema

bp_personas = Blueprint('bp_personas', __name__)


@bp_personas.route('/personas')
def consultar_personas():
    tipo = request.args.get('tipo')
    session = Session()
    objeto_personas = session.query(Personas).filter_by(tipo=tipo).all()

    schema = PersonasSchema(many=True)
    personas = schema.dump(objeto_personas)

    session.close()
    return jsonify(personas)


@bp_personas.route('/personas/id', methods=['GET'])
@jwt_required
def consultar_persona_id():
    correo = request.args.get('correo')
    session = Session()
    objeto_persona = session.query(Personas).get(correo)

    schema = PersonasSchema()
    persona = schema.dump(objeto_persona)
    session.close()
    return jsonify(persona)


@bp_personas.route('/personas', methods=['POST'])
@jwt_required
def agregar_persona():
    posted_persona = PersonasSchema(
        only=('correo', 'nombre', 'apellido1', 'apellido2', 'tipo', 'escuela', 'informacion_adicional')) \
        .load(request.get_json())

    persona = Personas(**posted_persona)

    session = Session()

    persona_base = session.query(Personas).get(persona.correo)
    if persona_base is not None:
        session.close()
        return 'Persona ya se encuentra en la base', 409

    session.add(persona)
    session.commit()

    # return created exam
    nueva_persona = PersonasSchema().dump(persona)
    session.close()
    return jsonify(nueva_persona), 201


@bp_personas.route('/personas/editar', methods=['POST'])
@jwt_required
def editar_usuario():
    posted_persona = PersonasSchema(
        only=('correo', 'nombre', 'apellido1', 'apellido2', 'tipo', 'escuela', 'informacion_adicional')) \
        .load(request.get_json())

    persona_actualizada = Personas(**posted_persona)

    session = Session()
    objeto_persona = session.query(Personas).get(persona_actualizada.correo)
    if objeto_persona is None:
        return "Persona no encontrada", 404

    schema = PersonasSchema()

    objeto_persona.correo = persona_actualizada.correo
    objeto_persona.nombre = persona_actualizada.nombre
    objeto_persona.apellido1 = persona_actualizada.apellido1
    objeto_persona.apellido2 = persona_actualizada.apellido2
    objeto_persona.tipo = persona_actualizada.tipo
    objeto_persona.escuela = persona_actualizada.escuela
    objeto_persona.informacion_adicional = persona_actualizada.informacion_adicional

    session.add(objeto_persona)
    session.commit()
    persona = schema.dump(objeto_persona)
    session.close()

    return jsonify(persona)


@bp_personas.route('/personas', methods=['DELETE'])
@jwt_required
def eliminar_persona():
    correo = request.args.get('correo')
    session = Session()
    objeto_persona = session.query(Personas).get(correo)
    if objeto_persona is None:
        return "Persona no encontrada", 404

    session.delete(objeto_persona)
    session.commit()

    session.close()
    return '', 200
