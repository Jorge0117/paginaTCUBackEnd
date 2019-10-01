from sqlalchemy import Column, String, Integer
from .entity import Base
from marshmallow import Schema, fields

class AreasDeInteres(Base):
    __tablename__ = 'areasdeinteres'

    id = Column(Integer, autoincrement=True, primary_key=True)
    esp_nombre = Column(String)
    ing_nombre = Column(String)
    ubicacion_imagen = Column(String)

    def __init__(self, id, esp_nombre, ing_nombre, ubicacion_imagen):
        self.id = id
        self.esp_nombre = esp_nombre
        self.ing_nombre = ing_nombre
        self.ubicacion_imagen = ubicacion_imagen

class AreasDeInteresSchema(Schema):
    id = fields.Int()
    esp_nombre = fields.Str()
    ing_nombre = fields.Str()
    ubicacion_imagen = fields.Str()