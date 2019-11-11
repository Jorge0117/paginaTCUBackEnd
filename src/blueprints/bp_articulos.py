from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from ..entities.entity import Session
from ..entities.articulos import Articulos, ArticulosSchema

bp_articulos = Blueprint('bp_articulos', __name__)

@bp_articulos.route('/articulos/area')
def consultar_articulos_area():
    idArea = request.args.get('area')
    session = Session()
    objeto_articulos = session.query(Articulos).filter_by(id_area_interes=idArea).all()
    schema = ArticulosSchema(many=True)
    articulos = schema.dump(objeto_articulos)
    session.close()
    return jsonify(articulos)

@bp_articulos.route('/articulos', methods=['POST'])
@jwt_required
def agregar_articulo():

    json_articulo = request.get_json()
    json_articulo['fecha'] = json_articulo['fecha'].split('T')[0]
    posted_articulo = ArticulosSchema().load(json_articulo)

    articulo = Articulos(**posted_articulo)

    session = Session()

    articulo_base = session.query(Articulos).get(articulo.id)
    if articulo_base is not None:
        session.close()
        return 'Artículo ya se encuentra en la base', 409

    session.add(articulo)
    session.flush()
    nueva_area = ArticulosSchema().dump(articulo)
    session.commit()

    # return created exam

    session.close()
    return jsonify(nueva_area), 201