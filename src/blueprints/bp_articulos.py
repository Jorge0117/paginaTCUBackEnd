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