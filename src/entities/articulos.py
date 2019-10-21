from sqlalchemy import Column, String, Integer, Date, Text
from .entity import Base
from marshmallow import Schema, fields


class Articulos(Base):
    __tablename__ = 'articulos'

    id = Column(Integer, autoincrement=True, primary_key=True)
    fecha = Column(Date)
    esp_titulo = Column(String)
    ing_titulo = Column(String)
    ubicacion_thumbnail = Column(String)
    esp_cuerpo = Column(Text)
    ing_cuerpo = Column(Text)
    id_area_interes = Column(Integer)
    correo_usuario = Column(Text)

    def __init__(self, id, fecha, esp_titulo, ing_titulo, ubicacion_thumbnail, esp_cuerpo, ing_cuerpo, id_area_interes,
                 correo_usuario):
        self.id = id
        self.fecha = fecha
        self.esp_titulo = esp_titulo
        self.ing_titulo = ing_titulo
        self.ubicacion_thumbnail = ubicacion_thumbnail
        self.esp_cuerpo = esp_cuerpo
        self.ing_cuerpo = ing_cuerpo
        self.id_area_interes = id_area_interes
        self.correo_usuario = correo_usuario


class ArticulosSchema(Schema):
    id = fields.Int()
    fecha = fields.Date()
    esp_titulo = fields.Str()
    ing_titulo = fields.Str()
    ubicacion_thumbnail = fields.Str()
    esp_cuerpo = fields.Str()
    ing_cuerpo = fields.Str()
    id_area_interes = fields.Int()
    correo_usuario = fields.Str()
