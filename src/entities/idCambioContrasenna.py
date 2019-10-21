from sqlalchemy import Column, String, TIMESTAMP
from .entity import Base
from marshmallow import Schema, fields


class IdCambioContrasenna(Base):
    __tablename__ = 'idcambiocontrasenna'

    correo = Column(String, primary_key=True)
    id = Column(String)
    fechaCreacion = Column(TIMESTAMP)

    def __init__(self, correo, id, fechaCreacion):
        self.correo = correo
        self.id = id
        self.fechaCreacion = fechaCreacion


class IdCambioContrasennaSchema(Schema):
    correo = fields.Str()
    id = fields.Str()
