from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from ..entities.entity import Session
from ..entities.areasDeInteres import AreasDeInteres, AreasDeInteresSchema

bp_areasDeInteres = Blueprint('bp_areasDeInteres', __name__)

@bp_areasDeInteres.route('/areasdeinteres')
@jwt_required
def consultar_areas_de_interes():
    session = Session()
    objeto_areasdeinteres = session.query(AreasDeInteres).all()

    schema = AreasDeInteresSchema(many=True)
    areasdeinteres = schema.dump(objeto_areasdeinteres)

    session.close()
    return jsonify(areasdeinteres)

@bp_areasDeInteres.route('/areasdeinteres/id', methods=['GET'])
@jwt_required
def consultar_areas_de_interes_id():
    id = request.args.get('id')
    session = Session()
    objeto_areasdeinteres = session.query(AreasDeInteres).get(id)

    schema = AreasDeInteresSchema()
    areasdeinteres = schema.dump(objeto_areasdeinteres)
    session.close()
    return jsonify(areasdeinteres)

@bp_areasDeInteres.route('/areasdeinteres', methods=['POST'])
@jwt_required
def agregar_areas_de_interes():

    posted_area = AreasDeInteresSchema(only=('id', 'esp_nombre', 'ing_nombre', 'ubicacion_imagen'))\
        .load(request.get_json())

    area = AreasDeInteres(**posted_area)

    session = Session()

    usuario_base = session.query(AreasDeInteres).get(area.id)
    if usuario_base is not None:
        session.close()
        return 'Área de interés ya se encuentra en la base', 409

    session.add(area)
    session.flush()
    nueva_area = AreasDeInteresSchema().dump(area)
    session.commit()

    # return created exam

    session.close()
    return jsonify(nueva_area), 201

@bp_areasDeInteres.route('/areasdeinteres/editar', methods=['POST'])
@jwt_required
def editar_areas_de_interes():
    posted_area = AreasDeInteresSchema(only=('id', 'esp_nombre', 'ing_nombre', 'ubicacion_imagen')) \
        .load(request.get_json())

    area_actualizada = AreasDeInteres(**posted_area)

    session = Session()
    objeto_area = session.query(AreasDeInteres).get(area_actualizada.id)
    if objeto_area is None:
        return "Área de interés no encontrada", 404

    schema = AreasDeInteresSchema()

    objeto_area.esp_nombre = area_actualizada.esp_nombre
    objeto_area.ing_nombre = area_actualizada.ing_nombre
    objeto_area.ubicacion_imagen = area_actualizada.ubicacion_imagen

    session.add(objeto_area)
    session.commit()
    area = schema.dump(objeto_area)
    session.close()

    return jsonify(area)

@bp_areasDeInteres.route('/areasdeinteres', methods=['DELETE'])
@jwt_required
def eliminar_areas_de_interes():
    id = request.args.get('id')
    session = Session()
    objeto_area = session.query(AreasDeInteres).get(id)
    if objeto_area is None:
        return "Área de interés no encontrada", 404

    session.delete(objeto_area)
    session.commit()

    session.close()
    return '', 200
