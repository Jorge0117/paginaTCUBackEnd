from sqlalchemy import Column, String
from .entity import Base
from marshmallow import Schema, fields


class Personas(Base):
    __tablename__ = 'personas'

    correo = Column(String, primary_key=True)
    nombre = Column(String)
    apellido1 = Column(String)
    apellido2 = Column(String)
    tipo = Column(String)
    escuela = Column(String)
    informacion_adicional = Column(String)

    def __init__(self, correo, nombre, apellido1, apellido2, tipo, escuela, informacion_adicional):
        self.correo = correo
        self.nombre = nombre
        self.apellido1 = apellido1
        self.apellido2 = apellido2
        self.tipo = tipo
        self.escuela = escuela
        self.informacion_adicional = informacion_adicional


class PersonasSchema(Schema):
    correo = fields.Str()
    nombre = fields.Str()
    apellido1 = fields.Str()
    apellido2 = fields.Str()
    tipo = fields.Str()
    escuela = fields.Str()
    informacion_adicional = fields.Str()
