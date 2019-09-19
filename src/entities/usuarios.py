from sqlalchemy import Column, String
from .entity import Base
from marshmallow import Schema, fields

class Usuarios(Base):
    __tablename__ = 'usuarios'

    correo = Column(String, primary_key=True)
    nombre = Column(String)
    apellido1 = Column(String)
    apellido2 = Column(String)
    contrasenna = Column(String)
    tipo = Column(String)

    def __init__(self, correo, nombre, apellido1, apellido2, contrasenna, tipo):
        self.correo = correo
        self.nombre = nombre
        self.apellido1 = apellido1
        self.apellido2 = apellido2
        self.contrasenna = contrasenna
        self.tipo = tipo

class UsuariosSchema(Schema):
    correo = fields.Str()
    nombre = fields.Str()
    apellido1 = fields.Str()
    apellido2 = fields.Str()
    contrasenna = fields.Str()
    tipo = fields.Str()