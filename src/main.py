from flask import Flask, jsonify, request
from flask_cors import CORS

from .entities.entity import Session, engine, Base
from .entities.usuarios import Usuarios, UsuariosSchema

# creating the Flask application
app = Flask(__name__)
CORS(app, resources={r"/src/*": {"origins": "http://localhost:4200"}})

# if needed, generate database schema
Base.metadata.create_all(engine)


@app.route('/usuarios')
def get_exams():
    # fetching from the database
    session = Session()
    exam_objects = session.query(Usuarios).all()

    # transforming into JSON-serializable objects
    schema = UsuariosSchema(many=True)
    usuario = schema.dump(exam_objects)

    # serializing as JSON
    session.close()
    return jsonify(usuario)


@app.route('/usuarios', methods=['POST'])
def add_exam():
    # mount exam object
    posted_usuario = UsuariosSchema(only=('correo', 'nombre', 'apellido1', 'apellido2', 'contrasenna', 'tipo'))\
        .load(request.get_json())

    usuario = Usuarios(**posted_usuario)

    # persist exam
    session = Session()
    session.add(usuario)
    session.commit()

    # return created exam
    new_exam = UsuariosSchema().dump(usuario)
    session.close()
    return jsonify(new_exam), 201
